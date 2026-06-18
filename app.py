"""
Entry point utama — router navigasi & halaman Beranda.
"""

import streamlit as st

from utils.ui import inject_global_css
from views import skrining, edukasi, riwayat, faq


st.set_page_config(
    page_title="Skrining Anemia Non-Invasif",
    page_icon="🩺",
    layout="wide",
)


def render_beranda():
    st.markdown(
        """
        <div class="hero">
            <h1>🩺 Skrining Anemia Non-Invasif</h1>
            <p>
                Deteksi kemungkinan anemia hanya dari foto konjungtiva mata —
                tanpa jarum, tanpa darah, hasil dalam hitungan detik.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="app-card">
            <span class="badge">NON-INVASIF</span>
            <span class="badge">REAL-TIME</span>
            <span class="badge">BERBASIS AI</span>
            <h3>Apa itu sistem ini?</h3>
            <p>
                Sistem ini melakukan skrining anemia secara non-invasif dengan
                menganalisis citra konjungtiva palpebra — bagian dalam kelopak
                mata bawah yang warnanya berubah pucat ketika kadar hemoglobin
                menurun. Cukup unggah satu foto, sistem akan menganalisis warna
                dan tekstur konjungtiva menggunakan kombinasi fitur
                <b>LBP (Local Binary Pattern)</b>, <b>GLCM</b>, dan
                <b>Color Histogram</b>, lalu mengklasifikasikannya dengan
                model <b>Ensemble Learning</b> (gabungan SVM, Random Forest,
                dan Gradient Boosting).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Bagaimana cara kerjanya?")
    st.markdown(
        """
        <div class="step-row">
            <div class="step-pill"><div class="num">1</div><div class="label">Unggah Foto<br>Konjungtiva</div></div>
            <div class="step-pill"><div class="num">2</div><div class="label">Pra-Pemrosesan<br>(CLAHE)</div></div>
            <div class="step-pill"><div class="num">3</div><div class="label">Ekstraksi Fitur<br>(346 Dimensi)</div></div>
            <div class="step-pill"><div class="num">4</div><div class="label">Klasifikasi<br>Ensemble Learning</div></div>
            <div class="step-pill"><div class="num">5</div><div class="label">Hasil &amp;<br>Probabilitas</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.page_link(skrining_page, label="🔍  Mulai Skrining Sekarang", use_container_width=True)

    st.write("")
    st.markdown(
        """
        <div class="app-card">
            <h3>Mengapa bisa dipercaya?</h3>
            <p>
                Model telah diuji pada 334 data uji independen dari tiga sumber
                populasi berbeda (Ghana, Italia-India, dan dataset Palpebral
                Conjunctiva), mencapai <b>akurasi 92.51%</b> dengan
                <b>sensitivitas 95%</b> dan <b>spesifisitas 90%</b> — melampaui
                standar minimum WHO untuk sistem skrining anemia berbasis
                teknologi.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "⚠️ Sistem ini adalah alat bantu skrining awal untuk tujuan edukasi dan "
        "penelitian, bukan pengganti diagnosis medis profesional. Lihat halaman "
        "FAQ untuk informasi lebih lanjut."
    )


# ── Daftarkan seluruh halaman ──────────────────────────────────────────────
beranda_page = st.Page(render_beranda, title="Beranda", icon="🏠", default=True)
skrining_page = st.Page(skrining.render, title="Skrining", icon="🔍")
edukasi_page = st.Page(edukasi.render, title="Edukasi Anemia", icon="🩸")
riwayat_page = st.Page(riwayat.render, title="Riwayat", icon="📋")
faq_page = st.Page(faq.render, title="FAQ", icon="❓")

pg = st.navigation(
    [beranda_page, skrining_page, edukasi_page, riwayat_page, faq_page],
    position="top",
)

inject_global_css()
pg.run()
