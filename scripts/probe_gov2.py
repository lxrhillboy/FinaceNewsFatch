import re
import urllib.request

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
req = urllib.request.Request("https://www.gov.cn/yaowen/liebiao/", headers=headers)
html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
scripts = re.findall(r'<script[^>]+src="([^"]+)"', html)
print("scripts", len(scripts))
for s in scripts:
    print(s)
# inline script snippets around listArrP
idx = html.find("listArrP")
print(html[idx - 500 : idx + 800])
