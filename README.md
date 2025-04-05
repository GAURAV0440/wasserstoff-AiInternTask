# 🤖 AI Email Assistant – Wasserstoff

This is an intelligent assistant that reads emails from Gmail, summarizes and understands the content using AI, generates smart replies, creates calendar events for meetings and sends only safe replies with user confirmation. It also features a simple Streamlit dashboard to review all emails and their actions.


## Technologies Used

- **Python 3.10+**
- **Hugging Face Transformers** – for summarization and reply generation (FLAN-T5, BART)
- **Gmail API & Google Calendar API**
- **Streamlit** – for dashboard UI
- **SQLite** – for local email database
- **Serper.dev (Google Search API)** – for info enrichment
- **OAuth 2.0** – for secure Gmail & Calendar access


## 🧠 How It Works

1. **Reads Emails**: Uses Gmail API to fetch the latest emails
2. **Summarizes & Understands**: Summarizes emails and detects intent using LLM
3. **Handles Info Requests**: Uses web search if email asks a question
4. **Generates Smart Replies**: With FLAN-T5 for selected intents
5. **Skips Unsafe Emails**: Promotional/spam/vague emails are skipped
6. **Sends Confirmed Replies**: User confirms each reply before it's sent
7. **Books Calendar Events**: Creates meetings via Google Calendar API
8. **Dashboard View**: Streamlit UI to view processed emails and replies


## Run in this order:

python upgrade_db.py              # Setup DB

python email_reader.py           # Fetch Gmail emails

python analyze_emails.py         # Summarize + detect intent

python generate_replies.py       # Generate safe replies

python calendar_event_creator.py # Optional: add meetings

python send_replies.py           # Confirm + send replies

streamlit run app.py


## Libraries used:

transformers – for summarizing emails and generating replies using FLAN-T5 and BART models

google-api-python-client – to access Gmail and Google Calendar APIs

google-auth, google-auth-oauthlib – to handle Google login securely

python-dotenv – to load secret API key from the .env file

requests – to fetch web search results from Serper.dev

streamlit – to create a simple dashboard

sqlite3 (built-in) – to store email data locally

base64, json, os, datetime (built-in) – for data handling and email formatting

## APIs and external tools:

Gmail API – to fetch and send emails

Google Calendar API – to schedule meetings

Hugging Face Transformers – to summarize and generate replies

Serper.dev – to perform web search for info request emails


---

![Screenshot 2025-04-05 152020](https://github.com/user-attachments/assets/a4b39b22-041f-4753-be0e-0bd9c7335b6a)
![Screenshot 2025-04-05 152051](https://github.com/user-attachments/assets/07d29f17-0d46-4483-a237-40eb5639f3ad)
![Screenshot 2025-04-05 152120](https://github.com/user-attachments/assets/2f70df0a-45b3-4ed5-ac6d-b5b3b39342e1)
