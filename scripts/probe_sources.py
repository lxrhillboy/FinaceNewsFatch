import re
import urllib.request

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}

for name, url in [
    ("gov", "https://www.gov.cn/yaowen/liebiao/"),
    ("cs", "https://www.cs.com.cn/yaowen.html"),
    ("paper", "https://www.thepaper.cn/list_25429"),
]:
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    links = re.findall(r'href="([^"]+)"[^>]*>([^<]{5,80})</a>', html)
    print("===", name, "links", len(links))
    for h, t in links[:8]:
        print(t.strip()[:50], h[:60])
