"""GitHub REST + GraphQL: topic search, repo metadata, star history, contributors, README.

Star history costs one request per tracked repo, so set GH_PAT (5,000 requests/hour)
rather than relying on the Actions GITHUB_TOKEN (1,000/hour).
"""

from __future__ import annotations

import os
import time
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timedelta, timezone

import requests

API = "https://api.github.com"
GRAPHQL = f"{API}/graphql"
BATCH = 20
# GitHub refuses to list contributors for very large histories; that alone says "many".
TOO_MANY_CONTRIBUTORS = 1000

_BASE_FIELDS = """
  nameWithOwner url description stargazerCount forkCount isArchived isFork pushedAt createdAt
  primaryLanguage { name }
  licenseInfo { spdxId }
  owner { __typename login }
  repositoryTopics(first: 20) { nodes { topic { name } } }
  latestRelease { publishedAt }
"""
# Since mid-2026 GitHub lists individual stargazers only to a repo's admins and collaborators;
# everyone else gets empty results. /stargazers/history serves counts instead, on this API version.
STAR_HISTORY_API_VERSION = "2026-03-10"


class GitHub:
    def __init__(self, token: str | None = None, session: requests.Session | None = None):
        token = token or os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN")
        self.session = session or requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "it-ai-baseline",
        })
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        self.errors: dict[str, str] = {}  # owner/name -> why GitHub wouldn't serve it (other than not-found)

    # -- search -----------------------------------------------------------

    def search(self, query: str, per_page: int, pause: float = 2.2) -> list[dict]:
        """Repo search, highest stars first. Search allows 30 requests/minute, hence the pause."""
        resp = self.session.get(f"{API}/search/repositories",
                                params={"q": query, "sort": "stars", "order": "desc", "per_page": per_page},
                                timeout=30)
        time.sleep(pause)
        if resp.status_code == 422:  # GitHub rejects some topic names; skip rather than fail the run
            return []
        resp.raise_for_status()
        return [from_rest(item) for item in resp.json().get("items", [])]

    # -- graphql ----------------------------------------------------------

    def graphql(self, query: str, variables: dict) -> dict:
        resp = self.session.post(GRAPHQL, json={"query": query, "variables": variables}, timeout=60)
        resp.raise_for_status()
        body = resp.json()
        if not body.get("data"):
            raise RuntimeError(f"GraphQL error: {body.get('errors')}")
        return body

    def repos(self, names: list[str]) -> tuple[dict[str, dict], list[str]]:
        """Fetch metadata for owner/name strings. Returns ({lowercase name: record}, names not found).

        Repos that fail for any other reason are left out and recorded in self.errors.
        """
        found: dict[str, dict] = {}
        missing: list[str] = []
        for start in range(0, len(names), BATCH):
            chunk = names[start:start + BATCH]
            params, parts, variables = [], [], {}
            for i, name in enumerate(chunk):
                owner, _, repo = name.partition("/")
                params.append(f"$o{i}: String!, $n{i}: String!")
                parts.append(f"r{i}: repository(owner: $o{i}, name: $n{i}) {{ {_BASE_FIELDS} }}")
                variables[f"o{i}"], variables[f"n{i}"] = owner, repo
            query = f"query({', '.join(params)}) {{ {' '.join(parts)} }}"
            body = self.graphql(query, variables)
            data = body["data"]
            errors = {e["path"][0]: e for e in body.get("errors", []) if e.get("path")}
            for i, name in enumerate(chunk):
                node = data.get(f"r{i}")
                if node is None:
                    error = errors.get(f"r{i}", {})
                    if error.get("type", "NOT_FOUND") == "NOT_FOUND":
                        missing.append(name)
                    else:
                        self.errors[name] = error.get("message", "unknown GraphQL error")
                    continue
                # Keyed by the requested name so renamed repos still line up with their sources.
                found[name.lower()] = from_graphql(node)
        return found, missing

    # -- per-repo REST ----------------------------------------------------

    def star_history(self, full_name: str, weeks: int) -> list[dict] | None:
        """Weekly star counts, newest week first: [{"week": unix start, "total": n, "days": [Sun..Sat]}].

        Returns None, with the reason in self.errors, when GitHub won't serve it.
        """
        resp = self.session.get(f"{API}/repos/{full_name}/stargazers/history", params={"per_page": weeks},
                                headers={"X-GitHub-Api-Version": STAR_HISTORY_API_VERSION}, timeout=30)
        if resp.status_code != 200:
            self.errors[full_name] = f"star history returned HTTP {resp.status_code}"
            return None
        return resp.json()

    def contributors(self, full_name: str) -> int | None:
        """Contributor count from the Link header's last page (one request)."""
        resp = self.session.get(f"{API}/repos/{full_name}/contributors", params={"per_page": 1, "anon": "false"},
                                timeout=30)
        if resp.status_code == 403 and "too large" in resp.text:
            return TOO_MANY_CONTRIBUTORS
        if resp.status_code in (204, 403, 404):
            return None
        resp.raise_for_status()
        last = resp.links.get("last", {}).get("url")
        if not last:
            return len(resp.json())
        return int(parse_qs(urlparse(last).query)["page"][0])

    def readme(self, full_name: str, limit: int = 8000) -> str:
        resp = self.session.get(f"{API}/repos/{full_name}/readme",
                                headers={"Accept": "application/vnd.github.raw"}, timeout=30)
        if resp.status_code == 404:
            return ""
        resp.raise_for_status()
        return resp.text[:limit]


def stars_gained(history: list[dict], now: datetime, days: int) -> int:
    """Stars gained in the last `days` days (today included) from star_history weeks.

    GitHub only counts stars that still exist, and its week/day boundaries may not align
    with UTC, so the window edge can be off by a day.
    """
    first_day = (now - timedelta(days=days - 1)).date()
    today = now.date()
    total = 0
    for week in history:
        start = datetime.fromtimestamp(week["week"], tz=timezone.utc).date()
        for offset, count in enumerate(week.get("days", [])):
            if first_day <= start + timedelta(days=offset) <= today:
                total += count
    return total


def from_rest(item: dict) -> dict:
    return {
        "full_name": item["full_name"],
        "url": item["html_url"],
        "description": item.get("description") or "",
        "language": item.get("language"),
        "topics": item.get("topics") or [],
        "stars": item.get("stargazers_count", 0),
        "forks": item.get("forks_count", 0),
        "archived": item.get("archived", False),
        "fork": item.get("fork", False),
        "pushed_at": item.get("pushed_at"),
        "created_at": item.get("created_at"),
        "license": (item.get("license") or {}).get("spdx_id"),
        "owner": item["owner"]["login"],
        "owner_type": item["owner"].get("type"),
    }


def from_graphql(node: dict) -> dict:
    return {
        "full_name": node["nameWithOwner"],
        "url": node["url"],
        "description": node.get("description") or "",
        "language": (node.get("primaryLanguage") or {}).get("name"),
        "topics": [t["topic"]["name"] for t in node["repositoryTopics"]["nodes"]],
        "stars": node["stargazerCount"],
        "forks": node["forkCount"],
        "archived": node["isArchived"],
        "fork": node["isFork"],
        "pushed_at": node["pushedAt"],
        "created_at": node["createdAt"],
        "license": (node.get("licenseInfo") or {}).get("spdxId"),
        "owner": node["owner"]["login"],
        "owner_type": node["owner"]["__typename"],
        "latest_release_at": (node.get("latestRelease") or {}).get("publishedAt"),
    }
