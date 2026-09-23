import json
import re
import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})
cid = "34130338"
r = session.get(f"https://www.thepaper.cn/newsDetail_forward_{cid}", timeout=25)
html = r.text
for pat in ["contentapi", "contContent", "__NEXT_DATA__", "detailData"]:
    print(pat, pat in html)

# try other apis
for u in [
    f"https://www.thepaper.cn/contentapi/cont/getContent?contId={cid}",
    f"https://www.thepaper.cn/contentapi/cont/content/{cid}",
    f"https://www.thepaper.cn/contentapi/nodeCont/detail?contId={cid}",
]:
    try:
        rr = session.get(u, timeout=20)
        print(u, rr.status_code, rr.text[:250])
    except Exception as e:
        print(u, e)

# parse embedded json in page
m = re.search(r'"contContent":"((?:\\.|[^"\\])*)"', html)
if m:
    print("contContent len", len(m.group(1)))
