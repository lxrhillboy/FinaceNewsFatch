import json
import re

import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})

# gov article
url = "https://www.gov.cn/yaowen/liebiao/202609/content_7081833.htm"
r = session.get(url, timeout=25)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "lxml")
title = soup.select_one("h1")
print("gov title", title.get_text(strip=True) if title else None)
for sel in ["#UCAP-CONTENT", ".pages_content", ".article"]:
    node = soup.select_one(sel)
    if node:
        print("gov body sel", sel, node.get_text(strip=True)[:120])

# thepaper article
cid = "34130338"
r = session.get(f"https://www.thepaper.cn/newsDetail_forward_{cid}", timeout=25)
html = r.text
m = re.search(r'"content":"([^"]*)"', html)
m2 = re.search(r'"pubTime":"([^"]*)"', html)
print("paper pub", m2.group(1) if m2 else None)
print("paper content", (m.group(1)[:120] if m else None))

# yicai juhelist item detail
r = session.get(
    "https://www.yicai.com/api/ajax/getjuhelist?cid=48&page=1&pagesize=5", timeout=25
)
items = r.json()
item = items[0]
print("yicai keys", item.keys())
news_id = item.get("NewsID") or item.get("EntityId")
link = item.get("url") or item.get("Url")
print("yicai item", item.get("NewsTitle"), news_id, link)
if link:
    if not link.startswith("http"):
        link = "https://www.yicai.com" + link
    r = session.get(link, timeout=25)
    soup = BeautifulSoup(r.text, "lxml")
    for sel in [".m-txt", "#multi-text", "article"]:
        n = soup.select_one(sel)
        if n:
            print("yicai body", sel, n.get_text(strip=True)[:120])
            break

# cs list page structure
r = session.get("https://www.cs.com.cn/xwzx/jr/list.html", timeout=25)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "lxml")
for a in soup.select("a")[:30]:
    t = a.get_text(strip=True)
    h = a.get("href", "")
    if len(t) > 8 and "list" not in h:
        print("cs", t[:40], h)
