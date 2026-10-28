"""Daily job: save today's GitHub trending pages and prune old snapshots.

    python -m pipeline.snapshot
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone

from pipeline.config import SNAPSHOTS, Settings, iso, write_json
from pipeline.sources import github_trending


def main() -> int:
    now = datetime.now(timezone.utc)
    cfg = Settings().topics["trending"]
    pages = github_trending.fetch_snapshot(cfg["languages"], cfg["periods"])
    empty = [key for key, rows in pages.items() if not rows]
    if len(empty) == len(pages):
        print("every trending page parsed empty; GitHub's markup probably changed", file=sys.stderr)
        return 1
    path = SNAPSHOTS / f"{now.date().isoformat()}.json"
    write_json(path, {"date": now.date().isoformat(), "fetched_at": iso(now), "pages": pages})
    removed = github_trending.prune(SNAPSHOTS, now, cfg["keep_days"])
    print(f"wrote {path.name}: {sum(len(r) for r in pages.values())} rows across {len(pages)} pages"
          f"{f', {len(empty)} empty' if empty else ''}; pruned {len(removed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
