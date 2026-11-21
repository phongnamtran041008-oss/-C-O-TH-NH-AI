"""Thiên Công Phường."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "thien_cong_phuong"


def workshop() -> dict:
    """Thiên Công Phường (Lập Trình): an abandoned quarter of workshops on dirt and stone,
    plaza streets, a cold forge, a great furnace, a fenced gear yard and the yard where the
    leader of the Cơ Quan Nhân stands. East gate -> Trúc Lâm Thôn."""
    m = MapBuilder("thien_cong_phuong", "Thiên Công Phường", 56, 40, "thien_cong_phuong")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            m.setg(x, y, "dirt0" if r < 0.55 else "stone0" if r < 0.85 else "dark_grass0")
    east_gap = set(range(18, 22))
    m.fill(1, 18, W - 1, 21, ["plaza0", "plaza1"])              # the main street, from the gate
    m.fill(26, 2, 29, H - 3, ["plaza0", "plaza1"])              # the cross street
    m.fill(4, 3, 14, 8, ["stone0", "plaza1"])                   # the forge yard
    m.fill(37, 2, 48, 7, "stone0")                              # under the great furnace
    m.fill(36, 28, 50, 36, ["plaza0", "plaza1"])                # the leader's yard
    m.fill(4, 28, 16, 36, "wood0")                              # the gear yard's floor
    m.ring("ink_tree", {("e", y) for y in east_gap})
    for i, (tx, ty) in enumerate(((8, 13), (14, 13), (20, 13), (33, 13), (39, 13), (45, 13),
                                  (8, 23), (14, 23), (33, 23), (39, 23))):
        m.building("Xưởng", "house", tx, ty, 48, 48, 20, variant=i)
    # the cold forge: anvils and a dead furnace
    m.thing("Đe nguội", "anvil", 7, 5, 24, 20, foot=(20, 8))
    m.thing("Đe nguội", "anvil", 11, 5, 24, 20, foot=(20, 8))
    m.thing("Lò nguội", "furnace", 9, 3, 24, 28, foot=(18, 12))
    # the great furnace: three mouths side by side
    for tx in (41, 43, 45):
        m.thing("Lò Lớn", "furnace", tx, 4, 24, 28, foot=(20, 12))
    m.sign("Lò Lớn", "Lò Lớn: chỉ cháy lại khi đủ công lực", 39, 5)
    # the gear yard, behind its gate: a bamboo fence with one opening to the north
    for x in range(3, 18):
        if x in (9, 10, 11):
            continue
        m.obj("bamboo", "prop", x * T, 27 * T - 24, 16, 40, sprite="bamboo", variant=x + 400)
    for y in range(28, 38):
        for xx in (3, 17):
            m.obj("bamboo", "prop", xx * T, y * T - 24, 16, 40, sprite="bamboo", variant=y + 500 + xx)
    for x in range(4, 17):
        m.obj("bamboo", "prop", x * T, 37 * T - 24, 16, 40, sprite="bamboo", variant=x + 700)
    m.solid(3 * T, 27 * T, 6 * T, T)
    m.solid(12 * T, 27 * T, 6 * T, T)
    m.solid(3 * T, 27 * T, T, 11 * T)
    m.solid(17 * T, 27 * T, T, 11 * T)
    m.solid(3 * T, 37 * T, 15 * T, T)
    m.reserve(3 * T, 27 * T, 15 * T, 11 * T, pad=0)
    m.thing("Cơ Quan Cửa", "gate", 10, 27, 32, 32)
    for i, (tx, ty) in enumerate(((6, 30), (14, 30), (6, 35), (14, 35))):
        m.thing("Bánh xe gỗ", "log" if i % 2 else "stump", tx, ty, 24, 16, foot=(18, 8), variant=i)
    # the leader's yard
    for i, (tx, ty) in enumerate(((37, 29), (49, 29), (37, 35), (49, 35))):
        m.thing("Đèn", "lantern", tx, ty, 8, 24, foot=(4, 4), variant=i)
    m.thing("Giếng", "well", 27, 25, 24, 24, foot=(20, 12))
    for i, tx in enumerate((4, 12, 20, 34, 42, 50)):
        m.thing("Đèn", "lantern", tx, 17, 8, 24, foot=(4, 4), variant=i + 4)
    m.thing("Sạp bỏ hoang", "stall", 21, 23, 40, 32, foot=(36, 12), variant=0)
    m.thing("Bảng thợ", "board", 50, 23, 24, 28, foot=(20, 8))
    m.obj("co_quan_tay", "monster_area", 2 * T, 15 * T, 20 * T, 10 * T, monster="co_quan_nhan", count=4)
    m.obj("co_quan_dong", "monster_area", 32 * T, 15 * T, 18 * T, 10 * T, monster="co_quan_nhan", count=3)
    m.obj("co_quan_bac", "monster_area", 16 * T, 2 * T, 20 * T, 8 * T, monster="co_quan_nhan", count=3)
    m.obj("co_quan_dau_dan", "monster_area", 38 * T, 29 * T, 11 * T, 7 * T, monster="co_quan_nhan_dau_dan",
          count=1)
    for i, (tx, ty) in enumerate(((22, 30), (31, 33), (52, 9), (20, 6), (33, 6))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
        m.blocked_tiles.add((tx, ty))
    m.scatter_trees(12, "ink_tree")
    m.gate("e", 18, "truc_lam_thon", "from_thien_cong_phuong", "Cổng Đông")
    m.sign("Về Trúc Lâm Thôn", "Trúc Lâm Thôn →", W - 5, 16)
    m.obj("spawn", "spawn", (W - 4) * T, 20 * T, 1, 1)
    m.obj("from_village", "spawn", (W - 4) * T, 20 * T, 1, 1)
    # bách thú (2026-11-20): the monster areas of the thirteen new creatures
    m.obj("co_quan_thu_hanh_lang", "monster_area", 352, 192, 144, 208, monster="co_quan_thu", count=3)
    m.obj("lo_linh_xuong_nam", "monster_area", 304, 432, 272, 160, monster="lo_linh", count=1)
    return m.build({"music": "forest", "safe": "false"})


build = workshop
