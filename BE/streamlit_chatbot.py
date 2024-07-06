from pathlib import Path
import os
import pandas as pd
import streamlit as st
import yaml
from textblob import TextBlob
import openai
from sqlalchemy.orm import sessionmaker
from config import engine
from models import EmailAnalysis, CopingStrategy, ChatSession, EmotionalState, Message, User
from authlib.integrations.requests_client import OAuth2Session
import requests
import datetime
import uuid

# Load configuration
config_path = Path('/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/Project/config.yaml')
config = yaml.safe_load(open(config_path))
os.environ["OPENAI_API_KEY"] = config['KEYS']['openai']
openai.api_key = os.environ["OPENAI_API_KEY"]
google_client_id = config['KEYS']['google_client_id']
google_client_secret = config['KEYS']['google_client_secret']
redirect_uri = 'http://localhost:8501'

# Database session setup
Session = sessionmaker(bind=engine)
session = Session()

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Ensure the path to the style.css file is correct
local_css("/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/Project/FE/.streamlit/style.css")

# Initialize OAuth2 session
def get_google_oauth_session(state=None, token=None):
    return OAuth2Session(
        client_id=google_client_id,
        client_secret=google_client_secret,
        redirect_uri=redirect_uri,
        scope='openid email profile',
        state=state,
        token=token
    )

# Function to generate a response from GPT-3.5-turbo
def generate_response(prompt, user_context=""):
    try:
        full_prompt = f"{user_context}\n\nUser: {prompt}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mental health assistant. Your goal is to provide empathetic and supportive responses to help users manage their mental health. Offer coping strategies and encourage positive actions."},
                {"role": "user", "content": full_prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return f"An error occurred: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Enhanced Emotional State Analysis
def analyze_emotional_state(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    subjectivity = analysis.sentiment.subjectivity

    if polarity > 0.5:
        return "Very Positive", polarity, subjectivity
    elif 0.1 < polarity <= 0.5:
        return "Positive", polarity, subjectivity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", polarity, subjectivity
    elif -0.5 < polarity < -0.1:
        return "Negative", polarity, subjectivity
    else:
        return "Very Negative", polarity, subjectivity

# Provide detailed personalized recommendations
def provide_personalized_recommendations(sentiment, subjectivity):
    if sentiment == "Very Positive":
        strategy = """
            It's great to see you're feeling very positive. Here are some ways to maintain and leverage your positive mindset:
            - **Share Your Positivity:** Spread your positive energy by engaging in conversations or activities with others. Positivity is contagious!
            - **Set New Goals:** Use your positive outlook to set new personal or professional goals. A positive mindset can enhance your motivation and productivity.
            - **Reflect and Appreciate:** Take some time to reflect on the things that are going well and express gratitude. This practice can reinforce your positive feelings.
        """
    elif sentiment == "Positive":
        strategy = """
            It's good to see you're feeling positive. Here are a few suggestions to keep up the positive momentum:
            - **Engage in Enjoyable Activities:** Continue doing activities that bring you joy and satisfaction. It could be hobbies, sports, or spending time with loved ones.
            - **Practice Gratitude:** Regularly acknowledge and appreciate the good things in your life. Consider keeping a gratitude journal.
            - **Stay Connected:** Maintain social connections with friends and family. Positive interactions can help sustain your positive feelings.
        """
    elif sentiment == "Neutral":
        strategy = """
            Feeling neutral is completely okay. Here are some strategies to enhance your well-being:
            - **Explore New Interests:** Try picking up a new hobby or interest. It can add excitement and break the monotony.
            - **Mindfulness Practices:** Engage in mindfulness or meditation to center yourself and improve your emotional awareness.
            - **Physical Activity:** Incorporate regular physical activity into your routine. Exercise can boost your mood and energy levels.
        """
    elif sentiment == "Negative":
        strategy = """
            It seems you're feeling a bit down. Here are some steps you can take to improve your mood:
            - **Reach Out for Support:** Talk to a trusted friend or family member about how you're feeling. Sharing your thoughts can provide relief.
            - **Engage in Relaxing Activities:** Consider activities like reading, listening to music, or taking a walk to help you relax and unwind.
            - **Professional Help:** If your negative feelings persist, consider reaching out to a mental health professional for guidance and support.
        """
    else:  # Very Negative
        strategy = """
            I'm sorry to hear that you're feeling very negative. Here are some urgent steps to take care of your mental health:
            - **Seek Immediate Support:** If you're feeling overwhelmed, reach out to a crisis hotline or mental health professional immediately.
            - **Connect with Loved Ones:** Talk to friends or family members who can offer support and understanding.
            - **Self-Care:** Engage in activities that promote relaxation and self-care, such as deep breathing exercises, meditation, or a warm bath.
            - **Professional Help:** Consider scheduling an appointment with a therapist or counselor to explore your feelings and get professional advice.
        """
    return strategy

# Save coping strategy to the database
def save_coping_strategy(strategy):
    new_strategy = CopingStrategy(strategy=strategy)
    session.add(new_strategy)
    session.commit()

# Save user message and sentiment to the database
def save_user_message(session_id, sender, message_text, sentiment=None, polarity=None):
    new_message = Message(
        session_id=session_id,
        sender=sender,
        message_text=message_text
    )
    session.add(new_message)
    session.commit()

    if sender == "You" and sentiment and polarity:
        new_emotion = EmotionalState(
            session_id=session_id,
            detected_emotion=sentiment,
            confidence_score=polarity
        )
        session.add(new_emotion)
        session.commit()

# Ensure default user exists
def ensure_default_user():
    user = session.query(User).filter_by(email='default_user@example.com').first()
    if not user:
        user = User(username='default_user', email='default_user@example.com', password_hash='default_hash')
        session.add(user)
        session.commit()
    return user.user_id

# Fetch user context from email analysis
def get_user_context():
    try:
        latest_analysis = session.query(EmailAnalysis).order_by(EmailAnalysis.created_at.desc()).first()
        if latest_analysis:
            return f"Latest email analysis:\n\nSubject: {latest_analysis.subject}\nFrom: {latest_analysis.sender}\nTo: {latest_analysis.recipient}\n\nAnalysis: {latest_analysis.analysis}\n\n"
        return ""
    except Exception as e:
        return f"Error fetching user context: {str(e)}"

# Display notification
def show_notification(message):
    st.toast(message)

# Ensure user is stored in the database
def store_user_if_not_exists(user_info):
    existing_user = session.query(User).filter_by(email=user_info['email']).first()
    if not existing_user:
        new_user = User(
            username=user_info['name'],
            email=user_info['email'],
            password_hash=str(uuid.uuid4())  # Using a random UUID as password hash for simplicity
        )
        session.add(new_user)
        session.commit()
        return new_user.user_id
    return existing_user.user_id

# Retrieve chat history for the user
def get_chat_history(user_id):
    chat_sessions = session.query(ChatSession).filter_by(user_id=user_id).order_by(ChatSession.started_at.desc()).all()
    chat_history = []
    for chat_session in chat_sessions:
        messages = session.query(Message).filter_by(session_id=chat_session.session_id).order_by(Message.created_at).all()
        for message in messages:
            chat_history.append((message.sender, message.message_text, message.created_at))
    return chat_history

# Trigger email analysis task
def trigger_email_analysis():
    try:
        response = requests.post("http://localhost:5001/fetch_analyze_emails")
        if response.status_code == 202:
            st.success("Email analysis started.")
        else:
            st.error(f"Failed to start email analysis: {response.text}")
    except Exception as e:
        st.error(f"Failed to start email analysis: {e}")

# Streamlit application
st.title("Mental Health Support Chatbot")

if 'token' not in st.session_state:
    st.session_state['token'] = None

if 'oauth_state' not in st.session_state:
    st.session_state['oauth_state'] = None

# Chatbot interface
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'mood_tracker' not in st.session_state:
    st.session_state['mood_tracker'] = []
if 'coping_strategies' not in st.session_state:
    st.session_state['coping_strategies'] = []
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

def submit():
    user_message = st.session_state.input_text.strip()
    if not user_message:
        st.warning("Please enter a message.")
        return

    if 'input_text' in st.session_state and len(st.session_state.input_text.split()) < 5:
        st.warning("Please enter at least 5 words.")
        return

    st.session_state['messages'].insert(0, ("You", user_message))

    sentiment, polarity, subjectivity = analyze_emotional_state(user_message)
    coping_strategy = provide_personalized_recommendations(sentiment, subjectivity)
    st.session_state['coping_strategies'].insert(0, coping_strategy)

    if st.session_state['token']:  # Only save if user is logged in
        save_coping_strategy(coping_strategy)  # Save the coping strategy to the database
        save_user_message(st.session_state['session_id'], "You", user_message, sentiment, polarity)  # Save the user message to the database

    user_context = get_user_context()
    response = generate_response(user_message, user_context)

    st.session_state['messages'].insert(0, ("Bot", response))
    if st.session_state['token']:  # Only save if user is logged in
        save_user_message(st.session_state['session_id'], "Bot", response)  # Save the bot response to the database

    st.session_state['mood_tracker'].insert(0, (user_message, sentiment, polarity))
    st.session_state.input_text = ""  # Clear the input after submission

    # Display notification about the user's emotional state
    notification_message = f"Your current emotional state is {sentiment}. We have provided a personalized coping strategy."
    show_notification(notification_message)

    st.experimental_rerun()  # Rerun the app to update the UI after message submission

def display_messages(messages):
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for sender, message in messages:
        if sender == "You":
            st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>{message}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.text_input("You:", key="input_text", on_change=submit, label_visibility="collapsed")

# Authentication section
if st.session_state['token'] is None:
    if st.button('Login with Gmail', key="login_button"):
        oauth = get_google_oauth_session()
        authorization_url, state = oauth.create_authorization_url('https://accounts.google.com/o/oauth2/auth')
        st.session_state['oauth_state'] = state
        st.write(f"[Click here to authorize]({authorization_url})")

    query_params = st.experimental_get_query_params()
    if 'code' in query_params:
        oauth = get_google_oauth_session(state=st.session_state['oauth_state'])
        try:
            token = oauth.fetch_token(
                'https://accounts.google.com/o/oauth2/token',
                authorization_response=f'{redirect_uri}?code={query_params["code"][0]}',
                grant_type='authorization_code'  # Ensure the correct grant type is used
            )
            st.session_state['token'] = token
            st.experimental_rerun()  # Rerun the app to update the UI
        except Exception as e:
            st.error(f"OAuth error: {e}")
else:
    oauth = get_google_oauth_session(token=st.session_state['token'])
    user_info = oauth.get('https://www.googleapis.com/oauth2/v1/userinfo').json()

    # Store user in the database if not exists
    user_id = store_user_if_not_exists(user_info)
    st.session_state['user_id'] = user_id

    # Retrieve and display chat history
    if st.session_state['session_id'] is None:
        new_session = ChatSession(user_id=user_id)
        session.add(new_session)
        session.commit()
        st.session_state['session_id'] = new_session.session_id

        chat_history = get_chat_history(user_id)
        # Sort messages with the newest ones at the top
        chat_history.sort(key=lambda x: x[2], reverse=True)
        st.session_state['messages'] = [(msg[0], msg[1]) for msg in chat_history]

    # Trigger email analysis task after login
    trigger_email_analysis()

if st.session_state['messages']:
    display_messages(st.session_state['messages'])

if st.session_state['token']:  # Only show logout button if logged in
    if st.button('Logout', key="logout_button_logged_in"):
        st.session_state['token'] = None
        st.session_state['session_id'] = None
        st.session_state['messages'] = []
        st.session_state['mood_tracker'] = []
        st.session_state['coping_strategies'] = []
        st.experimental_rerun()

if st.session_state['mood_tracker']:
    mood_data = pd.DataFrame(st.session_state['mood_tracker'], columns=["Message", "Sentiment", "Polarity"])
    st.markdown("<br>", unsafe_allow_html=True)  # Add space between Coping Strategy and Mental Analysis
    st.markdown("### Latest Coping Strategy")
    st.markdown(f"{st.session_state['coping_strategies'][0]}", unsafe_allow_html=True)  # Display the latest coping strategy
    st.markdown("### Mental Analysis")
    st.line_chart(mood_data['Polarity'])

st.sidebar.write("If you need immediate help, please contact one of the following resources:")
st.sidebar.write("1. Telefonseelsorge: 0800 111 0 111 or 0800 111 0 222 (available 24/7)")
st.sidebar.write("2. Berliner Krisendienst: 030 39063 00 (available 24/7 in Berlin)")
st.sidebar.write("3. Telefonberatung für Kinder und Jugendliche (Nummer gegen Kummer): 116 111 (available Monday to Saturday from 14:00 to 20:00)")
st.sidebar.write("4. Deutsche Depressionshilfe: 0800 33 44 533 (hotline for depression, available Monday to Thursday from 13:00 to 17:00)")
st.sidebar.write("[More Resources](https://www.deutsche-depressionshilfe.de/depression-infos-und-hilfe/wo-finde-ich-hilfe/krisendienste-und-beratungsstellen)")

st.sidebar.title("How to Interact with the Chatbot")
st.sidebar.write("""
- Please enter at least 5 words.
- Include your feelings or emotions in the message.
- Be as specific as possible about your current situation or problems.
- Example: "I am feeling very anxious about my upcoming exams."
""")

# Knowledge Base Section
st.sidebar.title("Knowledge Base")
st.sidebar.write("Here are some useful resources for mental health information in German:")
st.sidebar.write("[Bundeszentrale für gesundheitliche Aufklärung (BZgA)](https://www.bzga.de/)")
st.sidebar.write("Offers a wide range of information on mental health, prevention, and support services.")
st.sidebar.write("[psychenet](https://www.psychenet.de/)")
st.sidebar.write("A mental health information network providing insights, self-tests, and support for various mental health issues.")
st.sidebar.write("[Mindzone](https://mindzone.info/)")
st.sidebar.write("A project aimed at promoting mental health and providing support for young people.")

if st.sidebar.button("Show Session Summary", key="session_summary_button"):
    st.sidebar.write("### Session Summary")
    for i, (message, sentiment, polarity) in enumerate(st.session_state['mood_tracker']):
        st.sidebar.write(f"{i + 1}. {message} - Sentiment: {sentiment} (Polarity: {polarity})")
