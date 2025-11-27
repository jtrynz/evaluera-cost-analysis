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
    - Dynamic Mesh Gradient Background (CSS Animation)
    - EVALUERA logo (PNG)
    - Enhanced Glassmorphism Card
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
    
    # Load background image
    bg_base64 = ""
    try:
        # Construct absolute path to assets/login_bg_final.jpg
        bg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'login_bg_final.jpg')
        with open(bg_path, "rb") as f:
            bg_base64 = base64.b64encode(f.read()).decode()
    except Exception as e:
        # Fallback if image missing
        print(f"Error loading background: {e}")
        pass

    # CSS for background
    if bg_base64:
        background_css = f"""
            background-image: url("data:image/jpeg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        """
    else:
        # Fallback gradient (Minty)
        background_css = """
            background: linear-gradient(-45deg, #B8D4D1, #E7F1EF, #B8D4D1, #8FAEAB);
            background-size: 400% 400%;
            animation: gradient-animation 15s ease infinite;
        """

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            :root {{
                --eval-primary: {COLORS['primary']};
                --eval-secondary: {COLORS['secondary']};
                --eval-dark: {COLORS['dark_accent']};
                --eval-glass: rgba(255, 255, 255, 0.25); /* Slightly more opaque for mint bg */
                --eval-soft: #E7F1EF;
            }}

            /* DYNAMIC BACKGROUND */
            html, body, .stApp, [data-testid="stAppViewContainer"] {{
                {background_css}
                height: 100vh;
                overflow: hidden;
            }}

            @keyframes float {{
                0% {{ transform: translateY(0px); }}
                50% {{ transform: translateY(-8px); }}
                100% {{ transform: translateY(0px); }}
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
                padding: 48px 40px !important;
                width: 100%;
                max-width: 460px;
                margin-top: 0 !important;
                
                /* PREMIUM GLASSMORPHISM */
                background: rgba(255, 255, 255, 0.60);
                backdrop-filter: blur(24px) saturate(180%);
                -webkit-backdrop-filter: blur(24px) saturate(180%);
                border: 1px solid rgba(255, 255, 255, 0.6);
                
                border-radius: 28px;
                box-shadow:
                    0 25px 50px -12px rgba(0, 0, 0, 0.15),
                    0 0 0 1px rgba(255, 255, 255, 0.4) inset;
                
                position: relative;
                overflow: hidden;
                animation: float 8s ease-in-out infinite;
            }}

            /* Entfernt evtl. leere Streifen-Container */
            .block-container > div:empty {{
                display: none !important;
            }}

            .login-header {{
                text-align: center;
                margin-bottom: 32px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}

            .login-logo {{
                width: 190px;
                height: auto;
                filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
                margin-bottom: 12px;
                display: block;
                margin-left: auto;
                margin-right: auto;
            }}

            .login-title {{
                color: #1E2E32;
                font-size: 24px;
                font-weight: 700;
                letter-spacing: -0.02em;
                margin-bottom: 4px;
            }}

            .login-tagline {{
                color: rgba(30, 46, 50, 0.75);
                font-size: 14px;
                font-weight: 500;
            }}

            .stTextInput > label {{
                color: #2A4F57 !important;
                font-weight: 600 !important;
                font-size: 13px !important;
                letter-spacing: 0.03em !important;
                margin-bottom: 6px !important;
                text-transform: uppercase;
            }}

            .stTextInput > div > div > input {{
                background: rgba(255, 255, 255, 0.5) !important;
                border: 1px solid rgba(42, 79, 87, 0.2) !important;
                border-radius: 12px !important;
                color: #1E2E32 !important;
                padding: 12px 16px !important;
                font-size: 15px !important;
                min-height: 46px !important;
                transition: all 0.2s ease !important;
            }}

            .stTextInput > div > div > input::placeholder {{
                color: rgba(30, 46, 50, 0.45) !important;
            }}

            .stTextInput > div > div > input:focus {{
                background: #FFFFFF !important;
                border-color: #2A4F57 !important;
                box-shadow: 0 0 0 3px rgba(42, 79, 87, 0.1) !important;
                transform: translateY(-1px);
            }}

            /* Button Styling - HIGH CONTRAST */
            .stButton > button {{
                width: 100% !important;
                background: #1E2E32 !important; /* Dark Charcoal for max contrast */
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 14px !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                letter-spacing: 0.01em !important;
                box-shadow: 0 4px 12px rgba(30, 46, 50, 0.3) !important;
                transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
                margin-top: 12px !important;
            }}

            .stButton > button:hover {{
                background: #2A4F57 !important; /* Deep Teal on hover */
                transform: translateY(-2px) !important;
                box-shadow: 0 8px 20px rgba(30, 46, 50, 0.4) !important;
            }}

            .stButton > button:active {{
                transform: translateY(0) scale(0.98) !important;
            }}

            .login-divider {{
                height: 1px;
                width: 100%;
                background: linear-gradient(90deg, transparent, rgba(42, 79, 87, 0.15), transparent);
                margin: 24px 0;
            }}

            .error-alert {{
                background: rgba(239, 68, 68, 0.08) !important;
                border: 1px solid rgba(239, 68, 68, 0.2) !important;
                color: #EF4444 !important;
                border-radius: 10px !important;
                padding: 10px !important;
                margin-bottom: 20px !important;
                text-align: center;
                font-size: 13px;
                font-weight: 500;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }}

            .login-footnote {{
                text-align: center;
                color: rgba(255, 255, 255, 0.7);
                font-size: 11px;
                margin-top: 24px;
                font-weight: 500;
                letter-spacing: 0.05em;
                text-transform: uppercase;
            }}
            
            .forgot-link {{
                text-align: right;
                margin-top: 8px;
            }}
            
            .forgot-link a {{
                color: #2A4F57;
                font-size: 12px;
                text-decoration: none;
                font-weight: 600;
                opacity: 0.8;
                transition: opacity 0.2s;
            }}
            
            .forgot-link a:hover {{
                opacity: 1;
                text-decoration: underline;
            }}

            @media (max-width: 600px) {{
                .login-card {{
                    padding: 26px 22px 22px 22px;
                }}

                .login-logo {{
                    width: 160px;
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
                <div class="login-tagline">Sichere Anmeldung zur KI-Kostenanalyse</div>
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
                <span>Benutzername oder Passwort falsch</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    username = st.text_input(
        "Benutzername",
        placeholder="name@firma.de",
        key="login_username",
        label_visibility="visible",
    )

    password = st.text_input(
        "Passwort",
        type="password",
        placeholder="••••••••",
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

    st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)

    if st.button("Anmelden", use_container_width=True, key="login_btn"):
        if username and password:
            with st.spinner("Authentifizierung..."):
                success = login(username, password)
            st.session_state.login_error = not success
            if success:
                st.rerun()
        else:
            st.session_state.login_error = True

    st.markdown('<div class="login-footnote">EVALUERA BRAND EXPERIENCE</div>', unsafe_allow_html=True)
    st.markdown('</div></div></div>', unsafe_allow_html=True)


def render_logout_button():
    """Render premium logout button in sidebar"""
    with st.sidebar:
        # Divider removed to allow custom layout in app.py
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

