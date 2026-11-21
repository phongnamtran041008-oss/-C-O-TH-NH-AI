"""Math question loop (milestone M2): pick a floor of a math bí cảnh, then answer one
question after another. Each question has a countdown; when it runs out the server counts
a wrong answer. After a wrong answer the card shows the solution step by step.

M5: the hub says which parts are open, which are passed and how far the mastery gate of the
part being played has come; a part whose gate is open offers its Thiên kiếp nhỏ, a sitting of
one question per micro-skill that ends in a verdict. Questions that come from a node below
say so ("Ôn xoắn ốc"). Since Đạo Thụ the hub lists the nodes of the curriculum tree, not floors.

The client never knows the answer: it sends what the player chose or typed and shows what
the server reveals afterwards (the same rule as QuizScene)."""
from __future__ import annotations

import math

import importlib
import re

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..ui import mathinputs as MI
from ..ui.mathdraw import draw_matrices, fit, matrices_size
from ..ui.mathtext import pretty
from .base import Scene
from .math_code import ProblemListScene
from .math_library import DocScene, LibraryListScene, scroll_rows, subject_tabs
from .math_tree import (NEXT_TAB, NodeCardScene, Row, draw_chips, exercises_subject, first_tab, fit_lines,
                        header_text, later_ids, locked_reason, main_head, main_label, main_progress, main_step,
                        names_of, node_by_id, node_rows, part_playable, progress_text, row_state, stage_text,
                        tab_list)
from .quiz import KEYS, CombatCard, QuizScene

GREY = "#5A5A5A"
INK = "#2B2B2B"
PALE = "#9A9387"
OPTION_KEYS = KEYS + [pygame.K_5, pygame.K_6]


def review_badge(m: dict) -> str:
    """What the card says over a review question: the node of Đạo Thụ it comes from (it may be
    in another subject), else - a sitting with no node, from before Đạo Thụ - the floor."""
    if m.get("review_node_vi"):
        return T.MATH_REVIEW_NODE.format(name=m["review_node_vi"])
    return T.MATH_REVIEW.format(n=m.get("floor", "?"))


def tiers_text(lo: int, hi: int) -> str:
    return T.MATH_TIER_ONE.format(lo=lo) if lo == hi else T.MATH_TIERS.format(lo=lo, hi=hi)


# ------------------------------------------------------------------ the question card: layout
# The card is a vertical flow of zones, measured before anything is drawn:
#   header      subject · floor · skill on the left (wrapped, never under the tier), the tier on
#               the right; under it the countdown (question) or the verdict bar (reveal)
#   status      short badges (review / parallel, a chiêu, Hộ Thể...), side by side when they fit
#   instruction what to do, one line where it fits
#   prompt      the question (font 10 -> 9 -> 8) and its matrices; when it still does not fit
#               it scrolls (wheel, Up / Down, a scrollbar and "còn nữa") - never drawn over the
#               input, never cut
#   input       true/false, the options (wrapped, sized to their text, one or two columns, font
#               8 -> 7), the number box, a matching / ordering / find-the-mistake board or a
#               Thiên kiếp - always whole and clickable
#   footer      the run line, a combat card's mistake line, the buttons of the reveal
# After the answer everything between the verdict and the footer is ONE scrolling region: the
# question, "Bạn trả lời", the right answer (every line of a matching / ordering answer) and
# every solution step. A low card (a fight's) grows upwards, as far as CARD_TOP, before its
# prompt has to scroll.
HEAD = 7                    # the header line, badges and instruction
PROMPT_SIZES = (10, 9, 8)
OPTION_SIZES = (8, 7)
ZONE_GAP = 4                # between two zones
OPT_GAP = 4                 # between two options


def _lh(ui, size: float) -> float:
    return ui.text_size("Ag", size)[1]


def _pitch(ui, size: float) -> float:
    return _lh(ui, size) * 1.15


def _block(ui, n: int, size: float) -> float:
    """The height of n lines of text drawn one under the other at this size."""
    return 0.0 if n <= 0 else (n - 1) * _pitch(ui, size) + _lh(ui, size)


def draw_lines(ui, lines: list[str], x: float, y: float, size: float, colour, align: str = "left",
               width: float = 0.0) -> float:
    """Lines already wrapped, one under the other from y; returns the y under the last."""
    p = _pitch(ui, size)
    for i, line in enumerate(lines):
        if align == "center":
            ui.text(line, x + width / 2, y + i * p, size, colour, anchor="midtop")
        elif align == "right":
            ui.text(line, x + width, y + i * p, size, colour, anchor="topright")
        else:
            ui.text(line, x, y + i * p, size, colour)
    return y + _block(ui, len(lines), size)


def flow_rows(ui, items, width: float, size: float = HEAD) -> list[tuple[float, list]]:
    """Short labels (text, colour, align "left" / "center" / "right") laid out in rows across
    `width`: labels of different alignments share a row when they fit side by side without
    touching; a label wider than the row gets rows of its own, wrapped. Returns
    [(row height, [(lines, colour, align)])]."""
    rows: list[list] = []
    cur: list = []

    def fits(row, text, align) -> bool:
        spans = []
        for lines, _, a in row + [([text], None, align)]:
            tw = ui.text_size(lines[0], size)[0]
            x0 = 0.0 if a == "left" else width - tw if a == "right" else (width - tw) / 2
            spans.append((x0 - 6, x0 + tw + 6))
        spans.sort()
        return all(a[1] <= b[0] + 6 for a, b in zip(spans, spans[1:])) and not any(a == align for _, _, a in row)

    for text, colour, align in items:
        if not text:
            continue
        if ui.text_size(text, size)[0] > width:
            if cur:
                rows.append(cur)
                cur = []
            rows.append([(MI._wrap(ui, text, size, width), colour, align)])
            continue
        if cur and not fits(cur, text, align):
            rows.append(cur)
            cur = []
        cur.append(([text], colour, align))
    if cur:
        rows.append(cur)
    return [(_block(ui, max(len(lines) for lines, _, _ in row), size), row) for row in rows]


def draw_flow(ui, rows, x: float, y: float, width: float, size: float = HEAD) -> float:
    for h, row in rows:
        for lines, colour, align in row:
            draw_lines(ui, lines, x, y, size, colour, align, width)
        y += h + 2
    return y


def option_plan(ui, options: list[dict], w: float, cols: int, size: float) -> tuple[float, dict]:
    """(height, plan) of the options in `cols` columns at this font size: every option wrapped to
    its column and as tall as its text."""
    cw = (w - 32 - (cols - 1) * 6) / cols
    rows = []
    for r in range(0, len(options), cols):
        group = options[r:r + cols]
        lines = [MI._wrap(ui, pretty(o["text"]), size, cw - 24) for o in group]
        rows.append((max(17.0, max(len(ls) for ls in lines) * _pitch(ui, size) + 5), lines))
    need = sum(h for h, _ in rows) + OPT_GAP * max(0, len(rows) - 1)
    return need, {"cols": cols, "size": size, "rows": rows, "cw": cw}


class MathQuizScene(QuizScene):
    """One math question: true/false, multiple choice, a typed number, a matching / ordering /
    find-the-mistake board or a Thiên kiếp - laid out as the zones described above."""

    in_combat = False        # M7: the card a quái lỗi sai opens closes itself
    can_stop = True          # "Nghỉ" ends a buổi luyện; a card with no sitting to end has no such button
    solution_margin = 40     # the reveal stops this far above the bottom edge of the card (+12)

    def input_margin(self) -> int:
        """How far above the bottom edge of the card the input zone ends (the run line is under it)."""
        return 20

    CARD_TOP = 18            # the highest a card may reach: a toast fits in the strip above it

    def card_rect(self):
        """Where this kind of card would like to sit (a combat card sits low, under the HUD)."""
        return (24, self.CARD_TOP, 432, 246)

    def panel_rect(self):
        """The card's rectangle: `card_rect`, grown upwards (never above CARD_TOP) when its
        question - prompt at font 8, the input at its smallest - needs more room than it has.
        After the answer a low card grows again, as far as the reveal (the solution steps)
        needs: the fight is waiting for the player to read it."""
        x, y, w, h = self.card_rect()
        short = self.board_shortfall(x, y, w, h)
        if self.result:
            short = max(short, self.reveal_shortfall(x, y, w, h))
        grow = min(max(0.0, short), y - self.CARD_TOP)
        if grow > 0:
            grow = float(int(grow + 0.999))
            y, h = y - grow, h + grow
        return (x, y, w, h)

    def reveal_shortfall(self, x, y, w, h) -> float:
        """How many base pixels the whole reveal lacks inside the card x, y, w, h."""
        ui = getattr(self.game, "ui", None)
        if ui is None or not self.result:
            return 0.0
        key = (ui.s, x, y, w, h, id(self.result))
        if self._reveal_short is None or self._reveal_short[0] != key:
            res = self.result
            rows = self.reveal_rows(res, bool(res.get("correct")), bool(res.get("timed_out") or self.timed_out))
            content = sum(MI._line_h(ui, ln) for ln in MI.view_lines(ui, rows, w - 32 - 6, 8))
            top = 6 + self.header_h(ui, w) + 3 + self.verdict_h(ui, w, res) + 4
            self._reveal_short = (key, top + content + 1 + (self.solution_margin - 12) - h)
        return self._reveal_short[1]

    def board_shortfall(self, x, y, w, h) -> float:
        """How many base pixels this question lacks inside the card x, y, w, h (<= 0: it
        fits). Measured once per window scale."""
        ui = getattr(self.game, "ui", None)
        if ui is None:
            return 0.0
        if self._shortfall is None or self._shortfall[0] != (ui.s, x, y, w, h):
            self._shortfall = ((ui.s, x, y, w, h), self._measure_shortfall(ui, x, y, w, h))
        return self._shortfall[1]

    def _measure_shortfall(self, ui, x, y, w, h) -> float:
        top = self.top_of_prompt(ui, x, y, w) - y
        prompt = self.q.get("prompt") or {}
        if self.q.get("input") == "tribulation":
            need = self.tribulation_need(ui, w)
        else:
            plans = self.input_plans(ui, w)          # (grown for the input at font 7, not the last resort 6)
            need = (min(self.prompt_need(ui, w, PROMPT_SIZES[-1], side) for side in (False, True))
                    + ZONE_GAP + min(p[0] for p in plans if p[1] <= 1))
        return top + need + self.footer_h(ui, w) - h if prompt or need else 0.0

    def __init__(self, game, question: dict, run: dict | None = None, on_result=None):
        self._shortfall = None
        self._reveal_short = None
        self._plans: dict = {}
        super().__init__(game, question)
        self.run = run or {}
        self.on_math_result = on_result
        self.given: dict = {}
        self.timed_out = False
        if question.get("input") == "number":
            game.ui.set_focus("quiz_text")
        prompt = question.get("prompt") or {}
        # M9: the two inputs that are more than one click; their state lives here, not in the widgets
        self.match = MI.MatchingState(len(prompt.get("left") or [])) if question.get("input") == "matching" else None
        self.ordering = MI.OrderingState(len(prompt.get("steps") or [])) if question.get("input") == "ordering" else None
        self.mistake = MI.FindMistakeState(len(prompt.get("lines") or [])) if question.get("input") == "find_mistake" else None
        # M11 đợt 2: a Thiên kiếp - its parts answered one at a time, all sent together
        self.trib = MI.TribulationState(prompt.get("parts") or []) if question.get("input") == "tribulation" else None
        if self.trib is not None:                   # the number boxes keep their text by id: start empty
            for k in range(self.trib.n):
                game.ui.set_value(f"trib_text_{k}", "")
        self.prompt_scroll = 0          # the first line of a long prompt in view
        self.reveal_scroll = 0          # the first line of the reveal in view
        self.prompt_scrolls = False     # (set while drawing: the layout audit reads them)
        self.reveal_scrolls = False

    # ------------------------------------------------------------ actions
    def submit(self, answer: dict):
        if not self.sent:
            self.given = answer
        super().submit(answer)

    def update(self, dt, top):
        self.t += dt
        if self.result:
            self.result_t += dt
        elif not self.sent and self.t > self.limit:
            self.timed_out = True                       # the server counts it as a wrong answer
            self.submit({"timed_out": True})

    def finish(self, stop: bool = False):
        self.close()
        self.tell_fortune()
        if self.on_math_result and self.result:
            self.on_math_result(self.result, stop)

    def tell_fortune(self) -> None:
        """M10: a right answer can bring a cơ duyên. The answer itself says so
        (`math.fortune_offer`), whichever card asked the question, and the player is told
        when that card closes."""
        from .math_fortune import notice      # imported here: that module imports this one
        notice(self.game, self.result)

    def seconds_left(self) -> int:
        return max(0, math.ceil(self.limit - self.t))

    def given_text(self) -> str:
        """What the player answered, as the reveal shows it: an option's text as maths, typed
        text exactly as typed."""
        g = self.given
        if "value" in g:
            return T.MATH_TRUE if g["value"] else T.MATH_FALSE
        if "option" in g:
            return pretty(next((o["text"] for o in self.q.get("options") or [] if o["id"] == g["option"]), ""))
        if "pairs" in g or "order" in g or "line" in g:
            return MI.given_text(self.q.get("input", ""), g)
        return str(g.get("text", ""))

    # ------------------------------------------------------------ zones (measured, not drawn)
    def header_lines(self, ui, w) -> tuple[list[str], str]:
        """The left of the header (subject · floor · skill, wrapped to the room the tier label
        leaves; the subject is dropped when it would take more than two lines) and the tier."""
        m = self.q.get("math", {})
        tier = T.MATH_TIER_LABEL.format(n=m.get("tier", "?"), name=m.get("tier_name_vi", ""))
        room = w - 24 - ui.text_size(tier, HEAD)[0] - 10
        parts = [m.get("subject_name_vi", ""), T.MATH_FLOOR.format(n=m.get("floor", "?")),
                 pretty(m.get("skill_name_vi", ""))]
        lines = MI._wrap(ui, " · ".join(p for p in parts if p), HEAD, room)
        if len(lines) > 2:
            lines = MI._wrap(ui, " · ".join(p for p in parts[1:] if p), HEAD, room)
        return lines, tier

    def header_h(self, ui, w) -> float:
        return _block(ui, len(self.header_lines(ui, w)[0]), HEAD)

    def status_items(self) -> list[tuple[str, str, str]]:
        """The badges under the countdown: (text, colour, "left" / "center" / "right")."""
        m = self.q.get("math", {})
        badge = (T.MATH_PARALLEL if m.get("parallel") else       # rule 6a: the idea just missed
                 review_badge(m) if m.get("review") else "")     # rule 6b: a question from another node
        return [(pretty(badge), UICOL["accent"], "center")] if badge else []

    def instruction(self) -> str:
        if self.q.get("input") == "number":       # one clear line: how a number is written
            return T.MATH_NUMBER_INSTRUCTION
        return self.q.get("instruction_vi", "")

    def head_items(self) -> list[tuple[str, str, str]]:
        """The badges and the instruction, in the order the rows take them: the instruction
        comes right after the left-hand badges, so it shares their row when it fits between
        them and a right-hand one."""
        items = self.status_items()
        lefts = [it for it in items if it[2] == "left"]
        instr = self.instruction()
        return lefts + ([(instr, GREY, "center")] if instr else []) + [it for it in items if it[2] != "left"]

    def top_of_prompt(self, ui, x, y, w) -> float:
        """Where the prompt zone starts: under the header, the countdown, the badges and the
        instruction."""
        cy = y + 6 + self.header_h(ui, w) + 3 + _lh(ui, 8) + 3
        rows = flow_rows(ui, self.head_items(), w - 24)
        return cy + sum(rh + 2 for rh, _ in rows) - 2 + ZONE_GAP

    def footer_h(self, ui, w) -> float:
        return float(self.input_margin())

    def side_width(self, ui, w) -> float:
        """The width of the matrices when they stand beside the text (0: they do not, or there
        are none - beside is only for matrices narrower than half the card)."""
        mats = (self.q.get("prompt") or {}).get("matrices")
        if not mats:
            return 0.0
        mw = matrices_size(ui, mats)[0]
        return mw if mw <= (w - 36) / 2 else 0.0

    def prompt_text(self, ui, w, size, side: bool = False) -> list[str]:
        tw = w - 36 - (self.side_width(ui, w) + 12 if side else 0)
        return MI._wrap(ui, pretty((self.q.get("prompt") or {}).get("text", "")), size, tw)

    def prompt_need(self, ui, w, size, side: bool = False) -> float:
        """The height of the prompt at this size, its matrices under the text or beside it."""
        mats = (self.q.get("prompt") or {}).get("matrices")
        lines = self.prompt_text(ui, w, size, side)
        need = _block(ui, len(lines), size) if any(lines) else 0.0
        if mats:
            mh = matrices_size(ui, mats)[1]
            need = max(need, mh) if side else need + 6 + mh
        return need

    def prompt_layouts(self, ui, w) -> list[tuple[int, bool]]:
        """(size, beside) of the prompt, best first: matrices under the text at 10, 9, 8, then
        beside it at 10, 9, 8 (when they are narrow enough)."""
        out = [(size, False) for size in PROMPT_SIZES]
        if self.side_width(ui, w):
            out += [(size, True) for size in PROMPT_SIZES]
        return out

    def input_plans(self, ui, w) -> list[tuple[float, int, dict]]:
        """The ways the input zone can be drawn, best first: (height, rank, plan); rank 0 is a
        plan at the full font size."""
        inp = self.q.get("input")
        prompt = self.q.get("prompt") or {}
        if inp == "truefalse":
            return [(30.0, 0, {})]
        if inp == "number":
            return [(22.0, 0, {})]
        if inp == "choice":
            opts = self.q.get("options") or []
            if not opts:
                return [(0.0, 0, {"cols": 1, "size": 8, "rows": [], "cw": w - 32})]
            plans = []
            for rank, size in enumerate(OPTION_SIZES):
                for cols in ((1, 2) if len(opts) >= 3 else (1,)):
                    need, plan = option_plan(ui, opts, w, cols, size)
                    plans.append((need, rank, plan))
            return plans
        if inp in ("matching", "ordering", "find_mistake"):
            return [(MI.board_need(ui, inp, prompt, w, size), rank, {"size": size})
                    for rank, size in enumerate(MI.SIZES)]
        return [(0.0, 0, {})]

    def tribulation_need(self, ui, w) -> float:
        prompt = self.q.get("prompt") or {}
        parts = prompt.get("parts") or []
        board = max((MI._part_need(ui, p, w) for p in parts), default=0.0)
        mats = prompt.get("matrices") or []
        mh = matrices_size(ui, mats, MI.TEXT_SIZE)[1] if mats else 0.0
        lines = MI._wrap(ui, pretty(prompt.get("text", "")), MI.TEXT_SIZE, w - 32)
        return max(mh, min(len(lines), 4) * _pitch(ui, MI.TEXT_SIZE), MI.MIN_SITUATION) + 4 + board

    def question_plan(self, ui, x, y, w, h) -> dict:
        """Where every zone of the question goes in the card x, y, w, h (cached)."""
        key = ("q", ui.s, x, y, w, h)
        if key in self._plans:
            return self._plans[key]
        plan: dict = {"head": self.header_lines(ui, w), "status": flow_rows(ui, self.head_items(), w - 24)}
        top = self.top_of_prompt(ui, x, y, w)
        bottom = y + h - self.footer_h(ui, w)
        plan["top"], plan["bottom"] = top, bottom
        avail = bottom - top
        if self.q.get("input") == "tribulation":
            self._plans[key] = plan
            return plan
        inputs = self.input_plans(ui, w)
        choice = None
        for allowed in ({0}, {0, 1, 2}):
            for size, side in self.prompt_layouts(ui, w):
                need = self.prompt_need(ui, w, size, side)
                for ineed, rank, ip in inputs:
                    if rank in allowed and need + ZONE_GAP + ineed <= avail + 0.01:
                        choice = (size, side, need, ineed, ip)
                        break
                if choice:
                    break
            if choice:
                break
        if choice is not None:
            size, side, need, ineed, ip = choice
            plan["prompt"] = {"size": size, "lines": self.prompt_text(ui, w, size, side), "h": need,
                              "scroll": False, "side": side}
        else:            # the prompt scrolls (its matrices stay in view beside it); the input keeps its room
            ineed, _, ip = min(inputs, key=lambda p: p[0])
            mats = (self.q.get("prompt") or {}).get("matrices")
            side = bool(self.side_width(ui, w))
            mh = matrices_size(ui, mats)[1] if mats else 0.0
            more = _lh(ui, 6) + 1                   # (the "còn nữa" line under the two lines)
            least = max(_block(ui, 2, 8) + 2 + more, mh if side else (mh + 6 if mats else 0.0))
            view = max(least, avail - ZONE_GAP - ineed)
            plan["prompt"] = {"size": 8, "h": view, "scroll": True, "side": side}
        plan["input"] = ip
        plan["input_h"] = ineed
        plan["input_y"] = top + plan["prompt"]["h"] + ZONE_GAP
        self._plans[key] = plan
        return plan

    # ------------------------------------------------------------ drawing: the question
    def draw_ui(self, ui):
        ui.dim(150)
        x, y, w, h = self.panel_rect()
        ui.panel(x, y, w, h)
        self.draw_header(ui, x, y, w)
        if self.result:
            self.draw_math_result(ui, x, y, w, h)
            return
        plan = self.question_plan(ui, x, y, w, h)
        cy = y + 6 + _block(ui, len(plan["head"][0]), HEAD) + 3
        frac = max(0.0, 1 - self.t / self.limit)
        row = _lh(ui, 8)
        ui.progress(x + 12, cy + row / 2 - 2, w - 74, 4, frac, "#BC4749" if frac < 0.3 else "#6A994E")
        ui.text(T.MATH_SECONDS.format(n=self.seconds_left()), x + w - 12, cy + row / 2, 8,
                "#BC4749" if frac < 0.3 else GREY, anchor="midright")
        draw_flow(ui, plan["status"], x + 12, cy + row + 3, w - 24)
        top, bottom = plan["top"], plan["bottom"]
        prompt = self.q.get("prompt", {})
        if self.q.get("input") == "tribulation" and self.trib is not None:     # M11 đợt 2: Thiên kiếp
            ans = MI.draw_tribulation(ui, self.trib, prompt, x, top, w, bottom, self.sent)
            if ans is not None:
                self.submit(ans)
            self.draw_run(ui, x, y, w, h)
            return
        self.draw_prompt(ui, plan, x, top, w)
        iy = plan["input_y"]
        spare = bottom - iy - plan["input_h"]
        inp = self.q.get("input")
        if inp in ("truefalse", "choice", "number"):
            iy += max(0.0, min(spare / 2, 24.0))            # a little air under a short prompt
        if inp == "truefalse":
            self.draw_true_false(ui, x, iy, w)
        elif inp == "choice":
            self.draw_options(ui, x, iy, w, plan["input"])
        elif inp == "number":
            self.draw_number(ui, x, iy, w)
        elif inp == "matching" and self.match is not None:
            ans = MI.draw_matching(ui, self.match, prompt.get("left") or [], prompt.get("right") or [],
                                   x, iy, w, bottom, self.sent)
            if ans is not None:
                self.submit(ans)
        elif inp == "ordering" and self.ordering is not None:
            ans = MI.draw_ordering(ui, self.ordering, prompt.get("steps") or [], x, iy, w, bottom, self.sent)
            if ans is not None:
                self.submit(ans)
        elif inp == "find_mistake" and self.mistake is not None:        # M11: Tìm chỗ sai
            ans = MI.draw_find_mistake(ui, self.mistake, prompt.get("lines") or [], x, iy, w, bottom, self.sent)
            if ans is not None:
                self.submit(ans)
        self.draw_run(ui, x, y, w, h)

    def draw_header(self, ui, x, y, w):
        lines, tier = self.header_lines(ui, w)
        draw_lines(ui, lines, x + 12, y + 6, HEAD, GREY)
        ui.text(tier, x + w - 12, y + 6, HEAD, UICOL["accent"], anchor="topright")

    def draw_prompt(self, ui, plan, x, top, w):
        p = plan["prompt"]
        prompt = self.q.get("prompt") or {}
        mats = prompt.get("matrices")
        self.prompt_scrolls = p["scroll"]
        side = p.get("side") and mats
        mw = self.side_width(ui, w) if side else 0.0
        if side:                                         # the matrices on the right, the text on the left
            draw_matrices(ui, mats, x + w - 18 - mw, top, centered=False)
        if p["scroll"]:
            rows = [{"text": pretty(prompt.get("text", "")), "colour": INK, "size": 8}]
            if mats and not side:
                rows.append({"matrices": mats, "indent": 8})
            tw = w - 32 - (mw + 12 if side else 0)
            self.prompt_scroll, _ = MI.scroll_view(ui, rows, x + 16, top, tw, p["h"], self.prompt_scroll,
                                                   8, scroll=not self.sent)
            return
        lines, size = p["lines"], p["size"]
        if side:
            draw_lines(ui, lines, x + 18, top, size, INK)
            return
        align = "center" if len(lines) <= 2 else "left"
        cy = draw_lines(ui, lines, x + 18, top, size, INK, align, w - 36) if any(lines) else top
        if mats:
            draw_matrices(ui, mats, x + w / 2, cy + 6)

    def run_line(self, r: dict, answered: bool) -> str:
        """The line along the bottom of the card: how the sitting is going, or - in a Thiên
        kiếp nhỏ - which question of the trial this is and how many misses are left."""
        if r.get("mode") == "trial":
            t = r.get("trial") or {}
            total = t.get("total", 0)
            n = min(total, r.get("asked", 0) + (0 if answered else 1))
            left = max(0, t.get("max_wrong", 0) - t.get("wrong", 0))
            return f"{T.MATH_TRIAL_PROGRESS.format(n=n, t=total)}   {T.MATH_TRIAL_ALLOWED.format(n=left)}"
        line = (f"{T.MATH_COMBO.format(n=r.get('combo', 0))}   "
                f"{T.MATH_SCORE.format(c=r.get('correct', 0), a=r.get('asked', 0))}")
        # M11 đợt 2, rule 8: a rung of a ladder says so; a tier-5 miss says a ladder comes next
        rung = (self.q.get("math") or {}).get("ladder")
        opened = ((getattr(self, "result", None) or {}).get("math") or {}).get("ladder") if answered else None
        if rung:
            line = f"{T.MATH_LADDER_STEP.format(n=rung.get('step', 1), t=rung.get('steps', 1))}   {line}"
        elif opened and opened.get("started"):
            line = f"{T.MATH_LADDER_OPENED.format(t=opened.get('steps', 0))}   {line}"
        return line

    def draw_run(self, ui, x, y, w, h):
        if self.run:
            self.draw_footer_line(ui, self.run_line(self.run, answered=False), x, y, w, h, w - 24, GREY)

    def draw_footer_line(self, ui, text: str, x, y, w, h, room: float, colour) -> None:
        """A line along the bottom-left of the card, in `room`: size 7, else 6, else two lines."""
        for size in (7, 6):
            if ui.text_size(text, size)[0] <= room:
                ui.text(text, x + 12, y + h - 12, size, colour, anchor="midleft")
                return
        lines = MI._wrap(ui, text, 6, room)[:2]
        draw_lines(ui, lines, x + 12, y + h - 12 - _block(ui, len(lines), 6) / 2, 6, colour)

    def draw_true_false(self, ui, x, y, w):
        for i, (wid, label, value) in enumerate((("math_true", T.MATH_TRUE, True),
                                                 ("math_false", T.MATH_FALSE, False))):
            bx = x + w / 2 - 126 + i * 132
            if ui.button(wid, bx, y, 120, 28, f"{i + 1}. {label}", size=10,
                         key=KEYS[i] if not self.sent else None,
                         enabled=not self.sent, style="green" if value else "primary"):
                self.submit({"value": value})

    def draw_options(self, ui, x, y, w, plan: dict | None = None):
        opts = self.q.get("options") or []
        if plan is None:                                 # (a caller with no layout: one column, font 8)
            plan = option_plan(ui, opts, w, 1, 8)[1]
        cols, size, cw = plan["cols"], plan["size"], plan["cw"]
        cy = y
        for r, (rh, lines) in enumerate(plan["rows"]):
            for c, ls in enumerate(lines):
                i = r * cols + c
                o = opts[i]
                bx = x + 16 + c * (cw + 6)
                clicked = ui.button(f"opt_{o['id']}", bx, cy, cw, rh, "", enabled=not self.sent,
                                    key=OPTION_KEYS[i] if not self.sent and i < len(OPTION_KEYS) else None)
                ui.text(str(i + 1), bx + 6, cy + rh / 2, 7, "#8E877A", anchor="midleft")
                draw_lines(ui, ls, bx + 18, cy + (rh - _block(ui, len(ls), size)) / 2, size, INK)
                if clicked and not self.sent:
                    self.submit({"option": o["id"]})
            cy += rh + OPT_GAP

    def draw_number(self, ui, x, y, w):
        # (the instruction above says how to write a number: no second hint here)
        val = ui.input_box("quiz_text", x + w / 2 - 130, y, 180, 20, placeholder=T.MATH_NUMBER_PLACEHOLDER,
                           max_len=60)
        go = ui.button("quiz_submit", x + w / 2 + 58, y, 72, 20, T.QUIZ_SUBMIT, style="primary",
                       enabled=bool(val.strip()) and not self.sent)
        if (go or ui.submitted("quiz_text")) and val.strip() and not self.sent:
            self.submit({"text": val.strip()})

    # ------------------------------------------------------------ drawing: the reveal
    def reveal_lines(self) -> list[tuple[str, str]]:
        """Lines a subclass puts at the top of the reveal (what the answer did in a fight)."""
        return []

    def answer_rows(self, text: str) -> list:
        """The right answer as rows of the reveal: one per pair / step of a matching / ordering
        answer, all of them."""
        inp = self.q.get("input", "")
        green = UICOL["green"]
        if inp not in ("matching", "ordering"):
            return [{"text": T.QUIZ_ANSWER_WAS.format(a=pretty(text)), "colour": green,
                     "size": 8 if inp == "find_mistake" else 9}]
        rows: list = [{"text": T.QUIZ_ANSWER_WAS.format(a=""), "colour": green, "size": 9}]
        lefts = (self.q.get("prompt") or {}).get("left")
        rows += [{"text": pretty(line), "colour": green, "indent": 8} for line in MI.answer_lines(inp, text, lefts)]
        return rows

    def reveal_rows(self, res: dict, good: bool, timed_out: bool) -> list:
        """Everything between the verdict and the footer, in reading order."""
        rows: list = [{"text": pretty(t), "colour": c} for t, c in self.reveal_lines()]
        prompt = self.q.get("prompt") or {}
        rv = res.get("reveal") or {}
        if self.q.get("input") == "tribulation":       # M11 đợt 2: part by part, then the steps (rule 6)
            trib = MI.tribulation_reveal_rows(prompt.get("parts") or [],
                                              {**rv, "solution_vi": [] if good else rv.get("solution_vi") or []},
                                              self.given, bool(good), bool(timed_out))
            for text, colour, indent in trib:          # a numbered step hangs its number, as below
                step = re.match(r"(\d+)\. (.*)", text, re.S) if indent == 4 else None
                rows.append({"text": step.group(2), "colour": colour, "hang": f"{step.group(1)}.", "indent": 2}
                            if step else (text, colour, indent))
            return rows
        if self.q.get("input") != "find_mistake":     # (its prompt is the same long sentence every time)
            rows.append({"text": pretty(prompt.get("text", "")), "colour": GREY})
        if prompt.get("matrices"):
            rows.append({"matrices": prompt["matrices"], "indent": 4})
        if not good and not timed_out and self.given_text():
            rows.append({"text": T.MATH_YOUR_ANSWER.format(a=self.given_text()), "colour": UICOL["accent"]})
        rows += self.answer_rows(rv.get("answer_text", ""))
        if not good and rv.get("solution_vi"):      # rule 6: after a wrong answer, every step
            rows.append({"text": T.MATH_SOLUTION, "colour": INK})
            rows += [{"text": pretty(step), "colour": INK, "hang": f"{n}.", "indent": 2}
                     for n, step in enumerate(rv["solution_vi"], 1)]
        return rows

    def verdict_notes(self, res: dict) -> list[str]:
        m = res.get("math") or {}
        notes = []
        if (res.get("xp") or {}).get("gained"):
            notes.append(T.MATH_XP.format(n=res["xp"]["gained"]))
        run = m.get("run") or {}
        if m.get("tier_change", 0) > 0:
            notes.append(T.MATH_TIER_UP.format(name=run.get("tier_name_vi", "")))
        elif m.get("tier_change", 0) < 0:
            notes.append(T.MATH_TIER_DOWN.format(name=run.get("tier_name_vi", "")))
        if m.get("parallel_waiting"):
            notes.append(T.MATH_WILL_RETURN)
        elif res.get("correct") and m.get("parallel"):
            notes.append(T.MATH_PARALLEL_CLEARED)
        verdict = (m.get("trial") or {}).get("passed")
        if verdict is not None:
            notes.append(T.MATH_TRIAL_PASSED if verdict else T.MATH_TRIAL_FAILED)
        return notes

    def verdict_layout(self, ui, w, res: dict) -> tuple:
        """(title, its colour, the room for the notes, their size, their lines, the bar's height)."""
        good = res.get("correct")
        timed_out = res.get("timed_out") or self.timed_out
        col = UICOL["green"] if good else UICOL["accent"]
        title = T.QUIZ_CORRECT if good else (T.QUIZ_TIMEOUT if timed_out else T.QUIZ_WRONG)
        room = w - 20 - 16 - ui.text_size(title, 12)[0] - 14
        notes = "   ".join(self.verdict_notes(res))
        size, lines = 9, [notes] if notes else []
        if notes and ui.text_size(notes, 9)[0] > room:
            size, lines = 8, MI._wrap(ui, notes, 8, room)
        return title, col, room, size, lines, max(22.0, _block(ui, len(lines), size) + 6)

    def verdict_h(self, ui, w, res: dict) -> float:
        return self.verdict_layout(ui, w, res)[-1]

    def draw_verdict(self, ui, x, y, w, res: dict) -> float:
        """The bar that says right / wrong / out of time, with the notes on its right (wrapped
        when they do not fit beside the title). Returns the y under it."""
        good = res.get("correct")
        title, col, room, size, lines, bh = self.verdict_layout(ui, w, res)
        ui.fill(x + 10, y, w - 20, bh, "#E8F2DC" if good else "#F6E0DE")
        ui.border(x + 10, y, w - 20, bh, col, 2)
        ui.text(title, x + 18, y + bh / 2, 12, col, anchor="midleft")
        if lines:
            draw_lines(ui, lines, x + w - 18 - room, y + (bh - _block(ui, len(lines), size)) / 2, size,
                       "#C99A3A", "right", room)
        return y + bh

    def footer_buttons(self, ui, x, y, w, h) -> float:
        """The buttons of the reveal along the bottom right; returns the x where they start."""
        res = self.result or {}
        left = x + w - 12
        doc = (self.q.get("math") or {}).get("doc")
        if self.in_combat:          # the fight is waiting: no "stop" and no "next"
            left = x + w - 108
        else:
            verdict = ((res.get("math") or {}).get("trial") or {}).get("passed")
            over = verdict is not None                  # the trial is decided: no more questions
            if not over and self.can_stop and ui.button("math_stop", x + w - 176, y + h - 22, 60, 16, T.MATH_STOP,
                                                        key=pygame.K_ESCAPE):
                self.finish(stop=True)
                return x + w - 176
            left = x + w - 176 if (not over and self.can_stop) else x + w - 108
            if ui.button("math_next", x + w - 108, y + h - 22, 96, 16, T.MATH_RESULT if over else T.MATH_NEXT,
                         style="primary") or ui.key(pygame.K_RETURN) or ui.key(pygame.K_SPACE):
                self.finish(stop=over)
        if doc:
            left = min(left, x + w - 252)
            if ui.button("math_doc", x + w - 252, y + h - 22, 70, 16, T.LIB_OPEN, size=7, style="gold",
                         key=pygame.K_t):
                self.game.push(DocScene(self.game, doc["id"], doc.get("block", 0)))
        return left

    def draw_math_result(self, ui, x, y, w, h):
        res = self.result
        good = bool(res.get("correct"))
        timed_out = bool(res.get("timed_out") or self.timed_out)
        top = self.draw_verdict(ui, x, y + 6 + self.header_h(ui, w) + 3, w, res) + 4
        bottom = y + h - self.solution_margin + 12
        rows = self.reveal_rows(res, good, timed_out)
        self.reveal_scroll, self.reveal_scrolls = MI.scroll_view(ui, rows, x + 16, top, w - 32, bottom - top,
                                                                 self.reveal_scroll, 8)
        run = (res.get("math") or {}).get("run") or {}
        left = self.footer_buttons(ui, x, y, w, h)
        if run and self.result is not None and not isinstance(self, CombatCard):   # (a fight has no sitting)
            self.draw_footer_line(ui, self.run_line(run, answered=True), x, y, w, h, left - 8 - (x + 12), GREY)


class MathCombatQuizScene(CombatCard, MathQuizScene):
    """The card a quái lỗi sai opens (M7): the math card of Động Phủ, but low on the screen
    with the fight still visible. The monster's own mistake is named along the bottom, so the
    player can see what they are arguing with. A right answer closes it a moment later; after a
    wrong answer or a timeout it stays until the player has read the solution and closes it
    ("Đã hiểu", Enter or Space)."""
    modal = False
    draws_world = False
    toast_y = 70
    in_combat = True
    solution_margin = 40        # the reveal ends above the row of "Đã hiểu"

    def input_margin(self) -> int:
        """A quái lỗi sai has its mistake written along the bottom of the card: the input zone
        (a board's buttons and key hint included) stays above it."""
        ui = getattr(self.game, "ui", None)
        lines = self.mistake_lines(ui, self.card_rect()[2]) if ui is not None else []
        if not lines or not self.mistake_in_question(ui):
            return 20
        return max(32, int(_block(ui, len(lines), HEAD) + 14))

    def mistake_in_question(self, ui) -> bool:
        """Whether the monster's mistake has room along the bottom of the question: on a card
        that cannot hold the question and it (a long board), the mistake waits for the reveal."""
        if self._mistake_here is None or self._mistake_here[0] != ui.s:
            self._mistake_here = (ui.s, True)
            x, y, w, h = self.card_rect()
            top = self.CARD_TOP
            self._mistake_here = (ui.s, self._measure_shortfall(ui, x, top, w, y + h - top) <= 0)
        return self._mistake_here[1]

    def card_rect(self):
        return (24, 56, 432, 202)

    def __init__(self, game, question: dict, monster_id: str, on_result=None, cast: dict | None = None):
        super().__init__(game, question, run=None, on_result=None)
        self.monster_id = monster_id
        self.cast = cast            # M9: {"k": chiêu id, "name_vi": ...} when a chiêu asked this
        self.on_combat_result = on_result
        self.close_after = 2.0      # (after a right answer; see close_delay)
        self._mistake_here = None

    def mistake_lines(self, ui, w) -> list[str]:
        m = self.q.get("math", {})
        if not m.get("mistake_vi"):
            return []
        return MI._wrap(ui, f"{m.get('monster_vi', '')}: {pretty(m['mistake_vi'])}", HEAD, w - 30)

    def close_delay(self) -> float | None:
        """Seconds after the verdict before the card closes by itself: only after a right
        answer. None: it waits for the player (a mistake is only worth something once read)."""
        res = self.result or {}
        if not res.get("correct"):
            return None
        c = res.get("combat") or {}
        if c.get("cast") and not c.get("missed"):
            return 0.9              # the effect of the chiêu waits for this card to go
        if c.get("shield_broken"):
            return 1.2              # a right answer gets back to the fight a little faster
        return self.close_after

    def update(self, dt, top):
        super().update(dt, top)
        delay = self.close_delay() if self.result else None
        if delay is not None and self.result_t >= delay:
            self.finish()

    def finish(self, stop: bool = False):
        self.close()
        self.tell_fortune()
        if self.on_combat_result and self.result:
            self.on_combat_result(self.result)

    def status_items(self):
        items = []
        if self.cast:                # the chiêu being cast: its name, so the card says what a right answer does
            items.append((T.MSKILL_BADGE.format(name=self.cast.get("name_vi", "")), "#B8862E", "left"))
        return items + super().status_items() + [(T.HOI_THE, UICOL["green"], "right")]

    def draw_ui(self, ui):
        super().draw_ui(ui)
        if self.result:
            return
        x, y, w, h = self.panel_rect()
        lines = self.mistake_lines(ui, w) if self.mistake_in_question(ui) else []
        if lines:
            draw_lines(ui, lines, x + 15, y + h - 7 - _block(ui, len(lines), HEAD), HEAD, UICOL["accent"],
                       "center", w - 30)

    def reveal_lines(self):
        return self.combat_lines() + self.mistake_reveal()

    def mistake_reveal(self) -> list[tuple[str, str]]:
        """The monster's mistake, after a wrong answer on a card that had no room for it before."""
        ui = getattr(self.game, "ui", None)
        m = self.q.get("math", {})
        if ui is None or not m.get("mistake_vi") or self.mistake_in_question(ui) or (self.result or {}).get("correct"):
            return []
        return [(f"{m.get('monster_vi', '')}: {m['mistake_vi']}", UICOL["accent"])]

    def combat_lines(self) -> list[tuple[str, str]]:
        c = (self.result or {}).get("combat") or {}
        if c.get("cast"):           # M9: a chiêu lands or fizzles; it never costs a Mặc Kích
            if c.get("missed"):
                return [(T.MSKILL_MISSED, UICOL["accent"])]
            txt = (T.MSKILL_LANDED_CRIT if c.get("crit") else T.MSKILL_LANDED).format(n=c.get("damage", 0))
            if c.get("combo", 0) > 1:
                txt += "   " + T.MSKILL_COMBO.format(n=c["combo"])
            return [(txt, UICOL["green"])]
        if c.get("shield_broken"):
            return [(f"{T.SHIELD_BROKEN} {T.NGO_DAO} -{c.get('damage', 0)}" + (" (chí mạng!)" if c.get("crit") else ""),
                     UICOL["green"])]
        if c.get("mac_kich"):
            return [(f"{T.MAC_KICH} -{c['mac_kich']}", UICOL["accent"])]
        return []

    def footer_buttons(self, ui, x, y, w, h) -> float:
        left = super().footer_buttons(ui, x, y, w, h)
        waiting = self.close_delay() is None
        if ui.button("math_got_it", x + w - 108, y + h - 22, 96, 16, T.QUIZ_GOT_IT, style="primary"):
            self.finish()
            return left
        if waiting:                  # the key that closes it, on the left of the footer
            ui.text(T.QUIZ_GOT_IT_KEYS, x + 12, y + h - 14, 7, GREY, anchor="midleft")
        # a player who has read enough closes it (not in the first half second: the key that
        # sent the answer must not close the card that shows its solution)
        if self.result_t >= 0.5 and (ui.key(pygame.K_RETURN) or ui.key(pygame.K_SPACE)
                                     or ui.key(pygame.K_ESCAPE)):
            self.finish()
        return left


# M10: (widget id, label, module, scene class) of the doors along the bottom of the hub. The
# scenes are imported when a door is opened, so a mode that is not there costs nothing.
HUB_DOORS = (("math_hub_dungeon", T.MATH_HUB_DUNGEON, ".math_dungeon", "MathDungeonScene"),
             ("math_hub_td", T.MATH_HUB_TD, ".math_td", "MathTdScene"),
             ("math_hub_fortune", T.MATH_HUB_FORTUNE, ".math_fortune", "MathFortuneScene"))


class MathPracticeScene(Scene):
    """The hub of the math bí cảnh: Đạo Thụ, the curriculum tree, and the sitting that runs on a node.

    The first tab is **Chính đạo**, the main quest: a card for the ONE next step the server names
    (GET /math/tree `main`) - the node's full name, why an AI engineer needs it, the chips Hiểu ->
    Luyện -> Vượt cổng and one primary button (also Enter) whose label follows the step: Học bài
    (opens the lesson and reports it read, POST /guide/read), Luyện, Độ Thiên kiếp nhỏ, Làm bài tập.
    Under the card the main nodes of the stage in path order, each done / now / later.

    A tab per branch lists its nodes for browsing: one row per part of a node (a node that spans
    two floors has two) with its gate, its Thiên kiếp nhỏ, its Tàng Thư page and "Luyện"; a node
    ahead of the current step carries "Để sau" but is not blocked. Clicking a node's name opens its
    card. A branch that is a subject keeps the bài kiểm tra đầu vào and the bài tập of that subject.
    Hầm Ngục, Thủ Thành and Cơ Duyên sit small along the bottom under "Luyện thêm".

    Both the tree (GET /math/tree) and the path (GET /math/path, for the placement test and the
    exercise count) are read; the hub shows nothing until both have come. `act=True` (the board's
    "Đi tới") does the card's action as soon as they have."""

    LIST_TOP = 52           # the first row, below the tabs and the header line
    ROW = 16
    SHOWN = 9               # rows that fit above the bottom buttons
    CARD_TOP = 36           # the Chính đạo card, right under the tabs

    def __init__(self, game, act: bool = False):
        super().__init__(game)
        self.path: dict | None = None
        self.tree: dict | None = None
        self.tabs: list[dict] = []
        self.run: dict | None = None
        self.summary: dict | None = None
        self.trial: dict | None = None      # the verdict of the Thiên kiếp nhỏ just finished
        self.busy = False
        self.tab: str | None = None         # the id of the tab shown ("next" or a branch id)
        self.first = 0                      # the first row shown (the list scrolls)
        self.act = act                      # do the Chính đạo action once the tree has come
        self.reload_on_resume = False       # a lesson, exercises or a side mode was opened over the hub

    def on_enter(self):
        self.load()

    def on_resume(self):
        if self.reload_on_resume:
            self.reload_on_resume = False
            self.load(quiet=True)

    def side(self, scene) -> None:
        """Open a scene over the hub; the tree is read again when it closes."""
        self.reload_on_resume = True
        self.game.push(scene)

    # ------------------------------------------------------------ Chính đạo
    def read_lesson(self, node_id: str, floor: int, doc_id: str | None, block: int = 0,
                    practice: bool = False) -> None:
        """Học bài: the lesson of this part, and the server is told it was opened (step hiểu done)."""
        def ok(r):
            if isinstance(r, dict) and r.get("guide"):
                self.game.set_guide(r["guide"], announce=False)
        self.api.post("/guide/read", {"node_id": node_id, "floor": floor}, ok, lambda e: None)
        if doc_id:
            # `practice`: the last page offers "Luyện ngay", straight into a sitting on this part
            self.side(DocScene(self.game, doc_id, block,
                               on_practice=(lambda: self.practise_part(node_id, floor)) if practice else None))
        else:
            self.load()

    def practise_part(self, node_id: str, floor: int) -> None:
        """A sitting on this part: the one left open there, else a new one."""
        run = self.open_run()
        if run and run.get("node_id") == node_id and run.get("floor") == floor:
            self.resume(run)
        else:
            self.start(node_id, floor)

    def do_main(self, m: dict | None = None) -> None:
        """The action of the Chính đạo card's one button (also the board's "Đi tới")."""
        m = m or main_step(self.tree)
        if not m or self.busy:
            return
        step = m["step"]
        if step == "hoc":
            self.read_lesson(m["node_id"], m["floor"], m.get("doc_id"), m.get("block") or 0, practice=True)
        elif step in ("luyen", "kiep"):
            run = self.open_run()
            if m.get("resume") and run and run.get("node_id") == m["node_id"]:
                self.resume(run)
            else:
                self.start(m["node_id"], m["floor"], trial=step == "kiep")
        elif step == "code":
            node = node_by_id(self.tree, m["node_id"]) or {}
            subject = exercises_subject(node) or m.get("subject_id")
            if subject:
                self.side(ProblemListScene(self.game, subject, only=[p["id"] for p in node.get("problems", [])]
                                           or None))

    # ------------------------------------------------------------ server calls
    def load(self, quiet: bool = False):
        """Read the path and the tree. `quiet` (the hub came back from a lesson, exercises or a
        side mode): the buttons stay usable while the new tree comes."""
        if not quiet:
            self.busy = True
        got: dict = {}
        failed = []

        def arrived(key):
            def ok(data):
                got[key] = data
                if len(got) < 2:
                    return
                if not quiet:
                    self.busy = False
                self.path, self.tree = got["path"], got["tree"]
                self.tabs = tab_list(self.tree)
                if self.tab not in [t["id"] for t in self.tabs]:
                    self.tab, self.first = first_tab(self.tree), 0
                if self.act:                    # the board's "Đi tới": the card's action, once
                    self.act = False
                    self.tab = NEXT_TAB
                    self.do_main()
            return ok

        def broke(err):
            if not failed:                  # one message for the pair of requests
                failed.append(err)
                if quiet:
                    self.game.api_error(err)
                else:
                    self.fail(err)
        self.api.get("/math/path", arrived("path"), broke)
        self.api.get("/math/tree", arrived("tree"), broke)

    def tab_subject(self) -> dict | None:
        """The math subject (a block of /math/path) of the branch shown, if it is one."""
        tab = next((t for t in self.tabs if t["id"] == self.tab), None)
        sid = tab.get("subject") if tab else None
        return next((s for s in (self.path or {}).get("subjects", []) if s["id"] == sid), None)

    def open_run(self) -> dict | None:
        return (self.tree or {}).get("run")

    def placement(self, subject: dict):
        """M11: the bài kiểm tra đầu vào of this subject, in a scene of its own."""
        from .math_placement import PlacementScene       # (it imports this module)
        self.game.push(PlacementScene(self.game, subject, on_close=self.load))

    def fail(self, err):
        self.busy = False
        self.game.api_error(err)

    def start(self, node_id: str, floor: int, trial: bool = False):
        """Open a sitting on this part of a node: ordinary practice, or its Thiên kiếp nhỏ (M5)."""
        if self.busy:
            return
        self.busy = True
        self.trial = None

        def ok(res):
            self.run = res["run"]
            self.next_question()
        self.api.post("/math/node/trial" if trial else "/math/node/start",
                      {"node_id": node_id, "floor": floor}, ok, self.fail)

    def resume(self, run: dict):
        if self.busy:
            return
        self.busy = True
        self.run = run
        self.next_question()

    def next_question(self):
        self.busy = True
        self.summary = None

        def ok(res):
            self.busy = False
            self.run = res["run"]
            self.game.push(MathQuizScene(self.game, res["question"], res["run"], on_result=self.on_result))
        self.api.post("/math/run/next", {"run_id": self.run["run_id"]}, ok, self.fail)

    def on_result(self, res: dict, stop: bool):
        m = res.get("math") or {}
        self.run = m.get("run") or self.run
        trial = m.get("trial") or {}
        if trial.get("passed") is not None:         # the Thiên kiếp nhỏ is decided
            self.trial = trial
            self.end()
        elif stop:
            self.end()
        else:
            self.next_question()

    def end(self):
        self.busy = True

        def ok(res):
            self.busy = False
            self.summary = res["run"]
            self.run = None
            self.load()
            self.game.refresh_guide()      # a step may be done now: the "Xong" toast
        self.api.post("/math/run/end", {"run_id": self.run["run_id"]}, ok, self.fail)

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 40, 16, 400, 238
        ui.panel(x, y, w, h, T.MATH_TITLE)
        ready = self.path is not None and self.tree is not None
        if self.summary:
            self.draw_summary(ui, x, y, w, h)
        elif not ready:
            ui.text(T.MATH_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        else:
            self.draw_tree(ui, x, y, w, h)
        if ui.button("math_library", x + 12, y + h - 20, 76, 14, T.LIB_TITLE, size=7, enabled=ready):
            sub = self.tab_subject()
            m = main_step(self.tree) if ready else None
            rows = node_rows(self.tree, self.tab) if ready else []
            first = (m or {}).get("subject_id") if self.tab == NEXT_TAB else None
            first = first or next((r.part["subject_id"] for r in rows if r.part), None)
            self.side(LibraryListScene(self.game, sub["id"] if sub else first))
        if not self.summary:      # M10: the other ways to play - side modes, drawn small: "Luyện thêm"
            ui.text(T.PATH_SIDE, x + 95, y + h - 13, 7, PALE, anchor="midleft")
            for i, (wid, label, module, cls) in enumerate(HUB_DOORS):
                bx = x + 148 + i * 59               # (light: a thin pale frame, no fill, no shadow)
                ui.border(bx, y + h - 19, 56, 12, "#C9B48A")
                if ui.button(wid, bx, y + h - 19, 56, 12, label, size=7, style="ghost", enabled=ready,
                             tooltip=T.PATH_SIDE_TIP):
                    self.side(getattr(importlib.import_module(module, __package__), cls)(self.game))
        if ui.button("math_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_tree(self, ui, x, y, w, h):
        tab = subject_tabs(ui, "math_tab", self.tabs, [t["id"] for t in self.tabs].index(self.tab),
                           x + 12, y + 19, w - 24)
        if self.tabs[tab]["id"] != self.tab:
            self.tab, self.first = self.tabs[tab]["id"], 0
        m = main_step(self.tree)
        if self.tab == NEXT_TAB and m is not None:
            self.draw_main(ui, x, y, w, h, m)
            return
        self.draw_header(ui, x, y + 36, w)
        rows = node_rows(self.tree, self.tab)
        top, height = y + self.LIST_TOP, self.ROW * self.SHOWN
        if not rows:
            ui.text(T.TREE_NEXT_EMPTY if self.tab == NEXT_TAB else T.TREE_EMPTY, x + w / 2, top + 40, 8, GREY,
                    anchor="center")
            return
        self.first = scroll_rows(ui, self.first, len(rows), self.SHOWN, x, top, w, height)
        run = self.open_run()
        self.later = later_ids(self.tree)       # ahead of the current step on Chính đạo: "Để sau"
        cy = top
        for row in rows[self.first:self.first + self.SHOWN]:
            self.draw_row(ui, x, cy, w, row, run)
            cy += self.ROW
        if len(rows) > self.SHOWN:
            ui.text(T.MATH_LIST_MORE.format(a=self.first + 1, b=min(len(rows), self.first + self.SHOWN), t=len(rows)),
                    x + 12, top + height + 4, 7, GREY)

    # ------------------------------------------------------------ the Chính đạo tab
    def draw_main(self, ui, x, y, w, h, m: dict):
        """The card of the one next step, then the main nodes of its stage in path order."""
        cx, cw = x + 12, w - 24
        top = y + self.CARD_TOP
        if m["step"] == "done":
            ui.text(header_text(self.tree["stage"]), cx, top + 2, 8, UICOL["accent"])
            ui.text(T.PATH_DONE_TITLE, x + w / 2, top + 50, 11, UICOL["green"], anchor="center")
            ui.text(T.PATH_DONE_BODY, x + w / 2, top + 66, 8, GREY, anchor="midtop", max_w=w - 60)
            return
        bottom = self.draw_card(ui, cx, top, cw, m)
        self.draw_stage_list(ui, cx, bottom + 5, cw, y + h - 24, m)

    def draw_card(self, ui, x, y, w, m: dict) -> float:
        """The card; returns its bottom edge. Nothing on it is cut: the name takes a second line or a
        smaller size, the why wraps."""
        pad, inner = 8, w - 16

        def lh(size):
            return ui.text_size("Ag", size)[1]
        name_size, name_lines = fit_lines(ui, m["name_vi"], inner, sizes=(11, 10, 9, 8), lines=2)
        why = m.get("why_vi") or ""
        why_lines = ui.f.wrap(why, 7, int(inner * ui.s), ui.s) if why else []
        name_h = lh(name_size) * (1 + 1.0 * (len(name_lines) - 1))
        why_h = lh(7) * 1.1 * len(why_lines)
        h = pad + lh(7) + 3 + name_h + 3 + why_h + 6 + 16 + pad - 2
        ui.fill(x + 1, y + 2, w, h, (0, 0, 0, 50))
        ui.fill(x, y, w, h, "#FFF8E6")
        ui.border(x, y, w, h, "#B8862E")
        ui.fill(x, y, 3, h, UICOL["gold"])
        cy = y + pad - 2
        ui.text(main_head(m), x + pad, cy, 7, "#B8862E")
        ui.text(m.get("branch_vi") or "", x + w - pad, cy, 7, GREY, anchor="topright")
        cy += lh(7) + 3
        if ui.button("math_main_info", x + pad - 2, cy - 1, inner + 4, name_h + 2, "", style="ghost"):
            node = node_by_id(self.tree, m["node_id"])
            if node:
                self.game.push(NodeCardScene(self.game, node, self.tree))
        ui.text("\n".join(name_lines), x + pad, cy, name_size, INK, line_gap=1.0)
        cy += name_h + 3
        if why_lines:
            ui.text("\n".join(why_lines), x + pad, cy, 7, GREY, line_gap=1.1)
            cy += why_h
        cy += 6
        # the chips Hiểu -> Luyện -> Vượt cổng, then what is left inside the step
        chx = draw_chips(ui, x + pad, cy + 1, m)
        more = main_progress(m)
        if more:
            ui.text(more, chx, cy + 7.5, 7, GREY, anchor="midleft")
        bw = 104
        if ui.button("math_main_go", x + w - pad - bw, cy - 1, bw, 16, main_label(m), size=8, style="primary",
                     key=pygame.K_RETURN, enabled=not self.busy):
            self.do_main(m)
        if m["step"] in ("luyen", "kiep") and m.get("doc_id") and ui.button(
                "math_main_read", x + w - pad - bw - 62, cy + 1, 58, 12, T.PATH_REREAD, size=7,
                enabled=not self.busy):
            self.read_lesson(m["node_id"], m["floor"], m["doc_id"], m.get("block") or 0,
                             practice=m["step"] == "luyen")
        return y + h

    def draw_stage_list(self, ui, x, y, w, bottom, m: dict):
        """The main nodes of the stage in path order, numbered: done / now / later (dimmed, still
        reachable: a click opens the node's card). One column, or two when the stage is long."""
        nodes = m.get("stage_nodes") or []
        ui.text(T.PATH_LIST.format(n=m.get("stage") or 0), x + 2, y, 7, UICOL["accent"])
        top = y + 11
        if not nodes:
            return
        room = bottom - top
        cols = 1 if room / len(nodes) >= 10 else 2
        per = -(-len(nodes) // cols)
        pitch = min(13.0, room / per)
        colw = w / cols
        for i, n in enumerate(nodes):
            c, r = divmod(i, per)
            rx, ry, rw = x + c * colw, top + r * pitch, colw - (4 if cols > 1 else 0)
            state = n["state"]
            if state == "now":
                ui.fill(rx, ry, rw, pitch - 1, "#F6DFA0")
            if ui.button(f"math_path_{n['id']}", rx, ry, rw, pitch - 1, "", style="ghost"):
                node = node_by_id(self.tree, n["id"])
                if node:
                    self.game.push(NodeCardScene(self.game, node, self.tree))
            ink = {"done": GREY, "now": INK}.get(state, PALE)
            mcol = {"done": UICOL["green"], "now": "#B8862E"}.get(state, PALE)
            mid = ry + (pitch - 1) / 2
            if cols == 1:                       # the state in words at the right end
                mark = T.PATH_STATE.get(state, "")
                ui.text(mark, rx + rw - 3, mid, 7, mcol, anchor="midright")
                room_w = rw - 18 - ui.text_size(mark, 7)[0] - 8
            else:                               # two columns: a coloured square, the name gets the room
                ui.fill(rx + rw - 7, mid - 2, 4, 4, mcol)
                room_w = rw - 18 - 10
            ui.text(f"{i + 1}.", rx + 3, mid, 7, ink, anchor="midleft")
            # one line at 7, 6 or 5; two lines only where two really fit in the row
            two = 2 if pitch >= 2 * ui.text_size("Ag", 6)[1] + 1 else 1
            size, lines = fit_lines(ui, n["name_vi"], room_w, sizes=(7, 6, 5), lines=two)
            ui.text("\n".join(lines), rx + 16, mid, size, ink, anchor="midleft", line_gap=0.95)

    def draw_header(self, ui, x, cy, w):
        """Under the tabs: where the player stands, and - on the branch of a subject - the bài
        kiểm tra đầu vào when it is offered (or going on) and the subject's bài tập (M6)."""
        s = self.tab_subject()
        p = (s or {}).get("placement") or {}
        buttons = bool(s) and bool(s.get("problems") or p.get("offered") or p.get("status") == "in_progress")
        room = w - 190 if buttons else w - 24                 # (the buttons sit at the right end)
        head = header_text(self.tree["stage"])
        ui.text(head, x + 12, cy + 7, 8, UICOL["accent"], anchor="midleft", max_w=room)
        more = progress_text(ui, self.tree["stage"], room - ui.text_size(head, 8)[0] - 8)    # how far inside the stage
        if more:
            ui.text(more, x + 20 + ui.text_size(head, 8)[0], cy + 7, 7, GREY, anchor="midleft")
        if not s:
            return
        if s.get("problems") and ui.button(f"math_code_{s['id']}", x + w - 78, cy, 66, 13,
                                           T.CODE_SHORT, size=7, enabled=not self.busy):
            self.game.push(ProblemListScene(self.game, s["id"]))      # bài tập lập trình (M6)
        going = p.get("status") == "in_progress"
        if (p.get("offered") or going) and ui.button(
                f"math_place_{s['id']}", x + w - 174, cy, 90, 13,
                T.MATH_PLACE_CONTINUE if going else T.MATH_PLACE_BUTTON, size=7, style="gold",
                enabled=not self.busy):
            self.placement(s)

    def draw_row(self, ui, x, cy, w, row: Row, run: dict | None):
        node, part, kind = row.node, row.part, row_state(row)
        # ahead on Chính đạo and open (a locked node already says what it needs first)
        later = node["id"] in getattr(self, "later", ()) and kind != "locked"
        ink = INK if kind in ("part", "code") and not later else PALE
        if later:                                   # ahead on Chính đạo: reachable, but marked
            ui.text(stage_text(node), x + 12, cy + 4, 6, GREY, anchor="midleft")
            ui.text(T.PATH_LATER, x + 12, cy + 11, 6, "#B8862E", anchor="midleft")
        else:
            ui.text(stage_text(node), x + 12, cy + 7, 7, GREY if node.get("stage") is not None else "#C99A3A",
                    anchor="midleft")
        info = f"math_info_{node['id']}" if row.first else f"math_info_{node['id']}_{row.index}"
        if ui.button(info, x + 50, cy, 128 if part is not None else 172, 13, "", style="ghost"):
            self.game.push(NodeCardScene(self.game, node, self.tree))
        # (a row with no part has no tiers, so its name may use the room of the tiers column); a long
        # name goes on two lines or a size smaller, never cut
        tail = " " + T.TREE_PART.format(i=row.index, n=row.count) if row.count > 1 else ""
        size, lines = fit_lines(ui, node["name_vi"] + tail, 124 if part is not None else 170)
        ui.text("\n".join(lines), x + 52, cy + 7, size, ink, anchor="midleft", line_gap=1.0)
        if part is not None:
            ui.text(tiers_text(part["tier_min"], part["tier_max"]), x + 182, cy + 7, 7, GREY, anchor="midleft")
        if kind == "vacant":
            ui.text(T.TREE_VACANT, x + w - 12, cy + 7, 7, PALE, anchor="midright")
            return
        if kind == "locked":
            size, lines = fit_lines(ui, locked_reason(node), 166, sizes=(7, 6))
            ui.text("\n".join(lines), x + w - 12, cy + 7, size, PALE, anchor="midright", line_gap=1.0)
            return
        if kind == "code":
            ui.text(T.TREE_NODE_DONE if node["state"] == "done" else T.TREE_CODE_ONLY, x + w - 12, cy + 7, 7,
                    "#C99A3A" if node["state"] == "done" else GREY, anchor="midright")
            return
        floor = part["floor"]
        mine = bool(run) and run.get("node_id") == node["id"] and run.get("floor") == floor
        self.draw_part_gate(ui, x, cy, w, node, part)
        if part.get("doc_id") and ui.button(f"math_doc_{node['id']}_{floor}", x + w - 118, cy, 34, 13,
                                            T.LIB_READ, size=7, style="gold"):
            self.read_lesson(node["id"], floor, part["doc_id"], practice=part_playable(row))
        if part_playable(row) and ui.button(f"math_node_{node['id']}_{floor}", x + w - 76, cy, 64, 13,
                                            T.MATH_RESUME if mine else T.MATH_PLAY, size=7, style="primary",
                                            enabled=not self.busy):
            if mine:
                self.resume(run)
            else:
                self.start(node["id"], floor)

    def draw_part_gate(self, ui, x, cy, w, node: dict, part: dict):
        """The slot between the tiers and the Tàng Thư button (M5): how far the mastery gate has
        come, or the button for the Thiên kiếp nhỏ once the gate is open, or "Đã qua"."""
        gate = part.get("gate")
        if part["passed"]:                          # passed, or skipped by the bài kiểm tra đầu vào
            ui.text(T.MATH_CLEARED, x + w - 122, cy + 7, 7, "#C99A3A", anchor="midright")
        elif not gate:
            return
        elif gate["ok"]:
            if ui.button(f"math_trial_{node['id']}_{part['floor']}", x + w - 180, cy, 58, 13,
                         T.MATH_TRIAL, size=7, style="gold", enabled=not self.busy):
                self.start(node["id"], part["floor"], trial=True)
        else:
            done = sum(1 for k in gate["skills"] if k["ok"])
            ui.text(T.MATH_GATE.format(n=done, t=len(gate["skills"])), x + w - 122, cy + 7, 7, GREY,
                    anchor="midright")

    def gate_hint(self, run: dict) -> str:
        """What the part just practised still wants before its Thiên kiếp nhỏ opens (M5), read
        from the tree that was reloaded when the sitting ended."""
        node = node_by_id(self.tree, run.get("node_id"))
        for part in (node or {}).get("parts", []):
            gate = part.get("gate")
            if part["floor"] == run["floor"] and gate and not gate["ok"] and gate["skills"]:
                k = gate["skills"][0]
                return T.MATH_GATE_HINT.format(need=k["needed"], window=k["window"], tier=k["top_tier"])
        return ""

    def draw_summary(self, ui, x, y, w, h):
        r = self.summary
        if self.trial is not None:                  # the verdict of a Thiên kiếp nhỏ
            t = self.trial
            title = T.MATH_TRIAL_PASSED if t["passed"] else T.MATH_TRIAL_FAILED
            colour = UICOL["green"] if t["passed"] else UICOL["accent"]
            lines = [T.MATH_SUMMARY_SCORE.format(c=t["correct"], a=t["asked"]),
                     T.MATH_SUMMARY_XP.format(n=r["xp_gained"])]
            if t["passed"]:
                if t.get("node_done") and r.get("node_name_vi"):
                    lines.append(T.TREE_NODE_DONE_LINE.format(name=r["node_name_vi"]))
                opened = names_of(self.tree, t.get("opened") or [])
                if opened:                          # the nodes this trial opened, named from the reloaded tree
                    lines.append(T.TREE_OPENED.format(names=", ".join(opened)))
            else:
                lines.append(T.MATH_TRIAL_AGAIN)
        else:
            title, colour = T.MATH_SUMMARY, UICOL["accent"]
            lines = [T.MATH_SUMMARY_SCORE.format(c=r["correct"], a=r["asked"]),
                     T.MATH_SUMMARY_COMBO.format(n=r["best_combo"]),
                     T.MATH_SUMMARY_XP.format(n=r["xp_gained"]),
                     T.MATH_SUMMARY_TIER.format(name=r["tier_name_vi"])]
            if r.get("review_asked"):
                lines.append(T.MATH_REVIEW_COUNT.format(n=r["review_asked"]))
            if r.get("ladders"):                    # M11 đợt 2, rule 8
                lines.append(T.MATH_LADDER_COUNT.format(n=r["ladders"]))
            hint = self.gate_hint(r)
            if hint:
                lines.append(hint)
        ui.text(title, x + w / 2, y + 40, 12, colour, anchor="center")
        if r.get("node_name_vi"):                   # the node the sitting was on
            ui.text(r["node_name_vi"], x + w / 2, y + 52, 8, GREY, anchor="midtop", max_w=w - 40)
        pitch = 18 if len(lines) <= 6 else 15       # (seven lines still clear the button)
        for i, line in enumerate(lines):
            ui.text(line, x + w / 2, y + 74 + i * pitch, 9, "#2B2B2B", anchor="center", max_w=w - 40)
        if ui.button("math_back", x + w / 2 - 45, y + 176, 90, 16, T.MATH_BACK, style="primary",
                     key=pygame.K_RETURN):
            self.summary = self.trial = None
