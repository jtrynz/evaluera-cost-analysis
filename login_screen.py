import streamlit as st

VALID_CREDENTIALS = {
    "admin": "evaluera2024",
    "demo": "demo123",
    "user": "password"
}


def check_login():
    """Return True if user is logged in."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    return st.session_state.logged_in


def login(username, password):
    """Validate login credentials."""
    if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False


def logout():
    """Logout user."""
    st.session_state.logged_in = False
    if "username" in st.session_state:
        del st.session_state.username
    st.rerun()


def render_login_screen():
    """
    Render simple login screen without custom HTML/CSS
    """

    st.title("EVALUERA")
    st.caption("KI-gestützte Kostenanalyse")

    if "login_error" in st.session_state and st.session_state.login_error:
        st.error("Ungültige Zugangsdaten")

    username = st.text_input(
        "Benutzername",
        placeholder="Benutzername eingeben",
        key="login_username",
    )

    password = st.text_input(
        "Passwort",
        type="password",
        placeholder="Passwort eingeben",
        key="login_password",
    )

    if st.button("Anmelden", key="login_btn"):
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

def render_logout_button():
    with st.sidebar:
        st.write("Eingeloggt als:", st.session_state.get("username", "Benutzer"))
        if st.button("Abmelden"):
            logout()