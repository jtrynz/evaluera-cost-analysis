"""
🔐 EVALUERA - Premium Login Screen
====================================
Uses existing EVALUERA loading animation as permanent background
"""

import streamlit as st
from ui_theme import COLORS


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


# ==================== RENDER PERMANENT LOADING ANIMATION BACKGROUND ====================
def render_permanent_loading_background():
    """
    Render EVALUERA loading animation as permanent fullscreen background
    Uses the EXACT same animation from ui_components.py
    """
    st.markdown("""
    <div class="loading-animation-background">
        <div class="loading-gradient"></div>
        <div class="loading-content">
            <div class="spinner-wrapper">
                <div class="spinner-circle">
                    <div class="spinner-icon">🤖</div>
                </div>
                <div class="spinner-ring"></div>
            </div>
            <div class="loading-text">
                <div class="loading-title">EVALUERA</div>
                <div class="loading-subtitle">KI-Engine läuft...</div>
            </div>
        </div>
        <div class="progress-bar-container">
            <div class="shimmer-effect"></div>
        </div>
        <div class="bounce-dots-container">
            <div class="bounce-dot"></div>
            <div class="bounce-dot"></div>
            <div class="bounce-dot"></div>
        </div>
    </div>

    <style>
        /* ========== FULLSCREEN LOADING ANIMATION BACKGROUND ========== */
        .loading-animation-background {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: -10 !important;
            background: linear-gradient(135deg, #7BA5A0 0%, #5A8680 50%, #B8D4D1 100%);
            border-radius: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            box-shadow: 0 20px 60px rgba(123, 165, 160, 0.3), 0 8px 16px rgba(0, 0, 0, 0.1);
            border: none !important;
            backdrop-filter: blur(20px);
            overflow: hidden;
        }

        .loading-gradient {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 50%, rgba(184, 212, 209, 0.4) 0%, transparent 50%);
            animation: moveGradient 3s ease-in-out infinite;
        }

        .loading-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1;
        }

        /* Spinner Circle */
        .spinner-wrapper {
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
        }

        .spinner-circle {
            width: 120px;
            height: 120px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            position: relative;
            z-index: 2;
        }

        .spinner-icon {
            font-size: 3rem;
            animation: pulse 2s ease-in-out infinite;
        }

        .spinner-ring {
            position: absolute;
            top: -10px;
            left: -10px;
            width: 140px;
            height: 140px;
            border: 4px solid rgba(255, 255, 255, 0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 1.5s linear infinite;
        }

        /* Loading Text */
        .loading-text {
            text-align: center;
        }

        .loading-title {
            color: white;
            font-weight: 700;
            font-size: 2rem;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            letter-spacing: 0.1em;
        }

        .loading-subtitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
            font-weight: 500;
        }

        /* Progress Bar */
        .progress-bar-container {
            position: absolute;
            bottom: 35%;
            left: 50%;
            transform: translateX(-50%);
            width: 320px;
            height: 6px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 100px;
            overflow: hidden;
            box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);
        }

        .shimmer-effect {
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 50%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
            animation: shimmer 1.8s ease-in-out infinite;
        }

        /* Bounce Dots */
        .bounce-dots-container {
            position: absolute;
            bottom: 30%;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
        }

        .bounce-dot {
            width: 10px;
            height: 10px;
            background: white;
            border-radius: 50%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .bounce-dot:nth-child(1) {
            animation: bounce 1.4s ease-in-out infinite;
        }

        .bounce-dot:nth-child(2) {
            animation: bounce 1.4s ease-in-out 0.2s infinite;
        }

        .bounce-dot:nth-child(3) {
            animation: bounce 1.4s ease-in-out 0.4s infinite;
        }

        /* ========== ANIMATIONS ========== */
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(300%); }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        @keyframes moveGradient {
            0%, 100% { transform: translateX(0) translateY(0); }
            50% { transform: translateX(20px) translateY(-20px); }
        }
    </style>
    """, unsafe_allow_html=True)


# ==================== LOGIN SCREEN ====================
def render_login_screen():
    """
    Render premium login screen with permanent loading animation background
    """

    # Render permanent loading animation background
    render_permanent_loading_background()

    # Dark overlay
    st.markdown("""
    <div class="dark-overlay"></div>
    <style>
        .dark-overlay {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: rgba(0, 0, 0, 0.35) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            z-index: -9 !important;
            pointer-events: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Login panel styles
    st.markdown("""
    <style>
        /* ========== HIDE STREAMLIT UI ========== */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        [data-testid="stSidebar"] {display: none !important;}

        /* ========== TRANSPARENT MAIN ========== */
        .main {
            background: transparent !important;
        }

        body {
            background: transparent !important;
        }

        /* ========== CENTER LOGIN PANEL ========== */
        .main .block-container {
            padding: 0 !important;
            max-width: 480px !important;
            margin: 0 auto !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            min-height: 100vh !important;
        }

        /* ========== FROSTED GLASS LOGIN PANEL ========== */
        .login-panel {
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(30px) saturate(150%);
            -webkit-backdrop-filter: blur(30px) saturate(150%);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 22px;
            padding: 40px;
            width: 100%;
            max-width: 460px;
            box-shadow:
                0 10px 40px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards;
            position: relative;
            z-index: 1;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* ========== BRANDING ========== */
        .login-header {
            text-align: center;
            margin-bottom: 32px;
        }

        .login-header h1 {
            font-size: 34px;
            font-weight: 300;
            letter-spacing: 0.12em;
            color: #ffffff;
            margin: 0 0 8px 0;
            text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
        }

        .login-header p {
            font-size: 15px;
            color: rgba(255, 255, 255, 0.8);
            margin: 0;
            font-weight: 400;
        }

        /* ========== GLASS INPUT FIELDS ========== */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.22) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px !important;
            padding: 15px 18px !important;
            font-size: 15px !important;
            color: #ffffff !important;
            transition: all 0.3s ease !important;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1) !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
        }

        .stTextInput > div > div > input:focus {
            background: rgba(255, 255, 255, 0.28) !important;
            border-color: rgba(184, 212, 209, 0.7) !important;
            box-shadow:
                inset 0 2px 4px rgba(0, 0, 0, 0.1),
                0 0 0 3px rgba(184, 212, 209, 0.2) !important;
            outline: none !important;
        }

        /* ========== PASSWORD TOGGLE ========== */
        .stCheckbox > label {
            color: rgba(255, 255, 255, 0.75) !important;
            font-size: 14px !important;
        }

        /* ========== PREMIUM BUTTON ========== */
        .stButton > button {
            width: 100% !important;
            background: linear-gradient(135deg, #2F4A56 0%, #3D5A68 50%, #4B6A78 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 15px 24px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow:
                0 8px 24px rgba(47, 74, 86, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
            margin-top: 12px !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow:
                0 12px 32px rgba(47, 74, 86, 0.5),
                inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
        }

        .stButton > button:active {
            transform: translateY(0) scale(0.98) !important;
        }

        /* ========== ERROR MESSAGE ========== */
        .login-error {
            background: rgba(239, 68, 68, 0.18);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(239, 68, 68, 0.35);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 16px;
            color: #fff;
            font-size: 14px;
            text-align: center;
            animation: shake 0.5s ease;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-6px); }
            20%, 40%, 60%, 80% { transform: translateX(6px); }
        }

        /* ========== HELPER TEXT ========== */
        .login-helper {
            text-align: center;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.65);
            margin-top: 24px;
            line-height: 1.6;
        }

        .login-helper strong {
            color: rgba(255, 255, 255, 0.9);
            font-weight: 600;
        }

        .login-helper code {
            background: rgba(255, 255, 255, 0.18);
            padding: 3px 8px;
            border-radius: 6px;
            font-family: 'SF Mono', monospace;
            font-size: 12px;
            color: #fff;
        }

        /* ========== DIVIDER ========== */
        .login-divider {
            height: 1px;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.25),
                transparent
            );
            margin: 24px 0 16px 0;
        }

        /* ========== RESPONSIVE ========== */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 20px !important;
            }

            .login-panel {
                padding: 32px 28px;
            }

            .login-header h1 {
                font-size: 28px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # ==================== LOGIN PANEL ====================
    with st.container():
        st.markdown('<div class="login-panel">', unsafe_allow_html=True)

        # Branding
        st.markdown("""
        <div class="login-header">
            <h1>EVALUERA</h1>
            <p>KI-gestützte Kostenanalyse</p>
        </div>
        """, unsafe_allow_html=True)

        # Error message
        if "login_error" in st.session_state and st.session_state.login_error:
            st.markdown("""
            <div class="login-error">
                ⚠️ Zugangsdaten ungültig
            </div>
            """, unsafe_allow_html=True)

        # Username input
        username = st.text_input(
            "Benutzername",
            placeholder="Benutzername eingeben",
            key="login_username",
            label_visibility="collapsed"
        )

        st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)

        # Password input
        if "show_password" not in st.session_state:
            st.session_state.show_password = False

        password = st.text_input(
            "Passwort",
            type="default" if st.session_state.show_password else "password",
            placeholder="Passwort eingeben",
            key="login_password",
            label_visibility="collapsed"
        )

        # Password toggle
        col1, col2 = st.columns([1, 5])
        with col1:
            show_pwd = st.checkbox("👁️", key="show_pwd_toggle", value=st.session_state.show_password)
            st.session_state.show_password = show_pwd
        with col2:
            st.markdown(
                '<div style="padding-top: 8px; font-size: 14px; color: rgba(255, 255, 255, 0.75);">Passwort anzeigen</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)

        # Login button
        if st.button("🔐  Anmelden", type="primary", use_container_width=True, key="login_btn"):
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

        # Demo credentials
        st.markdown("""
        <div class="login-helper">
            <strong>Demo-Zugangsdaten</strong><br>
            <code>demo</code> / <code>demo123</code> ·
            <code>admin</code> / <code>evaluera2024</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def render_logout_button():
    """Render logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"""
        <div style="
            padding: 1rem;
            background: rgba(184, 212, 209, 0.2);
            border-radius: 12px;
            text-align: center;
        ">
            <div style="font-size: 0.875rem; color: {COLORS['gray_600']}; margin-bottom: 0.5rem;">
                Eingeloggt als
            </div>
            <div style="font-weight: 600; color: {COLORS['gray_900']};">
                {st.session_state.get('username', 'Benutzer')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Abmelden", use_container_width=True):
            logout()
