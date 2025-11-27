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

        /* ========== INPUT FIELDS (CLEAN EVALUERA STYLE) ========== */
        /* Remove all default/red glows */
        input, textarea, select {{
            box-shadow: none !important;
            outline: none !important;
        }}
        input:focus, input:focus-visible, input:active {{
            outline: none !important;
            box-shadow: none !important;
        }}
        input:invalid, input:invalid:focus, input:user-invalid, input:user-invalid:focus {{
            box-shadow: none !important;
            outline: none !important;
            border-color: {COLORS['primary']} !important;
        }}

        /* BaseWeb Input wrapper */
        div[data-baseweb="input"] {{
            border: 1.8px solid rgba(42, 79, 87, 0.35) !important;
            border-radius: 10px !important;
            min-height: 48px !important;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.06) !important;
            background: rgba(255, 255, 255, 0.95) !important;
            transition: all 0.2s ease !important;
            overflow: hidden !important;
        }}

        /* Inner padding + alignment */
        div[data-baseweb="input"] > div {{
            padding: 0 12px !important;
            align-items: center !important;
        }}

        /* Actual input */
        div[data-baseweb="input"] input {{
            height: 46px !important;
            padding: 0 8px !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            color: {COLORS['dark_accent']} !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }}

        /* Focus in brand color */
        div[data-baseweb="input"]:focus-within {{
            border-color: {COLORS['primary']} !important;
            box-shadow:
                0 0 0 2px rgba(42, 79, 87, 0.18),
                0 6px 16px rgba(0, 0, 0, 0.08) !important;
            background: rgba(255, 255, 255, 0.98) !important;
        }}

        /* Hard override any invalid/red glow */
        div[data-baseweb="input"][aria-invalid="true"],
        div[data-baseweb="input"][aria-invalid="true"]:focus-within,
        div[data-baseweb="input"] input[aria-invalid="true"],
        div[data-baseweb="input"] input[aria-invalid="true"]:focus,
        .stTextInput input:invalid,
        .stTextInput input:invalid:focus,
        .stTextInput input:user-invalid,
        .stTextInput input:user-invalid:focus {{
            border-color: {COLORS['primary']} !important;
            box-shadow:
                0 0 0 2px rgba(42, 79, 87, 0.18) !important;
            outline: none !important;
        }}

        /* Strip any leftover default focus glow */
        div[data-baseweb="input"] input:focus,
        div[data-baseweb="input"] input:focus-visible,
        div[data-baseweb="input"] input:active {{
            box-shadow: none !important;
            outline: none !important;
        }}

        /* Ultimate override: kill any red glow/outline */
        input,
        input:focus,
        input:focus-visible,
        input:active,
        input:invalid,
        input:invalid:focus,
        input:user-invalid,
        input:user-invalid:focus,
        div[data-baseweb="input"],
        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="input"] * {{
            outline: none !important;
            box-shadow: none !important;
            -webkit-box-shadow: none !important;
            -moz-box-shadow: none !important;
        }}

        input,
        input:focus,
        input:focus-visible,
        input:active,
        input:invalid,
        input:invalid:focus,
        input:user-invalid,
        input:user-invalid:focus {{
            border-color: {COLORS['primary']} !important;
            border-width: 2px !important;
        }}

        /* Labels and placeholder */
        .stTextInput > label,
        .stNumberInput > label,
        .stTextArea > label,
        .stSelectbox > label {{
            color: {COLORS['dark_accent']} !important;
            font-weight: 600 !important;
            margin-bottom: 6px !important;
        }}
        div[data-baseweb="input"] input::placeholder {{
            color: rgba(30, 46, 50, 0.6) !important;
            font-weight: 400 !important;
        }}

        /* Password eye icon: align or hide if desired */
        button[aria-label="Show password"],
        button[aria-label="Hide password"] {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            width: 36px !important;
            height: 36px !important;
            margin-right: 6px !important;
            color: {COLORS['primary']} !important;
        }}
        button[aria-label="Show password"]:focus,
        button[aria-label="Hide password"]:focus {{
            box-shadow: none !important;
            outline: none !important;
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

        /* ========== SIDEBAR (CALM VISION OS) ========== */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(0, 0, 0, 0.05) !important;
            box-shadow: 20px 0 40px rgba(0, 0, 0, 0.02) !important;
        }}

        /* Sidebar User Profile / Footer Area (if any) */
        [data-testid="stSidebar"] .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }}

        /* ========== SIDEBAR NAVIGATION ITEMS (Secondary Buttons) ========== */
        /* Transform standard buttons into Menu Items */
        [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"] {{
            background: transparent !important;
            border: 1px solid transparent !important;
            color: #374151 !important; /* Gray 700 */
            border-radius: 12px !important;
            padding: 10px 16px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-align: left !important;
            display: flex !important;
            justify-content: flex-start !important;
            width: 100% !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
            margin-bottom: 4px !important;
        }}

        /* Hover State for Nav Items */
        [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"]:hover {{
            background: rgba(167, 255, 229, 0.15) !important; /* Very light Mint */
            color: #2A4F57 !important; /* Deep Teal */
            transform: translateX(4px) !important;
        }}

        /* Active/Focus State (Simulated) */
        [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-secondary"]:focus {{
            background: rgba(167, 255, 229, 0.25) !important;
            color: #2A4F57 !important;
            border-color: transparent !important;
            box-shadow: none !important;
        }}

        /* ========== SIDEBAR CTA (Primary Button - e.g. Upload) ========== */
        [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {{
            background: linear-gradient(135deg, #2A4F57 0%, #1C1F1E 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 20px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(42, 79, 87, 0.2) !important;
            transition: all 0.2s ease !important;
            margin-bottom: 24px !important; /* Spacing after main CTA */
        }}

        [data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"]:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(42, 79, 87, 0.3) !important;
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

        /* ========== PREMIUM GLASS EFFECT UTILITIES ========== */
        /* Subtle glass card - for main content areas */
        .glass-card-subtle {{
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px) saturate(110%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(110%) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            border-radius: {RADIUS['lg']} !important;
            box-shadow: 
                0 8px 32px rgba(42, 79, 87, 0.08),
                inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .glass-card-subtle:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 
                0 12px 40px rgba(42, 79, 87, 0.12),
                inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
        }}

        /* Strong glass card - for important components */
        .glass-card-strong {{
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(28px) saturate(120%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(120%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: {RADIUS['xl']} !important;
            box-shadow: 
                0 12px 40px rgba(42, 79, 87, 0.10),
                inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}

        .glass-card-strong:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 
                0 16px 48px rgba(42, 79, 87, 0.14),
                inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        }}

        /* Legacy glass classes (keep for backward compatibility) */
        .glass {{
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(20px) saturate(110%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(110%) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 8px 32px rgba(42, 79, 87, 0.08) !important;
        }}

        .glass-strong {{
            background: rgba(255, 255, 255, 0.95) !important;
            backdrop-filter: blur(28px) saturate(120%) !important;
            -webkit-backdrop-filter: blur(28px) saturate(120%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            box-shadow: 0 12px 40px rgba(42, 79, 87, 0.10) !important;
        }}

        /* Premium content container */
        .premium-content-container {{
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(24px) saturate(115%);
            -webkit-backdrop-filter: blur(24px) saturate(115%);
            border: 1px solid rgba(255, 255, 255, 0.7);
            border-radius: {RADIUS['xl']};
            padding: {SPACING['xl']};
            box-shadow: 
                0 10px 36px rgba(42, 79, 87, 0.09),
                inset 0 1px 0 rgba(255, 255, 255, 0.5);
            margin-bottom: {SPACING['lg']};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .premium-content-container:hover {{
            box-shadow: 
                0 14px 44px rgba(42, 79, 87, 0.11),
                inset 0 1px 0 rgba(255, 255, 255, 0.7);
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
