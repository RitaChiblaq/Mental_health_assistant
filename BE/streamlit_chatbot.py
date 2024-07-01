import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import yaml
from textblob import TextBlob
from openai import OpenAI

config_path = Path('/Users/klaudia/Documents/Mental_health_assistant/config.yaml')
config = yaml.safe_load(open(config_path))
client = OpenAI(api_key=config['KEYS']['openai'])

# Update this path to the correct one
sys.path.insert(0, '/Users/klaudia/Documents/Mental_health_assistant/Setup')


# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Ensure the path to the style.css file is correct
local_css("/Users/klaudia/Documents/Mental_health_assistant/FE/.streamlit/style.css")

# Function to generate a response from GPT-3.5-turbo
def generate_response(prompt):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful mental health assistant."},
            {"role": "user", "content": prompt}
        ])
        return response.choices[0].message.content.strip()
    except openai.OpenAIError as e:
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


# Streamlit application
st.title("Mental Health Support Chatbot")

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

        response = generate_response(user_message)

        st.session_state['messages'].append(("Bot", response))
        st.session_state['mood_tracker'].append((user_message, sentiment, polarity))
        st.session_state.input_text = ""  # Clear the input after submission

st.text_input("You:", key="input_text", on_change=submit, label_visibility="collapsed")

# Display messages
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for sender, message in st.session_state['messages']:
    if sender == "You":
        st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{message}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Display mood tracking chart
if st.session_state['mood_tracker']:
    mood_data = pd.DataFrame(st.session_state['mood_tracker'], columns=["Message", "Sentiment", "Polarity"])
    st.line_chart(mood_data['Polarity'])

# Display coping strategies
if 'user_message' in locals() and user_message:
    st.write(f"Suggested Coping Strategy: {coping_strategy}")

# Display resources
st.sidebar.title("Resources")
st.sidebar.write("If you need immediate help, please contact one of the following resources:")
st.sidebar.write("1. National Suicide Prevention Lifeline: 1-800-273-8255")
st.sidebar.write("2. Crisis Text Line: Text 'HELLO' to 741741")
st.sidebar.write("3. SAMHSA’s National Helpline: 1-800-662-HELP (4357)")
st.sidebar.write("[More Resources](https://www.mentalhealth.gov/get-help/immediate-help)")

# Add guidelines for interacting with the chatbot
st.sidebar.title("How to Interact with the Chatbot")
st.sidebar.write("""
- Please enter at least 5 words.
- Include your feelings or emotions in the message.
- Be as specific as possible about your current situation or problems.
- Example: "I am feeling very anxious about my upcoming exams."
""")

# Display session summary
if st.sidebar.button("Show Session Summary"):
    st.sidebar.write("### Session Summary")
    for i, (message, sentiment, polarity) in enumerate(st.session_state['mood_tracker']):
        st.sidebar.write(f"{i + 1}. {message} - Sentiment: {sentiment} (Polarity: {polarity})")