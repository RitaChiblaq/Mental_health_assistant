import chainlit as cl
from openai import OpenAI
from BE.models import Message, ChatSession, User
from BE.chromadb_client import ChromaDBClient
from BE.utils import generate_embedding
from sqlalchemy.orm import sessionmaker
from BE.config import engine

Session = sessionmaker(bind=engine)
session = Session()
chroma_client = ChromaDBClient()
openai_client = OpenAI(api_key='your_openai_api_key')


@cl.on_message
async def handle_message(message):
    user_id = message['user_id']
    user_message = message['text']

    # Retrieve or start a chat session
    chat_session = session.query(ChatSession).filter_by(user_id=user_id).order_by(ChatSession.started_at.desc()).first()
    if not chat_session:
        chat_session = ChatSession(user_id=user_id)
        session.add(chat_session)
        session.commit()

    # Store the user message
    new_message = Message(session_id=chat_session.session_id, sender='user', message_text=user_message)
    session.add(new_message)
    session.commit()

    # Store message embedding in ChromaDB
    embedding = generate_embedding(user_message)
    chroma_client.store_message_embedding(new_message.message_id, user_id, embedding)

    # Generate a response using OpenAI
    response = openai_client.Completion.create(
        engine="davinci",
        prompt=user_message,
        max_tokens=150
    )

    bot_message = response.choices[0].text.strip()

    # Store the bot response
    new_bot_message = Message(session_id=chat_session.session_id, sender='bot', message_text=bot_message)
    session.add(new_bot_message)
    session.commit()

    # Send the response back to the user
    await cl.send_message(user_id, bot_message)


if __name__ == "__main__":
    cl.run()