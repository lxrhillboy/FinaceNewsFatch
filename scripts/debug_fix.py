from news_fetcher.http import HttpClient
from bs4 import BeautifulSoup
import re

html = HttpClient().get_text(
    "https://www.gov.cn/yaowen/liebiao/202609/content_7081833.htm",
    encoding="utf-8",
)
print("UCAP in raw", "UCAP-CONTENT" in html)
soup = BeautifulSoup(html, "html.parser")
node = soup.find(id="UCAP-CONTENT")
print("html.parser node", bool(node), len(node.get_text()) if node else 0)

guide = HttpClient().get_text("https://www.cs.com.cn/js/9903/mi4_page_articles_guide.js")
idx = guide.find("PAGE_INDEX_MAP")
print("idx", idx, guide[idx : idx + 80])
start = guide.find("{", idx)
depth = 0
end = start
for i, ch in enumerate(guide[start:], start=start):
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0:
            end = i
            break
import json

mapping = json.loads(guide[start : end + 1])
print("map size", len(mapping))
vals = [v for v in mapping.values() if isinstance(v, str) and v.endswith(".js")]
print("js files", vals[:5])
