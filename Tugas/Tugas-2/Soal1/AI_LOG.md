# Log Penggunaan AI (AI Usage Log) — Tugas 2 Pengantar Sains Data (Soal 1)

**Informasi Mahasiswa & Tugas:**
- **Nama:** Michael Alexander Newton
- **NIM:** 105224017
- **Mata Kuliah:** Pengantar Sains Data (52305)
- **Topik Tugas:** Tugas 2 Individu — Data Preprocessing (Soal 1: Volume Pengangkutan Sampah di Kali, Sungai, Situ, dan Waduk DKI Jakarta Bulan Januari 2021)
- **Asisten AI yang Digunakan:** Google Antigravity (Gemini)

---

## 1. Tujuan Penggunaan AI
AI digunakan sebagai asisten diskusi (*pair programming* & *proofreading*) dalam pengerjaan Soal 1 untuk:
1. Membantu mendiagnosis kendala teknis saat pembacaan berkas CSV mentah (`UnicodeDecodeError` dan pemisah titik koma `;`).
2. Menyusun kode Python (`pandas`, `numpy`, `matplotlib`, `seaborn`) yang terstruktur untuk tahapan inspeksi data, eksplorasi statistik awal (EDA), pembersihan *noise*, konsistensi kolom, serta imputasi *missing values*.
3. Memvalidasi kesesuaian hasil statistik antara kode pada Jupyter Notebook (`Preprocessing(Soal1).ipynb`), berkas keluaran Excel (`volume_pengangkutan_sampah_preprocessed.xlsx`), dan dokumen laporan akhir.

---

## 2. Riwayat Interaksi & Tahapan Penggunaan AI

| Tahap | Masalah / Kebutuhan yang Ditanyakan ke AI | Solusi & Kontribusi AI | Verifikasi & Tindakan Mahasiswa |
| :---: | :--- | :--- | :--- |
| **1** | Menyusun alur tahapan *preprocessing* data di Jupyter Notebook (`.ipynb`) mulai dari inspeksi variabel, pembersihan *noise* & konsistensi kolom, imputasi *missing values*, hingga ekspor ke Excel. | Memberikan struktur kode per-*cell* sesuai tahapan *Data Understanding* dan *Data Preparation* (CRISP-DM). | Menjalankan kode di notebook lokal dan menyesuaikan path berkas CSV. |
| **2** | Menangani *error* `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb3` saat membaca berkas CSV mentah. | Menjelaskan bahwa *byte* `0xb3` berasal dari karakter pangkat tiga (`³` pada satuan `m³`) dan menyarankan penggunaan parameter `encoding='latin1'` serta `sep=';'`. | Menerapkan parameter tersebut pada `pd.read_csv()` dan memverifikasi seluruh 8 kolom (54.343 baris) terbaca dengan benar. |
| **3** | Melakukan inspeksi *noise* pada seluruh 8 variabel dan identifikasi statistik deskriptif lengkap (EDA awal) sebagai acuan metode imputasi, serta memperbaiki `TypeError` saat pembulatan persentase modus. | Menyusun skrip inspeksi menyeluruh (spasi tersembunyi, *outlier*, *skewness*, kuartil, perbandingan *Mean vs Median* per wilayah) serta menambahkan konversi `.astype(float)` sebelum `.round(2)`. | Menjalankan kode EDA, mengevaluasi visualisasi *boxplot*, dan menggunakan hasilnya sebagai dasar pemilihan *Median* dan *Modus*. |
| **4** | Memastikan keakuratan konsistensi kolom (`panjang/luas` & `satuan_panjang/luas`) serta pengisian *missing values* pada berkas Excel hasil *preprocessing*. | Menyusun logika pemisahan satuan yang menempel (`800m`, `1Ha`), *parsing* format `Panjang/Lebar` (`3500/70`), standarisasi 11 variasi satuan menjadi 5 satuan baku (`m`, `Ha`, `m2`, `m3`, `km`), penyelarasan nilai antar-tanggal per lokasi (kasus `1.36` -> `1360` m di Kec. Kebon Jeruk), serta imputasi *Group Median* dan *fallback* `0` (MNAR). | Mengecek ulang berkas `volume_pengangkutan_sampah_preprocessed.xlsx` hingga dipastikan 0 *missing values* dan konsisten di setiap titik lokasi. |
| **5** | Merapikan struktur penulisan laporan, membuat diagram alur (*flowchart*) langkah pengerjaan, serta mengaudit kesesuaian angka pada laporan PDF. | Membuat kode visualisasi *flowchart* menggunakan `matplotlib` dan mengaudit kesesuaian angka tabel di laporan agar selaras dengan output notebook. | Memperbarui dokumen laporan, memeriksa ulang seluruh tabel dan grafik, serta mengekspor laporan akhir ke PDF. |

---

## 3. Pernyataan Integritas Akademik
Seluruh kode program di dalam `Preprocessing(Soal1).ipynb`, berkas hasil olahan `volume_pengangkutan_sampah_preprocessed.xlsx`, dan analisis di dalam laporan telah dijalankan, diuji, dipahami, serta diverifikasi kebenarannya secara mandiri oleh mahasiswa.