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
html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}}
#lottie {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    pointer-events: none;
}}
</style>
</head>
<body>
<lottie-player
    id="lottie"
    autoplay
    loop
    mode="normal"
    src="{src}">
</lottie-player>
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
</body>
</html>
"""

    st.components.v1.html(html, height=600, width=1000, scrolling=False)

    st.markdown("""
    <style>
        /* Lottie iframe fullscreen fix */
        iframe[title="st.components.v1.html"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: -1 !important;
            pointer-events: none !important;
            border: none !important;
            opacity: 1 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
<style>
html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"],
.block-container, .main, section.main, div.main,
[data-testid="stHeader"], [data-testid="stDecoration"] {
    background: transparent !important;
    background-color: transparent !important;
}

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
