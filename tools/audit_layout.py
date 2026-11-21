#!/usr/bin/env python3
"""Show every question of the bank on the question card and check nothing is cut, covered or
outside the card:

    SDL_VIDEODRIVER=dummy python tools/audit_layout.py [--quick] [--scales 2,3] [--draws 5]

For every hand-written item and `--draws` draws of every generator, the public question
(math_items.to_question, exactly what the server sends) is shown in the practice card
(MathQuizScene, with a run line) and in the combat card (MathCombatQuizScene, with a monster's
mistake line and a chiêu badge), before answering and in the reveal after a wrong answer (the
reveal payload faked the way /quiz/answer sends it), at each window scale. The kit's audit
recorder (client/ui/kit.py, client/ui/audit.py) lists what each frame drew; every problem is
reported. No server and no window are needed.

Writes tools/reports/layout_audit.md: the totals, every problem by item id, and the items
whose prompt (or reveal) needs scrolling in each card - those are the ones to shorten.
Exit code 1 when there is any hard problem (cut, overlap, clipped, off the card)."""
from __future__ import annotations

import argparse
import os
import random
import sys
import time
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "server"))

import pygame  # noqa: E402

from app.learning import math_items, math_path  # noqa: E402
from client.engine.display import Display  # noqa: E402
from client.engine.text import Fonts  # noqa: E402
from client.ui import audit  # noqa: E402
from client.ui.kit import UI  # noqa: E402

REPORT = ROOT / "tools" / "reports" / "layout_audit.md"
MISTAKE = "Quái lỗi sai này hay quên đổi dấu khi chuyển vế và bỏ sót nghiệm âm của phương trình."
CAST = {"k": "audit", "name_vi": "Ngũ Hành Trận Pháp"}
RUN = {"mode": "practice", "combo": 12, "correct": 34, "asked": 40, "tier_name_vi": "Thành thạo"}


class _Api:
    def post(self, *a, **k): ...

    def get(self, *a, **k): ...


def fake_game(ui: UI):
    return SimpleNamespace(ui=ui, api=_Api(), audio=SimpleNamespace(play=lambda *a: None), toast=lambda *a, **k: None,
                           push=lambda *a: None, pop=lambda *a: None, on_xp=lambda *a: None, scenes=[], top=None,
                           now=0.0, state=SimpleNamespace())


def cases(draws: int, only: set[str] | None = None):
    """(id, MathQuestion) of every bank item and `draws` draws of every generator."""
    config = math_path.cfg()
    skipped = []
    for item in math_items.bank().values():
        if only and item.id not in only:
            continue
        try:
            yield item.id, math_items.to_question(item, random.Random(item.id), config)
        except ValueError:
            skipped.append(item.id)
    for spec in math_items.generators().values():
        if only and spec.id not in only:
            continue
        for seed in range(draws):
            item = math_items.draw(spec, random.Random(seed))
            try:
                yield f"{spec.id}#{seed}", math_items.to_question(item, random.Random(seed), config)
            except ValueError:
                skipped.append(spec.id)
    cases.skipped = skipped


def public(mq, n: int) -> dict:
    q = mq.public()
    q["session_id"] = "audit"
    m = dict(q["math"])
    if n % 3 == 1:                       # some cards carry the review badge, some the parallel one
        m["review"], m["review_node_vi"] = True, "Đạo hàm của hàm hợp và quy tắc chuỗi nhiều tầng"
    elif n % 3 == 2:
        m["parallel"] = True
    q["math"] = m
    return q


def wrong_answer(q: dict, key: dict) -> dict:
    """An answer the server would grade wrong, of the shape the card sends."""
    inp = q["input"]
    if inp == "truefalse":
        return {"value": not key.get("value")}
    if inp == "choice":
        return {"option": next(o["id"] for o in q["options"] if o["id"] != key.get("option"))}
    if inp == "number":
        return {"text": "12345/678"}
    if inp == "matching":
        n = len(q["prompt"]["left"])
        return {"pairs": [(k + 1) % n for k in range(n)]}
    if inp == "ordering":
        return {"order": list(range(len(q["prompt"]["steps"])))[::-1]}
    if inp == "find_mistake":
        return {"line": (key.get("line", 0) + 1) % len(q["prompt"]["lines"])}
    if inp == "tribulation":
        parts = []
        for p in q["prompt"]["parts"]:
            if p["input"] == "truefalse":
                parts.append({"value": True})
            elif p["input"] == "choice":
                parts.append({"option": p["options"][0]["id"]})
            else:
                parts.append({"text": "7"})
        return {"parts": parts}
    return {}


def result_payload(key: dict, combat: bool) -> dict:
    res = {"correct": False, "reveal": key.get("reveal"), "xp": {"gained": 3},
           "math": {"run": dict(RUN), "tier_change": -1, "parallel_waiting": True}}
    if combat:
        res["combat"] = {"mac_kich": 18}
    return res


def make_card(kind: str, game, q: dict):
    from client.scenes.math_practice import MathCombatQuizScene, MathQuizScene
    if kind == "combat":
        m = dict(q["math"], mistake_vi=MISTAKE, monster_vi="Mặc Quái Đổi Dấu")
        return MathCombatQuizScene(game, {**q, "math": m}, "audit-monster", cast=CAST)
    return MathQuizScene(game, q, run=dict(RUN))


def frame(ui: UI, card) -> list:
    ui.audit = []
    ui.begin([], 0.016)
    card.draw_ui(ui)
    rec, ui.audit = ui.audit, None
    return rec


def check(ui: UI, game, cid: str, q: dict, key: dict, kind: str, found, scrolls) -> None:
    card = make_card(kind, game, q)
    panel = card.panel_rect()
    rec = frame(ui, card)
    for p in audit.problems(rec, panel=panel):
        found.append((cid, kind, "question", ui.s, p))
    if getattr(card, "prompt_scrolls", False):
        scrolls[(kind, "question")].add(cid)
    card.given = wrong_answer(q, key)
    card.sent = True
    card.result = result_payload(key, kind == "combat")
    rec = frame(ui, card)
    for p in audit.problems(rec, panel=card.panel_rect()):
        found.append((cid, kind, "reveal", ui.s, p))
    if getattr(card, "reveal_scrolls", False):
        scrolls[(kind, "reveal")].add(cid)


def run(scales: list[int], draws: int, only: set[str] | None = None, write: bool = True,
        quiet: bool = False) -> tuple[list, dict, int]:
    pygame.init()
    fonts = Fonts()
    found: list = []
    scrolls: dict = defaultdict(set)
    qs = list(cases(draws, only))
    t0 = time.time()
    for scale in scales:
        ui = UI(Display(0, False, size=(480 * scale, 270 * scale)), fonts)
        game = fake_game(ui)
        for n, (cid, mq) in enumerate(qs):
            q = public(mq, n)
            for kind in ("practice", "combat"):
                check(ui, game, cid, q, mq.answer_key, kind, found, scrolls)
        if not quiet:
            print(f"scale {scale}: {len(qs)} questions, {time.time() - t0:.0f} s", flush=True)
    if write:
        write_report(qs, scales, found, scrolls)
    return found, scrolls, len(qs)


def write_report(qs, scales, found, scrolls) -> None:
    by_kind = audit.summary([p for *_, p in found])
    lines = ["# Layout audit of the question card", "",
             f"Questions: {len(qs)} (bank items and generator draws), cards: practice + combat, "
             f"states: question + reveal after a wrong answer, scales: {', '.join(map(str, scales))}.",
             f"Frames checked: {len(qs) * 4 * len(scales)}. Skipped (not askable at their tier): "
             f"{len(set(getattr(cases, 'skipped', [])))}.", "",
             "Written by `tools/audit_layout.py`; the checks are those of `client/ui/audit.py`.", "",
             "## Totals", ""]
    if not found:
        lines.append("No problem: no text off the card, cut, clipped or overlapping.")
    for k, v in sorted(by_kind.items()):
        lines.append(f"- {k}: {v}")
    lines += ["", "## Prompts that need scrolling (to shorten)", "",
              "The card shows them whole, but the player has to scroll. Shorter wording would read better.", ""]
    for (kind, state), ids in sorted(scrolls.items()):
        lines.append(f"### {kind} card, {state} ({len(ids)})")
        lines.append("")
        lines += [f"- {i}" for i in sorted(ids)]
        lines.append("")
    lines += ["## Problems by item", ""]
    per: dict = defaultdict(list)
    for cid, kind, state, scale, p in found:
        per[cid].append(f"{kind}/{state}/x{scale}: {p.describe()}")
    for cid in sorted(per):
        lines.append(f"### {cid}")
        lines += [f"- {x}" for x in per[cid][:30]]
        if len(per[cid]) > 30:
            lines.append(f"- ... {len(per[cid]) - 30} more")
        lines.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scales", default="2,3")
    ap.add_argument("--draws", type=int, default=5)
    ap.add_argument("--only", default="", help="comma-separated item / generator ids")
    args = ap.parse_args()
    only = set(filter(None, args.only.split(","))) or None
    found, scrolls, n = run([int(s) for s in args.scales.split(",")], args.draws, only)
    hard = [p for *_, p in found if p.kind in audit.HARD]
    print(f"{n} questions; problems: {audit.summary([p for *_, p in found]) or 'none'}")
    for (kind, state), ids in sorted(scrolls.items()):
        print(f"  scrolls in the {kind} card ({state}): {len(ids)}")
    print(f"report: {REPORT.relative_to(ROOT)}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
