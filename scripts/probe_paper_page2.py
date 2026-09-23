import json
import re
import requests

r = requests.get(
    "https://www.thepaper.cn/list_25429?page=2",
    timeout=25,
    headers={"User-Agent": "Mozilla/5.0"},
)
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text)
d = json.loads(m.group(1))
data = d["props"]["pageProps"]["data"]
print("page", data.get("pageNum"), "items", len(data.get("list", [])))
