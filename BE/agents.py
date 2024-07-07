import os
import base64
import yaml
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build, logger
from email import policy
from email.parser import BytesParser
from openai import OpenAI

# Load configuration from file
config_path = "/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/project/config.yaml"
oauth_client_secret_file = "/Users/ritachiblaq/Downloads/client_secret_868701777334-iftiplo2g719831dt8f6ah0kdi4cl2db.apps.googleusercontent.com.json"
config = yaml.safe_load(open(config_path))

# Initialize OpenAI client with API key
client = OpenAI(api_key=config['KEYS']['openai'])

# Authenticate and set up Gmail API using OAuth 2.0
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None

# Token file to store the user's access and refresh tokens
token_file = 'token.json'

# Check if token file exists and load credentials
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

# Build the Gmail API service
service = build('gmail', 'v1', credentials=creds)


def get_emails(last_email_id=None, user_id='me', query='in:sent', max_results=10):
    """
    Fetches emails from the user's Gmail account.

    Args:
        last_email_id (str): The ID of the last email fetched to avoid duplicates.
        user_id (str): The ID of the user (default is 'me' which refers to the authenticated user).
        query (str): The query string to filter emails.
        max_results (int): The maximum number of results to fetch.

    Returns:
        list: A list of dictionaries containing email data.
    """
    try:
        query_string = query
        if last_email_id:
            query_string += f' AND after:{last_email_id}'

        results = service.users().messages().list(userId=user_id, q=query_string, maxResults=max_results).execute()
        messages = results.get('messages', [])
        email_data = []

        for message in messages:
            msg = service.users().messages().get(userId=user_id, id=message['id'], format='raw').execute()
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
        logger.error(f"Error fetching emails: {e}")
        return []

def get_email_body(mime_msg):
    """
    Extracts the body of the email.

    Args:
        mime_msg (email.message.EmailMessage): The MIME message object.

    Returns:
        str: The email body.
    """
    if mime_msg.is_multipart():
        for part in mime_msg.iter_parts():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode(part.get_content_charset())
    else:
        return mime_msg.get_payload(decode=True).decode(mime_msg.get_content_charset())


def analyze_sentiment_and_tone(text):
    """
    Analyzes the sentiment and tone of the given text using OpenAI.

    Args:
        text (str): The text to analyze.

    Returns:
        str: The analysis result.
    """
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
    """
    Analyzes the mental health indications in the given text using OpenAI.

    Args:
        text (str): The text to analyze.

    Returns:
        str: The analysis result.
    """
    try:
        prompt = (
            "Please analyze the following email and identify any indications of mental health issues "
            "such as aggression, panic attacks, depression, anxiety, stress, or any other concerning behaviors. "
            "Provide a detailed analysis and identify specific sentences or phrases that suggest these issues.\n\n"
            f"Email: {text}"
        )
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ])
        analysis = response.choices[0].message.content.strip()
        return analysis
    except Exception as e:
        print(f"Error analyzing mental health: {e}")
        return f"Error: {e}"


def analyze_new_emails():
    """
    Fetches and analyzes new emails from the user's Gmail account.

    Returns:
        list: A list of dictionaries containing analyzed email data.
    """
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