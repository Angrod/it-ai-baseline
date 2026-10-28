"""Weekly build: candidates -> enrichment -> scoring -> site/data.json + data/review.md.

    python -m pipeline.build                          # live run (GitHub + Scorecard + Claude)
    python -m pipeline.build --classify off           # skip Claude
    python -m pipeline.build --classify dry-run       # list what Claude would score
    python -m pipeline.build --offline tests/fixtures --out /tmp/data.json   # no network
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

from pipeline import classify, lens, score
from pipeline.config import CACHE, DATA, SITE, SNAPSHOTS, Settings, days_since, iso, load_json, write_json
from pipeline.sources import github_trending, scorecard
from pipeline.sources.github_api import GitHub, stars_gained

CLASSIFY_LIMIT = 60       # new Claude scores per run; caps spend on a big first run
CLASSIFY_TRENDING = 40    # also score the top-N trending repos so keyword noise can be dropped
CONTRIBUTORS_CACHE_DAYS = 7

CARD_FIELDS = (
    "full_name", "url", "description", "language", "stars", "stars_gained_7d", "stars_gained_30d",
    "stars_gained_estimated", "times_trending_7d", "times_trending_30d", "trend_score", "trend_rank",
    "lens_rank", "fit", "scored_by", "tags", "why", "first_step", "readonly_mode", "trust_score",
    "trust_badge", "trust_reasons", "gated", "pushed_at", "license", "needs_review",
)


def collect(settings: Settings, gh, now: datetime, snapshots: list[dict]) -> tuple[dict, dict, list[str]]:
    """Union of every source. Returns ({key: record}, {key: {source, ...}}, names GitHub couldn't find)."""
    records: dict[str, dict] = {}
    sources: dict[str, set[str]] = {}

    search = settings.topics["search"]
    suffix = f" stars:>={search['min_stars']} archived:false"
    queries = [f"topic:{t}{suffix}" for t in search.get("topics", [])]
    queries += [f"{q}{suffix}" for q in search.get("queries", [])]
    for query in queries:
        for rec in gh.search(query, search["per_query"]):
            key = rec["full_name"].lower()
            records.setdefault(key, rec)
            sources.setdefault(key, set()).add("search")

    named: dict[str, str] = {}
    for key, name in github_trending.pool_from_snapshots(snapshots).items():
        named[key] = name
        sources.setdefault(key, set()).add("trending")
    for source, names in (("nominated", settings.nominations), ("baseline", settings.baseline_repos()),
                          ("foundation", settings.foundation_repos())):
        for name in names:
            named.setdefault(name.lower(), name)
            sources.setdefault(name.lower(), set()).add(source)

    found, missing = gh.repos([name for key, name in named.items() if key not in records], now)
    records.update(found)
    return records, sources, missing


def apply_judgment(rec: dict, cached: dict | None, override: dict | None, tag_order: list[str]) -> None:
    """Merge keyword tags, Claude's first pass, and the human override (which always wins)."""
    rec.update(fit=None, why="", first_step="", readonly_mode=None, scored_by=None, needs_review=None)
    tags = rec["keyword_tags"]
    if cached and cached.get("status") == "scored":
        rec.update(fit=cached["fit"], why=cached["why"], first_step=cached["first_step"],
                   readonly_mode=cached["readonly_mode"], scored_by="claude")
        tags = cached["tags"] or tags
    elif cached and cached.get("status") == "needs_review":
        rec["needs_review"] = cached["reason"]
    if override:
        for field in ("fit", "why", "first_step", "readonly_mode"):
            if field in override:
                rec[field] = override[field]
        if "fit" in override:
            rec["scored_by"] = "human"
            rec["needs_review"] = None
        tags = override.get("tags", tags)
    rec["tags"] = [t for t in tag_order if t in tags]


def contributor_counts(gh, keys: list[str], records: dict, cache: dict, now: datetime) -> None:
    for key in keys:
        entry = cache.get(key)
        if entry is None or days_since(entry["fetched_at"], now) > CONTRIBUTORS_CACHE_DAYS:
            entry = {"count": gh.contributors(records[key]["full_name"]), "fetched_at": iso(now)}
            cache[key] = entry
        records[key]["contributors"] = entry["count"]


def resolve_baseline(baseline: dict, records: dict, missing: set[str]) -> dict:
    def entry(e: dict) -> dict:
        out = {k: e[k] for k in ("repo", "skill", "idea", "note") if k in e}
        if "repo" in e:
            key = e["repo"].lower()
            out["key"] = key
            out["unverified"] = key in missing or key not in records
        return out

    return {
        "levels": baseline.get("levels", []),
        "domains": [{"id": d["id"], "label": d["label"],
                     "cells": {lvl: [entry(e) for e in (entries or [])] for lvl, entries in d.get("cells", {}).items()}}
                    for d in baseline.get("domains", [])],
        "foundations": [entry(f) for f in baseline.get("foundations", [])],
        "checklist": baseline.get("checklist", []),
    }


def methodology(settings: Settings, history_days: int) -> dict:
    trending = settings.scoring["trending"]
    lens_cfg = settings.scoring["lens"]
    return {
        "weights": trending["weights"],
        "window_days": trending["window_days"],
        "log_total_stars": trending.get("log_total_stars", True),
        "gate": lens_cfg["gate"],
        "show": {"trending": trending["show"], "lens": lens_cfg["show"]},
        "trust": settings.scoring["trust"],
        "history_days": history_days,
        "fit_scale": settings.rubric["fit_scale"],
        "trending_languages": [lang or "all" for lang in settings.topics["trending"]["languages"]],
    }


def review_digest(now: datetime, stats: dict, records: dict, classified: list[str], lens_keys: list[str],
                  previous_lens: list[str], missing: list[str], baseline_out: dict) -> str:
    lines = [f"# Weekly refresh: {now.date().isoformat()}", "",
             "Review the changes below. To change a score, tag or note, edit `curation/overrides.yaml` "
             "in this PR; overrides beat Claude's first pass.", "",
             "| Candidates | IT-relevant | Passed gate | Scored by Claude this run | Needs review |",
             "|---|---|---|---|---|",
             f"| {stats['candidates']} | {stats['relevant']} | {stats['gated']} | {len(classified)} | "
             f"{stats['needs_review']} |", ""]

    entered = [k for k in lens_keys if k not in previous_lens]
    left = [k for k in previous_lens if k not in lens_keys]
    if entered or left:
        lines += ["## IT Ops lens changes", ""]
        lines += [f"- ⬆️ **{records[k]['full_name']}** entered at #{records[k]['lens_rank']}" for k in entered]
        lines += [f"- ⬇️ {k} left the top {len(lens_keys)}" for k in left]
        lines.append("")

    if classified:
        lines += ["## Scored by Claude this run", "",
                  "| Repo | Fit | Tags | Trust | Why for sysadmins |", "|---|---|---|---|---|"]
        for name in classified:
            rec = records[name.lower()]
            fit = "needs review" if rec.get("needs_review") else rec.get("fit")
            why = (rec.get("why") or rec.get("needs_review") or "").replace("|", "/")
            lines.append(f"| [{rec['full_name']}]({rec['url']}) | {fit} | {', '.join(rec['tags'])} | "
                         f"{rec.get('trust_badge', '')} | {why} |")
        lines.append("")

    flagged = [rec for rec in records.values() if rec.get("needs_review")]
    if flagged:
        lines += ["## Needs a human decision", ""]
        lines += [f"- {rec['full_name']}: {rec['needs_review']}" for rec in flagged]
        lines.append("")

    unverified = sorted({e["repo"] for d in baseline_out["domains"] for cell in d["cells"].values()
                         for e in cell if e.get("unverified")} |
                        {e["repo"] for e in baseline_out["foundations"] if e.get("unverified")})
    if missing or unverified:
        lines += ["## Not found on GitHub", "", "Fix or remove these in `curation/`:", ""]
        lines += [f"- {name}" for name in sorted(set(missing) | set(unverified))]
        lines.append("")
    return "\n".join(lines)


def build(settings: Settings, gh, now: datetime, *, snapshot_dir: Path = SNAPSHOTS,
          scorecard_lookup: Callable[[list[str], dict, datetime], dict] = scorecard.scores,
          classify_mode: str = "live", classifier: classify.Classifier | None = None,
          classify_limit: int = CLASSIFY_LIMIT, out: Path = SITE / "data.json",
          review: Path = DATA / "review.md", cache_dir: Path = CACHE) -> dict:
    trending_cfg = settings.scoring["trending"]
    lens_cfg = settings.scoring["lens"]
    window = trending_cfg["window_days"]
    tag_order = [t["id"] for t in settings.tags]

    snaps = github_trending.load_snapshots(snapshot_dir, now, window)
    week_start = (now - timedelta(days=7)).date()
    tt30 = github_trending.times_trending(snaps)
    tt7 = github_trending.times_trending([s for s in snaps if datetime.strptime(s["date"], "%Y-%m-%d").date() > week_start])

    records, sources, missing = collect(settings, gh, now, snaps)
    overrides = {k.lower(): v or {} for k, v in (settings.overrides or {}).items()}
    compiled = lens.compile_tags(settings.tags)
    curated = ({k for k, s in sources.items() if s & {"baseline", "nominated"}}
               | {k for k, v in overrides.items() if "fit" in v})

    # -- relevance ------------------------------------------------------------
    pool_keys, display_keys = [], []
    for key, rec in records.items():
        rec["keyword_tags"] = lens.match_tags(rec, compiled)
        if overrides.get(key, {}).get("exclude"):
            continue
        eligible = key in curated or (not rec.get("fork") and lens.is_relevant(rec["keyword_tags"], settings.tags))
        if eligible and not rec.get("archived"):
            pool_keys.append(key)
        elif key in curated or "foundation" in sources.get(key, ()):
            display_keys.append(key)  # shown with live data (e.g. in the baseline), never ranked
    tracked = pool_keys + display_keys

    # -- enrichment (stars over time, releases) -------------------------------
    enriched, gone = gh.repos([records[k]["full_name"] for k in tracked], now, with_stars=True,
                              window_days=window, max_star_pages=settings.scoring["stargazers"]["max_pages"])
    missing = sorted(set(missing) | set(gone))
    for key in tracked:
        if key not in enriched:
            continue
        rec = records[key]
        rec.update(enriched[key])
        starred, exhausted = rec.pop("starred_at", []), rec.pop("starred_exhausted", True)
        g30, est30 = stars_gained(starred, exhausted, now, window)
        g7, est7 = stars_gained(starred, exhausted, now, 7)
        rec.update(stars_gained_30d=g30, stars_gained_7d=g7, stars_gained_estimated=est30 or est7,
                   times_trending_30d=tt30.get(key, 0), times_trending_7d=tt7.get(key, 0))
        rec["gated"], rec["gate_failures"] = lens.gate(rec, lens_cfg["gate"], now)
    pool_keys = [k for k in pool_keys if k in enriched]
    tracked = [k for k in tracked if k in enriched]

    deep = [k for k in tracked if records[k]["gated"] or k in curated or k in display_keys]
    contributor_cache = load_json(cache_dir / "contributors.json", {})
    contributor_counts(gh, deep, records, contributor_cache, now)
    scorecard_cache = load_json(cache_dir / "scorecard.json", {})
    cards = scorecard_lookup([records[k]["full_name"] for k in deep], scorecard_cache, now)
    for key in deep:
        records[key]["scorecard"] = cards.get(key)

    # -- Claude first pass ----------------------------------------------------
    score.trending_scores([records[k] for k in pool_keys], trending_cfg["weights"],
                          trending_cfg.get("log_total_stars", True))
    by_trend = sorted(pool_keys, key=lambda k: -records[k]["trend_score"])
    wanted = [k for k in pool_keys if records[k]["gated"] or k in curated] + by_trend[:CLASSIFY_TRENDING]
    human_done = {k for k, v in overrides.items() if "fit" in v and "why" in v}
    candidates = [records[k] for k in dict.fromkeys(wanted) if k not in human_done]

    cache = load_json(cache_dir / "classifications.json", {})
    classified: list[str] = []
    if classify_mode == "dry-run":
        todo = classify.pending(candidates, cache, settings.rubric["version"])
        print(f"{len(todo)} repos would be scored (limit {classify_limit}):")
        for rec in todo[:classify_limit]:
            print(f"  {rec['full_name']}")
    elif classify_mode == "live":
        classified = classify.run(candidates, cache, settings.rubric, gh.readme, now, classify_limit, classifier)

    for key in tracked:
        rec = records[key]
        apply_judgment(rec, cache.get(key), overrides.get(key), tag_order)
        rec["trust_score"], rec["trust_badge"], rec["trust_reasons"] = lens.trust(
            rec, settings.scoring["trust"], settings.orgs, now)

    # -- views ----------------------------------------------------------------
    pool = [records[k] for k in pool_keys if records[k].get("fit") != 0]
    score.trending_scores(pool, trending_cfg["weights"], trending_cfg.get("log_total_stars", True))
    trending = sorted(pool, key=lambda r: (-r["trend_score"], -r["stars"]))
    score.assign_rank(trending, "trend_rank")
    lens_list = sorted([r for r in pool if r["gated"] and (r.get("fit") or 0) >= 1], key=lens.lens_sort_key)
    score.assign_rank(lens_list, "lens_rank")

    views = {
        "trending": [r["full_name"].lower() for r in trending[:trending_cfg["show"]]],
        "lens": [r["full_name"].lower() for r in lens_list[:lens_cfg["show"]]],
    }
    # Views reference records by their full_name key; renamed repos keep their original key.
    keyed = {r["full_name"].lower(): r for r in records.values()}
    baseline_out = resolve_baseline(settings.baseline, keyed, set(m.lower() for m in missing))
    referenced = set(views["trending"]) | set(views["lens"]) | {
        e["key"] for d in baseline_out["domains"] for cell in d["cells"].values() for e in cell if "key" in e
    } | {e["key"] for e in baseline_out["foundations"] if "key" in e}

    previous = load_json(out, {}) or {}
    history_days = len(snaps)
    data = {
        "generated_at": iso(now),
        "source_repo": os.environ.get("GITHUB_REPOSITORY"),  # set in Actions; links skills to their source
        "methodology": methodology(settings, history_days),
        "tags": [{"id": t["id"], "label": t["label"]} for t in settings.tags],
        "views": views,
        "baseline": baseline_out,
        "repos": {k: {f: keyed[k].get(f) for f in CARD_FIELDS} for k in sorted(referenced) if k in keyed},
    }
    write_json(out, data)

    stats = {"candidates": len(records), "relevant": len(pool_keys),
             "gated": sum(1 for k in pool_keys if records[k]["gated"]),
             "needs_review": sum(1 for k in tracked if records[k].get("needs_review"))}
    digest = review_digest(now, stats, keyed, classified, views["lens"],
                           previous.get("views", {}).get("lens", []), missing, baseline_out)
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_text(digest, encoding="utf-8")

    write_json(cache_dir / "classifications.json", cache)
    write_json(cache_dir / "contributors.json", contributor_cache)
    write_json(cache_dir / "scorecard.json", scorecard_cache)
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--classify", choices=["live", "dry-run", "off"], default="live")
    parser.add_argument("--limit", type=int, default=CLASSIFY_LIMIT, help="max new Claude scores this run")
    parser.add_argument("--offline", type=Path, help="fixture directory (repos.json + snapshots/); no network")
    parser.add_argument("--now", help="ISO timestamp to treat as the current time")
    parser.add_argument("--out", type=Path, default=SITE / "data.json")
    parser.add_argument("--review", type=Path, default=DATA / "review.md")
    parser.add_argument("--cache-dir", type=Path, default=CACHE)
    args = parser.parse_args(argv)

    now = datetime.fromisoformat(args.now.replace("Z", "+00:00")) if args.now else datetime.now(timezone.utc)
    settings = Settings()
    kwargs = dict(classify_mode=args.classify, classify_limit=args.limit, out=args.out, review=args.review,
                  cache_dir=args.cache_dir)
    if args.offline:
        from pipeline.offline import FixtureGitHub, fixture_scorecards
        gh = FixtureGitHub(args.offline)
        kwargs.update(snapshot_dir=args.offline / "snapshots", scorecard_lookup=fixture_scorecards(gh))
        if args.classify == "live":
            kwargs["classify_mode"] = "off"
    else:
        gh = GitHub()
    data = build(settings, gh, now, **kwargs)
    print(f"wrote {args.out}: {len(data['views']['trending'])} trending, {len(data['views']['lens'])} lens, "
          f"{len(data['repos'])} repos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
