from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List

from news_fetcher.http import HttpClient
from news_fetcher.models import NewsArticle


class NewsSource(ABC):
    name: str = "base"
    label: str = "基础来源"

    def __init__(self, client: HttpClient):
        self.client = client

    @abstractmethod
    def fetch(
        self,
        start: date,
        end: date,
        *,
        fetch_body: bool = True,
        limit: int = 50,
    ) -> List[NewsArticle]:
        raise NotImplementedError
