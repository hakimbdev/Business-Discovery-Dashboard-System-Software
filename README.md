# 🎯 Automated Business Discovery System for Nigeria

A powerful Python-based OSINT system that automatically detects **newly created Facebook Pages and LinkedIn Company Pages** for specific business categories in Nigeria, with real-time alerts and a beautiful web dashboard.

## 🌟 Features

### ✅ Automated Discovery
- **Facebook Pages**: Discovers new business pages using Graph API and search methods
- **LinkedIn Companies**: Finds new company pages using ethical scraping
- **Google OSINT**: Uses Google search operators (dorks) for comprehensive discovery
- **Time-based Filtering**: Focuses on recently created pages (configurable lookback period)

### ✅ Target Business Categories
- Startups & Tech Companies
- Hotels & Hospitality
- Suites & Apartments
- Travel & Tour Agencies
- Real Estate Companies
- Schools & Educational Institutions
- Restaurants & Cafés

### ✅ Intelligent Lead Scoring
- Confidence scoring (0-100) based on multiple signals
- Priority classification (High/Medium/Low)
- Location verification (Nigerian cities, phone patterns)
- Category keyword matching
- Contact information validation

### ✅ Multi-Channel Alerts
- **Email**: HTML-formatted alerts via SMTP
- **Telegram**: Instant notifications via Telegram Bot
- **Desktop**: Native OS notifications
- **Batch Mode**: Daily summary reports

### ✅ Web Dashboard
- Real-time business monitoring
- Filter by platform, category, location
- Export to CSV
- Statistics and analytics
- Manual discovery triggers

### ✅ De-duplication & Storage
- SQLite database (PostgreSQL support available)
- Hash-based duplicate detection
- Search history tracking
- Export capabilities

---

## 🏗️ System Architecture

```
Discovery Layer (Facebook, LinkedIn, Google)
    ↓
Core Processing (Extraction, Validation, Scoring)
    ↓
Storage Layer (SQLite/PostgreSQL)
    ↓
Alert Layer (Email, Telegram, Desktop)
    ↓
Dashboard (FastAPI + Web UI)
```

---

## 📋 Prerequisites

- Python 3.8 or higher
- Internet connection
- API Keys (see Configuration section)

---

## 🚀 Quick Start

### 1. Clone or Download

```bash
cd "Automated System Alert"
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Edit `config/settings.yaml` and add your API credentials:

```yaml
api_keys:
  facebook:
    access_token: "YOUR_FACEBOOK_ACCESS_TOKEN"
  
  google:
    api_key: "YOUR_GOOGLE_API_KEY"
    search_engine_id: "YOUR_SEARCH_ENGINE_ID"
  
  telegram:
    bot_token: "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id: "YOUR_TELEGRAM_CHAT_ID"
  
  email:
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    sender_email: "your_email@gmail.com"
    sender_password: "your_app_password"
    recipient_email: "recipient@example.com"
```

### 4. Run the System

```bash
# Start full system (scheduler + dashboard)
python main.py

# Run manual discovery once
python main.py discover

# Show help
python main.py help
```

### 5. Access Dashboard

Open your browser and navigate to:
```
http://localhost:8000
```

Default credentials:
- Username: `admin`
- Password: `changeme123`

---

## 🔑 API Keys Setup Guide

### Facebook Graph API

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add "Facebook Login" product
4. Get your App ID, App Secret, and Access Token
5. Note: Facebook's search API is limited; Google search is more effective

### Google Custom Search API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Custom Search API"
4. Create credentials (API Key)
5. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
6. Create a new search engine
7. Get your Search Engine ID

### Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow instructions
3. Copy the bot token
4. Start a chat with your bot
5. Get your chat ID from `https://api.telegram.org/bot<TOKEN>/getUpdates`

### Email (Gmail)

1. Enable 2-Factor Authentication on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an app password for "Mail"
4. Use this password in the configuration

---

## ⚙️ Configuration

### Business Categories

Edit `config/keywords.yaml` to customize:
- Business categories and keywords
- Nigerian cities and locations
- Phone number patterns
- Detection settings

### Scheduler Intervals

Edit `config/settings.yaml`:

```yaml
scheduler:
  facebook_interval_minutes: 30
  linkedin_interval_minutes: 45
  google_interval_minutes: 60
```

### Rate Limiting

```yaml
rate_limiting:
  facebook_rpm: 10
  linkedin_rpm: 5
  google_rpm: 10
  request_delay_min: 2
  request_delay_max: 5
```

---

## 📊 Dashboard Features

- **Real-time Statistics**: Total businesses, recent discoveries, platform breakdown
- **Filtering**: By platform, category, priority
- **Search**: Find specific businesses
- **Export**: Download data as CSV
- **Manual Triggers**: Run discovery on-demand

---

## 🔄 How It Works

### Discovery Process

1. **Scheduler** triggers discovery tasks at configured intervals
2. **Scrapers** search for new pages using:
   - Google search with site-specific operators
   - Facebook Graph API (where available)
   - LinkedIn public pages
3. **Data Processor** extracts business information
4. **Lead Scorer** assigns confidence scores and priorities
5. **Deduplication** checks if business already exists
6. **Database** stores new businesses
7. **Alert Manager** sends notifications
8. **Dashboard** displays results in real-time

### Google Search Operators (Dorks)

The system uses advanced search queries like:
```
site:facebook.com/pages "hotel" "Lagos" "Nigeria"
site:linkedin.com/company "startup" "Abuja" "Nigeria"
```

With time filters to find recently indexed pages.

---

## 📁 Project Structure

```
Automated System Alert/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── config/
│   ├── settings.yaml      # Main configuration
│   └── keywords.yaml      # Business categories & keywords
├── src/
│   ├── core/
│   │   ├── config_manager.py
│   │   ├── database.py
│   │   ├── logger.py
│   │   └── lead_scorer.py
│   ├── scrapers/
│   │   ├── facebook_scraper.py
│   │   ├── linkedin_scraper.py
│   │   └── google_scraper.py
│   ├── alerts/
│   │   └── alert_manager.py
│   ├── scheduler/
│   │   └── task_scheduler.py
│   └── dashboard/
│       ├── api.py
│       └── static/
│           ├── index.html
│           └── app.js
├── data/                  # SQLite database (auto-created)
├── logs/                  # Log files (auto-created)
└── exports/               # CSV exports (auto-created)
```

---

## 🚀 Deployment Options

### Local Machine (Windows/Mac/Linux)

```bash
python main.py
```

### VPS/Cloud Server

1. **Install Python 3.8+**
2. **Clone repository**
3. **Install dependencies**
4. **Configure settings**
5. **Run with systemd (Linux)** or **Task Scheduler (Windows)**

### Linux Systemd Service

Create `/etc/systemd/system/business-discovery.service`:

```ini
[Unit]
Description=Business Discovery System
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/Automated System Alert
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable business-discovery
sudo systemctl start business-discovery
```

---

## 🛡️ Ethical Considerations

This system uses **ethical OSINT methods**:

✅ **Public Data Only**: Only accesses publicly available information
✅ **Rate Limiting**: Respects API limits and adds delays
✅ **Terms of Service**: Uses official APIs where available
✅ **No Authentication Bypass**: Doesn't attempt to access private data
✅ **Robots.txt**: Respects website policies

---

## 🔧 Troubleshooting

### No businesses discovered

- Check API keys are configured correctly
- Verify internet connection
- Check logs in `logs/system.log`
- Try manual discovery: `python main.py discover`

### Rate limit errors

- Increase delay in `config/settings.yaml`
- Reduce scheduler frequency
- Use proxy rotation (advanced)

### Dashboard not loading

- Check port 8000 is not in use
- Verify firewall settings
- Check logs for errors

---

## 📈 Performance Tips

1. **Google Search is Most Effective**: Enable Google scraper for best results
2. **Adjust Intervals**: Balance between freshness and rate limits
3. **Use Batch Alerts**: Reduce notification fatigue
4. **Regular Exports**: Backup data periodically
5. **Monitor Logs**: Check for errors and optimize

---

## 🎯 Business Use Case

Perfect for:
- **Lead Generation**: Contact businesses immediately after launch
- **Market Research**: Track new competitors and trends
- **Sales Outreach**: Offer services (web dev, SEO, branding)
- **First-Mover Advantage**: Reach businesses before competitors

---

## 📝 License

This project is for educational and business purposes. Ensure compliance with platform terms of service.

---

## 🤝 Support

For issues or questions:
1. Check logs in `logs/system.log`
2. Review configuration files
3. Verify API keys and credentials

---

## 🎉 Happy Lead Hunting!

Start discovering new Nigerian businesses today! 🚀

# Business-Discovery-Dashboard-System-Software
