"""
Futuristischer, animierter Login-Screen für EVALUERA (Streamlit Cloud).
"""

import os
import base64
import streamlit as st
from src.ui.theme import COLORS, RADIUS, SHADOWS

# ==================== CREDENTIALS ====================
VALID_CREDENTIALS = {
    "admin": "evaluera2024",
    "demo": "demo123",
    "user": "password",
}


# ==================== AUTHENTICATION HELPERS ====================
def check_login() -> bool:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in


def login(username: str, password: str) -> bool:
    if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False


def logout():
    st.session_state.logged_in = False
    if "username" in st.session_state:
        del st.session_state.username
    st.rerun()


def get_logo_base64():
    logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "EVALUERA.png")
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


# ==================== FUTURISTIC LOGIN SCREEN ====================
def render_login_screen():
    """Render futuristisch-animierten Login mit Glassmorphism."""
    if "login_error" not in st.session_state:
        st.session_state.login_error = False

    logo_base64 = get_logo_base64()

    st.markdown(
        f"""
        <style>
            :root {{
                --bg1: #a8f1ec;
                --bg2: #68d7ff;
                --bg3: #5da59f;
                --text-strong: #0f1f2a;
                --text-soft: rgba(15, 31, 42, 0.78);
                --accent: #36d1dc;
                --accent-2: #7b61ff;
            }}

            html, body, .stApp, [data-testid="stAppViewContainer"] {{
                background: linear-gradient(125deg, var(--bg1), var(--bg2), var(--bg3)) !important;
                background-size: 240% 240% !important;
                animation: bgShift 18s ease-in-out infinite;
                min-height: 100vh;
                overflow: hidden;
            }}

            @keyframes bgShift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}

            .orb {{
                position: absolute;
                border-radius: 999px;
                filter: blur(60px);
                opacity: 0.55;
                mix-blend-mode: screen;
                animation: float 22s ease-in-out infinite alternate;
            }}
            .orb.one {{ width: 360px; height: 360px; background: #8df3ff; top: 10%; left: 12%; }}
            .orb.two {{ width: 420px; height: 420px; background: #7bd6ff; top: 60%; right: 8%; animation-delay: 4s; }}
            .orb.three {{ width: 300px; height: 300px; background: #5be3c6; bottom: 4%; left: 35%; animation-delay: 2s; }}
            @keyframes float {{
                0% {{ transform: translate3d(0,0,0); opacity: .45; }}
                100% {{ transform: translate3d(0px,-18px,0); opacity: .7; }}
            }}

            .login-stage {{
                position: relative;
                min-height: 100vh;
                display: grid;
                place-items: center;
                padding: 24px;
                isolation: isolate;
            }}

            .login-card {{
                width: min(480px, 92vw);
                padding: 28px 26px 24px 26px;
                border-radius: 18px;
                background: rgba(255,255,255,0.16);
                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
                border: 1px solid rgba(255,255,255,0.28);
                box-shadow:
                    0 18px 40px rgba(0,0,0,0.20),
                    0 0 0 1px rgba(255,255,255,0.12) inset;
                position: relative;
                overflow: hidden;
                color: var(--text-strong);
            }}

            .login-card::before {{
                content: "";
                position: absolute;
                inset: -30% -10%;
                background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.28), transparent 42%),
                            radial-gradient(circle at 80% 30%, rgba(255,255,255,0.22), transparent 40%);
                opacity: 0.7;
                pointer-events: none;
            }}

            .brand-row {{
                display: flex;
                align-items: center;
                gap: 14px;
                margin-bottom: 14px;
            }}
            .brand-row img {{ height: 50px; width: auto; }}
            .brand-title {{
                font-size: 15px;
                letter-spacing: 0.18em;
                font-weight: 700;
                text-transform: uppercase;
                color: var(--text-soft);
            }}
            .hero-title {{ margin: 6px 0 4px 0; font-size: 26px; font-weight: 800; letter-spacing: -0.02em; }}
            .hero-sub {{ margin: 0 0 12px 0; color: var(--text-soft); font-weight: 500; font-size: 14px; }}

            .stTextInput > label {{
                color: var(--text-strong) !important;
                font-weight: 600 !important;
                margin-bottom: 6px !important;
                letter-spacing: 0.01em !important;
            }}
            .stTextInput > div > div {{
                background: rgba(255,255,255,0.35) !important;
                border: 1.8px solid rgba(255,255,255,0.45) !important;
                border-radius: 12px !important;
                transition: all 0.22s ease !important;
                box-shadow: 0 8px 28px rgba(0,0,0,0.06) inset !important;
            }}
            .stTextInput > div > div:hover {{ border-color: rgba(255,255,255,0.65) !important; }}
            .stTextInput > div > div:focus-within {{
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 2px rgba(54,209,220,0.35), 0 12px 26px rgba(0,0,0,0.12) !important;
                background: rgba(255,255,255,0.48) !important;
            }}
            .stTextInput input {{
                color: var(--text-strong) !important;
                font-weight: 600 !important;
                background: transparent !important;
                padding: 12px 14px !important;
            }}
            .stTextInput input::placeholder {{ color: rgba(15,31,42,0.55) !important; }}

            .stButton > button {{
                width: 100% !important;
                border-radius: 12px !important;
                padding: 12px 16px !important;
                font-size: 15px !important;
                font-weight: 700 !important;
                background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
                color: #ffffff !important;
                border: 0 !important;
                box-shadow: 0 14px 26px rgba(0,0,0,0.16) !important;
                transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
            }}
            .stButton > button:hover {{
                transform: translateY(-1px) scale(1.01);
                box-shadow: 0 16px 32px rgba(0,0,0,0.20) !important;
                filter: brightness(1.02);
            }}
            .stButton > button:active {{ transform: translateY(0px) scale(0.995); }}

            .forgot {{ text-align: right; margin-top: 6px; }}
            .forgot a {{
                color: var(--text-soft);
                font-weight: 600;
                text-decoration: none;
                transition: color 0.2s ease;
            }}
            .forgot a:hover {{ color: var(--accent); }}

            .error-box {{
                background: rgba(255, 82, 82, 0.10);
                border: 1px solid rgba(255, 82, 82, 0.35);
                color: #8b0000;
                padding: 10px 12px;
                border-radius: 10px;
                font-weight: 600;
                margin-bottom: 10px;
            }}

            .pw-toggle-btn {{
                position: absolute;
                right: 12px;
                top: 50%;
                transform: translateY(-50%);
                background: rgba(255,255,255,0.45);
                border: 1px solid rgba(255,255,255,0.55);
                color: var(--text-strong);
                border-radius: 999px;
                padding: 4px 9px;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
            }}
            .pw-toggle-btn:hover {{
                background: rgba(255,255,255,0.75);
                border-color: var(--accent);
                color: var(--accent-2);
            }}

            header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stSidebar"], [data-testid="stToolbar"] {{
                display: none !important;
            }}

            @media (max-width: 600px) {{
                .login-card {{ padding: 22px 18px; }}
                .hero-title {{ font-size: 22px; }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="login-stage">
            <div class="orb one"></div>
            <div class="orb two"></div>
            <div class="orb three"></div>
            <div class="login-card">
                <div class="brand-row">
                    {"<img src='data:image/png;base64," + logo_base64 + "' alt='EVALUERA' />" if logo_base64 else ""}
                    <div class="brand-title">Future Access</div>
                </div>
                <div class="hero-title">Willkommen zurück</div>
                <div class="hero-sub">Sichere Anmeldung zur KI-gestützten Kostenanalyse</div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        username = st.text_input("Benutzername", key="login_username", placeholder="your.name")
        password = st.text_input("Passwort", key="login_password", type="password", placeholder="••••••••")
        st.markdown('<div class="forgot"><a href="#" tabindex="-1">Passwort vergessen?</a></div>', unsafe_allow_html=True)
        submit = st.form_submit_button("Sicher anmelden")

    if submit:
        if login(username.strip(), password):
            st.success("✅ Login erfolgreich. Weiterleitung...")
            st.experimental_rerun()
        else:
            st.session_state.login_error = True

    if st.session_state.login_error:
        st.markdown('<div class="error-box">Benutzername oder Passwort falsch.</div>', unsafe_allow_html=True)

    st.markdown(
        """
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <script>
            (function() {
                const pwd = window.document.querySelector('input[type="password"]');
                if (pwd && !document.querySelector('.pw-toggle-btn')) {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'pw-toggle-btn';
                    btn.innerText = 'show';
                    btn.onclick = () => {
                        const isPw = pwd.getAttribute('type') === 'password';
                        pwd.setAttribute('type', isPw ? 'text' : 'password');
                        btn.innerText = isPw ? 'hide' : 'show';
                    };
                    const wrapper = pwd.parentElement;
                    if (wrapper) {
                        wrapper.style.position = 'relative';
                        wrapper.appendChild(btn);
                    }
                }
            })();
        </script>
        """,
        unsafe_allow_html=True,
    )


# ==================== LOGOUT BUTTON ====================
def render_logout_button():
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            f"""
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
            """,
            unsafe_allow_html=True,
        )

        if st.button("🚪 Abmelden", use_container_width=True):
            logout()


def inject_lottie_background():
    """Deprecated placeholder for old Lottie background (no-op)."""
    return
