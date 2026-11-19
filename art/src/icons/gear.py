"""trang_bi atlas: six slots (ao, mu, giay, gang, nhan, day_chuyen) x four tiers (1, 3, 5, 7):
plain cloth -> jade-green silk -> spirit glow -> ice with small wings."""
import math

from lib import W, leaf, sparkle, stars_at

SLOTS = ["ao", "mu", "giay", "gang", "nhan", "day_chuyen"]
SLOT_VI = {"ao": "Áo", "mu": "Mũ", "giay": "Giày", "gang": "Găng", "nhan": "Nhẫn", "day_chuyen": "Dây Chuyền"}
TIERS = [1, 3, 5, 7]
TIER_VI = {1: "Vải Thô", 3: "Bích Lụa", 5: "Linh Quang", 7: "Băng Dực"}
IDS = ["%s_%d" % (s, t) for t in TIERS for s in SLOTS]

TH = {
    1: dict(main="cloth_b", dark="cloth_d", trim="clay", metal="iron_d", gem=None, glow=None, hi="clay"),
    3: dict(main="jade", dark="jade_d", trim="gold", metal="bronze", gem="jade_l", glow=None, hi="jade_l"),
    5: dict(main="blue", dark="blue_d", trim="gold_d", metal="gold", gem="violet", glow="cyan", hi="blue_l"),
    7: dict(main="ice_w", dark="blue_l", trim="gold", metal="gold", gem="ice", glow="ice_hi", hi="porcelain"),
}


def wing_pair(w, key, c, length=0.2, wid=0.07, n=3, rise=62, step=14, y=0.05):
    for sx in (-1, 1):
        for k in range(n):
            leaf(w, key, (c[0] + sx * 0.0, c[1] + k * 0.014), sx * (rise + k * step), length - k * 0.03, wid,
                 thick=0.014, y=y)


# ----------------------------------------------------------------- ao (robe)
def ao(w, t):
    th = TH[t]
    torso = [(-0.15, -0.23), (0.15, -0.23), (0.145, 0.0), (0.12, 0.14), (0.05, 0.19), (-0.05, 0.19), (-0.12, 0.14),
             (-0.145, 0.0)]
    w.poly(th["main"], torso, -0.04, 0.04, bevel=0.006)
    for sx in (-1, 1):  # sleeves hang to the sides
        sl = [(sx * 0.11, 0.17), (sx * 0.17, 0.15), (sx * 0.32, -0.12), (sx * 0.30, -0.2), (sx * 0.19, -0.17),
              (sx * 0.12, 0.0)]
        w.poly(th["main"], sl if sx > 0 else sl[::-1], -0.05, 0.05, bevel=0.006)
        # cuff
        w.box(th["trim"] if t > 1 else th["dark"], (sx * 0.255, -0.045, -0.165), (0.12, 0.11, 0.034),
              rot=(0, sx * -42, 0), bevel=0.003)
    # neck opening and crossed collar
    w.poly(th["dark"], [(-0.05, 0.19), (0.05, 0.19), (0.0, 0.10)], -0.045, 0.045, bevel=0.002)
    for sx in (-1, 1):
        w.box(th["trim"] if t > 1 else th["hi"], (sx * 0.035, -0.047, 0.115), (0.015, 0.012, 0.13),
              rot=(0, sx * 28, 0), bevel=0)
    # belt
    w.box(th["dark"] if t == 1 else th["metal"], (0.0, -0.045, -0.05), (0.30, 0.02, 0.05), bevel=0.003)
    w.box("clay" if t == 1 else th["trim"], (0.0, -0.058, -0.05), (0.05, 0.016, 0.055), bevel=0.003)
    # hem
    if t > 1:
        w.box(th["glow"] or th["trim"], (0.0, -0.043, -0.215), (0.29, 0.012, 0.018), bevel=0)
    if t == 1:
        w.box("cloth_d", (0.07, -0.043, -0.15), (0.05, 0.012, 0.045), bevel=0)  # patch
        w.box("clay", (-0.08, -0.043, 0.04), (0.04, 0.012, 0.03), bevel=0)
    if t >= 5:
        w.sph(th["gem"], (0.0, -0.055, 0.07), 0.026, scale=(1, 0.5, 1), seg=6)
        w.torus(th["glow"], (0, -0.046, -0.14), 0.05, 0.009, rot=(90, 0, 0), seg=10, tseg=4)
        for sx in (-1, 1):
            w.box(th["glow"], (sx * 0.085, -0.043, -0.15), (0.012, 0.01, 0.12), bevel=0)
    if t == 3:
        w.torus("gold", (0, -0.046, -0.14), 0.045, 0.008, rot=(90, 0, 0), seg=10, tseg=4)
        w.sph("jade_l", (0.0, -0.058, 0.07), 0.022, scale=(1, 0.5, 1), seg=6)
    if t == 7:
        wing_pair(w, "porcelain", (0.0, 0.17), length=0.24, wid=0.08, rise=55, step=15, y=0.07)
        for sx in (-1, 1):
            w.ico("ice_hi", (sx * 0.17, -0.06, 0.14), 0.035, sub=1)


# ----------------------------------------------------------------- mu (hat / helm)
def dome(w, key, R, h, base_z=0.0, brim=None, seg=12):
    prof = [(0.0 + 0.0001, base_z), (R, base_z), (R * 0.98, base_z + h * 0.45), (R * 0.82, base_z + h * 0.8),
            (R * 0.45, base_z + h * 0.97), (0.0, base_z + h)]
    prof[0] = (R * 0.0, base_z)
    w.lathe(key, prof, seg=seg)


def mu(w, t):
    th = TH[t]
    if t == 1:  # straw conical hat with a chin cord
        w.lathe("wood_l", [(0, 0.17), (0.04, 0.16), (0.12, 0.06), (0.24, -0.02), (0.22, -0.045), (0.12, -0.02),
                          (0.0, 0.0)], seg=14)
        w.torus("clay_d", (0, 0, 0.0), 0.15, 0.012, seg=14, tseg=4)
        w.cyl("clay_d", (0, 0, 0.175), 0.02, 0.0, 0.04, seg=5)
        for sx in (-1, 1):
            w.bar("cloth_d", (sx * 0.14, -0.04, -0.02), (sx * 0.1, -0.06, -0.15), 0.01, seg=4)
        w.box("clay", (0.05, -0.12, 0.06), (0.06, 0.01, 0.02), rot=(0, 0, 25), bevel=0)
    elif t == 3:  # scholar's cap: green dome, flat top, bronze band, jade stone, ties
        w.lathe("jade", [(0, 0), (0.16, 0), (0.17, 0.05), (0.15, 0.12), (0.12, 0.17), (0.0, 0.17)], seg=12)
        w.box("jade_d", (0, 0, 0.18), (0.30, 0.17, 0.03), bevel=0.005)
        w.torus("bronze", (0, 0, 0.035), 0.165, 0.017, seg=12, tseg=4)
        w.sph("jade_l", (0, -0.16, 0.07), 0.034, scale=(1, 0.5, 1), seg=6)
        w.sph("gold", (0, -0.17, 0.07), 0.016, seg=4)
        for sx in (-1, 1):
            w.bar("jade_d", (sx * 0.15, 0.0, 0.04), (sx * 0.2, -0.04, -0.14), 0.018, 0.012, seg=4)
            w.box("gold", (sx * 0.2, -0.04, -0.15), (0.04, 0.02, 0.04), bevel=0)
    elif t == 5:  # blue helm with gold circlet, glowing crest and gem
        w.lathe("blue", [(0, -0.02), (0.17, -0.02), (0.18, 0.06), (0.15, 0.15), (0.08, 0.21), (0.0, 0.22)], seg=12)
        w.torus("gold_d", (0, 0, 0.04), 0.175, 0.02, seg=12, tseg=4)
        w.box("blue_d", (0, -0.12, 0.0), (0.24, 0.1, 0.05), bevel=0.004)  # brow
        w.box("cyan", (0, 0.0, 0.25), (0.03, 0.12, 0.12), rot=(0, 0, 0), bevel=0)
        w.cyl("cyan", (0, 0.0, 0.31), 0.03, 0.0, 0.1, seg=4)
        w.sph("violet", (0, -0.17, 0.07), 0.04, scale=(1, 0.5, 1), seg=6)
        for sx in (-1, 1):
            w.box("blue_d", (sx * 0.16, -0.01, -0.05), (0.05, 0.16, 0.12), bevel=0.004)
    else:  # ice helm with wings at the temples
        w.lathe("blue_l", [(0, -0.02), (0.17, -0.02), (0.18, 0.06), (0.15, 0.15), (0.08, 0.21), (0.0, 0.22)], seg=12)
        w.torus("gold", (0, 0, 0.04), 0.175, 0.02, seg=12, tseg=4)
        w.box("ice_w", (0, 0.0, 0.25), (0.03, 0.12, 0.13), bevel=0)
        w.cyl("ice_hi", (0, 0.0, 0.325), 0.03, 0.0, 0.1, seg=4)
        w.sph("ice_hi", (0, -0.17, 0.07), 0.04, scale=(1, 0.5, 1), seg=6)
        for sx in (-1, 1):
            for k in range(3):
                leaf(w, "porcelain", (sx * 0.17, 0.06 + k * 0.014), sx * (45 + k * 16), 0.22 - k * 0.03, 0.07,
                     thick=0.014, y=0.0)


# ----------------------------------------------------------------- giay (boots)
def boot(w, t, x, y, scale=1.0):
    th = TH[t]
    with w.at((x, y, 0), (0, 0, 0), (scale, scale, scale)):
        w.box(th["main"], (0.0, 0.03, 0.12), (0.135, 0.13, 0.25), bevel=0.012)         # shaft
        w.box(th["main"], (0.0, -0.07, -0.035), (0.135, 0.21, 0.095), bevel=0.012)      # foot
        w.sph(th["main"], (0.0, -0.17, -0.035), 0.068, scale=(1, 1, 0.75), seg=8)        # toe cap
        w.box(th["dark"], (0.0, -0.08, -0.09), (0.15, 0.31, 0.03), bevel=0.004)          # sole
        w.box(th["dark"], (0.0, 0.07, -0.075), (0.15, 0.06, 0.05), bevel=0.003)          # heel
        w.box(th["trim"] if t > 1 else th["dark"], (0.0, 0.03, 0.255), (0.15, 0.15, 0.035), bevel=0.005)  # cuff
        w.box(th["dark"], (0.0, 0.03, 0.272), (0.10, 0.10, 0.012), bevel=0)               # opening
        if t == 1:
            w.box("clay", (0.0, -0.045, 0.14), (0.05, 0.01, 0.07), bevel=0)
            w.box("cloth_d", (0.0, -0.052, 0.17), (0.07, 0.01, 0.012), bevel=0)
        if t >= 3:
            w.box(th["trim"], (0.0, -0.038, 0.07), (0.1, 0.012, 0.025), bevel=0)
        if t >= 5:
            w.sph(th["gem"], (0.0, -0.045, 0.17), 0.024, scale=(1, 0.5, 1), seg=6)
            w.box(th["glow"], (0.0, -0.08, -0.071), (0.14, 0.26, 0.01), bevel=0)
        if t == 7:
            for sx in (-1, 1):
                for k in range(3):
                    leaf(w, "porcelain", (sx * 0.07, 0.1 + k * 0.014), sx * (55 + k * 14), 0.15 - k * 0.025, 0.055,
                         thick=0.014, y=0.03)


def giay(w, t):
    w.pose = dict(angle=0, spin=-28)
    boot(w, t, 0.11, 0.0)
    boot(w, t, -0.11, 0.0)


# ----------------------------------------------------------------- gang (glove)
def gang(w, t):
    th = TH[t]
    w.pose = dict(angle=0, spin=0)
    w.box(th["main"], (0, 0, 0.0), (0.27, 0.08, 0.18), bevel=0.012)                     # palm / back
    for dx, ln, a in ((-0.09, 0.17, 5), (-0.03, 0.22, 1), (0.03, 0.21, -1), (0.09, 0.15, -5)):
        w.box(th["main"], (dx, 0, 0.09 + ln / 2), (0.062, 0.07, ln), rot=(0, a, 0), bevel=0.006)
        w.box(th["dark"], (dx, -0.037, 0.09 + ln * 0.5), (0.05, 0.008, 0.016), bevel=0)  # knuckle fold
    for gx, ln in ((-0.06, 0.15), (0.0, 0.2), (0.06, 0.18)):                              # finger gaps
        w.box("ink", (gx, -0.038, 0.09 + ln / 2 + 0.01), (0.012, 0.008, ln), bevel=0)
    w.box(th["main"], (0.18, 0, 0.0), (0.17, 0.07, 0.06), rot=(0, 42, 0), bevel=0.008)  # thumb
    w.box("ink", (0.12, -0.037, 0.045), (0.014, 0.008, 0.07), rot=(0, 0, -40), bevel=0)
    w.box(th["dark"], (0, 0, -0.11), (0.23, 0.10, 0.07), bevel=0.01)                     # wrist
    w.box(th["trim"] if t > 1 else th["dark"], (0, 0, -0.17), (0.27, 0.12, 0.06), bevel=0.008)  # cuff
    if t == 1:
        w.box("clay", (-0.03, -0.042, 0.03), (0.06, 0.008, 0.045), bevel=0)
    if t >= 3:
        w.box(th["metal"], (0, -0.043, 0.04), (0.20, 0.014, 0.03), bevel=0.002)
    if t >= 5:
        w.sph(th["gem"], (0, -0.058, -0.03), 0.03, scale=(1, 0.5, 1), seg=6)
        w.box(th["glow"], (0, -0.062, -0.17), (0.22, 0.01, 0.014), bevel=0)
    if t == 7:
        for k in range(3):
            leaf(w, "porcelain", (-0.12, -0.12 + k * 0.014), -(58 + k * 14), 0.17 - k * 0.03, 0.06, thick=0.014,
                 y=0.06)


# ----------------------------------------------------------------- nhan (ring)
def nhan(w, t):
    th = TH[t]
    w.pose = dict(angle=0, spin=24)
    band = {1: "iron_d", 3: "jade", 5: "gold", 7: "steel"}[t]
    w.torus(band, (0, 0, 0.0), 0.13, 0.036, rot=(90, 0, 0), seg=16, tseg=6, scale=(1, 1, 1.5))
    w.box(band, (0, 0, 0.16), (0.1, 0.075, 0.07), bevel=0.008)  # bezel
    gem = {1: "stone", 3: "gold", 5: "cyan", 7: "ice"}[t]
    if t == 1:
        w.ico("stone", (0, -0.03, 0.2), 0.065, sub=1)
        w.box("stone_d", (0, -0.075, 0.2), (0.03, 0.012, 0.03), bevel=0)
    elif t == 3:
        for dy in (-0.035, 0.035):
            w.torus("gold", (0, dy, 0.0), 0.13, 0.012, rot=(90, 0, 0), seg=16, tseg=4)
        w.ico("jade_l", (0, -0.03, 0.2), 0.065, sub=1)
        w.sph("gold", (0, -0.08, 0.2), 0.018, seg=5)
    elif t == 5:
        w.ico("cyan", (0, -0.03, 0.21), 0.075, scale=(1, 0.8, 1.15), sub=1)
        w.ico("cyan_hi", (-0.02, -0.07, 0.23), 0.03, sub=1)
        sparkle(w, "cyan_hi", (0.15, -0.08, 0.3), 0.03)
    else:
        w.ico("ice", (0, -0.03, 0.21), 0.075, scale=(1, 0.8, 1.15), sub=1)
        w.ico("ice_hi", (-0.02, -0.07, 0.23), 0.03, sub=1)
        for sx in (-1, 1):
            for k in range(3):
                leaf(w, "porcelain", (sx * 0.05, 0.15 + k * 0.014), sx * (62 + k * 14), 0.17 - k * 0.03, 0.055,
                     thick=0.014, y=0.03)
        sparkle(w, "ice_hi", (0.18, -0.08, 0.32), 0.028)


# ----------------------------------------------------------------- day_chuyen (necklace)
def day_chuyen(w, t):
    th = TH[t]
    w.pose = dict(angle=0, spin=0)
    cord = {1: "wood_d", 3: "bronze", 5: "gold", 7: "steel"}[t]
    bead = {1: "wood_l", 3: "jade_l", 5: "gold", 7: "ice_w"}[t]
    n = 15
    R = 0.2
    cz = 0.07
    pts = []
    for i in range(n):
        a = math.radians(205 + i * 130 / (n - 1))
        pts.append((math.cos(a) * R * 1.05, 0, cz + math.sin(a) * R * 1.0))
    # string
    w.path(cord, pts, 0.008)
    for i, p in enumerate(pts):
        big = t == 1 or i % 3 == 1
        w.sph(bead, (p[0], 0, p[2]), 0.027 if big else 0.016, seg=6)
    bz = pts[n // 2][2]
    if t == 1:
        w.sph("wood", (0, -0.01, bz - 0.055), 0.065, seg=7)
        w.box("clay", (0.0, -0.065, bz - 0.04), (0.03, 0.01, 0.03), bevel=0)
    elif t == 3:
        w.cyl("jade", (0, 0, bz - 0.07), 0.075, 0.075, 0.03, rot=(90, 0, 0), seg=12)
        w.torus("gold", (0, 0, bz - 0.07), 0.075, 0.011, rot=(90, 0, 0), seg=12, tseg=4)
        w.cyl("jade_d", (0, -0.02, bz - 0.07), 0.024, 0.024, 0.02, rot=(90, 0, 0), seg=8)
    elif t == 5:
        w.box("gold", (0, 0, bz - 0.025), (0.05, 0.02, 0.04), bevel=0.003)
        w.ico("cyan", (0, -0.015, bz - 0.1), 0.07, scale=(0.8, 0.6, 1.3), sub=1)
        w.ico("cyan_hi", (-0.015, -0.045, bz - 0.09), 0.025, sub=1)
        sparkle(w, "cyan_hi", (0.14, -0.05, bz - 0.06), 0.028)
    else:
        w.box("gold", (0, 0, bz - 0.025), (0.05, 0.02, 0.04), bevel=0.003)
        w.ico("ice", (0, -0.015, bz - 0.1), 0.07, scale=(0.8, 0.6, 1.3), sub=1)
        w.ico("ice_hi", (-0.015, -0.045, bz - 0.09), 0.025, sub=1)
        for sx in (-1, 1):
            for k in range(3):
                leaf(w, "porcelain", (sx * 0.06, bz - 0.09 + k * 0.014), sx * (70 + k * 14), 0.15 - k * 0.025, 0.05,
                     thick=0.014, y=0.03)


BUILD = {"ao": ao, "mu": mu, "giay": giay, "gang": gang, "nhan": nhan, "day_chuyen": day_chuyen}


def make(wid):
    slot, t = wid.rsplit("_", 1)
    t = int(t)
    w = W(wid, "%s %s" % (SLOT_VI[slot], TIER_VI[t]), t)
    w.pose = dict(angle=0, spin=0)
    BUILD[slot](w, t)
    return w
