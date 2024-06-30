from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from models import User, ChatSession, Message, EmotionalState
from chromadb_client import ChromaDBClient
from utils import generate_embedding
from config import engine

Session = sessionmaker(bind=engine)
session = Session()
chroma_client = ChromaDBClient(base_url="http://localhost:8000")

app = Flask(__name__)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(username=data['username'], email=data['email'], password_hash=data['password_hash'])
    session.add(new_user)
    session.commit()
    return jsonify({'user_id': str(new_user.user_id)})

@app.route('/start_chat_session', methods=['POST'])
def start_chat_session():
    data = request.json
    new_session = ChatSession(user_id=data['user_id'])
    session.add(new_session)
    session.commit()
    return jsonify({'session_id': str(new_session.session_id)})

@app.route('/add_message', methods=['POST'])
def add_message():
    data = request.json
    new_message = Message(session_id=data['session_id'], sender=data['sender'], message_text=data['message_text'])
    session.add(new_message)
    session.commit()

    # Store message embedding in ChromaDB
    embedding = generate_embedding(new_message.message_text)
    chroma_client.store_message_embedding(new_message.message_id, new_message.chat_session.user_id, embedding)
    return jsonify({'message_id': str(new_message.message_id)})

@app.route('/add_emotional_state', methods=['POST'])
def add_emotional_state():
    data = request.json
    new_emotional_state = EmotionalState(session_id=data['session_id'], detected_emotion=data['detected_emotion'], confidence_score=data['confidence_score'])
    session.add(new_emotional_state)
    session.commit()
    return jsonify({'emotion_id': str(new_emotional_state.emotion_id)})

@app.route('/add_coping_strategy', methods=['POST'])
def add_coping_strategy():
    data = request.json
    new_strategy = CopingStrategy(session_id=data['session_id'], strategy_text=data['strategy_text'], strategy_type=data['strategy_type'])
    session.add(new_strategy)
    session.commit()

    # Store strategy embedding in ChromaDB
    embedding = generate_embedding(new_strategy.strategy_text)
    chroma_client.store_strategy_embedding(new_strategy.strategy_id, embedding)
    return jsonify({'strategy_id': str(new_strategy.strategy_id)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)