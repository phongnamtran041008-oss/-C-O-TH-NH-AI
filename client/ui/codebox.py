"""A small code editor for the programming exercises (M6).

The game's interface kit has a one-line input box; a solution needs several lines, a
caret that moves, and a view that scrolls. This is that, and no more: no syntax colours,
no undo. The text is kept as a list of lines with a (row, col) caret, exactly what the
keys below need, and the file on disk stays the real home of the solution - the player can
edit it in their own editor just as well (plan 5.2: "chạy file bài làm của người học").

Every character occupies exactly one cell, the width of "0" (client/ui/mono.py: a letter
VT323 draws wider, or one only the fallback font has, is drawn alone and shrunk into its
cell), so the caret, a click and the selection land where they look. Tabs become four
spaces, on load and on paste. The text never leaves the box: it is clipped to the text area,
the view scrolls sideways to follow the caret, and a line that goes on past the left or the
right edge shows a mark there. The gutter of line numbers stays fixed.

Keys: arrows, Home / End (Ctrl: the whole file), PgUp / PgDn, Shift with any of them
selects, Ctrl+A selects everything, Ctrl+C / Ctrl+X / Ctrl+V copy, cut and paste (a pasted
block keeps its own indentation), the wheel scrolls (Shift+wheel sideways), a drag selects.
"""
from __future__ import annotations

import pygame

from ..art.palette import UI as UICOL
from .mono import TABSIZE, cell, clean_text, draw_cells, draw_scrollbar

TAB = " " * TABSIZE             # Python, so a tab means four spaces
SIZE = 7                        # font size of the code
LINE_GAP = 1.25
INK = "#2B2B2B"
GUTTER_INK = "#9A9387"
SELECT = "#F3D9A4"
MARK = UICOL["accent"]


def _clipboard_get() -> str:
    try:
        return pygame.scrap.get_text() or ""
    except (pygame.error, AttributeError, NotImplementedError):
        return ""


def _clipboard_put(text: str) -> None:
    try:
        pygame.scrap.put_text(text)
    except (pygame.error, AttributeError, NotImplementedError):
        pass


class CodeBox:
    """One editable block of code. `handle` takes this frame's keys, `draw` paints it."""

    def __init__(self, text: str = "", wid: str = "code", max_chars: int = 20000):
        self.wid = wid
        self.max_chars = max_chars
        self.lines: list[str] = clean_text(text).split("\n")
        self.row = self.col = 0
        self.top = 0                        # first line shown
        self.left = 0                       # first column shown
        self.rows_shown = 1
        self.cols_shown = 1
        self.anchor: tuple[int, int] | None = None     # the other end of the selection
        self.goal: int | None = None        # the column Up / Down try to keep
        self.blink = 0.0
        self.clipboard = ""                 # the last copy, when the system clipboard fails
        self._seen: tuple | None = None     # the caret last drawn: the view follows it when it moves
        self._was_down = False
        self._dragging = False
        self.geometry: dict = {}            # where the last draw put things (tests, clicks)

    # ------------------------------------------------------------ text
    @property
    def text(self) -> str:
        return "\n".join(self.lines)

    def set_text(self, text: str) -> None:
        self.lines = clean_text(text).split("\n")
        self.anchor = None
        self._clamp()

    @property
    def chars(self) -> int:
        return sum(len(l) + 1 for l in self.lines) - 1

    def _clamp(self) -> None:
        self.lines = self.lines or [""]
        self.row = max(0, min(self.row, len(self.lines) - 1))
        self.col = max(0, min(self.col, len(self.lines[self.row])))

    # ------------------------------------------------------------ selection
    def selection(self) -> tuple[tuple[int, int], tuple[int, int]] | None:
        """((row, col), (row, col)) in order, or None when nothing is selected."""
        if self.anchor is None or self.anchor == (self.row, self.col):
            return None
        return tuple(sorted((self.anchor, (self.row, self.col))))

    def selected_text(self) -> str:
        sel = self.selection()
        if not sel:
            return ""
        (r0, c0), (r1, c1) = sel
        if r0 == r1:
            return self.lines[r0][c0:c1]
        return "\n".join([self.lines[r0][c0:]] + self.lines[r0 + 1:r1] + [self.lines[r1][:c1]])

    def delete_selection(self) -> bool:
        sel = self.selection()
        self.anchor = None
        if not sel:
            return False
        (r0, c0), (r1, c1) = sel
        self.lines[r0:r1 + 1] = [self.lines[r0][:c0] + self.lines[r1][c1:]]
        self.row, self.col = r0, c0
        return True

    def select_all(self) -> None:
        self.anchor = (0, 0)
        self.row, self.col = len(self.lines) - 1, len(self.lines[-1])

    # ------------------------------------------------------------ editing
    def insert(self, s: str, auto_indent: bool = True) -> None:
        """Type or paste `s` at the caret (over the selection). A single Enter keeps the
        indent of the line (one step more after a ':'); a pasted block is put in as it is."""
        s = clean_text(s)
        if not s:
            return
        self.delete_selection()
        room = self.max_chars - self.chars
        if room <= 0:
            return
        line = self.lines[self.row]
        head, tail = line[:self.col], line[self.col:]
        if s == "\n" and auto_indent:
            indent = line[:len(line) - len(line.lstrip(" "))][:self.col]
            if head.rstrip().endswith(":"):
                indent += TAB
            s = "\n" + indent[:max(0, room - 1)]
        s = s[:room]
        parts = s.split("\n")
        if len(parts) == 1:
            self.lines[self.row] = head + s + tail
            self.col += len(s)
            return
        self.lines[self.row:self.row + 1] = [head + parts[0]] + parts[1:-1] + [parts[-1] + tail]
        self.row += len(parts) - 1
        self.col = len(parts[-1])

    def paste(self, text: str) -> None:
        self.insert(text, auto_indent=False)

    def backspace(self) -> None:
        if self.delete_selection():
            return
        line = self.lines[self.row]
        if self.col > 0:
            back = len(TAB) if self.col >= len(TAB) and line[:self.col].endswith(TAB) \
                and not line[:self.col].strip() else 1
            self.lines[self.row] = line[:self.col - back] + line[self.col:]
            self.col -= back
        elif self.row > 0:
            above = self.lines[self.row - 1]
            self.col = len(above)
            self.lines[self.row - 1] = above + line
            del self.lines[self.row]
            self.row -= 1

    def delete(self) -> None:
        if self.delete_selection():
            return
        line = self.lines[self.row]
        if self.col < len(line):
            self.lines[self.row] = line[:self.col] + line[self.col + 1:]
        elif self.row < len(self.lines) - 1:
            self.lines[self.row] = line + self.lines[self.row + 1]
            del self.lines[self.row + 1]

    def _move(self, row: int, col: int, extend: bool, keep_goal: bool = False) -> None:
        if extend and self.anchor is None:
            self.anchor = (self.row, self.col)
        elif not extend:
            self.anchor = None
        self.row = max(0, min(row, len(self.lines) - 1))
        self.col = max(0, min(col, len(self.lines[self.row])))
        if not keep_goal:
            self.goal = None

    def _vertical(self, drow: int, extend: bool) -> None:
        goal = self.col if self.goal is None else self.goal
        self._move(self.row + drow, goal, extend, keep_goal=True)
        self.goal = goal

    # ------------------------------------------------------------ keys
    def handle(self, ui) -> None:
        """Everything typed this frame. Call it while the box has the focus."""
        mods = pygame.key.get_mods()
        shift = bool(mods & pygame.KMOD_SHIFT)
        if mods & pygame.KMOD_CTRL:
            if ui.key(pygame.K_v):
                self.paste(_clipboard_get() or self.clipboard)
            if ui.key(pygame.K_a):
                self.select_all()
            copy, cut = ui.key(pygame.K_c), ui.key(pygame.K_x)
            if copy or cut:
                picked = self.selected_text()
                if picked:
                    self.clipboard = picked
                    _clipboard_put(picked)
                    if cut:
                        self.delete_selection()
            if ui.key(pygame.K_HOME):
                self._move(0, 0, shift)
            if ui.key(pygame.K_END):
                self._move(len(self.lines) - 1, len(self.lines[-1]), shift)
            ui.inp.text = []                    # Ctrl+key never types a character
            return
        for t in ui.inp.text:
            self.insert(t)
            self.goal = None
        ui.inp.text = []
        for _ in range(ui.inp.keys.count(pygame.K_BACKSPACE)):
            ui.key(pygame.K_BACKSPACE)
            self.backspace()
        for _ in range(ui.inp.keys.count(pygame.K_DELETE)):
            ui.key(pygame.K_DELETE)
            self.delete()
        for key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            for _ in range(ui.inp.keys.count(key)):
                ui.key(key)
                self.insert("\n")
        for _ in range(ui.inp.keys.count(pygame.K_TAB)):
            ui.key(pygame.K_TAB)
            self.insert(TAB)
        if ui.key(pygame.K_LEFT):
            if self.selection() and not shift:
                (r, c), _ = self.selection()
                self._move(r, c, False)
            elif self.col:
                self._move(self.row, self.col - 1, shift)
            elif self.row:
                self._move(self.row - 1, len(self.lines[self.row - 1]), shift)
        if ui.key(pygame.K_RIGHT):
            if self.selection() and not shift:
                _, (r, c) = self.selection()
                self._move(r, c, False)
            elif self.col < len(self.lines[self.row]):
                self._move(self.row, self.col + 1, shift)
            elif self.row < len(self.lines) - 1:
                self._move(self.row + 1, 0, shift)
        if ui.key(pygame.K_UP):
            self._vertical(-1, shift)
        if ui.key(pygame.K_DOWN):
            self._vertical(1, shift)
        if ui.key(pygame.K_HOME):
            stripped = len(self.lines[self.row]) - len(self.lines[self.row].lstrip(" "))
            self._move(self.row, 0 if self.col == stripped else stripped, shift)
        if ui.key(pygame.K_END):
            self._move(self.row, len(self.lines[self.row]), shift)
        if ui.key(pygame.K_PAGEUP):
            self._vertical(-self.rows_shown, shift)
        if ui.key(pygame.K_PAGEDOWN):
            self._vertical(self.rows_shown, shift)
        self._clamp()

    # ------------------------------------------------------------ geometry
    def cell_at(self, mx: float, my: float) -> tuple[int, int]:
        """The (row, col) a point of the screen (base units) falls on, from the last draw."""
        g = self.geometry
        if not g:
            return self.row, self.col
        row = self.top + int((my - g["text_y"]) // g["line_h"]) if my >= g["text_y"] else self.top - 1
        row = max(0, min(row, len(self.lines) - 1))
        col = self.left + round((mx - g["text_x"]) / g["cw"])
        return row, max(0, min(col, len(self.lines[row])))

    def caret_xy(self) -> tuple[float, float] | None:
        """Where the caret is drawn (base units), or None when it is out of view."""
        g = self.geometry
        if not g or not (self.top <= self.row < self.top + self.rows_shown) \
                or not (self.left <= self.col <= self.left + self.cols_shown):
            return None
        return g["text_x"] + (self.col - self.left) * g["cw"], g["text_y"] + (self.row - self.top) * g["line_h"]

    def _follow_caret(self) -> None:
        if self.row < self.top:
            self.top = self.row
        elif self.row >= self.top + self.rows_shown:
            self.top = self.row - self.rows_shown + 1
        jump = max(1, self.cols_shown // 4)       # scroll sideways in steps, not one column at a time
        if self.col < self.left:
            self.left = max(0, self.col - jump)
        elif self.col > self.left + self.cols_shown - 1:
            self.left = self.col - self.cols_shown + 1 + min(jump, max(0, len(self.lines[self.row]) - self.col))

    # ------------------------------------------------------------ drawing
    def draw(self, ui, x: float, y: float, w: float, h: float, focused: bool = True) -> None:
        cw, ch = cell(ui, SIZE)
        line_h = ch * LINE_GAP
        n = len(self.lines)
        longest = max(len(l) for l in self.lines)
        gutter = cw * (len(str(max(n, 1))) + 1) + 2
        text_x = x + gutter + 4                   # 3 px between gutter and text: the left mark
        text_y = y + 2
        vbar = 0
        rows_fit = max(1, int((h - 4) // line_h))
        if n > rows_fit:
            vbar = 4
        text_w = x + w - 4 - vbar - text_x        # 3 px at the right: the right mark
        cols = max(1, int(text_w // cw))
        hbar = 3 if longest >= cols else 0
        rows = max(1, int((h - 4 - hbar) // line_h))
        if not vbar and n > rows:
            vbar = 4
            text_w = x + w - 4 - vbar - text_x
            cols = max(1, int(text_w // cw))
        self.rows_shown, self.cols_shown = rows, cols
        self.geometry = {"text_x": text_x, "text_y": text_y, "cw": cw, "line_h": line_h, "gutter": gutter,
                         "clip": (text_x, y + 1, cols * cw + 1, rows * line_h + 1)}

        if ui.hover(x, y, w, h) and ui.inp.wheel:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                self.left -= ui.inp.wheel * 4
            else:
                self.top -= ui.inp.wheel * 3
            ui.inp.wheel = 0
        self._mouse(ui, x, y, w, h)
        if (self.row, self.col, n) != self._seen:
            self._follow_caret()
            self._seen = (self.row, self.col, n)
        self.top = max(0, min(self.top, max(0, n - rows)))
        self.left = max(0, min(self.left, max(0, longest - cols + 1)))

        ui.fill(x, y, w, h, "#FFFDF7")
        ui.border(x, y, w, h, UICOL["accent"] if focused else "#9A9387")
        ui.fill(x + 1, y + 1, gutter, h - 2, "#F2EADA")
        sel = self.selection()
        for i in range(rows):
            r = self.top + i
            if r >= n:
                break
            ly = text_y + i * line_h
            ui.text(str(r + 1), x + gutter - 1, ly, SIZE, GUTTER_INK, anchor="topright")
            line = self.lines[r]
            if sel and sel[0][0] <= r <= sel[1][0]:           # the selected part of this row
                c0 = sel[0][1] if r == sel[0][0] else 0
                c1 = sel[1][1] if r == sel[1][0] else len(line) + 1
                a, b = max(c0, self.left), min(c1, self.left + cols)
                if b > a:
                    ui.fill(text_x + (a - self.left) * cw, ly, (b - a) * cw, line_h, SELECT)
            if self.left and line[:self.left]:                # more of the line on the left
                ui.fill(text_x - 3, ly + 1, 2, ch - 1, MARK)
            if len(line) > self.left + cols:                  # and on the right
                ui.fill(text_x + cols * cw + 1, ly + 1, 2, ch - 1, MARK)
        ui.push_clip(*self.geometry["clip"])
        try:
            for i in range(rows):
                r = self.top + i
                if r >= n:
                    break
                draw_cells(ui, self.lines[r][self.left:self.left + cols], text_x, text_y + i * line_h, SIZE, INK)
            caret = self.caret_xy()
            if focused and caret and int(ui.time * 2) % 2 == 0:
                ui.fill(min(caret[0], text_x + cols * cw), caret[1], 1, ch, INK)
        finally:
            ui.pop_clip()
        if vbar:                                              # how far down the file we are
            draw_scrollbar(ui, x + w - 4, y + 2, h - 4 - hbar, self.top, rows, n)
        if hbar:                                              # and how far along the long lines
            track = text_w
            ui.fill(text_x, y + h - 3, track, 2, "#E2D8C3")
            bar = max(6.0, track * min(1.0, cols / max(1, longest + 1)))
            pos = (track - bar) * min(1.0, self.left / max(1, longest + 1 - cols))
            ui.fill(text_x + pos, y + h - 3, bar, 2, "#B9AD93")

    def _mouse(self, ui, x, y, w, h) -> None:
        """A press puts the caret there, a drag selects, a click without a press (a test
        driver) just puts the caret."""
        down = ui.inp.mouse_down and ui.enabled
        mx, my = ui.inp.mouse
        if down and not self._was_down and ui.hover(x, y, w, h):
            self._dragging = True
            self.row, self.col = self.cell_at(mx, my)
            self.anchor = (self.row, self.col)
            self.goal = None
        elif down and self._dragging:
            self.row, self.col = self.cell_at(mx, my)
        if not down and ui.inp.clicked and ui.hover(x, y, w, h):
            ui.inp.clicked = False
            if not self._dragging:
                self.row, self.col = self.cell_at(mx, my)
                self.anchor = None
                self.goal = None
        if not down:
            self._dragging = False
            if self.anchor == (self.row, self.col):
                self.anchor = None
        self._was_down = down
