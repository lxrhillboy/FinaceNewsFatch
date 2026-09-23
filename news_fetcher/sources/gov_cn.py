from __future__ import annotations

from datetime import date, datetime
from typing import List

from bs4 import BeautifulSoup

from news_fetcher.models import NewsArticle
from news_fetcher.sources.base import NewsSource
from news_fetcher.utils import clean_html_text, date_range_bounds, in_range, parse_datetime


class GovCnSource(NewsSource):
    name = "gov_cn"
    label = "中国政府网要闻"
    LIST_URL = "https://www.gov.cn/yaowen/liebiao/YAOWENLIEBIAO.json"

    def fetch(
        self,
        start: date,
        end: date,
        *,
        fetch_body: bool = True,
        limit: int = 50,
    ) -> List[NewsArticle]:
        start_dt, end_dt = date_range_bounds(start, end)
        items = self.client.get_json(self.LIST_URL)
        articles: List[NewsArticle] = []
        for item in items:
            published = parse_datetime(item.get("DOCRELPUBTIME", ""))
            if not in_range(published, start_dt, end_dt):
                continue
            url = item.get("URL", "")
            title = item.get("TITLE", "").strip()
            if not title or not url:
                continue
            body = ""
            if fetch_body:
                body = self._fetch_body(url)
            articles.append(
                NewsArticle(
                    title=title,
                    url=url,
                    source=self.label,
                    published_at=published or datetime.combine(start, datetime.min.time()),
                    body=body,
                    summary=item.get("SUB_TITLE", "") or "",
                    category="政务要闻",
                )
            )
            if len(articles) >= limit:
                break
        return articles

    def _fetch_body(self, url: str) -> str:
        html = self.client.get_text(url, encoding="utf-8")
        soup = BeautifulSoup(html, "html.parser")
        node = soup.find(id="UCAP-CONTENT")
        if not node:
            node = soup.select_one("div.pages_content")
        if not node:
            return ""
        return clean_html_text(node.decode_contents())
