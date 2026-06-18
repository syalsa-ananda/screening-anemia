"""
Halaman Edukasi Anemia — informasi kesehatan umum tentang anemia.
"""

import streamlit as st


def render():
    st.markdown(
        """
        <div class="hero" style="background: linear-gradient(135deg, #DD8452 0%, #B25C2E 100%);">
            <h1>🩸 Mengenal Anemia</h1>
            <p>Apa itu anemia, mengapa terjadi, dan bagaimana mencegahnya.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="app-card">
            <h3>Apa itu Anemia?</h3>
            <p>
                Anemia adalah kondisi ketika tubuh tidak memiliki cukup sel
                darah merah sehat, atau kadar hemoglobin dalam darah berada di
                bawah batas normal. Hemoglobin adalah protein dalam sel darah
                merah yang bertugas mengangkut oksigen ke seluruh jaringan
                tubuh. Ketika kadarnya rendah, tubuh kekurangan oksigen yang
                cukup untuk berfungsi secara optimal.
            </p>
            <p style="margin-bottom:0;">
                Menurut WHO, seseorang dikategorikan anemia jika kadar
                hemoglobin berada di bawah <b>13 g/dL untuk laki-laki dewasa</b>
                dan di bawah <b>12 g/dL untuk perempuan dewasa</b>.
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
                <h3>🔎 Gejala Umum</h3>
                <ul>
                    <li>Mudah lelah dan lemas</li>
                    <li>Kulit dan konjungtiva (bagian dalam kelopak mata) pucat</li>
                    <li>Sering pusing atau sakit kepala</li>
                    <li>Jantung berdebar atau sesak napas saat beraktivitas</li>
                    <li>Tangan dan kaki terasa dingin</li>
                    <li>Sulit berkonsentrasi</li>
                    <li>Kulit, kuku, atau rambut menjadi rapuh</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="app-card" style="height:100%;">
                <h3>🧬 Penyebab Umum</h3>
                <ul>
                    <li>Kekurangan zat besi (jenis paling umum)</li>
                    <li>Kekurangan vitamin B12 atau folat</li>
                    <li>Kehilangan darah (menstruasi berat, luka, pendarahan internal)</li>
                    <li>Penyakit kronis (ginjal, kanker, infeksi jangka panjang)</li>
                    <li>Kelainan genetik (misalnya thalasemia)</li>
                    <li>Kehamilan (kebutuhan zat besi meningkat)</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="app-card">
            <h3>🛡️ Cara Pencegahan</h3>
            <p>Beberapa langkah yang dapat membantu mencegah anemia akibat kekurangan zat besi:</p>
            <ul>
                <li>Konsumsi makanan tinggi zat besi: daging merah, hati, bayam, kacang-kacangan</li>
                <li>Konsumsi makanan tinggi vitamin C bersamaan untuk membantu penyerapan zat besi</li>
                <li>Konsumsi sumber vitamin B12: telur, susu, ikan, daging</li>
                <li>Pemeriksaan rutin terutama untuk ibu hamil dan wanita usia reproduktif</li>
                <li>Konsultasi dengan tenaga medis untuk suplementasi zat besi bila diperlukan</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="app-card">
            <h3>📌 Fakta Singkat</h3>
            <div class="step-row">
                <div class="step-pill"><div class="label" style="font-size:1.3rem;">1.92 Miliar</div><div class="label">orang terdampak anemia secara global</div></div>
                <div class="step-pill"><div class="label" style="font-size:1.3rem;">24.3%</div><div class="label">prevalensi anemia di seluruh populasi dunia</div></div>
                <div class="step-pill"><div class="label" style="font-size:1.3rem;">↑</div><div class="label">paling banyak menyerang ibu hamil &amp; anak balita</div></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("🔍 Buka menu **Skrining** di navbar atas untuk mencoba deteksi sekarang.")
