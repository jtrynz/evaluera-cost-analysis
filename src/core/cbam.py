import os, re, json, math, requests, base64, io
from typing import Optional, Dict, Any, List

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

try:
    from PIL import Image
except Exception:
    Image = None

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

_DENSITY = {
    "stahl": 7.85, "steel": 7.85, "a2": 7.9, "a4": 7.9, "edelstahl": 7.9, "inox": 7.9,
    "alu": 2.7, "aluminium": 2.7, "aluminum": 2.7,
    "messing": 8.5, "brass": 8.5,
    "kupfer": 8.96, "copper": 8.96,
    "zink": 7.14, "zinc": 7.14,
    "nickel": 8.9
}

_TE_MAP = {
    "stahl":"steel","steel":"steel","a2":"steel","a4":"steel","edelstahl":"steel","inox":"steel",
    "alu":"aluminum","aluminium":"aluminum","aluminum":"aluminum",
    "messing":"copper","brass":"copper","kupfer":"copper","copper":"copper",
    "zink":"zinc","zinc":"zinc",
    "nickel":"nickel"
}

def density_g_cm3(material: str) -> float:
    if not material:
        return 7.85
    return _DENSITY.get(str(material).lower(), 7.85)

def parse_dims(text: str):
    if not text:
        return None, None
    s = str(text).lower().replace("×","x").replace("*","x").replace("–","-").replace("—","-")
    m = re.search(r"m\s*([0-9]+(?:\.[0-9]+)?)\s*[x-]\s*([0-9]+(?:\.[0-9]+)?)", s)
    if m:
        try: return float(m.group(1)), float(m.group(2))
        except: pass
    m2 = re.search(r"\b([0-9]+(?:\.[0-9]+)?)\s*(?:mm)?\s*[x-]\s*([0-9]+(?:\.[0-9]+)?)\b", s)
    if m2:
        try: return float(m2.group(1)), float(m2.group(2))
        except: pass
    md = re.search(r"(?:\bd\b|ø|dia)[:=\s]*([0-9]+(?:\.[0-9]+)?)", s)
    ml = re.search(r"(?:\bl\b|length)[:=\s]*([0-9]+(?:\.[0-9]+)?)", s)
    d = float(md.group(1)) if md else None
    l = float(ml.group(1)) if ml else None
    return d, l

def clamp_dims(d: Optional[float], l: Optional[float]):
    def _c(v, lo, hi):
        if v is None: return None
        return max(lo, min(hi, v))
    return _c(d, 1.0, 2000.0), _c(l, 1.0, 5000.0)

def mass_cylindrical_approx(d_mm: Optional[float], l_mm: Optional[float], material: str = "stahl") -> Optional[float]:
    if d_mm is None or l_mm is None:
        return None
    r_mm = d_mm/2.0
    vol_mm3 = math.pi * (r_mm**2) * l_mm
    vol_cm3 = vol_mm3 / 1000.0
    return vol_cm3 * density_g_cm3(material) / 1000.0

def get_material_price_eurkg(material: str) -> float:
    key = os.getenv("TRADINGECONOMICS_CLIENTKEY","")
    sym = _TE_MAP.get(str(material or "").lower(), "steel")
    url = f"https://api.tradingeconomics.com/commodities/{sym}?c={key}"
    try:
        r = requests.get(url, timeout=8)
        if r.ok:
            js = r.json()
            if isinstance(js, list) and js:
                p = float(js[0].get("price", 0.0))
                return p / 1000.0
    except Exception:
        pass
    defaults = {"steel":1.2,"aluminum":2.5,"copper":8.0,"zinc":2.3,"nickel":18.0}
    return defaults.get(sym, 1.0)

def gpt_estimate_material(description: str) -> Dict[str, Any]:
    """
    Schätzt Material, Masse und Abmessungen mit GPT-4o.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        print("⚠️ WARNING: FALLBACK - Kein API Key oder OpenAI nicht verfügbar!")
        return {"material_guess":"stahl","mass_kg":None,"d_mm":None,"l_mm":None,"raw":None,"_fallback":True}

    print(f"✅ GPT-4o API-Call: gpt_estimate_material()")
    print(f"   API Key verfügbar: {key[:20]}...{key[-4:]}")
    client = OpenAI(api_key=key)

    prompt = f"""Du bist ein HOCHSPEZIALISIERTER Maschinenbau-Ingenieur und Normteile-Experte mit 25+ Jahren Erfahrung in Präzisions-Kostenkalkulation.

**KRITISCH WICHTIG:** Diese Analyse wird für ECHTE Einkaufsentscheidungen verwendet. ABSOLUTE PRÄZISION ist erforderlich!

**AUFGABE:** Analysiere die Artikelbezeichnung und berechne EXAKTE Material- und Geometriedaten mit vollständiger mathematischer Begründung!

**ARTIKELBEZEICHNUNG:** {description}

**REFERENZ-BEISPIELE FÜR PRÄZISION (so genau musst du sein!):**

Beispiel 1: ISO 4028-10.9-(ZN-NI)-M10×1,25×45
Interpretation:
- ISO 4028 = Madenschraube (set screw, flacher Punkt)
- 10.9 = vergüteter Stahl (Festigkeitsklasse)
- ZN-NI = Zink-Nickel-Beschichtung (in Klammern!)
- M10 = Gewindedurchmesser 10 mm
- 1,25 = Feingewinde-Steigung
- 45 = Länge 45 mm
→ Material: **STAHL** (vergütet), Dichte: 7.85 g/cm³

Beispiel 2: DIN933-ST-(A2K)-M8×25
Interpretation:
- DIN933 = Sechskantschraube Vollgewinde
- ST = Stahl (explizit!)
- (A2K) = A2K-Beschichtung (Zink-Nickel) in Klammern!
- M8 = Gewindedurchmesser 8 mm
- 25 = Länge 25 mm
→ Material: **STAHL** (C-Stahl), Dichte: 7.85 g/cm³, Oberfläche: A2K
→ **NICHT Edelstahl A2!** (wegen "ST-" und Klammern)

Beispiel 3: DIN934-A2-70-M10
Interpretation:
- DIN934 = Sechskantmutter
- A2-70 = Edelstahl A2 (1.4301) mit Festigkeit 70 (OHNE Klammern!)
- M10 = Gewindedurchmesser 10 mm
→ Material: **EDELSTAHL_A2**, Dichte: 7.90 g/cm³, KEINE Beschichtung

PRÄZISE BERECHNUNG (als Vollzylinder):
1. Volumen: V = π × r² × L = π × (5 mm)² × 45 mm = 3534 mm³ = 3,534 cm³
2. Masse: m = V × ρ = 3,534 cm³ × 7,85 g/cm³ = 27,74 g = 0,02774 kg
3. Materialpreis: 1,40 €/kg (vergüteter Stahl 10.9 nach Wärmebehandlung)
4. Materialkosten: 0,02774 kg × 1,40 €/kg = 0,0388 € / Stk

→ **DU MUSST DIESE PRÄZISION ERREICHEN!**

**DEIN TEIL ZUM ANALYSIEREN:** {description}

**WICHTIGE NORMEN & TEILE-TYPEN:**

**SCHRAUBEN:**
- DIN933 / ISO 4017 = Sechskantschraube Vollgewinde
- DIN931 / ISO 4014 = Sechskantschraube Teilgewinde
- DIN912 / ISO 4762 = Zylinderkopfschraube (Innensechskant)
- DIN913 = Gewindestift mit Innensechskant (Madenschraube)
- DIN963 / ISO 2009 = Senkschraube mit Schlitz
- DIN965 / ISO 7046 = Senkschraube Kreuzschlitz (Phillips)
- DIN7991 / ISO 10642 = Senkschraube Innensechskant
- DIN603 / ISO 8677 = Flachrundschraube (Schlossschraube)
- DIN571 = Holzschraube (Sechskantkopf)

**MUTTERN:**
- DIN934 / ISO 4032 = Sechskantmutter
- DIN985 / ISO 10511 = Sechskantmutter mit Kunststoffring (Stoppmutter)
- DIN439 = Sechskantmutter niedrige Form
- DIN1587 = Hutmutter (Überwurfmutter)
- DIN928 = Schweißmutter (Vierkant)
- DIN6923 = Sechskantmutter mit Flansch

**SCHEIBEN:**
- DIN125 / ISO 7089 = Scheibe (Unterlegscheibe)
- DIN127 / ISO 7090 = Federscheibe (Sicherungsscheibe)
- DIN6798 = Zahnscheibe (Fächerscheibe)
- DIN9021 / ISO 7093 = Scheibe mit großem Außendurchmesser (Karosseriescheibe)

**BOLZEN & STIFTE:**
- DIN1444 = Gewindestange
- DIN7 / ISO 2338 = Zylinderstift (Passstift)
- DIN1 / ISO 2339 = Kegelstifte
- DIN94 = Splinte

**NIETE:**
- DIN660 = Halbrundniet
- DIN661 = Senkniet

**GEWINDE:**
- M3, M4, M5, M6, M8, M10, M12, M16, M20, M24, M30 = Metrische Regelgewinde (Durchmesser in mm)
- M10x1.25 = Feingewinde (Durchmesser × Steigung)

**FESTIGKEITSKLASSEN (Schrauben):**
- 4.6, 5.6, 8.8, 10.9, 12.9 = Stahl (8.8 Standard, 10.9/12.9 hochfest)
- A2-70, A4-80 = Edelstahl (A2 Standard, A4 säurebeständig)

**MATERIALIEN:**
- Stahl: C-Stahl, Automatenstahl
- Edelstahl: A2 (1.4301 / AISI 304), A4 (1.4401 / AISI 316)
- Aluminium: AlMg3, AlMg5
- Messing: CuZn39Pb3 (Ms58)
- Kunststoff: PA6, PA66, POM

**OBERFLÄCHENBEHANDLUNG:**
- VZ / verzinkt = Galvanisch verzinkt
- feuerverzinkt / sendzimir = Feuerverzinkung
- blank = Unbehandelt
- brüniert = Schwarz oxydiert
- vernickelt = Nickelschicht
- galvanisch = Galvanik generell
- gelb verzinkt, blau verzinkt = Chromatierung
- A2K = Zink-Nickel-Beschichtung (NICHT Edelstahl A2!)
- ZN-NI = Zink-Nickel-Beschichtung

🚨🚨🚨 **ULTRA-KRITISCH: MATERIAL VS. OBERFLÄCHENBEHANDLUNG** 🚨🚨🚨

**DU WIRST DIESEN FEHLER NIEMALS MACHEN:**
A2K ist NIEMALS Edelstahl A2! A2K ist eine Zink-Nickel-Beschichtung auf STAHL!

**ABSOLUT EINDEUTIGE REGELN - KEINE AUSNAHMEN:**

1. **KLAMMERN = BESCHICHTUNG**
   - "(A2K)" → Beschichtung auf Stahl
   - "(ZN-NI)" → Beschichtung auf Stahl
   - "(VZ)" → Verzinkung auf Stahl
   - Material ist IMMER Stahl (7.85 g/cm³), NIEMALS Edelstahl!

2. **"ST-" PREFIX = STAHL**
   - "ST-(A2K)" → Stahl mit A2K-Beschichtung
   - "ST-VZ" → Stahl verzinkt
   - "ST-blank" → Stahl unbehandelt
   - Material: STAHL (7.85 g/cm³), Oberfläche: siehe Klammer

3. **NUR OHNE KLAMMERN = EDELSTAHL**
   - "A2-70" → Edelstahl A2 (7.90 g/cm³), KEINE Beschichtung
   - "A4-80" → Edelstahl A4 (7.90 g/cm³), KEINE Beschichtung
   - "1.4301" → Edelstahl A2 (Werkstoffnummer)
   - NUR wenn KEIN "ST-" Prefix UND KEINE Klammern!

4. **TEST: Wenn DU UNSICHER bist:**
   - Siehst du Klammern? → STAHL mit Beschichtung
   - Siehst du "ST-"? → STAHL
   - Siehst du "verzinkt", "galvanisch", "beschichtet"? → STAHL
   - Nur wenn NICHTS davon UND "A2" oder "A4" steht → Edelstahl

**BEISPIELE - LERNE SIE AUSWENDIG:**
- ❌ FALSCH: "ST-(A2K)" → Edelstahl A2
- ✅ RICHTIG: "ST-(A2K)" → Stahl (7.85 g/cm³) + A2K-Beschichtung
- ❌ FALSCH: "(ZN-NI)" → Irgendein Material
- ✅ RICHTIG: "(ZN-NI)" → Stahl (7.85 g/cm³) + Zink-Nickel-Beschichtung
- ✅ RICHTIG: "A2-70" → Edelstahl A2 (7.90 g/cm³), keine Beschichtung
- ✅ RICHTIG: "DIN933-A2-M8" → Edelstahl A2, keine Beschichtung

**UNTERSCHEIDUNGSREGEL:**
1. "ST-" oder "Stahl" im Namen → Grundmaterial ist STAHL (C-Stahl)
2. "(Buchstaben+Zahlen)" in Klammern → Oberflächenbehandlung auf STAHL
3. "A2" oder "A4" OHNE Klammern und OHNE "ST-" → Edelstahl
4. Bei Zweifel: Prüfe ob Beschichtung (verzinkt, galvanisch) angegeben → dann Stahl!

**GEWICHTSBERECHNUNG - ABSOLUTE PRÄZISION ERFORDERLICH!**

**GRUNDREGEL:** Berechne IMMER mit exakter Formel, NICHT mit Schätzwerten!

**Berechnungsmethodik:**

1. **Vollzylinder-Approximation** (für einfache Teile):
   - Volumen: V = π × r² × L (in mm³)
   - Masse: m = V × Dichte / 1000 (in Gramm)
   - Beispiel M10×45: V = π × 5² × 45 = 3534 mm³ → 27,74 g

2. **Schrauben mit Kopf:**
   - Kopf-Volumen (Sechskant): V_kopf = (Schlüsselweite/2)² × π × Kopfhöhe × 0.85
   - Schaft-Volumen: V_schaft = π × (d/2)² × (Länge - Kopfhöhe)
   - Gewinde-Reduktion: -15% wegen Kerben
   - Gesamt: V_total = V_kopf + V_schaft × 0.85

3. **Muttern:**
   - Außen-Volumen: V_außen = (Schlüsselweite/2)² × π × Höhe × 0.85
   - Gewindeloch-Abzug: -40% für Kernloch
   - Netto: V_netto = V_außen × 0.60

**REALISTISCHE GEWICHTS-REFERENZEN (Stahl 7,85 g/cm³):**
- M6×20 Schraube: 5,2 g (berechnet: π×3²×20×0.85 = 481 mm³ = 3,78 g + Kopf ~1,5 g)
- M8×30 Schraube: 13,5 g
- M10×30 Schraube: 20,1 g (Zylinder: π×5²×30 = 2356 mm³ = 18,5 g + Kopf)
- M10×45 Madenschraube: 27,74 g (Vollzylinder ohne Kopf!)
- M12×40 Schraube: 38,2 g
- M16×50 Schraube: 85,3 g

**MATERIALPREISE (realistisch für industrielle Beschaffung):**
- Standard-Stahl C-Stahl (4.6, 5.6): 0,90-1,10 €/kg
- Vergüteter Stahl (8.8): 1,20-1,35 €/kg
- Hochfester Stahl (10.9, 12.9): 1,35-1,50 €/kg
- Edelstahl A2 (1.4301): 2,80-3,20 €/kg
- Edelstahl A4 (1.4401): 3,50-4,00 €/kg
- Aluminium AlMg3: 2,20-2,60 €/kg
- Messing CuZn39: 7,50-8,50 €/kg

**Antworte als DETAILLIERTES JSON mit ALLEN Berechnungsschritten:**
{{
  "material_guess": "stahl|edelstahl_a2|edelstahl_a4|aluminium|messing",
  "mass_kg": 0.02774,
  "diameter_mm": 10,
  "length_mm": 45,
  "confidence": "high|medium|low",

  "part_identification": {{
    "part_type": "set_screw|bolt|screw|nut|washer|pin|rivet|stud",
    "standard": "ISO 4028",
    "description": "Madenschraube mit flachem Punkt",
    "din_equivalent": "DIN 913 / DIN 916"
  }},

  "geometry_details": {{
    "thread_size": "M10",
    "thread_pitch_mm": 1.25,
    "thread_type": "feingewinde",
    "nominal_length_mm": 45,
    "nominal_diameter_mm": 10,
    "head_type": "none|hexagon|cylindrical|countersunk",
    "head_dimensions": "Ohne Kopf (Madenschraube) oder Schlüsselweite XX mm",
    "drive_type": "slot|hex_socket|phillips|torx"
  }},

  "material_details": {{
    "base_material": "stahl",
    "material_grade": "10.9",
    "strength_class": "10.9 = vergüteter Stahl, Rm=1000 MPa",
    "density_g_cm3": 7.85,
    "surface_treatment": "Zink-Nickel (ZN-NI) Beschichtung",
    "material_price_eur_kg": 1.40,
    "price_justification": "Vergüteter Stahl 10.9 nach Wärmebehandlung"
  }},

  "mass_calculation": {{
    "calculation_method": "Vollzylinder-Approximation (keine Kopf, Madenschraube)",
    "radius_mm": 5.0,
    "length_mm": 45,
    "volume_formula": "V = π × r² × L",
    "volume_mm3": 3534,
    "volume_cm3": 3.534,
    "density_g_cm3": 7.85,
    "calculated_mass_g": 27.74,
    "mass_kg": 0.02774,
    "step_by_step": [
      "1. Radius: r = 10mm / 2 = 5 mm",
      "2. Volumen: V = π × (5 mm)² × 45 mm = π × 25 × 45 = 3534 mm³",
      "3. Volumen in cm³: 3534 mm³ / 1000 = 3.534 cm³",
      "4. Masse: m = 3.534 cm³ × 7.85 g/cm³ = 27.74 g",
      "5. Masse in kg: 27.74 g / 1000 = 0.02774 kg"
    ],
    "head_volume_cm3": 0,
    "shaft_volume_cm3": 3.534,
    "thread_reduction_factor": 1.0
  }},

  "material_cost_calculation": {{
    "mass_kg": 0.02774,
    "material_price_eur_kg": 1.40,
    "material_cost_eur": 0.0388,
    "calculation": "0.02774 kg × 1.40 €/kg = 0.0388 €/Stk"
  }},

  "alternative_interpretations": [
    "ISO 4028 kann auch andere Punktformen haben (Kegelspitze, Ringschneide)"
  ],

  "assumptions": [
    "Vollzylinder ohne Kopf (Madenschraube)",
    "Feingewinde M10×1,25 (Standard für M10 Feingewinde)",
    "Vergüteter Stahl 10.9 nach DIN EN ISO 898-1",
    "Zink-Nickel Beschichtung ~8-12 µm"
  ]
}}

⚙️ **MATERIAL-PROZESS-KOMPATIBILITÄT PRÜFEN:**

Nachdem du das Material geschätzt hast, VALIDIERE ob das Material mit typischen Fertigungsprozessen für dieses Teil kompatibel ist:

**Typische Prozesse nach Teil-Typ:**
- **Schrauben/Muttern (Normteile):**
  - Massenproduktion: **Cold Forming (Kaltumformung)** für Stahl, Edelstahl
  - Kleinserien: **CNC-Drehen** für alle Materialien
  - WICHTIG: Cold Forming funktioniert NICHT mit spröden Materialien (Gusseisen, Keramik)

- **Custom Teile:**
  - **CNC-Drehen/Fräsen** für Metalle (Stahl, Edelstahl, Aluminium, Messing)
  - **Guss** für Eisen, Aluminium
  - **Kunststoff-Spritzguss** für PA, POM, etc.

**VALIDIERUNGS-REGEL:**
1. Wenn Material + Prozess INKOMPATIBEL → Material ist falsch! Korrigiere!
2. Wenn Material unklar → Wähle das Material das am besten zum Prozess passt!

**Beispiele Material-Prozess-Kompatibilität:**
- ✅ Schraube aus Stahl + Cold Forming = PERFEKT
- ✅ Schraube aus Edelstahl A2 + Cold Forming = PERFEKT
- ❌ Schraube aus Gusseisen + Cold Forming = UNMÖGLICH → Material falsch!
- ✅ Bolzen aus Messing + CNC-Drehen = PERFEKT
- ❌ Normschraube aus Titan + Cold Forming = TEUER/UNÜBLICH → Prüfe nochmal!

**WENN MATERIAL UNKLAR:**
1. Prüfe den wahrscheinlichsten Fertigungsprozess
2. Wähle das Material das am besten zu diesem Prozess passt
3. Für Schrauben/Normteile: Default ist STAHL (nicht Edelstahl ohne eindeutigen Hinweis!)
4. Für Custom-Teile: Analysiere Anforderungen (Festigkeit, Korrosion, Gewicht)

**KRITISCH WICHTIG:**
- Gewicht MUSS realistisch sein (Schrauben wiegen Gramm, nicht Kilogramm!)
- Bei unklarer Bezeichnung: Mehrere Interpretationen angeben
- Confidence "high" NUR bei eindeutiger Norm-Erkennung
- Für Muttern/Scheiben: Passende Geometrie nutzen!
- **MATERIAL-PROZESS-KOMPATIBILITÄT IMMER VALIDIEREN!**
"""

    try:
        # GPT-4o: Bestes verfügbares Modell für maximale Präzision
        # WICHTIG: GPT-4o verwendet max_completion_tokens und erlaubt keine custom temperature
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role":"system","content":"Du bist ein SENIOR COST ENGINEER mit 25+ Jahren Erfahrung in Präzisions-Kostenkalkulation für Normteile und technische Komponenten. Du arbeitest für einen Einkaufsleiter, der deine Zahlen für ECHTE Verhandlungen nutzt. ABSOLUTE MATHEMATISCHE PRÄZISION ist erforderlich - keine Schätzungen, nur exakte Berechnungen mit vollständiger Dokumentation aller Schritte!"},
                {"role":"user","content":prompt}
            ],
            max_tokens=3000  # GPT-4o API verwendet max_completion_tokens
        )
        txt = res.choices[0].message.content.strip()

        # Robustes JSON Parsing mit mehreren Fallbacks
        data = {}
        try:
            # Versuch 1: Ganzer Text ist JSON
            data = json.loads(txt)
        except Exception:
            try:
                # Versuch 2: JSON in ```json ... ``` Code-Block
                m = re.search(r'```json\s*([\s\S]*?)\s*```', txt)
                if m:
                    data = json.loads(m.group(1))
                else:
                    # Versuch 3: Beliebiges { ... } Pattern
                    m = re.search(r'\{[\s\S]*\}', txt)
                    if m:
                        data = json.loads(m.group(0))
                    else:
                        print(f"⚠️  Kein JSON gefunden in GPT Response!")
                        print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                        data = {}
            except Exception as e2:
                print(f"⚠️  JSON Parsing fehlgeschlagen: {e2}")
                print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                data = {}

        # Material-String bereinigen (nur ersten Wert nehmen)
        material = str(data.get("material_guess", "stahl")).split("|")[0].strip().lower()

        # Extrahiere alle detaillierten Felder
        part_id = data.get("part_identification", {})
        geometry = data.get("geometry_details", {})
        material_details = data.get("material_details", {})
        mass_calc = data.get("mass_calculation", {})

        # Masse: Priorisiere detaillierte Berechnung
        mass_kg = mass_calc.get("mass_kg") or data.get("mass_kg")

        # Materialpreis: Priorisiere aus material_details
        material_price_eur_kg = material_details.get("material_price_eur_kg")
        if not material_price_eur_kg:
            # Fallback auf Top-Level
            material_price_eur_kg = data.get("material_price_eur_kg")

        # Materialkosten: Priorisiere aus material_cost_calculation
        material_cost_eur = None
        material_cost_calc = data.get("material_cost_calculation", {})
        if material_cost_calc:
            material_cost_eur = material_cost_calc.get("material_cost_eur")

        print(f"✅ GPT-4o Response erhalten - Tokens: {res.usage.total_tokens}")
        print(f"   → Masse: {mass_kg:.5f} kg" if mass_kg else "   → Masse: N/A")
        print(f"   → Materialpreis: {material_price_eur_kg:.2f} €/kg" if material_price_eur_kg else "   → Materialpreis: N/A")
        print(f"   → Materialkosten: {material_cost_eur:.4f} €/Stk" if material_cost_eur else "   → Materialkosten: N/A")

        return {
            # Hauptfelder
            "material_guess": material,
            "mass_kg": mass_kg,
            "d_mm": data.get("diameter_mm"),
            "l_mm": data.get("length_mm"),
            "confidence": data.get("confidence", "medium"),

            # Materialpreise & Kosten (NEU)
            "material_price_eur_kg": material_price_eur_kg,
            "material_cost_eur": material_cost_eur,

            # Detaillierte Analysen
            "part_identification": part_id,
            "geometry_details": geometry,
            "material_details": material_details,
            "mass_calculation": mass_calc,
            "material_cost_calculation": material_cost_calc,

            # Zusatzinfos
            "alternative_interpretations": data.get("alternative_interpretations", []),
            "assumptions": data.get("assumptions", []),

            "raw": txt,
            "_api_called": True,
            "_tokens_used": res.usage.total_tokens
        }
    except Exception as e:
        import traceback
        error_details = str(e)
        trace = traceback.format_exc()
        print(f"❌ ERROR in gpt_estimate_material: {error_details}")
        print(f"   Traceback: {trace}")

        # Gebe detaillierte Fehlerinfo zurück
        return {
            "material_guess":"stahl",
            "mass_kg":None,
            "d_mm":None,
            "l_mm":None,
            "confidence":"low",
            "error":error_details,
            "error_trace":trace,
            "raw":error_details,
            "_error":True,
            "_error_type": type(e).__name__
        }

def choose_process_with_gpt(description: str, material: str, d_mm: Optional[float], l_mm: Optional[float], lot_size: int = 1000) -> Dict[str, Any]:
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        return {"process":"turning","setup_time_min":30,"cycle_time_s":6.0,"machine_eur_h":80.0,"labor_eur_h":30.0,"overhead_pct":0.2,"raw":None}
    client = OpenAI(api_key=key)
    prompt = f"""Wähle plausiblen Hauptprozess. JSON:
{{"process":"cold_forming|turning|milling|casting|stamping|injection_molding","setup_time_min":30,"cycle_time_s":1.5,"machine_eur_h":60,"labor_eur_h":25,"overhead_pct":0.15}}
Teil: {description}, Material: {material}, D: {d_mm}, L: {l_mm}, Losgröße: {lot_size}"""
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"Return only compact JSON."},{"role":"user","content":prompt}],
            temperature=0.1,
            max_tokens=300
        )
        txt = res.choices[0].message.content.strip()

        # Robustes JSON Parsing mit mehreren Fallbacks
        data = {}
        try:
            # Versuch 1: Ganzer Text ist JSON
            data = json.loads(txt)
        except Exception:
            try:
                # Versuch 2: JSON in ```json ... ``` Code-Block
                m = re.search(r'```json\s*([\s\S]*?)\s*```', txt)
                if m:
                    data = json.loads(m.group(1))
                else:
                    # Versuch 3: Beliebiges { ... } Pattern
                    m = re.search(r'\{[\s\S]*\}', txt)
                    if m:
                        data = json.loads(m.group(0))
                    else:
                        print(f"⚠️  Kein JSON gefunden in GPT Response!")
                        print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                        data = {}
            except Exception as e2:
                print(f"⚠️  JSON Parsing fehlgeschlagen: {e2}")
                print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                data = {}
        data["raw"] = txt
        return data
    except Exception as e:
        return {"process":"turning","setup_time_min":30,"cycle_time_s":6.0,"machine_eur_h":80.0,"labor_eur_h":30.0,"overhead_pct":0.2,"raw":str(e)}

def calc_fab_cost_per_unit(proc: Dict[str, Any], lot_size: int = 1000) -> Optional[float]:
    if not isinstance(proc, dict):
        return None
    st_min = float(proc.get("setup_time_min", 30.0))
    ct_s = float(proc.get("cycle_time_s", 1.5))
    mh = float(proc.get("machine_eur_h", 60.0))
    lh = float(proc.get("labor_eur_h", 25.0))
    oh = float(proc.get("overhead_pct", 0.15))
    setup = (st_min/60.0) * (mh + lh)
    setup_per = setup/lot_size if lot_size and lot_size>0 else setup
    var = (ct_s/3600.0) * (mh + lh)
    return (setup_per + var) * (1.0 + oh)

def gpt_fab_cost_per_unit(description: str, lot_size: int) -> Optional[float]:
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        return None
    client = OpenAI(api_key=key)
    prompt = f"""Schätze die reinen Fertigungskosten pro Stück in EUR (ohne Material).
Antworte nur als kompaktes JSON: {{"cost_per_unit_eur": 0.0}}
Artikel: {description}
Losgröße: {lot_size}"""
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"Return only compact JSON."},{"role":"user","content":prompt}],
            temperature=0.15,
            max_tokens=120
        )
        txt = res.choices[0].message.content.strip()

        # Robustes JSON Parsing mit mehreren Fallbacks
        data = {}
        try:
            # Versuch 1: Ganzer Text ist JSON
            data = json.loads(txt)
        except Exception:
            try:
                # Versuch 2: JSON in ```json ... ``` Code-Block
                m = re.search(r'```json\s*([\s\S]*?)\s*```', txt)
                if m:
                    data = json.loads(m.group(1))
                else:
                    # Versuch 3: Beliebiges { ... } Pattern
                    m = re.search(r'\{[\s\S]*\}', txt)
                    if m:
                        data = json.loads(m.group(0))
                    else:
                        print(f"⚠️  Kein JSON gefunden in GPT Response!")
                        print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                        data = {}
            except Exception as e2:
                print(f"⚠️  JSON Parsing fehlgeschlagen: {e2}")
                print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                data = {}
        v = data.get("cost_per_unit_eur")
        return float(v) if v is not None else None
    except Exception:
        return None

def _encode_image_to_base64(image_data: bytes, format: str = "PNG") -> str:
    """Kodiert Bilddaten zu Base64 für GPT Vision API"""
    if Image:
        # Optimiere Bildgröße
        img = Image.open(io.BytesIO(image_data))
        # Max 2000px zur Kostenoptimierung
        max_size = 2000
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        img.save(buffer, format=format)
        image_data = buffer.getvalue()

    return base64.b64encode(image_data).decode('utf-8')


def gpt_analyze_technical_drawing(image_data: bytes, filename: str = "drawing") -> Dict[str, Any]:
    """
    Analysiert technische Zeichnung (CAD, PDF, Bild) mit GPT-4o Vision.
    Extrahiert: Artikelbezeichnung, Maße, Material, Toleranzen, Stückliste
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        return {"error": "OpenAI API nicht verfügbar", "items": []}

    client = OpenAI(api_key=key)

    # Bild zu Base64
    try:
        base64_image = _encode_image_to_base64(image_data)
    except Exception as e:
        return {"error": f"Bildverarbeitung fehlgeschlagen: {str(e)}", "items": []}

    prompt = """Du bist ein Experte für technische Zeichnungen und CAD-Dokumente. Analysiere dieses technische Dokument und extrahiere ALLE relevanten Informationen.

Suche nach:
1. **Artikelbezeichnungen** (z.B. "DIN933 M10x30", "Schraube", "Mutter M8")
2. **Maße** (Durchmesser, Länge, Breite, Höhe, Gewinde)
3. **Material**
   - Unterscheide genau: Stahl, Edelstahl (A2/A4), Messing, etc.
   - **WICHTIG:** Achte auf Zusätze wie "vergütet", "vergüteter Stahl", "QT", "heat treated", "10.9", "12.9".
   - Wenn "vergütet" oder hohe Festigkeitsklasse (8.8, 10.9, 12.9) erwähnt wird, setze "is_tempered": true.
4. **Oberflächenbehandlung**
   - Sei PRÄZISE! Nicht nur "verzinkt".
   - Suche nach: "Geomet", "Dacromet", "Zink-Lamelle", "flZn", "ZnNi", "Zink-Nickel", "phosphatiert", "brüniert", "eloxiert", "passiviert", "Dickschichtpassivierung".
   - Übernimm die GENAUE Bezeichnung aus der Zeichnung (z.B. "Geomet 500A", "A2K", "galv. verzinkt gelb").
5. **Verzahnung / Rippen (Sperrfunktion)**
   - Suche nach "Verzahnung", "Sperrverzahnung", "Rippen", "Sperrrippen", "Rippen unter Kopf", "Flansch mit Verzahnung".
   - Das ist ein wichtiges Merkmal für die Kosten!
6. **Extras / Besonderheiten**
   - Fasse hier ALLE speziellen Merkmale zusammen, die den Preis beeinflussen (außer Standard-Maßen).
   - Dazu gehören: Spezielle Oberflächen, Verzahnungen, Sicherungen (Tuflok, Kleber), 100% Prüfung, besondere Toleranzen.
   - Gib dies als Liste von kurzen Strings zurück.
7. **Toleranzen** (ISO, DIN)
8. **Stückzahlen** (falls Stückliste vorhanden)
9. **Zeichnungsnummer**, **Revision**, **Datum**

Antworte NUR als kompaktes JSON:
{
  "drawing_number": "12345-A",
  "revision": "Rev. 2",
  "items": [
    {
      "position": "1",
      "description": "DIN933 M10x30 10.9 Geomet",
      "quantity": 4,
      "material": "Stahl vergütet",
      "is_tempered": true,
      "diameter_mm": 10,
      "length_mm": 30,
      "surface_treatment": "Geomet 500A",
      "has_serration": true,
      "serration_type": "Sperrverzahnung unter Kopf",
      "extras": ["Vergütet 10.9", "Geomet 500A", "Sperrverzahnung"],
      "tolerances": "ISO 4017",
      "weight_g": 15.3
    },
    {
      "position": "2",
      "description": "Scheibe DIN125",
      "quantity": 4,
      "material": "Stahl",
      "is_tempered": false,
      "diameter_mm": 10.5,
      "surface_treatment": "galv. verzinkt",
      "has_serration": false,
      "extras": ["galv. verzinkt"]
    }
  ],
  "total_items": 2,
  "notes": ["Alle Teile nach DIN-Norm", "Oberfläche: Geomet 500A"],
  "confidence": "high|medium|low"
}

Wichtig:
- Extrahiere ALLE Positionen aus der Stückliste
- Wenn keine Stückliste: Identifiziere Hauptteil
- Wenn unklar: "confidence": "low" setzen
- Realistische Schätzungen für Gewicht/Maße"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # gpt-4o-mini unterstützt auch Vision!
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                                "detail": "high"  # "high" für detaillierte Analyse
                            }
                        }
                    ]
                }
            ],
            max_tokens=1500,
            temperature=0.1
        )

        txt = response.choices[0].message.content.strip()
        try:
            data = json.loads(txt)
        except Exception:
            m = re.search(r"\{[\s\S]*\}", txt)
            data = json.loads(m.group(0)) if m else {}

        return {
            "ok": True,
            "drawing_number": data.get("drawing_number"),
            "revision": data.get("revision"),
            "items": data.get("items", []),
            "total_items": data.get("total_items", 0),
            "notes": data.get("notes", []),
            "confidence": data.get("confidence", "medium"),
            "raw": txt
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "items": []
        }


def gpt_analyze_pdf_drawing(pdf_bytes: bytes) -> Dict[str, Any]:
    """
    Analysiert technische Zeichnung aus PDF mit GPT-4o Vision.
    Konvertiert erste Seite zu Bild und analysiert.
    """
    if not fitz:
        return {"error": "PyMuPDF nicht installiert (pip install pymupdf)", "items": []}

    try:
        # PDF öffnen
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Erste Seite zu Bild konvertieren
        page = pdf_document[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x Auflösung
        img_data = pix.tobytes("png")

        pdf_document.close()

        # Mit Vision API analysieren
        return gpt_analyze_technical_drawing(img_data, filename="drawing.pdf")

    except Exception as e:
        return {
            "ok": False,
            "error": f"PDF-Verarbeitung fehlgeschlagen: {str(e)}",
            "items": []
        }


def gpt_negotiation_prep(supplier_name: str, country: str = None, rating: int = None,
                          strengths: List[str] = None, weaknesses: List[str] = None,
                          avg_price: float = None, target_price: float = None,
                          article_name: str = None, total_orders: int = None,
                          supplier_competencies: Dict[str, Any] = None,
                          min_price: float = None, max_price: float = None,
                          commodity_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Generiert Verhandlungsstrategie für Einkäufer basierend auf Lieferantenbewertung.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        return {"strategy": "Keine GPT-Verfügbarkeit", "talking_points": [], "tactics": [], "red_flags": []}

    client = OpenAI(api_key=key)

    # Kontext aufbauen - SO VIEL WIE MÖGLICH!
    context_parts = [f"Lieferant: {supplier_name}"]
    if article_name:
        context_parts.append(f"Artikel: {article_name}")
    if country:
        context_parts.append(f"Land: {country}")
    if rating:
        rating_quality = "exzellent" if rating >= 8 else "gut" if rating >= 6 else "bedenklich"
        context_parts.append(f"Internes Rating: {rating}/10 ({rating_quality})")
    if total_orders:
        context_parts.append(f"Bestellhistorie: {total_orders} Bestellungen")
    if avg_price and target_price:
        delta_pct = ((avg_price - target_price) / target_price * 100) if target_price > 0 else 0
        delta_eur = avg_price - target_price
        context_parts.append(f"Aktueller Preis: {avg_price:.4f}€/Stk")
        context_parts.append(f"Zielpreis: {target_price:.4f}€/Stk")
        context_parts.append(f"Einsparungspotenzial: {delta_eur:+.4f}€ ({delta_pct:+.1f}%)")

    # Min/Max Preise hinzufügen
    if min_price and max_price and min_price < max_price:
        price_spread = ((max_price - min_price) / min_price * 100)
        context_parts.append(f"Min-Preis (Benchmark): {min_price:.4f}€/Stk")
        context_parts.append(f"Max-Preis: {max_price:.4f}€/Stk")
        context_parts.append(f"Preisspanne: {price_spread:.1f}% (WICHTIG für Verhandlung!)")

    context = "\n".join(context_parts)

    strengths_text = "\n".join([f"  • {s}" for s in (strengths or [])])
    weaknesses_text = "\n".join([f"  • {w}" for w in (weaknesses or [])])

    # Lieferanten-Kompetenzen-Analyse
    competencies_text = ""
    if supplier_competencies and not supplier_competencies.get('_error'):
        comp_parts = []
        comp_parts.append("\n🏭 **LIEFERANTEN-PRODUKTIONSKOMPETENZEN (SEHR WICHTIG für Verhandlung!):**\n")

        # Hauptkompetenzen
        core_comps = supplier_competencies.get('core_competencies', [])
        if core_comps:
            comp_parts.append("**Hauptkompetenzen:**")
            for comp in core_comps[:5]:  # Top 5
                process = comp.get('process', 'unknown')
                level = comp.get('capability_level', 'proficient')
                conf = comp.get('confidence', 'medium')
                evidence = comp.get('evidence', [])

                comp_parts.append(f"  • **{process}** (Level: {level}, Confidence: {conf})")
                if evidence:
                    comp_parts.append(f"    → Beweis: {', '.join(evidence[:2])}")

        # Spezialisierung
        spec = supplier_competencies.get('specialization', {})
        if spec:
            primary_focus = spec.get('primary_focus', 'unknown')
            part_complexity = spec.get('part_complexity', 'unknown')
            comp_parts.append(f"\n**Spezialisierung:**")
            comp_parts.append(f"  • Hauptfokus: **{primary_focus}**")
            comp_parts.append(f"  • Teilekomplexität: **{part_complexity}**")
            industries = spec.get('industries_served', [])
            if industries:
                comp_parts.append(f"  • Branchen: {', '.join(industries[:3])}")

        # Produktionskapazitäten
        prod_cap = supplier_competencies.get('production_capabilities', {})
        if prod_cap:
            comp_parts.append(f"\n**Produktionskapazitäten:**")
            if prod_cap.get('preferred_lot_sizes'):
                comp_parts.append(f"  • Bevorzugte Losgrößen: {prod_cap['preferred_lot_sizes']}")
            if prod_cap.get('automation_level'):
                comp_parts.append(f"  • Automatisierung: {prod_cap['automation_level']}")
            if prod_cap.get('lead_times_typical_days'):
                comp_parts.append(f"  • Typische Lieferzeit: {prod_cap['lead_times_typical_days']} Tage")

        # Material-Expertise
        mat_exp = supplier_competencies.get('material_expertise', [])
        if mat_exp:
            materials = [m.get('material', 'unknown') for m in mat_exp[:5]]
            comp_parts.append(f"\n**Material-Expertise:** {', '.join(materials)}")

        # Ungeeignete Prozesse (WICHTIG für Verhandlung!)
        unsuitable = supplier_competencies.get('unsuitable_processes', [])
        if unsuitable:
            comp_parts.append(f"\n⚠️ **NICHT GEEIGNETE PROZESSE (Hebelwirkung für Verhandlung!):**")
            for unsui in unsuitable[:3]:
                proc = unsui.get('process', 'unknown')
                reason = unsui.get('reason', 'Keine Expertise')
                comp_parts.append(f"  • {proc}: {reason}")

        # Empfehlungen
        recommendations = supplier_competencies.get('recommendations', [])
        if recommendations:
            comp_parts.append(f"\n💡 **Strategie-Empfehlungen basierend auf Kompetenzen:**")
            for rec in recommendations[:3]:
                comp_parts.append(f"  • {rec}")

        competencies_text = "\n".join(comp_parts)

    # Rohstoffmarkt-Analyse Text
    commodity_text = ""
    if commodity_analysis and commodity_analysis.get('ok'):
        commodity_text = f"""
📊 **ROHSTOFFMARKT-ANALYSE (KRITISCH für Verhandlung!):**

**Material:** {commodity_analysis.get('material', 'unbekannt')}
**Aktueller Marktpreis:** {commodity_analysis.get('current_price_eur_kg', 0):.2f} €/kg
**Preistrend:** {commodity_analysis.get('trend', 'unbekannt')} ({commodity_analysis.get('trend_percentage', 0):+.1f}% über {commodity_analysis.get('timeframe', 'unbekannt')})
**Verhandlungshebel:** {commodity_analysis.get('negotiation_leverage', 'NEUTRAL')}

**Marktanalyse:**
{commodity_analysis.get('analysis', 'Keine Analyse verfügbar')}

⚡ **NUTZE DEN MARKTTREND AKTIV:**
{'- ✅ STARK FALLENDE PREISE → Fordere Preisanpassung! "Der Markt ist um X% gefallen, wir erwarten eine entsprechende Reduktion"' if commodity_analysis.get('trend_percentage', 0) < -3 else ''}
{'- ✅ Fallende Preise → Nutze als Argument für bessere Konditionen' if commodity_analysis.get('trend_percentage', 0) < -1 and commodity_analysis.get('trend_percentage', 0) >= -3 else ''}
{'- ⚠️ STEIGENDE PREISE → Fixiere Konditionen SCHNELL! "Wir müssen jetzt abschließen bevor weitere Erhöhungen kommen"' if commodity_analysis.get('trend_percentage', 0) > 3 else ''}
{'- 📊 Stabile Preise → Fokus auf Volumen und Lieferkonditionen statt Preis' if abs(commodity_analysis.get('trend_percentage', 0)) <= 1 else ''}

**Datenquelle:** {commodity_analysis.get('data_source', 'Unbekannt')}
"""

    prompt = f"""Du bist ein SENIOR PROCUREMENT NEGOTIATION EXPERT mit 20+ Jahren Erfahrung in strategischem Einkauf von technischen Teilen, Normteilen und industriellen Komponenten. Du hast hunderte erfolgreiche Verhandlungen geführt und kennst alle Taktiken und Strategien.

**VOLLSTÄNDIGER KONTEXT:**
{context}

**Stärken des Lieferanten:**
{strengths_text if strengths_text else "  (keine bekannt)"}

**Schwächen des Lieferanten:**
{weaknesses_text if weaknesses_text else "  (keine bekannt)"}
{competencies_text}
{commodity_text}

**AUFGABE:** Erstelle eine HOCHSPEZIFISCHE, MAẞGESCHNEIDERTE Verhandlungsstrategie NUR für diesen Lieferanten und diesen spezifischen Artikel!

**SEHR WICHTIG - NUTZE DIE PRODUKTIONSKOMPETENZEN STRATEGISCH:**
1. **Wenn Lieferant EXPERTISE hat für das Produkt:**
   - Argumentiere mit erwarteten Skaleneffekten und Effizienz
   - "Da Sie ein Spezialist für [Prozess] sind, erwarten wir optimierte Prozesse und entsprechend günstigere Preise"
   - Nutze deren Spezialisierung als Hebel für bessere Konditionen

2. **Wenn Lieferant KEINE/WENIG Expertise hat:**
   - Das ist ein MAJOR LEVERAGE POINT!
   - "Wir sehen, dass [Prozess] nicht zu Ihren Kernkompetenzen gehört - wir müssten alternative Lieferanten prüfen"
   - Nutze dies für Preisnachlässe oder um zum kompe tenten Lieferanten zu wechseln

3. **Material-Prozess-Kompatibilität:**
   - Wenn Material NICHT optimal für Lieferanten-Prozesse: "Warum sollten wir Sie beauftragen wenn Ihre Prozesse für dieses Material suboptimal sind?"
   - Wenn Material PERFEKT passt: "Da Sie Experten für [Material] sind, erwarten wir Best-in-Class Preise"

4. **Preisspanne-Argumentation:**
   - Wenn Min-Preis deutlich niedriger als aktueller Preis: "Andere Lieferanten bieten [X%] günstiger - können Sie das matchen?"
   - Nutze Wettbewerb als Druckmittel

**WICHTIG:**
- Nutze ALLE Informationen (Artikel-Details, Preise, Rating, Bestellhistorie, Land, KOMPETENZEN!)
- Sei SEHR konkret und spezifisch - keine generischen Phrasen!
- Berücksichtige den Artikeltyp (z.B. Normteil vs. Custom Part)
- Nutze die Schwächen UND fehlenden Kompetenzen des Lieferanten strategisch
- Sei realistisch über Verhandlungsspielraum
- Gebe KONKRETE Argumente und Formulierungen mit Bezug auf Produktionskompetenzen

Erstelle eine HOCHDETAILLIERTE Verhandlungsstrategie mit:
1. **Gesamtstrategie** (kooperativ vs. kompetitiv) - SPEZIFISCH für diesen Lieferanten!
2. **Verhandlungsziele** - Preis, Qualität, Lieferzeit - priorisiert!
3. **Konkrete Argumente** - Mit Fakten untermauert!
4. **Verhandlungstaktiken** - BATNA, Anker, Timing
5. **Konkrete Formulierungen** - Was GENAU sagen?
6. **Zugeständnisse & Gegenleistungen** - Trade-offs
7. **Risiken & Warnsignale** - Wann abbrechen?

Antworte als AUSFÜHRLICHES JSON:
{{
  "strategy_overview": {{
    "main_approach": "win-win|competitive|collaborative|defensive",
    "rationale": "DETAILLIERTE Begründung warum dieser Ansatz für DIESEN Lieferanten gewählt wurde",
    "negotiation_power_balance": "buyer_advantage|balanced|supplier_advantage",
    "estimated_success_probability": "high|medium|low",
    "key_leverage_points": ["Konkrete Hebelpunkte die wir haben"]
  }},

  "objectives": {{
    "primary_goal": "z.B. Preisreduktion um 12% auf 0.045€/Stk",
    "secondary_goals": ["Zahlungsziel auf 60 Tage", "Rabattmodell bei Jahresabnahme"],
    "minimum_acceptable_outcome": "Was ist das absolute Minimum?",
    "batna": "Best Alternative To Negotiated Agreement - konkret!"
  }},

  "key_arguments": [
    {{
      "argument": "Konkretes Argument mit Zahlen",
      "supporting_facts": ["Fakt 1", "Fakt 2"],
      "expected_counter": "Wie könnte der Lieferant reagieren?",
      "our_response": "Wie kontern wir?"
    }}
  ],

  "tactics": [
    "KONKRETE Taktik 1 mit Timing",
    "KONKRETE Taktik 2 mit Beispiel"
  ],

  "concessions": [
    {{
      "what_we_offer": "z.B. Erhöhung Mindestbestellmenge auf 5000",
      "what_we_want": "Preis von 0.055€ auf 0.048€",
      "trade_off_value": "Gut für uns, da..."
    }}
  ],

  "red_flags": [
    "SPEZIFISCHES Warnsignal 1",
    "SPEZIFISCHES Warnsignal 2"
  ],

  "opening_statement": "VOLLSTÄNDIGE, wörtliche Eröffnung (3-5 Sätze)",
  "closing_statement": "VOLLSTÄNDIGE, wörtliche Abschlussformulierung",

  "talking_points": ["Legacy-Feld für Kompatibilität"],
  "recommendations": ["Legacy-Feld"]
}}

**KRITISCH WICHTIG:**
- Sei EXTREM spezifisch - nutze konkrete Zahlen, Namen, Fakten!
- Keine generischen Phrasen - alles muss auf DIESEN Fall zugeschnitten sein!
- Gebe wörtliche Formulierungen die der Einkäufer 1:1 nutzen kann!"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o",  # UPGRADE: Beste Qualität für strategische Beratung!
            messages=[
                {"role": "system", "content": "Du bist ein SENIOR PROCUREMENT NEGOTIATION EXPERT mit 20+ Jahren Erfahrung. Gib HOCHSPEZIFISCHE, maßgeschneiderte Strategien mit konkreten Formulierungen. Keine generischen Ratschläge - alles muss auf den spezifischen Fall zugeschnitten sein!"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.15,  # Etwas Kreativität für Strategie, aber präzise
            max_tokens=3000  # MAXIMAL viel Platz!
        )

        txt = res.choices[0].message.content.strip()

        # Robustes JSON Parsing mit mehreren Fallbacks
        data = {}
        try:
            # Versuch 1: Ganzer Text ist JSON
            data = json.loads(txt)
        except Exception:
            try:
                # Versuch 2: JSON in ```json ... ``` Code-Block
                m = re.search(r'```json\s*([\s\S]*?)\s*```', txt)
                if m:
                    data = json.loads(m.group(1))
                else:
                    # Versuch 3: Beliebiges { ... } Pattern
                    m = re.search(r'\{[\s\S]*\}', txt)
                    if m:
                        data = json.loads(m.group(0))
                    else:
                        print(f"⚠️  Kein JSON gefunden in GPT Response!")
                        print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                        data = {}
            except Exception as e2:
                print(f"⚠️  JSON Parsing fehlgeschlagen: {e2}")
                print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                data = {}

        print(f"✅ GPT-4o Response - Tokens: {res.usage.total_tokens}")

        # Extrahiere detaillierte Strategie-Daten
        strategy_overview = data.get("strategy_overview", {})
        objectives = data.get("objectives", {})

        return {
            # Neue detaillierte Felder
            "strategy_overview": strategy_overview,
            "objectives": objectives,
            "key_arguments": data.get("key_arguments", []),
            "tactics": data.get("tactics", []),
            "concessions": data.get("concessions", []),
            "red_flags": data.get("red_flags", []),
            "opening_statement": data.get("opening_statement", ""),
            "closing_statement": data.get("closing_statement", ""),

            # Legacy-Felder für Kompatibilität
            "strategy": strategy_overview.get("rationale") or data.get("strategy", "Standard-Verhandlung"),
            "approach": strategy_overview.get("main_approach") or data.get("approach", "collaborative"),
            "talking_points": data.get("talking_points", []),
            "recommendations": data.get("recommendations", []),

            "raw": txt,
            "_api_called": True,
            "_tokens_used": res.usage.total_tokens
        }

    except Exception as e:
        return {
            "strategy": f"Fehler: {str(e)}",
            "talking_points": [],
            "tactics": [],
            "red_flags": [],
            "concessions": [],
            "raw": str(e)
        }


def calculate_co2_footprint(mass_kg: float, supplier_country: str, material: str,
                            distance_km: float = None, transport_mode: str = "truck") -> Dict[str, Any]:
    """
    Berechnet CO₂-Footprint und CBAM-Kosten für ein Bauteil.

    CBAM (Carbon Border Adjustment Mechanism) gilt ab 2026 für Importe in die EU.

    Parameter:
    - mass_kg: Masse des Bauteils in kg
    - supplier_country: Herkunftsland
    - material: Material (steel, stainless_steel, aluminum, etc.)
    - distance_km: Transportdistanz (optional, wird geschätzt falls None)
    - transport_mode: truck|ship|air

    Returns:
    - co2_production_kg: CO₂ aus Materialproduktion
    - co2_transport_kg: CO₂ aus Transport
    - co2_total_kg: Gesamt-CO₂
    - cbam_cost_eur: Geschätzte CBAM-Kosten (ab 2026)
    """
    # CO₂-Emissionsfaktoren für Materialproduktion (kg CO₂ pro kg Material)
    # Quelle: Durchschnittswerte für EU/globale Produktion
    co2_factors = {
        "steel": 1.85,  # kg CO₂ / kg Stahl (EU-Durchschnitt)
        "stainless_steel": 3.1,  # Edelstahl (höher wegen Legierungen)
        "aluminum": 8.2,  # Aluminium (sehr energieintensiv!)
        "brass": 3.5,
        "copper": 3.8,
        "zinc": 3.2,
        "titanium": 20.0,  # Extrem energieintensiv!
        "cast_iron": 1.5,
        "plastics": 3.0  # Kunststoff (abhängig von Typ)
    }

    # Transportemissionen (kg CO₂ pro kg pro km)
    transport_factors = {
        "truck": 0.00012,  # 120 g CO₂/t·km
        "ship": 0.000015,  # 15 g CO₂/t·km (deutlich effizienter!)
        "air": 0.0016,     # 1600 g CO₂/t·km (sehr ineffizient!)
        "rail": 0.00003    # 30 g CO₂/t·km
    }

    # Material-Emissionsfaktor
    material_lower = str(material or "steel").lower()
    co2_factor = co2_factors.get(material_lower, 1.85)  # Fallback: Stahl

    # CO₂ aus Materialproduktion
    co2_production_kg = mass_kg * co2_factor

    # Transport-Distanz schätzen falls nicht angegeben
    if distance_km is None:
        # Geschätzte Distanzen basierend auf Land (sehr grob!)
        distance_estimates = {
            "deutschland": 300, "germany": 300,
            "österreich": 500, "austria": 500,
            "schweiz": 600, "switzerland": 600,
            "polen": 800, "poland": 800,
            "tschechien": 700, "czech republic": 700,
            "italien": 1000, "italy": 1000,
            "frankreich": 800, "france": 800,
            "china": 8000,  # Seefracht!
            "indien": 7000, "india": 7000,
            "usa": 7500,
            "türkei": 2500, "turkey": 2500,
            "spanien": 1800, "spain": 1800
        }
        country_lower = str(supplier_country or "").lower()
        distance_km = distance_estimates.get(country_lower, 1500)  # Fallback: 1500 km

        # Wenn Asien/USA: Vermutlich Seefracht
        if distance_km > 5000:
            transport_mode = "ship"

    # CO₂ aus Transport
    transport_factor = transport_factors.get(transport_mode, 0.00012)
    co2_transport_kg = mass_kg * distance_km * transport_factor

    # Gesamt-CO₂
    co2_total_kg = co2_production_kg + co2_transport_kg

    # CBAM-Kosten berechnen (ab 2026)
    # EU ETS-Preis: ~80-100 €/t CO₂ (Stand 2024, Prognose 2026: ~100 €/t)
    # CBAM gilt nur für Nicht-EU-Importe!
    cbam_price_per_ton = 100.0  # €/t CO₂ (Prognose 2026)

    # Prüfe ob Import aus Nicht-EU-Land
    eu_countries = ["deutschland", "germany", "österreich", "austria", "frankreich", "france",
                    "italien", "italy", "spanien", "spain", "polen", "poland",
                    "niederlande", "netherlands", "belgien", "belgium", "tschechien", "czech republic",
                    "ungarn", "hungary", "rumänien", "romania", "schweden", "sweden",
                    "dänemark", "denmark", "finnland", "finland", "portugal", "griechenland", "greece"]

    country_lower = str(supplier_country or "").lower()
    is_eu = any(eu in country_lower for eu in eu_countries)

    if is_eu:
        cbam_cost_eur = 0.0  # CBAM gilt nicht für EU-Binnenmarkt!
        cbam_status = "Nicht anwendbar (EU-Binnenmarkt)"
    else:
        # CBAM gilt NUR für Materialproduktion, NICHT für Transport
        cbam_cost_eur = (co2_production_kg / 1000.0) * cbam_price_per_ton
        cbam_status = f"CBAM-pflichtig (Nicht-EU Import ab 2026)"

    return {
        "co2_production_kg": round(co2_production_kg, 6),
        "co2_transport_kg": round(co2_transport_kg, 6),
        "co2_total_kg": round(co2_total_kg, 6),
        "co2_total_g": round(co2_total_kg * 1000, 2),  # Für bessere Lesbarkeit
        "cbam_cost_eur": round(cbam_cost_eur, 6),
        "cbam_status": cbam_status,
        "is_eu_source": is_eu,
        "transport_distance_km": distance_km,
        "transport_mode": transport_mode,
        "material_co2_factor_kg_per_kg": co2_factor,
        "assumptions": [
            f"Material CO₂-Faktor: {co2_factor} kg CO₂/kg {material}",
            f"Transportdistanz: {distance_km} km ({transport_mode})",
            f"CBAM-Preis 2026: {cbam_price_per_ton} €/t CO₂",
            f"Quelle: {'EU (CBAM nicht anwendbar)' if is_eu else 'Nicht-EU (CBAM-pflichtig ab 2026)'}"
        ]
    }


def get_supplier_financial_data(supplier_name: str, country: str = None,
                                 api_provider: str = "creditreform",
                                 api_credentials: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Ruft Finanzdaten eines Lieferanten über Kreditauskunfts-APIs ab.

    Unterstützte API-Provider:
    - creditreform: Creditreform (Deutschland)
    - dun_bradstreet: Dun & Bradstreet (international)
    - bisnode: Bisnode (Skandinavien/Europa)
    - coface: Coface (international)

    Parameter:
    - supplier_name: Name des Lieferanten
    - country: Land des Lieferanten
    - api_provider: Welcher API-Provider (default: creditreform)
    - api_credentials: Dict mit {"username": "...", "password": "...", "api_key": "..."}

    Returns:
    - credit_rating: Bonitätsbewertung (z.B. AAA, AA, A, BBB, etc.)
    - risk_score: Numerischer Risiko-Score (0-100, 0=kein Risiko)
    - financial_strength: Finanzielle Stärke (excellent|good|fair|poor|critical)
    - revenue_eur: Geschätzter Jahresumsatz in EUR
    - employees: Anzahl Mitarbeiter
    - payment_behavior: Zahlungsverhalten (excellent|good|delayed|critical)
    - insolvency_risk: Insolvenzrisiko (low|medium|high|critical)
    - warnings: Liste von Warnungen (z.B. ["Zahlungsverzug", "Negativeintrag"])
    """

    # PLACEHOLDER: In Produktion würde hier ein echter API-Call erfolgen
    print(f"⚠️ PLACEHOLDER: Kreditreform API-Call für {supplier_name} (Provider: {api_provider})")

    if not api_credentials:
        print("   → Keine API-Credentials angegeben. Nutze Demo-Daten.")

    # Demo-Daten basierend auf Lieferanten-Name (für Testing)
    # In Produktion: Echter API-Call zu Creditreform/Dun & Bradstreet/etc.

    # Simuliere Rating basierend auf Name (für Demo)
    name_lower = str(supplier_name or "").lower()

    if "gmbh" in name_lower or "ag" in name_lower or "inc" in name_lower or "ltd" in name_lower:
        # Etablierte Unternehmen → besseres Rating
        credit_rating = "AA"
        risk_score = 15
        financial_strength = "good"
        payment_behavior = "good"
        insolvency_risk = "low"
        warnings = []
    else:
        # Kleinere/unbekannte Lieferanten → moderates Rating
        credit_rating = "BBB"
        risk_score = 35
        financial_strength = "fair"
        payment_behavior = "fair"
        insolvency_risk = "medium"
        warnings = ["Begrenzte Finanzinformationen verfügbar"]

    return {
        "ok": True,
        "api_provider": api_provider,
        "supplier_name": supplier_name,
        "country": country,

        # Bewertungen
        "credit_rating": credit_rating,
        "risk_score": risk_score,
        "financial_strength": financial_strength,
        "payment_behavior": payment_behavior,
        "insolvency_risk": insolvency_risk,

        # Finanzdaten (Demo-Werte)
        "revenue_eur": None,  # Würde von API kommen
        "revenue_range": "1M-10M",  # Geschätzter Bereich
        "employees": None,
        "employees_range": "10-50",
        "founded_year": None,

        # Warnungen
        "warnings": warnings,
        "negative_entries": [],

        # Meta
        "_demo_mode": True,
        "_message": """
        ⚠️ **DEMO-MODUS AKTIV!**

        Für echte Finanzdaten benötigen Sie API-Zugang zu:
        - **Creditreform** (Deutschland): https://www.creditreform.de/api
        - **Dun & Bradstreet** (international): https://www.dnb.com/
        - **Bisnode** (Europa): https://www.bisnode.com/
        - **Coface** (international): https://www.coface.com/

        **Integration-Schritte:**
        1. API-Credentials bei Provider erwerben
        2. In .env Datei hinterlegen: CREDITREFORM_API_KEY=xxx
        3. Code in `get_supplier_financial_data()` anpassen
        4. Echte API-Calls implementieren

        **Kosten:** Ca. 1-5 € pro Abfrage (je nach Provider und Detailtiefe)
        """,

        "api_setup_instructions": {
            "creditreform": {
                "url": "https://www.creditreform.de/produkte/wirtschaftsinformationen",
                "env_var": "CREDITREFORM_API_KEY",
                "typical_cost_per_query": "2-5 EUR",
                "coverage": "Deutschland, Österreich, Schweiz"
            },
            "dun_bradstreet": {
                "url": "https://www.dnb.com/products/finance-credit-risk/dnb-direct.html",
                "env_var": "DNB_API_KEY",
                "typical_cost_per_query": "3-8 EUR",
                "coverage": "Weltweit"
            },
            "bisnode": {
                "url": "https://www.bisnode.com/products/credit-information/",
                "env_var": "BISNODE_API_KEY",
                "typical_cost_per_query": "2-6 EUR",
                "coverage": "Europa (Skandinavien, D-A-CH, BeNeLux)"
            }
        }
    }


def gpt_analyze_supplier_competencies(supplier_name: str, article_history: List[str] = None,
                                       country: str = None) -> Dict[str, Any]:
    """
    Analysiert die Hauptkompetenzen eines Lieferanten basierend auf dessen Artikelportfolio.
    Returns: Dict mit core_competencies, production_methods, material_expertise, etc.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        print("⚠️ WARNING: FALLBACK - Kein API Key für gpt_analyze_supplier_competencies!")
        return {"core_competencies": ["turning", "milling"], "material_expertise": ["steel"], "production_methods": [], "_fallback": True}

    print(f"✅ GPT-4o API-Call: gpt_analyze_supplier_competencies({supplier_name})")
    client = OpenAI(api_key=key)

    # Artikel-Historie zusammenfassen
    article_summary = "\n".join([f"- {art}" for art in (article_history or [])[:50]]) if article_history else "Keine Artikelhistorie verfügbar"

    prompt = f"""Du bist ein SENIOR SUPPLY CHAIN ANALYST und MANUFACTURING EXPERT mit 20+ Jahren Erfahrung in Lieferanten-Due-Diligence und Fertigungsprozess-Analyse.

**AUFGABE:** Analysiere den Lieferanten und identifiziere dessen HAUPTKOMPETENZEN basierend auf dessen Artikelportfolio!

**LIEFERANT:** {supplier_name}
**LAND:** {country or 'unbekannt'}

**ARTIKELHISTORIE (Beispiel-Artikel die dieser Lieferant liefert):**
{article_summary}

**WICHTIG:** Analysiere die Artikel-Bezeichnungen und leite daraus ab:
1. **Fertigungsverfahren** die der Lieferant beherrscht
2. **Material-Expertise** (welche Materialien verarbeitet er?)
3. **Teilekomplexität** (einfache Normteile vs. komplexe Bauteile?)
4. **Produktions-Technologie** (Kaltumformung, Drehen, Fräsen, Guss, Schmieden, etc.)
5. **Spezialisierung** (z.B. Normteile, Befestigungstechnik, Automotive, etc.)

**FERTIGUNGSVERFAHREN-ÜBERSICHT:**

**Umformtechnik (für Massen-produktion):**
- cold_forming: Kaltumformung (Schrauben, Niete, Bolzen aus Draht)
- hot_forging: Warmschmieden (große, komplexe Teile, hohe Festigkeit)
- stamping: Stanzen (Blechteile, Scheiben)
- deep_drawing: Tiefziehen (Blechformteile)

**Zerspanende Verfahren:**
- turning: Drehen/CNC-Drehen (runde Teile, Wellen, Bolzen)
- milling: Fräsen/CNC-Fräsen (komplexe Geometrien, Flansche)
- threading: Gewindeschneiden/-rollen
- grinding: Schleifen (Präzisionsteile)

**Guss-Verfahren:**
- die_casting: Druckguss (Aluminium, Zink - Massenproduktion)
- sand_casting: Sandguss (Eisen, Stahl - Prototypen/Kleinserien)
- investment_casting: Feinguss/Wachsausschmelzverfahren (Präzisionsteile)

**Kunststoff-Verarbeitung:**
- injection_molding: Spritzguss (Kunststoffteile, Massenproduktion)
- extrusion: Extrusion (Profile, Rohre)

**Verbindungstechnik:**
- welding: Schweißen
- brazing: Löten

**MATERIAL-KATEGORIEN:**
- steel: Stahl (C-Stahl, vergüteter Stahl)
- stainless_steel: Edelstahl (A2, A4)
- aluminum: Aluminium (AlMg)
- brass: Messing (CuZn)
- copper: Kupfer
- titanium: Titan
- plastics: Kunststoffe (PA, POM, etc.)
- cast_iron: Gusseisen

**HINWEISE ZUR ANALYSE:**
- Schrauben, Muttern, Bolzen → Hinweis auf **cold_forming** oder **turning**
- DIN/ISO-Normteile → Spezialisierung auf **Befestigungstechnik**
- M6, M8, M10 etc. → **Metrische Gewinde** (Gewinderollen/-schneiden)
- Große Losgrößen (>10k) → **Massenproduktion** (cold_forming, stamping)
- A2, A4 Edelstahl → **Edelstahl-Expertise**
- Aluminium-Teile → Möglicherweise **Druckguss** oder **CNC-Bearbeitung**
- Komplexe Geometrien → **CNC-Fräsen/Drehen**

Antworte als DETAILLIERTES JSON:
{{
  "supplier_name": "{supplier_name}",
  "analysis_confidence": "high|medium|low",

  "core_competencies": [
    {{
      "process": "cold_forming|turning|milling|die_casting|...",
      "confidence": "high|medium|low",
      "evidence": ["Artikel 1", "Artikel 2"],
      "capability_level": "expert|proficient|basic",
      "typical_lot_sizes": "mass_production|medium_batch|small_batch|prototypes"
    }}
  ],

  "material_expertise": [
    {{
      "material": "steel|stainless_steel|aluminum|brass|...",
      "confidence": "high|medium|low",
      "evidence": ["Artikel mit diesem Material"],
      "processing_methods": ["cold_forming", "heat_treatment", "surface_coating"]
    }}
  ],

  "specialization": {{
    "primary_focus": "fasteners|turned_parts|stamped_parts|cast_parts|custom_parts",
    "industries_served": ["automotive", "construction", "machinery", "electronics"],
    "part_complexity": "simple_standard_parts|medium_complexity|high_complexity_custom",
    "quality_standards": ["ISO 9001", "IATF 16949", "etc."]
  }},

  "production_capabilities": {{
    "preferred_lot_sizes": "10-1000|1000-10000|10000-100000|>100000",
    "lead_times_typical_days": 14,
    "automation_level": "fully_automated|semi_automated|manual",
    "secondary_operations": ["heat_treatment", "surface_coating", "quality_inspection"]
  }},

  "material_process_compatibility": {{
    "steel": ["cold_forming", "turning", "milling"],
    "stainless_steel": ["turning", "milling", "casting"],
    "aluminum": ["die_casting", "turning", "milling"],
    "brass": ["turning", "cold_forming", "machining"]
  }},

  "unsuitable_processes": [
    {{
      "process": "injection_molding",
      "reason": "Keine Hinweise auf Kunststoffverarbeitung im Portfolio"
    }}
  ],

  "recommendations": [
    "Dieser Lieferant eignet sich besonders für...",
    "Nicht geeignet für..."
  ]
}}

**WICHTIG:** Sei SEHR spezifisch! Nutze die Artikelbezeichnungen um präzise Rückschlüsse zu ziehen!"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o",  # Beste Qualität für Analyse!
            messages=[
                {"role": "system", "content": "Du bist ein Senior Manufacturing & Supply Chain Analyst. Analysiere Lieferanten-Kompetenzen EXTREM präzise basierend auf deren Artikelportfolio. Identifiziere Fertigungsverfahren und Materialexpertise."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2500
        )
        txt = res.choices[0].message.content.strip()

        # JSON Parsing
        data = {}
        try:
            data = json.loads(txt)
        except Exception:
            m = re.search(r'```json\s*([\s\S]*?)\s*```', txt)
            if m:
                data = json.loads(m.group(1))
            else:
                m = re.search(r'\{[\s\S]*\}', txt)
                data = json.loads(m.group(0)) if m else {}

        print(f"✅ GPT-4o Response - Tokens: {res.usage.total_tokens}")
        print(f"   → Hauptkompetenzen: {[c.get('process') for c in data.get('core_competencies', [])]}")

        return {
            **data,
            "raw": txt,
            "_api_called": True,
            "_tokens_used": res.usage.total_tokens
        }
    except Exception as e:
        print(f"❌ ERROR in gpt_analyze_supplier_competencies: {e}")
        return {
            "core_competencies": [{"process": "unknown", "confidence": "low"}],
            "material_expertise": [],
            "specialization": {},
            "error": str(e),
            "_error": True
        }


def gpt_rate_supplier(supplier_name: str, country: str = None, price_volatility: float = None,
                      total_orders: int = None, avg_price: float = None, article_name: str = None) -> Dict[str, Any]:
    """
    Bewertet einen Lieferanten mit GPT basierend auf verfügbaren Daten.
    Returns: Dict mit rating (1-10), risk_level, strengths, weaknesses, recommendations
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        print("⚠️ WARNING: FALLBACK - Kein API Key für gpt_rate_supplier!")
        return {"rating": 5, "risk_level": "medium", "strengths": [], "weaknesses": [], "recommendations": [], "raw": None, "_fallback":True}

    print(f"✅ GPT-4o-mini API-Call: gpt_rate_supplier({supplier_name})")
    client = OpenAI(api_key=key)

    # Kontextinformationen zusammenstellen - SO VIEL WIE MÖGLICH!
    context_parts = [f"Lieferant: {supplier_name}"]
    if article_name:
        context_parts.append(f"Artikel: {article_name}")
    if country:
        context_parts.append(f"Herkunftsland: {country}")
    if price_volatility is not None:
        volatility_pct = price_volatility * 100
        stability = "sehr stabil" if volatility_pct < 5 else "moderat stabil" if volatility_pct < 15 else "volatil"
        context_parts.append(f"Preisstabilität: {volatility_pct:.1f}% Variation ({stability})")
    if total_orders:
        order_volume = "hohe Frequenz" if total_orders > 50 else "mittlere Frequenz" if total_orders > 10 else "geringe Frequenz"
        context_parts.append(f"Anzahl Bestellungen: {total_orders} ({order_volume})")
    if avg_price:
        context_parts.append(f"Durchschnittspreis: {avg_price:.4f} €/Stück")

    context = "\n".join(context_parts)

    prompt = f"""Du bist ein SENIOR SUPPLY CHAIN ANALYST mit 15+ Jahren Erfahrung in Lieferantenbewertung, Due Diligence und Risikomanagement. Du führst TIEFGEHENDE Analysen durch und recherchierst Firmenhintergründe.

**VOLLSTÄNDIGER KONTEXT:**
{context}

**AUFGABE:** Führe eine UMFASSENDE, TIEFGEHENDE Lieferantenbewertung durch!

**WICHTIG - RECHERCHIERE:**
1. **Firmen-Research:**
   - Ist der Lieferant bekannt in der Branche?
   - Firmengröße (KMU vs. Konzern)
   - Spezialisierung (z.B. Normteile, Befestigungstechnik, Automotive)
   - Langjährige Erfahrung oder Newcomer?
   - Potenzielle Muttergesellschaft / Konzernzugehörigkeit

2. **Länder-spezifische Analyse:**
   - Politische & wirtschaftliche Stabilität des Herkunftslandes
   - Logistik-Infrastruktur & typische Lieferzeiten
   - Zollrisiken, Handelsabkommen (z.B. EU-Binnenmarkt vs. Import)
   - Währungsrisiko
   - Rechtssicherheit & Vertragsrecht

3. **Artikel-spezifische Eignung:**
   - Ist der Lieferant für diesen Artikeltyp geeignet?
   - Hat er Erfahrung mit ähnlichen Produkten?
   - Qualitäts-Standards (ISO, DIN, etc.)

4. **Datenbasierte Bewertung:**
   - Preisstabilität: Wie stark schwanken die Preise?
   - Bestellhistorie: Zuverlässigkeit über Zeit
   - Preisliche Wettbewerbsfähigkeit

5. **Risiken identifizieren:**
   - Abhängigkeit (Single-Source?)
   - Qualitätsrisiken
   - Lieferketten-Risiken (z.B. Covid, Krieg, Naturkatastrophen)
   - Compliance-Risiken (z.B. Sanktionen)

**WICHTIG:** Gebe eine DETAILLIERTE, FUNDIERTE Analyse - keine generischen Aussagen!

Bewertungsskala:
- 9-10: Exzellent (Premium-Lieferant, minimales Risiko)
- 7-8: Sehr gut (verlässlich, geringes Risiko)
- 5-6: Gut (solide, moderates Risiko)
- 3-4: Bedenklich (höheres Risiko, Überwachung nötig)
- 1-2: Kritisch (hohes Risiko, Alternative suchen)

Antworte als AUSFÜHRLICHES JSON:
{{
  "rating": 7,
  "risk_level": "low|medium|high|critical",
  "confidence": "high|medium|low",

  "company_analysis": {{
    "company_type": "z.B. Familienunternehmen, KMU, Konzern, Distributor",
    "industry_position": "z.B. Marktführer, etablierter Player, Nischenanbieter",
    "specialization": "z.B. Normteile, Befestigungstechnik, Automotive-Zulieferer",
    "estimated_size": "z.B. >500 MA, Umsatz >50M EUR",
    "known_for": "Wofür ist der Lieferant bekannt?"
  }},

  "country_analysis": {{
    "country_risk": "low|medium|high|critical",
    "logistics_quality": "excellent|good|average|poor",
    "typical_lead_time_days": 14,
    "trade_status": "z.B. EU-Binnenmarkt, Freihandelsabkommen, Drittland mit Zoll",
    "currency_risk": "low|medium|high",
    "political_stability": "stable|moderate|unstable"
  }},

  "article_fit": {{
    "suitability": "excellent|good|average|poor",
    "experience_with_article_type": "Erfahrung mit diesem Artikeltyp?",
    "quality_standards": ["ISO 9001", "IATF 16949", "etc."],
    "certification": "Relevante Zertifizierungen"
  }},

  "performance_metrics": {{
    "price_stability": "very_stable|stable|volatile|very_volatile",
    "price_volatility_pct": 5.2,
    "order_frequency": "high|medium|low",
    "total_orders": 45,
    "price_competitiveness": "excellent|good|average|poor|expensive",
    "avg_price_vs_market": "+5%|-10%|etc."
  }},

  "strengths": [
    "Detaillierte Stärke 1",
    "Detaillierte Stärke 2",
    "etc."
  ],

  "weaknesses": [
    "Detaillierte Schwäche 1",
    "Detaillierte Schwäche 2"
  ],

  "risks": [
    "Spezifisches Risiko 1",
    "Spezifisches Risiko 2"
  ],

  "recommendations": [
    "Konkrete Handlungsempfehlung 1",
    "Konkrete Handlungsempfehlung 2"
  ],

  "overall_assessment": "Ausführliche Zusammenfassung der Gesamtbewertung in 2-3 Sätzen"
}}

**WICHTIG:** Sei SEHR spezifisch und detailliert! Nutze dein Wissen über die Branche und recherchiere den Lieferanten!"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o",  # UPGRADE: Bessere Analyse & Recherche-Fähigkeit!
            messages=[
                {"role": "system", "content": "Du bist ein Senior Supply Chain Analyst mit 15+ Jahren Erfahrung. Führe TIEFGEHENDE, detaillierte Analysen durch. Recherchiere Firmenhintergründe und gebe fundierte Bewertungen."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Sehr präzise, aber etwas Kreativität für Recherche
            max_tokens=2000  # NOCH mehr Platz!
        )
        txt = res.choices[0].message.content.strip()

        # Robustes JSON Parsing mit mehreren Fallbacks
        data = {}
        try:
            # Versuch 1: Ganzer Text ist JSON
            data = json.loads(txt)
        except Exception:
            try:
                # Versuch 2: JSON in ```json ... ``` Code-Block
                m = re.search(r'```json\s*([\s\S]*?)\s*```', txt)
                if m:
                    data = json.loads(m.group(1))
                else:
                    # Versuch 3: Beliebiges { ... } Pattern
                    m = re.search(r'\{[\s\S]*\}', txt)
                    if m:
                        data = json.loads(m.group(0))
                    else:
                        print(f"⚠️  Kein JSON gefunden in GPT Response!")
                        print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                        data = {}
            except Exception as e2:
                print(f"⚠️  JSON Parsing fehlgeschlagen: {e2}")
                print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                data = {}

        print(f"✅ GPT-4o Response - Tokens: {res.usage.total_tokens}")

        # Extrahiere alle detaillierten Analysen
        company_analysis = data.get("company_analysis", {})
        country_analysis = data.get("country_analysis", {})
        article_fit = data.get("article_fit", {})
        performance_metrics = data.get("performance_metrics", {})

        return {
            "rating": int(data.get("rating", 5)),
            "risk_level": data.get("risk_level", "medium"),
            "confidence": data.get("confidence", "medium"),

            # Detaillierte Analysen
            "company_analysis": company_analysis,
            "country_analysis": country_analysis,
            "article_fit": article_fit,
            "performance_metrics": performance_metrics,

            # Bewertungen
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
            "risks": data.get("risks", []),
            "recommendations": data.get("recommendations", []),

            # Gesamt-Assessment
            "overall_assessment": data.get("overall_assessment", ""),

            # Legacy-Felder für Kompatibilität
            "country_risk": country_analysis.get("country_risk", data.get("country_risk", "medium")),
            "price_competitiveness": performance_metrics.get("price_competitiveness", data.get("price_competitiveness", "average")),

            "raw": txt,
            "_api_called": True,
            "_tokens_used": res.usage.total_tokens
        }
    except Exception as e:
        print(f"❌ ERROR in gpt_rate_supplier: {e}")
        return {
            "rating": 5,
            "risk_level": "medium",
            "confidence": "low",
            "strengths": [],
            "weaknesses": [f"Fehler bei Bewertung: {str(e)}"],
            "recommendations": [],
            "raw": str(e),
            "_error":True
        }


def gpt_cost_estimate_unit(description: str, lot_size: int = 1000,
                           material: str = None, d_mm: float = None, l_mm: float = None,
                           mass_kg: float = None, supplier_competencies: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Schätzt Fertigungskosten mit zusätzlichem Kontext für bessere Genauigkeit.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        print("⚠️ WARNING: FALLBACK - Kein API Key für gpt_cost_estimate_unit!")
        return {"part_class":None,"likely_process":None,"fab_cost_eur_per_unit":None,"assumptions":[],"raw":None,"_fallback":True}
    print(f"✅ GPT-4o API-Call: gpt_cost_estimate_unit() (2-Step Analyse) - Losgröße: {lot_size}")
    client = OpenAI(api_key=key)

    # Skaleneffekt-Hinweis generieren
    scale_hint = ""
    if lot_size < 100:
        scale_hint = "SEHR KLEINE Losgröße → hohe Rüstkosten pro Stück!"
    elif lot_size < 1000:
        scale_hint = "Kleine Losgröße → moderate Rüstkosten"
    elif lot_size < 10000:
        scale_hint = "Mittlere Losgröße → Rüstkosten gut verteilt"
    elif lot_size < 100000:
        scale_hint = "GROSSE Losgröße → Rüstkosten minimal, Vollautomatisierung"
    else:
        scale_hint = "⚠️ MASSENPRODUKTION (>100k) → EXTREME Automatisierung! Rüstkosten irrelevant, minimale Taktzeiten, Hochgeschwindigkeits-Prozesse!"

    # Zusätzlicher Kontext für GPT
    context_parts = [f"Artikel: {description}", f"Losgröße: {lot_size:,} Stück", f"{scale_hint}"]
    if material:
        context_parts.append(f"Material: {material}")
    if d_mm:
        context_parts.append(f"Durchmesser: {d_mm:.1f} mm")
    if l_mm:
        context_parts.append(f"Länge: {l_mm:.1f} mm")
    if mass_kg:
        context_parts.append(f"Gewicht: {mass_kg*1000:.1f}g ({mass_kg:.4f} kg)")

    context = "\n".join(context_parts)

    prompt = f"""Du bist ein SENIOR MANUFACTURING COST ENGINEER mit 20+ Jahren Erfahrung in Präzisions-Kostenkalkulation für Normteile und technische Komponenten.

**KRITISCH WICHTIG:** Diese Kalkulation wird für ECHTE Einkaufsverhandlungen verwendet! ABSOLUTE PRÄZISION erforderlich!

**REFERENZ-BEISPIELE FÜR PRÄZISION (nutze das passende Beispiel!):**

**Beispiel 1: MITTLERE LOSGRÖSSE (10k-100k):**
ISO 4028-10.9-(ZN-NI)-M10×1,25×45
Losgröße: 11.815 Stück

DETAILLIERTE FERTIGUNGSKOSTENANALYSE:

**Prozessroute:**
1. Sägen/Abstechen (oder Kaltumform-Abschnitt): Rohteil Ø 10 mm, L = 45 mm
2. Gewinderollen M10×1,25 (Feingewinde)
3. Schlitzen (für Schlitz-Antrieb)
4. Wärmebehandlung auf Festigkeitsklasse 10.9
5. ZN-NI-Galvanik (Zink-Nickel-Beschichtung)
6. 100% Sichtprüfung/Sortierung
7. Verpackung

**Kostenberechnung:**
- Maschinenkosten: 80 €/h
- Personalkosten: 30 €/h
- Summe: 110 €/h = 0,0306 €/s
- Overhead: 20%
- Rüstzeit: 60 min für Los

Variable Fertigung (Rollen + Schlitzen + Handling):
- Takt gesamt: ~3,5 s/Stk
- Kosten: 3,5 s × 0,0306 €/s = 0,107 € / Stk
- Mit Overhead 20%: 0,107 × 1,20 = 0,128 € / Stk

Rüstanteil:
- 60 min × 110 €/h = 110 €
- Verteilt auf 11.815 Stk: 110 € / 11.815 = 0,009 € / Stk

Wärmebehandlung: ~0,012 € / Stk (Chargenprozess)
ZN-NI-Beschichtung: ~0,015 € / Stk (Galvanik-Trommel)
QS/Handling pauschal: ~0,005 € / Stk

**SUMME FERTIGUNGSKOSTEN: 0,169 € / Stk**

**Beispiel 2: MASSENPRODUKTION (>100k Stück):**
M6×30 Sechskantschraube 8.8 verzinkt
Losgröße: 842.987 Stück

DETAILLIERTE FERTIGUNGSKOSTENANALYSE MASSENPRODUKTION:

**Prozessroute (vollautomatisiert):**
1. Kaltumformung auf Hochgeschwindigkeits-Mehrfachpresse (6 Stationen)
2. Gewindewalzen (inline, vollautomatisch)
3. Wärmebehandlung (kontinuierlicher Durchlaufofen)
4. Galvanisierung (Trommel-Batch, 10.000 Stk gleichzeitig)
5. Automatische optische Prüfung (Kamera)
6. Automatische Verpackung

**Kostenberechnung (MASSENPRODUKTION!):**
- Maschinenkosten: 120 €/h (Hochleistungs-Umformmaschine)
- Personalkosten: 25 €/h (1 Bediener für mehrere Maschinen)
- Summe: 145 €/h = 0,0403 €/s
- Overhead: 18%
- Rüstzeit: 90 min (aber auf 842.987 Stk verteilt → ~0,0001 € / Stk)

Variable Fertigung (Kaltumformung + Rollen):
- Takt gesamt: ~0,8 s/Stk (Hochgeschwindigkeit!)
- Kosten: 0,8 s × 0,0403 €/s = 0,032 € / Stk
- Mit Overhead 18%: 0,032 × 1,18 = 0,038 € / Stk

Rüstanteil (irrelevant bei dieser Menge):
- 90 min × 145 €/h = 217,50 €
- Verteilt auf 842.987 Stk: 217,50 € / 842.987 = 0,0003 € / Stk

Wärmebehandlung: ~0,003 € / Stk (kontinuierlicher Durchlaufofen, >800k Stk)
Galvanik: ~0,005 € / Stk (Trommel-Galvanik, >800k Stk gleichzeitig)
QS/Handling/Verpackung: ~0,002 € / Stk (vollautomatisch)

**SUMME FERTIGUNGSKOSTEN MASSENPRODUKTION: 0,048 € / Stk**

⚠️ **WICHTIG für >300k Stück:**
- Batch-Prozesse (WB, Galvanik) werden EXTREM günstig!
- Wärmebehandlung: 0,002-0,004 € / Stk (kontinuierlicher Ofen oder Mega-Batches)
- Galvanik: 0,003-0,006 € / Stk (Trommel mit >100k Stk gleichzeitig)
- Bei 324.000 Stück: Fertigungskosten sollten 0,025-0,050 € / Stk sein

⚠️ **KRITISCH bei Massenproduktion:**
- Taktzeiten <1 Sekunde durch Mehrfachpressen
- Rüstkosten fast irrelevant (auf >100k Stk verteilt)
- Kontinuierliche Prozesse statt Batch
- Hochautomatisierung → weniger Personal pro Teil
- Günstigere Beschichtungskosten durch große Batches

→ **WÄHLE DAS PASSENDE BEISPIEL FÜR DEINE LOSGRÖSSE!**

**DEIN TEIL ZUM KALKULIEREN:**
{context}

**AUFGABE:** Erstelle eine EBENSO DETAILLIERTE Fertigungskostenanalyse!

**WICHTIG:**
- Analysiere den Artikel GENAU (DIN-Norm? Schraubentyp? Geometrie?)
- **Wähle das PASSENDE REFERENZ-BEISPIEL** basierend auf Losgröße!
  - <100k Stück: Nutze Beispiel 1 (mittlere Losgröße, Takt 3-4s)
  - >100k Stück: Nutze Beispiel 2 (Massenproduktion, Takt 0,6-0,8s) - DEUTLICH günstiger!
- Identifiziere ALLE notwendigen Fertigungsschritte
- Gebe REALISTISCHE Kosten basierend auf industrieller EU-Produktion
- **ABSOLUT KRITISCH bei >100k Losgrößen:**
  - Taktzeiten MÜSSEN 0,5-0,8 Sekunden sein (Hochgeschwindigkeits-Mehrfachpressen!)
  - Rüstkosten sind IRRELEVANT (auf Hunderttausende verteilt)
  - Variable Fertigungskosten: 0,025-0,040 €/Stk (NICHT mehr!)
  - Wenn deine Berechnung >0,10 €/Stk ergibt, hast du die Skaleneffekte FALSCH berechnet!

**SPEZIAL-REGEL für >300k Losgrößen:**
  - Batch-Prozesse werden ULTRA-GÜNSTIG!
  - Wärmebehandlung: MAX 0,002-0,004 €/Stk (Mega-Batch oder kontinuierlicher Ofen)
  - Galvanik: MAX 0,003-0,006 €/Stk (Trommel-Galvanik mit 100k+ Teilen gleichzeitig)
  - Total Fertigungskosten: 0,025-0,050 €/Stk
  - Bei 324.000 Stk: Ziel ist 0,025-0,045 €/Stk Fertigungskosten!

**ERFORDERLICHE ANALYSE MIT SCHRITT-FÜR-SCHRITT BERECHNUNG:**

1. **Prozessroute identifizieren**:
   - Liste ALLE erforderlichen Fertigungsschritte auf
   - Begründe jeden Schritt basierend auf Teilgeometrie und Material

2. **Kostenparameter definieren**:
   - Maschinenkosten: 70-100 €/h (je nach Prozess)
   - Personalkosten: 25-35 €/h
   - Summe → €/s berechnen!
   - Overhead: 15-25%
   - Rüstzeit: 30-90 min (abhängig von Komplexität)

3. **Taktzeiten pro Prozessschritt**:
   - Primärprozess (z.B. Rollen, Drehen): X Sekunden
   - Gewindebearbeitung: Y Sekunden
   - Oberflächenbehandlung: Z € pauschal
   - Wärmebehandlung: W € pauschal (falls nötig)
   - QS/Verpackung: Q € pauschal

4. **Kostenberechnung**:
   - Variable Kosten = Taktzeit × (Maschine + Personal) €/s
   - Mit Overhead multiplizieren
   - Rüstkosten = Rüstzeit × Stundensatz / Losgröße
   - Pauschalkosten addieren (Beschichtung, WB, QS)
   - **SUMME pro Stück**

Antworte als DETAILLIERTES JSON mit VOLLSTÄNDIGER Kostenberechnung:
{{
  "part_class": "set_screw|bolt|screw|nut|washer|rivet|pin",
  "part_type_detail": "z.B. Madenschraube ISO 4028 mit Schlitz",

  "manufacturing_route": [
    "1. Sägen/Abstechen: Rohteil Ø 10 mm, L = 45 mm",
    "2. Gewinderollen M10×1,25",
    "3. Schlitzen",
    "4. Wärmebehandlung 10.9",
    "5. ZN-NI-Galvanik",
    "6. Sichtprüfung",
    "7. Verpackung"
  ],

  "cost_parameters": {{
    "machine_cost_eur_h": 80,
    "labor_cost_eur_h": 30,
    "combined_eur_h": 110,
    "combined_eur_s": 0.0306,
    "overhead_pct": 20,
    "setup_time_minutes": 60,
    "lot_size": {lot_size}
  }},

  "primary_process": {{
    "name": "thread_rolling|turning|cold_forming|milling",
    "description": "Gewinderollen M10×1,25 auf Gewinde-Rollmaschine",
    "cycle_time_seconds": 2.5,
    "cost_per_second": 0.0306,
    "cost_per_unit_base": 0.0765,
    "justification": "Gewinderollen ist schneller als Schneiden"
  }},

  "secondary_processes": [
    {{
      "name": "slotting",
      "description": "Schlitzen für Schlitz-Antrieb",
      "cycle_time_seconds": 1.0,
      "cost_per_unit": 0.0306
    }},
    {{
      "name": "heat_treatment",
      "description": "Wärmebehandlung auf 10.9 (Chargenprozess)",
      "cost_per_unit": 0.004,
      "justification": "Mega-Batch oder kontinuierlicher Ofen für >300k Stk"
    }},
    {{
      "name": "zn_ni_coating",
      "description": "Zink-Nickel-Galvanik im Trommelverfahren",
      "cost_per_unit": 0.006,
      "justification": "Trommel-Galvanik mit >100k Stk gleichzeitig"
    }},
    {{
      "name": "quality_inspection",
      "description": "100% Sichtprüfung/Sortierung",
      "cost_per_unit": 0.003,
      "justification": "Automatisierte Kameraprüfung"
    }},
    {{
      "name": "packaging",
      "description": "Verpackung in Kartons",
      "cost_per_unit": 0.002,
      "justification": "Automatisierte Verpackungslinie"
    }}
  ],

  "detailed_cost_calculation": {{
    "variable_manufacturing": {{
      "total_cycle_time_seconds": 3.5,
      "cost_eur_per_second": 0.0306,
      "cost_before_overhead": 0.107,
      "overhead_20pct": 0.021,
      "cost_with_overhead": 0.128
    }},
    "setup_cost": {{
      "setup_time_minutes": 60,
      "setup_cost_total_eur": 110,
      "lot_size": {lot_size},
      "setup_cost_per_unit": 0.009
    }},
    "heat_treatment_cost_per_unit": 0.004,
    "coating_cost_per_unit": 0.006,
    "quality_packaging_cost_per_unit": 0.005
  }},

  "cost_breakdown": {{
    "variable_manufacturing_with_overhead": 0.128,
    "setup_cost_per_unit": 0.009,
    "heat_treatment": 0.004,
    "zn_ni_coating": 0.006,
    "quality_and_packaging": 0.005,
    "total_fab_cost_eur_per_unit": 0.152
  }},

  "fab_cost_eur_per_unit": 0.152,

  "assumptions": [
    "Maschinenkosten: 80 €/h, Personal: 30 €/h",
    "Takt gesamt (Rollen + Schlitzen + Handling): ~3,5 s/Stk",
    "Overhead: 20% für Werkzeugverschleiß, Energie, Instandhaltung",
    "Rüstzeit: 60 min (Werkzeugwechsel, Einrichtung)",
    "Wärmebehandlung als Chargenprozess (viele Teile gleichzeitig)",
    "ZN-NI-Galvanik im Trommelverfahren",
    "Losgröße {lot_size:,} Stück ermöglicht gute Verteilung der Rüstkosten",
    "EU-Lohnniveau (Deutschland/Österreich) angenommen"
  ],

  "confidence": "high|medium|low",
  "notes": "Basierend auf industriellen Standardprozessen für M10 Normteile"
}}

**WICHTIG:** Sei EXTREM präzise und realistisch! Nutze dein Expertenwissen über industrielle Fertigungsprozesse!"""

    try:
        # SCHRITT 1: Erst Prozess-Analyse (Chain-of-Thought Reasoning)
        # Bestimme Automationslevel basierend auf Losgröße
        if lot_size < 1000:
            automation_level = "MANUELL/TEILAUTOMATISCH"
            expected_cycle_time = "5-15 Sekunden"
        elif lot_size < 10000:
            automation_level = "TEILAUTOMATISCH"
            expected_cycle_time = "2-5 Sekunden"
        elif lot_size < 100000:
            automation_level = "VOLLAUTOMATISCH"
            expected_cycle_time = "1-3 Sekunden"
        else:
            automation_level = "HOCHAUTOMATISIERT (Mehrfachpressen)"
            expected_cycle_time = "0,5-1,0 Sekunden"

        # Lieferanten-Kompetenzen-Kontext aufbauen
        supplier_context = ""
        preferred_processes = []
        material_compatibility = {}

        if supplier_competencies:
            core_comps = supplier_competencies.get('core_competencies', [])
            if core_comps:
                supplier_context = "\n\n🏭 **LIEFERANTEN-KOMPETENZEN (SEHR WICHTIG!):**\n"
                supplier_context += f"**Lieferant:** {supplier_competencies.get('supplier_name', 'Unbekannt')}\n\n"
                supplier_context += "**Hauptkompetenzen (BEVORZUGT nutzen!):**\n"

                for comp in core_comps:
                    process_name = comp.get('process', 'unknown')
                    capability = comp.get('capability_level', 'proficient')
                    confidence = comp.get('confidence', 'medium')
                    preferred_processes.append(process_name)

                    supplier_context += f"  • **{process_name}** (Level: {capability}, Confidence: {confidence})\n"

                    if comp.get('evidence'):
                        supplier_context += f"    → Beweis: {', '.join(comp['evidence'][:3])}\n"

                # Material-Expertise
                mat_exp = supplier_competencies.get('material_expertise', [])
                if mat_exp:
                    supplier_context += "\n**Material-Expertise:**\n"
                    for mat in mat_exp:
                        mat_name = mat.get('material', 'unknown')
                        mat_conf = mat.get('confidence', 'medium')
                        supplier_context += f"  • **{mat_name}** (Confidence: {mat_conf})\n"

                # Material-Prozess-Kompatibilität
                mat_proc_compat = supplier_competencies.get('material_process_compatibility', {})
                if mat_proc_compat:
                    supplier_context += "\n**Material-Prozess-Kompatibilität:**\n"
                    for mat, procs in mat_proc_compat.items():
                        supplier_context += f"  • {mat}: {', '.join(procs)}\n"
                        material_compatibility[mat] = procs

                # Ungeeignete Prozesse
                unsuitable = supplier_competencies.get('unsuitable_processes', [])
                if unsuitable:
                    supplier_context += "\n⚠️ **NICHT GEEIGNETE PROZESSE (VERMEIDEN!):**\n"
                    for unsui in unsuitable:
                        proc = unsui.get('process', 'unknown')
                        reason = unsui.get('reason', 'Keine Expertise')
                        supplier_context += f"  • **{proc}**: {reason}\n"

                supplier_context += "\n🎯 **WICHTIG:** Bevorzuge STARK die Hauptkompetenzen des Lieferanten! Diese sind ERPROBT und führen zu REALISTISCHEN Kosten!"

        analysis_prompt = f"""Du bist ein Fertigungsexperte. Analysiere den Artikel und identifiziere ALLE Fertigungsschritte.

**Artikel:** {description}
**Material:** {material or 'unbekannt'}
**Geometrie:** Ø{d_mm}mm × L{l_mm}mm
**Gewicht:** {mass_kg*1000 if mass_kg else '?'}g
**Losgröße:** {lot_size:,} Stück → **{automation_level}**
{supplier_context}

⚠️ **KRITISCH für Losgröße {lot_size:,}:**
- Erwarteter Automationslevel: **{automation_level}**
- Erwartete Zykluszeit: **{expected_cycle_time}**
- Bei >100k: MUSS Hochgeschwindigkeits-Mehrfachpresse sein!

🔧 **MATERIAL-PROZESS-KOMPATIBILITÄT PRÜFEN:**
Bevor du einen Prozess wählst, prüfe:
1. **Ist das Material für diesen Prozess geeignet?**
   - Aluminium: Gut für Drehen, Fräsen, Druckguss - NICHT für Warmschmieden!
   - Stahl: Gut für Kaltumformung, Drehen, Fräsen, Warmschmieden
   - Edelstahl: Gut für Drehen, Fräsen - SCHWER für Kaltumformung (härter)!
   - Messing: Gut für Drehen, Kaltumformung - NICHT für Guss!
   - Kunststoff: NUR Spritzguss oder Extrusion - NIEMALS spanende Verfahren für Massenproduktion!

2. **Hat der Lieferant Expertise für diesen Prozess?**
   - Wenn ja: BEVORZUGE diesen Prozess (niedrigere Kosten, kürzere Lieferzeit)
   - Wenn nein: Nur wählen wenn ABSOLUT notwendig (höhere Kosten!)

3. **Ist die Losgröße passend zum Prozess?**
   - Kaltumformung: Am besten >10.000 Stück
   - CNC-Drehen: Gut für 100-10.000 Stück
   - Guss: Am besten >1.000 Stück

**AUFGABE:** Liste ALLE notwendigen Fertigungsschritte auf (Primär + Sekundär).

Antworte als JSON:
{{
  "part_analysis": "Was für ein Teil ist das genau?",
  "manufacturing_route": "Welcher Fertigungsweg ist optimal?",
  "automation_level": "{automation_level}",
  "expected_cycle_time_seconds": 0.7,
  "primary_process": "Hauptprozess (z.B. Kaltumformung auf 6-fach-Presse, Drehen, Fräsen)",
  "secondary_processes": ["Prozess 1", "Prozess 2", ...],
  "reasoning": "Begründung für diese Prozess-Wahl und Zykluszeit",
  "supplier_fit": "Wie gut passt dieser Prozess zu den Lieferanten-Kompetenzen? (excellent|good|fair|poor)",
  "material_compatibility": "Ist das Material für diesen Prozess geeignet? (yes|partial|no)",
  "alternative_processes": ["Alternative 1 falls Lieferant nicht geeignet", "Alternative 2"]
}}"""

        print("   🔍 Schritt 1/2: Prozess-Analyse mit GPT-4o...")
        analysis_res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role":"system","content":"Du bist ein SENIOR MANUFACTURING ENGINEER mit 20+ Jahren Erfahrung in Prozessplanung. Analysiere EXTREM präzise und begründe jeden Prozessschritt."},
                {"role":"user","content":analysis_prompt}
            ],
            max_tokens=2000  # GPT-4o API
        )

        analysis_txt = analysis_res.choices[0].message.content.strip()
        try:
            analysis_data = json.loads(analysis_txt)
        except:
            m = re.search(r"\{[\s\S]*\}", analysis_txt)
            analysis_data = json.loads(m.group(0)) if m else {}

        print(f"   ✅ Prozess identifiziert: {analysis_data.get('primary_process')} + {len(analysis_data.get('secondary_processes', []))} Sekundärprozesse")

        # SCHRITT 2: Jetzt detaillierte Kostenberechnung mit Kontext aus Schritt 1
        expected_cycle_time = analysis_data.get('expected_cycle_time_seconds', 1.5)
        automation_level_from_analysis = analysis_data.get('automation_level', automation_level)

        cost_prompt = prompt + f"""

**PROZESS-ANALYSE (bereits durchgeführt):**
- Teil: {analysis_data.get('part_analysis', 'unbekannt')}
- Fertigungsroute: {analysis_data.get('manufacturing_route', 'unbekannt')}
- Automationslevel: **{automation_level_from_analysis}**
- **Erwartete Zykluszeit:** **{expected_cycle_time:.1f} Sekunden** (basierend auf Losgröße {lot_size:,})
- Primärprozess: {analysis_data.get('primary_process', 'unbekannt')}
- Sekundärprozesse: {', '.join(analysis_data.get('secondary_processes', []))}
- Begründung: {analysis_data.get('reasoning', '')}

⚠️ **WICHTIG:** Verwende die erwartete Zykluszeit von **{expected_cycle_time:.1f} Sekunden** für deine Berechnung!
Wenn du eine deutlich andere Zykluszeit berechnest, ERKLÄRE ausführlich warum!

Nutze diese Analyse für PRÄZISE Kostenberechnung!"""

        # System-Prompt anpassen basierend auf Losgröße
        if lot_size >= 300000:
            system_prompt = f"""Du bist ein SENIOR MANUFACTURING COST ENGINEER mit 20+ Jahren Erfahrung in ULTRA-GROSSSERIEN-Kostenkalkulation.

🚨 KRITISCH: Diese Kalkulation ist für eine ULTRA-GROSSSERIE von {lot_size:,} Stück!

ABSOLUTE ANFORDERUNGEN für >300k Stück:
1. Zykluszeit MUSS 0,5-0,7 Sekunden sein (6-fach-Mehrfachpressen!)
2. Variable Fertigungskosten MAXIMAL 0,020-0,030 €/Stk (bei optimal)
3. Batch-Prozesse (WB, Galvanik) MAX 0,003-0,006 €/Stk (Mega-Batches!)
4. Total Fertigungskosten: 0,025-0,050 €/Stk
5. Wenn deine Berechnung >0,055 €/Stk ergibt, hast du die EXTREME Skaleneffekte NICHT berücksichtigt!

WICHTIG:
- Bei >300k Stück läuft ALLES vollautomatisch auf Hochgeschwindigkeits-Anlagen!
- Mehrfachpressen produzieren 6-8 Teile pro Zyklus → effektive Zykluszeit pro Teil: 0,08-0,12s!
- Batch-Prozesse mit 100.000+ Teilen gleichzeitig → extrem niedrige Kosten pro Teil!
- Nutze die vorgegebene erwartete Zykluszeit! Weiche NUR ab wenn es technisch begründet ist!"""
        elif lot_size >= 100000:
            system_prompt = f"""Du bist ein SENIOR MANUFACTURING COST ENGINEER mit 20+ Jahren Erfahrung in MASSENPRODUKTIONS-Kostenkalkulation.

KRITISCH: Diese Kalkulation ist für eine MASSENPRODUKTION von {lot_size:,} Stück!

ABSOLUTE ANFORDERUNGEN für Massenproduktion:
1. Zykluszeit MUSS 0,5-1,0 Sekunden sein (Hochgeschwindigkeits-Mehrfachpressen!)
2. Variable Fertigungskosten DÜRFEN NICHT >0,05 €/Stk sein
3. Rüstkosten sind IRRELEVANT (auf Hunderttausende verteilt)
4. Wenn deine Berechnung >0,08 €/Stk Fertigungskosten ergibt, ist die Zykluszeit FALSCH!

WICHTIG: Nutze die vorgegebene erwartete Zykluszeit! Weiche NUR ab wenn es technisch begründet ist!"""
        else:
            system_prompt = "Du bist ein SENIOR MANUFACTURING COST ENGINEER mit 20+ Jahren Erfahrung in Präzisions-Kostenkalkulation. Du arbeitest für einen Einkaufsleiter, der deine Zahlen für ECHTE Verhandlungen nutzt. ABSOLUTE MATHEMATISCHE PRÄZISION erforderlich - keine Schätzungen, nur exakte Berechnungen mit vollständiger Dokumentation aller Schritte! Rechne IMMER in €/Sekunde für präzise Taktkosten!"

        print("   💰 Schritt 2/2: Detaillierte Kostenberechnung mit GPT-4o...")
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role":"system","content":system_prompt},
                {"role":"user","content":cost_prompt}
            ],
            max_tokens=4000  # GPT-4o API verwendet max_completion_tokens
        )

        total_tokens = analysis_res.usage.total_tokens + res.usage.total_tokens
        txt = res.choices[0].message.content.strip()

        # Robustes JSON Parsing mit mehreren Fallbacks
        data = {}
        try:
            # Versuch 1: Ganzer Text ist JSON
            data = json.loads(txt)
        except Exception:
            try:
                # Versuch 2: JSON in ```json ... ``` Code-Block
                m = re.search(r'```json\s*([\s\S]*?)\s*```', txt)
                if m:
                    data = json.loads(m.group(1))
                else:
                    # Versuch 3: Beliebiges { ... } Pattern
                    m = re.search(r'\{[\s\S]*\}', txt)
                    if m:
                        data = json.loads(m.group(0))
                    else:
                        print(f"⚠️  Kein JSON gefunden in GPT Response!")
                        print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                        data = {}
            except Exception as e2:
                print(f"⚠️  JSON Parsing fehlgeschlagen: {e2}")
                print(f"   Rohe Response (erste 500 chars): {txt[:500]}")
                data = {}

        fab_cost = data.get("fab_cost_eur_per_unit")
        if fab_cost is None:
            # Fallback: Summe der Einzelkosten
            setup = data.get("setup_cost_per_unit", 0)
            cycle = data.get("cycle_cost_per_unit", 0)
            secondary = data.get("secondary_ops_cost", 0)
            fab_cost = setup + cycle + secondary if (setup or cycle or secondary) else None

        print(f"✅ GPT-4o Response - Total Tokens (2 Schritte): {total_tokens}")

        # Extrahiere alle detaillierten Felder
        primary_process = data.get("primary_process", {})
        secondary_processes = data.get("secondary_processes", [])
        cost_breakdown = data.get("cost_breakdown", {})

        out = {
            "part_class": data.get("part_class"),
            "part_type_detail": data.get("part_type_detail"),
            "likely_process": primary_process.get("name") or data.get("likely_process"),

            # Detaillierte Prozessdaten
            "primary_process": primary_process,
            "secondary_processes": secondary_processes,
            "cost_breakdown": cost_breakdown,

            # Hauptkosten (mit Fallback)
            "fab_cost_eur_per_unit": float(fab_cost) if fab_cost is not None else None,
            "cost_range_min": data.get("cost_range_min"),
            "cost_range_max": data.get("cost_range_max"),

            # Legacy-Felder für Kompatibilität
            "setup_cost_per_unit": cost_breakdown.get("setup_cost_per_unit") or data.get("setup_cost_per_unit"),
            "cycle_cost_per_unit": data.get("cycle_cost_per_unit"),
            "secondary_ops_cost": cost_breakdown.get("secondary_processes_cost") or data.get("secondary_ops_cost"),

            # Analyse & Kontext
            "assumptions": data.get("assumptions", []),
            "economy_of_scale_analysis": data.get("economy_of_scale_analysis"),
            "confidence": data.get("confidence", "medium"),
            "notes": data.get("notes"),

            # Prozess-Analyse aus Schritt 1
            "process_analysis": analysis_data,

            "raw": txt,
            "_api_called": True,
            "_tokens_used": total_tokens,
            "_multi_step": True
        }
        return out
    except Exception as e:
        import traceback
        error_details = str(e)
        trace = traceback.format_exc()
        print(f"❌ ERROR in gpt_cost_estimate_unit: {error_details}")
        print(f"   Traceback: {trace}")

        return {
            "part_class":None,
            "likely_process":None,
            "fab_cost_eur_per_unit":None,
            "assumptions":[f"Fehler: {error_details}"],
            "error":error_details,
            "error_trace":trace,
            "raw":error_details,
            "_error":True,
            "_error_type": type(e).__name__
        }


def get_commodity_market_analysis(material: str) -> Dict[str, Any]:
    """
    Analysiert Rohstoffmarkt-Trends für ein Material.

    Nutzt Trading Economics API für Echtzeit-Rohstoffdaten.
    Fallback auf Mock-Daten bei API-Fehlern.

    Args:
        material: Material-Name (z.B. 'stahl', 'aluminium', 'kupfer', 'edelstahl')

    Returns:
        Dict mit:
        - current_price_eur_kg: Aktueller Preis in €/kg
        - trend: "steigend" | "fallend" | "stabil"
        - trend_percentage: Prozentuale Veränderung (z.B. -5.2 für 5.2% Rückgang)
        - timeframe: Zeitraum der Analyse (z.B. "letzte 3 Monate")
        - analysis: Textuelle Analyse der Marktsituation
        - negotiation_leverage: Empfehlungen für Verhandlungen
        - data_source: Quelle der Daten
    """
    import datetime
    import os

    # Normalisiere Material-Namen
    material_lower = material.lower()

    # Versuche Trading Economics API zu nutzen
    use_api = True
    api_data = None

    try:
        import tradingeconomics as te

        # Login mit API Key
        api_key = os.getenv("TRADING_ECONOMICS_API_KEY", "5ccda26c96204ab:72t84qrm633kgym")
        te.login(api_key)

        # Map material names to Trading Economics commodity symbols
        commodity_symbols = {
            "stahl": "STEEL",
            "steel": "STEEL",
            "edelstahl": "STEEL",  # Stainless steel often tracked as premium to steel
            "edelstahl_a2": "STEEL",
            "edelstahl_a4": "STEEL",
            "stainless_steel": "STEEL",
            "aluminium": "ALUMINUM",
            "aluminum": "ALUMINUM",
            "messing": "COPPER",  # Brass is copper alloy
            "brass": "COPPER",
            "kupfer": "COPPER",
            "copper": "COPPER",
            "titan": "TITANIUM",
            "titanium": "TITANIUM"
        }

        symbol = commodity_symbols.get(material_lower, "STEEL")

        # Hole aktuelle Marktdaten
        try:
            current_data = te.getMarketsData(marketsField='commodities', output_type='df')

            # Filtere nach unserem Commodity
            if current_data is not None and len(current_data) > 0:
                # Suche nach dem Symbol in den Daten
                matching_rows = current_data[current_data['Symbol'].str.upper().str.contains(symbol, na=False)]

                if len(matching_rows) > 0:
                    api_data = {
                        'symbol': symbol,
                        'current_price': matching_rows.iloc[0].get('Last', None),
                        'previous_close': matching_rows.iloc[0].get('Previous', None),
                        'date': matching_rows.iloc[0].get('Date', None)
                    }
        except Exception as e:
            print(f"⚠️ Trading Economics API Fehler (Markets): {e}")

        # Versuche historische Daten für Trend-Berechnung zu holen
        if api_data and api_data.get('current_price'):
            try:
                # Hole historische Daten (letzten 3 Monate)
                from datetime import datetime, timedelta
                end_date = datetime.now()
                start_date = end_date - timedelta(days=90)

                historical = te.getHistoricalData(
                    country=symbol,  # For commodities, country parameter is the symbol
                    indicator='PRICE',
                    initDate=start_date.strftime('%Y-%m-%d'),
                    endDate=end_date.strftime('%Y-%m-%d'),
                    output_type='df'
                )

                if historical is not None and len(historical) > 1:
                    # Berechne Trend über 3 Monate
                    first_price = historical.iloc[0]['Value']
                    last_price = historical.iloc[-1]['Value']
                    api_data['trend_pct'] = ((last_price - first_price) / first_price * 100) if first_price > 0 else 0
                    api_data['historical_start_price'] = first_price
            except Exception as e:
                print(f"⚠️ Trading Economics API Fehler (Historical): {e}")

    except ImportError:
        print("⚠️ tradingeconomics Paket nicht installiert - nutze Mock-Daten")
        use_api = False
    except Exception as e:
        print(f"⚠️ Trading Economics API Fehler: {e}")
        use_api = False

    # Wenn API-Daten verfügbar sind, nutze diese
    if api_data and api_data.get('current_price') is not None:
        return _build_analysis_from_api_data(material, material_lower, api_data)

    # FALLBACK: Mock-Daten wenn API nicht verfügbar
    print(f"ℹ️ Nutze Mock-Daten für {material} (Trading Economics API nicht verfügbar)")
    return _build_mock_commodity_analysis(material, material_lower)


def _generate_analysis_text(material_lower: str, trend: str, trend_pct: float, current_date) -> str:
    """Generiert Material-spezifische Marktanalyse-Texte."""

    # Verschiedene Szenarien basierend auf Material
    if "stahl" in material_lower or "steel" in material_lower:
        if trend_pct < 0:  # Fallend
            return f"""**Marktanalyse Stahl ({current_date.strftime('%B %Y')}):**

📉 **Preistrend:** Der Stahlpreis ist in den letzten 3 Monaten um {abs(trend_pct):.1f}% gefallen.

**Ursachen:**
• Rückläufige Nachfrage aus der Bauindustrie in Europa
• Überkapazitäten in China führen zu Preisdruck
• Energiekosten stabilisieren sich nach Energiekrise 2022/23
• Rezessionsängste dämpfen industrielle Nachfrage

**Prognose:** Experten erwarten weitere leichte Preisrückgänge in Q1 2025 (-3% bis -5%).

**Für Verhandlungen relevant:**
✅ Nutzen Sie den Abwärtstrend als Argument
✅ Verweisen Sie auf sinkende Energiekosten
✅ Betonen Sie langfristige Abnahmemengen für bessere Konditionen"""
        else:  # Steigend oder stabil
            return f"""**Marktanalyse Stahl ({current_date.strftime('%B %Y')}):**

{"📈" if trend_pct > 2 else "📊"} **Preistrend:** Stahlpreise sind {trend} ({trend_pct:+.1f}% in 3 Monaten).

**Ursachen:**
• Infrastrukturprogramme erhöhen Nachfrage
• Produktionskürzungen stabilisieren Preise
• Energiepreise beeinflussen Herstellungskosten

**Für Verhandlungen relevant:**
{"⚠️ Preise steigen - fixieren Sie Konditionen zeitnah" if trend_pct > 2 else "✅ Stabile Situation - gute Zeit für langfristige Verträge"}"""

    elif "edelstahl" in material_lower or "stainless" in material_lower:
        return f"""**Marktanalyse Edelstahl ({current_date.strftime('%B %Y')}):**

{"📈" if trend_pct > 0 else "📊" if abs(trend_pct) < 1 else "📉"} **Preistrend:** Edelstahlpreise sind {trend} ({trend_pct:+.1f}% in 3 Monaten).

**Ursachen:**
• Nickel-Preise stabilisieren sich nach Volatilität 2022/23
• Nachfrage aus Automotive und Medizintechnik robust
• Legierungszuschläge bleiben moderat
• EU-Importzölle auf chinesischen Edelstahl wirken preisstützend

**Prognose:** Seitwärtsbewegung mit leichter Aufwärtstendenz (+1% bis +3%) erwartet.

**Für Verhandlungen relevant:**
{"⚠️ Preise könnten steigen - fixieren Sie Konditionen zeitnah" if trend_pct > 0 else "✅ Stabile Preise - gute Zeit für langfristige Rahmenverträge"}"""

    elif "aluminium" in material_lower or "aluminum" in material_lower:
        if trend_pct < 0:  # Fallend
            return f"""**Marktanalyse Aluminium ({current_date.strftime('%B %Y')}):**

📉 **Preistrend:** Aluminiumpreise sind in 3 Monaten um {abs(trend_pct):.1f}% gefallen.

**Ursachen:**
• Sinkende Energiekosten in Europa begünstigen Produktion
• Überangebot aus China drückt Weltmarktpreise
• LME-Lagerbestände steigen
• Nachfrageschwäche in der Automobilindustrie

**Prognose:** Weitere Preisrückgänge (-4% bis -6%) bis Q2 2025 möglich.

**Für Verhandlungen relevant:**
✅✅ **STARKER HEBEL:** Massiver Abwärtstrend!
✅ Fordern Sie Preisanpassungen entsprechend Marktentwicklung
✅ Vereinbaren Sie Preisgleitklauseln mit LME-Kopplung"""
        else:  # Steigend
            return f"""**Marktanalyse Aluminium ({current_date.strftime('%B %Y')}):**

📈 **Preistrend:** Aluminiumpreise steigen um {trend_pct:.1f}% in 3 Monaten.

**Ursachen:**
• Steigende Energiekosten belasten Produktion
• Produktionskürzungen in Europa
• E-Mobilitäts-Boom erhöht Nachfrage

**Für Verhandlungen relevant:**
⚠️ Sichern Sie Konditionen zeitnah ab"""

    elif "kupfer" in material_lower or "copper" in material_lower or "messing" in material_lower or "brass" in material_lower:
        return f"""**Marktanalyse Kupfer/Messing ({current_date.strftime('%B %Y')}):**

{"📈" if trend_pct > 0 else "📉"} **Preistrend:** Kupferpreise sind {trend} ({trend_pct:+.1f}% in 3 Monaten).

**Ursachen:**
• Starke Nachfrage aus Energiewende (E-Mobilität, Windkraft)
• Angebotsengpässe aus Chile und Peru
• Investitionen in erneuerbare Energien treiben Nachfrage
• Chinas Wirtschaftsstimuli stützen Kupferpreise

**Prognose:** {"Weiterer Anstieg (+3% bis +8%) bis Mitte 2025 erwartet" if trend_pct > 0 else "Konsolidierung auf hohem Niveau"}.

**Für Verhandlungen relevant:**
{"⚠️ **SCHWIERIGES UMFELD:** Preise steigen! 🔒 Sichern Sie Konditionen schnell ab" if trend_pct > 0 else "📊 Nutzen Sie Stabilisierung für Verhandlungen"}
🤝 Bieten Sie langfristige Verträge für Preissicherheit"""

    else:
        # Generisches Material
        return f"**Marktanalyse ({current_date.strftime('%B %Y')}):**\n\nMarktdaten für '{material_lower}' sind begrenzt. Trend: {trend} ({trend_pct:+.1f}%).\n\nNutzen Sie externe Marktberichte für detaillierte Analyse."


def _calculate_negotiation_leverage(trend_pct: float) -> str:
    """Berechnet Verhandlungshebel basierend auf Preistrend."""
    if trend_pct < -3:
        return "HOCH - Fallende Preise sind starkes Argument für Preissenkungen"
    elif trend_pct < -1:
        return "MITTEL - Leicht fallende Preise können als Argument genutzt werden"
    elif trend_pct > 3:
        return "NIEDRIG - Steigende Preise erschweren Verhandlungen, schnelles Handeln empfohlen"
    elif trend_pct > 1:
        return "MITTEL - Leicht steigende Preise, Konditionen zeitnah fixieren"
    else:
        return "NEUTRAL - Stabile Preise, Fokus auf Volumen und Lieferkonditionen"


def _build_analysis_from_api_data(material: str, material_lower: str, api_data: Dict) -> Dict[str, Any]:
    """Erstellt Analyse-Dict aus Trading Economics API-Daten."""
    import datetime

    current_price_usd = api_data.get('current_price', 0)
    trend_pct = api_data.get('trend_pct', 0)

    # Konvertierung USD -> EUR (vereinfachte Annahme: 1 USD = 0.92 EUR, Stand 2024)
    # In Produktion: Echten Wechselkurs von API abrufen
    usd_to_eur = 0.92

    # Preise sind meist in USD/Tonne oder USD/lb - konvertiere zu EUR/kg
    # Steel: USD/Tonne -> EUR/kg
    # Aluminum: USD/Tonne -> EUR/kg
    # Copper: USD/Tonne -> EUR/kg
    if "stahl" in material_lower or "steel" in material_lower:
        current_price_eur_kg = (current_price_usd * usd_to_eur) / 1000  # USD/t -> EUR/kg
    elif "aluminium" in material_lower or "aluminum" in material_lower:
        current_price_eur_kg = (current_price_usd * usd_to_eur) / 1000
    elif "kupfer" in material_lower or "copper" in material_lower or "messing" in material_lower:
        current_price_eur_kg = (current_price_usd * usd_to_eur) / 1000
    else:
        current_price_eur_kg = (current_price_usd * usd_to_eur) / 1000

    # Trend-Klassifizierung
    if trend_pct < -3:
        trend = "fallend"
    elif trend_pct < -1:
        trend = "leicht fallend"
    elif trend_pct > 3:
        trend = "steigend"
    elif trend_pct > 1:
        trend = "leicht steigend"
    else:
        trend = "stabil"

    current_date = datetime.datetime.now()

    # Generiere Analyse basierend auf echten Daten
    analysis = _generate_analysis_text(material_lower, trend, trend_pct, current_date)

    # Verhandlungshebel ableiten
    leverage = _calculate_negotiation_leverage(trend_pct)

    return {
        "ok": True,
        "material": material,
        "current_price_eur_kg": round(current_price_eur_kg, 3),
        "api_price_usd": round(current_price_usd, 2),
        "trend": trend,
        "trend_percentage": round(trend_pct, 2),
        "timeframe": "letzte 3 Monate",
        "analysis": analysis,
        "negotiation_leverage": leverage,
        "data_source": f"Trading Economics API (Live-Daten, {current_date.strftime('%d.%m.%Y')})",
        "recommendation": "📊 Echtzeit-Marktdaten - nutzen Sie diese aktiv in Verhandlungen!",
        "_is_mock": False,
        "_api_symbol": api_data.get('symbol')
    }


def _build_mock_commodity_analysis(material: str, material_lower: str) -> Dict[str, Any]:
    """Fallback-Funktion mit Mock-Daten wenn API nicht verfügbar."""
    import random
    import datetime

    # Realistische Basispreise (Stand 2024)
    base_prices = {
        "stahl": 0.95,  # €/kg
        "steel": 0.95,
        "edelstahl": 2.90,
        "edelstahl_a2": 2.90,
        "edelstahl_a4": 3.50,
        "stainless_steel": 2.90,
        "aluminium": 2.40,
        "aluminum": 2.40,
        "messing": 7.80,
        "brass": 7.80,
        "kupfer": 8.50,
        "copper": 8.50,
        "titan": 25.00,
        "titanium": 25.00
    }

    # Finde passendes Material
    base_price = base_prices.get(material_lower, 1.20)

    # MOCK: Simuliere realistischen Markt-Trend
    current_date = datetime.datetime.now()

    # Verschiedene Szenarien basierend auf Material
    if "stahl" in material_lower or "steel" in material_lower:
        # Stahl: Aktuell (2024) leicht fallend nach Höchstständen 2022
        trend_pct = random.uniform(-8.0, -2.0)  # Fallend
        trend = "fallend"
    elif "edelstahl" in material_lower or "stainless" in material_lower:
        # Edelstahl: Aktuell stabil mit leichten Schwankungen
        trend_pct = random.uniform(-2.0, 2.0)
        if trend_pct > 1.0:
            trend = "leicht steigend"
        elif trend_pct < -1.0:
            trend = "leicht fallend"
        else:
            trend = "stabil"
    elif "aluminium" in material_lower or "aluminum" in material_lower:
        # Aluminium: Volatil, aktuell eher fallend
        trend_pct = random.uniform(-6.0, -1.0)
        trend = "fallend"
    elif "kupfer" in material_lower or "copper" in material_lower or "messing" in material_lower or "brass" in material_lower:
        # Kupfer/Messing: Eher steigend (Energiewende-Nachfrage)
        trend_pct = random.uniform(1.0, 6.0)
        trend = "steigend"
    else:
        # Generisches Material
        trend_pct = random.uniform(-3.0, 3.0)
        trend = "steigend" if trend_pct > 1 else "fallend" if trend_pct < -1 else "stabil"

    # Generiere Analyse-Text (nutzt shared helper function)
    analysis = _generate_analysis_text(material_lower, trend, trend_pct, current_date)

    # Berechne aktuellen Preis basierend auf Trend
    current_price = base_price * (1 + trend_pct / 100)

    # Verhandlungshebel ableiten (nutzt shared helper function)
    leverage = _calculate_negotiation_leverage(trend_pct)

    return {
        "ok": True,
        "material": material,
        "current_price_eur_kg": round(current_price, 3),
        "base_price_eur_kg": round(base_price, 3),
        "trend": trend,
        "trend_percentage": round(trend_pct, 2),
        "timeframe": "letzte 3 Monate",
        "analysis": analysis,
        "negotiation_leverage": leverage,
        "data_source": "MOCK-Daten (Demo-Modus) - Für Produktion echte API integrieren",
        "recommendation": "📊 Nutzen Sie diese Marktanalyse aktiv in Verhandlungen!",
        "_is_mock": True  # Kennzeichnung dass es Mock-Daten sind
    }


def creditreform_login(username: str, password: str) -> Dict[str, Any]:
    """
    MOCK: Creditreform/Kreditreform Login-Funktion.

    In Produktion würde hier eine echte API-Authentifizierung stattfinden.
    Für Demo-Zwecke akzeptiert diese Funktion beliebige Credentials.

    Args:
        username: Benutzername
        password: Passwort

    Returns:
        Dict mit Login-Status und Session-Token
    """
    import hashlib
    import time

    # MOCK: Akzeptiere alle Logins (für Demo)
    if username and password:
        # Generiere Mock-Session-Token
        session_token = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()[:32]

        return {
            "ok": True,
            "logged_in": True,
            "username": username,
            "session_token": session_token,
            "api_access": True,
            "message": "✅ Login erfolgreich (DEMO-MODUS)",
            "_is_mock": True
        }
    else:
        return {
            "ok": False,
            "logged_in": False,
            "message": "❌ Benutzername oder Passwort fehlt",
            "_is_mock": True
        }


def creditreform_get_company_data(company_name: str, session_token: str = None) -> Dict[str, Any]:
    """
    MOCK: Creditreform Firmen-Finanzdaten abrufen.

    In Produktion würde hier eine echte API-Abfrage zur Creditreform/Kreditreform Datenbank erfolgen.
    Diese Funktion liefert realistische Mock-Daten.

    Args:
        company_name: Firmenname
        session_token: Session-Token vom Login

    Returns:
        Dict mit Finanzkennzahlen und Rating
    """
    import random

    # Validierung (optional, in echtem System)
    if not session_token:
        return {
            "ok": False,
            "error": "Kein Session-Token - bitte einloggen",
            "_is_mock": True
        }

    # MOCK-DATEN generieren (realistische Werte)
    # In Produktion: API-Call zur Creditreform

    # Verschiedene Risiko-Profile basierend auf Firmennamen (für realistische Demo)
    company_lower = company_name.lower()

    if "acme" in company_lower or "bolt" in company_lower or "fix" in company_lower:
        # Gute Bonität
        credit_score = random.randint(250, 300)  # Creditreform Score: 100-600 (niedriger = besser)
        risk_class = "Geringes Risiko"
        insolvency_probability_pct = random.uniform(0.1, 0.5)
        payment_behavior = "Ausgezeichnet"
        equity_ratio_pct = random.uniform(30, 45)
        liquidity_ratio = random.uniform(1.8, 2.5)
        revenue_eur_m = random.uniform(5, 50)
        employees = random.randint(50, 500)
    else:
        # Mittlere Bonität
        credit_score = random.randint(300, 400)
        risk_class = "Mittleres Risiko"
        insolvency_probability_pct = random.uniform(1.0, 3.0)
        payment_behavior = "Zufriedenstellend"
        equity_ratio_pct = random.uniform(15, 30)
        liquidity_ratio = random.uniform(1.0, 1.8)
        revenue_eur_m = random.uniform(1, 20)
        employees = random.randint(10, 200)

    return {
        "ok": True,
        "company_name": company_name,

        # Creditreform Bonit äts-Score
        "creditreform_score": credit_score,
        "score_interpretation": f"Score {credit_score}/600 (100=beste Bonität, 600=schlechteste)",

        # Risiko-Klassifizierung
        "risk_class": risk_class,
        "insolvency_probability_pct": round(insolvency_probability_pct, 2),

        # Zahlungsverhalten
        "payment_behavior": payment_behavior,
        "average_payment_delay_days": random.randint(0, 30) if payment_behavior != "Ausgezeichnet" else random.randint(0, 10),

        # Finanz-Kennzahlen
        "financial_data": {
            "revenue_eur_million": round(revenue_eur_m, 1),
            "equity_ratio_pct": round(equity_ratio_pct, 1),
            "liquidity_ratio": round(liquidity_ratio, 2),
            "ebitda_margin_pct": round(random.uniform(5, 15), 1),
            "debt_to_equity_ratio": round(random.uniform(0.5, 2.5), 2)
        },

        # Unternehmens-Info
        "company_info": {
            "employees": employees,
            "founded_year": random.randint(1980, 2015),
            "legal_form": random.choice(["GmbH", "AG", "GmbH & Co. KG"]),
            "industry": "Metallverarbeitung / Befestigungstechnik"
        },

        # Empfehlungen
        "recommendations": [
            f"✅ Kreditlimit empfohlen: {int(revenue_eur_m * 50000)} EUR" if risk_class == "Geringes Risiko" else f"⚠️ Kreditlimit empfohlen: {int(revenue_eur_m * 20000)} EUR",
            "📊 Regelmäßiges Monitoring empfohlen" if risk_class != "Geringes Risiko" else "✅ Stabiler Partner",
            "💳 Anzahlung empfohlen bei Großaufträgen" if risk_class == "Mittleres Risiko" else "✅ Standardzahlungsziele möglich"
        ],

        "data_source": "Creditreform MOCK-Daten (Demo)",
        "last_updated": "2024-12-01",
        "_is_mock": True
    }
