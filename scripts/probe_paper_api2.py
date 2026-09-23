import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0", "Referer": "https://www.thepaper.cn/list_25429"})

payloads = [
    ("get", "https://www.thepaper.cn/contentapi/nodeCont/list?nodeId=25429&pageNum=2&pageSize=20"),
    (
        "post",
        "https://www.thepaper.cn/contentapi/nodeCont/list",
        {"nodeId": 25429, "pageNum": 2, "pageSize": 20},
    ),
    (
        "post",
        "https://www.thepaper.cn/contentapi/nodeCont/getNodeContList",
        {"nodeId": 25429, "pageNum": 2, "pageSize": 20, "excludeContIds": []},
    ),
]
for item in payloads:
    method = item[0]
    url = item[1]
    data = item[2] if len(item) > 2 else None
    try:
        if method == "get":
            r = session.get(url, timeout=20)
        else:
            r = session.post(url, json=data, timeout=20)
        print(method, url, r.status_code, r.text[:200])
    except Exception as e:
        print(method, url, e)
