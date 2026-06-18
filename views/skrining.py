"""
Halaman Skrining — upload citra, prediksi, dan visualisasi hasil.
"""

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from utils.feature_extraction import extract_all_features, load_and_resize, preprocess_image
from utils.model_loader import load_model_and_scaler
from utils.ui import spectrum_divider


LABELS = {0: "Non-Anemia", 1: "Anemia"}
COLORS = {0: "#5C7A6B", 1: "#8B2942"}


def pil_to_bgr(pil_image: Image.Image) -> np.ndarray:
    rgb = np.array(pil_image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def run_prediction(img_bgr: np.ndarray, model, scaler):
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


def render():
    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown('<div class="eyebrow" style="color:#8B2942;">Skrining</div>', unsafe_allow_html=True)
    st.markdown("### Unggah satu foto konjungtiva")
    st.caption(
        "Bagian dalam kelopak mata bawah — tarik kelopak sedikit ke bawah "
        "saat memotret agar area konjungtiva terlihat jelas."
    )
    spectrum_divider(thin=True)

    try:
        model, scaler = load_model_and_scaler()
        model_ready = True
    except FileNotFoundError as e:
        model_ready = False
        st.error(str(e))

    uploaded_file = st.file_uploader(
        "Pilih atau seret foto",
        type=["jpg", "jpeg", "png"],
        disabled=not model_ready,
    )

    if uploaded_file is not None and model_ready:
        pil_image = Image.open(uploaded_file)
        img_bgr = pil_to_bgr(pil_image)

        with st.spinner("Menganalisis citra..."):
            result = run_prediction(img_bgr, model, scaler)

        st.session_state.history.append(
            {
                "nama_file": uploaded_file.name,
                "label": result["label"],
                "confidence": result["confidence"],
            }
        )

        # ── Pra-pemrosesan ────────────────────────────────────────────────
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("##### Penyetaraan kontras")
        col_a, col_b = st.columns(2)
        with col_a:
            st.image(result["img_original"], caption="Sebelum", use_container_width=True)
        with col_b:
            st.image(result["img_clahe"], caption="Setelah CLAHE", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Hasil prediksi ────────────────────────────────────────────────
        pred_color = COLORS[result["kode"]]
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("##### Hasil")
        col_pred, col_conf = st.columns(2)
        with col_pred:
            st.markdown(
                f"<h2 style='color:{pred_color}; font-style:italic; margin:0;'>{result['label']}</h2>",
                unsafe_allow_html=True,
            )
        with col_conf:
            st.metric("Tingkat keyakinan", f"{result['confidence']:.1%}")

        if result["kode"] == 1:
            st.warning(
                "Indikasi anemia terdeteksi. Pemeriksaan laboratorium "
                "disarankan untuk konfirmasi kadar hemoglobin."
            )
        else:
            st.success("Tidak ada indikasi anemia pada foto ini.")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Grafik probabilitas ─────────────────────────────────────────────
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("##### Distribusi probabilitas")
        proba_df = pd.DataFrame(
            {
                "Kelas": ["Non-Anemia", "Anemia"],
                "Probabilitas": [result["proba_non_anemia"], result["proba_anemia"]],
            }
        ).set_index("Kelas")
        st.bar_chart(proba_df, color=["#8B2942"], height=260)

        col_p1, col_p2 = st.columns(2)
        col_p1.metric("Non-Anemia", f"{result['proba_non_anemia']:.1%}")
        col_p2.metric("Anemia", f"{result['proba_anemia']:.1%}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.caption("Lihat seluruh riwayat prediksi sesi ini di menu Riwayat.")
