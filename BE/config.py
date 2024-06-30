from sqlalchemy import create_engine


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/emotional_support_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)