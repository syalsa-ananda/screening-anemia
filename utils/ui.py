"""
Modul styling dan komponen UI bersama untuk seluruh halaman aplikasi.
Menyediakan tema visual custom, navbar atas, dan helper komponen kartu/metrik.
"""

import streamlit as st


PRIMARY = "#DD8452"
SECONDARY = "#4C72B0"
DARK = "#1F2937"
BG_SOFT = "#FAFAFA"


def inject_global_css():
    """Suntikkan CSS global: sembunyikan sidebar, tema warna, kartu, dan navbar."""
    st.markdown(
        f"""
        <style>
        /* Sembunyikan sidebar Streamlit bawaan & nav multipage default */
        [data-testid="stSidebar"] {{ display: none; }}
        [data-testid="stSidebarCollapsedControl"] {{ display: none; }}
        header[data-testid="stHeader"] {{ background: transparent; }}

        .block-container {{
            padding-top: 1.2rem;
            max-width: 980px;
        }}

        /* Navbar custom — styling untuk st.page_link */
        .navbar-wrap {{
            background: {DARK};
            border-radius: 14px;
            padding: 8px;
            margin-bottom: 4px;
        }}
        .navbar-wrap [data-testid="stPageLink"] {{
            background: transparent;
            border-radius: 10px;
        }}
        .navbar-wrap [data-testid="stPageLink"] p {{
            color: #D1D5DB;
            font-weight: 600;
            font-size: 0.88rem;
            text-align: center;
            margin: 0;
        }}
        .navbar-wrap [data-testid="stPageLink"]:hover {{
            background: #374151;
        }}
        .navbar-wrap [data-testid="stPageLink"]:hover p {{
            color: #FFFFFF;
        }}

        /* Kartu umum */
        .app-card {{
            background: #FFFFFF;
            border: 1px solid #EEEEEE;
            border-radius: 16px;
            padding: 24px 26px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}
        .app-card h3 {{
            margin-top: 0;
        }}

        /* Hero header */
        .hero {{
            background: linear-gradient(135deg, {SECONDARY} 0%, #2F4A73 100%);
            border-radius: 18px;
            padding: 36px 32px;
            color: white;
            margin-bottom: 24px;
        }}
        .hero h1 {{
            color: white;
            margin: 0 0 8px 0;
            font-size: 2.0rem;
        }}
        .hero p {{
            color: #E5E9F2;
            font-size: 1.02rem;
            margin: 0;
        }}

        /* Step pill untuk alur kerja */
        .step-row {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin: 18px 0;
        }}
        .step-pill {{
            background: #F3F4F6;
            border-radius: 12px;
            padding: 14px 16px;
            flex: 1;
            min-width: 130px;
            text-align: center;
            border: 1px solid #E5E7EB;
        }}
        .step-pill .num {{
            display: inline-block;
            background: {PRIMARY};
            color: white;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            font-size: 0.85rem;
            font-weight: 700;
            line-height: 26px;
            margin-bottom: 6px;
        }}
        .step-pill .label {{
            font-size: 0.85rem;
            font-weight: 600;
            color: {DARK};
        }}

        /* Badge kecil */
        .badge {{
            display: inline-block;
            background: #FFF1E8;
            color: {PRIMARY};
            border-radius: 8px;
            padding: 3px 10px;
            font-size: 0.78rem;
            font-weight: 700;
            margin-right: 6px;
        }}

        footer {{ visibility: hidden; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


NAV_ITEMS = [
    ("🏠 Beranda", "app.py"),
    ("🔍 Skrining", "pages/1_Skrining.py"),
    ("🩸 Edukasi Anemia", "pages/2_Edukasi_Anemia.py"),
    ("📋 Riwayat", "pages/3_Riwayat.py"),
    ("❓ FAQ", "pages/4_FAQ.py"),
]


def render_navbar(active_label: str):
    """Render navbar horizontal menggunakan st.page_link, dibungkus styling custom."""
    st.markdown('<div class="navbar-wrap">', unsafe_allow_html=True)
    cols = st.columns(len(NAV_ITEMS))
    for col, (label, target) in zip(cols, NAV_ITEMS):
        with col:
            st.page_link(target, label=label, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:10px'></div>", unsafe_allow_html=True)
