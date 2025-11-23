"""
GPT UTILITIES
=============
Wiederverwendbare Helper-Funktionen für GPT-Interaktionen.
Reduziert Code-Duplikation massiv (DRY-Prinzip).
"""

import json
import re
import unicodedata
import traceback
from typing import Dict, Any, Optional, Callable


def sanitize_input(text: Any) -> str:
    """Entfernt problematische Unicode-Zeichen (U+2028/2029, Zero-Width, Control) und normalisiert."""
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u2028", " ").replace("\u2029", " ")
    text = re.sub(r"[\u200B-\u200F\uFEFF]", "", text)
    text = re.sub(r"[\x00-\x1F\x7F]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def sanitize_payload_recursive(obj: Any):
    """Sanitizes all strings (keys + values) recursively in payloads for GPT/JSON."""
    if isinstance(obj, dict):
        return {sanitize_input(k): sanitize_payload_recursive(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_payload_recursive(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(sanitize_payload_recursive(v) for v in obj)
    if isinstance(obj, str):
        return sanitize_input(obj)
    return obj


def safe_print(msg: str):
    try:
        print(sanitize_input(msg))
    except Exception:
        try:
            print(sanitize_input(msg).encode("utf-8", errors="ignore").decode("utf-8", errors="ignore"))
        except Exception:
            pass


def safe_gpt_request(
    model: str,
    messages: Any,
    client_factory: Callable[[], Any],
    temperature: float = 0.1,
    max_tokens: int = 2000,
    retries: int = 1,
) -> Dict[str, Any]:
    """
    Führt einen GPT-Request robust aus (UTF-8 safe, Sanitizing, optional Retry).
    Erwartet eine client_factory, die den OpenAI-Client liefert.
    """
    clean_messages = sanitize_payload_recursive(messages)

    # Debug serialization (UTF-8, ensure_ascii=False)
    try:
        _ = json.dumps({"model": model, "messages": clean_messages}, ensure_ascii=False)[:0]
    except Exception as ser_err:
        return {
            "_error": True,
            "error": f"Serialization failed: {ser_err}",
            "trace": traceback.format_exc(),
            "_stage": "serialize",
        }

    last_err = None
    for attempt in range(retries + 1):
        try:
            client = client_factory()
            res = client.chat.completions.create(
                model=model,
                messages=clean_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return {
                "_error": False,
                "response": res,
            }
        except Exception as e:
            last_err = e
            if attempt >= retries:
                return {
                    "_error": True,
                    "error": str(e),
                    "trace": traceback.format_exc(),
                    "_stage": "api_call",
                }
    return {
        "_error": True,
        "error": str(last_err) if last_err else "unknown_error",
        "_stage": "api_call",
    }


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
        text = sanitize_input(text)
        return json.loads(text)
    except Exception:
        pass  # continue

    try:
        # Versuch 2: JSON in ```json ... ``` Code-Block
        match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if match:
            return json.loads(sanitize_input(match.group(1)))
    except Exception:
        pass

    try:
        # Versuch 3: Beliebiges { ... } Pattern
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(sanitize_input(match.group(0)))
    except Exception:
        pass

    # Alles fehlgeschlagen
    try:
        print("WARN JSON Parsing fehlgeschlagen!")
        print(f"   Response (erste 300 chars): {text[:300]}")
    except Exception:
        pass
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
