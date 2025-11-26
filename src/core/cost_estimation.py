"""
OPTIMIZED COST ESTIMATION
=========================
Kombiniert Material-Schätzung + Fertigungskosten in EINEM GPT-Call

VORHER:
1. gpt_estimate_material() → Material/Masse/Geometrie
2. gpt_cost_estimate_unit() → Fertigungskosten
= 2 API-Calls, langsamer, teurer

NACHHER:
1. gpt_complete_cost_estimate() → ALLES in einem!
= 1 API-Call, 50% schneller, günstiger, genauer
"""

import os
import json
import traceback
from typing import Dict, Any, Optional
from src.gpt.utils import (
    parse_gpt_json,
    safe_float,
    sanitize_input,
    sanitize_payload_recursive,
    safe_print,
    safe_gpt_request,
)

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def gpt_complete_cost_estimate(
    description: str,
    lot_size: int = 1000,
    supplier_competencies: Optional[Dict[str, Any]] = None,
    technical_drawing_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    ALL-IN-ONE Kostenschätzung mit einem GPT-Call.

    Schätzt in EINEM Durchgang:
    - Material (Stahl, Edelstahl, Alu, etc.)
    - Geometrie (Durchmesser, Länge, Masse)
    - Materialpreis (€/kg)
    - Fertigungsprozess (cold_forming, turning, etc.)
    - Fertigungskosten (€/Stk)
    - Gesamtkosten (Material + Fertigung)

    Args:
        description: Artikel-Bezeichnung (z.B. "DIN933 M10x30")
        lot_size: Losgröße
        supplier_competencies: Optional Lieferanten-Kontext

    Returns:
        Dict mit allen Kosten-Informationen
    """
    description = sanitize_input(description)

    def _debug_unicode(label: str, text: str):
        try:
            if "\u2028" in text or "\u2029" in text:
                safe_print(f"DEBUG unicode in {label}: contains U+2028/U+2029")
        except Exception:
            pass

    def _debug_unicode(label: str, text: str):
        try:
            if "\u2028" in text or "\u2029" in text:
                safe_print(f"DEBUG unicode in {label}: contains U+2028/U+2029")
        except Exception:
            pass

    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        return {
            "material_guess": "stahl",
            "mass_kg": None,
            "d_mm": None,
            "l_mm": None,
            "material_price_eur_kg": 1.2,
            "material_cost_eur": None,
            "process": "cold_forming",
            "fab_cost_eur": None,
            "total_cost_eur": None,
            "_fallback": True
        }

    safe_print(f"OK GPT-4o ALL-IN-ONE Cost Estimate: {description} @ {lot_size:,} Stk")
    client = OpenAI(api_key=key)

    # Losgrössen-Kontext
    scale_hint = ""
    if lot_size < 100:
        scale_hint = "SEHR KLEIN → hohe Rüstkosten/Stk!"
    elif lot_size < 1000:
        scale_hint = "Klein → moderate Rüstkosten"
    elif lot_size < 10000:
        scale_hint = "Mittel → Rüstkosten gut verteilt"
    elif lot_size < 100000:
        scale_hint = "GROSS → minimale Rüstkosten, Automatisierung"
    else:
        scale_hint = "MASSENPRODUKTION (>100k) → Vollautomatisierung!"

    # Lieferanten-Kontext (falls vorhanden)
    supplier_context = ""
    if supplier_competencies and not supplier_competencies.get('_fallback'):
        comps = supplier_competencies.get('core_competencies', [])
        if comps:
            processes = [c.get('process') for c in comps[:3]]
            supplier_context = f"\n**LIEFERANTEN-EXPERTISE:** {', '.join(sanitize_input(p or '') for p in processes)}"

    # Technische Zeichnung Kontext (falls vorhanden)
    drawing_context_str = ""
    if technical_drawing_context:
        # Extrahiere relevante Infos (Oberfläche, Toleranzen, etc.)
        drawing_context_str = f"\n**TECHNISCHE ZEICHNUNG INFOS:** {json.dumps(technical_drawing_context, ensure_ascii=False)}"

    # KOMBINIERTER PROMPT - Material + Prozess + Kosten (EXTREM GÜNSTIG - WORST CASE)
    prompt = f"""Du bist ein SENIOR COST ENGINEER mit 25+ Jahren Erfahrung in globaler Low-Cost-Beschaffung.

**🎯 KALKULATIONSSTRATEGIE - ABSOLUT MINIMAL REALISTISCH (WORST-CASE FOR SELLER):**

**PFLICHT-ANNAHMEN** für Kalkulation:
✅ **FIND THE MINIMALLY POSSIBLE REALISTIC MANUFACTURING COSTS**
✅ **Assume BEST-CASE EFFICIENCY AT SCALE**
✅ **Assume supplier with HIGHEST AUTOMATION LEVEL**
✅ **Assume LOWEST GLOBAL RAW MATERIAL SPOT PRICE**
✅ **Assume OPTIMIZED CYCLE TIME & MINIMAL SCRAP (<2%)**
✅ **Assume EXPERT SUPPLIER** (wenn expertise vorhanden)

Berechne mit folgenden EXTREM günstigen Parametern:
- **Niedriglohnland:** China/Vietnam/Indien (Lohnkosten: 5-15€/h)
- **Energiekosten:** Minimale Industriepreise (0.06-0.10€/kWh)
- **Vollautomatisierung:** 24/7 Betrieb, >95% Maschinenauslastung
- **Moderne Technologie:** Neueste CNC/Robotik/Industrie 4.0
- **Großabnehmer-Konditionen:** Rohstoff-Spot-Markt, Direktbezug
- **Optimale Materialausnutzung:** Verschnitt <2%, optimierte Blanks
- **Economies of Scale:** Große Losgrößen, minimale Rüstkosten

**KRITISCH WICHTIG:**
- Wähle **IMMER den ABSOLUT UNTEREN BEREICH** plausibler Kosten
- Modelliere **Best-Case-Szenarien** für ALLE Aspekte
- Ziel: Zeige MAXIMALES Einsparungspotenzial für Einkäufer
- Kosten müssen technisch plausibel bleiben (KEINE Fantasiewerte!)
- Denke wie ein Low-Cost-Anbieter in Asien mit modernster Ausstattung

**AUFGABE:** Analysiere den Artikel und berechne KOMPLETTE Kosten (Material + Fertigung) in EINEM Durchgang!

**ARTIKEL:** {description}
**LOSGRÖSSE:** {lot_size:,} Stück ({scale_hint}){supplier_context}{drawing_context_str}

**WAS DU BERECHNEN MUSST:**

1. **MATERIAL-ANALYSE:**
   - Material (stahl/edelstahl_a2/aluminium/messing/etc.)
   - Geometrie (Durchmesser d_mm, Länge l_mm)
   - Masse (mass_kg) - Zylinder-Approximation OK
   - Materialpreis (material_price_eur_kg) - realistisch für EU
   - Materialkosten (material_cost_eur = mass_kg × price_eur_kg)

2. **FERTIGUNGS-ANALYSE:**
   - Prozess (cold_forming/turning/milling/stamping/etc.)
   - Rüstzeit (setup_time_min)
   - Taktzeit (cycle_time_s pro Stück)
   - Maschinenkosten (machine_eur_h)
   - Personalkosten (labor_eur_h)
   - Overhead (overhead_pct, typisch 15-25%)
   - Sekundär-Ops (Wärmebehandlung, Beschichtung, etc.)
   - **Fertigungskosten (fab_cost_eur) berechnet!**

3. **GESAMT-KALKULATION:**
   - total_cost_eur = material_cost_eur + fab_cost_eur

**WICHTIGE REGELN:**

**Material-Erkennung:**
- **WENN TECHNISCHE ZEICHNUNG VORHANDEN:** Verwende das EXAKTE Material aus der Zeichnung (z.B. "FeZnNi", "CuZn39Pb3", etc.) - KEINE Vereinfachung!
- DIN/ISO-Normen beachten
- (Klammern) = Beschichtung, NICHT Material!
- A2/A4 ohne Klammern = Edelstahl
- ST- oder "Stahl" = C-Stahl
- Festigkeitsklassen (8.8, 10.9) = Stahl

**Prozess-Auswahl:**
- Schrauben/Normteile + Losgrösse >1000 → cold_forming
- Custom-Teile oder Kleinserien → turning/milling
- Blechteile → stamping
- Aluminium-Teile → die_casting oder turning

**Kosten-Berechnung:**
```
Rüstkosten/Stk = (setup_time_min / 60 × (machine_eur_h + labor_eur_h)) / lot_size
Variable Kosten = cycle_time_s / 3600 × (machine_eur_h + labor_eur_h)
Fertigung/Stk = (Rüstkosten/Stk + Variable Kosten) × (1 + overhead_pct)
+ Sekundär-Ops (falls vorhanden)
```

**BEISPIEL - M10×30 Schraube, 10000 Stk:**

```json
{{
  "material_guess": "stahl",
  "d_mm": 10.0,
  "l_mm": 30.0,
  "mass_kg": 0.0186,
  "material_price_eur_kg": 1.20,
  "material_cost_eur": 0.0223,

  "process": "cold_forming",
  "setup_time_min": 45,
  "cycle_time_s": 1.8,
  "machine_eur_h": 70,
  "labor_eur_h": 30,
  "overhead_pct": 0.18,
  "secondary_ops": [
    {{"name": "threading", "cost_eur": 0.008}},
    {{"name": "heat_treatment", "cost_eur": 0.012}}
  ],

  "fab_cost_eur": 0.0824,
  "total_cost_eur": 0.1047,

  "confidence": "high",
  "assumptions": [
    "Zylinder-Approximation für Masse",
    "Cold forming für Standard-Schraube",
    "Wärmebehandlung in Charge"
  ]
}}
```

**ANTWORTE NUR ALS KOMPAKTES JSON (alle Felder):**

{{
  "material_guess": "...",
  "d_mm": 0.0,
  "l_mm": 0.0,
  "mass_kg": 0.0,
  "material_price_eur_kg": 0.0,
  "material_cost_eur": 0.0,

  "process": "...",
  "setup_time_min": 0,
  "cycle_time_s": 0.0,
  "machine_eur_h": 0,
  "labor_eur_h": 0,
  "overhead_pct": 0.0,
  "secondary_ops": [...],

  "fab_cost_eur": 0.0,
  "total_cost_eur": 0.0,

  "confidence": "high|medium|low",
  "assumptions": [...]
}}
"""

    try:
        messages = sanitize_payload_recursive([
            {
                "role": "system",
                "content": sanitize_input(
                    "Du bist ein Senior Cost Engineer. Analysiere Artikel und berechne KOMPLETTE Kosten (Material + Fertigung) präzise. Antworte NUR als JSON."
                ),
            },
            {
                "role": "user",
                "content": sanitize_input(prompt),
            },
        ])

        _debug_unicode("prompt", prompt)
        _debug_unicode("description", description)
        _debug_unicode("supplier_context", supplier_context)

        safe_print("DEBUG cost_estimation: messages built, calling OpenAI...")

        api_result = safe_gpt_request(
            model="gpt-4o",
            messages=messages,
            client_factory=lambda: OpenAI(api_key=key),
            temperature=0.1,
            max_tokens=2000,
            retries=1,
        )

        if api_result.get("_error"):
            safe_print(f"ERROR in safe_gpt_request: {api_result}")
            raise RuntimeError(api_result.get("error", "safe_gpt_request failed"))

        response = api_result["response"]

        raw_txt = response.choices[0].message.content or ""
        txt = sanitize_input(raw_txt.strip())
        data = parse_gpt_json(txt, default={})

        # Extrahiere alle Werte mit Fallbacks
        result = {
            # Material
            "material_guess": str(data.get("material_guess", "stahl")).split("|")[0].strip().lower(),
            "d_mm": safe_float(data.get("d_mm")),
            "l_mm": safe_float(data.get("l_mm")),
            "mass_kg": safe_float(data.get("mass_kg")),
            "material_price_eur_kg": safe_float(data.get("material_price_eur_kg"), 1.2),
            "material_cost_eur": safe_float(data.get("material_cost_eur")),

            # Fertigung
            "process": str(data.get("process", "cold_forming")),
            "setup_time_min": safe_float(data.get("setup_time_min"), 30),
            "cycle_time_s": safe_float(data.get("cycle_time_s"), 2.0),
            "machine_eur_h": safe_float(data.get("machine_eur_h"), 70),
            "labor_eur_h": safe_float(data.get("labor_eur_h"), 30),
            "overhead_pct": safe_float(data.get("overhead_pct"), 0.18),
            "secondary_ops": data.get("secondary_ops", []),
            "fab_cost_eur": safe_float(data.get("fab_cost_eur")),

            # Gesamt
            "total_cost_eur": safe_float(data.get("total_cost_eur")),

            # Meta
            "confidence": data.get("confidence", "medium"),
            "assumptions": data.get("assumptions", []),

            # Debug
            "raw": txt,
            "_tokens_used": response.usage.total_tokens,
            "_api_called": True
        }

        # Fallback-Berechnung falls GPT was vergessen hat
        if result["material_cost_eur"] is None and result["mass_kg"] and result["material_price_eur_kg"]:
            result["material_cost_eur"] = result["mass_kg"] * result["material_price_eur_kg"]

        if result["total_cost_eur"] is None:
            mat_cost = result["material_cost_eur"] or 0.0
            fab_cost = result["fab_cost_eur"] or 0.0
            result["total_cost_eur"] = mat_cost + fab_cost

        safe_print(f"OK ALL-IN-ONE Estimate tokens={result.get('_tokens_used')}")
        safe_print(f"Material: {result.get('material_cost_eur')} | Fertigung: {result.get('fab_cost_eur')} | TOTAL: {result.get('total_cost_eur')}")

        return result

    except Exception as e:
        safe_print(f"ERROR in gpt_complete_cost_estimate: {e!r}")
        return {
            "material_guess": "stahl",
            "error": str(e),
            "error_trace": traceback.format_exc(),
            "_error": True,
            "_debug_prompt_present": ("\u2028" in prompt) or ("\u2029" in prompt),
            "_debug_description": description,
            "_debug_supplier_context": supplier_context,
            "_debug_messages": messages if 'messages' in locals() else None,
        }
