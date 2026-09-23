from __future__ import annotations

import json
import re
from datetime import date, datetime
from typing import List

from news_fetcher.models import NewsArticle
from news_fetcher.sources.base import NewsSource
from news_fetcher.utils import clean_html_text, date_range_bounds, in_range, parse_datetime


class ThePaperSource(NewsSource):
    name = "thepaper"
    label = "澎湃新闻"
    LIST_URL = "https://www.thepaper.cn/list_25429"

    def fetch(
        self,
        start: date,
        end: date,
        *,
        fetch_body: bool = True,
        limit: int = 50,
    ) -> List[NewsArticle]:
        start_dt, end_dt = date_range_bounds(start, end)
        html = self.client.get_text(self.LIST_URL)
        match = re.search(
            r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',
            html,
            re.S,
        )
        if not match:
            return []
        payload = json.loads(match.group(1))
        items = payload.get("props", {}).get("pageProps", {}).get("data", {}).get("list", [])
        articles: List[NewsArticle] = []
        for item in items:
            published = parse_datetime(item.get("publishTime", ""))
            if not published and item.get("pubTimeLong"):
                published = datetime.fromtimestamp(int(item["pubTimeLong"]) / 1000)
            if not in_range(published, start_dt, end_dt):
                continue
            cont_id = item.get("contId")
            title = (item.get("name") or "").strip()
            if not title or not cont_id:
                continue
            url = f"https://www.thepaper.cn/newsDetail_forward_{cont_id}"
            body = ""
            if fetch_body:
                body = self._fetch_body(cont_id)
            articles.append(
                NewsArticle(
                    title=title,
                    url=url,
                    source=self.label,
                    published_at=published or start_dt,
                    body=body,
                    category=item.get("nodeInfo", {}).get("name", ""),
                )
            )
            if len(articles) >= limit:
                break
        return articles

    def _fetch_body(self, cont_id: str) -> str:
        html = self.client.get_text(
            f"https://www.thepaper.cn/newsDetail_forward_{cont_id}"
        )
        match = re.search(
            r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',
            html,
            re.S,
        )
        if not match:
            return ""
        payload = json.loads(match.group(1))
        detail = (
            payload.get("props", {})
            .get("pageProps", {})
            .get("detailData", {})
            .get("contentDetail", {})
        )
        return clean_html_text(detail.get("content", "") or "")
