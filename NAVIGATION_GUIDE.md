# 📑 EVALUERA Navigation Sidebar - Dokumentation

## Überblick

Apple-ähnliche Navigation Sidebar mit Accordion-Struktur für intuitive Navigation durch verschiedene App-Bereiche.

---

## Features

✅ **Apple-ähnliches Design**
- Clean, minimalistisch
- Dünne Linien, dezente Akzente
- Leichte Schatten
- Starke visuelle Ruhe

✅ **Accordion-Struktur**
- Hauptkategorien ausklappbar
- Sub-Items leicht eingerückt
- Nur eine Ebene gleichzeitig aktiv

✅ **Smooth Animations**
- Hover-Effekte (Opazität 0.85 → 1.0)
- Transition: 0.2s ease
- Smooth Scroll-Verhalten

✅ **EVALUERA Branding**
- Mint/Türkis Akzente (#B8D4D1, #7BA5A0)
- Konsistente Farbpalette
- Wiederverwendbare Design Tokens

✅ **Responsive Design**
- Sidebar einklappbar
- Mobile-optimiert
- Hamburger-Menü auf kleinen Bildschirmen

---

## Installation

### 1. Import der Module

```python
from navigation_sidebar import NavigationSidebar, create_section_anchor, create_scroll_behavior
```

### 2. Setup in Ihrer App

```python
import streamlit as st
from navigation_sidebar import NavigationSidebar, create_section_anchor

# Page Config
st.set_page_config(
    page_title="Ihre App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Navigation
nav = NavigationSidebar()
nav.render()

# Smooth Scroll
create_scroll_behavior()
```

---

## Navigation-Struktur

### Hauptbereiche

1. **📦 Produktdaten**
   - Artikel-Informationen
   - Spezifikationen
   - Material

2. **🌍 CO₂-Analyse**
   - Carbon Footprint
   - Emissionsverteilung

3. **💰 Kostenübersicht**
   - Kostenaufschlüsselung
   - Gesamtkosten

4. **♻️ Nachhaltigkeit**
   - CBAM-Konformität
   - Recyclingfähigkeit
   - Empfehlungen

5. **⚙️ Debug / Technische Details**
   - Session State
   - Logs
   - API-Informationen

6. **✨ Erweiterte Funktionen** (mit Badge "NEU")
   - 📐 Technische Zeichnung
   - 🎲 3D-Modell

---

## Verwendung

### Section Anchor erstellen

```python
from navigation_sidebar import create_section_anchor

# Einfache Section
create_section_anchor("produktdaten", "📦 Produktdaten")

# Section mit Subtitle
create_section_anchor(
    "co2_analyse",
    "🌍 CO₂-Analyse",
    "Umweltauswirkungen und Carbon Footprint"
)
```

### Content basierend auf aktiver Section

```python
# Check welche Section aktiv ist
if st.session_state.nav_active_section == "produktdaten":
    create_section_anchor("produktdaten", "📦 Produktdaten")

    st.markdown("### Artikelinformationen")
    # ... Ihr Content

elif st.session_state.nav_active_section == "co2_analyse":
    create_section_anchor("co2_analyse", "🌍 CO₂-Analyse")

    # ... Ihr Content
```

### Subsections (Accordion)

Subsections werden automatisch gerendert, wenn die Hauptsektion erweitert wird:

```python
# In NavigationSidebar.SECTIONS
"erweitert": {
    "title": "Erweiterte Funktionen",
    "icon": "✨",
    "subsections": [
        {"id": "zeichnung", "title": "Technische Zeichnung", "icon": "📐"},
        {"id": "modell3d", "title": "3D-Modell", "icon": "🎲"}
    ]
}
```

---

## Design-Spezifikationen

### Spacing

- **xs**: 0.25rem (4px)
- **sm**: 0.5rem (8px)
- **md**: 1rem (16px)
- **lg**: 1.5rem (24px)
- **xl**: 2rem (32px)
- **xxl**: 3rem (48px)

### Farben

```python
# Navigation Item
color: #3f3f46 (gray_700)
background: transparent

# Hover
background: #f4f4f5 (gray_100)
opacity: 1.0

# Active
background: #B8D4D1 (primary_light)
color: #1a1a1a (gray_900)
border-left: 3px solid #7BA5A0 (primary)
font-weight: 600
```

### Typography

- **Font Family**: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto
- **Main Item**: 0.95rem
- **Sub Item**: 0.875rem
- **Header**: 0.75rem, uppercase, letter-spacing: 0.08em

### Border Radius

- **sm**: 8px (Navigation Items)
- **md**: 14px (Sections)
- **full**: 9999px (Badges)

---

## Anpassung

### Neue Section hinzufügen

```python
# In navigation_sidebar.py - NavigationSidebar.SECTIONS
"meine_section": {
    "title": "Meine Section",
    "icon": "🎯",
    "subsections": []
}
```

### Subsections hinzufügen

```python
"meine_section": {
    "title": "Meine Section",
    "icon": "🎯",
    "subsections": [
        {"id": "sub1", "title": "Unterbereich 1", "icon": "📌"},
        {"id": "sub2", "title": "Unterbereich 2", "icon": "📍"}
    ]
}
```

### Badge anpassen

```python
# Im _render_nav_item() - für bestimmte Sections
if section_id == "meine_section":
    badge_html = '<span class="nav-badge">NEU</span>'
```

---

## Demo starten

```bash
streamlit run demo_navigation.py
```

---

## Integration in bestehende App

### Option 1: Ersetzen der Wizard-Sidebar

```python
# Auskommentieren/entfernen:
# wizard = WizardManager()
# wizard.render_all_steps_sidebar()

# Ersetzen mit:
nav = NavigationSidebar()
nav.render()
```

### Option 2: Beide parallel nutzen

```python
# Tabs in Sidebar
tab1, tab2 = st.sidebar.tabs(["Wizard", "Navigation"])

with tab1:
    wizard = WizardManager()
    wizard.render_all_steps_sidebar()

with tab2:
    nav = NavigationSidebar()
    nav.render()
```

---

## Best Practices

1. **Konsistente Section IDs**: Verwenden Sie Kleinbuchstaben und Unterstriche
2. **Aussagekräftige Icons**: Wählen Sie Emojis, die den Inhalt klar repräsentieren
3. **Kurze Titel**: Max. 3-4 Wörter für bessere Lesbarkeit
4. **Logische Reihenfolge**: Wichtigste Sections zuerst
5. **Nicht zu viele Subsections**: Max. 3-4 pro Hauptbereich

---

## Accessibility

- Große Klickbereiche (min. 44x44px)
- Hoher Kontrast (Text zu Hintergrund)
- Keyboard-Navigation möglich
- Screen-Reader freundlich

---

## Troubleshooting

### Sidebar nicht sichtbar
```python
# Sicherstellen dass initial_sidebar_state korrekt ist
st.set_page_config(initial_sidebar_state="expanded")
```

### Section wechselt nicht
```python
# Session State überprüfen
st.write(st.session_state.nav_active_section)
```

### Styling wird nicht angewendet
```python
# apply_global_styles() vor Navigation aufrufen
apply_global_styles()
nav = NavigationSidebar()
```

---

## Performance

- Lazy Loading für Sections möglich
- Session State für schnelle Navigation
- CSS Transitions für smooth UX
- Minimale Re-Renders

---

**Happy Navigating! 🚀**
