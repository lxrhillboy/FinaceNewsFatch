import json
import re

import requests

r = requests.get(
    "https://www.thepaper.cn/newsDetail_forward_34130338",
    timeout=25,
    headers={"User-Agent": "Mozilla/5.0"},
)
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text)
if not m:
    print("no next data")
    raise SystemExit(1)
d = json.loads(m.group(1))
props = d.get("props", {}).get("pageProps", {})
print("pageProps keys", props.keys())
for k, v in props.items():
    if isinstance(v, dict):
        print(" dict", k, list(v.keys())[:15])
        if "content" in v:
            print(" content len", len(str(v["content"])))
        if "name" in v:
            print(" name", v.get("name"))

cd = props.get("detailData", {}).get("contentDetail", {})
print("contentDetail keys", cd.keys())
print("title", cd.get("name"))
content = cd.get("content") or ""
print("content preview", content[:300])
print("pub", cd.get("pubTime"), cd.get("publishTime"))
