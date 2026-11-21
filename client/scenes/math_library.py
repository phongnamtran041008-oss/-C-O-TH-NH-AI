"""Tàng Thư Các of the math bí cảnh: the documents that explain what the questions ask.

The server sends a document as blocks (learning/math_library.py); nothing here parses
Markdown. A document is read one page at a time, one page per section (one micro-skill):
a card with the reason to learn it (hook), a figure, the essence in one sentence (core), a
worked example, a formula, Trúc Lão's warning (note) and a self-check whose answer stays
hidden until the player asks for it. Left / Right turn the pages; a page taller than the
panel scrolls.

Text is drawn with the game's own font, matrices are drawn as boxes of numbers, figures
are drawn from the primitives the server laid out (ui/figures.py), and every other formula
is a picture built before release. When a picture is missing the plain-text form of the
formula is shown instead, so a page is never empty.

`layout_problems()` checks the page it has laid out: nothing outside the content box,
nothing on top of something else, no line wider than its column, no figure label outside
its figure. tools/shot_library.py runs it over every page of every document.
"""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..ui import figures, mathdraw
from ..ui.mathtext import pretty
from .base import Scene

GREY = "#5A5A5A"
INK = "#2B2B2B"
PAPER_NOTE = "#F3E7CC"
PAPER_HOOK = "#E3ECD5"
HOOK_EDGE = UICOL["green"]
PAPER_CORE = "#F7E6AE"
CORE_EDGE = "#C99A3A"
CORE_INK = "#8A6418"
PAPER_CHECK = "#ECE4F1"
CHECK_EDGE = "#8E5AC8"
RULE = "#D8CBAE"
BODY, HEAD, SECTION = 8, 9, 11
BODY_V2 = 9                           # a card (format 2) is short, so its text can be bigger
CORE_SIZE = 10
LABEL_SIZE = 7
PANEL = (10, 8, 460, 254)             # x, y, w, h
PAD = 14
CONTENT_TOP = 38                      # below the page header
CONTENT_BOTTOM = 23                   # above the buttons
BAR_W = 4                             # room kept for the scrollbar
SCROLL_STEP = 24
GAP = 5                               # between two blocks
FLOAT_MAX = 0.56                      # a figure at most this share of the width sits beside the text
FLOAT_GAP = 10
CAPTION_MIN = 130                     # a floating figure's caption is at least this wide
BOX_PAD = 5


def line_h(ui, size: float) -> float:
    return ui.text_size("Ag", size)[1] * 1.15


class _Page:
    """Lays out the blocks of one page into items with their rectangles (page coordinates:
    0, 0 is the top-left corner of the content box)."""

    def __init__(self, ui, cw: float, body: float, revealed: set[int]):
        self.ui, self.cw, self.body, self.revealed = ui, cw, body, revealed
        self.items: list[dict] = []
        self.y = 0.0
        self.float_bottom = 0.0
        self.float_top = -1.0
        self.float_x = 0.0
        self.anchors: dict[int, float] = {}

    # -- the column the next block goes into: beside a floating figure, or the full width
    def col(self) -> tuple[float, float]:
        if self.y < self.float_bottom:
            return self.float_x, self.cw - self.float_x
        return 0.0, self.cw

    def clear(self) -> None:
        self.y = max(self.y, self.float_bottom)
        self.float_bottom = 0.0

    def add(self, **it) -> dict:
        self.items.append(it)
        return it

    def lines(self, text: str, size: float, colour: str, x: float, width: float, parent: int | None = None,
              first: str | None = None, first_colour: str | None = None) -> None:
        ui = self.ui
        lh = line_h(ui, size)
        wrapped = ui.f.wrap((first or "") + pretty(text), size, int(width * ui.s), ui.s)   # x^2 drawn as maths
        for i, line in enumerate(wrapped):
            w, h = ui.text_size(line, size)
            it = self.add(kind="text", text=line, x=x, y=self.y, w=w, h=h, size=size, color=colour, role="fg",
                          maxw=width, parent=parent)
            if i == 0 and first and line.startswith(first.strip()):
                it["prefix"], it["prefix_color"] = first, first_colour or UICOL["accent"]
            self.y += lh

    def box(self, x: float, w: float, fill: str, edge: str | None, bar: str | None) -> int:
        """Opens a box at the current y; returns its index (its height is set by close_box)."""
        self.items.append({"kind": "box", "x": x, "y": self.y, "w": w, "h": 0.0, "fill": fill, "edge": edge,
                           "bar": bar, "role": "bg"})
        return len(self.items) - 1

    def close_box(self, i: int) -> None:
        self.items[i]["h"] = self.y - self.items[i]["y"]

    # -- blocks
    @staticmethod
    def clears(kinds: tuple) -> bool:
        """True when the block of kinds[0] (followed by kinds[1:]) is a worked example: it
        reads best on full lines, so it starts below any figure."""
        return bool(kinds) and (kinds[0] == "steps" or (kinds[0] == "text" and kinds[1:2] == ("steps",)))

    def block(self, n: int, b: dict, last: bool, after: tuple = ()) -> None:
        ui, kind = self.ui, b["type"]
        if self.clears((kind,) + after[:1]):
            self.clear()
        self.anchors[n] = self.y
        x, w = self.col()
        body = self.body
        if kind == "section":
            return
        if kind == "heading":
            self.y += 2
            self.lines(b["title_vi"], HEAD + (1 if body > BODY else 0), INK, x, w)
            self.y += 2
        elif kind == "text":
            self.lines(b["text"], body, INK, x, w)
        elif kind in ("bullets", "steps"):
            lh = line_h(ui, body)
            for i, item in enumerate(b["items"], 1):
                if kind == "steps":
                    label = f"{i}."
                    lw, lh_ = ui.text_size(label, body)
                    self.add(kind="text", text=label, x=x + 1, y=self.y, w=lw, h=lh_, size=body,
                             color=UICOL["accent"], role="fg", maxw=12, parent=None)
                else:
                    self.add(kind="fill", x=x + 4, y=self.y + lh / 2 - 1.5, w=3, h=3, color=UICOL["accent"],
                             role="deco")
                self.lines(item, body, INK, x + 14, w - 14)
                self.y += 1
        elif kind == "hook":
            i = self.box(x, w, PAPER_HOOK, None, HOOK_EDGE)
            self.y += BOX_PAD - 1
            self.lines(T.LIB_HOOK, LABEL_SIZE, HOOK_EDGE, x + 8, w - 8 - BOX_PAD, parent=i)
            self.lines(b["text"], body, INK, x + 8, w - 8 - BOX_PAD, parent=i)
            self.y += BOX_PAD - 2
            self.close_box(i)
        elif kind == "core":
            i = self.box(x, w, PAPER_CORE, CORE_EDGE, None)
            self.y += BOX_PAD - 1
            self.lines(T.LIB_CORE, LABEL_SIZE, CORE_INK, x + 7, w - 14, parent=i)
            self.lines(b["text"], CORE_SIZE if body > BODY else HEAD, INK, x + 7, w - 14, parent=i)
            self.y += BOX_PAD - 1
            self.close_box(i)
        elif kind == "note":
            i = self.box(x, w, PAPER_NOTE, None, UICOL["accent"])
            self.y += 4
            # A note that names itself ("Lỗi thường gặp: ...") keeps its own label: the reader's
            # "Trúc Lão nhắc:" in front of it was two labels in a row.
            label, sep, rest = b["text"].partition(": ")
            own = bool(sep) and len(label) <= 24 and rest
            self.lines(rest if own else b["text"], body, INK, x + 8, w - 8 - BOX_PAD, parent=i,
                       first=f"{label}: " if own else T.LIB_NOTE)
            self.y += 3
            self.close_box(i)
        elif kind == "check":
            i = self.box(x, w, PAPER_CHECK, CHECK_EDGE, None)
            self.items[i]["check"] = n
            self.y += BOX_PAD - 1
            self.lines(T.LIB_CHECK, LABEL_SIZE, CHECK_EDGE, x + 7, w - 14, parent=i)
            self.lines(b["question"], body, INK, x + 7, w - 14, parent=i)
            self.y += 1
            if n in self.revealed:
                self.lines(b["answer"], body, INK, x + 7, w - 14, parent=i, first=T.LIB_ANSWER,
                           first_colour=UICOL["green"])
            else:
                self.lines(T.LIB_SHOW, LABEL_SIZE, GREY, x + 7, w - 14, parent=i)
            self.y += BOX_PAD - 1
            self.close_box(i)
        elif kind == "formula":
            fw, fh = float(b.get("w") or 0), float(b.get("h") or 0)
            if fw <= 0 or fh <= 0:          # no picture: its plain-text form, wrapped like text
                self.lines(b["alt"], body, UICOL["accent"], x, w)
            else:
                if fw > w:
                    self.clear()
                    x, w = self.col()
                k = min(1.0, w / fw)
                self.y += 2
                self.add(kind="formula", block={**b, "w": fw * k, "h": fh * k}, x=x + (w - fw * k) / 2, y=self.y,
                         w=fw * k, h=fh * k, role="fg")
                self.y += fh * k + 2
        elif kind == "matrices":
            size = 9
            mw, mh = mathdraw.matrices_size(ui, b["matrices"], size)
            while mw > w and size > 6:
                size -= 1
                mw, mh = mathdraw.matrices_size(ui, b["matrices"], size)
            if mw > w and self.y < self.float_bottom:
                self.clear()
                x, w = self.col()
            self.y += 2
            self.add(kind="matrices", block=b, size=size, x=x + (w - mw) / 2, y=self.y, w=mw, h=mh, role="fg")
            self.y += mh + 2
        elif kind == "figure":
            beside = self.y == self.float_top and b["w"] <= w      # two figures in a row: side by side
            if self.y < self.float_bottom and not beside:    # else a second figure goes below the first
                self.clear()
                x, w = self.col()
                self.anchors[n] = self.y
            # floats only when something can sit beside it: another figure, or a block that is
            # not a worked example
            floating = (b["w"] <= self.cw * FLOAT_MAX and not last and not beside
                        and (after[:1] == ("figure",) or not self.clears(after)))
            if floating:            # a narrow figure: on the left, the text beside it
                self.float_top = self.y
                colw = max(b["w"], CAPTION_MIN)
                fw, fh, k = figures.size(ui, b, colw)
                self.add(kind="figure", block=b, x=x, dx=(colw - fw) / 2, y=self.y + 1, w=colw, h=fh, k=k,
                         role="fg")
                self.float_bottom = self.y + 1 + fh + GAP
                self.float_x = x + colw + FLOAT_GAP
                self.anchors[n] = self.y
                return                      # the next block starts beside it, at the same y
            if b["w"] > w:
                self.clear()
                x, w = self.col()
            fw, fh, k = figures.size(ui, b, w)
            colw = max(fw, min(w, 160.0))
            self.add(kind="figure", block=b, x=x + (w - colw) / 2, dx=(colw - fw) / 2, y=self.y + 1, w=colw, h=fh,
                     k=k, role="fg")
            self.y += fh + 2
        self.y += GAP

    def finish(self) -> float:
        return max(self.y - GAP, self.float_bottom)


class DocScene(Scene):
    """One document, one page per section; a page taller than the panel scrolls."""

    def __init__(self, game, doc_id: str, block: int = 0, on_practice=None):
        super().__init__(game)
        self.doc_id = doc_id
        self.doc: dict | None = None
        self.want_block = block
        self.on_practice = on_practice
        self.page = 0
        self.pages: list[tuple[int, int]] = []        # (first block, end) of each page
        self.page_section: list[int] = []             # the section each page belongs to
        self.scroll = 0.0
        self.items: list[dict] = []
        self.block_y: dict[int, float] = {}
        self.total = 0.0
        self.revealed: set[int] = set()
        self.built_for: tuple | None = None
        self.api.get(f"/math/library/{doc_id}", self.loaded, self.game.api_error)

    def loaded(self, doc: dict) -> None:
        self.doc = doc
        self.built_for = None
        # A page per section; in a format-2 lesson a `###` heading inside a section starts a page of
        # its own, so a micro-skill that holds two ideas is two short pages, not one long scroll.
        breaks = ("section", "heading") if doc.get("format", 1) >= 2 else ("section",)
        starts = [n for n, b in enumerate(doc["blocks"]) if b["type"] in breaks] or [0]
        starts[0] = 0                                    # anything before the first section joins page 1
        ends = starts[1:] + [len(doc["blocks"])]
        self.pages = list(zip(starts, ends))
        first = [n for n, b in enumerate(doc["blocks"]) if b["type"] == "section"]
        self.page_section = [max(0, sum(1 for s in first if s <= a) - 1) for a, _ in self.pages]
        self.page = self.page_of(self.want_block)
        self.want_block = 0
        self.game.guide_seen("library_doc")

    def page_of(self, block: int) -> int:
        for i, (a, b) in enumerate(self.pages):
            if a <= block < b:
                return i
        return 0

    @property
    def v2(self) -> bool:
        return bool(self.doc) and self.doc.get("format", 1) >= 2

    # ------------------------------------------------------------ layout
    def content_box(self) -> tuple[float, float, float, float]:
        x, y, w, h = PANEL
        return x + PAD, y + CONTENT_TOP, w - 2 * PAD - BAR_W, h - CONTENT_TOP - CONTENT_BOTTOM

    def build(self, ui) -> None:
        """Lays out the current page. Done again when the page, the window scale or an
        answer shown changes, because wrapping depends on them."""
        _, _, cw, _ = self.content_box()
        a, b = self.pages[self.page]
        lay = _Page(ui, cw, BODY_V2 if self.v2 else BODY, self.revealed)
        blocks = self.doc["blocks"]
        for n in range(a, b):
            lay.block(n, blocks[n], last=n == b - 1, after=tuple(blk["type"] for blk in blocks[n + 1:min(b, n + 3)]))
        self.items, self.block_y, self.total = lay.items, lay.anchors, lay.finish()
        self.built_for = self.build_key(ui)
        self.scroll = self.clamp(self.scroll)

    def build_key(self, ui) -> tuple:
        return (ui.s, self.doc_id, self.page, frozenset(self.revealed))

    def clamp(self, value: float) -> float:
        _, _, _, ch = self.content_box()
        return max(0.0, min(value, max(0.0, self.total - ch)))

    def at_bottom(self) -> bool:
        _, _, _, ch = self.content_box()
        return self.scroll >= self.total - ch - 0.5

    # ------------------------------------------------------------ moving around
    def sections(self) -> list[tuple[int, str]]:
        return [(n, b["title_vi"]) for n, b in enumerate(self.doc["blocks"]) if b["type"] == "section"]

    def current_section(self) -> int:
        """The index of the section (micro-skill) the page shown belongs to."""
        return self.page_section[self.page] if self.page < len(self.page_section) else self.page

    def part_of_section(self) -> tuple[int, int]:
        """(k, m): the page shown is page k of the m pages of its section."""
        here = self.current_section()
        same = [i for i, s in enumerate(self.page_section) if s == here]
        return (same.index(self.page) + 1, len(same)) if self.page in same else (1, 1)

    def go_page(self, page: int, to_end: bool = False) -> None:
        page = max(0, min(len(self.pages) - 1, page))
        if page != self.page:
            self.page = page
            self.built_for = None
            self.items = []
            self.total = 0.0
        self.scroll = 1e9 if to_end else 0.0

    def go_section(self, delta: int) -> None:
        self.go_page(self.page + delta)

    def page_down(self, ch: float) -> None:
        """PgDn / Space: the rest of the page, then the next page."""
        if self.at_bottom():
            if self.page < len(self.pages) - 1:
                self.go_page(self.page + 1)
        else:
            self.scroll = self.clamp(self.scroll + ch - 12)

    def page_up(self, ch: float) -> None:
        if self.scroll <= 0.5:
            if self.page > 0:
                self.go_page(self.page - 1, to_end=True)
        else:
            self.scroll = self.clamp(self.scroll - (ch - 12))

    def reveal(self, block: int | None = None) -> None:
        """Shows the answer of a self-check (the first hidden one on the page by default)."""
        if block is None:
            block = next((it["check"] for it in self.items if it.get("check") is not None
                          and it["check"] not in self.revealed), None)
        if block is not None:
            self.revealed.add(block)
            self.built_for = None

    def practice(self) -> None:
        self.close()
        if self.on_practice:
            self.on_practice()

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
        if self.built_for != self.build_key(ui):
            self.build(ui)
        cx, cy, cw, ch = self.content_box()
        sections = self.sections()
        n_pages = len(self.pages)
        self.draw_header(ui, x, y, w, sections, n_pages)

        if ui.inp.wheel and ui.enabled:
            self.scroll = self.clamp(self.scroll - ui.inp.wheel * SCROLL_STEP)
        if ui.key(pygame.K_PAGEDOWN) or ui.key(pygame.K_SPACE):
            self.page_down(ch)
        if ui.key(pygame.K_PAGEUP):
            self.page_up(ch)
        if ui.key(pygame.K_HOME):
            self.go_page(0)
        if ui.key(pygame.K_END):
            self.go_page(n_pages - 1, to_end=True)
        if ui.key(pygame.K_RETURN) or ui.key(pygame.K_KP_ENTER):
            self.reveal()
        if self.built_for != self.build_key(ui):
            self.build(ui)
        for it in self.items:                       # a click on a self-check shows its answer
            if it.get("check") is not None and it["check"] not in self.revealed:
                top = cy + it["y"] - self.scroll
                vis_top, vis_bot = max(top, cy), min(top + it["h"], cy + ch)
                if vis_bot > vis_top and ui.click_in(cx + it["x"], vis_top, it["w"], vis_bot - vis_top):
                    self.reveal(it["check"])
        if self.built_for != self.build_key(ui):
            self.build(ui)
        self.draw_content(ui, cx, cy, cw, ch)
        self.draw_bar(ui, x + w - PAD + 2, cy, ch)
        self.draw_footer(ui, x, y, w, h, n_pages)

    def draw_header(self, ui, x, y, w, sections, n_pages) -> None:
        here = self.page
        dots_w = n_pages * 6
        count = T.LIB_PAGE.format(n=here + 1, t=n_pages)
        right = x + w - PAD
        ui.text(count, right, y + 12, 8, GREY, anchor="midright")
        count_w = ui.text_size(count, 8)[0]
        dx = right - count_w - 6 - dots_w
        for i in range(n_pages):
            colour = UICOL["accent"] if i == here else "#CDBF9F"
            size = 4 if i == here else 3
            ui.fill(dx + i * 6 + (4 - size) / 2, y + 12 - size / 2, size, size, colour)
        head = f"{T.MATH_FLOOR.format(n=self.doc['floor'])} · {self.doc['title_vi']}"
        ui.text(pretty(mathdraw.fit(ui, head, 7, dx - x - PAD - 8)), x + PAD, y + 12, 7, GREY, anchor="midleft")
        sec = self.current_section()
        title = sections[sec][1] if sec < len(sections) else self.doc["title_vi"]
        k, m = self.part_of_section()
        part = f" ({k}/{m})" if m > 1 else ""            # a section split into several short pages
        ui.text(pretty(mathdraw.fit(ui, title, SECTION, w - 2 * PAD - ui.text_size(part, SECTION)[0])) + part,
                x + PAD, y + 18, SECTION, UICOL["accent"])
        ui.fill(x + PAD, y + CONTENT_TOP - 4, w - 2 * PAD, 1, RULE)

    def draw_footer(self, ui, x, y, w, h, n_pages) -> None:
        here = self.page
        by = y + h - 19
        last = here == n_pages - 1
        if last and self.on_practice:
            if ui.button("doc_practice", x + PAD, by, 72, 14, T.LIB_PRACTICE, size=8, style="primary"):
                self.practice()
                return
        else:
            hint = T.LIB_KEYS if self.at_bottom() or self.total <= self.content_box()[3] else T.LIB_KEYS_SCROLL
            ui.text(hint, x + PAD, by + 7, 7, GREY, anchor="midleft")
        if ui.button("doc_prev", x + w - 176, by, 52, 14, T.LIB_PREV, size=7, enabled=here > 0, key=pygame.K_LEFT):
            self.go_section(-1)
        if ui.button("doc_next", x + w - 120, by, 52, 14, T.LIB_NEXT, size=7, enabled=not last,
                     key=pygame.K_RIGHT, style="normal" if last else "primary"):
            self.go_section(1)
        if ui.button("doc_close", x + w - 64, by, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_content(self, ui, cx, cy, cw, ch) -> None:
        wx, wy = ui.d.to_window(cx - 2, cy)
        old = ui.win.get_clip()
        ui.win.set_clip(pygame.Rect(int(wx), int(wy), int((cw + 4) * ui.s) + 1, int(ch * ui.s) + 1))
        try:
            for it in self.items:
                top = it["y"] - self.scroll
                height = it.get("h", line_h(ui, it.get("size", BODY)))
                if top + height < -2 or top > ch + 2:
                    continue
                px, py = cx + it["x"], cy + top
                kind = it["kind"]
                if kind == "text":
                    if it.get("prefix") and it["text"].startswith(it["prefix"]):
                        pre = it["prefix"]
                        ui.text(pre, px, py, it["size"], it["prefix_color"])
                        ui.text(it["text"][len(pre):], px + ui.text_size(pre, it["size"])[0], py, it["size"],
                                it["color"])
                    elif it.get("prefix"):
                        ui.text(it["text"], px, py, it["size"], it["prefix_color"])
                    else:
                        ui.text(it["text"], px, py, it["size"], it["color"])
                elif kind == "fill":
                    ui.fill(px, py, it["w"], it["h"], it["color"])
                elif kind == "box":
                    ui.fill(px, py, it["w"], it["h"], it["fill"])
                    if it.get("edge"):
                        ui.border(px, py, it["w"], it["h"], it["edge"])
                    if it.get("bar"):
                        ui.fill(px, py, 2, it["h"], it["bar"])
                elif kind == "matrices":
                    mathdraw.draw_matrices(ui, it["block"]["matrices"], px + it["w"] / 2, py, size=it["size"])
                elif kind == "figure":
                    fig, k = it["block"], it["k"]
                    figures.draw(ui, fig, px + it["dx"], py, k)
                    figures.draw_caption(ui, fig, px, py + fig["h"] * k, it["w"])
                elif kind == "formula":
                    if not mathdraw.draw_formula(ui, it["block"], px + it["w"] / 2, py):
                        ui.text(it["block"]["alt"], px + it["w"] / 2, py + height / 2, BODY, UICOL["accent"],
                                anchor="center", max_w=cw)
        finally:
            ui.win.set_clip(old)

    def draw_bar(self, ui, x: float, y: float, ch: float) -> None:
        if self.total <= ch:
            return
        ui.fill(x, y, 3, ch, "#DCD2BC")
        bar = max(10.0, ch * ch / self.total)
        ui.fill(x, y + (ch - bar) * self.scroll / max(1.0, self.total - ch), 3, bar, UICOL["accent"])

    # ------------------------------------------------------------ the layout check
    def layout_problems(self, ui) -> list[str]:
        """Everything wrong with the page as laid out now: a thing outside the content box,
        two things on top of each other, a line wider than its column, a box too small for
        its text, a figure label outside its figure or on another label."""
        if self.built_for != self.build_key(ui):
            self.build(ui)
        _, _, cw, _ = self.content_box()
        out: list[str] = []

        def name(it) -> str:
            if it["kind"] == "text":
                return repr(it["text"][:40])
            if it["kind"] == "figure":
                return f"figure {it['block']['kind']}"
            if it["kind"] == "formula":
                return f"formula {it['block'].get('alt', '')[:30]!r}"
            return it["kind"]
        tol = 0.6
        for it in self.items:
            if it["x"] < -tol or it["x"] + it["w"] > cw + tol or it["y"] < -tol:
                out.append(f"{name(it)} leaves the content box (x {it['x']:.1f}..{it['x'] + it['w']:.1f} of {cw:.0f})")
            if it["kind"] == "text" and it["w"] > it["maxw"] + tol:
                out.append(f"{name(it)} is {it['w']:.0f} wide, its column {it['maxw']:.0f}")
            if it.get("parent") is not None:
                box = self.items[it["parent"]]
                if (it["x"] < box["x"] - tol or it["x"] + it["w"] > box["x"] + box["w"] + tol
                        or it["y"] < box["y"] - tol or it["y"] + it["h"] > box["y"] + box["h"] + tol):
                    out.append(f"{name(it)} sticks out of its box")
            if it["kind"] == "formula" and it["block"].get("w"):
                b = it["block"]
                if mathdraw.image(b["key"], max(1, round(b["w"] * ui.s)), max(1, round(b["h"] * ui.s))) is None:
                    out.append(f"{name(it)}: no picture shipped ({b['key']}.png)")
            if it["kind"] == "figure":
                out += self.figure_problems(ui, it)
        fg = [it for it in self.items if it["role"] in ("fg",)]
        boxes = [it for it in self.items if it["role"] == "bg"]
        for group in (fg, boxes):
            for i, a in enumerate(group):
                for b in group[i + 1:]:
                    if _overlap((a["x"], a["y"], a["w"], a["h"]), (b["x"], b["y"], b["w"], b["h"]), tol):
                        out.append(f"{name(a)} overlaps {name(b)}")
        for it in fg:                       # a thing in no box must not run into a box
            if it.get("parent") is not None:
                continue
            for box in boxes:
                if _overlap((it["x"], it["y"], it["w"], it["h"]), (box["x"], box["y"], box["w"], box["h"]), tol):
                    out.append(f"{name(it)} runs into a box")
        return out

    def figure_problems(self, ui, it: dict) -> list[str]:
        fig, k = it["block"], it["k"]
        out = []
        fx, fy = it["x"] + it["dx"], it["y"]
        fw, fh = fig["w"] * k, fig["h"] * k
        rects = figures.text_rects(ui, fig, fx, fy, k)
        for s, (x0, y0, w, h) in rects:
            if x0 < fx - 1 or y0 < fy - 1.5 or x0 + w > fx + fw + 1 or y0 + h > fy + fh + 1.5:
                out.append(f"figure {fig['kind']}: the label {s!r} leaves the figure")
        for i, (sa, ra) in enumerate(rects):
            for sb, rb in rects[i + 1:]:
                # the font's boxes carry some empty room above and below the letters
                if _overlap((ra[0], ra[1] + ra[3] * 0.2, ra[2], ra[3] * 0.6),
                            (rb[0], rb[1] + rb[3] * 0.2, rb[2], rb[3] * 0.6), 0.3):
                    out.append(f"figure {fig['kind']}: the labels {sa!r} and {sb!r} overlap")
        cap_w = it["w"]
        for line in figures.caption_lines(ui, fig, cap_w):
            if ui.text_size(line, figures.CAPTION)[0] > cap_w + 0.6:
                out.append(f"figure {fig['kind']}: a caption line is wider than the figure: {line!r}")
        return out


def _overlap(a, b, tol: float) -> bool:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax + aw - tol > bx and bx + bw - tol > ax and ay + ah - tol > by and by + bh - tol > ay


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
