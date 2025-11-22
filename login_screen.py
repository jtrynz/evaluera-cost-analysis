"""
🔐 EVALUERA - Premium Apple-Like Login Screen
==============================================
Modern, secure login with dark gradient, glassmorphism, and UX optimizations
"""

import streamlit as st
import json
from pathlib import Path
from ui_theme import COLORS, RADIUS, SPACING, SHADOWS, TYPOGRAPHY


# ==================== CREDENTIALS ====================
VALID_CREDENTIALS = {
    "admin": "evaluera2024",
    "demo": "demo123",
    "user": "password"
}


# ==================== AUTHENTICATION ====================
def check_login():
    """Check if user is logged in"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in


def login(username: str, password: str) -> bool:
    """
    Validate login credentials

    Args:
        username: Username
        password: Password

    Returns:
        True if valid, False otherwise
    """
    if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False


def logout():
    """Logout user and clear session"""
    st.session_state.logged_in = False
    if "username" in st.session_state:
        del st.session_state.username
    st.rerun()


# ==================== APPLE-LIKE PREMIUM LOGIN SCREEN ====================
def render_login_screen():
    """
    Render Apple-inspired premium login screen with:
    - Dark gradient animated background
    - Glassmorphism card effect
    - Caps Lock warning
    - Input validation
    - Smooth animations
    """

    # STEP 1: Inject Apple-Like Login CSS with Dark Gradient Background
    st.markdown(f"""
    <style>
        /* ========== IMPORT SF PRO FONT (APPLE) ========== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Override Streamlit body to use Apple font */
        body, html, * {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Inter', 'Segoe UI', sans-serif !important;
        }}

        /* ========== DARK GRADIENT ANIMATED BACKGROUND ========== */
        .login-background {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;
            z-index: -1 !important;
            background: radial-gradient(
                ellipse at 50% 50%,
                {COLORS['primary']} 0%,
                {COLORS['dark_primary']} 35%,
                {COLORS['dark_deep']} 70%,
                {COLORS['dark_overlay']} 100%
            ) !important;
            animation: gradientShift 15s ease-in-out infinite !important;
        }}

        /* Subtle gradient animation */
        @keyframes gradientShift {{
            0%, 100% {{
                background-position: 0% 50%;
                filter: hue-rotate(0deg);
            }}
            50% {{
                background-position: 100% 50%;
                filter: hue-rotate(5deg);
            }}
        }}

        /* Noise overlay for texture */
        .login-background::before {{
            content: '';
            position: absolute;
            inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
            pointer-events: none;
        }}

        /* ========== APPLE GLASSMORPHISM LOGIN CONTAINER ========== */
        .login-container {{
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            z-index: 99999 !important;
            width: 90% !important;
            max-width: 460px !important;
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards !important;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translate(-50%, -45%) scale(0.92);
            }}
            to {{
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }}
        }}

        /* ========== FROSTED GLASS PANEL (ENHANCED) ========== */
        .glass-panel {{
            background: rgba(255, 255, 255, 0.75) !important;
            backdrop-filter: blur(40px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.9) !important;
            border-radius: {RADIUS['xxl']} !important;
            padding: 56px 48px !important;
            box-shadow:
                0 30px 80px rgba(0, 0, 0, 0.25),
                0 10px 30px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(255, 255, 255, 0.7) inset !important;
            position: relative;
            overflow: hidden;
        }}

        /* Subtle glow effect */
        .glass-panel::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(
                circle,
                rgba(255, 255, 255, 0.1) 0%,
                transparent 70%
            );
            animation: glowPulse 4s ease-in-out infinite;
            pointer-events: none;
        }}

        @keyframes glowPulse {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 0.6; }}
        }}

        /* ========== LOGO & HEADER (APPLE PREMIUM STYLE) ========== */
        .login-logo {{
            text-align: center !important;
            margin-bottom: 48px !important;
            position: relative;
            z-index: 1;
        }}

        .login-logo h1 {{
            font-size: 56px !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            margin: 0 0 12px 0 !important;
            text-shadow: 0 4px 20px rgba(42, 79, 87, 0.2) !important;
            line-height: 1.1 !important;
        }}

        .login-tagline {{
            font-size: 17px !important;
            font-weight: 500 !important;
            color: {COLORS['text_secondary']} !important;
            margin: 0 !important;
            letter-spacing: 0.02em !important;
            opacity: 0.9;
        }}

        /* ========== INPUT FIELDS (APPLE REFINED) ========== */
        .login-container .stTextInput > div > div > input {{
            background: {COLORS['surface_light']} !important;
            border: 2px solid {COLORS['border']} !important;
            border-radius: {RADIUS['lg']} !important;
            padding: 18px 20px !important;
            font-size: 17px !important;
            font-weight: 500 !important;
            color: {COLORS['text_primary']} !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
        }}

        .login-container .stTextInput > div > div > input::placeholder {{
            color: {COLORS['text_light']} !important;
            font-weight: 400 !important;
        }}

        .login-container .stTextInput > div > div > input:focus {{
            background: {COLORS['surface']} !important;
            border-color: {COLORS['primary']} !important;
            box-shadow:
                0 0 0 4px rgba(42, 79, 87, 0.12),
                0 4px 12px rgba(0, 0, 0, 0.08) !important;
            outline: none !important;
        }}

        /* Input validation states */
        .input-valid {{
            border-color: {COLORS['success']} !important;
        }}

        .input-invalid {{
            border-color: {COLORS['error']} !important;
        }}

        /* Remove dark backgrounds */
        .login-container .stTextInput,
        .login-container .stTextInput > div,
        .login-container .stTextInput > div > div {{
            background: transparent !important;
        }}

        /* ========== CAPS LOCK WARNING ========== */
        .caps-lock-warning {{
            background: rgba(255, 149, 0, 0.12) !important;
            border: 1.5px solid {COLORS['warning']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 10px 16px !important;
            margin-top: 8px !important;
            color: {COLORS['warning']} !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            text-align: center !important;
            animation: slideDown 0.3s ease !important;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}

        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* ========== CHECKBOX (APPLE CLEAN) ========== */
        .login-container .stCheckbox {{
            background: transparent !important;
            padding: 12px 0 !important;
        }}

        .login-container .stCheckbox > label {{
            color: {COLORS['text_secondary']} !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            background: transparent !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
            transition: color 0.2s ease;
        }}

        .login-container .stCheckbox > label:hover {{
            color: {COLORS['primary']} !important;
        }}

        .login-container .stCheckbox input[type="checkbox"] {{
            accent-color: {COLORS['primary']} !important;
            width: 20px !important;
            height: 20px !important;
            cursor: pointer !important;
            transition: transform 0.15s ease;
        }}

        .login-container .stCheckbox input[type="checkbox"]:hover {{
            transform: scale(1.1);
        }}

        /* Remove all backgrounds from checkbox wrappers */
        .login-container .stCheckbox > label > div,
        .login-container .stCheckbox > label > div > div,
        .login-container .stCheckbox > div,
        .login-container .stCheckbox > div > div,
        .login-container .stCheckbox div {{
            background: transparent !important;
            background-color: transparent !important;
        }}

        /* Hide tooltip popup on checkbox */
        .login-container .stCheckbox [data-testid="stTooltipHoverTarget"],
        .login-container .stCheckbox [data-baseweb="tooltip"],
        .login-container [role="tooltip"],
        .login-container [class*="Tooltip"],
        div[data-baseweb="tooltip"],
        div[role="tooltip"] {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }}

        /* ========== LOGIN BUTTON (APPLE PREMIUM) ========== */
        .login-container .stButton > button {{
            width: 100% !important;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['dark_primary']} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: {RADIUS['lg']} !important;
            padding: 18px 32px !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            letter-spacing: 0.02em !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow:
                0 10px 30px rgba(42, 79, 87, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.15) inset !important;
            margin-top: 24px !important;
            position: relative;
            overflow: hidden;
        }}

        /* Button shine effect */
        .login-container .stButton > button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s ease;
        }}

        .login-container .stButton > button:hover::before {{
            left: 100%;
        }}

        .login-container .stButton > button:hover {{
            transform: translateY(-3px) !important;
            box-shadow:
                0 15px 40px rgba(42, 79, 87, 0.5),
                0 0 0 1px rgba(255, 255, 255, 0.25) inset !important;
        }}

        .login-container .stButton > button:active {{
            transform: translateY(-1px) scale(0.98) !important;
            box-shadow:
                0 8px 20px rgba(42, 79, 87, 0.35),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
        }}

        /* ========== ERROR MESSAGE (APPLE ALERT) ========== */
        .error-box {{
            background: rgba(255, 59, 48, 0.12) !important;
            backdrop-filter: blur(10px) !important;
            border: 2px solid {COLORS['error']} !important;
            border-radius: {RADIUS['lg']} !important;
            padding: 16px 20px !important;
            margin-bottom: 28px !important;
            color: {COLORS['error']} !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            text-align: center !important;
            animation: shake 0.5s ease, fadeIn 0.3s ease !important;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            10%, 30%, 50%, 70%, 90% {{ transform: translateX(-10px); }}
            20%, 40%, 60%, 80% {{ transform: translateX(10px); }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* ========== SUCCESS MESSAGE ========== */
        .success-box {{
            background: rgba(52, 199, 89, 0.12) !important;
            backdrop-filter: blur(10px) !important;
            border: 2px solid {COLORS['success']} !important;
            border-radius: {RADIUS['lg']} !important;
            padding: 16px 20px !important;
            margin-bottom: 28px !important;
            color: {COLORS['success']} !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            text-align: center !important;
            animation: fadeIn 0.3s ease !important;
        }}

        /* ========== DIVIDER (MINIMAL) ========== */
        .divider {{
            height: 1px !important;
            background: linear-gradient(
                90deg,
                transparent,
                {COLORS['border']},
                transparent
            ) !important;
            margin: 32px 0 !important;
        }}

        /* ========== FOOTER LINK ========== */
        .footer-link {{
            text-align: center;
            margin-top: 24px;
            font-size: 14px;
            color: {COLORS['accent']};
            font-weight: 500;
            cursor: pointer;
            transition: color 0.2s ease;
        }}

        .footer-link:hover {{
            color: {COLORS['primary']};
            text-decoration: underline;
        }}

        /* ========== RESPONSIVE ========== */
        @media (max-width: 768px) {{
            .glass-panel {{
                padding: 40px 32px !important;
            }}

            .login-logo h1 {{
                font-size: 44px !important;
            }}

            .login-tagline {{
                font-size: 15px !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

    # STEP 2: Render Dark Gradient Background
    st.markdown('<div class="login-background"></div>', unsafe_allow_html=True)

    # STEP 3: Render Login Panel
    st.markdown('<div class="login-container"><div class="glass-panel">', unsafe_allow_html=True)

    # Logo & Header (centered)
    st.markdown("""
    <div class="login-logo">
        <h1>EVALUERA</h1>
        <p class="login-tagline">KI-gestützte Kostenanalyse & Beschaffungsoptimierung</p>
    </div>
    """, unsafe_allow_html=True)

    # Error Message
    if "login_error" in st.session_state and st.session_state.login_error:
        st.markdown("""
        <div class="error-box">
            <span>⚠️</span>
            <span>Ungültige Zugangsdaten. Bitte erneut versuchen.</span>
        </div>
        """, unsafe_allow_html=True)

    # Success Message (for validation feedback)
    if "login_success" in st.session_state and st.session_state.login_success:
        st.markdown("""
        <div class="success-box">
            <span>✓</span>
            <span>Anmeldung erfolgreich!</span>
        </div>
        """, unsafe_allow_html=True)

    # Username Input with validation
    username = st.text_input(
        "Benutzername",
        placeholder="Benutzername eingeben",
        key="login_username",
        label_visibility="collapsed"
    )

    # Username validation indicator
    if username:
        if len(username) >= 3:
            st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

    # Password Input
    if "show_password" not in st.session_state:
        st.session_state.show_password = False

    password = st.text_input(
        "Passwort",
        type="default" if st.session_state.show_password else "password",
        placeholder="Passwort eingeben",
        key="login_password",
        label_visibility="collapsed"
    )

    # Caps Lock Warning (simulated - Streamlit doesn't have real caps lock detection)
    # In a real implementation, this would use JavaScript
    if password and password.isupper() and len(password) > 2:
        st.markdown("""
        <div class="caps-lock-warning">
            <span>⚠️</span>
            <span>Feststelltaste ist möglicherweise aktiviert</span>
        </div>
        """, unsafe_allow_html=True)

    # Password Toggle (Apple Clean Style)
    show_pwd = st.checkbox(
        "Passwort anzeigen",
        key="show_pwd_toggle",
        value=st.session_state.show_password,
        help=""
    )
    st.session_state.show_password = show_pwd

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Login Button
    if st.button("🔐  Sicher Anmelden", type="primary", use_container_width=True, key="login_btn"):
        if username and password:
            if login(username, password):
                st.session_state.login_error = False
                st.session_state.login_success = True
                st.rerun()
            else:
                st.session_state.login_error = True
                st.session_state.login_success = False
                st.rerun()
        else:
            st.session_state.login_error = True
            st.session_state.login_success = False
            st.rerun()

    # Footer - Optional alternative login methods
    st.markdown("""
    <div class="footer-link">
        Passwort vergessen?
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


def render_logout_button():
    """Render Apple-style logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"""
        <div style="
            padding: 20px;
            background: linear-gradient(135deg, {COLORS['light_accent']} 0%, {COLORS['secondary']} 100%);
            border-radius: {RADIUS['lg']};
            text-align: center;
            box-shadow: {SHADOWS['md']};
            border: 1px solid {COLORS['border_light']};
        ">
            <div style="
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: {COLORS['text_muted']};
                margin-bottom: 10px;
            ">
                Eingeloggt als
            </div>
            <div style="
                font-weight: 800;
                font-size: 18px;
                color: {COLORS['primary']};
                letter-spacing: -0.02em;
            ">
                {st.session_state.get('username', 'Benutzer')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Abmelden", use_container_width=True):
            logout()
