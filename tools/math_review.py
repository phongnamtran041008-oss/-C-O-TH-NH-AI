#!/usr/bin/env python3
"""Write the review sheet of the math question bank: every hand-written question and
three sample draws of every generator, by floor and micro-skill, with answers and
solutions - one Markdown file per subject in tools/reports/.

    python tools/math_review.py                 # every written subject
    python tools/math_review.py --floor 2       # one floor only

Reading it is the "my review" step of the pipeline (draft -> automatic checks -> review).
A question that is right gets "reviewed": true in server/data/math/items/<subject>.json
(for a generator: in its "generators" entry). Unreviewed questions are served only where
ALLOW_UNREVIEWED=1 (the dev default). The sheet is the same on every run (fixed seeds).
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_items, math_path  # noqa: E402

SAMPLE_SEEDS = (1, 2, 3)


def _type_vi(qtype: str) -> str:
    """The type's name as balance/math.json gives it (Ghép cặp, Sắp xếp bước giải, ...)."""
    return math_path.question_types()[qtype]["name_vi"]


def _matrices(item: math_items.MathItem) -> list[str]:
    return [f"  - {name} = " + "; ".join("(" + ", ".join(row) + ")" for row in rows) + "  (từng hàng)"
            for name, rows in item.matrices]


def _question(item: math_items.MathItem) -> list[str]:
    lines = [f"  - **Câu hỏi:** {item.prompt_vi}", *_matrices(item)]
    if item.qtype == "find_mistake":
        # the lines as the player sees them, numbered, then which one is wrong, then why
        lines.append("  - **Lời giải đưa ra (có một bước sai):**")
        lines += [f"    {n}. {line}" + ("   **<- bước sai đầu tiên**" if n - 1 == item.answer else "")
                  for n, line in enumerate(item.lines_vi, 1)]
        lines.append(f"  - **Đáp án:** {item.answer_text}")
        lines.append("  - **Vì sao sai, và bước đúng:**")
        lines += [f"    {n}. {step}" for n, step in enumerate(item.solution_vi, 1)]
        return lines
    if item.qtype in ("matching", "ordering"):
        # the data order is the answer, so it is shown whole (the game shuffles what the player sees)
        if item.qtype == "matching":
            lines.append("  - **Đáp án (ghép đúng):**")
            lines += [f"    - {left}{math_items.MATCH_SEP_VI}{right}" for left, right in item.pairs_vi]
        else:
            lines.append("  - **Đáp án (thứ tự đúng):**")
            lines += [f"    {n}. {step}" for n, step in enumerate(item.steps_vi, 1)]
        lines.append("  - **Lời giải:**")
        lines += [f"    {n}. {step}" for n, step in enumerate(item.solution_vi, 1)]
        return lines
    if item.qtype == "multiple_choice":
        lines += [f"    - {'**(đúng)** ' if k == item.answer else ''}{text}" for k, text in enumerate(item.options_vi)]
    lines.append(f"  - **Đáp án:** {item.answer_text}" + ("  (thứ tự nào cũng được)" if item.unordered else ""))
    lines += [f"    {n}. {step}" for n, step in enumerate(item.solution_vi, 1)]
    return lines


def subject_sheet(subject: math_path.Subject, only_floor: int | None = None) -> str:
    cfg = math_path.cfg()
    out = [f"# Bảng duyệt câu hỏi: {subject.name_vi}", "",
           "Tạo bởi `python tools/math_review.py`. Đánh dấu đã duyệt bằng `\"reviewed\": true` trong "
           f"`server/data/math/items/{subject.id}.json`.", ""]
    for floor in subject.floors:
        templates = math_items.floor_templates(subject.id, floor.number, allow_unreviewed=True)
        if not templates or (only_floor is not None and floor.number != only_floor):
            continue
        gens = sum(1 for t in templates if t.generated)
        waiting = sum(1 for t in templates if not t.reviewed)
        out += [f"## Tầng {floor.number}: {floor.title_vi}", "",
                f"{len(templates)} dạng câu ({len(templates) - gens} câu viết tay, {gens} bộ sinh câu); "
                f"{waiting} chưa duyệt.", ""]
        for skill in floor.skills:
            out += [f"### {skill.name_vi} (`{skill.id}`)", ""]
            own = sorted((t for t in templates if t.skill == skill.id), key=lambda t: (t.tier, t.generated, t.id))
            for t in own:
                tier = cfg["tiers"][str(t.tier)]["name_vi"]
                mark = "đã duyệt" if t.reviewed else "CHƯA DUYỆT"
                kind = "bộ sinh câu, 3 mẫu" if t.generated else "viết tay"
                out.append(f"- `{t.id}` · bậc {t.tier} ({tier}) · {_type_vi(t.qtype)} · {kind} · {mark}")
                if t.generated:
                    for seed in SAMPLE_SEEDS:
                        out += _question(math_items.draw(t, random.Random(seed)))
                else:
                    out += _question(t)
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--floor", type=int, help="only this floor")
    ap.add_argument("--out", type=Path, default=ROOT / "tools" / "reports", help="folder for the sheets")
    args = ap.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)
    for subject in math_path.subjects():
        if not math_items.items_path(subject.id).is_file():
            continue
        path = args.out / f"math_review_{subject.id}.md"
        path.write_text(subject_sheet(subject, args.floor), "utf-8", newline="\n")
        print(f"{path.relative_to(ROOT)}: {sum(1 for _ in path.open(encoding='utf-8'))} lines")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
