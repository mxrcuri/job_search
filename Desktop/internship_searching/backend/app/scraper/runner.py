import logging
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.db_models import Job, Base
from app.scraper.sources import get_job_sources
from app.scraper.parsers import ParserFactory
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_scraper():
    """
    Main function to run the scraping process.
    """
    logger.info("Starting scraper job...")
    sources = get_job_sources()
    db = SessionLocal()
    
    new_jobs_count = 0
    
    # For demonstration, limit to a few sources to avoid blocking
    # In production, we could process more or use a queue
    for source in sources[:10]: 
        company = source["company"]
        ats = source["ats"]
        url = source["url"]
        
        parser = ParserFactory.get_parser(ats)
        if not parser:
            continue
            
        logger.info(f"Scraping {company} ({ats})...")
        jobs = parser.parse(url, company)
        
        for job_data in jobs:
            # Check if job already exists (by URL)
            existing = db.query(Job).filter(Job.url == job_data["url"]).first()
            if not existing:
                new_job = Job(**job_data)
                db.add(new_job)
                new_jobs_count += 1
        
        db.commit()
    
    db.close()
    logger.info(f"Scraper job finished. Added {new_jobs_count} new jobs.")
    return new_jobs_count

scheduler = BackgroundScheduler()

def start_scheduler():
    """
    Starts the APScheduler to run the scraper periodically.
    """
    if not scheduler.running:
        # Run every 24 hours
        scheduler.add_job(run_scraper, 'interval', hours=24, id='job_scraper_id')
        scheduler.start()
        logger.info("Scheduler started.")

def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("Scheduler shut down.")

if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    run_scraper()
