# Folder Models

Letakkan dua file berikut di folder ini sebelum menjalankan aplikasi:

1. **`ensemble_final.pkl`** — model Ensemble Learning (SVM + Random Forest + Gradient Boosting) hasil Sel 20 pada notebook `skrining_anemia_FINAL.ipynb`.
2. **`scaler_final.pkl`** — StandardScaler yang sudah di-fit, juga dari Sel 20.

## Cara mendapatkan kedua file ini

Kedua file sudah otomatis tersimpan di Google Drive Anda setelah menjalankan Sel 20 pada notebook, di lokasi:

```
MyDrive/Data_Anemia/saved_model_final/ensemble_final.pkl
MyDrive/Data_Anemia/saved_model_final/scaler_final.pkl
```

Unduh kedua file tersebut dari Google Drive, lalu salin ke folder `models/` ini sebelum melakukan deploy ke Streamlit Cloud atau menjalankan aplikasi secara lokal.

## Catatan ukuran file

Karena ukuran kedua file ini kecil (di bawah 25MB), keduanya bisa langsung di-commit ke repository GitHub tanpa memerlukan Git LFS atau penyimpanan cloud tambahan.
