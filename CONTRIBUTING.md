# Contributing to EVALUERA

Vielen Dank für dein Interesse, zu EVALUERA beizutragen! Wir freuen uns über jeden Beitrag.

## Wie kann ich beitragen?

### Bugs melden

Wenn du einen Bug gefunden hast:

1. Überprüfe, ob der Bug bereits in den [Issues](https://github.com/DEIN-USERNAME/evaluera_screw_cost_app/issues) gemeldet wurde
2. Falls nicht, erstelle ein neues Issue mit:
   - Klarer, beschreibender Titel
   - Detaillierte Beschreibung des Problems
   - Schritte zur Reproduktion
   - Erwartetes vs. tatsächliches Verhalten
   - Screenshots (falls zutreffend)
   - Systeminfo (OS, Python-Version, etc.)

### Feature-Vorschläge

Wir sind offen für neue Ideen:

1. Erstelle ein Issue mit dem Label "enhancement"
2. Beschreibe:
   - Das Problem, das das Feature lösen würde
   - Deine vorgeschlagene Lösung
   - Mögliche Alternativen

### Code-Beiträge

#### Setup

1. Forke das Repository
2. Klone deinen Fork:
```bash
git clone https://github.com/DEIN-USERNAME/evaluera_screw_cost_app.git
cd evaluera_screw_cost_app
```

3. Erstelle einen Branch für dein Feature:
```bash
git checkout -b feature/mein-neues-feature
```

4. Virtual Environment einrichten:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Entwicklung

1. **Code-Style**: Befolge PEP 8
   ```bash
   # Code formatieren
   black .

   # Linting
   flake8
   ```

2. **Type Hints**: Verwende Type Hints für bessere Code-Qualität
   ```python
   def calculate_cost(price: float, quantity: int) -> float:
       return price * quantity
   ```

3. **Dokumentation**: Docstrings für alle Funktionen
   ```python
   def my_function(param: str) -> int:
       """
       Kurze Beschreibung der Funktion.

       Args:
           param: Beschreibung des Parameters

       Returns:
           Beschreibung des Rückgabewerts
       """
       pass
   ```

4. **Tests**: Schreibe Tests für neue Features
   ```bash
   pytest
   ```

#### Commit Guidelines

Verwende aussagekräftige Commit-Messages:

```
feat: Neue Funktion für CO2-Berechnung hinzugefügt
fix: Fehler bei der Preisberechnung behoben
docs: README um Installation-Anleitung erweitert
style: Code-Formatierung verbessert
refactor: Kostenfunktionen refactored
test: Tests für Lieferantenanalyse hinzugefügt
chore: Dependencies aktualisiert
```

#### Pull Request

1. Pushe deinen Branch:
```bash
git push origin feature/mein-neues-feature
```

2. Erstelle einen Pull Request auf GitHub

3. Beschreibe im PR:
   - Was wurde geändert und warum
   - Welche Issues werden geschlossen (z.B. "Closes #123")
   - Screenshots/GIFs bei UI-Änderungen
   - Testplan

4. Warte auf Code-Review

## Code-Struktur

```
evaluera_screw_cost_app/
├── simple_app.py           # Hauptanwendung - UI & Workflows
├── cost_helpers.py         # Kostenberechnungen & GPT-Integration
├── gpt_engine.py           # GPT-Routing & Analyse-Engine
├── ui_components.py        # Wiederverwendbare UI-Komponenten
├── security.py             # Sicherheitsfunktionen
└── *_styles.py            # Style-Module
```

## Best Practices

### Sicherheit

- Niemals API Keys oder Secrets im Code
- Verwende `.env` für sensitive Daten
- Validiere alle User-Inputs
- Siehe `SECURITY.md` für Details

### Performance

- Caching für teure Operationen verwenden
- Lazy Loading für große Datasets
- Streamlit `@st.cache_data` und `@st.cache_resource` nutzen

### UI/UX

- Konsistenter Style (siehe `DESIGN_GUIDE.md`)
- Ladeanimationen für lange Operationen
- Fehlerbehandlung mit benutzerfreundlichen Messages
- Responsive Design

## Fragen?

Bei Fragen kannst du:
- Ein Issue erstellen
- Im Pull Request kommentieren
- Die Diskussionen auf GitHub nutzen

Vielen Dank für deine Beiträge!
