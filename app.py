"""
🎯 EVALUERA - KI-gestützte Kostenanalyse
==========================================
Professional cost analysis platform with AI-powered insights

Entry point for the Streamlit application.
All modules are cleanly organized under src/ directory.
"""

import os
import sys
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Add src to path for clean imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# UI modules
from src.ui.theme import apply_global_styles, COLORS, SPACING, RADIUS
from src.ui.login import check_login, render_login_screen, render_logout_button, inject_lottie_background
from src.ui.navigation import NavigationSidebar
from src.ui.wizard import WizardManager
from src.ui.cards import render_evaluera_logo, GPTLoadingAnimation, ExcelLoadingAnimation

# Business logic - GPT/AI
from src.gpt.engine import gpt_intelligent_article_search
from src.gpt.cache import cached_gpt_complete_cost_estimate, cached_gpt_analyze_supplier

# Business logic - Core
from src.core.cbam import (
    parse_dims,
    clamp_dims,
    gpt_rate_supplier,
    calculate_co2_footprint,
)
from src.negotiation.engine import gpt_negotiation_prep_enhanced

# Utilities
from src.utils.excel_helpers import find_column, get_price_series_per_unit
from src.core.price_utils import derive_unit_price

# ==================== CONFIGURATION ====================
load_dotenv()

st.set_page_config(
    page_title="EVALUERA - Kostenanalyse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ==================== AUTHENTICATION ====================
# Inject Lottie background for login screen
inject_lottie_background()

# Check authentication
if not check_login():
    render_login_screen()
    st.stop()

# ==================== GLOBAL STYLING ====================
apply_global_styles()

# ==================== NAVIGATION ====================
nav = NavigationSidebar()

# ==================== SESSION STATE INITIALIZATION ====================
def init_session_state():
    """Initialize all required session state variables"""
    defaults = {
        'wizard_step': 1,
        'uploaded_file': None,
        'df_raw': None,
        'selected_row': None,
        'article_name': '',
        'supplier_name': '',
        'material': '',
        'dimensions': '',
        'lot_size': 1,
        'process': '',
        'cost_estimate': None,
        'supplier_analysis': None,
        'negotiation_prep': None,
        'co2_data': None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==================== MAIN APP HEADER ====================
st.markdown(f"""
<div style="text-align: center; padding: {SPACING['xl']} 0 {SPACING['md']} 0;">
""", unsafe_allow_html=True)

render_evaluera_logo(align="center", width=230)

st.markdown(f"""
<div style="text-align: center; margin-top: {SPACING['md']}; margin-bottom: {SPACING['xl']};">
    <h1 style="color: {COLORS['error']}; font-weight: 700; margin: 0;">
        KI-gestützte Bestellanalyse & Kostenschätzung
    </h1>
    <p style="color: {COLORS['gray_600']}; font-size: 1.1rem; margin-top: {SPACING['sm']};">
        Professionelle Beschaffungsoptimierung mit künstlicher Intelligenz
    </p>
</div>
</div>
""", unsafe_allow_html=True)

# Logout button in top right
col1, col2 = st.columns([6, 1])
with col2:
    render_logout_button()

# ==================== WIZARD NAVIGATION ====================
wizard = WizardManager()
wizard.render_progress()

# ==================== STEP 1: EXCEL UPLOAD ====================
if wizard.get_current_step() == 1:
    st.markdown(f"""
    <div style="background: {COLORS['surface_tint']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; border-left: 4px solid {COLORS['primary']}; margin: {SPACING['lg']} 0;">
        <h3 style="color: {COLORS['error']}; margin: 0 0 {SPACING['sm']} 0;">📁 Schritt 1: Bestellung hochladen</h3>
        <p style="color: {COLORS['gray_700']}; margin: 0;">
            Laden Sie Ihre Excel-Bestellung hoch. Wir analysieren automatisch Artikel, Preise und Lieferanten.
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Excel-Datei auswählen",
        type=["xlsx", "xls"],
        help="Unterstützte Formate: .xlsx, .xls"
    )

    if uploaded_file:
        with ExcelLoadingAnimation("Excel-Datei wird analysiert..."):
            try:
                df = pd.read_excel(uploaded_file)
                st.session_state.df_raw = df
                st.session_state.uploaded_file = uploaded_file.name

                st.success(f"✓ **{uploaded_file.name}** erfolgreich geladen ({len(df)} Zeilen)")

                # Preview
                st.markdown(f"**Vorschau der ersten 10 Zeilen:**")
                st.dataframe(df.head(10), use_container_width=True)

                if st.button("Weiter zu Schritt 2", type="primary", use_container_width=True):
                    wizard.next_step()
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Fehler beim Laden der Datei: {str(e)}")

# ==================== STEP 2: ARTICLE SELECTION ====================
elif wizard.get_current_step() == 2:
    st.markdown(f"""
    <div style="background: {COLORS['surface_tint']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; border-left: 4px solid {COLORS['primary']}; margin: {SPACING['lg']} 0;">
        <h3 style="color: {COLORS['error']}; margin: 0 0 {SPACING['sm']} 0;">🔍 Schritt 2: Artikel auswählen</h3>
        <p style="color: {COLORS['gray_700']}; margin: 0;">
            Wählen Sie einen Artikel zur Analyse oder verwenden Sie die KI-Suche.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.df_raw is not None:
        df = st.session_state.df_raw

        # AI-powered search
        search_query = st.text_input(
            "🤖 KI-Artikelsuche",
            placeholder="z.B. 'Zylinderschraube M8x30' oder 'Edelstahlblech 2mm'",
            help="Beschreiben Sie den gesuchten Artikel - die KI findet passende Einträge"
        )

        if search_query:
            with GPTLoadingAnimation("KI analysiert Ihre Suchanfrage..."):
                try:
                    matches = gpt_intelligent_article_search(search_query, df)
                    if matches:
                        st.success(f"✓ {len(matches)} passende Artikel gefunden")
                        st.dataframe(matches, use_container_width=True)
                except Exception as e:
                    st.warning(f"⚠️ KI-Suche fehlgeschlagen: {str(e)}")

        # Manual selection
        st.markdown("**Oder wählen Sie manuell:**")
        selected_idx = st.selectbox(
            "Zeile auswählen",
            options=range(len(df)),
            format_func=lambda x: f"Zeile {x+1}: {df.iloc[x, 0] if len(df.columns) > 0 else 'N/A'}"
        )

        if selected_idx is not None:
            st.session_state.selected_row = df.iloc[selected_idx]

            st.markdown("**Ausgewählter Artikel:**")
            st.json(st.session_state.selected_row.to_dict())

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("← Zurück", use_container_width=True):
                    wizard.prev_step()
                    st.rerun()
            with col2:
                if st.button("Weiter zu Schritt 3 →", type="primary", use_container_width=True):
                    wizard.next_step()
                    st.rerun()

# ==================== STEP 3: ARTICLE DETAILS ====================
elif wizard.get_current_step() == 3:
    st.markdown(f"""
    <div style="background: {COLORS['surface_tint']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; border-left: 4px solid {COLORS['primary']}; margin: {SPACING['lg']} 0;">
        <h3 style="color: {COLORS['error']}; margin: 0 0 {SPACING['sm']} 0;">📝 Schritt 3: Artikeldetails eingeben</h3>
        <p style="color: {COLORS['gray_700']}; margin: 0;">
            Präzisieren Sie die technischen Details für eine genaue Kostenschätzung.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        article_name = st.text_input("Artikelbezeichnung", value=st.session_state.article_name)
        material = st.text_input("Material", value=st.session_state.material, placeholder="z.B. Edelstahl 1.4301, S235JR")
        dimensions = st.text_input("Abmessungen", value=st.session_state.dimensions, placeholder="z.B. 100x50x2mm")

    with col2:
        supplier_name = st.text_input("Lieferant", value=st.session_state.supplier_name)
        lot_size = st.number_input("Losgröße", min_value=1, value=st.session_state.lot_size)
        process = st.text_input("Fertigungsverfahren", value=st.session_state.process, placeholder="z.B. Laserschneiden, CNC-Fräsen")

    st.session_state.article_name = article_name
    st.session_state.material = material
    st.session_state.dimensions = dimensions
    st.session_state.supplier_name = supplier_name
    st.session_state.lot_size = lot_size
    st.session_state.process = process

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Zurück", use_container_width=True):
            wizard.prev_step()
            st.rerun()
    with col2:
        if st.button("Weiter zu Schritt 4 →", type="primary", use_container_width=True):
            wizard.next_step()
            st.rerun()

# ==================== STEP 4: COST ESTIMATION ====================
elif wizard.get_current_step() == 4:
    st.markdown(f"""
    <div style="background: {COLORS['surface_tint']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; border-left: 4px solid {COLORS['primary']}; margin: {SPACING['lg']} 0;">
        <h3 style="color: {COLORS['error']}; margin: 0 0 {SPACING['sm']} 0;">💰 Schritt 4: KI-Kostenschätzung</h3>
        <p style="color: {COLORS['gray_700']}; margin: 0;">
            Unsere KI berechnet den minimal möglichen Zielpreis basierend auf Marktdaten.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Kostenschätzung starten", type="primary", use_container_width=True):
        with GPTLoadingAnimation("KI berechnet optimale Kosten..."):
            try:
                # Enhanced prompt for minimal costs
                result = cached_gpt_complete_cost_estimate(
                    article=st.session_state.article_name,
                    material=st.session_state.material,
                    dimensions=st.session_state.dimensions,
                    lot_size=st.session_state.lot_size,
                    process=st.session_state.process,
                    supplier=st.session_state.supplier_name
                )

                st.session_state.cost_estimate = result
                st.success("✓ Kostenschätzung abgeschlossen!")

            except Exception as e:
                st.error(f"❌ Fehler bei der Kostenschätzung: {str(e)}")

    if st.session_state.cost_estimate:
        result = st.session_state.cost_estimate

        # Display results in professional cards
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style="background: {COLORS['surface']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; border: 2px solid {COLORS['primary']}; text-align: center;">
                <p style="color: {COLORS['gray_600']}; margin: 0; font-size: 0.9rem;">Materialkosten</p>
                <h2 style="color: {COLORS['primary']}; margin: {SPACING['sm']} 0;">€ {result.get('material_cost_min', 0):.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background: {COLORS['surface']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; border: 2px solid {COLORS['primary']}; text-align: center;">
                <p style="color: {COLORS['gray_600']}; margin: 0; font-size: 0.9rem;">Fertigungskosten</p>
                <h2 style="color: {COLORS['primary']}; margin: {SPACING['sm']} 0;">€ {result.get('fabrication_cost_min', 0):.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%); padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <p style="color: white; margin: 0; font-size: 0.9rem; opacity: 0.9;">🎯 Zielpreis (minimal)</p>
                <h2 style="color: white; margin: {SPACING['sm']} 0; font-size: 2rem;">€ {result.get('target_price_min', 0):.2f}</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"**Konfidenz:** {result.get('confidence', 'N/A')}")
        st.markdown(f"**Methodik:** {result.get('method_info', 'N/A')}")

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Zurück", use_container_width=True):
                wizard.prev_step()
                st.rerun()
        with col2:
            if st.button("Weiter zu Schritt 5 →", type="primary", use_container_width=True):
                wizard.next_step()
                st.rerun()

# ==================== STEP 5: SUPPLIER ANALYSIS ====================
elif wizard.get_current_step() == 5:
    st.markdown(f"""
    <div style="background: {COLORS['surface_tint']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; border-left: 4px solid {COLORS['primary']}; margin: {SPACING['lg']} 0;">
        <h3 style="color: {COLORS['error']}; margin: 0 0 {SPACING['sm']} 0;">🏭 Schritt 5: Lieferanten-Analyse</h3>
        <p style="color: {COLORS['gray_700']}; margin: 0;">
            Detaillierte Bewertung der Lieferantenfähigkeiten und Standortfaktoren.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍 Lieferanten-Analyse starten", type="primary", use_container_width=True):
        with GPTLoadingAnimation("KI analysiert Lieferanten..."):
            try:
                analysis = cached_gpt_analyze_supplier(
                    supplier=st.session_state.supplier_name,
                    material=st.session_state.material,
                    process=st.session_state.process
                )

                st.session_state.supplier_analysis = analysis
                st.success("✓ Lieferanten-Analyse abgeschlossen!")

            except Exception as e:
                st.error(f"❌ Fehler bei der Lieferanten-Analyse: {str(e)}")

    if st.session_state.supplier_analysis:
        st.markdown("### Analyse-Ergebnis")
        st.json(st.session_state.supplier_analysis)

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Zurück", use_container_width=True):
                wizard.prev_step()
                st.rerun()
        with col2:
            if st.button("Weiter zu Schritt 6 →", type="primary", use_container_width=True):
                wizard.next_step()
                st.rerun()

# ==================== STEP 6: NEGOTIATION STRATEGY ====================
elif wizard.get_current_step() == 6:
    st.markdown(f"""
    <div style="background: {COLORS['surface_tint']}; padding: {SPACING['lg']}; border-radius: {RADIUS['lg']}; border-left: 4px solid {COLORS['primary']}; margin: {SPACING['lg']} 0;">
        <h3 style="color: {COLORS['error']}; margin: 0 0 {SPACING['sm']} 0;">🎯 Schritt 6: Verhandlungsstrategie</h3>
        <p style="color: {COLORS['gray_700']}; margin: 0;">
            KI-generierte Verhandlungsstrategie mit Marktanalyse und Taktiken.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Strategie generieren", type="primary", use_container_width=True):
        with GPTLoadingAnimation("KI erstellt Verhandlungsstrategie..."):
            try:
                strategy = gpt_negotiation_prep_enhanced(
                    article=st.session_state.article_name,
                    current_price=100.0,  # From Excel if available
                    target_price=st.session_state.cost_estimate.get('target_price_min', 50.0) if st.session_state.cost_estimate else 50.0,
                    supplier=st.session_state.supplier_name,
                    material=st.session_state.material,
                    lot_size=st.session_state.lot_size
                )

                st.session_state.negotiation_prep = strategy
                st.success("✓ Verhandlungsstrategie erstellt!")

            except Exception as e:
                st.error(f"❌ Fehler bei Strategieerstellung: {str(e)}")

    if st.session_state.negotiation_prep:
        st.markdown("### 📋 Verhandlungsstrategie")
        st.json(st.session_state.negotiation_prep)

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Zurück", use_container_width=True):
                wizard.prev_step()
                st.rerun()
        with col2:
            if st.button("✓ Analyse abschließen", type="primary", use_container_width=True):
                st.balloons()
                st.success("🎉 Analyse erfolgreich abgeschlossen!")

# ==================== SIDEBAR NAVIGATION ====================
nav.render()

# ==================== FOOTER ====================
st.markdown(f"""
<div style="text-align: center; padding: {SPACING['xl']} 0; color: {COLORS['gray_500']}; font-size: 0.85rem; border-top: 1px solid {COLORS['primary_light']}; margin-top: {SPACING['xxl']};">
    <p>EVALUERA © 2024 | KI-gestützte Kostenanalyse</p>
</div>
""", unsafe_allow_html=True)
