"""Fixture-backed stand-ins for the network sources, used by tests and `build --offline`.

A fixture directory holds repos.json ({owner/name: record}) and snapshots/*.json.
Records use the same shape the GitHub client returns, plus optional
`stars_30d`, `contributors`, `scorecard` and `readme` fields.
"""

from __future__ import annotations

import copy
from datetime import datetime, timedelta
from pathlib import Path

from pipeline.config import load_json


class FixtureGitHub:
    def __init__(self, directory: Path):
        raw = load_json(Path(directory) / "repos.json", {})
        self.records = {name.lower(): {"full_name": name, **rec} for name, rec in raw.items()}

    def _public(self, rec: dict, with_stars: bool, now: datetime | None = None) -> dict:
        out = {k: copy.deepcopy(v) for k, v in rec.items() if k not in ("stars_30d", "contributors", "scorecard", "readme")}
        if with_stars:
            out["starred_at"] = recent_stars(rec.get("stars_30d", 0), now)
            out["starred_exhausted"] = True
        return out

    def search(self, query: str, per_page: int) -> list[dict]:
        if not query.startswith("topic:"):
            return []
        topic = query.split()[0].removeprefix("topic:")
        hits = [r for r in self.records.values() if topic in r.get("topics", [])]
        return [self._public(r, False) for r in hits[:per_page]]

    def repos(self, names: list[str], now: datetime, with_stars: bool = False, **_) -> tuple[dict, list[str]]:
        found, missing = {}, []
        for name in names:
            rec = self.records.get(name.lower())
            if rec is None:
                missing.append(name)
            else:
                found[name.lower()] = self._public(rec, with_stars, now)
        return found, missing

    def contributors(self, full_name: str) -> int | None:
        return self.records.get(full_name.lower(), {}).get("contributors")

    def readme(self, full_name: str) -> str:
        return self.records.get(full_name.lower(), {}).get("readme", "")


def recent_stars(count: int, now: datetime) -> list[str]:
    """Newest-first starredAt times: `count` spread over the last 30 days, then three older ones."""
    days = [30 * (i + 0.5) / count for i in range(count)] + [40, 41, 42]
    return [(now - timedelta(days=d)).strftime("%Y-%m-%dT%H:%M:%SZ") for d in days]


def fixture_scorecards(gh: FixtureGitHub):
    def lookup(names: list[str], cache: dict, now: datetime) -> dict:
        return {n.lower(): gh.records.get(n.lower(), {}).get("scorecard") for n in names}
    return lookup
