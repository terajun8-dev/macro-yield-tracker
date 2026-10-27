"""Optional related-news helpers for the market report."""

from __future__ import annotations

import json
import os
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"
PUBLICATION_DATE_FORMAT = "%Y-%m-%d"
RSS_FEEDS = (
    "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja",
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "https://feeds.reuters.com/reuters/worldNews",
    "https://jp.reuters.com/rssFeed/topNews",
)


def _normalize_news_item(item: dict[str, Any]) -> dict[str, str]:
    title = str(item.get("title") or "").strip()
    if not title:
        return {}
    source = str(item.get("source") or "").strip() or "News"
    url = str(item.get("url") or "").strip()
    publication_date = _parse_publication_date(item.get("publication_date"))
    return {
        "title": title,
        "source": source,
        "url": url,
        "publication_date": publication_date,
    }


def _parse_publication_date(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    try:
        published = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        try:
            published = parsedate_to_datetime(text)
        except (TypeError, ValueError, OverflowError):
            return ""
    return published.strftime(PUBLICATION_DATE_FORMAT)


def _read_rss_feed(feed_url: str, limit: int = 3) -> list[dict[str, str]]:
    request = Request(feed_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request, timeout=20) as response:
            payload = response.read()
    except (HTTPError, URLError, TimeoutError):
        return []

    try:
        root = ET.fromstring(payload)
    except ET.ParseError:
        return []

    items: list[dict[str, str]] = []
    for node in root.findall(".//item")[:limit]:
        title = (node.findtext("title") or "").strip()
        link = (node.findtext("link") or "").strip()
        if not title:
            continue
        source = (node.findtext("source") or "").strip() or "RSS"
        normalized = _normalize_news_item(
            {
                "title": title,
                "source": source,
                "url": link,
                "publication_date": node.findtext("pubDate") or node.findtext("date") or "",
            }
        )
        if normalized:
            items.append(normalized)

    if items:
        return items

    for node in root.findall(".//entry")[:limit]:
        title = (node.findtext("title") or "").strip()
        link = (node.findtext("link") or "").strip()
        if not title:
            continue
        source = (node.findtext("source") or "").strip() or "RSS"
        normalized = _normalize_news_item(
            {
                "title": title,
                "source": source,
                "url": link,
                "publication_date": node.findtext("published") or node.findtext("updated") or "",
            }
        )
        if normalized:
            items.append(normalized)
    return items


def _newsapi_headlines(limit: int = 4) -> list[dict[str, str]]:
    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        return []

    params = {
        "country": "jp",
        "category": "business",
        "pageSize": 4,
        "apiKey": api_key,
    }
    try:
        request = Request(
            f"{NEWSAPI_URL}?{urlencode(params)}",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, ValueError):
        return []

    articles = payload.get("articles") or []
    results = []
    for article in articles[:limit]:
        normalized = _normalize_news_item(
            {
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
                "publication_date": article.get("publishedAt"),
            }
        )
        if normalized:
            results.append(normalized)
    return results


def fetch_related_news(limit: int = 4) -> list[dict[str, str]]:
    """Fetch optional related headline snippets, preferring News API if configured else RSS fallback."""
    items: list[dict[str, str]] = _newsapi_headlines(limit=limit)
    seen: set[str] = {item["title"] for item in items}

    for feed_url in RSS_FEEDS:
        for item in _read_rss_feed(feed_url, limit=limit):
            title = item.get("title", "")
            if title and title not in seen:
                items.append(item)
                seen.add(title)
            if len(items) >= limit:
                return items[:limit]
    return items[:limit]
