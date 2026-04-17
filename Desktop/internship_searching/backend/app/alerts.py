import logging
from app.db_models import User, Job, EmailNotification
from sqlalchemy.orm import Session
from datetime import datetime

logger = logging.getLogger(__name__)

def send_job_alert(user_email: str, job_title: str, job_url: str):
    """
    Mock function for sending an email alert.
    In production, this would use fastapi-mail or an external SMTP service.
    """
    logger.info(f"ALERTER: Sending alert to {user_email} for job: {job_title} ({job_url})")
    # Simulation of success
    return True

def process_alerts(db: Session, new_jobs: list[Job]):
    """
    Scan for new jobs and notify relevant users.
    (Currently notifies all users for all new jobs for demo purposes)
    """
    users = db.query(User).all()
    
    for user in users:
        for job in new_jobs:
            success = send_job_alert(user.email, job.title, job.url)
            if success:
                # Log the notification in DB
                notification = EmailNotification(
                    user_id=user.id,
                    job_id=job.id,
                    sent_at=datetime.now()
                )
                db.add(notification)
    
    db.commit()
