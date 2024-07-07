broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
timezone = 'UTC'
beat_schedule = {
    'fetch-and-analyze-emails-every-10-minutes': {
        'task': 'tasks.fetch_and_analyze_emails',
        'schedule': 600.0,  # Every 10 minutes
    },
}
