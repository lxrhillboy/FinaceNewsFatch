import json
import re
import requests
from bs4 import BeautifulSoup

t = requests.get(
    "https://www.cs.com.cn/js/9903/mi4_sub_articles_20260921.js", timeout=25
).text
start = t.find("[")
end = t.rfind("]") + 1
item = json.loads(t[start:end])[0]
print(item)
url = item.get("url")
if url and not url.startswith("http"):
    url = "https://www.cs.com.cn" + url
print("url", url)
if url:
    r = requests.get(url, timeout=25)
    r.encoding = r.apparent_encoding or "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    for sel in [".article-content", ".Custom_UnionStyle", "#ContentBody", ".content"]:
        n = soup.select_one(sel)
        if n:
            print(sel, n.get_text(strip=True)[:150])
