"""
Halaman FAQ — pertanyaan umum seputar penggunaan aplikasi.
"""

import streamlit as st


FAQS = [
    (
        "Apakah hasil prediksi ini akurat?",
        """
        Model telah diuji pada 334 data uji independen (data yang tidak
        pernah dilihat selama pelatihan) yang berasal dari gabungan tiga
        sumber dataset berbeda populasi. Hasilnya mencapai
        <b>akurasi 92.51%</b>, dengan <b>sensitivitas 95%</b>
        (kemampuan mendeteksi kasus anemia yang sebenarnya) dan
        <b>spesifisitas 90%</b> (kemampuan mengenali kondisi normal dengan
        benar). Kedua nilai ini sudah melampaui standar minimum WHO untuk
        sistem skrining anemia berbasis teknologi.
        """,
    ),
    (
        "Apakah aplikasi ini bisa menggantikan tes darah?",
        """
        <b>Tidak.</b> Sistem ini adalah alat bantu skrining awal untuk
        tujuan edukasi dan penelitian, <b>bukan pengganti diagnosis medis
        profesional</b>. Jika hasil menunjukkan indikasi anemia, atau jika
        Anda merasakan gejala seperti lemas, pucat, atau pusing berkepanjangan,
        tetap disarankan melakukan pemeriksaan laboratorium (tes darah
        lengkap) dan berkonsultasi dengan tenaga medis untuk konfirmasi dan
        penanganan yang tepat.
        """,
    ),
    (
        "Foto seperti apa yang ideal untuk diunggah?",
        """
        Untuk hasil terbaik, unggah foto konjungtiva palpebra (bagian
        dalam kelopak mata bawah, bukan bagian putih mata) yang diambil
        dari jarak dekat, dengan pencahayaan yang cukup dan tidak buram.
        Tarik kelopak mata bawah sedikit ke bawah dengan jari saat
        memotret agar bagian dalam konjungtiva terlihat jelas.
        """,
    ),
    (
        "Apakah foto yang saya unggah disimpan?",
        """
        Foto yang diunggah hanya diproses secara sementara di memori
        server selama sesi berlangsung untuk menghasilkan prediksi, dan
        tidak disimpan secara permanen di server manapun. Riwayat prediksi
        yang ditampilkan di halaman Riwayat juga hanya tersimpan di sesi
        browser Anda saat ini dan akan hilang ketika halaman ditutup atau
        dimuat ulang.
        """,
    ),
    (
        "Bagaimana cara kerja sistem ini secara teknis?",
        """
        Sistem mengekstrak 346 fitur visual dari setiap foto menggunakan
        kombinasi <b>Local Binary Pattern (LBP)</b> multi-skala untuk
        tekstur halus, <b>Gray-Level Co-occurrence Matrix (GLCM)</b> untuk
        statistik tekstur, dan <b>Color Histogram</b> dari ruang warna
        RGB, HSV, dan LAB untuk menangkap tingkat kepucatan konjungtiva.
        Fitur-fitur ini kemudian diklasifikasikan menggunakan
        <b>Ensemble Learning</b> yang menggabungkan tiga model — Support
        Vector Machine, Random Forest, dan Gradient Boosting — melalui
        skema <i>soft voting</i>.
        """,
    ),
    (
        "Dataset apa yang digunakan untuk melatih model ini?",
        """
        Model dilatih menggunakan gabungan tiga dataset dari populasi
        berbeda: <b>CP-AnemiC</b> (710 citra anak-anak Ghana, diperoleh
        dari platform Mendeley Data), <b>Eyes-defy-anemia</b> (215 citra
        dewasa Italia dan India, diperoleh dari platform Kaggle), dan
        <b>Palpebral Conjunctiva</b> (187 citra, juga dari platform
        Kaggle). Ketiga dataset digabungkan dan dibagi secara stratifikasi
        dengan rasio 70:30 untuk pelatihan dan pengujian.
        """,
    ),
    (
        "Apakah hasil ini berlaku untuk semua populasi termasuk Indonesia?",
        """
        Ini adalah keterbatasan penting yang perlu disampaikan secara
        jujur: dataset pelatihan saat ini belum mencakup populasi
        Indonesia secara spesifik. Karakteristik fisik konjungtiva dapat
        sedikit berbeda antar populasi, sehingga performa model pada
        populasi Indonesia belum tervalidasi secara khusus dan dapat
        berbeda dari angka akurasi yang dilaporkan. Validasi lebih lanjut
        dengan data lokal Indonesia menjadi rencana pengembangan
        selanjutnya.
        """,
    ),
]


def render():
    st.markdown(
        """
        <div class="hero" style="background: linear-gradient(135deg, #4C72B0 0%, #2F4A73 100%);">
            <h1>❓ Pertanyaan Umum</h1>
            <p>Hal-hal yang sering ditanyakan seputar sistem skrining anemia ini.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for question, answer in FAQS:
        with st.expander(f"**{question}**"):
            st.markdown(answer, unsafe_allow_html=True)

    st.write("")
    st.markdown(
        """
        <div class="app-card" style="background:#FFF7ED; border-color:#FED7AA;">
            <h3 style="margin-top:0;">⚠️ Disclaimer</h3>
            <p style="margin-bottom:0;">
                Sistem ini dikembangkan untuk tujuan penelitian dan edukasi.
                Hasil prediksi tidak boleh dijadikan satu-satunya dasar
                keputusan medis. Selalu konsultasikan kondisi kesehatan Anda
                dengan dokter atau tenaga medis profesional.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
