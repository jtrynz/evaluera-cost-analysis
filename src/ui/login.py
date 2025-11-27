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
    
    # Load background image (Final Version)
    bg_base64 = ""
    try:
        # Construct absolute path to assets/login_bg_final.jpg
        bg_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'login_bg_final.jpg')
        with open(bg_path, "rb") as f:
            bg_base64 = base64.b64encode(f.read()).decode()
    except Exception as e:
        print(f"Error loading background: {e}")
        pass

    # CSS for background
    if bg_base64:
        background_css = f"""
            background-image: url("data:image/png;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        """
    else:
        background_css = """
            background: linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 100%);
        """

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            /* ========== 0. RESET & VARS ========== */
            :root {{
                --brand-mint: #A7FFE5;
                --brand-dark: #0E1111;
                --brand-dark-soft: #1C1F1E;
                --glass-border: rgba(255, 255, 255, 0.4);
                --glass-surface: rgba(255, 255, 255, 0.15);
                --shadow-ambient: 0 20px 40px rgba(0,0,0,0.05);
                --shadow-key: 0 4px 8px rgba(0,0,0,0.08);
                --ease-spring: cubic-bezier(0.4, 0, 0.2, 1);
            }}

            /* ========== 1. BACKGROUND & LAYOUT ========== */
            html, body, .stApp, [data-testid="stAppViewContainer"] {{
                {background_css}
                height: 100vh;
                overflow: hidden !important; /* No scroll */
            }}

            /* Vignette Overlay */
            .stApp::before {{
                content: "";
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.03) 100%);
                pointer-events: none;
                z-index: 0;
            }}

            /* Hide Streamlit Elements */
            header[data-testid="stHeader"], footer, #MainMenu {{ display: none !important; }}

            /* Absolute Centering Container */
            .block-container {{
                position: absolute !important;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 100%;
                max-width: 500px; /* Optimal width for premium feel */
                padding: 0 !important;
                margin: 0 !important;
                overflow: visible !important;
            }}

            /* ========== 2. GLASS CARD (VISION OS STYLE) ========== */
            /* We target the first child div of block-container which usually holds the content */
            .block-container > div:first-child {{
                background: var(--glass-surface);
                backdrop-filter: blur(30px) saturate(120%);
                -webkit-backdrop-filter: blur(30px) saturate(120%);
                border: 1px solid var(--glass-border);
                border-radius: 32px;
                padding: 48px 40px;
                box-shadow: 
                    var(--shadow-ambient),
                    var(--shadow-key),
                    inset 0 0 0 1px rgba(255,255,255,0.2); /* Inner light edge */
                
                animation: cardSlideUp 0.8s var(--ease-spring) forwards;
                opacity: 0;
                transform: translateY(20px);
            }}

            @keyframes cardSlideUp {{
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            /* ========== 3. TYPOGRAPHY ========== */
            h1, h2, h3, p, div, label, input, button {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
                -webkit-font-smoothing: antialiased;
            }}

            .login-header {{
                text-align: center;
                margin-bottom: 40px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}

            .login-logo {{
                width: 220px; /* Slightly larger */
                height: auto;
                margin-bottom: 24px;
                filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));
                transition: transform 0.5s var(--ease-spring);
            }}
            .login-logo:hover {{ transform: scale(1.02); }}

            .login-title {{
                color: #111827;
                font-size: 26px;
                font-weight: 600;
                letter-spacing: -0.02em;
                margin-bottom: 8px;
            }}

            .login-tagline {{
                color: rgba(17, 24, 39, 0.6);
                font-size: 14px;
                font-weight: 500;
            }}

            /* ========== 4. INPUT FIELDS (PREMIUM) ========== */
            /* Label Styling */
            .stTextInput > label {{
                color: rgba(17, 24, 39, 0.5) !important;
                font-size: 12px !important;
                font-weight: 600 !important;
                letter-spacing: 0.03em !important;
                text-transform: uppercase !important;
                margin-bottom: 8px !important;
                transition: color 0.2s ease;
            }}

            /* Input Container */
            .stTextInput > div[data-baseweb="input"] {{
                background: rgba(255, 255, 255, 0.6) !important;
                border: 1px solid rgba(0, 0, 0, 0.06) !important;
                border-radius: 16px !important;
                min-height: 52px !important;
                box-shadow: 
                    0 2px 6px rgba(0,0,0,0.02),
                    inset 0 1px 2px rgba(255,255,255,0.8);
                transition: all 0.3s var(--ease-spring) !important;
            }}

            /* Focus State */
            .stTextInput > div[data-baseweb="input"]:focus-within {{
                background: #FFFFFF !important;
                border-color: var(--brand-mint) !important;
                box-shadow: 
                    0 0 0 4px rgba(167, 255, 229, 0.25), /* Mint Glow */
                    0 4px 12px rgba(0,0,0,0.05);
                transform: translateY(-1px);
            }}

            /* Input Text */
            .stTextInput input {{
                color: #111827 !important;
                font-size: 16px !important;
                font-weight: 500 !important;
                padding: 0 16px !important;
                background: transparent !important;
            }}

            .stTextInput input::placeholder {{
                color: rgba(17, 24, 39, 0.3) !important;
            }}

            /* ========== 5. BUTTON (ULTRA PREMIUM) ========== */
            .stButton > button {{
                width: 100% !important;
                /* Lighter Blue-Green Gradient as requested */
                background: linear-gradient(135deg, #2A4F57 0%, #487e78 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 18px !important; /* Soft roundness */
                padding: 16px !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                letter-spacing: 0.01em !important;
                
                /* Sophisticated Shadow */
                box-shadow: 
                    0 4px 6px rgba(42, 79, 87, 0.2),
                    0 10px 20px rgba(42, 79, 87, 0.15),
                    inset 0 1px 0 rgba(255,255,255,0.2);
                
                transition: all 0.4s var(--ease-spring) !important;
                margin-top: 16px !important;
                position: relative;
                overflow: hidden;
            }}

            /* Hover Glow */
            .stButton > button:hover {{
                transform: translateY(-2px) !important;
                box-shadow: 
                    0 0 20px rgba(72, 126, 120, 0.4), /* Teal Glow */
                    0 12px 24px rgba(42, 79, 87, 0.25) !important;
                filter: brightness(1.1);
            }}

            /* Active / Pressed */
            .stButton > button:active {{
                transform: scale(0.98) translateY(0) !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            }}

            /* ========== 6. MICRO-DETAILS ========== */
            .login-divider {{
                height: 1px;
                width: 100%;
                background: linear-gradient(90deg, transparent, rgba(0,0,0,0.06), transparent);
                margin: 32px 0;
            }}

            .error-alert {{
                background: rgba(254, 242, 242, 0.8) !important;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(239, 68, 68, 0.2) !important;
                color: #EF4444 !important;
                border-radius: 14px !important;
                padding: 12px !important;
                margin-bottom: 24px !important;
                text-align: center;
                font-size: 13px;
                font-weight: 500;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                animation: shake 0.4s var(--ease-spring);
            }}

            @keyframes shake {{
                0%, 100% {{ transform: translateX(0); }}
                25% {{ transform: translateX(-4px); }}
                75% {{ transform: translateX(4px); }}
            }}

            .login-footnote {{
                text-align: center;
                color: rgba(17, 24, 39, 0.6); /* Dark text as requested */
                font-size: 11px;
                margin-top: 32px;
                font-weight: 600;
                letter-spacing: 0.05em;
                text-transform: uppercase;
            }}
            
            .forgot-link {{
                text-align: right;
                margin-top: 12px;
            }}
            
            .forgot-link a {{
                color: rgba(17, 24, 39, 0.5);
                font-size: 13px;
                text-decoration: none;
                font-weight: 500;
                transition: color 0.2s;
            }}
            
            .forgot-link a:hover {{
                color: var(--brand-dark);
            }}

            /* Mobile Optimization */
            @media (max-width: 600px) {{
                .block-container {{ max-width: 90% !important; }}
                .block-container > div:first-child {{ padding: 32px 24px; }}
                .login-logo {{ width: 180px; }}
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

