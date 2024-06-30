from sqlalchemy import create_engine, Column, String, Float, ForeignKey, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
import datetime

Base = declarative_base()

# Database connection
engine = create_engine('postgresql://username:password@localhost/emotional_support_db')


# Define the Users table
class User(Base):
    __tablename__ = 'users'
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


# Define the Chat Sessions table
class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    started_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    ended_at = Column(TIMESTAMP)

    user = relationship('User', back_populates='chat_sessions')


User.chat_sessions = relationship('ChatSession', order_by=ChatSession.started_at, back_populates='user')


# Define the Messages table
class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.session_id'), nullable=False)
    sender = Column(String, nullable=False)
    message_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    chat_session = relationship('ChatSession', back_populates='messages')


ChatSession.messages = relationship('Message', order_by=Message.created_at, back_populates='chat_session')


# Define the Emotional States table
class EmotionalState(Base):
    __tablename__ = 'emotional_states'
    emotion_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.session_id'), nullable=False)
    detected_emotion = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    chat_session = relationship('ChatSession', back_populates='emotional_states')


ChatSession.emotional_states = relationship('EmotionalState', order_by=EmotionalState.created_at, back_populates='chat_session')
