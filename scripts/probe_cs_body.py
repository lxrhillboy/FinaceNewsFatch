import requests
from bs4 import BeautifulSoup

url = "https://www.cs.com.cn/xwzx/jr/2026/09/21/detail_2026092110040682.html"
r = requests.get(url, timeout=25)
r.encoding = r.apparent_encoding or "utf-8"
soup = BeautifulSoup(r.text, "lxml")
print("title", soup.title.get_text() if soup.title else None)
for sel in [
    ".article-content",
    ".Custom_UnionStyle",
    "#ContentBody",
    ".content",
    ".detail-content",
    ".main-article",
    "article",
]:
    n = soup.select_one(sel)
    if n:
        print(sel, len(n.get_text(strip=True)))

# fallback: longest p container
divs = sorted(soup.select("div"), key=lambda x: len(x.get_text(strip=True)), reverse=True)
for d in divs[:5]:
    cls = d.get("class")
    print("div", cls, len(d.get_text(strip=True)))
