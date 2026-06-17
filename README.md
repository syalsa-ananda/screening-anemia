# Skrining Anemia Non-Invasif — Aplikasi Streamlit

Aplikasi web untuk skrining anemia non-invasif berbasis citra konjungtiva, menggunakan fitur LBP, GLCM, dan Color Histogram dengan klasifikasi Ensemble Learning (SVM + Random Forest + Gradient Boosting).

## Struktur Folder

```
streamlit_app/
├── app.py                      # Aplikasi utama Streamlit
├── requirements.txt            # Daftar dependency Python
├── .streamlit/
│   └── config.toml             # Konfigurasi tema aplikasi
├── models/
│   ├── README.md               # Instruksi mengisi folder ini
│   ├── ensemble_final.pkl      # (Anda upload sendiri) Model Ensemble
│   └── scaler_final.pkl        # (Anda upload sendiri) StandardScaler
├── utils/
│   ├── __init__.py
│   ├── feature_extraction.py   # Pipeline ekstraksi fitur 346 dimensi
│   └── model_loader.py         # Loader model dengan caching
└── assets/                     # (opsional) gambar contoh, logo, dll.
```

## Fitur Aplikasi

1. **Upload citra konjungtiva** dalam format JPG, JPEG, atau PNG.
2. **Preview pra-pemrosesan** — menampilkan citra asli berdampingan dengan citra setelah CLAHE.
3. **Hasil prediksi** — label Anemia/Non-Anemia beserta tingkat kepercayaan (confidence).
4. **Grafik probabilitas** — bar chart distribusi probabilitas kedua kelas.
5. **Riwayat prediksi** — tabel berisi seluruh prediksi yang dilakukan dalam sesi browser saat ini (akan hilang jika halaman di-refresh atau ditutup).

## Langkah Persiapan Sebelum Deploy

### 1. Lengkapi folder `models/`

Unduh `ensemble_final.pkl` dan `scaler_final.pkl` dari Google Drive Anda (folder `Data_Anemia/saved_model_final/`), lalu salin ke folder `models/` di project ini. Lihat `models/README.md` untuk detail.

### 2. Uji secara lokal (opsional, disarankan)

```bash
cd streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

Aplikasi akan terbuka di browser pada alamat `http://localhost:8501`.

### 3. Push ke GitHub

```bash
git init
git add .
git commit -m "Aplikasi skrining anemia non-invasif"
git remote add origin https://github.com/syalsa-ananda/<nama-repo-baru>.git
git push -u origin main
```

> Catatan: pastikan file `.pkl` di folder `models/` ikut ter-commit. Karena ukurannya kecil (di bawah 25MB), GitHub akan menerimanya tanpa perlu Git LFS.

### 4. Deploy ke Streamlit Community Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io) dan login dengan akun GitHub.
2. Klik **New app**, pilih repository yang baru saja di-push.
3. Pastikan **Main file path** diisi `app.py`.
4. Klik **Deploy**.

Streamlit Cloud akan otomatis membaca `requirements.txt` dan `.streamlit/config.toml` untuk menyiapkan environment yang sesuai.

## Konsistensi Pipeline Fitur

File `utils/feature_extraction.py` berisi fungsi-fungsi yang **harus identik** dengan pipeline ekstraksi fitur di notebook training (`skrining_anemia_FINAL.ipynb`, Sel 5). Jika Anda melatih ulang model dengan parameter berbeda (misalnya jumlah bin histogram atau parameter LBP), pastikan untuk memperbarui konstanta di file ini juga, agar urutan dan dimensi fitur saat inferensi tetap konsisten dengan saat training.

## Disclaimer

Aplikasi ini adalah alat bantu skrining awal untuk tujuan penelitian/akademik, bukan pengganti diagnosis medis profesional. Hasil prediksi sebaiknya dikonfirmasi dengan pemeriksaan laboratorium oleh tenaga medis.
