import base64
import sqlite3
import json
import os
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://mail.google.com/']
TOKEN_FILE = 'token_send.json'
SAFE_INTENTS = ["info request", "meeting request", "customer query"]
LOG_FILE = "sent_reply_log.txt"

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_info(json.load(open(TOKEN_FILE)), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(to, subject, body, thread_id):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw, 'threadId': thread_id}

def log_sent_reply(sender, subject, reply):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"TO: {sender}\nSUBJECT: Re: {subject}\nREPLY:\n{reply}\n{'-'*60}\n")

def send_replies():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, threadId, sender, subject, draft_reply, intent FROM emails")
    emails = cursor.fetchall()
    conn.close()

    service = get_gmail_service()
    sent_count = 0

    for eid, threadId, sender, subject, reply, intent in emails:
        if intent not in SAFE_INTENTS:
            continue
        if not reply or reply.startswith("🟡") or reply.startswith("⚠️"):
            continue

        print(f"\n📨 Ready to send to: {sender}")
        print(f"Subject: Re: {subject}")
        print(f"Reply:\n{reply}")
        confirm = input("✅ Send this reply? (y/n): ").strip().lower()

        if confirm == "y":
            try:
                msg = create_message(sender, f"Re: {subject}", reply, threadId)
                service.users().messages().send(userId="me", body=msg).execute()
                print(f"✅ Sent reply to: {sender}")
                log_sent_reply(sender, subject, reply)
                sent_count += 1
            except Exception as e:
                print(f"❌ Failed to send reply to {sender}: {e}")
        else:
            print("⏭️ Skipped.")

    print(f"\n📨 Total Replies Sent: {sent_count}")
    print(f"📝 Log saved to {LOG_FILE}")

if __name__ == "__main__":
    send_replies()