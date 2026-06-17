"""
Modul untuk memuat model Ensemble dan scaler yang telah dilatih.
Menggunakan st.cache_resource agar model hanya dimuat sekali per sesi server.
"""

import os
import joblib
import streamlit as st

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "ensemble_final.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler_final.pkl")


@st.cache_resource(show_spinner=False)
def load_model():
    """Memuat model Ensemble Learning (SVM + Random Forest + Gradient Boosting)."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model tidak ditemukan di {MODEL_PATH}. "
            "Pastikan file ensemble_final.pkl sudah diunggah ke folder models/."
        )
    return joblib.load(MODEL_PATH)


@st.cache_resource(show_spinner=False)
def load_scaler():
    """Memuat StandardScaler yang di-fit pada data latih."""
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(
            f"Scaler tidak ditemukan di {SCALER_PATH}. "
            "Pastikan file scaler_final.pkl sudah diunggah ke folder models/."
        )
    return joblib.load(SCALER_PATH)


def load_model_and_scaler():
    """Helper untuk memuat keduanya sekaligus."""
    model = load_model()
    scaler = load_scaler()
    return model, scaler
