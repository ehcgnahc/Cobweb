import sys
import sqlite3
import target
import functions
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt

def setup_database(database, blacklist):
    database_conn = sqlite3.connect(database)
    blacklist_conn = sqlite3.connect(blacklist)
    database_cursor = database_conn.cursor()
    blacklist_cursor = blacklist_conn.cursor()

    database_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            School TEXT NOT NULL,
            Title TEXT UNIQUE NOT NULL,
            Title_Simplified TEXT UNIQUE NOT NULL,
            Link TEXT NOT NULL,
            UNIQUE (School, Link)
        )
        """
    )
    
    blacklist_cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS blacklist (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            School TEXT NOT NULL,
            Title TEXT UNIQUE NOT NULL,
            Title_Simplified TEXT UNIQUE NOT NULL,
            Link TEXT NOT NULL,
            UNIQUE (School, Link)
        )
        """
    )
    
    database_conn.commit()
    blacklist_conn.commit()
    return database_conn, database_cursor, blacklist_conn, blacklist_cursor

def get_events(site, headers):
    print(f"正在解析: {site['school']} ({site['url']})")
    
    response = get(site["url"], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    events = []
    
    title_list = soup.select(site["selector"])
    for event in title_list:
        title = event.get("title", "").strip() or event.text.strip()
        title_simplified = functions.normalize_text(title)
        link = urljoin(site["url"], event.get("href", ""))
        # title = re.sub(r"(\*\*|__)(.*?)\1", "r\1", title)
        
        events.append((site["school"], title, title_simplified, link))
    
    return events
    
def save_events_to_database(database_conn, database_cursor, blacklist_conn, blacklist_cursor, events):
    for school, title, title_simplified, link in events:
        try:
            database_cursor.execute(
                """
                INSERT INTO events (School, Title, Title_Simplified, Link)
                VALUES (?, ?, ?, ?)
                """,
                (school, title, title_simplified, link)
            )
        except sqlite3.IntegrityError:
            print(f"資料已存在: {school, title}")
    database_conn.commit()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AMONGUS")
        self.setGeometry(100, 100, 800, 600)

def main():
    try:
        database_conn, database_cursor, blacklist_conn, blacklist_cursor = setup_database('database.db', 'blacklist.db')
        
        headers = {
            "content-type": "text/html; charset=utf-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        
        for site in target.sites:
            events = get_events(site, headers)
            save_events_to_database(database_conn, database_cursor, blacklist_conn, blacklist_cursor, events)
        
        database_conn.close()
    
    except Exception as e:
        print(f"未成功連接到Database: {e}")
    
if __name__ == "__main__":
    main()