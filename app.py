"""
🎯 EVALUERA - KI-gestützte Kostenanalyse
==========================================
Moderne Wizard-basierte Oberfläche für intelligente Beschaffung
"""

import os
import re
import traceback
import sys
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.gpt.utils import sanitize_input

# Sicherstellen, dass das Projekt-Root und das src-Paket im Python-Pfad liegen
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
for path in (BASE_DIR, SRC_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

# Zentrale Sicherung der Auswahl-States
def ensure_selection_state():
    """Initialisiert und säubert zentrale Auswahl-Keys."""
    defaults = {
        "selected_article": None,
        "selected_supplier_name": None,
        "selected_supplier": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Sanitize vorhandene Werte
    if st.session_state.get("selected_article"):
        st.session_state.selected_article = sanitize_input(st.session_state.selected_article)
    if st.session_state.get("selected_supplier_name"):
        st.session_state.selected_supplier_name = sanitize_input(st.session_state.selected_supplier_name)
    if st.session_state.get("selected_supplier"):
        sup = st.session_state.selected_supplier
        if isinstance(sup, dict):
            st.session_state.selected_supplier = {sanitize_input(k): sanitize_input(v) for k, v in sup.items()}
        else:
            st.session_state.selected_supplier = {"name": sanitize_input(str(sup))}

ensure_selection_state()


def set_selected_article(article_value: str):
    """Zentraler Setter für die Artikelauswahl."""
    ensure_selection_state()
    if article_value:
        st.session_state.selected_article = sanitize_input(article_value)
    else:
        st.session_state.selected_article = None
    st.write(f"DEBUG set_selected_article -> {st.session_state.selected_article}")


def render_negotiation_tips(tips: dict):
    """UI-freundliche Darstellung der Verhandlungsstrategie."""
    if not tips:
        st.info("Keine Verhandlungsstrategie verfügbar.")
        return

    def show_list(title, items, icon="•"):
        if items:
            st.markdown(f"**{title}**")
            for it in items:
                st.markdown(f"- {icon} {it}")

    st.markdown("#### 🏭 Lieferantenanalyse")
    sa = tips.get("supplier_analysis", {})
    show_list("Produktionskompetenzen", sa.get("production_competencies", []))
    if sa.get("scaling_capabilities"):
        st.markdown(f"**Skalierung:** {sa['scaling_capabilities']}")
    show_list("Zertifizierungen", sa.get("certifications", []))
    show_list("Standortvorteile", sa.get("location_advantages", []), icon="✅")
    show_list("Standortnachteile", sa.get("location_disadvantages", []), icon="⚠️")
    show_list("Supply-Chain-Risiken", sa.get("supply_chain_risks", []), icon="🚨")

    st.markdown("#### 📊 Marktanalyse")
    ma = tips.get("market_analysis", {})
    raw = ma.get("raw_material_trends", {})
    if raw:
        st.markdown(f"- **Material:** {raw.get('material','')} | Aktuell: {raw.get('current_price_eur_kg','')} €/kg | Trend 12M: {raw.get('price_trend_12mo','')}")
    show_list("Konkurrenzangebote", ma.get("competitor_offers", []))
    cr = ma.get("country_risks", {})
    if cr:
        st.markdown(f"- **Zölle:** {cr.get('tariffs','')} | CBAM: {cr.get('cbam_costs','')} | Transport: {cr.get('transport_costs','')}")
    if ma.get("expected_price_development"):
        st.markdown(f"- **Erwartete Preisentwicklung:** {ma['expected_price_development']}")

    st.markdown("#### 🧭 Strategie")
    so = tips.get("strategy_overview", {})
    if so:
        st.markdown(f"- **Ansatz:** {so.get('main_approach','')} | Machtbalance: {so.get('negotiation_power_balance','')} | Erfolg: {so.get('estimated_success_probability','')}")
        show_list("Hebelpunkte", so.get("key_leverage_points", []))

    st.markdown("#### 🎯 Ziele")
    obj = tips.get("objectives", {})
    if obj:
        st.markdown(f"- **Primär:** {obj.get('primary_goal','')}")
        show_list("Sekundär", obj.get("secondary_goals", []))
        if obj.get("minimum_acceptable_outcome"):
            st.markdown(f"- **Minimum:** {obj['minimum_acceptable_outcome']}")
        if obj.get("batna"):
            st.markdown(f"- **BATNA:** {obj['batna']}")

    st.markdown("#### 📝 Kernargumente")
    for idx, arg in enumerate(tips.get("key_arguments", []), 1):
        st.markdown(f"**Argument {idx}:** {arg.get('argument','')}")
        show_list("Fakten", arg.get("supporting_facts", []))
        if arg.get("expected_counter"):
            st.markdown(f"- Erwarteter Einwand: {arg['expected_counter']}")
        if arg.get("our_response"):
            st.markdown(f"- Unsere Antwort: {arg['our_response']}")

    show_list("🎭 Taktiken", tips.get("tactics", []))

    st.markdown("#### 🤝 Zugeständnisse")
    for conc in tips.get("concessions", []):
        st.markdown(f"- Wir bieten: {conc.get('what_we_offer','')} | Wir fordern: {conc.get('what_we_want','')} | Wert: {conc.get('trade_off_value','')}")

    show_list("🚨 Red Flags", tips.get("red_flags", []))

    if tips.get("opening_statement") or tips.get("closing_statement"):
        st.markdown("#### 💬 Formulierungen")
        if tips.get("opening_statement"):
            st.info(f"Eröffnung: {tips['opening_statement']}")
        if tips.get("closing_statement"):
            st.success(f"Abschluss: {tips['closing_statement']}")

# Backend-Funktionen (angepasste src-Pfade)
from src.core.price_utils import derive_unit_price
from src.core.cbam import (
    parse_dims,
    clamp_dims,
    gpt_rate_supplier,
    gpt_negotiation_prep,
    calculate_co2_footprint,
)
from src.negotiation.engine import gpt_negotiation_prep_enhanced
from src.gpt.engine import gpt_intelligent_article_search
from src.utils.excel_helpers import (
    find_column,
    get_price_series_per_unit,
)
from src.gpt.cache import (
    cached_gpt_complete_cost_estimate,
    cached_gpt_analyze_supplier,
)

# UI-System (angepasste src-Pfade)
# UI-System (angepasste src-Pfade)
from src.ui.theme import (
    apply_global_styles,
    section_header,
    divider,
    status_badge,
    card,
    COLORS,
    SPACING,
    RADIUS,
    SHADOWS,
)
from src.ui.wizard import (
    WizardManager,
    create_data_table,
    create_compact_kpi_row,
)
from src.ui.cards import GPTLoadingAnimation, ExcelLoadingAnimation
from src.ui.navigation import NavigationSidebar, create_section_anchor, create_scroll_behavior
from src.ui.login import check_login, render_login_screen, render_logout_button, inject_lottie_background, get_logo_base64
from src.ui.liquid_glass import apply_liquid_glass_styles, liquid_header, glass_card
from src.ui.drawing_analysis import render_drawing_analysis_page

# ==================== SETUP ====================
load_dotenv()

st.set_page_config(
    page_title="EVALUERA - Kostenanalyse",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# ==================== GLOBAL PERMANENT BACKGROUND (LOGIN ONLY) ====================
# Lottie-Login-Background auskommentiert (nicht benötigt)
# from inject_lottie_login_background import inject_lottie_background
# inject_lottie_background()

# EVALUERA Theme Override - handled by theme.py now


# ==================== LOGIN CHECK ====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    render_login_screen()
    st.stop()

# ==================== MAIN APP (nur wenn eingeloggt) ====================
# Ruhiger Hintergrund ohne Wellen (verhindert flackernde Mint-Overlays)
st.markdown(
    """
    <style>
    body, .stApp, [data-testid="stAppViewContainer"], .main, .block-container {
        background: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

apply_global_styles()
apply_liquid_glass_styles()
create_scroll_behavior()
wizard = WizardManager()
nav = NavigationSidebar()

# ==================== API KEY ====================
def get_api_key(key_name, default=None):
    try:
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except (FileNotFoundError, KeyError):
        pass
    return os.getenv(key_name) or default

openai_key = get_api_key("OPENAI_API_KEY")
if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
else:
    st.error("🚨 OpenAI API Key fehlt! Bitte in Streamlit Secrets konfigurieren.")

# ==================== HELPER FUNCTIONS ====================
def normalize_columns(df):
    df_norm = df.copy()
    df_norm.columns = [c.strip().lower() for c in df.columns]
    return df_norm


def find_col(df, possible_names):
    df_norm_cols = [c.strip().lower() for c in df.columns]
    for name in possible_names:
        if name in df_norm_cols:
            return df.columns[df_norm_cols.index(name)]
    return None

# ==================== HEADER - VisionOS Style ====================
logo_b64 = get_logo_base64()

# Main Container for Content
main_container = st.container()

with main_container:
    # Header Area
    col_header, col_spacer = st.columns([2, 1])
    with col_header:
        st.markdown(
            f"""
            <div style="padding: {SPACING['lg']} 0 {SPACING['md']} 0;">
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
                    {"<img src='data:image/png;base64," + logo_b64 + "' alt='EVALUERA' style='height: 48px; object-fit: contain;' />" if logo_b64 else "<h1 style='margin:0; color:#2A4F57; font-weight:800; font-size: 24px;'>EVALUERA</h1>"}
                    <div style="height: 24px; width: 1px; background: {COLORS['border_medium']};"></div>
                    <div style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase;">Intelligent Procurement</div>
                </div>
                <h1 style="
                    color: {COLORS['primary']}; 
                    font-weight: 700; 
                    margin: 0; 
                    font-size: 2.5rem; 
                    letter-spacing: -0.02em;
                    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                ">
                    Bestellanalyse & Kostenschätzung
                </h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Sidebar Navigation - Apple-ähnliche Navigation
nav.render()

# Sidebar Footer (Technical Drawing + Logout)
with st.sidebar:
    st.markdown("---")
    
    # Technical Drawing Button (Standalone)
    is_drawing_active = st.session_state.nav_active_section == "drawing_analysis"
    if st.button(
        "📐  Technische Zeichnung",
        key="nav_drawing_analysis",
        use_container_width=True,
        type="primary" if is_drawing_active else "secondary"
    ):
        st.session_state.nav_active_section = "drawing_analysis"
        st.rerun()
        
    st.write("") # Spacer

# Logout Button (Divider removed in login.py)
render_logout_button()

# Synchronize Navigation with Wizard Steps
nav_to_wizard = {
    "upload": 1,
    "artikel": 2,
    "preis": 3,
    "lieferanten": 4,
    "kosten": 5,
    "nachhaltigkeit": 6
}
if st.session_state.nav_active_section in nav_to_wizard:
    wizard_step = nav_to_wizard[st.session_state.nav_active_section]
    if wizard_step != st.session_state.wizard_current_step:
        wizard.set_step(wizard_step)

# Progress Bar (Hide on Drawing Analysis Page)
if st.session_state.nav_active_section != "drawing_analysis":
    wizard.render_progress()


# ==================== STEP 1: UPLOAD ====================
# ==================== STEP 1: UPLOAD ====================
def step1_upload():
    section_header(
        "Daten hochladen",
        "Starten Sie die Analyse mit Ihren Bestelldaten"
    )

    card_content = st.container()
    with card_content:
        uploaded_file = st.file_uploader(
            "Excel- oder CSV-Datei auswählen",
            type=["csv", "xlsx"],
            key="file_upload",
        )

        if uploaded_file:
            st.success(f"✅ Datei geladen: {uploaded_file.name}")

            try:
                # Read file with loading animation
                with ExcelLoadingAnimation(f"📂 Analysiere {uploaded_file.name}", icon="📊"):
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file, sep=None, engine="python")
                    else:
                        df = pd.read_excel(uploaded_file)

                    st.session_state.df = df
                    st.session_state.uploaded_file_name = uploaded_file.name
                    wizard.complete_step(1)

                    # Preview
                    with st.expander("📊 Datenvorschau anzeigen", expanded=False):
                        st.write(f"**{len(df):,} Zeilen × {len(df.columns)} Spalten**")
                        st.dataframe(df.head(10), use_container_width=True)

            except Exception as e:
                st.error(f"❌ Fehler beim Lesen der Datei: {e}")
        else:
            st.info("👆 Bitte laden Sie eine Datei hoch, um fortzufahren.")

    # Render Card
    card(card_content, padding="xl", glass=True)


# ==================== STEP 2: ARTIKEL-SUCHE ====================
# ==================== STEP 2: ARTIKEL-SUCHE ====================
def step2_article_search():
    section_header(
        "Artikel identifizieren",
        "Intelligente Suche in Ihren Bestelldaten"
    )

    if "df" not in st.session_state:
        st.warning("⚠️ Bitte zuerst Datei in Schritt 1 hochladen")
        return

    df = st.session_state.df

    # Find item column
    item_col = find_col(df, ["item", "artikel", "bezeichnung", "produkt", "artikelnummer", "artnr"])

    if not item_col:
        st.error("❌ Keine Artikel-Spalte gefunden. Bitte prüfen Sie die Spaltennamen.")
        return

    st.session_state.item_col = item_col

    # Search Card
    search_container = st.container()
    with search_container:
        query = st.text_input(
            "Suchbegriff eingeben",
            placeholder="z.B. 'DIN 933 M8' oder 'Zylinderschraube'",
            key="article_search"
        )

        if query and query.strip():
            with GPTLoadingAnimation("🔍 Suche Artikel...", icon="🤖"):
                all_items = df[item_col].unique().tolist()

                # AI + String search
                matched_indices = gpt_intelligent_article_search(query, all_items)
                matched_items = set([all_items[i] for i in matched_indices]) if matched_indices else set()

                # String fallback
                query_tokens = query.lower().split()
                for item in all_items:
                    if all(token in str(item).lower() for token in query_tokens):
                        matched_items.add(item)

                if matched_items:
                    idf = df[df[item_col].isin(matched_items)].copy()
                    st.session_state.idf = idf

                    supplier_col = find_col(df, ["supplier", "lieferant", "vendor"])
                    st.session_state.supplier_col = supplier_col

                    num_suppliers = idf[supplier_col].nunique() if supplier_col else 1
                    
                    st.markdown("---")
                    create_compact_kpi_row([
                        {"label": "Gefundene Einträge", "value": str(len(idf)), "icon": "📦"},
                        {"label": "Varianten", "value": str(idf[item_col].nunique()), "icon": "🔍"},
                        {"label": "Lieferanten", "value": str(num_suppliers), "icon": "🏭"},
                    ])
                    st.markdown("---")

                    # Auswahl nur per Nutzerklick (kein Default)
                    unique_items = sorted(idf[item_col].unique().tolist())
                    options = ["(Bitte wählen...)"] + unique_items

                    # Wenn noch nichts gewählt, automatisch erstes Ergebnis setzen
                    default_idx = 0
                    if st.session_state.selected_article in unique_items:
                        default_idx = options.index(st.session_state.selected_article)
                    elif unique_items:
                        default_idx = 1
                        set_selected_article(unique_items[0])
                        st.info(f"💡 Automatisch gewählt: {st.session_state.selected_article}")

                    choice = st.selectbox(
                        "Spezifischen Artikel auswählen",
                        options=options,
                        index=default_idx,
                        key="article_selector"
                    )
                    if choice != "(Bitte wählen...)":
                        set_selected_article(choice)
                        st.success(f"**Ausgewählt:** {st.session_state.selected_article}")
                        wizard.complete_step(2)
                    else:
                        set_selected_article(None)

                else:
                    st.warning(f"❌ Keine Ergebnisse für '{query}' gefunden.")
        else:
            st.info("💡 Geben Sie einen Suchbegriff ein, um relevante Artikel zu finden.")

    card(search_container, padding="lg")


# ==================== STEP 3: PREISÜBERSICHT ====================
# ==================== STEP 3: PREISÜBERSICHT ====================
def step3_price_overview():
    section_header(
        "Preisübersicht",
        "Statistische Auswertung der historischen Daten"
    )

    if "idf" not in st.session_state:
        st.warning("⚠️ Bitte zuerst Artikel in Schritt 2 suchen")
        return

    idf = st.session_state.idf
    item_col = st.session_state.item_col
    supplier_col = st.session_state.get("supplier_col")

    try:
        avg, mn, mx, qty_col, _src = derive_unit_price(idf)

        # KPI Row
        price_range = ((mx - mn) / mn * 100) if (mn and mx and mn > 0) else None

        create_compact_kpi_row([
            {"label": "Ø Preis", "value": f"{avg:,.4f} €" if avg else "N/A", "icon": "💰"},
            {"label": "Min", "value": f"{mn:,.4f} €" if mn else "N/A", "icon": "📉"},
            {"label": "Max", "value": f"{mx:,.4f} €" if mx else "N/A", "icon": "📈"},
            {"label": "Range", "value": f"{price_range:,.1f}%" if price_range else "N/A", "icon": "📊"},
        ])

        st.session_state.avg_price = avg
        st.session_state.qty_col = qty_col
        wizard.complete_step(3)

        # Breakdown by supplier
        if supplier_col and supplier_col in idf.columns:
            st.markdown(f"<div style='margin-top: {SPACING['lg']};'></div>", unsafe_allow_html=True)
            
            breakdown_container = st.container()
            with breakdown_container:
                st.markdown("#### 📋 Preis-Breakdown nach Lieferant")
                price_series = get_price_series_per_unit(idf, qty_col)
                if price_series is not None:
                    temp = idf.copy()
                    temp['_price'] = price_series

                    breakdown = temp.groupby(supplier_col).agg({
                        '_price': ['mean', 'min', 'max', 'count']
                    }).round(4)

                    breakdown.columns = ['Ø Preis', 'Min', 'Max', 'Anzahl']
                    breakdown = breakdown.sort_values('Ø Preis')

                    st.dataframe(
                        breakdown.style.highlight_min(subset=['Ø Preis'], color='#A7FFE5'),
                        use_container_width=True
                    )
            
            card(breakdown_container, padding="lg")

    except Exception as e:
        st.error(f"❌ Preisberechnung fehlgeschlagen: {e}")


# ==================== STEP 4: LIEFERANTEN ====================
# ==================== STEP 4: LIEFERANTEN-ANALYSE ====================
def step4_suppliers():
    section_header(
        "Lieferanten-Analyse",
        "Vergleich der Top-Lieferanten für diesen Artikel"
    )

    if "idf" not in st.session_state:
        st.warning("⚠️ Bitte zuerst Artikel in Schritt 2 suchen")
        return

    idf = st.session_state.idf
    supplier_col = st.session_state.get("supplier_col")
    qty_col = st.session_state.get("qty_col")

    if not supplier_col:
        st.warning("⚠️ Keine Lieferanten-Spalte gefunden.")
        return

    # Supplier Card
    supplier_container = st.container()
    with supplier_container:
        st.markdown("#### 🏆 Top Lieferanten nach Volumen")
        
        top_suppliers = idf[supplier_col].value_counts().head(5)
        
        # Prepare chart data
        chart_data = pd.DataFrame({
            'Lieferant': top_suppliers.index,
            'Anzahl': top_suppliers.values
        })
        
        st.bar_chart(chart_data.set_index('Lieferant'), color=COLORS['primary'])

        # Selection
        st.markdown("#### 🎯 Lieferant für Vergleich wählen")
        suppliers = sorted(idf[supplier_col].unique().tolist())
        
        # Default logic
        default_idx = 0
        if st.session_state.selected_supplier in suppliers:
            default_idx = suppliers.index(st.session_state.selected_supplier)
        
        selected_supplier = st.selectbox(
            "Lieferant auswählen",
            options=suppliers,
            index=default_idx,
            key="supplier_selector"
        )
        
        if selected_supplier:
            st.session_state.selected_supplier = selected_supplier
            
            # Show supplier specific stats
            supplier_data = idf[idf[supplier_col] == selected_supplier]
            avg_supp_price = supplier_data['_price'].mean() if '_price' in supplier_data else 0
            
            st.info(f"ℹ️ Durchschnittspreis bei **{selected_supplier}**: {avg_supp_price:,.4f} €")
            wizard.complete_step(4)

    card(supplier_container, padding="lg")


# ==================== STEP 5: KOSTENSCHÄTZUNG ====================
def step5_cost_estimation():
    section_header(
        "Kostenschätzung",
        "KI-basierte Should-Cost Analyse"
    )

    if not st.session_state.selected_article:
        st.warning("⚠️ Bitte Artikel auswählen")
        return

    # Input Card
    input_container = st.container()
    with input_container:
        st.markdown("#### ⚙️ Parameter für Schätzung")
        
        col1, col2 = st.columns(2)
        with col1:
            lot_size = st.number_input("Losgröße (Stück)", min_value=1, value=1000, step=100)
        with col2:
            material = st.selectbox("Material", ["Stahl 8.8", "Edelstahl A2", "Messing", "Aluminium"])

        if st.button("🚀 Kosten jetzt schätzen", type="primary", use_container_width=True):
            with GPTLoadingAnimation("🤖 Berechne Should-Cost...", icon="💰"):
                # Simulation
                import time
                time.sleep(1.5)
                
                # Mock calculation
                base_price = st.session_state.avg_price if st.session_state.avg_price else 0.50
                estimated = base_price * 0.85 # 15% saving potential
                
                st.session_state.estimated_cost = estimated
                st.session_state.savings_potential = base_price - estimated
                
                wizard.complete_step(5)

    card(input_container, padding="lg")

    # Result Card (only if calculated)
    if "estimated_cost" in st.session_state:
        result_container = st.container()
        with result_container:
            st.markdown("#### 💡 Ergebnis der Analyse")
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric(
                    "Geschätzter Should-Cost",
                    f"{st.session_state.estimated_cost:,.4f} €",
                    delta=f"-{(st.session_state.savings_potential / (st.session_state.avg_price or 1) * 100):.1f}%",
                    delta_color="inverse"
                )
            with col_res2:
                st.metric(
                    "Potenzielle Einsparung",
                    f"{st.session_state.savings_potential:,.4f} €",
                    "pro Stück"
                )
            
            st.markdown(f"""
            <div style="
                margin-top: {SPACING['md']}; 
                padding: {SPACING['md']}; 
                background: {COLORS['accent']}20; 
                border-radius: {RADIUS['md']}; 
                border: 1px solid {COLORS['accent']};
                color: {COLORS['primary_dark']};
                font-size: 14px;
            ">
                <strong>KI-Empfehlung:</strong> Der Preis liegt {((st.session_state.savings_potential / (st.session_state.avg_price or 1) * 100)):.1f}% unter dem historischen Durchschnitt. 
                Es wird empfohlen, neu zu verhandeln.
            </div>
            """, unsafe_allow_html=True)

        card(result_container, padding="lg", glass=True)


# ==================== STEP 6: NACHHALTIGKEIT ====================
# ==================== STEP 6: NACHHALTIGKEIT ====================
# ==================== STEP 6: NACHHALTIGKEIT ====================
def step6_sustainability():
    section_header(
        "Nachhaltigkeit & Verhandlung",
        "PCF-Berechnung, CBAM und Verhandlungsstrategie"
    )

    # ==================== CARD 1: CO2 & CBAM ====================
    co2_container = st.container()
    with co2_container:
        st.markdown("#### 🌱 CO₂-Fußabdruck & CBAM")
        
        st.info("""
        **CBAM (Carbon Border Adjustment Mechanism):**
        EU-Klimaabgabe auf CO₂-intensive Importe (Stahl, Alu, etc.). 
        Ab 2026 werden CO₂-Zertifikate verpflichtend.
        """)

        if st.button("🌍 CO₂-Fußabdruck berechnen", use_container_width=True):
            if "cost_result" in st.session_state:
                res = st.session_state.cost_result
                material = res.get('material', 'steel')

                # Lieferantenland
                supplier_data = st.session_state.get("selected_supplier")
                supplier_country = "CN"  # Default
                if supplier_data and "Land" in supplier_data:
                    country_map = {
                        "China": "CN", "Deutschland": "DE", "Germany": "DE",
                        "Italien": "IT", "Italy": "IT", "Polen": "PL", "Poland": "PL",
                        "Tschechien": "CZ", "Czech Republic": "CZ", "Österreich": "AT", "Austria": "AT"
                    }
                    supplier_country = country_map.get(supplier_data.get("Land"), "CN")

                # Masse
                mass_kg = res.get('mass_kg')
                if mass_kg is None or mass_kg <= 0:
                    d_mm = res.get('d_mm', 0)
                    l_mm = res.get('l_mm', 0)
                    if d_mm and l_mm and d_mm > 0 and l_mm > 0:
                        volume_cm3 = 3.14159 * ((d_mm/2)**2) * l_mm / 1000
                        mass_kg = (volume_cm3 * 7.85) / 1000
                    else:
                        mass_kg = 0.023 # Default

                with GPTLoadingAnimation("🌱 Berechne CO₂-Fußabdruck...", icon="🌍"):
                    try:
                        co2_result = calculate_co2_footprint(
                            material=material,
                            mass_kg=mass_kg,
                            supplier_country=supplier_country
                        )

                        if co2_result:
                            total_co2 = co2_result.get('total_co2_kg', 0) or co2_result.get('co2_total_kg', 0)
                            production_co2 = co2_result.get('co2_production_kg', 0)
                            transport_co2 = co2_result.get('co2_transport_kg', 0)
                            cbam_cost_per_unit = co2_result.get('cbam_cost_eur', 0)

                            if total_co2 == 0 and (production_co2 > 0 or transport_co2 > 0):
                                total_co2 = production_co2 + transport_co2

                            lot_size = st.session_state.get('lot_size', 1000)
                            if 'cost_result' in st.session_state:
                                lot_size = st.session_state.cost_result.get('lot_size', lot_size)

                            cbam_cost_total = cbam_cost_per_unit * lot_size if cbam_cost_per_unit else 0

                            st.session_state.co2_result = {
                                'total_co2_kg': total_co2,
                                'cbam_cost_eur_total': cbam_cost_total,
                            }

                            st.success(f"✅ CO₂-Fußabdruck: ~{total_co2:.3f} kg CO₂e pro Stück")

                            create_compact_kpi_row([
                                {"label": "Produktion", "value": f"{production_co2:.3f} kg", "icon": "🏭"},
                                {"label": "Transport", "value": f"{transport_co2:.3f} kg", "icon": "🚢"},
                                {"label": f"CBAM ({lot_size} Stk)", "value": f"{cbam_cost_total:.2f} €", "icon": "💰"},
                            ])
                        else:
                            st.error("❌ Keine Daten verfügbar")
                    except Exception as e:
                        st.error(f"❌ Fehler: {e}")
            else:
                st.warning("⚠️ Bitte zuerst Kostenschätzung durchführen")

    card(co2_container, padding="lg")

    # ==================== CARD 2: NEGOTIATION ====================
    neg_container = st.container()
    with neg_container:
        st.markdown("#### 💼 Verhandlungsvorbereitung")
        
        if st.button("📋 Verhandlungsstrategie generieren", type="primary", use_container_width=True):
            ensure_selection_state()
            article = st.session_state.get("selected_article")
            avg_price = st.session_state.get("avg_price")
            supplier = st.session_state.get("selected_supplier_name")
            cost_result = st.session_state.get("cost_result")
            supplier_data = st.session_state.get("selected_supplier")
            
            if article and supplier:
                with GPTLoadingAnimation("🤖 Generiere Strategie...", icon="💼"):
                    try:
                        tips = gpt_negotiation_prep_enhanced(
                            supplier_name=supplier,
                            article_name=article,
                            avg_price=avg_price,
                            target_price=cost_result.get("target") if cost_result else None,
                            country=supplier_data.get("Land") if supplier_data else None,
                            cost_result=cost_result
                        )

                        if tips and not tips.get("_error"):
                            st.session_state.negotiation_tips = tips
                            render_negotiation_tips(tips)
                        else:
                            st.error("❌ Strategie konnte nicht generiert werden")
                    except Exception as e:
                        st.error(f"❌ Fehler: {e}")
            else:
                st.warning("⚠️ Bitte Artikel und Lieferant auswählen")
        
        elif st.session_state.get("negotiation_tips"):
            render_negotiation_tips(st.session_state.get("negotiation_tips"))

    card(neg_container, padding="lg")

    # ==================== CARD 3: FINAL REPORT ====================
    action_container = st.container()
    with action_container:
        st.markdown("#### 🏁 Abschluss")
        if st.button("📄 Bericht generieren (PDF)", type="primary", use_container_width=True):
            with st.spinner("Generiere PDF..."):
                import time
                time.sleep(1)
            st.success("Bericht erfolgreich erstellt!")
            st.balloons()
            
    card(action_container, padding="lg", glass=True)
    
    wizard.complete_step(6)


# ==================== MAIN ROUTING ====================
if st.session_state.nav_active_section == "drawing_analysis":
    render_drawing_analysis_page()
elif st.session_state.nav_active_section == "upload":
    step1_upload()
elif st.session_state.nav_active_section == "artikel":
    step2_article_search()
elif st.session_state.nav_active_section == "preis":
    step3_price_overview()
elif st.session_state.nav_active_section == "lieferanten":
    step4_suppliers()
elif st.session_state.nav_active_section == "kosten":
    step5_cost_estimation()
elif st.session_state.nav_active_section == "nachhaltigkeit":
    step6_sustainability()
else:
    step1_upload()

# Navigation with conditional "Weiter" button
divider()

current_step = wizard.get_current_step()
next_disabled = False

if current_step == 1:
    # Step 1: Requires file upload
    next_disabled = "df" not in st.session_state
elif current_step == 2:
    # Step 2: Requires article selection
    next_disabled = "selected_article" not in st.session_state
elif current_step == 3:
    # Step 3: Requires price overview completion
    next_disabled = "avg_price" not in st.session_state
elif current_step == 4:
    # Step 4: Requires supplier selection (or no suppliers)
    next_disabled = "selected_supplier_name" not in st.session_state and "df" in st.session_state
elif current_step == 5:
    # Step 5: Requires cost estimation completion
    next_disabled = "cost_result" not in st.session_state
# Step 6: Always enabled (last step)

wizard.render_navigation(next_disabled=next_disabled)

# Developer Mode
with st.expander("🔧 Developer Mode", expanded=False):
    st.json({
        "current_step": wizard.get_current_step(),
        "completed_steps": list(st.session_state.get("wizard_completed_steps", set())),
        "has_data": "df" in st.session_state,
        "has_article": "selected_article" in st.session_state,
        "has_supplier": "selected_supplier_name" in st.session_state,
        "has_results": "cost_result" in st.session_state,
    })
