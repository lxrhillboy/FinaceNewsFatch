import re
import urllib.request

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
req = urllib.request.Request("https://www.cs.com.cn/yaowen.html", headers=headers)
html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
print("len", len(html))
for pat in [".json", "ajax", "api", "list"]:
    if pat in html:
        print(pat, "yes")
# find article links
links = re.findall(r'href="(//www\.cs\.com\.cn/[^"]+)"', html)
links += re.findall(r'href="(https://www\.cs\.com\.cn/[^"]+)"', html)
print("links", len(set(links)))
for x in list(set(links))[:10]:
    print(x)
