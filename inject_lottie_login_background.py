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
        id="lottie-bg"
        src="{data_url}"
        background="transparent"
        speed="1"
        loop
        autoplay
        renderer="svg"
        style="
            position:fixed !important;
            top:0 !important;
            left:0 !important;
            width:100vw !important;
            height:100vh !important;
            object-fit:cover !important;
            margin:0 !important;
            padding:0 !important;
            z-index:-1 !important;
        "
    ></lottie-player>
    """

    components.html(lottie_html, height=0, width=0)

    st.markdown(
        """
        <style>
            html, body, .stApp {
                margin:0 !important;
                padding:0 !important;
                width:100vw !important;
                height:100vh !important;
                overflow:hidden !important;
                background:transparent !important;
            }

            iframe[title="st.components.v1.html"] {
                position: fixed !important;
                top:0 !important;
                left:0 !important;
                width:100vw !important;
                height:100vh !important;
                border:none !important;
                z-index:-1 !important;
                pointer-events:none !important;
                -webkit-transform: translateZ(0) !important;
                transform: translateZ(0) !important;
                will-change: transform !important;
            }

            #lottie-bg {
                -webkit-transform: translateZ(0) !important;
                transform: translateZ(0) !important;
                will-change: transform !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )