"""
GPT UTILITIES
=============
Wiederverwendbare Helper-Funktionen für GPT-Interaktionen.
Reduziert Code-Duplikation massiv (DRY-Prinzip).
"""

import json
import re
from typing import Dict, Any, Optional


def parse_gpt_json(text: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Robustes JSON-Parsing aus GPT-Responses.
    Versucht mehrere Extraktionsmethoden.

    Args:
        text: GPT Response Text
        default: Fallback-Dict bei Parsing-Fehler

    Returns:
        Geparste JSON-Dict oder default
    """
    if default is None:
        default = {}

    def _clean(t: str) -> str:
        return (t or "").replace("\u2028", " ").replace("\u2029", " ")

    try:
        text = _clean(text)
        # Versuch 1: Ganzer Text ist JSON
        return json.loads(text)
    except Exception:
        pass

    try:
        # Versuch 2: JSON in ```json ... ``` Code-Block
        match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if match:
            return json.loads(_clean(match.group(1)))
    except Exception:
        pass

    try:
        # Versuch 3: Beliebiges { ... } Pattern
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(_clean(match.group(0)))
    except Exception:
        pass

    # Alles fehlgeschlagen
    print(f"⚠️ JSON Parsing fehlgeschlagen!")
    print(f"   Response (erste 300 chars): {text[:300]}")
    return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """Sichere Float-Konvertierung mit Fallback."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """Sichere Int-Konvertierung mit Fallback."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def extract_material_from_gpt(data: Dict[str, Any], default: str = "stahl") -> str:
    """
    Extrahiert Material aus GPT-Response.
    Bereinigt Material-String (nur ersten Wert nehmen).
    """
    material = data.get("material_guess", data.get("material", default))
    # Wenn Format "stahl|edelstahl|..." → nur erstes nehmen
    material = str(material).split("|")[0].strip().lower()
    return material if material else default


def create_error_response(error: Exception, error_type: str = None) -> Dict[str, Any]:
    """
    Erstellt standardisierte Error-Response für GPT-Calls.

    Args:
        error: Exception-Objekt
        error_type: Optionaler Error-Typ (z.B. "material_estimation")

    Returns:
        Error-Dict mit standardisierten Feldern
    """
    import traceback

    return {
        "error": str(error),
        "error_trace": traceback.format_exc(),
        "error_type": error_type or type(error).__name__,
        "_error": True,
        "_fallback": False
    }


def validate_json_fields(data: Dict[str, Any], required_fields: list) -> bool:
    """
    Validiert ob alle erforderlichen Felder in JSON vorhanden sind.

    Args:
        data: Geparste JSON-Dict
        required_fields: Liste erforderlicher Feldnamen

    Returns:
        True wenn alle Felder vorhanden, sonst False
    """
    return all(field in data for field in required_fields)


def log_gpt_call(function_name: str, tokens_used: int = None, success: bool = True):
    """
    Loggt GPT-API-Call für Debugging.

    Args:
        function_name: Name der GPT-Funktion
        tokens_used: Anzahl verwendeter Tokens
        success: Ob Call erfolgreich war
    """
    status = "✅" if success else "❌"
    tokens_info = f" - {tokens_used} Tokens" if tokens_used else ""
    print(f"{status} GPT-Call: {function_name}{tokens_info}")
