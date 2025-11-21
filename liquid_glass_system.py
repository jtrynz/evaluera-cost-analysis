"""
✨ EVALUERA - Liquid Glass Design System
=========================================
Apple-ähnliches Glassmorphism Design mit animierten Liquid-Effekten
"""

import streamlit as st
from ui_theme import COLORS, SPACING, RADIUS


def apply_liquid_glass_styles():
    """Apply global liquid glass CSS animations and effects"""
    st.markdown("""
    <style>
        /* ========== LIQUID GLASS ANIMATIONS ========== */
        @keyframes liquidMove {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }
            33% {
                transform: translate(30px, -30px) scale(1.1);
            }
            66% {
                transform: translate(-20px, 20px) scale(0.9);
            }
        }

        @keyframes liquidPulse {
            0%, 100% {
                opacity: 0.3;
            }
            50% {
                opacity: 0.6;
            }
        }

        @keyframes glassShine {
            0% {
                background-position: -200% center;
            }
            100% {
                background-position: 200% center;
            }
        }

        @keyframes floatSlow {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-20px);
            }
        }

        /* ========== LIQUID GLASS BACKGROUND ========== */
        .liquid-glass-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        .liquid-blob {
            position: absolute;
            border-radius: 50%;
            filter: blur(60px);
            opacity: 0.4;
            animation: liquidMove 20s ease-in-out infinite;
        }

        .liquid-blob-1 {
            width: 400px;
            height: 400px;
            background: linear-gradient(135deg, #B8D4D1 0%, #7BA5A0 100%);
            top: 10%;
            left: 10%;
            animation-duration: 25s;
        }

        .liquid-blob-2 {
            width: 350px;
            height: 350px;
            background: linear-gradient(135deg, #7BA5A0 0%, #2F4A56 100%);
            top: 50%;
            right: 15%;
            animation-duration: 30s;
            animation-delay: -5s;
        }

        .liquid-blob-3 {
            width: 300px;
            height: 300px;
            background: linear-gradient(135deg, #B8D4D1 0%, rgba(184, 212, 209, 0.5) 100%);
            bottom: 20%;
            left: 40%;
            animation-duration: 35s;
            animation-delay: -10s;
        }

        /* ========== GLASSMORPHISM CARD ========== */
        .glass-card {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(30px) saturate(150%);
            -webkit-backdrop-filter: blur(30px) saturate(150%);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow:
                0 8px 32px 0 rgba(31, 38, 135, 0.15),
                inset 0 0 0 1px rgba(255, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
        }

        .glass-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.3),
                transparent
            );
            animation: glassShine 3s ease-in-out infinite;
        }

        /* ========== FROSTED GLASS PANEL ========== */
        .frosted-panel {
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 2rem;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
        }

        /* ========== LIQUID GLASS HEADER ========== */
        .liquid-header {
            position: relative;
            background: linear-gradient(135deg,
                rgba(184, 212, 209, 0.2) 0%,
                rgba(123, 165, 160, 0.2) 100%
            );
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            padding: 1.5rem 2rem;
            border-radius: 0 0 24px 24px;
            overflow: hidden;
        }

        .liquid-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(
                circle,
                rgba(184, 212, 209, 0.3) 0%,
                transparent 70%
            );
            animation: liquidPulse 8s ease-in-out infinite;
        }

        /* ========== GLASS BUTTON ========== */
        .glass-button {
            background: rgba(47, 74, 86, 0.8);
            backdrop-filter: blur(10px);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 1rem 2rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 16px rgba(47, 74, 86, 0.2);
        }

        .glass-button:hover {
            background: rgba(47, 74, 86, 0.95);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(47, 74, 86, 0.3);
        }

        /* ========== FLOATING GLASS CARD ========== */
        .floating-glass {
            animation: floatSlow 6s ease-in-out infinite;
        }

        /* ========== FADE ANIMATIONS ========== */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: scale(0.95);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        @keyframes fadeOut {
            from {
                opacity: 1;
                transform: scale(1);
            }
            to {
                opacity: 0;
                transform: scale(0.95);
            }
        }

        .fade-in {
            animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }

        .fade-out {
            animation: fadeOut 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }

        /* ========== GLASS INPUT FIELDS ========== */
        .glass-input {
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            padding: 0.875rem 1.25rem;
            font-size: 1rem;
            color: #1a1a1a;
            transition: all 0.3s ease;
        }

        .glass-input:focus {
            outline: none;
            background: rgba(255, 255, 255, 0.7);
            border-color: rgba(123, 165, 160, 0.5);
            box-shadow: 0 0 0 3px rgba(123, 165, 160, 0.1);
        }

        /* ========== PREMIUM SIDEBAR GLASS ========== */
        [data-testid="stSidebar"] {
            background: linear-gradient(
                180deg,
                rgba(255, 255, 255, 0.7) 0%,
                rgba(245, 247, 250, 0.6) 100%
            );
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }
    </style>
    """, unsafe_allow_html=True)


def render_liquid_background():
    """Render animated liquid glass background"""
    st.markdown("""
    <div class="liquid-glass-bg">
        <div class="liquid-blob liquid-blob-1"></div>
        <div class="liquid-blob liquid-blob-2"></div>
        <div class="liquid-blob liquid-blob-3"></div>
    </div>
    """, unsafe_allow_html=True)


def glass_card(content: str, floating: bool = False):
    """
    Create a glassmorphism card

    Args:
        content: HTML content
        floating: Enable floating animation
    """
    float_class = "floating-glass" if floating else ""
    st.markdown(f"""
    <div class="glass-card {float_class} fade-in">
        {content}
    </div>
    """, unsafe_allow_html=True)


def frosted_panel(content: str):
    """
    Create a frosted glass panel

    Args:
        content: HTML content
    """
    st.markdown(f"""
    <div class="frosted-panel fade-in">
        {content}
    </div>
    """, unsafe_allow_html=True)


def liquid_header(title: str, subtitle: str = None):
    """
    Create a liquid glass header

    Args:
        title: Header title
        subtitle: Optional subtitle
    """
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <p style="
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
            color: rgba(26, 26, 26, 0.7);
            font-weight: 400;
        ">{subtitle}</p>
        """

    st.markdown(f"""
    <div class="liquid-header">
        <h1 style="
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
            letter-spacing: 0.05em;
            color: #1a1a1a;
        ">{title}</h1>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def glass_metric_card(label: str, value: str, icon: str = None):
    """
    Premium glass metric card

    Args:
        label: Metric label
        value: Metric value
        icon: Optional emoji icon
    """
    icon_html = f"<span style='font-size: 2rem; margin-bottom: 0.5rem;'>{icon}</span>" if icon else ""

    content = f"""
    <div style="padding: 1.5rem; text-align: center;">
        {icon_html}
        <div style="
            font-size: 0.875rem;
            color: rgba(26, 26, 26, 0.6);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
            font-weight: 600;
        ">{label}</div>
        <div style="
            font-size: 2.25rem;
            font-weight: 700;
            color: #1a1a1a;
            letter-spacing: -0.02em;
        ">{value}</div>
    </div>
    """
    glass_card(content, floating=True)
