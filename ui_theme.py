"""
🎨 EVALUERA - Modern UI Theme System
=====================================
Apple-inspired minimal design with consistent components
"""

import streamlit as st

# ==================== DESIGN TOKENS ====================
COLORS = {
    # Primary
    "primary": "#7c3aed",  # Lila
    "primary_light": "#a78bfa",
    "primary_dark": "#5b21b6",

    # Neutrals
    "gray_50": "#fafafa",
    "gray_100": "#f4f4f5",
    "gray_200": "#e4e4e7",
    "gray_300": "#d4d4d8",
    "gray_400": "#a1a1aa",
    "gray_500": "#71717a",
    "gray_600": "#52525b",
    "gray_700": "#3f3f46",
    "gray_800": "#27272a",
    "gray_900": "#18181b",

    # Status
    "success": "#22c55e",
    "warning": "#eab308",
    "error": "#ef4444",
    "info": "#3b82f6",

    # Backgrounds
    "bg_primary": "#ffffff",
    "bg_secondary": "#fafafa",
    "surface": "#ffffff",
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
    "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "h1": "2rem",
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
    "sm": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
}


def apply_global_styles():
    """Apply global CSS theme"""
    st.markdown(f"""
    <style>
        /* Global Resets */
        .main {{
            background-color: {COLORS['bg_secondary']};
            font-family: {TYPOGRAPHY['font_family']};
        }}

        /* Hide Streamlit Branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Container Max Width for Readability */
        .block-container {{
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        /* Typography */
        h1 {{
            font-size: {TYPOGRAPHY['h1']};
            font-weight: 700;
            color: {COLORS['gray_900']};
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

        p {{
            color: {COLORS['gray_600']};
            line-height: 1.6;
            max-width: 700px;
        }}

        /* Custom Scrollbar */
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

        /* Streamlit Elements Override */
        .stButton > button {{
            border-radius: {RADIUS['md']};
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .stSelectbox {{
            border-radius: {RADIUS['md']};
        }}

        /* Expander Styling */
        .streamlit-expanderHeader {{
            background-color: {COLORS['surface']};
            border-radius: {RADIUS['md']};
            border: 1px solid {COLORS['gray_200']};
            font-weight: 500;
        }}

        /* Metric Card Override */
        div[data-testid="stMetricValue"] {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {COLORS['gray_900']};
        }}
    </style>
    """, unsafe_allow_html=True)


# ==================== COMPONENT LIBRARY ====================

def card(content, padding="md", hover=False, border=True):
    """
    Minimal card component

    Args:
        content: HTML content
        padding: xs, sm, md, lg, xl
        hover: Enable hover effect
        border: Show border
    """
    hover_style = "transition: transform 0.2s ease, box-shadow 0.2s ease;" if hover else ""
    hover_class = "transform: translateY(-2px); box-shadow: " + SHADOWS['lg'] if hover else ""
    border_style = f"border: 1px solid {COLORS['gray_200']};" if border else ""

    st.markdown(f"""
    <div style="
        background: {COLORS['surface']};
        {border_style}
        border-radius: {RADIUS['md']};
        padding: {SPACING[padding]};
        box-shadow: {SHADOWS['sm']};
        {hover_style}
    " onmouseover="this.style.cssText=this.style.cssText.replace('box-shadow: {SHADOWS['sm']}', 'box-shadow: {SHADOWS['md']}')"
       onmouseout="this.style.cssText=this.style.cssText.replace('box-shadow: {SHADOWS['md']}', 'box-shadow: {SHADOWS['sm']}')">
        {content}
    </div>
    """, unsafe_allow_html=True)


def button(label, variant="primary", icon=None, disabled=False):
    """
    Consistent button component

    Args:
        label: Button text
        variant: primary, secondary, ghost
        icon: Optional emoji/icon
        disabled: Disable button
    """
    if variant == "primary":
        bg = COLORS['primary']
        text = "#ffffff"
        border = "none"
        hover_bg = COLORS['primary_dark']
    elif variant == "secondary":
        bg = COLORS['gray_100']
        text = COLORS['gray_900']
        border = f"1px solid {COLORS['gray_300']}"
        hover_bg = COLORS['gray_200']
    else:  # ghost
        bg = "transparent"
        text = COLORS['gray_700']
        border = "none"
        hover_bg = COLORS['gray_100']

    icon_html = f"<span style='margin-right: 0.5rem;'>{icon}</span>" if icon else ""
    opacity = "0.5" if disabled else "1"
    cursor = "not-allowed" if disabled else "pointer"

    return f"""
    <button style="
        background: {bg};
        color: {text};
        border: {border};
        border-radius: {RADIUS['md']};
        padding: 0.75rem 1.5rem;
        font-size: {TYPOGRAPHY['body']};
        font-weight: 500;
        cursor: {cursor};
        opacity: {opacity};
        transition: all 0.2s ease;
        font-family: {TYPOGRAPHY['font_family']};
    " {'disabled' if disabled else ''}
       onmouseover="this.style.background='{hover_bg}'"
       onmouseout="this.style.background='{bg}'">
        {icon_html}{label}
    </button>
    """


def kpi_card(label, value, icon=None, help_text=None, trend=None):
    """
    Compact KPI card for metrics

    Args:
        label: Metric name
        value: Metric value
        icon: Optional emoji
        help_text: Optional tooltip
        trend: Optional trend (positive/negative/neutral)
    """
    icon_html = f"<span style='font-size: 1.5rem; margin-right: 0.75rem;'>{icon}</span>" if icon else ""
    help_html = f"<div style='font-size: {TYPOGRAPHY['tiny']}; color: {COLORS['gray_400']}; margin-top: 0.25rem;'>{help_text}</div>" if help_text else ""

    trend_html = ""
    if trend:
        if trend == "positive":
            trend_html = f"<span style='color: {COLORS['success']}; font-size: {TYPOGRAPHY['small']};'>↑</span>"
        elif trend == "negative":
            trend_html = f"<span style='color: {COLORS['error']}; font-size: {TYPOGRAPHY['small']};'>↓</span>"

    content = f"""
    <div style="display: flex; align-items: center;">
        {icon_html}
        <div style="flex: 1;">
            <div style="font-size: {TYPOGRAPHY['tiny']}; color: {COLORS['gray_500']}; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                {label}
            </div>
            <div style="font-size: 1.5rem; font-weight: 700; color: {COLORS['gray_900']};">
                {value} {trend_html}
            </div>
            {help_html}
        </div>
    </div>
    """

    card(content, padding="md")


def wizard_step(step_number, title, description, is_active, is_completed):
    """
    Wizard step indicator

    Args:
        step_number: 1-6
        title: Step title
        description: Step description
        is_active: Currently active step
        is_completed: Step completed
    """
    if is_completed:
        bg = COLORS['success']
        text_color = "#ffffff"
        icon = "✓"
    elif is_active:
        bg = COLORS['primary']
        text_color = "#ffffff"
        icon = str(step_number)
    else:
        bg = COLORS['gray_200']
        text_color = COLORS['gray_500']
        icon = str(step_number)

    return f"""
    <div style="display: flex; align-items: center; gap: 1rem; padding: {SPACING['md']}; margin-bottom: {SPACING['sm']};
                background: {COLORS['surface']}; border-radius: {RADIUS['md']};
                border: 2px solid {bg if is_active else COLORS['gray_200']};
                opacity: {1 if (is_active or is_completed) else 0.6};">
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
            font-size: {TYPOGRAPHY['body']};
        ">
            {icon}
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 600; color: {COLORS['gray_900']}; font-size: {TYPOGRAPHY['body']};">
                {title}
            </div>
            <div style="font-size: {TYPOGRAPHY['small']}; color: {COLORS['gray_500']};">
                {description}
            </div>
        </div>
    </div>
    """


def status_badge(text, variant="info"):
    """
    Compact status badge

    Args:
        text: Badge text
        variant: success, warning, error, info
    """
    colors_map = {
        "success": COLORS['success'],
        "warning": COLORS['warning'],
        "error": COLORS['error'],
        "info": COLORS['info'],
    }

    color = colors_map.get(variant, COLORS['info'])

    return f"""
    <span style="
        background: {color}20;
        color: {color};
        padding: 0.25rem 0.75rem;
        border-radius: {RADIUS['full']};
        font-size: {TYPOGRAPHY['small']};
        font-weight: 500;
    ">
        {text}
    </span>
    """


def section_header(title, subtitle=None):
    """Section header with optional subtitle"""
    subtitle_html = f"<p style='color: {COLORS['gray_500']}; margin-top: 0.5rem; font-size: {TYPOGRAPHY['body']};'>{subtitle}</p>" if subtitle else ""

    st.markdown(f"""
    <div style="margin-bottom: {SPACING['lg']};">
        <h2 style="color: {COLORS['gray_900']}; font-weight: 700; margin: 0;">{title}</h2>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def divider():
    """Minimal divider"""
    st.markdown(f"""
    <div style="
        height: 1px;
        background: {COLORS['gray_200']};
        margin: {SPACING['xl']} 0;
    "></div>
    """, unsafe_allow_html=True)


def loading_spinner(text="Lädt..."):
    """Minimal loading spinner"""
    return f"""
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        padding: {SPACING['xl']};
    ">
        <div style="
            width: 24px;
            height: 24px;
            border: 3px solid {COLORS['gray_200']};
            border-top-color: {COLORS['primary']};
            border-radius: {RADIUS['full']};
            animation: spin 1s linear infinite;
        "></div>
        <span style="color: {COLORS['gray_600']};">{text}</span>
    </div>

    <style>
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
    """
