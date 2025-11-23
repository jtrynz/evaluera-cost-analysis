# 🎨 EVALUERA UI/UX Redesign

## Übersicht

Das neue Design-System transformiert EVALUERA in eine moderne, minimalistische Anwendung mit klarem Wizard-Workflow und Apple-inspiriertem Design.

---

## ✨ Neue Dateien

### 1. `ui_theme.py`
Zentrales Design-System mit wiederverwendbaren Komponenten:

- **Design Tokens**: Farben, Abstände, Typografie, Schatten
- **Komponenten**: Cards, Buttons, KPI-Cards, Status-Badges
- **Wizard-Elemente**: Step-Indikatoren, Progress-Bar
- **Global Styles**: Konsistentes Look & Feel

**Farbpalette**:
- **Primär**: Lila (#7c3aed)
- **Neutral**: Grautöne (50-900)
- **Status**: Grün (Erfolg), Gelb (Warnung), Rot (Fehler), Blau (Info)

### 2. `wizard_system.py`
6-Stufen Wizard-Management:

```python
STEPS = {
    1: "Upload"
    2: "Artikel-Erkennung"
    3: "Preisübersicht"
    4: "Lieferantenanalyse"
    5: "Kosten-Schätzung"
    6: "Nachhaltigkeit & Verhandlung"
}
```

**Features**:
- State-Management über Session State
- Automatische Step-Validierung
- Collapsible Steps (nur aktiver Step sichtbar)
- Sidebar-Navigation
- Progress-Tracking

### 3. `app_wizard.py`
Moderne Demo-Anwendung:

- Clean, minimalistisches Design
- Wizard-basierter Workflow
- Responsive Layout
- Developer Mode (collapsed)
- Kompakte KPI-Zeilen statt große Blöcke

---

## 🚀 Verwendung

### Neue App starten

```bash
streamlit run app_wizard.py
```

### Integration in bestehende App

```python
# 1. Theme anwenden
from ui_theme import apply_global_styles, kpi_card, section_header
from wizard_system import WizardManager

apply_global_styles()
wizard = WizardManager()

# 2. Wizard-Steps definieren
def my_step_content():
    section_header("Mein Schritt", "Beschreibung")
    # ... Inhalt

# 3. Steps rendern
wizard.render_step_content(1, my_step_content)
```

---

## 📐 Design-Prinzipien

### 1. Minimalismus
- Reduzierte Farbpalette (Lila + Grautöne)
- Weißraum für bessere Lesbarkeit
- Klare visuelle Hierarchie

### 2. Konsistenz
- Einheitliche Komponenten
- Fester Border-Radius (14px)
- Konsistente Abstände (Spacing-System)

### 3. Wizard-Flow
- **Ein Step = Eine Aufgabe**
- Nur aktiver Step sichtbar
- Klare Navigation (Zurück/Weiter)
- Progress-Tracking

### 4. Kompakte Metriken
- KPI-Zeilen statt große farbige Blöcke
- Ruhige, strukturierte Cards
- Icons für schnelle Orientierung

### 5. Tabellen statt Karten
- **Vorher**: 26 individuelle Lieferanten-Karten
- **Nachher**: Eine saubere Tabelle mit Spalten
  - Name
  - Land
  - CBAM-Status
  - Preis
  - Button für Details

### 6. Developer Mode
- Debug-Infos in separatem Tab
- Im normalen UI nicht sichtbar
- JSON-Ausgabe für Session State

---

## 🎯 Komponenten-Bibliothek

### Cards

```python
from ui_theme import card

card_content = "<p>Inhalt</p>"
card(card_content, padding="md", hover=True, border=True)
```

### KPI-Cards

```python
from ui_theme import kpi_card

kpi_card(
    label="Ø Preis",
    value="0.1234 €",
    icon="💰",
    help_text="Gewichteter Durchschnitt",
    trend="positive"  # positive, negative, neutral
)
```

### Buttons

```python
from ui_theme import button

# Primary
button("Weiter", variant="primary", icon="→")

# Secondary
button("Abbrechen", variant="secondary")

# Ghost
button("Zurück", variant="ghost", icon="←")
```

### KPI-Zeilen

```python
from wizard_system import create_compact_kpi_row

kpis = [
    {"label": "Ø Preis", "value": "0.1234 €", "icon": "💰"},
    {"label": "Min", "value": "0.0500 €", "icon": "📉"},
    {"label": "Max", "value": "0.2000 €", "icon": "📈"},
]

create_compact_kpi_row(kpis)
```

### Tabellen

```python
from wizard_system import create_data_table

create_data_table(
    df=my_dataframe,
    columns_config={
        "Preis": st.column_config.NumberColumn(format="%.4f €"),
    },
    max_height=400
)
```

### Status-Badges

```python
from ui_theme import status_badge

status_badge("Aktiv", variant="success")  # Grün
status_badge("Warnung", variant="warning")  # Gelb
status_badge("Fehler", variant="error")  # Rot
status_badge("Info", variant="info")  # Blau
```

---

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 1200px → 2-Spalten-Layout
- **Tablet**: 768px - 1200px → 1-Spalte
- **Mobile**: < 768px → 1-Spalte, horizontales Scrolling

### KPI-Zeilen
- Auto-Umbruch bei schmalen Bildschirmen
- Stack-Verhalten unter 768px

### Tabellen
- Horizontal scrollbar bei Overflow
- Fixed Header bei langem Inhalt

---

## 🔄 Migration von alter zu neuer UI

### Phase 1: Vorbereitung
1. Backup erstellen: `cp simple_app.py simple_app_backup.py`
2. Neue Dateien reviewen: `ui_theme.py`, `wizard_system.py`, `app_wizard.py`

### Phase 2: Schrittweise Integration

#### Option A: Paralleler Betrieb
- Alte App: `simple_app.py`
- Neue App: `app_wizard.py`
- Beide parallel verfügbar

#### Option B: Feature-für-Feature Migration
1. **Woche 1**: Upload + Artikel-Suche
2. **Woche 2**: Preisübersicht + Lieferanten
3. **Woche 3**: Kostenschätzung
4. **Woche 4**: CBAM/CO₂/Verhandlung

### Phase 3: Komponenten ersetzen

**Vorher** (simple_app.py):
```python
st.markdown("""
<div style='background: gradient(...); padding: 1rem;'>
    <h3>Große Box</h3>
</div>
""", unsafe_allow_html=True)
```

**Nachher** (app_wizard.py):
```python
from ui_theme import kpi_card
kpi_card(label="Label", value="Wert", icon="💰")
```

---

## 📊 Vergleich Alt vs. Neu

### Datenmenge
| Metrik | Alt | Neu | Verbesserung |
|--------|-----|-----|--------------|
| Zeilen Code | 2118 | ~500 | -76% |
| CSS Styles | >500 Zeilen | ~200 | -60% |
| Komponenten | Inline HTML | Wiederverwendbar | +100% |

### Visuelle Komplexität
- **Farbige Blöcke**: 15+ → 4 (Primär/Neutral/Status)
- **Lieferanten-Karten**: 26 Karten → 1 Tabelle
- **Debug-Output**: Inline → Developer Mode Tab

### User Experience
- **Steps**: Scroll durch lange Seite → 6 klare Steps
- **Navigation**: Manuelles Scrollen → Wizard-Buttons
- **Feedback**: Unklarer Fortschritt → Progress Bar (0-100%)

---

## 🛠 Wartung & Erweiterung

### Neue Komponente hinzufügen

```python
# In ui_theme.py
def my_new_component(content, variant="default"):
    """Dokumentation"""
    return f"""
    <div style="...">
        {content}
    </div>
    """
```

### Farbe ändern

```python
# In ui_theme.py
COLORS = {
    "primary": "#7c3aed",  # <- Hier ändern
    # ...
}
```

### Neuen Wizard-Step hinzufügen

```python
# In wizard_system.py
STEPS = {
    # ...
    7: {"title": "Neuer Step", "desc": "Beschreibung"},
}

# In app_wizard.py
def step7_my_feature():
    section_header("Neuer Step")
    # Logik

wizard.render_step_content(7, step7_my_feature)
```

---

## ✅ Checkliste für UI-Redesign

- [x] Theme-System mit Design Tokens
- [x] Wizard-System mit 6 Steps
- [x] Wiederverwendbare Komponenten
- [x] Demo-App (`app_wizard.py`)
- [x] Kompakte KPI-Zeilen
- [x] Developer Mode (collapsed)
- [x] Responsive Design
- [x] Status-Badges
- [x] Tabellen statt Karten
- [x] Dokumentation

---

## 🎓 Best Practices

1. **Immer Komponenten nutzen**
   - ❌ Inline HTML mit `st.markdown()`
   - ✅ `kpi_card()`, `card()`, `button()`

2. **Wizard für mehrstufige Workflows**
   - ❌ Lange scrollbare Seite
   - ✅ Klare Steps mit Navigation

3. **Developer Mode für Debug-Infos**
   - ❌ Token-Counts direkt im UI
   - ✅ Collapsed Expander am Ende

4. **Kompakte Metriken**
   - ❌ Große farbige Boxen
   - ✅ KPI-Zeilen mit Icons

5. **Tabellen für Listen**
   - ❌ 20+ Karten nebeneinander
   - ✅ Eine sortierbare Tabelle

---

## 📞 Support

Bei Fragen zum neuen UI-System:

1. Siehe Komponenten-Dokumentation in `ui_theme.py`
2. Prüfe Beispiele in `app_wizard.py`
3. Teste mit: `streamlit run app_wizard.py`

**Happy Coding!** 🚀
