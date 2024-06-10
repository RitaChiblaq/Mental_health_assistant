import os
from http import client

import config
from openai import OpenAI

import yaml
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email import message_from_bytes, policy
from email.parser import BytesParser

# Load configuration
config_path = "/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/Mental_health_assistant/config.yaml"
oauth_client_secret_file = "/Users/ritachiblaq/Downloads/client_secret_868701777334-iftiplo2g719831dt8f6ah0kdi4cl2db.apps.googleusercontent.com.json"

try:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        if not isinstance(config, dict):
            raise ValueError("Config file is not properly formatted.")
except Exception as e:
    print(f"Error loading config file: {e}")
    raise

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
        flow = InstalledAppFlow.from_client_secrets_file(
            oauth_client_secret_file, SCOPES
        )
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

def analyze_sentiment(text):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Analyze the sentiment of this text: {text}"}
        ])
        sentiment = response.choices[0].message.content.strip()
        return sentiment
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "Error"

emails = get_emails(query='in:sent')

for email in emails:
    sentiment = analyze_sentiment(email['body'])
    print(f"Subject: {email['subject']}")
    print(f"Sentiment: {sentiment}\n")
