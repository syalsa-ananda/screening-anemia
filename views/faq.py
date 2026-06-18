"""
Halaman FAQ — pertanyaan umum seputar penggunaan aplikasi.
"""

import streamlit as st

from utils.ui import spectrum_divider


FAQS = [
    (
        "Seberapa akurat hasil ini?",
        """
        Pada 334 foto uji yang tidak pernah dilihat model selama pelatihan,
        sistem mencapai <b>akurasi 92,5%</b>, dengan <b>sensitivitas 95%</b>
        (mendeteksi kasus anemia yang sebenarnya) dan <b>spesifisitas 90%</b>
        (mengenali kondisi normal dengan benar). Kedua nilai ini melampaui
        standar minimum WHO untuk sistem skrining anemia berbasis teknologi.
        """,
    ),
    (
        "Apakah ini bisa menggantikan tes darah?",
        """
        <b>Tidak.</b> Ini adalah alat bantu skrining awal untuk tujuan edukasi
        dan penelitian, bukan pengganti diagnosis medis. Jika hasil menunjukkan
        indikasi anemia, atau Anda merasakan gejala seperti lemas dan pucat
        berkepanjangan, tetap disarankan melakukan tes darah lengkap dan
        berkonsultasi dengan tenaga medis.
        """,
    ),
    (
        "Foto seperti apa yang ideal?",
        """
        Foto konjungtiva palpebra (bagian dalam kelopak mata bawah, bukan
        bagian putih mata), diambil dari jarak dekat dengan pencahayaan
        cukup dan tidak buram. Tarik kelopak mata bawah sedikit ke bawah
        saat memotret agar area konjungtiva terlihat jelas.
        """,
    ),
    (
        "Apakah foto saya disimpan?",
        """
        Foto hanya diproses sementara di memori server selama sesi
        berlangsung, tidak disimpan permanen di server manapun. Riwayat
        prediksi juga hanya tersimpan di sesi browser Anda dan hilang saat
        halaman ditutup atau dimuat ulang.
        """,
    ),
    (
        "Bagaimana cara kerjanya secara teknis?",
        """
        Sistem mengekstrak 346 ukuran visual dari setiap foto: <b>Local
        Binary Pattern</b> multi-skala untuk tekstur halus, <b>Gray-Level
        Co-occurrence Matrix</b> untuk statistik tekstur, dan <b>histogram
        warna</b> dari ruang warna RGB, HSV, dan LAB untuk menangkap tingkat
        kepucatan. Ukuran-ukuran ini diklasifikasikan oleh tiga model —
        Support Vector Machine, Random Forest, dan Gradient Boosting —
        melalui skema <i>soft voting</i>.
        """,
    ),
    (
        "Dataset apa yang digunakan?",
        """
        Gabungan tiga dataset dari populasi berbeda: <b>CP-AnemiC</b>
        (710 foto anak-anak Ghana, dari Mendeley Data), <b>Eyes-defy-anemia</b>
        (215 foto dewasa Italia dan India, dari Kaggle), dan <b>Palpebral
        Conjunctiva</b> (187 foto, juga dari Kaggle). Ketiganya digabung dan
        dibagi 70:30 untuk pelatihan dan pengujian.
        """,
    ),
    (
        "Apakah berlaku untuk populasi Indonesia?",
        """
        Ini keterbatasan penting: dataset pelatihan belum mencakup populasi
        Indonesia secara spesifik. Karakteristik konjungtiva dapat sedikit
        berbeda antar populasi, sehingga performa pada populasi Indonesia
        belum tervalidasi khusus dan dapat berbeda dari angka yang
        dilaporkan. Validasi dengan data lokal adalah rencana pengembangan
        berikutnya.
        """,
    ),
]


def render():
    st.markdown('<div class="eyebrow" style="color:#8B2942;">FAQ</div>', unsafe_allow_html=True)
    st.markdown("### Pertanyaan umum")
    spectrum_divider(thin=True)

    for question, answer in FAQS:
        with st.expander(question):
            st.markdown(answer, unsafe_allow_html=True)

    st.write("")
    st.markdown(
        """
        <div class="app-card" style="border-left: 3px solid #8B2942;">
            <h3 style="font-size:1.05rem; margin-top:0;">Disclaimer</h3>
            <p style="margin-bottom:0;">
                Dikembangkan untuk tujuan penelitian dan edukasi. Hasil
                prediksi tidak boleh dijadikan satu-satunya dasar keputusan
                medis. Konsultasikan kondisi kesehatan Anda dengan dokter
                atau tenaga medis profesional.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
