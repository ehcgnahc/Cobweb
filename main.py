import sys
import sqlite3
import target
import functions
from requests import get
from bs4 import BeautifulSoup
from urllib import parse
from PyQt5 import QtWidgets

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
        link = parse.urljoin(site["url"], event.get("href", ""))
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


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('CobWeb')
        self.resize(600, 400)
        self.setStyleSheet("#MainWindow { background-color: #fcc; }")
        self.selection_box = self.Selection_Box()
        self.info = self.INFO()

    def Selection_Box(self):
        selection_box = QtWidgets.QComboBox(self)
        selection_box.addItem("請選擇學校")
        selection_box.addItem("ALL")
        for site in target.sites: 
            selection_box.addItem(site['school'])
        selection_box.setGeometry(10, 10, 200, 30)
        selection_box.move(50, 50)
        selection_box.currentIndexChanged.connect(self.Selection_Changed)
        return selection_box
    
    def INFO(self):
        info = QtWidgets.QLabel(self)
        info.move(200, 100)
        info.setText(self.selection_box.currentText())
        info.setStyleSheet("color: #00c; font-size: 20px;")
        return info

    def Selection_Changed(self):
        self.info.setText(self.selection_box.currentText())

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
    # main()
    app = QtWidgets.QApplication(sys.argv)
    Window = App()
    Window.show()
    sys.exit(app.exec_())