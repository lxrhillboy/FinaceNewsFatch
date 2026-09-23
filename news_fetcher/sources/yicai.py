from __future__ import annotations

from datetime import date, datetime
from typing import List

from bs4 import BeautifulSoup

from news_fetcher.models import NewsArticle
from news_fetcher.sources.base import NewsSource
from news_fetcher.utils import clean_html_text, date_range_bounds, in_range, parse_datetime


class YicaiSource(NewsSource):
    name = "yicai"
    label = "第一财经"
    LIST_URL = "https://www.yicai.com/api/ajax/getjuhelist"

    def fetch(
        self,
        start: date,
        end: date,
        *,
        fetch_body: bool = True,
        limit: int = 50,
    ) -> List[NewsArticle]:
        start_dt, end_dt = date_range_bounds(start, end)
        articles: List[NewsArticle] = []
        for page in range(1, 6):
            items = self.client.get_json(
                self.LIST_URL,
                params={"cid": 48, "page": page, "pagesize": 30},
            )
            if not isinstance(items, list):
                break
            for item in items:
                published = parse_datetime(item.get("CreateDate", ""))
                if not in_range(published, start_dt, end_dt):
                    continue
                title = (item.get("NewsTitle") or "").strip()
                news_id = item.get("NewsID")
                if not title or not news_id:
                    continue
                url = f"https://www.yicai.com/news/{news_id}.html"
                body = ""
                if fetch_body:
                    body = self._fetch_body(url, item)
                articles.append(
                    NewsArticle(
                        title=title,
                        url=url,
                        source=self.label,
                        published_at=published or start_dt,
                        body=body,
                        summary=(item.get("NewsNotes") or "").strip(),
                        category=item.get("ChannelName", "") or "财经",
                    )
                )
                if len(articles) >= limit:
                    return articles
            if not items:
                break
        return articles

    def _fetch_body(self, url: str, item: dict) -> str:
        try:
            html = self.client.get_text(url, encoding="utf-8")
        except RuntimeError:
            return clean_html_text(item.get("NewsNotes", "") or "")
        soup = BeautifulSoup(html, "lxml")
        node = soup.select_one("article") or soup.select_one(".m-txt")
        if node:
            text = clean_html_text(node.decode_contents())
            if text:
                return text
        return clean_html_text(item.get("NewsNotes", "") or "")
