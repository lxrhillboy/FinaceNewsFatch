import json
import re

import requests

r = requests.get(
    "https://www.thepaper.cn/list_25429",
    timeout=25,
    headers={"User-Agent": "Mozilla/5.0"},
)
m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text)
if m:
    d = json.loads(m.group(1))
    props = d.get("props", {}).get("pageProps", {})
    print("keys", props.keys())
    for k in props:
        v = props[k]
        if isinstance(v, dict):
            print(k, v.keys())
        elif isinstance(v, list):
            print(k, "list", len(v))
            if v:
                print(" sample", v[0].keys() if isinstance(v[0], dict) else v[0])
