import sqlite3

conn = sqlite3.connect('data/database.db')
cursor = conn.cursor()

# cursor.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin')")
# cursor.execute("Delete FROM users")
# conn.commit()

# cursor.execute("SELECT * FROM events")
# print(cursor.fetchall())

# cursor.execute("DROP TABLE IF EXISTS events")
# conn.commit()

# cursor.execute("SELECT * FROM events WHERE School = 'NTU' AND Link = 'https://csie.ntu.edu.tw/zh_tw/Announcements/Announcement9/%5B%E6%B4%BB%E5%8B%95%5D%C2%A022%E5%B1%86%E8%82%B2%E7%A7%80%E7%9B%83%E5%89%B5%E6%84%8F%E7%8D%8E%E7%AB%B6%E8%B3%BD-%E3%80%8A%E6%95%B8%E4%BD%8D%E6%87%89%E7%94%A8-%E5%B7%A5%E6%A5%AD%E8%A8%AD%E8%A8%88-%E6%94%B6%E4%BB%B6%E5%80%92%E6%95%B8-%E3%80%8B%E9%A6%96%E7%8D%8E20%E8%90%AC%E5%85%83-%E6%AD%A1%E8%BF%8E%E6%8A%95%E4%BB%B6-73291116'")
cursor.execute("SELECT * FROM events WHERE School = 'NTU'")
tables = cursor.fetchall()

for table in tables:
    print(table)

cursor.close()