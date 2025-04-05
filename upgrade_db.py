import sqlite3

conn = sqlite3.connect("emails.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE emails ADD COLUMN summary TEXT")
except sqlite3.OperationalError:
    print("✅ 'summary' column already exists")

try:
    cursor.execute("ALTER TABLE emails ADD COLUMN intent TEXT")
except sqlite3.OperationalError:
    print("✅ 'intent' column already exists")

conn.commit()
conn.close()

print("✅ Database upgraded successfully!")