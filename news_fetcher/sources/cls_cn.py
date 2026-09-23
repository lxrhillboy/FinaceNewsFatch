from __future__ import annotations

from datetime import date, datetime
from typing import List

from news_fetcher.models import NewsArticle
from news_fetcher.sources.base import NewsSource
from news_fetcher.utils import clean_html_text, date_range_bounds, in_range


class ClsSource(NewsSource):
    name = "cls"
    label = "财联社电报"
    API_URL = "https://www.cls.cn/nodeapi/telegraphs"

    def fetch(
        self,
        start: date,
        end: date,
        *,
        fetch_body: bool = True,
        limit: int = 50,
    ) -> List[NewsArticle]:
        start_dt, end_dt = date_range_bounds(start, end)
        payload = self.client.get_json(
            self.API_URL,
            params={
                "app": "CailianpressWeb",
                "os": "web",
                "sv": "8.4.6",
                "rn": min(limit * 3, 150),
            },
        )
        roll = payload.get("data", {}).get("roll_data", [])
        articles: List[NewsArticle] = []
        for item in roll:
            ts = item.get("ctime") or item.get("modified_time")
            published = None
            if ts:
                published = datetime.fromtimestamp(int(ts))
            if not in_range(published, start_dt, end_dt):
                continue
            title = (item.get("title") or "").strip()
            content = (item.get("content") or item.get("brief") or "").strip()
            if not title and content:
                title = content[:60]
            if not title:
                continue
            article_id = item.get("id") or item.get("article_id")
            url = f"https://www.cls.cn/detail/{article_id}" if article_id else "https://www.cls.cn/telegraph"
            body = clean_html_text(content) if fetch_body else ""
            articles.append(
                NewsArticle(
                    title=title,
                    url=url,
                    source=self.label,
                    published_at=published or start_dt,
                    body=body,
                    summary=(item.get("brief") or "").strip(),
                    category="电报",
                )
            )
            if len(articles) >= limit:
                break
        return articles
