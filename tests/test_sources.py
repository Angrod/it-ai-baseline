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


def week(y, m, d, days):
    """One star-history entry: Sunday-start week, Unix timestamp, per-day counts."""
    ts = int(datetime(y, m, d, tzinfo=timezone.utc).timestamp())
    return {"week": ts, "total": sum(days), "days": days}


# NOW is Monday 2026-10-26. A 30-day window covers 09-27..10-26; a 7-day window 10-20..10-26.
HISTORY = [
    week(2026, 10, 25, [3, 2, 50, 0, 0, 0, 0]),   # Sun 3 + Mon 2 count; Tue is in the future
    week(2026, 10, 18, [1, 1, 1, 1, 1, 1, 1]),    # all 7 in 30d; Tue-Sat (5) in 7d
    week(2026, 9, 27, [4, 0, 0, 0, 0, 0, 0]),     # first day of the 30-day window
    week(2026, 9, 20, [9, 9, 9, 9, 9, 9, 9]),     # entirely before the window
]


def test_stars_gained_counts_days_inside_the_window():
    assert stars_gained(HISTORY, NOW, 30) == 5 + 7 + 4
    assert stars_gained(HISTORY, NOW, 7) == 5 + 5


def test_stars_gained_empty_history_is_zero():
    assert stars_gained([], NOW, 30) == 0
