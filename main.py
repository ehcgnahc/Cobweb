from requests import get
from bs4 import BeautifulSoup
import target

headers = {
    "content-type": "text/html; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

for site in target.sites:
    print(site["school"])
    response = get(site["url"], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_list = soup.select(".card-title a[title]")
    for events in title_list:
        title = events["title"]
        link = events["href"]
        print(title, "https://csie.yuntech.edu.tw" + link)
    

