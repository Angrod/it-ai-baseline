"""OpenSSF Scorecard: pre-computed security health scores (0-10) for public repos.

Only repos whose maintainers publish results are listed; everything else
returns None and gets the neutral score in the trust model. Results are cached
for a week because Scorecard itself rescans weekly.
"""

from __future__ import annotations

from datetime import datetime

import requests

from pipeline.config import days_since, iso

SCORECARD_URL = "https://api.securityscorecards.dev/projects/github.com/{full_name}"
CACHE_DAYS = 7


def fetch(full_name: str, session: requests.Session) -> float | None:
    resp = session.get(SCORECARD_URL.format(full_name=full_name), timeout=30)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    score = resp.json().get("score")
    return float(score) if score is not None else None


def scores(names: list[str], cache: dict, now: datetime, session: requests.Session | None = None) -> dict:
    """Return {lowercase name: score or None}, refreshing stale cache entries in place."""
    session = session or requests.Session()
    result = {}
    for name in names:
        key = name.lower()
        entry = cache.get(key)
        if entry is None or days_since(entry["fetched_at"], now) > CACHE_DAYS:
            try:
                entry = {"score": fetch(name, session), "fetched_at": iso(now)}
            except requests.RequestException:
                entry = entry or {"score": None, "fetched_at": iso(now)}
            cache[key] = entry
        result[key] = entry["score"]
    return result
