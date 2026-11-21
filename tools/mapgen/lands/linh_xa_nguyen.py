"""Linh Xạ Nguyên (zone linh_xa_nguyen, land linh_xa_nguyen, branch Thực Chiến AI): the steppe of
targets, a giant land of Đại Địa Đồ (320 x 240 tiles).

The gate is in the west (Trúc Lâm Thôn's east gate leads here) and the plain rises eastward in
three tiers: the green ranges and the wind-combed meadow of Ngoại Vi (tầng 1-3); across Sông Tên
Rơi the low hills, the training yards of the straw men and the long-distance range of Trung Vực
(tầng 4-6); up an escarpment the burnt pasture of the horse lord, where Xích Diễm Mã runs, and
Đài Vấn Tâm, where one's own Tâm Ma waits (Thâm Xứ, tầng 7-9). A rest camp waits after each wall.
An open plain is the hardest place to keep worth walking: every screenful has a range, a row of
targets, a yard, a hill, a stand of trees or a milestone, and a road or a lane to follow.
Everything the small map had is here: the bow rack at the first range (cung_1 hạ), the rows of
targets (cung_1 trung behind the second row of the long range), the far field where one's own
Tâm Ma waits (cung_1 thượng), Ngọc Thố between two rows of targets in the south, the old sign of
the range.
"""
from __future__ import annotations

import math

from ..builder import T
from ..giant import DaiDiaDo, Theme
from . import _xay_dung as X

ZONE = "linh_xa_nguyen"
SIZE = (320, 240)

# the places other data points at (world_plan.json weapons_placed / beasts `pos`): tiles
GIA_CUNG = (32, 104)             # the bow rack at the first range; cung_1 hạ lies in front of it
CUNG_1_HA = (GIA_CUNG[0], GIA_CUNG[1] + 1)
NGOC_THO = (62, 202)             # between the two rows of targets of Bãi Bia Nam
TRUONG_XA = (124, 184, 204, 216)  # the long-distance range (shooting line x0, lanes to x1)
CUNG_1_TRUNG = (196, 199)        # behind its second row of targets
DAI = (272, 186)                 # Đài Vấn Tâm, the terrace where one's own Tâm Ma waits
CUNG_1_THUONG = DAI
GATE_Y = 118                     # the west gate covers tiles 118..121 of the west edge


# ------------------------------------------------------------------ the grounds
def g_plain(P, D, r):            # the green steppe
    if P > 0.68 and D > 0.4:
        return "flowers0" if r < 0.6 else "flowers1"
    if P < 0.28:
        return "dark_grass0" if r < 0.8 else "dark_grass1"
    return "grass0" if r < 0.55 else "grass1" if r < 0.88 else "grass2"


def g_hills(P, D, r):            # low hills: stone showing through the turf
    if P > 0.74:
        return "stone0"
    if P < 0.26:
        return "dark_grass0" if r < 0.8 else "dark_grass1"
    return "grass1" if r < 0.6 else "grass0"


def g_yard(P, D, r):             # training ground: trodden dirt in patches
    if P > 0.64:
        return "dirt0"
    if P < 0.2:
        return "dark_grass0"
    return "grass0" if r < 0.6 else "grass1"


def g_burnt(P, D, r):            # the burnt pasture
    if P > 0.58:
        return "dirt0"
    if P < 0.3:
        return "dark_grass1" if r < 0.8 else "dark_grass0"
    return "dirt0" if D > 0.52 else "dark_grass1"


def g_heart(P, D, r):            # the high field of Đài Vấn Tâm
    if P > 0.72:
        return "stone0"
    if P < 0.24:
        return "dark_grass0" if r < 0.7 else "dark_grass1"
    if P > 0.58 and D > 0.5:
        return "flowers1"
    return "grass1" if r < 0.7 else "grass2"


def themes(m: DaiDiaDo) -> None:
    th = m.themes
    th["thao_nguyen"] = Theme("thao_nguyen", g_plain, [("tall_grass", 5), ("bush", 2), ("rock", 1), ("peach", 1),
                                                       ("tree", 1)],
                              [("tree", 4), ("peach", 2), ("bush", 2)], 0.035, 0.16, 15.0, 0.62)
    th["co_gio"] = Theme("co_gio", g_plain, [("tall_grass", 6), ("bush", 1), ("rock", 1)],
                         [("peach", 3), ("tree", 2), ("bush", 2)], 0.03, 0.15, 15.0, 0.64)
    th["doi_thap"] = Theme("doi_thap", g_hills, [("rock", 3), ("tall_grass", 3), ("boulder", 1), ("pine", 1),
                                                 ("bush", 1)],
                           [("pine", 4), ("boulder", 2), ("rock", 1)], 0.035, 0.15, 14.0, 0.6)
    th["bai_tap"] = Theme("bai_tap", g_yard, [("tall_grass", 3), ("bush", 2), ("stump", 1), ("rock", 1), ("log", 1)],
                          [("tree", 4), ("bush", 2), ("peach", 1)], 0.03, 0.15, 15.0, 0.62)
    th["truong_xa"] = Theme("truong_xa", g_plain, [("tall_grass", 4), ("bush", 2), ("rock", 1), ("tree", 1)],
                            [("tree", 4), ("bush", 2), ("pine", 1)], 0.032, 0.15, 15.0, 0.62)
    th["dong_chay"] = Theme("dong_chay", g_burnt, [("stump", 3), ("dead_tree", 2), ("rock", 2), ("log", 2),
                                                   ("tall_grass", 1)],
                            [("dead_tree", 5), ("stump", 2), ("boulder", 1)], 0.04, 0.17, 14.0, 0.58)
    th["van_tam"] = Theme("van_tam", g_heart, [("rock", 2), ("tall_grass", 3), ("crystal", 1), ("bush", 1),
                                               ("cloud", 1)],
                          [("pine", 3), ("tree", 2), ("boulder", 1), ("crystal", 1)], 0.035, 0.15, 15.0, 0.6)


# ------------------------------------------------------------------ the map
def build() -> dict:
    W, H = SIZE
    m = DaiDiaDo(ZONE, "Linh Xạ Nguyên", W, H, "linh_xa_nguyen_dai_dia_do")
    themes(m)

    # ---- 1. the khu (band 1 by the west gate, band 3 on the high plain in the east)
    m.khu("lxn_truong_ban", "Trường Bắn Tân Thủ", 1, (0, 0, 109, 119), "thao_nguyen", (56, 60),
          "Những trường bắn đầu tiên phía bắc cổng: nhắm, bắn, xem lệch bao nhiêu rồi chỉnh lại. Thảo Nhân đứng đón tên.")
    m.khu("lxn_co_chai_gio", "Đồng Cỏ Chải Gió", 1, (0, 120, 109, 239), "co_gio", (56, 182),
          "Đồng cỏ gió chải thành từng luống; Ngọc Thố gặm cỏ trăng giữa hai dãy bia phía nam.")
    m.khu("lxn_doi_thap", "Đồi Thấp Gió Lộng", 2, (110, 0, 214, 79), "doi_thap", (160, 40),
          "Những ngọn đồi thấp lô nhô đá, gió lộng; Tâm Ma ẩn sau từng mỏm.")
    m.khu("lxn_bai_tap", "Bãi Tập Thảo Nhân", 2, (110, 80, 214, 159), "bai_tap", (160, 120),
          "Các sân tập có rào, người rơm đứng thành hàng: đánh, xem sai, đánh lại.")
    m.khu("lxn_truong_xa", "Trường Bắn Tầm Xa", 2, (110, 160, 214, 239), "truong_xa", (160, 200),
          "Trường bắn dài nhất thảo nguyên, hai hàng bia: tên bay càng xa, sai số càng lớn.")
    m.khu("lxn_dong_chay", "Đồng Cháy Xích Mã", 3, (215, 0, 319, 119), "dong_chay", (266, 60),
          "Bãi chăn ngựa của một mã chủ đã cháy rụi; Xích Diễm Mã còn phi trên tro.")
    m.khu("lxn_van_tam", "Đài Vấn Tâm", 3, (215, 120, 319, 239), "van_tam", (258, 204),
          "Cao nguyên lặng gió quanh Đài Vấn Tâm, nơi Tâm Ma của chính mình chờ sẵn.")

    # ---- 2. the ground, the camps
    m.paint(warp=7.0, scale=26.0)
    m.camp("lxn_leu_cong", "Lều Cửa Thảo Nguyên", (18, 120), r=8,
           desc_vi="Lều nghỉ ngay trong cổng thảo nguyên, cạnh giá cung. Không có quái.",
           label_vi="Lều Cửa Thảo Nguyên · giá cung", to_edge="w")
    m.camp("lxn_tram_gio", "Trạm Gió Bờ Sông", (128, 120), r=6,
           desc_vi="Trạm nghỉ bên kia Sông Tên Rơi, cửa vào Trung Vực.", label_vi="Trạm Gió Bờ Sông · cửa Trung Vực")
    m.camp("lxn_leu_ngua", "Lều Mã Phu", (232, 120), r=6,
           desc_vi="Lều mã phu trên dốc cao, cửa vào Thâm Xứ.", label_vi="Lều Mã Phu · cửa Thâm Xứ")
    m.clear_zones.append((0, GATE_Y - 4, 12, GATE_Y + 7))               # the gate and the spawn

    # ---- 3. the large features
    m.lake(84, 30, 6, 4)                                   # Hồ Gương Cỏ, in the north range
    m.lake(300, 214, 6, 4)                                 # a still pool by Đài Vấn Tâm
    m.lake(198, 128, 4, 3)                                 # a pond in the training ground
    keep_landmarks(m)
    hills(m)
    training_grounds(m)
    corral(m)

    # ---- 4. the walls: Sông Tên Rơi, then the escarpment
    band1, band2, band3 = ("lxn_truong_ban", "lxn_co_chai_gio"), \
        ("lxn_doi_thap", "lxn_bai_tap", "lxn_truong_xa"), ("lxn_dong_chay", "lxn_van_tam")
    walls = {}
    for a in band1:
        for b in band2:
            walls[(a, b)] = "water"
    for a in band2 + band1:
        for b in band3:
            walls[(a, b)] = "cliff"
    m.barriers(walls, default="open")
    widen_river(m)

    # ---- 5. the ranges and lanes, then the roads
    ranges(m)
    m.node("gate", (3, GATE_Y + 2), "Cổng Tây · về Trúc Lâm Thôn")
    m.node("n_truong_ban", (56, 60), "Trường Bắn Tân Thủ · Ngoại Vi, tầng 1-3")
    m.node("n_co_gio", (56, 182), "Đồng Cỏ Chải Gió · Ngoại Vi, tầng 1-3")
    m.node("n_bia_nam", (NGOC_THO[0], NGOC_THO[1] + 12), "Bãi Bia Nam", sign=False)
    m.node("n_doi", (160, 40), "Đồi Thấp Gió Lộng · Trung Vực, tầng 4-6")
    m.node("n_bai_tap", (160, 120), "Bãi Tập Thảo Nhân · Trung Vực, tầng 4-6")
    m.node("n_truong_xa", (160, 200), "Trường Bắn Tầm Xa · Trung Vực, tầng 4-6")
    m.node("n_dong_chay", (266, 60), "Đồng Cháy Xích Mã · Thâm Xứ, tầng 7-9")
    m.node("n_van_tam", (258, 204), "Đài Vấn Tâm · Thâm Xứ, tầng 7-9")
    m.node("n_dai", (DAI[0], DAI[1] + 10), "Đài Vấn Tâm", sign=False)
    m.network([
        ("gate", "lxn_leu_cong", "main"),
        ("lxn_leu_cong", "n_truong_ban", "main"),
        ("lxn_leu_cong", "n_co_gio", "main"),
        ("lxn_leu_cong", "lxn_tram_gio", "main"),
        ("n_co_gio", "n_bia_nam", "trail"),
        ("lxn_tram_gio", "n_doi", "main"),
        ("lxn_tram_gio", "n_bai_tap", "main"),
        ("lxn_tram_gio", "n_truong_xa", "main"),
        ("n_truong_ban", "n_doi", "trail"),
        ("n_co_gio", "n_truong_xa", "trail"),
        ("n_bai_tap", "lxn_leu_ngua", "main"),
        ("lxn_leu_ngua", "n_dong_chay", "main"),
        ("lxn_leu_ngua", "n_van_tam", "main"),
        ("n_van_tam", "n_dai", "trail"),
        ("n_doi", "n_dong_chay", "trail"),
        ("n_truong_xa", "n_van_tam", "trail"),
    ])
    m.carve([(x, GATE_Y + 2) for x in range(1, 18)], "main")             # through the gate

    # ---- 6. the places
    gate_camp(m)
    landmarks(m)
    comb_the_grass(m)
    milestones(m)
    plain_features(m, ("lxn_truong_ban", "lxn_co_chai_gio", "lxn_doi_thap", "lxn_bai_tap", "lxn_truong_xa",
                       "lxn_dong_chay", "lxn_van_tam"))
    m.signposts()

    # ---- 8. the monsters
    monsters(m)

    # ---- 9, 10
    m.dress_barriers()
    m.scatter()
    m.gate("w", GATE_Y, "truc_lam_thon", "from_linh_xa_nguyen", "Cổng Tây")
    m.sign("Về Trúc Lâm Thôn", "Tây → Trúc Lâm Thôn", 3, GATE_Y - 2)
    m.poi("gate", "Cổng Tây · về Trúc Lâm Thôn", 1, GATE_Y + 2)
    m.obj("spawn", "spawn", 4 * T, (GATE_Y + 2) * T, 1, 1)
    m.obj("from_village", "spawn", 4 * T, (GATE_Y + 2) * T, 1, 1)
    return m.finish({"music": "forest", "safe": "false"}, ring="peach",
                    gaps={("w", y) for y in range(GATE_Y, GATE_Y + 4)})


# ------------------------------------------------------------------ the features
def keep_landmarks(m: DaiDiaDo) -> None:
    m.keep_rect(26, 98, 82, 110)                               # Trường Bắn Đầu, by the gate camp
    m.keep_rect(28, 50, 86, 70)                                # Trường Bắn Bảy Bia
    m.keep_rect(40, 192, 82, 212)                              # Bãi Bia Nam
    x0, y0, x1, y1 = TRUONG_XA
    m.keep_rect(x0 - 2, y0 - 1, x1 + 2, y1 + 1)                # Trường Bắn Tầm Xa
    m.keep_rect(DAI[0] - 10, DAI[1] - 9, DAI[0] + 10, DAI[1] + 9)
    m.keep_rect(256, 48, 280, 72)                              # the horse lord's camp


def hills(m: DaiDiaDo) -> None:
    """Đồi Thấp: low hills of turf and stone the paths wind between; each a solid knoll with
    boulders on its crown."""
    ri = X.region_index(m, "lxn_doi_thap")
    spots = [(124, 14), (142, 22), (178, 12), (198, 30), (128, 52), (184, 58), (204, 66), (150, 68),
             (118, 34), (196, 8), (168, 72), (138, 38)]
    for n, (cx, cy) in enumerate(spots):
        rx, ry = 3 + n % 3, 2 + (n + 1) % 2
        knoll = {(x, y) for (x, y) in m.blob(cx, cy, rx, ry, 0.2, salt=60 + n)
                 if m.inside(x, y, 3) and m.region[m.i(x, y)] == ri and not m.keep[m.i(x, y)]}
        if abs(cx - 160) < 8 and abs(cy - 40) < 8:
            continue
        X.solid_ring(m, knoll, "dark_grass1")
        for (x, y) in sorted(knoll):
            if (x + 2 * y) % 2 == 0:
                m.obj("Đồi đá", "prop", x * T - 8, y * T - 8, 32, 24, sprite="boulder",
                      variant=(x * 13 + y) % 1000)
            elif (x * 3 + y) % 5 == 0:
                m.obj("tree", "prop", x * T - 8, y * T - 24, 32, 40, sprite="pine", variant=(x * 7 + y) % 1000)
            m.blocked_tiles.add((x, y))
        m.keep_rect(cx - rx - 1, cy - ry - 1, cx + rx + 1, cy + ry + 1)


def corral(m: DaiDiaDo) -> None:
    """Chuồng Ngựa Cháy: the burnt corral of the horse lord, a fence of charred logs with a gap
    to the south; his huts beside it."""
    x0, y0, x1, y1 = 258, 50, 278, 64
    fence = {t for t in X.outline(x0, y0, x1, y1) if not (t[1] == y1 and 266 <= t[0] <= 270)}
    X.solid_ring(m, fence, "dirt0")
    for (x, y) in sorted(fence):
        if (x + y) % 2 == 0:
            m.obj("Rào cháy", "prop", x * T - 4, y * T - 2, 24, 16, sprite="log", variant=(x * 7 + y) % 1000)
        m.blocked_tiles.add((x, y))
    for y in range(y0 + 1, y1):
        for x in range(x0 + 1, x1):
            m.setg(x, y, "dirt0")


def widen_river(m: DaiDiaDo) -> None:
    """Sông Tên Rơi: the water barrier between Ngoại Vi and Trung Vực made a real river, four
    tiles wide with stone banks (the roads bridge it)."""
    wet = {(x, y) for y in range(m.H) for x in range(m.W) if m.barrier[m.i(x, y)] == "water"}
    more = {(x + dx, y + dy) for (x, y) in wet for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    m._wet({t for t in more if not m.keep[m.i(*t)]} | wet, "water0", 1, "stone0")


def ranges(m: DaiDiaDo) -> None:
    """The archery ranges: dirt lanes from a shooting line to rows of stone targets."""
    # Trường Bắn Đầu, by the gate camp: three lanes, targets near and far
    shooting_range(m, 36, 78, (100, 104, 108), [50, 64, 77])
    # Trường Bắn Bảy Bia, around the anchor of the north range: six lanes, two rows and strays
    shooting_range(m, 30, 86, (51, 54, 57, 63, 66, 69), [44, 62, 85])
    # Bãi Bia Nam, where Ngọc Thố grazes: moon grass between two rows of targets
    for (x, y) in m.blob(62, 202, 9, 6, 0.3, salt=81):
        if m.inside(x, y, 3) and not m.hard[m.i(x, y)]:
            m.setg(x, y, "flowers1" if m.noise.value(x, y, 4.0, 82) > 0.45 else "flowers0")
    # Trường Bắn Tầm Xa: six long lanes, two rows of targets, strays between
    x0, y0, x1, y1 = TRUONG_XA
    shooting_range(m, x0 + 2, x1, (186, 191, 196, 201, 206, 211), [146, 162, 178, 192])


def shooting_range(m: DaiDiaDo, xa: int, xb: int, lanes, rows) -> None:
    """A range: one-tile dirt lanes from a shooting line (lanterns, a rack of arrows, a mat per
    lane) eastward, a target at the end of every lane and, lane by lane, targets at the nearer
    distances `rows` (staggered, so the rows read as distances, not as a wall)."""
    for n, y in enumerate(lanes):
        X.lane(m, [(x, y) for x in range(xa, xb) if not m.hard[m.i(x, y)]], "dirt0")
        m.thing("Chiếu bắn", "mat", xa, y, 24, 16)
        for k, tx in enumerate(rows):
            if k < len(rows) - 1 and (n + k) % 2:
                continue
            if not m.hard[m.i(tx, y - 1)]:
                m.thing("Bia bắn", "tablet", tx, y - 1, 16, 24, foot=(12, 8), variant=tx * 3 + y)
                m.blocked_tiles.add((tx, y - 1))
        if n % 2 == 0:
            m.thing("Cỏ", "tall_grass", xa + 4 + (n * 5) % 9, y + 1, 24, 16, variant=xa + y)
    top, bottom = min(lanes) - 2, max(lanes) + 2
    for y in (top, bottom):
        m.thing("Đèn", "lantern", xa - 1, y, 8, 24, foot=(4, 4), variant=xa + y)
    m.thing("Giá tên", "board", xa - 3, (top + bottom) // 2, 24, 28, foot=(20, 8), variant=xa)


def gate_camp(m: DaiDiaDo) -> None:
    gx, gy = GIA_CUNG
    m.thing("Giá Cung", "board", gx, gy, 24, 28, foot=(20, 8))
    m.sign("Trường bắn", "Nhắm, bắn, xem lệch bao nhiêu rồi chỉnh lại: đó là huấn luyện", gx + 2, gy + 1)
    m.poi("landmark", "Trường Bắn Đầu", 56, 104)
    m.sign("Bảng chỉ dẫn", "Thảo nguyên đi về đông là vào sâu.\n"
           "Qua Sông Tên Rơi là Trung Vực, lên dốc cháy là Thâm Xứ.", 26, 116)


def landmarks(m: DaiDiaDo) -> None:
    m.poi("landmark", "Trường Bắn Bảy Bia", 56, 60)
    m.sign("Trường Bắn Bảy Bia", "Bảy làn bắn, hai hàng bia: bắn nhiều lượt, lấy trung bình độ lệch rồi mới chỉnh.",
           28, 58)
    m.poi("landmark", "Hồ Gương Cỏ", 84, 30)
    # Bãi Bia Nam: two rows of targets facing each other, the moon grass between
    for ty in range(194, 212, 3):
        for tx in (50, 74):
            m.thing("Bia bắn", "tablet", tx, ty, 16, 24, foot=(12, 8), variant=tx + ty)
    m.thing("Đèn", "lantern", 62, 193, 8, 24, foot=(4, 4), variant=3)
    for i, (tx, ty) in enumerate(((55, 197), (58, 207), (67, 196), (69, 206), (64, 209), (56, 202), (70, 200))):
        m.thing("Cỏ trăng", "tall_grass", tx, ty, 24, 16, variant=i + 40)
    for i, (tx, ty) in enumerate(((53, 210), (71, 194))):
        m.thing("Bụi cây", "bush", tx, ty, 24, 16, variant=i + 44)
    m.sign("Bãi Bia Nam", "Giữa hai dãy bia mọc cỏ trăng: thỏ ngọc hay ra đây gặm cỏ.", 58, 214)
    m.poi("landmark", "Bãi Bia Nam", 62, 202)
    m.poi("beast", "Bãi Bia Nam · Ngọc Thố", *NGOC_THO)
    # Trường Bắn Tầm Xa
    x0, y0, x1, y1 = TRUONG_XA
    m.sign("Trường Bắn Tầm Xa", "Bia càng xa, mũi tên càng lệch: sai một ly ở dây cung, đi một dặm ở đích.",
           x0, y0 - 1)
    m.poi("landmark", "Trường Bắn Tầm Xa", 160, 198)
    # Bãi Tập: the pavilion of the master among the yards
    m.building("Đình Huấn Luyện", "pavilion", 154, 103, 64, 64, 22)
    m.sign("Đình Huấn Luyện", "Đánh, xem sai ở đâu, đánh lại: Thảo Nhân không biết đau, chỉ biết sai số.", 152, 108)
    m.poi("landmark", "Đình Huấn Luyện", 156, 106)
    m.poi("landmark", "Ao Sân Tập", 198, 128)
    # Đồi Thấp: a lookout cairn on the highest hill
    m.thing("Cột mốc gió", "tablet", 160, 34, 16, 24, foot=(12, 8))
    m.sign("Gò Gió Lộng", "Đứng trên gò mới thấy hết các trường bắn: nhìn toàn cục trước khi chỉnh từng mũi tên.",
           163, 36)
    m.poi("landmark", "Gò Gió Lộng", 160, 34)
    # the horse lord's camp beside the burnt corral
    m.building("Lều Mã Chủ", "hut", 260, 67, 64, 56, 30)
    m.thing("Sạp cỏ khô", "stall", 274, 69, 40, 32, foot=(36, 12))
    m.thing("Máng nước", "well", 268, 57, 24, 24, foot=(20, 12))
    for i, (tx, ty) in enumerate(((261, 53), (275, 53), (261, 61), (275, 61), (264, 56), (272, 59))):
        m.thing("Cọc buộc ngựa" if i < 4 else "Gốc cháy", "stump", tx, ty, 24, 16, foot=(18, 8), variant=i + 60)
    m.tree(271, 53, "ink_tree")
    m.thing("Khúc gỗ cháy", "log", 263, 59, 24, 16, foot=(18, 8), variant=66)
    m.sign("Chuồng Ngựa Cháy", "Chuồng ngựa của mã chủ cháy rụi: Xích Diễm Mã vẫn chạy vòng quanh như chưa biết.",
           265, 74)
    m.poi("landmark", "Chuồng Ngựa Cháy", 268, 57)
    # Đài Vấn Tâm: a round terrace, crystals round it, the shrine
    dx, dy = DAI
    for y in range(dy - 7, dy + 8):
        for x in range(dx - 8, dx + 9):
            d = math.hypot(x - dx, (y - dy) * 1.15)
            if d <= 6.5:
                m.setg(x, y, "realm_floor0" if (x + y) % 3 else "realm_floor1")
            elif d <= 8:
                m.setg(x, y, "plaza0" if (x + y) % 2 else "plaza1")
    for i in range(8):
        a = i * math.pi / 4 + math.pi / 8
        m.thing("Tâm Tinh", "crystal", round(dx + 9.5 * math.cos(a)), round(dy + 8 * math.sin(a)), 24, 32,
                foot=(14, 8), variant=i)
    m.thing("Miếu Vấn Tâm", "shrine", dx, dy - 5, 32, 44, foot=(28, 12))
    m.sign("Đài Vấn Tâm", "Đài Vấn Tâm: đối thủ khó nhất là chính mình của hôm qua.", dx + 3, dy + 9)
    m.poi("landmark", "Đài Vấn Tâm", dx, dy)
    m.poi("landmark", "Hồ Lặng", 300, 214)


def training_grounds(m: DaiDiaDo) -> None:
    """Bãi Tập: fenced yards with rows of straw posts around the pavilion of the master (laid
    before the roads, which come in through the gaps)."""
    for n, (yx, yy) in enumerate(((134, 90), (174, 90), (134, 136), (172, 138))):
        training_yard(m, yx, yy, n)
    m.keep_rect(152, 101, 160, 108)


def training_yard(m: DaiDiaDo, x0: int, y0: int, n: int) -> None:
    """A fenced yard (bamboo, a gap facing the pavilion) with rows of straw posts on trodden dirt."""
    x1, y1 = x0 + 14, y0 + 10
    gap_x = range(x0 + 6, x0 + 9)
    fence = {t for t in X.outline(x0, y0, x1, y1) if not (t[1] in (y0, y1) and t[0] in gap_x)}
    if any(m.hard[m.i(*t)] or m.keep[m.i(*t)] for t in X.outline(x0, y0, x1, y1)):
        return
    X.fence(m, fence, "dirt0", every=1)
    for y in range(y0 + 1, y1):
        for x in range(x0 + 1, x1):
            m.setg(x, y, "dirt0")
    for ty in (y0 + 3, y0 + 7):
        for tx in range(x0 + 3, x1 - 1, 3):
            m.thing("Cọc rơm", "tablet", tx, ty, 16, 24, foot=(12, 8), variant=tx + ty + n)
    m.keep_rect(x0, y0, x1, y1)


def comb_the_grass(m: DaiDiaDo) -> None:
    """Đồng Cỏ Chải Gió: the wind combs the grass into long slanting rows, tall grass along them
    (walk-through) with gaps where the gusts broke them."""
    ri = X.region_index(m, "lxn_co_chai_gio")
    for y in range(124, 236):
        for x in range(4, 108):
            j = m.i(x, y)
            if m.region[j] != ri or m.hard[j] or m.road[j] or m.keep[j] or (x, y) in m.blocked_tiles:
                continue
            wave = round(2.2 * math.sin(x / 6.0) + 1.2 * math.sin(x / 2.7 + y / 9.0))
            s = (y + wave) % 6
            if s == 0 and x % 2 == 0 and m.noise.value(x, y, 7.0, 71) > 0.3:
                m.thing("Cỏ", "tall_grass", x, y, 24, 16, variant=(x * 31 + y) % 1000)
                m.blocked_tiles.add((x, y))
            elif s == 3 and m.noise.value(x, y, 9.0, 72) > 0.66:
                m.setg(x, y, "flowers0")


FEATURES = (    # small compositions for the open plain: (prop, dx, dy) relative to a spot
    (("tree", 0, 0), ("bush", -2, 1), ("bush", 2, 1), ("tall_grass", 1, 2)),
    (("boulder", 0, 0), ("rock", -2, 1), ("rock", 2, 0), ("tall_grass", 0, 2)),
    (("peach", 0, 0), ("peach", 3, 1), ("tall_grass", -2, 1)),
    (("stump", 0, 0), ("log", 2, 0), ("tall_grass", -1, 1), ("bush", 1, -2)),
    (("x_target", 0, 0), ("x_lantern", 2, 0), ("tall_grass", -1, 1)),
    (("pine", 0, 0), ("pine", 2, 1), ("rock", -1, 2)),
)


def plain_features(m: DaiDiaDo, kids, cell=(15, 9)) -> None:
    """One small composition (a stand of trees, rocks round a boulder, a lone target, a fallen
    log) in every screenful of the open plain that has neither a road nor a landmark nor a clump
    of its own, so no screenful is an empty carpet of grass."""
    from ..giant import PROPS, Prop
    PROPS.setdefault("x_target", Prop("thing", "tablet", "Bia bắn lẻ", 16, 24, (12, 8)))
    PROPS.setdefault("x_lantern", Prop("thing", "lantern", "Đèn", 8, 24, (4, 4)))
    cw, ch = cell
    for kid in kids:
        k = X.khu_of(m, kid)
        ri = m.bands_khu.index(k)
        x0, y0, x1, y1 = k.rect
        for cy in range(y0 + 2, y1 - ch + 2, ch):
            for cx in range(x0 + 2, x1 - cw + 2, cw):
                busy = sum(1 for y in range(cy, cy + ch) for x in range(cx, cx + cw)
                           if m.inside(x, y) and (m.road[m.i(x, y)] or m.keep[m.i(x, y)]
                                                  or m.hard[m.i(x, y)] or (x, y) in m.blocked_tiles))
                if busy > cw * ch // 6:
                    continue
                for _ in range(4):
                    sx, sy = m.rng.randint(cx + 3, cx + cw - 4), m.rng.randint(cy + 3, cy + ch - 3)
                    comp = FEATURES[m.rng.randrange(len(FEATURES))]
                    if X.clear_box(m, sx - 3, sy - 3, sx + 3, sy + 3, ri):
                        for prop, dx, dy in comp:
                            X.try_thing(m, prop, sx + dx, sy + dy, ri)
                        break


def milestones(m: DaiDiaDo) -> None:
    """Along every main road, a milestone or a lantern every couple of screens, so the way on is
    never lost on the open plain."""
    n = 0
    for e in m.edges:
        if e["style"] != "main":
            continue
        for k in range(14, len(e["path"]) - 8, 26):
            x, y = e["path"][k]
            spot = m.free_near(x, y, radius=3)
            if spot is None:
                continue
            if n % 2:
                m.thing("Đèn đường", "lantern", *spot, 8, 24, foot=(4, 4), variant=n)
            else:
                m.thing("Cột mốc", "tablet", *spot, 16, 24, foot=(12, 8), variant=n + 50)
            n += 1


# ------------------------------------------------------------------ the monsters
def monsters(m: DaiDiaDo) -> None:
    """Band 1: Thảo Nhân and Tâm Ma (their low nodes); band 2: the same with their middle nodes
    and a few elites; band 3: only the elites (the land has no normal creature of tầng 7-9), one
    per area, a handful per khu: Xích Diễm Mã on its burnt pasture, Tâm Ma Chấp Niệm round Đài Vấn
    Tâm."""
    m.monsters("lxn_truong_ban", [("thao_nhan", 3), ("tam_ma", 1)], tiles_per=200)
    m.monsters("lxn_co_chai_gio", [("thao_nhan", 2), ("tam_ma", 2)], tiles_per=200)
    m.monsters("lxn_doi_thap", [("tam_ma", 3), ("thao_nhan", 1)], [("xich_diem_ma", 1), ("tam_ma_chap_niem", 1)],
               tiles_per=200)
    m.monsters("lxn_bai_tap", [("thao_nhan", 3), ("tam_ma", 1)], [("tam_ma_chap_niem", 1), ("xich_diem_ma", 1)],
               tiles_per=200)
    m.monsters("lxn_truong_xa", [("tam_ma", 2), ("thao_nhan", 2)], [("xich_diem_ma", 1), ("tam_ma_chap_niem", 1)],
               tiles_per=200)
    dx, dy = DAI
    m.monster_area("lxn_van_tam", "tam_ma_chap_niem", (dx - 6, dy - 4, dx + 6, dy + 5), 1, name="tam_ma_chap_niem")
    m.monsters("lxn_dong_chay", [("xich_diem_ma", 2), ("tam_ma_chap_niem", 1)], cell=(16, 14), tiles_per=1e9,
               max_areas=7)
    m.monsters("lxn_van_tam", [("tam_ma_chap_niem", 2), ("xich_diem_ma", 1)], cell=(16, 14), tiles_per=1e9,
               max_areas=6, skip=lambda r: abs((r[0] + r[2]) / 2 - dx) < 16 and abs((r[1] + r[3]) / 2 - dy) < 14)
