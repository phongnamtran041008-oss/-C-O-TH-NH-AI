"""Lôi Kiếp Đài (zone loi_kiep_dai, kind boss): the terrace where Luyện Khí ends, 120 x 90 tiles.

The end of a pilgrimage, not a wild land: from the south gate a pilgrims' camp, then a long stair
of stone up a ridge of storm-scarred rock between two abysses of cloud and ink, through two gates,
to the round terrace on the summit where Thiên Kiếp Lôi Long waits; on two small platforms either
side of it, joined by stone bridges, the two Lôi Linh hover and never attack first.

The map has no khu and no bands (docs/DAI_DIA_DO.md, rule 4: the boss arena has no bands): its
three monster areas keep their names and behave exactly as on the small map - `loi_long` in the
middle of the terrace, `loi_linh_tay` and `loi_linh_dong` beyond the boss's reach on either side.
The giant-land toolkit paints it; finish_unbanded() writes no khu.
"""
from __future__ import annotations

import math

from ..builder import T
from ..giant import DaiDiaDo, Theme
from . import _xay_dung as X

ZONE = "loi_kiep_dai"
SIZE = (120, 90)

DAI = (60, 20)                   # the centre of the terrace (Thiên Kiếp Lôi Long; cung_2 drops here)
CUNG_2_HA = DAI
LOI_LINH = ((37, 19), (83, 19))  # the two platforms of the Lôi Linh
GATE_X = 58                      # the south gate covers tiles 58..61 of the south edge
CAMP = (60, 78)
STAIR = (36, 70)                 # the stair climbs from y 70 to y 36


def g_slope(P, D, r):            # storm-scarred rock: stone, scorched patches, a little turf
    if P < 0.26:
        return "dark_grass1" if r < 0.8 else "dark_grass0"
    if P > 0.7 and D > 0.45:
        return "dirt0"
    return "stone0"


def g_peak(P, D, r):
    if P > 0.68:
        return "dirt0"
    return "stone0"


def build() -> dict:
    W, H = SIZE
    m = DaiDiaDo(ZONE, "Lôi Kiếp Đài", W, H, "loi_kiep_dai_dai_dia_do")
    m.themes["soi_set"] = Theme("soi_set", g_slope, [("rock", 3), ("dead_tree", 2), ("crystal", 1), ("boulder", 1)],
                                [("dead_tree", 4), ("boulder", 2), ("crystal", 1)], 0.05, 0.16, 12.0, 0.58)
    m.themes["dinh_set"] = Theme("dinh_set", g_peak, [("rock", 3), ("crystal", 2), ("cloud", 1)],
                                 [("boulder", 3), ("crystal", 2)], 0.04, 0.12, 12.0, 0.6)
    # the two grounds (painting only: finish_unbanded writes no khu)
    m.khu("lkd_suon", "Sườn Sét", 3, (0, 34, W - 1, H - 1), "soi_set", (CAMP[0], CAMP[1] - 8))
    m.khu("lkd_dinh", "Đỉnh Lôi Kiếp", 3, (0, 0, W - 1, 33), "dinh_set", DAI)
    m.paint(warp=3.0, scale=20.0)
    m.camp("lkd_trai", "Trại Hành Hương", CAMP, r=6,
           desc_vi="Trại của người hành hương dưới chân đài.", label_vi="Trại Hành Hương")

    # ---- the ridge between two abysses, the terrace, the platforms
    ridge(m)
    terrace(m)
    stair(m)

    # ---- the roads
    m.node("gate", (GATE_X + 2, H - 4), "Cổng Nam · về Trúc Lâm Thôn")
    m.node("n_chan", (60, STAIR[1] + 1), "Thang Lôi Kiếp · lên đài", sign=False)
    m.node("n_dai", (60, 33), "Lôi Kiếp Đài", sign=False)
    m.node("n_tay", (LOI_LINH[0][0], LOI_LINH[0][1] + 3), "Đài Lôi Linh Tây", sign=False)
    m.node("n_dong", (LOI_LINH[1][0], LOI_LINH[1][1] + 3), "Đài Lôi Linh Đông", sign=False)
    m.node("n_cau_tay", (48, 22), "Cầu Đá Tây", sign=False)
    m.node("n_cau_dong", (72, 22), "Cầu Đá Đông", sign=False)
    m.network([
        ("gate", "lkd_trai", "main"),
        ("lkd_trai", "n_chan", "main"),
        ("n_chan", "n_dai", "main"),
        ("n_cau_tay", "n_tay", "trail", True),
        ("n_cau_dong", "n_dong", "trail", True),
    ])
    m.carve([(GATE_X + 2, y) for y in range(H - 8, H - 1)], "main")      # through the gate

    # ---- the places
    places(m)
    m.signposts()
    monster_areas(m)

    m.dress_barriers()
    m.scatter()
    clouds(m)
    m.gate("s", GATE_X, "truc_lam_thon", "from_loi_kiep_dai", "Cổng Nam")
    m.sign("Về Trúc Lâm Thôn", "Nam → Trúc Lâm Thôn", GATE_X + 4, H - 4)
    m.poi("gate", "Cổng Nam · về Trúc Lâm Thôn", GATE_X + 2, H - 2)
    m.obj("spawn", "spawn", (GATE_X + 1) * T + 8, (H - 4) * T, 1, 1)
    m.obj("from_village", "spawn", (GATE_X + 1) * T + 8, (H - 4) * T, 1, 1)
    return X.finish_unbanded(m, {"music": "forest", "safe": "false"}, ring="ink_tree",
                             gaps={("s", x) for x in range(GATE_X, GATE_X + 4)})


# ------------------------------------------------------------------ the shape of the mountain
def ridge_half_width(y: float, m: DaiDiaDo) -> float:
    """Half the width of the walkable ridge at row y: wide at the camp, narrow along the stair,
    with a ragged edge."""
    if y >= 66:
        base = 26.0 - (90 - y) * 0.2
    elif y >= 36:
        base = 9.0 + (y - 36) * 0.12
    else:
        base = 7.0
    return base + (m.noise.fbm(0.0, y, 6.0, 2, 51) - 0.5) * 6.0


def ridge(m: DaiDiaDo) -> None:
    """The abyss of cloud and ink on both sides of the ridge (solid), the ridge itself left as
    painted; the summit is cut out by terrace()."""
    pit = set()
    for y in range(1, m.H - 1):
        hw = ridge_half_width(y, m)
        for x in range(1, m.W - 1):
            off = (m.noise.fbm(x, y, 5.0, 2, 52) - 0.5) * 3.0
            if abs(x - 60) > hw + off and y >= 34:
                pit.add((x, y))
            elif y < 34:
                pit.add((x, y))
    m.chasm({t for t in pit if not m.keep[m.i(*t)]})


def terrace(m: DaiDiaDo) -> None:
    """The summit: the round terrace (realm floor in a ring of paving), the two platforms of the
    Lôi Linh, and the shoulder that joins the terrace to the top of the stair."""
    cx, cy = DAI
    top = set()
    for y in range(1, 36):
        for x in range(1, m.W - 1):
            d = math.hypot(x - cx, (y - cy) * 1.1)
            if d <= 13.5 + (m.noise.fbm(x, y, 4.0, 2, 53) - 0.5) * 1.5:
                top.add((x, y))
            elif 30 <= y <= 35 and abs(x - cx) <= 7:
                top.add((x, y))
            for (px, py) in LOI_LINH:
                if math.hypot(x - px, (y - py) * 1.1) <= 5.5 + (m.noise.fbm(x, y, 4.0, 2, 54) - 0.5) * 1.0:
                    top.add((x, y))
    m.open_tiles(top)
    for (x, y) in top:
        d = math.hypot(x - cx, (y - cy) * 1.1)
        m.setg(x, y, "dirt0" if m.noise.fbm(x, y, 5.0, 2, 57) > 0.66 else "stone0")
        if d <= 9.5:
            m.setg(x, y, "realm_floor0" if (x + y) % 3 else "realm_floor1")
        elif d <= 11.5:
            m.setg(x, y, "plaza0" if (x + y) % 2 else "plaza1")
        elif any(math.hypot(x - px, (y - py) * 1.1) <= 3.5 for (px, py) in LOI_LINH):
            m.setg(x, y, "plaza0" if (x + y) % 2 else "plaza1")
    m.keep_rect(cx - 12, cy - 11, cx + 12, cy + 11)
    for (px, py) in LOI_LINH:
        m.keep_rect(px - 4, py - 4, px + 4, py + 4)


def stair(m: DaiDiaDo) -> None:
    """Thang Lôi Kiếp: five tiles of steps from the camp to the summit, a darker tread every
    third row."""
    y_top, y_bottom = STAIR
    tiles = [(x, y) for y in range(y_top, y_bottom + 1) for x in range(58, 63)]
    X.lane(m, tiles, "plaza0")
    for (x, y) in tiles:
        if y % 3 == 0:
            m.setg(x, y, "stone0")
        elif x in (58, 62):
            m.setg(x, y, "plaza1")
    m.keep_rect(56, y_top, 64, y_bottom)


# ------------------------------------------------------------------ the places
def places(m: DaiDiaDo) -> None:
    cx, cy = DAI
    # the eight Lôi Tinh round the terrace (the small map had them at 10.5 tiles)
    for i in range(8):
        a = i * math.pi / 4 + math.pi / 8
        m.thing("Lôi Tinh", "crystal", round(cx + 12.5 * math.cos(a)), round(cy + 11 * math.sin(a)), 24, 32,
                foot=(14, 8), variant=i)
    m.sign("Lôi Kiếp Đài", "Thiên Kiếp Luyện Khí: chỉ Phản Đòn mới phá được khiên của Lôi Long", 63, 33)
    m.poi("boss", "Lôi Kiếp Đài · Thiên Kiếp Lôi Long", cx, cy)
    for name, (px, py) in zip(("Đài Lôi Linh Tây", "Đài Lôi Linh Đông"), LOI_LINH):
        for i, (dx, dy) in enumerate(((-3, -3), (3, -3), (-3, 3), (3, 3))):
            m.thing("Lôi Tinh nhỏ", "crystal", px + dx, py + dy, 24, 32, foot=(14, 8), variant=px + i)
        m.poi("landmark", name, px, py)
    # the stair: lanterns in pairs, two gates of the pilgrimage
    y_top, y_bottom = STAIR
    for n, y in enumerate(range(y_bottom - 2, y_top, -6)):
        for x in (56, 64):
            m.thing("Đèn", "lantern", x, y, 8, 24, foot=(4, 4), variant=n * 2 + x)
    for i, y in enumerate((60, 44)):
        m.thing("Cổng hành hương", "gate", 60, y, 32, 32, variant=i)
    m.sign("Thang Lôi Kiếp", "Chín mươi chín bậc: mỗi bậc là một ngày khổ luyện. Lên tới đỉnh là gặp thiên kiếp.",
           64, y_bottom + 1)
    m.poi("landmark", "Thang Lôi Kiếp", 60, 52)
    m.poi("landmark", "Cổng Vấn Đạo", 60, 44)
    # the pilgrims' camp: a shrine where they leave their offerings, a board
    m.thing("Miếu Hành Hương", "shrine", CAMP[0] + 9, CAMP[1] - 3, 32, 44, foot=(28, 12))
    m.thing("Bảng hành hương", "board", CAMP[0] - 9, CAMP[1] - 2, 24, 28, foot=(20, 8))
    m.sign("Bảng hành hương", "Người lên đài phải đủ chín tầng Luyện Khí.\nLôi Linh hai bên đài không tự gây sự.",
           CAMP[0] - 7, CAMP[1] - 1)
    m.poi("landmark", "Miếu Hành Hương", CAMP[0] + 9, CAMP[1] - 3)
    # storm scars on the ridge: rocks split by lightning, crystals grown where it struck
    for i, (x, y) in enumerate(((50, 62), (70, 58), (52, 48), (69, 46), (48, 74), (73, 70), (54, 40), (66, 38))):
        if X.clear_box(m, x - 1, y - 1, x + 1, y):
            m.thing("Đá sét đánh", "boulder", x, y, 32, 24, foot=(26, 10), variant=i)
            X.try_thing(m, "crystal", x + 2, y + 1, name="Lôi tinh")


def monster_areas(m: DaiDiaDo) -> None:
    """The three areas of the small map, by their names: the boss in the middle of the terrace
    (10 x 10 tiles), the Lôi Linh on their platforms, beyond the boss's reach."""
    cx, cy = DAI
    m.obj("loi_long", "monster_area", (cx - 5) * T, (cy - 5) * T, 10 * T, 10 * T, monster="loi_long", count=1)
    for name, (px, py) in zip(("loi_linh_tay", "loi_linh_dong"), LOI_LINH):
        m.obj(name, "monster_area", (px - 3) * T, (py - 5) * T, 6 * T, 10 * T, monster="loi_linh", count=1)


def clouds(m: DaiDiaDo) -> None:
    """Clouds drifting over the abyss near its rim (pictures only: the abyss is solid anyway)."""
    n = 0
    for y in range(3, m.H - 4, 3):
        for x in range(3, m.W - 4, 4):
            j = m.i(x, y)
            if m.hard[j] and m.noise.value(x, y, 7.0, 55) > 0.58:
                rim = any(not m.hard[m.i(x + dx, y + dy)] for dx in (-5, 0, 5) for dy in (-4, 0, 4)
                          if m.inside(x + dx, y + dy))
                if rim or m.noise.value(x, y, 3.0, 56) > 0.8:
                    m.obj("Mây", "prop", x * T - 8, y * T - 4, 32, 20, sprite="cloud_puff", variant=n)
                    n += 1
