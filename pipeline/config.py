"""Paths and YAML/JSON loaders shared by every pipeline stage."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
CURATION = ROOT / "curation"
DATA = ROOT / "data"
SNAPSHOTS = DATA / "snapshots" / "trending"
CACHE = DATA / "cache"
SITE = ROOT / "site"


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def days_since(value: str | None, now: datetime) -> float | None:
    dt = parse_time(value)
    if dt is None:
        return None
    return (now - dt).total_seconds() / 86400


class Settings:
    """All config files, loaded once."""

    def __init__(self, config_dir: Path = CONFIG, curation_dir: Path = CURATION):
        self.rubric = load_yaml(config_dir / "rubric.yaml")
        self.topics = load_yaml(config_dir / "topics.yaml")
        self.scoring = load_yaml(config_dir / "scoring.yaml")
        self.orgs = load_yaml(config_dir / "orgs.yaml")
        self.baseline = load_yaml(curation_dir / "baseline.yaml")
        self.overrides = load_yaml(curation_dir / "overrides.yaml")
        self.nominations = load_yaml(curation_dir / "nominations.yaml").get("repos", [])

    @property
    def tags(self) -> list[dict]:
        return self.rubric["tags"]

    def baseline_repos(self) -> list[str]:
        """Repos in the matrix cells. These join the ranking pool like nominations."""
        repos = []
        for domain in self.baseline.get("domains", []):
            for entries in domain.get("cells", {}).values():
                repos.extend(e["repo"] for e in entries or [] if "repo" in e)
        return list(dict.fromkeys(repos))

    def foundation_repos(self) -> list[str]:
        """Cross-cutting building blocks: shown with live data, never ranked."""
        return [f["repo"] for f in self.baseline.get("foundations", []) if "repo" in f]
