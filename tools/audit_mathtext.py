#!/usr/bin/env python3
"""What client/ui/mathtext.pretty does to the question bank, for a person to review:

    python tools/audit_mathtext.py [--draws 5]

Runs `pretty` over every text the question card shows (prompt, options, matching / ordering /
find-the-mistake rows, Thiên kiếp parts and their options, the answer, every solution step, the
skill name) of every bank item and `--draws` draws of every generator, and writes
tools/reports/mathtext_audit.md: every distinct change, before -> after, grouped by pattern
(digits folded, so x^2 and x^3 are one pattern) with how often it happens and one example
(id and the text around it). A superscript is written ^{...} and a subscript _{...} there.
Prints how many strings changed. Exit code 1 when pretty emits a character neither shipped
font has (the unit test checks the same)."""
from __future__ import annotations

import argparse
import difflib
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_items, math_path  # noqa: E402
from client.ui.mathtext import END, SUB, SUP, pretty  # noqa: E402

REPORT = ROOT / "tools" / "reports" / "mathtext_audit.md"
FONTS = [ROOT / "client" / "assets" / "fonts" / "VT323-Regular.ttf",
         ROOT / "client" / "assets" / "fonts" / "NotoSansSC-Game.otf"]


def shown(s: str) -> str:
    return s.replace(SUP, "^{").replace(SUB, "_{").replace(END, "}")


def texts_of(item) -> list[str]:
    out = [item.prompt_vi, *item.options_vi, *(t for pair in item.pairs_vi for t in pair), *item.steps_vi,
           *item.lines_vi, *item.solution_vi]
    for part in item.parts:
        out += [part.prompt_vi, *part.options_vi]
    try:
        out.append(item.answer_text)
    except (IndexError, TypeError, ValueError):
        pass
    return [t for t in out if isinstance(t, str) and t]


def items(draws: int):
    for item in math_items.bank().values():
        yield item.id, item
    for spec in math_items.generators().values():
        for seed in range(draws):
            yield f"{spec.id}#{seed}", math_items.draw(spec, random.Random(seed))


def changes(before: str, after: str) -> list[tuple[str, str]]:
    """The changed fragments as whole words (pretty never adds or removes a space, so the words
    of the two texts pair up), with the punctuation around a word left out."""
    a, b = before.split(" "), shown(after).split(" ")
    out = []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if i2 - i1 == j2 - j1:
            pairs = [(x, y) for x, y in zip(a[i1:i2], b[j1:j2]) if x != y]
        else:
            pairs = [(" ".join(a[i1:i2]), " ".join(b[j1:j2]))]
        for x, y in pairs:
            while x and y and x[-1] == y[-1] and x[-1] in ",.;:!?":
                x, y = x[:-1], y[:-1]
            while x and y and x[0] == y[0] and x[0] in "([{":
                x, y = x[1:], y[1:]
            out.append((x, y))
    return out


def pattern(frag: str) -> str:
    return re.sub(r"\d+", "#", frag)


def font_chars() -> set[int] | None:
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    have: set[int] = set()
    for f in FONTS:
        have |= set(TTFont(str(f)).getBestCmap())
    return have


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=5)
    args = ap.parse_args()
    groups: dict[tuple[str, str], dict] = {}
    total = changed = 0
    seen: set[str] = set()
    missing: dict[str, str] = {}
    have = font_chars()
    for cid, item in items(args.draws):
        texts = texts_of(item)
        try:
            texts.append(math_path.subject(item.subject).skills[item.skill].name_vi)
        except (KeyError, AttributeError):
            pass
        for t in texts:
            if t in seen:
                continue
            seen.add(t)
            total += 1
            p = pretty(t)
            if p == t:
                continue
            changed += 1
            if have is not None:
                for ch in p:
                    if ch not in (SUP, SUB, END) and ord(ch) not in have and ch not in t:
                        missing.setdefault(ch, cid)
            for before, after in changes(t, p):
                key = (pattern(before), pattern(after))
                g = groups.setdefault(key, {"n": 0, "id": cid, "before": before, "after": after,
                                            "text": shown(p)})
                g["n"] += 1
    lines = ["# What `pretty` does to the question bank", "",
             f"Strings looked at: {total} (distinct texts of {len(math_items.bank())} bank items and "
             f"{args.draws} draws of each of {len(math_items.generators())} generators).",
             f"Strings changed: {changed}. Distinct patterns: {len(groups)}.", "",
             "A superscript run is written `^{...}`, a subscript run `_{...}` (the game draws them smaller, "
             "raised or lowered). Digits are folded into `#` to group the patterns.", ""]
    if missing:
        lines += ["## Characters no font has (must be empty)", ""]
        lines += [f"- U+{ord(c):04X} {c!r} (e.g. {i})" for c, i in sorted(missing.items())]
        lines.append("")
    lines += ["## Changes, most frequent first", "", "| count | before | after | example id | example (after) |",
              "|---:|---|---|---|---|"]

    def cell(s: str) -> str:
        return s.replace("|", "\\|").replace("\n", " ")
    for (bp, ap_), g in sorted(groups.items(), key=lambda kv: (-kv[1]["n"], kv[0])):
        ex = g["text"]
        k = ex.find(shown(g["after"])[:12]) if g["after"] else -1
        ex = ex[max(0, k - 40):k + 60] if k >= 0 else ex[:100]
        lines.append(f"| {g['n']} | `{cell(g['before'])}` | `{cell(g['after'])}` | {g['id']} | {cell(ex)} |")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{changed} of {total} strings changed, {len(groups)} patterns; report: {REPORT.relative_to(ROOT)}")
    if missing:
        print("characters no font has:", "".join(sorted(missing)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
