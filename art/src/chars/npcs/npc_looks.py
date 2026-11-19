"""Village NPC looks on the v2 body (runs inside Blender).

Same body, rig and bones as the player; each NPC is an outfit plus a body-mesh variation
(women: narrower shoulders and chest; the smith: broader) applied to the torso pieces only,
so the skinning still follows the shared bones. Colours follow the old code-drawn villagers
(client/engine/sprites.py::NPC_LOOKS) so they stay recognisable.
"""
from __future__ import annotations

import math

import bpy
from mathutils import Matrix, Vector

import geo
import ld_body as LB
import ld_looks as LL
import rig as R
from ld_body import V, build_body, build_hair, build_head, build_legs, cuboid, limb
from ld_looks import WAIST, belt, lapels, skirt_panels, sleeves, upper_garment

NPCS = {
    "shopkeeper": "Chủ Tiệm",
    "alchemist": "Đan Sư",
    "smith": "Thợ Rèn",
    "librarian": "Thủ Thư",
    "guide": "Tiểu Lan",
    "fisher": "Ngư Ông",
    "truc_lao": "Trúc Lão",
    "villager": "Dân Làng",
}

# how each one stands and moves: stoop (deg), gesture, holds (prop in a hand)
STYLE = {
    "shopkeeper": dict(stoop=2, idle="nod", hands="clasp", plump=True),
    "alchemist": dict(stoop=5, idle="sway", hands="behind"),
    "smith": dict(stoop=0, idle="shift", hands="fists", wide=True),
    "librarian": dict(stoop=0, idle="tilt", hands="scroll", woman=True),
    "guide": dict(stoop=-2, idle="bounce", hands="clasp", woman=True),
    "fisher": dict(stoop=12, idle="bob", hands="behind"),
    "truc_lao": dict(stoop=10, idle="beard", hands="staff"),
    "villager": dict(stoop=0, idle="breathe", hands="loose"),
}


def srgb(rgb):
    return tuple(c ** 2.2 for c in rgb)


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


class NKit(LB.Kit):
    """Kit that reshapes the torso pieces for a woman (narrower shoulders) or the smith
    (broader), leaving limbs, hands and head exactly on their bones."""

    def __init__(self, rig, col, *, shoulders=1.0, depth=1.0):
        super().__init__(rig, col)
        self.sx, self.sy = shoulders, depth

    def add(self, name, part, mat, wfn, **kw):
        if (self.sx != 1.0 or self.sy != 1.0) and callable(wfn):
            v, f = part
            cen = sum((Vector(p) for p in v), Vector()) / max(len(v), 1)
            w = wfn(cen)
            top = max(w, key=w.get) if w else ""
            if top in ("spine", "chest", "neck") or (top == "hips" and cen.z > 0.52):
                out = []
                for p in v:
                    p = Vector(p)
                    k = max(0.0, min(1.0, (p.z - 0.52) / 0.16))        # full effect at the chest
                    p.x *= 1 + (self.sx - 1) * k
                    p.y *= 1 + (self.sy - 1) * k
                    out.append(p)
                part = (out, f)
        return super().add(name, part, mat, wfn, **kw)

    def drop(self, prefix):
        for ob in [o for o in self.objs if o.name.startswith(prefix)]:
            self.objs.remove(ob)
            bpy.data.objects.remove(ob, do_unlink=True)


# ---------------------------------------------------------------- pieces
def hair_style(k: NKit, hair, hi, tie, style, ornament=None):
    """bun (topknot) | long (topknot + hair down the back) | short (no knot) |
    twin (two buns, a girl's style) | none (under a hat)."""
    build_hair(k, hair, tie, hair_hi=hi, long=(style == "long"), ornament=ornament)
    if style in ("short", "twin", "none"):
        k.drop("SM_hair_bun")
        k.drop("SM_hair_tie")
    if style == "twin":
        head = R.w_rigid("head")
        for s in (1, -1):
            k.add("SM_hair_bun2", geo.ellipsoid((s * 0.085, 0.02, 1.0), (0.038, 0.036, 0.036), 8, 6), hair, head)
            k.add("SM_hair_tie2", geo.ellipsoid((s * 0.07, 0.0, 0.975), (0.018, 0.016, 0.014), 6, 4), tie, head)
    if style in ("none", "long", "twin"):      # women and hats: no spiky tufts
        k.drop("SM_hair_tuft")


def beard(k: NKit, m, long=False, brows=False):
    head = R.w_rigid("head")
    zb = 0.60 if long else 0.69
    pts = [V(0, -0.088, 0.765), V(0, -0.098, 0.73), V(0, -0.092, (0.73 + zb) / 2), V(0, -0.08, zb)]
    k.add("SM_beard", geo.sweep(pts, [(0.05, 0.02), (0.052, 0.024), (0.04, 0.02), (0.0, 0.012)], 6, up=(0, -1, 0)), m,
          head if not long else R.w_chain(["head", "chest"], 0.76, 0.62))
    for s in (1, -1):      # moustache
        k.add("SM_moustache", LB.lock(V(s * 0.006, -0.1, 0.786), (s * 0.8, -0.1, -0.6), 0.05, 0.016, thick=0.008,
                                      side=(0, 0, 1)), m, head)
        if brows:          # long white brows hanging past the eyes
            k.add("SM_brow_long", LB.lock(V(s * 0.02, -0.098, LB.EYE_Z + 0.036), (s * 0.9, -0.15, -0.4), 0.07, 0.016,
                                          thick=0.008, side=(0, 0, 1)), m, head)


def cap(k: NKit, m):
    head = R.w_rigid("head")
    k.add("SM_cap", geo.lathe([(0.93, 0.118, 0.11, 0.01), (0.975, 0.112, 0.106, 0.01), (1.03, 0.09, 0.088, 0.01),
                               (1.045, 0.0, 0.0, 0.01)], 8, phase=math.pi / 8), m, head)


def straw_hat(k: NKit, m):
    head = R.w_rigid("head")
    k.add("SM_straw_hat", geo.lathe([(0.925, 0.0, 0.0), (0.93, 0.25, 0.24), (0.965, 0.17, 0.165), (1.03, 0.08, 0.08),
                                     (1.075, 0.0, 0.0)], 12), m, head, solid=0.01)


def headband(k: NKit, m):
    head = R.w_rigid("head")
    k.add("SM_headband", geo.lathe([(0.915, 0.136, 0.124, 0.01), (0.942, 0.13, 0.12, 0.01)], 8, phase=math.pi / 8,
                                   cap_bottom=False, cap_top=False), m, head, solid=0.012)
    k.add("SM_headband_tail", LB.lock(V(0, 0.11, 0.9), (0.2, 0.6, -0.7), 0.09, 0.018, thick=0.006, side=(1, 0, 0)), m,
          head)


def pouch_and_abacus(k: NKit, pouch, frame, beads):
    hips = R.w_rigid("hips")
    k.add("SM_pouch", cuboid((0.095, -0.06, WAIST - 0.045), (0.026, 0.02, 0.03), top_scale=(0.8, 0.8)), pouch, hips)
    k.add("SM_abacus", cuboid((-0.085, -0.085, WAIST - 0.05), (0.04, 0.008, 0.026)), frame, hips)
    for dz in (-0.012, 0.0, 0.012):
        k.add("SM_abacus_beads", cuboid((-0.085, -0.095, WAIST - 0.05 + dz), (0.03, 0.006, 0.004)), beads, hips)


def gourd(k: NKit, m, cord):
    hips = R.w_rigid("hips")
    c = V(-0.115, -0.01, WAIST - 0.09)
    k.add("SM_gourd", geo.ellipsoid(c, (0.034, 0.032, 0.04), 8, 6), m, hips)
    k.add("SM_gourd_top", geo.ellipsoid(c + V(0, 0, 0.055), (0.022, 0.021, 0.024), 8, 5), m, hips)
    k.add("SM_gourd_cord", cuboid(c + V(0, 0, 0.033), (0.024, 0.024, 0.005)), cord, hips)


def apron(k: NKit, m, strap):
    wf = R.w_skirt(WAIST, 0.28, top_fn=R.w_near(["spine", "chest"], power=3))
    rows = []
    for z in (0.68, 0.62, 0.56, WAIST, 0.45, 0.36, 0.28):
        if z >= WAIST:
            yy = LL.torso_front(0, z, 0.03) * 1.05
            hw = 0.075 if z > 0.6 else 0.095
        else:
            yy = -0.13 - (WAIST - z) * 0.08
            hw = 0.11
        rows.append([V(x * hw, yy + 0.012 * abs(x), z) for x in (-1, -0.33, 0.33, 1)])
    k.add("SM_apron", geo.sheet(rows), m, wf, solid=0.01)
    for s in (1, -1):
        pts = [V(s * 0.07, LL.torso_front(s * 0.07, 0.68, 0.03), 0.68), V(s * 0.05, -0.03, 0.735), V(0, 0.07, 0.72)]
        k.add("SM_apron_strap", geo.sweep(pts, [(0.01, 0.004)] * 3, 4, tip=False), strap, R.w_rigid("chest"))


def hammer(k: NKit, wood, iron):
    hips = R.w_rigid("hips")
    k.add("SM_hammer_handle", limb([V(0.105, -0.06, WAIST + 0.03), V(0.12, -0.075, WAIST - 0.17)], [0.011, 0.011], 6),
          wood, hips)
    k.add("SM_hammer_head", cuboid((0.105, -0.06, WAIST + 0.045), (0.035, 0.018, 0.018)), iron, hips)


def scroll_in_hand(k: NKit, paper, rod):
    """Held in the left fist across the chest (rigid to the hand)."""
    hand = R.w_rigid("hand.L")
    wr = V(*R.BONES["hand.L"][0])
    c = wr + V(0.003, -0.03, -0.03)
    ax = V(0, -0.35, 1).normalized()            # held across the chest once the arm is raised
    k.add("SM_scroll", limb([c - ax * 0.075, c + ax * 0.075], [0.018, 0.018], 6), paper, hand)
    for t in (0.08, -0.08):
        k.add("SM_scroll_rod", limb([c + ax * (t - 0.01), c + ax * (t + 0.01)], [0.023, 0.023], 6), rod, hand)


def staff(k: NKit, bamboo, node):
    """A bamboo staff through the right fist, along the hand's weapon axis (the clips aim
    that axis up, so it stands on the ground beside him)."""
    hand = R.w_rigid("hand.R")
    wr = V(*R.BONES["hand.R"][0])
    c = wr + V(-0.003, -0.018, -0.04)
    ax = R.BLADE_REST["hand.R"]
    k.add("SM_staff", limb([c - ax * 0.36, c + ax * 0.72], [0.014, 0.012], 6), bamboo, hand)
    for t in (-0.2, 0.15, 0.4, 0.62):
        k.add("SM_staff_node", limb([c + ax * (t - 0.006), c + ax * (t + 0.006)], [0.017, 0.017], 6), node, hand)


# ---------------------------------------------------------------- the eight
def build(rig, col, npc_id):
    st = STYLE[npc_id]
    k = NKit(rig, col, shoulders=0.86 if st.get("woman") else (1.16 if st.get("wide") else (1.06 if st.get("plump") else 1.0)),
             depth=0.92 if st.get("woman") else (1.12 if st.get("wide") else (1.2 if st.get("plump") else 1.0)))
    p = f"MAT_npc_{npc_id}_"

    def m(name, rgb, ramp, **kw):
        return LB.mat(p + name, srgb(rgb), ramp, **kw)

    skin_rgb = (0.92, 0.70, 0.55) if npc_id not in ("fisher", "smith") else (0.80, 0.56, 0.40)
    skin = LB.mat(p + "skin", skin_rgb, "skin")
    white = m("white_hair", (0.90, 0.89, 0.86), "bone")
    white_hi = m("white_hair_hi", (1.0, 1.0, 0.98), "bone")

    def head(hair_rgb, style, ramp="hair", tie_rgb=(0.5, 0.38, 0.24), tie_ramp="wood", ornament=None):
        build_head(k, skin, skin_rgb=skin_rgb)
        hr = m("hair", hair_rgb, ramp)
        hh = m("hair_hi", tuple(min(1, c * 1.35 + 0.06) for c in hair_rgb), ramp)
        hair_style(k, hr, hh, m("tie", tie_rgb, tie_ramp), style, ornament=ornament)
        return hr

    if npc_id == "shopkeeper":
        tan, tan2 = m("robe", hexc("C9B48A"), "earth"), m("trim", hexc("8A7550"), "earth")
        head(hexc("5C3A21"), "none", ramp="wood")
        cap(k, m("cap", (0.26, 0.16, 0.30), "purple"))
        for s in (1, -1):        # a merchant's thin moustache
            k.add("SM_moustache", LB.lock(V(s * 0.006, -0.1, 0.786), (s * 0.85, -0.1, -0.5), 0.05, 0.012, thick=0.008,
                                          side=(0, 0, 1)), m("hair", hexc("5C3A21"), "wood"), R.w_rigid("head"))
        build_body(k, skin, tan)
        build_legs(k, m("trousers", (0.36, 0.28, 0.20), "wood"), m("shoe", (0.22, 0.16, 0.12), "wood"),
                   m("shoe", (0.22, 0.16, 0.12), "wood"), trouser_len=0.2, loose=0.066)
        upper_garment(k, "SM_robe", tan)
        skirt_panels(k, "SM_robe_skirt", tan, 0.20, flare=0.035, side_split=0.4)
        lapels(k, tan2)
        belt(k, m("belt", (0.40, 0.24, 0.12), "wood"), tails=False)
        sleeves(k, tan, tan2, to_elbow=False, wide=0.01, cuff=tan2)
        pouch_and_abacus(k, m("pouch", (0.55, 0.35, 0.18), "wood"), m("abacus", (0.30, 0.18, 0.10), "wood"),
                         m("beads", (0.85, 0.62, 0.30), "gold"))
    elif npc_id == "alchemist":
        blue, blue2 = m("robe", hexc("A8C6E0"), "blue"), m("trim", hexc("5F84A8"), "blue")
        head(hexc("8E8E8E"), "bun", ramp="stone", tie_rgb=(0.3, 0.4, 0.6), tie_ramp="blue")
        beard(k, m("beard", (0.62, 0.62, 0.62), "stone"), long=False)
        build_body(k, skin, blue)
        build_legs(k, m("trousers", (0.30, 0.36, 0.46), "blue"), m("shoe", (0.2, 0.22, 0.28), "stone"),
                   m("shoe", (0.2, 0.22, 0.28), "stone"), trouser_len=0.22, loose=0.064)
        upper_garment(k, "SM_robe", blue)
        skirt_panels(k, "SM_robe_skirt", blue, 0.14, flare=0.035, side_split=0.4)
        lapels(k, blue2)
        belt(k, blue2, tails=True)
        sleeves(k, blue, blue2, to_elbow=False, wide=0.02, cuff=blue2)
        gourd(k, m("gourd", (0.80, 0.48, 0.18), "wood"), m("cord", (0.75, 0.15, 0.12), "red"))
    elif npc_id == "smith":
        grey, dark = m("shirt", hexc("8C8C8C"), "stone"), m("trim", hexc("4A4A4A"), "stone")
        head(hexc("2B2B2B"), "short")
        headband(k, m("band", (0.70, 0.16, 0.12), "red"))
        build_body(k, skin, grey)
        build_legs(k, m("trousers", (0.24, 0.22, 0.22), "hair"), m("wrap", (0.48, 0.42, 0.34), "earth"),
                   m("boot", (0.20, 0.15, 0.11), "wood"), trouser_len=0.22, loose=0.074)
        upper_garment(k, "SM_shirt", grey)
        skirt_panels(k, "SM_shirt_skirt", grey, 0.42, flare=0.02)
        sleeves(k, grey, dark, to_elbow=True)
        belt(k, m("belt", (0.24, 0.16, 0.10), "wood"), tails=False)
        apron(k, m("apron", (0.50, 0.32, 0.18), "wood"), m("strap", (0.26, 0.17, 0.10), "wood"))
        hammer(k, m("handle", (0.45, 0.30, 0.16), "wood"), m("iron", (0.40, 0.42, 0.46), "steel", metal=0.9, rough=0.3))
    elif npc_id == "librarian":
        rose, red = m("robe", hexc("E89AB0"), "pink"), m("trim", hexc("BC4749"), "red")
        head((0.10, 0.08, 0.10), "long", tie_rgb=hexc("BC4749"), tie_ramp="red",
             ornament=m("pin", (0.95, 0.78, 0.32), "gold", metal=0.9, rough=0.35))
        build_body(k, skin, rose)
        build_legs(k, m("trousers", hexc("BC4749"), "red"), m("shoe", (0.42, 0.14, 0.16), "red"),
                   m("shoe", (0.42, 0.14, 0.16), "red"), trouser_len=0.3, loose=0.058)
        upper_garment(k, "SM_robe", rose)
        skirt_panels(k, "SM_robe_skirt", rose, 0.07, flare=0.05, side_split=0.25)
        lapels(k, red)
        belt(k, red, tails=True)
        sleeves(k, rose, red, to_elbow=False, wide=0.016, cuff=red)
        scroll_in_hand(k, m("paper", (0.94, 0.90, 0.78), "paper"), m("rod", (0.40, 0.22, 0.14), "wood"))
    elif npc_id == "guide":
        green, green2 = m("robe", hexc("B5D67A"), "leaf"), m("trim", hexc("6E9440"), "leaf")
        head(hexc("A0522D"), "twin", ramp="wood", tie_rgb=(0.96, 0.84, 0.40), tie_ramp="gold")
        build_body(k, skin, green)
        build_legs(k, m("trousers", hexc("8DB360"), "leaf"), m("shoe", (0.36, 0.26, 0.16), "wood"),
                   m("shoe", (0.36, 0.26, 0.16), "wood"), trouser_len=0.28, loose=0.058)
        upper_garment(k, "SM_robe", green)
        skirt_panels(k, "SM_robe_skirt", green, 0.16, flare=0.05, side_split=0.3)
        lapels(k, m("collar", (0.98, 0.95, 0.86), "bone"))
        belt(k, m("sash", (0.96, 0.62, 0.32), "wood"), tails=True)
        sleeves(k, green, green2, to_elbow=False, wide=0.012, cuff=green2)
    elif npc_id == "fisher":
        brown, brown2 = m("robe", hexc("B89B5E"), "earth"), m("trim", hexc("7E6A3E"), "earth")
        head(hexc("D8D2C4"), "none", ramp="bone")
        beard(k, white, long=False)
        straw_hat(k, m("straw", (0.86, 0.72, 0.42), "wood"))
        build_body(k, skin, brown)
        build_legs(k, m("trousers", (0.36, 0.34, 0.30), "stone"), skin, m("sandal", (0.40, 0.30, 0.18), "wood"),
                   trouser_len=0.26, loose=0.07)
        upper_garment(k, "SM_robe", brown)
        skirt_panels(k, "SM_robe_skirt", brown, 0.38, flare=0.025)
        lapels(k, brown2)
        belt(k, m("rope", (0.70, 0.60, 0.40), "earth"), tails=True)
        sleeves(k, brown, brown2, to_elbow=True)
    elif npc_id == "truc_lao":
        bamboo, bamboo2 = m("robe", (0.48, 0.66, 0.36), "leaf"), m("trim", (0.24, 0.40, 0.20), "leaf")
        build_head(k, skin, skin_rgb=skin_rgb)
        hair_style(k, white, white_hi, m("tie", (0.30, 0.46, 0.24), "leaf"), "bun")
        beard(k, white, long=True, brows=True)
        build_body(k, skin, bamboo)
        build_legs(k, m("trousers", (0.86, 0.84, 0.76), "bone"), m("shoe", (0.24, 0.30, 0.18), "leaf"),
                   m("shoe", (0.24, 0.30, 0.18), "leaf"), trouser_len=0.3, loose=0.062)
        upper_garment(k, "SM_robe", bamboo)
        skirt_panels(k, "SM_robe_skirt", bamboo, 0.10, flare=0.045, side_split=0.3)
        lapels(k, m("collar", (0.90, 0.88, 0.80), "bone"))
        belt(k, bamboo2, tails=True)
        sleeves(k, bamboo, bamboo2, to_elbow=False, wide=0.024, cuff=bamboo2)
        staff(k, m("bamboo", (0.70, 0.74, 0.36), "leaf"), m("node", (0.46, 0.52, 0.22), "leaf"))
    else:   # villager: a plain young passer-by in undyed cloth
        cloth, cloth2 = m("tunic", (0.86, 0.82, 0.72), "bone"), m("trim", (0.56, 0.48, 0.36), "earth")
        head((0.12, 0.10, 0.11), "short")
        build_body(k, skin, cloth)
        build_legs(k, m("trousers", (0.52, 0.46, 0.38), "earth"), m("wrap", (0.70, 0.64, 0.52), "earth"),
                   m("shoe", (0.30, 0.22, 0.15), "wood"), trouser_len=0.2, loose=0.066)
        upper_garment(k, "SM_tunic", cloth)
        skirt_panels(k, "SM_tunic_skirt", cloth, 0.40, flare=0.02)
        lapels(k, cloth2)
        belt(k, cloth2, tails=False)
        sleeves(k, cloth, cloth2, to_elbow=True)
    return k.objs
