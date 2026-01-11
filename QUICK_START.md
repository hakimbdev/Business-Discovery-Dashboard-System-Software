# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## 🚀 Installation (2 minutes)

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Test configuration
python scripts/test_config.py
```

---

## 🔑 Minimum Configuration (2 minutes)

**For the system to work, you MUST configure Google Custom Search API:**

### Get Google API Key (FREE - 100 searches/day)

1. **Create Google Cloud Project:**
   - Go to https://console.cloud.google.com/
   - Create new project
   - Enable "Custom Search API"

2. **Get API Key:**
   - Go to "Credentials" → "Create Credentials" → "API Key"
   - Copy the key

3. **Create Search Engine:**
   - Go to https://programmablesearchengine.google.com/
   - Click "Add" → Create new search engine
   - Leave "Sites to search" empty (search entire web)
   - Copy the "Search engine ID"

4. **Add to Configuration:**
   
   Edit `config/settings.yaml`:
   ```yaml
   api_keys:
     google:
       api_key: "YOUR_GOOGLE_API_KEY_HERE"
       search_engine_id: "YOUR_SEARCH_ENGINE_ID_HERE"
   ```

---

## ✅ Verify Setup (30 seconds)

```bash
# Test configuration
python scripts/test_config.py

# Should show:
# ✅ Google API key configured
# ✅ Google search engine ID configured
```

---

## 🎯 Run Your First Discovery (30 seconds)

```bash
# Run manual discovery
python main.py discover
```

This will:
- Search for new Nigerian businesses
- Score and filter results
- Save to database
- Show results in console

---

## 📊 View Results (30 seconds)

```bash
# View discovered businesses
python scripts/view_database.py
```

---

## 🌐 Start Full System (30 seconds)

```bash
# Start automated system + dashboard
python main.py
```

Then open: **http://localhost:8000**

Default login:
- Username: `admin`
- Password: `changeme123`

---

## 🎉 That's It!

You now have a working business discovery system!

### What's Running:

✅ **Automated Discovery** - Searches every hour for new businesses  
✅ **Web Dashboard** - View and filter discovered businesses  
✅ **Database** - Stores all discoveries with deduplication  

---

## 📈 Next Steps (Optional)

### 1. Add Telegram Alerts (5 minutes)

Get instant notifications on your phone!

1. Open Telegram, search `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy bot token
4. Start chat with your bot
5. Get chat ID from: `https://api.telegram.org/bot<TOKEN>/getUpdates`

Add to `config/settings.yaml`:
```yaml
api_keys:
  telegram:
    bot_token: "YOUR_BOT_TOKEN"
    chat_id: "YOUR_CHAT_ID"

alerts:
  enable_telegram: true
```

### 2. Add Email Alerts (5 minutes)

1. Enable 2FA on Gmail
2. Generate app password: https://myaccount.google.com/apppasswords
3. Add to config:

```yaml
api_keys:
  email:
    sender_email: "your_email@gmail.com"
    sender_password: "your_app_password"
    recipient_email: "recipient@example.com"

alerts:
  enable_email: true
```

### 3. Customize Keywords

Edit `config/keywords.yaml` to add your specific business types and locations.

### 4. Adjust Discovery Frequency

Edit `config/settings.yaml`:
```yaml
scheduler:
  google_interval_minutes: 60  # Run every hour
```

---

## 🆘 Troubleshooting

**No businesses found?**
- Make sure Google API key is configured
- Check you have API quota remaining (100/day free)
- Try: `python main.py discover` to test manually

**Dashboard not loading?**
- Check port 8000 is not in use
- Try changing port in `config/settings.yaml`

**Errors in console?**
- Check `logs/system.log` for details
- Run `python scripts/test_config.py`

---

## 📚 Learn More

- **Full Setup Guide:** See `SETUP_GUIDE.md`
- **Complete Documentation:** See `README.md`
- **View Logs:** `tail -f logs/system.log`
- **View Database:** `python scripts/view_database.py`

---

## 💡 Pro Tips

1. **Start Small:** Use default settings first, then customize
2. **Monitor Logs:** Check `logs/system.log` regularly
3. **Export Data:** Use dashboard to export CSV regularly
4. **Rate Limits:** Google free tier = 100 searches/day (enough for testing)
5. **Best Results:** Google search is most effective for discovery

---

## 🎯 Your First Lead!

When the system discovers a business, you'll see:

**In Dashboard:**
- Business name, platform, category
- Confidence score
- Contact information
- Direct link to page

**In Alerts (if configured):**
- Instant Telegram message
- Email notification
- Desktop popup

**Next Action:**
- Visit the business page
- Contact them with your services
- Close the deal! 💰

---

## 🚀 Happy Lead Hunting!

You're now ready to discover and contact new Nigerian businesses before your competitors!

**Questions?** Check the logs or review the full documentation.

