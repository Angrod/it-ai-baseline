"""Trending composite: the Scribes formula, applied to the IT-relevant pool.

Each signal is normalized across the pool to 0..1, then weighted:
  40% stars gained (30d) + 35% times trending (30d) + 25% total stars
Total stars use log normalization by default (see config/scoring.yaml).
"""

from __future__ import annotations

import math


def max_norm(values: list[float]) -> list[float]:
    top = max(values, default=0)
    return [v / top if top > 0 else 0.0 for v in values]


def log_norm(values: list[float]) -> list[float]:
    return max_norm([math.log1p(max(v, 0)) for v in values])


def trending_scores(repos: list[dict], weights: dict, log_total_stars: bool = True) -> None:
    """Set trend_score (0-100) and trend_parts on each repo in place."""
    gained = max_norm([r.get("stars_gained_30d", 0) for r in repos])
    trended = max_norm([r.get("times_trending_30d", 0) for r in repos])
    stars = [r.get("stars", 0) for r in repos]
    total = log_norm(stars) if log_total_stars else max_norm(stars)
    for repo, g, t, s in zip(repos, gained, trended, total):
        parts = {"stars_gained": g, "times_trending": t, "total_stars": s}
        repo["trend_parts"] = {k: round(v, 4) for k, v in parts.items()}
        repo["trend_score"] = round(100 * sum(weights[k] * v for k, v in parts.items()), 2)


def assign_rank(repos: list[dict], field: str) -> None:
    """1-based rank in list order."""
    for i, repo in enumerate(repos, 1):
        repo[field] = i
