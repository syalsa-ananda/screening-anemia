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
    """Header branding di atas sidebar via pseudo-element ::before.

    st.navigation() selalu merender daftar menu di posisi pertama DOM
    sidebar terlepas urutan kode Python, JavaScript, atau position:fixed
    (yang ternyata salah lebar karena meniru ukuran sidebar secara manual).
    Pseudo-element ::before pada container sidebar utama dijamin selalu
    tampil sebelum seluruh konten asli elemen tersebut -- ini aturan baku
    CSS, bukan tebakan struktur DOM, sehingga lebar & posisi otomatis
    ikut mengikuti sidebar aslinya tanpa hardcode ukuran apapun.
    """
    st.markdown(
        """
        <style>
        [data-testid="stSidebarContent"]::before,
        [data-testid="stSidebarUserContent"]::before {
            content: "";
            display: block;
            height: 76px;
        }
        [data-testid="stSidebar"] {
            position: relative;
        }
        .sidebar-brand-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 76px;
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 0 20px;
            background: #1B1F2A;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            z-index: 10;
        }
        .sidebar-brand-overlay .mark {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            background: #262B3A;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        .sidebar-brand-overlay .mark svg {
            width: 19px;
            height: 19px;
        }
        .sidebar-brand-overlay .name {
            font-family: 'Fraunces', serif;
            color: #FFFFFF;
            font-weight: 600;
            font-size: 0.98rem;
            line-height: 1.2;
        }
        .sidebar-brand-overlay .sub {
            color: #8A93A8;
            font-size: 0.7rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        </style>
        <div class="sidebar-brand-overlay">
            <div class="mark">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M2 12C2 12 5.5 5 12 5C18.5 5 22 12 22 12C22 12 18.5 19 12 19C5.5 19 2 12 2 12Z"
                          stroke="#E8C4A0" stroke-width="1.6" stroke-linejoin="round"/>
                    <circle cx="12" cy="12" r="3.2" stroke="#8B2942" stroke-width="1.6"/>
                    <circle cx="12" cy="12" r="1.1" fill="#8B2942"/>
                </svg>
            </div>
            <div>
                <div class="name">Skrining Anemia</div>
                <div class="sub">Non-Invasif</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def spectrum_divider(thin: bool = False):
    """Render pita gradient sebagai divider visual (signature element)."""
    cls = "spectrum-bar thin" if thin else "spectrum-bar"
    st.markdown(f'<div class="{cls}"></div>', unsafe_allow_html=True)
