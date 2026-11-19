"""Check the essay bank of Luận Đạo Đài (server/data/math/essays/<subject>.json).

    python tools/check_essays.py                 # the data on its own
    python tools/check_essays.py --tree PATH     # + every essay belongs to a node of the tree

The rules live in server/app/learning/math_essays.py; this only runs them. The curriculum
tree (tree.json) belongs to another piece of work and is only read here, when given.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_essays  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--tree", type=Path, help="tree.json to check the nodes against")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    nodes = None
    if args.tree:
        nodes = {n["id"] for n in json.loads(args.tree.read_text(encoding="utf-8"))["nodes"]}
    errors = math_essays.validate_all(nodes=nodes)
    bank = math_essays.bank()
    by_subject: dict[str, int] = {}
    for essay in bank.values():
        by_subject[essay.subject] = by_subject.get(essay.subject, 0) + 1
    print(f"{len(bank)} essays: " + ", ".join(f"{s} {n}" for s, n in by_subject.items()))
    for line in errors:
        print("ERROR", line)
    print("OK" if not errors else f"{len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
