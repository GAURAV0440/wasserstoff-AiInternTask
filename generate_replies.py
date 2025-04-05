import sqlite3
from transformers import pipeline

# Load FLAN-T5 model
reply_generator = pipeline("text2text-generation", model="google/flan-t5-base", max_length=150)

REPLYABLE_INTENTS = ["info request", "meeting request", "customer query"]
PROMO_KEYWORDS = ["sale", "offer", "discount", "subscribe", "unsubscribe", "newsletter", "limited time", "save"]

def is_promotional(summary, subject):
    subject = subject.lower()
    if subject.startswith("apply to jobs"):
        return True
    summary = summary.lower()
    return any(word in summary for word in PROMO_KEYWORDS)

def clean_reply(text):
    sentences = text.split(". ")
    unique_sentences = []
    for s in sentences:
        if s.strip() and s not in unique_sentences:
            unique_sentences.append(s)
    reply = ". ".join(unique_sentences).strip()
    return reply.replace("\n", " ").strip()

def generate_reply(summary, intent, subject):
    if is_promotional(summary, subject):
        return "🟡 This appears to be a promotional email. No reply is necessary."

    prompt = f"You received the following email summary:\n\n\"{summary}\"\n\nIntent: {intent}\nWrite a short, polite, and helpful reply to this email:"
    response = reply_generator(prompt)
    raw_reply = response[0]['generated_text'].strip()
    reply = clean_reply(raw_reply)

    if not reply or len(reply.split()) < 5 or "i'm sorry to hear" in reply.lower():
        return "⚠️ Couldn't generate a meaningful reply. Please check manually."

    return reply

def draft_replies():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject, summary, intent FROM emails")

    print("\n📬 Drafted Replies:\n")

    for msg_id, subject, summary, intent in cursor.fetchall():
        if not subject or not summary:
            continue

        try:
            reply = generate_reply(summary, intent, subject)

            cursor.execute("UPDATE emails SET draft_reply = ? WHERE id = ?", (reply, msg_id))
            conn.commit()

            print(f"Subject: {subject}")
            print(f"Intent: {intent}")
            print(f"Reply:\n{reply}")
            print("-" * 60)

        except Exception as e:
            print(f"❌ Error on {msg_id[:8]}: {e}")

    conn.close()
    print("\n✅ All replies generated and saved to DB!")

if __name__ == "__main__":
    draft_replies()