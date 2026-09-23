import json
import re
import requests

headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get("https://www.thepaper.cn/list_25429", timeout=25, headers=headers)
d = json.loads(
    re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text).group(1)
)
build_id = d["buildId"]
start = d["props"]["pageProps"]["data"]["startTime"]
ids = [x["contId"] for x in d["props"]["pageProps"]["data"]["list"][:3]]
print("first ids", ids, "start", start)

for q in [
    f"id=25429&startTime={start}",
    f"id=25429&pageNum=2",
    f"id=25429&excludeContIds={ids[0]}",
]:
    u = f"https://www.thepaper.cn/_next/data/{build_id}/list_25429.json?{q}"
    rr = requests.get(u, timeout=25, headers=headers)
    if rr.status_code != 200:
        print(q, rr.status_code)
        continue
    lst = rr.json()["pageProps"]["data"]["list"]
    print(q, "->", [x["contId"] for x in lst[:3]])
