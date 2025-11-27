"""
🎨 EVALUERA - VisionOS Design System
====================================
Premium Apple-inspired design with advanced glassmorphism,
mint accents, and calm typography.
"""

import streamlit as st

# ==================== COLOR PALETTE (VISION OS / MINT) ====================
COLORS = {
    # Brand Colors
    "primary": "#2A4F57",        # Deep Teal (Text, Primary Actions)
    "primary_dark": "#1C353A",   # Darker Teal for hover/active
    "accent": "#A7FFE5",         # Bright Mint (Highlights, Focus)
    "accent_soft": "#B8D4D1",    # Soft Mint (Secondary, Backgrounds)
    "accent_glass": "rgba(167, 255, 229, 0.15)", # Mint Glass Tint

    # Neutrals
    "bg_app": "#F5F7F8",         # Very light cool gray/white
    "surface": "#FFFFFF",        # Pure white surface
    "text_main": "#111827",      # Almost black (Gray 900)
    "text_secondary": "#4B5563", # Gray 600
    "text_tertiary": "#9CA3AF",  # Gray 400
    "border_light": "rgba(255, 255, 255, 0.6)",
    "border_medium": "rgba(0, 0, 0, 0.06)",

    # Semantic
    "success": "#059669",        # Emerald 600
    "warning": "#D97706",        # Amber 600
    "error": "#DC2626",          # Red 600
    "info": "#2563EB",           # Blue 600
}

SPACING = {
    "xs": "0.25rem",    # 4px
    "sm": "0.5rem",     # 8px
    "md": "1rem",       # 16px
    "lg": "1.5rem",     # 24px
    "xl": "2.5rem",     # 40px
    "xxl": "4rem",      # 64px
}

RADIUS = {
    "sm": "8px",
    "md": "16px",       # Standard UI elements
    "lg": "24px",       # Cards
    "xl": "32px",       # Large containers
    "full": "9999px",
}

SHADOWS = {
    "sm": "0 1px 2px rgba(0, 0, 0, 0.04)",
    "md": "0 4px 12px rgba(0, 0, 0, 0.06)",
    "lg": "0 12px 32px rgba(0, 0, 0, 0.08)",
    "glass": "0 8px 32px 0 rgba(31, 38, 135, 0.07)",
    "glow": f"0 0 20px {COLORS['accent_glass']}",
}

TYPOGRAPHY = {
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif",
    "h1": "2.5rem",
    "h2": "1.75rem",
    "h3": "1.25rem",
    "body": "1rem",
    "small": "0.875rem",
}


# ==================== GLOBAL STYLES ====================
def apply_global_styles():
    """Inject global CSS for the VisionOS theme"""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* RESET & BASE */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: {TYPOGRAPHY['font_family']} !important;
            color: {COLORS['text_main']} !important;
            background-color: {COLORS['bg_app']} !important;
            -webkit-font-smoothing: antialiased;
        }}

        /* BACKGROUND GRADIENT (Subtle Vignette) */
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: radial-gradient(circle at 50% 0%, #FFFFFF 0%, {COLORS['bg_app']} 100%);
            z-index: -1;
            pointer-events: none;
        }}

        /* TYPOGRAPHY */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS['primary']} !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em !important;
        }}
        
        p, div, span, label {{
            color: {COLORS['text_secondary']};
            line-height: 1.6;
        }}

        /* SIDEBAR (Glass Panel) */
        [data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.75) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border-right: 1px solid {COLORS['border_medium']} !important;
            box-shadow: {SHADOWS['md']} !important;
        }}
        
        [data-testid="stSidebar"] .block-container {{
            padding-top: 2rem !important;
        }}

        /* BUTTONS (Primary - Dark Gradient) */
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: {RADIUS['md']} !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 500 !important;
            box-shadow: {SHADOWS['md']}, inset 0 1px 0 rgba(255,255,255,0.2) !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button[kind="primary"]:hover {{
            transform: translateY(-2px) !important;
            box-shadow: {SHADOWS['lg']}, 0 0 15px {COLORS['accent_glass']} !important;
        }}

        /* BUTTONS (Secondary - Glass) */
        .stButton > button[kind="secondary"] {{
            background: rgba(255, 255, 255, 0.5) !important;
            border: 1px solid {COLORS['border_medium']} !important;
            color: {COLORS['text_main']} !important;
            border-radius: {RADIUS['md']} !important;
            backdrop-filter: blur(10px) !important;
        }}

        /* INPUTS (Minimalist) */
        .stTextInput > div[data-baseweb="input"] {{
            background-color: rgba(255, 255, 255, 0.6) !important;
            border: 1px solid {COLORS['border_medium']} !important;
            border-radius: {RADIUS['md']} !important;
            transition: all 0.2s ease !important;
        }}
        
        .stTextInput > div[data-baseweb="input"]:focus-within {{
            background-color: white !important;
            border-color: {COLORS['accent']} !important;
            box-shadow: 0 0 0 3px {COLORS['accent_glass']} !important;
        }}

        /* HIDE STREAMLIT BRANDING */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* SCROLLBAR */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: transparent;
        }}
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['border_medium']};
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['text_tertiary']};
        }}
    </style>
    """, unsafe_allow_html=True)


# ==================== COMPONENTS ====================

def card(content, padding="lg", glass=True):
    """
    Liquid Glass Card Component
    """
    bg_style = f"""
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(24px) saturate(140%);
        -webkit-backdrop-filter: blur(24px) saturate(140%);
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: {SHADOWS['glass']};
    """ if glass else f"background: {COLORS['surface']}; border: 1px solid {COLORS['border_medium']};"

    st.markdown(f"""
    <div style="
        {bg_style}
        border-radius: {RADIUS['lg']};
        padding: {SPACING[padding]};
        margin-bottom: {SPACING['md']};
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    " onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='{SHADOWS['lg']}';" 
       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='{SHADOWS['glass']}';">
        {content}
    </div>
    """, unsafe_allow_html=True)


def section_header(title, subtitle=None):
    """
    Clean Section Header
    """
    st.markdown(f"""
    <div style="margin-bottom: {SPACING['lg']}; margin-top: {SPACING['md']};">
        <h2 style="margin: 0; font-size: {TYPOGRAPHY['h2']}; color: {COLORS['primary']};">{title}</h2>
        {f'<p style="margin-top: 4px; color: {COLORS["text_secondary"]}; font-size: {TYPOGRAPHY["body"]};">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def wizard_step(step_number, title, description, is_active, is_completed):
    """
    Minimalist Wizard Step Indicator
    """
    if is_completed:
        icon_bg = COLORS['success']
        icon_content = "✓"
        opacity = 1.0
        border = f"1px solid {COLORS['success']}"
    elif is_active:
        icon_bg = COLORS['primary']
        icon_content = str(step_number)
        opacity = 1.0
        border = f"1px solid {COLORS['primary']}"
    else:
        icon_bg = COLORS['border_medium']
        icon_content = str(step_number)
        opacity = 0.5
        border = "1px solid transparent"

    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: {RADIUS['md']};
        border: {border};
        margin-bottom: 8px;
        opacity: {opacity};
        transition: all 0.3s ease;
    ">
        <div style="
            width: 32px; height: 32px;
            background: {icon_bg};
            color: white;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-weight: 600; font-size: 14px;
            margin-right: 12px;
        ">
            {icon_content}
        </div>
        <div>
            <div style="font-weight: 600; color: {COLORS['primary']}; font-size: 14px;">{title}</div>
            <div style="font-size: 12px; color: {COLORS['text_secondary']};">{description}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown(f'<div style="height: 1px; background: {COLORS["border_medium"]}; margin: {SPACING["lg"]} 0;"></div>', unsafe_allow_html=True)


def status_badge(text, variant="info"):
    color = COLORS.get(variant, COLORS['info'])
    st.markdown(f"""
    <span style="
        background-color: {color}20;
        color: {color};
        padding: 4px 10px;
        border-radius: {RADIUS['full']};
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    ">{text}</span>
    """, unsafe_allow_html=True)
