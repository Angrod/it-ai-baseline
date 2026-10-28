"""Daily snapshots of github.com/trending, plus the "times trending" counts derived from them.

GitHub has no trending API, so we keep our own history: one JSON file per day
under data/snapshots/trending/. "Times trending" is the number of distinct days
a repo appeared on any daily page (global or a language page) inside the window,
so the same repo trending on two pages on one day counts once.
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

from pipeline.config import load_json

TRENDING_URL = "https://github.com/trending{lang}?since={period}"
USER_AGENT = "it-ai-baseline (+https://github.com/Angrod/it-ai-baseline)"

_ARTICLE = re.compile(r'<article class="Box-row".*?</article>', re.S)
_REPO = re.compile(r'<h2[^>]*>\s*<a[^>]*?href="/([^"/\s]+/[^"/\s]+)"', re.S)
_PERIOD_STARS = re.compile(r"([\d,]+)\s+stars?\s+(?:today|this week|this month)")


def parse_trending(html: str) -> list[dict]:
    """Return [{repo, rank, period_stars}] in page order."""
    rows = []
    for article in _ARTICLE.findall(html):
        repo = _REPO.search(article)
        if not repo:
            continue
        stars = _PERIOD_STARS.search(article)
        rows.append({
            "repo": repo.group(1),
            "rank": len(rows) + 1,
            "period_stars": int(stars.group(1).replace(",", "")) if stars else 0,
        })
    return rows


def page_key(lang: str, period: str) -> str:
    return f"{lang or 'all'}/{period}"


def fetch_snapshot(languages: list[str], periods: list[str], session: requests.Session | None = None,
                   pause: float = 1.0) -> dict[str, list[dict]]:
    session = session or requests.Session()
    pages: dict[str, list[dict]] = {}
    for lang in languages:
        for period in periods:
            url = TRENDING_URL.format(lang=f"/{lang}" if lang else "", period=period)
            resp = session.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
            resp.raise_for_status()
            pages[page_key(lang, period)] = parse_trending(resp.text)
            time.sleep(pause)
    return pages


def load_snapshots(directory: Path, now: datetime, window_days: int) -> list[dict]:
    """Snapshots whose date falls inside the window, oldest first."""
    cutoff = (now - timedelta(days=window_days)).date()
    snapshots = []
    for path in sorted(directory.glob("*.json")):
        try:
            day = datetime.strptime(path.stem, "%Y-%m-%d").date()
        except ValueError:
            continue
        if cutoff < day <= now.date():
            snapshots.append(load_json(path))
    return snapshots


def times_trending(snapshots: list[dict]) -> dict[str, int]:
    """Distinct days each repo appeared on any daily page, keyed by lowercase name."""
    counts: dict[str, int] = {}
    for snap in snapshots:
        seen = {
            row["repo"].lower()
            for key, rows in snap["pages"].items() if key.endswith("/daily")
            for row in rows
        }
        for repo in seen:
            counts[repo] = counts.get(repo, 0) + 1
    return counts


def pool_from_snapshots(snapshots: list[dict]) -> dict[str, str]:
    """Every repo seen on any page in the window: {lowercase name: page-cased name}."""
    pool: dict[str, str] = {}
    for snap in snapshots:
        for rows in snap["pages"].values():
            for row in rows:
                pool.setdefault(row["repo"].lower(), row["repo"])
    return pool


def prune(directory: Path, now: datetime, keep_days: int) -> list[Path]:
    cutoff = (now - timedelta(days=keep_days)).date()
    removed = []
    for path in directory.glob("*.json"):
        try:
            day = datetime.strptime(path.stem, "%Y-%m-%d").date()
        except ValueError:
            continue
        if day < cutoff:
            path.unlink()
            removed.append(path)
    return removed
