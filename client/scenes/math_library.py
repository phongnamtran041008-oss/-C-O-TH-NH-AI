"""Tàng Thư Các of the math bí cảnh: the documents that explain what the questions ask.

The server sends a document as blocks (learning/math_library.py); nothing here parses
Markdown. Text is drawn with the game's own font, matrices are drawn as boxes of numbers,
and every other formula is a picture built before release. When a picture is missing the
plain-text form of the formula is shown instead, so a page is never empty.
"""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..ui import mathdraw
from .base import Scene

GREY = "#5A5A5A"
INK = "#2B2B2B"
PAPER_NOTE = "#F3E7CC"
BODY, HEAD, SECTION = 8, 9, 11
PANEL = (20, 10, 440, 250)            # x, y, w, h
PAD = 16
CONTENT_TOP = 40                      # below the title bar
CONTENT_BOTTOM = 22                   # above the buttons
SCROLL_STEP = 24


def line_h(ui, size: float) -> float:
    return ui.text_size("Ag", size)[1] * 1.15


class DocScene(Scene):
    """One document, laid out once and then scrolled."""

    def __init__(self, game, doc_id: str, block: int = 0):
        super().__init__(game)
        self.doc_id = doc_id
        self.doc: dict | None = None
        self.want_block = block
        self.scroll = 0.0
        self.items: list[dict] = []
        self.block_y: dict[int, float] = {}
        self.total = 0.0
        self.built_for: tuple | None = None
        self.api.get(f"/math/library/{doc_id}", self.loaded, self.game.api_error)

    def loaded(self, doc: dict) -> None:
        self.doc = doc
        self.built_for = None

    # ------------------------------------------------------------ layout
    def content_box(self) -> tuple[float, float, float, float]:
        x, y, w, h = PANEL
        return x + PAD, y + CONTENT_TOP, w - 2 * PAD, h - CONTENT_TOP - CONTENT_BOTTOM

    def build(self, ui) -> None:
        """Turns the blocks into things to draw, with their place on the page. Done again
        only when the window scale changes, because wrapping depends on it."""
        cx, _, cw, _ = self.content_box()
        items: list[dict] = []
        block_y: dict[int, float] = {}
        y = 0.0

        def text_lines(text: str, size: float, colour: str, indent: float = 0.0) -> None:
            nonlocal y
            lh = line_h(ui, size)
            for line in ui.f.wrap(text, size, int((cw - indent) * ui.s), ui.s):
                items.append({"kind": "text", "text": line, "x": indent, "y": y, "size": size, "color": colour})
                y += lh

        for n, b in enumerate(self.doc["blocks"]):
            kind = b["type"]
            block_y[n] = y
            if kind == "section":
                y += 6 if items else 0
                text_lines(b["title_vi"], SECTION, UICOL["accent"])
                items.append({"kind": "fill", "x": 0, "y": y + 1, "w": cw, "h": 1, "color": "#D8CBAE"})
                y += 6
            elif kind == "heading":
                y += 4
                text_lines(b["title_vi"], HEAD, INK)
                y += 2
            elif kind == "text":
                text_lines(b["text"], BODY, INK)
                y += 4
            elif kind in ("bullets", "steps"):
                lh = line_h(ui, BODY)
                for i, item in enumerate(b["items"], 1):
                    if kind == "steps":
                        items.append({"kind": "text", "text": f"{i}.", "x": 2, "y": y, "size": BODY,
                                      "color": GREY})
                    else:
                        items.append({"kind": "fill", "x": 4, "y": y + lh / 2 - 1, "w": 3, "h": 3,
                                      "color": UICOL["accent"]})
                    text_lines(item, BODY, INK, indent=14)
                    y += 2
                y += 3
            elif kind == "formula":
                h = float(b.get("h") or 0) or line_h(ui, BODY)
                items.append({"kind": "formula", "block": b, "x": cw / 2, "y": y + 3, "h": h})
                y += h + 8
            elif kind == "matrices":
                _, h = mathdraw.matrices_size(ui, b["matrices"])
                items.append({"kind": "matrices", "block": b, "x": cw / 2, "y": y + 3, "h": h})
                y += h + 8
            elif kind == "note":
                lines = ui.f.wrap(T.LIB_NOTE + b["text"], BODY, int((cw - 18) * ui.s), ui.s)
                h = len(lines) * line_h(ui, BODY) + 8
                items.append({"kind": "fill", "x": 0, "y": y, "w": cw, "h": h, "color": PAPER_NOTE})
                items.append({"kind": "fill", "x": 0, "y": y, "w": 2, "h": h, "color": UICOL["accent"]})
                y += 4
                for i, line in enumerate(lines):
                    items.append({"kind": "text", "text": line, "x": 8, "y": y, "size": BODY,
                                  "color": INK if i else UICOL["accent"]})
                    y += line_h(ui, BODY)
                y += 8
        self.items, self.block_y, self.total = items, block_y, y
        self.built_for = (ui.s, self.doc_id)
        if self.want_block:
            self.scroll = self.clamp(self.block_y.get(self.want_block, 0.0))
            self.want_block = 0

    def clamp(self, value: float) -> float:
        _, _, _, ch = self.content_box()
        return max(0.0, min(value, max(0.0, self.total - ch)))

    # ------------------------------------------------------------ moving around
    def sections(self) -> list[tuple[int, str]]:
        return [(n, b["title_vi"]) for n, b in enumerate(self.doc["blocks"]) if b["type"] == "section"]

    def current_section(self) -> int:
        here = 0
        for i, (n, _) in enumerate(self.sections()):
            if self.block_y.get(n, 0.0) <= self.scroll + 2:
                here = i
        return here

    def go_section(self, delta: int) -> None:
        sections = self.sections()
        i = max(0, min(len(sections) - 1, self.current_section() + delta))
        self.scroll = self.clamp(self.block_y.get(sections[i][0], 0.0))

    def update(self, dt, top):
        if top and self.doc is not None:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                self.scroll = self.clamp(self.scroll + 120 * dt)
            if keys[pygame.K_UP]:
                self.scroll = self.clamp(self.scroll - 120 * dt)

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = PANEL
        ui.panel(x, y, w, h, T.LIB_TITLE)
        if self.doc is None:
            ui.text(T.MATH_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
            if ui.button("doc_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
                self.close()
            return
        if self.built_for != (ui.s, self.doc_id):
            self.build(ui)
        ui.text(self.doc["title_vi"], x + PAD, y + 20, 10, INK)
        ui.text(T.MATH_FLOOR.format(n=self.doc["floor"]), x + w - PAD, y + 21, 8, GREY, anchor="midright")

        cx, cy, cw, ch = self.content_box()
        if ui.inp.wheel and ui.enabled:
            self.scroll = self.clamp(self.scroll - ui.inp.wheel * SCROLL_STEP)
        for key, delta in ((pygame.K_PAGEDOWN, ch - 12), (pygame.K_PAGEUP, -(ch - 12)),
                           (pygame.K_SPACE, ch - 12)):
            if ui.key(key):
                self.scroll = self.clamp(self.scroll + delta)
        if ui.key(pygame.K_HOME):
            self.scroll = 0.0
        if ui.key(pygame.K_END):
            self.scroll = self.clamp(self.total)
        self.draw_content(ui, cx, cy, cw, ch)
        self.draw_bar(ui, x + w - 7, cy, ch)

        sections = self.sections()
        here = self.current_section()
        ui.text(T.LIB_SECTION.format(n=here + 1, t=len(sections), name=sections[here][1]) if sections else "",
                x + PAD, y + h - 14, 7, GREY, max_w=w - 170)
        if ui.button("doc_prev", x + w - 166, y + h - 20, 44, 14, T.LIB_PREV, size=7,
                     enabled=here > 0, key=pygame.K_LEFT):
            self.go_section(-1)
        if ui.button("doc_next", x + w - 118, y + h - 20, 44, 14, T.LIB_NEXT, size=7,
                     enabled=here < len(sections) - 1, key=pygame.K_RIGHT):
            self.go_section(1)
        if ui.button("doc_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_content(self, ui, cx, cy, cw, ch) -> None:
        wx, wy = ui.d.to_window(cx, cy)
        old = ui.win.get_clip()
        ui.win.set_clip(pygame.Rect(int(wx), int(wy), int(cw * ui.s) + 1, int(ch * ui.s) + 1))
        try:
            for it in self.items:
                top = it["y"] - self.scroll
                height = it.get("h", line_h(ui, it.get("size", BODY)))
                if top + height < -2 or top > ch + 2:
                    continue
                px, py = cx + it["x"], cy + top
                if it["kind"] == "text":
                    ui.text(it["text"], px, py, it["size"], it["color"])
                elif it["kind"] == "fill":
                    ui.fill(px, py, it["w"], it["h"], it["color"])
                elif it["kind"] == "matrices":
                    mathdraw.draw_matrices(ui, it["block"]["matrices"], px, py)
                elif it["kind"] == "formula":
                    if not mathdraw.draw_formula(ui, it["block"], px, py):
                        ui.text(it["block"]["alt"], px, py + height / 2, BODY, UICOL["accent"],
                                anchor="center", max_w=cw)
        finally:
            ui.win.set_clip(old)

    def draw_bar(self, ui, x: float, y: float, ch: float) -> None:
        if self.total <= ch:
            return
        ui.fill(x, y, 3, ch, "#DCD2BC")
        bar = max(10.0, ch * ch / self.total)
        ui.fill(x, y + (ch - bar) * self.scroll / max(1.0, self.total - ch), 3, bar, UICOL["accent"])


def subject_tabs(ui, prefix: str, subjects: list[dict], current: int, x: float, y: float, w: float,
                 h: float = 13) -> int:
    """M11: one tab per bí cảnh (four subjects do not fit one panel), widget ids
    `<prefix>_<subject id>`. Click a tab, or Left / Right to move to the next one. Returns the
    index of the subject now shown."""
    n = len(subjects)
    if not n:
        return 0
    current = max(0, min(current, n - 1))
    gap = 4
    widths = [ui.text_size(s["name_vi"], 7)[0] + 12 for s in subjects]
    k = min(1.0, (w - gap * (n - 1)) / sum(widths))         # names that do not fit are shortened
    cx = x
    for i, s in enumerate(subjects):
        bw = widths[i] * k
        label = s["name_vi"] if k >= 1 else mathdraw.fit(ui, s["name_vi"], 7, bw - 6)
        if ui.button(f"{prefix}_{s['id']}", cx, y, bw, h, label, size=7, selected=i == current):
            current = i
        cx += bw + gap
    if n > 1:
        if ui.key(pygame.K_RIGHT):
            current = (current + 1) % n
        if ui.key(pygame.K_LEFT):
            current = (current - 1) % n
    return current


def scroll_rows(ui, first: int, total: int, shown: int, x: float, y: float, w: float, h: float) -> int:
    """M11: the index of the first row a list shows, after the mouse wheel (over the list) and
    Up / Down. `total` rows, `shown` fit."""
    most = max(0, total - shown)
    if ui.hover(x, y, w, h) and ui.inp.wheel:
        first -= ui.inp.wheel
        ui.inp.wheel = 0
    if ui.key(pygame.K_DOWN):
        first += 1
    if ui.key(pygame.K_UP):
        first -= 1
    return max(0, min(first, most))


class LibraryListScene(Scene):
    """Every document the game ships, one bí cảnh at a time (M11: a tab per subject), floor
    by floor; a subject with more documents than the panel holds scrolls."""

    ROW = 28            # a document: its line and its summary

    def __init__(self, game, subject_id: str | None = None):
        super().__init__(game)
        self.data: dict | None = None
        self.want = subject_id          # open on this subject when it has documents
        self.tab = 0
        self.first = 0                  # the first document shown (scrolling)
        self.api.get("/math/library", self.loaded, self.game.api_error)

    def loaded(self, data: dict) -> None:
        self.data = data
        ids = [s["id"] for s in data.get("subjects", [])]
        self.tab = ids.index(self.want) if self.want in ids else 0

    def open(self, doc_id: str) -> None:
        self.game.push(DocScene(self.game, doc_id))

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 40, 16, 400, 238
        ui.panel(x, y, w, h, T.LIB_TITLE)
        if self.data is None:
            ui.text(T.MATH_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        elif not self.data["subjects"]:
            ui.text(T.LIB_EMPTY, x + w / 2, y + h / 2, 8, GREY, anchor="center")
        else:
            subjects = self.data["subjects"]
            tab = subject_tabs(ui, "lib_tab", subjects, self.tab, x + 12, y + 19, w - 24)
            if tab != self.tab:
                self.tab, self.first = tab, 0
            docs = subjects[self.tab]["documents"]
            top, bottom = y + 38, y + h - 24
            shown = int((bottom - top) // self.ROW)
            self.first = scroll_rows(ui, self.first, len(docs), shown, x, top, w, bottom - top)
            cy = top
            for d in docs[self.first:self.first + shown]:
                ui.text(T.MATH_FLOOR.format(n=d["floor"]), x + 12, cy + 6, 8, INK, anchor="midleft")
                ui.text(mathdraw.fit(ui, d["title_vi"], 8, 150), x + 58, cy + 6, 8, INK, anchor="midleft")
                ui.text(T.LIB_SECTIONS.format(n=len(d["sections"])), x + 218, cy + 6, 7, GREY,
                        anchor="midleft")
                if ui.button(f"lib_open_{d['id']}", x + w - 68, cy, 56, 13, T.LIB_READ, size=7,
                             style="primary"):
                    self.open(d["id"])
                cy += 16
                ui.text(mathdraw.fit(ui, d["summary_vi"], 7, w - 90), x + 58, cy, 7, GREY)
                cy += 12
            more = len(docs) - shown
            if more > 0:
                ui.text(T.MATH_LIST_MORE.format(a=self.first + 1, b=min(len(docs), self.first + shown),
                                                t=len(docs)), x + 12, y + h - 13, 7, GREY, anchor="midleft")
        if ui.button("lib_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()
