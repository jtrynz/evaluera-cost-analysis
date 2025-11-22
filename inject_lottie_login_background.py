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
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    min-width: 100%;
    min-height: 100%;
    width: auto;
    height: auto;
    pointer-events: none;
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

    st.components.v1.html(html, height=0, width=0, scrolling=False)

    st.markdown("""
<style>
    /* ========== IFRAME FULLSCREEN POSITIONING ========== */
    iframe[title="st.components.v1.html"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        z-index: -999 !important;
        pointer-events: none !important;
        overflow: hidden !important;
        opacity: 1 !important;
        display: block !important;
    }

    /* ========== STREAMLIT CONTAINERS TRANSPARENT (NOT FULLSCREEN) ========== */
    [data-testid="stApp"],
    .stApp {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stAppViewContainer"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    .main,
    section.main,
    div.main {
        background: transparent !important;
        background-color: transparent !important;
    }

    [data-testid="stHeader"],
    [data-testid="stDecoration"] {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* ========== LOGIN UI WRAPPER WITH Z-INDEX ========== */
    .block-container {
        background: transparent !important;
        background-color: transparent !important;
        position: relative !important;
        z-index: 1 !important;
    }

    /* ========== HIDE STREAMLIT UI ELEMENTS ========== */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}

    .stApp > div:first-child {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)
