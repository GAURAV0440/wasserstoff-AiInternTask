import sqlite3
from transformers import pipeline
from web_search import search_web

summarizer = pipeline("summarization", model="philschmid/distilbart-cnn-12-6-samsum")

def detect_intent(text):
    text = text.lower()
    if "?" in text or any(q in text for q in ["what is", "how", "can you", "who is", "when", "where"]):
        return "info request"
    elif "meeting" in text or "schedule" in text or "calendar" in text:
        return "meeting request"
    elif "apply" in text or "hiring" in text or "position" in text:
        return "job alert"
    elif "unsubscribe" in text or "newsletter" in text:
        return "newsletter"
    elif any(x in text for x in ["query", "question", "please help", "support"]):
        return "customer query"
    else:
        return "general update"

def update_emails():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, body FROM emails WHERE summary IS NULL OR intent IS NULL")

    for msg_id, body in cursor.fetchall():
        try:
            print(f"🧠 Analyzing email ID: {msg_id[:8]}...")
            intent = detect_intent(body)
            if len(body.split()) < 15:
                summary = body  # too short, just use the raw body
            else:
                summary = summarizer(body[:800], max_length=60, min_length=15, do_sample=False)[0]['summary_text']

            if intent == "info request":
                summary += f"\n\n🔍 Web Info: {search_web(body)}"

            cursor.execute("UPDATE emails SET summary=?, intent=? WHERE id=?", (summary.strip(), intent, msg_id))
            conn.commit()
        except Exception as e:
            print(f"❌ Error on {msg_id[:8]}: {e}")

    conn.close()
    print("✅ All emails analyzed!")

if __name__ == "__main__":
    update_emails()