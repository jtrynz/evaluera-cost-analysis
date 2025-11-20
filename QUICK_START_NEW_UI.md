# 🚀 Quick Start - Neue EVALUERA UI

## Sofort starten

```bash
streamlit run app_wizard.py
```

---

## Was ist neu?

### ✨ Wizard-System (6 Steps)
Klarer, schrittweiser Workflow statt langer scrollbarer Seite:

1. **Upload** → Datei hochladen
2. **Artikel-Erkennung** → Artikel suchen
3. **Preisübersicht** → Statistiken anzeigen
4. **Lieferantenanalyse** → Lieferant wählen (Tabelle statt Karten!)
5. **Kosten-Schätzung** → KI-Analyse
6. **Nachhaltigkeit** → CBAM, CO₂, Verhandlung

**Nur der aktive Step ist sichtbar** - alles andere eingeklappt!

### 🎨 Minimalistisches Design
- **Farbpalette**: Lila (Primär) + Grautöne + Status-Farben
- **Kompakte KPIs**: Kleine Cards statt große farbige Blöcke
- **Tabellen**: Lieferanten in strukturierter Tabelle
- **Developer Mode**: Debug-Infos collapsed am Ende

### 📱 Responsive
- Desktop: 2-Spalten
- Tablet/Mobile: 1-Spalte
- Tabellen: Horizontal scrollbar

---

## Datei-Struktur

```
evaluera_screw_cost_app/
├── app_wizard.py           # 🆕 Neue Wizard-basierte App
├── ui_theme.py             # 🆕 Design-System & Komponenten
├── wizard_system.py        # 🆕 Wizard-Logik
├── UI_REDESIGN.md          # 📚 Vollständige Dokumentation
├── simple_app.py           # ⚠️  Alte App (Backup)
└── simple_app_backup.py    # 💾 Sicherheitskopie
```

---

## Unterschiede auf einen Blick

| Feature | Alte App | Neue App |
|---------|----------|----------|
| **Navigation** | Scrollen | Wizard (6 Steps) |
| **Lieferanten** | 26 Karten | 1 Tabelle |
| **KPIs** | Große Blöcke | Kompakte Zeile |
| **Debug-Infos** | Inline | Developer Mode Tab |
| **Zeilen Code** | 2118 | ~500 |
| **Design** | Viele Farben | Lila + Grau |

---

## Demo-Workflow

### Step 1: Upload
```
📤 Datei hochladen
   → Excel/CSV auswählen
   → Automatische Validierung
   → Vorschau anzeigen
```

### Step 2: Artikel-Erkennung
```
🔍 Artikel suchen
   → Suchbegriff eingeben (z.B. "DIN 933 M8")
   → KI findet passende Artikel
   → Artikel aus Liste wählen
```

### Step 3: Preisübersicht
```
💰 Kompakte KPI-Zeile:
   [Ø Preis] [Min] [Max] [Range]

   Optional: Breakdown nach Lieferant (collapsed)
```

### Step 4: Lieferanten
```
📊 Tabelle statt Karten:
   | Lieferant | Einträge | Ø Preis |
   |-----------|----------|---------|
   | Firma A   | 45       | 0.1234€ |
   | Firma B   | 23       | 0.1456€ |

   → Lieferant auswählen
```

### Step 5: Kostenschätzung
```
🤖 KI-Analyse:
   → Losgröße eingeben
   → "Kosten schätzen" Button
   → Ladeanimation
   → Ergebnis: [Material] [Fertigung] [Ziel] [Delta]
```

### Step 6: Nachhaltigkeit
```
🌱 CBAM & CO₂
   → Nachhaltigkeits-Info
   → Verhandlungstipps generieren
```

---

## Komponenten-Beispiele

### KPI-Zeile
```python
from wizard_system import create_compact_kpi_row

create_compact_kpi_row([
    {"label": "Ø Preis", "value": "0.1234 €", "icon": "💰"},
    {"label": "Lieferanten", "value": "3", "icon": "🏭"},
])
```

### Tabelle
```python
from wizard_system import create_data_table

create_data_table(
    df=supplier_dataframe,
    max_height=400
)
```

### Section Header
```python
from ui_theme import section_header

section_header("Mein Titel", "Untertitel oder Beschreibung")
```

---

## Migration von alter zu neuer App

### Option 1: Parallel betreiben
```bash
# Alte App
streamlit run simple_app.py --server.port 8501

# Neue App
streamlit run app_wizard.py --server.port 8502
```

### Option 2: Schrittweise migrieren
Siehe `UI_REDESIGN.md` → "Migration Phase 2"

---

## Troubleshooting

### Import-Fehler
```bash
# Fehlende Abhängigkeiten installieren
pip install streamlit pandas python-dotenv
```

### Wizard startet nicht bei Step 1
```python
# Session State löschen
st.session_state.clear()
# oder
del st.session_state.wizard_current_step
```

### Alte Styles überschreiben neue
→ Sicherstellen dass `apply_global_styles()` **nach** `st.set_page_config()` aufgerufen wird

---

## Features im Detail

### 🎯 Wizard-Navigation
- **Sidebar**: Übersicht aller Steps (klickbar wenn completed)
- **Progress Bar**: 0-100% Fortschritt
- **Buttons**: Zurück / Weiter
- **Auto-Complete**: Step wird automatisch als "completed" markiert

### 🎨 Design-Tokens
```python
from ui_theme import COLORS, SPACING, RADIUS

# Farben
COLORS['primary']    # #7c3aed (Lila)
COLORS['success']    # #22c55e (Grün)

# Abstände
SPACING['sm']        # 0.5rem
SPACING['md']        # 1rem
SPACING['lg']        # 1.5rem

# Border-Radius
RADIUS['md']         # 14px (Standard)
```

### 📊 Status-Badges
```python
from ui_theme import status_badge

status_badge("Aktiv", variant="success")
status_badge("Warnung", variant="warning")
status_badge("Fehler", variant="error")
```

---

## Performance

### Vorher (simple_app.py)
- 2118 Zeilen Code
- >500 Zeilen inline CSS
- Viele redundante Komponenten
- Schwer wartbar

### Nachher (app_wizard.py)
- ~500 Zeilen Code (-76%)
- Wiederverwendbare Komponenten
- Klare Struktur
- Leicht erweiterbar

---

## Nächste Schritte

1. **Testen**: `streamlit run app_wizard.py`
2. **Dokumentation**: `UI_REDESIGN.md` lesen
3. **Anpassen**: Komponenten in `ui_theme.py` erweitern
4. **Migrieren**: Schrittweise alte Features portieren

---

## 📞 Hilfe

**Dokumentation**: Siehe `UI_REDESIGN.md`

**Beispiele**: Siehe `app_wizard.py`

**Komponenten**: Siehe `ui_theme.py` (Docstrings)

---

**Viel Erfolg mit der neuen UI!** 🎉
