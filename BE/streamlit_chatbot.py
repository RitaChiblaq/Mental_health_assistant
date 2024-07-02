import sys
from pathlib import Path
import os
import pandas as pd
import streamlit as st
import yaml
from textblob import TextBlob
import openai
from sqlalchemy.orm import sessionmaker
from config import engine
from models import EmailAnalysis
from authlib.integrations.requests_client import OAuth2Session
from requests import get
import json

# Load configuration
config_path = Path('/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/Project/config.yaml')
config = yaml.safe_load(open(config_path))
os.environ["OPENAI_API_KEY"] = config['KEYS']['openai']
openai.api_key = os.environ["OPENAI_API_KEY"]
google_client_id = config['KEYS']['google_client_id']
google_client_secret = config['KEYS']['google_client_secret']
redirect_uri = 'http://localhost:8501'  # Update with your Streamlit app URL

# Update this path to the correct one
sys.path.insert(0, '/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/Project/Setup')

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


# Analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", polarity
    elif 0.1 < polarity <= 0.5:
        return "Positive", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", polarity
    elif -0.5 < polarity < -0.1:
        return "Negative", polarity
    else:
        return "Very Negative", polarity


# Provide coping strategies
def provide_coping_strategy(sentiment):
    strategies = {
        "Very Positive": "Keep up the positive vibes! Consider sharing your good mood with others.",
        "Positive": "It's great to see you're feeling positive. Keep doing what you're doing!",
        "Neutral": "Feeling neutral is okay. Consider engaging in activities you enjoy.",
        "Negative": "It seems you're feeling down. Try to take a break and do something relaxing.",
        "Very Negative": "I'm sorry to hear that you're feeling very negative. Consider talking to a friend or seeking professional help."
    }
    return strategies.get(sentiment, "Keep going, you're doing great!")

# Fetch user context from email analysis
def get_user_context():
    try:
        latest_analysis = session.query(EmailAnalysis).order_by(EmailAnalysis.created_at.desc()).first()
        if latest_analysis:
            return f"Latest email analysis:\n\nSubject: {latest_analysis.subject}\nFrom: {latest_analysis.sender}\nTo: {latest_analysis.recipient}\n\nAnalysis: {latest_analysis.analysis}\n\n"
        return ""
    except Exception as e:
        return f"Error fetching user context: {str(e)}"


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

def submit():
    user_message = st.session_state.input_text.strip()
    word_count = len(user_message.split())
    if word_count < 5:
        st.warning("Please enter at least 5 words.")
    else:
        st.session_state['messages'].append(("You", user_message))

        sentiment, polarity = analyze_sentiment(user_message)
        coping_strategy = provide_coping_strategy(sentiment)

        user_context = get_user_context()
        response = generate_response(user_message, user_context)
        full_response = f"{response}\n\nCoping Strategy: {coping_strategy}"

        st.session_state['messages'].append(("Bot", full_response))
        st.session_state['mood_tracker'].append((user_message, sentiment, polarity))
        st.session_state.input_text = ""  # Clear the input after submission

st.text_input("You:", key="input_text", on_change=submit, label_visibility="collapsed")

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for sender, message in st.session_state['messages']:
    if sender == "You":
        st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{message}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state['mood_tracker']:
    mood_data = pd.DataFrame(st.session_state['mood_tracker'], columns=["Message", "Sentiment", "Polarity"])
    st.line_chart(mood_data['Polarity'])

# Authentication section
if st.session_state['token'] is None:
    if st.button('Login with Gmail'):
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

    if st.button('Logout'):
        st.session_state['token'] = None
        st.experimental_rerun()

st.sidebar.title("Resources")
st.sidebar.write("If you need immediate help, please contact one of the following resources:")
st.sidebar.write("1. National Suicide Prevention Lifeline: 1-800-273-8255")
st.sidebar.write("2. Crisis Text Line: Text 'HELLO' to 741741")
st.sidebar.write("3. SAMHSA’s National Helpline: 1-800-662-HELP (4357)")
st.sidebar.write("[More Resources](https://www.mentalhealth.gov/get-help/immediate-help)")

st.sidebar.title("How to Interact with the Chatbot")
st.sidebar.write("""
- Please enter at least 5 words.
- Include your feelings or emotions in the message.
- Be as specific as possible about your current situation or problems.
- Example: "I am feeling very anxious about my upcoming exams."
""")

if st.sidebar.button("Show Session Summary"):
    st.sidebar.write("### Session Summary")
    for i, (message, sentiment, polarity) in enumerate(st.session_state['mood_tracker']):
        st.sidebar.write(f"{i + 1}. {message} - Sentiment: {sentiment} (Polarity: {polarity})")
