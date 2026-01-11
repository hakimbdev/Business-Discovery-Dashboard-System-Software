"""
Database Viewer Script
View and analyze discovered businesses in the database
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.database import DatabaseHandler


def view_database():
    """View database contents"""
    db = DatabaseHandler()
    
    print("=" * 80)
    print("DATABASE VIEWER")
    print("=" * 80)
    
    # Get statistics
    stats = db.get_statistics()
    
    print("\n📊 STATISTICS")
    print("-" * 80)
    print(f"Total Businesses: {stats['total']}")
    print(f"Discovered in Last 24h: {stats['recent_24h']}")
    
    print("\n📱 By Platform:")
    for platform, count in stats['by_platform'].items():
        print(f"  {platform}: {count}")
    
    print("\n🏢 By Category:")
    for category, count in stats['by_category'].items():
        print(f"  {category}: {count}")
    
    # Get recent businesses
    print("\n" + "=" * 80)
    print("RECENT BUSINESSES (Last 10)")
    print("=" * 80)
    
    businesses = db.get_recent_businesses(limit=10)
    
    if not businesses:
        print("\nNo businesses found in database.")
        print("Run 'python main.py discover' to start discovering businesses.")
        return
    
    for i, business in enumerate(businesses, 1):
        print(f"\n{i}. {business['business_name']}")
        print(f"   Platform: {business['platform']}")
        print(f"   Category: {business['category']}")
        print(f"   Location: {business['location']}")
        print(f"   Score: {business['confidence_score']}/100")
        print(f"   Priority: {business['priority']}")
        print(f"   URL: {business['page_url']}")
        print(f"   Discovered: {business['discovered_date']}")
        print(f"   Alerted: {'Yes' if business['alerted'] else 'No'}")
    
    # Unalereted businesses
    unalereted = db.get_unalereted_businesses()
    if unalereted:
        print("\n" + "=" * 80)
        print(f"⚠️  {len(unalereted)} BUSINESSES PENDING ALERT")
        print("=" * 80)
        for business in unalereted[:5]:
            print(f"  - {business['business_name']} ({business['platform']})")
    
    print("\n" + "=" * 80)


def export_all():
    """Export all businesses to CSV"""
    db = DatabaseHandler()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"exports/all_businesses_{timestamp}.csv"
    
    Path("exports").mkdir(exist_ok=True)
    
    db.export_to_csv(output_file)
    print(f"✅ Exported to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export_all()
    else:
        view_database()

