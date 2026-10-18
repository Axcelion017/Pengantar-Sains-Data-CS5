"""
Analisis statistik deskriptif + visualisasi
Dataset: BigDataset_dki_jakarta_2021_2025.xlsx (BPS - DKI Jakarta)

Output:
  - hasil_statistik_deskriptif.csv / .xlsx
  - grafik/<kolom>.png  -> boxplot, histogram, dan kurva distribusi normal (+ skewness)
  - grafik/00_boxplot_semua_variabel.png

Kebutuhan: pandas, numpy, scipy, matplotlib, openpyxl
  pip install pandas numpy scipy matplotlib openpyxl
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# ------------------------------------------------------------------
# 1. KONFIGURASI
# ------------------------------------------------------------------
FILE_PATH = "/Users/michaelalex/Desktop/VS Code/Kuliah/Pengantar Sains Data/Tugas/Tugas-1 /BigDataset_dki_jakarta_2021_2025.xlsx"   # ubah sesuai lokasi file
OUTPUT_DIR = "grafik"
os.makedirs(OUTPUT_DIR, exist_ok=True)

TAMPILKAN_GRAFIK = True   # True = grafik muncul di layar (jendela plot) + disimpan ke file
                          # False = hanya disimpan ke file (mis. di server tanpa layar)

def simpan_tampilkan(fig, nama_file):
    """Simpan grafik ke folder OUTPUT_DIR, lalu tampilkan di layar jika diminta."""
    fig.savefig(os.path.join(OUTPUT_DIR, nama_file), dpi=150)
    if TAMPILKAN_GRAFIK:
        plt.show()
    plt.close(fig)

# Label yang lebih rapi untuk judul grafik
LABEL = {
    "rata_rata_lama_sekolah_tahun":   "Rata-rata Lama Sekolah (tahun)",
    "tpt_laki_laki":                  "TPT Laki-laki (%)",
    "tpt_perempuan":                  "TPT Perempuan (%)",
    "tpt_jumlah":                     "TPT Total (%)",
    "p0_persentase_penduduk_miskin":  "Persentase Penduduk Miskin P0 (%)",
    "p1_indeks_kedalaman_kemiskinan": "Indeks Kedalaman Kemiskinan P1",
}

# ------------------------------------------------------------------
# 2. LOAD & BERSIHKAN DATA
#    Baris di bawah data berisi catatan sumber ("# Sumber: ...") dan
#    baris kosong, jadi harus dibuang.
# ------------------------------------------------------------------
df = pd.read_excel(FILE_PATH)
df = df.dropna(subset=["wilayah"]).copy()          # buang baris catatan/kosong
df["tahun"] = df["tahun"].astype(int)

kolom_numerik = df.select_dtypes(include="number").columns.drop("tahun").tolist()
print(f"Jumlah observasi : {len(df)}")
print(f"Variabel dianalisis: {kolom_numerik}\n")

# ------------------------------------------------------------------
# 3. STATISTIK DESKRIPTIF
# ------------------------------------------------------------------
def ringkasan(x: pd.Series) -> dict:
    x = x.dropna()
    q1, q3 = x.quantile(0.25), x.quantile(0.75)
    modus = x.mode()                                 # bisa lebih dari satu nilai
    return {
        "N": len(x),
        "Mean": x.mean(),
        "Median": x.median(),
        "Modus": ", ".join(f"{m:.2f}" for m in modus.head(3))
                 + (" (multimodal)" if len(modus) > 3 else ""),
        "Minimum": x.min(),
        "Maksimum": x.max(),
        "Range": x.max() - x.min(),
        "Q1": q1,
        "Q3": q3,
        "IQR": q3 - q1,
        "Varians (sampel)": x.var(ddof=1),
        "Std. Deviasi (sampel)": x.std(ddof=1),
        "Std. Deviasi (populasi)": x.std(ddof=0),
        "Skewness": stats.skew(x, bias=False),
        "Kurtosis (excess)": stats.kurtosis(x, bias=False),
    }

hasil = pd.DataFrame({k: ringkasan(df[k]) for k in kolom_numerik})
hasil.columns = [LABEL.get(c, c) for c in hasil.columns]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 20)
print(hasil.to_string(float_format=lambda v: f"{v:.4f}"))

hasil.to_csv("hasil_statistik_deskriptif.csv", encoding="utf-8-sig")
hasil.to_excel("hasil_statistik_deskriptif.xlsx")

# ------------------------------------------------------------------
# 4. INTERPRETASI SKEWNESS
# ------------------------------------------------------------------
def tafsir_skew(s: float) -> str:
    if abs(s) < 0.5:
        return "hampir simetris"
    arah = "positif (miring ke kanan)" if s > 0 else "negatif (miring ke kiri)"
    tingkat = "sedang" if abs(s) < 1 else "kuat"
    return f"miring {tingkat}, {arah}"

# ------------------------------------------------------------------
# 5. GRAFIK PER VARIABEL: Boxplot | Histogram + Normal | Q-Q plot
# ------------------------------------------------------------------
for k in kolom_numerik:
    x = df[k].dropna()
    mu, sd = x.mean(), x.std(ddof=1)
    skew = stats.skew(x, bias=False)
    judul = LABEL.get(k, k)

    fig, ax = plt.subplots(1, 3, figsize=(17, 5))
    fig.suptitle(f"{judul}  |  Skewness = {skew:.3f} ({tafsir_skew(skew)})",
                 fontsize=13, fontweight="bold")

    # (a) Box plot
    ax[0].boxplot(x, patch_artist=True, showmeans=True,
                  boxprops=dict(facecolor="#9ecae1"),
                  medianprops=dict(color="red", lw=2),
                  meanprops=dict(marker="D", markerfacecolor="green",
                                 markeredgecolor="green"))
    ax[0].set_title("Box Plot (◆ = mean, garis merah = median)")
    ax[0].set_ylabel(judul)
    ax[0].set_xticks([])

    # (b) Histogram + kurva distribusi normal
    bins = int(np.ceil(np.log2(len(x)) + 1))        # aturan Sturges
    ax[1].hist(x, bins=bins, density=True, color="#9ecae1",
               edgecolor="white", label="Histogram")
    xs = np.linspace(x.min() - sd, x.max() + sd, 400)
    ax[1].plot(xs, stats.norm.pdf(xs, mu, sd), "r-", lw=2,
               label=f"Kurva normal (μ={mu:.2f}, σ={sd:.2f})")
    ax[1].axvline(mu, color="green", ls="--", label="Mean")
    ax[1].axvline(x.median(), color="orange", ls="--", label="Median")
    ax[1].set_title("Histogram & Distribusi Normal")
    ax[1].set_xlabel(judul)
    ax[1].set_ylabel("Densitas")
    ax[1].legend(fontsize=8)

    # (c) Q-Q plot (cek kenormalan secara visual)
    stats.probplot(x, dist="norm", plot=ax[2])
    ax[2].set_title("Q-Q Plot (uji kenormalan visual)")
    sh_stat, sh_p = stats.shapiro(x)
    ax[2].text(0.05, 0.92, f"Shapiro-Wilk p = {sh_p:.4f}\n"
               f"({'normal' if sh_p > 0.05 else 'tidak normal'} pada α=0.05)",
               transform=ax[2].transAxes, fontsize=9, va="top",
               bbox=dict(boxstyle="round", fc="white", ec="gray"))

    plt.tight_layout()
    simpan_tampilkan(fig, f"{k}.png")

# ------------------------------------------------------------------
# 6. BOX PLOT GABUNGAN (satu panel per variabel, skala berbeda-beda)
# ------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for a, k in zip(axes.ravel(), kolom_numerik):
    a.boxplot(df[k].dropna(), patch_artist=True, showmeans=True,
              boxprops=dict(facecolor="#9ecae1"),
              medianprops=dict(color="red", lw=2))
    a.set_title(LABEL.get(k, k), fontsize=10)
    a.set_xticks([])
fig.suptitle("Box Plot Seluruh Variabel – DKI Jakarta 2021–2025",
             fontsize=14, fontweight="bold")
plt.tight_layout()
simpan_tampilkan(fig, "00_boxplot_semua_variabel.png")

# ------------------------------------------------------------------
# 7. ANALISIS KORELASI: Kemiskinan  x  Pendidikan  x  Pengangguran
#    Kemiskinan   = persentase penduduk miskin (P0) & indeks kedalaman (P1)
#    Pendidikan   = rata-rata lama sekolah
#    Pengangguran = TPT total
# ------------------------------------------------------------------
import seaborn as sns

def kekuatan(r):
    a = abs(r)
    k = ("sangat lemah" if a < 0.2 else "lemah" if a < 0.4 else
         "sedang" if a < 0.6 else "kuat" if a < 0.8 else "sangat kuat")
    return f"{k}, {'positif' if r > 0 else 'negatif'}"

# 7a. Matriks korelasi (Pearson & Spearman) -> heatmap
kor_cols = ["rata_rata_lama_sekolah_tahun", "tpt_jumlah",
            "p0_persentase_penduduk_miskin", "p1_indeks_kedalaman_kemiskinan"]
nama_pendek = {"rata_rata_lama_sekolah_tahun": "Lama Sekolah",
               "tpt_jumlah": "TPT Total",
               "p0_persentase_penduduk_miskin": "Penduduk Miskin (P0)",
               "p1_indeks_kedalaman_kemiskinan": "Kedalaman Miskin (P1)"}

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
for a, metode in zip(axes, ["pearson", "spearman"]):
    m = df[kor_cols].corr(method=metode).rename(index=nama_pendek, columns=nama_pendek)
    sns.heatmap(m, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1,
                square=True, linewidths=.5, ax=a, cbar_kws={"shrink": .8})
    a.set_title(f"Korelasi {metode.capitalize()}")
fig.suptitle("Matriks Korelasi – Pendidikan, Pengangguran, Kemiskinan",
             fontsize=13, fontweight="bold")
plt.tight_layout()
simpan_tampilkan(fig, "10_heatmap_korelasi.png")

# 7b. Uji signifikansi tiap pasangan (r, rho, p-value)
pasangan = [
    ("rata_rata_lama_sekolah_tahun", "p0_persentase_penduduk_miskin"),
    ("rata_rata_lama_sekolah_tahun", "p1_indeks_kedalaman_kemiskinan"),
    ("tpt_jumlah",                   "p0_persentase_penduduk_miskin"),
    ("tpt_jumlah",                   "p1_indeks_kedalaman_kemiskinan"),
    ("rata_rata_lama_sekolah_tahun", "tpt_jumlah"),
]
baris = []
for a_, b_ in pasangan:
    r, p_r = stats.pearsonr(df[a_], df[b_])
    rho, p_s = stats.spearmanr(df[a_], df[b_])
    baris.append({"Variabel X": nama_pendek[a_], "Variabel Y": nama_pendek[b_],
                  "Pearson r": r, "p (Pearson)": p_r,
                  "Spearman rho": rho, "p (Spearman)": p_s,
                  "Kekuatan (Pearson)": kekuatan(r),
                  "Signifikan (α=0.05)": "Ya" if p_r < 0.05 else "Tidak"})
tabel_kor = pd.DataFrame(baris)
print("\n=== HASIL UJI KORELASI ===")
print(tabel_kor.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
tabel_kor.to_csv("hasil_korelasi.csv", index=False, encoding="utf-8-sig")

# 7c. Scatter plot + garis regresi untuk tiap pasangan
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
palet = dict(zip(df["wilayah"].unique(), sns.color_palette("tab10", df["wilayah"].nunique())))
for a, (x_, y_) in zip(axes.ravel(), pasangan):
    sns.scatterplot(data=df, x=x_, y=y_, hue="wilayah", palette=palet, s=70, ax=a, legend=False)
    sns.regplot(data=df, x=x_, y=y_, scatter=False, color="black", ax=a,
                line_kws={"lw": 1.5})
    r, p_r = stats.pearsonr(df[x_], df[y_])
    a.set_xlabel(nama_pendek[x_]); a.set_ylabel(nama_pendek[y_])
    a.set_title(f"r = {r:.2f}, p = {p_r:.4f}\n({kekuatan(r)})", fontsize=10)
# panel ke-6 dipakai sebagai legenda wilayah
leg = axes.ravel()[-1]; leg.axis("off")
for w, c in palet.items():
    leg.scatter([], [], color=c, label=w, s=70)
leg.legend(title="Wilayah", loc="center", fontsize=11)
fig.suptitle("Scatter Plot & Garis Regresi – Kemiskinan, Pendidikan, Pengangguran",
             fontsize=14, fontweight="bold")
plt.tight_layout()
simpan_tampilkan(fig, "11_scatter_korelasi.png")

# 7d. Sensitivitas: korelasi tanpa Kepulauan Seribu (outlier pada P0 & lama sekolah)
df2 = df[df["wilayah"] != "Kepulauan Seribu"]
print("\n=== KORELASI TANPA KEPULAUAN SERIBU (n={}) ===".format(len(df2)))
for a_, b_ in pasangan:
    r, p_r = stats.pearsonr(df2[a_], df2[b_])
    print(f"{nama_pendek[a_]:>14} vs {nama_pendek[b_]:<22} r = {r:+.3f}  p = {p_r:.4f}")

print(f"\nSelesai. Tabel statistik & grafik tersimpan di folder: {os.getcwd()}")