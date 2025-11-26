"""
🎨 EVALUERA - UI Components
===========================
Apple-like UI-Komponenten und Ladeanimationen für ultra-professionelles Design
"""

import streamlit as st
import time
import os

def get_icon_path(icon_name):
    """
    Returns the absolute path to a custom icon.
    Args:
        icon_name: Name of the icon (e.g., 'rocket', 'eye')
    Returns:
        Absolute path to the icon file or None if not found.
    """
    icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icons', f'{icon_name}.png')
    if os.path.exists(icon_path):
        return icon_path
    return None

def load_image_as_base64(image_path):
    """Loads an image and returns a base64 string for HTML embedding"""
    import base64
    if not image_path or not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def render_evaluera_logo(align="center", width=230):
    """
    Renders the EVALUERA logo with responsive sizing and proper alignment.

    Args:
        align: "center" (default), "left", or "right"
        width: Logo width in pixels (default: 230)

    Returns:
        None (renders directly to Streamlit)
    """
    # Get logo path
    logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'EVALUERA.png')

    # Responsive CSS for logo
    st.markdown(f"""
    <style>
        .evaluera-logo-container {{
            display: flex;
            justify-content: {align};
            align-items: center;
            margin-bottom: -10px;
            margin-top: 0;
            padding: 0;
        }}

        .evaluera-logo-container img {{
            width: {width}px !important;
            max-width: 100% !important;
            height: auto !important;
            image-rendering: -webkit-optimize-contrast !important;
            image-rendering: crisp-edges !important;
        }}

        /* Responsive breakpoints */
        @media (max-width: 900px) {{
            .evaluera-logo-container img {{
                width: 200px !important;
            }}
        }}

        @media (max-width: 600px) {{
            .evaluera-logo-container img {{
                width: 160px !important;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

    # Render logo
    if align == "center":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(logo_path, width=width)
    elif align == "left":
        st.image(logo_path, width=width)
    elif align == "right":
        col1, col2 = st.columns([3, 1])
        with col2:
            st.image(logo_path, width=width)


def show_apple_loader(text="Lädt...", duration=None):
    """
    Zeigt einen Apple-like Ladeindikator mit optionalem Text.

    Args:
        text: Text der während des Ladens angezeigt wird
        duration: Optional - Dauer in Sekunden (None = unbegrenzt)
    """
    html = f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 0;">
        <div class="apple-loader"></div>
        <p style="margin-top: 1.5rem; color: var(--apple-text-secondary); font-size: 1rem; font-weight: 500;">
            {text}
        </p>
    </div>
    """

    loader_container = st.empty()
    loader_container.markdown(html, unsafe_allow_html=True)

    if duration:
        time.sleep(duration)
        loader_container.empty()

    return loader_container


def show_shimmer_skeleton(height="100px", count=1):
    """
    Zeigt Skeleton-Loading mit Shimmer-Effekt (wie Apple verwendet).

    Args:
        height: Höhe des Skeleton-Elements
        count: Anzahl der Skeleton-Elemente
    """
    skeletons = ""
    for i in range(count):
        margin = "margin-bottom: 1rem;" if i < count - 1 else ""
        skeletons += f"""
        <div class="loading-shimmer" style="
            height: {height};
            border-radius: var(--apple-radius-sm);
            {margin}
        "></div>
        """

    st.markdown(f"""
    <div style="padding: 1rem 0;">
        {skeletons}
    </div>
    """, unsafe_allow_html=True)


def show_progress_animation(progress, text=""):
    """
    Zeigt eine animierte Apple-like Progress Bar.

    Args:
        progress: Fortschritt von 0.0 bis 1.0
        text: Optionaler Text unter der Progress Bar
    """
    percentage = int(progress * 100)

    html = f"""
    <div style="padding: 1rem 0;">
        <div style="
            background: var(--apple-surface-hover);
            border-radius: 100px;
            height: 6px;
            overflow: hidden;
            box-shadow: var(--apple-shadow-sm);
        ">
            <div style="
                background: linear-gradient(90deg, var(--apple-accent), #0077ed);
                width: {percentage}%;
                height: 100%;
                border-radius: 100px;
                transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            "></div>
        </div>
        <p style="
            margin-top: 0.75rem;
            color: var(--apple-text-secondary);
            font-size: 0.9rem;
            text-align: center;
            font-weight: 500;
        ">{text} {percentage}%</p>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


def show_glass_card(content, title=None):
    """
    Zeigt einen Glassmorphism-Card (wie iOS/macOS).

    Args:
        content: Inhalt der Card
        title: Optionaler Titel
    """
    title_html = f"<h3 style='margin-top: 0; margin-bottom: 1rem;'>{title}</h3>" if title else ""

    st.markdown(f"""
    <div class="glass-card fade-in">
        {title_html}
        {content}
    </div>
    """, unsafe_allow_html=True)


def show_status_badge(text, status="success"):
    """
    Zeigt ein Status-Badge (wie Apple's Pills).

    Args:
        text: Badge-Text
        status: 'success', 'warning', oder 'error'
    """
    return f'<span class="status-badge status-{status}">{text}</span>'


def show_metric_card(label, value, delta=None, help_text=None):
    """
    Zeigt eine verbesserte Metrik-Karte im Apple-Stil.

    Args:
        label: Label der Metrik
        value: Wert
        delta: Optionale Änderung (z.B. "+5%")
        help_text: Optionaler Hilfetext
    """
    delta_html = ""
    if delta:
        delta_color = "#34c759" if "+" in str(delta) else "#2F4A56" if "-" in str(delta) else "#86868b"
        delta_html = f"""
        <div style="
            color: {delta_color};
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 0.5rem;
        ">{delta}</div>
        """

    help_html = ""
    if help_text:
        help_html = f"""
        <div style="
            color: var(--apple-text-secondary);
            font-size: 0.85rem;
            margin-top: 0.5rem;
            line-height: 1.4;
        ">{help_text}</div>
        """

    st.markdown(f"""
    <div class="hover-lift" style="
        background: var(--apple-surface);
        border-radius: var(--apple-radius);
        padding: 1.5rem;
        box-shadow: var(--apple-shadow-sm);
        border: 1px solid var(--apple-border);
    ">
        <div style="
            font-size: 0.85rem;
            color: var(--apple-text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.75rem;
        ">{label}</div>
        <div style="
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--apple-text);
            letter-spacing: -0.03em;
        ">{value}</div>
        {delta_html}
        {help_html}
    </div>
    """, unsafe_allow_html=True)


def show_info_card(icon, title, description, color="#0071e3"):
    """
    Zeigt eine Info-Card mit Icon im Apple-Stil.

    Args:
        icon: Emoji oder Icon
        title: Titel
        description: Beschreibung
        color: Akzentfarbe (Hex)
    """
    # Icon handling
    icon_html = f'<div style="font-size: 2rem; line-height: 1;">{icon}</div>'
    if icon and (icon.endswith('.png') or icon.endswith('.jpg')) and os.path.exists(icon):
        b64_img = load_image_as_base64(icon)
        if b64_img:
            icon_html = f'<img src="data:image/png;base64,{b64_img}" style="width: 40px; height: 40px; object-fit: contain;">'

    st.markdown(f"""
    <div class="fade-in" style="
        background: var(--apple-surface);
        border-radius: var(--apple-radius);
        padding: 1.5rem;
        box-shadow: var(--apple-shadow-sm);
        border: 1px solid var(--apple-border);
        border-left: 4px solid {color};
        margin: 1rem 0;
    ">
        <div style="display: flex; align-items: start; gap: 1rem;">
            {icon_html}
            <div style="flex: 1;">
                <h4 style="
                    margin: 0 0 0.5rem 0;
                    color: var(--apple-text);
                    font-weight: 600;
                    font-size: 1.1rem;
                ">{title}</h4>
                <p style="
                    margin: 0;
                    color: var(--apple-text-secondary);
                    font-size: 0.95rem;
                    line-height: 1.5;
                ">{description}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show_loading_with_steps(steps, current_step):
    """
    Zeigt einen mehrstufigen Ladeindikator.

    Args:
        steps: Liste von Step-Namen
        current_step: Index des aktuellen Steps (0-basiert)
    """
    total_steps = len(steps)
    progress = (current_step + 1) / total_steps

    steps_html = ""
    for i, step in enumerate(steps):
        if i < current_step:
            # Abgeschlossen
            color = "#34c759"
            icon = "✓"
            opacity = "1"
        elif i == current_step:
            # Aktuell
            color = "#0071e3"
            icon = "●"
            opacity = "1"
        else:
            # Ausstehend
            color = "#d1d1d6"
            icon = "○"
            opacity = "0.5"

        steps_html += f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
            opacity: {opacity};
            transition: all 0.3s ease;
        ">
            <div style="
                color: {color};
                font-size: 1.5rem;
                line-height: 1;
                min-width: 24px;
            ">{icon}</div>
            <div style="
                color: var(--apple-text);
                font-weight: 500;
                font-size: 0.95rem;
            ">{step}</div>
        </div>
        """

    st.markdown(f"""
    <div style="
        background: var(--apple-surface);
        border-radius: var(--apple-radius);
        padding: 2rem;
        box-shadow: var(--apple-shadow-md);
        border: 1px solid var(--apple-border);
    ">
        <div style="margin-bottom: 1.5rem;">
            <div style="
                background: var(--apple-surface-hover);
                border-radius: 100px;
                height: 6px;
                overflow: hidden;
            ">
                <div style="
                    background: linear-gradient(90deg, #0071e3, #0077ed);
                    width: {int(progress * 100)}%;
                    height: 100%;
                    border-radius: 100px;
                    transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                "></div>
            </div>
        </div>
        {steps_html}
    </div>
    """, unsafe_allow_html=True)


def show_pulse_loader(text="Verarbeite..."):
    """
    Zeigt einen pulsierenden Ladeindikator.

    Args:
        text: Text während des Ladens
    """
    st.markdown(f"""
    <div class="loading-pulse" style="
        text-align: center;
        padding: 2rem 0;
    ">
        <div style="
            display: inline-block;
            width: 12px;
            height: 12px;
            background: var(--apple-accent);
            border-radius: 50%;
            margin: 0 0.5rem;
            animation: pulse 1.4s infinite ease-in-out;
        "></div>
        <div style="
            display: inline-block;
            width: 12px;
            height: 12px;
            background: var(--apple-accent);
            border-radius: 50%;
            margin: 0 0.5rem;
            animation: pulse 1.4s infinite ease-in-out 0.2s;
        "></div>
        <div style="
            display: inline-block;
            width: 12px;
            height: 12px;
            background: var(--apple-accent);
            border-radius: 50%;
            margin: 0 0.5rem;
            animation: pulse 1.4s infinite ease-in-out 0.4s;
        "></div>
        <p style="
            margin-top: 1rem;
            color: var(--apple-text-secondary);
            font-size: 0.95rem;
            font-weight: 500;
        ">{text}</p>
    </div>
    """, unsafe_allow_html=True)


def create_two_column_layout():
    """
    Erstellt ein schönes 2-Spalten-Layout im Apple-Stil.

    Returns:
        Tuple von (col1, col2)
    """
    col1, col2 = st.columns(2, gap="large")
    return col1, col2


def create_three_column_layout():
    """
    Erstellt ein schönes 3-Spalten-Layout im Apple-Stil.

    Returns:
        Tuple von (col1, col2, col3)
    """
    col1, col2, col3 = st.columns(3, gap="large")
    return col1, col2, col3


def show_divider(text=None):
    """
    Zeigt einen stilvollen Divider, optional mit Text.

    Args:
        text: Optionaler Text in der Mitte des Dividers
    """
    if text:
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            margin: 3rem 0;
            gap: 1.5rem;
        ">
            <div style="
                flex: 1;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--apple-border), transparent);
            "></div>
            <div style="
                color: var(--apple-text-secondary);
                font-weight: 600;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            ">{text}</div>
            <div style="
                flex: 1;
                height: 1px;
                background: linear-gradient(90deg, transparent, var(--apple-border), transparent);
            "></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <hr style="
            margin: 3rem 0;
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--apple-border), transparent);
        ">
        """, unsafe_allow_html=True)


def show_empty_state(icon, title, description, button_text=None, button_action=None):
    """
    Zeigt einen Empty State im Apple-Stil.

    Args:
        icon: Emoji oder Icon
        title: Titel
        description: Beschreibung
        button_text: Optionaler Button-Text
        button_action: Optionale Button-Aktion (Key für st.button)
    """
    button_html = ""
    if button_text and button_action:
        button_html = f"""
        <div style="margin-top: 1.5rem;">
            <a href="#" style="
                display: inline-block;
                background: var(--apple-accent);
                color: white;
                padding: 0.75rem 2rem;
                border-radius: var(--apple-radius-sm);
                text-decoration: none;
                font-weight: 600;
                transition: all 0.2s ease;
            ">{button_text}</a>
        </div>
        """

    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        background: var(--apple-surface);
        border-radius: var(--apple-radius);
        border: 1px solid var(--apple-border);
    ">
        <div style="
            font-size: 4rem;
            line-height: 1;
            margin-bottom: 1.5rem;
            opacity: 0.5;
        ">{icon}</div>
        <h3 style="
            color: var(--apple-text);
            font-weight: 600;
            margin-bottom: 0.75rem;
        ">{title}</h3>
        <p style="
            color: var(--apple-text-secondary);
            font-size: 1rem;
            max-width: 400px;
            margin: 0 auto;
            line-height: 1.5;
        ">{description}</p>
        {button_html}
    </div>
    """, unsafe_allow_html=True)


class GPTLoadingAnimation:
    """
    Context-Manager für EVALUERA-gebrandete KI-Ladeanimationen.

    Verwendung:
        with GPTLoadingAnimation("Analysiere Material..."):
            result = gpt_function()
    """

    def __init__(self, message="KI analysiert...", icon="🤖"):
        self.message = message
        self.icon = icon
        self.container = None

    def __enter__(self):
        """Startet die Ladeanimation"""
        self.container = st.empty()
        
        # Icon handling (Emoji vs Image)
        icon_html = f'<div style="font-size: 2.2rem; animation: pulse 2s ease-in-out infinite;">{self.icon}</div>'
        if self.icon and (self.icon.endswith('.png') or self.icon.endswith('.jpg')) and os.path.exists(self.icon):
            b64_img = load_image_as_base64(self.icon)
            if b64_img:
                icon_html = f'<img src="data:image/png;base64,{b64_img}" style="width: 50px; height: 50px; object-fit: contain; animation: pulse 2s ease-in-out infinite;">'

        # EVALUERA-gebrandete Ladeanimation mit Mint/Türkis Gradient
        self.container.markdown(f"""<div style="background: linear-gradient(135deg, #7BA5A0 0%, #5A8680 50%, #B8D4D1 100%); border-radius: 20px; padding: 2.5rem; margin: 2rem 0; box-shadow: 0 20px 60px rgba(123, 165, 160, 0.3), 0 8px 16px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(20px); position: relative; overflow: hidden;"><div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at 30% 50%, rgba(184, 212, 209, 0.4) 0%, transparent 50%); animation: moveGradient 3s ease-in-out infinite;"></div><div style="position: relative; z-index: 1;"><div style="display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1.5rem;"><div style="position: relative;"><div style="width: 60px; height: 60px; background: rgba(255, 255, 255, 0.15); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);">{icon_html}</div><div style="position: absolute; top: -5px; left: -5px; width: 70px; height: 70px; border: 3px solid rgba(255, 255, 255, 0.3); border-top-color: white; border-radius: 50%; animation: spin 1.5s linear infinite;"></div></div><div style="flex: 1;"><div style="color: white; font-weight: 700; font-size: 1.3rem; margin-bottom: 0.5rem; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); letter-spacing: 0.02em;">{self.message}</div><div style="color: rgba(255, 255, 255, 0.9); font-size: 0.95rem; font-weight: 500;">EVALUERA KI-Engine arbeitet...</div></div></div><div style="background: rgba(255, 255, 255, 0.15); border-radius: 100px; height: 6px; overflow: hidden; position: relative; box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2);"><div style="position: absolute; top: 0; left: 0; height: 100%; width: 50%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent); animation: shimmer 1.8s ease-in-out infinite;"></div></div><div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center;"><div style="width: 8px; height: 8px; background: white; border-radius: 50%; animation: bounce 1.4s ease-in-out infinite;"></div><div style="width: 8px; height: 8px; background: white; border-radius: 50%; animation: bounce 1.4s ease-in-out 0.2s infinite;"></div><div style="width: 8px; height: 8px; background: white; border-radius: 50%; animation: bounce 1.4s ease-in-out 0.4s infinite;"></div></div></div></div><style>@keyframes spin {{from {{transform: rotate(0deg);}} to {{transform: rotate(360deg);}}}} @keyframes shimmer {{0% {{transform: translateX(-100%);}} 100% {{transform: translateX(300%);}}}} @keyframes pulse {{0%, 100% {{transform: scale(1);}} 50% {{transform: scale(1.1);}}}} @keyframes bounce {{0%, 100% {{transform: translateY(0);}} 50% {{transform: translateY(-8px);}}}} @keyframes moveGradient {{0%, 100% {{transform: translateX(0) translateY(0);}} 50% {{transform: translateX(20px) translateY(-20px);}}}}</style>""", unsafe_allow_html=True)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Beendet die Ladeanimation"""
        if self.container:
            self.container.empty()
        return False


class ExcelLoadingAnimation:
    """
    Context-Manager für EVALUERA Excel-Upload Ladeanimationen.

    Verwendung:
        with ExcelLoadingAnimation("Lade Excel-Datei..."):
            df = pd.read_excel(file)
    """

    def __init__(self, message="Lade Daten...", icon="📊"):
        self.message = message
        self.icon = icon
        self.container = None

    def __enter__(self):
        """Startet die Ladeanimation"""
        self.container = st.empty()

        # Icon handling (Emoji vs Image)
        icon_html = f'<div style="font-size: 2rem; animation: float 2s ease-in-out infinite;">{self.icon}</div>'
        if self.icon and (self.icon.endswith('.png') or self.icon.endswith('.jpg')) and os.path.exists(self.icon):
            b64_img = load_image_as_base64(self.icon)
            if b64_img:
                icon_html = f'<img src="data:image/png;base64,{b64_img}" style="width: 40px; height: 40px; object-fit: contain; animation: float 2s ease-in-out infinite;">'

        # EVALUERA Excel-Upload Animation
        self.container.markdown(f"""<div style="background: linear-gradient(135deg, #B8D4D1 0%, #7BA5A0 100%); border-radius: 16px; padding: 2rem; margin: 1.5rem 0; box-shadow: 0 12px 40px rgba(123, 165, 160, 0.25); border: 1px solid rgba(255, 255, 255, 0.3); position: relative; overflow: hidden;"><div style="position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%); animation: rotate 8s linear infinite;"></div><div style="position: relative; z-index: 1; display: flex; align-items: center; gap: 1.5rem;"><div style="position: relative;"><div style="width: 50px; height: 50px; background: rgba(255, 255, 255, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">{icon_html}</div></div><div style="flex: 1;"><div style="color: #1a1a1a; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem; letter-spacing: 0.02em;">{self.message}</div><div style="display: flex; gap: 0.4rem; align-items: center;"><div style="width: 6px; height: 6px; background: #1a1a1a; border-radius: 50%; animation: loadingDot 1.4s ease-in-out infinite;"></div><div style="width: 6px; height: 6px; background: #1a1a1a; border-radius: 50%; animation: loadingDot 1.4s ease-in-out 0.2s infinite;"></div><div style="width: 6px; height: 6px; background: #1a1a1a; border-radius: 50%; animation: loadingDot 1.4s ease-in-out 0.4s infinite;"></div><span style="margin-left: 0.5rem; color: rgba(26, 26, 26, 0.7); font-size: 0.9rem; font-weight: 500;">Verarbeite Daten</span></div></div></div></div><style>@keyframes rotate {{from {{transform: rotate(0deg);}} to {{transform: rotate(360deg);}}}} @keyframes float {{0%, 100% {{transform: translateY(0);}} 50% {{transform: translateY(-8px);}}}} @keyframes loadingDot {{0%, 100% {{opacity: 0.3; transform: scale(0.8);}} 50% {{opacity: 1; transform: scale(1.2);}}}}</style>""", unsafe_allow_html=True)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Beendet die Ladeanimation"""
        if self.container:
            self.container.empty()
        return False


def show_gpt_success(message, icon="✅"):
    """
    Zeigt eine EVALUERA-gebrandete Erfolgsmeldung.

    Args:
        message: Erfolgsnachricht
        icon: Icon (Standard: ✅)
    """
    # Icon handling
    icon_html = f'<div style="font-size: 1.8rem; animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);">{icon}</div>'
    if icon and (icon.endswith('.png') or icon.endswith('.jpg')) and os.path.exists(icon):
        b64_img = load_image_as_base64(icon)
        if b64_img:
            icon_html = f'<img src="data:image/png;base64,{b64_img}" style="width: 32px; height: 32px; object-fit: contain; animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);">'

    st.markdown(f"""<div style="background: linear-gradient(135deg, #7BA5A0 0%, #5A8680 100%); border-radius: 12px; padding: 1.25rem 1.75rem; margin: 1rem 0; box-shadow: 0 8px 24px rgba(123, 165, 160, 0.3); border: 1px solid rgba(255, 255, 255, 0.2); display: flex; align-items: center; gap: 1rem; animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);">{icon_html}<div style="color: white; font-weight: 600; font-size: 1.05rem; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);">{message}</div></div><style>@keyframes slideIn {{from {{opacity: 0; transform: translateY(-10px);}} to {{opacity: 1; transform: translateY(0);}}}} @keyframes scaleIn {{from {{transform: scale(0);}} to {{transform: scale(1);}}}}</style>""", unsafe_allow_html=True)


def show_gpt_error(message, icon="❌"):
    """
    Zeigt eine EVALUERA-gebrandete Fehlermeldung.

    Args:
        message: Fehlernachricht
        icon: Icon (Standard: ❌)
    """
    # Icon handling
    icon_html = f'<div style="font-size: 1.8rem; animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);">{icon}</div>'
    if icon and (icon.endswith('.png') or icon.endswith('.jpg')) and os.path.exists(icon):
        b64_img = load_image_as_base64(icon)
        if b64_img:
            icon_html = f'<img src="data:image/png;base64,{b64_img}" style="width: 32px; height: 32px; object-fit: contain; animation: scaleIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);">'

    st.markdown(f"""<div style="background: linear-gradient(135deg, #FF6B6B 0%, #EE5253 100%); border-radius: 12px; padding: 1.25rem 1.75rem; margin: 1rem 0; box-shadow: 0 8px 24px rgba(238, 82, 83, 0.3); border: 1px solid rgba(255, 255, 255, 0.2); display: flex; align-items: center; gap: 1rem; animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);">{icon_html}<div style="color: white; font-weight: 600; font-size: 1.05rem; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);">{message}</div></div>""", unsafe_allow_html=True)
