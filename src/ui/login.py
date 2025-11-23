"""
🔐 EVALUERA - Premium Apple-Inspired Login Screen
===================================================
Professional authentication with glassmorphism, dark gradient,
and Apple Human Interface Guidelines compliance
"""

import streamlit as st
import os
import base64
from src.ui.theme import COLORS, RADIUS, SPACING, SHADOWS, TYPOGRAPHY


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


def get_logo_base64():
    """Get EVALUERA logo as base64 for embedding"""
    logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'EVALUERA.png')
    try:
        with open(logo_path, 'rb') as f:
            logo_data = f.read()
            return base64.b64encode(logo_data).decode()
    except:
        return None


# ==================== PREMIUM LOGIN SCREEN ====================
def render_login_screen():
    """
    Render premium Apple-inspired login screen with:
    - Dark gradient animated background
    - EVALUERA logo (PNG)
    - Premium glassmorphism card
    - Live input validation
    - Caps Lock warning
    - Smooth animations
    - Apple-like typography
    """

    # Initialize session state
    if "show_password" not in st.session_state:
        st.session_state.show_password = False
    if "login_error" not in st.session_state:
        st.session_state.login_error = False

    # Get logo
    logo_base64 = get_logo_base64()

    # Inject Premium CSS
    st.markdown(f"""
    <style>
        /* ========== APPLE FONTS ========== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* ========== DARK GRADIENT BACKGROUND ========== */
        .login-screen {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(
                135deg,
                {COLORS['dark_accent']} 0%,
                {COLORS['primary']} 25%,
                {COLORS['dark_accent']} 50%,
                {COLORS['primary']} 75%,
                {COLORS['dark_accent']} 100%
            );
            background-size: 400% 400%;
            animation: gradientFlow 18s ease infinite;
            z-index: -2;
        }}

        @keyframes gradientFlow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* Animated overlay pattern */
        .login-screen::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                radial-gradient(circle at 25% 30%, rgba(184, 212, 209, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 75% 70%, rgba(184, 212, 209, 0.06) 0%, transparent 40%);
            animation: patternPulse 15s ease-in-out infinite;
        }}

        @keyframes patternPulse {{
            0%, 100% {{ opacity: 0.6; }}
            50% {{ opacity: 0.9; }}
        }}

        /* Hide Streamlit chrome */
        .stApp:has(.login-container) {{
            overflow: hidden !important;
        }}

        header[data-testid="stHeader"],
        .stApp:has(.login-container) [data-testid="stSidebar"],
        .stApp:has(.login-container) [data-testid="stToolbar"],
        #MainMenu,
        footer {{
            display: none !important;
        }}

        /* ========== LOGIN CONTAINER (CENTERED) ========== */
        .login-container {{
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            z-index: 99999 !important;
            width: 92% !important;
            max-width: 460px !important;
            animation: floatIn 0.9s cubic-bezier(0.16, 1, 0.3, 1) both;
        }}

        @keyframes floatIn {{
            from {{
                opacity: 0;
                transform: translate(-50%, -46%) scale(0.93);
                filter: blur(12px);
            }}
            to {{
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
                filter: blur(0);
            }}
        }}

        /* ========== PREMIUM GLASS CARD ========== */
        .glass-card {{
            background: rgba(255, 255, 255, 0.09) !important;
            backdrop-filter: blur(45px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(45px) saturate(180%) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: {RADIUS['xl']} !important;
            padding: 48px 44px !important;
            box-shadow:
                0 40px 80px rgba(0, 0, 0, 0.5),
                0 0 0 1px rgba(255, 255, 255, 0.06) inset,
                0 2px 4px rgba(255, 255, 255, 0.12) inset !important;
            position: relative;
            overflow: hidden;
        }}

        /* Subtle shine effect */
        .glass-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(255, 255, 255, 0.03),
                transparent
            );
            animation: rotate 8s linear infinite;
        }}

        @keyframes rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        /* ========== LOGO & BRANDING ========== */
        .login-header {{
            text-align: center !important;
            margin-bottom: 40px !important;
            position: relative;
            z-index: 1;
        }}

        .logo-container {{
            margin-bottom: 16px;
            animation: logoFloat 3s ease-in-out infinite;
        }}

        @keyframes logoFloat {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-6px); }}
        }}

        .logo-container img {{
            width: 220px !important;
            height: auto !important;
            filter: drop-shadow(0 8px 24px rgba(255, 255, 255, 0.15));
            opacity: 0.95;
        }}

        .login-tagline {{
            font-size: 15px !important;
            font-weight: 500 !important;
            color: rgba(255, 255, 255, 0.75) !important;
            margin: 12px 0 0 0 !important;
            letter-spacing: 0.03em !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }}

        /* ========== INPUT FIELDS (APPLE STYLE) ========== */
        .login-container .stTextInput > label {{
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            margin-bottom: 8px !important;
            letter-spacing: 0.01em !important;
            font-family: 'Inter', sans-serif !important;
        }}

        .login-container .stTextInput > div > div > input {{
            background: rgba(231, 241, 239, 0.08) !important;
            border: 1.5px solid rgba(231, 241, 239, 0.15) !important;
            border-radius: {RADIUS['md']} !important;
            padding: 15px 18px !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            color: #FFFFFF !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
            font-family: 'Inter', sans-serif !important;
        }}

        .login-container .stTextInput > div > div > input::placeholder {{
            color: rgba(255, 255, 255, 0.4) !important;
            font-weight: 400 !important;
        }}

        .login-container .stTextInput > div > div > input:focus {{
            background: rgba(231, 241, 239, 0.12) !important;
            border-color: {COLORS['secondary']} !important;
            box-shadow:
                0 0 0 4px rgba(184, 212, 209, 0.12),
                0 4px 16px rgba(0, 0, 0, 0.25) !important;
            outline: none !important;
        }}

        /* Remove dark backgrounds */
        .login-container .stTextInput,
        .login-container .stTextInput > div,
        .login-container .stTextInput > div > div {{
            background: transparent !important;
        }}

        /* ========== PASSWORD CONTROLS ========== */
        .password-controls {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 14px 0 20px 0;
            padding: 10px 14px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: {RADIUS['sm']};
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .login-container .stCheckbox {{
            margin: 0 !important;
        }}

        .login-container .stCheckbox > label {{
            color: rgba(255, 255, 255, 0.8) !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }}

        .login-container .stCheckbox input[type="checkbox"] {{
            width: 18px !important;
            height: 18px !important;
            cursor: pointer !important;
            accent-color: {COLORS['secondary']} !important;
        }}

        /* ========== CAPS LOCK WARNING ========== */
        .caps-warning {{
            display: none;
            align-items: center;
            gap: 8px;
            padding: 10px 14px;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.35);
            border-radius: {RADIUS['sm']};
            margin: 0 0 16px 0;
            animation: slideDown 0.3s ease;
        }}

        .caps-warning.active {{
            display: flex;
        }}

        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-8px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .caps-warning span {{
            color: #FCD34D;
            font-size: 13px;
            font-weight: 500;
        }}

        /* ========== LOGIN BUTTON (PRIMARY BRAND COLOR) ========== */
        .login-container .stButton > button {{
            width: 100% !important;
            background: linear-gradient(
                135deg,
                {COLORS['primary']} 0%,
                {COLORS['dark_accent']} 100%
            ) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
            color: #FFFFFF !important;
            border-radius: {RADIUS['md']} !important;
            padding: 17px 32px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow:
                0 12px 36px rgba(42, 79, 87, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
            margin-top: 8px !important;
            font-family: 'Inter', sans-serif !important;
            position: relative;
            overflow: hidden;
        }}

        /* Button glow effect */
        .login-container .stButton > button::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.15);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }}

        .login-container .stButton > button:hover {{
            transform: translateY(-2px) !important;
            background: linear-gradient(
                135deg,
                {COLORS['primary']} 0%,
                #1A2528 100%
            ) !important;
            border-color: rgba(255, 255, 255, 0.25) !important;
            box-shadow:
                0 16px 48px rgba(42, 79, 87, 0.5),
                0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
        }}

        .login-container .stButton > button:hover::after {{
            width: 300px;
            height: 300px;
        }}

        .login-container .stButton > button:active {{
            transform: translateY(0) scale(0.98) !important;
            box-shadow:
                0 8px 24px rgba(42, 79, 87, 0.35),
                0 0 0 1px rgba(255, 255, 255, 0.15) inset !important;
        }}

        /* ========== ERROR ALERT ========== */
        .error-alert {{
            background: rgba(239, 68, 68, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            border: 1.5px solid rgba(239, 68, 68, 0.35) !important;
            border-radius: {RADIUS['md']} !important;
            padding: 14px 18px !important;
            margin-bottom: 20px !important;
            color: #FCA5A5 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            text-align: center !important;
            animation: shake 0.5s ease, fadeIn 0.3s ease !important;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}

        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            10%, 30%, 50%, 70%, 90% {{ transform: translateX(-5px); }}
            20%, 40%, 60%, 80% {{ transform: translateX(5px); }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* ========== DIVIDER ========== */
        .divider {{
            height: 1px !important;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.15),
                transparent
            ) !important;
            margin: 28px 0 24px 0 !important;
        }}

        /* ========== MOBILE RESPONSIVE ========== */
        @media (max-width: 600px) {{
            .glass-card {{
                padding: 36px 28px !important;
            }}

            .logo-container img {{
                width: 180px !important;
            }}

            .login-tagline {{
                font-size: 14px !important;
            }}
        }}
    </style>

    <!-- Dark Gradient Background -->
    <div class="login-screen"></div>
    """, unsafe_allow_html=True)

    # Render Login Card
    st.markdown('<div class="login-container"><div class="glass-card">', unsafe_allow_html=True)

    # Logo & Header
    if logo_base64:
        st.markdown(f"""
        <div class="login-header">
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" alt="EVALUERA" />
            </div>
            <div class="login-tagline">KI-gestützte Kostenanalyse</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback if logo not found
        st.markdown("""
        <div class="login-header">
            <div style="font-size: 42px; font-weight: 800; color: rgba(255,255,255,0.95); margin-bottom: 8px; letter-spacing: -0.02em;">
                EVALUERA
            </div>
            <div class="login-tagline">KI-gestützte Kostenanalyse</div>
        </div>
        """, unsafe_allow_html=True)

    # Error Message
    if st.session_state.login_error:
        st.markdown("""
        <div class="error-alert">
            <svg width="18" height="18" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <span>Ungültige Zugangsdaten</span>
        </div>
        """, unsafe_allow_html=True)

    # Username Input
    st.markdown('<div style="margin-bottom: 18px;">', unsafe_allow_html=True)
    username = st.text_input(
        "Benutzername",
        placeholder="Ihr Benutzername",
        key="login_username",
        label_visibility="visible"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Password Input
    st.markdown('<div style="margin-bottom: 4px;">', unsafe_allow_html=True)
    password = st.text_input(
        "Passwort",
        type="default" if st.session_state.show_password else "password",
        placeholder="Ihr Passwort",
        key="login_password",
        label_visibility="visible"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Password Controls
    st.markdown('<div class="password-controls">', unsafe_allow_html=True)
    col1, col2 = st.columns([0.07, 0.93])
    with col1:
        show_pwd = st.checkbox("", key="show_pwd_toggle", value=st.session_state.show_password)
        st.session_state.show_password = show_pwd
    with col2:
        icon = "🔓" if show_pwd else "👁️"
        text = "Passwort verbergen" if show_pwd else "Passwort anzeigen"
        st.markdown(
            f'<span style="color: rgba(255,255,255,0.8); font-size: 13px; font-weight: 500;">{icon} {text}</span>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Caps Lock Warning
    st.markdown("""
    <script>
        document.addEventListener('keyup', function(e) {
            const warning = document.getElementById('caps-warning');
            if (warning) {
                if (e.getModifierState && e.getModifierState('CapsLock')) {
                    warning.classList.add('active');
                } else {
                    warning.classList.remove('active');
                }
            }
        });
    </script>
    <div id="caps-warning" class="caps-warning">
        <svg width="16" height="16" viewBox="0 0 20 20" fill="#FCD34D">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
        </svg>
        <span>Caps Lock ist aktiviert</span>
    </div>
    """, unsafe_allow_html=True)

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
    """Render premium logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"""
        <div style="
            padding: 18px;
            background: linear-gradient(135deg, rgba(42, 79, 87, 0.08) 0%, rgba(184, 212, 209, 0.08) 100%);
            backdrop-filter: blur(10px);
            border-radius: {RADIUS['md']};
            text-align: center;
            box-shadow: {SHADOWS['sm']};
            border: 1.5px solid {COLORS['gray_200']};
        ">
            <div style="
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: {COLORS['gray_500']};
                margin-bottom: 10px;
            ">
                Eingeloggt als
            </div>
            <div style="
                font-weight: 700;
                font-size: 17px;
                color: {COLORS['primary']};
                letter-spacing: -0.01em;
            ">
                {st.session_state.get('username', 'Benutzer')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Abmelden", use_container_width=True):
            logout()


def inject_lottie_background():
    """
    Legacy function - background is now handled via CSS
    Kept for compatibility with existing code
    """
    pass
