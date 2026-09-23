import re
import requests

u = "https://www.cs.com.cn/js/9903/mi4_page_articles_guide.js"
t = requests.get(u, timeout=25).text
print("len", len(t))
print(t[:800])
urls = re.findall(r"https?://[^\"'\s]+", t)
print("urls", urls[:20])
for kw in ["api", "article", "list", "mi4"]:
    if kw in t:
        print("has", kw)
