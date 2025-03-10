import sqlite3

conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS events")
conn.commit()