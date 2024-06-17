import time

from Setup.agents import analyze_new_emails, analyze_sentiment_and_tone

# https://fastapi.tiangolo.com/tutorial/first-steps/

analyzed_emails = set()

while True:
    new_emails = analyze_new_emails()
    for email in new_emails:
        if email['id'] not in analyzed_emails:
            analysis = analyze_sentiment_and_tone(email['body'])
            print(f"Subject: {email['subject']}")
            print(f"Analysis: {analysis}\n")
            analyzed_emails.add(email['id'])

    time.sleep(60)  # Wait for 60 seconds before checking for new emails again

if __name__ == "__main__":
    main()
