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

# Sicherstellen, dass das Projekt-Root und das src-Paket im Python-Pfad liegen
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
for path in (BASE_DIR, SRC_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

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
from src.ui.theme import (
    apply_global_styles,
    section_header,
    divider,
    status_badge,
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

# EVALUERA Theme Override - muss nach set_page_config kommen
st.markdown("""
<style>
/* Primary Button Override - EVALUERA Blaugrau */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"],
button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #6FBFB8 0%, #5DA59F 100%) !important;
    color: #FFFFFF !important;
    border: 2px solid rgba(0,0,0,0.06) !important;
    font-weight: 700 !important;
    letter-spacing: 0.01em;
}
.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span,
.stButton > button[kind="primary"] div,
button[kind="primary"] p,
button[kind="primary"] span,
button[kind="primary"] div {
    color: #FFFFFF !important;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover,
button[kind="primary"]:hover {
    background: linear-gradient(135deg, #5DA59F 0%, #4C8B86 100%) !important;
    box-shadow: 0 6px 16px rgba(0,0,0,0.18) !important;
    border: 2px solid rgba(0,0,0,0.12) !important;
    color: #FFFFFF !important;
}
/* Disabled Button */
.stButton > button[kind="primary"]:disabled,
.stButton > button[data-testid="baseButton-primary"]:disabled {
    background: #E5E7EB !important;
    color: #9CA3AF !important;
    border: 2px solid #D1D5DB !important;
}
</style>
""", unsafe_allow_html=True)

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

# ==================== HEADER - nur neu gestalteter Header ====================
logo_b64 = get_logo_base64()
st.markdown(
    f"""
    <div style="text-align: center; padding: {SPACING['xl']} 0 {SPACING['md']} 0;">
        {"<img src='data:image/png;base64," + logo_b64 + "' alt='EVALUERA' style='height: 80px; object-fit: contain; margin-bottom: 18px;' />" if logo_b64 else "<h1 style='margin-bottom:12px; color:#1F3C45; font-weight:800;'>EVALUERA</h1>"}
        <h1 style="color: {COLORS['primary']}; font-weight: 800; margin: 0 0 10px 0; font-size: 2.6rem;">
            KI-gestützte Bestellanalyse & Kostenschätzung
        </h1>
        
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation - Apple-ähnliche Navigation
nav.render()

# Logout Button
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

# Progress Bar
wizard.render_progress()


# ==================== STEP 1: UPLOAD ====================
def step1_upload():
    section_header(
        "Daten hochladen",
        "Excel- oder CSV-Datei mit Bestelldaten"
    )

    uploaded_file = st.file_uploader(
        "Datei auswählen",
        type=["csv", "xlsx"],
        key="file_upload",
    )

    if uploaded_file:
        st.success(f"✅ Datei: {uploaded_file.name}")

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
                with st.expander("📊 Datenvorschau", expanded=False):
                    st.write(f"**{len(df):,} Zeilen × {len(df.columns)} Spalten**")
                    st.dataframe(df.head(10), use_container_width=True)

        except Exception as e:
            st.error(f"❌ Fehler: {e}")
    else:
        st.info("👆 Bitte Datei hochladen")


# ==================== STEP 2: ARTIKEL-SUCHE ====================
def step2_article_search():
    section_header(
        "Artikel suchen",
        "Intelligente Suche in Ihren Bestelldaten"
    )

    if "df" not in st.session_state:
        st.warning("⚠️ Bitte zuerst Datei in Schritt 1 hochladen")
        return

    df = st.session_state.df

    # Find item column
    item_col = find_col(df, ["item", "artikel", "bezeichnung", "produkt", "artikelnummer", "artnr"])

    if not item_col:
        st.error("❌ Keine Artikel-Spalte gefunden")
        return

    st.session_state.item_col = item_col

    # Search
    query = st.text_input(
        "Suche",
        placeholder="z.B. 'DIN 933 M8'",
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
                create_compact_kpi_row([
                    {"label": "Einträge", "value": str(len(idf)), "icon": "📦"},
                    {"label": "Artikel-Varianten", "value": str(idf[item_col].nunique()), "icon": "🔍"},
                    {"label": "Lieferanten", "value": str(num_suppliers), "icon": "🏭"},
                ])

                # Auswahl nur per Nutzerklick (kein Default)
                unique_items = sorted(idf[item_col].unique().tolist())
                options = ["(Bitte wählen...)"] + unique_items
                choice = st.selectbox(
                    "Artikel wählen",
                    options=options,
                    index=0,
                    key="article_selector"
                )
                if choice != "(Bitte wählen...)":
                    st.session_state.selected_article = choice
                    st.success(f"**Artikel:** {choice}")
                    wizard.complete_step(2)
                else:
                    st.session_state.selected_article = None

            else:
                st.warning(f"❌ Keine Ergebnisse für '{query}'")
    else:
        st.info("💡 Suchbegriff eingeben")


# ==================== STEP 3: PREISÜBERSICHT ====================
def step3_price_overview():
    section_header(
        "Preisübersicht",
        "Statistische Auswertung"
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
            with st.expander("📋 Breakdown nach Lieferant"):
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
                        breakdown.style.highlight_min(subset=['Ø Preis'], color='lightgreen'),
                        use_container_width=True
                    )

    except Exception as e:
        st.error(f"❌ Preisberechnung fehlgeschlagen: {e}")


# ==================== STEP 4: LIEFERANTEN ====================
def step4_suppliers():
    section_header(
        "Lieferant auswählen",
        "Wählen Sie einen Lieferanten für die Kostenschätzung"
    )

    if "idf" not in st.session_state:
        st.warning("⚠️ Bitte zuerst Artikel suchen")
        return

    idf = st.session_state.idf
    supplier_col = st.session_state.get("supplier_col")
    qty_col = st.session_state.get("qty_col")

    if not supplier_col or supplier_col not in idf.columns:
        st.info("ℹ️ Keine Lieferanten-Spalte gefunden")
        wizard.complete_step(4)
        return

    suppliers = sorted(idf[supplier_col].dropna().unique().tolist())

    if len(suppliers) == 0:
        st.warning("⚠️ Keine Lieferanten gefunden")
        return

    st.info(f"📦 **{len(suppliers)} Lieferanten** verfügbar")

    # Build supplier table
    supplier_data = []
    price_series = get_price_series_per_unit(idf, qty_col) if qty_col else None

    for sup in suppliers:
        sup_df = idf[idf[supplier_col] == sup]

        if price_series is not None:
            avg_price = price_series.loc[sup_df.index].mean()
        else:
            try:
                avg_price, _, _, _, _ = derive_unit_price(sup_df)
            except:
                avg_price = None

        supplier_data.append({
            "Lieferant": sup,
            "Einträge": len(sup_df),
            "Ø Preis (€)": f"{avg_price:,.4f}" if avg_price else "N/A",
        })

    df_suppliers = pd.DataFrame(supplier_data)
    st.dataframe(df_suppliers, use_container_width=True, hide_index=True)

    # Selection
    if "selected_supplier_name" not in st.session_state:
        st.session_state.selected_supplier_name = None

    supplier_options = ["(Bitte wählen...)"] + suppliers
    default_idx = 0
    if st.session_state.selected_supplier_name in suppliers:
        default_idx = supplier_options.index(st.session_state.selected_supplier_name)

    selected = st.selectbox(
        "Lieferant wählen",
        options=supplier_options,
        index=default_idx,
        key="supplier_dropdown"
    )

    if selected != "(Bitte wählen...)":
        st.session_state.selected_supplier_name = selected
        st.success(f"✅ **{selected}** ausgewählt")
        wizard.complete_step(4)
    else:
        st.session_state.selected_supplier_name = None


# ==================== STEP 5: KOSTENSCHÄTZUNG ====================
def step5_cost_estimation():
    section_header(
        "KI-Kostenschätzung",
        "Material- und Fertigungskosten"
    )

    if "selected_article" not in st.session_state:
        st.warning("⚠️ Bitte zuerst Artikel auswählen")
        return

    article = st.session_state.selected_article
    avg_price = st.session_state.get("avg_price")
    supplier = st.session_state.get("selected_supplier_name")

    lot_size = st.number_input(
        "Losgröße",
        min_value=1,
        max_value=1_000_000,
        value=1000,
        step=100,
        key="lot_size"
    )

    def _sanitize(text: str) -> str:
        """Entfernt Steuerzeichen wie U+2028/U+2029, behält aber Unicode bei."""
        if not text:
            return ""
        return re.sub(r"[\u2028\u2029]", "", text)

    def _sanitize_obj(obj):
        """Sanitize recursively to remove U+2028/U+2029 from strings inside dict/list."""
        if isinstance(obj, str):
            return _sanitize(obj)
        elif isinstance(obj, list):
            return [_sanitize_obj(v) for v in obj]
        elif isinstance(obj, dict):
            return {k: _sanitize_obj(v) for k, v in obj.items()}
        else:
            return obj

    if st.button("🚀 Kosten schätzen", type="primary", use_container_width=True):
        with GPTLoadingAnimation("🤖 Analysiere mit KI...", icon="💰"):
            # Supplier analysis (if available)
            supplier_competencies = None
            if supplier:
                try:
                    import json
                    idf = st.session_state.idf
                    supplier_col = st.session_state.get("supplier_col")
                    item_col = st.session_state.item_col

                    sup_df = idf[idf[supplier_col] == supplier]
                    article_history = [_sanitize_obj(a) for a in sup_df[item_col].unique().tolist()[:50]]

                    supplier_competencies = cached_gpt_analyze_supplier(
                        supplier_name=supplier,
                        article_history_json=json.dumps(article_history, ensure_ascii=False),
                        country=None
                    )
                except Exception as e:
                    st.warning(f"Lieferanten-Analyse fehlgeschlagen: {e}")

            # Cost estimation
            try:
                article_clean = _sanitize(article)
                supplier_comp_clean = None if not supplier_competencies else _sanitize_obj(supplier_competencies)
                result = cached_gpt_complete_cost_estimate(
                    description=article_clean,
                    lot_size=int(lot_size),
                    supplier_competencies_json=None if not supplier_comp_clean else json.dumps(supplier_comp_clean, ensure_ascii=False)
                )
            except Exception as e:
                st.error(f"❌ Kostenschätzung Exception: {e}")
                st.error(traceback.format_exc())
                st.info(f"Debug info: article='{article_clean}', lot_size={lot_size}, supplier_competencies_present={supplier_comp_clean is not None}")
                return

            if result and not result.get("_error"):
                material_eur = result.get('material_cost_eur')
                fab_eur = result.get('fab_cost_eur')
                target = (material_eur or 0) + (fab_eur or 0)
                delta = (avg_price - target) if avg_price else None

                st.session_state.cost_result = {
                    "material_eur": material_eur,
                    "fab_eur": fab_eur,
                    "target": target,
                    "delta": delta,
                    "material": result.get('material_guess'),
                    "process": result.get('process'),
                    "confidence": result.get('confidence'),
                    "mass_kg": result.get('mass_kg', 0.023),
                }

                wizard.complete_step(5)
                st.success("✅ Schätzung abgeschlossen!")
            else:
                msg = "Unbekannter Fehler"
                if result:
                    msg = result.get("message") or result.get("error") or result.get("_error") or msg
                st.error(f"❌ Schätzung fehlgeschlagen: {msg}")

    # Show results
    if "cost_result" in st.session_state:
        res = st.session_state.cost_result

        # Determine trend: positive delta = paying too much (red), negative delta = saving (green)
        delta_trend = None
        if res['delta'] is not None:
            delta_trend = "negative" if res['delta'] > 0 else "positive"  # negative trend = red = bad, positive trend = green = good

        create_compact_kpi_row([
            {
                "label": "Material €/Stk",
                "value": f"{res['material_eur']:,.4f} €" if res['material_eur'] else "N/A",
                "icon": "💎"
            },
            {
                "label": "Fertigung €/Stk",
                "value": f"{res['fab_eur']:,.4f} €" if res['fab_eur'] else "N/A",
                "icon": "⚙️"
            },
            {
                "label": "Zielkosten (KI-Optimiert)",
                "value": f"{res['target']:,.4f} €" if res['target'] else "N/A",
                "icon": "🎯",
                "help": "Minimal realistisch mögliche Kosten"
            },
            {
                "label": "Delta (Aktuell - Ziel)",
                "value": f"{res['delta']:+,.4f} €" if res['delta'] else "N/A",
                "icon": "📊",
                "trend": delta_trend,
                "help": "Positiv = Einsparungspotenzial, Negativ = unter Zielkosten"
            },
        ])

        # Details
        with st.expander("📋 Details"):
            col1, col2, col3 = st.columns(3)
            col1.metric("Material", res.get('material', 'N/A'))
            col2.metric("Prozess", res.get('process', 'N/A'))
            col3.metric("Confidence", res.get('confidence', 'N/A'))


# ==================== STEP 6: NACHHALTIGKEIT ====================
def step6_sustainability():
    section_header(
        "Nachhaltigkeit & Verhandlung",
        "CBAM, CO₂-Analyse und Verhandlungstipps"
    )

    if "selected_article" not in st.session_state:
        st.warning("⚠️ Bitte zuerst Analyse abschließen")
        return

    # CBAM Info
    st.markdown("### 🌱 CBAM (Carbon Border Adjustment Mechanism)")
    st.info("""
    - EU-Klimaabgabe auf CO₂-intensive Importe
    - Betrifft: Stahl, Aluminium, Zement, Dünger, Wasserstoff
    - Ab 2026: Verpflichtende CO₂-Zertifikate
    """)

    # CO₂ Calculation
    if st.button("🌍 CO₂-Fußabdruck berechnen", use_container_width=True):
        if "cost_result" in st.session_state:
            res = st.session_state.cost_result
            material = res.get('material', 'steel')

            # Lieferantenland
            supplier_data = st.session_state.get("selected_supplier")
            supplier_country = "CN"  # Default
            if supplier_data and "Land" in supplier_data:
                country_map = {
                    "China": "CN",
                    "Deutschland": "DE",
                    "Germany": "DE",
                    "Italien": "IT",
                    "Italy": "IT",
                    "Polen": "PL",
                    "Poland": "PL",
                    "Tschechien": "CZ",
                    "Czech Republic": "CZ",
                    "Österreich": "AT",
                    "Austria": "AT"
                }
                supplier_country = country_map.get(supplier_data.get("Land"), "CN")

            # Masse
            mass_kg = res.get('mass_kg')
            if mass_kg is None or mass_kg <= 0:
                d_mm = res.get('d_mm', 0)
                l_mm = res.get('l_mm', 0)

                if d_mm and l_mm and d_mm > 0 and l_mm > 0:
                    volume_cm3 = 3.14159 * ((d_mm/2)**2) * l_mm / 1000  # mm³ to cm³
                    mass_kg = (volume_cm3 * 7.85) / 1000  # g to kg
                    st.info(f"ℹ️ Masse aus Geometrie berechnet: {mass_kg*1000:.1f}g (Ø{d_mm}mm × {l_mm}mm)")
                else:
                    mass_kg = 0.023  # Default 23g
                    st.warning(f"⚠️ Keine Geometrie - verwende Standard: {mass_kg*1000:.0f}g")

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
                        cbam_cost = co2_result.get('cbam_cost_eur', 0)
                        cbam_cost_per_unit = co2_result.get('cbam_cost_eur', 0)

                        if total_co2 == 0 and (production_co2 > 0 or transport_co2 > 0):
                            total_co2 = production_co2 + transport_co2

                        lot_size = st.session_state.get('lot_size', 1000)
                        if 'cost_result' in st.session_state:
                            lot_size = st.session_state.cost_result.get('lot_size', lot_size)

                        cbam_cost_total = cbam_cost_per_unit * lot_size if cbam_cost_per_unit else 0

                        st.session_state.co2_result = {
                            'total_co2_kg': total_co2,
                            'co2_production_kg': production_co2,
                            'co2_transport_kg': transport_co2,
                            'cbam_cost_eur': cbam_cost,
                            'cbam_cost_eur_per_unit': cbam_cost_per_unit,
                            'cbam_cost_eur_total': cbam_cost_total,
                            'lot_size': lot_size,
                            'material': material,
                            'mass_kg': mass_kg
                        }

                        st.success(f"✅ CO₂-Fußabdruck: ~{total_co2:.3f} kg CO₂e ({mass_kg*1000:.1f}g Masse)")
                        st.success(f"✅ CO₂-Fußabdruck: ~{total_co2:.3f} kg CO₂e pro Stück ({mass_kg*1000:.1f}g Masse)")

                        create_compact_kpi_row([
                            {
                                "label": "Produktion",
                                "value": f"{production_co2:.3f} kg",
                                "icon": "🏭",
                            },
                            {
                                "label": "Transport",
                                "value": f"{transport_co2:.3f} kg",
                                "icon": "🚢",
                            },
                            {
                                "label": f"CBAM 2026 ({lot_size:,} Stk)",
                                "value": f"{cbam_cost_total:.2f} €",
                                "icon": "💰",
                            },
                        ])
                    else:
                        st.error("❌ CO₂-Berechnung fehlgeschlagen: calculate_co2_footprint returned None")
                except Exception as e:
                    st.error(f"❌ CO₂-Berechnung fehlgeschlagen: {e}")

    divider()

    # Negotiation Tips
    st.markdown("### 💼 Verhandlungsvorbereitung")

    if st.button("📋 Verhandlungsstrategie generieren", type="primary", use_container_width=True):
        article = st.session_state.get("selected_article")
        avg_price = st.session_state.get("avg_price")
        supplier = st.session_state.get("selected_supplier_name")
        cost_result = st.session_state.get("cost_result")

        supplier_data = st.session_state.get("selected_supplier")
        supplier_competencies = st.session_state.get("supplier_competencies")
        commodity_analysis = st.session_state.get("commodity_analysis")
        price_stats = st.session_state.get("price_stats", {})

        target_price = None
        if cost_result:
            target_price = cost_result.get("target")

        if article and supplier:
            with GPTLoadingAnimation("🤖 Generiere Strategie...", icon="💼"):
                try:
                    tips = gpt_negotiation_prep_enhanced(
                        supplier_name=supplier,
                        article_name=article,
                        avg_price=avg_price,
                        target_price=target_price,
                        country=supplier_data.get("Land") if supplier_data else None,
                        rating=supplier_data.get("Rating") if supplier_data else None,
                        strengths=supplier_data.get("strengths", []) if supplier_data else None,
                        weaknesses=supplier_data.get("weaknesses", []) if supplier_data else None,
                        total_orders=supplier_data.get("total_orders") if supplier_data else None,
                        supplier_competencies=supplier_competencies,
                        min_price=price_stats.get("min"),
                        max_price=price_stats.get("max"),
                        commodity_analysis=commodity_analysis,
                        cost_result=cost_result
                    )

                    if tips and not tips.get("_error"):
                        st.session_state.negotiation_tips = tips

                        # Minimal Anzeige (Details nach Bedarf erweiterbar)
                        st.json(tips)
                    else:
                        st.error("❌ Verhandlungsstrategie konnte nicht generiert werden")
                except Exception as e:
                    st.error(f"❌ Fehler: {e}")
        else:
            st.warning("⚠️ Bitte Artikel und Lieferant auswählen")

    wizard.complete_step(6)


# ==================== RENDER WIZARD ====================
wizard.render_step_content(1, step1_upload)
wizard.render_step_content(2, step2_article_search)
wizard.render_step_content(3, step3_price_overview)
wizard.render_step_content(4, step4_suppliers)
wizard.render_step_content(5, step5_cost_estimation)
wizard.render_step_content(6, step6_sustainability)

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
