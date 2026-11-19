"""Bi canh (secret realm) pieces: ancient ruin stone, abstract glowing strokes (no letters, no digits). 2x the old sprites."""
from __future__ import annotations

import math

import wt_common as C
from wt_common import mat
from wt_village import X, Y, Z, bx, cy, bl, tubep, shadow
from wt_garden import tb, tbl


def glow_stroke(col, pts, r, on, kind="glow_y"):
    m = mat(kind, 3, emit=1.6, prio=3.0) if on else mat("red", 1)
    tubep(col, pts, r, m, seg=4)


# --------------------------------------------------------------------------- rift: a tear in the air (8 frames)
def rift(col, f):
    shadow(col, 0, 2, 12, 4)
    a = f * math.pi / 4
    bl(col, 0, 3, 30, 11, 27, mat("ink", 0), sub=2, ry=1.6)
    for k in range(2):
        s = 1 if k else -1
        pts = [(s * (3 + 7 * math.sin(math.pi * i / 9)) + math.sin(i * 0.9 + a) * 1.4, 1.6, 6 + i * 5.2) for i in range(10)]
        tubep(col, pts, 1.5, mat("mist", 2, emit=1.8, prio=2.0), seg=4)
    for k in range(4):
        b = a + k * 1.57
        bl(col, 8 * math.cos(b), 1.0, 30 + 16 * math.sin(b), 1.2, 1.2, mat("mist", 3, emit=2.6, prio=4.0), sub=1)
    for k in range(2):                                      # drifting ink beads at the foot
        bl(col, -6 + k * 12 + math.sin(a + k) * 2, 2, 4 + (f + k * 3) % 4, 1.4, 1.4, mat("ink", 1), sub=1)


# --------------------------------------------------------------------------- pedestal: off / on / lit
def pedestal(state):
    def b(col, f):
        shadow(col, 0, 3, 18, 7)
        cy(col, 0, 7, 0, 16, 9, mat("stone", 1), seg=18, r1=14)
        cy(col, 0, 7, 9, 14.5, 3, mat("stone", 2), seg=18, r1=14)
        for k in range(8):                                  # carved facets
            a = k * math.pi / 4
            bx(col, 15 * math.cos(a), 7 + 15 * math.sin(a) * 0.57, 1, 3, 1.5, 6, mat("stone", 0))
        if state == "off":
            cy(col, 0, 7, 12, 9, 0.8, mat("stone", 0), seg=16)
            cy(col, 0, 7, 12.6, 6.5, 0.6, mat("stone", 2), seg=16)
        else:
            ring = mat("crys_c", 3, emit=1.4) if state == "on" else mat("glow_y", 3, emit=1.8)
            cy(col, 0, 7, 12, 9.5, 0.9, ring, seg=18)
            cy(col, 0, 7, 12.9, 7.0, 0.7, mat("stone", 1), seg=18)
            if state == "lit":
                bl(col, 0, 7, 17, 3.6, 3.6, mat("glow_y", 3, emit=2.6, prio=3.0), sub=1)
                for k in range(3):
                    a = k * 2.1
                    bl(col, 8 * math.cos(a), 7 + 3 * math.sin(a), 15 + k * 2, 0.9, 0.9, mat("glow_y", 3, emit=2.6, prio=4.0), sub=1)
    return b


# --------------------------------------------------------------------------- rune tile: top-down floor stone, blank carved sigil
def rune_tile(state):
    def b(col, f):
        base = {"off": ("steel", 0), "idle": ("stone", 1), "next": ("stone", 2), "done": ("gold", 1)}[state]
        tb(col, 0, 0, 0, 34, 34, 2.5, mat(*base), bevel=1.0)
        tb(col, 0, 0, 2.5, 23, 23, 0.9, mat(base[0], max(0, base[1] - 1)), bevel=0.5)          # sunken plaque (the game writes the number)
        for k in range(4):                                  # corner studs
            tbl(col, (-1 if k % 2 else 1) * 13.5, (-1 if k // 2 else 1) * 13.5, 3, 1.6, 1.0, mat(base[0], min(3, base[1] + 1)))
        if state == "next":
            for (x, d, w, h) in ((0, -16.2, 34, 1.5), (0, 16.2, 34, 1.5), (-16.2, 0, 1.5, 34), (16.2, 0, 1.5, 34)):
                tb(col, x, d, 2.6, w, h, 0.8, mat("crys_c", 3, emit=1.8, prio=3.0))
        if state == "done":
            for (x, d, w, h) in ((0, -16.2, 34, 1.5), (0, 16.2, 34, 1.5), (-16.2, 0, 1.5, 34), (16.2, 0, 1.5, 34)):
                tb(col, x, d, 2.6, w, h, 0.8, mat("glow_y", 3, emit=1.6, prio=3.0))
    return b


# --------------------------------------------------------------------------- pillar: four tone contours, glow off / on
TONES = {1: [(-6, 0), (6, 0)], 2: [(-6, -4), (6, 4)], 3: [(-6, 2), (-1, -4.5), (6, 4.5)], 4: [(-6, 4.5), (6, -4.5)]}


def pillar(tone, on):
    def b(col, f):
        shadow(col, 0, 3, 14, 5)
        bx(col, 0, 1, 0, 24, 14, 6, mat("stone", 2), bevel=1.0)
        bx(col, 0, 3, 6, 18, 10, 44, mat("stone", 1), bevel=1.0)
        bx(col, 0, 1, 50, 24, 14, 6, mat("stone", 2), bevel=1.0)
        for z in (14, 38):
            bx(col, 0, 2.6, z, 19.5, 0.8, 1.4, mat("stone", 0))                                    # weathered bands
        pts = [(x, 2.2, 30 + dz) for x, dz in TONES[tone]]
        glow_stroke(col, pts, 1.5, on)
        for k in range(2):                                  # a small dot above, like a mark of the tone
            bl(col, -3 + k * 6, 2.0, 41, 0.9, 0.9, mat("glow_y", 3, emit=1.6, prio=3.0) if on else mat("red", 1), sub=1)
    return b


# --------------------------------------------------------------------------- statue (2 frames: the second glows)
def statue(col, f):
    shadow(col, 0, 4, 17, 6)
    bx(col, 0, 1, 0, 34, 16, 8, mat("stone", 1), bevel=1.0)
    cy(col, 0, 8, 8, 11, 24, mat("stone", 2), seg=12, r1=6)                                        # robe
    bx(col, 0, 3, 18, 14, 3, 9, mat("paper", 2), bevel=0.6)                                        # the scroll
    for k in range(3):
        bx(col, -4 + k * 4, 1.7, 20, 2, 0.6, 5, mat("gold", 1))
    bl(col, 0, 8, 38, 6.2, 6.5, mat("stone", 2), sub=2)
    for sx in (-1, 1):                                                                            # arms
        bl(col, sx * 9, 5, 24, 2.6, 5, mat("stone", 1), sub=1)
    if f == 1:
        for sx in (-1, 1):
            bl(col, sx * 2.4, 2.4, 39, 1.0, 1.0, mat("glow_y", 3, emit=2.6, prio=4.0), sub=1)
        for k in range(8):
            a = k * math.pi / 4
            bl(col, 11 * math.cos(a), 8 + 2 * math.sin(a), 40 + 8 * math.sin(a), 0.8, 0.8, mat("glow_y", 3, emit=2.0, prio=3.0), sub=1)


# --------------------------------------------------------------------------- mirror (4 frames)
def mirror(col, f):
    a = f * math.pi / 2
    bl(col, 0, 10, 0.5, 38, 1.2, mat("crys_c", 1, emit=0.9), sub=2, ry=11)                         # pool of light on the floor
    bl(col, 0, 10, 0.8, 26, 1.0, mat("crys_c", 3, emit=1.3), sub=2, ry=7)
    bx(col, 0, 8, 0, 18, 6, 4, mat("stone", 2), bevel=1.0)
    bx(col, 0, 9.5, 4, 5, 3, 22, mat("earth", 1), bevel=0.6)
    for sx in (-1, 1):
        tubep(col, [(sx * 4, 9.5, 4), (sx * 14, 9.5, 12)], 1.4, mat("earth", 1), seg=5)
    cy_x, cy_z = 0, 44
    # bronze frame (a disc seen from the front) and the glass
    C.cyl(col, "frame", (X(cy_x), Y(8.0), Z(cy_z)), X(20), X(20), Z(3), mat("gold", 1), seg=24, tilt=(0, 0))
    ob = col.objects[-1]
    ob.rotation_euler = (math.pi / 2, 0, 0)
    ob.location = (X(cy_x), Y(8.0), Z(cy_z))
    C.cyl(col, "glass", (0, 0, 0), X(16.5), X(16.5), Z(1.5), mat("crys_c", 2, emit=0.8), seg=24)
    ob = col.objects[-1]
    ob.rotation_euler = (math.pi / 2, 0, 0)
    ob.location = (X(cy_x), Y(6.4), Z(cy_z))
    gx, gz = 7 * math.cos(a + 2), 6 * math.sin(a + 2)
    tubep(col, [(cy_x + gx - 4, 5, cy_z + gz + 4), (cy_x + gx + 4, 5, cy_z + gz - 4)], 0.9, mat("white", 3, emit=2.4, prio=4.0), seg=4)
    for k in range(3):
        bl(col, 12 * math.cos(a + k * 2.1), 5, cy_z + 12 * math.sin(a + k * 2.1), 0.9, 0.9, mat("white", 3, emit=2.0, prio=3.0), sub=1)


# --------------------------------------------------------------------------- exit door in the north wall (closed / open, 2 frames)
def realm_exit(opened):
    def b(col, f):
        shadow(col, 0, 3, 28, 6)
        for sx in (-1, 1):
            bx(col, sx * 24, 1, 0, 14, 8, 44, mat("basalt", 1), bevel=1.0)
        bx(col, 0, 1, 40, 62, 8, 7, mat("basalt", 0), bevel=1.0)
        bx(col, 0, 0.2, 41.5, 10, 1.4, 5, mat("red", 1))
        bx(col, 0, 4, 0, 34, 3, 40, mat("basalt", 0))
        if opened:
            bx(col, 0, 3.6, 0, 30, 1.6, 38, mat("glow_y", 1, emit=1.1))
            bx(col, 0, 3.0, 6, 18, 1.4, 28, mat("white", 3, emit=1.8))
            for k in range(4):
                bl(col, -10 + k * 6.6, 2.5, 10 + (k * 7 + f * 4) % 26, 0.9, 0.9, mat("glow_y", 3, emit=2.6, prio=4.0), sub=1)
        else:
            bx(col, 0, 3.4, 0, 30, 1.6, 38, mat("ink", 0))
            for k in range(3):
                z = 8 + k * 11 + (f % 2) * 1.5
                bx(col, 0, 2.6, z, 26 - k * 2, 1.0, 1.5, mat("mist", 1, emit=1.2, prio=2.0))
            bx(col, 0, 2.4, 6, 1.5, 1.0, 30, mat("red", 1))
    return b


# --------------------------------------------------------------------------- chest
def chest(opened):
    def b(col, f):
        shadow(col, 0, 3, 20, 6)
        bx(col, 0, 1, 0, 38, 14, 14, mat("wood", 1), bevel=1.0)
        for sx in (-1, 1):
            bx(col, sx * 13, 0.6, 0, 3, 15, 14.5, mat("steel", 1), bevel=0.4)
        bx(col, 0, 0.2, 5, 4, 1.4, 6, mat("gold", 2))
        if opened:
            bx(col, 0, 1.6, 13, 33, 12, 1.2, mat("glow_y", 2, emit=1.7))
            for k in range(6):
                bl(col, -12 + k * 5, 6, 15.5 + (k % 2), 2.0, 1.4, mat("gold", 2), sub=1)
            lid = bx(col, 0, 12.5, 15, 38, 3, 14, mat("wood", 2), bevel=1.0)
            bx(col, 0, 13.6, 24, 38, 3, 2.5, mat("steel", 1), bevel=0.6)
            for k in range(3):
                bl(col, -8 + k * 8, 3, 17 + k * 2, 0.9, 0.9, mat("glow_y", 3, emit=2.6, prio=4.0), sub=1)
        else:
            bx(col, 0, 1, 14, 38, 14, 9, mat("wood", 2), bevel=1.2)
            for sx in (-1, 1):
                bx(col, sx * 13, 0.6, 14, 3, 15, 9.5, mat("steel", 1), bevel=0.4)
            bl(col, 0, 0.4, 14, 2.2, 2.2, mat("gold", 2), sub=1)
    return b


def specs():
    out = []
    mk = lambda **k: out.append(k)
    mk(name="rift", W=48, H=64, frames=8, base=4, ppm=42, build=rift, vi="Khe Nứt Mực", extra={"old": "rift(frame)"})
    for st in ("off", "on", "lit"):
        mk(name=f"pedestal_{st}", W=48, H=48, base=5, build=pedestal(st), vi="Đài đá", extra={"old": {"off": "pedestal(False, *)", "on": "pedestal(True, False)", "lit": "pedestal(True, True)"}[st]})
    for st in ("off", "idle", "next", "done"):
        mk(name=f"rune_{st}", W=40, H=40, mode="top", build=rune_tile(st), vi="Phiến đá chữ", pivot=(20, 40), extra={"old": f"rune_tile('{st}')"})
    for tone in (1, 2, 3, 4):
        for on in (False, True):
            mk(name=f"pillar_{tone}_{'on' if on else 'off'}", W=32, H=64, base=4, ppm=38, build=pillar(tone, on), vi="Trụ Thanh Điệu",
               extra={"old": f"pillar({tone}, {on})"})
    mk(name="statue", W=48, H=64, frames=2, base=4, ppm=42, build=statue, vi="Tượng đọc sách", extra={"old": "statue(frame) (frame % 2)"})
    mk(name="mirror", W=96, H=80, frames=4, base=4, build=mirror, vi="Gương Ý Nghĩa", extra={"old": "mirror(frame)"})
    mk(name="exit_closed", W=64, H=48, frames=2, base=4, ppm=33, build=realm_exit(False), vi="Cửa phong mực", extra={"old": "realm_exit(False, frame) (frame % 2)"})
    mk(name="exit_open", W=64, H=48, frames=2, base=4, ppm=33, build=realm_exit(True), vi="Cửa mở", extra={"old": "realm_exit(True, frame)"})
    mk(name="chest_closed", W=48, H=36, base=4, ppm=33, build=chest(False), vi="Rương báu", extra={"old": "chest(False)"})
    mk(name="chest_open", W=48, H=36, base=4, ppm=29, build=chest(True), vi="Rương báu mở", extra={"old": "chest(True)"})
    return out
