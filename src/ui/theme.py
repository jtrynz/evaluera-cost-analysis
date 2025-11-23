"""
🎨 EVALUERA - Apple-Like UI Theme System
=========================================
Premium Apple-inspiriertes Design mit Glassmorphism
"""

import streamlit as st

# ==================== APPLE-LIKE EVALUERA COLOR PALETTE ====================
COLORS = {
    # EVALUERA Brand Colors
    "primary": "#2A4F57",        # Primary: Dunkles Evaluera Blaugrau
    "primary_light": "#E7F1EF",  # Primary Light: Sehr helles Mint
    "secondary": "#B8D4D1",      # Secondary: Helles Mint
    "light_accent": "#E7F1EF",   # Light Accent: Sehr helles Mint
    "dark_accent": "#1E2E32",    # Dark Accent: Fast Schwarz
    "highlight": "#8FAEAB",      # Optional Highlight: Mittleres Mint

    # Neutrals (Apple-Stil: warm, soft)
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",

    # Status Colors
    "success": "#10B981",  # Apple Green
    "warning": "#F59E0B",  # Apple Orange
    "error": "#EF4444",    # Apple Red
    "info": "#3B82F6",     # Apple Blue

    # Backgrounds
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F9FAFB",
    "surface": "#FFFFFF",
    "surface_tint": "#F9FAFB",   # Leicht getönte Oberfläche
}

SPACING = {
    "xs": "0.25rem",    # 4px
    "sm": "0.5rem",     # 8px
    "md": "1rem",       # 16px
    "lg": "1.5rem",     # 24px
    "xl": "2rem",       # 32px
    "xxl": "3rem",      # 48px
    "xxxl": "4rem",     # 64px
}

TYPOGRAPHY = {
    "font_family": "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', sans-serif",
    "h1": "2.5rem",     # 40px
    "h2": "1.875rem",   # 30px
    "h3": "1.5rem",     # 24px
    "h4": "1.25rem",    # 20px
    "body": "1rem",     # 16px
    "small": "0.875rem", # 14px
    "tiny": "0.75rem",  # 12px
}

RADIUS = {
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "20px",
    "full": "9999px",
}

SHADOWS = {
    "xs": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "sm": "0 2px 8px rgba(0, 0, 0, 0.08)",
    "md": "0 4px 16px rgba(0, 0, 0, 0.10)",
    "lg": "0 8px 24px rgba(0, 0, 0, 0.12)",
    "xl": "0 16px 40px rgba(0, 0, 0, 0.15)",
    "glass": "0 8px 32px 0 rgba(31, 38, 135, 0.15)",
}

# ==================== GLOBAL APPLE-LIKE STYLES ====================
def apply_global_styles():
    """Apply Apple-inspired global CSS theme"""
    st.markdown(f"""
    <style>
        /* ========== IMPORT APPLE FONTS ========== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ========== GLOBAL RESET & LAYOUT ========== */
        * {{
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        html, body, [data-testid="stApp"], .stApp {{
            background: {COLORS['bg_primary']} !important;
            color: {COLORS['dark_accent']} !important;
            font-family: {TYPOGRAPHY['font_family']} !important;
            font-size: {TYPOGRAPHY['body']};
            line-height: 1.6;
        }}

        .main {{
            background: transparent !important;
            padding: {SPACING['lg']} {SPACING['xl']} !important;
        }}

        .block-container {{
            max-width: 1400px;
            padding-top: {SPACING['xl']};
            padding-bottom: {SPACING['xl']};
        }}

        /* ========== HIDE STREAMLIT BRANDING ========== */
        #MainMenu {{visibility: hidden !important;}}
        footer {{visibility: hidden !important;}}
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        /* ========== TYPOGRAPHY (APPLE STYLE) ========== */
        h1 {{
            font-size: {TYPOGRAPHY['h1']} !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
            color: {COLORS['primary']} !important;
            margin: {SPACING['lg']} 0 {SPACING['md']} 0 !important;
            line-height: 1.2 !important;
        }}

        h2 {{
            font-size: {TYPOGRAPHY['h2']} !important;
            font-weight: 600 !important;
            letter-spacing: -0.01em !important;
            color: {COLORS['dark_accent']} !important;
            margin: {SPACING['lg']} 0 {SPACING['md']} 0 !important;
            line-height: 1.3 !important;
        }}

        h3 {{
            font-size: {TYPOGRAPHY['h3']} !important;
            font-weight: 600 !important;
            color: {COLORS['gray_800']} !important;
            margin: {SPACING['md']} 0 {SPACING['sm']} 0 !important;
            line-height: 1.4 !important;
        }}

        /* ========== FIX 6: HIGH CONTRAST TEXT ========== */
        p, span, label, div {{
            color: {COLORS['gray_800']} !important;
            line-height: 1.6 !important;
        }}

        /* Strong text for readability */
        .stMarkdown strong, b {{
            color: {COLORS['gray_900']} !important;
            font-weight: 600 !important;
        }}

        /* Body text high contrast */
        .stMarkdown p {{
            color: {COLORS['gray_800']} !important;
        }}

        /* ========== APPLE SCROLLBAR ========== */
        ::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}
        ::-webkit-scrollbar-track {{
            background: {COLORS['gray_100']};
            border-radius: {RADIUS['full']};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['gray_300']};
            border-radius: {RADIUS['full']};
            border: 2px solid {COLORS['gray_100']};
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['gray_400']};
        }}

        /* ========== INPUT FIELDS (APPLE STYLE) ========== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox > div > div {{
            background: {COLORS['surface']} !important;
            border: 1.5px solid {COLORS['gray_300']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 12px 16px !important;
            font-size: {TYPOGRAPHY['body']} !important;
            color: {COLORS['dark_accent']} !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: {SHADOWS['xs']} !important;
        }}

        .stTextInput > div > div > input::placeholder,
        .stNumberInput > div > div > input::placeholder,
        .stTextArea textarea::placeholder {{
            color: {COLORS['gray_400']} !important;
            font-weight: 400 !important;
        }}

        /* ========== FIX 6: REMOVE RED BORDERS - APPLE FOCUS STATE ========== */
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea textarea:focus,
        .stSelectbox > div > div:focus-within {{
            border-color: {COLORS['primary']} !important;
            box-shadow: 0 0 0 4px {COLORS['light_accent']} !important;
            outline: none !important;
        }}

        /* Ensure NO red borders on invalid state */
        .stTextInput > div > div > input:invalid,
        .stNumberInput > div > div > input:invalid,
        .stTextArea textarea:invalid {{
            border-color: {COLORS['gray_300']} !important;
            box-shadow: none !important;
        }}

        .stTextInput > div > div > input:invalid:focus,
        .stNumberInput > div > div > input:invalid:focus,
        .stTextArea textarea:invalid:focus {{
            border-color: {COLORS['primary']} !important;
            box-shadow: 0 0 0 4px {COLORS['light_accent']} !important;
        }}

        /* Remove Streamlit's dark input background */
        .stTextInput, .stNumberInput, .stTextArea, .stSelectbox {{
            background: transparent !important;
        }}

        .stTextInput > div, .stNumberInput > div, .stTextArea > div, .stSelectbox > div {{
            background: transparent !important;
        }}

        /* ========== BUTTONS (APPLE GLASSMORPHISM) ========== */
        /* ========== FIX 6: SMOOTH ANIMATIONS (280ms ease-out) ========== */
        .stButton > button[kind="primary"],
        button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['dark_accent']} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: {RADIUS['md']} !important;
            padding: 12px 24px !important;
            font-size: {TYPOGRAPHY['body']} !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            box-shadow: {SHADOWS['md']}, 0 0 0 1px rgba(255,255,255,0.1) inset !important;
            transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
        }}

        .stButton > button[kind="primary"]:hover,
        button[kind="primary"]:hover {{
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: {SHADOWS['lg']}, 0 0 0 1px rgba(255,255,255,0.2) inset !important;
        }}

        .stButton > button[kind="primary"]:active,
        button[kind="primary"]:active {{
            transform: translateY(0) scale(0.98) !important;
            transition: all 0.12s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stButton > button[kind="secondary"],
        button[kind="secondary"] {{
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(10px) !important;
            color: {COLORS['primary']} !important;
            border: 1.5px solid {COLORS['gray_300']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            box-shadow: {SHADOWS['sm']} !important;
            transition: all 0.26s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background: rgba(255, 255, 255, 1) !important;
            border-color: {COLORS['primary']} !important;
            transform: translateY(-2px) scale(1.01) !important;
            box-shadow: {SHADOWS['md']} !important;
        }}

        .stButton > button[kind="secondary"]:active {{
            transform: translateY(0) scale(0.99) !important;
            transition: all 0.12s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        /* ========== CHECKBOX & RADIO (APPLE STYLE) ========== */
        .stCheckbox > label,
        .stRadio > label {{
            color: {COLORS['gray_700']} !important;
            font-size: {TYPOGRAPHY['small']} !important;
            font-weight: 500 !important;
        }}

        .stCheckbox input[type="checkbox"],
        .stRadio input[type="radio"] {{
            accent-color: {COLORS['primary']} !important;
            width: 20px !important;
            height: 20px !important;
        }}

        /* ========== FILE UPLOADER (APPLE STYLE) ========== */
        .stFileUploader {{
            background: {COLORS['surface']} !important;
            border: 2px dashed {COLORS['gray_300']} !important;
            border-radius: {RADIUS['lg']} !important;
            padding: {SPACING['lg']} !important;
            transition: all 0.2s ease !important;
        }}

        .stFileUploader:hover {{
            border-color: {COLORS['primary']} !important;
            background: {COLORS['light_accent']} !important;
        }}

        .stFileUploader label {{
            color: {COLORS['gray_700']} !important;
            font-weight: 600 !important;
        }}

        /* ========== EXPANDER (APPLE STYLE) ========== */
        .streamlit-expanderHeader {{
            background: rgba(255, 255, 255, 0.8) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid {COLORS['gray_200']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: {SPACING['md']} !important;
            font-weight: 600 !important;
            color: {COLORS['primary']} !important;
            transition: all 0.2s ease !important;
        }}

        .streamlit-expanderHeader:hover {{
            background: rgba(255, 255, 255, 1) !important;
            border-color: {COLORS['primary']} !important;
        }}

        /* ========== METRICS (APPLE STYLE) ========== */
        div[data-testid="stMetricValue"] {{
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: {COLORS['primary']} !important;
            letter-spacing: -0.02em !important;
        }}

        div[data-testid="stMetricLabel"] {{
            font-size: {TYPOGRAPHY['small']} !important;
            font-weight: 600 !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            color: {COLORS['gray_500']} !important;
        }}

        /* ========== FIX 6: APPLE-STYLE CARDS WITH SMOOTH HOVER ========== */
        .stAlert, [data-testid="stMetric"], div[data-testid="column"] > div {{
            border-radius: {RADIUS['lg']} !important;
            border: 1px solid {COLORS['gray_200']} !important;
            box-shadow: {SHADOWS['sm']} !important;
            transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stAlert:hover, [data-testid="stMetric"]:hover {{
            box-shadow: {SHADOWS['md']} !important;
            transform: translateY(-1px) !important;
            border-color: {COLORS['gray_300']} !important;
        }}

        /* Alert variants */
        .stAlert[data-baseweb="notification"] {{
            border-left-width: 4px !important;
        }}

        /* ========== SIDEBAR (APPLE GLASSMORPHISM) ========== */
        [data-testid="stSidebar"] {{
            background: linear-gradient(
                180deg,
                rgba(255, 255, 255, 0.95) 0%,
                rgba(231, 241, 239, 0.95) 100%
            ) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-right: 1px solid {COLORS['gray_200']} !important;
            box-shadow: 4px 0 16px rgba(0, 0, 0, 0.05) !important;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            border-radius: {RADIUS['md']} !important;
        }}

        /* ========== DATAFRAME/TABLE (APPLE STYLE) ========== */
        .stDataFrame, .dataframe {{
            border-radius: {RADIUS['md']} !important;
            border: 1px solid {COLORS['gray_200']} !important;
            overflow: hidden !important;
            box-shadow: {SHADOWS['sm']} !important;
        }}

        .stDataFrame thead tr th {{
            background: {COLORS['light_accent']} !important;
            color: {COLORS['primary']} !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            font-size: {TYPOGRAPHY['tiny']} !important;
            letter-spacing: 0.05em !important;
            border-bottom: 2px solid {COLORS['primary']} !important;
        }}

        /* ========== LOADING SPINNER (APPLE STYLE) ========== */
        .stSpinner > div {{
            border-top-color: {COLORS['primary']} !important;
        }}

        /* ========== TABS (APPLE STYLE) ========== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: transparent !important;
            border-bottom: 2px solid {COLORS['gray_200']} !important;
        }}

        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border: none !important;
            padding: 12px 24px !important;
            color: {COLORS['gray_600']} !important;
            font-weight: 600 !important;
            border-radius: {RADIUS['md']} {RADIUS['md']} 0 0 !important;
            transition: all 0.2s ease !important;
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            background: {COLORS['light_accent']} !important;
            color: {COLORS['primary']} !important;
        }}

        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            background: {COLORS['light_accent']} !important;
            color: {COLORS['primary']} !important;
            border-bottom: 3px solid {COLORS['primary']} !important;
        }}

        /* ========== SOFT FADE ANIMATIONS ========== */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        .fade-in {{
            animation: fadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* ========== GLASS EFFECT UTILITIES ========== */
        .glass {{
            background: rgba(255, 255, 255, 0.7) !important;
            backdrop-filter: blur(10px) saturate(150%) !important;
            -webkit-backdrop-filter: blur(10px) saturate(150%) !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            box-shadow: {SHADOWS['glass']} !important;
        }}

        .glass-strong {{
            background: rgba(255, 255, 255, 0.9) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            box-shadow: {SHADOWS['md']} !important;
        }}
    </style>
    """, unsafe_allow_html=True)


# ==================== GLASSMORPHISM & LIQUID GLASS ====================
def apply_liquid_glass_styles():
    """Apply premium glassmorphism effects"""
    st.markdown(f"""
    <style>
        /* ========== LIQUID GLASS CARD ========== */
        .liquid-glass-card {{
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(16px) saturate(150%);
            -webkit-backdrop-filter: blur(16px) saturate(150%);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: {RADIUS['lg']};
            padding: {SPACING['lg']};
            box-shadow: {SHADOWS['glass']}, inset 0 1px 0 rgba(255, 255, 255, 0.8);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .liquid-glass-card:hover {{
            transform: translateY(-4px);
            box-shadow: {SHADOWS['xl']}, inset 0 1px 0 rgba(255, 255, 255, 1);
            border-color: rgba(255, 255, 255, 0.8);
        }}

        /* ========== GLOW EFFECT ========== */
        .glow {{
            box-shadow: 0 0 20px {COLORS['primary']}33, {SHADOWS['md']};
        }}

        .glow-hover:hover {{
            box-shadow: 0 0 30px {COLORS['primary']}55, {SHADOWS['lg']};
        }}
    </style>
    """, unsafe_allow_html=True)


# ==================== SCROLL BEHAVIOR ====================
def create_scroll_behavior():
    """Smooth scroll behavior"""
    st.markdown("""
    <style>
        html {{
            scroll-behavior: smooth;
        }}

        .main {{
            scroll-behavior: smooth;
        }}
    </style>
    """, unsafe_allow_html=True)


# ==================== COMPONENT LIBRARY ====================

def card(content, padding="md", glass=False, hover=True):
    """Apple-style Card Component"""
    glass_class = "glass" if glass else ""
    hover_style = "cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease;" if hover else ""

    st.markdown(
        f"""
        <div class="{glass_class}" style="
            background: {COLORS['surface']};
            border: 1px solid {COLORS['gray_200']};
            border-radius: {RADIUS['lg']};
            padding: {SPACING[padding]};
            box-shadow: {SHADOWS['sm']};
            {hover_style}
        ">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text, variant="info"):
    """Apple-style Status Badge"""
    colors_map = {
        "success": COLORS["success"],
        "warning": COLORS["warning"],
        "error": COLORS["error"],
        "info": COLORS["info"],
    }
    color = colors_map.get(variant, COLORS["info"])

    return f"""
    <span style="
        background: {color}15;
        color: {color};
        padding: 4px 12px;
        border-radius: {RADIUS['full']};
        font-size: {TYPOGRAPHY['small']};
        font-weight: 600;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    ">
        {text}
    </span>
    """


def section_header(title, subtitle=None):
    """Apple-style Section Header"""
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <p style="
            color: {COLORS['gray_500']};
            margin-top: 8px;
            font-size: {TYPOGRAPHY['body']};
            font-weight: 400;
            line-height: 1.6;
        ">{subtitle}</p>
        """

    st.markdown(
        f"""
        <div style="margin-bottom: {SPACING['lg']}; margin-top: {SPACING['xl']};">
            <h2 style="
                color: {COLORS['primary']};
                font-weight: 700;
                font-size: {TYPOGRAPHY['h2']};
                letter-spacing: -0.01em;
                margin: 0;
                line-height: 1.3;
            ">{title}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider():
    """Minimal Apple Divider"""
    st.markdown(
        f"""
        <div style="
            height: 1px;
            background: linear-gradient(
                90deg,
                transparent,
                {COLORS['gray_300']},
                transparent
            );
            margin: {SPACING['xl']} 0;
        "></div>
        """,
        unsafe_allow_html=True,
    )


def wizard_step(step_number, title, description, is_active, is_completed):
    """Apple-style Wizard Step Component"""
    if is_completed:
        bg = COLORS["success"]
        text_color = "#FFFFFF"
        icon = "✓"
        border_color = COLORS["success"]
    elif is_active:
        bg = COLORS["primary"]
        text_color = "#FFFFFF"
        icon = str(step_number)
        border_color = COLORS["primary"]
    else:
        bg = COLORS["gray_200"]
        text_color = COLORS["gray_500"]
        icon = str(step_number)
        border_color = COLORS["gray_200"]

    opacity = "1" if (is_active or is_completed) else "0.5"

    return f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px 20px;
        margin-bottom: 12px;
        background: {COLORS['surface']};
        border: 2px solid {border_color};
        border-radius: {RADIUS['lg']};
        opacity: {opacity};
        box-shadow: {SHADOWS['sm']};
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    ">
        <div style="
            width: 48px;
            height: 48px;
            border-radius: {RADIUS['full']};
            background: {bg};
            color: {text_color};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.125rem;
            box-shadow: {SHADOWS['sm']};
        ">
            {icon}
        </div>

        <div style="flex: 1;">
            <div style="
                font-weight: 600;
                color: {COLORS['primary']};
                font-size: {TYPOGRAPHY['body']};
                margin-bottom: 4px;
            ">
                {title}
            </div>

            <div style="
                font-size: {TYPOGRAPHY['small']};
                color: {COLORS['gray_600']};
                line-height: 1.4;
            ">
                {description}
            </div>
        </div>
    </div>
    """
