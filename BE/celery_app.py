from celery import Celery
from config import Config

# Initialize Celery app with broker and backend configuration
celery_app = Celery('tasks', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)


@celery_app.task
def analyze_email(email_text):
    """
    Celery task to analyze an email for mental health issues.

    Args:
        email_text (str): The text of the email to be analyzed.

    Returns:
        str: The result of the mental health analysis.
    """
    from agents import analyze_mental_health
    return analyze_mental_health(email_text)