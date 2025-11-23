"""
🎨 EVALUERA - Professional UI Theme System
==========================================
Evaluera brand colors with professional design system
"""

import streamlit as st

# ==================== EVALUERA BRAND COLOR PALETTE ====================
COLORS = {
    # EVALUERA Primary Brand Colors (aus Anforderung)
    "primary": "#7BA5A0",           # Primary: Evaluera Mint-Türkis
    "primary_light": "#B8D4D1",     # Primary Light: Helles Mint
    "primary_dark": "#5A8680",      # Primary Dark: Dunkles Mint-Türkis
    "error": "#2F4A56",             # Error/Dark: Dunkles Blaugrau

    # Extended Palette
    "primary_hover": "#8FB3AE",     # Slightly lighter for hover states
    "primary_glow": "#7BA5A088",    # 50% opacity for glow effects
    "surface_tint": "#F0F7F6",      # Very light mint background

    # Neutrals (warm, professional)
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",

    # Status Colors
    "success": "#10B981",  # Green
    "warning": "#F59E0B",  # Orange
    "info": "#3B82F6",     # Blue

    # Backgrounds
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F9FAFB",
    "surface": "#FFFFFF",
    "surface_elevated": "#FFFFFF",
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

RADIUS = {
    "sm": "0.375rem",   # 6px
    "md": "0.5rem",     # 8px
    "lg": "0.75rem",    # 12px
    "xl": "1rem",       # 16px
    "xxl": "1.5rem",    # 24px
    "full": "9999px",   # Fully rounded
}

SHADOWS = {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "glass": "0 8px 32px 0 rgba(123, 165, 160, 0.1)",
    "glow": f"0 0 20px {COLORS['primary_glow']}",
}

TYPOGRAPHY = {
    "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    "font_size_xs": "0.75rem",   # 12px
    "font_size_sm": "0.875rem",  # 14px
    "font_size_md": "1rem",      # 16px
    "font_size_lg": "1.125rem",  # 18px
    "font_size_xl": "1.25rem",   # 20px
    "font_size_2xl": "1.5rem",   # 24px
    "font_size_3xl": "1.875rem", # 30px
    "font_size_4xl": "2.25rem",  # 36px
}


# ==================== GLOBAL STYLES ====================
def apply_global_styles():
    """Apply global Evaluera theme styles to the entire app"""
    st.markdown(f"""
    <style>
        /* ===== GLOBAL RESET ===== */
        * {{
            box-sizing: border-box;
        }}

        /* ===== ROOT VARIABLES ===== */
        :root {{
            --primary: {COLORS['primary']};
            --primary-light: {COLORS['primary_light']};
            --primary-dark: {COLORS['primary_dark']};
            --primary-hover: {COLORS['primary_hover']};
            --error: {COLORS['error']};
            --bg-primary: {COLORS['bg_primary']};
            --surface: {COLORS['surface']};
        }}

        /* ===== STREAMLIT APP BACKGROUND ===== */
        .stApp {{
            background: {COLORS['bg_primary']};
            font-family: {TYPOGRAPHY['font_family']};
        }}

        /* ===== REMOVE BLACK ELEMENTS ===== */
        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS['error']} !important;
            font-weight: 600 !important;
        }}

        /* Paragraph text */
        p, span, div {{
            color: {COLORS['gray_700']} !important;
        }}

        /* ===== INPUT FIELDS - GLASS EFFECT ===== */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div {{
            background: rgba(255, 255, 255, 0.7) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid {COLORS['primary_light']} !important;
            border-radius: {RADIUS['md']} !important;
            color: {COLORS['error']} !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: {COLORS['primary']} !important;
            box-shadow: 0 0 0 3px {COLORS['primary_glow']}, {SHADOWS['md']} !important;
            outline: none !important;
        }}

        /* ===== BUTTONS - EVALUERA STYLE ===== */
        .stButton > button {{
            background: {COLORS['primary_dark']} !important;
            color: white !important;
            border: none !important;
            border-radius: {RADIUS['lg']} !important;
            padding: {SPACING['md']} {SPACING['xl']} !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: {SHADOWS['md']} !important;
        }}

        .stButton > button:hover {{
            background: {COLORS['primary_hover']} !important;
            transform: translateY(-2px) !important;
            box-shadow: {SHADOWS['lg']} !important;
        }}

        .stButton > button:active {{
            transform: translateY(0) !important;
        }}

        /* ===== DATAFRAME / TABLES ===== */
        .stDataFrame {{
            border: 1px solid {COLORS['primary_light']} !important;
            border-radius: {RADIUS['md']} !important;
        }}

        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['surface']} 0%, {COLORS['surface_tint']} 100%) !important;
            border-right: 1px solid {COLORS['primary_light']} !important;
        }}

        /* ===== PROGRESS BAR ===== */
        .stProgress > div > div > div {{
            background: {COLORS['primary']} !important;
        }}

        /* ===== EXPANDER ===== */
        .streamlit-expanderHeader {{
            background: {COLORS['surface_tint']} !important;
            border-radius: {RADIUS['md']} !important;
            color: {COLORS['error']} !important;
        }}

        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: {SPACING['sm']};
        }}

        .stTabs [data-baseweb="tab"] {{
            background: transparent !important;
            border-bottom: 2px solid transparent !important;
            color: {COLORS['gray_600']} !important;
            padding: {SPACING['md']} {SPACING['lg']} !important;
        }}

        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            border-bottom-color: {COLORS['primary']} !important;
            color: {COLORS['primary']} !important;
        }}

        /* ===== METRICS ===== */
        [data-testid="stMetricValue"] {{
            color: {COLORS['primary']} !important;
            font-weight: 700 !important;
        }}

        /* ===== SPINNER ===== */
        .stSpinner > div {{
            border-top-color: {COLORS['primary']} !important;
        }}

        /* ===== FILE UPLOADER ===== */
        .stFileUploader {{
            border: 2px dashed {COLORS['primary_light']} !important;
            border-radius: {RADIUS['lg']} !important;
            background: {COLORS['surface_tint']} !important;
        }}

        /* ===== REMOVE STREAMLIT BRANDING ===== */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)


# ==================== UTILITY FUNCTIONS ====================

def glass_card(content_html, padding="md"):
    """Create a glass-morphism card"""
    return f"""
    <div style="
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid {COLORS['primary_light']};
        border-radius: {RADIUS['lg']};
        padding: {SPACING[padding]};
        box-shadow: {SHADOWS['glass']};
        margin: {SPACING['md']} 0;
    ">
        {content_html}
    </div>
    """


def section_header(title, subtitle=None):
    """Create a consistent section header"""
    subtitle_html = f'<p style="color: {COLORS["gray_600"]}; margin-top: {SPACING["xs"]};">{subtitle}</p>' if subtitle else ""
    return f"""
    <div style="margin: {SPACING['xl']} 0 {SPACING['lg']} 0;">
        <h2 style="color: {COLORS['error']}; font-weight: 600; margin: 0;">{title}</h2>
        {subtitle_html}
    </div>
    """


def divider():
    """Create a subtle divider"""
    return f'<hr style="border: none; border-top: 1px solid {COLORS["primary_light"]}; margin: {SPACING["xl"]} 0;" />'


def badge(text, color="primary"):
    """Create a small badge"""
    bg_color = COLORS.get(color, COLORS["primary"])
    return f"""
    <span style="
        background: {bg_color};
        color: white;
        padding: {SPACING['xs']} {SPACING['sm']};
        border-radius: {RADIUS['full']};
        font-size: {TYPOGRAPHY['font_size_xs']};
        font-weight: 600;
        display: inline-block;
    ">{text}</span>
    """


def kpi_card(label, value, change=None):
    """Create a KPI card with optional change indicator"""
    change_html = ""
    if change:
        color = COLORS['success'] if change > 0 else COLORS['error']
        icon = "↑" if change > 0 else "↓"
        change_html = f'<span style="color: {color}; font-size: {TYPOGRAPHY["font_size_sm"]};">{icon} {abs(change)}%</span>'

    return f"""
    <div style="
        background: {COLORS['surface']};
        border: 1px solid {COLORS['primary_light']};
        border-radius: {RADIUS['lg']};
        padding: {SPACING['lg']};
        box-shadow: {SHADOWS['md']};
    ">
        <p style="color: {COLORS['gray_600']}; font-size: {TYPOGRAPHY['font_size_sm']}; margin: 0;">{label}</p>
        <h3 style="color: {COLORS['primary']}; font-weight: 700; margin: {SPACING['xs']} 0;">{value}</h3>
        {change_html}
    </div>
    """


def wizard_step(step_number, title, is_active=False, is_completed=False):
    """Create a wizard step indicator"""
    if is_completed:
        bg_color = COLORS['success']
        icon = "✓"
    elif is_active:
        bg_color = COLORS['primary']
        icon = str(step_number)
    else:
        bg_color = COLORS['gray_300']
        icon = str(step_number)

    return f"""
    <div style="display: flex; align-items: center; gap: {SPACING['md']};">
        <div style="
            width: 40px;
            height: 40px;
            border-radius: {RADIUS['full']};
            background: {bg_color};
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
        ">{icon}</div>
        <span style="color: {COLORS['error'] if is_active else COLORS['gray_600']}; font-weight: {'600' if is_active else '400'};">{title}</span>
    </div>
    """
