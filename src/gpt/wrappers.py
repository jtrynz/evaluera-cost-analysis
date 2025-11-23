import traceback
from typing import Any, Dict, Optional
from cost_helpers import (
    gpt_estimate_material as _gpt_estimate_material,
    choose_process_with_gpt as _choose_process_with_gpt,
)

def safe_gpt_estimate_material(sel_text: str) -> Dict[str, Any]:
    try:
        out = _gpt_estimate_material(sel_text) or {}
        if not isinstance(out, dict):
            return {"error": "GPT returned non-dict", "raw": out}
        return out
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}

def safe_choose_process(sel_text: str, mat: Optional[str] = None, d_mm: Optional[float] = None, l_mm: Optional[float] = None, lot_size: int = 1000) -> Dict[str, Any]:
    """
    Wrapper für choose_process_with_gpt mit Fehlerbehandlung.
    Alle Parameter außer sel_text sind optional.
    """
    try:
        out = _choose_process_with_gpt(sel_text, mat or "stahl", d_mm, l_mm, lot_size=lot_size) or {}
        if not isinstance(out, dict):
            return {"error": "GPT returned non-dict", "raw": out}
        return out
    except Exception as e:
        # Fallback mit Standardwerten
        return {
            "process": "cold_forming",
            "setup_time_min": 30,
            "cycle_time_s": 2.0,
            "machine_eur_h": 70,
            "labor_eur_h": 30,
            "overhead_pct": 0.2,
            "error": str(e),
            "trace": traceback.format_exc()
        }
