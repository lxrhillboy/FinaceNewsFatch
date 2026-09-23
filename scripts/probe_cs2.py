import re
import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})
for url in [
    "https://www.cs.com.cn/xwzx/jr/list.html",
    "https://www.cs.com.cn/xwzx/jr/",
]:
    r = session.get(url, timeout=25)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    print("===", url)
    for li in soup.select("li")[:20]:
        a = li.select_one("a")
        if not a:
            continue
        t = a.get_text(strip=True)
        h = a.get("href", "")
        span = li.select_one("span")
        d = span.get_text(strip=True) if span else ""
        if len(t) > 6:
            print(t[:45], h, d)
