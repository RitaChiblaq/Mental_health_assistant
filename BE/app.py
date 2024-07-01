from flask import Flask, request, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker

from BE.utils import generate_embedding
from models import User, ChatSession, Message, EmotionalState
from chromadb_client import ChromaDBClient
from config import engine
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database session setup
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

app = Flask(__name__)
chroma_client = ChromaDBClient(base_url="http://localhost:8000")

@app.teardown_appcontext
def remove_session(exception=None):
    Session.remove()

@app.route('/add_user', methods=['POST'])
def add_user():
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
    session = Session()
    try:
        data = request.json
        new_message = Message(session_id=data['session_id'], sender=data['sender'], message_text=data['message_text'])
        session.add(new_message)
        session.commit()
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
    session = Session()
    try:
        data = request.json
        new_emotional_state = EmotionalState(session_id=data['session_id'], detected_emotion=data['detected_emotion'], confidence_score=data['confidence_score'])
        session.add(new_emotional_state)
        session.commit()
        return jsonify({'emotion_id': str(new_emotional_state.emotion_id)})
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding emotional state: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
