import json
import re
import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})
cid = "34130338"
for u in [
    f"https://www.thepaper.cn/newsDetail_forward_{cid}",
    f"https://m.thepaper.cn/newsDetail_forward_{cid}",
]:
    try:
        r = session.get(u, timeout=25)
        print(u, r.status_code, len(r.text))
        m = re.search(r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\});", r.text)
        if m:
            print("initial state found", len(m.group(1)))
        m2 = re.search(r'"content":"((?:\\.|[^"\\])*)"', r.text)
        if m2:
            raw = m2.group(1)[:200]
            print("content snippet", raw)
    except Exception as e:
        print(u, e)

for api in [
    f"https://api.thepaper.cn/contentapi/cont/detail/{cid}",
    f"https://www.thepaper.cn/contentapi/cont/detail/{cid}",
]:
    try:
        r = session.get(api, timeout=20)
        print("api", api, r.status_code, r.text[:300])
    except Exception as e:
        print("api fail", api, e)
