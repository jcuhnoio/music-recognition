import sqlite3

conn = sqlite3.connect('./db/fingerprints.db')
cursor = conn.cursor()

with open('./db/schema.sql', 'r') as f:
    cursor.executescript(f.read())

conn.commit()
conn.close()

print("Database and tables created ✅")
