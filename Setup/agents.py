import openai
import yaml
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email import message_from_bytes

# Load configuration
config = yaml.safe_load(open("/Users/ritachiblaq/Library/CloudStorage/OneDrive-Personal/HTW/4.Semester/Unternehmenssoftware/Assignments/Mental_health_assistant/config.yaml"))

# Set up OpenAI API
openai.api_key = config['KEYS']['openai']

# Authenticate and set up Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SERVICE_ACCOUNT_FILE = '/Users/ritachiblaq/Downloads/mental-health-assistant-425320-b96a4704a659.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('gmail', 'v1', credentials=credentials)

# Function to get email data
def get_emails(user_id, query='', max_results=10):
    results = service.users().messages().list(userId=user_id, q=query, maxResults=max_results).execute()
    messages = results.get('messages', [])
    email_data = []

    for message in messages:
        msg = service.users().messages().get(userId=user_id, id=message['id'], format='raw').execute()
        msg_str = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
        mime_msg = message_from_bytes(msg_str)
        email_data.append({
            'subject': mime_msg['subject'],
            'from': mime_msg['from'],
            'to': mime_msg['to'],
            'body': mime_msg.get_payload()
        })

    return email_data

# Function to analyze sentiment using OpenAI
def analyze_sentiment(text):
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=f"Analyze the sentiment of this text: {text}",
        max_tokens=60
    )
    sentiment = response.choices[0].text.strip()
    return sentiment

# Create an assistant
assistant = openai.beta.assistants.create(
    name="Behavioral Email Analyst",
    instructions="You analyze email history to recognize user emotions, writing styles, and behavioral changes.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4"
)

assistant_id = assistant.id

# Once created, you can always find your assistant at:
# https://platform.openai.com/assistants

# Create a thread (representing a conversation)
thread = openai.beta.threads.create()

# Add a message to the thread
message = openai.beta.threads.runs.create (
    thread_id=thread.id,
    role="user",
    content="Please analyze my recent email conversations and provide insights."
)

# Fetch and analyze emails
emails = get_emails('me')
for email in emails:
    sentiment = analyze_sentiment(email['body'])
    print(f"Subject: {email['subject']}")
    print(f"Sentiment: {sentiment}\n")

    # Add email content to the thread
    message = openai.Thread.message.create(
        thread_id=thread.id,
        role="user",
        content=email['body']
    )

# Run the assistant
run = openai.Thread.run.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
    instructions="Analyze the provided emails and provide a summary of emotional trends and behavioral changes."
)

# Check run status
finished = False
while not finished:
    run = openai.Thread.run.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run.status != "in_progress":
        finished = True

# Display the assistant's response
messages = openai.Thread.message.list(
    thread_id=thread.id
)
for message in messages:
    print(message.content)

# Get run steps to see the assistant's inner workings
run_steps = openai.Thread.run.steps.list(
    thread_id=thread.id,
    run_id=run.id
)
print(run_steps.data[1].step_details.tool_calls[0].code_interpreter.input)
