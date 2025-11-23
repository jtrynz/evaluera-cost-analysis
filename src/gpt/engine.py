import os, json, math
import pandas as pd
from dotenv import load_dotenv
from src.gpt.utils import sanitize_input, sanitize_payload_recursive, safe_gpt_request, safe_print
load_dotenv()

def _safe_float(x, d=None):
    try:
        return float(x)
    except:
        return d

def route_scenarios_with_gpt(item_text, material, d_mm, l_mm, lot_sizes):
    key=os.getenv("OPENAI_API_KEY")
    if not key:
        out=[]
        for ls in lot_sizes:
            out.append({"label":"Heuristik CNC-Drehen","primary":{"name":"turning","setup_time_min":20,"cycle_time_s":6.0,"machine_eur_h":80,"labor_eur_h":35,"overhead_pct":0.2},"secondary_ops":[],"lot_size":int(ls)})
        return out
    from openai import OpenAI
    client=OpenAI(api_key=key)
    sys="Du erstellst 3 bis 5 alternative Fertigungsszenarien für das Teil. Antworte ausschließlich als JSON-Array. Jedes Szenario: {label, primary:{name,setup_time_min,cycle_time_s,machine_eur_h,labor_eur_h,overhead_pct}, secondary_ops:[{name,cycle_time_s,machine_eur_h,labor_eur_h}], lot_size}."
    user=f"Bezeichnung: {item_text}\nMaterial: {material}\nD_mm: {d_mm}\nL_mm: {l_mm}\nLosgrößen: {list(map(int,lot_sizes))}\nErzeuge realistische Szenarien wie cold_forming, warm_forging, turning, machining, stamping. Sekundäre Operationen nur falls plausibel. Parameter realistisch in EU-üblichen Spannen."
    r=client.chat.completions.create(model="gpt-4o-mini",temperature=0,messages=[{"role":"system","content":sys},{"role":"user","content":user}])
    txt=r.choices[0].message.content.strip()
    try:
        arr=json.loads(txt)
        out=[]
        for sc in arr:
            pr=sc.get("primary",{})
            prn=str(pr.get("name","turning"))
            st=_safe_float(pr.get("setup_time_min"),20)
            cy=_safe_float(pr.get("cycle_time_s"),6.0)
            mh=_safe_float(pr.get("machine_eur_h"),80)
            lh=_safe_float(pr.get("labor_eur_h"),35)
            oh=_safe_float(pr.get("overhead_pct"),0.2)
            ops=[]
            for op in sc.get("secondary_ops",[]):
                ops.append({"name":str(op.get("name","")).strip() or "turning_finish","cycle_time_s":_safe_float(op.get("cycle_time_s"),1.0),"machine_eur_h":_safe_float(op.get("machine_eur_h"),60),"labor_eur_h":_safe_float(op.get("labor_eur_h"),30)})
            out.append({"label":str(sc.get("label",prn)).strip() or prn,"primary":{"name":prn,"setup_time_min":st,"cycle_time_s":cy,"machine_eur_h":mh,"labor_eur_h":lh,"overhead_pct":oh},"secondary_ops":ops,"lot_size":int(_safe_float(sc.get("lot_size"), lot_sizes[0]))})
        if not out:
            raise ValueError("empty")
        return out
    except:
        out=[]
        for ls in lot_sizes:
            out.append({"label":"Fallback cold_forming","primary":{"name":"cold_forming","setup_time_min":30,"cycle_time_s":1.8,"machine_eur_h":70,"labor_eur_h":30,"overhead_pct":0.18},"secondary_ops":[],"lot_size":int(ls)})
        return out

def calc_route_cost_per_unit(route, lot_size):
    p=route.get("primary",{})
    st=float(p.get("setup_time_min",30))
    cy=float(p.get("cycle_time_s",2.0))
    mh=float(p.get("machine_eur_h",70))
    lh=float(p.get("labor_eur_h",30))
    oh=float(p.get("overhead_pct",0.2))
    su=(st/60.0)*mh/max(int(lot_size),1)
    run=(cy/3600.0)*(mh+lh)
    cost=(su+run)*(1.0+oh)
    for op in route.get("secondary_ops",[]):
        cost += (float(op.get("cycle_time_s",0))/3600.0)*(float(op.get("machine_eur_h",0))+float(op.get("labor_eur_h",0)))
    return cost

def supplier_scores(idf, qty_col, price_series):
    df=idf.copy()
    if price_series is not None:
        df["_unit_price"]=price_series
    grp_cols=[c for c in df.columns if str(c).lower() in ("supplier","lieferant","anbieter","vendor","firma")]
    ctry_cols=[c for c in df.columns if str(c).lower() in ("country","land","herkunft","ursprung","origin")]
    by=grp_cols + ctry_cols
    by=[b for b in by if b in df.columns]
    if not by:
        by=[df.columns[0]]
    if qty_col and qty_col in df.columns:
        q=pd.to_numeric(df[qty_col],errors="coerce").fillna(0)
    else:
        q=pd.Series(1,index=df.index,dtype="float64")
    p=pd.to_numeric(df.get("_unit_price",pd.Series(index=df.index,dtype="float64")),errors="coerce")
    agg=df.assign(_q=q,_p=p).groupby(by,dropna=False).agg(avg_price=("_p","mean"), std_price=("_p","std"), n=(" _p","count") if " _p" in df.columns else ("_p","count"), qty_total=("_q","sum")).reset_index()
    agg["cv"]=agg["std_price"]/agg["avg_price"]
    agg["risk"]=agg["cv"].fillna(0)*0.6 + (1.0/agg["qty_total"].replace(0,1))*0.4
    return agg

def translate_query_with_gpt(headers, prompt):
    key=os.getenv("OPENAI_API_KEY")
    if not key or not prompt or not prompt.strip():
        return {}
    from openai import OpenAI
    client=OpenAI(api_key=key)
    sys="Du übersetzt eine deutsche Freitext-Abfrage in Filterregeln gegen ein Tabellen-DataFrame. Antworte nur als kompaktes JSON mit Feldern wie {contains:{col:text}, range:{col:[min,max]}, equals:{col:value}}. Nutze nur vorhandene Spaltennamen."
    user=f"Spalten: {headers}\nAbfrage: {prompt}"
    r=client.chat.completions.create(model="gpt-4o-mini",temperature=0,messages=[{"role":"system","content":sys},{"role":"user","content":user}])
    txt=r.choices[0].message.content.strip()
    try:
        return json.loads(txt)
    except:
        return {}

def apply_json_filter(df, spec):
    out=df.copy()
    if not spec:
        return out
    if "contains" in spec and isinstance(spec["contains"],dict):
        for col, val in spec["contains"].items():
            if col in out.columns:
                v=str(val).lower()
                out=out[out[col].astype(str).str.lower().str.contains(v, na=False)]
    if "equals" in spec and isinstance(spec["equals"],dict):
        for col, val in spec["equals"].items():
            if col in out.columns:
                out=out[out[col].astype(str)==str(val)]
    if "range" in spec and isinstance(spec["range"],dict):
        for col, rr in spec["range"].items():
            if col in out.columns:
                lo=rr[0] if len(rr)>0 else None
                hi=rr[1] if len(rr)>1 else None
                s=pd.to_numeric(out[col], errors="coerce")
                if lo is not None:
                    s=s[s>=_safe_float(lo,s.min())]
                if hi is not None:
                    s=s[s<=_safe_float(hi,s.max())]
                out=out.loc[s.index]
    return out

def trend_scenarios(eur_per_kg, deltas):
    out=[]
    base=float(eur_per_kg or 0.0)
    for d in deltas:
        out.append({"delta_pct":d,"eur_per_kg":base*(1.0+d/100.0)})
    return out

def gpt_intelligent_article_search(query, item_column_values):
    """
    GPT-basierte intelligente Artikel-Suche.
    GPT analysiert die Suchanfrage und findet passende Artikel auch wenn die Reihenfolge anders ist.

    Args:
        query: Suchanfrage (z.B. "DIN933 M12")
        item_column_values: Liste aller verfügbaren Artikelbezeichnungen

    Returns:
        Liste der passenden Artikel-Indizes oder leere Liste
    """
    query = sanitize_input(query)
    item_column_values = [sanitize_input(v) for v in item_column_values]

    key = os.getenv("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("OPENAI_API_KEY")
        except Exception:
            key = None
    if not key or not query or not query.strip():
        return []

    # Limit zu max 1000 Artikel für bessere Recall
    sample_items = list(item_column_values)[:1000]

    from openai import OpenAI

    system_prompt = """Du bist ein intelligenter Artikel-Such-Assistent für technische Teile.

Aufgabe: Analysiere die Suchanfrage und finde ALLE passenden Artikel aus der Liste.

Regeln:
1. Suche ist FLEXIBEL - Reihenfolge der Begriffe ist egal
   - "DIN933 M12" soll auch "M12 DIN933" oder "Schraube M12x30 DIN933" finden
2. Erkenne Varianten und Schreibweisen
   - "M12" matched auch "M 12", "m12", "12mm"
   - "DIN933" matched auch "DIN 933", "din933"
3. Berücksichtige technische Synonyme
   - "Schraube" = "Bolt" = "Verbindungselement"
4. Finde ALLE relevanten Artikel, nicht nur exakte Matches
5. **WICHTIG**: Sei GROSSZÜGIG - wenn ein Artikel die wichtigsten Suchbegriffe enthält, inkludiere ihn!
   - Partielle Matches sind OK
   - Verschiedene Längen/Dimensionen des gleichen Grundtyps sind OK

Antworte NUR als JSON-Array mit den Indizes der passenden Artikel: [0, 3, 5, ...]
Wenn nichts passt: []"""

    user_prompt = f"""Suchanfrage: "{query}"

Verfügbare Artikel:
{chr(10).join([f"{i}: {item}" for i, item in enumerate(sample_items)])}

Welche Artikel passen zur Suchanfrage? Gib NUR die Indizes als JSON-Array zurück.
WICHTIG: Finde ALLE Varianten, auch mit unterschiedlichen Längen/Größen!"""

    messages = sanitize_payload_recursive([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])

    try:
        res = safe_gpt_request(
            model="gpt-4o-mini",
            messages=messages,
            client_factory=lambda: OpenAI(api_key=key),
            temperature=0.3,
            max_tokens=500,
            retries=0,
        )
        if res.get("_error"):
            safe_print(f"GPT Artikel-Suche fehlgeschlagen: {res}")
            return []
        r = res["response"]
        txt = sanitize_input(r.choices[0].message.content or "")

        # Extrahiere JSON aus möglicher Markdown-Formatierung
        if "```json" in txt:
            txt = txt.split("```json")[1].split("```")[0].strip()
        elif "```" in txt:
            txt = txt.split("```")[1].split("```")[0].strip()

        indices = json.loads(txt)

        # Validiere Indizes
        valid_indices = [i for i in indices if isinstance(i, int) and 0 <= i < len(sample_items)]

        safe_print(f"GPT Intelligente Suche: '{query}' → {len(valid_indices)} Treffer gefunden")
        return valid_indices

    except Exception as e:
        safe_print(f"⚠️ GPT Artikel-Suche fehlgeschlagen: {e!r}")
        # Fallback: Einfache String-Suche
        return []
