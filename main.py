from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import re
import target

def setup_database(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            School TEXT NOT NULL,
            Title TEXT NOT NULL,
            Link TEXT NOT NULL
        )
        """
    )

    conn.commit()
    return conn, cursor

def get_events(site, headers):
    print(f"正在解析: {site['school']} ({site['url']})")
    
    response = get(site["url"], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    events = []
    
    title_list = soup.select(site["selector"])
    for event in title_list:
        title = event.get("title", "").strip() or event.text.strip()
        link = urljoin(site["url"], event.get("href", ""))
        # title = re.sub(r"(\*\*|__)(.*?)\1", "r\1", title)
        
        events.append((site["school"], title, link))
    
    return events

def save_events_to_database(cursor, conn, events):
    for school, title, link in events:
        cursor.execute(
            """
            INSERT INTO events (School, Title, Link)
            SELECT ?, ?, ? WHERE NOT EXISTS (
                SELECT 1 FROM events WHERE School = ? AND LINK = ?
            )
            """
            , (school, title, link, school, link)
        )
    conn.commit()

def main():
    conn, cursor = setup_database('database.db')
    
    headers = {
        "content-type": "text/html; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    for site in target.sites:
        events = get_events(site, headers)
        save_events_to_database(cursor, conn, events)
    
    conn.close()
    
if __name__ == "__main__":
    main()