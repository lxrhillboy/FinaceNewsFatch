import json
import re

import requests

session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
)

def get(url, **kw):
    r = session.get(url, timeout=25, **kw)
    r.raise_for_status()
    return r

# gov.cn
r = get("https://www.gov.cn/yaowen/liebiao/YAOWENLIEBIAO.json")
data = r.json()
print("gov items", len(data), data[0])

# cs.com.cn
r = get("https://www.cs.com.cn/yaowen.html")
html = r.text
print("cs encoding", r.encoding)
for m in re.finditer(r"href=['\"]([^'\"]+)['\"]", html):
    h = m.group(1)
    if "cs.com.cn" in h or h.startswith("/"):
        if "yaowen" in h or "xw" in h or "content" in h or re.search(r"/\d{4}/", h):
            print("cs link", h[:80])

# thepaper - try API
for u in [
    "https://api.thepaper.cn/contentapi/nodeContList?nodeId=25429&pageNum=1&pageSize=10",
    "https://cache.thepaper.cn/contentapi/nodeContList?nodeId=25429&pageNum=1&pageSize=10",
]:
    try:
        r = get(u)
        d = r.json()
        print("paper api", u, d.get("code"), list(d.keys()))
        lst = d.get("data", {}).get("list", d.get("data"))
        if isinstance(lst, list) and lst:
            print(" sample", lst[0].get("name"), lst[0].get("pubTime"))
    except Exception as e:
        print("paper api fail", u, e)

# yicai
try:
    r = get("https://www.yicai.com/api/ajax/getlist?page=1&pagesize=20")
    print("yicai", r.status_code, r.text[:300])
except Exception as e:
    print("yicai fail", e)

# cls
try:
    r = get("https://www.cls.cn/nodeapi/telegraphs?app=CailianpressWeb&os=web&sv=8.4.6&rn=10")
    d = r.json()
    roll = d.get("data", {}).get("roll_data", [])
    print("cls", len(roll), roll[0] if roll else d.keys())
except Exception as e:
    print("cls fail", e)

# nbd
try:
    r = get("https://economy.nbd.com.cn/columns/44/")
    print("nbd len", len(r.text))
except Exception as e:
    print("nbd fail", e)
