"""
🎨 EVALUERA - Navigation Demo
==============================
Demonstration der neuen Apple-ähnlichen Sidebar-Navigation
"""

import streamlit as st
from navigation_sidebar import NavigationSidebar, create_section_anchor, create_scroll_behavior
from ui_theme import apply_global_styles, COLORS, SPACING

# Setup
st.set_page_config(
    page_title="EVALUERA - Navigation Demo",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_global_styles()
create_scroll_behavior()

# Initialize Navigation
nav = NavigationSidebar()
nav.render()

# Main Content
st.markdown(f"""
<div style="
    background: {COLORS['brand_bg']};
    padding: {SPACING['xl']} {SPACING['xxl']};
    border-radius: 20px;
    margin-bottom: {SPACING['xl']};
">
    <h1 style="
        margin: 0;
        color: {COLORS['gray_900']};
        font-size: 3rem;
        font-weight: 300;
        letter-spacing: 0.1em;
    ">EVALUERA</h1>
    <p style="margin: {SPACING['md']} 0 0 0; color: {COLORS['gray_800']}; font-size: 1.1rem; max-width: 700px;">
        Neue Apple-ähnliche Navigation mit Accordion-Struktur
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== SECTION 1: PRODUKTDATEN ====================
if st.session_state.nav_active_section == "produktdaten":
    create_section_anchor("produktdaten", "📦 Produktdaten", "Übersicht der Produktinformationen")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Artikelinformationen")
        st.text_input("Artikelnummer", placeholder="z.B. DIN 933 M8")
        st.text_input("Bezeichnung", placeholder="z.B. Sechskantschraube")

    with col2:
        st.markdown("### Spezifikationen")
        st.number_input("Länge (mm)", min_value=0, value=50)
        st.number_input("Durchmesser (mm)", min_value=0, value=8)

    st.markdown("### Material")
    st.selectbox("Material auswählen", ["Stahl", "Edelstahl", "Aluminium", "Messing"])

# ==================== SECTION 2: CO₂-ANALYSE ====================
elif st.session_state.nav_active_section == "co2_analyse":
    create_section_anchor("co2_analyse", "🌍 CO₂-Analyse", "Umweltauswirkungen und Carbon Footprint")

    st.markdown("### CO₂-Fußabdruck")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Material-CO₂",
            value="2.4 kg",
            delta="-0.3 kg"
        )

    with col2:
        st.metric(
            label="Transport-CO₂",
            value="0.8 kg",
            delta="0.1 kg",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            label="Gesamt-CO₂",
            value="3.2 kg",
            delta="-0.2 kg"
        )

    st.markdown("### Emissionsverteilung")
    st.progress(0.75)
    st.caption("Material: 75% | Transport: 25%")

# ==================== SECTION 3: KOSTENÜBERSICHT ====================
elif st.session_state.nav_active_section == "kostenuebersicht":
    create_section_anchor("kostenuebersicht", "💰 Kostenübersicht", "Detaillierte Kostenaufstellung")

    st.markdown("### Kostenstruktur")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### Kostenaufschlüsselung")
        cost_data = {
            "Materialkosten": 45.50,
            "Fertigungskosten": 28.30,
            "Transportkosten": 12.20,
            "Verwaltung": 8.00
        }

        for label, value in cost_data.items():
            st.markdown(f"""
            <div style="
                display: flex;
                justify-content: space-between;
                padding: {SPACING['sm']} {SPACING['md']};
                margin: {SPACING['xs']} 0;
                background: {COLORS['gray_50']};
                border-radius: {SPACING['xs']};
            ">
                <span>{label}</span>
                <span style="font-weight: 600;">{value:.2f} €</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Gesamt")
        total = sum(cost_data.values())
        st.markdown(f"""
        <div style="
            background: {COLORS['primary_light']};
            padding: {SPACING['lg']};
            border-radius: {SPACING['md']};
            text-align: center;
        ">
            <div style="font-size: 0.875rem; color: {COLORS['gray_700']}; margin-bottom: {SPACING['xs']};">
                Gesamtkosten
            </div>
            <div style="font-size: 2rem; font-weight: 700; color: {COLORS['primary_dark']};">
                {total:.2f} €
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== SECTION 4: NACHHALTIGKEIT ====================
elif st.session_state.nav_active_section == "nachhaltigkeit":
    create_section_anchor("nachhaltigkeit", "♻️ Nachhaltigkeit", "CBAM und Nachhaltigkeitsindikatoren")

    st.markdown("### Nachhaltigkeitsbewertung")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Recyclingfähigkeit")
        st.progress(0.85)
        st.caption("85% recycelbar")

    with col2:
        st.markdown("#### Ressourceneffizienz")
        st.progress(0.72)
        st.caption("72% effizient")

    with col3:
        st.markdown("#### CBAM-Konformität")
        st.progress(0.95)
        st.caption("95% konform")

    st.markdown("### Empfehlungen")
    st.info("💡 **Tipp**: Durch Umstellung auf regionalen Lieferanten kann der CO₂-Fußabdruck um 30% reduziert werden.")

# ==================== SECTION 5: DEBUG ====================
elif st.session_state.nav_active_section == "debug":
    create_section_anchor("debug", "⚙️ Debug / Technische Details", "Entwicklerinformationen und Logs")

    with st.expander("🔍 Session State", expanded=False):
        st.json(dict(st.session_state))

    with st.expander("📊 Navigation State", expanded=True):
        st.write("Aktive Section:", st.session_state.nav_active_section)
        st.write("Erweiterte Sections:", list(st.session_state.nav_expanded_sections))

# ==================== SECTION 6: ERWEITERTE FUNKTIONEN ====================
elif st.session_state.nav_active_section == "erweitert":
    create_section_anchor("erweitert", "✨ Erweiterte Funktionen", "Zusätzliche Tools und Features")

    st.info("🎯 Wählen Sie eine Funktion aus der Sidebar aus")

# Technische Zeichnung
elif st.session_state.nav_active_section == "zeichnung":
    create_section_anchor("zeichnung", "📐 Technische Zeichnung", "2D-Zeichnungsgenerator")

    st.markdown("### Zeichnungsparameter")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox("Ansicht", ["Vorderansicht", "Seitenansicht", "Draufsicht", "Isometrisch"])
        st.selectbox("Maßstab", ["1:1", "1:2", "1:5", "1:10"])

    with col2:
        st.checkbox("Bemaßung anzeigen", value=True)
        st.checkbox("Toleranzen anzeigen", value=True)

    if st.button("🎨 Zeichnung generieren", type="primary", use_container_width=True):
        st.success("✅ Zeichnung wird generiert...")
        st.info("📄 Dies ist eine Demo-Funktion")

# 3D-Modell
elif st.session_state.nav_active_section == "modell3d":
    create_section_anchor("modell3d", "🎲 3D-Modell", "Interaktiver 3D-Viewer")

    st.markdown("### 3D-Viewer Optionen")

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox("Renderqualität", ["Niedrig", "Mittel", "Hoch", "Ultra"])
        st.checkbox("Beleuchtung", value=True)

    with col2:
        st.checkbox("Schatten", value=True)
        st.checkbox("Wireframe-Modus", value=False)

    if st.button("🎬 3D-Modell laden", type="primary", use_container_width=True):
        st.success("✅ 3D-Modell wird geladen...")
        st.info("🎲 Dies ist eine Demo-Funktion")

# ==================== FOOTER ====================
st.markdown(f"""
<div style="
    margin-top: {SPACING['xxl']};
    padding-top: {SPACING['lg']};
    border-top: 1px solid {COLORS['gray_200']};
    text-align: center;
    color: {COLORS['gray_500']};
    font-size: 0.875rem;
">
    EVALUERA - KI-gestützte Kostenanalyse
</div>
""", unsafe_allow_html=True)
