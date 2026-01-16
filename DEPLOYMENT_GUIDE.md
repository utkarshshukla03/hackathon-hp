# 🚀 DEPLOYMENT GUIDE

## HPCL Intelligent Cost Database - Deployment Instructions

---

## Option 1: Local Development (Recommended for First Demo)

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

```bash
# Step 1: Navigate to project directory
cd intelligent-cost-database

# Step 2: Create virtual environment (recommended)
python -m venv venv

# Step 3: Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Navigate to frontend
cd frontend

# Step 6: Launch Streamlit app
streamlit run app.py
```

**Result**: Dashboard opens automatically at http://localhost:8501

### Verify Installation
```bash
# Test Streamlit
streamlit version

# Test Pandas
python -c "import pandas as pd; print(pd.__version__)"

# Test Plotly
python -c "import plotly; print(plotly.__version__)"
```

---

## Option 2: Docker Deployment

### Prerequisites
- Docker installed and running

### Create Dockerfile

```dockerfile
# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build & Run

```bash
# Build image
docker build -t hpcl-cost-db:latest .

# Run container
docker run -p 8501:8501 hpcl-cost-db:latest

# Run with data volume (for persistent data)
docker run -v $(pwd)/data:/app/data -p 8501:8501 hpcl-cost-db:latest
```

**Result**: Dashboard available at http://localhost:8501

### Docker Compose (Multi-container setup)

```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped

  # Future: Add database service here
  # postgres:
  #   image: postgres:14
  #   environment:
  #     POSTGRES_DB: hpcl_cost_db
  #     POSTGRES_PASSWORD: secure_password
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   restart: unless-stopped

volumes:
  postgres_data:
```

**Run with Docker Compose**:
```bash
docker-compose up
```

---

## Option 3: Streamlit Cloud (Easiest - Free Hosting)

### Prerequisites
- GitHub account
- Streamlit account (free)

### Steps

1. **Push Code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: HPCL Cost Database"
   git branch -M main
   git remote add origin https://github.com/username/hpcl-cost-db.git
   git push -u origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Sign up with GitHub
   - Click "New app"
   - Select your repository
   - Set branch: `main`
   - Set main file path: `frontend/app.py`
   - Click "Deploy"

3. **Share URL**
   - Your app is live at: `https://[username]-[appname].streamlit.app`
   - Share link with stakeholders

### Streamlit Cloud Configuration

Create `.streamlit/config.toml`:
```toml
[client]
showErrorDetails = false
toolbarMode = "minimal"

[logger]
level = "warning"

[theme]
primaryColor = "#667eea"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#2c3e50"
font = "sans serif"
```

---

## Option 4: AWS Deployment

### Using Elastic Beanstalk

1. **Create Procfile** (in root directory):
   ```
   web: cd frontend && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create requirements-aws.txt**:
   ```
   streamlit==1.28.1
   pandas==2.1.3
   plotly==5.18.0
   numpy==1.24.3
   python-dateutil==2.8.2
   gunicorn==21.2.0
   ```

3. **Deploy**:
   ```bash
   eb init -p python-3.9 hpcl-cost-db
   eb create hpcl-cost-db-env
   eb deploy
   ```

### Using EC2

```bash
# SSH to EC2 instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# Clone repository
git clone https://github.com/username/hpcl-cost-db.git
cd hpcl-cost-db

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/streamlit.service
```

### Systemd Service File:
```ini
[Unit]
Description=HPCL Cost Database Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/hpcl-cost-db
Environment="PATH=/home/ubuntu/hpcl-cost-db/venv/bin"
ExecStart=/home/ubuntu/hpcl-cost-db/venv/bin/streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable streamlit
sudo systemctl start streamlit
```

---

## Option 5: Azure Deployment

### Using App Service

1. **Create Azure App Service**:
   ```bash
   az group create --name hpcl-rg --location eastus
   
   az appservice plan create \
     --name hpcl-plan \
     --resource-group hpcl-rg \
     --sku B1
   
   az webapp create \
     --resource-group hpcl-rg \
     --plan hpcl-plan \
     --name hpcl-cost-db \
     --deployment-container-image-name-user-provided \
     --docker-registry-server-url https://myregistry.azurecr.io
   ```

2. **Configure app**:
   ```bash
   az webapp config appsettings set \
     --resource-group hpcl-rg \
     --name hpcl-cost-db \
     --settings WEBSITES_PORT=8501
   ```

3. **Deploy**:
   ```bash
   az webapp deployment source config-zip \
     --resource-group hpcl-rg \
     --name hpcl-cost-db \
     --src project.zip
   ```

---

## Option 6: Heroku Deployment (Legacy - Still Works)

### Create Procfile:
```
web: cd frontend && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Deploy:
```bash
heroku create hpcl-cost-db
heroku config:set IS_HEROKU=true
git push heroku main
```

---

## Configuration for Production

### Environment Variables

Create `.env` file:
```env
# Environment
ENVIRONMENT=production

# Streamlit
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_LOGGER_LEVEL=warning

# Data
DATA_PATH=/app/data
LOG_PATH=/app/logs

# Security (when Phase 2 adds auth)
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:5432/db
```

Load in app.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DATA_PATH = os.getenv('DATA_PATH', './data')
```

---

## Performance Optimization

### Streamlit-Specific

```python
# In app.py
import streamlit as st

# Cache data loading
@st.cache_data
def load_data():
    # Load data efficiently
    return data

# Set page config once
st.set_page_config(
    page_title="HPCL Cost DB",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Use columns for layout (faster than containers)
col1, col2 = st.columns(2)
```

### Data Handling

```python
# Use efficient data types
df = pd.read_csv('file.csv', dtype={
    'po_id': 'string',
    'unit_price': 'float32',
    'quantity': 'int16'
})

# Filter early, display less data
filtered = df[df['region'] == selected_region]
```

### Caching Strategy

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def expensive_computation():
    return result

@st.cache_resource  # Cache once, reuse forever
def init_connection():
    return connection
```

---

## Monitoring & Logging

### Local Monitoring

```python
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info(f"User accessed {tab_name} tab")
```

### Production Monitoring

**Recommended tools**:
- **Logs**: CloudWatch (AWS), Log Analytics (Azure), Stackdriver (GCP)
- **Metrics**: Prometheus + Grafana
- **APM**: Datadog, New Relic, Elastic APM
- **Health Checks**: Pingdom, Uptime Robot

### Health Check Endpoint (Flask add-on)

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({
        'uptime': uptime_seconds,
        'requests': total_requests,
        'errors': error_count
    }), 200
```

---

## Troubleshooting Deployment

### Common Issues & Solutions

| Issue | Cause | Solution |
|---|---|---|
| **Port already in use** | Another app on port 8501 | `lsof -i :8501` and kill process |
| **Module not found** | Missing dependency | `pip install -r requirements.txt` |
| **Data not loading** | Wrong path | Check `__file__` and use absolute paths |
| **Slow performance** | Large dataset | Add caching, filter early |
| **Memory errors** | Dataset too large | Use chunking, database |

### Debug Commands

```bash
# Check Python version
python --version

# List installed packages
pip list

# Test imports
python -c "import streamlit; print(streamlit.__version__)"

# Run with verbose logging
streamlit run app.py --logger.level=debug

# Check port availability
netstat -an | grep LISTEN
```

---

## Scaling Strategy

### Phase 1 (Now): Single Server
- 1 Streamlit instance
- CSV files for data
- < 1000 concurrent users

### Phase 2: Multiple Instances
- Load balancer (Nginx/HAProxy)
- Shared storage (S3, Azure Blob)
- Database (PostgreSQL)
- 1000-10K concurrent users

### Phase 3: Microservices
- Separate API service
- Separate analytics service
- Caching layer (Redis)
- 10K+ concurrent users

### Phase 4: Enterprise
- CDN for static assets
- Multi-region deployment
- Advanced security (SAML, OAuth)
- Compliance (GDPR, SOC2)

---

## Security Checklist

- [ ] Remove debug mode in production
- [ ] Use HTTPS/TLS certificates
- [ ] Set strong authentication (Phase 2)
- [ ] Encrypt sensitive data
- [ ] Regular backups
- [ ] WAF (Web Application Firewall)
- [ ] DDoS protection
- [ ] Regular security audits
- [ ] Penetration testing
- [ ] Compliance validation (ISO 27001, SOC2)

---

## Cost Estimation

| Deployment | Monthly Cost | Suitable For |
|---|---|---|
| **Local** | $0 | Development |
| **Streamlit Cloud** | Free (up to 3 apps) | Small teams |
| **Docker + AWS** | $20-50 | Pilot projects |
| **AWS App Service** | $50-200 | Department-wide |
| **Azure Multi-region** | $500-1000 | Enterprise |

---

## Post-Deployment Checklist

- [ ] Test all dashboard tabs
- [ ] Verify data loads correctly
- [ ] Check filters and search
- [ ] Test export functionality
- [ ] Monitor performance metrics
- [ ] Set up logging
- [ ] Create backup strategy
- [ ] Document access procedures
- [ ] Train users
- [ ] Plan maintenance windows

---

## Support & Maintenance

### Backup Strategy
```bash
# Automated daily backup
0 2 * * * tar -czf /backups/data-$(date +\%Y\%m\%d).tar.gz /app/data
```

### Update Strategy
```bash
# Test updates in staging first
# Then deploy to production
# Keep version history
```

### User Support
- Provide QUICKSTART.md link
- FAQ document
- Video tutorial
- Email support channel

---

## Next Steps

1. **Choose deployment option** based on your infrastructure
2. **Follow the setup steps** for your chosen option
3. **Test thoroughly** before going live
4. **Monitor performance** post-deployment
5. **Plan Phase 2** enhancements (database, ML)

---

**Deployment Complete!** 🎉

For questions, refer to:
- [README.md](README.md)
- [QUICKSTART.md](QUICKSTART.md)
- [PROJECT_COMPLETION_SUMMARY.md](PROJECT_COMPLETION_SUMMARY.md)

