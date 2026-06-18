# Skrining Anemia Non-Invasif — Aplikasi Streamlit

Aplikasi web untuk skrining anemia non-invasif berbasis citra konjungtiva, menggunakan fitur LBP, GLCM, dan Color Histogram dengan klasifikasi Ensemble Learning (SVM + Random Forest + Gradient Boosting).

## Struktur Folder

```
streamlit_app/
├── app.py                          # Entry point + router (st.navigation)
├── views/
│   ├── __init__.py
│   ├── skrining.py                  # Upload, prediksi, hasil
│   ├── edukasi.py                   # Edukasi kesehatan tentang anemia
│   ├── riwayat.py                   # Riwayat prediksi sesi
│   └── faq.py                       # FAQ + disclaimer + info dataset/performa
├── requirements.txt                # Daftar dependency Python
├── packages.txt                    # Dependency sistem (libgl1 untuk OpenCV)
├── .streamlit/
│   └── config.toml                 # Konfigurasi tema aplikasi
├── models/
│   ├── README.md                   # Instruksi mengisi folder ini
│   ├── ensemble_final.pkl          # (Anda upload sendiri) Model Ensemble
│   └── scaler_final.pkl            # (Anda upload sendiri) StandardScaler
├── utils/
│   ├── __init__.py
│   ├── ui.py                        # CSS global, tema kartu & hero
│   ├── feature_extraction.py       # Pipeline ekstraksi fitur 346 dimensi
│   └── model_loader.py             # Loader model dengan caching
└── assets/                         # (opsional) gambar contoh, logo, dll.
```

## Halaman Aplikasi

1. **🏠 Beranda** — pengantar sistem, alur kerja visual, tombol mulai skrining.
2. **🔍 Skrining** — upload citra, preview CLAHE, hasil prediksi, grafik probabilitas.
3. **🩸 Edukasi Anemia** — gejala, penyebab, dan pencegahan anemia secara umum.
4. **📋 Riwayat** — daftar prediksi yang dilakukan dalam sesi browser saat ini.
5. **❓ FAQ** — pertanyaan umum, disclaimer medis, dan info dataset/metodologi.

Navigasi antar halaman menggunakan `st.navigation()` resmi dari Streamlit (membutuhkan Streamlit ≥1.36), ditampilkan sebagai tab horizontal di bagian atas.

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
