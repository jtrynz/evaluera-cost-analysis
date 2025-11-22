"""
🔐 EVALUERA - Apple-Like Premium Login Screen
==============================================
Secure login with animated background and glassmorphism
"""

import streamlit as st
from ui_theme import COLORS, RADIUS, SPACING, SHADOWS, TYPOGRAPHY
from ui_components import render_evaluera_logo


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


# ==================== APPLE-LIKE LOGIN SCREEN ====================
def render_login_screen():
    """
    Render Apple-inspired premium login screen
    Background animation is rendered in simple_app.py
    """

    # STEP 1: Inject Apple-Like Login CSS
    st.markdown(f"""
    <style>
        /* ========== APPLE GLASSMORPHISM LOGIN CONTAINER ========== */
        .login-container {{
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            z-index: 99999 !important;
            width: 90% !important;
            max-width: 420px !important;
            animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) backwards !important;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translate(-50%, -45%) scale(0.95);
            }}
            to {{
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }}
        }}

        /* ========== GLASS PANEL (APPLE CARD STYLE) ========== */
        .glass-panel {{
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(30px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: {RADIUS['xl']} !important;
            padding: 48px 40px !important;
            box-shadow:
                0 20px 60px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(255, 255, 255, 0.6) inset !important;
        }}

        /* ========== LOGO & HEADER (APPLE TYPOGRAPHY) ========== */
        .login-logo {{
            text-align: center !important;
            margin-bottom: 40px !important;
        }}

        .login-logo h1 {{
            font-size: 40px !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
            color: {COLORS['primary']} !important;
            margin: 0 0 8px 0 !important;
            text-shadow: 0 2px 12px rgba(42, 79, 87, 0.15) !important;
        }}

        .login-logo p {{
            font-size: 15px !important;
            font-weight: 500 !important;
            color: {COLORS['gray_600']} !important;
            margin: 0 !important;
            letter-spacing: 0.01em !important;
        }}

        /* ========== INPUT FIELDS (APPLE CLEAN STYLE) ========== */
        .login-container .stTextInput > div > div > input {{
            background: {COLORS['surface']} !important;
            border: 1.5px solid {COLORS['gray_300']} !important;
            border-radius: {RADIUS['md']} !important;
            padding: 14px 18px !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            color: {COLORS['dark_accent']} !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        }}

        .login-container .stTextInput > div > div > input::placeholder {{
            color: {COLORS['gray_400']} !important;
            font-weight: 400 !important;
        }}

        .login-container .stTextInput > div > div > input:focus {{
            background: {COLORS['surface']} !important;
            border-color: {COLORS['primary']} !important;
            box-shadow: 0 0 0 4px {COLORS['light_accent']}, 0 2px 8px rgba(0,0,0,0.08) !important;
            outline: none !important;
        }}

        /* Remove dark backgrounds */
        .login-container .stTextInput,
        .login-container .stTextInput > div,
        .login-container .stTextInput > div > div {{
            background: transparent !important;
        }}

        /* ========== CHECKBOX (APPLE CLEAN) ========== */
        .login-container .stCheckbox > label {{
            color: {COLORS['gray_600']} !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }}

        .login-container .stCheckbox input[type="checkbox"] {{
            accent-color: {COLORS['primary']} !important;
            width: 18px !important;
            height: 18px !important;
            cursor: pointer !important;
        }}

        /* ========== LOGIN BUTTON (APPLE GLOSSY) ========== */
        .login-container .stButton > button {{
            width: 100% !important;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['dark_accent']} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: {RADIUS['md']} !important;
            padding: 16px 24px !important;
            font-size: 17px !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            cursor: pointer !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow:
                0 8px 24px rgba(42, 79, 87, 0.35),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
            margin-top: 16px !important;
        }}

        .login-container .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow:
                0 12px 32px rgba(42, 79, 87, 0.45),
                0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
        }}

        .login-container .stButton > button:active {{
            transform: translateY(0) scale(0.98) !important;
            box-shadow:
                0 6px 18px rgba(42, 79, 87, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
        }}

        /* ========== ERROR MESSAGE (APPLE ALERT STYLE) ========== */
        .error-box {{
            background: rgba(239, 68, 68, 0.12) !important;
            backdrop-filter: blur(10px) !important;
            border: 1.5px solid {COLORS['error']}40 !important;
            border-radius: {RADIUS['md']} !important;
            padding: 14px 18px !important;
            margin-bottom: 24px !important;
            color: {COLORS['error']} !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-align: center !important;
            animation: shake 0.5s ease, fadeIn 0.3s ease !important;
        }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            10%, 30%, 50%, 70%, 90% {{ transform: translateX(-8px); }}
            20%, 40%, 60%, 80% {{ transform: translateX(8px); }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* ========== DIVIDER (MINIMAL) ========== */
        .divider {{
            height: 1px !important;
            background: linear-gradient(
                90deg,
                transparent,
                {COLORS['gray_300']},
                transparent
            ) !important;
            margin: 28px 0 24px 0 !important;
        }}

        /* ========== PASSWORD TOGGLE (APPLE CLEAN) ========== */
        .password-toggle {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 12px 0;
        }}

        .password-toggle-label {{
            padding-top: 8px;
            font-size: 14px;
            color: {COLORS['gray_600']};
            font-weight: 500;
        }}
    </style>
    """, unsafe_allow_html=True)

    # STEP 2: Render Login Panel
    st.markdown('<div class="login-container"><div class="glass-panel">', unsafe_allow_html=True)

    # Logo & Header
    st.markdown('<div class="login-logo">', unsafe_allow_html=True)
    render_evaluera_logo(align="center", width=230)
    st.markdown('<p style="text-align: center; margin-top: 16px;">KI-gestützte Kostenanalyse</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Error Message
    if "login_error" in st.session_state and st.session_state.login_error:
        st.markdown("""
        <div class="error-box">
            ⚠️ Ungültige Zugangsdaten. Bitte erneut versuchen.
        </div>
        """, unsafe_allow_html=True)

    # Username Input
    username = st.text_input(
        "Benutzername",
        placeholder="Benutzername eingeben",
        key="login_username",
        label_visibility="collapsed"
    )

    st.markdown('<div style="height: 16px;"></div>', unsafe_allow_html=True)

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

    # Password Toggle (Apple Clean Style)
    col1, col2 = st.columns([1, 6])
    with col1:
        show_pwd = st.checkbox("", key="show_pwd_toggle", value=st.session_state.show_password)
        st.session_state.show_password = show_pwd
    with col2:
        st.markdown(
            f'<div class="password-toggle-label">Passwort anzeigen</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Login Button
    if st.button("🔐  Sicher Anmelden", type="primary", use_container_width=True, key="login_btn"):
        if username and password:
            if login(username, password):
                st.session_state.login_error = False
                st.rerun()
            else:
                st.session_state.login_error = True
                st.rerun()
        else:
            st.session_state.login_error = True
            st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)


def render_logout_button():
    """Render Apple-style logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"""
        <div style="
            padding: 16px;
            background: linear-gradient(135deg, {COLORS['light_accent']} 0%, {COLORS['secondary']} 100%);
            border-radius: {RADIUS['md']};
            text-align: center;
            box-shadow: {SHADOWS['sm']};
            border: 1px solid {COLORS['gray_200']};
        ">
            <div style="
                font-size: 12px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: {COLORS['gray_500']};
                margin-bottom: 8px;
            ">
                Eingeloggt als
            </div>
            <div style="
                font-weight: 700;
                font-size: 16px;
                color: {COLORS['primary']};
                letter-spacing: -0.01em;
            ">
                {st.session_state.get('username', 'Benutzer')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Abmelden", use_container_width=True):
            logout()
