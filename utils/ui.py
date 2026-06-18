"""
Modul styling bersama untuk seluruh halaman aplikasi.
Navigasi antar halaman ditangani oleh st.navigation() di app.py,
modul ini hanya menyediakan tema visual (CSS) dan komponen kartu.
"""

import streamlit as st


PRIMARY = "#DD8452"
SECONDARY = "#4C72B0"
DARK = "#1F2937"


def inject_global_css():
    """Suntikkan CSS global: tema warna, kartu, hero, dan styling navigasi atas."""
    st.markdown(
        f"""
        <style>
        .block-container {{
            padding-top: 1.5rem;
            max-width: 980px;
        }}
        header[data-testid="stHeader"] {{ background: transparent; }}

        /* Styling untuk navigasi st.navigation (tampil sebagai tab atas) */
        [data-testid="stNavigationTabs"] button {{
            font-weight: 600;
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
        .app-card h3 {{ margin-top: 0; }}

        /* Hero header */
        .hero {{
            background: linear-gradient(135deg, {SECONDARY} 0%, #2F4A73 100%);
            border-radius: 18px;
            padding: 36px 32px;
            color: white;
            margin-bottom: 24px;
        }}
        .hero h1 {{ color: white; margin: 0 0 8px 0; font-size: 2.0rem; }}
        .hero p {{ color: #E5E9F2; font-size: 1.02rem; margin: 0; }}

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
