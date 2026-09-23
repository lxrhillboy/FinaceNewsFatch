import re
import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})
url = "https://www.gov.cn/yaowen/liebiao/202609/content_7081833.htm"
r = session.get(url, timeout=25)
r.encoding = "utf-8"
for pat in ["UCAP", "pages_content", "TRS_Editor", "content", "article"]:
    if pat in r.text:
        print("has", pat)
# print snippet around pages_content
i = r.text.find("pages_content")
if i >= 0:
    print(r.text[i : i + 500])
