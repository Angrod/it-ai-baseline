"""GitHub client against a fake HTTP session: query shape, star paging, Link-header counts."""

from datetime import datetime, timedelta, timezone

from pipeline.sources.github_api import TOO_MANY_CONTRIBUTORS, GitHub

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)


def ago(days):
    return (NOW - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


class Resp:
    def __init__(self, body=None, status=200, links=None, text=""):
        self.body, self.status_code, self.links, self.text = body, status, links or {}, text

    def json(self):
        return self.body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(self.status_code)


class Session:
    def __init__(self, posts=(), gets=()):
        self.headers, self.posts, self.gets, self.sent = {}, list(posts), list(gets), []

    def post(self, url, json=None, timeout=None):
        self.sent.append(json)
        return self.posts.pop(0)

    def get(self, url, params=None, headers=None, timeout=None):
        self.sent.append((url, params))
        return self.gets.pop(0)


def node(name, starred, has_next):
    return {
        "nameWithOwner": name, "url": f"https://github.com/{name}", "description": "d", "stargazerCount": 500,
        "forkCount": 1, "isArchived": False, "isFork": False, "pushedAt": ago(1), "createdAt": ago(400),
        "primaryLanguage": {"name": "Go"}, "licenseInfo": {"spdxId": "MIT"},
        "owner": {"__typename": "Organization", "login": name.split("/")[0]},
        "repositoryTopics": {"nodes": [{"topic": {"name": "okta"}}]},
        "latestRelease": None,
        "stargazers": {"edges": [{"starredAt": t} for t in starred],
                       "pageInfo": {"hasNextPage": has_next, "endCursor": "c1"}},
    }


def test_repos_pages_stars_until_past_the_window_and_reports_missing():
    first_page = [ago(1)] * 100
    second_page = [ago(5)] * 50 + [ago(45)] * 50
    session = Session(posts=[
        Resp({"data": {"r0": node("acme-it/hot", first_page, True), "r1": None}}),
        Resp({"data": {"repository": {"stargazers": {"edges": [{"starredAt": t} for t in second_page],
                                                     "pageInfo": {"hasNextPage": True, "endCursor": "c2"}}}}}),
    ])
    found, missing = GitHub(token="t", session=session).repos(["acme-it/hot", "acme-it/gone"], NOW, with_stars=True)
    assert missing == ["acme-it/gone"]
    rec = found["acme-it/hot"]
    assert rec["topics"] == ["okta"] and rec["owner_type"] == "Organization" and rec["license"] == "MIT"
    assert len(rec["starred_at"]) == 200 and rec["starred_exhausted"] is False
    batch_query = session.sent[0]
    assert batch_query["variables"] == {"o0": "acme-it", "n0": "hot", "o1": "acme-it", "n1": "gone"}
    assert "orderBy: {field: STARRED_AT, direction: DESC}" in batch_query["query"]
    assert session.sent[1]["variables"]["c"] == "c1"
    assert len(session.posts) == 0  # stopped once the oldest star left the window


def test_contributors_from_link_header():
    last = "https://api.github.com/repositories/1/contributors?per_page=1&anon=false&page=37"
    gh = GitHub(token="t", session=Session(gets=[
        Resp([{}], links={"last": {"url": last}}),
        Resp([{}]),
        Resp(status=403, text="The history or contributor list is too large to list contributors"),
        Resp(status=404),
    ]))
    assert gh.contributors("a/b") == 37
    assert gh.contributors("a/b") == 1
    assert gh.contributors("a/b") == TOO_MANY_CONTRIBUTORS
    assert gh.contributors("a/b") is None


def test_search_skips_rejected_queries():
    item = {"full_name": "acme-it/x", "html_url": "u", "stargazers_count": 9, "owner": {"login": "acme-it", "type": "User"},
            "license": None, "topics": ["jamf"]}
    gh = GitHub(token="t", session=Session(gets=[Resp({"items": [item]}), Resp(status=422)]))
    assert [r["full_name"] for r in gh.search("topic:jamf", 5, pause=0)] == ["acme-it/x"]
    assert gh.search("topic:bad!", 5, pause=0) == []
