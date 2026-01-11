"""
Task Scheduler
Manages automated discovery tasks using APScheduler
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from typing import List, Dict, Any
from src.core.config_manager import config
from src.core.database import DatabaseHandler
from src.core.logger import get_logger
from src.scrapers.facebook_scraper import FacebookScraper
from src.scrapers.linkedin_scraper import LinkedInScraper
from src.scrapers.google_scraper import GoogleScraper
from src.alerts.alert_manager import AlertManager

logger = get_logger(__name__)


class TaskScheduler:
    """Manage automated discovery tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.db = DatabaseHandler()
        self.alert_manager = AlertManager()
        
        # Initialize scrapers
        self.facebook_scraper = FacebookScraper(self.db)
        self.linkedin_scraper = LinkedInScraper(self.db)
        self.google_scraper = GoogleScraper(self.db)
        
        # Load configuration
        self.facebook_enabled = config.is_enabled('facebook')
        self.linkedin_enabled = config.is_enabled('linkedin')
        self.google_enabled = config.is_enabled('google')
        
        self.facebook_interval = config.get('scheduler.facebook_interval_minutes', 30)
        self.linkedin_interval = config.get('scheduler.linkedin_interval_minutes', 45)
        self.google_interval = config.get('scheduler.google_interval_minutes', 60)
        
        self.batch_mode = config.get('alerts.batch_mode', False)
        self.batch_interval = config.get('alerts.batch_interval_hours', 4)
        
        logger.info("Task Scheduler initialized")
    
    def start(self):
        """Start the scheduler and all enabled tasks"""
        logger.info("Starting task scheduler...")
        
        # Schedule Facebook discovery
        if self.facebook_enabled:
            self.scheduler.add_job(
                func=self.run_facebook_discovery,
                trigger=IntervalTrigger(minutes=self.facebook_interval),
                id='facebook_discovery',
                name='Facebook Page Discovery',
                replace_existing=True
            )
            logger.info(f"Facebook discovery scheduled every {self.facebook_interval} minutes")
        
        # Schedule LinkedIn discovery
        if self.linkedin_enabled:
            self.scheduler.add_job(
                func=self.run_linkedin_discovery,
                trigger=IntervalTrigger(minutes=self.linkedin_interval),
                id='linkedin_discovery',
                name='LinkedIn Company Discovery',
                replace_existing=True
            )
            logger.info(f"LinkedIn discovery scheduled every {self.linkedin_interval} minutes")
        
        # Schedule Google discovery
        if self.google_enabled:
            self.scheduler.add_job(
                func=self.run_google_discovery,
                trigger=IntervalTrigger(minutes=self.google_interval),
                id='google_discovery',
                name='Google Search Discovery',
                replace_existing=True
            )
            logger.info(f"Google discovery scheduled every {self.google_interval} minutes")
        
        # Schedule alert processing
        if self.batch_mode:
            # Batch alerts
            self.scheduler.add_job(
                func=self.process_batch_alerts,
                trigger=IntervalTrigger(hours=self.batch_interval),
                id='batch_alerts',
                name='Batch Alert Processing',
                replace_existing=True
            )
            logger.info(f"Batch alerts scheduled every {self.batch_interval} hours")
        else:
            # Instant alerts
            self.scheduler.add_job(
                func=self.process_instant_alerts,
                trigger=IntervalTrigger(minutes=5),
                id='instant_alerts',
                name='Instant Alert Processing',
                replace_existing=True
            )
            logger.info("Instant alerts scheduled every 5 minutes")
        
        # Start the scheduler
        self.scheduler.start()
        logger.info("Task scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler"""
        logger.info("Stopping task scheduler...")
        self.scheduler.shutdown()
        logger.info("Task scheduler stopped")
    
    def run_facebook_discovery(self):
        """Run Facebook page discovery"""
        try:
            logger.info("Running Facebook discovery task...")
            discovered = self.facebook_scraper.discover_new_pages()
            logger.info(f"Facebook discovery completed: {len(discovered)} new pages found")
        except Exception as e:
            logger.error(f"Error in Facebook discovery task: {str(e)}")
    
    def run_linkedin_discovery(self):
        """Run LinkedIn company discovery"""
        try:
            logger.info("Running LinkedIn discovery task...")
            discovered = self.linkedin_scraper.discover_new_companies()
            logger.info(f"LinkedIn discovery completed: {len(discovered)} new companies found")
        except Exception as e:
            logger.error(f"Error in LinkedIn discovery task: {str(e)}")
    
    def run_google_discovery(self):
        """Run Google search discovery"""
        try:
            logger.info("Running Google discovery task...")
            discovered = self.google_scraper.discover_new_pages()
            logger.info(f"Google discovery completed: {len(discovered)} new pages found")
        except Exception as e:
            logger.error(f"Error in Google discovery task: {str(e)}")
    
    def process_instant_alerts(self):
        """Process and send instant alerts for new businesses"""
        try:
            # Get unalereted businesses
            businesses = self.db.get_unalereted_businesses()
            
            if not businesses:
                return
            
            logger.info(f"Processing {len(businesses)} unalereted businesses")
            
            for business in businesses:
                # Send alert
                self.alert_manager.send_alert(business)
                
                # Mark as alerted
                self.db.mark_as_alerted(business['id'])
            
            logger.info(f"Instant alerts sent for {len(businesses)} businesses")
            
        except Exception as e:
            logger.error(f"Error processing instant alerts: {str(e)}")
    
    def process_batch_alerts(self):
        """Process and send batch alerts"""
        try:
            # Get unalereted businesses
            businesses = self.db.get_unalereted_businesses()
            
            if not businesses:
                logger.info("No new businesses to alert")
                return
            
            logger.info(f"Processing batch alert for {len(businesses)} businesses")
            
            # Send batch alert
            self.alert_manager.send_batch_alert(businesses)
            
            # Mark all as alerted
            for business in businesses:
                self.db.mark_as_alerted(business['id'])
            
            logger.info(f"Batch alert sent for {len(businesses)} businesses")
            
        except Exception as e:
            logger.error(f"Error processing batch alerts: {str(e)}")
    
    def get_job_status(self) -> List[Dict[str, Any]]:
        """Get status of all scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None
            })
        return jobs

