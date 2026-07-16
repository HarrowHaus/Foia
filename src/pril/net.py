from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from .config import network_config


class NetworkError(RuntimeError):
    pass


@dataclass(frozen=True)
class Response:
    url: str
    status: int
    headers: dict[str, str]
    body: bytes

    def json(self) -> Any:
        return json.loads(self.body.decode("utf-8"))


def request(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    method: str = "GET",
    data: bytes | None = None,
) -> Response:
    cfg = network_config()
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        url = f"{url}{'&' if '?' in url else '?'}{query}"
    merged = {"User-Agent": cfg.user_agent, "Accept": "application/json, text/html;q=0.9, */*;q=0.8"}
    if headers:
        merged.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=merged)
    time.sleep(max(0.0, cfg.request_delay_seconds))
    try:
        with urllib.request.urlopen(req, timeout=cfg.timeout_seconds) as resp:
            body = resp.read()
            return Response(resp.geturl(), int(resp.status), dict(resp.headers.items()), body)
    except urllib.error.HTTPError as exc:
        detail = exc.read(1000).decode("utf-8", errors="replace")
        raise NetworkError(f"HTTP {exc.code} for {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise NetworkError(f"Network error for {url}: {exc.reason}") from exc
