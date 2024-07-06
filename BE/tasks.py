from celery import Celery
from agents import get_emails, analyze_mental_health
from models import EmailAnalysis
from sqlalchemy.orm import sessionmaker
from config import engine
import logging

import logging
from celery import Celery

# Initialize Celery
celery_app = Celery('tasks')
celery_app.config_from_object('celery_config')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    handlers=[
        logging.FileHandler("celery.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)

@celery_app.task
def fetch_and_analyze_emails():
    session = Session()
    try:
        logger.info("Fetching emails...")

        # Fetch emails
        emails = get_emails()

        for email in emails:
            logger.info(f"Fetched email data: {email}")
            if 'id' not in email or 'subject' not in email or 'from' not in email or 'to' not in email or 'body' not in email:
                logger.error(f"Email data missing required fields: {email}")
                continue  # Skip this email if any field is missing

            # Check if the email has already been analyzed
            existing_analysis = session.query(EmailAnalysis).filter_by(email_id=email['id']).first()
            if existing_analysis:
                logger.info(f"Email with ID {email['id']} has already been analyzed. Skipping...")
                continue

            if email['body'] is None:
                logger.error(f"Skipping email with subject: {email['subject']} because body is None")
                continue

            logger.info(f"Analyzing email with subject: {email['subject']}")
            analysis = analyze_mental_health(email['body'])
            logger.info(f"Analysis result: {analysis}")

            email_analysis = EmailAnalysis(
                email_id=email['id'],
                subject=email['subject'],
                sender=email['from'],
                recipient=email['to'],
                body=email['body'],
                analysis=analysis,
                is_analyzed=True  # Mark the email as analyzed
            )
            session.add(email_analysis)

        session.commit()
        logger.info("Email analysis data committed to the database.")
    except Exception as e:
        session.rollback()
        logger.error(f"Error in fetch_and_analyze_emails: {e}")
    finally:
        session.close()
