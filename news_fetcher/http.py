from __future__ import annotations

import time
from typing import Optional

import requests

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9",
}


class HttpClient:
    def __init__(self, timeout: int = 25, retries: int = 3, pause: float = 0.4):
        self.timeout = timeout
        self.retries = retries
        self.pause = pause
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def get(
        self,
        url: str,
        *,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        encoding: Optional[str] = None,
    ) -> requests.Response:
        last_error: Optional[Exception] = None
        for attempt in range(self.retries):
            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                if encoding:
                    response.encoding = encoding
                elif not response.encoding or response.encoding.lower() == "iso-8859-1":
                    response.encoding = response.apparent_encoding or "utf-8"
                return response
            except Exception as exc:  # noqa: BLE001 - surface after retries
                last_error = exc
                if attempt + 1 < self.retries:
                    time.sleep(self.pause * (attempt + 1))
        raise RuntimeError(f"GET 失败: {url} ({last_error})")

    def get_json(self, url: str, **kwargs) -> dict:
        return self.get(url, **kwargs).json()

    def get_text(self, url: str, **kwargs) -> str:
        return self.get(url, **kwargs).text
