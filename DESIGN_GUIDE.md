# 🎨 EVALUERA - Design Guide

## Apple-like Design System

Die EVALUERA-App verwendet ein ultra-professionelles, Apple-inspiriertes Design-System mit:
- Minimalistischer Ästhetik
- Eleganten Animationen
- Glassmorphism-Effekten
- Smooth Transitions
- Hochwertige Typografie

---

## 🎯 Design-Prinzipien

### 1. **Minimalismus**
- Fokus auf Inhalt, nicht auf Dekoration
- Großzügiger Weißraum
- Klare visuelle Hierarchie

### 2. **Konsistenz**
- Einheitliche Farben, Abstände und Schriften
- Wiederverwendbare UI-Komponenten
- Vorhersehbare Interaktionen

### 3. **Performance**
- Smooth Animationen (60 FPS)
- Optimierte Ladezeiten
- Progressive Enhancement

---

## 🎨 Farbpalette

```css
--apple-bg: #fbfbfd              /* Hintergrund */
--apple-surface: #ffffff          /* Oberflächen (Cards, etc.) */
--apple-surface-hover: #f5f5f7    /* Hover-Zustand */
--apple-text: #1d1d1f             /* Haupttext */
--apple-text-secondary: #86868b   /* Sekundärtext */
--apple-accent: #0071e3           /* Akzentfarbe (Blau) */
--apple-accent-hover: #0077ed     /* Akzent Hover */
--apple-accent-light: rgba(0, 113, 227, 0.1) /* Transparenter Akzent */
```

### Status-Farben
- **Success**: `#34c759` (Grün)
- **Warning**: `#ff9f0a` (Orange)
- **Error**: `#ff3b30` (Rot)
- **Info**: `#0071e3` (Blau)

---

## 📐 Spacing & Layout

### Border Radius
- **Small**: `8px` - Inputs, kleine Buttons
- **Medium**: `12px` - Cards, Container
- **Large**: `18px` - Hero-Sections

### Shadows
```css
--apple-shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.04)   /* Subtle */
--apple-shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08)  /* Normal */
--apple-shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.12)  /* Elevated */
```

### Padding
- **Tight**: `0.5rem` (8px)
- **Normal**: `1rem` (16px)
- **Comfortable**: `1.5rem` (24px)
- **Spacious**: `2rem` (32px)

---

## ✍️ Typografie

### Schriftarten
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
```

### Gewichte
- **Light**: 300 - Für große Überschriften
- **Regular**: 400 - Fließtext
- **Medium**: 500 - Hervorhebungen
- **Semibold**: 600 - Labels, Buttons
- **Bold**: 700 - Überschriften
- **Extrabold**: 800 - Hero-Titel

### Größen
- **H1**: `3.5rem` (56px) - Haupttitel
- **H2**: `2rem` (32px) - Abschnittstitel
- **H3**: `1.5rem` (24px) - Untertitel
- **Body**: `1.05rem` (17px) - Fließtext
- **Small**: `0.85rem` (14px) - Labels

---

## 🧩 UI-Komponenten

### 1. Apple Loader
Verwendet für: API-Calls, Datei-Uploads

```python
from ui_components import show_apple_loader

# Einfacher Loader
loader = show_apple_loader("Lädt Daten...")

# Mit Dauer
show_apple_loader("Verarbeite...", duration=3)
```

**Visuals**: Rotierender Ring mit smooth Animation

---

### 2. Shimmer Skeleton
Verwendet für: Platzhalter während Daten laden

```python
from ui_components import show_shimmer_skeleton

# Ein Element
show_shimmer_skeleton(height="100px")

# Mehrere Elemente
show_shimmer_skeleton(height="80px", count=3)
```

**Visuals**: Animierter Glanz-Effekt über graue Boxen

---

### 3. Progress Animation
Verwendet für: Mehrstufige Prozesse

```python
from ui_components import show_progress_animation

show_progress_animation(0.65, text="Analysiere Daten")
```

**Visuals**: Elegante Progress Bar mit Prozentanzeige

---

### 4. Glass Card
Verwendet für: Hervorhebungen, spezielle Inhalte

```python
from ui_components import show_glass_card

show_glass_card(
    content="<p>Wichtige Information</p>",
    title="Hinweis"
)
```

**Visuals**: Glassmorphism-Effekt (Transparenz + Blur)

---

### 5. Status Badge
Verwendet für: Status-Anzeigen

```python
from ui_components import show_status_badge

badge_html = show_status_badge("Aktiv", status="success")
st.markdown(badge_html, unsafe_allow_html=True)
```

**Status-Typen**:
- `success` - Grün
- `warning` - Orange
- `error` - Rot

---

### 6. Metric Card
Verwendet für: KPIs, Zahlen

```python
from ui_components import show_metric_card

show_metric_card(
    label="Gesamtkosten",
    value="€ 45.230",
    delta="+12%",
    help_text="Im Vergleich zum letzten Monat"
)
```

**Features**:
- Hover-Effekt (lift)
- Delta-Färbung (grün/rot)
- Optional Hilfetext

---

### 7. Info Card
Verwendet für: Wichtige Informationen, Tipps

```python
from ui_components import show_info_card

show_info_card(
    icon="💡",
    title="Tipp",
    description="Sie können mehrere Dateien gleichzeitig hochladen.",
    color="#0071e3"
)
```

**Features**:
- Icon + Text
- Farbige Seitenleiste
- Fade-in Animation

---

### 8. Loading Steps
Verwendet für: Komplexe mehrstufige Prozesse

```python
from ui_components import show_loading_with_steps

steps = [
    "Datei hochladen",
    "Daten analysieren",
    "Kosten berechnen",
    "Bericht erstellen"
]

show_loading_with_steps(steps, current_step=1)
```

**Visuals**:
- Checkmarks für abgeschlossene Steps
- Aktueller Step highlighted
- Progress Bar oben

---

### 9. Pulse Loader
Verwendet für: Kurze Wartezeiten

```python
from ui_components import show_pulse_loader

show_pulse_loader("Verarbeite Anfrage...")
```

**Visuals**: Drei pulsierende Punkte

---

### 10. Divider
Verwendet für: Abschnittstrennungen

```python
from ui_components import show_divider

# Einfach
show_divider()

# Mit Text
show_divider("Ergebnisse")
```

---

### 11. Empty State
Verwendet für: Leere Zustände (keine Daten)

```python
from ui_components import show_empty_state

show_empty_state(
    icon="📂",
    title="Keine Daten vorhanden",
    description="Laden Sie eine Excel-Datei hoch, um zu beginnen.",
    button_text="Datei hochladen",
    button_action="upload"
)
```

---

## 🎬 Animationen

### Verfügbare Animationen

#### 1. **apple-spin**
Smooth Rotation (für Loader)
```css
animation: apple-spin 0.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
```

#### 2. **pulse**
Pulsieren (für Attention)
```css
animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
```

#### 3. **shimmer**
Glanz-Effekt (für Skeleton Loading)
```css
animation: shimmer 2s infinite;
```

#### 4. **fadeIn**
Sanftes Einblenden
```css
animation: fadeIn 0.5s ease-out;
```

### Easing Functions (Apple-like)
```css
/* Smooth & Natural */
cubic-bezier(0.4, 0, 0.2, 1)  /* Standard Ease */
cubic-bezier(0.68, -0.55, 0.27, 1.55)  /* Bounce */
```

---

## 🎯 Best Practices

### DO ✅

1. **Konsistente Abstände verwenden**
   ```python
   # Verwende CSS-Variablen
   padding: var(--apple-radius);
   ```

2. **Hover-Effekte hinzufügen**
   ```css
   .hover-lift:hover {
       transform: translateY(-2px);
       box-shadow: var(--apple-shadow-md);
   }
   ```

3. **Smooth Transitions**
   ```css
   transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
   ```

4. **Passende Icons verwenden**
   ```python
   st.markdown("✅ Erfolgreich")  # Emojis für visuelle Unterstützung
   ```

### DON'T ❌

1. **Zu viele Farben mischen**
   ```python
   # ❌ Nicht gut
   st.markdown("<span style='color: red; background: yellow;'>Text</span>")

   # ✅ Besser
   st.success("Text")  # Nutze Streamlit's built-in Komponenten
   ```

2. **Harte Kanten**
   ```css
   /* ❌ Vermeiden */
   border-radius: 0;

   /* ✅ Besser */
   border-radius: var(--apple-radius-sm);
   ```

3. **Langsame Animationen**
   ```css
   /* ❌ Zu langsam */
   transition: all 2s;

   /* ✅ Schneller & Smooth */
   transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
   ```

4. **Zu viele gleichzeitige Animationen**
   - Maximal 2-3 animierte Elemente gleichzeitig
   - Priorisiere wichtige Interaktionen

---

## 📱 Responsive Design

### Breakpoints
```css
/* Mobile */
@media (max-width: 768px) {
    h1 { font-size: 2.5rem; }
}

/* Tablet */
@media (max-width: 1024px) {
    .block-container { padding: 1rem; }
}

/* Desktop */
@media (min-width: 1025px) {
    .block-container { max-width: 1400px; }
}
```

---

## 🎨 Glassmorphism

Für spezielle Hervorhebungen:

```css
.glass-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: var(--apple-shadow-md);
}
```

**Verwendung**:
- Hero-Sections
- Modale
- Spezielle Call-to-Actions

---

## 🔧 Erweiterte Anpassungen

### Custom Button-Styles

```python
st.markdown("""
<style>
.custom-button {
    background: linear-gradient(135deg, #0071e3, #0077ed);
    color: white;
    padding: 0.75rem 2rem;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}
.custom-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 113, 227, 0.3);
}
</style>
""", unsafe_allow_html=True)
```

### Custom Metric Cards

```python
st.markdown(f"""
<div class="hover-lift" style="
    background: var(--apple-surface);
    padding: 1.5rem;
    border-radius: var(--apple-radius);
    box-shadow: var(--apple-shadow-sm);
">
    <div style="color: var(--apple-text-secondary); font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">
        TOTAL COST
    </div>
    <div style="color: var(--apple-text); font-size: 2.5rem; font-weight: 700; margin-top: 0.5rem;">
        € 45,230
    </div>
    <div style="color: #34c759; font-size: 0.9rem; font-weight: 600; margin-top: 0.5rem;">
        +12% ↑
    </div>
</div>
""", unsafe_allow_html=True)
```

---

## 📊 Tabellen-Styling

Tabellen verwenden automatisch Apple-Styling:
- Hover-Effekte auf Zeilen
- Subtile Borders
- Lesbare Typografie
- Box-Shadow für Elevation

**Keine zusätzlichen Anpassungen nötig!**

---

## 🎓 Beispiele

### Komplettes UI-Beispiel

```python
import streamlit as st
from ui_components import *

# Header
st.title("📊 Dashboard")

# Info Card
show_info_card(
    icon="💡",
    title="Willkommen!",
    description="Starten Sie mit dem Upload Ihrer Daten.",
    color="#0071e3"
)

# Divider
show_divider("Metriken")

# 3-Spalten Layout
col1, col2, col3 = st.columns(3)

with col1:
    show_metric_card("Bestellungen", "1,234", delta="+5%")

with col2:
    show_metric_card("Kosten", "€ 45.2K", delta="-2%")

with col3:
    show_metric_card("Lieferanten", "42")

# Loading
if st.button("Daten laden"):
    loader = show_apple_loader("Lädt...")
    # ... API Call ...
    loader.empty()
    st.success("Fertig!")
```

---

## 🚀 Performance-Tipps

1. **Animationen sparsam einsetzen**
   - Nur bei Benutzer-Interaktionen
   - Nicht bei scroll/hover auf großen Listen

2. **Lazy Loading für große Datensätze**
   ```python
   # Nicht alle Daten auf einmal rendern
   st.dataframe(df.head(100))  # Erste 100 Zeilen
   ```

3. **CSS-Variablen nutzen**
   - Schnellere Änderungen
   - Konsistenz garantiert
   - Kleinere Dateigröße

---

## 📖 Referenzen

- **Apple Human Interface Guidelines**: https://developer.apple.com/design/human-interface-guidelines/
- **Inter Font**: https://rsms.me/inter/
- **Streamlit Docs**: https://docs.streamlit.io/

---

## ✅ Checkliste: Professionelles Design

- [ ] Konsistente Farbpalette verwendet
- [ ] Alle Buttons haben Hover-Effekte
- [ ] Loading-States für alle API-Calls
- [ ] Passende Icons/Emojis verwendet
- [ ] Responsive auf Mobile getestet
- [ ] Animationen sind smooth (60 FPS)
- [ ] Typografie ist lesbar
- [ ] Ausreichend Weißraum
- [ ] Error-States sind benutzerfreundlich
- [ ] Empty-States sind klar

---

**Erstellt**: November 2025
**Version**: 1.0
**Status**: Production-Ready ✅

**Viel Spaß mit dem neuen Design!** 🎨✨
