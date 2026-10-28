"""GitHub REST + GraphQL: topic search, repo metadata, recent stargazers, contributors, README.

Works with the Actions GITHUB_TOKEN (1,000 requests/hour). Set GH_PAT for a
personal token's higher limits if the candidate pool grows.
"""

from __future__ import annotations

import os
import time
from urllib.parse import parse_qs, urlparse
from datetime import datetime, timedelta

import requests

from pipeline.config import parse_time

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
_STAR_FIELDS = """
  stargazers(first: 100, orderBy: {field: STARRED_AT, direction: DESC}%s) {
    edges { starredAt }
    pageInfo { hasNextPage endCursor }
  }
"""


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
        self.errors: dict[str, str] = {}  # owner/name -> GraphQL error message (other than not-found)

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

    def repos(self, names: list[str], now: datetime, with_stars: bool = False,
              window_days: int = 30, max_star_pages: int = 10) -> tuple[dict[str, dict], list[str]]:
        """Fetch metadata for owner/name strings. Returns ({lowercase name: record}, names not found).

        Repos that fail for any other reason are recorded in self.errors. With with_stars, they are
        retried without star history, so they come back without a starred_at field instead of vanishing.
        """
        found: dict[str, dict] = {}
        missing: list[str] = []
        failed: list[str] = []
        fields = _BASE_FIELDS + (_STAR_FIELDS % "" if with_stars else "")
        for start in range(0, len(names), BATCH):
            chunk = names[start:start + BATCH]
            params, parts, variables = [], [], {}
            for i, name in enumerate(chunk):
                owner, _, repo = name.partition("/")
                params.append(f"$o{i}: String!, $n{i}: String!")
                parts.append(f"r{i}: repository(owner: $o{i}, name: $n{i}) {{ {fields} }}")
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
                        failed.append(name)
                    continue
                record = from_graphql(node)
                if with_stars:
                    stars = node["stargazers"]
                    starred = [e["starredAt"] for e in stars["edges"]]
                    has_next = stars["pageInfo"]["hasNextPage"]
                    cursor = stars["pageInfo"]["endCursor"]
                    starred, has_next = self._more_stars(record["full_name"], starred, has_next, cursor,
                                                         now - timedelta(days=window_days), max_star_pages - 1)
                    record["starred_at"] = starred
                    record["starred_exhausted"] = not has_next
                # Keyed by the requested name so renamed repos still line up with their sources.
                found[name.lower()] = record
        if failed and with_stars:
            retried, gone = self.repos(failed, now)
            found.update(retried)
            missing += gone
        return found, missing

    def _more_stars(self, full_name: str, starred: list[str], has_next: bool, cursor: str | None,
                    cutoff: datetime, pages: int) -> tuple[list[str], bool]:
        """Keep paging while every star so far is newer than the cutoff."""
        owner, _, name = full_name.partition("/")
        query = ("query($o: String!, $n: String!, $c: String) { repository(owner: $o, name: $n) { "
                 + _STAR_FIELDS % ", after: $c" + " } }")
        while has_next and pages > 0 and starred and parse_time(starred[-1]) >= cutoff:
            repo = self.graphql(query, {"o": owner, "n": name, "c": cursor})["data"].get("repository")
            if repo is None:  # keep what we have; the count is flagged as estimated
                break
            stars = repo["stargazers"]
            starred += [e["starredAt"] for e in stars["edges"]]
            has_next, cursor = stars["pageInfo"]["hasNextPage"], stars["pageInfo"]["endCursor"]
            pages -= 1
        return starred, has_next

    # -- per-repo REST ----------------------------------------------------

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


def stars_gained(starred_at: list[str], exhausted: bool, now: datetime, days: int) -> tuple[int, bool]:
    """Stars gained in the last `days` from a newest-first list of starredAt times.

    Returns (count, estimated). When every fetched star is inside the window and
    more pages exist, the count is extrapolated from the fetched rate.
    """
    cutoff = now - timedelta(days=days)
    times = [parse_time(t) for t in starred_at]
    recent = sum(1 for t in times if t >= cutoff)
    if recent < len(times) or exhausted:
        return recent, False
    span_days = max((now - times[-1]).total_seconds() / 86400, 1 / 24)
    return round(len(times) / span_days * days), True


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
