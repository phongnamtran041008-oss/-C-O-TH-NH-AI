#!/usr/bin/env python3
"""Run every automated content check of the math game. A build must not go on when this
fails:

    python tools/check_all.py

Exit code 0 when every check passes, 1 otherwise. The list grows with each milestone
(plan section 6.4). Checks so far:

  * learning path: balance/math.json makes sense (tiers each floor may show, time limits
    per question type and tier, the rule numbers), every floor has 3-6 micro-skills with
    text the game can show, and prerequisites exist, never point to a later floor and
    have no cycle
  * question items (M2): every item of data/math/items/ belongs to a micro-skill, has a
    tier its floor allows and a type with a time limit at that tier; a multiple-choice
    item has exactly one right option and no two options with the same text; a numeric
    answer is a number, a fraction or a list of them; every text can be shown by the game
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_items, math_path  # noqa: E402


def check_learning_path() -> list[str]:
    return math_path.validate_all()


def check_items() -> list[str]:
    if math_path.validate_all():        # items are checked against the path: fix the path first
        return ["skipped: the learning path check above must pass first"]
    return math_items.validate_all()


# (name, function returning one line per problem; an empty list means the check passed)
CHECKS = [
    ("learning path: tiers per floor, time limits, micro-skill prerequisites", check_learning_path),
    ("question items: skill, tier, type, one right option, numeric answers, text", check_items),
]


def main(argv: list[str] | None = None) -> int:
    failed = 0
    for name, check in CHECKS:
        errors = check()
        print(f"[{'FAIL' if errors else ' OK '}] {name}")
        for e in errors:
            print(f"         - {e}")
        failed += bool(errors)
    print(f"{len(CHECKS) - failed}/{len(CHECKS)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):   # problem lines may quote Vietnamese text
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
