"""Vạn Tượng Trạch (zone ho_nghien_muc, land van_tuong_trach, branch Xác Suất và Thống Kê): the
marsh of ten thousand shapes, a giant land of Đại Địa Đồ (320 x 240 tiles).

Open water everywhere, and in it reed islands joined by boardwalks and plank bridges: every
island is a vertex, every boardwalk an edge, the signposts name the nearest place each way
leads. Fog lies on the ground (pale stone patches, drifting clouds), every step a little
uncertain. The three tiers of tu vi lie from the east gate to the west, each behind a wide
channel crossed by a long boardwalk: Ngoại Vi (tầng 1-3) by the gate, where Ngư Ông keeps his
dock on Hồ Nghiên Mực and fishing goes on as before; Trung Vực (tầng 4-6) with the fog island
where Huyền Quy suns itself and the mossy rock of Bích Nhãn Kim Thiềm; Thâm Xứ (tầng 7-9) with
the sunken shrine, the old tree in the deep water and the blood-red marsh of the crocodiles.
Two islets with no bridge (Đạp Kiếm Lướt) hold nothing but a sight worth the glide.
"""
from __future__ import annotations

import math
import random

from ..builder import T
from ..giant import SOLID_WATER, Theme
from ._do_thi import Builder, Cells, fill, islands, overlaps, route_signs, spread

ZONE = "ho_nghien_muc"
SIZE = (320, 240)
SEED = "van_tuong_trach_dai_dia_do"

GATE_Y = 118                   # the east gate: tiles 118..121 of the east edge
SPAWN = (316, 120)
CAMP1 = (301, 121)
CAMP2 = (196, 119)
CAMP3 = (90, 119)
# Ngư Ông's corner on Hồ Nghiên Mực: the small lake map's corner moved by (OX, OY); the dock
# runs north from the shore into the lake
OX, OY = 250, 88
NGU_ONG = (25 + OX, 27 + OY)   # his feet tile
DOCK = (27 + OX, 19 + OY, 28 + OX, 26 + OY)
LIEU = (23 + OX, 27 + OY)      # ho_lo_1 ha hangs from the willow by the dock
FOG = (160, 100)               # Đảo Sương: Huyền Quy, ho_lo_1 trung
HUYEN_QUY = FOG
HO_LO_TRUNG = (FOG[0] + 1, FOG[1] + 1)
KIM = (150, 28)                # the mossy rock of Bích Nhãn Kim Thiềm
MIEU = (48, 30)                # Miếu Chìm: ho_lo_1 thuong in front of it
HO_LO_THUONG = (MIEU[0], MIEU[1] + 1)
CO_THU = (36, 122)             # the old tree in the deep water: ho_lo_2 ha at its foot
HO_LO_2 = (CO_THU[0] - 1, CO_THU[1] + 1)
DOM_DOM = (262, 202)           # Bãi Đom Đóm
LAU = (262, 36)                # Đình Gió Lau
PHAO = (160, 204)              # Cầu Phao Chín Nhịp, the middle of the long boardwalk
NGAC = (52, 204)               # Bến Ngạc Đỏ


# ------------------------------------------------------------------ themes
def g_reeds(P, D, r):
    if P < 0.22:
        return "dark_grass0" if r < 0.7 else "dark_grass1"
    if P > 0.76 and D > 0.5:
        return "flowers0"
    return "grass0" if r < 0.45 else "grass1" if r < 0.85 else "grass2"


def g_fog(P, D, r):
    if P > 0.72 and D > 0.4:
        return "stone0"
    if P < 0.2:
        return "dark_grass0"
    return "grass2" if r < 0.55 else "grass1"


def g_moss(P, D, r):
    if P > 0.7:
        return "stone0"
    if P < 0.28:
        return "dark_grass0" if r < 0.6 else "dark_grass1"
    return "grass1" if r < 0.7 else "grass2"


def g_dark(P, D, r):
    if P < 0.46:
        return "dark_grass0" if r < 0.6 else "dark_grass1"
    if P > 0.7:
        return "dirt0"
    return "grass2" if r < 0.7 else "grass1"


def g_blood(P, D, r):
    if P > 0.5:
        return "dirt0"
    if P < 0.28:
        return "dark_grass1"
    return "grass2"


def themes(m) -> None:
    m.themes["lau_say"] = Theme("lau_say", g_reeds, [("tall_grass", 6), ("bush", 2), ("tree", 1), ("rock", 1)],
                                [("tall_grass", 4), ("tree", 3), ("bush", 2)], 0.05, 0.16, 14.0, 0.56)
    m.themes["suong_dam"] = Theme("suong_dam", g_fog, [("cloud", 5), ("tall_grass", 3), ("rock", 1), ("bush", 1)],
                                  [("cloud", 4), ("tree", 2), ("tall_grass", 2)], 0.055, 0.16, 14.0, 0.56)
    m.themes["reu"] = Theme("reu", g_moss, [("rock", 3), ("boulder", 1), ("tall_grass", 3), ("bush", 2)],
                            [("boulder", 3), ("tree", 2), ("bush", 2)], 0.045, 0.15, 14.0, 0.56)
    m.themes["dam_toi"] = Theme("dam_toi", g_dark, [("dead_tree", 3), ("tall_grass", 4), ("rock", 1), ("cloud", 1)],
                                [("dead_tree", 5), ("tall_grass", 2)], 0.045, 0.15, 14.0, 0.56)
    m.themes["huyet"] = Theme("huyet", g_blood, [("dead_tree", 2), ("rock", 3), ("tall_grass", 2), ("log", 1)],
                              [("dead_tree", 4), ("boulder", 2)], 0.045, 0.15, 14.0, 0.56)


# ------------------------------------------------------------------ build
def build() -> dict:
    W, H = SIZE
    m = Builder(ZONE, "Vạn Tượng Trạch", W, H, SEED)
    rng = random.Random(SEED + ":dao")
    themes(m)

    # ---- 1. the khu (band 1 by the east gate, band 3 in the west)
    K = {}
    K["lau"] = m.khu("vtt_lau_say", "Bãi Lau Sậy", 1, (215, 0, 319, 79), "lau_say", LAU,
                     "Những đảo lau sậy phía bắc bến: Đầu Tử Oa nhảy giữa các bụi lau.")
    K["ben"] = m.khu("vtt_ben_suong", "Bến Sương Mù", 1, (215, 80, 319, 159), "lau_say", (284, 117),
                     "Bến đầu đầm ngay trong cổng đông: Ngư Ông câu trên Hồ Nghiên Mực, cầu ván nối các đảo.")
    K["dom"] = m.khu("vtt_dom_dom", "Đầm Đom Đóm", 1, (215, 160, 319, 239), "suong_dam", DOM_DOM,
                     "Đầm sương phía nam, đêm nào cũng lập lòe U Minh Đăng như đom đóm.")
    K["thach"] = m.khu("vtt_thach_ban", "Thạch Bàn Rêu Xanh", 2, (105, 0, 214, 79), "reu", KIM,
                       "Những đảo đá phủ rêu; trên tảng đá lớn nhất, Bích Nhãn Kim Thiềm ngậm đồng tiền vàng.")
    K["suong"] = m.khu("vtt_dao_suong", "Đảo Sương Huyền Quy", 2, (105, 80, 214, 159), "suong_dam", FOG,
                       "Giữa đầm, đảo sương nơi Huyền Quy phơi mình; sương dày tới mức mỗi bước một điều chưa chắc.")
    K["phao"] = m.khu("vtt_cau_phao", "Lạch Cầu Phao", 2, (105, 160, 214, 239), "lau_say", PHAO,
                      "Lạch nước rộng, những cây cầu phao chín nhịp nối các đảo lau.")
    K["mieu"] = m.khu("vtt_mieu_chim", "Miếu Chìm", 3, (0, 0, 104, 79), "dam_toi", HO_LO_THUONG,
                      "Đầm tối phía tây bắc: một ngôi miếu cổ chìm nửa trong nước, Hồ Lô Tinh canh cửa.")
    K["co"] = m.khu("vtt_dam_sau", "Đầm Sâu Cổ Thụ", 3, (0, 80, 104, 159), "dam_toi", (66, 119),
                    "Nước sâu nhất của đầm; một cây cổ thụ đứng trên đảo nhỏ giữa vùng nước, chỉ một cầu ván dẫn tới.")
    K["huyet"] = m.khu("vtt_huyet_dam", "Huyết Đầm", 3, (0, 160, 104, 239), "huyet", NGAC,
                       "Đầm đất đỏ phía tây nam, nơi Huyết Ngạc nằm phục dưới nước.")
    ri = {key: m.bands_khu.index(k) for key, k in K.items()}

    # ---- 2. the ground, the camps
    m.paint(warp=7.0, scale=26.0)
    m.camp("vtt_trai_ben", "Trại Bến Đầm", CAMP1, r=7,
           desc_vi="Trại ngay trong cổng đông, cạnh lều Ngư Ông và Hồ Nghiên Mực. Không có quái.",
           label_vi="Trại Bến Đầm (nghỉ chân)", to_edge="e")
    m.camp("vtt_tram_suong", "Trạm Sương", CAMP2, r=6,
           desc_vi="Trạm nghỉ bên kia lạch lớn, cửa vào Trung Vực.", label_vi="Trạm Sương · cửa Trung Vực")
    m.camp("vtt_am_den", "Am Đèn Lồng", CAMP3, r=6,
           desc_vi="Am thắp đèn bên kia lạch sâu, cửa vào Thâm Xứ.", label_vi="Am Đèn Lồng · cửa Thâm Xứ")
    m.clear_zones.append((W - 6, GATE_Y - 2, W - 1, GATE_Y + 5))   # the gate and the spawn

    # ---- 3. the water: walls of water between the khu, the islands
    m.barriers({}, default="water")
    seeds, radius = island_seeds(m, rng)
    cells = Cells(m, seeds, warp=4.0)
    dry = dry_ground()
    islands(m, cells, radius, keep_land=lambda x, y: any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in dry))
    lake_corner(m)
    moats(m)

    # ---- 5. the roads: the boardwalks between the islands
    for sid in cells.ids:
        if sid not in m.nodes:
            m.node(sid, cells.tile[sid], "", sign=False)
    m.node("gate", (W - 4, GATE_Y + 1), "Cổng Đông · về Trúc Lâm Thôn", sign=False)
    m.node("n_ngu_ong", (NGU_ONG[0] + 8, NGU_ONG[1] + 1), "Lều Ngư Ông", sign=False)
    edges = graph_edges(m, cells, rng, ri)
    spine = spine_edges(edges, {k: v["tile"] for k, v in m.nodes.items()},
                        ["gate", "vtt_trai_ben", "vtt_tram_suong", "vtt_am_den"])
    order = [e for e in edges if frozenset(e) in spine] + [e for e in edges if frozenset(e) not in spine]
    m.network([(a, b, "main" if frozenset((a, b)) in spine else "trail") for (a, b) in order])
    m.carve([(x, GATE_Y + 1) for x in range(W - 5, W)], "main")      # through the gate
    m.carve([(MIEU[0], y) for y in range(MIEU[1] + 1, MIEU[1] + 7)], "trail")   # the plank to Miếu Chìm
    near = lambda kid, p: min((s for s in seeds if s[0].startswith(kid + "_")),  # noqa: E731
                              key=lambda s: math.dist(s[1], p))[1]
    K["co"].anchor = near("vtt_dam_sau", (62, 119))

    # ---- 6. the places, 7. the signposts
    places(m)
    glide_islets(m)
    named = {
        "gate": "Cổng Đông · về Trúc Lâm Thôn",
        "vtt_trai_ben": "Trại Bến Đầm",
        "n_ngu_ong": "Lều Ngư Ông · Hồ Nghiên Mực",
        "vtt_tram_suong": "Trạm Sương · Trung Vực",
        "vtt_am_den": "Am Đèn Lồng · Thâm Xứ",
        "n_lau": "Đình Gió Lau",
        "n_dom": "Bãi Đom Đóm",
        "n_kim": "Thạch Bàn Kim Thiềm",
        "n_fog": "Đảo Sương",
        "n_phao": "Cầu Phao Chín Nhịp",
        "n_mieu": "Miếu Chìm",
        "n_co_thu": "Cổ Thụ Giữa Đầm",
        "n_ngac": "Bến Ngạc Đỏ",
    }
    route_signs(m, named, at={"vtt_trai_ben", "vtt_tram_suong", "vtt_am_den"})

    # ---- 8. the monsters
    monsters(m)

    # ---- 9, 10
    m.dress_barriers()
    reeds(m)
    m.scatter()
    m.obj("Cổng Đông", "prop", (W - 2) * T, GATE_Y * T - 8, 32, 40, sprite="portal")
    m.obj("to_village", "portal", (W - 1) * T - 4, GATE_Y * T, T + 12, 4 * T, target="truc_lam_thon",
          target_spawn="from_lake")
    m.sign("Về Trúc Lâm Thôn", "Đông → Trúc Lâm Thôn", W - 5, GATE_Y - 2)
    m.poi("gate", "Cổng Đông · về Trúc Lâm Thôn", W - 2, GATE_Y + 1)
    m.obj("spawn", "spawn", SPAWN[0] * T, SPAWN[1] * T, 1, 1)
    m.obj("from_village", "spawn", SPAWN[0] * T, SPAWN[1] * T, 1, 1)
    return m.finish({"music": "forest", "safe": "false"}, ring="tree",
                    gaps={("e", y) for y in range(GATE_Y, GATE_Y + 4)})


# ------------------------------------------------------------------ the islands
def island_seeds(m, rng) -> tuple[list, dict]:
    """(seeds, radius): (id, tile, khu id) of every island and its radius in tiles."""
    seeds: list[tuple] = []
    radius: dict[str, float] = {}

    def add(sid, tile, kid, r):
        seeds.append((sid, tuple(tile), kid))
        radius[sid] = r

    special = [
        ("vtt_trai_ben", CAMP1, "vtt_ben_suong", 12), ("vtt_tram_suong", CAMP2, "vtt_dao_suong", 10),
        ("vtt_am_den", CAMP3, "vtt_dam_sau", 10),
        ("n_lau", LAU, "vtt_lau_say", 9), ("n_dom", DOM_DOM, "vtt_dom_dom", 9),
        ("n_kim", KIM, "vtt_thach_ban", 8), ("n_fog", FOG, "vtt_dao_suong", 10),
        ("n_phao", PHAO, "vtt_cau_phao", 6), ("n_mieu", (MIEU[0], MIEU[1] + 6), "vtt_mieu_chim", 7),
        ("n_co_thu", CO_THU, "vtt_dam_sau", 5.5), ("n_ngac", NGAC, "vtt_huyet_dam", 9),
    ]
    for sid, tile, kid, r in special:
        add(sid, tile, kid, r)
    rects = {"vtt_lau_say": (215, 0, 319, 79), "vtt_ben_suong": (215, 80, 319, 159),
             "vtt_dom_dom": (215, 160, 319, 239), "vtt_thach_ban": (105, 0, 214, 79),
             "vtt_dao_suong": (105, 80, 214, 159), "vtt_cau_phao": (105, 160, 214, 239),
             "vtt_mieu_chim": (0, 0, 104, 79), "vtt_dam_sau": (0, 80, 104, 159), "vtt_huyet_dam": (0, 160, 104, 239)}
    corner = (258, 88, 292, 126)
    for kid, (x0, y0, x1, y1) in rects.items():
        # islands keep off the channels between the bands (wide water: x near 105 and 215)
        rect = (x0 + (8 if x0 else 0), y0, x1 - (8 if x1 < 319 else 0), y1)
        have = [s[1] for s in seeds]
        spacing = 21 if kid != "vtt_dam_sau" else 24
        pts = spread(rng, rect, spacing, fixed=have, margin=5,
                     avoid=lambda x, y: corner[0] - 4 <= x <= corner[2] + 2 and corner[1] - 6 <= y <= corner[3])
        for n, p in enumerate(pts):
            add(f"{kid}_{n}", p, kid, spacing * (0.56 + 0.14 * rng.random()))
    # the deep water round the old tree: its neighbours are small
    for sid, tile, kid in seeds:
        if kid == "vtt_dam_sau" and sid not in ("vtt_am_den", "n_co_thu"):
            if math.dist(tile, CO_THU) < 26:
                radius[sid] = min(radius[sid], 6)
    return seeds, radius


def dry_ground() -> list[tuple]:
    """Rectangles that stay land whatever the islands do: the gate, Ngư Ông's shore."""
    W = SIZE[0]
    return [(W - 12, GATE_Y - 4, W - 2, GATE_Y + 6),
            (NGU_ONG[0] - 12, NGU_ONG[1] - 1, NGU_ONG[0] + 18, NGU_ONG[1] + 8)]


def lake_corner(m) -> None:
    """Hồ Nghiên Mực as the small map had it, moved: the lake north of the shore, the dock into
    it, the fishing area over it (what the server checks a cast against)."""
    nx, ny = NGU_ONG
    lake = m.blob(nx + 2, ny - 13, 15, 9, salt=33)
    lake |= {(x, y) for x in range(nx - 10, nx + 16) for y in range(ny - 10, ny - 1)}
    lake = {(x, y) for (x, y) in lake if y <= ny - 2}
    m._wet(lake, "water0", SOLID_WATER, None)
    x0, y0, x1, y1 = DOCK
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            j = m.i(x, y)
            m.hard[j] = 0
            m.road[j] = 2
            m.setg(x, y, "wood0")
    for x in range(nx - 10, nx + 16):                  # the stone shore
        if not m.road[m.i(x, ny - 1)]:
            m.setg(x, ny - 1, "stone0")
    xs = [x for x, _ in lake]
    ys = [y for _, y in lake]
    m.obj("lake_0", "area", min(xs) * T, min(ys) * T, (max(xs) - min(xs) + 1) * T, (max(ys) - min(ys) + 1) * T,
          kind="fishing", pool="ho")
    m.lake_rect = (min(xs), min(ys), max(xs), max(ys))


def moats(m) -> None:
    """Miếu Chìm stands in a ring of water (its island is reached by one plank, later); the old
    tree's islet too."""
    mx, my = MIEU
    ring = {(x, y) for x in range(mx - 5, mx + 6) for y in range(my - 4, my + 4)
            if not (mx - 3 <= x <= mx + 3 and my - 2 <= y <= my + 1)}
    m._wet(ring, "water0", SOLID_WATER, None)
    m.open_tiles({(x, y) for x in range(mx - 3, mx + 4) for y in range(my - 2, my + 2)}, "stone0")


def graph_edges(m, cells: Cells, rng, ri: dict) -> list[tuple]:
    out: list[tuple] = []

    def add(a, b):
        if a != b and not any({a, b} == {x, y} for x, y in out):
            out.append((a, b))

    def leaf_only(pairs, leaves):
        keep = []
        for lf in leaves:
            mine = [p for p in pairs if lf in p]
            if mine:
                keep.append(min(mine, key=lambda p: cells.dist(*p)))
        return [p for p in pairs if not any(lf in p for lf in leaves)] + keep

    extra = {"lau": 3, "ben": 2, "dom": 3, "thach": 2, "suong": 3, "phao": 2, "mieu": 1, "co": 1, "huyet": 2}
    for key, n in extra.items():
        pairs = cells.same_khu_pairs(ri[key])
        if key == "co":
            pairs = leaf_only(pairs, ["n_co_thu"])
        if key == "mieu":
            pairs = leaf_only(pairs, ["n_mieu"])
        for a, b in cells.tree(pairs, rng, extra=n):
            add(a, b)
    add("gate", "vtt_trai_ben")
    add("vtt_trai_ben", "n_ngu_ong")
    # between the khu: within a band, two boardwalks; across the channels, the long ones
    for a, b, p in (("lau", "ben", (262, 80)), ("ben", "dom", (262, 160)), ("lau", "ben", (300, 80)),
                    ("ben", "dom", (232, 160)), ("thach", "suong", (160, 80)), ("suong", "phao", (160, 160)),
                    ("thach", "suong", (196, 80)), ("mieu", "co", (52, 80)), ("co", "huyet", (52, 160)),
                    ("thach", "lau", (215, 40)), ("phao", "dom", (215, 200)), ("mieu", "thach", (105, 40)),
                    ("huyet", "phao", (105, 200))):
        add(*cells.link(ri[a], ri[b], p))
    ben_w = cells.link(ri["ben"], ri["suong"], (215, 119))[0]
    add(ben_w, "vtt_tram_suong")
    co_e = cells.link(ri["co"], ri["suong"], (105, 119))[1]
    add(co_e, "vtt_am_den")
    return out


def spine_edges(edges, tiles: dict, stops: list[str]) -> set:
    import heapq
    adj: dict[str, list] = {}
    for a, b in edges:
        w = math.dist(tiles[a], tiles[b])
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))
    out = set()
    for s, t in zip(stops, stops[1:]):
        dist, prev, q = {s: 0.0}, {}, [(0.0, s)]
        while q:
            d, u = heapq.heappop(q)
            if u == t:
                break
            if d > dist.get(u, 1e18):
                continue
            for v, w in adj.get(u, ()):
                if d + w < dist.get(v, 1e18):
                    dist[v], prev[v] = d + w, u
                    heapq.heappush(q, (d + w, v))
        u = t
        while u in prev:
            out.add(frozenset((u, prev[u])))
            u = prev[u]
    return out


# ------------------------------------------------------------------ the places
def _free(m, x, y) -> bool:
    j = m.i(x, y)
    return not (m.road[j] or m.hard[j] or (x, y) in m.blocked_tiles)


def thing_at(m, name, sprite, x, y, w, h, foot=None, **kw) -> None:
    if m.inside(x, y, 2) and _free(m, x, y):
        m.thing(name, sprite, x, y, w, h, foot=foot, **kw)


def tree_at(m, x, y, sprite="tree") -> None:
    if m.inside(x, y, 2) and _free(m, x, y):
        m.tree(x, y, sprite)
        m.blocked_tiles.update({(x - 1, y), (x, y), (x + 1, y), (x, y - 1)})


def places(m) -> None:
    # Ngư Ông's corner, as on the small map (moved by OX, OY)
    def at(x, y):
        return x + OX, y + OY
    m.building("Lều Ngư Ông", "hut", *at(18, 28), 64, 56, 30)
    m.npc("Ngư Ông", "fisher", *at(25, 27), action="fisher")
    tx, ty = at(31, 28)
    m.obj("Bảng Ngư Phổ", "interact", tx * T, ty * T, 16, 24, sprite="tablet", action="fish_book")
    m.solid(tx * T + 2, ty * T + 16, 12, 8)
    m.reserve(tx * T, ty * T, 16, 24)
    for i, (lx, ly) in enumerate((at(26, 26), at(29, 26))):
        m.obj("lantern", "prop", lx * T + 4, ly * T - 16, 8, 24, sprite="lantern", variant=i)
    m.tree(*at(23, 26), "tree")                                   # the willow by the dock
    for x in range(NGU_ONG[0] - 12, NGU_ONG[0] + 18):
        for y in range(NGU_ONG[1] - 1, NGU_ONG[1] + 8):
            m.blocked_tiles.add((x, y))
    m.poi("npc", "Ngư Ông · Hồ Nghiên Mực", *NGU_ONG)
    lx0, ly0, lx1, ly1 = m.lake_rect
    m.poi("landmark", "Hồ Nghiên Mực", (lx0 + lx1) // 2, (ly0 + ly1) // 2)
    # Đình Gió Lau: a tablet among the reeds
    x, y = LAU
    thing_at(m, "Bia Gió Lau", "tablet", x + 2, y - 2, 16, 24, foot=(12, 8))
    for i, (dx, dy) in enumerate(((-3, -2), (3, 2), (-3, 2))):
        thing_at(m, "Đèn", "lantern", x + dx, y + dy, 8, 24, foot=(4, 4), variant=i)
    m.sign("Đình Gió Lau", "Gió thổi lau rạp về đâu? Không ai biết trước,\nchỉ biết khả năng của mỗi hướng.", x - 2, y + 3)
    m.poi("landmark", "Đình Gió Lau", x, y)
    # Bãi Đom Đóm: lanterns scattered like fireflies
    x, y = DOM_DOM
    for i, (dx, dy) in enumerate(((-4, -3), (3, -4), (5, 1), (-5, 2), (0, 4), (2, -1))):
        thing_at(m, "Đèn đom đóm", "lantern", x + dx, y + dy, 8, 24, foot=(4, 4), variant=i + 10)
    m.poi("landmark", "Bãi Đom Đóm", x, y)
    # Thạch Bàn: the mossy rock of Bích Nhãn Kim Thiềm
    x, y = KIM
    for i, (dx, dy) in enumerate(((-3, -1), (3, -1), (0, -3), (-2, 2), (3, 2))):
        thing_at(m, "Đá rêu", "boulder", x + dx, y + dy, 32, 24, foot=(26, 10), variant=i)
    m.poi("beast", "Thạch Bàn · Bích Nhãn Kim Thiềm", x, y)
    # Đảo Sương: clouds, a lantern
    x, y = FOG
    for i, (dx, dy) in enumerate(((-3, -2), (3, -3), (-4, 2), (4, 2), (0, -4))):
        thing_at(m, "Sương", "cloud_puff", x + dx, y + dy, 32, 20, variant=i)
    thing_at(m, "Đèn đảo", "lantern", x - 1, y + 3, 8, 24, foot=(4, 4), variant=3)
    m.poi("beast", "Đảo Sương · Huyền Quy", x, y)
    # Cầu Phao Chín Nhịp
    x, y = PHAO
    m.sign("Cầu Phao", "Cầu Phao Chín Nhịp: mỗi nhịp một lần tung đồng xu,\nqua đủ chín nhịp là tới bờ.", x + 2, y - 2)
    m.poi("landmark", "Cầu Phao Chín Nhịp", x, y)
    # Miếu Chìm
    x, y = MIEU
    m.thing("Miếu Chìm", "shrine", x, y - 1, 32, 44, foot=(28, 12))
    for i, dx in enumerate((-2, 2)):
        thing_at(m, "Đèn miếu", "lantern", x + dx, y, 8, 24, foot=(4, 4), variant=i + 20)
    m.poi("landmark", "Miếu Chìm", x, y)
    # the old tree in the deep water
    x, y = CO_THU
    m.tree(x, y - 1, "tree")
    m.blocked_tiles.update({(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x, y - 2)})
    for i, (dx, dy) in enumerate(((-3, -1), (3, 0))):
        tree_at(m, x + dx, y + dy, "tree")
    thing_at(m, "Đèn gốc cây", "lantern", x + 2, y + 2, 8, 24, foot=(4, 4), variant=31)
    thing_at(m, "Rễ cổ thụ", "log", x - 2, y + 2, 24, 16)
    m.poi("landmark", "Cổ Thụ Giữa Đầm", x, y - 1)
    # Bến Ngạc Đỏ: dead trees round a pale shore
    x, y = NGAC
    for i, (dx, dy) in enumerate(((-4, -2), (4, -2), (-3, 3), (4, 3))):
        tree_at(m, x + dx, y + dy, "ink_tree")
    thing_at(m, "Đá", "rock", x + 1, y - 3, 16, 12, foot=(12, 8))
    m.poi("landmark", "Bến Ngạc Đỏ", x, y)


def glide_islets(m) -> None:
    """Two islets no bridge reaches (Đạp Kiếm Lướt): a 3 x 2 ground in a ring of water two tiles
    wide, a ledge of stone where the glide starts; a crystal on each, nothing to claim."""
    reach = m.reach()
    for name, want, sprite in (("Bãi Sen Ngọc", (132, 140), "crystal"), ("Đảo Lưu Ly", (24, 50), "crystal")):
        best = None
        for cy in range(want[1] - 18, want[1] + 19):
            for cx in range(want[0] - 18, want[0] + 19):
                win = [(x, y) for x in range(cx - 3, cx + 4) for y in range(cy - 3, cy + 3)]
                if not all(m.inside(x, y, 3) and m.hard[m.i(x, y)] == SOLID_WATER and not m.road[m.i(x, y)]
                           for x, y in win):
                    continue
                ledge = (cx, cy + 3)
                if not (m.inside(*ledge, 3) and not m.hard[m.i(*ledge)] and reach[m.i(*ledge)]):
                    continue
                d = abs(cx - want[0]) + abs(cy - want[1])
                if best is None or d < best[0]:
                    best = (d, cx, cy)
        if best is None:
            continue
        _d, cx, cy = best
        islet = {(x, y) for x in range(cx - 1, cx + 2) for y in (cy - 1, cy)}
        m.open_tiles(islet, "stone0")
        m.thing(name, sprite, cx, cy - 1, 24, 32, variant=7)
        m.blocked_tiles.update(islet)
        m.poi("landmark", name, cx, cy - 1)


def reeds(m) -> None:
    """Reeds along the shores: tall grass on some land tiles next to the water."""
    W, H = m.W, m.H
    for y in range(3, H - 3):
        for x in range(2, W - 2):
            j = y * W + x
            if m.hard[j] or m.road[j] or m.keep[j] or (x, y) in m.blocked_tiles:
                continue
            if not any(m.hard[m.i(x + dx, y + dy)] == SOLID_WATER for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                continue
            if m.noise.value(x, y, 4.0, 91) < 0.62:
                continue
            m.thing("Lau sậy", "tall_grass", x, y, 24, 16, variant=(x * 7 + y) % 1000)


# ------------------------------------------------------------------ the monsters
def monsters(m) -> None:
    """Band 1: Đầu Tử Oa and U Minh Đăng; band 2: the same with their higher nodes and a few
    elites; band 3: only the elites (no normal creature of the marsh reaches tầng 7)."""
    hand = []
    x, y = MIEU
    m.monster_area("vtt_mieu_chim", "ho_lo_tinh", (x - 6, y - 2, x + 6, y + 8), 1, name="ho_lo_tinh_mieu_chim")
    hand.append((x - 6, y - 2, x + 6, y + 8))
    sk = lambda r: overlaps(r, hand)  # noqa: E731
    kw = dict(cell=(18, 14), tiles_per=190, min_walk=0.6, skip=sk)
    fill(m, "vtt_lau_say", [("dau_tu_oa", 3), ("u_minh_dang", 1)], **kw)
    fill(m, "vtt_ben_suong", [("dau_tu_oa", 3), ("u_minh_dang", 1)], **kw)
    fill(m, "vtt_dom_dom", [("u_minh_dang", 3), ("dau_tu_oa", 1)], **kw)
    fill(m, "vtt_thach_ban", [("dau_tu_oa", 2), ("u_minh_dang", 2)], [("huyet_ngac", 1), ("ho_lo_tinh", 2)], **kw)
    fill(m, "vtt_dao_suong", [("u_minh_dang", 2), ("dau_tu_oa", 2)], [("ho_lo_tinh", 1), ("huyet_ngac", 2)], **kw)
    fill(m, "vtt_cau_phao", [("dau_tu_oa", 2), ("u_minh_dang", 2)], [("huyet_ngac", 2), ("ho_lo_tinh", 1)], **kw)
    ekw = dict(cell=(16, 13), tiles_per=1e9, min_walk=0.35, skip=sk)
    fill(m, "vtt_mieu_chim", [("ho_lo_tinh", 1), ("huyet_ngac", 1)], max_areas=6, **ekw)
    fill(m, "vtt_dam_sau", [("huyet_ngac", 1), ("ho_lo_tinh", 1)], max_areas=6, **ekw)
    fill(m, "vtt_huyet_dam", [("huyet_ngac", 2), ("ho_lo_tinh", 1)], max_areas=7, **ekw)
