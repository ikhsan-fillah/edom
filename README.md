# EDOM Dashboard

Aplikasi web otomatis untuk merekap dan memvisualisasikan data **EDOM (Evaluasi Dosen oleh Mahasiswa)** per dosen. Aplikasi ini membaca data mentah dari file Excel/CSV, mengelompokkannya berdasarkan periode penilaian, lalu menghasilkan grafik secara otomatis tanpa perlu membuat chart manual satu per satu.

## Tujuan

Mengotomatiskan proses rekap dan visualisasi hasil EDOM sehingga setiap dosen memiliki laporan grafik yang konsisten, cepat dibuat, dan mudah dibandingkan antar periode (Pra UTS vs Pra UAS).

## Teknologi

- **Python** sebagai bahasa utama, karena workflow olah data -> grafik lebih efisien menggunakan Pandas + Plotly/Matplotlib dibanding pendekatan JavaScript yang membutuhkan proses backend terpisah dan konversi ke JSON.
- **Streamlit** sebagai framework tampilan web untuk output akhir aplikasi.

## Struktur Data Sumber

- File: `EDOM-GENAP-25-26-Sheet1.csv`
- Encoding: `latin1` (bukan UTF-8)
- 1 sheet besar dengan kolom: `Timestamp`, `Nama dosen yang anda nilai`, dan 20 kolom kriteria (skor 1-8)
- Total 446 baris data, seluruhnya berhasil ter-parse tanpa masalah

## Aturan Pemisahan Periode

Periode dibedakan berdasarkan rentang tanggal pada kolom `Timestamp` (bukan kolom eksplisit):

| Periode   | Rentang Tanggal                          |
|-----------|-------------------------------------------|
| Pra UTS   | 08/01/2026 05.29 - 27/04/2026 13.56       |
| Pra UAS   | 08/06/2026 08.14 - 26/06/2026 14.46       |

Seluruh data sudah divalidasi masuk rapi ke salah satu rentang, tidak ada data yang berada di luar rentang tersebut.

## Grafik per Dosen

Setiap dosen memiliki 4 jenis grafik:

1. **Bar chart skor per kriteria** - 20 chart (1 per kriteria), skor 1-8, dikelompokkan Pra UTS | gap | Pra UAS
2. **Line chart jumlah responden** - 1 chart, tren responden Pra UTS vs Pra UAS
3. **Radar chart rata-rata skor Pra UTS** - 1 chart, 20 axis kriteria
4. **Radar chart rata-rata skor Pra UAS** - 1 chart, 20 axis kriteria

Semua grafik tersedia dalam format JPG/PNG dan dapat diunduh langsung dari tampilan Streamlit.

## Struktur Folder

```
edom_dashboard/
├── app.py
├── data/EDOM-GENAP-25-26-Sheet1.csv
├── src/
│   ├── data_loader.py
│   ├── chart_kriteria.py
│   ├── chart_responden.py
│   ├── chart_radar.py
│   └── utils.py
├── output/charts/<nama_dosen>/
├── requirements.txt
└── README.md
```

## Tampilan Web

Dibangun dengan Streamlit menggunakan expander/tab per dosen, mendukung scroll horizontal, dan setiap dosen menampilkan seluruh grafiknya lengkap dengan tombol download PNG/JPG.

## Instalasi

```bash
pip install -r requirements.txt
streamlit run app.py
```
