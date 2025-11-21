"""
🔐 EVALUERA - Premium Login Screen
====================================
Apple-inspired Glassmorphism Design
"""

import streamlit as st
from liquid_glass_system import render_liquid_background, apply_liquid_glass_styles
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


def render_login_screen():
    """
    Render premium Apple-style login screen with glassmorphism
    """

    # ==================== ANIMATED BACKGROUND ====================
    apply_liquid_glass_styles()
    render_liquid_background()

    # ==================== PREMIUM STYLING ====================
    st.markdown("""
    <style>
        /* ========== HIDE STREAMLIT UI ========== */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none !important;}

        /* ========== FULLSCREEN OVERLAY ========== */
        .main {
            background: transparent !important;
        }

        body {
            background: transparent !important;
        }

        /* Dark overlay over animated background */
        .main::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            z-index: -1;
        }

        /* ========== CENTER LOGIN PANEL ========== */
        .main .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            max-width: 480px !important;
            margin: 0 auto !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            min-height: 100vh !important;
        }

        /* ========== FROSTED GLASS CARD ========== */
        .login-panel {
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(35px) saturate(150%);
            -webkit-backdrop-filter: blur(35px) saturate(150%);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 22px;
            padding: 40px 36px;
            box-shadow:
                0 10px 40px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            animation: slideUpFadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
            position: relative;
            overflow: hidden;
        }

        /* Subtle shimmer effect */
        .login-panel::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(255, 255, 255, 0.08) 50%,
                transparent 70%
            );
            animation: shimmer 8s ease-in-out infinite;
        }

        @keyframes slideUpFadeIn {
            from {
                opacity: 0;
                transform: translateY(30px) scale(0.96);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        @keyframes shimmer {
            0%, 100% { transform: translate(-50%, -50%) rotate(0deg); }
            50% { transform: translate(-30%, -30%) rotate(180deg); }
        }

        /* ========== BRANDING ========== */
        .login-header {
            text-align: center;
            margin-bottom: 32px;
            position: relative;
            z-index: 1;
        }

        .login-header h1 {
            font-size: 32px;
            font-weight: 300;
            letter-spacing: 0.12em;
            color: #ffffff;
            margin: 0 0 8px 0;
            text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
        }

        .login-header p {
            font-size: 15px;
            color: rgba(255, 255, 255, 0.75);
            margin: 0;
            font-weight: 400;
            text-shadow: 0 1px 8px rgba(0, 0, 0, 0.2);
        }

        /* ========== GLASS INPUT FIELDS ========== */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.2) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            font-size: 15px !important;
            color: #ffffff !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
        }

        .stTextInput > div > div > input:focus {
            background: rgba(255, 255, 255, 0.25) !important;
            border-color: rgba(184, 212, 209, 0.6) !important;
            box-shadow:
                inset 0 1px 3px rgba(0, 0, 0, 0.1),
                0 0 0 3px rgba(184, 212, 209, 0.15) !important;
            outline: none !important;
        }

        /* ========== PASSWORD TOGGLE ========== */
        .stCheckbox {
            position: relative;
            z-index: 1;
        }

        .stCheckbox > label {
            color: rgba(255, 255, 255, 0.7) !important;
            font-size: 14px !important;
        }

        /* ========== PREMIUM BUTTON ========== */
        .stButton > button {
            width: 100% !important;
            background: linear-gradient(135deg, #2F4A56 0%, #3D5A68 50%, #4B6A78 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 24px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow:
                0 8px 24px rgba(47, 74, 86, 0.35),
                inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
            position: relative !important;
            overflow: hidden !important;
            margin-top: 8px !important;
        }

        /* Button shine effect */
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            transition: left 0.5s;
        }

        .stButton > button:hover::before {
            left: 100%;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow:
                0 12px 32px rgba(47, 74, 86, 0.45),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        }

        .stButton > button:active {
            transform: translateY(0) scale(0.98) !important;
            box-shadow:
                0 4px 16px rgba(47, 74, 86, 0.3),
                inset 0 1px 3px rgba(0, 0, 0, 0.2) !important;
        }

        /* ========== ERROR MESSAGE ========== */
        .login-error {
            background: rgba(239, 68, 68, 0.15);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 16px;
            color: #fee;
            font-size: 14px;
            text-align: center;
            animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97);
            position: relative;
            z-index: 1;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-8px); }
            20%, 40%, 60%, 80% { transform: translateX(8px); }
        }

        /* ========== HELPER TEXT ========== */
        .login-helper {
            text-align: center;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.6);
            margin-top: 24px;
            line-height: 1.6;
            position: relative;
            z-index: 1;
        }

        .login-helper strong {
            color: rgba(255, 255, 255, 0.85);
            font-weight: 600;
        }

        .login-helper code {
            background: rgba(255, 255, 255, 0.15);
            padding: 2px 8px;
            border-radius: 6px;
            font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            color: rgba(255, 255, 255, 0.9);
        }

        /* ========== DIVIDER ========== */
        .login-divider {
            height: 1px;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            margin: 24px 0 20px 0;
            position: relative;
            z-index: 1;
        }

        /* ========== RESPONSIVE ========== */
        @media (max-width: 768px) {
            .main .block-container {
                max-width: 90% !important;
                padding: 20px !important;
            }

            .login-panel {
                padding: 32px 24px;
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

        st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)

        # Password input with toggle
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
                '<div style="padding-top: 8px; font-size: 14px; color: rgba(255, 255, 255, 0.7);">Passwort anzeigen</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)

        # Login button with lock icon
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
