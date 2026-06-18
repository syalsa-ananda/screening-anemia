"""
Halaman Riwayat — daftar prediksi yang dilakukan dalam sesi browser saat ini.
"""

import pandas as pd
import streamlit as st

from utils.ui import spectrum_divider


def render():
    if "history" not in st.session_state:
        st.session_state.history = []

    st.markdown('<div class="eyebrow" style="color:#8B2942;">Riwayat</div>', unsafe_allow_html=True)
    st.markdown("### Prediksi sesi ini")
    st.caption("Daftar ini hilang saat halaman ditutup atau dimuat ulang.")
    spectrum_divider(thin=True)

    if st.session_state.history:
        hist_df = pd.DataFrame(st.session_state.history)
        hist_df.index = range(1, len(hist_df) + 1)

        total = len(hist_df)
        n_anemia = (hist_df["label"] == "Anemia").sum()
        n_non = total - n_anemia

        col1, col2, col3 = st.columns(3)
        col1.metric("Total", total)
        col2.metric("Anemia", int(n_anemia))
        col3.metric("Non-Anemia", int(n_non))

        st.markdown('<div class="app-card">', unsafe_allow_html=True)
        display_df = hist_df.copy()
        display_df["confidence"] = display_df["confidence"].apply(lambda x: f"{x:.1%}")
        display_df.columns = ["Berkas", "Hasil", "Keyakinan"]
        st.dataframe(display_df, use_container_width=True)

        if st.button("Hapus riwayat"):
            st.session_state.history = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div class="app-card" style="text-align:center; padding:48px 24px;">
                <p style="font-size:1.0rem; color:#6B7280; margin:0;">
                    Belum ada prediksi pada sesi ini.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption("Buka menu Skrining untuk membuat prediksi pertama.")
