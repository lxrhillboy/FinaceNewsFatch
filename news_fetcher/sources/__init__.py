from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional, Type

from news_fetcher.http import HttpClient
from news_fetcher.models import FetchResult
from news_fetcher.sources.base import NewsSource
from news_fetcher.sources.cls_cn import ClsSource
from news_fetcher.sources.cs_com_cn import CsComCnSource
from news_fetcher.sources.gov_cn import GovCnSource
from news_fetcher.sources.nbd import NbdSource
from news_fetcher.sources.thepaper import ThePaperSource
from news_fetcher.sources.yicai import YicaiSource

SOURCE_REGISTRY: Dict[str, Type[NewsSource]] = {
    "gov_cn": GovCnSource,
    "cls": ClsSource,
    "nbd": NbdSource,
    "thepaper": ThePaperSource,
    "cs_com_cn": CsComCnSource,
    "yicai": YicaiSource,
}

SOURCE_LABELS = {
    "gov_cn": "中国政府网要闻",
    "cls": "财联社电报",
    "nbd": "每日经济新闻",
    "thepaper": "澎湃新闻",
    "cs_com_cn": "中证网",
    "yicai": "第一财经",
}


def available_sources() -> List[str]:
    return list(SOURCE_REGISTRY.keys())


def fetch_all(
    start: date,
    end: date,
    sources: List[str],
    *,
    client: Optional[HttpClient] = None,
    fetch_body: bool = True,
    per_source_limit: int = 50,
) -> List[FetchResult]:
    http = client or HttpClient()
    results: List[FetchResult] = []
    for name in sources:
        cls = SOURCE_REGISTRY.get(name)
        if not cls:
            results.append(FetchResult(source=name, errors=[f"未知来源: {name}"]))
            continue
        source = cls(http)
        try:
            articles = source.fetch(
                start,
                end,
                fetch_body=fetch_body,
                limit=per_source_limit,
            )
            results.append(FetchResult(source=name, articles=articles))
        except Exception as exc:  # noqa: BLE001
            results.append(FetchResult(source=name, errors=[str(exc)]))
    return results
