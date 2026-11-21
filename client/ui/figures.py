"""Draws the figures of Tàng Thư Các (the diagrams of a lesson card).

The server lays every figure out (server/app/learning/math_figures.py) and sends a list of
primitives in base units: lines, arrows, polylines, filled shapes, rectangles, circles,
rows of shading and text. This module only draws them, at window resolution so a figure
stays crisp at every window scale, and knows nothing about planes, Venn diagrams or tables:
a new kind of figure needs no change here.

Colours arrive as Vietnamese names and become the game palette. A fill comes with `a`, how
strong its tint is: the colour is mixed with the paper it sits on, so figures never need
real transparency and overlapping shapes stay readable.
"""
from __future__ import annotations

import math

import pygame

from ..art.palette import UI as UICOL
from ..art.palette import rgb
from .mathtext import pretty

COLOURS = {
    "do": UICOL["accent"],      # vermilion
    "xanh": UICOL["blue"],
    "luc": UICOL["green"],
    "vang": "#C99A3A",          # the darker gold: gold itself is too pale for lines on paper
    "tim": "#8E5AC8",
    "xam": "#8C8C8C",
    "muc": UICOL["ink"],
    "giay": UICOL["paper"],
}
PAPER = UICOL["paper"]
CAPTION = 7
CAPTION_COLOUR = "#5A5A5A"
DASH = 3.0                      # base units of a dash, and of the gap after it


def colour(name: str | None, a: int = 255, paper: str = PAPER) -> tuple[int, int, int]:
    """A palette colour by name, mixed with the paper when a < 255."""
    base = rgb(COLOURS.get(name or "muc", name or COLOURS["muc"]))
    if a >= 255:
        return base
    p = rgb(paper)
    k = max(0, a) / 255
    return tuple(round(p[i] + (base[i] - p[i]) * k) for i in range(3))


def caption_lines(ui, fig: dict, width: float) -> list[str]:
    return ui.f.wrap(pretty(fig.get("caption", "")), CAPTION, int(width * ui.s), ui.s) if fig.get("caption") else []


def caption_h(ui, fig: dict, width: float) -> float:
    lines = caption_lines(ui, fig, width)
    return len(lines) * ui.text_size("Ag", CAPTION)[1] * 1.1 + (3 if lines else 0)


def scale_for(fig: dict, width: float) -> float:
    """How much a figure must shrink to fit `width` (1.0: it fits)."""
    return min(1.0, width / fig["w"]) if fig.get("w") else 1.0


def size(ui, fig: dict, width: float) -> tuple[float, float, float]:
    """(w, h, k): the room the figure and its caption take in a column `width` wide, and
    the factor the drawing is shrunk by."""
    k = scale_for(fig, width)
    w = fig["w"] * k
    cap_w = max(w, min(width, 160.0))
    return w, fig["h"] * k + caption_h(ui, fig, cap_w), k


class _Pen:
    """Base units (relative to the figure, times k) to window pixels."""

    def __init__(self, ui, x: float, y: float, k: float):
        self.ui, self.k = ui, k
        self.ox, self.oy = ui.d.to_window(x, y)
        self.s = ui.s * k

    def p(self, x: float, y: float) -> tuple[float, float]:
        return self.ox + x * self.s, self.oy + y * self.s

    def w(self, wd: float) -> int:
        return max(1, round(wd * self.s))


def _dashed(surf, c, a, b, width: int, step: float) -> None:
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    if d < 1:
        return
    n = int(d // (2 * step)) + 1
    for i in range(n):
        t0, t1 = (2 * i * step) / d, min(1.0, (2 * i + 1) * step / d)
        if t0 >= 1:
            break
        pygame.draw.line(surf, c, (x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0),
                         (x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1), width)


def _line(surf, c, a, b, width: int) -> None:
    if width <= 1:
        pygame.draw.aaline(surf, c, a, b)
    else:
        pygame.draw.line(surf, c, a, b, width)


def _polyline(surf, c, pts, width: int, dash: float = 0) -> None:
    if len(pts) < 2:
        return
    if dash:
        for a, b in zip(pts, pts[1:]):
            _dashed(surf, c, a, b, width, dash)
        return
    if width <= 1:
        pygame.draw.aalines(surf, c, False, pts)
        return
    pygame.draw.lines(surf, c, False, pts, width)
    r = width / 2
    if width >= 3:          # round joints: thick pygame lines leave notches at the bends
        for q in pts[1:-1]:
            pygame.draw.circle(surf, c, q, r)


def _head(surf, c, a, b, length: float, half: float) -> None:
    (x1, y1), (x2, y2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    if d < 1e-6:
        return
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    bx, by = x2 - ux * length, y2 - uy * length
    pts = [(x2, y2), (bx - uy * half, by + ux * half), (bx + uy * half, by - ux * half)]
    pygame.draw.polygon(surf, c, pts)
    pygame.draw.aalines(surf, c, True, pts)


def draw(ui, fig: dict, x: float, y: float, k: float = 1.0) -> None:
    """Draws the figure with its top-left corner at (x, y) in base units, shrunk by k.
    The caption is not drawn here (see draw_caption)."""
    pen = _Pen(ui, x, y, k)
    surf = ui.win
    for p in fig.get("prims", []):
        t = p["t"]
        if t == "text":
            ui.text(pretty(p["s"]), x + p["x"] * k, y + p["y"] * k, p["size"] * k, colour(p.get("c")),
                    anchor=p.get("anchor", "center"))
            continue
        c = colour(p.get("c"), p.get("a", 255))
        if t in ("line", "arrow"):
            a, b = pen.p(p["x1"], p["y1"]), pen.p(p["x2"], p["y2"])
            width = pen.w(p.get("wd", 1.0))
            if t == "arrow":
                head = p.get("head", 4.5) * pen.s
                d = math.hypot(b[0] - a[0], b[1] - a[1])
                if d > head:      # the shaft stops at the base of the head, so the tip stays sharp
                    b_shaft = (b[0] - (b[0] - a[0]) / d * head * 0.8, b[1] - (b[1] - a[1]) / d * head * 0.8)
                else:
                    b_shaft = a
                if p.get("dash"):
                    _dashed(surf, c, a, b_shaft, width, DASH * pen.s)
                else:
                    _line(surf, c, a, b_shaft, width)
                _head(surf, c, a, b, head, head * 0.42 + width * 0.3)
            elif p.get("dash"):
                _dashed(surf, c, a, b, width, DASH * pen.s)
            else:
                _line(surf, c, a, b, width)
        elif t == "polyline":
            _polyline(surf, c, [pen.p(*q) for q in p["pts"]], pen.w(p.get("wd", 1.0)),
                      DASH * pen.s if p.get("dash") else 0)
        elif t == "poly":
            pts = [pen.p(*q) for q in p["pts"]]
            pygame.draw.polygon(surf, colour(p.get("fill"), p.get("a", 80)), pts)
            if p.get("edge"):
                pygame.draw.aalines(surf, colour(p["edge"]), True, pts)
        elif t == "rect":
            x0, y0 = pen.p(p["x"], p["y"])
            x1, y1 = pen.p(p["x"] + p["w"], p["y"] + p["h"])
            r = pygame.Rect(round(x0), round(y0), max(1, round(x1) - round(x0)), max(1, round(y1) - round(y0)))
            radius = round(p.get("r", 0) * pen.s)
            if p.get("fill") and p.get("a", 255) > 0:
                pygame.draw.rect(surf, colour(p["fill"], p.get("a", 255)), r, border_radius=radius)
            if p.get("edge"):
                pygame.draw.rect(surf, colour(p["edge"]), r, pen.w(p.get("wd", 0.7)), border_radius=radius)
        elif t == "circle":
            cx, cy = pen.p(p["x"], p["y"])
            rad = p["r"] * pen.s
            if p.get("fill") and p.get("a", 255) > 0:
                pygame.draw.circle(surf, colour(p["fill"], p.get("a", 255)), (cx, cy), rad)
            if p.get("edge"):
                pygame.draw.circle(surf, colour(p["edge"]), (cx, cy), rad, pen.w(p.get("wd", 1.0)))
        elif t == "spans":
            y_top = p["y"]
            for i, row in enumerate(p["rows"]):
                ya = round(pen.p(0, y_top + i * p["dy"])[1])
                yb = round(pen.p(0, y_top + (i + 1) * p["dy"])[1])
                for xa, xb in zip(row[::2], row[1::2]):
                    wa, wb = round(pen.p(xa, 0)[0]), round(pen.p(xb, 0)[0])
                    if wb > wa and yb > ya:
                        surf.fill(c, pygame.Rect(wa, ya, wb - wa, yb - ya))


def draw_caption(ui, fig: dict, x: float, y: float, width: float) -> float:
    """The caption, centred under a figure in a column `width` wide from x. Returns its height."""
    lh = ui.text_size("Ag", CAPTION)[1] * 1.1
    lines = caption_lines(ui, fig, width)
    for i, line in enumerate(lines):
        ui.text(line, x + width / 2, y + 2 + i * lh, CAPTION, CAPTION_COLOUR, anchor="midtop")
    return len(lines) * lh + (3 if lines else 0)


def text_rects(ui, fig: dict, x: float, y: float, k: float = 1.0) -> list[tuple[str, pygame.Rect]]:
    """The real rectangle (base units, as floats in a Rect of tenths) every label covers.
    Used by the reader's layout check: labels must stay inside the figure and apart."""
    out = []
    for p in fig.get("prims", []):
        if p["t"] != "text":
            continue
        w, h = ui.text_size(pretty(p["s"]), p["size"] * k)
        a = p.get("anchor", "center")
        px, py = x + p["x"] * k, y + p["y"] * k
        x0 = px - (w / 2 if a in ("center", "midtop", "midbottom") else w if a.endswith("right") else 0)
        y0 = py - (h / 2 if a in ("center", "midleft", "midright") else h if a.startswith("bottom") else 0)
        out.append((p["s"], (x0, y0, w, h)))
    return out
