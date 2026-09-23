import re
import urllib.request

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
for u in [
    "https://www.gov.cn/yaowen/liebiao/",
    "https://www.gov.cn/yaowen/liebiao/index.htm",
]:
    try:
        req = urllib.request.Request(u, headers=headers)
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
        print("URL", u, "len", len(html))
        for pat in ["listArrP", "getJSON", "content_", "yaowen"]:
            print(pat, html.count(pat))
        m = re.search(r"var\s+listArrP\s*=\s*(\[.*?\]);", html, re.S)
        if m:
            print("found listArrP", m.group(1)[:200])
        urls = re.findall(r"https?://www\.gov\.cn/[^\s\"']+content_\d+\.htm", html)
        print("content urls", len(urls), urls[:3])
    except Exception as e:
        print(u, e)
