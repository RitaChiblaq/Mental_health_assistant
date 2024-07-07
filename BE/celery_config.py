# Celery configuration file

# URL for the message broker (Redis) used by Celery
broker_url = 'redis://localhost:6379/0'

# URL for the result backend (Redis) where Celery stores the results of tasks
result_backend = 'redis://localhost:6379/0'

# Timezone for the Celery scheduler
timezone = 'UTC'

# Schedule configuration for periodic tasks
beat_schedule = {
    'fetch-and-analyze-emails-every-10-minutes': {  # Name of the scheduled task
        'task': 'tasks.fetch_and_analyze_emails',  # Task to be executed
        'schedule': 600.0,  # Time interval in seconds (10 minutes)
    },
}