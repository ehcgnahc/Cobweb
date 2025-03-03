import requests
from bs4 import BeautifulSoup

headers = {
    "content-type": "text/html; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.get('https://csie.yuntech.edu.tw/index.php/newsclass', headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

title_list = soup.select(".card-title a[title]")
for news in title_list:
    title = news["title"]
    link = news["href"]
    print(title, "https://csie.yuntech.edu.tw" + link)
