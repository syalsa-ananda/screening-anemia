"""
Halaman Riwayat — daftar prediksi yang dilakukan dalam sesi browser saat ini.
"""

import pandas as pd
import streamlit as st

from utils.ui import inject_global_css, render_navbar


st.set_page_config(
    page_title="Riwayat — Skrining Anemia",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()
render_navbar("📋 Riwayat")

if "history" not in st.session_state:
    st.session_state.history = []

st.markdown(
    """
    <div class="app-card">
        <h3>📋 Riwayat Prediksi (Sesi Ini)</h3>
        <p style="margin-bottom:0;">
            Daftar berikut hanya menyimpan prediksi selama sesi browser ini
            berlangsung. Riwayat akan hilang jika halaman ditutup atau
            dimuat ulang.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.history:
    hist_df = pd.DataFrame(st.session_state.history)
    hist_df.index = range(1, len(hist_df) + 1)

    total = len(hist_df)
    n_anemia = (hist_df["label"] == "Anemia").sum()
    n_non = total - n_anemia

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Prediksi", total)
    col2.metric("Anemia", int(n_anemia))
    col3.metric("Non-Anemia", int(n_non))

    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    display_df = hist_df.copy()
    display_df["confidence"] = display_df["confidence"].apply(lambda x: f"{x:.1%}")
    display_df.columns = ["Nama Berkas", "Hasil Prediksi", "Kepercayaan"]
    st.dataframe(display_df, use_container_width=True)

    if st.button("🗑️ Hapus Semua Riwayat"):
        st.session_state.history = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div class="app-card" style="text-align:center; padding:48px 24px;">
            <p style="font-size:1.05rem; color:#6B7280;">
                Belum ada prediksi yang dilakukan pada sesi ini.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.page_link(
            "pages/1_Skrining.py",
            label="🔍  Mulai Skrining Pertama",
            use_container_width=True,
        )
