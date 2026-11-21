"""Immediate-mode interface kit. Scenes call ui.button(...), ui.text(...), ui.input_box(...)
while drawing; the kit draws at window resolution and reports clicks for this frame.

Coordinates are base pixels (480x270). Every interactive element has an id, recorded in
`ui.widgets` each frame (used for keyboard focus and by the automated test driver).

Layout audit (client/ui/audit.py): `ui.audit` is None in the game. Set it to a list and every
`ui.text`, `ui.button`, `ui.input_box` and `ui.panel` appends a record of what it drew - its
rectangle in base units, the ink box of a text, the clip rectangle in force, the button a
label belongs to - and a layout that had to shorten a text says so with `ui.note_cut`.
`audit.problems(records)` turns the records into a list of problems.

Clipping: `ui.push_clip(x, y, w, h)` / `ui.pop_clip()` limit drawing to a rectangle (nested
clips intersect); a scrolling region uses it as its safety net.

Marks: whatever the scene on top (ui.enabled) draws inside its panels is remembered for the
frame (`ui.marks`, `ui.panels`), so overlays drawn afterwards - toasts, the Thành Tựu banner -
can find a place that covers no text (`free_slot`).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from ..art.palette import UI as UICOL
from ..art.palette import rgb
from ..engine.display import Display
from ..engine.text import Fonts

INK = UICOL["ink"]
PAPER = UICOL["paper"]


@dataclass
class InputState:
    text: str = ""
    caret_t: float = 0.0
    composing: str = ""


@dataclass
class FrameInput:
    mouse: tuple[float, float] = (0, 0)
    clicked: bool = False
    right_clicked: bool = False
    wheel: int = 0
    keys: list[int] = field(default_factory=list)
    text: list[str] = field(default_factory=list)
    mouse_down: bool = False


class UI:
    def __init__(self, display: Display, fonts: Fonts):
        self.d = display
        self.f = fonts
        self.inp = FrameInput()
        self.enabled = True          # False while drawing scenes under a modal
        self.widgets: dict[str, pygame.Rect] = {}
        self.focus: str | None = None
        self.inputs: dict[str, InputState] = {}
        self._input_order: list[str] = []
        self.tooltip: tuple[str, float, float] | None = None
        self.time = 0.0
        self.hot: str | None = None
        self.sfx = None              # set by the game: callable(name)
        self.audit: list | None = None   # a list: every text / widget drawn is recorded (audit.py)
        self._clips: list[tuple[float, float, float, float]] = []
        self._owner: str | None = None   # the button whose label is being drawn
        self.marks: list[tuple[float, float, float, float]] = []    # text / widgets of the top scene
        self.panels: list[tuple[float, float, float, float]] = []   # panels of the top scene

    # ------------------------------------------------------------ frame
    @property
    def s(self) -> int:
        return self.d.scale

    @property
    def win(self) -> pygame.Surface:
        return self.d.window

    def begin(self, events: list[pygame.event.Event], dt: float) -> None:
        self.time += dt
        fi = FrameInput(mouse=self.d.to_base(pygame.mouse.get_pos()),
                        mouse_down=pygame.mouse.get_pressed()[0])
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                fi.clicked = True
                fi.mouse = self.d.to_base(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 3:
                fi.right_clicked = True
            elif e.type == pygame.MOUSEWHEEL:
                fi.wheel += e.y
            elif e.type == pygame.KEYDOWN:
                fi.keys.append(e.key)
            elif e.type == pygame.TEXTINPUT:
                fi.text.append(e.text)
            elif e.type == pygame.TEXTEDITING and self.focus in self.inputs:
                self.inputs[self.focus].composing = e.text
        self.inp = fi
        self.widgets = {}
        self._input_order = []
        self.tooltip = None
        self.hot = None
        self.marks, self.panels = [], []
        if self._clips:
            self._clips = []
            self.win.set_clip(None)

    def end(self) -> None:
        if self.tooltip:
            self._draw_tooltip(*self.tooltip)

    # ------------------------------------------------------------ input helpers
    def key(self, k: int) -> bool:
        if self.enabled and k in self.inp.keys:
            self.inp.keys.remove(k)
            return True
        return False

    def hover(self, x: float, y: float, w: float, h: float) -> bool:
        mx, my = self.inp.mouse
        return self.enabled and x <= mx < x + w and y <= my < y + h

    def click_in(self, x: float, y: float, w: float, h: float) -> bool:
        if self.enabled and self.inp.clicked and self.hover(x, y, w, h):
            self.inp.clicked = False
            return True
        return False

    def consume_click(self) -> bool:
        """A click that no widget used (e.g. clicking the world)."""
        if self.enabled and self.inp.clicked:
            self.inp.clicked = False
            return True
        return False

    # ------------------------------------------------------------ drawing
    def rect(self, x, y, w, h) -> pygame.Rect:
        return self.d.rect(x, y, w, h)

    def fill(self, x, y, w, h, color, radius: int = 0) -> None:
        c = pygame.Color(color) if isinstance(color, str) else color
        r = self.rect(x, y, w, h)
        if len(c) == 4 and c[3] < 255:
            surf = pygame.Surface(r.size, pygame.SRCALPHA)
            pygame.draw.rect(surf, c, surf.get_rect(), border_radius=radius * self.s)
            self.win.blit(surf, r.topleft)
        else:
            pygame.draw.rect(self.win, c, r, border_radius=radius * self.s)

    def border(self, x, y, w, h, color=INK, width: int = 1) -> None:
        pygame.draw.rect(self.win, pygame.Color(color), self.rect(x, y, w, h), max(1, width * self.s))

    def dim(self, alpha: int = 140) -> None:
        overlay = pygame.Surface(self.win.get_size(), pygame.SRCALPHA)
        overlay.fill((20, 18, 15, alpha))
        self.win.blit(overlay, (0, 0))

    # ------------------------------------------------------------ clipping, audit, marks
    def clip_rect(self) -> tuple[float, float, float, float] | None:
        """The clip rectangle in force (base units), or None."""
        return self._clips[-1] if self._clips else None

    def push_clip(self, x, y, w, h) -> None:
        """Draw only inside this rectangle until pop_clip (it is intersected with the clip in
        force)."""
        if self._clips:
            cx, cy, cw, ch = self._clips[-1]
            x0, y0 = max(x, cx), max(y, cy)
            x1, y1 = min(x + w, cx + cw), min(y + h, cy + ch)
            x, y, w, h = x0, y0, max(0.0, x1 - x0), max(0.0, y1 - y0)
        self._clips.append((x, y, w, h))
        self.win.set_clip(self.rect(x, y, w, h))

    def pop_clip(self) -> None:
        if self._clips:
            self._clips.pop()
        self.win.set_clip(self.rect(*self._clips[-1]) if self._clips else None)

    def note_cut(self, text: str, why: str = "cut") -> None:
        """A layout had to shorten or leave out this text (an ellipsis, a dropped row): the
        audit reports it."""
        if self.audit is not None:
            self.audit.append({"kind": why, "text": text, "clip": self.clip_rect()})

    def _record(self, kind: str, rect, **extra) -> None:
        if self.audit is not None:
            self.audit.append({"kind": kind, "rect": tuple(float(v) for v in rect), "clip": self.clip_rect(),
                               **extra})

    def _mark(self, x, y, w, h) -> None:
        if self.enabled:
            self.marks.append((x, y, w, h))

    def obstacles(self) -> list[tuple[float, float, float, float]]:
        """What an overlay must not cover this frame: the text and widgets the top scene drew
        inside its own panels or hugging their edges (a label just above a card belongs to it),
        and the panels' title boxes. (A scene with no panel - the world and its HUD - has none:
        overlays keep the place that scene gives them.)"""
        def meets(a, b) -> bool:
            return a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and a[1] < b[1] + b[3] + 16 and a[1] + a[3] > b[1] - 16
        return [m for m in self.marks if any(meets(m, p) for p in self.panels)]

    def free_slot(self, w: float, h: float, prefer: float, cx: float = 240, margin: float = 2,
                  obstacles=None) -> float | None:
        """The y (base units) of a w x h strip centred on cx that covers none of `obstacles`
        (default: `obstacles()`), nearest to `prefer`; a place outside the top scene's panels
        beats one inside them. None: there is no such place."""
        x0, x1 = cx - w / 2 - 1, cx + w / 2 + 1
        marks = self.obstacles() if obstacles is None else obstacles
        best = None
        y = margin
        while y + h <= 270 - margin:
            y0, y1 = y - 1, y + h + 1
            if not any(mx < x1 and mx + mw > x0 and my < y1 and my + mh > y0 for mx, my, mw, mh in marks):
                inside = any(px < x1 and px + pw > x0 and py < y1 and py + ph > y0 for px, py, pw, ph in self.panels)
                score = (inside, abs(y - prefer))
                if best is None or score < best[0]:
                    best = (score, y)
            y += 1
        return None if best is None else best[1]

    def panel(self, x, y, w, h, title: str | None = None, color=PAPER, edge=UICOL["panel_edge"]) -> None:
        self._record("panel", (x, y, w, h))
        if self.enabled:
            self.panels.append((x, y, w + 2, h + 2))
        self.fill(x + 2, y + 2, w, h, (0, 0, 0, 90))
        self.fill(x, y, w, h, color)
        self.border(x, y, w, h, edge, 2)
        self.border(x + 3, y + 3, w - 6, h - 6, UICOL["paper_dark"], 1)
        if title:
            tw, th = self.f.size(title, 9, self.s)
            bw = tw / self.s + 14
            self._mark(x + (w - bw) / 2, y - 6, bw, 13)
            self.fill(x + (w - bw) / 2, y - 6, bw, 13, UICOL["accent"])
            self.border(x + (w - bw) / 2, y - 6, bw, 13, INK)
            self.text(title, x + w / 2, y + 0.5, 9, "#FFFFFF", anchor="center")

    def text(self, txt: str, x: float, y: float, size: float = 8, color=INK, kind: str = "ui",
             anchor: str = "topleft", max_w: float | None = None, line_gap: float = 1.15) -> pygame.Rect:
        """Draws text; returns the occupied rect in base units."""
        lines = self.f.wrap(txt, size, int(max_w * self.s), self.s, kind) if max_w else txt.split("\n")
        surfs = [self.f.render(line, size, color, self.s, kind) for line in lines]
        lh = max((s_.get_height() for s_ in surfs), default=0) * (line_gap if len(surfs) > 1 else 1)
        total_h = lh * (len(surfs) - 1) + (surfs[-1].get_height() if surfs else 0)
        width = max((s_.get_width() for s_ in surfs), default=0)
        wx, wy = self.d.to_window(x, y)
        hx = {"topleft": "l", "midleft": "l", "bottomleft": "l", "center": "c", "midtop": "c",
              "midbottom": "c", "topright": "r", "midright": "r", "bottomright": "r"}[anchor]
        vy = {"topleft": "t", "midtop": "t", "topright": "t", "midleft": "m", "center": "m",
              "midright": "m", "bottomleft": "b", "midbottom": "b", "bottomright": "b"}[anchor]
        if hx == "c":
            wx -= width // 2
        elif hx == "r":
            wx -= width
        if vy == "m":
            wy -= int(total_h // 2)
        elif vy == "b":
            wy -= int(total_h)
        ink = None
        for i, sf in enumerate(surfs):
            lx = wx
            if hx == "c":
                lx = wx + (width - sf.get_width()) // 2
            elif hx == "r":
                lx = wx + width - sf.get_width()
            self.win.blit(sf, (lx, wy + int(i * lh)))
            if self.audit is not None:
                b = sf.get_bounding_rect()
                if b.width and b.height:
                    b.move_ip(lx, wy + int(i * lh))
                    ink = b if ink is None else ink.union(b)
        bx, by = (wx - self.d.ox) / self.s, (wy - self.d.oy) / self.s
        if self.enabled and txt.strip():
            self.marks.append((bx, by, width / self.s, total_h / self.s))
        if self.audit is not None:
            self._record("text", (bx, by, width / self.s, total_h / self.s), text=txt, size=size,
                         owner=self._owner, lines=len(lines),
                         ink=None if ink is None else ((ink.x - self.d.ox) / self.s, (ink.y - self.d.oy) / self.s,
                                                       ink.width / self.s, ink.height / self.s))
        return pygame.Rect(int(bx), int(by), int(width / self.s) + 1, int(total_h / self.s) + 1)

    def text_size(self, txt: str, size: float = 8, kind: str = "ui") -> tuple[float, float]:
        w, h = self.f.size(txt, size, self.s, kind)
        return w / self.s, h / self.s

    def image(self, surf: pygame.Surface, x: float, y: float, zoom: float = 1.0, anchor="topleft") -> None:
        """Blits a pixel-art surface scaled by (display scale x zoom) with nearest neighbour."""
        k = self.s * zoom
        w, h = int(surf.get_width() * k), int(surf.get_height() * k)
        img = pygame.transform.scale(surf, (w, h))
        wx, wy = self.d.to_window(x, y)
        if anchor == "center":
            wx, wy = wx - w // 2, wy - h // 2
        elif anchor == "midbottom":
            wx, wy = wx - w // 2, wy - h
        self.win.blit(img, (wx, wy))

    def set_tooltip(self, txt: str) -> None:
        mx, my = self.inp.mouse
        self.tooltip = (txt, mx, my)

    def _draw_tooltip(self, txt: str, mx: float, my: float) -> None:
        lines = self.f.wrap(txt, 8, 150 * self.s, self.s)
        w = max(self.text_size(l, 8)[0] for l in lines) + 8
        h = len(lines) * 10 + 5
        x = min(mx + 8, 480 - w - 2)
        y = min(my + 10, 270 - h - 2)
        self.fill(x, y, w, h, (43, 43, 43, 235))
        for i, l in enumerate(lines):
            self.text(l, x + 4, y + 2 + i * 10, 8, PAPER)

    # ------------------------------------------------------------ widgets
    def button(self, wid: str, x: float, y: float, w: float, h: float, label: str, *,
               key: int | None = None, enabled: bool = True, style: str = "normal",
               size: float = 8, kind: str = "ui", tooltip: str | None = None, selected: bool = False) -> bool:
        self.widgets[wid] = self.rect(x, y, w, h)
        hov = enabled and self.hover(x, y, w, h)
        base = {"normal": "#E3D5BA", "primary": UICOL["accent"], "gold": UICOL["gold"],
                "green": UICOL["green"], "ghost": (0, 0, 0, 0), "dark": "#3A342C"}[style]
        fg = "#FFFFFF" if style in ("primary", "green", "dark") else INK
        if selected:
            base, fg = UICOL["ink"], "#FFFFFF"
        if not enabled:
            base, fg = "#CFC6B4", "#8E877A"
        pressed = hov and self.inp.mouse_down
        oy = 1 if pressed else 0
        if style != "ghost":
            self.fill(x + 1, y + 2, w, h, (0, 0, 0, 80))
        self.fill(x, y + oy, w, h, base)
        if hov and style != "ghost":
            self.fill(x, y + oy, w, h, (255, 255, 255, 50))
        if style != "ghost":
            self.border(x, y + oy, w, h, INK)
        self._record("button", (x, y, w, h), id=wid, label=label)
        self._mark(x, y, w, h)
        self._owner = wid
        self.text(label, x + w / 2, y + h / 2 + oy, size, fg, kind=kind, anchor="center")
        self._owner = None
        if hov:
            self.hot = wid
            if tooltip:
                self.set_tooltip(tooltip)
        hit = enabled and (self.click_in(x, y, w, h) or (key is not None and self.key(key)))
        if hit and self.sfx:
            self.sfx("click")
        return hit

    def input_box(self, wid: str, x: float, y: float, w: float, h: float, placeholder: str = "",
                  password: bool = False, max_len: int = 64, kind: str = "ui") -> str:
        st = self.inputs.setdefault(wid, InputState())
        self.widgets[wid] = self.rect(x, y, w, h)
        self._input_order.append(wid)
        self._record("input", (x, y, w, h), id=wid)
        self._mark(x, y, w, h)
        if self.click_in(x, y, w, h):
            self.set_focus(wid)
        focused = self.focus == wid and self.enabled
        if focused:
            for t in self.inp.text:
                if len(st.text) + len(t) <= max_len:
                    st.text += t
            self.inp.text = []
            if pygame.K_BACKSPACE in self.inp.keys:
                self.inp.keys.remove(pygame.K_BACKSPACE)
                st.text = st.text[:-1]
            if pygame.K_v in self.inp.keys and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                self.inp.keys.remove(pygame.K_v)
                try:
                    st.text = (st.text + pygame.scrap.get_text())[:max_len]
                except (pygame.error, AttributeError):
                    pass
        self.fill(x, y, w, h, "#FFFDF7" if focused else "#F8F1E3")
        self.border(x, y, w, h, UICOL["accent"] if focused else INK)
        shown = ("•" * len(st.text)) if password else st.text
        if focused and st.composing:
            shown += st.composing
        self._owner = wid
        if shown:
            self.text(shown, x + 4, y + h / 2, 8, INK, kind=kind, anchor="midleft")
        elif placeholder:
            self.text(placeholder, x + 4, y + h / 2, 8, "#9A9387", anchor="midleft")
        self._owner = None
        if focused and int(self.time * 2) % 2 == 0:
            tw = self.text_size(shown, 8, kind)[0] if shown else 0
            cx = x + 4 + tw + 1
            self.fill(min(cx, x + w - 3), y + 3, 1, h - 6, INK)
            r = self.rect(x, y, w, h)
            try:
                pygame.key.set_text_input_rect(r)
            except (pygame.error, AttributeError):
                pass
        return st.text

    def submitted(self, wid: str) -> bool:
        """Enter pressed while this input has focus."""
        if self.focus == wid and (self.key(pygame.K_RETURN) or self.key(pygame.K_KP_ENTER)):
            return True
        return False

    def set_focus(self, wid: str | None) -> None:
        self.focus = wid
        if wid:
            pygame.key.start_text_input()

    def handle_tab(self) -> None:
        if self._input_order and self.key(pygame.K_TAB):
            if self.focus in self._input_order:
                i = (self._input_order.index(self.focus) + 1) % len(self._input_order)
            else:
                i = 0
            self.set_focus(self._input_order[i])

    def value(self, wid: str) -> str:
        return self.inputs.get(wid, InputState()).text

    def set_value(self, wid: str, text: str) -> None:
        self.inputs.setdefault(wid, InputState()).text = text

    def progress(self, x, y, w, h, frac: float, color, back="#3A342C") -> None:
        self.fill(x, y, w, h, back)
        self.fill(x, y, max(0.0, min(1.0, frac)) * w, h, color)
        self.border(x, y, w, h, INK)


def rarity_name(r: str) -> str:
    return {"common": "Thường", "rare": "Hiếm", "epic": "Sử thi", "legendary": "Huyền thoại"}.get(r, r)


def color_of(key: str):
    return rgb(key)
