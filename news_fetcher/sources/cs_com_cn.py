from __future__ import annotations

import re
from datetime import date, datetime
from typing import Dict, List, Set

from bs4 import BeautifulSoup

from news_fetcher.models import NewsArticle
from news_fetcher.sources.base import NewsSource
from news_fetcher.utils import (
    clean_html_text,
    date_range_bounds,
    extract_between_brackets_array,
    extract_json_object_after_marker,
    in_range,
    parse_datetime,
)


class CsComCnSource(NewsSource):
    name = "cs_com_cn"
    label = "中证网"
    GUIDE_URL = "https://www.cs.com.cn/js/9903/mi4_page_articles_guide.js"
    DATA_BASE = "https://www.cs.com.cn/js/9903/"

    def fetch(
        self,
        start: date,
        end: date,
        *,
        fetch_body: bool = True,
        limit: int = 50,
    ) -> List[NewsArticle]:
        start_dt, end_dt = date_range_bounds(start, end)
        files = self._list_data_files(start, end)
        articles: List[NewsArticle] = []
        for filename in files:
            text = self.client.get_text(self.DATA_BASE + filename)
            items = extract_between_brackets_array(text)
            for item in items:
                published = parse_datetime(item.get("pub_date", ""))
                if not in_range(published, start_dt, end_dt):
                    continue
                title = (item.get("title") or "").strip()
                url = item.get("external_link") or item.get("url") or ""
                if url and not url.startswith("http"):
                    url = "https://www.cs.com.cn" + url
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
                        published_at=published or start_dt,
                        body=body,
                        summary=(item.get("miSummary") or "").strip(),
                        category=item.get("subNm", "") or "财经",
                        extra={"origin": item.get("miOrigin", "")},
                    )
                )
                if len(articles) >= limit:
                    return articles
        return articles

    def _list_data_files(self, start: date, end: date) -> List[str]:
        guide = self.client.get_text(self.GUIDE_URL)
        mapping: Dict[str, str] = extract_json_object_after_marker(guide, "PAGE_INDEX_MAP")
        if not mapping:
            return []
        filenames: Set[str] = set()
        for value in mapping.values():
            if not isinstance(value, str) or not value.endswith(".js"):
                continue
            date_match = re.search(r"(\d{8})", value)
            if not date_match:
                continue
            file_date = datetime.strptime(date_match.group(1), "%Y%m%d").date()
            if start <= file_date <= end:
                filenames.add(value)
        return sorted(filenames, reverse=True)

    def _fetch_body(self, url: str) -> str:
        html = self.client.get_text(url)
        soup = BeautifulSoup(html, "html.parser")
        node = soup.select_one("article")
        if not node:
            return ""
        return clean_html_text(node.decode_contents())
