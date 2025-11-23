"""
🔐 EVALUERA - Premium Apple-Inspired Login Screen
===================================================
Professional authentication with glassmorphism, dark gradient,
and Apple Human Interface Guidelines compliance
"""

import streamlit as st
import os
import base64
from src.ui.theme import COLORS, RADIUS, SHADOWS


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
    Render premium EVALUERA-branded login screen with:
    - Dark gradient animated background (Lottie)
    - EVALUERA logo (PNG)
    - Premium glassmorphism card
    - Live input validation
    - Caps Lock warning
    - Smooth animations
    - Apple-like typography
    """

    # Initialize session state
    if "login_error" not in st.session_state:
        st.session_state.login_error = False

    # Get logo
    logo_base64 = get_logo_base64()

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            :root {{
                --eval-primary: {COLORS['primary']};
                --eval-secondary: {COLORS['secondary']};
                --eval-dark: {COLORS['dark_accent']};
                --eval-glass: rgba(255, 255, 255, 0.92);
                --eval-soft: #E7F1EF;
            }}

            html, body, .stApp, [data-testid="stAppViewContainer"] {{
                background: linear-gradient(140deg, #a9d9d3 0%, #88c2bd 45%, #6fa9a2 100%) !important;
            }}

            header[data-testid="stHeader"],
            #MainMenu,
            footer,
            [data-testid="stSidebar"],
            [data-testid="stToolbar"] {{
                display: none !important;
            }}

            section.main, .main {{
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 12px 0 18px 0 !important;
                position: relative;
                z-index: 2;
            }}

            .block-container {{
                padding: 0 !important;
                width: 100%;
                max-width: 520px;
                margin-top: 0 !important;
            }}

            .login-shell {{
                width: 100%;
                padding: 32px 16px;
                display: flex;
                justify-content: center;
            }}

            .login-card {{
                width: 100%;
                background: var(--eval-glass);
                border: 1px solid rgba(42, 79, 87, 0.18);
                border-radius: {RADIUS['xl']};
                box-shadow:
                    0 18px 55px rgba(0, 0, 0, 0.25),
                    0 0 0 1px rgba(255, 255, 255, 0.12) inset;
                padding: 32px 26px 28px 26px;
                position: relative;
                overflow: hidden;
            }}

            .login-inner {{
                position: relative;
                z-index: 2;
            }}

            .login-header {{
                text-align: center;
                margin-bottom: 20px;
            }}

            .login-logo {{
                width: 210px;
                height: auto;
                filter: drop-shadow(0 10px 30px rgba(0,0,0,0.45));
            }}

            /* Hinweis: ehemaliger liquid-glass Header bewusst entfernt (Balken über Logo) */

            .login-title {{
                color: #1E2E32;
                font-size: 24px;
                font-weight: 800;
                letter-spacing: -0.02em;
                margin-top: 10px;
                margin-bottom: 2px;
            }}

            .login-tagline {{
                color: rgba(30, 46, 50, 0.82);
                font-size: 15px;
                font-weight: 500;
                letter-spacing: 0.01em;
            }}

            .stTextInput > label {{
                color: #1E2E32 !important;
                font-weight: 600 !important;
                letter-spacing: 0.01em !important;
                margin-bottom: 6px !important;
            }}

            .stTextInput > div > div > input {{
                background: var(--eval-soft) !important;
                border: 1.5px solid rgba(42, 79, 87, 0.35) !important;
                border-radius: {RADIUS['md']} !important;
                color: #1E2E32 !important;
                padding: 14px 16px !important;
                font-size: 15px !important;
                transition: all 0.25s ease !important;
                box-shadow: 0 6px 18px rgba(0,0,0,0.12) !important;
            }}

            .stTextInput > div > div > input::placeholder {{
                color: rgba(30, 46, 50, 0.55) !important;
                font-weight: 400 !important;
            }}

            .stTextInput > div > div > input:focus {{
                border-color: #2A4F57 !important;
                box-shadow:
                    0 0 0 2px rgba(42, 79, 87, 0.28),
                    0 6px 16px rgba(0,0,0,0.18) !important;
                outline: none !important;
                background: #F6FAF9 !important;
            }}

            .stTextInput > div > div > input:invalid,
            .stTextInput > div > div > input:invalid:focus {{
                border-color: #2A4F57 !important;
                box-shadow:
                    0 0 0 2px rgba(42, 79, 87, 0.2),
                    0 4px 12px rgba(0,0,0,0.12) !important;
            }}

            .stCheckbox > label {{
                color: #1E2E32 !important;
                font-weight: 500 !important;
            }}

            .stCheckbox input[type="checkbox"] {{
                accent-color: var(--eval-secondary) !important;
                width: 18px !important;
                height: 18px !important;
            }}

            .login-divider {{
                height: 1px;
                width: 100%;
                background: linear-gradient(90deg, transparent, rgba(184, 212, 209, 0.35), transparent);
                margin: 18px 0 16px 0;
            }}

            .caps-warning {{
                display: none;
                align-items: center;
                gap: 8px;
                padding: 10px 14px;
                background: rgba(245, 158, 11, 0.12);
                border: 1px solid rgba(245, 158, 11, 0.32);
                border-radius: {RADIUS['sm']};
                color: #FCD34D;
                font-weight: 600;
                font-size: 13px;
                margin-top: 6px;
            }}

            .caps-warning.active {{
                display: flex;
            }}

            .stButton > button {{
                width: 100% !important;
                background: linear-gradient(135deg, #2A4F57 0%, #1E2E32 100%) !important;
                color: #F6FAF9 !important;
                border: none !important;
                border-radius: {RADIUS['md']} !important;
                padding: 15px 18px !important;
                font-size: 16px !important;
                font-weight: 700 !important;
                letter-spacing: 0.01em !important;
                box-shadow:
                    0 14px 32px rgba(0, 0, 0, 0.25),
                    0 0 0 1px rgba(255,255,255,0.1) inset !important;
                transition: all 0.22s ease !important;
            }}

            .stButton > button:hover {{
                transform: translateY(-1px) scale(1.01) !important;
                box-shadow:
                    0 18px 40px rgba(0, 0, 0, 0.4),
                    0 0 0 1px rgba(255,255,255,0.12) inset !important;
            }}

            .stButton > button:active {{
                transform: translateY(0) scale(0.99) !important;
            }}

            .error-alert {{
                background: rgba(239, 68, 68, 0.16) !important;
                border: 1.5px solid rgba(239, 68, 68, 0.4) !important;
                color: #FCA5A5 !important;
                border-radius: {RADIUS['md']} !important;
                padding: 12px 14px !important;
                margin: 10px 0 8px 0 !important;
                text-align: center;
                font-weight: 600;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }}

            .login-footnote {{
                text-align: center;
                color: rgba(231, 241, 239, 0.65);
                font-size: 12px;
                margin-top: 12px;
            }}

            /* Remove any visible iframe dot from Lottie component */
            iframe[title="st.components.v1.html"] {{
                position: fixed !important;
                inset: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                border: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
                opacity: 1 !important;
                pointer-events: none !important;
                background: transparent !important;
            }}

            .forgot-link {{
                margin-top: 8px;
                text-align: right;
            }}

            .forgot-link a {{
                color: {COLORS['primary']} !important;
                font-weight: 600;
                text-decoration: none;
            }}

            .forgot-link a:hover {{
                text-decoration: underline;
            }}

            @media (max-width: 600px) {{
                .login-card {{
                    padding: 26px 22px 22px 22px;
                }}

                .login-logo {{
                    width: 180px;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Layout shell
    st.markdown('<div class="login-shell"><div class="login-card"><div class="login-inner">', unsafe_allow_html=True)

    # Logo & Header
    if logo_base64:
        st.markdown(
            f"""
            <div class="login-header">
                <img class="login-logo" src="data:image/png;base64,{logo_base64}" alt="EVALUERA Logo" />
                <div class="login-title">Willkommen zurück</div>
                <div class="login-tagline">Sichere Anmeldung zur KI-gestützten Kostenanalyse</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="login-header">
                <div class="login-title">EVALUERA</div>
                <div class="login-tagline">KI-gestützte Kostenanalyse</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Error Message
    if st.session_state.login_error:
        st.markdown(
            """
            <div class="error-alert">
                <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
                </svg>
                <span>Ungültige Zugangsdaten</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    username = st.text_input(
        "Benutzername",
        placeholder="Ihr Benutzername",
        key="login_username",
        label_visibility="visible",
    )

    password = st.text_input(
        "Passwort",
        type="password",
        placeholder="Ihr Passwort",
        key="login_password",
        label_visibility="visible",
    )

    st.markdown(
        """
        <div class="forgot-link">
            <a href="#" aria-label="Passwort vergessen">Passwort vergessen?</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)

    if st.button("🔐  Sicher anmelden", use_container_width=True, key="login_btn"):
        if username and password:
            with st.spinner("Authentifizierung läuft..."):
                success = login(username, password)
            st.session_state.login_error = not success
            if success:
                st.rerun()
        else:
            st.session_state.login_error = True

    st.markdown('<div class="login-footnote">Nur für autorisierte Nutzer – Evaluera Brand Experience</div>', unsafe_allow_html=True)
    st.markdown('</div></div></div>', unsafe_allow_html=True)


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
    Previously rendered animated Lottie background.
    Disabled to keep the mint gradient clean (liquid glass header removed).
    """
    return
