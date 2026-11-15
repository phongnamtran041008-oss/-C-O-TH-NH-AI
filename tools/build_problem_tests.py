#!/usr/bin/env python3
"""Fill in the expected output of the hidden tests of the programming exercises (M6).

    python tools/build_problem_tests.py            # fill the empty ones
    python tools/build_problem_tests.py --all      # rebuild every hidden answer

The expected output of a hidden test is whatever the exercise's reference solution prints
for it - the way a problem setter does it. The **samples** are never touched: their answers
are written by hand in the JSON, so that tools/check_all.py comparing the reference
solution against them is a real check and not the same number twice.

Run this after adding a test or changing a reference solution; check_all.py then proves the
two still agree.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
sys.path.insert(0, str(ROOT))

from app.learning import math_path, math_problems  # noqa: E402
from client.engine import coderun  # noqa: E402


def build(subject_id: str, rebuild_all: bool, math_dir: Path = math_problems.MATH_DIR) -> list[str]:
    """Returns one line per test that was filled in, or per problem that could not be."""
    path = math_problems.problems_path(subject_id, math_dir)
    raw = json.loads(path.read_text("utf-8"))
    notes: list[str] = []
    changed = False
    for problem in raw.get("problems", []):
        pid = problem.get("id")
        solution = math_problems.solution_path(subject_id, pid, math_dir)
        if not solution.is_file():
            notes.append(f"{pid}: no reference solution at {solution}")
            continue
        limit = int(problem.get("time_limit_ms", math_path.cfg()["programming"]["time_limit_ms"]))
        for n, test in enumerate(problem.get("tests", []), 1):
            if test.get("out") and not rebuild_all:
                continue
            result = coderun.run_one(solution, test["in"], limit)
            if not result.ok:
                notes.append(f"{pid} test {n}: the reference solution gave {result.status} {result.error}")
                continue
            text = result.output
            if not text.endswith("\n"):
                text += "\n"
            if test.get("out") != text:
                test["out"] = text
                changed = True
                notes.append(f"{pid} test {n}: {text.strip()[:60]!r}")
    if changed:
        path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", "utf-8", newline="\n")
    return notes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="rebuild answers that are already there")
    ap.add_argument("subject", nargs="?", default="", help="only this subject")
    args = ap.parse_args(argv)
    subjects = [args.subject] if args.subject else [s.id for s in math_path.subjects()]
    for subject_id in subjects:
        if not math_problems.problems_path(subject_id).is_file():
            continue
        print(f"== {subject_id}")
        for line in build(subject_id, args.all) or ["(nothing to fill in)"]:
            print("  ", line)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
