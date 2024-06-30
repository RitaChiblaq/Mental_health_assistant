import os
import base64
import time
from textblob import TextBlob
import yaml
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email import policy
from email.parser import BytesParser
from openai import OpenAI


# Load configuration
config_path = "/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/project/config.yaml"
oauth_client_secret_file = "/Users/ritachiblaq/Downloads/client_secret_868701777334-iftiplo2g719831dt8f6ah0kdi4cl2db.apps.googleusercontent.com.json"
config = yaml.safe_load(open(config_path))
client = OpenAI(api_key=config['KEYS']['openai'])
# Set up OpenAI API key

# Authenticate and set up Gmail API using OAuth 2.0
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None

# Token file to store the user's access and refresh tokens
token_file = 'token.json'

# Check if token file exists
if os.path.exists(token_file):
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)

# If there are no valid credentials, prompt the user to log in
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(oauth_client_secret_file, SCOPES)
        creds = flow.run_local_server(port=8080)

    # Save the credentials for the next run
    with open(token_file, 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)


def get_emails(user_id='me', query='in:sent', max_results=10):
    try:
        results = service.users().messages().list(userId=user_id, q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        email_data = []

        for message in messages:
            msg = service.users().messages().get(userId=user_id, id=message['id'], format='raw').execute()
            msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            mime_msg = BytesParser(policy=policy.default).parsebytes(msg_str)
            email_data.append({
                'subject': mime_msg['subject'],
                'from': mime_msg['from'],
                'to': mime_msg['to'],
                'body': get_email_body(mime_msg)
            })

        return email_data
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []


def get_email_body(mime_msg):
    if mime_msg.is_multipart():
        for part in mime_msg.iter_parts():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        return mime_msg.get_payload(decode=True).decode(mime_msg.get_content_charset())


def analyze_sentiment_and_tone(text):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Analyze the sentiment, the emotions and tone of this text: {text}"}
        ])
        analysis = response.choices[0].message.content.strip()
        return analysis
    except Exception as e:
        print(f"Error analyzing sentiment and tone: {e}")
        return f"Error: {e}"

def analyze_mental_health(text):
    try:
        prompt = (
            "Please analyze the following email and identify any indications of mental health issues "
            "such as aggression, panic attacks, depression, anxiety, stress, or any other concerning behaviors. "
            "Provide a detailed analysis and identify specific sentences or phrases that suggest these issues.\n\n"
            f"Email: {text}"
        )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        analysis = response['choices'][0]['message']['content'].strip()
        return analysis
    except Exception as e:
        print(f"Error analyzing mental health: {e}")
        return f"Error: {e}"


def analyze_new_emails():
    try:
        # Get the list of sent emails
        results = service.users().messages().list(userId='me', q='in:sent', maxResults=10).execute()
        messages = results.get('messages', [])
        email_data = []

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
            msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
            mime_msg = BytesParser(policy=policy.default).parsebytes(msg_str)
            email_data.append({
                'id': message['id'],
                'subject': mime_msg['subject'],
                'from': mime_msg['from'],
                'to': mime_msg['to'],
                'body': get_email_body(mime_msg)
            })

        return email_data
    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []

# Function to generate a response from GPT-3
def generate_response(prompt):
    try:
        response = client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except client.OpenAIError as e:
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
