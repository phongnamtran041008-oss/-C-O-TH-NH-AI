"""Village buildings and structures (props/buildings.png): xianxia timber houses, tiled roofs with upturned eaves,
paper lanterns, stone bases. Modelled for the standard 35 degree prop camera at PPM px per metre.

Design coordinates are SCREEN PIXELS of the final sprite, relative to the pivot: x right of the centre, `d` the depth
into the picture measured as screen pixels of ground (0 = the front edge of the building, where the door is), z the
height above the ground in screen pixels. X() / Y() / Z() turn them into metres.
"""
from __future__ import annotations

import math

import bpy
import bmesh
from mathutils import Vector

import wt_common as C
from wt_common import mat

PPM = 47.0
CUR = [96, 96]          # width, height of the sprite being built (set by scene_village)
C35, S35 = math.cos(math.radians(35)), math.sin(math.radians(35))


def X(p): return p / PPM
def Y(p): return p / (PPM * S35)
def Z(p): return p / (PPM * C35)


def sm(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


# --------------------------------------------------------------------------- primitives in sprite pixels
def bx(col, cx, d0, z0, w, d, h, m, bevel=0.0, rot=0.0, taper=1.0):
    return C.box(col, "b", (X(cx), Y(d0 + d / 2), Z(z0 + h / 2)), (X(w), Y(d), Z(h)), m, rot_z=rot, bevel=X(bevel), taper=taper)


def cy(col, cx, dc, z0, r, h, m, seg=12, r1=None, smooth=True):
    return C.cyl(col, "c", (X(cx), Y(dc), Z(z0)), X(r), X(r if r1 is None else r1), Z(h), m, seg=seg, smooth=smooth)


def bl(col, cx, dc, zc, rx, rz, m, seed=0, rough=0.0, sub=1, ry=None):
    return C.blob(col, "o", (X(cx), Y(dc), Z(zc)), (X(rx), X(ry if ry is not None else rx), Z(rz)), m, seed=seed, rough=rough,
                  subdiv=sub, smooth=True)


def rodz(col, cx, dc, z0, z1, r, m, seg=6):
    return cy(col, cx, dc, z0, r, z1 - z0, m, seg=seg)


def tubep(col, pts, r, m, seg=5):
    """Tube through points given as (x, d, z) in sprite pixels."""
    return C.tube(col, "t", [(X(x), Y(d), Z(z)) for x, d, z in pts], [X(r)] * len(pts), m, seg=seg)


def glow_mat(kind, emit=1.5, step=2, prio=0.0):
    return mat(kind, step, emit=emit, prio=prio)


# --------------------------------------------------------------------------- shared parts
def shadow(col, cx, dc, rx, ry):
    """The contact shadow: one flat darker-grass blob (kit recipe), offset down-right; its front edge stays 2 px below
    the base line so it never touches the frame."""
    dc = ry - 1
    rx = min(rx, CUR[0] / 2 - 5)
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=20, radius=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * X(rx), v.co.y * Y(ry), 0.0))
    m = mat("grass", 1, name="MAT_contact_shadow", extra={"kit_outline": 0, "kit_shadow": 2.0, "kit_light": 3.0})
    ob = C.mesh_obj("contact_shadow", bm, m, col)
    ob.location = (X(cx + 2), Y(dc - 1), 0.004)


def roof(col, cx, dc, w, d, z_eave, rise, ox, oy, ramp, hip=False, up=4.0, courses=9, step=1):
    """Curved tiled roof with upturned eaves. (cx, dc) = centre of the walls, w x d = the walls it covers."""
    hx, hy = (w / 2 + ox), (d / 2 + oy)
    ridge_w = max(w + 2 * ox - 2 * hy * 1.1, 4.0)
    x0, x1 = X(cx - hx), X(cx + hx)
    y0, y1 = Y(dc - hy), Y(dc + hy)
    xc, yc = (x0 + x1) / 2, (y0 + y1) / 2
    ze, zr, zu = Z(z_eave), Z(rise), Z(up)
    mats = [mat(ramp, step), mat(ramp, step + 1 if step < 2 else 2), mat(ramp, 0)]

    def uv(x, y):
        return (x - xc) / ((x1 - x0) / 2), (y - yc) / ((y1 - y0) / 2)

    def z_fn(x, y):
        u, v = uv(x, y)
        if hip:
            t = min(1.0 - abs(v), (1.0 - abs(u)) * hx / hy * 0.85)
            lift = zu * (sm(0.78, 1.0, abs(u)) * 0.8 + sm(0.78, 1.0, abs(v)) * 0.8)
            return ze + zr * max(t, 0.0) ** 1.35 + lift
        t = 1.0 - abs(v)
        return ze + zr * max(t, 0.0) ** 1.5 + zu * (sm(0.8, 1.0, abs(v)) + 0.7 * sm(0.86, 1.0, abs(u)))

    def m_fn(x, y):
        u, v = uv(x, y)
        if hip:
            return int(abs(v) * courses) % 2
        if abs(v) < 0.06:
            return 2
        return int(abs(v) * courses) % 2

    C.heightfield(col, "roof", x0, y0, x1, y1, 72, z_fn, m_fn, mats, smooth=False)
    # fascia board under the front eave and a ridge cap
    bx(col, cx, dc - hy, z_eave - 3, w + 2 * ox, 2.5, 3.5, mat("wood", 0))
    if not hip:
        bx(col, cx, dc - 1.6, z_eave + rise + 0.5, w + 2 * ox - 2, 3.2, 3.0, mat(ramp, 0), bevel=0.8)
        for sx in (-1, 1):
            bl(col, cx + sx * (w / 2 + ox - 1.5), dc, z_eave + rise + 3.4, 2.6, 2.6, mat("gold", 2), sub=1)


def post_set(col, xs, d, z0, h, size, m):
    for x in xs:
        bx(col, x, d - size / 2, z0, size, size, h, m, bevel=0.6)


def door(col, cx, d, z0, w, h, leaf="red"):
    bx(col, cx, d - 1.5, z0, w + 5, 2.5, h + 4, mat("wood", 0))
    bx(col, cx, d - 2.5, z0, w, 1.8, h, mat(leaf, 1), bevel=0.5)
    bx(col, cx, d - 3.4, z0 + 2, 1.4, 1.0, h - 4, mat("wood", 0))
    for sx in (-1, 1):
        bl(col, cx + sx * 3.2, d - 4, z0 + h * 0.48, 1.3, 1.3, mat("gold", 2), sub=1)
    for k in range(2):
        for sx in (-1, 1):
            bl(col, cx + sx * (w / 2 - 2.2), d - 3.4, z0 + h * (0.28 + 0.4 * k), 0.9, 0.9, mat("gold", 1), sub=1)


def window(col, cx, d, z0, w, h, shutter=False):
    bx(col, cx, d - 1.0, z0, w + 3, 2.0, h + 3, mat("wood", 0))
    bx(col, cx, d - 1.6, z0 + 0.8, w, 1.6, h - 1.0, mat("paper", 2))
    bx(col, cx, d - 2.4, z0 + h / 2 - 0.2, w, 1.0, 1.5, mat("wood", 1))
    bx(col, cx, d - 2.4, z0, 1.5, 1.0, h, mat("wood", 1))
    if shutter:
        for sx in (-1, 1):
            bx(col, cx + sx * (w / 2 + 3.2), d - 1.8, z0, 3.5, 1.4, h, mat("red", 1))


def lantern(col, cx, dc, zc, r=4.0, glow=1.0, ramp="lava", string=True):
    """Paper lantern: a glowing body with gold caps and a tassel."""
    if string:
        bx(col, cx, dc - 0.4, zc + r, 0.9, 0.9, 5, mat("wood", 0))
    bl(col, cx, dc, zc, r * 0.85, r, mat(ramp, 2, emit=1.4 * glow), sub=1)
    cy(col, cx, dc, zc + r * 0.9, r * 0.45, 1.6, mat("gold", 2), seg=8)
    cy(col, cx, dc, zc - r - 0.8, r * 0.45, 1.6, mat("gold", 2), seg=8)
    bx(col, cx, dc - 0.3, zc - r - 5, 0.9, 0.9, 4.2, mat("red", 1))


def stone_base(col, cx, w, d, h, steps=1, ramp="stone"):
    for k in range(steps):
        sh = 2.2 * k
        bx(col, cx, -1.0 + sh * 0.5, h * k / steps, w - 2 * sh, d - sh, h / steps, mat(ramp, 1 if k % 2 == 0 else 2), bevel=0.8)


def scroll(col, cx, d, zc, ramp="paper", cap="red", length=5.0):
    cy(col, cx, d, zc - length / 2, 1.3, length, mat(ramp, 2), seg=6)
    cy(col, cx, d, zc + length / 2 - 0.2, 1.6, 0.9, mat(cap, 1), seg=6)


# =========================================================================== buildings
def house(col, v, f=0):
    teal = ("teal", "red", "steel")[v]
    wall_ramp = ("paper", "paper", "paper")[v]
    W, Dp = 76, 12
    shadow(col, 0, 5, 42, 10)
    stone_base(col, 0, W + 8, Dp + 4, 4, steps=1)
    bx(col, 0, 1.0, 4, W, Dp, 60, mat(wall_ramp, 2 if v != 1 else 1), bevel=0.8)
    post_set(col, (-W / 2 + 1, W / 2 - 1), 1.0, 4, 60, 4.5, mat("wood", 1))
    bx(col, 0, -0.5, 61, W + 2, 3.5, 4.5, mat("wood", 1), bevel=0.8)            # tie beam under the eaves
    door(col, 0, 0.8, 4, 19, 55, leaf=("red", "wood", "red")[v])
    for sx in (-1, 1):
        window(col, sx * 26, 0.8, 32, 12, 14, shutter=(v == 2))
    roof(col, 0, 7, W, Dp, 65, 9, 7, 4, teal, up=4.0)
    if v == 1:                                              # hanging lantern and a banner
        lantern(col, 32, -3, 52, 3.6)
        bx(col, -32, -2.5, 32, 6, 1.0, 26, mat("red", 1))
    if v == 2:                                              # herb basket and a lantern
        lantern(col, -32, -3, 50, 3.4)
        bl(col, 31, -5, 7, 5.5, 3.5, mat("wood", 2), sub=1)
    if v == 0:
        lantern(col, 32, -3, 52, 3.4)


def hut(col, v=0, f=0):
    W, Dp = 100, 30
    shadow(col, 0, 8, 56, 16)
    bx(col, 0, 0, 0, W + 6, Dp + 4, 4, mat("stone", 1), bevel=0.8)
    bx(col, 0, 2, 4, W, Dp, 56, mat("wood", 2), bevel=0.8)
    for k in range(10):                                     # vertical boards
        bx(col, -W / 2 + 5 + k * 10, 1.0, 5, 0.9, 1.0, 54, mat("wood", 0))
    post_set(col, (-W / 2, W / 2, -34, 34), 2, 4, 56, 5, mat("wood", 1))
    door(col, 0, 1.4, 4, 20, 52, leaf="wood")
    window(col, -32, 1.4, 28, 14, 14)
    window(col, 32, 1.4, 28, 14, 14)
    roof(col, 0, 16, W, Dp, 59, 17, 10, 8, "earth", up=3.0, courses=12, step=1)
    for k in range(7):                                      # straw tufts on the eave
        bx(col, -45 + k * 15, -(11 - 1.8), 54, 6, 2, 6, mat("earth", 1))
    for k in range(3):                                      # hanging herbs and a gourd by the door
        bl(col, 28 + k * 5, -3, 46 - k * 2, 2.2, 3.6, mat("glow_g", 1, emit=0.5), sub=1)
    bl(col, -30, -3, 48, 4, 5, mat("gold", 2), sub=1)
    bx(col, -30, -3.4, 52, 1.0, 1.0, 6, mat("wood", 0))
    bl(col, 40, 1, 5, 6, 4, mat("wood", 2), sub=1)          # a stack of wood / barrel
    cy(col, -42, 1, 4, 5, 9, mat("wood", 1), seg=10)


def pavilion(col, v=0, f=0):
    shadow(col, 0, 10, 52, 14)
    stone_base(col, 0, 100, 30, 7, steps=2, ramp="stone")
    bx(col, 0, 3, 7, 88, 24, 1.5, mat("wood", 1), bevel=0.4)                            # timber deck inside the pillars
    xs = (-40, -13, 13, 40)
    for x in xs:
        cy(col, x, 3, 7, 2.8, 40, mat("red", 1), seg=8)
        bx(col, x, 1.5, 7, 6.5, 3.5, 2.5, mat("stone", 2))
    for x in (-40, 40):
        cy(col, x, 22, 7, 2.8, 40, mat("red", 1), seg=8)
    bx(col, 0, 0.5, 44, 92, 5, 4.5, mat("wood", 1), bevel=0.8)
    bx(col, 0, 20, 44, 92, 5, 4.5, mat("wood", 1), bevel=0.8)
    bx(col, 0, 3, 48, 86, 20, 2.5, mat("wood", 0))
    for x in (-27, 0, 27):                                  # banner boards with abstract gold strokes
        bx(col, x, 0.2, 30, 12, 1.0, 10, mat("paper", 2))
        for k in range(3):
            bx(col, x - 3 + k * 3, -0.6, 32, 1.2, 0.6, 6, mat("gold", 1))
    roof(col, 0, 12, 88, 24, 50, 14, 7, 5, "teal", hip=True, up=5.0, courses=6)
    roof(col, 0, 12, 50, 12, 62, 14, 5, 4, "teal", hip=True, up=4.0, courses=5, step=2)
    cy(col, 0, 12, 73, 1.2, 7, mat("gold", 2), seg=6)
    bl(col, 0, 12, 82, 2.4, 3.0, mat("gold", 2), sub=1)
    sway = (0, 2, 0, -2)[f % 4]
    for x in (-38, 38):
        lantern(col, x + sway, -4, 36, 4.0, glow=(0.8, 1.1, 1.4, 1.1)[f % 4])
    lantern(col, sway * 0.5, -4, 38, 4.2, glow=(1.2, 1.0, 0.8, 1.0)[f % 4])


def library(col, v=0, f=0):
    shadow(col, 0, 10, 56, 14)
    stone_base(col, 0, 112, 36, 6, steps=2)
    # ground floor: open front, scroll racks along the back wall
    bx(col, 0, 19, 6, 98, 3, 38, mat("wood", 0))
    for r in range(3):
        bx(col, 0, 15, 12 + r * 11, 90, 5, 1.6, mat("wood", 1))
        for k in range(15):
            scroll(col, -42 + k * 6, 16.5, 12 + r * 11 + 4, ramp=("paper", "bone", "paper")[(k + r) % 3],
                   cap=("red", "gold", "teal")[(k + 2 * r) % 3], length=5)
    for x in (-46, -16, 16, 46):
        cy(col, x, 3, 6, 3.0, 38, mat("red", 1), seg=8)
    bx(col, 0, 1, 44, 100, 5, 4, mat("wood", 1), bevel=0.8)
    for sx in (-1, 1):
        bx(col, sx * 31, 1.2, 6, 26, 1.6, 8, mat("wood", 1), bevel=0.4)                    # low balustrade: the racks show above it
    door(col, 0, 1.2, 6, 18, 36, leaf="wood")
    roof(col, 0, 11, 90, 20, 47, 6, 12, 5, "teal", up=4.0, courses=6, step=1)
    bx(col, 0, 5, 50, 62, 14, 20, mat("paper", 2), bevel=0.8)                            # upper floor
    post_set(col, (-30, 30), 5, 50, 20, 4, mat("red", 1))
    for sx in (-1, 0, 1):
        window(col, sx * 19, 4.5, 54, 12, 11)
    bx(col, 0, 4.0, 62, 22, 1.2, 7, mat("red", 1))
    for k in range(4):
        bx(col, -7.5 + k * 5, 3.2, 63.5, 2.2, 0.8, 4.5, mat("gold", 2))
    roof(col, 0, 12, 66, 14, 70, 10, 9, 5, "teal", up=5.0, courses=7, step=1)
    lantern(col, -50, -5, 38, 4.0)
    lantern(col, 50, -5, 38, 4.0)

def stall(col, v, f=0):
    shadow(col, 0, 7, 36, 10)
    bx(col, 0, 2, 0, 64, 11, 17, mat("wood", 1), bevel=0.8)                              # counter
    bx(col, 0, 1.2, 16, 68, 13, 2.5, mat("wood", 2), bevel=0.8)
    for x in (-34, 34):
        bx(col, x, 0, 0, 3.5, 3.5, 38, mat("wood", 0), bevel=0.5)
        bx(col, x, 12, 0, 3.5, 3.5, 42, mat("wood", 0), bevel=0.5)
    c1, c2 = (("red", "paper"), ("teal", "paper"))[v]
    for k in range(10):                                     # striped awning, slanting up to the back
        x = -38 + k * 7.6
        m = mat(c1 if k % 2 == 0 else c2, 1 if k % 2 == 0 else 2)
        bx(col, x + 3.8, -3, 40, 7.5, 17, 2.4, m, bevel=0.4)
        bx(col, x + 3.8, -4.5, 36, 7.5, 2.4, 5.0, m)
    if v == 0:                                              # fruit, grain, a bowl
        for k in range(5):
            bl(col, -25 + k * 5.6, 6, 22, 2.9, 2.9, mat(("red", "gold", "red", "foliage", "gold")[k], 1), sub=1)
        cy(col, 18, 7, 18.5, 7, 6, mat("wood", 2), seg=10)
        for k in range(6):
            bl(col, 13 + k * 2.8, 7, 25, 1.8, 1.8, mat("gold", 2), sub=1)
        bl(col, 29, 6, 22, 4.5, 4.5, mat("paper", 1), sub=1)
    else:                                                   # jars and pill bottles
        for k, (xx, hh) in enumerate(((-26, 8), (-16, 11), (-6, 7), (6, 9))):
            cy(col, xx, 6, 18.5, 3.6, hh, mat(("teal", "earth", "wood", "teal")[k], 2), seg=10)
            cy(col, xx, 6, 18.5 + hh, 2.2, 2.0, mat("red", 1), seg=8)
        for k in range(3):
            bl(col, 18 + k * 5.0, 6, 21, 2.2, 2.9, mat("glow_g", 1, emit=0.6), sub=1)
        bx(col, 27, 5, 18.5, 10, 6, 2.5, mat("paper", 2))
    lantern(col, 0, -4, 31, 3.2)

def shrine(col, v=0, f=0):
    shadow(col, 0, 12, 26, 11)
    stone_base(col, 0, 52, 28, 8, steps=3)
    bx(col, 0, 6, 8, 30, 14, 8, mat("stone", 2), bevel=0.8)                              # altar
    bx(col, 0, 9, 16, 22, 3, 26, mat("rock", 1), bevel=0.8)                              # stele
    for k in range(4):                                      # abstract glow strokes (no letters)
        bx(col, -5 + k * 3.4, 7.8, 26 + (k % 2) * 2, 1.4, 0.8, 9, mat("gold", 2, emit=0.8))
    for x in (-13, 13):
        bx(col, x, 8, 8, 3.5, 3.5, 36, mat("red", 1), bevel=0.5)
    roof(col, 0, 12, 34, 12, 44, 10, 8, 6, "red", up=4.0, courses=5)
    cy(col, 0, 2, 8, 6.0, 5.5, mat("gold", 1), seg=10, r1=7.5)                           # incense burner
    for k in range(3):
        bx(col, -2 + k * 2, 2, 13.5, 0.9, 0.9, 6, mat("wood", 0))
        bl(col, -2 + k * 2, 2, 19.8, 0.8, 0.8, mat("lava", 3, emit=2.2, prio=3.0), sub=1)
    for k in range(4):                                      # smoke: puffs rise 2 px per frame, loop after 4
        z = 24 + ((k * 8 + f * 2) % 32)
        r = 1.8 + (z - 24) * 0.05
        bl(col, 1 + math.sin(z * 0.3) * 2.0, 3, z, r, r, mat("bone", 2), sub=1)
    lantern(col, -22, 6, 32, 3.4, glow=(0.8, 1.1, 1.3, 1.0)[f % 4])
    lantern(col, 22, 6, 32, 3.4, glow=(1.2, 1.0, 0.8, 1.0)[f % 4])


def furnace(col, v=0, f=0):
    shadow(col, 0, 6, 19, 7)
    bx(col, 0, 0, 0, 34, 12, 5, mat("stone", 1), bevel=0.8)
    cy(col, 0, 6, 5, 14, 18, mat("earth", 1), seg=14, r1=10.5)                           # clay body
    cy(col, 0, 6, 23, 10.5, 3, mat("stone", 2), seg=14, r1=9.5)
    cy(col, 5, 8, 26, 3.0, 7, mat("stone", 1), seg=8)                                   # chimney
    bx(col, 0, -1, 7, 16, 3, 13, mat("basalt", 0), bevel=0.6)                            # fire mouth
    fl = ((0, 0), (1, 2), (-1, 3), (0, 1))[f % 4]
    bl(col, fl[0] * 1.5, -2, 11, 5, 4.2 + fl[1] * 0.8, mat("lava", 2, emit=2.0), sub=1)
    bl(col, -fl[0], -3, 10, 3, 3 + fl[1] * 0.6, mat("lava", 3, emit=2.6, prio=3.0), sub=1)
    bl(col, 2 * fl[0], -2.4, 14 + fl[1] * 0.4, 2.2, 3.4, mat("lava", 3, emit=2.2), sub=1)
    for x in (-12, 12):
        bx(col, x, 2, 5, 3, 3, 12, mat("red", 1))
    bl(col, 5 + (0, 1, 0, -1)[f % 4], 8, 36 + (f % 4), 1.8, 1.6, mat("bone", 1), sub=1)

def anvil(col, v=0, f=0):
    shadow(col, 0, 7, 22, 7)
    cy(col, 0, 7, 0, 10, 10, mat("bark", 1), seg=10, r1=9)
    cy(col, 0, 7, 10, 9, 0.8, mat("wood", 0), seg=10)
    bx(col, 0, 4, 11, 22, 8, 4, mat("steel", 1), bevel=0.8)                              # body
    bx(col, 0, 5, 15, 26, 7, 3.2, mat("steel", 2), bevel=0.8)                            # face
    C.cyl(col, "horn", (X(13), Y(8.5), Z(16)), X(2.8), X(0.6), Z(6), mat("steel", 2), seg=8, tilt=(0.7, 0))
    bl(col, -2, 8, 19.6, 6, 0.9, mat("lava", 2, emit=1.3), sub=1)                        # a hot bar
    bx(col, -17, 9, 0, 3, 3, 10, mat("wood", 1))                                         # hammer leaning on the stump
    bx(col, -17, 8, 9, 7, 4, 4.5, mat("steel", 1), bevel=0.5)
    for k in range(3):
        bl(col, 1 + k * 3, 6, 20 + k * 2, 0.9, 0.9, mat("lava", 3, emit=2.5, prio=3.0), sub=1)


def board(col, v=0, f=0):
    shadow(col, 0, 4, 18, 5)
    for x in (-16, 16):
        bx(col, x, 1, 0, 4, 4, 34, mat("wood", 0), bevel=0.5)
    bx(col, 0, 2, 8, 38, 2, 24, mat("wood", 1), bevel=0.6)
    for k, (x, z, w, h) in enumerate(((-9, 20, 9, 10), (4, 22, 10, 8), (-3, 11, 11, 7), (12, 12, 7, 9))):
        bx(col, x, 0.8, z, w, 1, h, mat("paper", 2))
        bx(col, x, 0.4, z + h - 2.5, w - 3, 0.6, 1.0, mat("red", 1))
    roof(col, 0, 3, 36, 5, 35, 5, 3, 3, "teal", up=3.0, courses=4)

def well(col, v=0, f=0):
    shadow(col, 0, 8, 22, 9)
    cy(col, 0, 8, 0, 17, 10, mat("stone", 1), seg=18, r1=16)
    cy(col, 0, 8, 10, 17, 3, mat("stone", 2), seg=18, r1=17)
    cy(col, 0, 8, 12.6, 12.5, 0.6, mat("water", 1), seg=18)                              # water
    for x in (-15, 15):
        bx(col, x, 8, 11, 3.2, 3.2, 12, mat("wood", 1), bevel=0.5)
    bx(col, 0, 8, 22, 36, 3, 3, mat("wood", 0), bevel=0.5)
    roof(col, 0, 8, 30, 6, 24, 3, 4, 3, "teal", up=2.0, courses=3)
    tubep(col, [(0, 8, 22), (0, 8, 15)], 0.5, mat("wood", 0), seg=4)
    cy(col, 0, 8, 12, 3.2, 5, mat("wood", 2), seg=8, r1=2.8)

def lantern_post(col, v=0, f=0):
    shadow(col, 0, 3, 6, 3)
    bx(col, 0, 1, 0, 7, 6, 5, mat("stone", 2), bevel=0.6)
    bx(col, 0, 2.5, 5, 3, 3, 24, mat("wood", 1), bevel=0.4)
    bx(col, 1.5, 2.2, 28, 6, 2.2, 2, mat("wood", 0))
    g = (0.9, 1.25, 1.5, 1.1)[f % 4]
    lantern(col, 3.5, 2.4, 32, 3.2, glow=g, string=False)
    bl(col, 3.5, 2.4, 32, 2.0, 2.4, mat("lava", 3, emit=2.0 * g), sub=1)


def portal(col, v=0, f=0):
    shadow(col, 0, 5, 28, 7)
    for x in (-22, 22):                                     # stone pillars with glowing rune bands
        bx(col, x, 0, 0, 10, 8, 50, mat("rock", 1), bevel=1.2)
        for k in range(3):
            bx(col, x, -0.3, 10 + k * 13, 6, 0.8, 3, mat("crys_c", 2, emit=1.1))
    bx(col, 0, 0, 48, 56, 8, 9, mat("rock", 2), bevel=1.2)
    bl(col, 0, 3, 61, 5, 3.4, mat("crys_c", 2, emit=1.8), sub=1)
    # swirling light between the pillars
    bl(col, 0, 5, 26, 17, 23, mat("crys_v", 0, emit=0.6), sub=2, ry=1.2)
    for k in range(3):
        pts = []
        for i in range(12):
            r = 3 + i * 1.5
            a = f * math.pi / 6 + k * 2.094 + i * 0.5
            pts.append((r * math.cos(a) * 0.9, 3.5, 26 + r * math.sin(a) * 1.25))
        tubep(col, pts, 1.7, mat("crys_c", 3, emit=2.2, prio=2.0), seg=4)
    for k in range(5):
        a = f * 0.8 + k * 1.26
        bl(col, 22 * math.cos(a) * 0.8, 3, 26 + 22 * math.sin(a), 1.0, 1.0, mat("crys_c", 3, emit=2.6, prio=4.0), sub=1)


def td_gate(col, v=0, f=0):
    shadow(col, 0, 8, 32, 9)
    for x in (-28, 28):
        bx(col, x, 0, 0, 11, 10, 46, mat("red", 1), bevel=1.2)
        bx(col, x, -1.5, 0, 14, 12, 6, mat("stone", 2), bevel=1.0)
    bx(col, 0, 0, 44, 66, 10, 7, mat("red", 1), bevel=1.0)
    roof(col, 0, 5, 66, 10, 51, 9, 4, 4, "teal", up=5.0, courses=6)
    bx(col, 0, -1.2, 47, 18, 1.2, 6, mat("gold", 1))
    for k in range(3):
        bx(col, -5 + k * 5, -2, 48.5, 1.6, 0.8, 4, mat("gold", 3, emit=1.6))
    g = (0.8, 1.2, 1.6, 1.2)[f % 4]
    bl(col, 0, 5, 26, 22, 24, mat("crys_c", 0), sub=2, ry=1.0)
    for k in range(4):                                      # shimmering strands in the curtain
        pts = [(-15 + k * 10 + math.sin(z * 0.25 + f * 1.57 + k) * 3, 4, z) for z in range(6, 50, 6)]
        tubep(col, pts, 1.5, mat("crys_c", 2, emit=1.6 * g, prio=2.0), seg=4)
    for k in range(4):
        z = 8 + ((k * 12 + f * 3) % 44)
        bl(col, -14 + k * 9, 4, z, 2.4, 3.2, mat("crys_c", 3, emit=2.4, prio=3.0), sub=1)
    for x in (-28, 28):
        lantern(col, x, -6, 50, 4.0, glow=g)


def realm_gate(col, v=0, f=0):
    shadow(col, 0, 6, 33, 8)
    for x in (-27, 27):
        bx(col, x, 0, 0, 12, 10, 56, mat("basalt", 1), bevel=1.2)
        bx(col, x, -0.4, 4, 9, 0.8, 48, mat("stone", 1))
    bx(col, 0, 0, 54, 72, 9, 8, mat("basalt", 0), bevel=1.0)
    bx(col, 0, -1.0, 58, 14, 1.5, 7, mat("red", 1))
    # torn curtain of ink with purple light, swirling
    bl(col, 0, 5, 28, 21, 26, mat("ink", 0), sub=2, ry=1.2)
    for k in range(3):
        pts = []
        for i in range(10):
            z = 6 + i * 5.2
            x = math.sin(z * 0.28 + f * math.pi / 2 + k * 2.1) * (6 + 4 * k)
            pts.append((x, 4, z))
        tubep(col, pts, 1.8, mat("mist", 2, emit=1.8, prio=2.0), seg=4)
    for k in range(4):
        a = f * 0.9 + k * 1.57
        bl(col, 20 * math.cos(a), 3.5, 28 + 22 * math.sin(a), 1.1, 1.1, mat("mist", 3, emit=2.6, prio=4.0), sub=1)


def sign(col, v=0, f=0):
    shadow(col, 0, 3, 9, 3)
    bx(col, 0, 2, 0, 3.5, 3.5, 22, mat("wood", 0), bevel=0.4)
    bx(col, 0, 1, 9, 22, 2.2, 12, mat("wood", 2), bevel=0.6)
    for k in range(3):
        bx(col, -5 + k * 5, 0.2, 11.5, 1.8, 0.7, 7, mat("red", 1))
    roof(col, 0, 2, 20, 4, 22, 3, 2, 2, "red", up=2.0, courses=3)

def tablet(col, v=0, f=0):
    shadow(col, 0, 3, 11, 3.5)
    bx(col, 0, 0, 0, 18, 6, 4, mat("stone", 2), bevel=0.8)
    bx(col, 0, 1.5, 4, 13, 3.5, 24, mat("rock", 1), bevel=1.0)
    for k in range(4):
        bx(col, -4.5 + k * 3, 0.4, 12 + (k % 2) * 2, 1.4, 0.7, 10, mat("gold", 2, emit=0.7))
    roof(col, 0, 3, 14, 4, 27, 3, 2, 2, "teal", up=2.0, courses=3)

def table(col, v=0, f=0):
    shadow(col, 0, 5, 21, 5)
    bx(col, 0, 2, 8, 40, 10, 3, mat("wood", 2), bevel=0.8)
    for x in (-17, 17):
        for d in (3, 10):
            bx(col, x, d, 0, 3, 3, 8, mat("wood", 0), bevel=0.4)
    cy(col, -8, 6, 11, 3.2, 3.5, mat("steel", 2), seg=10, r1=2.6)                        # teapot
    bl(col, -8, 6, 15, 2.2, 1.3, mat("steel", 2), sub=1)
    for k in range(2):
        cy(col, 2 + k * 6, 5, 11, 1.7, 1.8, mat("paper", 3), seg=8)
    bx(col, 13, 4, 11, 9, 5, 1.0, mat("paper", 2))
    bx(col, 13, 4, 12, 9, 1.0, 1.0, mat("red", 1))

def gate(col, v=0, f=0):
    shadow(col, 0, 4, 26, 7)
    for x in (-22, 22):
        bx(col, x, 0, 0, 7, 7, 37, mat("red", 1), bevel=0.8)
        bx(col, x, -0.8, 0, 10, 9, 4, mat("stone", 2), bevel=0.8)
    bx(col, 0, 0, 33, 50, 7, 5, mat("red", 0), bevel=0.8)
    roof(col, 0, 3.5, 48, 7, 37, 8, 4, 4, "teal", up=3.5, courses=5)
    bx(col, 0, -0.6, 38, 16, 1.0, 6, mat("gold", 1))
    for x in (-15, 15):
        lantern(col, x, -2, 25, 3.4)


def mat_(col, v=0, f=0):
    shadow(col, 0, 8, 21, 7)
    bx(col, 0, 1, 0, 40, 22, 2.5, mat("gold", 1), bevel=0.8)
    for k in range(7):
        bx(col, -17 + k * 5.6, 1.5, 2.3, 0.9, 21, 0.6, mat("earth", 2 if k % 2 else 1))
    bl(col, -13, 11, 5, 6, 3.2, mat("paper", 2), sub=1, ry=4)                            # pillow
    bx(col, 8, 6, 2.5, 12, 8, 0.8, mat("red", 1))


def hive(col, v=0, f=0):
    shadow(col, 0, 5, 14, 5)
    for x in (-8, 8):
        bx(col, x, 3, 0, 3, 3, 19, mat("wood", 0), bevel=0.4)
    bx(col, 0, 1, 19, 24, 12, 17, mat("wood", 2), bevel=0.8)
    bx(col, 0, 0.2, 23, 6, 1.0, 5, mat("basalt", 0))                                     # entrance
    roof(col, 0, 7, 24, 12, 36, 4, 3, 3, "earth", up=2.0, courses=3, step=1)
    for k in range(2):
        bl(col, -6 + k * 9, 0, 29 - k * 3, 1.6, 3.4, mat("gold", 3), sub=1)                # honey
    for k in range(3):                                      # bees circle the hive
        a = f * math.pi / 2 + k * 2.1
        bl(col, 15 * math.cos(a), 3 + 5 * math.sin(a), 32 + 5 * math.sin(a * 2), 1.3, 1.3, mat("gold", 2, prio=4.0), sub=1)
        bl(col, 15 * math.cos(a), 3 + 5 * math.sin(a), 33.6 + 5 * math.sin(a * 2), 0.8, 0.8, mat("basalt", 0, prio=4.0), sub=1)


# name, (W, H) of the old sprite doubled, builder, variants, frames, solid (dx, dy, w, h) relative to the pivot, Vietnamese name
BUILDINGS = [
    ("hut", (128, 112), hut, 1, 1, (-54, -26, 108, 26), "Nhà tranh"),
    ("house", (96, 96), house, 3, 1, (-40, -20, 80, 20), "Nhà gỗ"),
    ("pavilion", (128, 128), pavilion, 1, 4, (-50, -40, 100, 40), "Đình"),
    ("library", (128, 112), library, 1, 1, (-54, -44, 108, 44), "Tàng Kinh Các"),
    ("stall", (80, 64), stall, 2, 1, (-34, -18, 68, 18), "Quầy hàng"),
    ("shrine", (64, 88), shrine, 1, 4, (-24, -22, 48, 22), "Miếu thờ"),
    ("furnace", (48, 56), furnace, 1, 4, (-16, -12, 32, 12), "Lò luyện đan"),
    ("anvil", (48, 40), anvil, 1, 1, (-11, -10, 22, 10), "Đe rèn"),
    ("board", (48, 56), board, 1, 1, (-18, -6, 36, 6), "Bảng thông báo"),
    ("well", (48, 48), well, 1, 1, (-17, -16, 34, 16), "Giếng nước"),
    ("lantern", (16, 48), lantern_post, 1, 4, (-3, -5, 6, 5), "Đèn lồng"),
    ("portal", (64, 80), portal, 1, 4, (-26, -8, 52, 8), "Cổng dịch chuyển"),
    ("td_gate", (80, 80), td_gate, 1, 4, (-36, -10, 72, 10), "Cổng thủ thành"),
    ("realm_gate", (80, 80), realm_gate, 1, 4, (-34, -10, 68, 10), "Cổng Bí Cảnh"),
    ("sign", (32, 40), sign, 1, 1, (-3, -4, 6, 4), "Biển chỉ đường"),
    ("tablet", (32, 48), tablet, 1, 1, (-8, -6, 16, 6), "Bia đá"),
    ("table", (48, 32), table, 1, 1, (-18, -12, 36, 12), "Bàn trà"),
    ("gate", (64, 64), gate, 1, 1, None, "Cổng làng"),
    ("mat", (48, 32), mat_, 1, 1, None, "Chiếu"),
    ("hive", (96 // 2, 64), hive, 1, 4, (-12, -8, 24, 8), "Tổ ong"),
]
