from flask import Flask, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
from BE.utils import generate_embedding
from models import User, ChatSession, Message, EmotionalState
from chromadb_client import ChromaDBClient
from BE.db_config import engine
from tasks import fetch_and_analyze_emails  # Import the Celery task
import logging
import subprocess

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database session setup
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Initialize Flask app
app = Flask(__name__)

# Initialize ChromaDB client
chroma_client = ChromaDBClient(base_url="http://localhost:8000")


@app.teardown_appcontext
def remove_session(exception=None):
    """
    Remove the database session after the context is torn down.
    """
    Session.remove()


@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Add a new user to the database.

    Expects a JSON payload with 'username', 'email', and 'password_hash'.

    Returns the user_id of the newly created user.
    """
    session = Session()
    try:
        data = request.json
        new_user = User(username=data['username'], email=data['email'], password_hash=data['password_hash'])
        session.add(new_user)
        session.commit()
        return jsonify({'user_id': str(new_user.user_id)})
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding user: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/start_chat_session', methods=['POST'])
def start_chat_session():
    """
    Start a new chat session for a user.

    Expects a JSON payload with 'user_id'.

    Returns the session_id of the newly created chat session.
    """
    session = Session()
    try:
        data = request.json
        new_session = ChatSession(user_id=data['user_id'])
        session.add(new_session)
        session.commit()
        return jsonify({'session_id': str(new_session.session_id)})
    except Exception as e:
        session.rollback()
        logger.error(f"Error starting chat session: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/add_message', methods=['POST'])
def add_message():
    """
    Add a new message to a chat session.

    Expects a JSON payload with 'session_id', 'sender', and 'message_text'.

    Returns the message_id of the newly created message.
    """
    session = Session()
    try:
        data = request.json
        new_message = Message(session_id=data['session_id'], sender=data['sender'], message_text=data['message_text'])
        session.add(new_message)
        session.commit()

        # Generate embedding and store it
        embedding = generate_embedding(new_message.message_text)
        chroma_client.store_message_embedding(new_message.message_id, new_message.chat_session.user_id, embedding)

        return jsonify({'message_id': str(new_message.message_id)})
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding message: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/add_emotional_state', methods=['POST'])
def add_emotional_state():
    """
    Add a new emotional state to a chat session.

    Expects a JSON payload with 'session_id', 'detected_emotion', and 'confidence_score'.

    Returns the emotion_id of the newly created emotional state.
    """
    session = Session()
    try:
        data = request.json
        new_emotional_state = EmotionalState(session_id=data['session_id'], detected_emotion=data['detected_emotion'],
                                             confidence_score=data['confidence_score'])
        session.add(new_emotional_state)
        session.commit()
        return jsonify({'emotion_id': str(new_emotional_state.emotion_id)})
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding emotional state: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/fetch_analyze_emails', methods=['POST'])
def fetch_analyze_emails():
    """
    Trigger the Celery task to fetch and analyze emails.

    Returns a status message indicating the email analysis has started.
    """
    fetch_and_analyze_emails.delay()
    return jsonify({'status': 'Email analysis started'}), 202


@app.route('/login', methods=['POST'])
def login():
    """
    Log in a user.

    Expects a JSON payload with 'email' and 'password'.

    Returns a success message and user_id if the login is successful, otherwise an error message.
    """
    session = Session()
    try:
        data = request.json
        user = session.query(User).filter_by(email=data['email']).first()
        if user and user.verify_password(data['password']):
            # Start Celery Worker and Beat
            subprocess.Popen(['celery', '-A', 'tasks', 'worker', '--loglevel=info'])
            subprocess.Popen(['celery', '-A', 'tasks', 'beat', '--loglevel=info'])
            return jsonify({'message': 'Login successful', 'user_id': str(user.user_id)})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)  # Ensure this is the correct port