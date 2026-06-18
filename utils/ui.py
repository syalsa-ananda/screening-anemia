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

        /* ── Sidebar navigasi gelap (mirip referensi dashboard) ──────────── */
        [data-testid="stSidebar"] {{
            background: #14213D;
            border-right: none;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1.2rem;
        }}

        /* Judul/branding kecil di atas sidebar (opsional, lihat render_sidebar_brand) */
        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 4px 18px 18px 18px;
            margin-bottom: 6px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }}
        .sidebar-brand .logo {{
            width: 34px;
            height: 34px;
            border-radius: 9px;
            background: {PRIMARY};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.05rem;
        }}
        .sidebar-brand .name {{
            color: #FFFFFF;
            font-weight: 700;
            font-size: 0.95rem;
            line-height: 1.15;
        }}
        .sidebar-brand .sub {{
            color: #8B95B3;
            font-size: 0.72rem;
        }}

        /* Item navigasi st.navigation di sidebar */
        [data-testid="stSidebarNav"] {{
            padding: 4px 10px;
        }}
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNav"] [data-testid="stPageLink"] {{
            border-radius: 10px;
            margin: 2px 4px;
            transition: background 0.15s ease;
        }}
        [data-testid="stSidebarNav"] span,
        [data-testid="stSidebarNav"] p {{
            color: #AEB6CC !important;
            font-weight: 600;
            font-size: 0.92rem;
        }}
        [data-testid="stSidebarNav"] a:hover {{
            background: rgba(255,255,255,0.06);
        }}
        [data-testid="stSidebarNav"] a:hover span,
        [data-testid="stSidebarNav"] a:hover p {{
            color: #FFFFFF !important;
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: {PRIMARY};
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"] span,
        [data-testid="stSidebarNav"] a[aria-current="page"] p {{
            color: #FFFFFF !important;
        }}

        /* Collapse control tetap terlihat di atas background gelap */
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg {{
            color: #AEB6CC;
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


def render_sidebar_brand():
    """Tampilkan branding kecil (logo + nama) di bagian atas sidebar."""
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="logo">🩺</div>
            <div>
                <div class="name">Skrining Anemia</div>
                <div class="sub">Non-Invasif</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
