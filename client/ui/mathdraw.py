"""Drawing the two kinds of maths the game shows: matrices it draws itself, and the
formula pictures built before release (tools/build_formulas.py).

A matrix is drawn here rather than shipped as a picture: it is just numbers in a box, it
stays sharp at every window size, and its numbers change from question to question.
Everything else (fractions, roots, sums) is a picture, because drawing it properly needs
a real formula renderer.
"""
from __future__ import annotations

from collections import OrderedDict

import pygame

from ..art.palette import UI as UICOL
from ..config import assets_dir

FORMULA_DIR_NAME = "formulas"
CELL_PAD = 5
ROW_H = 12
GAP = 16
MAX_CACHE = 60


def fit(ui, text: str, size: float, max_w: float) -> str:
    """The text, cut with "..." when it is wider than max_w."""
    if ui.text_size(text, size)[0] <= max_w:
        return text
    while text and ui.text_size(text + "...", size)[0] > max_w:
        text = text[:-1]
    return text.rstrip() + "..."


# ------------------------------------------------------------------ matrices
def _shapes(ui, matrices: list[dict], size: float) -> list[tuple]:
    out = []
    for mat in matrices:
        rows = [[str(v) for v in row] for row in mat.get("rows") or []]
        if not rows:
            continue
        label = f"{mat.get('name', '')} ="
        cell = max(ui.text_size(v, size)[0] for row in rows for v in row) + 2 * CELL_PAD
        out.append((label, rows, ui.text_size(label, size)[0] + 4, cell))
    return out


def matrices_size(ui, matrices: list[dict], size: float = 9) -> tuple[float, float]:
    """How much room this group of matrices needs, in base units."""
    shapes = _shapes(ui, matrices, size)
    if not shapes:
        return 0.0, 0.0
    width = sum(lw + 4 + cell * len(rows[0]) + 4 for _, rows, lw, cell in shapes) + GAP * (len(shapes) - 1)
    return width, max(len(rows) for _, rows, _, _ in shapes) * ROW_H


def draw_matrices(ui, matrices: list[dict], x: float, top: float, centered: bool = True,
                  size: float = 9) -> float:
    """Draws the matrices side by side ("A = [...]"), centred on x or starting at x.
    Returns the y just below them."""
    shapes = _shapes(ui, matrices, size)
    if not shapes:
        return top
    total, height = matrices_size(ui, matrices, size)
    cx = x - total / 2 if centered else x
    for label, rows, lw, cell in shapes:
        h = len(rows) * ROW_H
        y0 = top + (height - h) / 2
        ui.text(label, cx + lw - 2, y0 + h / 2, size, "#2B2B2B", anchor="midright")
        left, right = cx + lw + 2, cx + lw + 2 + cell * len(rows[0]) + 4
        for bx, tick in ((left, 3), (right, -3)):           # the two square brackets
            ui.fill(bx, y0, 1, h, "#2B2B2B")
            ui.fill(min(bx, bx + tick), y0, abs(tick) + 1, 1, "#2B2B2B")
            ui.fill(min(bx, bx + tick), y0 + h - 1, abs(tick) + 1, 1, "#2B2B2B")
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                ui.text(v, left + 2 + cell * c + cell / 2, y0 + r * ROW_H + ROW_H / 2, size,
                        UICOL["accent"] if v.isalpha() else "#2B2B2B", anchor="center")
        cx = right + 1 + GAP
    return top + height


# ------------------------------------------------------------------ formula pictures
_cache: OrderedDict[tuple, pygame.Surface | None] = OrderedDict()


def formula_dir():
    return assets_dir() / FORMULA_DIR_NAME


def image(key: str, px_w: int, px_h: int) -> pygame.Surface | None:
    """The picture of this formula at exactly this size, or None when it did not ship.
    Built at three times the size it is usually drawn, so it stays smooth."""
    cached = _cache.get((key, px_w, px_h))
    if cached is not None or (key, px_w, px_h) in _cache:
        _cache.move_to_end((key, px_w, px_h))
        return cached
    surf: pygame.Surface | None = None
    path = formula_dir() / f"{key}.png"
    if path.is_file() and px_w > 0 and px_h > 0:
        try:
            raw = pygame.image.load(str(path)).convert_alpha()
            surf = pygame.transform.smoothscale(raw, (px_w, px_h))
        except (pygame.error, OSError):
            surf = None
    _cache[(key, px_w, px_h)] = surf
    while len(_cache) > MAX_CACHE:
        _cache.popitem(last=False)
    return surf


def draw_formula(ui, block: dict, x: float, y: float, centered: bool = True) -> bool:
    """Draws a formula picture, x being its centre (or its left edge). False when the
    picture is missing and the caller should show block["alt"] instead."""
    w, h = float(block.get("w") or 0), float(block.get("h") or 0)
    if w <= 0 or h <= 0:
        return False
    img = image(block["key"], max(1, round(w * ui.s)), max(1, round(h * ui.s)))
    if img is None:
        return False
    wx, wy = ui.d.to_window(x, y)
    ui.win.blit(img, (wx - img.get_width() // 2 if centered else wx, wy))
    return True
