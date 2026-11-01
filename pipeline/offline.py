"""Fixture-backed stand-ins for the network sources, used by tests and `build --offline`.

A fixture directory holds repos.json ({owner/name: record}) and snapshots/*.json.
Records use the same shape the GitHub client returns, plus optional
`stars_30d`, `contributors`, `scorecard`, `readme` and `star_error` fields.
"""

from __future__ import annotations

import copy
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from pipeline.config import load_json

FIXTURE_ONLY = ("stars_30d", "contributors", "scorecard", "readme", "star_error")


class FixtureGitHub:
    def __init__(self, directory: Path, now: datetime | None = None):
        raw = load_json(Path(directory) / "repos.json", {})
        self.records = {name.lower(): {"full_name": name, **rec} for name, rec in raw.items()}
        self.now = now or datetime.now(timezone.utc)
        self.errors: dict[str, str] = {}

    def _public(self, rec: dict) -> dict:
        return {k: copy.deepcopy(v) for k, v in rec.items() if k not in FIXTURE_ONLY}

    def search(self, query: str, per_page: int) -> list[dict]:
        if not query.startswith("topic:"):
            return []
        topic = query.split()[0].removeprefix("topic:")
        hits = [r for r in self.records.values() if topic in r.get("topics", [])]
        return [self._public(r) for r in hits[:per_page]]

    def repos(self, names: list[str]) -> tuple[dict, list[str]]:
        found, missing = {}, []
        for name in names:
            rec = self.records.get(name.lower())
            if rec is None:
                missing.append(name)
            else:
                found[name.lower()] = self._public(rec)
        return found, missing

    def star_history(self, full_name: str, weeks: int) -> list[dict] | None:
        rec = self.records.get(full_name.lower(), {})
        if rec.get("star_error"):
            self.errors[full_name] = rec["star_error"]  # mimics GitHub refusing star history
            return None
        return history_from_dates(recent_star_dates(rec.get("stars_30d", 0), self.now))[:weeks]

    def contributors(self, full_name: str) -> int | None:
        return self.records.get(full_name.lower(), {}).get("contributors")

    def readme(self, full_name: str) -> str:
        return self.records.get(full_name.lower(), {}).get("readme", "")


def recent_star_dates(count: int, now: datetime) -> list[date]:
    """`count` star dates spread over the last 29 days, plus three from 40+ days ago."""
    days = [29 * (i + 0.5) / count for i in range(count)] + [40, 41, 42]
    return [(now - timedelta(days=d)).date() for d in days]


def history_from_dates(dates: list[date]) -> list[dict]:
    """Bucket star dates into GitHub's star-history shape: Sunday-start weeks, newest first."""
    weeks: dict[date, list[int]] = {}
    for d in dates:
        start = d - timedelta(days=(d.weekday() + 1) % 7)
        weeks.setdefault(start, [0] * 7)[(d - start).days] += 1
    return [{"week": int(datetime(s.year, s.month, s.day, tzinfo=timezone.utc).timestamp()),
             "total": sum(days), "days": days}
            for s, days in sorted(weeks.items(), reverse=True)]


def fixture_scorecards(gh: FixtureGitHub):
    def lookup(names: list[str], cache: dict, now: datetime) -> dict:
        return {n.lower(): gh.records.get(n.lower(), {}).get("scorecard") for n in names}
    return lookup
