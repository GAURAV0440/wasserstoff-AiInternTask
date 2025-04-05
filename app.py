import streamlit as st
import sqlite3

def get_emails():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, sender, subject, summary, intent, draft_reply, body FROM emails")
    records = cursor.fetchall()
    conn.close()
    return records

st.title("Email Assistant Dashboard")

emails = get_emails()

if emails:
    for email in emails:
        id, sender, subject, summary, intent, draft_reply, body = email
        with st.expander(f"{subject} — {sender}"):
            st.write("**Summary:**", summary)
            st.write("**Intent:**", intent)
            st.write("**Draft Reply:**", draft_reply)
            st.write("**Email Body:**")
            st.text(body)
else:
    st.write("No emails found in the database.")