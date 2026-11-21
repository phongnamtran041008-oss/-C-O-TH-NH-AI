"""Monospace text and scrolling text panes, for the programming exercises.

VT323 is a monospace font, but not for every letter: a few Vietnamese letters (ầ, ấ, ế, ồ,
ố, ư, ừ, ứ, ử, ữ, ự) are one pixel wider than a digit, and a character VT323 lacks falls back
to Noto Sans, which is proportional. Text measured as a whole string therefore drifts away
from a grid of columns. Here every character gets exactly one cell, the width of "0": runs of
characters that already are one cell wide are drawn as one string (fast, and identical), and
any other character is drawn alone, centred in its cell and shrunk to fit when it is wider.
The caret, clicks and the selection of the editor (codebox.py) use the same grid.

`TextPane` lays out a list of blocks (prose paragraphs, verbatim monospace boxes) into rows
and draws the rows that fit whole, from a first row that the wheel and PgUp / PgDn move, with
a scrollbar when there is more. A row is never cut in half.
"""
from __future__ import annotations

import pygame

from ..art.palette import UI as UICOL

TABSIZE = 4
TRACK = "#E2D8C3"
THUMB = "#B9AD93"


def clean_text(text: str) -> str:
    """Text as the editor keeps it: \\n line ends, tabs expanded to TABSIZE columns, and no
    other control character (they have no glyph and no width)."""
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    out = []
    for line in text.split("\n"):
        line = line.expandtabs(TABSIZE)
        out.append("".join(c for c in line if c >= " " and c != "\x7f"))
    return "\n".join(out)


def cell(ui, size: float) -> tuple[float, float]:
    """(width, height) of one cell in base units: those of "0"."""
    w, h = ui.f.size("0", size, ui.s)
    return w / ui.s, h / ui.s


_EXACT: dict = {}


def one_cell(ui, ch: str, size: float) -> bool:
    """True when VT323 draws this character exactly one cell wide."""
    key = (ch, size, ui.s)
    hit = _EXACT.get(key)
    if hit is None:
        if ch == " ":
            hit = True
        else:
            hit = ui.f._ui_has(ch) and ui.f.size(ch, size, ui.s)[0] == ui.f.size("0", size, ui.s)[0]
        _EXACT[key] = hit
    return hit


def draw_cells(ui, text: str, x: float, y: float, size: float, colour) -> None:
    """Draw `text` one character per cell, starting at (x, y) (top left, base units)."""
    if not text:
        return
    cw_px, ch_px = ui.f.size("0", size, ui.s)
    cw = cw_px / ui.s
    i, n = 0, len(text)
    while i < n:
        if one_cell(ui, text[i], size):
            j = i
            while j < n and one_cell(ui, text[j], size):
                j += 1
            run = text[i:j]
            if run.strip():
                ui.text(run, x + i * cw, y, size, colour)
            i = j
            continue
        _draw_one(ui, text[i], x + i * cw, y, size, colour, cw_px, ch_px)
        i += 1


def _draw_one(ui, ch: str, x: float, y: float, size: float, colour, cw_px: int, ch_px: int) -> None:
    """One character that is not one cell wide: centred in its cell, shrunk to fit."""
    surf = ui.f.render(ch, size, colour, ui.s)
    w, h = surf.get_size()
    if w > cw_px or h > ch_px:
        k = min(cw_px / max(1, w), ch_px / max(1, h))
        surf = pygame.transform.smoothscale(surf, (max(1, int(w * k)), max(1, int(h * k))))
        w, h = surf.get_size()
    wx, wy = ui.d.to_window(x, y)
    wx += (cw_px - w) // 2
    wy += (ch_px - h) // 2
    ui.win.blit(surf, (wx, wy))
    bx, by = (wx - ui.d.ox) / ui.s, (wy - ui.d.oy) / ui.s
    if ui.enabled:
        ui.marks.append((bx, by, w / ui.s, h / ui.s))
    if ui.audit is not None:
        b = surf.get_bounding_rect()
        ink = None
        if b.width and b.height:
            ink = (bx + b.x / ui.s, by + b.y / ui.s, b.width / ui.s, b.height / ui.s)
        ui._record("text", (bx, by, w / ui.s, h / ui.s), text=ch, size=size, owner=ui._owner, lines=1, ink=ink)


def wrap_cells(text: str, cols: int) -> list[tuple[str, bool]]:
    """Verbatim text cut into rows of at most `cols` characters: (row, continues) where
    `continues` says the source line goes on in the next row."""
    cols = max(1, cols)
    rows: list[tuple[str, bool]] = []
    for line in clean_text(text).split("\n"):
        if not line:
            rows.append(("", False))
            continue
        for k in range(0, len(line), cols):
            rows.append((line[k:k + cols], k + cols < len(line)))
    return rows


def wrap_prose(ui, text: str, size: float, max_w: float) -> list[str]:
    """Word wrap as ui.text does it, and a word longer than the whole width (a long name, a
    path) is broken between letters instead of running past the edge."""
    out: list[str] = []
    limit = int(max_w * ui.s)
    for line in ui.f.wrap(text, size, limit, ui.s):
        while ui.f.size(line, size, ui.s)[0] > limit and len(line) > 1:
            k = len(line) - 1
            while k > 1 and ui.f.size(line[:k], size, ui.s)[0] > limit:
                k -= 1
            out.append(line[:k])
            line = line[k:]
        out.append(line)
    return out or [""]


class TextPane:
    """A scrolling list of rows. Blocks (tuples):

        ("text", str, size, colour, indent, gap)     prose, word-wrapped (pass pretty() maths)
        ("mono", str, size, colour, indent, gap)     verbatim, one cell per character, wrapped
                                                     at the width, on a pale box
    `gap`: space after the block, base px."""

    MONO_BG = "#EFE6D2"

    def __init__(self):
        self.first = 0
        self.rows: list[dict] = []
        self._key = None
        self.scrolls = False
        self.shown = 0
        self.max_first = 0

    def layout(self, ui, blocks, w: float) -> list[dict]:
        rows: list[dict] = []
        for kind, text, size, colour, indent, gap in blocks:
            if kind == "mono":
                cw, ch = cell(ui, size)
                cols = max(1, int((w - indent - 4) // cw))
                pieces = wrap_cells(text, cols)
                for k, (piece, cont) in enumerate(pieces):
                    rows.append({"kind": "mono", "text": piece, "size": size, "colour": colour,
                                 "indent": indent, "h": ch, "pitch": ch * 1.15, "cont": cont,
                                 "cols": cols, "first": k == 0, "last": k == len(pieces) - 1})
            else:
                for line in wrap_prose(ui, text, size, w - indent - 2):
                    h = ui.f.render(line or " ", size, "#000000", ui.s).get_height() / ui.s
                    rows.append({"kind": "text", "text": line, "size": size, "colour": colour,
                                 "indent": indent, "h": h, "pitch": h + 0.5})
            if rows:
                rows[-1] = dict(rows[-1], pitch=rows[-1]["pitch"] + gap)
        return rows

    def _fit(self, rows, start: int, avail: float) -> int:
        """How many rows from `start` fit whole in `avail`."""
        used, n = 0.0, 0
        for r in rows[start:]:
            if used + r["h"] > avail + 0.01:
                break
            used += r["pitch"]
            n += 1
        return n

    def draw(self, ui, x: float, y: float, w: float, h: float, blocks, keys: bool = False,
             step: int = 2) -> None:
        avail = h - 4
        key = (tuple(blocks), w, ui.s)
        if key != self._key:
            rows = self.layout(ui, blocks, w)
            self.scrolls = self._fit(rows, 0, avail) < len(rows)
            if self.scrolls:
                rows = self.layout(ui, blocks, w - 5)       # room for the scrollbar
            self.rows, self._key = rows, key
            n = len(rows)
            self.max_first = 0
            while self.max_first < n and self._fit(rows, self.max_first, avail) < n - self.max_first:
                self.max_first += 1
        rows = self.rows
        if self.scrolls:
            if ui.hover(x, y, w, h) and ui.inp.wheel:
                self.first -= ui.inp.wheel * step
                ui.inp.wheel = 0
            if keys:
                page = max(1, self._fit(rows, self.first, avail) - 1)
                if ui.key(pygame.K_PAGEDOWN):
                    self.first += page
                if ui.key(pygame.K_PAGEUP):
                    self.first -= page
        self.first = max(0, min(self.first, self.max_first))
        self.shown = self._fit(rows, self.first, avail)
        inner_w = w - 5 if self.scrolls else w
        ui.push_clip(x, y + 1, inner_w, h - 2)
        try:
            cy = y + 2
            for r in rows[self.first:self.first + self.shown]:
                rx = x + r["indent"]
                if r["kind"] == "mono":
                    top = cy - (1 if r["first"] else 0)
                    bottom = cy + (r["h"] + 1 if r["last"] else r["pitch"])
                    ui.fill(rx - 2, top, inner_w - r["indent"], max(1.0, bottom - top), self.MONO_BG)
                    draw_cells(ui, r["text"], rx, cy, r["size"], r["colour"])
                    if r["cont"]:                       # the line goes on in the next row
                        cw, ch = cell(ui, r["size"])
                        ui.fill(rx + r["cols"] * cw + 0.5, cy + 1, 1, ch - 2, UICOL["accent"])
                elif r["text"].strip():
                    ui.text(r["text"], rx, cy, r["size"], r["colour"])
                cy += r["pitch"]
        finally:
            ui.pop_clip()
        if self.scrolls:
            draw_scrollbar(ui, x + w - 3, y + 2, h - 4, self.first, self.shown, len(rows))


def draw_scrollbar(ui, x: float, y: float, h: float, first: int, shown: int, total: int) -> None:
    """A thin vertical bar: where `shown` rows from `first` sit among `total`."""
    ui.fill(x, y, 2, h, TRACK)
    if total <= 0:
        return
    bar = max(6.0, h * min(1.0, shown / total))
    span = max(1, total - shown)
    pos = (h - bar) * min(1.0, first / span)
    ui.fill(x, y + pos, 2, bar, THUMB)
