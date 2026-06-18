"""
Halaman Edukasi Anemia — informasi kesehatan umum tentang anemia.
"""

import streamlit as st

from utils.ui import spectrum_divider


def render():
    st.markdown('<div class="eyebrow" style="color:#8B2942;">Edukasi</div>', unsafe_allow_html=True)
    st.markdown("### Mengenal anemia")
    st.caption("Apa itu, mengapa terjadi, dan bagaimana mencegahnya.")
    spectrum_divider(thin=True)

    st.markdown(
        """
        <div class="app-card">
            <p>
                Anemia terjadi ketika tubuh tidak memiliki cukup sel darah
                merah sehat, atau kadar hemoglobin berada di bawah batas
                normal. Hemoglobin mengangkut oksigen ke seluruh jaringan
                tubuh — saat kadarnya rendah, tubuh kekurangan oksigen yang
                cukup untuk berfungsi optimal.
            </p>
            <p style="margin-bottom:0;">
                Menurut WHO, seseorang dikategorikan anemia jika kadar
                hemoglobin di bawah <b>13 g/dL untuk laki-laki dewasa</b> dan
                di bawah <b>12 g/dL untuk perempuan dewasa</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="app-card" style="height:100%;">
                <h3 style="font-size:1.1rem;">Gejala umum</h3>
                <ul>
                    <li>Mudah lelah dan lemas</li>
                    <li>Kulit dan konjungtiva pucat</li>
                    <li>Sering pusing atau sakit kepala</li>
                    <li>Jantung berdebar, sesak saat beraktivitas</li>
                    <li>Tangan dan kaki dingin</li>
                    <li>Sulit berkonsentrasi</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="app-card" style="height:100%;">
                <h3 style="font-size:1.1rem;">Penyebab umum</h3>
                <ul>
                    <li>Kekurangan zat besi — paling umum</li>
                    <li>Kekurangan vitamin B12 atau folat</li>
                    <li>Kehilangan darah (menstruasi, luka, internal)</li>
                    <li>Penyakit kronis (ginjal, kanker, infeksi panjang)</li>
                    <li>Kelainan genetik, misalnya thalasemia</li>
                    <li>Kehamilan — kebutuhan zat besi meningkat</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="app-card">
            <h3 style="font-size:1.1rem;">Pencegahan</h3>
            <ul>
                <li>Konsumsi makanan tinggi zat besi: daging merah, hati, bayam, kacang-kacangan</li>
                <li>Padukan dengan vitamin C untuk membantu penyerapan zat besi</li>
                <li>Konsumsi sumber vitamin B12: telur, susu, ikan, daging</li>
                <li>Pemeriksaan rutin, terutama untuk ibu hamil dan wanita usia reproduktif</li>
                <li>Konsultasikan suplementasi zat besi dengan tenaga medis bila diperlukan</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    spectrum_divider(thin=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Terdampak global", "1,92 miliar")
    col2.metric("Prevalensi dunia", "24,3%")
    col3.metric("Kelompok rentan", "Ibu hamil & balita")

    st.caption("Ingin memeriksa kondisi Anda? Buka menu Skrining.")
