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
    "user": "password" ,
    "alex": "alex"
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
    Render premium login screen (background is rendered in simple_app.py)
    """

    # STEP 1: Render LOGIN PANEL CSS
    st.markdown("""
    <style>
        /* ========== GLASSMORPHISM LOGIN PANEL ========== */
        .login-container {
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            z-index: 99999 !important;
            width: 90% !important;
            max-width: 440px !important;
            background: rgba(255,255,255,0.2) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: 20px !important;
            padding: 40px 32px !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.25) !important;
            border: 2px solid rgba(255,255,255,0.3) !important;
            z-index: 100000 !important;
        }

        .glass-panel {
            background: none !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
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

        .divider {
            height: 1px !important;
            background: linear-gradient(90deg, transparent, rgba(47, 74, 86, 0.2), transparent) !important;
            margin: 24px 0 20px 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # STEP 2: Render Login Panel
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
