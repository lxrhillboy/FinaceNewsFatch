import re
import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})
r = session.get("https://www.cs.com.cn/xwzx/jr/list.html", timeout=25)
r.encoding = "utf-8"
html = r.text
for pat in [".json", "getList", "ajax", "listData"]:
    idx = html.find(pat)
    if idx >= 0:
        print(pat, html[idx : idx + 200])
urls = re.findall(r"https?://[^\"'\s]+", html)
jsons = [u for u in urls if ".json" in u or "api" in u]
print("json urls", jsons[:10])
