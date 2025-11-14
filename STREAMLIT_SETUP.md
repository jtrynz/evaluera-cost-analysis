# 🔐 Streamlit Cloud Secrets Konfiguration

Diese Anleitung erklärt, wie Sie API-Keys sicher in Streamlit Cloud konfigurieren.

## ⚠️ WICHTIG: Niemals API-Keys im Code committen!

Da das Repository **PUBLIC** ist, dürfen **KEINE** API-Keys in folgenden Orten gespeichert werden:
- ❌ `.env` Datei (wird von `.gitignore` ausgeschlossen)
- ❌ Im Python-Code hardcodiert
- ❌ In Git committed
- ✅ **NUR in Streamlit Cloud Secrets** (für Production)
- ✅ **NUR in lokaler `.env` Datei** (für lokale Entwicklung, NICHT committen!)

---

## 📋 Schritt-für-Schritt Anleitung

### 1. Streamlit Cloud App öffnen

1. Gehe zu: https://share.streamlit.io/
2. Login mit deinem GitHub Account
3. Finde deine App: `evaluera-cost-analysis`

### 2. Secrets konfigurieren

1. Klicke auf deine App in der Liste
2. Klicke auf **"⚙️ Settings"** (Zahnrad-Icon rechts oben)
3. Wähle den Tab **"Secrets"**
4. Füge folgende Secrets hinzu:

```toml
# Required: OpenAI API Key für GPT-4o
OPENAI_API_KEY = "sk-proj-DEIN_ECHTER_KEY_HIER"

# Optional: Trading Economics API (für Rohstoffmarkt-Daten)
TRADING_ECONOMICS_API_KEY = "client_key:secret_key"

# Optional: TradingEconomics Client Key
TRADINGECONOMICS_CLIENTKEY = "dein_key_hier"
```

### 3. App neu starten

1. Nach dem Speichern der Secrets klicke auf **"Reboot app"**
2. Die App wird mit den neuen Secrets neu gestartet
3. Die API-Keys sind jetzt sicher verfügbar!

---

## 🧪 Lokale Entwicklung

Für lokale Entwicklung auf deinem Computer:

1. Kopiere `.env.example` zu `.env`:
   ```bash
   cp .env.example .env
   ```

2. Öffne `.env` und füge deinen echten OpenAI API Key ein:
   ```bash
   OPENAI_API_KEY=sk-proj-DEIN_ECHTER_KEY
   ```

3. **WICHTIG:** Die `.env` Datei wird von Git ignoriert und wird **NIEMALS** committed!

4. Starte die App lokal:
   ```bash
   streamlit run simple_app.py
   ```

---

## 🔍 Wie funktioniert die sichere Key-Verwaltung?

Der Code in `simple_app.py` lädt API-Keys in folgender Priorität:

```python
def get_api_key(key_name, default=None):
    # 1. PRODUCTION: Streamlit Secrets (Streamlit Cloud)
    if hasattr(st, 'secrets') and key_name in st.secrets:
        return st.secrets[key_name]

    # 2. LOCAL: Environment Variable aus .env Datei
    value = os.getenv(key_name)
    if value:
        return value

    # 3. FALLBACK: Default
    return default
```

**Vorteile:**
- ✅ **Sicher:** Keys werden niemals im Code oder Git gespeichert
- ✅ **Flexibel:** Funktioniert lokal (.env) und in Production (Streamlit Secrets)
- ✅ **Best Practice:** Industry-Standard für Secret Management

---

## 🚨 Troubleshooting

### Problem: "OpenAI API Key not found"

**Lösung:**
1. Prüfe ob der Secret-Name **exakt** `OPENAI_API_KEY` heißt (case-sensitive!)
2. Prüfe ob der Key mit `sk-proj-` beginnt (neues Format) oder `sk-` (altes Format)
3. Reboot die App nach dem Hinzufügen von Secrets
4. Prüfe in OpenAI Dashboard ob der Key aktiv ist: https://platform.openai.com/api-keys

### Problem: "Rate limit exceeded"

**Lösung:**
1. Gehe zu OpenAI Dashboard: https://platform.openai.com/usage
2. Prüfe ob Credits verfügbar sind
3. Falls nötig: Upgrade deinen Plan oder füge Credits hinzu

### Problem: App zeigt "Unauthorized 401"

**Lösung:**
1. Key ist ungültig oder abgelaufen
2. Generiere einen neuen Key in OpenAI Dashboard
3. Update den Secret in Streamlit Cloud
4. Reboot die App

---

## 📚 Weitere Ressourcen

- [Streamlit Secrets Documentation](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Trading Economics API](https://tradingeconomics.com/analytics/api.aspx)

---

## 🔐 Security Best Practices

1. **Rotiere Keys regelmäßig** (alle 90 Tage)
2. **Verwende unterschiedliche Keys** für Dev/Staging/Production
3. **Aktiviere Rate Limiting** in deinem OpenAI Account
4. **Monitor API Usage** regelmäßig
5. **Lösche alte Keys** wenn nicht mehr verwendet
6. **Teile niemals Keys** in Slack, E-Mail, Screenshots, etc.

---

**Bei Fragen oder Problemen:** Erstelle ein Issue im GitHub Repository oder kontaktiere den Support.
