"""
Configuration Test Script
Tests if all API keys and configurations are properly set up
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.config_manager import config
from src.core.logger import get_logger

logger = get_logger(__name__)


def test_configuration():
    """Test all configuration settings"""
    print("=" * 80)
    print("CONFIGURATION TEST")
    print("=" * 80)
    
    issues = []
    warnings = []
    
    # Test Facebook configuration
    print("\n📘 Facebook Configuration:")
    fb_token = config.get_api_key('facebook', 'access_token')
    if fb_token and fb_token != 'YOUR_FACEBOOK_ACCESS_TOKEN':
        print("  ✅ Access token configured")
    else:
        warnings.append("Facebook access token not configured (optional)")
        print("  ⚠️  Access token not configured (optional)")
    
    # Test Google configuration
    print("\n🔍 Google Configuration:")
    google_key = config.get_api_key('google', 'api_key')
    google_cx = config.get_api_key('google', 'search_engine_id')
    
    if google_key and google_key != 'YOUR_GOOGLE_API_KEY':
        print("  ✅ API key configured")
    else:
        issues.append("Google API key not configured (REQUIRED for best results)")
        print("  ❌ API key not configured")
    
    if google_cx and google_cx != 'YOUR_SEARCH_ENGINE_ID':
        print("  ✅ Search engine ID configured")
    else:
        issues.append("Google search engine ID not configured (REQUIRED)")
        print("  ❌ Search engine ID not configured")
    
    # Test Telegram configuration
    print("\n💬 Telegram Configuration:")
    tg_token = config.get_api_key('telegram', 'bot_token')
    tg_chat = config.get_api_key('telegram', 'chat_id')
    
    if tg_token and tg_token != 'YOUR_TELEGRAM_BOT_TOKEN':
        print("  ✅ Bot token configured")
    else:
        warnings.append("Telegram bot token not configured (optional)")
        print("  ⚠️  Bot token not configured (optional)")
    
    if tg_chat and tg_chat != 'YOUR_TELEGRAM_CHAT_ID':
        print("  ✅ Chat ID configured")
    else:
        warnings.append("Telegram chat ID not configured (optional)")
        print("  ⚠️  Chat ID not configured (optional)")
    
    # Test Email configuration
    print("\n📧 Email Configuration:")
    email_sender = config.get_api_key('email', 'sender_email')
    email_password = config.get_api_key('email', 'sender_password')
    
    if email_sender and email_sender != 'your_email@gmail.com':
        print("  ✅ Sender email configured")
    else:
        warnings.append("Email sender not configured (optional)")
        print("  ⚠️  Sender email not configured (optional)")
    
    if email_password and email_password != 'your_app_password':
        print("  ✅ Email password configured")
    else:
        warnings.append("Email password not configured (optional)")
        print("  ⚠️  Email password not configured (optional)")
    
    # Test Scheduler configuration
    print("\n⏰ Scheduler Configuration:")
    fb_enabled = config.is_enabled('facebook')
    li_enabled = config.is_enabled('linkedin')
    google_enabled = config.is_enabled('google')
    
    print(f"  Facebook scraper: {'✅ Enabled' if fb_enabled else '❌ Disabled'}")
    print(f"  LinkedIn scraper: {'✅ Enabled' if li_enabled else '❌ Disabled'}")
    print(f"  Google scraper: {'✅ Enabled' if google_enabled else '❌ Disabled'}")
    
    if not any([fb_enabled, li_enabled, google_enabled]):
        issues.append("All scrapers are disabled!")
    
    # Test Database
    print("\n💾 Database Configuration:")
    try:
        from src.core.database import DatabaseHandler
        db = DatabaseHandler()
        print("  ✅ Database initialized successfully")
    except Exception as e:
        issues.append(f"Database initialization failed: {str(e)}")
        print(f"  ❌ Database initialization failed: {str(e)}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if not issues and not warnings:
        print("✅ All configurations are properly set up!")
        print("🚀 You're ready to start the system!")
        return True
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} Warning(s):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if issues:
        print(f"\n❌ {len(issues)} Issue(s) found:")
        for issue in issues:
            print(f"  - {issue}")
        print("\n⚠️  Please fix these issues before running the system.")
        print("📖 See SETUP_GUIDE.md for detailed instructions.")
        return False
    
    print("\n✅ Configuration is valid but some optional features are not configured.")
    print("🚀 You can start the system, but consider configuring optional features.")
    return True


if __name__ == "__main__":
    success = test_configuration()
    sys.exit(0 if success else 1)

