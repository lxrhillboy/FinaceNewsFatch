import json
import re
import requests

r = requests.get(
    "https://www.thepaper.cn/list_25429",
    timeout=25,
    headers={"User-Agent": "Mozilla/5.0"},
)
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text)
d = json.loads(m.group(1))
item = d["props"]["pageProps"]["data"]["list"][0]
print(item.keys())
print(item)
