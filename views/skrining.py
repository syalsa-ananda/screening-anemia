"""
Halaman Skrining — upload citra, prediksi, dan visualisasi hasil.

Pipeline validasi dua lapis:
  Lapis 1 — Gemini Vision: pastikan foto adalah konjungtiva mata sebelum
             dikirim ke model ML (menolak foto jalanan, makanan, screenshot, dll.)
  Lapis 2 — Threshold 55%: kalau confidence terlalu rendah bahkan setelah
             lolos Gemini, tampilkan catatan "hasil borderline, coba foto ulang".
"""

import base64
import io
import json
import logging

import cv2
import numpy as np
import pandas as pd
import requests
import streamlit as st
from PIL import Image

from utils.feature_extraction import extract_all_features, load_and_resize, preprocess_image
from utils.model_loader import load_model_and_scaler
from utils.ui import spectrum_divider

logger = logging.getLogger(__name__)

LABELS = {0: "Non-Anemia", 1: "Anemia"}
COLORS = {0: "#5C7A6B", 1: "#8B2942"}
CONFIDENCE_THRESHOLD = 0.55
GEMINI_MODEL = "gemini-1.5-flash"


# ── Gemini validation ─────────────────────────────────────────────────────────

def _get_gemini_key():
    try:
        key = st.secrets["GEMINI_API_KEY"]
        logger.info(f"[Gemini] API key ditemukan di st.secrets, panjang: {len(str(key))}")
        return key
    except Exception as e:
        logger.warning(f"[Gemini] Tidak ada key di st.secrets: {e}")
        return st.session_state.get("gemini_key_input")


def validate_conjunctiva(pil_image):
    api_key = _get_gemini_key()
    if not api_key:
        logger.warning("[Gemini] Tidak ada API key — validasi dilewati")
        return {"valid": True, "reason": "", "skipped": True}

    # Resize ke maksimal 1024px di sisi terpanjang untuk menghindari batas ukuran Gemini
    img_resized = pil_image.convert("RGB")
    max_size = 1024
    if max(img_resized.size) > max_size:
        ratio = max_size / max(img_resized.size)
        new_size = (int(img_resized.width * ratio), int(img_resized.height * ratio))
        img_resized = img_resized.resize(new_size, Image.LANCZOS)
        logger.info(f"[Gemini] Gambar direscale ke {new_size}")

    buf = io.BytesIO()
    img_resized.save(buf, format="JPEG", quality=80)
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    prompt = (
        "Lihat gambar ini dengan seksama. "
        "Apakah gambar ini menunjukkan konjungtiva palpebra manusia — "
        "yaitu bagian dalam kelopak mata bawah yang berwarna merah muda atau merah, "
        "biasanya diambil dengan menarik kelopak mata bawah ke bawah? "
        "Jawab HANYA dengan format JSON berikut tanpa teks lain:\n"
        "{\"is_conjunctiva\": true/false, \"reason\": \"alasan singkat dalam Bahasa Indonesia\"}"
    )

    payload = {
        "contents": [{"parts": [
            {"text": prompt},
            {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}},
        ]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 120},
    }

    try:
        resp = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{GEMINI_MODEL}:generateContent?key={api_key}",
            json=payload,
            timeout=15,
        )
        logger.info(f"[Gemini] Status response: {resp.status_code}")
        resp.raise_for_status()

        raw = resp.json()
        text = raw["candidates"][0]["content"]["parts"][0]["text"].strip()
        logger.info(f"[Gemini] Raw text response: {text}")

        # Bersihkan semua varian markdown code fence
        text = text.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(text)
        result = {
            "valid": bool(parsed.get("is_conjunctiva", False)),
            "reason": parsed.get("reason", ""),
            "skipped": False,
        }
        logger.info(f"[Gemini] Hasil validasi: {result}")
        return result

    except requests.exceptions.Timeout:
        logger.error("[Gemini] Request timeout")
        return {"valid": True, "reason": "Validasi timeout.", "skipped": True}
    except requests.exceptions.HTTPError as e:
        status = resp.status_code if resp else "?"
        body = resp.text[:300] if resp else ""
        logger.error(f"[Gemini] HTTP {status}: {body}")
        st.warning(f"DEBUG — Gemini HTTP {status}: {body[:200]}", icon="🔧")
        return {"valid": True, "reason": f"Gemini HTTP error {status}.", "skipped": True}
    except json.JSONDecodeError as e:
        logger.error(f"[Gemini] JSON parse error: {e}, text: '{text}'")
        st.warning(f"DEBUG — Gemini JSON error. Raw: {text[:200]}", icon="🔧")
        return {"valid": True, "reason": "Gagal parse respons Gemini.", "skipped": True}
    except Exception as e:
        logger.error(f"[Gemini] Unexpected: {type(e).__name__}: {e}")
        st.warning(f"DEBUG — {type(e).__name__}: {e}", icon="🔧")
        return {"valid": True, "reason": "Validasi tidak tersedia.", "skipped": True}


# ── Model prediction ──────────────────────────────────────────────────────────

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


# ── Render ────────────────────────────────────────────────────────────────────

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

    # ── Debug info (hanya tampil di development, tidak di production) ─────
    try:
        key = st.secrets["GEMINI_API_KEY"]
        st.info(f"✅ Gemini API key aktif (panjang: {len(str(key))} karakter)")
    except Exception:
        gemini_key = st.session_state.get("gemini_key_input")
        if not gemini_key:
            with st.expander("⚙️ Aktifkan validasi foto (Gemini API Key)"):
                st.caption(
                    "Masukkan Gemini API key untuk memastikan hanya foto konjungtiva "
                    "yang diproses. Tanpa ini, sistem tetap berjalan tanpa validasi jenis foto."
                )
                key_input = st.text_input(
                    "Gemini API Key", type="password",
                    placeholder="AIzaSy...", key="gemini_key_field",
                )
                if key_input:
                    st.session_state["gemini_key_input"] = key_input
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

        # ── LAPIS 1: Validasi Gemini ──────────────────────────────────────
        with st.spinner("Memvalidasi jenis citra..."):
            validation = validate_conjunctiva(pil_image)

        # Tampilkan hasil validasi untuk debug
        if not validation["skipped"]:
            st.caption(f"🔍 Validasi Gemini: {'✅ Lolos' if validation['valid'] else '❌ Ditolak'} — {validation['reason']}")
        else:
            st.caption(f"⚠️ Validasi Gemini dilewati: {validation['reason'] or 'API key tidak ditemukan'}")

        if not validation["skipped"] and not validation["valid"]:
            st.error(
                "**Foto tidak dikenali sebagai konjungtiva mata.**\n\n"
                f"{validation['reason']}\n\n"
                "Pastikan foto menunjukkan bagian **dalam kelopak mata bawah** "
                "dengan menarik kelopak sedikit ke bawah saat memotret."
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

        # ── Pra-pemrosesan ────────────────────────────────────────────────
        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        st.markdown("##### Penyetaraan kontras")
        col_a, col_b = st.columns(2)
        with col_a:
            st.image(result["img_original"], caption="Sebelum", use_container_width=True)
        with col_b:
            st.image(result["img_clahe"], caption="Setelah CLAHE", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Lapis 2: Borderline warning ───────────────────────────────────
        if is_borderline:
            st.warning(
                f"**Hasil tidak meyakinkan** — tingkat keyakinan model hanya "
                f"{result['confidence']:.1%} (di bawah ambang batas 55%).\n\n"
                "Kemungkinan penyebab: pencahayaan kurang, foto buram, atau "
                "area konjungtiva tidak terlihat jelas. "
                "**Coba foto ulang** dengan cahaya lebih terang."
            )
            st.stop()

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

        # ── Grafik probabilitas ───────────────────────────────────────────
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
