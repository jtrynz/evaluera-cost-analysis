import re
import pandas as pd
import numpy as np

PRICE_UNIT_CANDS = [
    "unit_price","einzelpreis","stkpreis","preis_pro_stk","preis je stück","preis je stk",
    "preis/stk","price_per_unit","avg_price","durchschnittspreis","preis_einheit"
]
PRICE_TOTAL_CANDS = [
    "rechnungsnettowert","rechnungsnettowert[hw]","nettowert","netto","betrag","invoice_amount",
    "amount","total","summe","gesamtbetrag","gesamt","net_amount","netto_betrag"
]
QTY_CANDS = ["quantity","menge","qty","anzahl","stueck","stück","pcs","qty_total","menge_total"]

def _norm_num(x):
    if x is None or (isinstance(x,float) and np.isnan(x)): return np.nan
    s = str(x).strip()
    if not s: return np.nan
    s = re.sub(r'(€|EUR|eur|\$|USD|usd)', '', s)
    s = s.replace(' ', '')
    if s.count(',')==1 and s.count('.')>=1: s = s.replace('.','')
    if s.count(',')==1 and s.count('.')==0: s = s.replace(',', '.')
    try:
        return float(s)
    except:
        return pd.to_numeric(s, errors="coerce")

def _find_col(df, keywords):
    low = {str(c).strip().lower(): c for c in df.columns}
    for kw in keywords:
        for k,orig in low.items():
            if kw in k:
                return orig
    return None

def derive_unit_price(df):
    qcol = _find_col(df, QTY_CANDS)
    w = df[qcol].map(_norm_num).fillna(1) if qcol is not None else pd.Series(1, index=df.index, dtype="float64")
    pcol = _find_col(df, PRICE_UNIT_CANDS)
    tcol = _find_col(df, PRICE_TOTAL_CANDS)
    unit = None
    src = None
    if pcol is not None:
        unit = df[pcol].map(_norm_num)
        src = ("unit", str(pcol))
    elif tcol is not None and qcol is not None:
        tot = df[tcol].map(_norm_num)
        q = df[qcol].map(_norm_num).replace(0, np.nan)
        unit = tot / q
        src = ("total/qty", f"{tcol}/{qcol}")
    if unit is None or not getattr(unit, "notna")().any():
        for c in df.columns:
            ser = df[c].map(_norm_num)
            if ser.notna().sum()>0:
                if qcol is not None and ser.max() > 10 and df[qcol].map(_norm_num).max() > 1:
                    q = df[qcol].map(_norm_num).replace(0, np.nan)
                    unit = ser / q
                    src = ("heur_total/qty", str(c)+"/"+str(qcol))
                else:
                    unit = ser
                    src = ("heur_unit", str(c))
                break
    if unit is None:
        return None, None, None, None, None
    p = pd.to_numeric(unit, errors="coerce")
    mn = float(p.min(skipna=True)) if p.notna().any() else None
    mx = float(p.max(skipna=True)) if p.notna().any() else None
    avg = float((p.fillna(0)*w).sum()/w.sum()) if p.notna().any() and w.sum()>0 else None
    return avg, mn, mx, qcol, src
