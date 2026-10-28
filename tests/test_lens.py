from datetime import datetime, timedelta, timezone

import pytest

from pipeline import lens
from pipeline.config import Settings

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
SETTINGS = Settings()
COMPILED = lens.compile_tags(SETTINGS.tags)
GATE = SETTINGS.scoring["lens"]["gate"]
TRUST = SETTINGS.scoring["trust"]


def ago(days):
    return (NOW - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


def repo(**kw):
    base = {"full_name": "acme-it/tool", "description": "", "topics": [], "stars": 0, "archived": False,
            "pushed_at": ago(3), "license": "MIT", "owner": "acme-it", "owner_type": "Organization"}
    base.update(kw)
    return base


@pytest.mark.parametrize("rec, expected", [
    (repo(description="Automated Okta offboarding with SCIM deprovisioning"), ["identity", "helpdesk"]),
    (repo(full_name="taylorwilsdon/google_workspace_mcp"), ["saas", "agent"]),
    (repo(topics=["jamf"]), ["endpoint"]),
    (repo(description="Gamma ray burst visualizer"), []),          # "gam" must be a whole word
    (repo(description="A framework for building chat apps"), []),
])
def test_match_tags(rec, expected):
    assert lens.match_tags(rec, COMPILED) == expected


def test_agent_tag_alone_is_not_it_relevant():
    assert not lens.is_relevant(["agent"], SETTINGS.tags)
    assert lens.is_relevant(["agent", "identity"], SETTINGS.tags)


@pytest.mark.parametrize("rec, passed", [
    (repo(stars=500), True),
    (repo(stars=10, stars_gained_30d=50), True),
    (repo(stars=10, times_trending_30d=1), True),
    (repo(stars=499, stars_gained_30d=49, times_trending_30d=0), False),
    (repo(stars=5000, archived=True), False),
    (repo(stars=5000, pushed_at=ago(181)), False),
    (repo(stars=5000, license="NOASSERTION"), False),
    (repo(stars=5000, license=None), False),
])
def test_gate(rec, passed):
    assert lens.gate(rec, GATE, NOW)[0] is passed


def test_gate_reports_why_it_failed():
    ok, reasons = lens.gate(repo(stars=5000, archived=True, pushed_at=ago(400)), GATE, NOW)
    assert not ok
    assert reasons == ["archived", "no push in 180 days"]


def test_trust_vendor_repo_is_production_ready():
    rec = repo(owner="okta", latest_release_at=ago(20), contributors=12)
    score, badge, reasons = lens.trust(rec, TRUST, SETTINGS.orgs, NOW)
    # 30 maintenance + 15 release + 15 community + 10 license + 15 vendor + 7.5 neutral scorecard
    assert score == round(92.5)
    assert badge == "production"
    assert "vendor or foundation maintained" in reasons


def test_trust_personal_unlicensed_stale_repo_is_experimental():
    rec = repo(owner="someone", owner_type="User", pushed_at=ago(100), license=None, contributors=2)
    score, badge, _ = lens.trust(rec, TRUST, SETTINGS.orgs, NOW)
    # 10 maintenance + 0 releases + 3 community + 0 license + 3 personal + 7.5 scorecard
    assert score == round(23.5)
    assert badge == "experimental"


def test_trust_readonly_mode_only_counts_for_agent_tools():
    base = repo(owner="someone", owner_type="User", latest_release_at=ago(20), contributors=4)
    plain, _, _ = lens.trust({**base, "tags": ["identity"], "readonly_mode": True}, TRUST, SETTINGS.orgs, NOW)
    agent_ro, _, _ = lens.trust({**base, "tags": ["identity", "agent"], "readonly_mode": True}, TRUST, SETTINGS.orgs, NOW)
    agent_rw, _, _ = lens.trust({**base, "tags": ["identity", "agent"], "readonly_mode": False}, TRUST, SETTINGS.orgs, NOW)
    assert agent_ro == plain + TRUST["readonly_bonus"]
    assert agent_rw == plain - TRUST["readonly_penalty"]


def test_small_org_repo_without_scorecard_is_only_pilot():
    rec = repo(latest_release_at=ago(20), contributors=4)
    # 30 + 15 + 10 community + 10 license + 7.5 org + 7.5 neutral scorecard
    assert lens.trust(rec, TRUST, SETTINGS.orgs, NOW)[:2] == (80, "pilot")


def test_archived_is_always_experimental():
    rec = repo(owner="okta", latest_release_at=ago(20), contributors=50, archived=True)
    assert lens.trust(rec, TRUST, SETTINGS.orgs, NOW)[1] == "experimental"


def test_lens_sort_prefers_fit_then_trust_then_momentum():
    a = {"fit": 3, "trust_score": 60, "trend_score": 10}
    b = {"fit": 3, "trust_score": 80, "trend_score": 1}
    c = {"fit": 2, "trust_score": 99, "trend_score": 99}
    assert sorted([c, a, b], key=lens.lens_sort_key) == [b, a, c]
