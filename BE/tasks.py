from agents import get_emails, analyze_mental_health
from models import EmailAnalysis
from sqlalchemy.orm import sessionmaker
from db_config import engine

import logging
from celery import Celery

# Initialize Celery application
celery_app = Celery('tasks')
celery_app.config_from_object('celery_config')

# Set up logging to log both to a file and to the console
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    handlers=[
        logging.FileHandler("celery.log"),  # Log to a file named 'celery.log'
        logging.StreamHandler()  # Also log to the console
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Create a database session factory
Session = sessionmaker(bind=engine)


@celery_app.task
def fetch_and_analyze_emails():
    """
    Celery task to fetch and analyze emails.

    This function fetches emails using the get_emails function, analyzes their content for mental health indications,
    and stores the analysis results in the database.
    """
    session = Session()  # Create a new database session
    try:
        logger.info("Fetching emails...")

        # Fetch emails from the email server
        emails = get_emails()

        for email in emails:
            logger.info(f"Fetched email data: {email}")
            # Ensure the email data contains all required fields
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
            # Analyze the email body for mental health indications
            analysis = analyze_mental_health(email['body'])
            logger.info(f"Analysis result: {analysis}")

            # Create a new EmailAnalysis object to store the analysis result
            email_analysis = EmailAnalysis(
                email_id=email['id'],
                subject=email['subject'],
                sender=email['from'],
                recipient=email['to'],
                body=email['body'],
                analysis=analysis,
                is_analyzed=True  # Mark the email as analyzed
            )
            session.add(email_analysis)  # Add the analysis result to the session

        session.commit()  # Commit the session to save the changes to the database
        logger.info("Email analysis data committed to the database.")
    except Exception as e:
        session.rollback()  # Rollback the session in case of an error
        logger.error(f"Error in fetch_and_analyze_emails: {e}")
    finally:
        session.close()  # Close the session