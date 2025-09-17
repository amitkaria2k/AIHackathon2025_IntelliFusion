# DEPLOYMENT_GUIDE.md
# IntelliFusion AI Document Assistant - Deployment Guide
## Bosch AI Hackathon 2025

## 🚀 **Quick Start (Recommended)**

### **Option 1: Windows Users**
1. **Double-click** `start_windows.bat`
2. **Follow the prompts** in the command window
3. **Open your browser** to `http://localhost:8501`

### **Option 2: Linux/macOS Users**
1. **Run** `./start_unix.sh` in terminal
2. **Follow the prompts** 
3. **Open your browser** to `http://localhost:8501`

### **Option 3: Manual Setup**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env  # Edit with your Bosch credentials

# 3. Launch application
python run.py
```

## 📋 **Detailed Setup Instructions**

### **Prerequisites**
- **Python 3.8+** installed and accessible via command line
- **Git** (if cloning from repository)
- **Bosch Network Access** (for LLM Farm integration)
- **Bosch Docupedia PAT** (Personal Access Token)

### **Step 1: Environment Setup**

#### **1.1 Clone/Download Project**
```bash
# If using git
git clone <repository-url>
cd AIHackathon2025_IntelliFusion

# If using downloaded zip
# Extract the zip file and navigate to the folder
```

#### **1.2 Create Virtual Environment (Recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### **1.3 Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Configuration**

#### **2.1 Environment Variables**
```bash
# Copy example file
cp .env.example .env  # Linux/macOS
copy .env.example .env  # Windows
```

#### **2.2 Edit .env File**
Open `.env` in your text editor and configure:

```env
# Bosch LLM Farm Configuration
LLM_FARM_API_KEY=your_bosch_llm_farm_api_key_here
LLM_FARM_ENDPOINT=aoai-farm.bosch-temp.com
LLM_FARM_MODEL=gpt-4o-mini

# Bosch Docupedia Integration
DOCUPEDIA_PAT=your_personal_access_token_here
DOCUPEDIA_USER_AGENT=BoschAI-DocumentAssistant/1.0
DOCUPEDIA_BASE_URL=https://docupedia.bosch.com

# Database Configuration
DATABASE_URL=sqlite:///bosch_projects.db

# Application Settings
DEFAULT_APPROVERS=PM,Technical_Lead,Quality_Manager
ENVIRONMENT=production
DEBUG=False

# Optional: Advanced Settings
MAX_FILE_SIZE_MB=100
SESSION_TIMEOUT_MINUTES=60
CACHE_TTL_SECONDS=300
```

#### **2.3 Validate Configuration**
```bash
# Test your setup
python -c "
from src.config import *
print('✅ Configuration loaded successfully')
print(f'🔗 LLM Farm Endpoint: {LLM_FARM_ENDPOINT}')
print(f'💾 Database: {DATABASE_URL}')
"
```

### **Step 3: Launch Application**

#### **3.1 Using Run Script (Recommended)**
```bash
python run.py
```

#### **3.2 Direct Streamlit Launch**
```bash
streamlit run app/main.py --server.port 8501
```

#### **3.3 Background/Production Mode**
```bash
# Linux/macOS
nohup python run.py > intellifusion.log 2>&1 &

# Windows (using PowerShell)
Start-Process python -ArgumentList "run.py" -WindowStyle Hidden
```

### **Step 4: Access & Verification**

#### **4.1 Open Application**
1. **Open browser** to `http://localhost:8501`
2. **Login** using your Bosch credentials
3. **Select role**: PM, Project Team, or Quality Team

#### **4.2 Test Core Features**
1. **Dashboard Access**: Verify role-based dashboard loads
2. **AI Assistant**: Test chat functionality
3. **Project Creation**: Create a sample project (PM role)
4. **Document Generation**: Generate a test document
5. **LLM Integration**: Check AI responses work properly

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Issue: "ModuleNotFoundError"**
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt

# Or install specific missing module
pip install <module-name>
```

#### **Issue: "Port 8501 already in use"**
```bash
# Solution: Use different port
streamlit run app/main.py --server.port 8502

# Or kill existing process
# Windows
taskkill /F /IM streamlit.exe

# Linux/macOS
pkill -f streamlit
```

#### **Issue: "LLM Farm Connection Failed"**
```bash
# Check your .env configuration
# Verify network access to Bosch LLM Farm
# Confirm API key is valid
```

#### **Issue: "Database Error"**
```bash
# Delete existing database file
rm bosch_projects.db  # Linux/macOS
del bosch_projects.db  # Windows

# Restart application (database will be recreated)
```

#### **Issue: "Permission Denied" (Unix systems)**
```bash
# Make startup script executable
chmod +x start_unix.sh

# Make run script executable
chmod +x run.py
```

### **Debug Mode**

#### **Enable Debug Logging**
Edit `.env` file:
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

#### **Run Debug Tests**
```bash
# Test database connectivity
python tests/diagnostic.py

# Test LLM service
python tests/test_llm_service.py

# Test authentication
python tests/test_auth.py
```

## 🌐 **Production Deployment**

### **Option 1: Local Server Deployment**

#### **1.1 System Service Setup (Linux)**
Create `/etc/systemd/system/intellifusion.service`:
```ini
[Unit]
Description=IntelliFusion AI Document Assistant
After=network.target

[Service]
Type=simple
User=bosch-user
WorkingDirectory=/path/to/AIHackathon2025_IntelliFusion
Environment=PATH=/path/to/venv/bin
ExecStart=/path/to/venv/bin/python run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable intellifusion
sudo systemctl start intellifusion
```

#### **1.2 Windows Service Setup**
Use `nssm` (Non-Sucking Service Manager):
```cmd
# Download and install NSSM
nssm install IntelliFusion
# Set path to python.exe and run.py
# Configure service startup
```

### **Option 2: Docker Deployment**

#### **2.1 Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["python", "run.py"]
```

#### **2.2 Build and Run**
```bash
# Build image
docker build -t intellifusion .

# Run container
docker run -d -p 8501:8501 \
  --env-file .env \
  --name intellifusion \
  intellifusion
```

### **Option 3: Cloud Deployment (Streamlit Cloud)**

#### **3.1 Repository Setup**
1. **Push to GitHub** with all required files
2. **Ensure** `.streamlit/config.toml` is configured
3. **Verify** `requirements.txt` is complete

#### **3.2 Streamlit Cloud Configuration**
1. **Connect GitHub repo** to Streamlit Cloud
2. **Set environment variables** in cloud dashboard
3. **Deploy** using `app/main.py` as main file

## 🔐 **Security Configuration**

### **Production Security Checklist**
- [ ] **Change default passwords** in authentication system
- [ ] **Use HTTPS** in production (configure reverse proxy)
- [ ] **Set secure session cookies** in Streamlit config
- [ ] **Enable audit logging** for user actions
- [ ] **Configure firewall rules** to restrict access
- [ ] **Regular security updates** for dependencies
- [ ] **Backup database** regularly
- [ ] **Monitor for suspicious activity**

### **Streamlit Security Settings**
Add to `.streamlit/config.toml`:
```toml
[server]
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 100

[browser]
serverAddress = "127.0.0.1"
gatherUsageStats = false
```

## 📊 **Performance Optimization**

### **Database Optimization**
```sql
-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_projects_created ON projects(created_at);
CREATE INDEX IF NOT EXISTS idx_documents_project ON documents(project_id);
CREATE INDEX IF NOT EXISTS idx_workflows_status ON workflows(status);
```

### **Streamlit Performance**
Add to `app/main.py`:
```python
# Enable caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_projects():
    return db.get_projects()

@st.cache_resource
def init_llm_service():
    return LLMService()
```

### **Resource Monitoring**
```bash
# Monitor CPU/Memory usage
htop  # Linux
Task Manager  # Windows

# Monitor database size
du -h bosch_projects.db

# Monitor log files
tail -f intellifusion.log
```

## 🔄 **Maintenance & Updates**

### **Regular Maintenance Tasks**
- **Weekly**: Check logs for errors
- **Monthly**: Update dependencies (`pip install -U -r requirements.txt`)
- **Quarterly**: Review and update documentation
- **As needed**: Database cleanup and optimization

### **Backup Strategy**
```bash
# Database backup
cp bosch_projects.db backups/db_$(date +%Y%m%d).db

# Configuration backup
tar -czf backups/config_$(date +%Y%m%d).tar.gz .env .streamlit/

# Full system backup
tar -czf backups/full_$(date +%Y%m%d).tar.gz . --exclude=venv --exclude=__pycache__
```

### **Update Procedure**
1. **Stop application**
2. **Backup current version**
3. **Update code** (git pull or file replacement)
4. **Update dependencies** (`pip install -U -r requirements.txt`)
5. **Test configuration**
6. **Restart application**
7. **Verify functionality**

## 📞 **Support & Resources**

### **Getting Help**
- **Documentation**: Check `/docs/` directory
- **Troubleshooting**: Run `python tests/diagnostic.py`
- **Logs**: Check application logs and Streamlit logs
- **Community**: Bosch internal AI/ML forums

### **Useful Commands**
```bash
# Check application status
curl http://localhost:8501/_stcore/health

# View active processes
ps aux | grep streamlit  # Linux/macOS
tasklist | findstr streamlit  # Windows

# Check port usage
netstat -an | grep 8501

# View application logs
tail -f ~/.streamlit/logs/streamlit.log
```

## ✅ **Deployment Checklist**

### **Pre-Deployment**
- [ ] Python 3.8+ installed
- [ ] All dependencies in `requirements.txt`
- [ ] `.env` file configured with valid credentials
- [ ] Network access to Bosch LLM Farm verified
- [ ] Database permissions configured
- [ ] Firewall rules configured (if applicable)

### **Post-Deployment**
- [ ] Application accessible at configured URL
- [ ] All user roles can log in successfully
- [ ] AI Assistant responds correctly
- [ ] Document generation works
- [ ] Database operations successful
- [ ] Performance metrics within acceptable ranges
- [ ] Security settings verified
- [ ] Backup procedures tested
- [ ] Monitoring tools configured

---

**🎉 Your IntelliFusion AI Document Assistant is now ready for production use!**

**© 2025 Team IntelliFusion - Bosch AI Hackathon 2025**
