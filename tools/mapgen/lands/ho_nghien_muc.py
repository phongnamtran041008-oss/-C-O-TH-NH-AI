"""Vạn Tượng Trạch (zone ho_nghien_muc)."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "ho_nghien_muc"


def lake() -> dict:
    """Hồ Nghiên Mực: the main fishing lake (spec 7.1, 11) with Ngư Ông on his dock and a few
    Mặc Quái on the shores. East gate -> Trúc Lâm Thôn."""
    m = MapBuilder("ho_nghien_muc", "Vạn Tượng Trạch", 56, 38, "lake")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "grass0" if r < 0.55 else "grass1" if r < 0.85 else
                   ("flowers1" if r > 0.97 else "grass2"))
    east_gap = set(range(17, 21))
    water = [(14, 7, 41, 25), (10, 12, 13, 19), (42, 10, 45, 16)]   # inclusive tile rects
    dock = (27, 19, 28, 26)
    for x0, y0, x1, y1 in water:   # stone shore first, water over it
        m.fill(x0 - 1, y0 - 1, x1 + 1, y1 + 1, "stone0")
    for x0, y0, x1, y1 in water:
        m.fill(x0, y0, x1, y1, "water0")
    m.fill(dock[0], dock[1], dock[2], dock[3], "wood0")
    # Thiên Địa Đồ: the misty island in the middle of the swamp, reached on a boardwalk from the
    # dock, and the islet of the old tree in the deep west water, on a plank from the shore
    walk = {(x, y) for x in (27, 28) for y in range(15, 19)} | {(x, y) for x in (29, 30, 31) for y in (15, 16)}
    island = {(x, y) for x in range(32, 36) for y in range(13, 18)}
    islet = {(x, y) for x in (11, 12) for y in (15, 16)} | {(10, 15), (10, 16)}
    for (x, y) in walk | {(10, 15), (10, 16)}:
        m.setg(x, y, "wood0")
    for (x, y) in island | islet - {(10, 15), (10, 16)}:
        m.setg(x, y, "stone0")
    wet = set()
    for x0, y0, x1, y1 in water:
        wet |= {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
    wet -= walk | island | islet | {(x, y) for x in (27, 28) for y in range(dock[1], dock[3] + 1)}
    for y in sorted({y for _, y in wet}):     # the water is solid, row by row
        xs = sorted(x for x, yy in wet if yy == y)
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            m.solid(start * T, y * T, (prev - start + 1) * T, T)
            if x is not None:
                start = prev = x
    for i, (x0, y0, x1, y1) in enumerate(water):   # where a fishing line can go (server checks it)
        m.obj(f"lake_{i}", "area", x0 * T, y0 * T, (x1 - x0 + 1) * T, (y1 - y0 + 1) * T, kind="fishing", pool="ho")
    m.fill(29, 26, 50, 27, ["path0", "path1"])                         # shore path to the east gate
    m.fill(50, 17, W - 1, 20, ["path0", "path1", "path0"])
    m.fill(50, 21, 51, 27, ["path0", "path1"])
    m.building("Lều Ngư Ông", "hut", 18, 28, 64, 56, 30)
    m.npc("Ngư Ông", "fisher", 25, 27, action="fisher")
    m.obj("Bảng Ngư Phổ", "interact", 31 * T, 28 * T, 16, 24, sprite="tablet", action="fish_book")
    m.solid(31 * T + 2, 28 * T + 16, 12, 8)
    m.reserve(31 * T, 28 * T, 16, 24)
    for i, (tx, ty) in enumerate(((26, 26), (29, 26))):
        m.obj("lantern", "prop", tx * T + 4, ty * T - 16, 8, 24, sprite="lantern", variant=i)
    m.ring("tree", {("e", y) for y in east_gap})
    m.obj("Cổng Đông", "prop", (W - 2) * T, 17 * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", (W - 1) * T - 4, 17 * T, T + 12, 4 * T, target="truc_lam_thon",
          target_spawn="from_lake")
    m.obj("Về Trúc Lâm Thôn", "sign", 51 * T, 15 * T, 16, 20, sprite="sign", text="Trúc Lâm Thôn →")
    m.solid(51 * T + 6, 15 * T + 14, 4, 6)
    m.reserve(48 * T, 14 * T, 8 * T, 8 * T, pad=0)
    m.reserve(16 * T, 26 * T, 18 * T, 6 * T, pad=0)
    for i, (tx, ty) in enumerate(((8, 24), (47, 20), (12, 5))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
        m.blocked_tiles.add((tx, ty))
    # Mặc Quái along the shores, away from Ngư Ông's dock
    # Thiên Địa Đồ: the creatures of Xác Suất along the shores (Vạn Tượng Trạch)
    m.obj("oa_west", "monster_area", 2 * T, 22 * T, 10 * T, 12 * T, monster="dau_tu_oa", count=5)
    m.obj("ho_lo_north", "monster_area", 18 * T, 1 * T, 24 * T, 5 * T, monster="ho_lo_tinh", count=2)
    m.obj("oa_east", "monster_area", 46 * T, 26 * T, 8 * T, 9 * T, monster="dau_tu_oa", count=3)
    m.scatter_trees(34)
    swamp_spots(m)
    m.obj("spawn", "spawn", (W - 4) * T, 19 * T, 1, 1)
    m.obj("from_village", "spawn", (W - 4) * T, 19 * T, 1, 1)
    # bách thú (2026-11-20): the monster areas of the thirteen new creatures
    m.obj("u_minh_dang_bac", "monster_area", 16, 32, 144, 192, monster="u_minh_dang", count=3)
    m.obj("huyet_ngac_dam_nam", "monster_area", 448, 416, 224, 144, monster="huyet_ngac", count=1)
    return m.build({"music": "forest", "safe": "false"})


def swamp_spots(m: MapBuilder) -> None:
    """Vạn Tượng Trạch (ho_nghien_muc): the willow at the landing stage, the misty island, the
    sunken shrine on the north shore and the old tree on its islet in the deep west water."""
    m.clear(21, 25, 24, 27)
    m.tree(23, 26, "tree")                                   # the willow by Ngư Ông's dock
    m.thing("Sương", "cloud_puff", 33, 14, 32, 20, variant=0)
    m.thing("Sương", "cloud_puff", 35, 16, 32, 20, variant=1)
    m.thing("Đèn đảo", "lantern", 32, 16, 8, 24, variant=3)
    m.clear(36, 2, 40, 5)
    m.thing("Miếu Chìm", "shrine", 38, 4, 32, 44, foot=(28, 12))
    m.clear(10, 14, 13, 17)
    m.tree(12, 15, "tree")                                   # the old tree in the deep water


build = lake
