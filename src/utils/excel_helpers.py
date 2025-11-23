"""
EXCEL HELPER FUNCTIONS
======================
Wiederverwendbare Funktionen für Excel-Verarbeitung.
Eliminiert Code-Duplikation in simple_app.py.
"""

import pandas as pd
from typing import Optional, Tuple, List
from ui_components import GPTLoadingAnimation
from gpt_cache import cached_gpt_article_search
import json


def read_and_normalize_excel(uploaded_file) -> pd.DataFrame:
    """
    Liest und normalisiert Excel/CSV-Datei.

    Args:
        uploaded_file: Streamlit UploadedFile Objekt

    Returns:
        Normalisiertes DataFrame
    """
    name = (uploaded_file.name or "").lower()

    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, sep=None, engine="python")
    else:
        df = pd.read_excel(uploaded_file)

    # Spaltennamen normalisieren
    df.columns = [str(c).strip() for c in df.columns]

    return df


def find_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """
    Findet Spalte basierend auf Kandidaten-Liste.

    Args:
        df: DataFrame
        candidates: Liste möglicher Spaltennamen

    Returns:
        Gefundener Spaltenname oder None
    """
    cols = list(df.columns)
    lower_map = {str(c).lower(): c for c in cols}

    # Exakter Match
    for cand in candidates:
        c = cand.lower()
        if c in lower_map:
            return lower_map[c]

    # Partial Match
    for cand in candidates:
        c = cand.lower()
        for k, v in lower_map.items():
            if c in k:
                return v

    return None


def search_excel_for_article(excel_df: pd.DataFrame,
                             description: str,
                             use_gpt: bool = True) -> Tuple[Optional[pd.DataFrame], Optional[float], Optional[float], Optional[float]]:
    """
    Durchsucht Excel nach Artikel-Beschreibung.

    Args:
        excel_df: Excel DataFrame
        description: Artikel-Beschreibung
        use_gpt: Ob GPT-basierte Suche verwendet werden soll

    Returns:
        Tuple: (matches_df, avg_price, min_price, max_price)
    """
    from price_utils import derive_unit_price

    # Finde Artikel-Spalte
    item_col = find_column(excel_df, ["item", "artikel", "bezeichnung", "produkt"])

    if not item_col:
        return None, None, None, None

    # Intelligente Suche
    if use_gpt and len(excel_df) > 0:
        item_values = excel_df[item_col].tolist()

        # GPT-basierte Suche mit Caching
        with GPTLoadingAnimation("🔍 Suche Artikel in Datenbank...", icon="🤖"):
            items_json = json.dumps(item_values[:500])  # Max 500 für Performance
            matching_indices = cached_gpt_article_search(description, items_json)

        if matching_indices:
            matches_df = excel_df.iloc[matching_indices].copy()
        else:
            # Fallback: String-Suche
            search_mask = excel_df[item_col].astype(str).str.lower().str.contains(
                description.lower(), na=False, regex=False
            )
            matches_df = excel_df[search_mask].copy()
    else:
        # Nur String-Suche
        search_mask = excel_df[item_col].astype(str).str.lower().str.contains(
            description.lower(), na=False, regex=False
        )
        matches_df = excel_df[search_mask].copy()

    if matches_df.empty:
        return None, None, None, None

    # Berechne Preise
    avg_price, min_price, max_price, _, _ = derive_unit_price(matches_df)

    return matches_df, avg_price, min_price, max_price


def get_price_series_per_unit(df: pd.DataFrame, qty_col: Optional[str]) -> Optional[pd.Series]:
    """
    Berechnet Preisserie pro Einheit.

    Args:
        df: DataFrame
        qty_col: Name der Mengen-Spalte

    Returns:
        Series mit Preisen pro Einheit oder None
    """
    # Suche Einzelpreis-Spalte
    price_col = find_column(df, [
        "unit_price", "einzelpreis", "stkpreis", "preis_pro_stk",
        "price", "preis", "avg_price"
    ])

    if price_col is not None:
        return pd.to_numeric(df[price_col], errors="coerce")

    # Fallback: Berechnung aus Total/Qty
    total_col = find_column(df, [
        "rechnungsnettowert", "nettowert", "netto", "betrag",
        "invoice_amount", "amount", "total"
    ])

    if total_col is not None and qty_col is not None:
        total = pd.to_numeric(df[total_col], errors="coerce")
        qty = pd.to_numeric(df[qty_col], errors="coerce").replace(0, pd.NA)
        return total / qty

    return None


def display_excel_matches(matches_df: pd.DataFrame, avg_price: float,
                         min_price: float, max_price: float, context: str = ""):
    """
    Zeigt Excel-Treffer mit Preisstatistiken an.

    Args:
        matches_df: DataFrame mit Treffern
        avg_price: Durchschnittspreis
        min_price: Minimalpreis
        max_price: Maximalpreis
        context: Kontext-String für Anzeige
    """
    import streamlit as st

    st.success(f"✅ **{len(matches_df)} historische Bestellung(en) gefunden{context}**")

    if avg_price is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric("📊 Historischer Ø Preis", f"{avg_price:,.4f} €")
        if min_price:
            c2.metric("Min-Preis", f"{min_price:,.4f} €")
        if max_price:
            c3.metric("Max-Preis", f"{max_price:,.4f} €")

    # Zeige Details in Expander
    with st.expander("📋 Historische Bestellungen", expanded=False):
        # Wähle relevante Spalten
        display_cols = [c for c in matches_df.columns
                       if c in ["item", "supplier", "quantity", "unit_price", "date", "artikel", "lieferant", "menge"]]

        if display_cols:
            st.dataframe(matches_df[display_cols], use_container_width=True)
        else:
            st.dataframe(matches_df, use_container_width=True)
