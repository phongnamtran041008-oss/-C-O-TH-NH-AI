"""Kiếm Trủng Sơn (zone loan_so_coc)."""
from __future__ import annotations

import random

from ..builder import GID, T, TILESET, MapBuilder  # noqa: F401

ZONE = "loan_so_coc"


def math_valley() -> dict:
    """Loạn Số Cốc (M7): the valley where the mistakes themselves walk around. Three stretches,
    one per floor of Đại Số Tuyến Tính, so a player meets the mistakes of the floor they are on
    first. South gate -> Trúc Lâm Thôn; Lò Toán stands just inside the gate."""
    m = MapBuilder("loan_so_coc", "Kiếm Trủng Sơn", 56, 44, "loan_so_coc")
    W, H = m.W, m.H
    for y in range(H):
        for x in range(W):
            r = m.rng.random()
            # the floor is bare stone where the numbers fell apart, grass where it is still quiet
            if y < 14:
                m.setg(x, y, "stone0" if r < 0.7 else "ink1" if r < 0.9 else "dirt0")
            elif y < 29:
                m.setg(x, y, "dirt0" if r < 0.5 else "stone0" if r < 0.8 else "dark_grass0")
            else:
                m.setg(x, y, "dark_grass0" if r < 0.6 else "dark_grass1" if r < 0.93 else "dirt0")
    south_gap = set(range(26, 30))
    # the one road: it runs the length of the valley, floor 1 at the gate, floor 3 at the far end
    for y in range(2, H - 1):
        m.fill(27, y, 28, y, ["path0", "path1"], reserve=False)
    m.fill(20, 30, 35, 33, ["path0", "path1"], reserve=False)      # the clearing by the gate
    m.fill(18, 18, 37, 20, ["path0", "path1"], reserve=False)      # the middle crossing
    m.fill(16, 5, 39, 7, ["path0", "path1"], reserve=False)        # the far end
    m.ring("ink_tree", {("s", x) for x in south_gap})
    # Lò Toán: the furnace that turns what the mistakes drop into equipment (data/math/crafting.json)
    m.building("Lò Toán", "furnace", 22, 34, 24, 28, 14, otype="interact", action="math_craft")
    m.obj("Lò Toán", "sign", 20 * T, 35 * T, 16, 20, sprite="sign", text="Lò Toán")
    m.solid(20 * T + 6, 35 * T + 14, 4, 6)
    # M8: the Đạo Sĩ practising by the furnace is a character rendered out of Blender;
    # the client draws him from client/assets/chars/, and skips him when not rendered yet.
    m.obj("Đạo Sĩ Luyện Kiếm", "char", 33 * T, 34 * T, 16, 24, sheet="dao_si_truc_co", facing="down")
    m.obj("Bảng chỉ dẫn", "sign", 30 * T, 35 * T, 16, 20, sprite="sign",
          text="Tầng 1 gần cổng, tầng 3 cuối cốc")
    m.solid(30 * T + 6, 35 * T + 14, 4, 6)
    # rocks to break the sight lines
    for i, (tx, ty) in enumerate(((12, 26), (44, 24), (16, 10), (40, 9), (22, 16), (34, 38))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
        m.blocked_tiles.add((tx, ty))
    # floor 1 (tập hợp và ánh xạ): just inside the gate
    m.obj("t1_phan_tu", "monster_area", 8 * T, 29 * T, 16 * T, 11 * T, monster="dstt_phan_tu_ma", count=5)
    m.obj("t1_nghich_hieu", "monster_area", 32 * T, 29 * T, 16 * T, 11 * T,
          monster="dstt_nghich_hieu_ma", count=4)
    m.obj("t1_anh_trung", "monster_area", 20 * T, 24 * T, 14 * T, 6 * T, monster="dstt_anh_trung_ma", count=1)
    # floor 2 (số phức): the middle of the valley
    m.obj("t2_phan_ao", "monster_area", 6 * T, 15 * T, 18 * T, 10 * T, monster="dstt_phan_ao_ma", count=4)
    m.obj("t2_binh_phuong", "monster_area", 32 * T, 15 * T, 18 * T, 10 * T,
          monster="dstt_binh_phuong_ma", count=4)
    m.obj("t2_modun", "monster_area", 22 * T, 12 * T, 14 * T, 6 * T, monster="dstt_modun_ma", count=1)
    # floor 3 (vectơ và ma trận): the far end, where the stone is bare
    m.obj("t3_chi_so", "monster_area", 6 * T, 2 * T, 18 * T, 10 * T, monster="dstt_chi_so_ma", count=4)
    m.obj("t3_chuyen_vi", "monster_area", 32 * T, 2 * T, 18 * T, 10 * T, monster="dstt_chuyen_vi_ma", count=4)
    m.obj("t3_doi_xung", "monster_area", 20 * T, 2 * T, 16 * T, 6 * T, monster="dstt_doi_xung_ma", count=1)
    m.scatter_trees(34, "ink_tree")
    m.scatter_trees(12, "tree")
    sword_mountain_spots(m)
    # the way home
    m.obj("Cổng Nam", "prop", 26 * T, (H - 2) * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", 26 * T, (H - 1) * T - 2, 4 * T, T + 10, target="truc_lam_thon",
          target_spawn="from_loan_so_coc")
    m.obj("spawn", "spawn", 27 * T + 8, (H - 5) * T, 1, 1)
    m.obj("from_village", "spawn", 27 * T + 8, (H - 5) * T, 1, 1)
    # bách thú (2026-11-20): the monster areas of the thirteen new creatures
    m.obj("thiet_giap_thu_suon_dong", "monster_area", 784, 416, 96, 192, monster="thiet_giap_thu", count=3)
    m.obj("vong_hon_vach_tay", "monster_area", 16, 32, 80, 192, monster="vong_hon_kiem_si", count=1)
    return m.build({"music": "forest", "safe": "false"})


def sword_mountain_spots(m: MapBuilder) -> None:
    """Kiếm Trủng Sơn (loan_so_coc): the stone tablet at the gate, the cave behind the falls,
    the field of broken swords and the peak beyond the chasm, plus Kiếm Linh, Thạch Khôi and
    Ma Trận Thú over the old stretches of the valley."""
    m.clear(23, 38, 26, 42)
    m.thing("Bia Kiếm", "tablet", 25, 40, 16, 24, foot=(12, 8))
    m.clear(1, 15, 9, 23)
    m.fill(3, 18, 6, 19, "stone0")                         # the cave behind the falls
    m.water({(x, y) for x in range(3, 7) for y in range(20, 23)})
    for tx in (3, 6):
        m.obj("rock", "prop", tx * T, 17 * T, 16, 12, sprite="rock", variant=tx)
        m.solid(tx * T + 2, 17 * T + 4, 12, 8)
    m.obj("thach_khoi_thac", "monster_area", 2 * T, 15 * T, 12 * T, 12 * T, monster="thach_khoi", count=3)
    m.clear(38, 8, 50, 14)
    for i, (tx, ty) in enumerate(((39, 9), (41, 12), (47, 12), (49, 9))):
        m.obj("rock", "prop", tx * T, ty * T, 16, 12, sprite="rock", variant=i + 7)
        m.solid(tx * T + 2, ty * T + 4, 12, 8)
    for tx, ty in ((42, 9), (46, 9), (44, 12)):
        m.thing("Mộ kiếm", "tablet", tx, ty, 16, 24, foot=(12, 8))
    m.obj("ma_tran_bai_kiem", "monster_area", 38 * T, 8 * T, 12 * T, 6 * T, monster="ma_tran_thu", count=1)
    m.clear(46, 1, 54, 7)
    peak = {(x, y) for x in range(50, 53) for y in range(2, 4)}
    m.pit({(x, y) for x in range(48, 55) for y in range(1, 6)} - peak, "ink0")
    m.fill(50, 2, 52, 3, "stone0")
    m.obj("kiem_linh_cong", "monster_area", 8 * T, 25 * T, 40 * T, 4 * T, monster="kiem_linh", count=4)


build = math_valley
