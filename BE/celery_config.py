from celery.schedules import crontab

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

beat_schedule = {
    'fetch-and-analyze-emails-every-2-minutes': {
        'task': 'tasks.fetch_and_analyze_emails',
        'schedule': 120.0,  # 2 minutes in seconds
    },
}

timezone = 'UTC'
