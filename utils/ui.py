"""
Modul styling bersama — identitas visual "Spektrum Konjungtiva".

Token desain:
  - Warna diturunkan dari subjek literal: gradasi konjungtiva dari merah-marun
    (kaya hemoglobin) ke krem-pucat (anemia), bukan palet generik biru/oranye.
  - Tipografi: Fraunces (display, berkarakter klinis-organik) + Inter (UI/body).
  - Signature element: "pita spektrum" gradient yang merepresentasikan literally
    rentang warna yang dianalisis sistem — dipakai di hero & sebagai divider.
"""

import streamlit as st


INK = "#1B1F2A"          # near-black navy, teks utama & sidebar
MAROON = "#8B2942"       # merah-marun hemoglobin, warna primer aksen
BLUSH = "#E8C4A0"        # pucat-konjungtiva, aksen sekunder/hover
CREAM = "#F7F3ED"        # background hangat, bukan putih steril
SAGE = "#5C7A6B"         # hijau muted, status "normal/non-anemia"
PAPER = "#FFFFFF"

SPECTRUM = f"linear-gradient(90deg, {MAROON} 0%, #B8556F 35%, {BLUSH} 75%, {CREAM} 100%)"


def inject_global_css():
    """Suntikkan font, palet, dan seluruh komponen visual kustom."""
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,400..600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

        <style>
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}
        .stApp {{ background: {CREAM}; }}
        .block-container {{
            padding-top: 2rem;
            max-width: 940px;
        }}
        header[data-testid="stHeader"] {{ background: transparent; }}
        footer {{ visibility: hidden; }}

        h1, h2, h3, .display {{
            font-family: 'Fraunces', serif;
            font-weight: 560;
            color: {INK};
            letter-spacing: -0.01em;
        }}

        /* ── Pita spektrum — signature element ───────────────────────────── */
        .spectrum-bar {{
            height: 6px;
            border-radius: 3px;
            background: {SPECTRUM};
            margin: 6px 0 28px 0;
        }}
        .spectrum-bar.thin {{ height: 3px; margin: 18px 0; }}

        /* ── Sidebar — kartu pasien gelap ─────────────────────────────────── */
        [data-testid="stSidebar"] {{
            background: {INK};
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 0;
        }}
        [data-testid="stSidebarUserContent"] {{
            padding-top: 0 !important;
        }}

        [data-testid="stSidebarNav"] {{ padding: 6px 10px; }}

        [data-testid="stSidebarNav"] a {{
            border-radius: 8px;
            margin: 1px 2px;
            transition: background 0.15s ease;
        }}
        [data-testid="stSidebarNav"] span,
        [data-testid="stSidebarNav"] p {{
            color: #9AA3B8 !important;
            font-weight: 500;
            font-size: 0.9rem;
        }}
        [data-testid="stSidebarNav"] a:hover {{ background: rgba(255,255,255,0.05); }}
        [data-testid="stSidebarNav"] a:hover span,
        [data-testid="stSidebarNav"] a:hover p {{ color: #FFFFFF !important; }}
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: rgba(139,41,66,0.35);
            border-left: 3px solid {MAROON};
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"] span,
        [data-testid="stSidebarNav"] a[aria-current="page"] p {{ color: #FFFFFF !important; }}

        [data-testid="stSidebarCollapsedControl"] svg {{ color: #9AA3B8; }}

        /* ── Hero ─────────────────────────────────────────────────────────── */
        .hero {{
            background: {INK};
            border-radius: 4px;
            padding: 44px 38px 36px 38px;
            color: {CREAM};
            margin-bottom: 8px;
            position: relative;
            overflow: hidden;
        }}
        .hero::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 5px;
            background: {SPECTRUM};
        }}
        .hero .eyebrow {{
            font-size: 0.75rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: {BLUSH};
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .hero h1 {{
            color: #FFFFFF;
            margin: 0 0 12px 0;
            font-size: 2.3rem;
            font-style: italic;
        }}
        .hero p {{
            color: #C9CDD8;
            font-size: 1.04rem;
            margin: 0;
            max-width: 540px;
        }}

        /* ── Kartu ────────────────────────────────────────────────────────── */
        .app-card {{
            background: {PAPER};
            border: 1px solid rgba(27,31,42,0.08);
            border-radius: 4px;
            padding: 28px 30px;
            margin-bottom: 20px;
        }}
        .app-card h3 {{ margin-top: 0; font-size: 1.3rem; }}

        /* ── Badge ────────────────────────────────────────────────────────── */
        .badge {{
            display: inline-block;
            background: transparent;
            color: {MAROON};
            border: 1px solid {MAROON};
            border-radius: 2px;
            padding: 3px 11px;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.06em;
            margin-right: 8px;
            text-transform: uppercase;
        }}

        /* ── Alur kerja — diberi nomor karena memang urutan proses ──────────── */
        .step-row {{ display: flex; gap: 0; margin: 22px 0; flex-wrap: wrap; }}
        .step-pill {{
            flex: 1;
            min-width: 130px;
            padding: 16px 14px;
            text-align: left;
            border-left: 2px solid rgba(27,31,42,0.12);
        }}
        .step-pill .num {{
            font-family: 'Fraunces', serif;
            font-style: italic;
            font-size: 1.5rem;
            color: {MAROON};
            display: block;
            margin-bottom: 6px;
        }}
        .step-pill .label {{
            font-size: 0.84rem;
            font-weight: 500;
            color: {INK};
            line-height: 1.35;
        }}

        /* ── Metric override agar serasi tema ───────────────────────────────── */
        [data-testid="stMetricValue"] {{
            font-family: 'Fraunces', serif;
            color: {INK};
        }}

        /* ── Tombol utama ────────────────────────────────────────────────────── */
        .stButton button, [data-testid="stPageLink"] {{
            border-radius: 2px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    """Header branding di atas daftar menu sidebar, via ::before pada stSidebarNav.

    st.navigation() selalu merender daftar menu di posisi pertama DOM
    sidebar. Pendekatan elemen HTML terpisah (markdown, JS, fixed/absolute
    positioning) semuanya gagal karena bergantung pada asumsi struktur
    parent yang ternyata tidak konsisten. Solusi paling pasti: suntik
    brand sebagai ::before pada [data-testid="stSidebarNav"] itu sendiri.
    Pseudo-element selalu dirender sebelum isi asli elemen -- ini perilaku
    CSS baku, bukan tebakan, dan otomatis mengikuti lebar elemen induknya.
    """
    droplet_svg = (
        "data:image/svg+xml;utf8,"
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none'>"
        "<path d='M12 2C12 2 5 11 5 16C5 19.866 8.134 23 12 23C15.866 23 19 19.866 19 16C19 11 12 2 12 2Z' "
        "fill='%238B2942' stroke='%23E8C4A0' stroke-width='1'/>"
        "</svg>"
    )
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebarNav"] {{
            position: relative;
            padding-top: 78px !important;
        }}
        [data-testid="stSidebarNav"]::before {{
            content: "Skrining Anemia";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 76px;
            display: flex;
            align-items: center;
            padding: 0 20px 0 56px;
            background-color: #1B1F2A;
            background-image: url("{droplet_svg}");
            background-repeat: no-repeat;
            background-position: 18px center;
            background-size: 22px 22px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            font-family: 'Fraunces', serif;
            font-weight: 600;
            font-size: 0.98rem;
            color: #FFFFFF;
            z-index: 5;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def spectrum_divider(thin: bool = False):
    """Render pita gradient sebagai divider visual (signature element)."""
    cls = "spectrum-bar thin" if thin else "spectrum-bar"
    st.markdown(f'<div class="{cls}"></div>', unsafe_allow_html=True)
