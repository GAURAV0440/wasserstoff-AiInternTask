import os, base64, json, sqlite3
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_info(json.load(open('token.json')), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_email_body(payload):
    parts = payload.get("parts")
    if parts:
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    data = payload.get("body", {}).get("data")
    if data:
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    return "[No plain text body found]"

def init_db():
    conn = sqlite3.connect("emails.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS emails (
        id TEXT PRIMARY KEY,
        threadId TEXT,
        sender TEXT,
        subject TEXT,
        date TEXT,
        snippet TEXT,
        body TEXT
    )''')
    return conn

def store_email(conn, data):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO emails (id, threadId, sender, subject, date, snippet, body)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Skip duplicates


def fetch_and_store_emails(n=5):
    service = get_gmail_service()
    conn = init_db()
    results = service.users().messages().list(userId='me', maxResults=n).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_data['payload']
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), None)
        sender = next((h['value'] for h in headers if h['name'] == 'From'), None)
        date = next((h['value'] for h in headers if h['name'] == 'Date'), None)
        body = get_email_body(payload)
        snippet = msg_data.get("snippet", "")

        email_tuple = (
            msg_data['id'],
            msg_data['threadId'],
            sender,
            subject,
            date,
            snippet,
            body
        )
        store_email(conn, email_tuple)

    conn.close()
    print(f"✅ Stored latest {len(messages)} emails into emails.db")

if __name__ == "__main__":
    fetch_and_store_emails(n=5)