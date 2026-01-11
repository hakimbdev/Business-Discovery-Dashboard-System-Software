# ✅ Setup Checklist

Use this checklist to ensure your Business Discovery System is properly configured and ready to use.

---

## 📋 Pre-Installation

- [ ] Python 3.8 or higher installed
- [ ] `pip` package manager available
- [ ] Internet connection active
- [ ] Text editor ready (VS Code, Notepad++, etc.)

**Verify Python:**
```bash
python --version
# Should show: Python 3.8.x or higher
```

---

## 📦 Installation

- [ ] Navigate to project directory
- [ ] Create virtual environment (recommended)
  ```bash
  python -m venv venv
  ```
- [ ] Activate virtual environment
  ```bash
  # Windows:
  venv\Scripts\activate
  # Mac/Linux:
  source venv/bin/activate
  ```
- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Verify installation
  ```bash
  python scripts/test_config.py
  ```

---

## 🔑 API Configuration

### Google Custom Search API (REQUIRED)

- [ ] Create Google Cloud account
- [ ] Create new project
- [ ] Enable Custom Search API
- [ ] Create API key
- [ ] Create Custom Search Engine
- [ ] Get Search Engine ID
- [ ] Add to `config/settings.yaml`:
  ```yaml
  api_keys:
    google:
      api_key: "YOUR_API_KEY_HERE"
      search_engine_id: "YOUR_SEARCH_ENGINE_ID_HERE"
  ```

**Test:**
```bash
python scripts/test_config.py
# Should show: ✅ Google API key configured
```

---

### Facebook Graph API (OPTIONAL)

- [ ] Create Facebook Developer account
- [ ] Create new app
- [ ] Get App ID and App Secret
- [ ] Generate access token
- [ ] Add to `config/settings.yaml`:
  ```yaml
  api_keys:
    facebook:
      app_id: "YOUR_APP_ID"
      app_secret: "YOUR_APP_SECRET"
      access_token: "YOUR_ACCESS_TOKEN"
  ```

---

### Telegram Bot (OPTIONAL - Recommended for Alerts)

- [ ] Open Telegram
- [ ] Search for `@BotFather`
- [ ] Send `/newbot` command
- [ ] Follow instructions
- [ ] Copy bot token
- [ ] Start chat with your bot
- [ ] Get chat ID from: `https://api.telegram.org/bot<TOKEN>/getUpdates`
- [ ] Add to `config/settings.yaml`:
  ```yaml
  api_keys:
    telegram:
      bot_token: "YOUR_BOT_TOKEN"
      chat_id: "YOUR_CHAT_ID"
  ```

---

### Email Alerts (OPTIONAL)

- [ ] Enable 2-Factor Authentication on Gmail
- [ ] Generate app password: https://myaccount.google.com/apppasswords
- [ ] Add to `config/settings.yaml`:
  ```yaml
  api_keys:
    email:
      smtp_server: "smtp.gmail.com"
      smtp_port: 587
      sender_email: "your_email@gmail.com"
      sender_password: "your_app_password"
      recipient_email: "recipient@example.com"
  ```

---

## ⚙️ System Configuration

### Keywords & Categories

- [ ] Review `config/keywords.yaml`
- [ ] Add/remove business categories as needed
- [ ] Customize keywords for your target market
- [ ] Add specific cities if needed
- [ ] Adjust confidence thresholds if needed

### Scheduler Settings

- [ ] Review `config/settings.yaml` scheduler section
- [ ] Set discovery intervals:
  ```yaml
  scheduler:
    facebook_interval_minutes: 30
    linkedin_interval_minutes: 45
    google_interval_minutes: 60
  ```
- [ ] Enable/disable scrapers:
  ```yaml
  scheduler:
    enable_facebook: true
    enable_linkedin: true
    enable_google: true
  ```

### Alert Settings

- [ ] Configure alert mode:
  ```yaml
  alerts:
    batch_mode: false  # false = instant, true = daily summary
    enable_email: true
    enable_telegram: true
    enable_desktop: true
  ```

### Dashboard Settings

- [ ] Change default password:
  ```yaml
  dashboard:
    username: "your_username"
    password: "your_secure_password"
    port: 8000
  ```

---

## 🧪 Testing

### Configuration Test

- [ ] Run configuration test:
  ```bash
  python scripts/test_config.py
  ```
- [ ] Verify all required settings show ✅
- [ ] Fix any ❌ errors shown

### Manual Discovery Test

- [ ] Run manual discovery:
  ```bash
  python main.py discover
  ```
- [ ] Check console output for discovered businesses
- [ ] Verify no errors in output
- [ ] Check `logs/system.log` for details

### Database Test

- [ ] View database contents:
  ```bash
  python scripts/view_database.py
  ```
- [ ] Verify businesses were saved
- [ ] Check statistics are displayed

### Alert Test (if configured)

- [ ] Check email inbox for test alert
- [ ] Check Telegram for test message
- [ ] Check desktop for notification

---

## 🚀 Deployment

### Local Deployment

- [ ] Start the system:
  ```bash
  python main.py
  ```
- [ ] Verify console shows:
  - "Scheduler started"
  - "Dashboard running on http://localhost:8000"
- [ ] Open browser to http://localhost:8000
- [ ] Login with configured credentials
- [ ] Verify dashboard loads correctly

### Dashboard Verification

- [ ] Dashboard loads without errors
- [ ] Statistics are displayed
- [ ] Business list is visible
- [ ] Filters work correctly
- [ ] Export to CSV works
- [ ] Manual trigger buttons work

---

## 📊 Monitoring

### First Hour

- [ ] Check logs every 15 minutes:
  ```bash
  tail -f logs/system.log
  ```
- [ ] Verify scheduled tasks are running
- [ ] Check for any errors
- [ ] Monitor discovery results

### First Day

- [ ] Review total discoveries
- [ ] Check alert delivery
- [ ] Verify database growth
- [ ] Test CSV export
- [ ] Review log files

### First Week

- [ ] Analyze discovery patterns
- [ ] Optimize keywords if needed
- [ ] Adjust intervals if needed
- [ ] Review and contact leads
- [ ] Export weekly report

---

## 🔧 Optimization

### Performance

- [ ] Monitor API quota usage
- [ ] Check database size
- [ ] Review log file size
- [ ] Optimize discovery intervals
- [ ] Adjust rate limits if needed

### Quality

- [ ] Review confidence scores
- [ ] Adjust scoring thresholds
- [ ] Refine keywords
- [ ] Add/remove categories
- [ ] Filter out false positives

---

## 📈 Production Readiness

### Security

- [ ] Change default dashboard password
- [ ] Secure API keys (not in Git)
- [ ] Review `.gitignore` file
- [ ] Use environment variables for production
- [ ] Enable HTTPS for dashboard (if public)

### Backup

- [ ] Set up database backup schedule
- [ ] Export data regularly
- [ ] Keep configuration backups
- [ ] Document custom settings

### Maintenance

- [ ] Schedule weekly log review
- [ ] Plan monthly keyword updates
- [ ] Set up monitoring alerts
- [ ] Document any customizations

---

## 🎯 First Actions

### Immediate (Day 1)

- [ ] Run first discovery
- [ ] Review first results
- [ ] Test alert system
- [ ] Familiarize with dashboard

### Short-term (Week 1)

- [ ] Contact first 5 leads
- [ ] Track conversion rates
- [ ] Optimize keywords
- [ ] Adjust settings based on results

### Long-term (Month 1)

- [ ] Analyze ROI
- [ ] Scale up if successful
- [ ] Add more categories
- [ ] Automate follow-up process

---

## ✅ Final Verification

Before considering setup complete, verify:

- [ ] ✅ System runs without errors
- [ ] ✅ Discoveries are being made
- [ ] ✅ Database is being populated
- [ ] ✅ Alerts are being sent
- [ ] ✅ Dashboard is accessible
- [ ] ✅ Logs are being created
- [ ] ✅ Export functionality works
- [ ] ✅ Manual triggers work

---

## 🎉 You're Ready!

If all items above are checked, your system is fully operational and ready to discover businesses!

### Next Steps:

1. **Monitor**: Check dashboard daily
2. **Act**: Contact discovered businesses
3. **Optimize**: Refine based on results
4. **Scale**: Add more categories as you grow
5. **Profit**: Close deals! 💰

---

## 🆘 Troubleshooting

If you encounter issues:

1. Check `logs/system.log` for errors
2. Run `python scripts/test_config.py`
3. Review configuration files
4. Verify API keys and quotas
5. Check internet connection
6. Restart the system

**Common Issues:**

- **No discoveries**: Check Google API key and quota
- **Dashboard not loading**: Check port 8000 is free
- **Alerts not working**: Verify API keys for email/Telegram
- **Database errors**: Check file permissions in `data/` folder

---

## 📚 Documentation Reference

- **Quick Start**: `QUICK_START.md`
- **Detailed Setup**: `SETUP_GUIDE.md`
- **System Overview**: `SYSTEM_OVERVIEW.md`
- **API Reference**: `API_DOCUMENTATION.md`
- **Project Summary**: `PROJECT_SUMMARY.md`

---

**Happy Lead Hunting! 🚀**

