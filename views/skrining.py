"""
Halaman Skrining — upload citra, prediksi, dan visualisasi hasil.
Validasi dua lapis:
  Lapis 1 — OpenAI GPT-4o-mini Vision: validasi apakah foto konjungtiva mata
  Lapis 2 — Threshold 55%: tolak hasil yang terlalu tidak meyakinkan
"""

import base64
import io
import json
import logging

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from utils.feature_extraction import extract_all_features, load_and_resize, preprocess_image
from utils.model_loader import load_model_and_scaler
from utils.ui import spectrum_divider

logger = logging.getLogger(__name__)

LABELS = {0: "Non-Anemia", 1: "Anemia"}
COLORS = {0: "#5C7A6B", 1: "#8B2942"}
CONFIDENCE_THRESHOLD = 0.55
OPENAI_MODEL = "gpt-4o-mini"


def _get_openai_key():
    try:
        key = st.secrets["OPENAI_API_KEY"]
        logger.info(f"[OpenAI] Key ditemukan, panjang: {len(str(key))}")
        return str(key).strip()
    except Exception:
        return st.session_state.get("openai_key_input")


def validate_conjunctiva(pil_image):
    """Validasi foto via OpenAI GPT-4o-mini Vision."""
    api_key = _get_openai_key()
    if not api_key:
        logger.warning("[OpenAI] Tidak ada API key — validasi dilewati")
        return {"valid": True, "reason": "", "skipped": True}

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Resize ke 800px max sebelum encode
        img = pil_image.convert("RGB")
        if max(img.size) > 800:
            ratio = 800 / max(img.size)
            img = img.resize(
                (int(img.width * ratio), int(img.height * ratio)),
                Image.LANCZOS
            )

        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        img_b64 = base64.b64encode(buf.getvalue()).decode()

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Lihat gambar ini dengan seksama. "
                                "Apakah gambar ini menunjukkan konjungtiva palpebra manusia — "
                                "yaitu bagian dalam kelopak mata bawah yang berwarna merah muda "
                                "atau merah, biasanya diambil dengan menarik kelopak mata bawah "
                                "ke bawah? "
                                "Jawab HANYA dengan format JSON berikut tanpa teks lain:\n"
                                "{\"is_conjunctiva\": true/false, "
                                "\"reason\": \"alasan singkat dalam Bahasa Indonesia\"}"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_b64}",
                                "detail": "low",
                            },
                        },
                    ],
                }
            ],
            max_tokens=100,
            temperature=0,
        )

        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        logger.info(f"[OpenAI] Response: {text}")

        parsed = json.loads(text)
        return {
            "valid": bool(parsed.get("is_conjunctiva", False)),
            "reason": parsed.get("reason", ""),
            "skipped": False,
        }

    except json.JSONDecodeError as e:
        logger.error(f"[OpenAI] JSON parse error: {e}, text: '{text}'")
        st.warning(f"🔧 DEBUG: Gagal parse JSON — {text[:200]}", icon="⚠️")
        return {"valid": True, "reason": "Gagal parse respons.", "skipped": True}
    except Exception as e:
        err_msg = f"{type(e).__name__}: {str(e)[:300]}"
        logger.error(f"[OpenAI] Error: {err_msg}")
        st.warning(f"🔧 DEBUG: {err_msg}", icon="⚠️")
        return {"valid": True, "reason": "Validasi tidak tersedia.", "skipped": True}


def pil_to_bgr(pil_image):
    rgb = np.array(pil_image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def run_prediction(img_bgr, model, scaler):
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

    # ── Status API key ────────────────────────────────────────────────────
    try:
        key = st.secrets["OPENAI_API_KEY"]
        st.info(f"✅ OpenAI API key aktif (panjang: {len(str(key))} karakter)")
    except Exception:
        if not st.session_state.get("openai_key_input"):
            with st.expander("⚙️ Aktifkan validasi foto (OpenAI API Key)"):
                st.caption(
                    "Masukkan OpenAI API key untuk memastikan hanya foto "
                    "konjungtiva yang diproses."
                )
                key_input = st.text_input(
                    "OpenAI API Key", type="password",
                    placeholder="sk-...", key="openai_key_field",
                )
                if key_input:
                    st.session_state["openai_key_input"] = key_input
                    st.success("API key aktif untuk sesi ini.")

    # ── Load model ────────────────────────────────────────────────────────
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

        # ── LAPIS 1: Validasi OpenAI Vision ──────────────────────────────
        with st.spinner("Memvalidasi jenis citra..."):
            validation = validate_conjunctiva(pil_image)

        if not validation["skipped"]:
            st.caption(
                f"🔍 Validasi: {'✅ Lolos' if validation['valid'] else '❌ Ditolak'}"
                f" — {validation['reason']}"
            )
        else:
            st.caption(f"⚠️ Validasi dilewati: {validation['reason'] or 'API key tidak ditemukan'}")

        if not validation["skipped"] and not validation["valid"]:
            st.error(
                "**Foto tidak dikenali sebagai konjungtiva mata.**\n\n"
                f"{validation['reason']}\n\n"
                "Pastikan foto menunjukkan bagian dalam kelopak mata bawah — "
                "tarik kelopak sedikit ke bawah saat memotret."
            )
            st.image(pil_image, caption="Foto yang diunggah", width=320)
            st.stop()

        # ── LAPIS 2: Prediksi model ───────────────────────────────────────
        with st.spinner("Menganalisis citra..."):
            result = run_prediction(img_bgr, model, scaler)

        is_borderline = result["confidence"] < CONFIDENCE_THRESHOLD

        if not is_borderline:
            st.session_state.history.append({
                "nama_file": uploaded_file.name,
                "label": result["label"],
                "confidence": result["confidence"],
            })

        # Pra-pemrosesan
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("##### Penyetaraan kontras")
        col_a, col_b = st.columns(2)
        with col_a:
            st.image(result["img_original"], caption="Sebelum", use_container_width=True)
        with col_b:
            st.image(result["img_clahe"], caption="Setelah CLAHE", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if is_borderline:
            st.warning(
                f"**Hasil tidak meyakinkan** — keyakinan hanya {result['confidence']:.1%} "
                f"(di bawah 55%). Coba foto ulang dengan cahaya lebih terang."
            )
            st.stop()

        # Hasil prediksi
        pred_color = COLORS[result["kode"]]
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("##### Hasil")
        col_pred, col_conf = st.columns(2)
        with col_pred:
            st.markdown(
                f"<h2 style='color:{pred_color}; font-style:italic; margin:0;'>"
                f"{result['label']}</h2>",
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

        # Grafik probabilitas
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("##### Distribusi probabilitas")
        proba_df = pd.DataFrame({
            "Kelas": ["Non-Anemia", "Anemia"],
            "Probabilitas": [result["proba_non_anemia"], result["proba_anemia"]],
        }).set_index("Kelas")
        st.bar_chart(proba_df, color=["#8B2942"], height=260)

        col_p1, col_p2 = st.columns(2)
        col_p1.metric("Non-Anemia", f"{result['proba_non_anemia']:.1%}")
        col_p2.metric("Anemia", f"{result['proba_anemia']:.1%}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.caption("Lihat seluruh riwayat prediksi sesi ini di menu Riwayat.")
