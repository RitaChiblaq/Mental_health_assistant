from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Recommendation(Base):
    __tablename__ = 'recommendations'
    rec_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    recommendation = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="recommendations")
