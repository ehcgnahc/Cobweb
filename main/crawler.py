from requests import get
from bs4 import BeautifulSoup
from urllib import parse
import functions

def get_events(site, headers):
    print(f"正在解析: {site['school']} ({site['url']})")
    
    response = get(site["url"], headers=headers, timeout=5)
    soup = BeautifulSoup(response.text, 'html.parser')

    events = []
    title_list = soup.select(site["selector"])

    for event in title_list:
        title = event.get("title", "").strip() or event.text.strip()
        title_simplified = functions.normalize_text(title)
        link = parse.urljoin(site["url"], event.get("href", ""))
        
        # print (title, link)
        events.append((site["school"], title, title_simplified, link))
    
    return events
