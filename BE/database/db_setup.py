from sqlalchemy import create_engine
from BE.models.user import Base
from BE.config import DATABASE_URI


def setup_db():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)