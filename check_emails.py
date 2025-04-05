import sqlite3

conn = sqlite3.connect("emails.db")
cursor = conn.cursor()

# Set the intent of the latest email to 'meeting request'
cursor.execute("UPDATE emails SET intent = 'meeting request' WHERE id = (SELECT id FROM emails LIMIT 1)")
conn.commit()
conn.close()

print("✅ Manually updated 1 email as 'meeting request'")
