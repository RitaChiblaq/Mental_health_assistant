#celery_app.py
from celery import Celery
from config import Config

celery_app = Celery('tasks', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

@celery_app.task
def analyze_email(email_text):
    from agents import analyze_mental_health
    return analyze_mental_health(email_text)
