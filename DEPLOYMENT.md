# 🚀 DEPLOYMENT GUIDE - EVALUERA

## Quick Start Deployment

### **Lokales Setup (Development)**

```bash
# 1. Repository clonen
git clone <repository-url>
cd evaluera_screw_cost_app

# 2. Virtual Environment erstellen
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ODER
.venv\Scripts\activate  # Windows

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. Environment Variables konfigurieren
cp .env.example .env
# WICHTIG: .env mit echten API-Keys befüllen!

# 5. App starten
streamlit run simple_app.py
```

App läuft auf: **http://localhost:8501**

---

## 🌐 Production Deployment

### **Option 1: Streamlit Community Cloud (Einfachst)**

1. **Repository auf GitHub pushen**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo>
   git push -u origin main
   ```

2. **Auf Streamlit Cloud deployen**
   - Gehen Sie zu: https://share.streamlit.io/
   - Klicken Sie "New app"
   - Wählen Sie Ihr GitHub Repository
   - Setzen Sie: `simple_app.py` als Main file
   - Fügen Sie Secrets hinzu (Environment Variables)

3. **Secrets konfigurieren** (in Streamlit Cloud UI):
   ```toml
   # Secrets Format (TOML)
   OPENAI_API_KEY = "sk-proj-..."
   TRADING_ECONOMICS_API_KEY = "key:secret"
   ```

4. **Deploy klicken!** ✅

**Vorteile**:
- ✅ Kostenlos (Community Plan)
- ✅ HTTPS automatisch
- ✅ Auto-Deployments bei Git Push
- ✅ Einfache Secret-Verwaltung

**Nachteile**:
- ❌ Öffentlich zugänglich (außer mit Password Protection)
- ❌ Limited Resources
- ❌ Keine VPN/Private Network

---

### **Option 2: Docker Deployment (Flexibel)**

#### **Dockerfile erstellen**:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App Code kopieren
COPY . .

# Port exposieren
EXPOSE 8501

# Health Check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# App starten
CMD ["streamlit", "run", "simple_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### **Docker Compose** (`docker-compose.yml`):
```yaml
version: '3.8'

services:
  evaluera:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    environment:
      - STREAMLIT_SERVER_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### **Deployment**:
```bash
# Build
docker-compose build

# Starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Stoppen
docker-compose down
```

---

### **Option 3: Cloud Providers (Enterprise)**

#### **AWS (Amazon Web Services)**

**A. Elastic Beanstalk** (Managed):
```bash
# 1. EB CLI installieren
pip install awsebcli

# 2. Initialisieren
eb init -p docker evaluera

# 3. Erstellen & Deployen
eb create evaluera-prod
eb deploy

# 4. Environment Variables setzen
eb setenv OPENAI_API_KEY=sk-proj-...
```

**B. ECS (Container Service)**:
- Push Docker Image zu ECR
- Erstellen Sie ECS Task Definition
- Deployen Sie mit Fargate (serverless)

**C. EC2 (Manual)**:
```bash
# Auf EC2 Instance
sudo apt update
sudo apt install python3-pip python3-venv nginx

# App Setup (wie lokal)
git clone <repo>
cd evaluera_screw_cost_app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Systemd Service erstellen
sudo nano /etc/systemd/system/evaluera.service
```

**Systemd Service** (`evaluera.service`):
```ini
[Unit]
Description=EVALUERA Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/evaluera_screw_cost_app
Environment="PATH=/home/ubuntu/evaluera_screw_cost_app/.venv/bin"
EnvironmentFile=/home/ubuntu/evaluera_screw_cost_app/.env
ExecStart=/home/ubuntu/evaluera_screw_cost_app/.venv/bin/streamlit run simple_app.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Service starten
sudo systemctl enable evaluera
sudo systemctl start evaluera
sudo systemctl status evaluera
```

**Nginx Reverse Proxy** (`/etc/nginx/sites-available/evaluera`):
```nginx
server {
    listen 80;
    server_name evaluera.ihrefirma.de;

    # SSL (LetsEncrypt - certbot)
    # Wird von certbot automatisch hinzugefügt

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# SSL mit LetsEncrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d evaluera.ihrefirma.de
```

#### **Azure (Microsoft)**

**Azure App Service**:
```bash
# 1. Azure CLI installieren
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# 2. Login
az login

# 3. Resource Group erstellen
az group create --name evaluera-rg --location westeurope

# 4. App Service Plan
az appservice plan create --name evaluera-plan --resource-group evaluera-rg --sku B1 --is-linux

# 5. Web App erstellen
az webapp create --resource-group evaluera-rg --plan evaluera-plan --name evaluera-app --runtime "PYTHON:3.12"

# 6. Code deployen
az webapp up --name evaluera-app --resource-group evaluera-rg

# 7. Environment Variables
az webapp config appsettings set --resource-group evaluera-rg --name evaluera-app --settings OPENAI_API_KEY="sk-proj-..."
```

#### **Google Cloud Platform**

**Cloud Run** (Serverless):
```bash
# 1. gcloud CLI installieren
curl https://sdk.cloud.google.com | bash

# 2. Login & Config
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Docker Image bauen & pushen
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/evaluera

# 4. Deployen
gcloud run deploy evaluera \
  --image gcr.io/YOUR_PROJECT_ID/evaluera \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY="sk-proj-..."
```

---

## 🔐 Security für Production

### **1. HTTPS/SSL erzwingen**

**Streamlit Config** (`.streamlit/config.toml`):
```toml
[server]
enableCORS = false
enableXsrfProtection = true
cookieSecret = "CHANGE_THIS_TO_RANDOM_SECRET"

[client]
toolbarMode = "minimal"
```

**Nginx** (force HTTPS):
```nginx
server {
    listen 80;
    server_name evaluera.ihrefirma.de;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name evaluera.ihrefirma.de;

    ssl_certificate /etc/letsencrypt/live/evaluera.ihrefirma.de/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/evaluera.ihrefirma.de/privkey.pem;

    # Strong SSL Config
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # ... rest of config
}
```

### **2. Authentication hinzufügen**

**Option A: Nginx Basic Auth** (Schnell & Einfach):
```bash
# Passwort-Datei erstellen
sudo htpasswd -c /etc/nginx/.htpasswd admin

# In nginx config:
location / {
    auth_basic "EVALUERA - Login Required";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://localhost:8501;
}
```

**Option B: Streamlit Authentication** (App-Level):
```python
# In simple_app.py am Anfang:
import streamlit_authenticator as stauth

# Config aus .env oder secrets.toml
authenticator = stauth.Authenticate(
    credentials,
    cookie_name='evaluera_auth',
    key='some_signature_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # App läuft wie normal
    st.title("EVALUERA")
    # ...
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()
```

### **3. Rate Limiting**

**Nginx**:
```nginx
http {
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        location / {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://localhost:8501;
        }
    }
}
```

**CloudFlare** (Empfohlen):
- Rate Limiting Rules
- DDoS Protection
- Bot Detection
- Analytics

---

## 📊 Monitoring & Logging

### **Logs sammeln**

```python
# In simple_app.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/evaluera.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("App started")
```

### **Error Tracking mit Sentry**

```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[LoggingIntegration()],
    environment="production",
    traces_sample_rate=0.1
)
```

### **Health Check Endpoint**

Streamlit hat einen built-in Health Check:
```
GET https://your-app.com/_stcore/health
```

---

## 🔄 CI/CD Pipeline

### **GitHub Actions** (`.github/workflows/deploy.yml`):

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pip install pytest
        pytest tests/

    - name: Security scan
      run: |
        pip install safety
        safety check

    - name: Deploy to Production
      env:
        SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
      run: |
        # SSH zu Production Server
        ssh user@your-server.com << 'EOF'
          cd /app/evaluera
          git pull
          source .venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart evaluera
        EOF
```

---

## 🆘 Troubleshooting

### **Problem: App startet nicht**

```bash
# Logs anschauen
sudo journalctl -u evaluera -f

# Häufige Ursachen:
# 1. Port bereits in Verwendung
sudo lsof -i :8501

# 2. Fehlende Environment Variables
cat .env

# 3. Permission Issues
sudo chown -R ubuntu:ubuntu /app/evaluera

# 4. Dependencies fehlen
pip install -r requirements.txt
```

### **Problem: "ModuleNotFoundError"**

```bash
# Venv aktiviert?
which python  # Sollte .venv/bin/python zeigen

# Dependencies neu installieren
pip install --force-reinstall -r requirements.txt
```

### **Problem: API Timeout**

```python
# In cost_helpers.py - Timeout erhöhen:
client = OpenAI(
    api_key=api_key,
    timeout=60.0,  # 60 Sekunden
    max_retries=3
)
```

---

## 📈 Scaling

### **Horizontal Scaling** (mehrere Instances):

**Load Balancer** (nginx):
```nginx
upstream evaluera_app {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}

server {
    location / {
        proxy_pass http://evaluera_app;
    }
}
```

**Kubernetes** (für große Deployments):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: evaluera
spec:
  replicas: 3
  selector:
    matchLabels:
      app: evaluera
  template:
    metadata:
      labels:
        app: evaluera
    spec:
      containers:
      - name: evaluera
        image: your-registry/evaluera:latest
        ports:
        - containerPort: 8501
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: evaluera-secrets
              key: openai-api-key
```

---

## ✅ Post-Deployment Checklist

- [ ] App läuft und ist erreichbar
- [ ] HTTPS aktiviert
- [ ] Authentication funktioniert
- [ ] Alle Environment Variables gesetzt
- [ ] Monitoring/Alerting konfiguriert
- [ ] Backups eingerichtet
- [ ] DNS konfiguriert
- [ ] Firewall Rules gesetzt
- [ ] Rate Limiting aktiv
- [ ] Error Tracking (Sentry) funktioniert
- [ ] Logs werden gespeichert
- [ ] Health Checks laufen
- [ ] Auto-Scaling konfiguriert (falls benötigt)
- [ ] Disaster Recovery Plan vorhanden

---

## 📞 Support & Kontakte

**Bei Problemen**:
1. Logs checken
2. GitHub Issues durchsuchen
3. Dokumentation lesen
4. Support kontaktieren

**Wichtige Links**:
- Streamlit Docs: https://docs.streamlit.io/
- OpenAI API: https://platform.openai.com/docs
- AWS Docs: https://docs.aws.amazon.com/
- Azure Docs: https://docs.microsoft.com/azure/

---

**Viel Erfolg beim Deployment!** 🚀
