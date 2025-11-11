"""
Loader Module - Lädt und normalisiert Bestelldaten aus CSV/Excel
"""

import pandas as pd
from typing import Union
import io


def load_orders(uploaded_file) -> pd.DataFrame:
    """
    Lädt Bestelldaten aus hochgeladenem CSV oder Excel File.

    Normalisiert automatisch Spaltennamen und erkennt häufige Aliase.

    Args:
        uploaded_file: Streamlit UploadedFile object oder File-like object

    Returns:
        pd.DataFrame mit normalisierten Spalten

    Erwartete Spalten (oder Aliase):
        - date / datum / bestelldatum
        - supplier / lieferant / anbieter / vendor
        - item / artikel / artikelname / bezeichnung
        - quantity / menge / qty / anzahl / stück / stueck
        - unit_price / einzelpreis / stkpreis / preis_pro_stk / preis
        - currency / waehrung / währung
    """

    # Dateiname ermitteln
    try:
        filename = uploaded_file.name if hasattr(uploaded_file, 'name') else 'unknown'
    except:
        filename = 'unknown'

    # Datei laden (CSV oder Excel)
    try:
        if filename.lower().endswith('.csv'):
            # CSV mit automatischer Delimiter-Erkennung
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        else:
            # Excel
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        raise ValueError(f"Fehler beim Laden der Datei: {e}")

    # Spaltennamen normalisieren (lowercase, strip whitespace)
    df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]

    # Aliase für häufige Spaltennamen
    column_aliases = {
        # Datum
        'datum': 'date',
        'bestelldatum': 'date',
        'order_date': 'date',
        'lieferdatum': 'date',

        # Lieferant
        'lieferant': 'supplier',
        'anbieter': 'supplier',
        'vendor': 'supplier',
        'firma': 'supplier',

        # Artikel
        'artikel': 'item',
        'artikelname': 'item',
        'artikelnummer': 'item',
        'bezeichnung': 'item',
        'produkt': 'item',
        'article': 'item',
        'artnr': 'item',
        'art-nr': 'item',
        'art_nr': 'item',

        # Menge
        'menge': 'quantity',
        'qty': 'quantity',
        'anzahl': 'quantity',
        'stueck': 'quantity',
        'stück': 'quantity',
        'pcs': 'quantity',

        # Preis
        'preis': 'unit_price',
        'einzelpreis': 'unit_price',
        'stkpreis': 'unit_price',
        'stk_preis': 'unit_price',
        'preis_pro_stk': 'unit_price',
        'preis_pro_stueck': 'unit_price',
        'preis_pro_stück': 'unit_price',
        'price': 'unit_price',
        'nettopreis': 'unit_price',
        'netto_preis': 'unit_price',

        # Währung
        'waehrung': 'currency',
        'währung': 'currency',
        'waerung': 'currency',

        # Land
        'land': 'country',
        'herkunft': 'country',
        'ursprung': 'country',
        'origin': 'country',

        # Material (optional)
        'werkstoff': 'material',
        'mat': 'material'
    }

    # Wende Aliase an
    rename_map = {}
    for col in df.columns:
        if col in column_aliases:
            rename_map[col] = column_aliases[col]

    if rename_map:
        df = df.rename(columns=rename_map)

    # Datentypen konvertieren
    # Datum
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Numerische Felder
    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    if 'unit_price' in df.columns:
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

    # String-Felder trimmen
    string_columns = ['supplier', 'item', 'currency', 'country', 'material']
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Entferne Zeilen mit komplett fehlenden Werten
    df = df.dropna(how='all')

    # Optional: Entferne Zeilen ohne kritische Werte (aber nur Warning, nicht komplett löschen)
    # critical_cols = ['item', 'quantity', 'unit_price']
    # missing_critical = df[critical_cols].isna().all(axis=1)
    # if missing_critical.any():
    #     print(f"⚠️ Warnung: {missing_critical.sum()} Zeilen haben fehlende kritische Werte")

    return df


def load_technical_drawing_metadata(uploaded_file) -> pd.DataFrame:
    """
    Lädt Metadaten aus technischer Zeichnung (Excel/CSV).

    Erwartet Spalten wie:
        - Position / Pos
        - Beschreibung / Description / Artikel
        - Menge / Quantity
        - Material
        - Durchmesser / Diameter
        - Länge / Length

    Returns:
        pd.DataFrame mit normalisierten Spalten
    """

    # Lade als normales DataFrame
    try:
        filename = uploaded_file.name if hasattr(uploaded_file, 'name') else 'unknown'
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        raise ValueError(f"Fehler beim Laden: {e}")

    # Normalisiere Spalten
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Aliase für Zeichnungs-Spalten
    aliases = {
        'pos': 'position',
        'pos.': 'position',
        'beschreibung': 'description',
        'artikel': 'description',
        'menge': 'quantity',
        'qty': 'quantity',
        'werkstoff': 'material',
        'mat': 'material',
        'durchmesser': 'diameter',
        'diameter': 'diameter',
        'ø': 'diameter',
        'laenge': 'length',
        'länge': 'length',
        'l': 'length'
    }

    rename_map = {}
    for col in df.columns:
        if col in aliases:
            rename_map[col] = aliases[col]

    if rename_map:
        df = df.rename(columns=rename_map)

    return df
