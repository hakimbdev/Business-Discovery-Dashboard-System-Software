# 📖 Complete Setup Guide

## Step-by-Step Installation & Configuration

### 1️⃣ System Requirements

**Minimum Requirements:**
- Python 3.8 or higher
- 2GB RAM
- 1GB free disk space
- Internet connection

**Recommended:**
- Python 3.10+
- 4GB RAM
- SSD storage
- Stable internet (for API calls)

---

### 2️⃣ Python Installation

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: `python --version`

#### Mac
```bash
# Using Homebrew
brew install python@3.10

# Verify
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv

# Verify
python3 --version
```

---

### 3️⃣ Project Setup

```bash
# Navigate to project directory
cd "Automated System Alert"

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 4️⃣ API Keys Configuration

#### A. Facebook Graph API (Optional but Recommended)

**Step 1: Create Facebook App**
1. Go to https://developers.facebook.com/
2. Click "My Apps" → "Create App"
3. Choose "Business" type
4. Fill in app details

**Step 2: Get Access Token**
1. Go to Graph API Explorer
2. Select your app
3. Request permissions: `pages_read_engagement`, `pages_show_list`
4. Generate token
5. Copy the access token

**Step 3: Add to Configuration**
Edit `config/settings.yaml`:
```yaml
api_keys:
  facebook:
    app_id: "YOUR_APP_ID"
    app_secret: "YOUR_APP_SECRET"
    access_token: "YOUR_ACCESS_TOKEN"
```

---

#### B. Google Custom Search API (Highly Recommended)

**Step 1: Create Google Cloud Project**
1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable "Custom Search API"
4. Go to "Credentials" → "Create Credentials" → "API Key"
5. Copy the API key

**Step 2: Create Custom Search Engine**
1. Go to https://programmablesearchengine.google.com/
2. Click "Add" to create new search engine
3. Sites to search: Leave empty or add `facebook.com`, `linkedin.com`
4. Click "Create"
5. Copy the "Search engine ID"

**Step 3: Add to Configuration**
```yaml
api_keys:
  google:
    api_key: "YOUR_GOOGLE_API_KEY"
    search_engine_id: "YOUR_SEARCH_ENGINE_ID"
```

**Note:** Google Custom Search API has a free tier of 100 queries/day. For more, you'll need to enable billing.

---

#### C. Telegram Bot (For Instant Alerts)

**Step 1: Create Bot**
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow instructions to name your bot
5. Copy the bot token

**Step 2: Get Chat ID**
1. Start a chat with your bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find `"chat":{"id":123456789}` in the response
5. Copy the chat ID

**Step 3: Add to Configuration**
```yaml
api_keys:
  telegram:
    bot_token: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    chat_id: "123456789"
```

---

#### D. Email Alerts (Gmail)

**Step 1: Enable 2-Factor Authentication**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification

**Step 2: Generate App Password**
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and your device
3. Click "Generate"
4. Copy the 16-character password

**Step 3: Add to Configuration**
```yaml
api_keys:
  email:
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    sender_email: "your_email@gmail.com"
    sender_password: "your_16_char_app_password"
    recipient_email: "recipient@example.com"
```

---

### 5️⃣ Customize Keywords & Categories

Edit `config/keywords.yaml` to add/remove:

**Add New Category:**
```yaml
business_categories:
  your_category:
    keywords:
      - "keyword1"
      - "keyword2"
    priority: high
```

**Add New Cities:**
```yaml
location_signals:
  major_cities:
    - "Your City"
    - "Another City"
```

---

### 6️⃣ Test the System

**Test Configuration:**
```bash
python -c "from src.core.config_manager import config; print('Config loaded successfully!')"
```

**Test Database:**
```bash
python -c "from src.core.database import DatabaseHandler; db = DatabaseHandler(); print('Database initialized!')"
```

**Run Manual Discovery:**
```bash
python main.py discover
```

This will run one discovery cycle and show results in logs.

---

### 7️⃣ Start the System

**Full System (Recommended):**
```bash
python main.py
```

This starts:
- Automated scheduler
- Web dashboard on http://localhost:8000
- Alert system

**Access Dashboard:**
1. Open browser
2. Go to http://localhost:8000
3. Login with:
   - Username: `admin`
   - Password: `changeme123`

---

### 8️⃣ Change Default Password

Edit `config/settings.yaml`:
```yaml
dashboard:
  username: "your_username"
  password: "your_secure_password"
```

---

### 9️⃣ Configure Scheduler Intervals

Edit `config/settings.yaml`:

```yaml
scheduler:
  # How often to run each scraper (in minutes)
  facebook_interval_minutes: 30
  linkedin_interval_minutes: 45
  google_interval_minutes: 60
  
  # Enable/disable scrapers
  enable_facebook: true
  enable_linkedin: true
  enable_google: true
```

**Recommendations:**
- **High frequency** (15-30 min): For time-sensitive leads
- **Medium frequency** (60 min): Balanced approach
- **Low frequency** (120+ min): To avoid rate limits

---

### 🔟 Configure Alert Mode

**Instant Alerts** (recommended for high-priority leads):
```yaml
alerts:
  batch_mode: false
  enable_email: true
  enable_telegram: true
  enable_desktop: true
```

**Batch Alerts** (daily summary):
```yaml
alerts:
  batch_mode: true
  batch_interval_hours: 24
```

---

## 🚀 Running on VPS/Cloud Server

### Deploy to Ubuntu Server

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python
sudo apt install python3.10 python3-pip python3-venv -y

# 3. Clone/upload project
cd /opt
sudo mkdir business-discovery
sudo chown $USER:$USER business-discovery
cd business-discovery

# 4. Upload files (use SCP, SFTP, or Git)

# 5. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Configure settings
nano config/settings.yaml

# 7. Test
python main.py discover

# 8. Create systemd service
sudo nano /etc/systemd/system/business-discovery.service
```

**Service file content:**
```ini
[Unit]
Description=Business Discovery System
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/opt/business-discovery
Environment="PATH=/opt/business-discovery/venv/bin"
ExecStart=/opt/business-discovery/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable business-discovery
sudo systemctl start business-discovery
sudo systemctl status business-discovery
```

---

## 🔍 Monitoring & Logs

**View Logs:**
```bash
tail -f logs/system.log
```

**Check Database:**
```bash
sqlite3 data/businesses.db "SELECT COUNT(*) FROM businesses;"
```

**Monitor System:**
```bash
# Check if running
ps aux | grep main.py

# Check resource usage
top -p $(pgrep -f main.py)
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] API keys configured
- [ ] Keywords customized
- [ ] Test discovery successful
- [ ] Dashboard accessible
- [ ] Alerts working
- [ ] Logs being created
- [ ] Database initialized

---

## 🆘 Common Issues

**Issue: ModuleNotFoundError**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue: Port 8000 already in use**
```yaml
# Solution: Change port in config/settings.yaml
dashboard:
  port: 8080
```

**Issue: No businesses discovered**
- Check API keys are valid
- Verify internet connection
- Check logs for errors
- Try manual discovery

---

## 🎉 You're Ready!

Your system is now configured and ready to discover Nigerian businesses!

**Next Steps:**
1. Monitor the dashboard
2. Check alerts
3. Export leads to CSV
4. Contact discovered businesses
5. Grow your business! 🚀

