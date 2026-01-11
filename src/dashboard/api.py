"""
FastAPI Dashboard Backend
REST API for the web dashboard
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import secrets
from src.core.config_manager import config
from src.core.database import DatabaseHandler
from src.scheduler.task_scheduler import TaskScheduler
from src.core.logger import get_logger

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Business Discovery System",
    description="Automated system for discovering new Nigerian businesses on Facebook and LinkedIn",
    version="1.0.0"
)

# Mount static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic authentication
security = HTTPBasic()
db = DatabaseHandler()


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify basic authentication credentials"""
    if not config.get('dashboard.enable_auth', True):
        return True
    
    correct_username = config.get('dashboard.username', 'admin')
    correct_password = config.get('dashboard.password', 'changeme123')
    
    is_correct_username = secrets.compare_digest(credentials.username, correct_username)
    is_correct_password = secrets.compare_digest(credentials.password, correct_password)
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    
    return True


@app.get("/")
async def root():
    """Serve the dashboard HTML"""
    static_dir = Path(__file__).parent / "static"
    index_file = static_dir / "index.html"

    if index_file.exists():
        return FileResponse(str(index_file))

    return {
        "message": "Business Discovery System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/api/businesses")
async def get_businesses(
    limit: int = Query(50, ge=1, le=500),
    platform: Optional[str] = None,
    category: Optional[str] = None
):
    """Get list of discovered businesses with optional filters"""
    try:
        businesses = db.get_recent_businesses(
            limit=limit,
            platform=platform,
            category=category
        )
        return {
            "success": True,
            "count": len(businesses),
            "data": businesses
        }
    except Exception as e:
        logger.error(f"Error fetching businesses: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/statistics")
async def get_statistics():
    """Get system statistics"""
    try:
        stats = db.get_statistics()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/categories")
async def get_categories():
    """Get list of business categories"""
    try:
        categories = config.get_keywords()
        category_list = [
            {
                "name": name,
                "keywords": data.get('keywords', []),
                "priority": data.get('priority', 'medium')
            }
            for name, data in categories.items()
        ]
        return {
            "success": True,
            "data": category_list
        }
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/export/csv")
async def export_csv():
    """Export businesses to CSV"""
    try:
        import tempfile
        import os
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        temp_path = temp_file.name
        temp_file.close()
        
        # Export to CSV
        db.export_to_csv(temp_path)
        
        # Return file
        return FileResponse(
            temp_path,
            media_type='text/csv',
            filename=f'businesses_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    except Exception as e:
        logger.error(f"Error exporting CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/trigger/facebook")
async def trigger_facebook_discovery(authenticated: bool = Depends(verify_credentials)):
    """Manually trigger Facebook discovery"""
    try:
        from src.scrapers.facebook_scraper import FacebookScraper
        scraper = FacebookScraper(db)
        discovered = scraper.discover_new_pages()
        
        return {
            "success": True,
            "message": f"Facebook discovery completed",
            "discovered": len(discovered)
        }
    except Exception as e:
        logger.error(f"Error triggering Facebook discovery: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/trigger/linkedin")
async def trigger_linkedin_discovery(authenticated: bool = Depends(verify_credentials)):
    """Manually trigger LinkedIn discovery"""
    try:
        from src.scrapers.linkedin_scraper import LinkedInScraper
        scraper = LinkedInScraper(db)
        discovered = scraper.discover_new_companies()
        
        return {
            "success": True,
            "message": f"LinkedIn discovery completed",
            "discovered": len(discovered)
        }
    except Exception as e:
        logger.error(f"Error triggering LinkedIn discovery: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/trigger/google")
async def trigger_google_discovery(authenticated: bool = Depends(verify_credentials)):
    """Manually trigger Google discovery"""
    try:
        from src.scrapers.google_scraper import GoogleScraper
        scraper = GoogleScraper(db)
        discovered = scraper.discover_new_pages()
        
        return {
            "success": True,
            "message": f"Google discovery completed",
            "discovered": len(discovered)
        }
    except Exception as e:
        logger.error(f"Error triggering Google discovery: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

