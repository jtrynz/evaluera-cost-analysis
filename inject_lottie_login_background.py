import streamlit as st
import base64
import os
import streamlit.components.v1 as components

def inject_lottie_login_background():
    lottie_path = os.path.join(os.path.dirname(__file__), "dark_gradient.json")

    with open(lottie_path, "rb") as f:
        animation_bytes = f.read()

    data_url = (
        "data:application/json;base64,"
        + base64.b64encode(animation_bytes).decode("utf-8")
    )

    lottie_html = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>

    <lottie-player
        src="{data_url}"
        background="transparent"
        speed="1"
        loop
        autoplay
        renderer="canvas"
        style="position: fixed; inset: 0; width: 100vw; height: 100vh; z-index:-9999;"
    ></lottie-player>
    """

    components.html(lottie_html, height=0, width=0)

    st.markdown(
        """
        <style>
        body { background: #BFDCDC !important; }
        .stApp { background: transparent !important; }
        iframe[title="st.components.v1.html"] {
            position: fixed !important;
            inset: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            z-index: -9999 !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )