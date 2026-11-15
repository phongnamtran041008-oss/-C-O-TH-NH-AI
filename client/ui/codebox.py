"""A small code editor for the programming exercises (M6).

The game's interface kit has a one-line input box; a solution needs several lines, a
caret that moves, and a view that scrolls. This is that, and no more: no syntax colours,
no undo. The text is kept as a list of lines with a (row, col) caret, exactly what the
keys below need, and the file on disk stays the real home of the solution - the player can
edit it in their own editor just as well (plan 5.2: "chạy file bài làm của người học").

The font that ships with the game (VT323) is monospace, so one character is one cell and
the caret lands where it looks like it should.
"""
from __future__ import annotations

import pygame

from ..art.palette import UI as UICOL

TAB = "    "                    # Python, so a tab means four spaces
SIZE = 7                        # font size of the code
LINE_GAP = 1.25
INK = "#2B2B2B"
GUTTER_INK = "#9A9387"


class CodeBox:
    """One editable block of code. `handle` takes this frame's keys, `draw` paints it."""

    def __init__(self, text: str = "", wid: str = "code", max_chars: int = 20000):
        self.wid = wid
        self.max_chars = max_chars
        self.lines: list[str] = (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
        self.row = self.col = 0
        self.top = 0                        # first line shown
        self.rows_shown = 1
        self.blink = 0.0

    # ------------------------------------------------------------ text
    @property
    def text(self) -> str:
        return "\n".join(self.lines)

    def set_text(self, text: str) -> None:
        self.lines = (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
        self.row = min(self.row, len(self.lines) - 1)
        self.col = min(self.col, len(self.lines[self.row]))

    @property
    def chars(self) -> int:
        return sum(len(l) + 1 for l in self.lines) - 1

    def _clamp(self) -> None:
        self.lines = self.lines or [""]
        self.row = max(0, min(self.row, len(self.lines) - 1))
        self.col = max(0, min(self.col, len(self.lines[self.row])))

    def insert(self, s: str) -> None:
        for ch in s:
            if self.chars >= self.max_chars:
                return
            line = self.lines[self.row]
            if ch == "\n":
                indent = line[:len(line) - len(line.lstrip(" "))]    # keep the Python indent
                rest = line[self.col:]
                self.lines[self.row] = line[:self.col]
                self.lines.insert(self.row + 1, indent + rest)
                self.row, self.col = self.row + 1, len(indent)
            else:
                self.lines[self.row] = line[:self.col] + ch + line[self.col:]
                self.col += 1

    def backspace(self) -> None:
        line = self.lines[self.row]
        if self.col > 0:
            back = len(TAB) if self.col >= len(TAB) and line[:self.col].endswith(TAB) else 1
            self.lines[self.row] = line[:self.col - back] + line[self.col:]
            self.col -= back
        elif self.row > 0:
            above = self.lines[self.row - 1]
            self.col = len(above)
            self.lines[self.row - 1] = above + line
            del self.lines[self.row]
            self.row -= 1

    def delete(self) -> None:
        line = self.lines[self.row]
        if self.col < len(line):
            self.lines[self.row] = line[:self.col] + line[self.col + 1:]
        elif self.row < len(self.lines) - 1:
            self.lines[self.row] = line + self.lines[self.row + 1]
            del self.lines[self.row + 1]

    # ------------------------------------------------------------ keys
    def handle(self, ui) -> None:
        """Everything typed this frame. Call it while the box has the focus."""
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL:
            if ui.key(pygame.K_v):
                try:
                    self.insert(pygame.scrap.get_text() or "")
                except (pygame.error, AttributeError):
                    pass
            if ui.key(pygame.K_HOME):
                self.row = self.col = 0
            if ui.key(pygame.K_END):
                self.row, self.col = len(self.lines) - 1, len(self.lines[-1])
            ui.inp.text = []                    # Ctrl+key never types a character
            return
        for t in ui.inp.text:
            self.insert(t)
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
            if self.col:
                self.col -= 1
            elif self.row:
                self.row, self.col = self.row - 1, len(self.lines[self.row - 1])
        if ui.key(pygame.K_RIGHT):
            if self.col < len(self.lines[self.row]):
                self.col += 1
            elif self.row < len(self.lines) - 1:
                self.row, self.col = self.row + 1, 0
        if ui.key(pygame.K_UP):
            self.row = max(0, self.row - 1)
        if ui.key(pygame.K_DOWN):
            self.row = min(len(self.lines) - 1, self.row + 1)
        if ui.key(pygame.K_HOME):
            stripped = len(self.lines[self.row]) - len(self.lines[self.row].lstrip(" "))
            self.col = 0 if self.col == stripped else stripped
        if ui.key(pygame.K_END):
            self.col = len(self.lines[self.row])
        if ui.key(pygame.K_PAGEUP):
            self.row = max(0, self.row - self.rows_shown)
        if ui.key(pygame.K_PAGEDOWN):
            self.row = min(len(self.lines) - 1, self.row + self.rows_shown)
        self._clamp()

    # ------------------------------------------------------------ drawing
    def draw(self, ui, x: float, y: float, w: float, h: float, focused: bool = True) -> None:
        cw, ch = ui.text_size("0", SIZE)
        line_h = ch * LINE_GAP
        self.rows_shown = max(1, int((h - 4) / line_h))
        gutter = cw * (len(str(max(len(self.lines), 1))) + 1)
        if ui.hover(x, y, w, h) and ui.inp.wheel:
            self.top -= ui.inp.wheel * 3
            ui.inp.wheel = 0
        self.top = max(0, min(self.top, max(0, len(self.lines) - self.rows_shown)))
        if self.row < self.top:                                  # keep the caret in view
            self.top = self.row
        elif self.row >= self.top + self.rows_shown:
            self.top = self.row - self.rows_shown + 1

        ui.fill(x, y, w, h, "#FFFDF7")
        ui.border(x, y, w, h, UICOL["accent"] if focused else "#9A9387")
        ui.fill(x + 1, y + 1, gutter, h - 2, "#F2EADA")
        if ui.click_in(x, y, w, h):                              # click to put the caret there
            mx, my = ui.inp.mouse
            self.row = min(len(self.lines) - 1, self.top + max(0, int((my - y - 2) / line_h)))
            self.col = max(0, min(len(self.lines[self.row]), round((mx - x - gutter - 2) / cw)))
        for i in range(self.rows_shown):
            n = self.top + i
            if n >= len(self.lines):
                break
            ly = y + 2 + i * line_h
            ui.text(str(n + 1), x + gutter - 3, ly, SIZE, GUTTER_INK, anchor="topright")
            ui.text(self.lines[n].replace("\t", TAB), x + gutter + 2, ly, SIZE, INK)
        if focused and int(ui.time * 2) % 2 == 0 and self.top <= self.row < self.top + self.rows_shown:
            caret_x = x + gutter + 2 + ui.text_size(self.lines[self.row][:self.col], SIZE)[0]
            ui.fill(min(caret_x, x + w - 2), y + 2 + (self.row - self.top) * line_h, 1, ch, INK)
        if len(self.lines) > self.rows_shown:                    # how far down the file we are
            frac = self.rows_shown / len(self.lines)
            bar = max(6, h * frac)
            pos = (h - bar) * (self.top / max(1, len(self.lines) - self.rows_shown))
            ui.fill(x + w - 3, y + 1 + pos, 2, bar, "#C9BFA8")
