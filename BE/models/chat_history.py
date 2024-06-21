from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class ChatHistory(Base):
    __tablename__ = 'chat_history'
    chat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message = Column(String(255), nullable=False)
    response = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    emotion = Column(String(255))
    user = relationship("User", back_populates="chat_history")