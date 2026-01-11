"""
Database Handler
Manages SQLite/PostgreSQL database operations for storing discovered businesses
"""

import sqlite3
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import json


class DatabaseHandler:
    """Handle all database operations"""
    
    def __init__(self, db_path: str = "data/businesses.db"):
        self.db_path = db_path
        self._ensure_directory()
        self._init_database()
    
    def _ensure_directory(self):
        """Ensure database directory exists"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Main businesses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS businesses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    business_name TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    page_url TEXT NOT NULL UNIQUE,
                    category TEXT,
                    location TEXT,
                    phone TEXT,
                    email TEXT,
                    description TEXT,
                    confidence_score INTEGER,
                    priority TEXT,
                    page_created_date TEXT,
                    discovered_date TEXT NOT NULL,
                    last_updated TEXT,
                    hash TEXT UNIQUE NOT NULL,
                    metadata TEXT,
                    alerted BOOLEAN DEFAULT 0,
                    exported BOOLEAN DEFAULT 0
                )
            """)
            
            # Search history table (for tracking what we've searched)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    platform TEXT NOT NULL,
                    query TEXT NOT NULL,
                    search_date TEXT NOT NULL,
                    results_count INTEGER
                )
            """)
            
            # Create indexes for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_platform 
                ON businesses(platform)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_category 
                ON businesses(category)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_discovered_date 
                ON businesses(discovered_date)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_hash 
                ON businesses(hash)
            """)
            
            conn.commit()
    
    def generate_hash(self, page_url: str) -> str:
        """Generate unique hash for a business page"""
        return hashlib.md5(page_url.lower().encode()).hexdigest()
    
    def business_exists(self, page_url: str) -> bool:
        """Check if business already exists in database"""
        hash_value = self.generate_hash(page_url)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM businesses WHERE hash = ?",
                (hash_value,)
            )
            count = cursor.fetchone()[0]
            return count > 0
    
    def add_business(self, business_data: Dict[str, Any]) -> bool:
        """
        Add a new business to the database
        Returns True if added, False if duplicate
        """
        page_url = business_data.get('page_url')
        
        if self.business_exists(page_url):
            return False
        
        hash_value = self.generate_hash(page_url)
        now = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO businesses (
                    business_name, platform, page_url, category, location,
                    phone, email, description, confidence_score, priority,
                    page_created_date, discovered_date, last_updated, hash, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                business_data.get('business_name'),
                business_data.get('platform'),
                page_url,
                business_data.get('category'),
                business_data.get('location'),
                business_data.get('phone'),
                business_data.get('email'),
                business_data.get('description'),
                business_data.get('confidence_score', 0),
                business_data.get('priority', 'medium'),
                business_data.get('page_created_date'),
                now,
                now,
                hash_value,
                json.dumps(business_data.get('metadata', {}))
            ))
            
            conn.commit()
            return True

    def get_recent_businesses(self, limit: int = 50, platform: str = None,
                             category: str = None) -> List[Dict[str, Any]]:
        """Get recently discovered businesses with optional filters"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM businesses WHERE 1=1"
            params = []

            if platform:
                query += " AND platform = ?"
                params.append(platform)

            if category:
                query += " AND category = ?"
                params.append(category)

            query += " ORDER BY discovered_date DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

    def get_unalereted_businesses(self) -> List[Dict[str, Any]]:
        """Get businesses that haven't been alerted yet"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM businesses
                WHERE alerted = 0
                ORDER BY confidence_score DESC, discovered_date DESC
            """)

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def mark_as_alerted(self, business_id: int):
        """Mark a business as alerted"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE businesses SET alerted = 1 WHERE id = ?",
                (business_id,)
            )
            conn.commit()

    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total businesses
            cursor.execute("SELECT COUNT(*) FROM businesses")
            total = cursor.fetchone()[0]

            # By platform
            cursor.execute("""
                SELECT platform, COUNT(*) as count
                FROM businesses
                GROUP BY platform
            """)
            by_platform = dict(cursor.fetchall())

            # By category
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM businesses
                GROUP BY category
            """)
            by_category = dict(cursor.fetchall())

            # Recent (last 24 hours)
            cursor.execute("""
                SELECT COUNT(*) FROM businesses
                WHERE datetime(discovered_date) > datetime('now', '-1 day')
            """)
            recent_24h = cursor.fetchone()[0]

            return {
                'total': total,
                'by_platform': by_platform,
                'by_category': by_category,
                'recent_24h': recent_24h
            }

    def add_search_history(self, platform: str, query: str, results_count: int):
        """Log search history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO search_history (platform, query, search_date, results_count)
                VALUES (?, ?, ?, ?)
            """, (platform, query, datetime.now().isoformat(), results_count))
            conn.commit()

    def export_to_csv(self, output_path: str, filters: Dict[str, Any] = None):
        """Export businesses to CSV"""
        import csv

        businesses = self.get_recent_businesses(limit=10000)

        if not businesses:
            return

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=businesses[0].keys())
            writer.writeheader()
            writer.writerows(businesses)

