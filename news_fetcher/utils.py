from __future__ import annotations

import html
import json
import re
from datetime import date, datetime, time, timedelta
from typing import Iterable, List, Optional, Tuple

from bs4 import BeautifulSoup
from dateutil import parser as date_parser


def parse_datetime(value: str) -> Optional[datetime]:
    if not value or not str(value).strip():
        return None
    text = str(value).strip()
    relative_markers = ("分钟前", "小时前", "天前", "刚刚", "昨天", "前天")
    if any(marker in text for marker in relative_markers):
        return None
    try:
        dt = date_parser.parse(text)
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt
    except (ValueError, TypeError, OverflowError):
        return None


def date_range_bounds(start: date, end: date) -> Tuple[datetime, datetime]:
    if end < start:
        raise ValueError("结束日期不能早于开始日期")
    start_dt = datetime.combine(start, time.min)
    end_dt = datetime.combine(end, time.max)
    return start_dt, end_dt


def in_range(dt: Optional[datetime], start: datetime, end: datetime) -> bool:
    if dt is None:
        return False
    return start <= dt <= end


def clean_html_text(raw_html: str) -> str:
    if not raw_html:
        return ""
    unescaped = html.unescape(raw_html)
    soup = BeautifulSoup(unescaped, "lxml")
    for tag in soup(["script", "style", "iframe", "noscript"]):
        tag.decompose()
    text = soup.get_text("\n", strip=True)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def extract_json_object_after_marker(text: str, marker: str) -> dict:
    idx = text.find(marker)
    if idx < 0:
        return {}
    start = text.find("{", idx)
    if start < 0:
        return {}
    depth = 0
    for i, ch in enumerate(text[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    return {}


def extract_between_brackets_array(js_text: str) -> list:
    start = js_text.find("[")
    end = js_text.rfind("]")
    if start < 0 or end <= start:
        return []
    return json.loads(js_text[start : end + 1])


def dedupe_articles(articles: Iterable) -> List:
    seen = set()
    result = []
    for article in articles:
        key = (article.source, article.url or article.title)
        if key in seen:
            continue
        seen.add(key)
        result.append(article)
    return result


def yesterday_range(today: Optional[date] = None) -> Tuple[date, date]:
    base = today or date.today()
    y = base - timedelta(days=1)
    return y, y
