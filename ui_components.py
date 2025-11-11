"""
🎨 EVALUERA - UI Components
===========================
Apple-like UI-Komponenten und Ladeanimationen für ultra-professionelles Design
"""

import streamlit as st
import time


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
        delta_color = "#34c759" if "+" in str(delta) else "#ff3b30" if "-" in str(delta) else "#86868b"
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
            <div style="
                font-size: 2rem;
                line-height: 1;
            ">{icon}</div>
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
