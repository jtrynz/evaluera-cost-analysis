"""
🔐 EVALUERA - Premium Apple-Inspired Login Screen
===================================================
Modern authentication with glassmorphism, dark gradient background,
and UX best practices following Apple Human Interface Guidelines
"""

import streamlit as st
import os
import json
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


# ==================== PREMIUM LOGIN SCREEN ====================
def render_login_screen():
    """
    Render premium Apple-inspired login screen with:
    - Dark gradient animated background
    - Glassmorphism card
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
    if "username_valid" not in st.session_state:
        st.session_state.username_valid = False

    # Inject Premium CSS
    st.markdown(f"""
    <style>
        /* ========== APPLE SF PRO FONT ========== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ========== DARK GRADIENT BACKGROUND ========== */
        .login-screen {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(
                135deg,
                #1E2E32 0%,
                #2A4F57 25%,
                #1E2E32 50%,
                #2A4F57 75%,
                #1E2E32 100%
            );
            background-size: 400% 400%;
            animation: gradientFlow 15s ease infinite;
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
            background: radial-gradient(
                circle at 20% 50%,
                rgba(47, 74, 86, 0.3) 0%,
                transparent 50%
            ),
            radial-gradient(
                circle at 80% 80%,
                rgba(47, 74, 86, 0.2) 0%,
                transparent 50%
            );
            animation: patternMove 20s ease-in-out infinite;
        }}

        @keyframes patternMove {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 0.8; }}
        }}

        /* Hide Streamlit default elements */
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
            width: 90% !important;
            max-width: 480px !important;
            animation: floatIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
        }}

        @keyframes floatIn {{
            from {{
                opacity: 0;
                transform: translate(-50%, -45%) scale(0.94);
                filter: blur(10px);
            }}
            to {{
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
                filter: blur(0);
            }}
        }}

        /* ========== GLASS CARD (PREMIUM FROSTED) ========== */
        .glass-card {{
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(40px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: {RADIUS['xl']} !important;
            padding: 56px 48px !important;
            box-shadow:
                0 32px 64px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.05) inset,
                0 1px 2px rgba(255, 255, 255, 0.1) inset !important;
            position: relative;
            overflow: hidden;
        }}

        /* Subtle light reflection */
        .glass-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -75%;
            width: 50%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.03),
                transparent
            );
            animation: shimmer 8s infinite;
        }}

        @keyframes shimmer {{
            0%, 100% {{ left: -75%; }}
            50% {{ left: 125%; }}
        }}

        /* ========== LOGO & BRANDING (APPLE-STYLE) ========== */
        .login-header {{
            text-align: center !important;
            margin-bottom: 48px !important;
        }}

        .login-logo {{
            font-size: 48px !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
            background: linear-gradient(
                135deg,
                #FFFFFF 0%,
                rgba(255, 255, 255, 0.85) 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 12px 0 !important;
            text-shadow: 0 4px 16px rgba(255, 255, 255, 0.1);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        .login-tagline {{
            font-size: 16px !important;
            font-weight: 500 !important;
            color: rgba(255, 255, 255, 0.7) !important;
            margin: 0 !important;
            letter-spacing: 0.02em !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }}

        /* ========== INPUT FIELDS (APPLE CLEAN) ========== */
        .login-container .stTextInput > div > div > input {{
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: {RADIUS['md']} !important;
            padding: 16px 20px !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            color: #FFFFFF !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
        }}

        .login-container .stTextInput > div > div > input::placeholder {{
            color: rgba(255, 255, 255, 0.4) !important;
            font-weight: 400 !important;
        }}

        .login-container .stTextInput > div > div > input:focus {{
            background: rgba(255, 255, 255, 0.09) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            box-shadow:
                0 0 0 4px rgba(255, 255, 255, 0.08),
                0 4px 16px rgba(0, 0, 0, 0.2) !important;
            outline: none !important;
        }}

        /* Valid input indicator */
        .input-valid input {{
            border-color: #10B981 !important;
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15) !important;
        }}

        /* Remove dark backgrounds */
        .login-container .stTextInput,
        .login-container .stTextInput > div,
        .login-container .stTextInput > div > div {{
            background: transparent !important;
        }}

        /* Input labels */
        .login-container .stTextInput > label {{
            color: rgba(255, 255, 255, 0.85) !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            margin-bottom: 8px !important;
            letter-spacing: 0.01em !important;
        }}

        /* ========== PASSWORD TOGGLE (PREMIUM) ========== */
        .password-controls {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 16px 0 24px 0;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.04);
            border-radius: {RADIUS['md']};
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .login-container .stCheckbox {{
            margin: 0 !important;
        }}

        .login-container .stCheckbox > label {{
            color: rgba(255, 255, 255, 0.75) !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .login-container .stCheckbox input[type="checkbox"] {{
            width: 20px !important;
            height: 20px !important;
            cursor: pointer !important;
            accent-color: rgba(255, 255, 255, 0.3) !important;
        }}

        /* ========== CAPS LOCK WARNING ========== */
        .caps-lock-warning {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 14px;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: {RADIUS['sm']};
            margin: -8px 0 16px 0;
            animation: slideDown 0.3s ease;
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

        .caps-lock-warning span {{
            color: #F59E0B;
            font-size: 13px;
            font-weight: 500;
        }}

        /* ========== LOGIN BUTTON (PREMIUM GRADIENT) ========== */
        .login-container .stButton > button {{
            width: 100% !important;
            background: linear-gradient(
                135deg,
                rgba(255, 255, 255, 0.15) 0%,
                rgba(255, 255, 255, 0.08) 100%
            ) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
            color: #FFFFFF !important;
            border-radius: {RADIUS['md']} !important;
            padding: 18px 32px !important;
            font-size: 17px !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow:
                0 12px 32px rgba(0, 0, 0, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
            margin-top: 8px !important;
            font-family: 'Inter', -apple-system, sans-serif !important;
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
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent
            );
            transition: left 0.5s;
        }}

        .login-container .stButton > button:hover {{
            transform: translateY(-2px) !important;
            background: linear-gradient(
                135deg,
                rgba(255, 255, 255, 0.2) 0%,
                rgba(255, 255, 255, 0.12) 100%
            ) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            box-shadow:
                0 16px 40px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
        }}

        .login-container .stButton > button:hover::before {{
            left: 100%;
        }}

        .login-container .stButton > button:active {{
            transform: translateY(0) scale(0.98) !important;
            box-shadow:
                0 8px 24px rgba(0, 0, 0, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.1) inset !important;
        }}

        /* ========== ERROR MESSAGE (APPLE ALERT) ========== */
        .error-alert {{
            background: rgba(239, 68, 68, 0.15) !important;
            backdrop-filter: blur(10px) !important;
            border: 1.5px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: {RADIUS['md']} !important;
            padding: 16px 20px !important;
            margin-bottom: 24px !important;
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
            10%, 30%, 50%, 70%, 90% {{ transform: translateX(-6px); }}
            20%, 40%, 60%, 80% {{ transform: translateX(6px); }}
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
            margin: 32px 0 28px 0 !important;
        }}

        /* ========== FOOTER HINT ========== */
        .login-footer {{
            text-align: center;
            margin-top: 32px;
            padding-top: 24px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }}

        .login-footer p {{
            color: rgba(255, 255, 255, 0.5);
            font-size: 13px;
            font-weight: 400;
            margin: 0;
            line-height: 1.6;
        }}

        .demo-credentials {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: {RADIUS['sm']};
            padding: 12px 16px;
            margin-top: 12px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 12px;
            color: rgba(255, 255, 255, 0.7);
            text-align: left;
        }}

        .demo-credentials code {{
            background: rgba(255, 255, 255, 0.08);
            padding: 2px 6px;
            border-radius: 4px;
            color: #B8D4D1;
        }}
    </style>

    <!-- Dark Gradient Background -->
    <div class="login-screen"></div>
    """, unsafe_allow_html=True)

    # Render Login Card
    st.markdown('<div class="login-container"><div class="glass-card">', unsafe_allow_html=True)

    # Logo & Header
    st.markdown("""
    <div class="login-header">
        <div class="login-logo">EVALUERA</div>
        <div class="login-tagline">KI-gestützte Kostenanalyse</div>
    </div>
    """, unsafe_allow_html=True)

    # Error Message
    if st.session_state.login_error:
        st.markdown("""
        <div class="error-alert">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <span>Ungültige Zugangsdaten. Bitte erneut versuchen.</span>
        </div>
        """, unsafe_allow_html=True)

    # Username Input
    st.markdown('<div style="margin-bottom: 20px;">', unsafe_allow_html=True)
    username = st.text_input(
        "Benutzername",
        placeholder="Geben Sie Ihren Benutzernamen ein",
        key="login_username",
        label_visibility="visible"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Password Input
    st.markdown('<div style="margin-bottom: 8px;">', unsafe_allow_html=True)
    password = st.text_input(
        "Passwort",
        type="default" if st.session_state.show_password else "password",
        placeholder="Geben Sie Ihr Passwort ein",
        key="login_password",
        label_visibility="visible"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Password Controls (Show Password + Caps Lock Warning)
    st.markdown('<div class="password-controls">', unsafe_allow_html=True)
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        show_pwd = st.checkbox("", key="show_pwd_toggle", value=st.session_state.show_password)
        st.session_state.show_password = show_pwd
    with col2:
        st.markdown(
            f'<span style="color: rgba(255,255,255,0.75); font-size: 14px; font-weight: 500;">{"🔓 Passwort verbergen" if show_pwd else "👁️ Passwort anzeigen"}</span>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Caps Lock Warning (JavaScript-based)
    st.markdown("""
    <script>
        document.addEventListener('keyup', function(event) {
            if (event.getModifierState && event.getModifierState('CapsLock')) {
                const warning = document.getElementById('caps-warning');
                if (warning) warning.style.display = 'flex';
            } else {
                const warning = document.getElementById('caps-warning');
                if (warning) warning.style.display = 'none';
            }
        });
    </script>
    <div id="caps-warning" class="caps-lock-warning" style="display: none;">
        <svg width="16" height="16" viewBox="0 0 20 20" fill="#F59E0B">
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

    # Footer with demo credentials
    st.markdown("""
    <div class="login-footer">
        <p>Demo-Zugang für Testzwecke:</p>
        <div class="demo-credentials">
            <code>admin</code> / <code>evaluera2024</code><br>
            <code>demo</code> / <code>demo123</code>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)


def render_logout_button():
    """Render premium logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"""
        <div style="
            padding: 20px;
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


def inject_lottie_background():
    """
    Inject dark gradient background animation
    Note: Background is now handled via CSS gradient in render_login_screen()
    This function is kept for compatibility but not required
    """
    pass
