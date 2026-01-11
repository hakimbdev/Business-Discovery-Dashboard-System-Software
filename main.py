"""
Business Discovery System - Main Application
Automated system for discovering newly created Facebook Pages and LinkedIn Company Pages in Nigeria
"""

import sys
import signal
import uvicorn
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.config_manager import config
from src.core.logger import SystemLogger
from src.core.database import DatabaseHandler
from src.scheduler.task_scheduler import TaskScheduler
from src.dashboard.api import app
from src.core.logger import get_logger

# Initialize logging
log_config = config.get('logging', {})
SystemLogger(
    log_file=log_config.get('file', 'logs/system.log'),
    level=log_config.get('level', 'INFO'),
    max_size_mb=log_config.get('max_size_mb', 10),
    backup_count=log_config.get('backup_count', 5),
    console_output=log_config.get('console_output', True)
)

logger = get_logger(__name__)

# Global scheduler instance
scheduler = None


def start_system():
    """Start the complete system"""
    global scheduler
    
    logger.info("=" * 80)
    logger.info("BUSINESS DISCOVERY SYSTEM - STARTING")
    logger.info("=" * 80)
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        db = DatabaseHandler()
        logger.info("Database initialized successfully")
        
        # Initialize and start scheduler
        logger.info("Initializing task scheduler...")
        scheduler = TaskScheduler()
        scheduler.start()
        logger.info("Task scheduler started successfully")
        
        # Get dashboard configuration
        dashboard_config = config.get('dashboard', {})
        host = dashboard_config.get('host', '0.0.0.0')
        port = dashboard_config.get('port', 8000)
        debug = dashboard_config.get('debug', False)
        
        logger.info(f"Starting web dashboard on http://{host}:{port}")
        logger.info("=" * 80)
        logger.info("System is now running!")
        logger.info(f"Dashboard: http://localhost:{port}")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 80)
        
        # Start FastAPI server
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info" if debug else "warning"
        )
        
    except Exception as e:
        logger.error(f"Error starting system: {str(e)}", exc_info=True)
        sys.exit(1)


def stop_system(signum=None, frame=None):
    """Stop the system gracefully"""
    global scheduler
    
    logger.info("=" * 80)
    logger.info("BUSINESS DISCOVERY SYSTEM - STOPPING")
    logger.info("=" * 80)
    
    if scheduler:
        logger.info("Stopping task scheduler...")
        scheduler.stop()
        logger.info("Task scheduler stopped")
    
    logger.info("System stopped successfully")
    logger.info("=" * 80)
    sys.exit(0)


def run_manual_discovery():
    """Run manual discovery without starting the full system"""
    logger.info("Running manual discovery...")
    
    db = DatabaseHandler()
    
    # Run all scrapers
    from src.scrapers.facebook_scraper import FacebookScraper
    from src.scrapers.linkedin_scraper import LinkedInScraper
    from src.scrapers.google_scraper import GoogleScraper
    from src.alerts.alert_manager import AlertManager
    
    alert_manager = AlertManager()
    
    # Facebook
    if config.is_enabled('facebook'):
        logger.info("Running Facebook discovery...")
        fb_scraper = FacebookScraper(db)
        fb_results = fb_scraper.discover_new_pages()
        logger.info(f"Facebook: {len(fb_results)} new pages discovered")
        
        for business in fb_results:
            alert_manager.send_alert(business)
    
    # LinkedIn
    if config.is_enabled('linkedin'):
        logger.info("Running LinkedIn discovery...")
        li_scraper = LinkedInScraper(db)
        li_results = li_scraper.discover_new_companies()
        logger.info(f"LinkedIn: {len(li_results)} new companies discovered")
        
        for business in li_results:
            alert_manager.send_alert(business)
    
    # Google
    if config.is_enabled('google'):
        logger.info("Running Google discovery...")
        google_scraper = GoogleScraper(db)
        google_results = google_scraper.discover_new_pages()
        logger.info(f"Google: {len(google_results)} new pages discovered")
        
        for business in google_results:
            alert_manager.send_alert(business)
    
    logger.info("Manual discovery completed")


if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, stop_system)
    signal.signal(signal.SIGTERM, stop_system)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "discover":
            # Run manual discovery
            run_manual_discovery()
        elif sys.argv[1] == "help":
            print("Business Discovery System")
            print("\nUsage:")
            print("  python main.py          - Start the full system (scheduler + dashboard)")
            print("  python main.py discover - Run manual discovery once")
            print("  python main.py help     - Show this help message")
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Run 'python main.py help' for usage information")
    else:
        # Start the full system
        start_system()

