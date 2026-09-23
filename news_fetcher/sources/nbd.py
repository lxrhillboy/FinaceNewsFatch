from __future__ import annotations

import re
from datetime import date, datetime
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from news_fetcher.models import NewsArticle
from news_fetcher.sources.base import NewsSource
from news_fetcher.utils import clean_html_text, date_range_bounds, in_range, parse_datetime


class NbdSource(NewsSource):
    name = "nbd"
    label = "每日经济新闻"
    LIST_URL = "https://economy.nbd.com.cn/columns/44/"

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
        soup = BeautifulSoup(html, "lxml")
        articles: List[NewsArticle] = []
        for anchor in soup.select("a"):
            title = anchor.get_text(strip=True)
            href = anchor.get("href") or ""
            if len(title) < 8:
                continue
            if not re.search(r"/articles/", href):
                continue
            url = urljoin(self.LIST_URL, href)
            published = self._guess_publish_time(anchor)
            if not in_range(published, start_dt, end_dt):
                continue
            body = ""
            if fetch_body:
                body = self._fetch_body(url)
            articles.append(
                NewsArticle(
                    title=title,
                    url=url,
                    source=self.label,
                    published_at=published or start_dt,
                    body=body,
                    category="经济新闻",
                )
            )
            if len(articles) >= limit:
                break
        return articles

    def _guess_publish_time(self, anchor) -> Optional[datetime]:
        parent = anchor.parent
        for _ in range(4):
            if not parent:
                break
            text = parent.get_text(" ", strip=True)
            match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
            if match:
                return parse_datetime(match.group(1))
            parent = parent.parent
        match = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", anchor.get("href", ""))
        if match:
            return parse_datetime("-".join(match.groups()))
        return None

    def _fetch_body(self, url: str) -> str:
        html = self.client.get_text(url)
        soup = BeautifulSoup(html, "lxml")
        for selector in ["article", ".g-article", ".article-content", "#article"]:
            node = soup.select_one(selector)
            if node:
                return clean_html_text(node.decode_contents())
        return ""
