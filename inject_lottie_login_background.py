import os
import base64
import streamlit as st


def inject_lottie_background():
    if st.session_state.get("logged_in"):
        return

    lottie_file = os.path.join(os.path.dirname(__file__), "dark_gradient.json")

    with open(lottie_file, "rb") as f:
        data = f.read()

    src = "data:application/json;base64," + base64.b64encode(data).decode()

    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html, body {{
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: fixed;
    inset: 0;
}}

#bg-container {{
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    z-index: 1;
}}

#lottie {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    margin: 0;
    padding: 0;
}}
</style>
</head>
<body>
<div id="bg-container">
    <lottie-player
        id="lottie"
        autoplay
        loop
        mode="normal"
        background="transparent"
        src="{src}">
    </lottie-player>
</div>
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
</body>
</html>
"""

    st.components.v1.html(html, height=1, scrolling=False)

    st.markdown("""
<style>
    /* ========== IFRAME FULLSCREEN FIXED ========== */
    iframe[title="st.components.v1.html"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        z-index: -1 !important;
        pointer-events: none !important;
        border: none !important;
    }

    /* ========== GLOBAL SCROLL PREVENTION ========== */
    html, body {
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        height: 100% !important;
    }

    /* ========== FIX: block-container Scrollraum entfernen ========== */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin: 0 !important;
        position: relative !important;
        z-index: 5 !important;
    }

    /* ========== FIX: Parent-Container des iframes aus Flow entfernen ========== */
    [data-testid="stApp"] .st-emotion-cache-*,
    [data-testid="stAppViewContainer"] .st-emotion-cache-* {
        height: 0 !important;
        min-height: 0 !important;
        overflow: hidden !important;
    }

    /* ========== STREAMLIT CONTAINERS TRANSPARENT ========== */
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background: transparent !important;
        background-color: transparent !important;
        position: static !important;
        height: auto !important;
        overflow: visible !important;
    }

    /* ========== TRANSPARENT CONTAINERS ========== */
    .stApp,
    section.main,
    div.main,
    [data-testid="stHeader"],
    [data-testid="stDecoration"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* ========== HIDE STREAMLIT UI ELEMENTS ========== */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}

    /* ========== LOGIN BOX Z-INDEX ========== */
    .login-container {
        position: relative !important;
        z-index: 10 !important;
    }
</style>
""", unsafe_allow_html=True)
