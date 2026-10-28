---
name: add-baseline-entry
description: Add, move or remove an entry in the AI-Ready Baseline matrix (curation/baseline.yaml), whether a repo, a skill in this repo, or an idea worth building. Use when asked to update the baseline, matrix, readiness levels, foundations or checklist.
---

# Update the AI-Ready Baseline matrix

The matrix is meant to change slowly. Each entry is a recommendation someone could act on tomorrow.

1. Read `curation/baseline.yaml`, especially the level definitions:
   - L1 Scriptable: an official API, SDK or CLI.
   - L2 Agent-readable: a read-only MCP server.
   - L3 Agent-operable: write access with least-privilege scopes plus human approval.
   - L4 Codified know-how: skills and runbooks (`skill:` for ones in `skills/`, `idea:` for ones not built yet).
2. Pick the domain and level from what the tool actually does today, not from its roadmap.
3. For a `repo:` entry, confirm the repository exists and prefer the vendor's official project over community ones.
   If you can't confirm the location, add `verify: true`; the weekly build lists unverified entries in its PR.
4. Write one `note:` sentence telling an admin how to start safely (scopes, read-only mode, sandbox).
5. When an entry needs a fit/why on the lens too, also follow the `score-it-repo` skill.
6. Run `pytest -q`. The offline build must still succeed.
