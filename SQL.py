import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """
)

cursor.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin')")
# cursor.execute("Delete FROM users")
conn.commit()

cursor.execute("SELECT * FROM admin")
print(cursor.fetchall())

cursor.close()