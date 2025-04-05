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


---

![Screenshot 2025-04-05 152020](https://github.com/user-attachments/assets/a4b39b22-041f-4753-be0e-0bd9c7335b6a)
![Screenshot 2025-04-05 152051](https://github.com/user-attachments/assets/07d29f17-0d46-4483-a237-40eb5639f3ad)
![Screenshot 2025-04-05 152120](https://github.com/user-attachments/assets/2f70df0a-45b3-4ed5-ac6d-b5b3b39342e1)
