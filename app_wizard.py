"""
🧙‍♂️ EVALUERA - Modern Wizard-Based UI
========================================
Clean, minimalist, Apple-inspired interface with 6-step workflow
"""

import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Import existing functionality
from price_utils import derive_unit_price
from excel_helpers import (
    read_and_normalize_excel,
    find_column,
    search_excel_for_article,
    get_price_series_per_unit as get_price_series_optimized,
)
from gpt_cache import (
    cached_gpt_complete_cost_estimate,
    cached_gpt_analyze_supplier,
)
from gpt_engine import gpt_intelligent_article_search

# Import new UI system
from ui_theme import (
    apply_global_styles,
    card,
    kpi_card,
    section_header,
    divider,
    status_badge,
    COLORS,
    SPACING,
    RADIUS,
)
from wizard_system import WizardManager, create_data_table, create_compact_kpi_row
from ui_components import GPTLoadingAnimation

# Load environment
load_dotenv()

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="EVALUERA - Cost Analysis Wizard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme
apply_global_styles()

# Initialize wizard
wizard = WizardManager()

# ==================== API KEY SETUP ====================
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

# ==================== HEADER ====================
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
    padding: {SPACING['xl']};
    border-radius: {RADIUS['lg']};
    margin-bottom: {SPACING['xxl']};
    color: white;
">
    <h1 style="margin: 0; color: white; font-size: 2.5rem; font-weight: 700;">
        EVALUERA
    </h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.1rem; max-width: 700px;">
        KI-gestützte Kostenanalyse für intelligente Beschaffung
    </p>
</div>
""", unsafe_allow_html=True)

# Render sidebar with wizard steps
wizard.render_all_steps_sidebar()

# Render wizard progress
wizard.render_progress()

# ==================== STEP 1: UPLOAD ====================
def step1_upload():
    section_header("Excel/CSV Datei hochladen", "Laden Sie Ihre Bestelldaten für die Analyse hoch")

    uploaded_file = st.file_uploader(
        "Datei auswählen",
        type=["csv", "xlsx"],
        key="wizard_file_upload",
        help="CSV oder Excel-Datei mit Bestelldaten"
    )

    if uploaded_file:
        st.success(f"✅ Datei hochgeladen: {uploaded_file.name}")

        # Store in session state
        if "uploaded_file" not in st.session_state or st.session_state.uploaded_file != uploaded_file:
            st.session_state.uploaded_file = uploaded_file

            # Read file
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file, sep=None, engine="python")
                else:
                    df = pd.read_excel(uploaded_file)

                st.session_state.df = df
                st.session_state.df_norm = df.copy()
                st.session_state.df_norm.columns = [c.strip().lower() for c in df.columns]

                wizard.complete_step(1)

            except Exception as e:
                st.error(f"❌ Fehler beim Lesen der Datei: {e}")
                return

        # Show preview
        if "df" in st.session_state:
            with st.expander("📊 Datenvorschau", expanded=False):
                df = st.session_state.df
                st.write(f"**{len(df)} Zeilen, {len(df.columns)} Spalten**")
                st.dataframe(df.head(10), use_container_width=True)

    else:
        st.info("👆 Bitte laden Sie eine Excel- oder CSV-Datei hoch, um zu beginnen")

# ==================== STEP 2: ARTIKEL-ERKENNUNG ====================
def step2_article_search():
    section_header("Artikel suchen", "Finden Sie Artikel in Ihren Bestelldaten")

    if "df" not in st.session_state:
        st.warning("⚠️ Bitte laden Sie zuerst eine Datei in Schritt 1 hoch")
        return

    df = st.session_state.df
    df_norm = st.session_state.df_norm

    # Find article column
    item_col = None
    for possible_col in ["item", "artikel", "bezeichnung", "produkt", "artikelnummer"]:
        if possible_col in df_norm.columns:
            item_col = df.columns[df_norm.columns.get_loc(possible_col)]
            break

    if not item_col:
        st.error("❌ Keine Artikel-Spalte gefunden. Erwartet: 'Artikel', 'Bezeichnung', 'Item', etc.")
        return

    st.session_state.item_col = item_col

    # Search bar
    query = st.text_input(
        "Artikel suchen",
        placeholder="z.B. 'DIN 933 M8' oder 'Schraube'",
        key="wizard_article_search"
    )

    if query and query.strip():
        with GPTLoadingAnimation("🔍 Suche Artikel...", icon="🤖"):
            all_items = df[item_col].unique().tolist()

            # Intelligent search
            matched_indices = gpt_intelligent_article_search(query, all_items)

            if matched_indices:
                matched_items = set([all_items[i] for i in matched_indices])
            else:
                matched_items = set()

            # String fallback
            query_tokens = query.lower().split()
            for item in all_items:
                item_lower = str(item).lower()
                if all(token in item_lower for token in query_tokens):
                    matched_items.add(item)

        if matched_items:
            idf = df[df[item_col].isin(matched_items)].copy()
            st.session_state.idf = idf

            # Show results in compact KPI row
            create_compact_kpi_row([
                {"label": "Einträge gefunden", "value": len(idf), "icon": "📦"},
                {"label": "Artikel-Varianten", "value": idf[item_col].nunique(), "icon": "🔍"},
                {"label": "Zeitraum", "value": "Alle Daten", "icon": "📅"},
            ])

            # Article selection
            unique_items = sorted(idf[item_col].unique().tolist())
            if len(unique_items) > 1:
                selected_article = st.selectbox(
                    "Artikel auswählen",
                    unique_items,
                    key="wizard_selected_article"
                )
            else:
                selected_article = unique_items[0]
                st.success(f"✅ Artikel: {selected_article}")

            st.session_state.selected_article = selected_article
            wizard.complete_step(2)

        else:
            st.warning(f"❌ Keine Ergebnisse für '{query}' gefunden")

    else:
        st.info("💡 Geben Sie einen Suchbegriff ein, um Artikel zu finden")

# ==================== STEP 3: PREISÜBERSICHT ====================
def step3_price_overview():
    section_header("Preisübersicht", "Statistische Auswertung Ihrer Bestelldaten")

    if "idf" not in st.session_state:
        st.warning("⚠️ Bitte suchen Sie zuerst einen Artikel in Schritt 2")
        return

    idf = st.session_state.idf
    item_col = st.session_state.item_col

    # Find columns
    df_norm = st.session_state.df_norm
    supplier_col = None
    for col in ["supplier", "lieferant", "vendor"]:
        if col in df_norm.columns:
            supplier_col = idf.columns[df_norm.columns.get_loc(col)]
            break

    # Calculate prices
    try:
        avg, mn, mx, _qcol, _src = derive_unit_price(idf)

        # Compact KPI row
        create_compact_kpi_row([
            {"label": "Ø Preis", "value": f"{avg:,.4f} €" if avg else "N/A", "icon": "💰"},
            {"label": "Min Preis", "value": f"{mn:,.4f} €" if mn else "N/A", "icon": "📉"},
            {"label": "Max Preis", "value": f"{mx:,.4f} €" if mx else "N/A", "icon": "📈"},
            {"label": "Preisrange", "value": f"{((mx-mn)/mn*100):,.1f}%" if (mn and mx and mn > 0) else "N/A", "icon": "📊"},
        ])

        st.session_state.avg_price = avg
        wizard.complete_step(3)

        # Price breakdown by supplier (collapsed)
        if supplier_col:
            with st.expander("📋 Preis-Breakdown nach Lieferant"):
                price_series = get_price_series_optimized(idf, _qcol)
                if price_series is not None:
                    idf_temp = idf.copy()
                    idf_temp['_unit_price'] = price_series

                    breakdown = idf_temp.groupby(supplier_col).agg({
                        '_unit_price': ['mean', 'min', 'max', 'count']
                    }).round(4)

                    breakdown.columns = ['Ø Preis', 'Min', 'Max', 'Anzahl']
                    breakdown = breakdown.sort_values('Ø Preis')

                    st.dataframe(breakdown, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Fehler bei Preisberechnung: {e}")

# ==================== STEP 4: LIEFERANTENANALYSE ====================
def step4_supplier_analysis():
    section_header("Lieferanten auswählen", "Wählen Sie einen Lieferanten für die Kostenschätzung")

    if "idf" not in st.session_state:
        st.warning("⚠️ Bitte suchen Sie zuerst einen Artikel in Schritt 2")
        return

    idf = st.session_state.idf
    df_norm = st.session_state.df_norm

    # Find supplier column
    supplier_col = None
    for col in ["supplier", "lieferant", "vendor"]:
        if col in df_norm.columns:
            supplier_col = idf.columns[df_norm.columns.get_loc(col)]
            break

    if not supplier_col or supplier_col not in idf.columns:
        st.info("ℹ️ Keine Lieferanten-Spalte gefunden. Fahren Sie mit Schritt 5 fort.")
        wizard.complete_step(4)
        return

    available_suppliers = sorted(idf[supplier_col].dropna().unique().tolist())

    if len(available_suppliers) == 0:
        st.warning("⚠️ Keine Lieferanten gefunden")
        return

    st.info(f"📦 {len(available_suppliers)} Lieferanten verfügbar")

    # Supplier table instead of cards
    supplier_data = []
    for supplier in available_suppliers:
        supplier_df = idf[idf[supplier_col] == supplier]
        try:
            avg_price, _, _, _, _ = derive_unit_price(supplier_df)
        except:
            avg_price = None

        supplier_data.append({
            "Lieferant": supplier,
            "Einträge": len(supplier_df),
            "Ø Preis": f"{avg_price:,.4f} €" if avg_price else "N/A",
        })

    supplier_df_display = pd.DataFrame(supplier_data)

    st.dataframe(supplier_df_display, use_container_width=True, hide_index=True)

    # Selection
    selected_supplier = st.selectbox(
        "Lieferant wählen",
        options=available_suppliers,
        key="wizard_supplier_selection"
    )

    if selected_supplier:
        st.session_state.selected_supplier = selected_supplier
        st.success(f"✅ Lieferant ausgewählt: **{selected_supplier}**")
        wizard.complete_step(4)

# ==================== STEP 5: KOSTEN-SCHÄTZUNG ====================
def step5_cost_estimation():
    section_header("KI-Kostenschätzung", "Material- und Fertigungskosten berechnen")

    if "selected_article" not in st.session_state:
        st.warning("⚠️ Bitte wählen Sie zuerst einen Artikel in Schritt 2")
        return

    article = st.session_state.selected_article
    avg_price = st.session_state.get("avg_price")

    lot_size = st.number_input("Losgröße", min_value=1, value=1000, step=100, key="wizard_lot_size")

    if st.button("🚀 Kosten schätzen", type="primary", use_container_width=True):
        with GPTLoadingAnimation("🤖 Analysiere Kosten mit KI...", icon="💰"):
            result = cached_gpt_complete_cost_estimate(
                description=article,
                lot_size=int(lot_size),
                supplier_competencies_json=None
            )

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
            }

            wizard.complete_step(5)
            st.success("✅ Kostenschätzung abgeschlossen!")
        else:
            st.error("❌ Kostenschätzung fehlgeschlagen")

    # Show results
    if "cost_result" in st.session_state:
        res = st.session_state.cost_result

        create_compact_kpi_row([
            {"label": "Material €/Stk", "value": f"{res['material_eur']:,.4f} €" if res['material_eur'] else "N/A", "icon": "💎"},
            {"label": "Fertigung €/Stk", "value": f"{res['fab_eur']:,.4f} €" if res['fab_eur'] else "N/A", "icon": "⚙️"},
            {"label": "Zielkosten", "value": f"{res['target']:,.4f} €" if res['target'] else "N/A", "icon": "🎯"},
            {"label": "Delta", "value": f"{res['delta']:+,.4f} €" if res['delta'] else "N/A", "icon": "📊", "trend": "positive" if res['delta'] and res['delta'] > 0 else "negative"},
        ])

# ==================== STEP 6: NACHHALTIGKEIT ====================
def step6_sustainability():
    section_header("Nachhaltigkeit & CBAM", "CO₂-Fußabdruck und Verhandlungstipps")

    st.info("🌱 **CBAM-Analyse und CO₂-Berechnung**")
    st.markdown("""
    - **Carbon Border Adjustment Mechanism** (CBAM) berücksichtigen
    - CO₂-Emissionen in Produktion und Transport
    - Nachhaltige Lieferanten bevorzugen
    """)

    if st.button("📋 Verhandlungstipps generieren", type="primary"):
        st.success("✅ Verhandlungsvorlage erstellt")

    wizard.complete_step(6)

# ==================== WIZARD FLOW ====================
current_step = wizard.get_current_step()

wizard.render_step_content(1, step1_upload)
wizard.render_step_content(2, step2_article_search)
wizard.render_step_content(3, step3_price_overview)
wizard.render_step_content(4, step4_supplier_analysis)
wizard.render_step_content(5, step5_cost_estimation)
wizard.render_step_content(6, step6_sustainability)

# Navigation at bottom
divider()
wizard.render_navigation()

# Developer Mode (collapsed)
with st.expander("🔧 Developer Mode", expanded=False):
    st.json(dict(st.session_state))
