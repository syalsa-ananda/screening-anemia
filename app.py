"""
Entry point utama — router navigasi & halaman Beranda.
"""

import streamlit as st

from utils.ui import inject_global_css, render_sidebar_brand, spectrum_divider
from views import skrining, edukasi, riwayat, faq


st.set_page_config(
    page_title="Skrining Anemia Non-Invasif",
    page_icon="🩸",
    layout="wide",
)


def render_beranda():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Skrining non-invasif</div>
            <h1>Warna mata Anda<br>sudah bicara banyak.</h1>
            <p>
                Konjungtiva — bagian dalam kelopak mata bawah — berubah pucat
                saat hemoglobin menurun. Satu foto cukup untuk membaca sinyal itu,
                tanpa jarum dan tanpa menunggu hasil laboratorium.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="app-card">
            <span class="badge">Non-invasif</span>
            <span class="badge">Real-time</span>
            <span class="badge">Ensemble Learning</span>
            <h3>Bagaimana ini bekerja</h3>
            <p>
                Setiap foto diproses menjadi 346 ukuran tekstur dan warna —
                kombinasi <b>Local Binary Pattern</b>, <b>Gray-Level
                Co-occurrence Matrix</b>, dan <b>histogram warna</b> lintas tiga
                ruang warna. Tiga model berbeda — Support Vector Machine,
                Random Forest, dan Gradient Boosting — lalu memberi suara
                bersama untuk satu keputusan akhir.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    spectrum_divider(thin=True)
    st.markdown("### Lima langkah, satu hasil")
    st.markdown(
        """
        <div class="step-row">
            <div class="step-pill"><span class="num">01</span><div class="label">Unggah foto konjungtiva</div></div>
            <div class="step-pill"><span class="num">02</span><div class="label">Penyetaraan kontras (CLAHE)</div></div>
            <div class="step-pill"><span class="num">03</span><div class="label">346 ukuran tekstur &amp; warna</div></div>
            <div class="step-pill"><span class="num">04</span><div class="label">Tiga model memberi suara</div></div>
            <div class="step-pill"><span class="num">05</span><div class="label">Hasil dan tingkat keyakinan</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.page_link(skrining_page, label="Mulai skrining", use_container_width=True)

    st.write("")
    st.markdown(
        f"""
        <div class="app-card">
            <h3>Diuji di luar data latih</h3>
            <p>
                Pada 334 foto yang belum pernah dilihat model, sistem mencapai
                <b>akurasi 92,5%</b> — sensitivitas 95%, spesifisitas 90%.
                Diuji lintas tiga populasi berbeda: Ghana, Italia–India, dan
                kumpulan data Palpebral Conjunctiva.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "Alat bantu skrining awal untuk tujuan edukasi dan penelitian — "
        "bukan pengganti diagnosis medis. Selengkapnya di halaman FAQ."
    )


# ── Daftarkan seluruh halaman ──────────────────────────────────────────────
beranda_page = st.Page(render_beranda, title="Beranda", url_path="beranda", default=True)
skrining_page = st.Page(skrining.render, title="Skrining", url_path="skrining")
edukasi_page = st.Page(edukasi.render, title="Edukasi Anemia", url_path="edukasi")
riwayat_page = st.Page(riwayat.render, title="Riwayat", url_path="riwayat")
faq_page = st.Page(faq.render, title="FAQ", url_path="faq")

inject_global_css()
render_sidebar_brand()

pg = st.navigation(
    [beranda_page, skrining_page, edukasi_page, riwayat_page, faq_page],
    position="sidebar",
)

pg.run()
