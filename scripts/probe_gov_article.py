import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})

url = "https://www.gov.cn/yaowen/liebiao/202609/content_7081833.htm"
r = session.get(url, timeout=25)
r.encoding = "utf-8"
print("status", r.status_code, "len", len(r.text))
soup = BeautifulSoup(r.text, "lxml")
print("title tag", soup.title.get_text() if soup.title else None)
for sel in ["h1", "h1#ti", ".article_title", "#ti"]:
    n = soup.select_one(sel)
    if n:
        print(sel, n.get_text(strip=True))
for sel in ["#UCAP-CONTENT", ".pages_content", ".TRS_Editor", "div.article"]:
    n = soup.select_one(sel)
    if n:
        print("body", sel, len(n.get_text(strip=True)))

# yicai news detail API?
r = session.get(
    "https://www.yicai.com/api/ajax/getjuhelist?cid=48&page=1&pagesize=3", timeout=25
)
for item in r.json():
    nid = item["NewsID"]
    for api in [
        f"https://www.yicai.com/api/ajax/getnews?id={nid}",
        f"https://www.yicai.com/api/ajax/getNews?id={nid}",
    ]:
        try:
            rr = session.get(api, timeout=15)
            if rr.headers.get("content-type", "").startswith("application/json") or rr.text.startswith("{"):
                d = rr.json()
                print("api", api, list(d.keys())[:8])
                notes = d.get("NewsNotes") or d.get("data", {}).get("NewsNotes")
                if notes:
                    print("notes len", len(notes))
        except Exception:
            pass
    print("item", item["NewsTitle"], item.get("pubDate"), item.get("NewsNotes", "")[:80] if item.get("NewsNotes") else "no notes")
