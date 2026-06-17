"""
Aplikasi Streamlit — Skrining Anemia Non-Invasif Berbasis Citra Konjungtiva
Menggunakan LBP, GLCM, Color Histogram, dan Ensemble Learning

Cara menjalankan secara lokal:
    streamlit run app.py
"""

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from utils.feature_extraction import extract_all_features, load_and_resize, preprocess_image
from utils.model_loader import load_model_and_scaler


# ── Konfigurasi halaman ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Skrining Anemia Non-Invasif",
    page_icon="🩺",
    layout="wide",
)

LABELS = {0: "Non-Anemia", 1: "Anemia"}
COLORS = {0: "#4C72B0", 1: "#DD8452"}


# ── State untuk riwayat prediksi dalam sesi ──────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []


def pil_to_bgr(pil_image: Image.Image) -> np.ndarray:
    """Konversi gambar PIL (RGB) ke array OpenCV (BGR)."""
    rgb = np.array(pil_image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def run_prediction(img_bgr: np.ndarray, model, scaler):
    """
    Jalankan pipeline lengkap: ekstraksi fitur -> scaling -> prediksi.
    Mengembalikan dict berisi label, confidence, probabilitas, dan citra CLAHE.
    """
    features = extract_all_features(img_bgr).reshape(1, -1)
    features_scaled = scaler.transform(features)

    pred = int(model.predict(features_scaled)[0])
    proba = model.predict_proba(features_scaled)[0]

    img_resized = load_and_resize(img_bgr)
    img_clahe = preprocess_image(img_resized)

    return {
        "label": LABELS[pred],
        "kode": pred,
        "confidence": float(proba[pred]),
        "proba_non_anemia": float(proba[0]),
        "proba_anemia": float(proba[1]),
        "img_original": cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB),
        "img_clahe": cv2.cvtColor(img_clahe, cv2.COLOR_BGR2RGB),
    }


# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Tentang Sistem")
    st.markdown(
        """
        Sistem ini melakukan skrining anemia non-invasif dari citra
        konjungtiva palpebra menggunakan kombinasi fitur **LBP**, **GLCM**,
        dan **Color Histogram**, diklasifikasikan dengan **Ensemble
        Learning** (SVM + Random Forest + Gradient Boosting).
        """
    )
    st.divider()
    st.subheader("Performa Model")
    col1, col2 = st.columns(2)
    col1.metric("Akurasi Eksternal", "92.51%")
    col2.metric("Akurasi Internal", "86.12%")
    col1.metric("Sensitivitas", "95%")
    col2.metric("Spesifisitas", "90%")
    st.divider()
    st.caption(
        "⚠️ Sistem ini adalah alat bantu skrining awal, bukan pengganti "
        "diagnosis medis profesional. Hasil prediksi sebaiknya "
        "dikonfirmasi dengan pemeriksaan laboratorium."
    )

    if st.session_state.history:
        st.divider()
        if st.button("🗑️ Hapus Riwayat", use_container_width=True):
            st.session_state.history = []
            st.rerun()


# ── Header ───────────────────────────────────────────────────────────────
st.title("🩺 Skrining Anemia Non-Invasif")
st.markdown(
    "Unggah foto konjungtiva (bagian dalam kelopak mata bawah) untuk "
    "mendapatkan prediksi kemungkinan anemia secara *real-time*."
)
st.divider()

# ── Load model (cached) ─────────────────────────────────────────────────
try:
    model, scaler = load_model_and_scaler()
    model_ready = True
except FileNotFoundError as e:
    model_ready = False
    st.error(str(e))

# ── Upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Pilih atau seret foto konjungtiva",
    type=["jpg", "jpeg", "png"],
    disabled=not model_ready,
)

if uploaded_file is not None and model_ready:
    pil_image = Image.open(uploaded_file)
    img_bgr = pil_to_bgr(pil_image)

    with st.spinner("Menganalisis citra..."):
        result = run_prediction(img_bgr, model, scaler)

    # Simpan ke riwayat sesi
    st.session_state.history.append(
        {
            "nama_file": uploaded_file.name,
            "label": result["label"],
            "confidence": result["confidence"],
        }
    )

    st.divider()

    # ── Baris 1: Citra sebelum vs sesudah CLAHE ──────────────────────────
    st.subheader("Pra-Pemrosesan Citra")
    col_a, col_b = st.columns(2)
    with col_a:
        st.image(result["img_original"], caption="Citra Asli (setelah resize)", use_container_width=True)
    with col_b:
        st.image(result["img_clahe"], caption="Setelah CLAHE", use_container_width=True)

    st.divider()

    # ── Baris 2: Hasil prediksi + confidence ─────────────────────────────
    st.subheader("Hasil Prediksi")
    pred_color = COLORS[result["kode"]]
    col_pred, col_conf = st.columns(2)
    with col_pred:
        st.markdown(
            f"<h2 style='color:{pred_color};'>● {result['label']}</h2>",
            unsafe_allow_html=True,
        )
    with col_conf:
        st.metric("Tingkat Kepercayaan", f"{result['confidence']:.1%}")

    if result["kode"] == 1:
        st.warning(
            "Hasil menunjukkan indikasi anemia. Disarankan melakukan "
            "pemeriksaan laboratorium untuk konfirmasi kadar hemoglobin."
        )
    else:
        st.success(
            "Hasil menunjukkan tidak ada indikasi anemia. Tetap jaga "
            "pola makan dan kesehatan secara umum."
        )

    st.divider()

    # ── Baris 3: Grafik probabilitas ──────────────────────────────────────
    st.subheader("Distribusi Probabilitas")
    proba_df = pd.DataFrame(
        {
            "Kelas": ["Non-Anemia", "Anemia"],
            "Probabilitas": [result["proba_non_anemia"], result["proba_anemia"]],
        }
    ).set_index("Kelas")
    st.bar_chart(proba_df, color=["#4C72B0"], height=280)

    col_p1, col_p2 = st.columns(2)
    col_p1.metric("P(Non-Anemia)", f"{result['proba_non_anemia']:.1%}")
    col_p2.metric("P(Anemia)", f"{result['proba_anemia']:.1%}")

# ── Riwayat prediksi dalam sesi ──────────────────────────────────────────
st.divider()
st.subheader("📋 Riwayat Prediksi (Sesi Ini)")

if st.session_state.history:
    hist_df = pd.DataFrame(st.session_state.history)
    hist_df.index = range(1, len(hist_df) + 1)
    hist_df["confidence"] = hist_df["confidence"].apply(lambda x: f"{x:.1%}")
    hist_df.columns = ["Nama Berkas", "Hasil Prediksi", "Kepercayaan"]
    st.dataframe(hist_df, use_container_width=True)
else:
    st.caption("Belum ada prediksi yang dilakukan pada sesi ini.")
