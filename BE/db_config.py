from sqlalchemy import create_engine


class Config:
    """
    Configuration class for the application settings.
    """
    # URI for connecting to the MySQL database
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://klaudia:mentalassistant@localhost/mental_health_assistant'

    # Disable SQLAlchemy event system to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # URI for connecting to the Redis broker for Celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'

    # URI for connecting to the Redis backend for Celery
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


# Create a SQLAlchemy engine instance using the database URI from the Config class
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)