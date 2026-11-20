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

Scored exercises (Xa Truong) have no expected output to fill: their hidden sets and labels
come from server/app/learning/xa_truong_data.py and the seeds in the JSON. For them:

    python tools/build_problem_tests.py --measure            # every scored exercise
    python tools/build_problem_tests.py --measure --seeds 20 xt_knn_phan_loai

runs the reference solution and the naive one on the exercise's hidden seeds and on seeds
1..N, and prints mean, min and max score and the slowest run: the numbers the bars
(`grades`) and `time_limit_ms` (about five times the reference's time) are set from.
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


def measure(problem, seeds: list[int]) -> list[str]:
    """Scores of the reference and the naive program of one scored exercise, per seed."""
    lines = []
    for who, path in (("reference", math_problems.solution_path(problem.subject, problem.id)),
                      ("naive", math_problems.naive_path(problem.subject, problem.id))):
        scores, slowest = [], 0
        for seed in seeds:
            data, labels = problem.data.make(seed)
            result = coderun.run_one(path, data, 60000)
            slowest = max(slowest, result.ms)
            score, _ = math_problems.score_output(labels, result.output, problem.checker) if result.ok else (None, "")
            scores.append(score)
        got = [s for s in scores if s is not None]
        if not got:
            lines.append(f"{who:9s} no score on any seed")
            continue
        lines.append(f"{who:9s} mean {sum(got) / len(got):.4f}  min {min(got):.4f}  max {max(got):.4f}  "
                     f"slowest {slowest} ms  unscored {len(scores) - len(got)}")
    return lines


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="rebuild answers that are already there")
    ap.add_argument("--measure", action="store_true", help="score the scored exercises' reference and naive programs")
    ap.add_argument("--seeds", type=int, default=20, help="with --measure: also seeds 1..N")
    ap.add_argument("subject", nargs="?", default="", help="only this subject (with --measure: this exercise)")
    args = ap.parse_args(argv)
    if args.measure:
        for problem in math_problems.bank().values():
            if not problem.scored or (args.subject and args.subject != problem.id):
                continue
            hidden = list(problem.data.seeds)
            print(f"== {problem.id} ({problem.checker}, bars {list(problem.grades)}, limit {problem.time_limit_ms} ms)")
            for name, seeds in (("hidden seeds", hidden), (f"seeds 1..{args.seeds}", list(range(1, args.seeds + 1)))):
                print(f"  {name}:")
                for line in measure(problem, seeds):
                    print("   ", line)
        return 0
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
