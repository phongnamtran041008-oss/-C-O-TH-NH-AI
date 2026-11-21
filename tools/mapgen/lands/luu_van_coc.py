"""Lưu Vân Cốc (zone luu_van_coc, land luu_van_coc, branch Giải Tích): a green valley crossed by
one winding stream, a giant land of Đại Địa Đồ (320 x 240 tiles).

The stream is a curve the player walks along: it falls out of a pool under the falls in the far
north-west, swings east in one long cosine, x = 160 - 72 cos(pi (y - 6) / 112), its sharpest bend
deep in Trung Vực (where the derivative changes sign), and leaves the valley to the west near the
gate. Three tiers of tu vi climb from the gate to the north: the meadows of Ngoại Vi (tầng 1-3),
behind a ridge of pines the woods and peach hills of Trung Vực (tầng 4-6), behind a cliff of
cloud the falls, the pass of the thunder wind and the stone plateau with the highest crag
(Thâm Xứ, tầng 7-9). Everything the small map had is here: the stream, the falls and their pool
with the ledge in the clouds (Đạp Kiếm Lướt), the boulder at the head of the stream, the crag.
"""
from __future__ import annotations

import math

from ..builder import T
from ..giant import DaiDiaDo, Theme

ZONE = "luu_van_coc"
SIZE = (320, 240)

LEDGE = (90, 3)                # dao_2_ha: in the clouds above the falls (the pool is around it)
KIM_SI_DIEU = (LEDGE[0] + 1, LEDGE[1])
BRIDGE_ROCK = (145, 186)       # dao_1_ha lies in front of it, at the first bridge
DAO_1_HA = (BRIDGE_ROCK[0], BRIDGE_ROCK[1] + 1)
BEND = (229, 118)              # dao_1_trung: at the bottom of the sharpest bend
CRAG = (272, 32)               # dao_1_thuong: on top of the highest crag
BACH_HAC = (40, 108)           # Mỏm Hạc Đậu, in the pine wood


def stream_x(y: float) -> float:
    return 160 - 72 * math.cos(math.pi * (y - 6) / 112)


def g_mist(P, D, r):
    if P > 0.60:
        return "stone0"
    if P < 0.20:
        return "dark_grass0"
    return "grass1" if r < 0.6 else "grass0" if r < 0.9 else "grass2"


def g_pass(P, D, r):
    if P > 0.66:
        return "stone0"
    if P < 0.22 and D > 0.5:
        return "dirt0"
    return "dark_grass0" if r < 0.6 else "dark_grass1"


def build() -> dict:
    W, H = SIZE
    m = DaiDiaDo(ZONE, "Lưu Vân Cốc", W, H, "luu_van_coc_dai_dia_do")
    m.themes["thac_may"] = Theme("thac_may", g_mist, [("cloud", 3), ("rock", 2), ("tall_grass", 2), ("bush", 1)],
                                 [("pine", 4), ("boulder", 2), ("cloud", 2)], 0.036, 0.15, 15.0, 0.55)
    m.themes["deo_gio"] = Theme("deo_gio", g_pass, [("rock", 3), ("stump", 2), ("tall_grass", 2)],
                                [("pine", 5), ("dead_tree", 1), ("boulder", 2)], 0.036, 0.17, 15.0, 0.54)

    # ---- 1. the khu
    m.khu("lvc_bai_suoi", "Bãi Suối Hạ Lưu", 1, (0, 165, 149, 239), "bai_suoi", (70, 202),
          "Bãi cỏ hai bờ hạ lưu, nơi suối rẽ tây ra khỏi cốc. Vân Xà trườn trong cỏ.")
    m.khu("lvc_dong_co", "Đồng Cỏ Gió Nhẹ", 1, (150, 165, 319, 239), "dong_co", (232, 204),
          "Đồng cỏ hoa phía đông cửa cốc, gió nhẹ và Vân Điệp bay lượn.")
    m.khu("lvc_rung_thong", "Rừng Thông Vân Ẩn", 2, (0, 85, 119, 164), "rung_thong", (60, 126),
          "Rừng thông phía tây chìm trong mây; Bạch Hạc đậu trên mỏm đá cao giữa rừng.")
    m.khu("lvc_doi_dao", "Đồi Hoa Đào", 2, (120, 85, 199, 164), "dong_hoa", (150, 120),
          "Đồi đào giữa thung, đường lên Am Gió đi qua đây.")
    m.khu("lvc_khuc_cong", "Khúc Suối Cong", 2, (200, 85, 319, 164), "bai_suoi", (222, 120),
          "Suối uốn cong gắt nhất ở đây: tại đáy khúc cong, đạo hàm đổi dấu.")
    m.khu("lvc_thac_may", "Thác Mây Đầu Nguồn", 3, (0, 0, 139, 84), "thac_may", (98, 12),
          "Thác đổ từ mây xuống hồ đầu nguồn; giữa hồ có mỏm đá chỉ Đạp Kiếm Lướt mới tới.")
    m.khu("lvc_deo_gio", "Đèo Gió Lôi", 3, (140, 0, 219, 84), "deo_gio", (186, 32),
          "Đèo cao gió lôi rít qua rặng thông đen, Lôi Ưng lượn trên đầu.")
    m.khu("lvc_cao_nguyen", "Cao Nguyên Đá Mây", 3, (220, 0, 319, 84), "cao_nguyen", (262, 46),
          "Cao nguyên đá trên mây, mỏm cao nhất thung lũng: điểm cực đại.")

    # ---- 2. the ground, the camps
    m.paint(warp=7.0, scale=26.0)
    m.camp("lvc_leu_cua_coc", "Lều Cửa Cốc", (151, 224), r=7,
           desc_vi="Lều nghỉ ngay trong cổng cốc. Không có quái.", label_vi="Lều Cửa Cốc")
    m.camp("lvc_tram_giua", "Trạm Mây Giữa", (156, 156), r=6,
           desc_vi="Trạm nghỉ sau rặng thông, cửa vào Trung Vực.", label_vi="Trạm Mây Giữa · cửa Trung Vực")
    m.camp("lvc_am_gio", "Am Gió", (196, 62), r=6,
           desc_vi="Am nhỏ trên đèo, bên kia vách mây: cửa vào Thâm Xứ.", label_vi="Am Gió · cửa Thâm Xứ")
    m.clear_zones.append((146, 228, 157, 239))           # the gate and the spawn

    # ---- 3. the stream, its pool, the tarns
    falls(m)
    pts = [(stream_x(y), y) for y in range(6, 231)]
    pts += [(88 - i, 230 + round(1.5 * math.sin(i / 9))) for i in range(1, 88)]
    m.river(pts, width=3)
    m.lake(282, 196, 8, 5)                                # Hồ Gương, in the eastern meadow
    m.lake(36, 52, 7, 4)                                  # a tarn in the mist
    keep_landmarks(m)

    # ---- 4. the walls between the tiers
    pines, cliff = "pines", "cliff"
    m.barriers({
        ("lvc_bai_suoi", "lvc_rung_thong"): pines, ("lvc_bai_suoi", "lvc_doi_dao"): pines,
        ("lvc_dong_co", "lvc_doi_dao"): pines, ("lvc_dong_co", "lvc_khuc_cong"): pines,
        ("lvc_bai_suoi", "lvc_dong_co"): "trees",
        ("lvc_rung_thong", "lvc_doi_dao"): "trees", ("lvc_doi_dao", "lvc_khuc_cong"): "trees",
        ("lvc_rung_thong", "lvc_thac_may"): cliff, ("lvc_doi_dao", "lvc_thac_may"): cliff,
        ("lvc_doi_dao", "lvc_deo_gio"): cliff, ("lvc_khuc_cong", "lvc_deo_gio"): cliff,
        ("lvc_khuc_cong", "lvc_cao_nguyen"): cliff, ("lvc_doi_dao", "lvc_cao_nguyen"): cliff,
        ("lvc_rung_thong", "lvc_deo_gio"): cliff,
        ("lvc_thac_may", "lvc_deo_gio"): cliff, ("lvc_deo_gio", "lvc_cao_nguyen"): cliff,
    })

    # ---- 5. the roads
    m.node("gate", (151, 234), "Cổng Nam · về Trúc Lâm Thôn")
    m.node("n_cau", (148, 189), "Cầu Đầu Suối")
    m.node("n_bai_suoi", (70, 202), "Bãi Suối Hạ Lưu · Ngoại Vi, tầng 1-3")
    m.node("n_dong_co", (232, 204), "Đồng Cỏ Gió Nhẹ · Ngoại Vi, tầng 1-3")
    m.node("n_rung_thong", (60, 126), "Rừng Thông Vân Ẩn · Trung Vực, tầng 4-6")
    m.node("n_hac", (BACH_HAC[0] + 6, BACH_HAC[1] + 4), "Mỏm Hạc Đậu", sign=False)
    m.node("n_doi_dao", (150, 120), "Đồi Hoa Đào · Trung Vực, tầng 4-6")
    m.node("n_khuc_cong", (222, 120), "Khúc Suối Cong · Trung Vực, tầng 4-6")
    m.node("n_bo_dong", (276, 128), "Bờ Đông Khúc Suối")
    m.node("n_deo_gio", (186, 32), "Đèo Gió Lôi · Thâm Xứ, tầng 7-9")
    m.node("n_thac", (98, 12), "Thác Mây Đầu Nguồn · Thâm Xứ, tầng 7-9")
    m.node("n_suong", (60, 60), "Đồng Sương", sign=False)
    m.node("n_cao_nguyen", (262, 46), "Cao Nguyên Đá Mây · Thâm Xứ, tầng 7-9")
    m.node("n_crag", (CRAG[0], CRAG[1] + 4), "Mỏm cao nhất", sign=False)
    m.network([
        ("gate", "lvc_leu_cua_coc", "main"),
        ("lvc_leu_cua_coc", "n_cau", "main"),
        ("lvc_leu_cua_coc", "n_dong_co", "main"),
        ("lvc_leu_cua_coc", "n_bai_suoi", "main"),
        ("n_cau", "lvc_tram_giua", "main"),
        ("n_bai_suoi", "n_rung_thong", "trail"),
        ("n_dong_co", "n_bo_dong", "trail"),
        ("lvc_tram_giua", "n_rung_thong", "main"),
        ("lvc_tram_giua", "n_doi_dao", "main"),
        ("lvc_tram_giua", "n_khuc_cong", "main"),
        ("n_khuc_cong", "n_bo_dong", "trail"),
        ("n_rung_thong", "n_hac", "trail"),
        ("n_doi_dao", "lvc_am_gio", "main"),
        ("n_rung_thong", "n_suong", "trail"),
        ("lvc_am_gio", "n_deo_gio", "main"),
        ("n_deo_gio", "n_thac", "main"),
        ("lvc_am_gio", "n_cao_nguyen", "main"),
        ("n_cao_nguyen", "n_crag", "trail"),
        ("n_suong", "n_thac", "trail"),
    ])
    m.carve([(151, y) for y in range(228, H - 1)], "main")      # through the gate

    # ---- 6. the places
    landmarks(m)
    m.signposts()

    # ---- 8. the monsters
    monsters(m)

    # ---- 9, 10
    m.dress_barriers()
    m.scatter()
    m.gate("s", 150, "truc_lam_thon", "from_luu_van_coc", "Cổng Nam")
    m.sign("Về Trúc Lâm Thôn", "Nam → Trúc Lâm Thôn", 154, H - 4)
    m.poi("gate", "Cổng Nam · về Trúc Lâm Thôn", 151, H - 2)
    m.obj("spawn", "spawn", 151 * T + 8, (H - 4) * T, 1, 1)
    m.obj("from_village", "spawn", 151 * T + 8, (H - 4) * T, 1, 1)
    return m.finish({"music": "forest", "safe": "false"}, ring="pine",
                    gaps={("s", x) for x in range(150, 154)})


def falls(m: DaiDiaDo) -> None:
    """The pool under the falls against the north edge, with the ledge in the clouds in its middle:
    the stream leaves the pool at its south-west corner; the stone shore south of the ledge is
    where a glide starts."""
    px, py = LEDGE
    pool = {(x, y) for x in range(px - 3, px + 5) for y in range(py - 1, py + 3)}
    ledge = {(px, py), (px + 1, py)}
    m._wet(pool - ledge, "water0", 1, "stone0")
    m.open_tiles(ledge, "stone0")
    m.keep_rect(px - 5, py - 1, px + 7, py + 5)


def keep_landmarks(m: DaiDiaDo) -> None:
    cx, cy = CRAG
    m.keep_rect(cx - 5, cy - 5, cx + 5, cy + 3)
    hx, hy = BACH_HAC
    m.keep_rect(hx - 3, hy - 3, hx + 3, hy + 2)
    bx, by = BEND
    m.keep_rect(bx - 4, by - 3, bx, by + 3)


def landmarks(m: DaiDiaDo) -> None:
    px, py = LEDGE
    m.thing("Đá đầu suối", "boulder", px + 5, py + 3, 32, 24, foot=(26, 10))
    for i, (dx, dy) in enumerate(((-1, -1), (2, -1), (1, 1), (-2, 2))):
        m.thing("Mây", "cloud_puff", px + dx, py + dy, 32, 20, variant=i)
    m.poi("landmark", "Thác Mây · hồ đầu nguồn", px, py)
    m.poi("beast", "Kim Sí Điểu", *KIM_SI_DIEU)
    m.sign("Hồ đầu nguồn", "Mỏm đá giữa hồ chỉ Đạp Kiếm Lướt mới tới.", px + 3, py + 4)
    # the first bridge: the rock at its south head
    m.thing("Đá đầu cầu", "boulder", *BRIDGE_ROCK, 32, 24, foot=(26, 10))
    m.poi("landmark", "Cầu Đầu Suối", 148, 181)
    # the sharpest bend
    bx, by = BEND
    m.sign("Suối", "Suối uốn theo đường cos: khúc cong nhất là nơi đạo hàm đổi dấu.", bx - 3, by - 2)
    m.thing("Đá đáy khúc", "rock", bx - 1, by + 2, 16, 12, foot=(12, 8))
    m.poi("landmark", "Đáy Khúc Suối Cong", bx, by)
    # the highest crag: boulders around its top
    cx, cy = CRAG
    for i, (dx, dy) in enumerate(((-3, -2), (3, -2), (-3, 2), (3, 2), (0, -4))):
        m.thing("Mỏm đá", "boulder", cx + dx, cy + dy, 32, 24, foot=(26, 10), variant=i)
    for i, (dx, dy) in enumerate(((-5, -4), (5, -3), (-5, 1), (5, 2))):
        m.thing("Mây", "cloud_puff", cx + dx, cy + dy, 32, 20, variant=i + 4)
    m.poi("landmark", "Mỏm Cao Nhất", cx, cy)
    # Mỏm Hạc Đậu, where Bạch Hạc perches
    hx, hy = BACH_HAC
    for i, (dx, dy) in enumerate(((-3, -1), (3, -1), (0, -3))):
        m.thing("Mỏm đá", "boulder", hx + dx, hy + dy, 32, 24, foot=(26, 10), variant=i + 6)
    m.poi("beast", "Mỏm Hạc Đậu · Bạch Hạc", hx, hy)
    m.poi("landmark", "Hồ Gương", 282, 196)


def monsters(m: DaiDiaDo) -> None:
    """Band 1: Vân Xà and Vân Điệp (the low stages); band 2: the same with their higher nodes and
    a few elites; band 3: only the elites (the land has no normal creature of tầng 7-9), one per
    area, a handful per khu."""
    m.monsters("lvc_bai_suoi", [("van_xa", 3), ("van_diep", 2)], tiles_per=210)
    m.monsters("lvc_dong_co", [("van_xa", 2), ("van_diep", 2)], tiles_per=210)
    m.monsters("lvc_rung_thong", [("van_xa", 2), ("van_diep", 2)], [("phong_lang", 2), ("loi_ung", 1)],
               tiles_per=210)
    m.monsters("lvc_doi_dao", [("van_diep", 2), ("van_xa", 1)], [("loi_ung", 2), ("phong_lang", 1)], tiles_per=210)
    m.monsters("lvc_khuc_cong", [("van_xa", 2), ("van_diep", 2)], [("loi_ung", 2), ("phong_lang", 2)],
               tiles_per=210)
    for kid, n in (("lvc_thac_may", 7), ("lvc_deo_gio", 6), ("lvc_cao_nguyen", 7)):
        m.monsters(kid, [("phong_lang", 1), ("loi_ung", 1)], cell=(16, 14), tiles_per=1e9, max_areas=n)
