import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from price_utils import derive_unit_price
from cost_helpers import (
    gpt_estimate_material,
    density_g_cm3,
    parse_dims,
    clamp_dims,
    get_material_price_eurkg,
    choose_process_with_gpt,
    calc_fab_cost_per_unit,
    gpt_cost_estimate_unit,
    gpt_rate_supplier,
    gpt_negotiation_prep,
    gpt_analyze_technical_drawing,
    gpt_analyze_pdf_drawing,
    calculate_co2_footprint,
    gpt_analyze_supplier_competencies,
    get_commodity_market_analysis,
    creditreform_login,
    creditreform_get_company_data
)
from gpt_wrappers import safe_gpt_estimate_material, safe_choose_process
from gpt_engine import (
    route_scenarios_with_gpt,
    calc_route_cost_per_unit,
    supplier_scores,
    translate_query_with_gpt,
    apply_json_filter,
    trend_scenarios,
    gpt_intelligent_article_search
)
from ui_components import (
    show_apple_loader,
    show_shimmer_skeleton,
    show_progress_animation,
    show_glass_card,
    show_status_badge,
    show_metric_card,
    show_info_card,
    show_loading_with_steps,
    show_pulse_loader,
    show_divider,
    show_empty_state
)

load_dotenv()

st.set_page_config(
    page_title="EVALUERA – Bestellanalyse & Kostenschätzung",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== HIDE STREAMLIT ELEMENTS ====================
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.css-1dp5vir {padding: 0 !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==================== EVALUERA ULTRA PROFESSIONAL DESIGN SYSTEM ====================
from ultra_professional_styles import ULTRA_PROFESSIONAL_CSS
st.markdown(ULTRA_PROFESSIONAL_CSS, unsafe_allow_html=True)


def _read_file(up):
    """Liest CSV oder Excel-Datei"""
    name = (up.name or "").lower()
    if name.endswith(".csv"):
        return pd.read_csv(up, sep=None, engine="python")
    return pd.read_excel(up)


def _norm_columns(df):
    """Normalisiert Spaltennamen"""
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def _find_col(df, candidates):
    """Findet Spalte basierend auf Kandidaten-Liste"""
    cols = list(df.columns)
    lower_map = {str(c).lower(): c for c in cols}
    for cand in candidates:
        c = cand.lower()
        if c in lower_map:
            return lower_map[c]
        for k, v in lower_map.items():
            if c in k:
                return v
    return None


def get_price_series_per_unit(df, qty_col):
    """
    Berechnet Preisserie pro Einheit.
    Fallback zu derive_unit_price wenn keine direkte Spalte vorhanden.
    """
    price_col = _find_col(df, [
        "unit_price", "einzelpreis", "stkpreis", "preis_pro_stk",
        "price", "preis", "avg_price"
    ])

    if price_col is not None:
        return pd.to_numeric(df[price_col], errors="coerce")

    # Fallback: Berechnung aus Total/Qty
    total_col = _find_col(df, [
        "rechnungsnettowert", "nettowert", "netto", "betrag",
        "invoice_amount", "amount", "total"
    ])

    if total_col is not None and qty_col is not None:
        total = pd.to_numeric(df[total_col], errors="coerce")
        qty = pd.to_numeric(df[qty_col], errors="coerce").replace(0, pd.NA)
        return total / qty

    return None


def _show_gpt_error(obj, label):
    """Zeigt GPT-Fehler falls vorhanden"""
    try:
        if not isinstance(obj, dict):
            return

        err = obj.get('error')
        err_type = obj.get('_error_type')
        err_trace = obj.get('error_trace')

        if err:
            st.error(f'❌ **{label} – Fehler:**\n\n{err}')

            if err_type:
                st.caption(f"Fehlertyp: `{err_type}`")

            # Zeige detaillierte Traceback in Expander
            if err_trace:
                with st.expander("🔍 Detaillierte Fehlerinfo (für Debugging)", expanded=False):
                    st.code(err_trace, language="python")

            # Hilfreiche Tipps basierend auf Fehlertyp
            if "401" in str(err) or "Unauthorized" in str(err):
                st.warning("""
                **💡 Lösungsvorschläge für 401-Fehler:**
                1. Prüfe ob der OpenAI API-Key in der .env Datei korrekt ist
                2. Prüfe ob der API-Key Zugriff auf GPT-4o hat
                3. Versuche den Key neu zu generieren
                4. Prüfe dein OpenAI Account-Status und Billing
                5. Stelle sicher, dass Credits/Budget verfügbar sind
                """)
            elif "429" in str(err):
                st.warning("⚠️ Rate Limit erreicht. Warte kurz und versuche es erneut.")
            elif "500" in str(err) or "503" in str(err):
                st.warning("⚠️ OpenAI Server-Problem. Versuche es in ein paar Minuten erneut.")

    except Exception:
        pass


def _run_cost_estimate(sel_text, lot_size, avg_purchase, idf=None, supplier_col=None, item_col=None, selected_supplier=None):
    """
    Führt vollständige Kostenschätzung durch:
    - Material (GPT + TradingEconomics)
    - Lieferanten-Kompetenzen-Analyse (NEU!)
    - Fertigung (GPT - direkt geschätzt, MIT Lieferanten-Kontext!)
    - Vergleich mit Einkaufspreis

    Args:
        selected_supplier: Optional - Spezifischer Lieferant für die Analyse (wenn gewählt)
    """
    try:
        # === LIEFERANTEN-KOMPETENZEN ANALYSIEREN (SEHR WICHTIG!) ===
        supplier_competencies = None
        supplier_name = None
        article_history = []

        if idf is not None and not idf.empty and supplier_col and supplier_col in idf.columns:
            # Verwende gewählten Lieferanten wenn vorhanden, sonst häufigsten
            if selected_supplier and selected_supplier != "":
                supplier_name = selected_supplier
                print(f"\n🏭 Verwende GEWÄHLTEN Lieferanten: {supplier_name}")
            else:
                # Ermittle Haupt-Lieferanten (häufigster Lieferant für diesen Artikel)
                supplier_counts = idf[supplier_col].value_counts()
                if not supplier_counts.empty:
                    supplier_name = supplier_counts.index[0]
                    print(f"\n🏭 Verwende häufigsten Lieferanten: {supplier_name}")

            # Sammle Artikel-Historie dieses Lieferanten
            supplier_df = idf[idf[supplier_col] == supplier_name] if supplier_name else idf
            if item_col and item_col in supplier_df.columns:
                article_history = supplier_df[item_col].unique().tolist()[:50]

            # Führe Kompetenzen-Analyse durch (für bessere Kostenschätzung)
            if supplier_name:
                print(f"\n🔍 Analysiere Produktionskompetenzen von: {supplier_name}")
                country = None
                if 'country' in idf.columns:
                    countries = idf[idf[supplier_col] == supplier_name]['country'].dropna().unique()
                    if len(countries) > 0:
                        country = countries[0]

                supplier_competencies = gpt_analyze_supplier_competencies(
                    supplier_name=supplier_name,
                    article_history=article_history,
                    country=country
                )

                if supplier_competencies and not supplier_competencies.get('_error'):
                    print(f"✅ Kompetenzen-Analyse abgeschlossen!")
                    core_comps = supplier_competencies.get('core_competencies', [])
                    if core_comps:
                        print(f"   → Hauptkompetenzen: {[c.get('process') for c in core_comps[:3]]}")
                else:
                    print(f"⚠️ Kompetenzen-Analyse fehlgeschlagen oder keine Daten")

        # === MATERIAL-SCHÄTZUNG (GPT) ===
        print(f"\n🔍 Starte Material-Schätzung für: '{sel_text}'")
        g = safe_gpt_estimate_material(sel_text)
        _show_gpt_error(g, 'Material-Schätzung')

        mat = g.get('material_guess', 'stahl')
        mass_kg = g.get('mass_kg')  # Direkt von GPT!
        d_mm = g.get('d_mm')
        l_mm = g.get('l_mm')
        confidence = g.get('confidence', 'unknown')

        print(f"   → Material: {mat}, Masse: {mass_kg}, d_mm: {d_mm}, l_mm: {l_mm}, Confidence: {confidence}")

        # Fallback: Dimensionen aus Text parsen falls GPT keine liefert
        if not d_mm or not l_mm:
            d_parsed, l_parsed = parse_dims(sel_text)
            d_mm = d_mm or d_parsed
            l_mm = l_mm or l_parsed
            if d_mm and l_mm:
                d_mm, l_mm = clamp_dims(d_mm, l_mm)
                print(f"   → Dimensionen aus Text geparst: d={d_mm}, l={l_mm}")

        # === MATERIALKOSTEN BERECHNEN ===
        # Priorisiere GPT's eigene Materialkosten-Berechnung
        material_eur = g.get('material_cost_eur')
        eur_per_kg = g.get('material_price_eur_kg')

        print(f"   → GPT material_cost_eur: {material_eur}, material_price_eur_kg: {eur_per_kg}")

        # Fallback: Berechne selbst
        if material_eur is None:
            # Prüfe ob GPT einen Materialpreis geschätzt hat
            if not eur_per_kg:
                # Fallback auf TradingEconomics
                eur_per_kg = get_material_price_eurkg(mat)
                print(f"   → TradingEconomics Materialpreis: {eur_per_kg} €/kg")

            if mass_kg is not None and eur_per_kg is not None:
                material_eur = mass_kg * eur_per_kg
                print(f"   → Berechnet: material_eur = {mass_kg} kg * {eur_per_kg} €/kg = {material_eur} €")
            else:
                # NEUER FALLBACK: Schätze Masse aus Dimensionen
                if d_mm and l_mm and material_eur is None:
                    # Zylinder-Volumen: V = π * r² * h
                    radius_mm = d_mm / 2.0
                    volume_mm3 = 3.14159 * (radius_mm ** 2) * l_mm
                    volume_cm3 = volume_mm3 / 1000.0

                    # Dichte schätzen
                    density = density_g_cm3(mat)
                    mass_g = volume_cm3 * density
                    mass_kg = mass_g / 1000.0

                    if eur_per_kg:
                        material_eur = mass_kg * eur_per_kg
                        print(f"   → FALLBACK Masse-Schätzung aus Geometrie: {mass_kg:.6f} kg → {material_eur:.4f} €")
                    else:
                        print(f"   ⚠️ Masse geschätzt ({mass_kg:.6f} kg) aber kein Materialpreis verfügbar")
                else:
                    print(f"   ⚠️ WARNUNG: Kann Materialkosten nicht berechnen (mass_kg={mass_kg}, eur_per_kg={eur_per_kg}, d_mm={d_mm}, l_mm={l_mm})")
        else:
            # Wenn GPT material_cost_eur direkt geliefert hat, verwende es!
            print(f"   ✅ GPT hat material_cost_eur direkt geliefert: {material_eur} €")

        # === FERTIGUNGSKOSTEN (GPT - DIREKT GESCHÄTZT, MIT LIEFERANTEN-KOMPETENZEN!) ===
        # Übergebe ALLE verfügbaren Infos für bessere Schätzung!
        print(f"\n💰 Starte Fertigungskosten-Schätzung {'MIT Lieferanten-Kompetenzen' if supplier_competencies else 'OHNE Lieferanten-Daten'}...")
        fab_result = gpt_cost_estimate_unit(
            sel_text,
            int(lot_size),
            material=mat,
            d_mm=d_mm,
            l_mm=l_mm,
            mass_kg=mass_kg,
            supplier_competencies=supplier_competencies  # NEU: Lieferanten-Kontext!
        )
        fab_eur = fab_result.get('fab_cost_eur_per_unit')
        process = fab_result.get('likely_process', 'unknown')
        part_class = fab_result.get('part_class', 'unknown')
        assumptions = fab_result.get('assumptions', [])

        # === GESAMT-SOLL-KOSTEN ===
        target = (material_eur or 0.0) + (fab_eur or 0.0)

        # === DELTA ZU EINKAUFSPREIS ===
        delta = (avg_purchase - target) if avg_purchase is not None else None

        return {
            'ok': True,
            'material_eur': material_eur,
            'eur_per_kg': eur_per_kg,
            'mass_kg': mass_kg,
            'fab_eur': fab_eur,
            'target': target,
            'delta': delta,
            'mat': mat,
            'd_mm': d_mm,
            'l_mm': l_mm,
            'process': process,
            'part_class': part_class,
            'confidence': confidence,
            'assumptions': assumptions,
            'gpt_material_raw': g,
            'gpt_fab_raw': fab_result,
            'supplier_competencies': supplier_competencies,  # NEU!
            'supplier_name': supplier_name  # NEU!
        }
    except Exception as e:
        import traceback
        return {'ok': False, 'error': str(e), 'trace': traceback.format_exc()}


# ==================== HAUPTANWENDUNG ====================

# Header mit Beschreibung und Theme Toggle
col_title, col_theme = st.columns([6, 1])

with col_title:
    st.title("EVALUERA")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h3 style='margin: 0; color: white;'>KI-gestützte Bestellanalyse & Kostenschätzung</h3>
        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
            Analysieren Sie Ihre Beschaffungsdaten, schätzen Sie Material- und Fertigungskosten mit KI,
            bewerten Sie Lieferanten und optimieren Sie Ihre Einkaufsstrategie.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_theme:
    st.markdown("<br>", unsafe_allow_html=True)
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    theme_label = "🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"
    if st.button(theme_label, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Theme CSS anwenden
if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .main { background-color: #1a1a2e !important; color: #eaeaea !important; }
        h1, h2, h3, h4, h5, h6 { color: #eaeaea !important; }
        .stAlert { background-color: #16213e !important; color: #eaeaea !important; }
        [data-testid="stMetricValue"] { color: #60a5fa !important; }
        .stButton > button { background-color: #2563eb !important; }
        [data-testid="stFileUploader"] { background-color: #16213e !important; border-color: #2563eb !important; }
        .stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {
            background-color: #16213e !important; color: #eaeaea !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Datei-Upload mit Tabs
upload_tab1, upload_tab2, upload_tab3 = st.tabs([
    "📊 Excel/CSV Bestelldaten",
    "📐 Technische Zeichnung",
    "🎯 3D-Modell (STEP/STL)"
])

df = pd.DataFrame()
drawing_data = None
cad_3d_data = None

with upload_tab1:
    up = st.file_uploader("CSV oder Excel (xlsx) hochladen", type=["csv", "xlsx"], key="excel_upload")

with upload_tab2:
    drawing_up = st.file_uploader(
        "Technische Zeichnung (PDF, PNG, JPG) hochladen",
        type=["pdf", "png", "jpg", "jpeg"],
        key="drawing_upload",
        help="KI analysiert die Zeichnung und extrahiert Artikelinfo, Maße, Material, Stückliste"
    )

    # Zusätzlich: Excel-Upload für technische Zeichnungen
    drawing_excel_up = st.file_uploader(
        "📊 Optional: Excel mit Bestellhistorie hochladen",
        type=["xlsx", "csv"],
        key="drawing_excel_upload",
        help="🤖 KI durchsucht automatisch nach erkannten Artikeln und zeigt historische Preise! Spart Zeit und liefert Benchmarks für Verhandlungen."
    )

with upload_tab3:
    st.markdown("### 🎯 3D-Datei Upload (STEP, STL, IGES)")
    st.info("""
    **Unterstützte Formate:**
    - **STEP (.step, .stp)**: ISO 10303 Standard für 3D-CAD-Daten
    - **STL (.stl)**: STereoLithography Format (für 3D-Druck)
    - **IGES (.iges, .igs)**: Initial Graphics Exchange Specification

    **Funktion:**
    - Automatische Geometrie-Extraktion (Volumen, Oberfläche, Bounding Box)
    - Masse-Schätzung basierend auf Material
    - Komplexitäts-Analyse für Fertigungsprozess-Auswahl
    """)

    cad_3d_up = st.file_uploader(
        "3D-Datei hochladen",
        type=["step", "stp", "stl", "iges", "igs"],
        key="cad_3d_upload",
        help="KI analysiert die 3D-Geometrie und schätzt Fertigungskosten"
    )

    # Zusätzlich: Excel-Upload für 3D-Dateien
    cad_3d_excel_up = st.file_uploader(
        "📊 Optional: Excel mit Bestellhistorie hochladen",
        type=["xlsx", "csv"],
        key="cad_3d_excel_upload",
        help="🤖 KI durchsucht automatisch nach 3D-Modell-Namen und zeigt historische Preise! Ideal für wiederkehrende Teile."
    )

    if cad_3d_up is not None:
        st.success(f"✅ 3D-Datei hochgeladen: {cad_3d_up.name}")

        # Placeholder für 3D-Datei-Analyse
        # In Produktion: Hier würde eine 3D-Geometrie-Analyse mit Open3D, trimesh oder FreeCAD erfolgen
        with st.spinner("🤖 Analysiere 3D-Geometrie..."):
            file_bytes = cad_3d_up.read()
            file_size_mb = len(file_bytes) / (1024 * 1024)

            st.info(f"""
            **📊 Datei-Info:**
            - Format: {cad_3d_up.name.split('.')[-1].upper()}
            - Größe: {file_size_mb:.2f} MB

            **⚠️ Hinweis:** Vollständige 3D-Geometrie-Analyse erfordert zusätzliche Bibliotheken (Open3D, trimesh, pythonocc-core).

            **Aktuelle Funktionalität:** Sie können trotzdem eine Kostenschätzung durchführen, indem Sie den Dateinamen eingeben.
            KI wird versuchen, aus dem Dateinamen Informationen zu extrahieren.
            """)

            # Placeholder-Daten für Demo
            cad_3d_data = {
                "ok": True,
                "filename": cad_3d_up.name,
                "format": cad_3d_up.name.split('.')[-1].upper(),
                "file_size_mb": file_size_mb,
                "geometry": {
                    "volume_mm3": None,  # Würde aus 3D-Analyse kommen
                    "surface_area_mm2": None,
                    "bounding_box_mm": {"x": None, "y": None, "z": None},
                    "complexity": "medium"  # simple|medium|complex
                },
                "message": "3D-Geometrie-Analyse eingeschränkt. Kostenschätzung basiert auf Dateinamen und manuellen Eingaben."
            }

        # === KOSTENSCHÄTZUNGS-BUTTON FÜR 3D-MODELL ===
        st.markdown("---")
        st.markdown("### 💰 Kostenschätzung für 3D-Modell")
        st.info("💡 **Automatische Erkennung:** KI analysiert den Dateinamen automatisch. Optional können Sie Details anpassen für präzisere Ergebnisse.")

        # Automatische Beschreibung aus Dateinamen
        auto_description = cad_3d_up.name.replace('.step', '').replace('.stp', '').replace('.stl', '').replace('.iges', '').replace('.igs', '').replace('_', ' ').replace('-', ' ')

        # Optional: Erweiterte Eingaben
        show_advanced = st.checkbox(
            "🔧 Erweitert: Details anpassen",
            value=False,
            key="show_3d_advanced",
            help="Standardmäßig nutzt KI den Dateinamen. Aktivieren um Beschreibung und Material manuell anzupassen."
        )

        if show_advanced:
            col1, col2 = st.columns(2)
            with col1:
                cad_3d_description = st.text_input(
                    "Artikelbezeichnung / Beschreibung",
                    value=auto_description,
                    key="cad_3d_desc",
                    help="Z.B. 'DIN 933 M8x30' oder 'Flansch Ø100 x 20mm'"
                )
                cad_3d_material = st.text_input(
                    "Material (optional)",
                    value="",
                    key="cad_3d_mat",
                    placeholder="Z.B. 'Stahl', 'Aluminium', 'Kunststoff'",
                    help="Leer lassen, damit KI aus Beschreibung schätzt"
                )

            with col2:
                cad_3d_lot_size = st.number_input(
                    "Losgröße",
                    min_value=1,
                    max_value=1_000_000,
                    value=1000,
                    step=100,
                    key="cad_3d_lot_size"
                )
        else:
            # Automatischer Modus
            cad_3d_description = auto_description
            cad_3d_material = ""
            st.caption(f"🤖 Automatisch erkannt: **{cad_3d_description}**")
            cad_3d_lot_size = st.number_input(
                "Losgröße",
                min_value=1,
                max_value=1_000_000,
                value=1000,
                step=100,
                key="cad_3d_lot_size_simple"
            )

        if st.button("🚀 Kosten für 3D-Modell schätzen", type="primary", use_container_width=True, key="cad_3d_cost_btn"):
            # Baue Beschreibung für Kostenanalyse
            full_description = cad_3d_description
            if cad_3d_material:
                full_description += f" Material: {cad_3d_material}"
            full_description += f" (aus 3D-Datei: {cad_3d_up.name})"

            # === NEU: Excel-Durchsuchung für 3D-Modell ===
            cad_3d_excel_df = None
            cad_3d_excel_matches = None
            cad_3d_avg_price = None

            if cad_3d_excel_up is not None:
                try:
                    with st.spinner("🔍 Durchsuche Excel nach 3D-Modell (KI-gestützt)..."):
                        cad_3d_excel_df = _read_file(cad_3d_excel_up)
                        cad_3d_excel_df = _norm_columns(cad_3d_excel_df)

                        # Finde Artikel-Spalte
                        cad_3d_item_col = _find_col(cad_3d_excel_df, ["item", "artikel", "bezeichnung", "produkt"])

                        if cad_3d_item_col:
                            # INTELLIGENT: GPT-basierte Suche
                            item_values = cad_3d_excel_df[cad_3d_item_col].tolist()
                            matching_indices = gpt_intelligent_article_search(cad_3d_description, item_values)

                            if matching_indices:
                                # Nutze GPT-Ergebnisse
                                cad_3d_excel_matches = cad_3d_excel_df.iloc[matching_indices].copy()
                            else:
                                # Fallback: Einfache String-Suche
                                search_mask = cad_3d_excel_df[cad_3d_item_col].astype(str).str.lower().str.contains(
                                    cad_3d_description.lower(), na=False
                                )
                                cad_3d_excel_matches = cad_3d_excel_df[search_mask].copy()

                            if not cad_3d_excel_matches.empty:
                                st.success(f"✅ **{len(cad_3d_excel_matches)} historische Bestellung(en) für 3D-Modell gefunden!**")

                                # Berechne Durchschnittspreis
                                cad_3d_qty_col = _find_col(cad_3d_excel_matches, ["quantity", "menge", "qty"])
                                cad_3d_avg_price, cad_3d_mn, cad_3d_mx, _, _ = derive_unit_price(cad_3d_excel_matches)

                                if cad_3d_avg_price:
                                    c1, c2, c3 = st.columns(3)
                                    c1.metric("📊 Historischer Ø Preis", f"{cad_3d_avg_price:,.4f} €")
                                    if cad_3d_mn:
                                        c2.metric("Min-Preis", f"{cad_3d_mn:,.4f} €")
                                    if cad_3d_mx:
                                        c3.metric("Max-Preis", f"{cad_3d_mx:,.4f} €")

                                # Zeige Details
                                with st.expander("📋 Historische Bestellungen", expanded=False):
                                    display_cols = [c for c in cad_3d_excel_matches.columns if c in ["item", "supplier", "quantity", "unit_price", "date"]]
                                    if display_cols:
                                        st.dataframe(cad_3d_excel_matches[display_cols], use_container_width=True)
                                    else:
                                        st.dataframe(cad_3d_excel_matches, use_container_width=True)
                            else:
                                st.info(f"ℹ️ 3D-Modell '**{cad_3d_description}**' nicht in Bestellhistorie gefunden. Führe KI-Schätzung durch...")
                        else:
                            st.warning("⚠️ Artikel-Spalte in Excel nicht gefunden")
                except Exception as e:
                    st.warning(f"⚠️ Excel-Durchsuchung fehlgeschlagen: {e}")

            with st.spinner("🤖 Analysiere 3D-Modell und schätze Kosten..."):
                st.session_state.cad_3d_est_result = _run_cost_estimate(full_description, int(cad_3d_lot_size), cad_3d_avg_price)

        # Ergebnis anzeigen
        if "cad_3d_est_result" in st.session_state and st.session_state.cad_3d_est_result:
            res = st.session_state.cad_3d_est_result

            if not res.get("ok"):
                st.error(f"❌ Schätzung fehlgeschlagen: {res.get('error', 'unbekannter Fehler')}")
                with st.expander("🔍 Debug-Info"):
                    st.json(res)
            else:
                st.success("✅ Kostenschätzung abgeschlossen!")

                # Metriken
                c1, c2, c3 = st.columns(3)
                material_eur = res.get("material_eur")
                fab_eur = res.get("fab_eur")
                target = res.get("target")

                c1.metric("💎 Material €/Stk", f"{material_eur:,.4f} €" if material_eur is not None else "N/A")
                c2.metric("⚙️ Fertigung €/Stk", f"{fab_eur:,.4f} €" if fab_eur is not None else "N/A")
                c3.metric("🎯 Soll-Kosten €/Stk", f"{target:,.4f} €" if target is not None else "N/A")

                if material_eur is None:
                    st.warning("⚠️ **Materialkosten konnten nicht berechnet werden.** Mögliche Gründe: Dateiname zu generisch, keine Dimensionen erkennbar. Prüfen Sie die Konsole für Details oder geben Sie eine präzisere Beschreibung ein.")

                st.info("ℹ️ **Hinweis**: KI-Schätzung basiert auf Dateinamen und eingegebener Beschreibung. Für präzisere Ergebnisse verwenden Sie technische Zeichnungen (Tab 2) oder geben Sie Details manuell ein (🔧 Erweitert aktivieren).")

                # Details
                with st.expander("📋 Technische Details", expanded=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"• Material: **{res.get('mat', 'unknown')}**")
                        if res.get('d_mm'):
                            st.write(f"• Durchmesser: **{res.get('d_mm'):.1f} mm**")
                        if res.get('l_mm'):
                            st.write(f"• Länge: **{res.get('l_mm'):.1f} mm**")
                    with col2:
                        if res.get('mass_kg'):
                            st.write(f"• Masse: **{res.get('mass_kg')*1000:.1f} g**")
                        st.write(f"• Prozess: **{res.get('process', 'unknown')}**")
                        conf = res.get('confidence', 'unknown')
                        conf_emoji = "🟢" if conf == "high" else "🟡" if conf == "medium" else "🔴"
                        st.write(f"• Vertrauen: {conf_emoji} **{conf}**")

                # Annahmen
                assumptions = res.get("assumptions", [])
                if assumptions:
                    with st.expander("🤖 GPT-Annahmen & Begründung", expanded=False):
                        for i, assumption in enumerate(assumptions, 1):
                            st.write(f"{i}. {assumption}")

                with st.expander("🔍 Debug: Rohe GPT-Ausgaben", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Material-Schätzung:**")
                        st.json(res.get("gpt_material_raw"))
                    with col2:
                        st.write("**Fertigungs-Schätzung:**")
                        st.json(res.get("gpt_fab_raw"))

    if drawing_up is not None:
        with st.spinner("🤖 KI analysiert technische Zeichnung..."):
            drawing_bytes = drawing_up.read()

            # PDF oder Bild?
            if drawing_up.name.lower().endswith('.pdf'):
                drawing_data = gpt_analyze_pdf_drawing(drawing_bytes)
            else:
                drawing_data = gpt_analyze_technical_drawing(drawing_bytes, drawing_up.name)

            if drawing_data.get("ok"):
                st.success(f"✅ {drawing_data.get('total_items', 0)} Artikel erkannt!")

                # Zeichnungsinfo
                col1, col2, col3 = st.columns(3)
                if drawing_data.get("drawing_number"):
                    col1.metric("Zeichnungs-Nr.", drawing_data["drawing_number"])
                if drawing_data.get("revision"):
                    col2.metric("Revision", drawing_data["revision"])
                if drawing_data.get("confidence"):
                    conf = drawing_data["confidence"]
                    conf_emoji = "🟢" if conf == "high" else "🟡" if conf == "medium" else "🔴"
                    col3.metric("Vertrauen", f"{conf_emoji} {conf}")

                # Artikel-Liste
                items = drawing_data.get("items", [])
                if items:
                    st.subheader("Extrahierte Artikel")
                    for item in items:
                        with st.expander(f"Pos. {item.get('position', '?')} – {item.get('description', 'Unbekannt')}", expanded=False):
                            c1, c2, c3, c4 = st.columns(4)
                            if item.get("quantity"):
                                c1.write(f"**Menge:** {item['quantity']}")
                            if item.get("material"):
                                c2.write(f"**Material:** {item['material']}")
                            if item.get("diameter_mm"):
                                c3.write(f"**Ø:** {item['diameter_mm']} mm")
                            if item.get("length_mm"):
                                c4.write(f"**L:** {item['length_mm']} mm")
                            if item.get("surface_treatment"):
                                st.write(f"**Oberflächenbehandlung:** {item['surface_treatment']}")

                # Notizen
                if drawing_data.get("notes"):
                    with st.expander("📝 Notizen", expanded=False):
                        for note in drawing_data["notes"]:
                            st.write(f"- {note}")

                # Konvertiere in DataFrame für weitere Analyse
                if items:
                    df_items = []
                    for item in items:
                        df_items.append({
                            "item": item.get("description", ""),
                            "quantity": item.get("quantity", 1),
                            "material": item.get("material", ""),
                            "diameter_mm": item.get("diameter_mm"),
                            "length_mm": item.get("length_mm")
                        })
                    df = pd.DataFrame(df_items)
                    st.info("💡 Artikel werden automatisch für Analyse geladen")

                    # === DIREKTER KOSTENSCHÄTZUNGS-BUTTON FÜR CAD ===
                    st.markdown("---")
                    st.markdown("### 💰 Kostenschätzung für CAD-Artikel")

                    st.info("💡 **Automatische Artikel-Erkennung:** KI analysiert die Zeichnung und schätzt Kosten direkt - keine manuelle Artikel-Auswahl nötig!")

                    # Optional: Artikel-Auswahl für erweiterte Analyse
                    show_article_selection = st.checkbox(
                        "🔧 Erweitert: Spezifischen Artikel auswählen",
                        value=False,
                        key="show_cad_article_select",
                        help="Standardmäßig analysiert KI automatisch. Aktiviere diese Option um einen spezifischen Artikel auszuwählen."
                    )

                    selected_cad_item = None
                    if show_article_selection:
                        cad_items_list = [f"Pos. {item.get('position', '?')} - {item.get('description', 'Unbekannt')}" for item in items]
                        selected_cad_idx = st.selectbox(
                            "Artikel wählen",
                            range(len(items)),
                            format_func=lambda i: cad_items_list[i],
                            key="cad_cost_select"
                        )
                        selected_cad_item = items[selected_cad_idx]
                    else:
                        # Automatisch: Nimm den ersten Artikel oder den mit der höchsten Konfidenz
                        if items:
                            # Sortiere nach Komplexität/Wichtigkeit (z.B. Position 1 zuerst)
                            selected_cad_item = items[0]
                            st.caption(f"🤖 Automatisch gewählt: **Pos. {selected_cad_item.get('position', '?')} - {selected_cad_item.get('description', 'Unbekannt')}**")

                    cad_lot_size = st.number_input("Losgröße", min_value=1, max_value=1_000_000, value=1000, step=100, key="cad_lot_size")

                    if st.button("🚀 Kosten für CAD-Artikel schätzen", type="primary", use_container_width=True):
                        # Wenn kein Artikel gewählt, verwende Zeichnungs-Beschreibung
                        if not selected_cad_item:
                            # Versuche generische Beschreibung aus Zeichnung zu generieren
                            cad_description = drawing_data.get("drawing_number", "") or "Technische Zeichnung Artikel"
                            if drawing_data.get("notes"):
                                cad_description += " - " + " ".join(drawing_data["notes"][:2])  # Erste 2 Notizen
                            st.info(f"ℹ️ Keine Artikeldetails erkennbar. GPT analysiert basierend auf: **{cad_description}**")
                        else:
                            cad_description = selected_cad_item.get('description', '')

                        # === NEU: Excel-Durchsuchung für CAD-Artikel ===
                        cad_excel_df = None
                        cad_excel_matches = None
                        cad_avg_price = None

                        if drawing_excel_up is not None:
                            try:
                                with st.spinner("🔍 Durchsuche Excel nach erkanntem Artikel (KI-gestützt)..."):
                                    cad_excel_df = _read_file(drawing_excel_up)
                                    cad_excel_df = _norm_columns(cad_excel_df)

                                    # Finde Artikel-Spalte
                                    cad_item_col = _find_col(cad_excel_df, ["item", "artikel", "bezeichnung", "produkt"])

                                    if cad_item_col:
                                        # INTELLIGENT: GPT-basierte Suche (erkennt Varianten, Reihenfolge, Synonyme)
                                        item_values = cad_excel_df[cad_item_col].tolist()
                                        matching_indices = gpt_intelligent_article_search(cad_description, item_values)

                                        if matching_indices:
                                            # Nutze GPT-Ergebnisse
                                            cad_excel_matches = cad_excel_df.iloc[matching_indices].copy()
                                        else:
                                            # Fallback: Einfache String-Suche
                                            search_mask = cad_excel_df[cad_item_col].astype(str).str.lower().str.contains(
                                                cad_description.lower(), na=False
                                            )
                                            cad_excel_matches = cad_excel_df[search_mask].copy()

                                        if not cad_excel_matches.empty:
                                            st.success(f"✅ **{len(cad_excel_matches)} historische Bestellung(en) gefunden!**")

                                            # Berechne Durchschnittspreis
                                            cad_qty_col = _find_col(cad_excel_matches, ["quantity", "menge", "qty"])
                                            cad_avg_price, cad_mn, cad_mx, _, _ = derive_unit_price(cad_excel_matches)

                                            if cad_avg_price:
                                                c1, c2, c3 = st.columns(3)
                                                c1.metric("📊 Historischer Ø Preis", f"{cad_avg_price:,.4f} €")
                                                if cad_mn:
                                                    c2.metric("Min-Preis", f"{cad_mn:,.4f} €")
                                                if cad_mx:
                                                    c3.metric("Max-Preis", f"{cad_mx:,.4f} €")

                                            # Zeige Details
                                            with st.expander("📋 Historische Bestellungen", expanded=False):
                                                display_cols = [c for c in cad_excel_matches.columns if c in ["item", "supplier", "quantity", "unit_price", "date"]]
                                                if display_cols:
                                                    st.dataframe(cad_excel_matches[display_cols], use_container_width=True)
                                                else:
                                                    st.dataframe(cad_excel_matches, use_container_width=True)
                                        else:
                                            st.info(f"ℹ️ Artikel '**{cad_description}**' nicht in Bestellhistorie gefunden. Führe KI-Schätzung durch...")
                                    else:
                                        st.warning("⚠️ Artikel-Spalte in Excel nicht gefunden")
                            except Exception as e:
                                st.warning(f"⚠️ Excel-Durchsuchung fehlgeschlagen: {e}")

                        with st.spinner("🤖 Analysiere CAD-Artikel..."):
                                st.session_state.cad_est_result = _run_cost_estimate(cad_description, int(cad_lot_size), cad_avg_price)

                    # Ergebnis anzeigen
                    if "cad_est_result" in st.session_state and st.session_state.cad_est_result:
                        res = st.session_state.cad_est_result

                        if not res.get("ok"):
                            st.error(f"❌ Schätzung fehlgeschlagen: {res.get('error', 'unbekannter Fehler')}")
                            with st.expander("🔍 Debug-Info"):
                                st.json(res)
                        else:
                            st.success("✅ Kostenschätzung abgeschlossen!")

                            # Metriken
                            c1, c2, c3 = st.columns(3)
                            material_eur = res.get("material_eur")
                            fab_eur = res.get("fab_eur")
                            target = res.get("target")

                            c1.metric("💎 Material €/Stk", f"{material_eur:,.4f} €" if material_eur is not None else "N/A")
                            c2.metric("⚙️ Fertigung €/Stk", f"{fab_eur:,.4f} €" if fab_eur is not None else "N/A")
                            c3.metric("🎯 Soll-Kosten €/Stk", f"{target:,.4f} €" if target is not None else "N/A")

                            st.info("ℹ️ **Hinweis**: Reine KI-Schätzung basierend auf technischer Zeichnung.")

                            # Details
                            with st.expander("📋 Technische Details", expanded=True):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"• Material: **{res.get('mat', 'unknown')}**")
                                    if res.get('d_mm'):
                                        st.write(f"• Durchmesser: **{res.get('d_mm'):.1f} mm**")
                                    if res.get('l_mm'):
                                        st.write(f"• Länge: **{res.get('l_mm'):.1f} mm**")
                                with col2:
                                    if res.get('mass_kg'):
                                        st.write(f"• Masse: **{res.get('mass_kg')*1000:.1f} g**")
                                    st.write(f"• Prozess: **{res.get('process', 'unknown')}**")
                                    conf = res.get('confidence', 'unknown')
                                    conf_emoji = "🟢" if conf == "high" else "🟡" if conf == "medium" else "🔴"
                                    st.write(f"• Vertrauen: {conf_emoji} **{conf}**")

            else:
                st.error(f"❌ Fehler: {drawing_data.get('error', 'Unbekannt')}")

# Excel-Upload verarbeiten
if 'up' in locals() and up is not None:
    try:
        df = _read_file(up)
        df = _norm_columns(df)
    except Exception as e:
        st.error(f"Datei konnte nicht gelesen werden: {e}")
        df = pd.DataFrame()

# Spalten-Mapping
item_col = _find_col(df, ["item", "artikel", "bezeichnung", "produkt", "artikelnummer", "artnr", "art-nr"])
supplier_col = _find_col(df, ["supplier", "lieferant", "anbieter", "vendor", "firma"])
country_col = _find_col(df, ["country", "land", "herkunft", "ursprung", "origin"])
qty_col = _find_col(df, ["quantity", "menge", "qty", "anzahl", "stueck", "stück", "pcs"])
price_col = _find_col(df, ["unit_price", "einzelpreis", "stkpreis", "preis_pro_stk", "price", "preis", "avg_price", "nettopreis"])

# Prüfe ob CAD-only Modus (nur CAD/3D, kein Excel)
cad_only_mode = (drawing_data and drawing_data.get('ok') and (df.empty or item_col is None)) or (cad_3d_data and cad_3d_data.get('ok'))

# Zeige nur relevante UI basierend auf Modus
if not cad_only_mode:
    # ==================== EXCEL-MODUS: Volle UI mit Artikel-Auswahl und Lieferanten ====================
    # Layout: Hauptbereich (links) + Lieferanten (rechts)
    left, right = st.columns([3, 2])

    # ==================== LINKE SPALTE: ARTIKEL & KOSTEN ====================
    with left:
        if df.empty or item_col is None:
            st.info("📊 Bitte Excel/CSV Datei hochladen. Erforderliche Spalten: Artikel/Bezeichnung, optional: Lieferant, Land, Menge, Einzelpreis.")
            sel = None
            idf = pd.DataFrame()
            avg = None
        else:
            # ==================== VERBESSERTE ARTIKEL-SUCHE ====================
            st.markdown("### 🔍 Artikel-Suche (lieferantenübergreifend)")
            query = st.text_input(
                "Artikelbezeichnung eingeben (z.B. 'DIN 933 M8')",
                "",
                placeholder="Beliebige Zeichenkette eingeben...",
                help="Sucht in ALLEN Artikelbezeichnungen aller Lieferanten. Findet z.B. 'DIN 933 M8' bei verschiedenen Lieferanten."
            )

            # Suche in ALLEN Zeilen mit GPT-basierter intelligenter Suche
            if query and query.strip():
                with st.spinner("🤖 KI analysiert Suchanfrage..."):
                    # Hole alle unique Artikel
                    all_items = df[item_col].unique().tolist()

                    # GPT-basierte intelligente Suche
                    matched_indices = gpt_intelligent_article_search(query, all_items)

                    if matched_indices:
                        # Konvertiere Indizes zu Artikelnamen
                        matched_items = [all_items[i] for i in matched_indices]

                        # Filtere DataFrame
                        idf = df[df[item_col].isin(matched_items)].copy()
                    else:
                        # Fallback: Einfache String-Suche
                        st.info("💡 KI-Suche lieferte keine Ergebnisse, nutze einfache Textsuche als Fallback...")
                        search_mask = df[item_col].astype(str).str.lower().str.contains(query.lower(), na=False)
                        idf = df[search_mask].copy()

                if not idf.empty:
                    # Zeige Anzahl gefundener Einträge
                    num_entries = len(idf)
                    num_unique_items = idf[item_col].nunique()
                    num_suppliers = idf[supplier_col].nunique() if supplier_col and supplier_col in idf.columns else "?"

                    st.success(f"✅ **{num_entries} Einträge gefunden** ({num_unique_items} einzigartige Artikel, {num_suppliers} Lieferanten)")

                    # Zeige gefundene Artikel-Varianten
                    unique_items_found = sorted(idf[item_col].unique().tolist())
                    if len(unique_items_found) > 1:
                        with st.expander(f"📋 {len(unique_items_found)} Artikel-Varianten gefunden", expanded=False):
                            for item in unique_items_found[:20]:  # Max 20 anzeigen
                                st.write(f"• {item}")
                            if len(unique_items_found) > 20:
                                st.caption(f"... und {len(unique_items_found) - 20} weitere")

                    # Wenn mehrere Artikel gefunden: Zeige ALLE, aber lass Nutzer wählen für Detail-Analyse
                    if num_unique_items > 1:
                        sel = st.selectbox(
                            "Artikel für Detail-Analyse wählen (zeigt alle Einträge für gewählten Artikel)",
                            unique_items_found,
                            index=0,
                            help="Wähle einen spezifischen Artikel für detaillierte Kostenanalyse. WICHTIG: Alle gefundenen Einträge bleiben sichtbar!"
                        )
                        # NICHT filtern! Behalte alle Suchergebnisse in idf
                        # Nur sel wird für Kostenanalyse verwendet
                    else:
                        sel = unique_items_found[0]
                else:
                    st.warning(f"❌ Keine Ergebnisse für '{query}' gefunden.")
                    sel = None
                    idf = pd.DataFrame()
            else:
                # Kein Query: Zeige altes Verhalten (Dropdown mit allen Artikeln)
                st.info("💡 Gib eine Zeichenkette ein, um lieferantenübergreifend zu suchen.")
                items_all = sorted(pd.Series(df[item_col].astype(str).unique()).tolist()[:500])  # Limit für Performance
                sel = st.selectbox("Oder wähle aus allen Artikeln", [""] + items_all, index=0)
                if sel:
                    idf = df[df[item_col] == sel].copy()
                else:
                    sel = None
                    idf = pd.DataFrame()

        # Preis-Statistik anzeigen (lieferantenübergreifend!)
        if not idf.empty:
            try:
                avg, mn, mx, _qcol, _src = derive_unit_price(idf)

                # Lieferanten-Info
                num_suppliers_in_results = idf[supplier_col].nunique() if supplier_col and supplier_col in idf.columns else 1
                num_entries = len(idf)

                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 1rem; border-radius: 10px; color: white; margin: 1rem 0;'>
                    <h4 style='margin: 0; color: white;'>📊 Preisübersicht über {num_suppliers_in_results} Lieferanten ({num_entries} Einträge)</h4>
                </div>
                """, unsafe_allow_html=True)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Ø Preis (gewichtet)", f"{avg:,.4f} €" if avg is not None else "N/A",
                         help="Gewichteter Durchschnitt über alle Lieferanten und Bestellungen")
                c2.metric("Min-Preis", f"{mn:,.4f} €" if mn is not None else "N/A",
                         help="Niedrigster gefundener Preis")
                c3.metric("Max-Preis", f"{mx:,.4f} €" if mx is not None else "N/A",
                         help="Höchster gefundener Preis")

                # Preisrange berechnen
                if mn is not None and mx is not None and mn > 0:
                    price_range_pct = ((mx - mn) / mn) * 100
                    c4.metric("Preisrange", f"{price_range_pct:,.1f}%",
                             help="Prozentuale Differenz zwischen Min und Max Preis",
                             delta=f"{mx - mn:,.4f} €" if mx != mn else None)
                else:
                    c4.metric("Preisrange", "N/A")

                # Detaillierte Lieferanten-Breakdown
                if supplier_col and supplier_col in idf.columns and num_suppliers_in_results > 1:
                    with st.expander(f"📋 Preis-Breakdown nach Lieferant ({num_suppliers_in_results} Lieferanten)", expanded=True):
                        # Gruppiere nach Lieferant
                        price_series = get_price_series_per_unit(idf, qty_col)
                        if price_series is not None:
                            idf_temp = idf.copy()
                            idf_temp['_unit_price'] = price_series

                            supplier_breakdown = idf_temp.groupby(supplier_col).agg({
                                '_unit_price': ['mean', 'min', 'max', 'count']
                            }).round(4)

                            # Flatten columns
                            supplier_breakdown.columns = ['Ø Preis', 'Min', 'Max', 'Anzahl Einträge']
                            supplier_breakdown = supplier_breakdown.sort_values('Ø Preis')
                            supplier_breakdown.index.name = 'Lieferant'

                            # Highlight bester Preis
                            st.dataframe(
                                supplier_breakdown.style.highlight_min(subset=['Ø Preis'], color='lightgreen'),
                                use_container_width=True
                            )

                with st.expander("🔍 Debug: Preis-Parsing", expanded=False):
                    st.write({"qty_col": str(_qcol), "source": _src, "columns": list(idf.columns)})
            except Exception as e:
                st.caption(f"Preis-Parsing fehlgeschlagen: {e}")
                avg = None
        else:
            avg = None

        # Kostenschätzung
        st.markdown("---")
        st.markdown("### 💰 Kostenschätzung")
        st.caption("KI-basierte Analyse von Material- und Fertigungskosten")

        if "est_result" not in st.session_state:
            st.session_state.est_result = None

        # ==================== LIEFERANTENAUSWAHL ====================
        selected_supplier = None
        if not idf.empty and supplier_col and supplier_col in idf.columns:
            available_suppliers = sorted(idf[supplier_col].dropna().unique().tolist())

            if len(available_suppliers) > 1:
                st.markdown("#### 🏭 Lieferantenauswahl")
                st.info(f"📦 Für diesen Artikel gibt es **{len(available_suppliers)} Lieferanten**. Wähle einen für die Kostenschätzung (verschiedene Lieferanten haben verschiedene Fertigungskompetenzen).")

                # Dropdown für Lieferanten
                selected_supplier = st.selectbox(
                    "Wähle Lieferanten für Kostenschätzung:",
                    options=[""] + available_suppliers,
                    index=0,
                    help="Die Fertigungskompetenzen und Kostenstruktur variieren je nach Lieferant"
                )

                if selected_supplier and selected_supplier != "":
                    # Zeige Info über gewählten Lieferanten
                    supplier_data = idf[idf[supplier_col] == selected_supplier]
                    # price_series ist bereits eine Series mit Preisen - wir filtern sie nach supplier_data Index
                    supplier_avg_price = price_series.loc[supplier_data.index].mean() if price_series is not None and len(supplier_data) > 0 else None

                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.metric("🏭 Gewählter Lieferant", selected_supplier)
                    with col_info2:
                        if supplier_avg_price is not None:
                            st.metric("💰 Ø Preis dieses Lieferanten", f"{supplier_avg_price:,.4f} €")
                        else:
                            st.metric("💰 Ø Preis dieses Lieferanten", "N/A")
                else:
                    st.warning("⚠️ Bitte wähle einen Lieferanten aus, um die Kostenschätzung zu starten.")
            elif len(available_suppliers) == 1:
                # Nur ein Lieferant verfügbar
                selected_supplier = available_suppliers[0]
                st.info(f"🏭 **Einziger Lieferant:** {selected_supplier}")

        lot_size = st.number_input("Losgröße", min_value=1, max_value=1_000_000, value=1000, step=100, key="excel_lot_size")

        # Button nur aktiv wenn Lieferant gewählt
        button_disabled = False
        if not idf.empty and supplier_col and supplier_col in idf.columns:
            available_suppliers_count = len(idf[supplier_col].dropna().unique())
            if available_suppliers_count > 1 and (not selected_supplier or selected_supplier == ""):
                button_disabled = True

        if st.button("🚀 Kosten schätzen (GPT + Lieferanten-Analyse)", type="primary", use_container_width=True, disabled=button_disabled):
            if sel:
                st.session_state.est_result = _run_cost_estimate(
                    sel,
                    int(lot_size),
                    avg,
                    idf=idf,  # NEU: Übergebe Lieferanten-Daten
                    supplier_col=supplier_col,
                    item_col=item_col,
                    selected_supplier=selected_supplier  # NEU: Übergebe gewählten Lieferanten
                )
            else:
                st.warning("Bitte zuerst einen Artikel wählen.")

        res = st.session_state.est_result
        if res is None:
            st.info("👆 Klicke auf **Kosten schätzen**, um Material- und Fertigungskosten zu berechnen.")
        else:
            if not res.get("ok"):
                st.error(f"❌ Schätzung fehlgeschlagen: {res.get('error', 'unbekannter Fehler')}")
            else:
                # API-Usage Tracking anzeigen
                gpt_material_raw = res.get("gpt_material_raw", {})
                gpt_fab_raw = res.get("gpt_fab_raw", {})

                material_api_called = gpt_material_raw.get("_api_called", False)
                material_fallback = gpt_material_raw.get("_fallback", False)
                material_tokens = gpt_material_raw.get("_tokens_used", 0)

                fab_api_called = gpt_fab_raw.get("_api_called", False)
                fab_fallback = gpt_fab_raw.get("_fallback", False)
                fab_tokens = gpt_fab_raw.get("_tokens_used", 0)

                total_tokens = material_tokens + fab_tokens

                # Info-Box: API Status
                if material_fallback or fab_fallback:
                    st.error("""
                    ⚠️ **WARNUNG: KEIN API-CALL!**

                    Die Ergebnisse basieren auf **Fallback-Code**, nicht auf GPT!
                    → **Keine Kosten bei OpenAI entstanden**

                    **Mögliche Ursachen:**
                    1. OpenAI Library nicht installiert
                    2. API-Key nicht richtig geladen
                    3. Netzwerk-Problem

                    **Lösung:** Check Konsole-Output für Details!
                    """)
                elif material_api_called or fab_api_called:
                    st.success(f"""
                    ✅ **GPT-4o API ERFOLGREICH AUFGERUFEN!**

                    - Material-Schätzung: **{material_tokens} Tokens** (GPT-4o)
                    - Fertigungs-Schätzung: **{fab_tokens} Tokens** (GPT-4o)
                    - **Total: {total_tokens} Tokens**

                    💰 **Geschätzte Kosten:** ~${total_tokens * 0.00002:.6f} USD
                    → Das sollte jetzt in deinem OpenAI Billing auftauchen!
                    """)


                # Hauptmetriken in visuellen Karten
                st.markdown("""
                <div style='background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 1rem 0;'>
                """, unsafe_allow_html=True)

                cA, cB, cC, cD = st.columns(4)
                material_eur = res.get("material_eur")
                fab_eur = res.get("fab_eur")
                target = res.get("target")
                delta = res.get("delta")

                cA.metric("💎 Material €/Stk", f"{material_eur:,.4f} €" if material_eur is not None else "N/A")
                cB.metric("⚙️ Fertigung €/Stk", f"{fab_eur:,.4f} €" if fab_eur is not None else "N/A")
                cC.metric("🎯 Soll-Kosten €/Stk", f"{target:,.4f} €" if target is not None else "N/A",
                         help="Geschätzte Gesamtkosten (Material + Fertigung)")

                delta_color = "🟢" if delta and delta > 0 else "🔴" if delta and delta < 0 else "⚪"
                cD.metric(
                    f"{delta_color} Delta vs. Ø Einkauf",
                    f"{delta:+,.4f} €" if delta is not None else "N/A",
                    delta=f"{(delta/avg*100):+.1f}%" if delta and avg and avg != 0 else None,
                    help="Positive Werte = Einsparungspotenzial"
                )

                st.markdown("</div>", unsafe_allow_html=True)

                # ==================== MÖGLICHE ERSPARNISSE (GPT-Schätzung) ====================
                if avg and target and avg > target:  # Nur wenn historischer Preis höher als GPT-Zielpreis
                    savings_per_unit = avg - target
                    savings_total = savings_per_unit * lot_size
                    savings_pct = (savings_per_unit / avg * 100) if avg > 0 else 0

                    st.markdown("---")
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                padding: 1.5rem; border-radius: 10px; color: white; margin: 1rem 0;'>
                        <h4 style='margin: 0; color: white;'>💰 Mögliche Ersparnisse</h4>
                        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                            Durch optimierte Fertigung und Verhandlung
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        "💵 Ersparnis pro Stück",
                        f"{savings_per_unit:,.4f} €",
                        delta=f"-{savings_pct:.1f}%",
                        help="Differenz zwischen historischem Ø-Preis und GPT-Zielkosten"
                    )
                    col2.metric(
                        "📊 Losgröße",
                        f"{lot_size:,} Stück",
                        help="Eingegebene Losgröße"
                    )
                    col3.metric(
                        "🎯 Gesamtersparnis",
                        f"{savings_total:,.2f} €",
                        help=f"{savings_per_unit:,.4f} € × {lot_size:,} Stück"
                    )

                    st.info(f"""
                    💡 **Interpretation:**
                    - **Historischer Durchschnitt:** {avg:,.4f} €/Stk (was Sie aktuell zahlen)
                    - **GPT-Zielkosten:** {target:,.4f} €/Stk (was Sie zahlen sollten)
                    - **Einsparungspotenzial:** {savings_total:,.2f} € bei {lot_size:,} Stück ({savings_pct:.1f}%)

                    ✅ Nutzen Sie diese Zahlen in Verhandlungen!
                    """)

                # ==================== LIEFERANTEN-KOMPETENZEN ANZEIGE ====================
                supplier_competencies = res.get('supplier_competencies')
                supplier_name = res.get('supplier_name')

                if supplier_competencies and not supplier_competencies.get('_error') and not supplier_competencies.get('_fallback'):
                    st.markdown("---")
                    st.markdown(f"### 🏭 Produktionskompetenzen: **{supplier_name}**")

                    core_comps = supplier_competencies.get('core_competencies', [])
                    spec = supplier_competencies.get('specialization', {})
                    mat_exp = supplier_competencies.get('material_expertise', [])

                    # Kompakte Anzeige
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                                padding: 1rem; border-radius: 10px; color: white; margin: 1rem 0;'>
                        <h4 style='margin: 0; color: white;'>🎯 Analyse der Produktionskompetenzen</h4>
                        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                            Basierend auf Artikelhistorie und Spezialisierung
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown("**🔧 Hauptkompetenzen:**")
                        if core_comps:
                            for comp in core_comps[:4]:
                                process = comp.get('process', 'unknown')
                                level = comp.get('capability_level', 'proficient')
                                emoji = "🟢" if level == "expert" else "🟡" if level == "proficient" else "🔴"
                                st.write(f"{emoji} **{process}** ({level})")
                        else:
                            st.caption("Keine Daten")

                    with col2:
                        st.markdown("**🏢 Spezialisierung:**")
                        if spec:
                            primary_focus = spec.get('primary_focus', 'unknown')
                            part_complexity = spec.get('part_complexity', 'unknown')
                            st.write(f"• Fokus: **{primary_focus}**")
                            st.write(f"• Komplexität: **{part_complexity}**")
                            prod_cap = supplier_competencies.get('production_capabilities', {})
                            if prod_cap.get('preferred_lot_sizes'):
                                st.write(f"• Losgrößen: **{prod_cap['preferred_lot_sizes']}**")
                        else:
                            st.caption("Keine Daten")

                    with col3:
                        st.markdown("**⚗️ Material-Expertise:**")
                        if mat_exp:
                            for mat in mat_exp[:4]:
                                mat_name = mat.get('material', 'unknown')
                                conf = mat.get('confidence', 'medium')
                                emoji = "🟢" if conf == "high" else "🟡" if conf == "medium" else "🔴"
                                st.write(f"{emoji} {mat_name}")
                        else:
                            st.caption("Keine Daten")

                    # Warnung bei ungeeigneten Prozessen
                    unsuitable = supplier_competencies.get('unsuitable_processes', [])
                    if unsuitable:
                        with st.expander("⚠️ Nicht geeignete Prozesse (wichtig für Verhandlung!)", expanded=False):
                            for unsui in unsuitable:
                                proc = unsui.get('process', 'unknown')
                                reason = unsui.get('reason', 'Keine Expertise')
                                st.warning(f"**{proc}**: {reason}")

                    # Empfehlungen
                    recommendations = supplier_competencies.get('recommendations', [])
                    if recommendations:
                        with st.expander("💡 Strategische Empfehlungen", expanded=True):
                            for rec in recommendations:
                                st.write(f"• {rec}")

                # ==================== MÖGLICHE ERSPARNISSE ====================
                if mn is not None and mx is not None and mn < mx:
                    st.markdown("---")
                    st.markdown("### 💰 Mögliche Ersparnisse durch Verhandlung")

                    # Berechne Einsparungspotenzial
                    savings_per_unit = mx - mn
                    savings_total = savings_per_unit * lot_size
                    savings_pct = (savings_per_unit / mx * 100) if mx > 0 else 0

                    # Zeige in schöner Box
                    st.markdown("""
                    <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                padding: 1.5rem; border-radius: 10px; color: white; margin: 1rem 0;'>
                        <h4 style='margin: 0; color: white;'>💡 Einsparungspotenzial</h4>
                        <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                            Durch Verhandlung von Max-Preis auf Min-Preis
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        "💵 Ersparnis pro Stück",
                        f"{savings_per_unit:,.4f} €",
                        delta=f"-{savings_pct:.1f}%",
                        help="Differenz zwischen höchstem und niedrigstem Preis"
                    )
                    col2.metric(
                        "📊 Losgröße",
                        f"{lot_size:,} Stück",
                        help="Eingegebene Losgröße"
                    )
                    col3.metric(
                        "💰 Total-Ersparnis",
                        f"{savings_total:,.2f} €",
                        delta=f"-{savings_pct:.1f}%",
                        help="Potenzielle Gesamtersparnis bei Min-Preis für gesamte Losgröße"
                    )

                    # Verhandlungs-Tipps
                    with st.expander("💡 Verhandlungs-Tipps", expanded=False):
                        st.markdown(f"""
                        **Argumentationsbasis:**
                        - Min-Preis: **{mn:,.4f} €** (Benchmark-Preis von günstigstem Lieferant)
                        - Max-Preis: **{mx:,.4f} €** (Aktueller Höchstpreis)
                        - Zielpreis: **{mn:,.4f} € - {(mn + mx)/2:,.4f} €** (realistischer Verhandlungsrahmen)

                        **Strategie:**
                        1. 🎯 Zeige dem Lieferanten, dass andere Anbieter **{savings_pct:.1f}% günstiger** sind
                        2. 💼 Nutze Losgröße ({lot_size:,} Stück) als Verhandlungshebel
                        3. 🤝 Biete langfristige Partnerschaft für bessere Konditionen
                        4. 📊 Verweis auf Marktdaten und Wettbewerb
                        5. ⏱️ Zeitliche Flexibilität gegen Preisnachlass
                        """)

            eur_per_kg = res.get("eur_per_kg")
            mat = res.get("mat")
            d_mm = res.get("d_mm")
            l_mm = res.get("l_mm")
            mass_kg = res.get("mass_kg")
            process = res.get("process", "unknown")
            part_class = res.get("part_class", "unknown")
            confidence = res.get("confidence", "unknown")

            # Details in organisierten Spalten
            with st.expander("📋 Technische Details & Parameter", expanded=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**🔧 Material & Abmessungen**")
                    st.write(f"• Material: **{mat}**")
                    if d_mm:
                        st.write(f"• Durchmesser: **{d_mm:.1f} mm**")
                    if l_mm:
                        st.write(f"• Länge: **{l_mm:.1f} mm**")
                    if mass_kg:
                        st.write(f"• Masse: **{mass_kg*1000:.1f} g** ({mass_kg:.4f} kg)")

                with col2:
                    st.markdown("**⚙️ Fertigungsprozess**")
                    st.write(f"• Teilklasse: **{part_class}**")
                    st.write(f"• Prozess: **{process}**")
                    if eur_per_kg:
                        st.write(f"• Materialpreis: **{eur_per_kg:.2f} €/kg**")

                with col3:
                    st.markdown("**📊 KI-Schätzung**")
                    conf_emoji = "🟢" if confidence == "high" else "🟡" if confidence == "medium" else "🔴"
                    st.write(f"• Vertrauen: {conf_emoji} **{confidence}**")
                    st.write(f"• Losgröße: **{lot_size:,} Stück**")

            # Annahmen anzeigen
            assumptions = res.get("assumptions", [])
            if assumptions:
                with st.expander("🤖 GPT-Annahmen & Begründung", expanded=False):
                    for i, assumption in enumerate(assumptions, 1):
                        st.write(f"{i}. {assumption}")

            with st.expander("🔍 Debug: Rohe GPT-Ausgaben", expanded=False):
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Material-Schätzung:**")
                    st.json(res.get("gpt_material_raw"))
                with col2:
                    st.write("**Fertigungs-Schätzung:**")
                    st.json(res.get("gpt_fab_raw"))

            # ==================== CO₂-FOOTPRINT & CBAM ====================
            if mass_kg and mass_kg > 0:
                st.markdown("---")
                st.markdown("### 🌍 CO₂-Footprint & CBAM-Kosten (ab 2026)")

                # Lieferanten-Land ermitteln (falls vorhanden)
                supplier_country = None
                if not idf.empty and country_col and country_col in idf.columns:
                    countries = idf[country_col].dropna().unique()
                    if len(countries) > 0:
                        supplier_country = countries[0]

                # CO₂-Berechnung
                co2_result = calculate_co2_footprint(
                    mass_kg=mass_kg,
                    supplier_country=supplier_country or "Deutschland",
                    material=mat
                )

                # Anzeige
                st.markdown("""
                <div style='background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
                            padding: 1rem; border-radius: 10px; color: white; margin: 1rem 0;'>
                    <h4 style='margin: 0; color: white;'>🌱 Nachhaltigkeits-Analyse</h4>
                    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                        CO₂-Emissionen und CBAM-Kosten (Carbon Border Adjustment Mechanism ab 2026)
                    </p>
                </div>
                """, unsafe_allow_html=True)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric(
                    "🏭 Produktion",
                    f"{co2_result['co2_total_g']:.1f} g CO₂",
                    help=f"CO₂-Emissionen aus Materialproduktion: {co2_result['co2_production_kg']:.6f} kg"
                )
                c2.metric(
                    "🚚 Transport",
                    f"{co2_result['co2_transport_kg']*1000:.1f} g CO₂",
                    help=f"Transport: {co2_result['transport_distance_km']} km via {co2_result['transport_mode']}"
                )
                c3.metric(
                    "🌍 Total CO₂",
                    f"{co2_result['co2_total_g']:.1f} g",
                    help=f"Gesamt CO₂ pro Stück: {co2_result['co2_total_kg']:.6f} kg"
                )
                c4.metric(
                    "💳 CBAM-Kosten",
                    f"{co2_result['cbam_cost_eur']:.6f} €" if co2_result['cbam_cost_eur'] > 0 else "N/A",
                    help=co2_result['cbam_status']
                )

                # CBAM-Status und Detailsanzeige
                with st.expander("📊 CO₂-Details & CBAM-Info", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**CO₂-Aufschlüsselung:**")
                        st.write(f"• Materialproduktion: **{co2_result['co2_production_kg']*1000:.2f} g CO₂**")
                        st.write(f"• Transport ({co2_result['transport_mode']}): **{co2_result['co2_transport_kg']*1000:.2f} g CO₂**")
                        st.write(f"• Distanz: **{co2_result['transport_distance_km']} km**")
                        st.write(f"• CO₂-Faktor ({mat}): **{co2_result['material_co2_factor_kg_per_kg']} kg CO₂/kg**")

                    with col2:
                        st.markdown("**CBAM-Status:**")
                        st.write(f"• Status: **{co2_result['cbam_status']}**")
                        st.write(f"• Herkunft: **{'EU' if co2_result['is_eu_source'] else 'Nicht-EU'}**")
                        if co2_result['cbam_cost_eur'] > 0:
                            cbam_total = co2_result['cbam_cost_eur'] * lot_size
                            st.write(f"• CBAM pro Stück: **{co2_result['cbam_cost_eur']:.6f} €**")
                            st.write(f"• CBAM für Losgröße: **{cbam_total:.2f} €** ({lot_size:,} Stk)")
                        else:
                            st.write("• CBAM: **Nicht anwendbar** (EU-Binnenmarkt)")

                    st.markdown("**ℹ️ CBAM-Info:**")
                    st.info("""
                    **Carbon Border Adjustment Mechanism (CBAM)** gilt ab 2026 für Importe in die EU.
                    CBAM zielt darauf ab, CO₂-Emissionen aus Nicht-EU-Importen zu bepreisen und gleiche
                    Wettbewerbsbedingungen für EU-Produzenten zu schaffen.

                    **Betroffene Materialien:** Stahl, Aluminium, Zement, Düngemittel, Strom, Wasserstoff

                    **Preis:** Orientiert sich am EU ETS (Emissionshandel), ca. 80-100 €/t CO₂ (Prognose 2026)
                    """)

                    # Annahmen
                    st.markdown("**📋 Annahmen:**")
                    for assumption in co2_result['assumptions']:
                        st.write(f"• {assumption}")

    # ==================== RECHTE SPALTE: LIEFERANTEN ====================
    with right:
        st.markdown("### 🏢 Lieferanten-Management")
        st.caption("Übersicht, Bewertung und Verhandlungsstrategien")

        if 'up' not in locals() or up is None or df.empty:
            st.info("📊 Laden Sie Excel/CSV Daten, um Lieferanten zu analysieren.")
        else:
            if supplier_col is None:
                st.info("ℹ️ Spalte für Lieferant nicht gefunden. Benötigte Spalten: 'Lieferant', 'Supplier' oder 'Vendor'")
            else:
                # KI-Lieferanten-Rating
                st.markdown("---")
                st.markdown("**🤖 KI-Bewertung**")

                # WICHTIG: Nur Lieferanten des ausgewählten Artikels bewerten!
                if sel and not idf.empty:
                    display_df = idf.copy()
                    st.info(f"📊 Bewerte nur Lieferanten für Artikel: **{sel}**")
                else:
                    # Kein Artikel ausgewählt -> NICHT alle bewerten (zu teuer!)
                    st.warning("⚠️ Bitte wähle zuerst einen Artikel aus, um Lieferanten zu bewerten.")
                    display_df = pd.DataFrame()  # Leerer DataFrame = keine Bewertung

                # Lieferanten aggregieren (nur wenn Artikel ausgewählt!)
                if not display_df.empty and supplier_col in display_df.columns:
                    # Berechne Statistiken pro Lieferant
                    grp_cols = [supplier_col]
                    if country_col and country_col in display_df.columns:
                        grp_cols.append(country_col)

                    price_series = get_price_series_per_unit(display_df, qty_col)
                    if price_series is not None:
                        display_df = display_df.assign(_unit_price=pd.to_numeric(price_series, errors='coerce'))

                    # Berechne Min/Max Preise über ALLE Lieferanten (für Verhandlung)
                    global_min_price = None
                    global_max_price = None
                    global_avg_price = None
                    if '_unit_price' in display_df.columns:
                        valid_prices = pd.to_numeric(display_df['_unit_price'], errors='coerce').dropna()
                        if len(valid_prices) > 0:
                            global_min_price = float(valid_prices.min())
                            global_max_price = float(valid_prices.max())
                            global_avg_price = float(valid_prices.mean())

                    # Aggregation Dictionary dynamisch bauen
                    agg_dict = {}

                    # Prüfe ob _unit_price existiert und numerische Werte hat
                    if '_unit_price' in display_df.columns:
                        valid_prices = pd.to_numeric(display_df['_unit_price'], errors='coerce').dropna()
                        if len(valid_prices) > 0:
                            agg_dict['_unit_price'] = ['mean', 'std', 'count']
                        else:
                            agg_dict['_unit_price'] = ['count']

                    # Quantity aggregieren falls vorhanden
                    if qty_col and qty_col in display_df.columns:
                        agg_dict[qty_col] = 'sum'

                    # Fallback falls keine Spalten
                    if not agg_dict:
                        agg_dict = {grp_cols[0]: 'count'}

                    supplier_stats = display_df.groupby(grp_cols, dropna=False).agg(agg_dict).reset_index()

                    # Flatten columns
                    supplier_stats.columns = ['_'.join(col).strip('_') if col[1] else col[0] for col in supplier_stats.columns]

                    # Rating für jeden Lieferanten
                    ratings = []
                    for idx, row in supplier_stats.iterrows():
                        supplier_name = row[supplier_col] if supplier_col in row else "Unbekannt"
                        country = row[country_col] if (country_col and country_col in row) else None
                        avg_price = row.get('_unit_price_mean')
                        std_price = row.get('_unit_price_std')
                        total_orders = row.get('_unit_price_count', 0)

                        # Preisvolatilität berechnen (CV)
                        price_volatility = None
                        if avg_price and std_price and avg_price > 0:
                            price_volatility = std_price / avg_price

                        # Eindeutiger Schlüssel für Session State
                        supplier_key = f"{sel}_{supplier_name}_{country}"

                        # Prüfe ob Analyse bereits gecacht ist
                        if 'supplier_ratings' not in st.session_state:
                            st.session_state.supplier_ratings = {}

                        if supplier_key in st.session_state.supplier_ratings:
                            # Nutze gecachte Analyse
                            rating_result = st.session_state.supplier_ratings[supplier_key]
                        else:
                            # Noch nicht analysiert
                            rating_result = None

                        ratings.append({
                            'supplier': supplier_name,
                            'country': country,
                            'avg_price': avg_price,
                            'std_price': std_price,
                            'total_orders': total_orders,
                            'price_volatility': price_volatility,
                            'rating_result': rating_result,
                            'supplier_key': supplier_key,
                            'article_name': sel  # Für spätere Analyse
                        })

                    # === NEUE ANZEIGE: Lieferanten mit Analyse-Button ===
                    for idx, r in enumerate(ratings):
                        supplier_name = r['supplier']
                        country = r.get('country', '?')
                        rating_result = r.get('rating_result')

                        # Titel je nach Analyse-Status
                        if rating_result:
                            # Bereits analysiert
                            rating_value = rating_result.get('rating', 5)
                            risk_level = rating_result.get('risk_level', 'medium')
                            risk_colors = {'low': '🟢', 'medium': '🟡', 'high': '🟠', 'critical': '🔴'}
                            risk_emoji = risk_colors.get(risk_level, '⚪')
                            title = f"{supplier_name} ({country}) – {rating_value}/10 {risk_emoji}"
                        else:
                            # Noch nicht analysiert
                            title = f"{supplier_name} ({country}) – ⏸️ Noch nicht analysiert"

                        with st.expander(title, expanded=False):
                            # Zeige Basisdaten
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Bestellungen", int(r['total_orders']) if r['total_orders'] else 0)
                            if r['avg_price']:
                                c2.metric("Ø Preis", f"{r['avg_price']:,.4f} €")
                            if r['price_volatility']:
                                c3.metric("Volatilität", f"{r['price_volatility']:.2%}")

                            # Analyse-Button oder Ergebnis
                            if not rating_result:
                                # Button zum Analysieren
                                if st.button(f"🤖 Lieferant analysieren", key=f"analyze_supplier_{idx}", type="primary", use_container_width=True):
                                    with st.spinner(f"🔍 Analysiere {supplier_name}..."):
                                        # GPT Rating anfordern
                                        rating_result = gpt_rate_supplier(
                                            supplier_name=str(supplier_name),
                                            country=str(country) if country else None,
                                            price_volatility=r['price_volatility'],
                                            total_orders=int(r['total_orders']) if r['total_orders'] else None,
                                            avg_price=float(r['avg_price']) if r['avg_price'] else None,
                                            article_name=r['article_name']
                                        )

                                        # Cache im Session State
                                        st.session_state.supplier_ratings[r['supplier_key']] = rating_result
                                        st.rerun()
                            else:
                                # Zeige Analyse-Ergebnis
                                rating_value = rating_result.get('rating', 5)
                                risk_level = rating_result.get('risk_level', 'medium')
                                stars = "⭐" * rating_value + "☆" * (10 - rating_value)

                                risk_colors = {'low': '🟢', 'medium': '🟡', 'high': '🟠', 'critical': '🔴'}
                                risk_emoji = risk_colors.get(risk_level, '⚪')

                                st.write(f"**Rating:** {stars}")
                                st.write(f"**Risiko:** {risk_emoji} {risk_level}")

                                if rating_result.get('strengths'):
                                    st.write("**✅ Stärken:**")
                                    for strength in rating_result['strengths']:
                                        st.write(f"  • {strength}")

                                if rating_result.get('weaknesses'):
                                    st.write("**⚠️ Schwächen:**")
                                    for weakness in rating_result['weaknesses']:
                                        st.write(f"  • {weakness}")

                                if rating_result.get('recommendations'):
                                    st.write("**💡 Empfehlungen:**")
                                    for rec in rating_result['recommendations']:
                                        st.write(f"  • {rec}")

                    # ==================== CREDITREFORM FINANZDATEN ====================
                    st.markdown("---")
                    st.markdown("### 💳 Creditreform / Kreditreform Bonitätsprüfung")
                    st.caption("Abruf von Finanzkennzahlen und Bonitätsdaten (DEMO-Modus)")

                    # Session State für Login
                    if 'creditreform_session' not in st.session_state:
                        st.session_state.creditreform_session = None

                    # Login-Bereich
                    if not st.session_state.creditreform_session:
                        st.info("🔐 **Login erforderlich** um Creditreform-Daten abzurufen (Demo-Modus: beliebige Credentials)")

                        with st.form("creditreform_login_form"):
                            cr_username = st.text_input("Benutzername", placeholder="demo@firma.de")
                            cr_password = st.text_input("Passwort", type="password", placeholder="password")
                            cr_submit = st.form_submit_button("🔐 Einloggen")

                            if cr_submit:
                                if cr_username and cr_password:
                                    login_result = creditreform_login(cr_username, cr_password)
                                    if login_result.get('ok'):
                                        st.session_state.creditreform_session = login_result
                                        st.success(login_result.get('message'))
                                        st.rerun()
                                    else:
                                        st.error(login_result.get('message'))
                                else:
                                    st.error("❌ Bitte Benutzername und Passwort eingeben")
                    else:
                        # Eingeloggt
                        session = st.session_state.creditreform_session
                        st.success(f"✅ Eingeloggt als: **{session.get('username')}**")

                        col1, col2 = st.columns([4, 1])
                        with col2:
                            if st.button("🚪 Logout", key="cr_logout"):
                                st.session_state.creditreform_session = None
                                st.rerun()

                        # Lieferanten-Auswahl für Finanzdaten
                        if ratings:
                            cr_supplier_names = [r['supplier'] for r in ratings]
                            cr_selected_idx = st.selectbox(
                                "Lieferant für Bonitätsprüfung wählen",
                                range(len(cr_supplier_names)),
                                format_func=lambda i: cr_supplier_names[i],
                                key="cr_supplier_select"
                            )

                            if st.button("📊 Finanzdaten abrufen", key="cr_fetch_btn"):
                                cr_supplier = cr_supplier_names[cr_selected_idx]
                                with st.spinner(f"🔍 Rufe Creditreform-Daten für {cr_supplier} ab..."):
                                    cr_data = creditreform_get_company_data(
                                        cr_supplier,
                                        session.get('session_token')
                                    )

                                    if cr_data.get('ok'):
                                        st.success(f"✅ Finanzdaten für **{cr_data.get('company_name')}** abgerufen")

                                        # Bonität & Risiko
                                        st.markdown("""
                                        <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                                                    padding: 1rem; border-radius: 10px; color: white; margin: 1rem 0;'>
                                            <h4 style='margin: 0; color: white;'>📊 Bonitätsbewertung</h4>
                                        </div>
                                        """, unsafe_allow_html=True)

                                        c1, c2, c3, c4 = st.columns(4)
                                        c1.metric("Creditreform Score", f"{cr_data.get('creditreform_score')}/600")
                                        c2.metric("Risiko-Klasse", cr_data.get('risk_class'))
                                        c3.metric("Insolvenz-Risiko", f"{cr_data.get('insolvency_probability_pct')}%")
                                        c4.metric("Zahlungsverhalten", cr_data.get('payment_behavior'))

                                        # Finanz-Kennzahlen
                                        fin_data = cr_data.get('financial_data', {})
                                        if fin_data:
                                            with st.expander("💰 Finanz-Kennzahlen", expanded=True):
                                                c1, c2, c3 = st.columns(3)
                                                with c1:
                                                    st.write(f"**Umsatz:** {fin_data.get('revenue_eur_million', 0):.1f} Mio. EUR")
                                                    st.write(f"**EBITDA-Marge:** {fin_data.get('ebitda_margin_pct', 0):.1f}%")
                                                with c2:
                                                    st.write(f"**Eigenkapitalquote:** {fin_data.get('equity_ratio_pct', 0):.1f}%")
                                                    st.write(f"**Liquidität:** {fin_data.get('liquidity_ratio', 0):.2f}")
                                                with c3:
                                                    st.write(f"**Verschuldungsgrad:** {fin_data.get('debt_to_equity_ratio', 0):.2f}")
                                                    st.write(f"**Ø Zahlungsziel:** {cr_data.get('average_payment_delay_days', 0)} Tage")

                                        # Unternehmens-Info
                                        comp_info = cr_data.get('company_info', {})
                                        if comp_info:
                                            with st.expander("🏢 Unternehmens-Info", expanded=False):
                                                st.write(f"• **Mitarbeiter:** {comp_info.get('employees')}")
                                                st.write(f"• **Gegründet:** {comp_info.get('founded_year')}")
                                                st.write(f"• **Rechtsform:** {comp_info.get('legal_form')}")
                                                st.write(f"• **Branche:** {comp_info.get('industry')}")

                                        # Empfehlungen
                                        recs = cr_data.get('recommendations', [])
                                        if recs:
                                            st.markdown("**💡 Empfehlungen:**")
                                            for rec in recs:
                                                st.write(f"• {rec}")

                                        st.caption(f"Datenquelle: {cr_data.get('data_source')} | Stand: {cr_data.get('last_updated')}")
                                    else:
                                        st.error(f"❌ Fehler: {cr_data.get('error')}")

                    # Verhandlungsvorbereitung
                    st.markdown("---")
                    st.markdown("### 🎯 Verhandlungsvorbereitung für Einkäufer")

                    if ratings:
                        # Wähle Lieferant für Verhandlungsprep
                        supplier_names = [r['supplier'] for r in ratings]

                        # Format-Funktion mit Fehlerbehandlung
                        def format_supplier(i):
                            name = supplier_names[i]
                            rating_result = ratings[i].get('rating_result')
                            if rating_result:
                                rating_val = rating_result.get('rating', '?')
                                return f"{name} ({rating_val}/10)"
                            else:
                                return f"{name} (nicht analysiert)"

                        selected_supplier_idx = st.selectbox(
                            "Lieferant für Verhandlung wählen",
                            range(len(supplier_names)),
                            format_func=format_supplier,
                            key="nego_supplier_select"
                        )

                        if st.button("📋 Verhandlungsstrategie generieren", key="nego_prep_btn"):
                            selected_rating = ratings[selected_supplier_idx]

                            # Zielpreis ermitteln (z.B. Mittelwert zwischen Min und Avg, oder 10% unter Avg)
                            target_price = None
                            if avg_price:
                                if global_min_price:
                                    # Ziel: Zwischen Min und Avg
                                    target_price = (global_min_price + avg_price) / 2
                                else:
                                    # Fallback: 10% unter Durchschnitt
                                    target_price = avg_price * 0.9

                            # Rohstoffmarktanalyse durchführen (falls Material bekannt)
                            commodity_analysis = None
                            material_for_analysis = None

                            # Versuche Material aus Kostenschätzung zu holen
                            if 'est_result' in st.session_state and st.session_state.est_result:
                                est_res = st.session_state.est_result
                                if est_res.get('ok'):
                                    material_for_analysis = est_res.get('mat')

                            # Falls kein Material aus Kostenschätzung: Versuche aus Artikel-Name zu schätzen
                            if not material_for_analysis and sel:
                                # Einfache Heuristik
                                sel_lower = sel.lower()
                                if 'edelstahl' in sel_lower or 'a2' in sel_lower or 'a4' in sel_lower or 'stainless' in sel_lower:
                                    material_for_analysis = 'edelstahl'
                                elif 'alu' in sel_lower or 'aluminum' in sel_lower:
                                    material_for_analysis = 'aluminium'
                                elif 'messing' in sel_lower or 'brass' in sel_lower:
                                    material_for_analysis = 'messing'
                                elif 'kupfer' in sel_lower or 'copper' in sel_lower:
                                    material_for_analysis = 'kupfer'
                                else:
                                    material_for_analysis = 'stahl'  # Default

                            # Rohstoffmarktanalyse durchführen
                            if material_for_analysis:
                                with st.spinner(f"📊 Analysiere Rohstoffmarkt ({material_for_analysis})..."):
                                    commodity_analysis = get_commodity_market_analysis(material_for_analysis)

                                    # Zeige Marktanalyse dem Benutzer
                                    if commodity_analysis and commodity_analysis.get('ok'):
                                        st.markdown("---")
                                        st.markdown("""
                                        <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                                                    padding: 1rem; border-radius: 10px; color: white; margin: 1rem 0;'>
                                            <h4 style='margin: 0; color: white;'>📊 Rohstoffmarkt-Analyse</h4>
                                        </div>
                                        """, unsafe_allow_html=True)

                                        c1, c2, c3, c4 = st.columns(4)
                                        c1.metric("Material", commodity_analysis.get('material', 'N/A'))
                                        c2.metric("Marktpreis", f"{commodity_analysis.get('current_price_eur_kg', 0):.2f} €/kg")

                                        trend_pct = commodity_analysis.get('trend_percentage', 0)
                                        trend_emoji = "📉" if trend_pct < 0 else "📈" if trend_pct > 0 else "📊"
                                        c3.metric("Trend", f"{trend_emoji} {commodity_analysis.get('trend', 'N/A')}",
                                                 delta=f"{trend_pct:+.1f}%")

                                        leverage = commodity_analysis.get('negotiation_leverage', 'NEUTRAL')
                                        leverage_color = "🟢" if "HOCH" in leverage else "🟡" if "MITTEL" in leverage else "🔴" if "NIEDRIG" in leverage else "⚪"
                                        c4.metric("Verhandlungshebel", f"{leverage_color} {leverage.split(' -')[0]}")

                                        # Detaillierte Analyse in Expander
                                        with st.expander("📈 Detaillierte Marktanalyse", expanded=True):
                                            st.markdown(commodity_analysis.get('analysis', 'Keine Details verfügbar'))
                                            st.caption(f"📊 {commodity_analysis.get('recommendation', '')}")
                                            st.caption(f"Quelle: {commodity_analysis.get('data_source', 'Unbekannt')}")

                            # Hole Rating-Daten
                            rating_result = selected_rating.get('rating_result')
                            if not rating_result:
                                st.warning("⚠️ Bitte analysieren Sie den Lieferanten zuerst, bevor Sie eine Verhandlungsstrategie generieren!")
                            else:
                                with st.spinner("🤖 GPT erstellt Verhandlungsstrategie..."):
                                    nego_prep = gpt_negotiation_prep(
                                        supplier_name=selected_rating['supplier'],
                                        country=selected_rating.get('country'),
                                        rating=rating_result.get('rating', 5),
                                        strengths=rating_result.get('strengths', []),
                                        weaknesses=rating_result.get('weaknesses', []),
                                        avg_price=float(selected_rating['avg_price']) if selected_rating.get('avg_price') else None,
                                    target_price=float(target_price) if target_price else None,
                                    article_name=sel,  # WICHTIG: Artikel-Kontext!
                                    total_orders=int(total_orders) if total_orders else None,
                                    min_price=global_min_price,  # NEU: Min-Preis für Benchmark
                                    max_price=global_max_price,  # NEU: Max-Preis für Verhandlungshebel
                                    commodity_analysis=commodity_analysis  # NEU: Rohstoffmarkt-Analyse!
                                )

                                st.success("✅ Verhandlungsstrategie bereit!")

                                # Strategie anzeigen
                                st.markdown(f"#### 🎯 Strategie: {nego_prep.get('strategy')}")

                                approach = nego_prep.get('approach', 'collaborative')
                                approach_emoji = "🤝" if approach == "win-win" else "⚔️" if approach == "competitive" else "🤝"
                                st.write(f"**Ansatz:** {approach_emoji} {approach}")

                                # Eröffnungsstatement
                                if nego_prep.get('opening_statement'):
                                    with st.expander("💬 Eröffnungsstatement", expanded=True):
                                        st.info(nego_prep['opening_statement'])

                                # Gesprächspunkte
                                col1, col2 = st.columns(2)

                                with col1:
                                    talking_points = nego_prep.get('talking_points', [])
                                    if talking_points:
                                        st.markdown("**📌 Gesprächspunkte:**")
                                        for i, point in enumerate(talking_points, 1):
                                            st.write(f"{i}. {point}")

                                    tactics = nego_prep.get('tactics', [])
                                    if tactics:
                                        st.markdown("**🎯 Verhandlungstaktiken:**")
                                        for tactic in tactics:
                                            st.write(f"• {tactic}")

                                with col2:
                                    red_flags = nego_prep.get('red_flags', [])
                                    if red_flags:
                                        st.markdown("**🚩 Warnsignale:**")
                                        for flag in red_flags:
                                            st.write(f"• {flag}")

                                    concessions = nego_prep.get('concessions', [])
                                    if concessions:
                                        st.markdown("**🔄 Mögliche Zugeständnisse:**")
                                        for concession in concessions:
                                            st.write(f"• {concession}")

            st.markdown("---")
            st.markdown("### 📊 Lieferanten-Übersicht")

            # Preisserie berechnen
            price_series = get_price_series_per_unit(display_df, qty_col)
            if price_series is not None:
                display_df = display_df.assign(_unit_price=price_series)

            # Aggregation
            agg_cols = {}
            if qty_col is not None and qty_col in display_df.columns:
                agg_cols[qty_col] = "sum"
            if "_unit_price" in display_df.columns:
                agg_cols["_unit_price"] = "mean"

            grp = None
            if agg_cols:
                group_by_cols = [c for c in [supplier_col, country_col] if c is not None]
                if group_by_cols:
                    grp = display_df.groupby(group_by_cols, dropna=False).agg(agg_cols).reset_index()

            if grp is not None:
                rename_map = {}
                if supplier_col is not None:
                    rename_map[supplier_col] = "Lieferant"
                if country_col is not None:
                    rename_map[country_col] = "Land"
                if qty_col is not None and qty_col in agg_cols:
                    rename_map[qty_col] = "Menge"
                if "_unit_price" in agg_cols:
                    rename_map["_unit_price"] = "Ø Preis"

                grp = grp.rename(columns=rename_map)
                st.dataframe(grp, use_container_width=True)
            else:
                base_cols = [c for c in [supplier_col, country_col, qty_col] if c is not None and c in display_df.columns]
                if "_unit_price" in display_df.columns:
                    base_cols += ["_unit_price"]

                if base_cols:
                    tbl = display_df[base_cols].copy()
                    rename_map = {}
                    if supplier_col in base_cols:
                        rename_map[supplier_col] = "Lieferant"
                    if country_col in base_cols:
                        rename_map[country_col] = "Land"
                    if qty_col in base_cols:
                        rename_map[qty_col] = "Menge"
                    if "_unit_price" in base_cols:
                        rename_map["_unit_price"] = "Preis"

                    tbl = tbl.rename(columns=rename_map)
                    st.dataframe(tbl, use_container_width=True)
                else:
                    st.info("Keine anzeigbaren Lieferanteninformationen gefunden.")

