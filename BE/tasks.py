from celery import Celery
from agents import get_emails, analyze_mental_health
from models import EmailAnalysis
from sqlalchemy.orm import sessionmaker
from config import engine

# Initialize Celery
celery_app = Celery('tasks')
celery_app.config_from_object('celery_config')

Session = sessionmaker(bind=engine)

@celery_app.task
def fetch_and_analyze_emails():
    session = Session()
    try:
        emails = get_emails()
        for email in emails:
            analysis = analyze_mental_health(email['body'])
            email_analysis = EmailAnalysis(
                email_id=email['id'],
                subject=email['subject'],
                sender=email['from'],
                recipient=email['to'],
                body=email['body'],
                analysis=analysis
            )
            session.add(email_analysis)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error in fetch_and_analyze_emails: {e}")
    finally:
        session.close()
