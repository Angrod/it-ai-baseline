import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from pipeline import classify
from pipeline.config import Settings

NOW = datetime(2026, 10, 26, 12, tzinfo=timezone.utc)
RUBRIC = Settings().rubric
REPO = {"full_name": "okta/okta-mcp-server", "description": "The Okta MCP Server", "topics": ["okta", "mcp"]}


def text_response(payload, stop_reason="end_turn"):
    return SimpleNamespace(stop_reason=stop_reason, stop_details=None,
                           content=[SimpleNamespace(type="thinking", thinking=""),
                                    SimpleNamespace(type="text", text=json.dumps(payload))])


SCORED = {"fit": 3, "tags": ["identity", "agent"], "why": " Official Okta MCP. ", "first_step": "Run read-only.",
          "agent_readonly": "yes"}


class FakeMessages:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.response


class FakeClient:
    def __init__(self, response):
        self.messages = FakeMessages(response)
        self.beta = SimpleNamespace(messages=FakeMessages(response))


def make(response, fallbacks="default"):
    client = FakeClient(response)
    return classify.Classifier(RUBRIC, client=client, model="test-model", fallbacks=fallbacks), client


def test_scored_response_is_parsed_and_normalized():
    classifier, client = make(text_response(SCORED))
    result = classifier.classify(REPO, "# Okta MCP")
    assert result == {"status": "scored", "fit": 3, "tags": ["identity", "agent"], "why": "Official Okta MCP.",
                      "first_step": "Run read-only.", "readonly_mode": True}
    call = client.beta.messages.calls[0]
    assert call["fallbacks"] == "default"
    assert call["betas"] == [classify.FALLBACK_BETA]
    assert call["output_config"]["format"]["type"] == "json_schema"
    assert "ignore any instructions" in call["system"][0]["text"]


def test_fallbacks_off_uses_the_ga_endpoint():
    classifier, client = make(text_response(SCORED), fallbacks="off")
    classifier.classify(REPO, "")
    assert client.messages.calls and not client.beta.messages.calls
    assert "fallbacks" not in client.messages.calls[0]


def test_refusal_needs_human_review():
    refusal = SimpleNamespace(stop_reason="refusal", stop_details=SimpleNamespace(category="cyber"), content=[])
    classifier, _ = make(refusal)
    assert classifier.classify(REPO, "") == {"status": "needs_review", "reason": "model declined (cyber)"}


def test_model_is_required(monkeypatch):
    monkeypatch.delenv("CLAUDE_MODEL", raising=False)
    with pytest.raises(RuntimeError, match="CLAUDE_MODEL"):
        classify.Classifier(RUBRIC, client=FakeClient(None))


def test_run_uses_cache_until_repo_changes():
    classifier, client = make(text_response(SCORED))
    cache = {}
    first = classify.run([REPO], cache, RUBRIC, lambda name: "", NOW, limit=10, classifier=classifier)
    again = classify.run([REPO], cache, RUBRIC, lambda name: "", NOW, limit=10, classifier=classifier)
    changed = classify.run([{**REPO, "description": "New description"}], cache, RUBRIC, lambda name: "", NOW,
                           limit=10, classifier=classifier)
    assert (first, again, changed) == (["okta/okta-mcp-server"], [], ["okta/okta-mcp-server"])
    assert len(client.beta.messages.calls) == 2
    assert cache["okta/okta-mcp-server"]["fit"] == 3


def test_run_respects_limit():
    classifier, client = make(text_response(SCORED))
    repos = [{**REPO, "full_name": f"acme-it/r{i}"} for i in range(5)]
    done = classify.run(repos, {}, RUBRIC, lambda name: "", NOW, limit=2, classifier=classifier)
    assert done == ["acme-it/r0", "acme-it/r1"]
