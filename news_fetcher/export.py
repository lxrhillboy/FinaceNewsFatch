from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from news_fetcher.models import FetchResult, NewsArticle
from news_fetcher.sources import SOURCE_LABELS


def flatten_articles(results: Iterable[FetchResult]) -> List[NewsArticle]:
    articles: List[NewsArticle] = []
    for result in results:
        articles.extend(result.articles)
    articles.sort(key=lambda item: item.published_at, reverse=True)
    return articles


def to_json_document(
    results: List[FetchResult],
    *,
    start: str,
    end: str,
) -> dict:
    return {
        "start_date": start,
        "end_date": end,
        "sources": [
            {
                "id": result.source,
                "name": SOURCE_LABELS.get(result.source, result.source),
                "errors": result.errors,
                "count": len(result.articles),
                "articles": [article.to_dict() for article in result.articles],
            }
            for result in results
        ],
        "total": sum(len(r.articles) for r in results),
    }


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(path: Path, articles: List[NewsArticle], *, start: str, end: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# 经济新闻抓取结果（{start} 至 {end}）", ""]
    if not articles:
        lines.append("_指定时间范围内未抓取到新闻。_")
    for index, article in enumerate(articles, start=1):
        lines.extend(
            [
                f"## {index}. {article.title}",
                "",
                f"- 来源：{article.source}",
                f"- 时间：{article.published_at.strftime('%Y-%m-%d %H:%M:%S')}",
                f"- 链接：{article.url}",
                "",
                article.body or article.summary or "（正文为空）",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")
