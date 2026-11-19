"""Tower-defence kit at the board's NATIVE 24 px cell: towers (7 roles x 3 levels, math-area silhouettes), core, spawn rift,
rocks, projectiles and hit puffs. Frames 24x30, the ground point of the cell is the pivot."""
from __future__ import annotations

import math

import wt_common as C
from wt_common import mat
from wt_village import X, Y, Z, bx, cy, bl, tubep, shadow
from wt_garden import tb, tbl

# role -> (old role name, math tower id, Vietnamese name, signature)
TOWERS = [
    ("hoa", "tap_hop", "Tháp Tập Hợp", "bronze cauldron on a tripod, an orbit of embers"),
    ("thuy", "so_phuc", "Tháp Số Phức", "spiral coil of blue light around a rod"),
    ("kim", "vecto", "Tháp Vectơ", "arrow ballista on a swivel"),
    ("son", "ma_tran", "Tháp Ma Trận", "cube-lattice pylon with glowing nodes"),
    ("quang", "xac_suat", "Tháp Xác Suất", "urn mortar with dice rising from the mouth"),
    ("ho_tro", "gradient", "Tháp Gradient", "slope ramp with a lens throwing a beam"),
    ("moc", "moc", "Tường Mộc", "palisade of stakes (the wall tower)"),
]


def plinth(col, w=16, h=3):
    shadow(col, 0, 3, w / 2 + 1, 4)
    bx(col, 0, 0.5, 0, w, 8, h, mat("stone", 1), bevel=0.8)


def t_hoa(col, lv):
    plinth(col)
    for sx in (-1, 0, 1):
        bx(col, sx * 5, 2.4 + (sx == 0) * 1.5, 3, 1.8, 1.8, 4 + lv, mat("wood", 0))
    r = 6 + lv
    cy(col, 0, 4.0, 5 + lv, r, 5 + lv, mat("gold", 1), seg=12, r1=r - 2)
    cy(col, 0, 4.0, 10 + 2 * lv, r - 2, 0.8, mat("lava", 2, emit=1.4), seg=12)
    bl(col, 0, 4, 11 + 2 * lv, 2 + lv * 0.8, 3 + lv, mat("lava", 3, emit=1.8, prio=3.0), sub=1)
    for k in range(lv):
        a = k * 2.1 + 0.5
        bl(col, 8 * math.cos(a), 4 + 3 * math.sin(a), 15 + 2 * lv + 2 * math.sin(a), 1.2, 1.2, mat("lava", 3, emit=2.6, prio=4.0), sub=1)


def t_thuy(col, lv):
    plinth(col)
    bx(col, 0, 2.5, 3, 2.4, 2.4, 9 + 4 * lv, mat("stone", 2), bevel=0.5)
    turns = 1.0 + lv * 0.8
    pts = []
    for i in range(16):
        t = i / 15
        a = t * turns * 2 * math.pi
        pts.append((math.cos(a) * 5.2, 3 + math.sin(a) * 2.6, 4 + t * (8 + 4 * lv)))
    tubep(col, pts, 1.3, mat("crys_c", 2, emit=1.7, prio=2.0), seg=4)
    if lv >= 3:
        bl(col, 0, 3, 22, 2.6, 2.6, mat("crys_c", 3, emit=2.4, prio=3.0), sub=1)
    elif lv == 2:
        bl(col, 0, 3, 17, 1.8, 1.8, mat("crys_c", 3, emit=2.0, prio=3.0), sub=1)


def t_kim(col, lv):
    plinth(col)
    bx(col, 0, 2.5, 3, 4, 4, 5, mat("wood", 1), bevel=0.6)
    arm = 7 + lv * 1.5
    for sx in (-1, 1):
        tubep(col, [(0, 3, 9), (sx * arm, 2.0, 11 + lv * 0.5)], 1.2, mat("gold" if lv == 3 else "wood", 2 if lv == 3 else 1), seg=4)
    tubep(col, [(-arm, 2.0, 11), (0, 1, 9.5), (arm, 2.0, 11)], 0.35, mat("steel", 3), seg=3)
    ln = 10 + 3 * lv
    for k in range(1 if lv < 2 else 2):
        o = -1.8 if k else 0
        tubep(col, [(-3, 3 + o, 9.5 + o), (ln * 0.6, 3 + o, 9.5 + ln * 0.5 + o)], 0.9, mat("steel", 2), seg=4)
        bl(col, ln * 0.6, 3 + o, 9.5 + ln * 0.5 + o, 1.6, 1.8, mat("gold", 3) if lv < 3 else mat("glow_y", 3, emit=2.2, prio=3.0), sub=1)


def t_son(col, lv):
    """Cube-lattice pylon: wire cubes stacked on a plinth, glowing nodes at the corners."""
    plinth(col)
    for z in range(lv):
        s = 10 - z * 1.2
        z0 = 3.5 + z * (s * 0.9)
        d0 = 3 - s * 0.25
        edge = mat("earth", 2 if z % 2 else 1)
        for sx in (-1, 1):
            for sy in (0, 1):
                bx(col, sx * s / 2, d0 + sy * s * 0.5, z0, 1.5, 1.5, s, edge)          # four posts
        for zz in (0, 1):
            for sy in (0, 1):
                bx(col, 0, d0 + sy * s * 0.5, z0 + zz * (s - 1.5), s, 1.4, 1.5, edge)    # beams along x
            for sx in (-1, 1):
                bx(col, sx * s / 2, d0, z0 + zz * (s - 1.5), 1.4, s * 0.5, 1.5, edge)     # beams along depth
        for sx in (-1, 1):
            bl(col, sx * s / 2, d0, z0 + s, 1.3, 1.3, mat("glow_y", 3, emit=2.4, prio=4.0), sub=1)
        bl(col, 0, d0 + s * 0.25, z0 + s * 0.5, 1.8, 1.8, mat("glow_y", 2, emit=1.4, prio=2.0), sub=1)


def t_quang(col, lv):
    plinth(col)
    cy(col, 0, 4, 3, 6.5, 8, mat("earth", 1), seg=12, r1=5.0)
    cy(col, 0, 4, 11, 5.3, 1.6, mat("earth", 2), seg=12, r1=6.2)
    bl(col, 0, 4, 12, 4.3, 0.8, mat("basalt", 0), sub=1)
    for k in range(lv):
        a = (k - (lv - 1) / 2) * 1.5
        x, z = a * 4.2, 14 + k * 2.2 + 2.5 * (k % 2)
        bx(col, x, 2.6, z, 4.2, 4.2, 4.2, mat("white", 2), bevel=0.5, rot=0.5 * k)
        bl(col, x, 0.7, z + 2.1, 0.55, 0.55, mat("basalt", 0), sub=1)
        bl(col, x + 1.1, 0.7, z + 3.1, 0.55, 0.55, mat("basalt", 0), sub=1)
    bl(col, 0, 3, 13 + 3 * lv, 1.2 + lv * 0.5, 1.2 + lv * 0.5, mat("glow_y", 3, emit=2.0, prio=3.0), sub=1)


def t_hotro(col, lv):
    plinth(col)
    bx(col, 0, 2.5, 3, 12, 6, 2.4, mat("wood", 1), bevel=0.5)
    C.box(col, "ramp", (X(-1.5), Y(3.0), Z(3 + 3 + lv)), (X(10 + lv), Y(5), Z(3 + 2.5 * lv)), mat("foliage", 1 + (lv > 1)), rot_z=0.0, bevel=X(0.5))
    ob = col.objects[-1]
    ob.rotation_euler = (0, -0.5, 0)
    r = 3.6 + lv * 0.5
    C.cyl(col, "lens", (0, 0, 0), X(r), X(r), Z(1.2), mat("glow_g", 2, emit=1.6, prio=2.0), seg=14)
    ob = col.objects[-1]
    ob.rotation_euler = (math.pi / 2, 0, 0)
    ob.location = (X(4.0), Y(1.2), Z(12 + 2 * lv))
    if lv >= 2:
        tubep(col, [(4, 1, 12 + 2 * lv), (8 + 2 * lv, 1, 15 + 3 * lv)], 0.8, mat("glow_g", 3, emit=2.2, prio=3.0), seg=4)
    if lv >= 3:
        bl(col, 4, 1, 12 + 2 * lv, 1.6, 1.6, mat("glow_g", 3, emit=2.8, prio=4.0), sub=1)


def t_moc(col, lv):
    shadow(col, 0, 3, 9, 4)
    n = 2 + lv * 1
    for k in range(n):
        x = (k - (n - 1) / 2) * (13 / max(n - 1, 1))
        h = 8 + lv * 3 + (k % 2) * 2
        cy(col, x, 3 + (k % 2), 0, 2.0, h, mat("wood", 1 + (k % 2)), seg=6, r1=1.4)
        bl(col, x, 3 + (k % 2), h + 1, 1.5, 2.2, mat("gold", 2) if lv == 3 else mat("wood", 2), sub=1)
    tubep(col, [(-7, 2.5, 5), (0, 2, 4.2), (7, 2.5, 5)], 0.7, mat("red" if lv == 3 else "earth", 1), seg=4)
    if lv >= 2:
        tubep(col, [(-7, 2.5, 5 + 5), (0, 2, 4.2 + 5), (7, 2.5, 5 + 5)], 0.7, mat("steel", 1), seg=4)


TOWER_FN = {"hoa": t_hoa, "thuy": t_thuy, "kim": t_kim, "son": t_son, "quang": t_quang, "ho_tro": t_hotro, "moc": t_moc}


def tower_builder(role, lv):
    def b(col, f):
        TOWER_FN[role](col, lv)
    return b


# --------------------------------------------------------------------------- core, spawn, rock
def core(col, f):
    shadow(col, 0, 3, 9, 4)
    bx(col, 0, 0.5, 0, 18, 8, 3, mat("stone", 2), bevel=0.8)
    bx(col, 0, 1.5, 3, 12, 6, 3, mat("stone", 1), bevel=0.8)
    p = (1.0, 1.3, 1.6, 1.3)[f % 4]
    C.cone(col, "crystal", (X(0), Y(3), Z(6)), X(4.6), Z(16), mat("crys_c", 2, emit=1.4 * p, prio=2.0), seg=6)
    C.cone(col, "crystal2", (X(-5), Y(3.5), Z(6)), X(2.6), Z(9), mat("crys_c", 3, emit=1.6 * p), seg=6)
    bl(col, 5, 3, 9, 1.0, 1.0, mat("crys_c", 3, emit=2.6, prio=4.0), sub=1)


def spawn(col, f):
    shadow(col, 0, 3, 10, 4)
    a = f * math.pi / 2
    cy(col, 0, 4, 0, 10, 2, mat("basalt", 1), seg=14, r1=9)
    cy(col, 0, 4, 2, 7.5, 0.8, mat("ink", 0), seg=14)
    for k in range(3):
        b = a + k * 2.1
        bl(col, 5.5 * math.cos(b), 4 + 5.5 * math.sin(b) * 0.57, 4, 1.4, 1.4, mat("mist", 3, emit=2.2, prio=3.0), sub=1)
    for k in range(2):
        b = -a * 1.5 + k * 3.1
        bl(col, 3 * math.cos(b), 4 + 3 * math.sin(b) * 0.57, 3.2, 1.0, 1.0, mat("mist", 2, emit=1.6, prio=2.0), sub=1)


def rock(v):
    def b(col, f):
        shadow(col, 0, 3, 9, 4)
        bl(col, 0, 3, 4.5, 8, 5.4, mat("stone", 1), sub=1, rough=0.28, ry=6)
        bl(col, -2, 2.5, 7.5, 4.2, 3, mat("stone", 2), sub=1, ry=3)
        if v:
            bl(col, 4, 1.5, 3, 2.6, 2.4, mat("stone", 1), sub=1)
            bl(col, -1, 3, 9.2, 3.0, 1.2, mat("foliage", 1), sub=1)
    return b


# --------------------------------------------------------------------------- projectiles and hits (face-on, drawn like icons)
def shot(role):
    def b(col, f):
        k = f % 3
        if role == "kim":
            tubep(col, [(-5, 0, 3), (4, 0, 3)], 0.7, mat("steel", 3), seg=4)
            bl(col, 5, 0, 3, 1.6, 1.0, mat("gold", 3), sub=1)
            bl(col, -5.5, 0, 3, 0.8, 1.6 + f * 0.3, mat("white", 2), sub=1)
            return
        kind = {"hoa": "lava", "thuy": "crys_c", "son": "glow_y", "quang": "glow_y"}[role]
        r = 2.6 + 0.5 * (k == 1)
        bl(col, 0, 0, 4, r, r, mat(kind, 2 if role in ("hoa", "thuy") else 3, emit=2.2, prio=3.0), sub=1)
        for j in range(2):
            bl(col, -2.6 - j * 2.4, 0, 4 + (k - 1) * 0.8, r * 0.6, r * 0.6, mat(kind, 3 - j if role != "son" else 3, emit=1.6), sub=1)
        if role == "son":
            bl(col, 0, 0, 4, r * 1.2, r * 1.0, mat("rock", 1), sub=1)
    return b


def hit(role):
    def b(col, f):
        r = 1.5 + f * 1.6
        kind = {"hoa": "lava", "thuy": "crys_c", "kim": "white", "son": "glow_y", "quang": "glow_y", "puff": "bone"}[role]
        n = 8
        em = role != "puff"
        for k in range(n):
            a = k * 2 * math.pi / n + f * 0.2
            sz = max(0.7, 2.2 - f * 0.4)
            m = mat(kind, 3 if em else 2, emit=2.0 if em else 0.0, prio=3.0)
            bl(col, r * math.cos(a), r * math.sin(a), 8, sz, sz, m, sub=1)
        if role == "kim":
            for s in (-1, 1):
                tubep(col, [(-r, -s * r, 8), (r, s * r, 8)], 0.7, mat("white", 3, emit=2.0, prio=3.0), seg=4)
        elif f < 2 and role != "puff":
            bl(col, 0, 0, 8, 4 - f * 1.4, 4 - f * 1.4, mat(kind, 3, emit=2.6, prio=4.0), sub=1)
    return b


def specs():
    out = []
    mk = lambda **k: out.append(k)
    for role, mid, vi, sig in TOWERS:
        for lv in (1, 2, 3):
            mk(name=f"tower_{role}_{lv}", W=24, H=30, base=3, ppm=34 if role != "ho_tro" else 28, build=tower_builder(role, lv), vi=f"{vi} cấp {lv}",
               extra={"role": role, "math_tower": mid, "level": lv, "silhouette": sig})
    mk(name="td_core", W=24, H=28, frames=4, base=3, ppm=38, build=core, vi="Lõi linh khí", extra={"old": "the blue circle at the core cell"})
    mk(name="td_spawn", W=24, H=24, frames=4, base=3, ppm=38, build=spawn, vi="Cửa quái", extra={"old": "the dark circle at the spawn cell"})
    for v in (0, 1):
        mk(name=f"td_rock_{v}", W=20, H=16, base=2, ppm=32, build=rock(v), vi="Đá", extra={"old": f"B.rock({v})"})
    for role in ("hoa", "thuy", "kim", "son", "quang"):
        mk(name=f"shot_{role}", W=20 if role == "kim" else 16, H=12 if role == "kim" else 16, frames=2 if role == "kim" else 3, mode="top", ppm=44,
           build=shot(role), vi="Đạn", pivot=((20 if role == "kim" else 16) // 2, (12 if role == "kim" else 16) // 2),
           extra={"role": role, "note": "points to the right; the game rotates it to the target; pivot = centre"})
    for role in ("hoa", "thuy", "kim", "son", "quang", "puff"):
        mk(name=f"hit_{role}", W=24, H=24, frames=4, mode="top", ppm=40, build=hit(role), vi="Hiệu ứng trúng", pivot=(12, 12),
           extra={"role": role, "note": "4 frames, expanding; pivot = centre; draw additively or normally"})
    return out
