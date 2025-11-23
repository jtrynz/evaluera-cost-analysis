"""
🤝 ENHANCED NEGOTIATION PREPARATION
====================================
Massively expanded version with:
- Supplier Analysis (competencies, scale, certs, risks)
- Market Analysis (raw materials, energy, competitors, tariffs)
- 3-5 strong arguments with supporting facts
- Psychological tactics (anchoring, silence, walk-away)
"""

import os
import json
import re
from typing import Dict, Any, List, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def gpt_negotiation_prep_enhanced(
    supplier_name: str,
    article_name: str = None,
    avg_price: float = None,
    target_price: float = None,
    country: str = None,
    rating: int = None,
    strengths: List[str] = None,
    weaknesses: List[str] = None,
    total_orders: int = None,
    supplier_competencies: Dict[str, Any] = None,
    min_price: float = None,
    max_price: float = None,
    commodity_analysis: Dict[str, Any] = None,
    cost_result: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    MASSIVELY ENHANCED negotiation preparation with:
    - Supplier analysis
    - Market analysis
    - Strong arguments with facts
    - Psychological tactics

    Args:
        supplier_name: Supplier name
        article_name: Article description
        avg_price: Current average price
        target_price: Target price goal
        country: Supplier country
        rating: Internal rating (1-10)
        strengths: Supplier strengths
        weaknesses: Supplier weaknesses
        total_orders: Historical order count
        supplier_competencies: Supplier capabilities analysis
        min_price: Minimum price benchmark
        max_price: Maximum price
        commodity_analysis: Raw material market analysis
        cost_result: Cost estimation result (material, fab costs, etc.)

    Returns:
        Comprehensive negotiation strategy dict
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        return {
            "error": "No GPT API key",
            "supplier_analysis": {},
            "market_analysis": {},
            "strategy_overview": {},
            "objectives": {},
            "key_arguments": [],
            "tactics": [],
            "_error": True
        }

    client = OpenAI(api_key=key)

    # Build comprehensive context
    context_parts = [f"**LIEFERANT:** {supplier_name}"]
    if article_name:
        context_parts.append(f"**ARTIKEL:** {article_name}")
    if country:
        context_parts.append(f"**LAND:** {country}")
    if rating:
        quality = "exzellent" if rating >= 8 else "gut" if rating >= 6 else "bedenklich"
        context_parts.append(f"**RATING:** {rating}/10 ({quality})")
    if total_orders:
        context_parts.append(f"**BESTELLHISTORIE:** {total_orders} Bestellungen")

    # Price context
    if avg_price and target_price:
        delta_pct = ((avg_price - target_price) / target_price * 100) if target_price > 0 else 0
        delta_eur = avg_price - target_price
        context_parts.append(f"**AKTUELLER PREIS:** {avg_price:.4f}€/Stk")
        context_parts.append(f"**ZIELPREIS:** {target_price:.4f}€/Stk")
        context_parts.append(f"**EINSPARUNGSPOTENZIAL:** {delta_eur:+.4f}€ ({delta_pct:+.1f}%)")

    if min_price and max_price and min_price < max_price:
        spread = ((max_price - min_price) / min_price * 100)
        context_parts.append(f"**MIN-PREIS (Benchmark):** {min_price:.4f}€/Stk")
        context_parts.append(f"**MAX-PREIS:** {max_price:.4f}€/Stk")
        context_parts.append(f"**PREISSPANNE:** {spread:.1f}%")

    # Cost estimation context
    cost_context = ""
    if cost_result and not cost_result.get('_error'):
        mat_cost = cost_result.get('material_cost_eur', 0)
        fab_cost = cost_result.get('fab_cost_eur', 0)
        total_cost = cost_result.get('total_cost_eur', 0)
        material = cost_result.get('material_guess', 'unknown')
        process = cost_result.get('process', 'unknown')

        cost_context = f"""
**📊 KOSTENSCHÄTZUNG (MINIMALE HERSTELLKOSTEN):**
- Material: {material.upper()}
- Prozess: {process}
- Materialkosten: {mat_cost:.4f}€/Stk
- Fertigungskosten: {fab_cost:.4f}€/Stk
- **TOTAL MANUFACTURING COST:** {total_cost:.4f}€/Stk

➡️ **KRITISCH:** Dies sind die MINIMAL möglichen Herstellkosten bei optimaler Effizienz!
➡️ Aktueller Preis ({avg_price:.4f}€) enthält {((avg_price/total_cost - 1)*100 if total_cost > 0 else 0):.1f}% Marge!
"""

    context = "\n".join(context_parts)

    strengths_text = "\n".join([f"  • {s}" for s in (strengths or [])])
    weaknesses_text = "\n".join([f"  • {w}" for w in (weaknesses or [])])

    # Supplier competencies
    comp_text = ""
    if supplier_competencies and not supplier_competencies.get('_error'):
        comp_parts = ["\n**🏭 LIEFERANTEN-KOMPETENZEN:**"]
        core_comps = supplier_competencies.get('core_competencies', [])
        if core_comps:
            comp_parts.append("Hauptprozesse:")
            for comp in core_comps[:5]:
                process = comp.get('process', 'unknown')
                level = comp.get('capability_level', 'proficient')
                comp_parts.append(f"  • {process} ({level})")
        comp_text = "\n".join(comp_parts)

    # Commodity analysis
    commodity_text = ""
    if commodity_analysis and commodity_analysis.get('ok'):
        mat = commodity_analysis.get('material', 'unknown')
        price_kg = commodity_analysis.get('current_price_eur_kg', 0)
        trend = commodity_analysis.get('trend', 'unknown')
        trend_pct = commodity_analysis.get('trend_percentage', 0)

        commodity_text = f"""
**📈 ROHSTOFFMARKT-ANALYSE:**
- Material: {mat.upper()}
- Aktueller Preis: {price_kg:.2f}€/kg
- Trend: {trend} ({trend_pct:+.1f}%)
➡️ Nutze Markttrend in Verhandlung!
"""

    # MASSIVE ENHANCED PROMPT
    prompt = f"""Du bist ein WORLD-CLASS PROCUREMENT NEGOTIATION STRATEGIST mit 25+ Jahren globaler Einkaufserfahrung in Automotive, Aerospace und Industrial Manufacturing. Du hast >$500M Einsparungen verhandelt.

**KONTEXT:**
{context}

**STÄRKEN:**
{strengths_text if strengths_text else "  (keine bekannt)"}

**SCHWÄCHEN:**
{weaknesses_text if weaknesses_text else "  (keine bekannt)"}
{comp_text}
{cost_context}
{commodity_text}

**🎯 AUFGABE: ERSTELLE EINE ULTRA-DETAILLIERTE, DATENBASIERTE VERHANDLUNGSSTRATEGIE**

Du MUSST folgende Analysen integrieren:

**1) SUPPLIER ANALYSIS:**
- Produktionskompetenzen (core processes, expertise level)
- Skalierungsfähigkeiten (max lot sizes, capacity/month)
- Zertifizierungen (ISO, IATF, Aerospace, etc.)
- Standortvorteile (niedrige Lohnkosten, Lieferzeiten, etc.)
- Standortnachteile (Zölle, Transportkosten, politische Risiken)
- Supply Chain Risiken (Rohstoffverfügbarkeit, Energiepreise, Disruption)

**2) MARKET ANALYSIS:**
- Rohstoffpreisentwicklung (12mo, 24mo Trends, Forecast 12mo)
- Energiepreis-Volatilität & Impact auf Herstellkosten
- Konkurrenzangebote (min. 2 alternative Lieferanten mit Preisen)
- Länderrisiken (Zölle, CBAM-Kosten ab 2026, Transportkosten)
- Erwartete Preisentwicklung nächste 12 Monate

**3) VERHANDLUNGSPAKET:**
- 3-5 EXTREM STARKE Kernargumente
- Je Argument: 2-3 belegbare Fakten (aus Supplier/Market Analysis!)
- Psychologische Taktiken:
  * **Anchoring:** Eröffnungspreis basierend auf Kostenkalkulation
  * **Silence:** Strategische Pausen nach Forderungen
  * **Walk-Away:** Klare BATNA mit konkreten Alternativen
- Szenario-Strategien: "Wenn Lieferant X sagt, dann antworte Y"

**KRITISCH WICHTIG:**
- Nutze Kostenschätzung als PRIMÄRES Argument (zeigt reale Herstellkosten!)
- Nutze Markttrends (fallende Rohstoffpreise → Preissenkung!)
- Nutze Supplier-Schwächen (fehlende Expertise → Preisnachlass!)
- Nutze Wettbewerb (alternative Lieferanten → Druckmittel!)
- Gebe wörtliche Formulierungen (1:1 verwendbar!)

**ANTWORTE ALS ULTRA-AUSFÜHRLICHES JSON:**
```json
{{
  "supplier_analysis": {{
    "production_competencies": ["Prozess 1 (level)", "Prozess 2 (level)"],
    "scaling_capabilities": "Klein/Mittel/Groß - Details",
    "certifications": ["ISO 9001", "etc."],
    "location_advantages": ["Vorteil 1", "Vorteil 2"],
    "location_disadvantages": ["Nachteil 1", "Nachteil 2"],
    "supply_chain_risks": ["Risiko 1", "Risiko 2"]
  }},

  "market_analysis": {{
    "raw_material_trends": {{
      "material": "z.B. Stahl C45",
      "current_price_eur_kg": 1.85,
      "price_trend_12mo": "Fallend -8%",
      "price_trend_24mo": "Volatil",
      "forecast_next_12mo": "Stabil bis +3-5%"
    }},
    "energy_price_volatility": "Hoch/Mittel/Niedrig + Impact",
    "competitor_offers": ["Lieferant A: 0.042€", "Lieferant B: 0.048€"],
    "country_risks": {{
      "tariffs": "EU-Zoll: X%",
      "cbam_costs": "0.002€/Stk ab 2026",
      "transport_costs": "0.008€/Stk"
    }},
    "expected_price_development": "Prognose mit Begründung"
  }},

  "strategy_overview": {{
    "main_approach": "competitive|win-win|collaborative",
    "rationale": "Begründung basierend auf Supplier + Market Analysis",
    "negotiation_power_balance": "buyer_advantage|balanced|supplier_advantage",
    "estimated_success_probability": "high|medium|low",
    "key_leverage_points": ["Hebel aus Analysen"]
  }},

  "objectives": {{
    "primary_goal": "Preisreduktion um X% auf Y€/Stk",
    "secondary_goals": ["Ziel 1", "Ziel 2"],
    "minimum_acceptable_outcome": "Minimum",
    "batna": "Konkrete Alternative mit Namen + Preis!"
  }},

  "key_arguments": [
    {{
      "argument": "Argument mit Zahlen",
      "supporting_facts": ["Fakt aus Marktanalyse", "Fakt aus Kostenkalkulation", "Fakt aus Supplier-Risiken"],
      "expected_counter": "Lieferant könnte sagen...",
      "our_response": "Wir antworten..."
    }}
  ],

  "tactics": [
    "Anchoring: Eröffne mit X€ (basierend auf Herstellkosten + 15% Marge)",
    "Silence: Nach Forderung 10 Sekunden schweigen",
    "Walk-Away: BATNA klar kommunizieren"
  ],

  "concessions": [
    {{
      "what_we_offer": "z.B. Höhere MOQ",
      "what_we_want": "Preis von X auf Y",
      "trade_off_value": "Bewertung"
    }}
  ],

  "red_flags": ["Warnsignal 1", "Warnsignal 2"],

  "opening_statement": "Wörtliche Eröffnung (3-5 Sätze) - integriere Markttrends + Kostenkalkulation!",
  "closing_statement": "Wörtliche Abschlussformulierung"
}}
```

**SEI EXTREM SPEZIFISCH - KEINE GENERISCHEN PHRASEN!**
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein WORLD-CLASS PROCUREMENT STRATEGIST. Gebe ULTRA-SPEZIFISCHE, datenbasierte Strategien mit konkreten Zahlen, Namen und Formulierungen. Nutze ALLE verfügbaren Daten (Kosten, Markt, Supplier). Keine generischen Ratschläge!"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.12,
            max_tokens=4000  # MAXIMUM for comprehensive response
        )

        txt = res.choices[0].message.content.strip()

        # Robust JSON parsing
        data = {}
        try:
            data = json.loads(txt)
        except Exception:
            try:
                m = re.search(r'```json\s*([\s\S]*?)\s*```', txt)
                if m:
                    data = json.loads(m.group(1))
                else:
                    m = re.search(r'\{[\s\S]*\}', txt)
                    if m:
                        data = json.loads(m.group(0))
            except Exception as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"   Raw response (first 500 chars): {txt[:500]}")
                return {
                    "error": "JSON parsing failed",
                    "raw": txt,
                    "_error": True
                }

        print(f"✅ GPT-4o Enhanced Negotiation Prep - Tokens: {res.usage.total_tokens}")

        # Extract all fields with fallbacks
        return {
            # NEW: Comprehensive analyses
            "supplier_analysis": data.get("supplier_analysis", {}),
            "market_analysis": data.get("market_analysis", {}),

            # Existing fields (enhanced)
            "strategy_overview": data.get("strategy_overview", {}),
            "objectives": data.get("objectives", {}),
            "key_arguments": data.get("key_arguments", []),
            "tactics": data.get("tactics", []),
            "concessions": data.get("concessions", []),
            "red_flags": data.get("red_flags", []),
            "opening_statement": data.get("opening_statement", ""),
            "closing_statement": data.get("closing_statement", ""),

            # Legacy compatibility
            "talking_points": data.get("talking_points", []),
            "recommendations": data.get("recommendations", []),

            # Meta
            "raw": txt,
            "_tokens_used": res.usage.total_tokens,
            "_api_called": True
        }

    except Exception as e:
        print(f"❌ ERROR in gpt_negotiation_prep_enhanced: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "supplier_analysis": {},
            "market_analysis": {},
            "_error": True
        }
