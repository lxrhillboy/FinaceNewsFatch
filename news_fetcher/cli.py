from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional, Tuple

from news_fetcher.export import flatten_articles, to_json_document, write_json, write_markdown
from news_fetcher.http import HttpClient
from news_fetcher.sources import SOURCE_LABELS, available_sources, fetch_all
from news_fetcher.utils import dedupe_articles, yesterday_range


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="抓取中国主流媒体经济新闻，支持自定义时间范围。",
    )
    parser.add_argument("--start", help="开始日期，格式 YYYY-MM-DD")
    parser.add_argument("--end", help="结束日期，格式 YYYY-MM-DD")
    parser.add_argument(
        "--yesterday",
        action="store_true",
        help="抓取昨天（等价于 start=end=昨天）",
    )
    parser.add_argument(
        "--sources",
        default="all",
        help="来源列表，逗号分隔；默认 all 表示全部来源",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="每个来源最多保留的新闻条数（默认 50）",
    )
    parser.add_argument(
        "--no-body",
        action="store_true",
        help="仅抓取标题和元数据，不抓取正文（更快）",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="输出目录（默认 output）",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "both"],
        default="both",
        help="输出格式（默认 json+markdown）",
    )
    return parser


def resolve_sources(raw: str) -> List[str]:
    if raw.strip().lower() == "all":
        return available_sources()
    names = [part.strip() for part in raw.split(",") if part.strip()]
    return names


def resolve_dates(args: argparse.Namespace) -> Tuple[date, date]:
    if args.yesterday:
        return yesterday_range()
    if not args.start or not args.end:
        raise SystemExit("请指定 --start 与 --end，或使用 --yesterday。")
    start = _parse_date(args.start)
    end = _parse_date(args.end)
    return start, end


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    start, end = resolve_dates(args)
    sources = resolve_sources(args.sources)
    client = HttpClient()
    results = fetch_all(
        start,
        end,
        sources,
        client=client,
        fetch_body=not args.no_body,
        per_source_limit=args.limit,
    )
    articles = dedupe_articles(flatten_articles(results))
    output_dir = Path(args.output_dir)
    stamp = f"{start.isoformat()}_{end.isoformat()}"
    payload = to_json_document(results, start=start.isoformat(), end=end.isoformat())

    if args.format in ("json", "both"):
        write_json(output_dir / f"news_{stamp}.json", payload)
    if args.format in ("markdown", "both"):
        write_markdown(
            output_dir / f"news_{stamp}.md",
            articles,
            start=start.isoformat(),
            end=end.isoformat(),
        )

    total = len(articles)
    errors = sum(len(r.errors) for r in results)
    print(f"完成：共 {total} 条新闻，{errors} 个来源错误。")
    for result in results:
        label = SOURCE_LABELS.get(result.source, result.source)
        if result.errors:
            print(f"  - {label}: 0 条，错误={'; '.join(result.errors)}")
        else:
            print(f"  - {label}: {len(result.articles)} 条")
    print(f"输出目录: {output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
