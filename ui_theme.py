"""
🎨 EVALUERA - Modern UI Theme System
=====================================
Apple-inspiriertes, helles Evaluera-Brand-Design
"""

import streamlit as st

# ==================== DESIGN TOKENS - EVALUERA BRANDING ====================
COLORS = {
    # Primary - EVALUERA Mint/Türkis
    "primary": "#7BA5A0",        # Haupttürkis
    "primary_light": "#B8D4D1",  # Hell-Mint (Hintergründe)
    "primary_dark": "#2F4A56",   # Dunkles Blaugrau für Akzente

    # Neutrals (leicht warm / Apple-like)
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2933",
    "gray_900": "#111827",

    # Status
    "success": "#22c55e",
    "warning": "#eab308",
    "error": "#ef4444",
    "info": "#7BA5A0",

    # Backgrounds
    "bg_primary": "#F7FAF9",     # sehr helles Mint-Grau
    "bg_secondary": "#ECF4F3",   # leicht stärkere Mint-Tönung
    "surface": "#FFFFFF",
    "brand_bg": "#B8D4D1",       # Evaluera Mint für Highlights
}

SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "xxl": "3rem",
}

TYPOGRAPHY = {
    "font_family": "-apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif",
    "h1": "2.25rem",
    "h2": "1.5rem",
    "h3": "1.25rem",
    "body": "1rem",
    "small": "0.875rem",
    "tiny": "0.75rem",
}

RADIUS = {
    "sm": "8px",
    "md": "14px",
    "lg": "20px",
    "full": "9999px",
}

SHADOWS = {
    "sm": "0 8px 16px rgba(15, 23, 42, 0.08)",
    "md": "0 12px 30px rgba(15, 23, 42, 0.12)",
    "lg": "0 18px 45px rgba(15, 23, 42, 0.16)",
}


def apply_global_styles():
    """Apply global CSS theme (hell, Evaluera-Brand)"""
    st.markdown(f"""
    <style>
        /* ===== Global Layout / Background ===== */
        html, body, [data-testid="stApp"], .stApp {{
            background: radial-gradient(circle at top left,
                        {COLORS['primary_light']} 0%,
                        {COLORS['bg_primary']} 40%,
                        #FFFFFF 100%);
            color: {COLORS['gray_800']};
            font-family: {TYPOGRAPHY['font_family']};
        }}

        .main {{
            background-color: transparent;
        }}

        .block-container {{
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        /* ===== Streamlit Branding ausblenden ===== */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* ===== Typografie ===== */
        h1 {{
            font-size: {TYPOGRAPHY['h1']};
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: {COLORS['primary_dark']};
            margin-bottom: {SPACING['lg']};
        }}

        h2 {{
            font-size: {TYPOGRAPHY['h2']};
            font-weight: 600;
            color: {COLORS['gray_800']};
            margin-bottom: {SPACING['md']};
        }}

        h3 {{
            font-size: {TYPOGRAPHY['h3']};
            font-weight: 600;
            color: {COLORS['gray_700']};
            margin-bottom: {SPACING['sm']};
        }}

        p, span, label {{
            color: {COLORS['gray_700']};
        }}

        /* ===== Scrollbar (dezent) ===== */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: {COLORS['gray_100']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['gray_300']};
            border-radius: {RADIUS['full']};
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['gray_400']};
        }}

        /* ===== Cards / Container ===== */
        .stCard, .stDataFrame, .stTable, [data-testid="stExpander"], .element-container {{
            border-radius: {RADIUS['md']} !important;
        }}

        /* ===== Inputs (Text, Select, Number) ===== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: {RADIUS['md']} !important;
            border: 1px solid {COLORS['primary_light']} !important;
            padding: 0.75rem 1rem !important;
            color: {COLORS['gray_900']} !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04) !important;
        }}

        .stTextInput > div > div > input::placeholder,
        .stNumberInput > div > div > input::placeholder {{
            color: {COLORS['gray_400']} !important;
        }}

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border: 1px solid {COLORS['primary']} !important;
            box-shadow: 0 0 0 2px rgba(123, 165, 160, 0.35) !important;
            outline: none !important;
        }}

        /* Checkbox */
        .stCheckbox > label {{
            color: {COLORS['gray_700']} !important;
            font-size: {TYPOGRAPHY['small']} !important;
        }}

        /* ===== Buttons (Primär/Standard) ===== */
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"],
        button[kind="primary"],
        button[data-testid="baseButton-primary"] {{
            background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['primary']} 100%) !important;
            color: #FFFFFF !important;
            border-radius: {RADIUS['md']} !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            padding: 0.9rem 1.6rem !important;
            font-weight: 600 !important;
            box-shadow: 0 10px 25px rgba(47, 74, 86, 0.35) !important;
            transition: all 0.2s ease !important;
        }}

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 14px 30px rgba(47, 74, 86, 0.45) !important;
        }}

        .stButton > button[kind="secondary"],
        .stButton > button[data-testid="baseButton-secondary"] {{
            background: {COLORS['gray_50']} !important;
            color: {COLORS['gray_800']} !important;
            border-radius: {RADIUS['md']} !important;
            border: 1px solid {COLORS['gray_200']} !important;
        }}

        /* ===== Expander ===== */
        .streamlit-expanderHeader {{
            background: rgba(255, 255, 255, 0.9) !important;
            border-radius: {RADIUS['md']} !important;
            border: 1px solid {COLORS['gray_200']} !important;
            font-weight: 500 !important;
            color: {COLORS['gray_800']} !important;
        }}

        /* ===== Metrics ===== */
        div[data-testid="stMetricValue"] {{
            font-size: 1.6rem;
            font-weight: 700;
            color: {COLORS['primary_dark']};
        }}

        div[data-testid="stMetricLabel"] {{
            font-size: {TYPOGRAPHY['tiny']};
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: {COLORS['gray_500']};
        }}

        /* ===== Sidebar ===== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(
                180deg,
                rgba(255, 255, 255, 0.95) 0%,
                rgba(236, 244, 243, 0.98) 100%
            ) !important;
            border-right: 1px solid {COLORS['primary_light']}33 !important;
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }}

        /* ==== FORCE OVERRIDE: Remove dark inputs from login screen ==== */
        input[type="text"],
        input[type="password"],
        textarea,
        select {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid {COLORS['primary_light']} !important;
            color: {COLORS['gray_900']} !important;
            border-radius: {RADIUS['md']} !important;
            box-shadow: 0 4px 12px rgba(15,23,42,0.06) !important;
        }}

        input[type="text"]::placeholder,
        input[type="password"]::placeholder {{
            color: {COLORS['gray_400']} !important;
        }}

        input[type="text"]:focus,
        input[type="password"]:focus {{
            background: #FFFFFF !important;
            border: 1px solid {COLORS['primary']} !important;
            box-shadow: 0 0 0 3px rgba(123,165,160,0.25) !important;
        }}

        /* Remove any dark background bars that Streamlit injects */
        .stTextInput, .stPasswordInput, .stTextInput > div, .stPasswordInput > div {{
            background: transparent !important;
        }}

        /* Remove black bar behind input wrapper */
        .stTextInput > div > div,
        .stPasswordInput > div > div {{
            background: transparent !important;
        }}

        /* ===== FILE UPLOADER OVERRIDE ===== */
        .stFileUploader, .stFileUploader > div, .stFileUploader > div > div {{
            background: rgba(255, 255, 255, 0.95) !important;
            border-radius: 14px !important;
            border: 1px solid {COLORS['primary_light']} !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06) !important;
        }}

        .stFileUploader label {{
            color: {COLORS['gray_700']} !important;
        }}

        .stFileUploader div[data-testid="stFileDropzone"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px dashed {COLORS['primary']}55 !important;
            border-radius: 14px !important;
        }}

        /* ===== TOP DARK BAR FIX ===== */
        header[data-testid="stHeader"] {{
            background: linear-gradient(
                90deg,
                {COLORS['primary_light']} 0%,
                {COLORS['bg_primary']} 60%,
                #ffffff 100%
            ) !important;
            border-bottom: 1px solid {COLORS['primary_light']}33 !important;
        }}

        header[data-testid="stHeader"] > div {{
            background: transparent !important;
        }}
    </style>
    """, unsafe_allow_html=True)


# ==================== COMPONENT LIBRARY ====================

def card(content, padding="md", hover=False, border=True):
    """Minimal Card-Komponente"""
    border_style = f"border: 1px solid {COLORS['gray_200']};" if border else ""
    hover_style = (
        "transition: transform 0.18s ease, box-shadow 0.18s ease;"
        "transform: translateY(0);"
        f"box-shadow: {SHADOWS['sm']};"
    )
    if hover:
        hover_style += (
            "cursor: default;"
            "transform: translateY(0);"
        )

    st.markdown(
        f"""
        <div style="
            background: {COLORS['surface']};
            {border_style}
            border-radius: {RADIUS['md']};
            padding: {SPACING[padding]};
            box-shadow: {SHADOWS['sm']};
        ">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text, variant="info"):
    """Kompakter Status-Badge"""
    colors_map = {
        "success": COLORS["success"],
        "warning": COLORS["warning"],
        "error": COLORS["error"],
        "info": COLORS["info"],
    }
    color = colors_map.get(variant, COLORS["info"])

    return f"""
    <span style="
        background: {color}16;
        color: {color};
        padding: 0.2rem 0.75rem;
        border-radius: {RADIUS['full']};
        font-size: {TYPOGRAPHY['small']};
        font-weight: 500;
    ">
        {text}
    </span>
    """


def section_header(title, subtitle=None):
    """Section-Header mit optionalem Untertitel"""
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <p style="
            color: {COLORS['gray_500']};
            margin-top: 0.35rem;
            font-size: {TYPOGRAPHY['body']};
        ">{subtitle}</p>
        """

    st.markdown(
        f"""
        <div style="margin-bottom: {SPACING['lg']};">
            <h2 style="
                color: {COLORS['primary_dark']};
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                font-size: 1.1rem;
                margin: 0 0 0.15rem 0;
            ">{title}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider():
    """Minimaler Divider"""
    st.markdown(
        f"""
        <div style="
            height: 1px;
            background: linear-gradient(
                90deg,
                transparent,
                {COLORS['gray_200']},
                transparent
            );
            margin: {SPACING['xl']} 0;
        "></div>
        """,
        unsafe_allow_html=True,
    )

def wizard_step(step_number, title, description, is_active, is_completed):
    """
    Wizard Step Component – kompatibel mit Evaluera UI Theme
    """
    # Farben abhängig vom Status
    if is_completed:
        bg = COLORS["success"]
        text_color = "#ffffff"
        icon = "✓"
    elif is_active:
        bg = COLORS["primary"]
        text_color = "#ffffff"
        icon = str(step_number)
    else:
        bg = COLORS["gray_200"]
        text_color = COLORS["gray_500"]
        icon = str(step_number)

    return f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: {SPACING['md']};
        margin-bottom: {SPACING['sm']};
        background: {COLORS['surface']};
        border-radius: {RADIUS['md']};
        border: 2px solid {bg if is_active else COLORS['gray_200']};
        opacity: {1 if (is_active or is_completed) else 0.6};
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
    ">
        <div style="
            width: 40px;
            height: 40px;
            border-radius: {RADIUS['full']};
            background: {bg};
            color: {text_color};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1rem;
        ">
            {icon}
        </div>

        <div style="flex: 1;">
            <div style="
                font-weight: 600;
                color: {COLORS['primary_dark']};
                font-size: 1rem;
            ">
                {title}
            </div>

            <div style="
                font-size: 0.875rem;
                color: {COLORS['gray_600']};
            ">
                {description}
            </div>
        </div>
    </div>
    """