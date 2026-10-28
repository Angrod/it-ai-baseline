# AI-Ready IT Baseline

GitHub repos worth a sysadmin's attention, scored for real usefulness and deploy-safety, plus the
APIs, MCP servers and skills that make an IT stack ready for agents.

It's the IT counterpart to Scribes' [Top GitHub repos for marketing & comms](https://wearescribes.xyz/top-github-repos-marketing-communications/),
with two IT-specific changes: a **trust badge**, because adopting an IT tool usually means handing it an
admin token, and an **AI-Ready Baseline** matrix, because the goal isn't only "what's hot" but "what
should my stack look like".

## The three views

| View | What it answers | How it ranks |
|---|---|---|
| **Trending** | What's gaining momentum in IT tooling? | 40% stars gained (30d) · 35% times trending (30d) · 25% total stars (log-normalized) |
| **IT Ops lens** | What would actually help a sysadmin, and is it safe to pilot? | Validation gate, then fit 0-3, then trust, then momentum |
| **AI-Ready Baseline** | What does an agent-ready IT stack look like? | Hand-curated matrix: 6 domains × 4 readiness levels |

### Why the marketing formula needed changes for IT
1. **IT tools rarely reach global trending.** AutoPkg, GAM, Okta and Jamf tooling trend on *language*
   pages (PowerShell, Shell, HCL, Swift…). So the snapshots cover those pages, and discovery also uses
   GitHub topic search (`config/topics.yaml`).
2. **Star counts are very skewed.** osquery has ~20k stars and Installomator ~2k, so total stars are
   log-normalized and one giant repo doesn't flatten the rest.
3. **Trust matters more than hype.** The badge (`pipeline/lens.py`) weighs maintenance, releases,
   contributors, license, provenance (vendor / community / personal), OpenSSF Scorecard and, for agent
   tools, whether a read-only mode exists.

All thresholds and weights live in `config/scoring.yaml`, and the site's "How repos are ranked" text is
generated from them.

## How it runs

```
daily    snapshot.yml  ->  data/snapshots/trending/YYYY-MM-DD.json        (committed to main)
weekly   refresh.yml   ->  GitHub search + GraphQL + Scorecard + Claude    -> PR "Weekly refresh"
on merge pages.yml     ->  site/ deployed to GitHub Pages
```

The weekly refresh never publishes directly. It opens a PR whose body (`data/review.md`) lists new lens
entries, every repo Claude scored, anything that needs a human decision, and baseline repos GitHub
couldn't find. Merging that PR is the approval.

**Human judgment always wins.** `curation/overrides.yaml` beats Claude's first pass, and
`curation/baseline.yaml` is entirely hand-curated.

## Setup (one time)

1. **Secrets and variables** (Settings → Secrets and variables → Actions):
   - Secret `ANTHROPIC_API_KEY`: used for the fit scoring. Without it, the refresh still runs and simply skips scoring.
   - Variable `CLAUDE_MODEL`: the Claude model ID to score with.
   - Optional variable `CLAUDE_FALLBACKS`: `default` (server-side refusal fallback, the default) or `off` for models that don't support it.
   - Optional secret `GH_PAT`: a fine-grained personal token, if the candidate pool outgrows the built-in token's 1,000 requests/hour.
2. **Actions permissions** (Settings → Actions → General → Workflow permissions): *Read and write*, and
   tick *Allow GitHub Actions to create and approve pull requests*.
3. **Pages** (Settings → Pages): Source = *GitHub Actions*.
4. Run **Trending snapshot** once by hand, then **Weekly refresh**. Merge the refresh PR and the site goes live.

"Times trending" builds from your own snapshots, so it starts at zero and fills in over the first 30 days.
The page shows how many days of history exist.

Pull requests opened with the built-in token don't trigger other workflows, so CI won't run on the
refresh PR. That's fine, because it only changes data files.

### Cost
Claude only scores repos that are new or have changed (results are cached in `data/cache/`), capped at
60 per run. The first run is the largest. After that, a typical week scores a handful of repos.

## Local development

```bash
pip install -r requirements.txt
pytest -q
python -m pipeline.build --offline tests/fixtures --now 2026-10-26T12:00:00Z \
  --out /tmp/data.json --review /tmp/review.md --cache-dir /tmp/cache
python -m pipeline.build --classify dry-run    # live data; lists what Claude would score
```

To preview the site, copy `site/` plus a generated `data.json` into one folder and serve it with
`python -m http.server`.

## Layout

| Path | What |
|---|---|
| `config/` | Rules: rubric tags and fit scale, discovery topics, scoring weights, trusted orgs |
| `curation/` | Human decisions: overrides, baseline matrix, nominations |
| `pipeline/` | `sources/` (fetch only), `score.py`, `lens.py`, `classify.py`, `build.py`, `snapshot.py` |
| `data/` | Machine output: snapshots, caches, the weekly review digest |
| `site/` | Static site (vanilla JS, no build step) |
| `skills/` | Example L4 skills for IT work: `okta-access-audit`, `offboard-user` |
| `.claude/skills/` | Skills for maintaining this repo: `score-it-repo`, `add-baseline-entry` |

## Using this to learn agents

This repo uses the same pattern you would bring to Okta or Jamf work:
- **An agent does the first pass** (`pipeline/classify.py`): structured output, a fixed rubric, README
  text treated as untrusted data, and results cached so nothing is re-scored for no reason.
- **A human approves**, through a PR: the change-management loop, unchanged.
- **Skills encode know-how**: `.claude/skills/` teaches Claude Code how to maintain this repo, and
  `skills/` holds IT runbooks you can copy into `~/.claude/skills/`.
- **The baseline checklist** (read-only first, sandbox tenants, scoped tokens, guardrail hooks, a kill
  switch) is the safety model for letting agents near production.
