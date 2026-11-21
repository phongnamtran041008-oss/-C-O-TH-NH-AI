"""Lôi Kiếp Đài."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "loi_kiep_dai"


def tribulation_terrace() -> dict:
    """Lôi Kiếp Đài: the arena at the end of Luyện Khí. A round stone terrace on a dark plain,
    crystals around it, Thiên Kiếp Lôi Long in the middle. South gate -> Trúc Lâm Thôn."""
    import math as _m
    m = MapBuilder("loi_kiep_dai", "Lôi Kiếp Đài", 40, 30, "loi_kiep_dai")
    W, H = m.W, m.H
    cx, cy = 20, 13
    for y in range(H):
        for x in range(W):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            r = m.rng.random()
            if d <= 7.5:
                m.setg(x, y, "realm_floor0" if (x + y) % 3 else "realm_floor1")
            elif d <= 9:
                m.setg(x, y, "plaza0" if r < 0.6 else "plaza1")
            else:
                m.setg(x, y, "ink0" if r < 0.45 else "ink1" if r < 0.85 else "dark_grass0")
    south_gap = set(range(18, 22))
    m.fill(19, 22, 20, H - 1, ["plaza0", "plaza1"])
    m.ring("ink_tree", {("s", x) for x in south_gap})
    for i in range(8):
        a = i * _m.pi / 4 + _m.pi / 8
        tx, ty = round(cx + 10.5 * _m.cos(a)), round(cy + 10.5 * _m.sin(a))
        m.thing("Lôi Tinh", "crystal", tx, ty, 24, 32, foot=(14, 8), variant=i)
    for i, ty in enumerate((24, 27)):
        for tx in (18, 21):
            m.thing("Đèn", "lantern", tx, ty, 8, 24, foot=(4, 4), variant=i * 2 + tx)
    m.sign("Lôi Kiếp Đài", "Thiên Kiếp Luyện Khí: chỉ Phản Đòn mới phá được khiên của Lôi Long", 22, 23)
    m.obj("loi_long", "monster_area", (cx - 5) * T, (cy - 5) * T, 10 * T, 10 * T, monster="loi_long", count=1)
    m.reserve((cx - 9) * T, (cy - 9) * T, 18 * T, 18 * T, pad=0)
    m.scatter_trees(10, "ink_tree")
    m.gate("s", 18, "truc_lam_thon", "from_loi_kiep_dai", "Cổng Nam")
    m.obj("spawn", "spawn", 19 * T + 8, (H - 4) * T, 1, 1)
    m.obj("from_village", "spawn", 19 * T + 8, (H - 4) * T, 1, 1)
    # bách thú (2026-11-20): the monster areas of the thirteen new creatures
    m.obj("loi_linh_tay", "monster_area", 32, 128, 96, 160, monster="loi_linh", count=1)
    m.obj("loi_linh_dong", "monster_area", 512, 128, 96, 160, monster="loi_linh", count=1)
    return m.build({"music": "forest", "safe": "false"})


build = tribulation_terrace
