"""
🔐 EVALUERA - Premium Login Screen with Animated Background
============================================================
Permanent fullscreen animated background with glassmorphism login panel
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


# ==================== LOGIN SCREEN ====================
def render_login_screen():
    """
    Render premium login screen with permanent animated background
    """

    # STEP 1: Render FULLSCREEN ANIMATED BACKGROUND + CSS (all in one block)
    st.markdown("""
    <div class="animated-bg">
        <div class="wave wave-1"></div>
        <div class="wave wave-2"></div>
        <div class="wave wave-3"></div>
        <div class="wave wave-4"></div>
    </div>

    <style>
        /* ========== FORCE TRANSPARENT STREAMLIT CONTAINERS ========== */
        .main {
            background: transparent !important;
        }

        .block-container {
            background: transparent !important;
            padding-top: 0 !important;
        }

        body {
            background: transparent !important;
            margin: 0 !important;
            overflow: hidden !important;
        }

        [data-testid="stAppViewContainer"] {
            background: transparent !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        /* Hide all Streamlit UI elements */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="stToolbar"] {display: none !important;}

        /* ========== FULLSCREEN ANIMATED BACKGROUND ========== */
        .animated-bg {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: #BFDCDC !important;
            z-index: -1 !important;
            overflow: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* ========== LIQUID WAVES ========== */
        .wave {
            position: absolute !important;
            border-radius: 50% !important;
            filter: blur(60px) !important;
            opacity: 0.4 !important;
            will-change: transform !important;
        }

        .wave-1 {
            width: 500px !important;
            height: 500px !important;
            background: radial-gradient(circle, rgba(255,255,255,0.6) 0%, transparent 70%) !important;
            top: -100px !important;
            left: -100px !important;
            animation: float1 25s ease-in-out infinite !important;
        }

        .wave-2 {
            width: 600px !important;
            height: 600px !important;
            background: radial-gradient(circle, rgba(255,255,255,0.5) 0%, transparent 70%) !important;
            bottom: -150px !important;
            right: -150px !important;
            animation: float2 30s ease-in-out infinite !important;
        }

        .wave-3 {
            width: 450px !important;
            height: 450px !important;
            background: radial-gradient(circle, rgba(255,255,255,0.55) 0%, transparent 70%) !important;
            top: 40% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            animation: float3 28s ease-in-out infinite !important;
        }

        .wave-4 {
            width: 400px !important;
            height: 400px !important;
            background: radial-gradient(circle, rgba(255,255,255,0.45) 0%, transparent 70%) !important;
            bottom: 20% !important;
            left: 20% !important;
            animation: float4 23s ease-in-out infinite !important;
        }

        /* ========== WAVE ANIMATIONS ========== */
        @keyframes float1 {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }
            33% {
                transform: translate(50px, 80px) scale(1.1);
            }
            66% {
                transform: translate(-30px, 40px) scale(0.95);
            }
        }

        @keyframes float2 {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }
            33% {
                transform: translate(-60px, -50px) scale(1.05);
            }
            66% {
                transform: translate(40px, 30px) scale(0.9);
            }
        }

        @keyframes float3 {
            0%, 100% {
                transform: translate(-50%, -50%) scale(1);
            }
            33% {
                transform: translate(calc(-50% + 40px), calc(-50% - 60px)) scale(1.08);
            }
            66% {
                transform: translate(calc(-50% - 50px), calc(-50% + 40px)) scale(0.92);
            }
        }

        @keyframes float4 {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }
            33% {
                transform: translate(70px, -40px) scale(1.12);
            }
            66% {
                transform: translate(-40px, 60px) scale(0.88);
            }
        }

        /* ========== GLASSMORPHISM LOGIN PANEL ========== */
        .login-container {
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            z-index: 100 !important;
            width: 90% !important;
            max-width: 440px !important;
        }

        .glass-panel {
            background: rgba(255, 255, 255, 0.18) !important;
            backdrop-filter: blur(25px) saturate(150%) !important;
            -webkit-backdrop-filter: blur(25px) saturate(150%) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 24px !important;
            padding: 48px 40px !important;
            box-shadow:
                0 8px 32px rgba(31, 38, 135, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
            animation: fadeInScale 0.8s cubic-bezier(0.16, 1, 0.3, 1) backwards !important;
        }

        @keyframes fadeInScale {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        /* ========== LOGIN HEADER ========== */
        .login-logo {
            text-align: center !important;
            margin-bottom: 32px !important;
        }

        .login-logo h1 {
            font-size: 36px !important;
            font-weight: 300 !important;
            letter-spacing: 0.15em !important;
            color: #2F4A56 !important;
            margin: 0 0 8px 0 !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
        }

        .login-logo p {
            font-size: 15px !important;
            color: rgba(47, 74, 86, 0.7) !important;
            margin: 0 !important;
            font-weight: 400 !important;
        }

        /* ========== INPUT FIELDS ========== */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.25) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 14px !important;
            padding: 16px 18px !important;
            font-size: 15px !important;
            color: #2F4A56 !important;
            transition: all 0.3s ease !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: rgba(47, 74, 86, 0.5) !important;
        }

        .stTextInput > div > div > input:focus {
            background: rgba(255, 255, 255, 0.35) !important;
            border-color: rgba(123, 165, 160, 0.6) !important;
            box-shadow: 0 0 0 3px rgba(123, 165, 160, 0.15) !important;
            outline: none !important;
        }

        /* ========== CHECKBOX ========== */
        .stCheckbox > label {
            color: rgba(47, 74, 86, 0.8) !important;
            font-size: 14px !important;
        }

        /* ========== LOGIN BUTTON ========== */
        .stButton > button {
            width: 100% !important;
            background: linear-gradient(135deg, #2F4A56 0%, #3D5A68 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 16px 24px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow:
                0 8px 24px rgba(47, 74, 86, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
            margin-top: 12px !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow:
                0 12px 32px rgba(47, 74, 86, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        }

        .stButton > button:active {
            transform: translateY(0) scale(0.98) !important;
        }

        /* ========== ERROR MESSAGE ========== */
        .error-box {
            background: rgba(239, 68, 68, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            margin-bottom: 20px !important;
            color: #dc2626 !important;
            font-size: 14px !important;
            text-align: center !important;
            animation: shake 0.5s ease !important;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
            20%, 40%, 60%, 80% { transform: translateX(8px); }
        }

        /* ========== DEMO CREDENTIALS ========== */
        .demo-creds {
            text-align: center !important;
            font-size: 13px !important;
            color: rgba(47, 74, 86, 0.6) !important;
            margin-top: 28px !important;
            line-height: 1.6 !important;
        }

        .demo-creds strong {
            color: rgba(47, 74, 86, 0.85) !important;
            font-weight: 600 !important;
            display: block !important;
            margin-bottom: 8px !important;
        }

        .demo-creds code {
            background: rgba(255, 255, 255, 0.25) !important;
            padding: 4px 10px !important;
            border-radius: 6px !important;
            font-family: 'SF Mono', monospace !important;
            font-size: 12px !important;
            color: #2F4A56 !important;
            white-space: nowrap !important;
        }

        .divider {
            height: 1px !important;
            background: linear-gradient(90deg, transparent, rgba(47, 74, 86, 0.2), transparent) !important;
            margin: 24px 0 20px 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # STEP 2: Render Login Panel (in regular Streamlit container with absolute positioning via CSS)
    st.markdown('<div class="login-container"><div class="glass-panel">', unsafe_allow_html=True)

    # Logo
    st.markdown("""
    <div class="login-logo">
        <h1>EVALUERA</h1>
        <p>KI-gestützte Kostenanalyse</p>
    </div>
    """, unsafe_allow_html=True)

    # Error message
    if "login_error" in st.session_state and st.session_state.login_error:
        st.markdown("""
        <div class="error-box">
            ⚠️ Ungültige Zugangsdaten
        </div>
        """, unsafe_allow_html=True)

    # Username
    username = st.text_input(
        "Benutzername",
        placeholder="Benutzername eingeben",
        key="login_username",
        label_visibility="collapsed"
    )

    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)

    # Password
    if "show_password" not in st.session_state:
        st.session_state.show_password = False

    password = st.text_input(
        "Passwort",
        type="default" if st.session_state.show_password else "password",
        placeholder="Passwort eingeben",
        key="login_password",
        label_visibility="collapsed"
    )

    # Show password toggle
    col1, col2 = st.columns([1, 5])
    with col1:
        show_pwd = st.checkbox("👁️", key="show_pwd_toggle", value=st.session_state.show_password)
        st.session_state.show_password = show_pwd
    with col2:
        st.markdown(
            '<div style="padding-top: 8px; font-size: 14px; color: rgba(47, 74, 86, 0.7);">Passwort anzeigen</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

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
    <div class="demo-creds">
        <strong>Demo-Zugangsdaten</strong>
        <code>demo</code> / <code>demo123</code><br>
        <code>admin</code> / <code>evaluera2024</code>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


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
