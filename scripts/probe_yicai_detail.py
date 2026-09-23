import requests
from bs4 import BeautifulSoup

items = requests.get(
    "https://www.yicai.com/api/ajax/getjuhelist?cid=48&page=1&pagesize=10",
    timeout=25,
).json()
for item in items:
    nid = item["NewsID"]
    paths = [
        item.get("url"),
        f"/news/{nid}.html",
        f"/brief/{nid}.html",
    ]
    for p in paths:
        if not p:
            continue
        u = p if p.startswith("http") else "https://www.yicai.com" + p
        try:
            r = requests.get(u, timeout=15)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, "lxml")
            art = soup.select_one("article") or soup.select_one(".m-txt")
            if art and len(art.get_text(strip=True)) > 50:
                print("OK", nid, u, len(art.get_text(strip=True)))
                break
        except Exception:
            pass
    else:
        notes = item.get("NewsNotes") or ""
        print("fallback", nid, len(notes), item.get("NewsTitle", "")[:30])
