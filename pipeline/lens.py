"""IT Ops lens: rubric tag matching, the validation gate, and the trust score."""

from __future__ import annotations

import re
from datetime import datetime

from pipeline.config import days_since

UNRECOGNISED_LICENSES = {None, "", "NOASSERTION", "OTHER"}


# -- tags ---------------------------------------------------------------------

def compile_tags(tags: list[dict]) -> list[tuple[str, set[str], re.Pattern | None]]:
    compiled = []
    for tag in tags:
        words = sorted(tag.get("keywords", []), key=len, reverse=True)
        pattern = None
        if words:
            alternation = "|".join(re.escape(w.lower()) for w in words)
            pattern = re.compile(rf"(?<![a-z0-9])(?:{alternation})(?![a-z0-9])")
        compiled.append((tag["id"], {t.lower() for t in tag.get("topics", [])}, pattern))
    return compiled


def match_tags(repo: dict, compiled: list) -> list[str]:
    """Tags whose topics or keywords appear on the repo (name + description + topics)."""
    topics = {t.lower() for t in repo.get("topics", [])}
    name = repo["full_name"].split("/")[-1].replace("-", " ").replace("_", " ")
    text = f"{name} {repo.get('description') or ''}".lower()
    return [tag_id for tag_id, tag_topics, pattern in compiled
            if topics & tag_topics or (pattern and pattern.search(text))]


def is_relevant(tag_ids: list[str], tags: list[dict]) -> bool:
    domain = {t["id"] for t in tags if t.get("domain")}
    return any(t in domain for t in tag_ids)


# -- gate ---------------------------------------------------------------------

def gate(repo: dict, cfg: dict, now: datetime) -> tuple[bool, list[str]]:
    """Validated = traction (any one) AND healthy (all). Returns (passed, reasons it failed)."""
    failures = []
    traction = (repo.get("stars", 0) >= cfg["min_stars"]
                or repo.get("stars_gained_30d", 0) >= cfg["min_stars_gained_30d"]
                or repo.get("times_trending_30d", 0) >= cfg["min_times_trending_30d"])
    if not traction:
        failures.append(f"under {cfg['min_stars']} stars, {cfg['min_stars_gained_30d']} gained/30d "
                        f"and {cfg['min_times_trending_30d']} trending days")
    if repo.get("archived"):
        failures.append("archived")
    age = days_since(repo.get("pushed_at"), now)
    if age is None or age > cfg["max_days_since_push"]:
        failures.append(f"no push in {cfg['max_days_since_push']} days")
    if cfg.get("require_license") and repo.get("license") in UNRECOGNISED_LICENSES:
        failures.append("no recognised license")
    return not failures, failures


# -- trust --------------------------------------------------------------------

def provenance(owner: str, owner_type: str | None, orgs: dict) -> tuple[float, str]:
    login = owner.lower()
    if login in {o.lower() for o in orgs.get("vendor", [])}:
        return 1.0, "vendor or foundation maintained"
    if login in {o.lower() for o in orgs.get("community", [])}:
        return 0.8, "established community org"
    if owner_type == "Organization":
        return 0.5, "organization-owned"
    return 0.2, "personal project"


def trust(repo: dict, cfg: dict, orgs: dict, now: datetime) -> tuple[int, str, list[str]]:
    """Deploy-safety score 0-100, a badge, and the human-readable reasons behind it."""
    pts = cfg["points"]
    score = 0.0
    reasons = []

    age = days_since(repo.get("pushed_at"), now)
    if age is not None and age <= 30:
        frac = 1.0
    elif age is not None and age <= 90:
        frac = 2 / 3
    elif age is not None and age <= 180:
        frac = 1 / 3
    else:
        frac = 0.0
    score += pts["maintenance"] * frac
    reasons.append(f"last push {round(age)}d ago" if age is not None else "no push date")

    release_age = days_since(repo.get("latest_release_at"), now)
    if release_age is not None and release_age <= 180:
        score += pts["releases"]
        reasons.append("release in last 180d")
    elif release_age is not None:
        score += pts["releases"] / 2
        reasons.append("has releases (none recent)")
    else:
        reasons.append("no GitHub releases")

    contributors = repo.get("contributors")
    if contributors is None:
        score += pts["community"] * 2 / 3
        reasons.append("contributors not checked")
    elif contributors >= 10:
        score += pts["community"]
        reasons.append(f"{contributors} contributors" if contributors < 1000 else "1,000+ contributors")
    elif contributors >= 3:
        score += pts["community"] * 2 / 3
        reasons.append(f"{contributors} contributors")
    else:
        score += pts["community"] / 5
        reasons.append(f"{contributors} contributor{'s' if contributors != 1 else ''}")

    if repo.get("license") not in UNRECOGNISED_LICENSES:
        score += pts["license"]
        reasons.append(f"{repo['license']} license")
    else:
        reasons.append("no recognised license")

    frac, label = provenance(repo.get("owner", repo["full_name"].split("/")[0]), repo.get("owner_type"), orgs)
    score += pts["provenance"] * frac
    reasons.append(label)

    card = repo.get("scorecard")
    if card is not None:
        score += pts["scorecard"] * min(card, 10) / 10
        reasons.append(f"OpenSSF Scorecard {card:.1f}/10")
    else:
        score += pts["scorecard"] / 2
        reasons.append("no OpenSSF Scorecard published")

    if "agent" in repo.get("tags", []):
        if repo.get("readonly_mode") is True:
            score += cfg["readonly_bonus"]
            reasons.append("documented read-only mode")
        elif repo.get("readonly_mode") is False:
            score -= cfg["readonly_penalty"]
            reasons.append("requires write access")

    final = max(0, min(100, round(score)))
    if repo.get("archived"):
        return final, "experimental", reasons + ["archived"]
    badges = cfg["badges"]
    badge = "production" if final >= badges["production"] else "pilot" if final >= badges["pilot"] else "experimental"
    return final, badge, reasons


def lens_sort_key(repo: dict) -> tuple:
    return (-(repo.get("fit") or 0), -repo.get("trust_score", 0), -repo.get("trend_score", 0))
