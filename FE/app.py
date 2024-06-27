# app.py
import sys
sys.path.insert(0, '/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/project/Setup')
from Setup import agents
import pandas as pd
import streamlit as st
st.title("Mental Health Support Chatbot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'mood_tracker' not in st.session_state:
    st.session_state['mood_tracker'] = []

with st.form(key='chat_form'):
    user_message = st.text_input("You:").strip()
    submit_button = st.form_submit_button(label='Send') and user_message

if submit_button:
    st.session_state['messages'].append(("You", user_message))

    sentiment, polarity = agents.analyze_sentiment(user_message)
    coping_strategy = agents.provide_coping_strategy(sentiment)

    response = agents.generate_response(user_message)

    st.session_state['messages'].append(("Bot", response))
    st.session_state['mood_tracker'].append((user_message, sentiment, polarity))

for sender, message in st.session_state['messages']:
    if sender == "You":
        st.text(f"You: {message}")
    else:
        st.text(f"Bot: {message}")

# Display mood tracking chart
if st.session_state['mood_tracker']:
    mood_data = pd.DataFrame(st.session_state['mood_tracker'], columns=["Message", "Sentiment", "Polarity"])
    st.line_chart(mood_data['Polarity'])

# Display coping strategies
if user_message:
    st.write(f"Suggested Coping Strategy: {coping_strategy}")

# Display resources
st.sidebar.title("Resources")
st.sidebar.write("If you need immediate help, please contact one of the following resources:")
st.sidebar.write("1. National Suicide Prevention Lifeline: 1-800-273-8255")
st.sidebar.write("2. Crisis Text Line: Text 'HELLO' to 741741")
st.sidebar.write("[More Resources](https://www.mentalhealth.gov/get-help/immediate-help)")

# Display session summary
if st.sidebar.button("Show Session Summary"):
    st.sidebar.write("### Session Summary")
    for i, (message, sentiment, polarity) in enumerate(st.session_state['mood_tracker']):
        st.sidebar.write(f"{i+1}. {message} - Sentiment: {sentiment} (Polarity: {polarity})")
