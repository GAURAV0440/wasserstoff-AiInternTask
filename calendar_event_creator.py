import json
import os
import sqlite3
import re
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('calendar_token.json'):
        creds = Credentials.from_authorized_user_info(json.load(open('calendar_token.json')), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('calendar_token.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def extract_date(text):
    match = re.search(r"(?:on\s)?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)", text, re.IGNORECASE)
    if match:
        day = match.group(1).capitalize()
        today = datetime.today()
        for i in range(7):
            date = today + timedelta(days=i)
            if date.strftime("%A") == day:
                return date
    return datetime.today() + timedelta(days=1)  # fallback: tomorrow

def create_calendar_event(service, subject, body, start_time):
    event = {
        'summary': subject,
        'description': body[:500],
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': (start_time + timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    created = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Event created: {created.get('htmlLink')}")

def process_meeting_emails():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT subject, body FROM emails WHERE intent='meeting request'")

    service = get_calendar_service()

    for subject, body in cursor.fetchall():
        try:
            meeting_date = extract_date(body)
            create_calendar_event(service, subject, body, meeting_date.replace(hour=11, minute=0))
        except Exception as e:
            print(f"❌ Could not create event: {e}")

    conn.close()

if __name__ == "__main__":
    process_meeting_emails()