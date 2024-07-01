#celery_config.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
beat_schedule = {
    'fetch-and-analyze-emails-every-10-minutes': {
        'task': 'tasks.fetch_and_analyze_emails',
        'schedule': 600.0,  # every 10 minutes
    },
}
timezone = 'UTC'
