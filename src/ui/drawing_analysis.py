"""
📐 EVALUERA - Technische Zeichnungsanalyse
=========================================
Standalone-Modul für die Analyse von technischen Zeichnungen (PDF/Bild)
"""

import streamlit as st
import pandas as pd
from src.ui.theme import section_header, card, COLORS
from src.ui.cards import ExcelLoadingAnimation
from src.core.cbam import gpt_analyze_technical_drawing, gpt_analyze_pdf_drawing, gpt_estimate_material
from src.gpt.cache import cached_gpt_complete_cost_estimate
from src.ui.wizard import create_compact_kpi_row
import json

def render_drawing_analysis_page():
    """Renders the Technical Drawing Analysis page"""
    section_header(
        "Technische Zeichnung analysieren",
        "Laden Sie eine Zeichnung (PDF/Bild) hoch für automatische Erkennung & Kostenschätzung"
    )

    # 1. Upload Section
    uploaded_file = st.file_uploader(
        "Zeichnung hochladen",
        type=["pdf", "png", "jpg", "jpeg"],
        key="drawing_upload"
    )

    if not uploaded_file:
        st.info("👆 Bitte laden Sie eine technische Zeichnung hoch, um zu beginnen.")
        return

    # 2. Analysis Trigger
    if uploaded_file:
        st.success(f"✅ Datei geladen: {uploaded_file.name}")
        
        # Button to start analysis
        if st.button("🔍 Zeichnung analysieren", type="primary", use_container_width=True):
            with ExcelLoadingAnimation("Analysiere Zeichnung mit GPT Vision...", icon="👁️"):
                try:
                    file_bytes = uploaded_file.getvalue()
                    
                    if uploaded_file.type == "application/pdf":
                        result = gpt_analyze_pdf_drawing(file_bytes)
                    else:
                        result = gpt_analyze_technical_drawing(file_bytes, filename=uploaded_file.name)
                    
                    if result.get("ok", False) or result.get("items"): # Check for success (API might return items directly or wrapped)
                         st.session_state.drawing_analysis_result = result
                         st.success("✅ Analyse erfolgreich!")
                    else:
                        st.error(f"❌ Analyse fehlgeschlagen: {result.get('error', 'Unbekannter Fehler')}")
                
                except Exception as e:
                    st.error(f"❌ Ein Fehler ist aufgetreten: {str(e)}")

    # 3. Results Display
    if "drawing_analysis_result" in st.session_state:
        result = st.session_state.drawing_analysis_result
        
        st.markdown("### 📋 Analyse-Ergebnisse")
        
        # Drawing Info
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Zeichnungs-Nr:** {result.get('drawing_number', 'N/A')}")
        with col2:
            st.markdown(f"**Revision:** {result.get('revision', 'N/A')}")
            
        # Items Table
        items = result.get("items", [])
        if items:
            df_items = pd.DataFrame(items)
            st.dataframe(df_items, use_container_width=True, hide_index=True)
            
            # Selection for Cost Estimation
            st.markdown("### 💰 Kostenschätzung")
            
            # Create options for selectbox
            item_options = [f"{i['position']}: {i['description']}" for i in items if 'description' in i]
            
            if not item_options and items:
                 # Fallback if description missing
                 item_options = [f"Pos {i.get('position', idx+1)}" for idx, i in enumerate(items)]
            
            # Add option for all items if there is more than one item
            if len(items) > 1:
                item_options.insert(0, "📦 Gesamtpaket (Alle Bauteile)")

            if item_options:
                selected_item_str = st.selectbox("Bauteil für Kalkulation wählen", options=item_options)
                
                # Find selected item data
                selected_item = None
                is_total_package = False
                
                if selected_item_str == "📦 Gesamtpaket (Alle Bauteile)":
                    is_total_package = True
                    selected_item = items # Truthy value to show inputs
                else:
                    for item in items:
                        # Simple matching logic
                        if f"{item.get('position')}: {item.get('description')}" == selected_item_str:
                            selected_item = item
                            break
                        if f"Pos {item.get('position')}" == selected_item_str: # Fallback match
                            selected_item = item
                            break
                
                if selected_item:
                    col_lot, col_btn = st.columns([1, 2])
                    with col_lot:
                        lot_size = st.number_input("Losgröße", min_value=1, value=1000, step=100)
                    
                    with col_btn:
                        st.write("") # Spacer
                        st.write("") # Spacer
                        if st.button("🚀 Kosten für dieses Bauteil schätzen", type="primary", use_container_width=True):
                                    with ExcelLoadingAnimation("Kalkuliere Kosten...", icon="🧮"):
                                        try:
                                            if is_total_package:
                                                total_mat = 0.0
                                                total_fab = 0.0
                                                details = []
                                                
                                                for item in items:
                                                    # Parse quantity
                                                    try:
                                                        qty = float(str(item.get('quantity', 1)).replace(',', '.').split()[0])
                                                    except:
                                                        qty = 1.0
                                                    
                                                    # Prepare description
                                                    desc = item.get('description', '')
                                                    mat = item.get('material', '')
                                                    dims = f"{item.get('diameter_mm', '')}x{item.get('length_mm', '')}"
                                                    full_desc = f"{desc} {mat} {dims}".strip()
                                                    
                                                    # Calculate effective lot size for this item
                                                    item_lot_size = int(lot_size * qty)
                                                    
                                                    # Call Cost Estimation
                                                    res = cached_gpt_complete_cost_estimate(
                                                        description=full_desc,
                                                        lot_size=item_lot_size
                                                    )
                                                    
                                                    if res and not res.get("_error"):
                                                        # Add to totals (cost per unit * quantity per set)
                                                        mat_cost = res.get('material_cost_eur', 0) * qty
                                                        fab_cost = res.get('fab_cost_eur', 0) * qty
                                                        total_mat += mat_cost
                                                        total_fab += fab_cost
                                                        
                                                        details.append({
                                                            "position": item.get('position'),
                                                            "description": desc,
                                                            "quantity": qty,
                                                            "unit_cost": res.get('material_cost_eur', 0) + res.get('fab_cost_eur', 0),
                                                            "total_cost": mat_cost + fab_cost
                                                        })
                                                
                                                cost_res = {
                                                    "material_cost_eur": total_mat,
                                                    "fab_cost_eur": total_fab,
                                                    "details": details,
                                                    "is_package": True
                                                }
                                                
                                            else:
                                                # Single item logic
                                                # Prepare description from analysis
                                                desc = selected_item.get('description', '')
                                                mat = selected_item.get('material', '')
                                                dims = f"{selected_item.get('diameter_mm', '')}x{selected_item.get('length_mm', '')}"
                                                full_desc = f"{desc} {mat} {dims}".strip()
                                                
                                                # Call Cost Estimation
                                                cost_res = cached_gpt_complete_cost_estimate(
                                                    description=full_desc,
                                                    lot_size=lot_size
                                                )
                                            
                                            if cost_res and not cost_res.get("_error"):
                                                st.session_state.drawing_cost_result = cost_res
                                                st.success("✅ Kalkulation abgeschlossen!")
                                                st.rerun()
                                            else:
                                                st.error("❌ Kalkulation fehlgeschlagen.")
                                                
                                        except Exception as e:
                                            st.error(f"❌ Fehler bei Kalkulation: {e}")

        else:
            st.info("Keine Bauteile in der Zeichnung erkannt.")

    # 4. Cost Result Display (similar to main app but standalone)
    if "drawing_cost_result" in st.session_state:
        res = st.session_state.drawing_cost_result
        
        st.markdown("#### 📊 Kalkulations-Ergebnis")
        
        is_package = res.get('is_package', False)
        unit_label = "€/Paket" if is_package else "€/Stk"
        
        create_compact_kpi_row([
            {
                "label": f"Material {unit_label}",
                "value": f"{res.get('material_cost_eur', 0):,.4f} €",
                "icon": "💎"
            },
            {
                "label": f"Fertigung {unit_label}",
                "value": f"{res.get('fab_cost_eur', 0):,.4f} €",
                "icon": "⚙️"
            },
            {
                "label": "Gesamt (Ziel)",
                "value": f"{(res.get('material_cost_eur', 0) + res.get('fab_cost_eur', 0)):,.4f} €",
                "icon": "🎯"
            }
        ])
        
        if is_package and "details" in res:
            st.markdown("##### 🧾 Einzelkosten-Aufstellung")
            st.dataframe(pd.DataFrame(res["details"]), use_container_width=True)
        
        with st.expander("📋 JSON-Details"):
            st.json(res)
