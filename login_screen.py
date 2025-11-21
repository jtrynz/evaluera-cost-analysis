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
