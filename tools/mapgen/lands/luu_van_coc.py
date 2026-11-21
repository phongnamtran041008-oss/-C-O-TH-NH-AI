"""Lưu Vân Cốc (zone luu_van_coc)."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "luu_van_coc"


def cloud_valley() -> dict:
    """Lưu Vân Cốc (Giải Tích): a green valley crossed by one winding stream - a sine that falls
    out of a pool under the falls in the north - with a stone plateau, the highest crag of the
    valley, in the north-east. South gate -> Trúc Lâm Thôn."""
    import math as _m
    m = MapBuilder("luu_van_coc", "Lưu Vân Cốc", 60, 40, "luu_van_coc")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "grass0" if r < 0.6 else "grass1" if r < 0.88 else ("flowers1" if r > 0.97 else "grass2"))
    for y in range(1, 14):                    # the plateau: bare stone
        for x in range(38, 59):
            if (x - 49) ** 2 / 100 + (y - 7) ** 2 / 30 <= 1:
                m.setg(x, y, "stone0")
    south_gap = set(range(28, 32))
    # the trail: north from the gate, a branch west to the falls, east up to the plateau
    trail = {(x, y) for x in (29, 30) for y in range(7, H)}
    trail |= {(x, y) for x in range(24, 31) for y in (7, 8)}
    trail |= {(x, y) for x in range(31, 45) for y in (8, 9)}
    trail |= {(x, y) for x in range(6, 29) for y in (20, 21)}
    for (x, y) in trail:
        m.setg(x, y, "path0" if (x + y) % 3 else "path1")
    # the stream: x = 18 + 7 sin((y - 6) / 4.5), two tiles wide, then west out of the valley
    stream = set()
    for y in range(6, H - 6):
        cx = round(18 + 7 * _m.sin((y - 6) / 4.5))
        stream |= {(cx, y), (cx + 1, y)}
        if y > 6:
            px = round(18 + 7 * _m.sin((y - 7) / 4.5))
            for x in range(min(px, cx), max(px, cx) + 1):
                stream |= {(x, y), (x + 1, y)}
    for x in range(1, 16):
        stream |= {(x, H - 7), (x, H - 6)}
    pool = {(x, y) for x in range(17, 25) for y in range(2, 6)}
    ledge = {(20, 3), (21, 3)}                       # in the clouds above the falls
    wet = stream | pool
    for (x, y) in wet:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (x + dx, y + dy)
                if n not in wet and n not in trail and 0 < n[0] < W - 1 and 0 < n[1] < H - 1:
                    m.setg(n[0], n[1], "stone0")
    m.water(wet - ledge, stream & trail)
    for (x, y) in ledge:
        m.setg(x, y, "stone0")
    for (x, y) in trail:
        m.blocked_tiles.add((x, y))
    m.ring("pine", {("s", x) for x in south_gap})
    # the head of the stream: a boulder, and the clouds over the falls
    m.thing("Đá đầu suối", "boulder", 25, 6, 32, 24, foot=(26, 10))
    for i, (tx, ty) in enumerate(((19, 2), (22, 2), (21, 4), (18, 5))):
        m.thing("Mây", "cloud_puff", tx, ty, 32, 20, variant=i)
    # the highest crag: boulders around the top of the plateau
    for i, (tx, ty) in enumerate(((46, 5), (52, 5), (46, 9), (52, 9), (49, 3))):
        m.thing("Mỏm đá", "boulder", tx, ty, 32, 24, foot=(26, 10), variant=i)
    for i, (tx, ty) in enumerate(((42, 3), (56, 4), (40, 11), (57, 10))):
        m.thing("Mây", "cloud_puff", tx, ty, 32, 20, variant=i + 4)
    m.sign("Suối", "Suối uốn theo đường sin: khúc cong nhất là nơi đạo hàm đổi dấu", 32, 30)
    m.obj("van_xa_bac", "monster_area", 8 * T, 10 * T, 20 * T, 12 * T, monster="van_xa", count=5)
    m.obj("van_xa_nam", "monster_area", 4 * T, 22 * T, 24 * T, 9 * T, monster="van_xa", count=4)
    m.obj("phong_lang_dinh", "monster_area", 40 * T, 2 * T, 17 * T, 10 * T, monster="phong_lang", count=1)
    m.obj("phong_lang_dong", "monster_area", 38 * T, 18 * T, 16 * T, 12 * T, monster="phong_lang", count=1)
    m.reserve(26 * T, (H - 6) * T, 8 * T, 6 * T, pad=0)
    m.scatter_trees(30, "pine")
    m.scatter_trees(10, "tree")
    m.gate("s", 28, "truc_lam_thon", "from_luu_van_coc", "Cổng Nam")
    m.sign("Về Trúc Lâm Thôn", "↓ Trúc Lâm Thôn", 32, H - 4)
    m.obj("spawn", "spawn", 29 * T + 8, (H - 4) * T, 1, 1)
    m.obj("from_village", "spawn", 29 * T + 8, (H - 4) * T, 1, 1)
    # bách thú (2026-11-20): the monster areas of the thirteen new creatures
    m.obj("van_diep_dong_co", "monster_area", 448, 192, 160, 224, monster="van_diep", count=4)
    m.obj("loi_ung_cao_nguyen", "monster_area", 16, 32, 240, 112, monster="loi_ung", count=1)
    return m.build({"music": "forest", "safe": "false"})


build = cloud_valley
