import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pipeline.sources import github_trending
from pipeline.sources.github_api import stars_gained

FIXTURES = Path(__file__).parent / "fixtures"
NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)


def ago(days):
    return (NOW - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_parse_trending_page():
    rows = github_trending.parse_trending((FIXTURES / "trending.html").read_text())
    assert rows == [
        {"repo": "acme-it/okta-offboarder", "rank": 1, "period_stars": 1021},
        {"repo": "GAM-team/GAM", "rank": 2, "period_stars": 87},
    ]


def test_snapshot_window_excludes_old_days():
    snaps = github_trending.load_snapshots(FIXTURES / "snapshots", NOW, 30)
    assert len(snaps) == 7
    assert all(s["date"] != "2026-09-21" for s in snaps)


def test_times_trending_counts_distinct_days():
    snaps = github_trending.load_snapshots(FIXTURES / "snapshots", NOW, 30)
    counts = github_trending.times_trending(snaps)
    # Listed on all/daily and powershell/daily on the same days: still one per day.
    assert counts["taylorwilsdon/google_workspace_mcp"] == 5
    assert counts["acme-it/ai-chat-framework"] == 4
    assert "acme-it/old-jamf-tool" not in counts


def test_weekly_pages_feed_the_pool_but_not_the_count(tmp_path):
    snap = {"date": "2026-10-25", "pages": {"all/weekly": [{"repo": "a/b", "rank": 1, "period_stars": 9}]}}
    (tmp_path / "2026-10-25.json").write_text(json.dumps(snap))
    snaps = github_trending.load_snapshots(tmp_path, NOW, 30)
    assert github_trending.times_trending(snaps) == {}
    assert github_trending.pool_from_snapshots(snaps) == {"a/b": "a/b"}


def test_prune_removes_only_expired_snapshots(tmp_path):
    for day in ("2026-08-01", "2026-10-20"):
        (tmp_path / f"{day}.json").write_text("{}")
    removed = github_trending.prune(tmp_path, NOW, 45)
    assert [p.name for p in removed] == ["2026-08-01.json"]
    assert (tmp_path / "2026-10-20.json").exists()


def test_stars_gained_counts_inside_window():
    starred = [ago(1), ago(5), ago(20), ago(40)]
    assert stars_gained(starred, exhausted=False, now=NOW, days=30) == (3, False)
    assert stars_gained(starred, exhausted=False, now=NOW, days=7) == (2, False)


def test_stars_gained_extrapolates_when_sample_is_all_recent():
    starred = [ago(10 * (i + 1) / 100) for i in range(100)]  # 100 stars over the last 10 days
    count, estimated = stars_gained(starred, exhausted=False, now=NOW, days=30)
    assert estimated
    assert count == 300


def test_stars_gained_exact_when_history_exhausted():
    starred = [ago(1), ago(2)]
    assert stars_gained(starred, exhausted=True, now=NOW, days=30) == (2, False)
