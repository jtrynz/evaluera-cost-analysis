# EVALUERA - Cost Analysis & Supplier Intelligence Platform

Eine professionelle Streamlit-Anwendung zur Analyse von Bestellhistorien, Kostenschätzung und Lieferantenbewertung mit KI-Integration.

## Features

### Kernfunktionen
- **Bestellhistorie-Analyse**: Upload von CSV/Excel mit automatischer Spaltenerkennung
- **Intelligente Artikelsuche**: Fuzzy-Match-Algorithmus mit GPT-Unterstützung
- **Kostenschätzung**:
  - Materialkosten basierend auf Geometrie und Dichte
  - Fertigungskosten (Rüstzeit, Zykluszeit, Gemeinkosten)
  - GPT-basierte Kostenschätzung
- **Lieferantenmanagement**:
  - Automatische Lieferantenbewertung
  - Kompetenzanalyse
  - Verhandlungsvorbereitung
- **Marktanalyse**: Integration von Trading Economics für Rohstoffpreise
- **CO2-Fußabdruck**: Berechnung der Umweltauswirkungen
- **Technische Zeichnungsanalyse**: PDF-Upload und automatische Analyse

### Premium UI/UX
- Moderne, professionelle Benutzeroberfläche
- Animierte Ladebildschirme
- Responsive Design
- Dark/Light Mode Support
- Glass-Morphism Effekte

## Voraussetzungen

- Python 3.10 oder höher
- OpenAI API Key (für GPT-Funktionen)
- Optional: Trading Economics API Key (für Marktdaten)
- Optional: Creditreform API Credentials (für Lieferantenprüfung)

## Installation

1. Repository klonen:
```bash
git clone https://github.com/DEIN-USERNAME/evaluera_screw_cost_app.git
cd evaluera_screw_cost_app
```

2. Virtual Environment erstellen:
```bash
python -m venv .venv
source .venv/bin/activate  # Auf Windows: .venv\Scripts\activate
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

4. Umgebungsvariablen konfigurieren:
```bash
cp .env.example .env
# .env mit deinen API Keys bearbeiten
```

## Konfiguration

Erstelle eine `.env` Datei mit folgenden Variablen:

```env
OPENAI_API_KEY=your_openai_api_key_here
TRADING_ECONOMICS_API_KEY=your_te_api_key_here
CREDITREFORM_USERNAME=your_username_here
CREDITREFORM_PASSWORD=your_password_here
```

## Verwendung

1. Anwendung starten:
```bash
streamlit run simple_app.py
```

2. Browser öffnet sich automatisch unter `http://localhost:8501`

3. CSV/Excel-Datei mit Bestelldaten hochladen

### Erwartetes Datenformat

Die Anwendung erkennt automatisch folgende Spaltennamen (DE/EN):

| Deutsch | English | Beschreibung |
|---------|---------|--------------|
| datum, bestelldatum | date | Bestelldatum |
| lieferant | supplier | Lieferantenname |
| artikel, artikelname, bezeichnung | item | Artikelbezeichnung |
| menge, qty | quantity | Bestellmenge |
| preis, einheitspreis, stk_preis | unit_price | Stückpreis |
| waehrung | currency | Währung |

Beispiel-CSV:
```csv
date,supplier,item,quantity,unit_price,currency
2024-01-15,Schrauben GmbH,M6x20 DIN 912,1000,0.05,EUR
2024-02-20,Fastener AG,M8x30 DIN 933,500,0.12,EUR
```

## Projektstruktur

```
evaluera_screw_cost_app/
├── simple_app.py              # Hauptanwendung
├── cost_helpers.py            # Kostenberechnungen & GPT-Integration
├── gpt_engine.py              # GPT-Routing & Analyse-Engine
├── gpt_wrappers.py            # Sichere GPT-Wrapper
├── price_utils.py             # Preisberechnungen
├── ui_components.py           # UI-Komponenten
├── enterprise_styles.py       # Enterprise-Styles
├── modern_premium_styles.py   # Premium-Styles
├── ultra_professional_styles.py # Professional-Styles
├── security.py                # Sicherheitsfunktionen
├── web_price.py               # Web-Scraping (Legacy)
├── loader.py                  # Ladeanimationen
├── requirements.txt           # Python-Abhängigkeiten
├── .env.example               # Beispiel-Konfiguration
└── sample_orders.csv          # Beispieldaten
```

## Sicherheit

- Sensitive Daten werden nicht geloggt
- API Keys werden sicher über Umgebungsvariablen verwaltet
- Input-Validierung für alle User-Eingaben
- Siehe `SECURITY.md` für Details

## Deployment

Siehe `DEPLOYMENT.md` für Anweisungen zum Deployment auf:
- Streamlit Cloud
- Heroku
- AWS
- Docker

## Entwicklung

### Code-Qualität
- Type Hints für bessere Code-Qualität
- Umfassende Fehlerbehandlung
- Logging für Debugging
- Siehe `DESIGN_GUIDE.md` für UI/UX-Richtlinien

### Tests ausführen
```bash
pytest
```

### Code-Formatierung
```bash
black .
flake8
```

## Dokumentation

- `DESIGN_GUIDE.md` - UI/UX Design-Richtlinien
- `DEPLOYMENT.md` - Deployment-Anleitungen
- `SECURITY.md` - Sicherheitsrichtlinien
- `LOADING_ANIMATIONS_GUIDE.md` - Ladeanimationen
- `TRADING_ECONOMICS_INTEGRATION.md` - Marktdaten-Integration

## Lizenz

Dieses Projekt ist nur für Evaluations- und Prototyping-Zwecke bestimmt.

## Support

Bei Fragen oder Problemen bitte ein Issue auf GitHub erstellen.

## Changelog

### Version 1.0.0
- Initiale Version
- GPT-4 Integration
- Trading Economics Integration
- Moderne UI mit Premium-Styles
- PDF-Zeichnungsanalyse
- CO2-Fußabdruck-Berechnung