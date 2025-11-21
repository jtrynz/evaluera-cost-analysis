"""
🔐 EVALUERA - Login Screen
===========================
Premium Glassmorphism Login mit EVALUERA Branding
"""

import streamlit as st
from liquid_glass_system import render_liquid_background, apply_liquid_glass_styles
from ui_theme import COLORS


# Demo-Credentials (in Produktion: externe Auth-Systeme nutzen)
VALID_CREDENTIALS = {
    "admin": "evaluera2024",
    "demo": "demo123",
    "user": "password"
}


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
    """Logout user"""
    st.session_state.logged_in = False
    if "username" in st.session_state:
        del st.session_state.username
    st.rerun()


def render_login_screen():
    """Render premium glassmorphism login screen"""

    # Apply liquid glass styles
    apply_liquid_glass_styles()

    # Render animated background
    render_liquid_background()

    # Hide Streamlit elements
    st.markdown("""
    <style>
        /* Hide Streamlit elements during login */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}

        /* Center login container */
        .login-container {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 2rem;
        }

        /* Login Card */
        .login-card {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(35px) saturate(180%);
            -webkit-backdrop-filter: blur(35px) saturate(180%);
            border-radius: 28px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            padding: 3rem 2.5rem;
            max-width: 440px;
            width: 100%;
            box-shadow:
                0 20px 60px 0 rgba(31, 38, 135, 0.2),
                inset 0 0 0 1px rgba(255, 255, 255, 0.4);
            animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* EVALUERA Logo */
        .login-logo {
            text-align: center;
            margin-bottom: 2rem;
        }

        .login-logo h1 {
            font-size: 2.5rem;
            font-weight: 300;
            letter-spacing: 0.15em;
            color: #1a1a1a;
            margin: 0 0 0.5rem 0;
        }

        .login-logo p {
            font-size: 0.95rem;
            color: rgba(26, 26, 26, 0.6);
            margin: 0;
            font-weight: 500;
        }

        /* Input Styling */
        .login-card input {
            width: 100%;
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(123, 165, 160, 0.3);
            border-radius: 14px;
            padding: 1rem 1.25rem;
            font-size: 1rem;
            color: #1a1a1a;
            transition: all 0.3s ease;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .login-card input:focus {
            outline: none;
            background: rgba(255, 255, 255, 0.8);
            border-color: #7BA5A0;
            box-shadow: 0 0 0 4px rgba(123, 165, 160, 0.12);
        }

        /* Button Styling */
        .login-card button[kind="primary"] {
            width: 100%;
            background: linear-gradient(135deg, #2F4A56 0%, #3D5A68 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 1rem;
            font-size: 1.05rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 6px 20px rgba(47, 74, 86, 0.3);
            margin-top: 1rem;
        }

        .login-card button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(47, 74, 86, 0.4);
        }

        /* Divider */
        .login-divider {
            height: 1px;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(123, 165, 160, 0.3),
                transparent
            );
            margin: 1.5rem 0;
        }

        /* Helper Text */
        .login-helper {
            text-align: center;
            font-size: 0.85rem;
            color: rgba(26, 26, 26, 0.5);
            margin-top: 1.5rem;
            line-height: 1.5;
        }

        /* Error Message */
        .login-error {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            margin-bottom: 1rem;
            color: #ef4444;
            font-size: 0.9rem;
            text-align: center;
            animation: shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97);
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }

        /* Password Toggle */
        .password-toggle {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-top: 0.75rem;
            font-size: 0.9rem;
            color: rgba(26, 26, 26, 0.6);
        }
    </style>
    """, unsafe_allow_html=True)

    # Main container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Login Card
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

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
            <div class="login-error">
                ❌ Ungültige Zugangsdaten. Bitte erneut versuchen.
            </div>
            """, unsafe_allow_html=True)

        # Input fields
        username = st.text_input(
            "Benutzername",
            placeholder="Benutzername eingeben",
            key="login_username",
            label_visibility="collapsed"
        )

        st.markdown('<div style="height: 0.75rem;"></div>', unsafe_allow_html=True)

        # Password toggle
        if "show_password" not in st.session_state:
            st.session_state.show_password = False

        password = st.text_input(
            "Passwort",
            type="text" if st.session_state.show_password else "password",
            placeholder="Passwort eingeben",
            key="login_password",
            label_visibility="collapsed"
        )

        # Show password toggle
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.checkbox("👁️", key="show_pwd_toggle"):
                st.session_state.show_password = True
            else:
                st.session_state.show_password = False
        with col2:
            st.markdown(
                '<div style="padding-top: 0.5rem; font-size: 0.9rem; color: rgba(26, 26, 26, 0.6);">Passwort anzeigen</div>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="login-divider"></div>', unsafe_allow_html=True)

        # Login button
        if st.button("🔐 Anmelden", type="primary", use_container_width=True):
            if username and password:
                if login(username, password):
                    st.session_state.login_error = False
                    st.success("✅ Erfolgreich eingeloggt!")
                    st.rerun()
                else:
                    st.session_state.login_error = True
                    st.rerun()
            else:
                st.session_state.login_error = True
                st.rerun()

        # Helper text
        st.markdown("""
        <div class="login-helper">
            <strong>Demo-Zugangsdaten:</strong><br>
            Benutzer: <code>demo</code> | Passwort: <code>demo123</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

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
