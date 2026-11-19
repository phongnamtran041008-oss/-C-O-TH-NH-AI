"""The answer inputs of M9 and M11 for the math question card: matching (Ghép cặp), ordering
(Sắp xếp bước giải) and find_mistake (Tìm chỗ sai). Used by the Động Phủ practice card and by the combat card of a chiêu or
a quái lỗi sai, which are the same class underneath.

The state of each input is a small plain object (`MatchingState`, `OrderingState`,
`FindMistakeState`) that knows
nothing about pygame, so the rules - re-pairing, undo, when the answer may be sent - are
tested without a window. `draw_matching` / `draw_ordering` draw the state in a rectangle of
the card, take mouse and keyboard, and return the answer to send (or None):

  * matching: pick a left item, then a right item, and the two are paired (a coloured link
    and the same colour on both). Picking a right item that is already paired moves it.
    The left items are keys 1-5, the right items A-E, Backspace takes the last pair away.
  * ordering: click the steps in the order the solution goes; each shows the number it was
    given and clicking it again takes it back. The steps are keys A-F, Backspace undoes the
    last one.
  * find_mistake (M11): the lines of a worked solution are listed numbered 1-6; click one (or
    press its number) to name it as the first wrong step, click another to change the choice,
    Backspace takes the choice back.

The answer is only sent when every left is paired / every step is numbered, and it is exactly
what the server grades (contract M9 section 1): {"pairs": [...]} / {"order": [...]} /
{"line": i}.

Vietnamese step text is long. Every row wraps its text to its column; when the rows would not
fit the room the card has, the font steps down 8 -> 7 -> 6 and, as the last resort, text is
cut with an ellipsis. Nothing is ever drawn outside the rectangle it was given.
"""
from __future__ import annotations

import re
from fractions import Fraction

import pygame

from .. import strings_vi as T

LETTERS = "ABCDEF"
PAIR_COLOURS = ("#C9573C", "#3C7CC8", "#5E9444", "#B8862E", "#8E5AC8", "#2F8F8F")
SIZES = (8, 7, 6)
BUTTONS_H = 15            # the row of Hoàn tác / Làm lại / Trả lời under the items
GAP = 3                   # between two rows
UI_GOLD = "#B8862E"    # the number badge of an ordered step
LINK = 26                 # the space between the two columns of matching, where the links run


class MatchingState:
    """pairs[k] = index of the right item chosen for left k (None: not paired yet)."""

    def __init__(self, n: int):
        self.n = n
        self.pairs: list[int | None] = [None] * n
        self.sel: int | None = None           # the left item waiting for its right item
        self.history: list[int] = []          # lefts in the order they were paired (for undo)

    def owner_of(self, j: int) -> int | None:
        return next((k for k, v in enumerate(self.pairs) if v == j), None)

    def pick_left(self, k: int) -> None:
        if 0 <= k < self.n:
            self.sel = None if self.sel == k else k

    def pick_right(self, j: int) -> None:
        if not 0 <= j < self.n:
            return
        if self.sel is None:                  # a paired right item: pick its left up again to re-pair it
            self.sel = self.owner_of(j)
            return
        other = self.owner_of(j)
        if other is not None:                 # one right item belongs to one left item only
            self.pairs[other] = None
            self.history = [h for h in self.history if h != other]
        self.pairs[self.sel] = j
        self.history = [h for h in self.history if h != self.sel] + [self.sel]
        self.sel = None

    def unpair(self, k: int) -> None:
        if 0 <= k < self.n and self.pairs[k] is not None:
            self.pairs[k] = None
            self.history = [h for h in self.history if h != k]

    def undo(self) -> None:
        if self.sel is not None:
            self.sel = None
        elif self.history:
            self.unpair(self.history[-1])

    def clear(self) -> None:
        self.__init__(self.n)

    @property
    def complete(self) -> bool:
        return all(v is not None for v in self.pairs) and len(set(self.pairs)) == self.n

    def answer(self) -> dict:
        return {"pairs": [int(v) for v in self.pairs]}


class OrderingState:
    """order = indices into the shown steps, in the order the player clicked them."""

    def __init__(self, n: int):
        self.n = n
        self.order: list[int] = []

    def number_of(self, i: int) -> int | None:
        return self.order.index(i) + 1 if i in self.order else None

    def click(self, i: int) -> None:
        if not 0 <= i < self.n:
            return
        if i in self.order:                   # clicking a numbered step takes it back
            self.order.remove(i)
        else:
            self.order.append(i)

    def undo(self) -> None:
        if self.order:
            self.order.pop()

    def clear(self) -> None:
        self.order = []

    @property
    def complete(self) -> bool:
        return len(self.order) == self.n

    def answer(self) -> dict:
        return {"order": list(self.order)}


class FindMistakeState:
    """sel = index of the line the player names as the first wrong one (None: no choice yet)."""

    def __init__(self, n: int):
        self.n = n
        self.sel: int | None = None

    def click(self, i: int) -> None:
        if 0 <= i < self.n:
            self.sel = i                      # choosing another line changes the choice

    def undo(self) -> None:
        self.sel = None

    def clear(self) -> None:
        self.sel = None

    @property
    def complete(self) -> bool:
        return self.sel is not None

    def answer(self) -> dict:
        return {"line": int(self.sel)}


def given_text(inp: str, given: dict) -> str:
    """What the player answered, short enough for one line of the reveal."""
    if inp == "matching":
        return ", ".join(f"{k + 1}-{LETTERS[j]}" for k, j in enumerate(given.get("pairs") or []))
    if inp == "ordering":
        return ", ".join(LETTERS[i] for i in given.get("order") or [])
    if inp == "find_mistake":
        line = given.get("line")
        return T.FM_STEP.format(n=line + 1) if type(line) is int else ""
    return ""


def answer_lines(inp: str, text: str) -> list[str]:
    """The `answer_text` of the reveal as one line per pair / step."""
    if inp == "matching":
        return [p.strip() for p in text.split(";") if p.strip()]
    if inp == "ordering":
        return [p.strip() for p in re.split(r"\s+(?=\d+\.\s)", text.strip()) if p.strip()]
    return [text] if text else []


# ------------------------------------------------------------------ layout
def _wrap(ui, text: str, size: float, max_w: float) -> list[str]:
    return ui.f.wrap(text, size, int(max_w * ui.s), ui.s) or [""]


def _clip(lines: list[str], n: int) -> list[str]:
    if len(lines) <= n:
        return lines
    keep = lines[:max(1, n)]
    keep[-1] = keep[-1].rstrip()[:-1].rstrip() + "…" if len(keep[-1]) > 1 else "…"
    return keep


def layout(ui, texts: list[str], widths: list[float], avail: float):
    """Pick a font size and row heights so every row fits `avail`. `texts` is a list of rows,
    each a list of the strings that share the row (one per column), `widths` the text width of
    each column. Returns (size, [(row height, [lines per column])])."""
    pitch = lambda size: ui.text_size("Ag", size)[1] * 1.15
    for size in SIZES:
        rows = []
        for row in texts:
            lines = [_wrap(ui, t, size, widths[c]) for c, t in enumerate(row)]
            rows.append((max(14.0, max(len(l) for l in lines) * pitch(size) + 4), lines))
        if sum(h for h, _ in rows) + GAP * (len(rows) - 1) <= avail:
            return size, rows
    size = SIZES[-1]                                    # last resort: cut the text, keep every row
    each = max(7.0, (avail - GAP * (len(texts) - 1)) / max(1, len(texts)))     # (never taller than the room allows)
    fit = max(1, int((each - 4) // pitch(size)))
    return size, [(each, [_clip(_wrap(ui, t, size, widths[c]), fit) for c, t in enumerate(row)])
                  for row in texts]


def _row_text(ui, lines: list[str], x: float, y: float, h: float, size: float, colour="#2B2B2B") -> None:
    pitch = ui.text_size("Ag", size)[1] * 1.15
    top = y + (h - len(lines) * pitch) / 2 + 0.5
    for i, line in enumerate(lines):
        ui.text(line, x, top + i * pitch, size, colour)


def draw_matching(ui, st: MatchingState, left: list[str], right: list[str], x: float, y: float, w: float,
                  bottom: float, sent: bool) -> dict | None:
    """Draw the pairing board in the rectangle x..x+w, y..bottom; returns the answer when sent."""
    cw = (w - 32 - LINK) / 2
    lx, rx = x + 16, x + 16 + cw + LINK
    tw = cw - 22
    avail = bottom - y - BUTTONS_H - 4
    size, rows = layout(ui, [[l, r] for l, r in zip(left, right)], [tw, tw], avail)
    # the rows of both columns are shared, so a left item and the right item beside it are as tall
    pos = []
    cy = y
    for h, _lines in rows:
        pos.append((cy, h))
        cy += h + GAP
    for k in range(st.n):
        ky, kh = pos[k]
        j = st.pairs[k]
        col = pygame.Color(PAIR_COLOURS[k % len(PAIR_COLOURS)])
        if ui.button(f"match_l_{k}", lx, ky, cw, kh, "", enabled=not sent, selected=st.sel == k,
                     key=pygame.K_1 + k if not sent else None):
            st.pick_left(k)
        fg = "#FFFFFF" if st.sel == k else "#2B2B2B"
        ui.text(str(k + 1), lx + 4, ky + kh / 2, 7, "#E9C46A" if st.sel == k else "#8E877A", anchor="midleft")
        _row_text(ui, rows[k][1][0], lx + 14, ky, kh, size, fg)
        if j is not None:
            ui.border(lx, ky, cw, kh, col, 2)
            ui.fill(lx + cw - 11, ky + kh / 2 - 5, 10, 10, col)
            ui.text(LETTERS[j], lx + cw - 6, ky + kh / 2, 7, "#FFFFFF", anchor="center")
    for j in range(st.n):
        jy, jh = pos[j]
        owner = st.owner_of(j)
        if ui.button(f"match_r_{j}", rx, jy, cw, jh, "", enabled=not sent,
                     key=pygame.K_a + j if not sent else None):
            st.pick_right(j)
        ui.text(LETTERS[j], rx + 4, jy + jh / 2, 7, "#8E877A", anchor="midleft")
        _row_text(ui, rows[j][1][1], rx + 14, jy, jh, size)
        if owner is not None:
            col = pygame.Color(PAIR_COLOURS[owner % len(PAIR_COLOURS)])
            ui.border(rx, jy, cw, jh, col, 2)
            ui.fill(rx + cw - 11, jy + jh / 2 - 5, 10, 10, col)
            ui.text(str(owner + 1), rx + cw - 6, jy + jh / 2, 7, "#FFFFFF", anchor="center")
            ky, kh = pos[owner]            # the link between the two paired items
            a = ui.d.to_window(lx + cw, ky + kh / 2)
            b = ui.d.to_window(rx, jy + jh / 2)
            pygame.draw.line(ui.win, col, a, b, max(2, ui.s * 2))
    by = bottom - BUTTONS_H
    return _bottom_row(ui, st, x, by, w, sent, T.MATCH_KEYS)


def draw_ordering(ui, st: OrderingState, steps: list[str], x: float, y: float, w: float, bottom: float,
                  sent: bool) -> dict | None:
    avail = bottom - y - BUTTONS_H - 4
    tw = w - 32 - 40
    size, rows = layout(ui, [[s] for s in steps], [tw], avail)
    cy = y
    for i, (h, lines) in enumerate(rows):
        n = st.number_of(i)
        if ui.button(f"ord_step_{i}", x + 16, cy, w - 32, h, "", enabled=not sent,
                     key=pygame.K_a + i if not sent else None, selected=False):
            st.click(i)
        ui.text(LETTERS[i], x + 21, cy + h / 2, 7, "#8E877A", anchor="midleft")
        _row_text(ui, lines[0], x + 32, cy, h, size)
        if n is not None:                                # the number this step was given
            ui.border(x + 16, cy, w - 32, h, UI_GOLD, 2)
            ui.fill(x + w - 16 - 19, cy + h / 2 - 7, 17, 14, UI_GOLD)
            ui.text(str(n), x + w - 16 - 11, cy + h / 2, 9, "#FFFFFF", anchor="center")
        cy += h + GAP
    return _bottom_row(ui, st, x, bottom - BUTTONS_H, w, sent, T.ORDER_KEYS)


def draw_find_mistake(ui, st: FindMistakeState, lines: list[str], x: float, y: float, w: float, bottom: float,
                      sent: bool) -> dict | None:
    """The numbered lines of the solution as rows; click one (or press its number) to name it."""
    avail = bottom - y - BUTTONS_H - 4
    tw = w - 32 - 40
    size, rows = layout(ui, [[s] for s in lines], [tw], avail)
    cy = y
    for i, (h, ls) in enumerate(rows):
        chosen = st.sel == i
        if ui.button(f"fm_line_{i}", x + 16, cy, w - 32, h, "", enabled=not sent,
                     key=pygame.K_1 + i if not sent else None, selected=chosen):
            st.click(i)
        ui.text(str(i + 1), x + 21, cy + h / 2, 8, "#E9C46A" if chosen else "#8E877A", anchor="midleft")
        _row_text(ui, ls[0], x + 32, cy, h, size, "#FFFFFF" if chosen else "#2B2B2B")
        if chosen:
            ui.border(x + 16, cy, w - 32, h, UI_GOLD, 2)
        cy += h + GAP
    return _bottom_row(ui, st, x, bottom - BUTTONS_H, w, sent, T.FIND_KEYS)


def _bottom_row(ui, st, x: float, y: float, w: float, sent: bool, key_hint: str) -> dict | None:
    """Hoàn tác and Làm lại on the left, Trả lời on the right, the key hint between them."""
    if ui.button("mq_undo", x + 16, y, 56, BUTTONS_H, T.MQ_UNDO, size=7,
                 enabled=not sent and (bool(getattr(st, "history", None) or getattr(st, "order", None))
                                       or getattr(st, "sel", None) is not None),
                 key=pygame.K_BACKSPACE if not sent else None):
        st.undo()
    if ui.button("mq_clear", x + 76, y, 52, BUTTONS_H, T.MQ_CLEAR, size=7, enabled=not sent):
        st.clear()
    ui.text(key_hint, x + 134 + (w - 134 - 16 - 78) / 2, y + BUTTONS_H / 2, 6, "#8E877A", anchor="center",
            max_w=w - 134 - 16 - 84)
    go = ui.button("mq_submit", x + w - 16 - 72, y, 72, BUTTONS_H, T.QUIZ_SUBMIT, style="primary", size=8,
                   enabled=st.complete and not sent, key=pygame.K_RETURN if st.complete and not sent else None)
    return st.answer() if go and st.complete and not sent else None

# ------------------------------------------------------------------ Thiên kiếp (M11 đợt 2)
PART_LETTERS = "abcd"
NAV_H = 15                # the row of Phần trước / Phần sau / Trả lời
PART_H = 13               # the row "Phần a / 3" with one tab per part
TF_H = 18                 # the Đúng / Sai buttons of a true/false part
BOX_H = 16                # the number box of a numeric part
TEXT_SIZE = 8             # the situation and the part's question
MIN_SITUATION = 22        # the situation always keeps at least two lines in view


class TribulationState:
    """A Thiên kiếp being answered: the parts are answered one at a time (`cur`), each one's
    answer is kept - and can be changed - until the whole question is sent. answers[k] is the
    part's answer in the shape its own type is graded in ({"value": bool} | {"option": id} |
    {"text": "..."}), or None while that part has none."""

    def __init__(self, parts: list[dict]):
        self.inputs = [p.get("input", "") for p in parts]
        self.n = len(parts)
        self.cur = 0
        self.answers: list[dict | None] = [None] * self.n
        self.scroll = 0                   # the first line of the situation in view
        self.focused: int | None = None   # the part whose number box was last given the focus

    @property
    def input(self) -> str:
        return self.inputs[self.cur] if self.n else ""

    def go(self, k: int) -> None:
        if 0 <= k < self.n:
            self.cur = k

    def next(self) -> None:
        self.go(self.cur + 1)

    def prev(self) -> None:
        self.go(self.cur - 1)

    def choose(self, value) -> None:
        """The answer of the current part: True / False for a true/false part, an option id for
        a choice part (choosing again changes it)."""
        if self.input == "truefalse" and isinstance(value, bool):
            self.answers[self.cur] = {"value": value}
        elif self.input == "choice" and isinstance(value, str):
            self.answers[self.cur] = {"option": value}

    def set_text(self, k: int, text: str) -> None:
        """What is typed in the number box of part k; an empty box is no answer."""
        if 0 <= k < self.n and self.inputs[k] == "number":
            self.answers[k] = {"text": text.strip()} if text.strip() else None

    def answered(self, k: int) -> bool:
        return 0 <= k < self.n and self.answers[k] is not None

    @property
    def complete(self) -> bool:
        return self.n > 0 and all(a is not None for a in self.answers)

    def answer(self) -> dict:
        return {"parts": [dict(a) for a in self.answers]}


def part_given_text(part: dict, given) -> str:
    """One part's answer as the player gave it, for the reveal."""
    if not isinstance(given, dict):
        return ""
    if "value" in given:
        return T.MATH_TRUE if given["value"] else T.MATH_FALSE
    if "option" in given:
        return next((o["text"] for o in part.get("options") or [] if o["id"] == given["option"]), "")
    return str(given.get("text", ""))


def _number(text: str) -> Fraction | None:
    """One number as the server reads it (math_items.parse_number): 7, -3, 0.25, 3/4."""
    s = text.strip().replace(" ", "")
    if not s or len(s) > 40:
        return None
    try:
        if "/" in s:
            num, den = s.split("/", 1)
            if not re.fullmatch(r"[+-]?\d+", num) or not den.isdigit() or int(den) == 0:
                return None
            return Fraction(int(num), int(den))
        if not re.fullmatch(r"[+-]?(\d+\.?\d*|\.\d+)", s):
            return None
        return Fraction(s)
    except (ValueError, ZeroDivisionError):
        return None


def part_right(key, given) -> bool:
    """Whether one part was answered right, by the rule of its type. Only for drawing the
    reveal: the server's verdict on the whole question is the one that counts."""
    if not isinstance(key, dict) or not isinstance(given, dict):
        return False
    if "value" in key:
        return given.get("value") is key["value"]
    if "option" in key:
        return given.get("option") == key["option"]
    if "numbers" in key:
        text = given.get("text")
        if not isinstance(text, str) or len(text) > 120:
            return False
        got = [_number(p) for p in text.replace(";", ",").split(",")]
        want = [Fraction(n) for n in key["numbers"]]
        if any(g is None for g in got) or len(got) != len(want):
            return False
        if key.get("unordered"):
            got, want = sorted(got), sorted(want)
        tol = Fraction(str(key.get("tolerance", 0)))
        return all(abs(g - w) <= tol for g, w in zip(got, want))
    return False


def tribulation_reveal_rows(parts: list[dict], reveal: dict, given: dict, correct: bool,
                            timed_out: bool) -> list[tuple[str, str, int]]:
    """(text, colour, indent) rows of the reveal of a Thiên kiếp: part by part what was right
    and wrong with the right answer, then the solution steps."""
    green, red, ink, grey = "#3F7A3A", "#B5452E", "#2B2B2B", "#5A5A5A"
    shown = (reveal or {}).get("parts") or []
    given_parts = (given or {}).get("parts")
    rows: list[tuple[str, str, int]] = []
    for k, part in enumerate(parts):
        info = shown[k] if k < len(shown) else {}
        letter, ans = PART_LETTERS[k], info.get("answer_text", "")
        g = given_parts[k] if isinstance(given_parts, list) and k < len(given_parts) else None
        if timed_out and g is None:
            rows.append((T.TRIB_PART_BLANK.format(k=letter, a=ans), grey, 0))
        elif correct or part_right(info.get("key"), g):
            rows.append((T.TRIB_PART_RIGHT.format(k=letter, a=ans), green, 0))
        elif g is None:
            rows.append((T.TRIB_PART_BLANK.format(k=letter, a=ans), red, 0))
        else:
            rows.append((T.TRIB_PART_WRONG.format(k=letter, a=ans), red, 0))
            rows.append((T.TRIB_PART_GIVEN.format(a=part_given_text(part, g)), red, 12))
    steps = (reveal or {}).get("solution_vi") or []
    if steps:
        rows.append((T.MATH_SOLUTION, ink, 0))
        rows += [(f"{n}. {step}", ink, 4) for n, step in enumerate(steps, 1)]
    return rows


def scroll_by(ui, offset: int) -> int:
    """The scroll position after this frame's wheel and Up / Down keys (not clamped)."""
    offset -= int(ui.inp.wheel) if ui.enabled else 0
    if ui.inp.wheel and ui.enabled:
        ui.inp.wheel = 0
    while ui.key(pygame.K_DOWN):
        offset += 1
    while ui.key(pygame.K_UP):
        offset -= 1
    return offset


def draw_scrolled(ui, rows: list[tuple[str, str, int]], x: float, y: float, w: float, bottom: float,
                  offset: int, size: float = 8, scroll: bool = True) -> int:
    """Rows of text wrapped to `w`, drawn from line `offset` for as many lines as fit between
    y and bottom; the wheel and Up / Down move them when they do not all fit (and a small hint
    says so). Nothing is drawn below `bottom`. Returns the clamped offset."""
    pitch = ui.text_size("Ag", size)[1] * 1.15
    lines: list[tuple[str, str, int]] = []
    for text, colour, indent in rows:
        lines += [(line, colour, indent) for line in _wrap(ui, text, size, w - indent - 10)]
    fit = max(1, int((bottom - y) / pitch + 1e-6))
    top = max(0, len(lines) - fit)
    if scroll and len(lines) > fit:
        offset = scroll_by(ui, offset)
    offset = max(0, min(offset, top))
    for i, (line, colour, indent) in enumerate(lines[offset:offset + fit]):
        ui.text(line, x + indent, y + i * pitch, size, colour)
    if len(lines) > fit:                    # a thin bar on the right: where the view is
        bar = bottom - y
        ui.fill(x + w - 3, y, 2, bar, "#D9CDB4")
        ui.fill(x + w - 3, y + bar * offset / len(lines), 2, max(4.0, bar * fit / len(lines)), "#8E877A")
    return offset


def _choice_rows(ui, options: list[dict], w: float, avail: float):
    """(columns, size, rows) for the options of a choice part: one column when they fit, else
    two side by side (layout() steps the font down, and clips as the last resort)."""
    texts = [f"{i + 1}. {o['text']}" for i, o in enumerate(options)]
    size, rows = layout(ui, [[t] for t in texts], [w - 12], avail)
    if size == SIZES[0] and len(texts) > 1 or len(texts) <= 2:
        return 1, size, rows
    cw = (w - 6) / 2
    paired = [texts[i:i + 2] + ([""] if i + 1 >= len(texts) else []) for i in range(0, len(texts), 2)]
    size2, rows2 = layout(ui, paired, [cw - 12, cw - 12], avail)
    return (2, size2, rows2) if size2 >= size else (1, size, rows)


def _part_need(ui, part: dict, w: float) -> float:
    """The height the board of this part wants: its question, its input and the rows around."""
    pitch = ui.text_size("Ag", TEXT_SIZE)[1] * 1.15
    q = min(3, len(_wrap(ui, part.get("text", ""), TEXT_SIZE, w - 32))) * pitch
    inp = part.get("input")
    if inp == "truefalse":
        body = TF_H
    elif inp == "choice":
        opts = part.get("options") or []
        body = sum(14.0 + GAP for _ in range((len(opts) + 1) // 2)) if len(opts) > 2 else 2 * (14 + GAP)
    else:
        body = BOX_H + 10
    return PART_H + 3 + q + 4 + body + 4 + NAV_H


def draw_tribulation(ui, st: TribulationState, prompt: dict, x: float, y: float, w: float, bottom: float,
                     sent: bool) -> dict | None:
    """The whole Thiên kiếp in the rectangle x..x+w, y..bottom: the situation at the top (its
    matrices on the right, the text scrolling with the wheel / Up / Down when it is longer
    than its room), then the current part - "Phần a / 3", its question and its own input -
    and the row that moves between parts and sends them all. Returns the answer when sent."""
    from .mathdraw import draw_matrices, matrices_size
    parts = prompt.get("parts") or []
    if not parts:
        return None
    pitch = ui.text_size("Ag", TEXT_SIZE)[1] * 1.15
    # the board is as tall as its tallest part, so it does not jump when the part changes
    board = max(_part_need(ui, p, w) for p in parts)
    mats = prompt.get("matrices") or []
    mw, mh = matrices_size(ui, mats, TEXT_SIZE) if mats else (0.0, 0.0)
    tw = w - 32 - (mw + 10 if mats else 0)
    lines = _wrap(ui, prompt.get("text", ""), TEXT_SIZE, tw)
    room = max(MIN_SITUATION, bottom - y - board - 4)
    # the text scrolls inside its room; the matrices are never cut (the board gives way instead)
    top_h = max(min(room, len(lines) * pitch), mh, pitch)
    if mats:
        draw_matrices(ui, mats, x + w - 16 - mw, y, centered=False, size=TEXT_SIZE)
    st.scroll = draw_scrolled(ui, [(prompt.get("text", ""), "#2B2B2B", 0)], x + 16, y, tw + 10, y + top_h,
                              st.scroll, TEXT_SIZE, scroll=not sent)
    cy = y + top_h + 4
    ui.fill(x + 16, cy - 2, w - 32, 1, "#D9CDB4")
    return _draw_part(ui, st, parts, x, cy, w, bottom, sent)


def _draw_part(ui, st: TribulationState, parts: list[dict], x: float, y: float, w: float, bottom: float,
               sent: bool) -> dict | None:
    part = parts[st.cur]
    letter = PART_LETTERS[st.cur]
    ui.text(T.TRIB_PART.format(k=letter, n=len(parts)), x + 16, y + PART_H / 2, 8, "#C9573C", anchor="midleft")
    for k in range(len(parts)):                         # one tab per part: green when it has an answer
        bx = x + w - 16 - (len(parts) - k) * 22
        if ui.button(f"trib_part_{k}", bx, y, 20, PART_H - 1, PART_LETTERS[k], size=7, enabled=not sent,
                     selected=k == st.cur, style="green" if st.answered(k) else "normal"):
            st.go(k)
    cy = y + PART_H + 3
    pitch = ui.text_size("Ag", TEXT_SIZE)[1] * 1.15
    nav_y = bottom - NAV_H
    inp = part.get("input")
    # up to three lines of the part's question; fewer only when the card is too short for them
    # and the input below (the last resort: then the text is cut with an ellipsis)
    keep = {"truefalse": TF_H, "number": BOX_H}.get(inp, 2 * (14 + GAP))
    room = max(1, min(3, int((nav_y - 8 - cy - keep) // pitch)))
    q_lines = _clip(_wrap(ui, part.get("text", ""), TEXT_SIZE, w - 32), room)
    for i, line in enumerate(q_lines):
        ui.text(line, x + 16, cy + i * pitch, TEXT_SIZE, "#2B2B2B")
    cy += len(q_lines) * pitch + 4
    if inp == "number":
        wid = f"trib_text_{st.cur}"
        if st.focused != st.cur and not sent:
            ui.set_focus(wid)
            st.focused = st.cur
        val = ui.input_box(wid, x + 16, cy, 170, BOX_H, placeholder=T.MATH_NUMBER_PLACEHOLDER, max_len=60)
        st.set_text(st.cur, val)
        ui.text(T.MATH_NUMBER_HINT, x + 194, cy + BOX_H / 2, 6, "#8E877A", anchor="midleft", max_w=w - 210)
    else:
        if st.focused is not None:
            ui.set_focus(None)
            st.focused = None
        given = st.answers[st.cur] or {}
        if inp == "truefalse":
            for i, (wid, label, value) in enumerate((("trib_true", T.MATH_TRUE, True),
                                                     ("trib_false", T.MATH_FALSE, False))):
                bx = x + w / 2 - 104 + i * 112
                if ui.button(wid, bx, cy, 96, TF_H, f"{i + 1}. {label}", size=9, enabled=not sent,
                             selected=given.get("value") is value, key=pygame.K_1 + i if not sent else None):
                    st.choose(value)
        elif inp == "choice":
            _draw_choices(ui, st, part.get("options") or [], x + 16, cy, w - 32, nav_y - 4, sent,
                          given.get("option"))
    # the row along the bottom: Phần trước, the key hint, Phần sau, Trả lời
    last = st.cur == st.n - 1
    if ui.button("trib_prev", x + 16, nav_y, 62, NAV_H, T.TRIB_PREV, size=7, enabled=not sent and st.cur > 0,
                 key=pygame.K_LEFT if not sent else None):
        st.prev()
    if ui.button("trib_next", x + 82, nav_y, 58, NAV_H, T.TRIB_NEXT, size=7, enabled=not sent and not last,
                 key=pygame.K_RIGHT if not sent else None):
        st.next()
    from .mathdraw import fit
    hint = T.TRIB_KEYS if st.complete or not last else T.TRIB_NEED_ALL
    ui.text(fit(ui, hint, 6, w - 146 - 16 - 84), x + 146 + (w - 146 - 16 - 78) / 2, nav_y + NAV_H / 2, 6,
            "#8E877A", anchor="center")
    go = ui.button("mq_submit", x + w - 16 - 72, nav_y, 72, NAV_H, T.QUIZ_SUBMIT, style="primary", size=8,
                   enabled=st.complete and not sent,
                   key=pygame.K_RETURN if st.complete and last and not sent else None)
    if not sent and not last and (ui.key(pygame.K_RETURN) or ui.key(pygame.K_KP_ENTER)):
        st.next()                                       # Enter before the last part: the next part
    return st.answer() if go and st.complete and not sent else None


def _draw_choices(ui, st: TribulationState, options: list[dict], x: float, y: float, w: float, bottom: float,
                  sent: bool, chosen: str | None) -> None:
    cols, size, rows = _choice_rows(ui, options, w, bottom - y)
    cw = w if cols == 1 else (w - 6) / 2
    cy = y
    for r, (h, lines) in enumerate(rows):
        for c in range(cols):
            i = r * cols + c
            if i >= len(options):
                break
            o = options[i]
            bx = x + c * (cw + 6)
            if ui.button(f"trib_opt_{o['id']}", bx, cy, cw, h, "", enabled=not sent, selected=chosen == o["id"],
                         key=pygame.K_1 + i if not sent and i < 6 else None):
                st.choose(o["id"])
            _row_text(ui, lines[c], bx + 5, cy, h, size, "#FFFFFF" if chosen == o["id"] else "#2B2B2B")
        cy += h + GAP
