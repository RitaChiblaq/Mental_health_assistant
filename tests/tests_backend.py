import pytest
from flask import Flask, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BE.models import Base, User, ChatSession, Message, EmotionalState, CopingStrategy
from BE.__init__ import create_app

# Create a new database for testing
TEST_DATABASE_URI = 'test_uri'
engine = create_engine(TEST_DATABASE_URI)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope='module')
def new_user():
    user = User(username='test_user', email='test_user@example.com', password_hash='test_hash')
    return user


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI

    # Create the database and the database table(s)
    Base.metadata.create_all(engine)

    # Establish an application context before running the tests
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

    # Drop the database and the database table(s)
    Base.metadata.drop_all(engine)


def test_add_user(test_client, new_user):
    """
    Test adding a new user to the database.
    """
    session = Session()
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email='test_user@example.com').first()
    assert user.email == 'test_user@example.com'


def test_start_chat_session(test_client, new_user):
    """
    Test starting a new chat session for a user.
    """
    session = Session()
    user = session.query(User).filter_by(email='test_user@example.com').first()
    new_session = ChatSession(user_id=user.user_id)
    session.add(new_session)
    session.commit()
    assert new_session.user_id == user.user_id


def test_add_message(test_client, new_user):
    """
    Test adding a new message to a chat session.
    """
    session = Session()
    user = session.query(User).filter_by(email='test_user@example.com').first()
    chat_session = session.query(ChatSession).filter_by(user_id=user.user_id).first()
    new_message = Message(session_id=chat_session.session_id, sender='user', message_text='Hello, this is a test message.')
    session.add(new_message)
    session.commit()
    assert new_message.message_text == 'Hello, this is a test message.'


def test_add_emotional_state(test_client, new_user):
    """
    Test adding an emotional state for a chat session.
    """
    session = Session()
    user = session.query(User).filter_by(email='test_user@example.com').first()
    chat_session = session.query(ChatSession).filter_by(user_id=user.user_id).first()
    new_emotion = EmotionalState(session_id=chat_session.session_id, detected_emotion='Happy', confidence_score=0.95)
    session.add(new_emotion)
    session.commit()
    assert new_emotion.detected_emotion == 'Happy'
    assert new_emotion.confidence_score == 0.95


def test_save_coping_strategy(test_client):
    """
    Test saving a coping strategy to the database.
    """
    session = Session()
    strategy_text = "Take deep breaths and meditate."
    new_strategy = CopingStrategy(strategy=strategy_text)
    session.add(new_strategy)
    session.commit()
    strategy = session.query(CopingStrategy).filter_by(strategy=strategy_text).first()
    assert strategy.strategy == strategy_text


def test_get_user_context(test_client, new_user):
    """
    Test fetching user context from the latest email analysis.
    """
    session = Session()
    user = session.query(User).filter_by(email='test_user@example.com').first()
    new_session = ChatSession(user_id=user.user_id)
    session.add(new_session)
    session.commit()
    chat_session = session.query(ChatSession).filter_by(user_id=user.user_id).first()
    new_message = Message(session_id=chat_session.session_id, sender='user', message_text='Test context message.')
    session.add(new_message)
    session.commit()
    analysis = EmailAnalysis(
        email_id='test_email_id',
        subject='Test Subject',
        sender='test_sender@example.com',
        recipient='test_recipient@example.com',
        body='Test email body.',
        analysis='No issues detected.',
        is_analyzed=True
    )
    session.add(analysis)
    session.commit()
    context = test_client.get_user_context()
    assert 'Test Subject' in context


def test_api_add_user(test_client):
    """
    Test API endpoint to add a new user.
    """
    data = {
        'username': 'api_test_user',
        'email': 'api_test_user@example.com',
        'password_hash': 'api_test_hash'
    }
    response = test_client.post('/add_user', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'user_id' in response_data


def test_api_start_chat_session(test_client):
    """
    Test API endpoint to start a new chat session.
    """
    data = {
        'user_id': 'test_user_id'
    }
    response = test_client.post('/start_chat_session', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'session_id' in response_data


def test_api_add_message(test_client):
    """
    Test API endpoint to add a message to a chat session.
    """
    data = {
        'session_id': 'test_session_id',
        'sender': 'user',
        'message_text': 'API test message'
    }
    response = test_client.post('/add_message', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'message_id' in response_data


def test_api_add_emotional_state(test_client):
    """
    Test API endpoint to add an emotional state to a chat session.
    """
    data = {
        'session_id': 'test_session_id',
        'detected_emotion': 'Stressed',
        'confidence_score': 0.85
    }
    response = test_client.post('/add_emotional_state', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'emotion_id' in response_data