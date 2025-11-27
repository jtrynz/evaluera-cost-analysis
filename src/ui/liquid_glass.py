"""
✨ EVALUERA - Liquid Glass Design System
=========================================
Apple-ähnliches Glassmorphism-Design mit Evaluera-Farben
"""

import streamlit as st
from src.ui.theme import COLORS, SPACING, RADIUS


def apply_liquid_glass_styles():
    """Globales Liquid-Glass-CSS mit Evaluera-Farben"""
    st.markdown(f"""
    <style>
        /* ========== LIQUID GLASS ANIMATIONS ========== */
        @keyframes liquidMove {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            33%       {{ transform: translate(30px, -30px) scale(1.08); }}
            66%       {{ transform: translate(-20px, 20px) scale(0.96); }}
        }}

        @keyframes liquidPulse {{
            0%, 100% {{ opacity: 0.25; }}
            50%      {{ opacity: 0.55; }}
        }}

        @keyframes glassShine {{
            0%   {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}

        @keyframes floatSlow {{
            0%, 100% {{ transform: translateY(0px); }}
            50%      {{ transform: translateY(-14px); }}
        }}

        /* ========== LIQUID GLASS BACKGROUND (hell, Evaluera) ========== */
        .liquid-glass-bg {{
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            overflow: hidden;
            background: radial-gradient(circle at top left,
                        {COLORS.get('accent_soft', '#B8D4D1')} 0%,
                        {COLORS.get('bg_app', '#F5F7F8')} 40%,
                        #FFFFFF 100%);
        }}

        .liquid-blob {{
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.45;
            animation: liquidMove 24s ease-in-out infinite;
        }}

        .liquid-blob-1 {{
            width: 420px;
            height: 420px;
            background: radial-gradient(circle at 0% 0%,
                        {COLORS['primary']} 0%,
                        rgba(255,255,255,0) 70%);
            top: 8%;
            left: 6%;
            animation-duration: 26s;
        }}

        .liquid-blob-2 {{
            width: 380px;
            height: 380px;
            background: radial-gradient(circle at 100% 0%,
                        {COLORS['dark_accent']} 0%,
                        rgba(255,255,255,0) 70%);
            top: 18%;
            right: 8%;
            animation-duration: 32s;
            animation-delay: -4s;
        }}

        .liquid-blob-3 {{
            width: 360px;
            height: 360px;
            background: radial-gradient(circle at 50% 100%,
                        {COLORS['secondary']} 0%,
                        rgba(255,255,255,0) 70%);
            bottom: 4%;
            left: 35%;
            animation-duration: 38s;
            animation-delay: -9s;
        }}

        /* ========== GLASSMORPHISM CARD ========== */
        .glass-card {{
            background: rgba(255, 255, 255, 0.78);
            backdrop-filter: blur(28px) saturate(150%);
            -webkit-backdrop-filter: blur(28px) saturate(150%);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.7);
            box-shadow:
                0 18px 45px rgba(15, 23, 42, 0.18),
                inset 0 0 0 1px rgba(255, 255, 255, 0.5);
            position: relative;
            overflow: hidden;
        }}

        .glass-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -120%;
            width: 60%;
            height: 100%;
            background: linear-gradient(
                120deg,
                transparent,
                rgba(255, 255, 255, 0.55),
                transparent
            );
            background-size: 200% 100%;
            animation: glassShine 4s ease-in-out infinite;
        }}

        /* ========== FROSTED GLASS PANEL ========== */
        .frosted-panel {{
            background: rgba(255, 255, 255, 0.82);
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.7);
            padding: 2rem;
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.16);
        }}

        /* ========== LIQUID GLASS HEADER ========== */
        .liquid-header {{
            position: relative;
            background: linear-gradient(135deg,
                rgba(184, 212, 209, 0.7) 0%,
                rgba(123, 165, 160, 0.65) 40%,
                rgba(255, 255, 255, 0.9) 100%
            );
            backdrop-filter: blur(22px);
            -webkit-backdrop-filter: blur(22px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.9);
            padding: 1.6rem 2.2rem;
            border-radius: 0 0 24px 24px;
            overflow: hidden;
        }}

        .liquid-header::before {{
            content: '';
            position: absolute;
            top: -40%;
            left: -30%;
            width: 60%;
            height: 180%;
            background: radial-gradient(
                circle,
                rgba(255, 255, 255, 0.7) 0%,
                transparent 70%
            );
            animation: liquidPulse 8s ease-in-out infinite;
        }}

        /* ========== FLOATING GLASS ================== */
        .floating-glass {{
            animation: floatSlow 7s ease-in-out infinite;
        }}

        /* ========== FADE ANIMATIONS ========== */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: scale(0.97); }}
            to   {{ opacity: 1; transform: scale(1); }}
        }}

        .fade-in {{
            animation: fadeIn 0.55s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }}
    </style>
    """, unsafe_allow_html=True)


def render_liquid_background():
    """Render Evaluera-Liquid-Background"""
    st.markdown(
        """
        <div class="liquid-glass-bg">
            <div class="liquid-blob liquid-blob-1"></div>
            <div class="liquid-blob liquid-blob-2"></div>
            <div class="liquid-blob liquid-blob-3"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_card(content: str, floating: bool = False):
    """Glassmorphism-Card"""
    float_class = "floating-glass" if floating else ""
    st.markdown(
        f"""
        <div class="glass-card {float_class} fade-in">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def frosted_panel(content: str):
    """Frosted-Glass-Panel"""
    st.markdown(
        f"""
        <div class="frosted-panel fade-in">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def liquid_header(title: str, subtitle: str = None):
    """Liquid-Glass-Header mit Evaluera-Branding"""
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <p style="
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
            color: rgba(17, 24, 39, 0.7);
            font-weight: 400;
        ">{subtitle}</p>
        """

    st.markdown(
        f"""
        <div class="liquid-header">
            <h1 style="
                margin: 0;
                font-size: 2.4rem;
                font-weight: 300;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                color: {COLORS['primary']};
            ">{title}</h1>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_metric_card(label: str, value: str, icon: str = None):
    """Premium Glass-Metric-Card"""
    icon_html = (
        f"<span style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</span>"
        if icon
        else ""
    )
    content = f"""
    <div style="padding: 1.5rem; text-align: center;">
        {icon_html}
        <div style="
            font-size: 0.8rem;
            color: rgba(55, 65, 81, 0.7);
            text-transform: uppercase;
            letter-spacing: 0.16em;
            margin-bottom: 0.4rem;
            font-weight: 600;
        ">{label}</div>
        <div style="
            font-size: 2.1rem;
            font-weight: 700;
            color: {COLORS['primary']};
            letter-spacing: -0.03em;
        ">{value}</div>
    </div>
    """
    glass_card(content, floating=True)