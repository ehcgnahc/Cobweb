from requests import get
from bs4 import BeautifulSoup
import target
from urllib.parse import urljoin
import sqlite3

# Connect to database
conn = sqlite3.connect('database.db')
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

headers = {
    "content-type": "text/html; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

for site in target.sites:
    print(f"正在解析: {site['school']} ({site['url']})")
    
    response = get(site["url"], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    extracted_data = []
    
    title_list = soup.select(site["selector"])
    for event in title_list:
        title = event.get("title", "").strip() or event.text.strip()
        link = urljoin(site["url"], event.get("href", ""))
        
        cursor.execute("INSERT INTO events (School, Title, Link) SELECT ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM events WHERE School = ? AND LINK = ?)", (site["school"], title, link, site["school"], link))
        extracted_data.append((title, link))
    
    conn.commit()
    
    for title, link in extracted_data:
        print(f"{title} → {link}")
    