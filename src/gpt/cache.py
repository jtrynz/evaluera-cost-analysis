"""
GPT CACHING LAYER
=================
Zentrales Caching für alle GPT-Calls zur massiven Token-Reduktion.
Nutzt Streamlit's @st.cache_data für Session-übergreifendes Caching.
"""

import streamlit as st
import hashlib
import json
from typing import Any, Dict, List, Optional, Callable


def _make_hashable(obj: Any) -> str:
    """Konvertiert beliebige Objekte zu hashbaren Strings."""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return str(obj)
    elif isinstance(obj, (list, tuple)):
        return json.dumps(obj, sort_keys=True)
    elif isinstance(obj, dict):
        return json.dumps(obj, sort_keys=True)
    else:
        return str(obj)


def _cache_key(*args, **kwargs) -> str:
    """Generiert eindeutigen Cache-Key aus Funktionsargumenten."""
    key_parts = [_make_hashable(arg) for arg in args]
    key_parts.extend([f"{k}:{_make_hashable(v)}" for k, v in sorted(kwargs.items())])
    combined = "|".join(key_parts)
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


@st.cache_data(ttl=3600, show_spinner=False)
def cached_gpt_estimate_material(description: str) -> Dict[str, Any]:
    """
    Gecachte Material-Schätzung.
    TTL: 1 Stunde - Material ändert sich nicht!

    DEPRECATED: Verwende cached_gpt_complete_cost_estimate() für bessere Performance!
    """
    from src.core.cbam import gpt_estimate_material
    return gpt_estimate_material(description)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_gpt_complete_cost_estimate(description: str, lot_size: int,
                                      supplier_competencies_json: Optional[str] = None) -> Dict[str, Any]:
    """
    ALL-IN-ONE Kostenschätzung mit Caching.
    Kombiniert Material + Fertigungskosten in EINEM GPT-Call!

    TTL: 1 Stunde
    50% schneller & günstiger als 2 separate Calls!

    Args:
        description: Artikel-Bezeichnung
        lot_size: Losgröße
        supplier_competencies_json: JSON-String (für Hashability)

    Returns:
        Komplette Kostenschätzung (Material + Fertigung)
    """
    from src.core.cost_estimation import gpt_complete_cost_estimate

    # Deserialize supplier_competencies
    supplier_competencies = None
    if supplier_competencies_json:
        supplier_competencies = json.loads(supplier_competencies_json)

    return gpt_complete_cost_estimate(description, lot_size, supplier_competencies)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_choose_process(description: str, material: str, d_mm: Optional[float],
                          l_mm: Optional[float], lot_size: int) -> Dict[str, Any]:
    """
    Gecachte Prozess-Auswahl.
    TTL: 1 Stunde
    """
    from src.core.cbam import choose_process_with_gpt
    return choose_process_with_gpt(description, material, d_mm, l_mm, lot_size)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_gpt_analyze_supplier(supplier_name: str, article_history_json: str,
                                country: Optional[str]) -> Dict[str, Any]:
    """
    Gecachte Lieferanten-Analyse.
    article_history als JSON-String für Hashability.
    TTL: 1 Stunde - Lieferanten-Kompetenzen ändern sich selten!
    """
    from src.core.cbam import gpt_analyze_supplier_competencies
    article_history = json.loads(article_history_json) if article_history_json else None
    return gpt_analyze_supplier_competencies(supplier_name, article_history, country)


@st.cache_data(ttl=1800, show_spinner=False)
def cached_gpt_article_search(query: str, items_json: str) -> List[int]:
    """
    Gecachte Artikel-Suche.
    items als JSON-String für Hashability.
    TTL: 30 Minuten (kürzer weil sich Suche öfter ändert)
    """
    from src.gpt.engine import gpt_intelligent_article_search
    items = json.loads(items_json)
    return gpt_intelligent_article_search(query, items)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_gpt_technical_drawing(image_hash: str, image_data: bytes, filename: str) -> Dict[str, Any]:
    """
    Gecachte Zeichnungsanalyse.
    image_hash für eindeutige Identifikation.
    TTL: 1 Stunde
    """
    from src.core.cbam import gpt_analyze_technical_drawing
    return gpt_analyze_technical_drawing(image_data, filename)


@st.cache_data(ttl=3600, show_spinner=False)
def cached_gpt_rate_supplier(supplier_name: str, country: Optional[str],
                            price_volatility: Optional[float], total_orders: Optional[int],
                            avg_price: Optional[float], article_name: Optional[str]) -> Dict[str, Any]:
    """
    Gecachte Lieferanten-Bewertung.
    TTL: 1 Stunde
    """
    from src.core.cbam import gpt_rate_supplier
    return gpt_rate_supplier(supplier_name, country, price_volatility,
                           total_orders, avg_price, article_name)


def clear_all_caches():
    """Löscht alle GPT-Caches (z.B. bei neuen Daten)."""
    st.cache_data.clear()


# Cache-Statistiken
_cache_hits = 0
_cache_misses = 0


def get_cache_stats() -> Dict[str, int]:
    """Gibt Cache-Statistiken zurück."""
    return {
        "hits": _cache_hits,
        "misses": _cache_misses,
        "hit_rate": _cache_hits / max(_cache_hits + _cache_misses, 1)
    }
