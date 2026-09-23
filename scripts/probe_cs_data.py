import json
import re
import requests

base = "https://www.cs.com.cn/js/9903/"
for name in ["mi4_sub_articles_top.js", "mi4_sub_articles_20260921.js"]:
    t = requests.get(base + name, timeout=25).text
    print("===", name, "len", len(t))
    print(t[:300])
    m = re.search(r"var\s+MI4_PAGE_ARTICLE\s*=\s*(\[.*?\]);", t, re.S)
    m2 = re.search(r"var\s+MI4_SUB_ARTICLES\s*=\s*(\[.*?\]);", t, re.S)
    for label, m in [("PAGE_ARTICLE", m), ("SUB", m2)]:
        if m:
            data = json.loads(m.group(1))
            print(label, "items", len(data), data[0].keys())
            print(data[0])
