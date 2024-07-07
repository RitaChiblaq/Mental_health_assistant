from sqlalchemy import create_engine, Column, String, Float, ForeignKey, Text, TIMESTAMP, Integer, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
import datetime

# Base class for the database models
Base = declarative_base()

# Database connection
engine = create_engine('mysql+mysqldb://klaudia:mentalassistant@localhost/mental_health_assistant')


# Define the Users table
class User(Base):
    """
    Model for the users table in the database.
    """
    __tablename__ = 'users'
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), nullable=False)  # Username of the user
    email = Column(String(100), nullable=False, unique=True)  # Email of the user, must be unique
    password_hash = Column(String(128), nullable=False)  # Hashed password
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)  # Timestamp for when the user is created
    updated_at = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)  # Timestamp for when the user is last updated


# Define the Chat Sessions table
class ChatSession(Base):
    """
    Model for the chat_sessions table in the database.
    """
    __tablename__ = 'chat_sessions'
    session_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)  # Foreign key referencing user
    started_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)  # Timestamp for when the session started
    ended_at = Column(TIMESTAMP)  # Timestamp for when the session ended

    # Relationship to the User model
    user = relationship('User', back_populates='chat_sessions')


# Relationship for User to access their chat sessions
User.chat_sessions = relationship('ChatSession', order_by=ChatSession.started_at, back_populates='user')


# Define the Messages table
class Message(Base):
    """
    Model for the messages table in the database.
    """
    __tablename__ = 'messages'
    message_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey('chat_sessions.session_id'), nullable=False)  # Foreign key referencing chat session
    sender = Column(String(50), nullable=False)  # Sender of the message
    message_text = Column(Text, nullable=False)  # Text content of the message
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)  # Timestamp for when the message is created

    # Relationship to the ChatSession model
    chat_session = relationship('ChatSession', back_populates='messages')


# Relationship for ChatSession to access its messages
ChatSession.messages = relationship('Message', order_by=Message.created_at, back_populates='chat_session')


# Define the Emotional States table
class EmotionalState(Base):
    """
    Model for the emotional_states table in the database.
    """
    __tablename__ = 'emotional_states'
    emotion_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey('chat_sessions.session_id'), nullable=False)  # Foreign key referencing chat session
    detected_emotion = Column(String(50), nullable=False)  # Detected emotion
    confidence_score = Column(Float, nullable=False)  # Confidence score of the detected emotion
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)  # Timestamp for when the emotion is detected

    # Relationship to the ChatSession model
    chat_session = relationship('ChatSession', back_populates='emotional_states')


# Relationship for ChatSession to access its emotional states
ChatSession.emotional_states = relationship('EmotionalState', order_by=EmotionalState.created_at, back_populates='chat_session')


# Define the Email Analysis table
class EmailAnalysis(Base):
    """
    Model for the email_analysis table in the database.
    """
    __tablename__ = 'email_analysis'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email_id = Column(String(100), nullable=False)  # Email ID
    subject = Column(String(255), nullable=False)  # Subject of the email
    sender = Column(String(100), nullable=False)  # Sender of the email
    recipient = Column(String(100), nullable=False)  # Recipient of the email
    body = Column(Text, nullable=False)  # Body content of the email
    analysis = Column(Text, nullable=False)  # Analysis of the email
    is_analyzed = Column(Boolean, default=False)  # Whether the email has been analyzed
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)  # Timestamp for when the email is created


# Define the Coping Strategy table
class CopingStrategy(Base):
    """
    Model for the coping_strategy table in the database.
    """
    __tablename__ = 'coping_strategy'
    id = Column(Integer, primary_key=True)
    strategy = Column(Text)  # Text content of the coping strategy
    created_at = Column(DateTime, default=func.now())  # Timestamp for when the strategy is created

# Create all tables in the database
Base.metadata.create_all(engine)