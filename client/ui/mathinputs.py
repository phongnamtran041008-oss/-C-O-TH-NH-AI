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
