"""End-to-end offline build against tests/fixtures."""

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline import build
from pipeline.config import Settings
from pipeline.offline import FixtureGitHub, fixture_scorecards

FIXTURES = Path(__file__).parent / "fixtures"
NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)


class FakeClassifier:
    """Scores everything fit 1, except a few names with fixed answers."""

    ANSWERS = {
        "acme-it/okta-offboarder": {"fit": 3, "tags": ["identity", "helpdesk"]},
        "acme-it/gam-docs-generator": {"fit": 0, "tags": []},
        "gam-team/gam": {"fit": 1, "tags": ["saas"]},  # the human override (fit 3) must win
    }

    def __init__(self):
        self.seen = []

    def classify(self, repo, readme):
        self.seen.append(repo["full_name"])
        answer = self.ANSWERS.get(repo["full_name"].lower(), {"fit": 1, "tags": []})
        return {"status": "scored", "why": f"why {repo['full_name']}", "first_step": "try it",
                "readonly_mode": None, **answer}


def run(tmp_path, classifier=None, mode="live"):
    gh = FixtureGitHub(FIXTURES)
    return build.build(Settings(), gh, NOW, snapshot_dir=FIXTURES / "snapshots",
                       scorecard_lookup=fixture_scorecards(gh), classify_mode=mode, classifier=classifier,
                       out=tmp_path / "data.json", review=tmp_path / "review.md", cache_dir=tmp_path / "cache")


@pytest.fixture
def scored(tmp_path):
    classifier = FakeClassifier()
    return run(tmp_path, classifier), classifier, tmp_path


def test_trending_view_is_it_only(scored):
    data, _, _ = scored
    trending = data["views"]["trending"]
    assert "acme-it/ai-chat-framework" not in trending      # trends hardest, but not IT
    assert "acme-it/forked-gam" not in trending              # forks are dropped
    assert "acme-it/old-jamf-tool" not in trending           # archived repos are never ranked
    assert "anthropics/skills" not in trending               # foundations are shown, never ranked
    assert "acme-it/gam-docs-generator" not in trending      # Claude scored it fit 0
    ranks = [data["repos"][k]["trend_rank"] for k in trending]
    assert ranks == list(range(1, len(trending) + 1))


def test_lens_needs_gate_and_fit(scored):
    data, _, _ = scored
    lens = data["views"]["lens"]
    assert "acme-it/okta-offboarder" in lens
    assert "acme-it/tiny-intune-script" not in lens   # fails the traction gate
    assert "acme-it/old-jamf-tool" not in lens        # archived
    fits = [data["repos"][k]["fit"] for k in lens]
    assert fits == sorted(fits, reverse=True)
    assert [data["repos"][k]["lens_rank"] for k in lens] == list(range(1, len(lens) + 1))


def test_human_override_beats_claude(scored):
    data, classifier, _ = scored
    gam = data["repos"]["gam-team/gam"]
    assert gam["fit"] == 3 and gam["scored_by"] == "human"
    assert "GAM-team/GAM" not in classifier.seen  # fully overridden repos never cost an API call


def test_counts_flow_through(scored):
    data, _, _ = scored
    mcp = data["repos"]["taylorwilsdon/google_workspace_mcp"]
    assert mcp["times_trending_30d"] == 5
    assert mcp["stars_gained_30d"] == 210
    assert mcp["trust_badge"] in {"production", "pilot", "experimental"}
    assert data["methodology"]["history_days"] == 7


def test_baseline_flags_missing_repos(scored):
    data, _, tmp_path = scored
    endpoint = next(d for d in data["baseline"]["domains"] if d["id"] == "endpoint")
    hub = next(e for e in endpoint["cells"]["L2"] if e.get("repo") == "Jamf-Concepts/mcp-hub")
    assert hub["unverified"] is True
    assert "anthropics/skills" in data["repos"]
    review = (tmp_path / "review.md").read_text()
    assert "Jamf-Concepts/mcp-hub" in review
    assert "acme-it/okta-offboarder" in review


def test_star_history_failure_keeps_repo_ranked(scored):
    data, _, tmp_path = scored
    munki = data["repos"]["munki/munki"]
    assert munki["stars_gained_unknown"] is True and munki["stars_gained_30d"] == 0
    assert "munki/munki" in data["views"]["trending"]
    review = (tmp_path / "review.md").read_text()
    assert "## Fetch problems" in review and "GH_PAT" in review
    assert "- munki/munki" not in review.split("## Fetch problems")[0]  # not reported as "not found"


def test_cache_prevents_rescoring(tmp_path):
    first = FakeClassifier()
    run(tmp_path, first)
    second = FakeClassifier()
    run(tmp_path, second)
    assert first.seen and second.seen == []


def test_classify_off_leaves_unscored_repos_out_of_lens(tmp_path):
    data = run(tmp_path, mode="off")
    assert "acme-it/okta-offboarder" in data["views"]["trending"]
    assert "acme-it/okta-offboarder" not in data["views"]["lens"]
    assert data["repos"]["acme-it/okta-offboarder"]["fit"] is None
    assert "okta/okta-mcp-server" in data["views"]["lens"]  # human-scored via overrides


def test_output_is_json_serializable(scored):
    _, _, tmp_path = scored
    json.loads((tmp_path / "data.json").read_text())
