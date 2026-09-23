import re
import urllib.request

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
req = urllib.request.Request("https://www.gov.cn/yaowen/liebiao/", headers=headers)
html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
for key in ["getFYDataFn", "FY_DATA", "ajax", "json"]:
    idx = 0
    count = 0
    while count < 3:
        i = html.find(key, idx)
        if i < 0:
            break
        print("---", key, "at", i)
        print(html[i : i + 400])
        idx = i + len(key)
        count += 1
