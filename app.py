"""
🎯 EVALUERA - KI-gestützte Kostenanalyse
==========================================
Professional cost analysis platform with AI-powered insights

Entry point for the Streamlit application.
All modules are cleanly organized under src/ directory.
"""

import os
import sys
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Add src to path for clean imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# UI modules
from src.ui.theme import apply_global_styles, COLORS, SPACING, RADIUS
from src.ui.login import check_login, render_login_screen, render_logout_button, inject_lottie_background, get_logo_base64
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
    gpt_analyze_supplier_competencies,
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

st.markdown(
    """
    <style>
html, body, .stApp, [data-testid="stAppViewContainer"], .main {background: #FFFFFF !important;}
.block-container {max-width:1300px!important; margin:0 auto!important; padding-left:1.25rem!important; padding-right:1.25rem!important; padding-top:0!important;}
[data-testid="stSidebar"] {background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(245,248,247,0.96) 100%) !important; backdrop-filter: blur(10px)!important; -webkit-backdrop-filter: blur(10px)!important; border-right:1px solid rgba(42,79,87,0.08)!important; box-shadow:4px 0 12px rgba(0,0,0,0.04)!important;}
[data-testid="stSidebar"] .stButton > button {min-height:42px!important; border-radius:10px!important; padding:10px 12px!important;}
[data-testid="stSidebar"] button[data-testid=\"baseButton-primary\"], [data-testid=\"stSidebar\"] button[kind=\"primary\"] {background:#2A4F57!important; color:#FFFFFF!important; border:1px solid rgba(42,79,87,0.3)!important; box-shadow:0 6px 14px rgba(0,0,0,0.1)!important; font-weight:700!important;}
[data-testid=\"stSidebar\"] button[data-testid=\"baseButton-secondary\"], [data-testid=\"stSidebar\"] button[kind=\"secondary\"] {background:rgba(255,255,255,0.92)!important; border:1px solid rgba(42,79,87,0.18)!important; color:#1E2E32!important; box-shadow:0 4px 12px rgba(0,0,0,0.05)!important; font-weight:600!important; margin:6px 0!important;}
/* Remove ghost containers / spacers */
div[data-testid=\"stHorizontalBlock\"], div[data-testid=\"stVerticalBlock\"], div[data-testid=\"column\"], div[data-testid=\"block-container\"], div[data-testid=\"element-container\"],
div[data-testid=\"stHorizontalBlock\"] > div, div[data-testid=\"stVerticalBlock\"] > div, div[data-testid=\"column\"] > div, div[data-testid=\"block-container\"] > div {
    background: transparent!important; border: none!important; box-shadow: none!important; padding: 0!important; margin:0!important;}
div[data-testid=\"stHorizontalBlock\"] > div > div, div[data-testid=\"stVerticalBlock\"] > div > div, div[data-testid=\"column\"] > div > div, div[data-testid=\"block-container\"] > div > div {
    background: transparent!important; border: none!important; box-shadow: none!important; padding:0!important; margin:0!important; border-radius:0!important;}
div[data-testid=\"stHorizontalBlock\"] > div > div:empty, div[data-testid=\"stVerticalBlock\"] > div > div:empty, div[data-testid=\"stHorizontalBlock\"] > div:empty, div[data-testid=\"stVerticalBlock\"] > div:empty,
div[data-testid=\"column\"] > div:empty, div[data-testid=\"block-container\"] > div:empty, div:empty {display:none!important; height:0!important; padding:0!important; margin:0!important; border:none!important; box-shadow:none!important; background:transparent!important;}
/* Essentials */
[data-testid=\"stProgressBar\"] > div {background:#E7F1EF!important; border-radius:9999px!important;}
[data-testid=\"stProgressBar\"] > div > div {background:#2A4F57!important; border-radius:9999px!important; height:10px!important;}
.stFileUploader {background:#FFFFFF!important; border:1.5px dashed rgba(42,79,87,0.18)!important; border-radius:16px!important; box-shadow:0 6px 14px rgba(0,0,0,0.06)!important;}
.stFileUploader:hover {border-color:#2A4F57!important; background:rgba(231,241,239,0.94)!important;}
.stFileUploader label {color:#1E2E32!important; font-weight:600!important;}
h1, h2, h3, h4 {color:#2A4F57!important;} p, span, label, div {color:#333333!important;}
hr, div[role=\"separator\"] {display:none!important; height:0!important; border:none!important; margin:0!important; padding:0!important; background:transparent!important;}
#wizard-next-fixed-container {position:fixed!important; right:2.4rem!important; bottom:2.0rem!important; z-index:9999!important;}
@media(max-width:900px){#wizard-next-fixed-container {right:50%!important; transform:translateX(50%);}}
div[data-baseweb=\"input\"]:focus-within {border-color:#1F3C45!important; box-shadow:0 0 0 2px rgba(31,60,69,0.18), 0 6px 16px rgba(0,0,0,0.08)!important;}
.stButton > button, button[kind=\"primary\"] {background:#1F3C45!important; color:#FFFFFF!important; border:none!important;}
.css-18e3th9, .css-1v0mbdj, .css-1dp5vir, .css-1kyxreq, .css-ocqkz7, .css-hg7snz, .css-ffhzg2 {display:none!important; height:0!important; padding:0!important; margin:0!important; box-shadow:none!important; background:transparent!important; border:none!important;}
    </style>
    """,
    unsafe_allow_html=True,
)

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
        # New: Store article search results
        'article_matches': None,
        'supplier_competencies': None,
        'reference_articles': None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==================== MAIN APP HEADER ====================
st.markdown(f"""
<div style="text-align: center; padding: {SPACING['xl']} 0 {SPACING['md']} 0;">
    <img src="data:image/png;base64,{get_logo_base64()}" alt="EVALUERA" style="height: 48px; object-fit: contain;" />
    <h1 style="color: {COLORS['primary']}; font-weight: 800; margin: {SPACING['md']} 0 {SPACING['sm']} 0;">
        KI-gestützte Bestellanalyse & Kostenschätzung
    </h1>
    <p style="color: #333333; font-size: 1.05rem; margin-top: 0; font-weight: 500;">
        Professionelle Beschaffungsoptimierung mit künstlicher Intelligenz
    </p>
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
    <div style="background: rgba(255,255,255,0.9); padding: {SPACING['lg']}; border-radius: 16px; box-shadow: 0 14px 36px rgba(0,0,0,0.12); border: 1px solid rgba(42,79,87,0.12); margin: {SPACING['lg']} 0;">
        <h3 style="color: {COLORS['primary']}; margin: 0 0 {SPACING['sm']} 0; font-weight: 700;">📁 Schritt 1: Bestellung hochladen</h3>
        <p style="color: #333333; margin: 0; font-weight: 500;">
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
        st.caption(f"Datei: **{uploaded_file.name}** ({uploaded_file.type or 'unbekannt'}, {uploaded_file.size} Bytes)")
        with ExcelLoadingAnimation("Excel-Datei wird analysiert..."):
            try:
                df = pd.read_excel(uploaded_file, engine=None)
                st.session_state.df_raw = df
                st.session_state.uploaded_file = uploaded_file.name

                st.success(f"✓ **{uploaded_file.name}** erfolgreich geladen ({len(df)} Zeilen)")

                # Keine Preview anzeigen (Performance/Clarity)
                # Falls gewünscht, hier wieder aktivieren.

                if st.button("Weiter zu Schritt 2", type="primary", use_container_width=True):
                    wizard.next_step()
                    st.rerun()

            except Exception as e:
                st.error(f"❌ Fehler beim Laden der Datei: {str(e)}")
                st.exception(e)

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

        matches_df = None
        if search_query:
            with GPTLoadingAnimation("KI analysiert Ihre Suchanfrage..."):
                try:
                    # Find item column
                    item_col = find_column(df, ["item", "artikel", "bezeichnung", "produkt", "article"])
                    if item_col:
                        # WICHTIG: Kein dropna() - sonst stimmen Indizes nicht!
                        item_values = df[item_col].tolist()
                        matching_indices = gpt_intelligent_article_search(search_query, item_values)

                        if matching_indices and len(matching_indices) > 0:
                            # GPT hat was gefunden
                            matches_df = df.iloc[matching_indices].copy()
                            st.session_state.article_matches = matches_df
                            st.session_state.article_name = search_query
                            st.success(f"✓ {len(matches_df)} passende Artikel gefunden (KI-Suche)")
                            st.dataframe(matches_df, use_container_width=True)
                        else:
                            # FALLBACK: String-basierte Suche (wie vorher!)
                            st.info("🔍 KI fand nichts - verwende erweiterte Suche...")
                            search_mask = df[item_col].astype(str).str.lower().str.contains(
                                search_query.lower(), na=False, regex=False
                            )
                            matches_df = df[search_mask].copy()

                            if len(matches_df) > 0:
                                st.session_state.article_matches = matches_df
                                st.session_state.article_name = search_query
                                st.success(f"✓ {len(matches_df)} passende Artikel gefunden (String-Suche)")
                                st.dataframe(matches_df, use_container_width=True)
                            else:
                                st.warning("⚠️ Keine passenden Artikel gefunden. Versuchen Sie andere Suchbegriffe.")
                    else:
                        st.error("❌ Keine Artikel-Spalte gefunden in der Excel-Datei")
                except Exception as e:
                    st.error(f"⚠️ KI-Suche fehlgeschlagen: {str(e)}")
                    # FALLBACK bei Fehler: String-Suche
                    item_col = find_column(df, ["item", "artikel", "bezeichnung", "produkt", "article"])
                    if item_col:
                        st.info("🔄 Verwende Fallback-Suche...")
                        search_mask = df[item_col].astype(str).str.lower().str.contains(
                            search_query.lower(), na=False, regex=False
                        )
                        matches_df = df[search_mask].copy()
                        if len(matches_df) > 0:
                            st.session_state.article_matches = matches_df
                            st.session_state.article_name = search_query
                            st.success(f"✓ {len(matches_df)} Artikel gefunden")
                            st.dataframe(matches_df, use_container_width=True)

        # Manual selection (fallback)
        if not search_query:
            st.markdown("**Oder wählen Sie manuell:**")
            selected_idx = st.selectbox(
                "Zeile auswählen",
                options=range(len(df)),
                format_func=lambda x: f"Zeile {x+1}: {df.iloc[x, 0] if len(df.columns) > 0 else 'N/A'}"
            )

            if selected_idx is not None:
                st.session_state.selected_row = df.iloc[selected_idx]
                st.session_state.article_matches = df.iloc[[selected_idx]].copy()

                st.markdown("**Ausgewählter Artikel:**")
                st.json(st.session_state.selected_row.to_dict())

        # Navigation buttons
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Zurück", use_container_width=True):
                wizard.prev_step()
                st.rerun()
        with col2:
            # Only allow progression if articles were found
            can_proceed = (st.session_state.article_matches is not None and
                          len(st.session_state.article_matches) > 0)
            if st.button("Weiter zu Schritt 3 →", type="primary", use_container_width=True,
                        disabled=not can_proceed):
                if can_proceed:
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

    # Check if we have article matches from step 2
    if st.session_state.article_matches is None or len(st.session_state.article_matches) == 0:
        st.warning("⚠️ Keine Artikel ausgewählt. Bitte gehen Sie zurück zu Schritt 2.")
        if st.button("← Zurück zu Schritt 2", use_container_width=True):
            wizard.prev_step()
            st.rerun()
    else:
        matches_df = st.session_state.article_matches

        # Display reference articles from Excel
        st.markdown("### 📋 Referenz-Artikel aus Bestellhistorie")
        st.markdown(f"Basierend auf Ihrer Suche: **{st.session_state.article_name}**")

        # Show matches in expandable section
        with st.expander("🔍 Gefundene Artikel anzeigen", expanded=True):
            st.dataframe(matches_df, use_container_width=True)

        st.markdown("---")

        # STEP 1: Select Supplier (Dropdown from Excel data)
        st.markdown("### 1️⃣ Lieferant auswählen")

        # Extract unique suppliers from matches
        supplier_col = find_column(matches_df, ["supplier", "lieferant", "anbieter", "vendor"])
        if supplier_col:
            suppliers = matches_df[supplier_col].dropna().unique().tolist()

            if len(suppliers) > 0:
                selected_supplier = st.selectbox(
                    "Lieferant",
                    options=suppliers,
                    index=suppliers.index(st.session_state.supplier_name) if st.session_state.supplier_name in suppliers else 0,
                    help="Wählen Sie einen Lieferanten aus, der diesen Artikel bereits geliefert hat"
                )

                st.session_state.supplier_name = selected_supplier

                # Show supplier articles
                supplier_articles = matches_df[matches_df[supplier_col] == selected_supplier]
                item_col = find_column(supplier_articles, ["item", "artikel", "bezeichnung", "produkt"])

                if item_col:
                    article_list = supplier_articles[item_col].tolist()
                    st.info(f"📦 **{selected_supplier}** hat {len(supplier_articles)} dieser Artikel geliefert")

                    # STEP 2: Analyze Supplier Competencies (Automatic)
                    st.markdown("### 2️⃣ Lieferanten-Kompetenzen analysieren")

                    if st.session_state.supplier_competencies is None or \
                       st.session_state.supplier_competencies.get('supplier_name') != selected_supplier:
                        if st.button("🔍 Lieferanten-Kompetenzen analysieren", type="primary"):
                            with GPTLoadingAnimation("KI analysiert Lieferanten-Kompetenzen..."):
                                try:
                                    # Analyze supplier competencies based on article history
                                    competencies = gpt_analyze_supplier_competencies(
                                        supplier_name=selected_supplier,
                                        article_history=article_list,
                                        country=None  # Could extract from Excel if available
                                    )

                                    st.session_state.supplier_competencies = competencies
                                    st.rerun()

                                except Exception as e:
                                    st.error(f"❌ Fehler bei Kompetenz-Analyse: {str(e)}")
                    else:
                        # Display competencies
                        comp = st.session_state.supplier_competencies

                        if not comp.get('_error') and not comp.get('_fallback'):
                            st.success("✓ Lieferanten-Kompetenzen analysiert")

                            # Core competencies
                            core_comps = comp.get('core_competencies', [])
                            if core_comps:
                                st.markdown("**🏭 Hauptkompetenzen:**")
                                for c in core_comps[:3]:  # Top 3
                                    process_name = c.get('process', 'Unknown')
                                    capability = c.get('capability_level', 'unknown')
                                    confidence = c.get('confidence', 'unknown')
                                    st.markdown(f"- **{process_name}** (Level: {capability}, Confidence: {confidence})")

                            # Material expertise
                            mat_exp = comp.get('material_expertise', [])
                            if mat_exp:
                                st.markdown("**🔩 Material-Expertise:**")
                                materials = [m.get('material', 'Unknown') for m in mat_exp[:3]]
                                st.markdown(f"- {', '.join(materials)}")

                            # STEP 3: Determine Process (Automatic from competencies)
                            st.markdown("### 3️⃣ Fertigungsverfahren (automatisch ermittelt)")

                            # Get primary process from competencies
                            if core_comps:
                                primary_process = core_comps[0].get('process', 'turning')
                                process_display = primary_process.replace('_', ' ').title()

                                st.session_state.process = primary_process
                                st.info(f"🎯 **Empfohlenes Verfahren:** {process_display}")
                                st.caption(f"Basierend auf Lieferanten-Kompetenz: {core_comps[0].get('capability_level', 'proficient')}")
                            else:
                                st.warning("⚠️ Kein primäres Fertigungsverfahren ermittelt")

                            # STEP 4: Material & Dimensions (User input with suggestions)
                            st.markdown("### 4️⃣ Material & Abmessungen")

                            col1, col2 = st.columns(2)

                            with col1:
                                # Suggest material based on competencies
                                suggested_materials = []
                                if mat_exp:
                                    suggested_materials = [m.get('material', '') for m in mat_exp[:3] if m.get('material')]

                                material_hint = f"z.B. {', '.join(suggested_materials)}" if suggested_materials else "z.B. Stahl, Edelstahl, Aluminium"

                                material = st.text_input(
                                    "Material",
                                    value=st.session_state.material,
                                    placeholder=material_hint,
                                    help="KI wird das Material basierend auf Artikel-Kontext weiter präzisieren"
                                )
                                st.session_state.material = material

                            with col2:
                                dimensions = st.text_input(
                                    "Abmessungen",
                                    value=st.session_state.dimensions,
                                    placeholder="z.B. M8x30, 100x50x2mm",
                                    help="Optional - wird aus Artikel extrahiert falls nicht angegeben"
                                )
                                st.session_state.dimensions = dimensions

                            # STEP 5: Lot Size
                            st.markdown("### 5️⃣ Losgröße")

                            # Get average lot size from history
                            qty_col = find_column(supplier_articles, ["quantity", "menge", "qty", "anzahl"])
                            avg_qty = 1

                            if qty_col:
                                quantities = pd.to_numeric(supplier_articles[qty_col], errors='coerce').dropna()
                                if len(quantities) > 0:
                                    avg_qty = int(quantities.mean())
                                    st.caption(f"📊 Durchschnittliche Bestellmenge: {avg_qty} Stück")

                            lot_size = st.number_input(
                                "Losgröße",
                                min_value=1,
                                value=max(avg_qty, st.session_state.lot_size) if st.session_state.lot_size > 1 else avg_qty,
                                help="Anzahl der zu produzierenden Teile"
                            )
                            st.session_state.lot_size = lot_size

                            # Summary before proceeding
                            st.markdown("---")
                            st.markdown("### ✅ Zusammenfassung")

                            summary_cols = st.columns(3)
                            with summary_cols[0]:
                                st.markdown(f"""
                                <div style="background: {COLORS['surface']}; padding: {SPACING['md']}; border-radius: {RADIUS['md']}; border-left: 3px solid {COLORS['primary']};">
                                    <p style="color: {COLORS['gray_600']}; margin: 0; font-size: 0.8rem;">Lieferant</p>
                                    <p style="color: {COLORS['error']}; margin: 0; font-weight: 600;">{selected_supplier}</p>
                                </div>
                                """, unsafe_allow_html=True)

                            with summary_cols[1]:
                                st.markdown(f"""
                                <div style="background: {COLORS['surface']}; padding: {SPACING['md']}; border-radius: {RADIUS['md']}; border-left: 3px solid {COLORS['primary']};">
                                    <p style="color: {COLORS['gray_600']}; margin: 0; font-size: 0.8rem;">Fertigungsverfahren</p>
                                    <p style="color: {COLORS['error']}; margin: 0; font-weight: 600;">{st.session_state.process.replace('_', ' ').title() if st.session_state.process else 'N/A'}</p>
                                </div>
                                """, unsafe_allow_html=True)

                            with summary_cols[2]:
                                st.markdown(f"""
                                <div style="background: {COLORS['surface']}; padding: {SPACING['md']}; border-radius: {RADIUS['md']}; border-left: 3px solid {COLORS['primary']};">
                                    <p style="color: {COLORS['gray_600']}; margin: 0; font-size: 0.8rem;">Losgröße</p>
                                    <p style="color: {COLORS['error']}; margin: 0; font-weight: 600;">{lot_size:,} Stück</p>
                                </div>
                                """, unsafe_allow_html=True)

                        else:
                            st.warning("⚠️ Lieferanten-Kompetenzen konnten nicht analysiert werden. Bitte klicken Sie auf 'Analysieren'.")

            else:
                st.error("❌ Keine Lieferanten in den gefundenen Artikeln")
        else:
            st.error("❌ Keine Lieferanten-Spalte in der Excel-Datei gefunden")

        # Navigation
        st.markdown("---")
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("← Zurück", use_container_width=True):
                wizard.prev_step()
                st.rerun()
        with col2:
            # Can only proceed if supplier competencies are analyzed
            can_proceed = (st.session_state.supplier_competencies is not None and
                          st.session_state.supplier_name and
                          st.session_state.process)

            if st.button("Weiter zu Schritt 4 →", type="primary", use_container_width=True,
                        disabled=not can_proceed):
                if can_proceed:
                    wizard.next_step()
                    st.rerun()
                else:
                    st.warning("⚠️ Bitte analysieren Sie zuerst die Lieferanten-Kompetenzen")

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
                # Build complete description from available data
                description_parts = [st.session_state.article_name]
                if st.session_state.material:
                    description_parts.append(f"Material: {st.session_state.material}")
                if st.session_state.dimensions:
                    description_parts.append(f"Abmessungen: {st.session_state.dimensions}")
                if st.session_state.process:
                    description_parts.append(f"Verfahren: {st.session_state.process}")

                full_description = " | ".join(description_parts)

                # Serialize supplier competencies for caching
                supplier_comp_json = None
                if st.session_state.supplier_competencies:
                    supplier_comp_json = json.dumps(st.session_state.supplier_competencies)

                # Call optimized cost estimation with supplier context
                result = cached_gpt_complete_cost_estimate(
                    description=full_description,
                    lot_size=st.session_state.lot_size,
                    supplier_competencies_json=supplier_comp_json
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
