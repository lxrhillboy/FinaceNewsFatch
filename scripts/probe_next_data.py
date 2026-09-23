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
build_id = d.get("buildId")
print("buildId", build_id)
data = d["props"]["pageProps"]["data"]
print(
    {
        k: data[k]
        for k in [
            "pageNum",
            "pages",
            "total",
            "nextPageNum",
            "startTime",
            "hasNext",
        ]
    }
)

if build_id:
    for page in [2, 3]:
        u = f"https://www.thepaper.cn/_next/data/{build_id}/list_25429.json?id=25429&page={page}"
        rr = requests.get(u, timeout=25, headers={"User-Agent": "Mozilla/5.0"})
        print("next data", page, rr.status_code)
        if rr.status_code == 200:
            dd = rr.json()["pageProps"]["data"]
            print(" items", len(dd.get("list", [])), "pageNum", dd.get("pageNum"))
