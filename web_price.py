"""
Web Price Module - Material-Erkennung und Marktpreise
"""

import re


def guess_material_from_text(text: str) -> str:
    """
    Errät Material basierend auf Textbezeichnung.

    Returns:
        Material-String wie "stahl", "edelstahl_a2", "aluminium", etc.
    """
    if not text:
        return "stahl"

    text_lower = str(text).lower()

    # Edelstahl (muss VOR normalem Stahl geprüft werden!)
    if "edelstahl" in text_lower or "inox" in text_lower or "stainless" in text_lower:
        if "a4" in text_lower or "1.4401" in text_lower or "1.4404" in text_lower:
            return "edelstahl_a4"
        elif "a2" in text_lower or "1.4301" in text_lower or "1.4307" in text_lower:
            # WICHTIG: Nur wenn NICHT in Klammern und kein "ST-" davor!
            if not re.search(r'\(.*a2.*\)', text_lower) and "st-" not in text_lower:
                return "edelstahl_a2"
        return "edelstahl_a2"  # Default Edelstahl

    # Aluminium
    if "alu" in text_lower or "aluminium" in text_lower or "aluminum" in text_lower:
        return "aluminium"

    # Messing
    if "messing" in text_lower or "brass" in text_lower or "cuzn" in text_lower or "ms58" in text_lower:
        return "messing"

    # Kupfer
    if "kupfer" in text_lower or "copper" in text_lower:
        return "kupfer"

    # Titan
    if "titan" in text_lower or "titanium" in text_lower:
        return "titan"

    # Kunststoff
    if any(plastic in text_lower for plastic in ["pa6", "pa66", "pom", "peek", "ptfe", "kunststoff", "plastic"]):
        return "kunststoff"

    # Stahl (Default)
    if "stahl" in text_lower or "steel" in text_lower or "st-" in text_lower:
        return "stahl"

    # Festigkeitsklassen deuten auf Stahl hin
    if any(grade in text_lower for grade in ["8.8", "10.9", "12.9", "5.6", "4.6"]):
        return "stahl"

    # Default: Stahl
    return "stahl"


def get_market_price_for_material(material: str, item_description: str = None) -> float:
    """
    Gibt Marktpreis für Material zurück (€/kg).

    Diese Funktion nutzt entweder:
    1. TradingEconomics API (wenn verfügbar)
    2. Hardcoded Durchschnittswerte (Fallback)

    Args:
        material: Material-String (z.B. "stahl", "edelstahl_a2", etc.)
        item_description: Optionale Artikelbezeichnung für bessere Schätzung

    Returns:
        Preis in EUR/kg
    """

    # Normalisiere Material-String
    material_lower = str(material or "stahl").lower()

    # Marktpreise (Stand 2024/2025 - Durchschnittswerte EU)
    # Quelle: TradingEconomics, LME (London Metal Exchange), etc.
    market_prices = {
        "stahl": 1.20,              # C-Stahl, Durchschnitt
        "steel": 1.20,
        "edelstahl": 3.00,          # Edelstahl generisch
        "edelstahl_a2": 3.20,       # A2 (1.4301)
        "edelstahl_a4": 3.80,       # A4 (1.4401) säurebeständig
        "stainless_steel": 3.20,
        "inox": 3.20,
        "aluminium": 2.50,          # Aluminium
        "aluminum": 2.50,
        "alu": 2.50,
        "messing": 7.50,            # Messing (CuZn)
        "brass": 7.50,
        "kupfer": 8.00,             # Kupfer
        "copper": 8.00,
        "zink": 2.30,               # Zink
        "zinc": 2.30,
        "nickel": 18.00,            # Nickel
        "titan": 35.00,             # Titan (sehr teuer!)
        "titanium": 35.00,
        "kunststoff": 2.80,         # Kunststoff (Durchschnitt PA6/POM)
        "plastic": 2.80,
    }

    # Versuche exakten Match
    if material_lower in market_prices:
        return market_prices[material_lower]

    # Fuzzy Matching
    for key, price in market_prices.items():
        if key in material_lower or material_lower in key:
            return price

    # Festigkeitsklassen → Stahl mit Aufschlag
    if item_description:
        desc_lower = str(item_description).lower()
        if "10.9" in desc_lower or "12.9" in desc_lower:
            return 1.40  # Vergüteter Stahl ist etwas teurer
        elif "8.8" in desc_lower:
            return 1.25

    # Default: Standard-Stahl
    return 1.20


def get_material_price_from_tradingeconomics(material: str) -> float:
    """
    PLACEHOLDER für TradingEconomics API Integration.

    Für echte Marktdaten benötigen Sie:
    1. TradingEconomics API Key
    2. pip install tradingeconomics
    3. Implementierung des API-Calls

    Kosten: Ca. $50-250/Monat je nach Plan

    Returns:
        Aktueller Marktpreis in EUR/kg (oder Fallback-Wert)
    """
    import os

    api_key = os.getenv("TRADINGECONOMICS_API_KEY")

    if not api_key:
        # Fallback auf hardcoded Werte
        return get_market_price_for_material(material)

    # TODO: Implementiere echten API-Call
    # import tradingeconomics as te
    # te.login(api_key)
    # data = te.getHistoricalData(country='EU', indicator='steel')
    # return data['Value'].iloc[-1] / 1000  # Von USD/ton zu EUR/kg

    # Für jetzt: Fallback
    return get_market_price_for_material(material)
