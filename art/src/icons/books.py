"""cong_phap atlas: 24 manuals = 8 grades x (sach book, cuon scroll, gian slips / floating tome)."""
import math

from lib import W, leaf, swirl2d, stars_at, sparkle

GRADE_VI = {1: "Phàm", 2: "Hoàng", 3: "Huyền", 4: "Địa", 5: "Linh", 6: "Bảo", 7: "Tiên", 8: "Thiên"}
FORM_VI = {"sach": "Thư", "cuon": "Quyển", "gian": "Giản"}
IDS = ["%s_%d" % (f, g) for g in range(1, 9) for f in ("sach", "cuon", "gian")]

# per grade: cover, cover_d, trim, ink(for strokes), glow(strokes) ...
TH = {
    1: dict(cover="clay_d", dark="cloth_d", trim=None, ink="cloth_d", rune=None, gem=None, knob="wood"),
    2: dict(cover="iron_d", dark="stone_d", trim="iron", ink="cloth_d", rune=None, gem=None, knob="iron"),
    3: dict(cover="jade", dark="jade_d", trim="bronze", ink="jade_d", rune=None, gem="jade_l", knob="bronze"),
    4: dict(cover="blue", dark="blue_d", trim="gold", ink="blue_d", rune=None, gem="teal", knob="gold"),
    5: dict(cover="blue_d", dark="blue_d", trim="gold_d", ink="cyan", rune="cyan", gem="violet", knob="violet"),
    6: dict(cover="red_d", dark="red_d", trim="gold_dk", ink="flame", rune="flame", gem="flame_y", knob="flame"),
    7: dict(cover="blue_l", dark="blue", trim="ice_w", ink="ice", rune="ice_hi", gem="ice_hi", knob="ice_hi"),
    8: dict(cover="purple", dark="purple", trim="gold", ink="gold_e", rune="gold_e", gem="star", knob="star"),
}

BW, BH, BT = 0.30, 0.40, 0.10
YF = -BT / 2


def ring(w, key, c, R, r, rot=(90, 0, 0)):
    w.torus(key, c, R, r, rot=rot, seg=14, tseg=4)


def strokes(w, key, cx, z0, z1, n, wid, y, seed=0, th=0.012):
    """Abstract writing: rows of short dashes (never letters)."""
    import random
    rnd = random.Random(seed)
    for i in range(n):
        z = z0 + (z1 - z0) * i / max(1, n - 1)
        x = cx - wid / 2
        while x < cx + wid / 2 - 0.02:
            ln = rnd.choice((0.03, 0.045, 0.06))
            ln = min(ln, cx + wid / 2 - x)
            w.box(key, (x + ln / 2, y, z), (ln, 0.006, th), bevel=0)
            x += ln + 0.018


# ----------------------------------------------------------------- book
def emblem(w, g, th):
    y = YF - 0.007
    if g == 1:  # nothing but a plain round tag on the cord binding
        w.cyl("clay", (0, y - 0.002, 0.0), 0.05, 0.05, 0.008, rot=(90, 0, 0), seg=12)
        w.cyl("clay_d", (0, y - 0.007, 0.0), 0.028, 0.028, 0.008, rot=(90, 0, 0), seg=10)
    elif g == 2:  # a single horizontal iron bar plate with two rivets
        w.box("iron", (0.0, y, 0.0), (0.17, 0.010, 0.05), bevel=0.002)
        for sx in (-1, 1):
            w.sph("iron_d", (sx * 0.065, y - 0.007, 0.0), 0.014, seg=5)
    elif g == 3:
        w.box("bronze", (0, y, 0.0), (0.12, 0.012, 0.12), rot=(0, 45, 0), bevel=0.002)
        w.box("jade_d", (0, y - 0.004, 0.0), (0.10, 0.010, 0.10), rot=(0, 45, 0), bevel=0.002)
        w.sph("jade_l", (0, y - 0.012, 0.0), 0.030, scale=(1, 0.5, 1), seg=6)
    elif g == 4:
        w.box("gold", (0, y, 0.0), (0.20, 0.010, 0.26), bevel=0.002)
        w.box("blue_d", (0, y - 0.003, 0.0), (0.17, 0.010, 0.23), bevel=0.002)
        w.sph("teal", (0, y - 0.012, 0.0), 0.040, scale=(1, 0.5, 1), seg=6)
    elif g == 5:
        ring(w, "cyan", (0, y - 0.004, 0.0), 0.085, 0.014)
        w.sph("violet", (0, y - 0.010, 0.0), 0.040, scale=(1, 0.5, 1), seg=6)
        w.box("cyan", (0, y - 0.004, 0.0), (0.012, 0.01, 0.17), bevel=0)
        w.box("cyan", (0, y - 0.004, 0.0), (0.17, 0.01, 0.012), bevel=0)
    elif g == 6:
        for dx, hh, rr in ((-0.05, 0.12, 0.030), (0.0, 0.17, 0.040), (0.05, 0.12, 0.030)):
            w.cyl("flame", (dx, y - 0.006, -0.05 + hh / 2), rr, 0.0, hh, rot=(90, 0, 0), seg=5) if False else \
                w.cyl("flame", (dx, y - 0.006, -0.07 + hh / 2), rr, 0.0, hh, seg=5)
        w.cyl("flame_y", (0, y - 0.012, -0.065 + 0.055), 0.022, 0.0, 0.11, seg=4)
        w.box("gold_dk", (0, y, -0.085), (0.15, 0.008, 0.030), bevel=0.001)
    elif g == 7:
        for a in (0, 60, 120):
            w.box("ice_hi", (0, y - 0.006, 0.0), (0.17, 0.010, 0.016), rot=(0, a, 0), bevel=0)
        w.sph("ice", (0, y - 0.012, 0.0), 0.026, scale=(1, 0.5, 1), seg=6)
        for sx in (-1, 1):  # little wings on the cover edge
            for k in range(3):
                leaf(w, "porcelain", (sx * 0.15, 0.04 - k * 0.045), sx * (62 + k * 12), 0.14 - k * 0.02, 0.06,
                     thick=0.012, y=-0.005)
    else:
        ring(w, "gold_e", (0, y - 0.004, 0.0), 0.085, 0.012)
        w.sph("star", (0, y - 0.010, 0.0), 0.034, scale=(1, 0.5, 1), seg=6)
        w.box("gold_e", (0, y - 0.004, 0.0), (0.012, 0.01, 0.20), bevel=0)
        w.box("gold_e", (0, y - 0.004, 0.0), (0.20, 0.01, 0.012), bevel=0)
        stars_at(w, "star", [(-0.10, y - 0.008, 0.14), (0.11, y - 0.008, 0.12), (-0.11, y - 0.008, -0.13),
                              (0.09, y - 0.008, -0.15), (0.0, y - 0.008, 0.16)], 0.014)


def sach(g):
    th = TH[g]
    w = W("sach_%d" % g, GRADE_VI[g] + " " + FORM_VI["sach"], g)
    w.pose = dict(angle=0, spin=28)
    # covers, spine, pages
    w.box(th["cover"], (0, YF + 0.007, 0), (BW, 0.014, BH), bevel=0.004)
    w.box(th["dark"], (0, -YF - 0.007, 0), (BW, 0.014, BH), bevel=0.004)
    w.box(th["dark"], (-BW / 2 + 0.012, 0, 0), (0.034, BT, BH + 0.004), bevel=0.005)
    w.box("paper", (0.006, 0, 0), (BW - 0.03, BT - 0.024, BH - 0.03), bevel=0.002)
    # page lines on the exposed edge
    for k in (-1, 0, 1):
        w.box("paper_d", (BW / 2 - 0.016, 0.0, k * 0.1), (0.004, BT - 0.03, 0.006), bevel=0)
    # binding: low grades are sewn with cord loops on the spine
    if g <= 2:
        for z in (-0.13, 0.0, 0.13):
            w.box("paper_d", (-BW / 2 - 0.003, YF + 0.008, z), (0.018, 0.012, 0.03), bevel=0.001)
    if th["trim"]:
        for sx in (-1, 1):
            for sz in (-1, 1):
                w.box(th["trim"], (sx * (BW / 2 - 0.028), YF + 0.007, sz * (BH / 2 - 0.028)),
                      (0.056, 0.018, 0.056), bevel=0.003)
        if g >= 4:
            w.box(th["trim"], (0, YF + 0.007, BH / 2 - 0.006), (BW - 0.06, 0.018, 0.012), bevel=0.002)
            w.box(th["trim"], (0, YF + 0.007, -BH / 2 + 0.006), (BW - 0.06, 0.018, 0.012), bevel=0.002)
    emblem(w, g, th)
    if g >= 6:  # clasp + faint glowing edge
        w.box(th["trim"], (BW / 2 - 0.004, YF + 0.01, 0), (0.02, 0.022, 0.05), bevel=0.003)
    return w


# ----------------------------------------------------------------- scroll
def roll(w, key_paper, key_knob, x, h=0.36, r=0.046, knob_r=0.028):
    w.cyl(key_paper, (x, 0, 0), r, r, h, seg=10)
    for sz in (-1, 1):
        w.cyl(key_knob, (x, 0, sz * (h / 2 + 0.014)), knob_r, knob_r, 0.03, seg=8)
        w.cyl(key_knob, (x, 0, sz * (h / 2 + 0.036)), knob_r * 0.6, knob_r * 0.6, 0.018, seg=6)


def cuon(g):
    th = TH[g]
    w = W("cuon_%d" % g, GRADE_VI[g] + " " + FORM_VI["cuon"], g)
    if g <= 2:  # closed roll tied with a cord, drawn diagonal
        w.pose = dict(angle=40, spin=0)
        paper = "wood_l" if g == 1 else "paper"
        w.cyl(paper, (0, 0, 0), 0.07, 0.07, 0.34, seg=10)
        # visible spiral of the roll on the end
        w.cyl("paper_d", (0, 0, 0.171), 0.045, 0.045, 0.004, seg=10)
        for sz in (-1, 1):
            w.cyl(th["knob"], (0, 0, sz * 0.19), 0.04, 0.04, 0.04, seg=8)
            w.cyl(th["knob"], (0, 0, sz * 0.222), 0.026, 0.026, 0.03, seg=8)
        cord = "red" if g == 2 else "clay_d"
        w.cyl(cord, (0, 0, 0.0), 0.078, 0.078, 0.045, seg=10)
        w.box("red_l" if g == 2 else "clay", (0.0, -0.075, -0.045), (0.03, 0.012, 0.09), bevel=0.001)
        return w
    w.pose = dict(angle=0, spin=-12)
    knob = th["knob"]
    paper = "paper_pu" if g == 8 else ("paper_ice" if g == 7 else "paper")
    rx = 0.165
    for sx in (-1, 1):
        roll(w, "wood_l" if g < 7 else paper, knob, sx * rx)
    sheet_h = 0.30
    w.box(paper, (0, 0, 0), (2 * rx - 0.02, 0.010, sheet_h), bevel=0.002)
    if g == 6:  # singed lower edge
        w.box("red_d", (0, -0.004, -sheet_h / 2 + 0.008), (2 * rx - 0.03, 0.012, 0.016), bevel=0)
    ink = th["ink"]
    rune = th["rune"] or th["ink"]
    if g == 3:
        strokes(w, ink, 0, -0.10, 0.10, 4, 0.20, -0.008, seed=3, th=0.014)
    elif g == 4:
        strokes(w, ink, 0, -0.08, 0.10, 3, 0.20, -0.008, seed=4, th=0.014)
        w.sph("teal", (0.0, -0.010, -0.10), 0.032, scale=(1, 0.5, 1), seg=6)
    elif g == 5:
        w.torus(rune, (0, -0.008, 0.02), 0.075, 0.010, rot=(90, 0, 0), seg=14, tseg=4)
        w.box(rune, (0, -0.008, 0.02), (0.012, 0.008, 0.15), bevel=0)
        w.box(rune, (0, -0.008, 0.02), (0.15, 0.008, 0.012), bevel=0)
        strokes(w, rune, 0, -0.11, -0.09, 1, 0.20, -0.008, seed=5, th=0.012)
        strokes(w, rune, 0, 0.12, 0.13, 1, 0.20, -0.008, seed=6, th=0.012)
    elif g == 6:
        for dx, hh, rr in ((-0.05, 0.10, 0.026), (0.0, 0.15, 0.036), (0.05, 0.10, 0.026)):
            w.cyl("flame", (dx, -0.010, -0.06 + hh / 2), rr, 0.0, hh, seg=5)
        w.cyl("flame_y", (0, -0.014, -0.06 + 0.045), 0.018, 0.0, 0.09, seg=4)
        strokes(w, "flame", 0, 0.10, 0.12, 1, 0.20, -0.008, seed=7, th=0.012)
    elif g == 7:
        for a in (0, 60, 120):
            w.box("ice_hi", (0, -0.009, 0.0), (0.17, 0.008, 0.014), rot=(0, a, 0), bevel=0)
        w.sph("ice", (0, -0.012, 0.0), 0.024, scale=(1, 0.5, 1), seg=6)
        strokes(w, "ice", 0, -0.11, -0.10, 1, 0.20, -0.008, seed=8, th=0.012)
        strokes(w, "ice", 0, 0.11, 0.12, 1, 0.20, -0.008, seed=9, th=0.012)
    else:
        w.torus("gold_e", (0, -0.008, 0.02), 0.075, 0.010, rot=(90, 0, 0), seg=14, tseg=4)
        w.sph("star", (0, -0.011, 0.02), 0.030, scale=(1, 0.5, 1), seg=6)
        stars_at(w, "star", [(-0.09, -0.010, 0.12), (0.10, -0.010, 0.10), (-0.10, -0.010, -0.11),
                              (0.08, -0.010, -0.12)], 0.013)
    return w


# ----------------------------------------------------------------- slips / floating tome
def slips(g):
    th = TH[g]
    w = W("gian_%d" % g, GRADE_VI[g] + " " + FORM_VI["gian"], g)
    w.pose = dict(angle=0, spin=-12)
    slat = {1: "wood_l", 2: "wood", 3: "jade", 4: "jade_l", 5: "cyan"}[g]
    mark = {1: "wood_d", 2: "wood_d", 3: "jade_d", 4: "jade_d", 5: "cyan_hi"}[g]
    cord = {1: "clay_d", 2: "red", 3: "bronze", 4: "gold", 5: "violet"}[g]
    n = 5
    pitch = 0.068
    for i in range(n):
        x = (i - (n - 1) / 2) * pitch
        top = 0.20 + (0.012 if i % 2 else 0.0)
        w.box(slat, (x, 0, 0), (0.050, 0.014, 2 * top), bevel=0.003)
        if g <= 2:  # node ring of the bamboo
            w.box("wood_d", (x, -0.008, 0.06), (0.056, 0.006, 0.012), bevel=0)
        for z in (-0.13, -0.04, 0.05, 0.14):
            w.box(mark, (x, -0.009, z), (0.012, 0.004, 0.04 if g != 5 else 0.036), bevel=0)
    for z in (-0.11, 0.11):
        w.box(cord, (0, -0.012, z), (pitch * n + 0.01, 0.012, 0.022), bevel=0.001)
        w.sph(cord, (pitch * n / 2 + 0.006, -0.014, z), 0.020, seg=6)
    if g >= 3:
        for sx in (-1, 1):
            w.box(th["trim"] or "bronze", (sx * (pitch * n / 2 + 0.002), 0, 0), (0.012, 0.018, 0.40), bevel=0.002)
    if g == 5:
        w.sph("violet", (0, -0.016, 0.11), 0.026, scale=(1, 0.5, 1), seg=6)
    return w


def tome(g):
    th = TH[g]
    w = W("gian_%d" % g, GRADE_VI[g] + " " + FORM_VI["gian"], g)
    w.pose = dict(angle=0, spin=0)
    glow = {6: "flame", 7: "ice", 8: "violet"}[g]
    glow_hi = {6: "flame_y", 7: "ice_hi", 8: "star"}[g]
    cover = th["cover"]
    with w.at((0, 0, 0), (-35, 0, 0), (1.5, 1.5, 1.5)):  # lay the open book back toward the camera
        for sx in (-1, 1):
            with w.at((sx * 0.012, 0, 0), (0, sx * -9, 0)):
                w.box(cover, (sx * 0.105, 0.012, 0), (0.22, 0.016, 0.30), bevel=0.003)   # cover under
                w.box("paper", (sx * 0.105, 0.0, 0.0), (0.20, 0.030, 0.27), bevel=0.003)   # page block
                w.box("paper_d", (sx * 0.105, -0.017, 0.0), (0.18, 0.006, 0.25), bevel=0.001)
                strokes(w, "cloth_d", sx * 0.105, -0.095, 0.095, 6, 0.15, -0.022, seed=10 + sx + g, th=0.012)
                w.box(th["trim"], (sx * 0.105, 0.016, 0.16), (0.22, 0.018, 0.014), bevel=0.001)
        w.box(th["dark"], (0, 0.01, 0), (0.03, 0.03, 0.30), bevel=0.004)
        # rune that lifts off the page
        w.sph(glow_hi, (0, -0.045, 0.02), 0.032, seg=6)
    # swirling qi: spirals behind the book plus short arcs at its sides
    swirl2d(w, glow, (0, 0, 0), 0.37, 0.46, 160, 330, n=14, r=0.016, y=0.09)
    swirl2d(w, glow, (0, 0, 0), 0.37, 0.46, 340, 510, n=14, r=0.016, y=0.09)
    swirl2d(w, glow_hi, (0, 0, 0), 0.42, 0.48, 200, 250, n=5, r=0.010, y=0.095)
    swirl2d(w, glow_hi, (0, 0, 0), 0.42, 0.48, 20, 70, n=5, r=0.010, y=0.095)
    sparkle(w, glow_hi, (0.2, -0.12, 0.3), 0.032)
    sparkle(w, glow_hi, (-0.26, -0.12, -0.24), 0.026)
    if g == 8:
        stars_at(w, "star", [(0.0, -0.1, 0.27), (-0.22, -0.1, 0.12), (0.22, -0.1, -0.1)], 0.015)
    return w


def make(wid):
    f, g = wid.split("_")
    g = int(g)
    if f == "sach":
        return sach(g)
    if f == "cuon":
        return cuon(g)
    return slips(g) if g <= 5 else tome(g)
