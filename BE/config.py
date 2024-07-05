from sqlalchemy import create_engine


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://Rita:mentalassistant@localhost/mental_assistant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
