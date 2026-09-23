from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class NewsArticle:
    title: str
    url: str
    source: str
    published_at: datetime
    body: str
    summary: str = ""
    category: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["published_at"] = self.published_at.isoformat(timespec="seconds")
        return data


@dataclass
class FetchResult:
    source: str
    articles: List[NewsArticle] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "errors": self.errors,
            "articles": [a.to_dict() for a in self.articles],
        }
