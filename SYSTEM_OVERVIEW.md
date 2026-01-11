# 🎯 Business Discovery System - Complete Overview

## 📖 What Is This System?

An **automated OSINT (Open-Source Intelligence) system** that continuously monitors the internet for **newly created Facebook Pages and LinkedIn Company Pages** of Nigerian businesses in specific categories, then instantly alerts you so you can contact them before your competitors.

### 🎯 Business Value

**Problem:** New businesses are launching every day, but by the time you find them, competitors have already reached out.

**Solution:** This system discovers businesses within hours of their page creation and alerts you immediately.

**Result:** First-mover advantage = Higher conversion rates = More clients = More revenue 💰

---

## 🏗️ How It Works

### 1. **Discovery Phase** (Automated, runs every hour)

The system uses three methods simultaneously:

**Method A: Google Search (Most Effective)**
- Uses Google Custom Search API
- Searches with advanced operators (dorks)
- Example: `site:facebook.com/pages "hotel" "Lagos" "Nigeria"`
- Filters by time (last 7 days)
- Finds newly indexed pages

**Method B: Facebook Graph API**
- Uses official Facebook API
- Limited search capabilities
- Good for getting detailed page info
- Requires access token

**Method C: LinkedIn Public Pages**
- Ethical scraping of public data
- Integrated with Google search
- Extracts company information

### 2. **Processing Phase**

For each discovered page:

1. **Extract Information:**
   - Business name
   - Platform (Facebook/LinkedIn)
   - Category (startup, hotel, etc.)
   - Location (city, state)
   - Contact info (phone, email)
   - Description

2. **Score the Lead (0-100):**
   - Location signals (30 points): Nigerian cities, +234 phone
   - Category match (25 points): Keywords in description
   - Contact info (20 points): Has phone/email
   - Freshness (15 points): Recently created
   - Content quality (10 points): Complete profile

3. **Assign Priority:**
   - **High** (80+ score): Hot leads, immediate action
   - **Medium** (60-79): Good leads, follow up soon
   - **Low** (<60): Potential leads, review later

4. **Check for Duplicates:**
   - Hash-based deduplication
   - Prevents duplicate alerts
   - Tracks in database

### 3. **Alert Phase** (Instant or Batched)

When a new business is discovered:

**Instant Mode:**
- Email alert with business details
- Telegram message to your phone
- Desktop notification
- Sent within minutes of discovery

**Batch Mode:**
- Daily summary report
- All discoveries in one email
- Reduces notification fatigue

### 4. **Storage & Access**

All discoveries are stored in SQLite database:
- Permanent record
- Searchable via dashboard
- Exportable to CSV
- API access available

---

## 📊 System Components

### Core Modules

1. **Config Manager** (`src/core/config_manager.py`)
   - Loads settings from YAML files
   - Manages API keys
   - Provides configuration access

2. **Database Handler** (`src/core/database.py`)
   - SQLite database operations
   - Deduplication logic
   - Statistics and exports

3. **Lead Scorer** (`src/core/lead_scorer.py`)
   - Calculates confidence scores
   - Assigns priorities
   - Validates location signals

4. **Logger** (`src/core/logger.py`)
   - Centralized logging
   - Rotating log files
   - Console and file output

### Scraper Modules

1. **Facebook Scraper** (`src/scrapers/facebook_scraper.py`)
   - Graph API integration
   - Page detail extraction
   - Rate limiting

2. **LinkedIn Scraper** (`src/scrapers/linkedin_scraper.py`)
   - Public page scraping
   - Company info extraction
   - Ethical methods only

3. **Google Scraper** (`src/scrapers/google_scraper.py`)
   - Custom Search API
   - Advanced search operators
   - Time-based filtering

### Alert Module

**Alert Manager** (`src/alerts/alert_manager.py`)
- Multi-channel alerts
- Email (SMTP)
- Telegram Bot API
- Desktop notifications
- HTML email templates

### Scheduler Module

**Task Scheduler** (`src/scheduler/task_scheduler.py`)
- APScheduler integration
- Configurable intervals
- Background tasks
- Job management

### Dashboard Module

**FastAPI Backend** (`src/dashboard/api.py`)
- REST API endpoints
- Authentication
- Real-time data
- Manual triggers

**Web Interface** (`src/dashboard/static/`)
- Modern responsive UI
- Real-time updates
- Filtering and search
- CSV export

---

## 🔄 Data Flow

```
1. SCHEDULER triggers discovery task
   ↓
2. SCRAPERS search for new pages
   ↓
3. DATA PROCESSOR extracts information
   ↓
4. LEAD SCORER calculates confidence
   ↓
5. DEDUPLICATION checks if new
   ↓
6. DATABASE stores business
   ↓
7. ALERT MANAGER sends notifications
   ↓
8. DASHBOARD displays results
```

---

## 📁 File Structure Explained

```
Automated System Alert/
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
│
├── config/                    # Configuration files
│   ├── settings.yaml         # Main settings (API keys, intervals)
│   └── keywords.yaml         # Business categories & keywords
│
├── src/                      # Source code
│   ├── core/                 # Core functionality
│   ├── scrapers/             # Discovery modules
│   ├── alerts/               # Alert system
│   ├── scheduler/            # Task automation
│   └── dashboard/            # Web interface
│
├── scripts/                  # Utility scripts
│   ├── test_config.py       # Test configuration
│   └── view_database.py     # View database contents
│
├── data/                     # Database (auto-created)
│   └── businesses.db        # SQLite database
│
├── logs/                     # Log files (auto-created)
│   └── system.log           # Application logs
│
├── exports/                  # CSV exports (auto-created)
│
└── Documentation/
    ├── README.md            # Main documentation
    ├── QUICK_START.md       # 5-minute setup
    ├── SETUP_GUIDE.md       # Detailed setup
    ├── API_DOCUMENTATION.md # API reference
    └── SYSTEM_OVERVIEW.md   # This file
```

---

## ⚙️ Configuration Files

### `config/settings.yaml`

**Purpose:** Main system configuration

**Contains:**
- API keys (Facebook, Google, Telegram, Email)
- Scheduler intervals
- Rate limiting settings
- Alert preferences
- Dashboard settings

**When to edit:**
- Adding API keys
- Changing discovery frequency
- Enabling/disabling features
- Adjusting rate limits

### `config/keywords.yaml`

**Purpose:** Business categories and search terms

**Contains:**
- Business categories (startups, hotels, etc.)
- Keywords for each category
- Nigerian cities and locations
- Phone number patterns
- Detection settings

**When to edit:**
- Adding new business categories
- Customizing keywords
- Adding more cities
- Adjusting confidence thresholds

---

## 🔐 Security & Privacy

### What Data Is Collected?

**Only public information:**
- Business names
- Page URLs
- Public descriptions
- Publicly listed contact info
- Location (if public)

**NOT collected:**
- Private messages
- Personal data
- Non-public information
- User profiles

### Ethical Considerations

✅ **Uses official APIs** where available  
✅ **Respects rate limits** to avoid bans  
✅ **Public data only** - no authentication bypass  
✅ **Robots.txt compliant**  
✅ **No spam** - alerts are for your use only  

### API Key Security

- Store in `config/settings.yaml` (not in code)
- Add to `.gitignore` (don't commit to Git)
- Use environment variables for production
- Rotate keys periodically

---

## 📈 Performance & Scalability

### Current Capacity

- **Discoveries:** 100-500 businesses/day (depends on API limits)
- **Database:** Handles 100,000+ records easily
- **Dashboard:** Real-time for <10,000 records
- **Alerts:** Instant delivery

### Bottlenecks

1. **Google API Quota:** 100 searches/day (free tier)
   - Solution: Upgrade to paid tier or use multiple keys

2. **Rate Limits:** Platform-specific limits
   - Solution: Adjust intervals, use proxies

3. **Database Size:** SQLite performance degrades >1M records
   - Solution: Switch to PostgreSQL

### Optimization Tips

1. **Reduce Discovery Frequency:** Run every 2-4 hours instead of hourly
2. **Focus on High-Priority Categories:** Disable low-value categories
3. **Use Batch Alerts:** Reduce notification overhead
4. **Regular Database Cleanup:** Archive old records
5. **Monitor Logs:** Identify and fix errors quickly

---

## 🚀 Deployment Scenarios

### Scenario 1: Local Development (Your Computer)

**Best for:** Testing, small-scale use  
**Setup time:** 5 minutes  
**Cost:** Free  

```bash
python main.py
```

### Scenario 2: VPS/Cloud Server (24/7 Operation)

**Best for:** Production, continuous monitoring  
**Setup time:** 30 minutes  
**Cost:** $5-20/month  

**Recommended providers:**
- DigitalOcean ($5/month)
- Linode ($5/month)
- AWS EC2 (free tier)
- Google Cloud (free tier)

### Scenario 3: Docker Container

**Best for:** Easy deployment, portability  
**Setup time:** 15 minutes  
**Cost:** Depends on hosting  

(Docker support can be added if needed)

---

## 🎯 Use Cases & ROI

### Use Case 1: Web Development Agency

**Target:** New startups and businesses  
**Action:** Offer website development  
**ROI:** 1 client/week × $2,000 = $8,000/month  

### Use Case 2: SEO/Marketing Agency

**Target:** New hotels and restaurants  
**Action:** Offer SEO and social media management  
**ROI:** 2 clients/week × $500/month = $4,000/month  

### Use Case 3: Business Consultant

**Target:** New real estate companies  
**Action:** Offer branding and strategy  
**ROI:** 1 client/month × $5,000 = $5,000/month  

### Use Case 4: Market Research

**Target:** All categories  
**Action:** Track market trends and competitors  
**ROI:** Informed business decisions = Priceless  

---

## 🔧 Maintenance

### Daily Tasks

- Check dashboard for new discoveries
- Review alerts
- Contact high-priority leads

### Weekly Tasks

- Review logs for errors
- Export data to CSV (backup)
- Check API quota usage

### Monthly Tasks

- Update keywords if needed
- Review and optimize settings
- Clean up old database records
- Update dependencies

---

## 📞 Support & Resources

### Documentation

- `README.md` - Main documentation
- `QUICK_START.md` - Fast setup guide
- `SETUP_GUIDE.md` - Detailed instructions
- `API_DOCUMENTATION.md` - API reference

### Troubleshooting

1. Check `logs/system.log`
2. Run `python scripts/test_config.py`
3. Review configuration files
4. Verify API keys and quotas

### Community

- Share your success stories
- Contribute improvements
- Report bugs and issues

---

## 🎉 Success Tips

1. **Start Simple:** Use default settings first
2. **Test Thoroughly:** Run manual discovery before automation
3. **Monitor Closely:** Check logs and results daily
4. **Act Fast:** Contact businesses within 24 hours
5. **Track Results:** Measure conversion rates
6. **Optimize:** Adjust based on what works
7. **Scale Up:** Add more categories as you grow

---

## 🚀 Next Steps

1. ✅ Complete setup (see QUICK_START.md)
2. ✅ Configure API keys
3. ✅ Run test discovery
4. ✅ Start automated system
5. ✅ Monitor dashboard
6. ✅ Contact first lead
7. ✅ Close first deal! 💰

---

**You now have a complete understanding of the system. Time to start discovering and closing deals!** 🎯

