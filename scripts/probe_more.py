import json
import re

import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})

# CS finance list
r = session.get("https://www.cs.com.cn/xwzx/jr/list.html", timeout=25)
r.encoding = r.apparent_encoding or "utf-8"
html = r.text
print("cs jr len", len(html))
links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]{4,60})</a>', html)
for h, t in links[:15]:
    if "list" not in h or "content" in h:
        print(t.strip()[:40], h[:70])

# yicai news list page
r = session.get("https://www.yicai.com/news/", timeout=25)
print("yicai news", r.status_code, len(r.text))
m = re.search(r"__NEXT_DATA__.*?>({.*?})</script>", r.text)
if m:
    d = json.loads(m.group(1))
    print("next keys", d.keys())

# try yicai api patterns
for u in [
    "https://www.yicai.com/api/ajax/getlist?cid=48&page=1&pagesize=20",
    "https://www.yicai.com/api/ajax/getjuhelist?cid=48&page=1&pagesize=20",
]:
    try:
        r = session.get(u, timeout=15)
        print(u, r.status_code, r.text[:200])
    except Exception as e:
        print(u, e)

# thepaper from HTML
r = session.get("https://www.thepaper.cn/list_25429", timeout=25)
html = r.text
print("paper len", len(html))
# look for contId
ids = re.findall(r"/newsDetail_forward_(\d+)", html)
print("paper ids", len(ids), ids[:5])
titles = re.findall(r'"name":"([^"]{10,80})"', html)
print("paper titles sample", titles[:5])
