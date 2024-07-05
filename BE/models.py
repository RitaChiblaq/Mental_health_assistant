from sqlalchemy import create_engine, Column, String, Float, ForeignKey, Text, TIMESTAMP, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
import datetime

Base = declarative_base()

# Database connection
engine = create_engine('mysql+mysqldb://Rita:mentalassistant@localhost/mental_assistant')


# Define the Users table
class User(Base):
    __tablename__ = 'users'
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), nullable=False)  # Specify length for String
    email = Column(String(100), nullable=False, unique=True)  # Specify length for String
    password_hash = Column(String(128), nullable=False)  # Specify length for String
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


# Define the Chat Sessions table
class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    session_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    started_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    ended_at = Column(TIMESTAMP)

    user = relationship('User', back_populates='chat_sessions')


User.chat_sessions = relationship('ChatSession', order_by=ChatSession.started_at, back_populates='user')


# Define the Messages table
class Message(Base):
    __tablename__ = 'messages'
    message_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey('chat_sessions.session_id'), nullable=False)
    sender = Column(String(50), nullable=False)  # Specify length for String
    message_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    chat_session = relationship('ChatSession', back_populates='messages')


ChatSession.messages = relationship('Message', order_by=Message.created_at, back_populates='chat_session')


# Define the Emotional States table
class EmotionalState(Base):
    __tablename__ = 'emotional_states'
    emotion_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey('chat_sessions.session_id'), nullable=False)
    detected_emotion = Column(String(50), nullable=False)  # Specify length for String
    confidence_score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    chat_session = relationship('ChatSession', back_populates='emotional_states')


ChatSession.emotional_states = relationship('EmotionalState', order_by=EmotionalState.created_at, back_populates='chat_session')

# Define the Email Analysis table
class EmailAnalysis(Base):
    __tablename__ = 'email_analysis'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email_id = Column(String(100), nullable=False)  # Specify length for String
    subject = Column(String(255), nullable=False)  # Specify length for String
    sender = Column(String(100), nullable=False)  # Specify length for String
    recipient = Column(String(100), nullable=False)  # Specify length for String
    body = Column(Text, nullable=False)
    analysis = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

class CopingStrategy(Base):
    __tablename__ = 'coping_strategy'
    id = Column(Integer, primary_key=True)
    strategy = Column(Text)
    created_at = Column(DateTime, default=func.now())

# Create all tables in the database
Base.metadata.create_all(engine)
