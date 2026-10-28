# AI-Ready IT Baseline

A static site plus a Python pipeline that ranks GitHub repos for sysadmins. See README.md for the methodology.

## Commands
- Tests: `pytest -q`
- Offline build (no network): `python -m pipeline.build --offline tests/fixtures --now 2026-10-26T12:00:00Z --out /tmp/data.json --review /tmp/review.md --cache-dir /tmp/cache`
- Regenerate fixtures after changing their generator: `python tests/fixtures/make_fixtures.py`

## Conventions
- `config/` holds rules, `curation/` holds human decisions, `data/` holds machine output. Never hand-edit `data/` or `site/data.json`.
- Human overrides in `curation/overrides.yaml` always beat Claude's first pass. Keep it that way in `build.apply_judgment`.
- `pipeline/sources/` only fetches; scoring logic belongs in `score.py` / `lens.py`.
- The site renders untrusted GitHub text, so only ever use `textContent` / text nodes in `site/app.js`, never `innerHTML`.
- The scoring model comes from the `CLAUDE_MODEL` environment variable. Don't hardcode a model ID.
- Changing the rubric's tags or fit scale: bump `version` in `config/rubric.yaml` so cached scores are redone.
- Use the `score-it-repo` and `add-baseline-entry` skills for curation changes.
