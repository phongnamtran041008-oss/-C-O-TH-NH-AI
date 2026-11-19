"""The eight realm looks on the v2 body (runs inside Blender).

Every look is a set of separate fitted pieces with its own materials (crafted gear, not a
realm reward: the game decides which set is worn). Built from the approved look-dev pieces
(../lookdev/ld_body.py, ld_looks.py) plus armour, ribbons, ponytail, crown and wings.
"""
from __future__ import annotations

import math

from mathutils import Vector

import geo
import ld_looks as LL
import rig as R
from ld_body import V, Kit, build_body, build_hair, build_head, build_legs, cuboid, limb, mat
from ld_looks import (WAIST, belt, coat_cape, forearm_wraps, halo, lapels, skirt_panels, sleeves,
                      upper_garment, wide_sleeves)

LOOKS = {
    "dao_si_luyen_khi": "Đạo Sĩ Luyện Khí",
    "dao_si_truc_co": "Đạo Sĩ Trúc Cơ",
    "dao_si_ket_dan": "Đạo Sĩ Kết Đan",
    "dao_si_nguyen_anh": "Đạo Sĩ Nguyên Anh",
    "dao_si_hoa_than": "Đạo Sĩ Hóa Thần",
    "dao_si_luyen_hu": "Đạo Sĩ Luyện Hư",
    "dao_si_hop_the": "Đạo Sĩ Hợp Thể",
    "dao_si_dai_thua": "Đạo Sĩ Đại Thừa",
}
WINGS = {"dao_si_luyen_hu": "flame", "dao_si_hop_the": "ice", "dao_si_dai_thua": "cosmic"}

SKIN = (0.94, 0.72, 0.56)


def glow(name, rgb, ramp, strength=5.0, halo_px=1, priority=None):
    return geo.material(name, rgb, emit=rgb, emit_strength=strength, glow=ramp, halo=halo_px, priority=priority)


# ---------------------------------------------------------------- armour and accessories
def pauldrons(k: Kit, m, trim=None, size=1.0):
    for s, side in ((1, "L"), (-1, "R")):
        sh = V(*R.BONES[f"upper_arm.{side}"][0])
        w = R.w_near(["chest", f"upper_arm.{side}"], power=2)
        k.add(f"SM_pauldron.{side}", cuboid(sh + V(s * 0.012, 0, 0.012), (0.056 * size, 0.058 * size, 0.03 * size),
                                            top_scale=(0.55, 0.6)), m, w)
        k.add(f"SM_pauldron2.{side}", cuboid(sh + V(s * 0.03, 0, -0.03), (0.05 * size, 0.054 * size, 0.022 * size),
                                             top_scale=(0.8, 0.85)), trim or m, R.w_rigid(f"upper_arm.{side}"))


def chest_plate(k: Kit, m, gem=None):
    prof = [(z, rx + 0.022, ry + 0.022) for z, rx, ry in LL.TORSO[1:5]]
    k.add("SM_chest_plate", geo.lathe(prof, 8, phase=math.pi / 8, gap=3.4, gap_at=math.pi / 2, cap_bottom=False,
                                      cap_top=False), m, R.w_near(["spine", "chest"], power=3), solid=0.012)
    if gem is not None:
        k.add("SM_chest_gem", cuboid((0, LL.torso_front(0, 0.645, 0.034), 0.645), (0.016, 0.008, 0.016)), gem,
              R.w_rigid("chest"))


def tassets(k: Kit, m, edge=None):
    wf = R.w_skirt(WAIST, 0.40, top_fn=R.w_near(["hips"]))
    for ang in (-62, -22, 22, 62, 118, 158, 202, 242):
        a = math.radians(ang - 90)
        d = V(math.cos(a), math.sin(a), 0)
        c = V(0, 0, WAIST - 0.065) + d * 0.122
        rot = R.rz(math.degrees(a) + 90).to_matrix()
        k.add("SM_tasset", cuboid(c, (0.036, 0.008, 0.06), top_scale=(0.85, 1.0), rot=rot), m, wf)
        if edge is not None:
            k.add("SM_tasset_edge", cuboid(c + V(0, 0, -0.058) + d * 0.004, (0.034, 0.008, 0.006), rot=rot), edge, wf)


def bracers(k: Kit, m):
    for side in "LR":
        el = V(*R.BONES[f"forearm.{side}"][0])
        wr = V(*R.BONES[f"hand.{side}"][0])
        k.add(f"SM_bracer.{side}", limb([el.lerp(wr, 0.3), wr + (wr - el).normalized() * 0.005], [0.036, 0.034], 6), m,
              R.w_rigid(f"forearm.{side}"))


def belt_plate(k: Kit, m):
    k.add("SM_belt_plate", cuboid((0, -0.104, WAIST), (0.03, 0.008, 0.024)), m, R.w_rigid("hips"))


def crown(k: Kit, m, gem=None):
    head = R.w_rigid("head")
    k.add("SM_crown", geo.lathe([(1.012, 0.046, 0.044, 0.024), (1.05, 0.05, 0.048, 0.024)], 8, phase=math.pi / 8,
                                cap_bottom=False, cap_top=False), m, head, solid=0.01)
    k.add("SM_crown_front", cuboid((0, -0.024, 1.07), (0.022, 0.006, 0.03), top_scale=(0.4, 1.0)), m, head)
    if gem is not None:
        k.add("SM_crown_gem", cuboid((0, -0.032, 1.055), (0.009, 0.006, 0.009)), gem, head)


def ribbons(k: Kit, m):
    for s, side in ((1, "L"), (-1, "R")):
        h1 = V(*R.BONES[f"ribbon_01.{side}"][0])
        t1 = V(*R.BONES[f"ribbon_01.{side}"][1])
        t2 = V(*R.BONES[f"ribbon_02.{side}"][1])
        end = t2 + (t2 - t1).normalized() * 0.12
        pts = [h1, t1, t1.lerp(t2, 0.5), t2, end]
        k.add(f"SM_ribbon.{side}", geo.sweep(pts, [(0.016, 0.004), (0.022, 0.004), (0.024, 0.004), (0.024, 0.004),
                                                   (0.0, 0.003)], 4, up=(s, 0, 0.3)),
              m, R.w_near([f"ribbon_01.{side}", f"ribbon_02.{side}"], power=3))
        k.add(f"SM_ribbon_bow.{side}", cuboid(h1 + V(s * 0.012, 0, 0), (0.016, 0.01, 0.012)), m, R.w_rigid("head"))


def ponytail(k: Kit, hair, hi):
    b = [V(*R.BONES[n][1]) for n in ("hair_01", "hair_02")]
    pts = [V(0, 0.045, 1.05), V(0, 0.085, 1.0), b[0] + V(0, 0.0, 0.03), b[1] + V(0, 0, 0.04), b[1] + V(0, 0.005, -0.06)]
    wf = R.w_near(["hair_01", "hair_02", "hair_03"], power=3)
    k.add("SM_ponytail", geo.sweep(pts, [(0.03, 0.026), (0.036, 0.03), (0.034, 0.026), (0.026, 0.02), (0.0, 0.01)], 6,
                                   up=(1, 0, 0)), hair, wf)
    pts2 = [p + V(0.012, -0.004, 0.0) for p in pts[1:]]
    k.add("SM_ponytail_hi", geo.sweep(pts2, [(0.012, 0.01), (0.012, 0.01), (0.01, 0.008), (0.0, 0.006)], 4, up=(1, 0, 0)),
          hi, wf)


def edge_lights(k: Kit, m):
    """Hop The: thin cyan light along the armour's edges (pauldron rims, chest plate hem)."""
    for s, side in ((1, "L"), (-1, "R")):
        sh = V(*R.BONES[f"upper_arm.{side}"][0])
        c = sh + V(s * 0.03, 0, -0.052)
        pts = [c + V(math.cos(a) * 0.052, math.sin(a) * 0.056, 0) for a in (math.tau * i / 10 for i in range(11))]
        k.add(f"SM_edge_light.{side}", geo.sweep(pts, 0.006, 4, tip=False, cap=False), m, R.w_rigid(f"upper_arm.{side}"))
    pts = []
    for i in range(9):
        a = -math.pi / 2 + (i - 4) * 0.33
        pts.append(V(math.cos(a) * 0.125, math.sin(a) * 0.10 - 0.002, 0.567))
    k.add("SM_edge_light_chest", geo.sweep(pts, 0.006, 4, tip=False, cap=False), m, R.w_near(["spine", "chest"]))
    pts = [V(x, LL.torso_front(x * 0.5, 0.66, 0.036), 0.70 - abs(x) * 1.2) for x in (-0.07, -0.03, 0.0, 0.03, 0.07)]
    k.add("SM_edge_light_v", geo.sweep(pts, 0.005, 4, tip=False, cap=False), m, R.w_rigid("chest"))


def star(p, size, facing=(0, -1, 0)):
    p = Vector(p)
    parts = []
    for ax in ((1, 0, 0), (0, 0, 1)):
        a = Vector(ax)
        parts.append(geo.leaf(p - a * size / 2, a, size, size * 0.24, side=Vector(facing).cross(a), thick=0.006,
                              shape="shard", segs=2))
    return geo.merge(*parts)


# ---------------------------------------------------------------- wings
BACK_ANGLE = math.radians(35)


def wing_mats(look_m, kind, glow_fn, p):
    """Per kind: root (darkest), A / B (alternating feather bodies), covert (one tone
    lighter), light (bright inner tips), tip (glowing outer tips), arm (leading edge)."""
    if kind == "flame":
        return dict(root=look_m("wf_root", (0.52, 0.07, 0.04), "red"),
                    A=look_m("wf_a", (0.86, 0.22, 0.07), "red"), B=look_m("wf_b", (0.94, 0.36, 0.10), "red"),
                    covert=look_m("wf_cov", (0.98, 0.56, 0.16), "gold"),
                    light=look_m("wf_light", (1.0, 0.74, 0.30), "gold"),
                    tip=glow_fn(p + "wf_tip", (1.0, 0.86, 0.45), "flame", 5.0, 0, 2.0),
                    arm=glow_fn(p + "wf_arm", (1.0, 0.55, 0.15), "flame", 3.0, 0, 1.5),
                    fleck=glow_fn(p + "wf_fleck", (1.0, 0.70, 0.25), "flame", 6.0, 0, 3.0))
    if kind == "ice":
        mk = dict(metal=0.85, rough=0.3)
        return dict(root=look_m("wi_root", (0.10, 0.20, 0.52), "blue", **mk),
                    A=look_m("wi_a", (0.24, 0.48, 0.84), "blue", **mk), B=look_m("wi_b", (0.36, 0.62, 0.92), "blue", **mk),
                    covert=look_m("wi_cov", (0.56, 0.84, 0.98), "teal", **mk),
                    light=look_m("wi_light", (0.80, 0.95, 1.0), "bone", **mk),
                    tip=glow_fn(p + "wi_tip", (0.90, 0.98, 1.0), "ice", 5.0, 0, 2.0),
                    arm=glow_fn(p + "wi_arm", (0.55, 0.92, 1.0), "ice", 3.0, 0, 1.5), fleck=None)
    gold = look_m("wc_gold", (0.98, 0.80, 0.34), "gold", metal=0.9, rough=0.35)
    return dict(root=look_m("wc_root", (0.26, 0.08, 0.46), "purple"),
                A=look_m("wc_a", (0.46, 0.20, 0.78), "purple"), B=look_m("wc_b", (0.56, 0.30, 0.86), "purple"),
                covert=look_m("wc_cov", (0.72, 0.52, 0.96), "purple"),
                light=look_m("wc_light", (0.86, 0.72, 1.0), "purple"),
                tip=glow_fn(p + "wc_tip", (1.0, 0.94, 0.70), "holy", 5.0, 0, 2.0),
                arm=gold, fleck=None)


def wing_extent():
    tip = V(*R.BONES["wing_03.L"][1])
    return tip.x + 0.30 * math.cos(math.radians(18)) * math.cos(BACK_ANGLE), tip.z


def wings(k: Kit, kind, wm, star_m=None):
    """A real wing: a three-bone arm (upper arm up-out, forearm out, hand out-down) with
    feathers hanging from it and overlapping like shingles (each covers ~40 % of the next),
    so the wing reads as one surface with a scalloped trailing edge: 7 broad primaries fanned
    on the hand (straight down at the wrist to outward-down at the tip), 6 secondaries down
    from the forearm, 3 tertials from the upper arm, two rows of small rounded coverts over
    the arm. Separation comes from tone: neighbouring feathers alternate A/B materials,
    coverts are a tone lighter, primaries dark at the root and bright at the tip; only the
    outer primaries' tips and the leading edge glow. The wing plane is turned 35 degrees back
    so the near wing reads in three-quarter from the side."""
    shape = {"flame": "flame", "ice": "shard", "cosmic": "plume"}[kind]
    thick = {"flame": 0.012, "ice": 0.02, "cosmic": 0.011}[kind]
    mats = [wm["root"], wm["A"], wm["B"], wm["covert"], wm["light"], wm["tip"]]
    for side in ("L", "R"):
        s = 1 if side == "L" else -1
        b1, b2, b3 = (V(*R.BONES[f"wing_0{i}.{side}"][0]) for i in (1, 2, 3))
        tip = V(*R.BONES[f"wing_03.{side}"][1])
        out = V(s * math.cos(BACK_ANGLE), math.sin(BACK_ANGLE), 0)
        up = V(0, 0, 1)
        nf = out.cross(up).normalized()
        if nf.y > 0:
            nf = -nf                                   # the wing face toward the front
        layer = [0]

        def dir_at(ang):
            a = math.radians(ang)
            return (out * math.cos(a) + up * math.sin(a)).normalized()

        def feather(base, ang, ln, wd, bone, role, idx, depth, shp=None, bend=0.0, curl=0.0):
            d = dir_at(ang)
            sv = nf.cross(d).normalized()
            layer[0] += 1
            base = base + nf * depth - nf * 0.0018 * layer[0]        # shingles: each one a hair behind
            sh = shp or shape
            v, f = geo.leaf(base, d, ln, wd, side=sv, thick=thick, shape=sh, bend=bend * s, tip_curl=curl * s,
                            segs=6 if sh != "shard" else 4)
            fm = []
            body = 1 if idx % 2 == 0 else 2
            for face in f:
                cen = sum((Vector(v[q]) for q in face), Vector()) / len(face)
                t = (cen - base).dot(d) / ln
                if role == "covert":
                    fm.append(3)
                elif role == "primary":
                    fm.append(0 if t < 0.3 else (body if t < 0.78 else (5 if idx >= 3 else 4)))
                else:
                    fm.append(0 if t < 0.25 else (body if t < 0.85 else 4))
            ob = geo.mesh_object(f"SM_wing_{role}.{side}", v, f, mats, k.col, subsurf=0, flat=True, face_mats=fm)
            R.bind(ob, k.rig, R.w_rigid(bone))
            k.objs.append(ob)
            return base + d * ln

        bend, curl = (0.012, -0.03) if kind == "flame" else (0.0, 0.0)
        # primaries on the hand: outermost first, so the inner ones overlap them
        tips = []
        for i in range(6, -1, -1):
            u = i / 6
            ang = -90 + 60 * u
            ln = [0.44, 0.46, 0.46, 0.45, 0.42, 0.38, 0.33][i]
            tips.append(feather(b3.lerp(tip, u), ang, ln, 0.085, f"wing_03.{side}", "primary", i, -0.004,
                                bend=bend, curl=curl))
        # secondaries down from the forearm, tertials from the upper arm
        for i in range(5, -1, -1):
            u = 0.06 + 0.9 * i / 5
            feather(b2.lerp(b3, u), -94 + 4 * u, 0.26 + 0.12 * u, 0.078, f"wing_02.{side}", "secondary", i, 0.0,
                    bend=bend, curl=curl)
        for i in range(2, -1, -1):
            u = 0.4 + 0.28 * i
            feather(b1.lerp(b2, u), -98, 0.16 + 0.08 * u, 0.07, f"wing_01.{side}", "secondary", i + 1, 0.002,
                    bend=bend, curl=curl)
        # two rows of rounded coverts over the arm
        for i in range(6, -1, -1):
            u = i / 6
            pos = b2.lerp(b3, u * 2) if u < 0.5 else b3.lerp(tip, (u - 0.5) * 2 * 0.8)
            feather(pos + V(0, 0, -0.014), -80 + 26 * u, 0.13, 0.066, f"wing_02.{side}" if u < 0.5 else f"wing_03.{side}",
                    "covert", i, 0.008, shp="covert")
        for i in range(6, -1, -1):
            u = i / 6
            pos = b1.lerp(b2, u * 2) if u < 0.5 else b2.lerp(b3, (u - 0.5) * 2)
            feather(pos, -72, 0.085, 0.056, f"wing_01.{side}" if u < 0.5 else f"wing_02.{side}", "covert", i, 0.014,
                    shp="covert")
        # the leading edge of the arm (glows, or gold on the cosmic wing)
        pts = [b1 + nf * 0.016, b2 + nf * 0.016, b3 + nf * 0.016, tip + nf * 0.016]
        k.add(f"SM_wing_arm.{side}", geo.sweep(pts, [(0.016, 0.012), (0.018, 0.013), (0.015, 0.012), (0.0, 0.01)], 5,
                                              up=nf), wm["arm"],
              R.w_near([f"wing_01.{side}", f"wing_02.{side}", f"wing_03.{side}"], power=4))
        # embers above the outer flame tips; stars on the cosmic secondaries
        if wm.get("fleck") is not None:
            for j, tp in enumerate(tips[:3]):
                fp = tp + up * (0.05 + 0.02 * j) + out * 0.02
                k.add(f"SM_wing_fleck.{side}", star(fp, 0.026, facing=tuple(nf)), wm["fleck"], R.w_rigid(f"wing_03.{side}"))
        if star_m is not None:
            for u, dz in ((0.25, -0.12), (0.6, -0.16), (0.9, -0.1)):
                sp = b2.lerp(b3, u) + up * dz + nf * 0.02
                k.add(f"SM_wing_star.{side}", star(sp, 0.035, facing=tuple(nf)), star_m, R.w_rigid(f"wing_02.{side}"))


# ---------------------------------------------------------------- the eight looks
def build(rig, col, look_id):
    k = Kit(rig, col)
    skin = mat("MAT_skin", SKIN, "skin")
    p = f"MAT_{look_id[7:]}_"

    # colours below are written as sRGB (what you see) and turned into the linear values a
    # Principled material takes; the two look-dev looks keep their approved linear values
    srgb = look_id not in ("dao_si_luyen_khi", "dao_si_hoa_than")

    def m(name, rgb, ramp, **kw):
        if srgb:
            rgb = tuple(c ** 2.2 for c in rgb)
        return mat(p + name, rgb, ramp, **kw)

    gold = m("gold", (0.98, 0.78, 0.30), "gold", metal=0.9, rough=0.35)
    black_hair = m("hair", (0.13, 0.11, 0.12), "hair")
    black_hi = m("hair_hi", (0.25, 0.21, 0.27), "hair")

    if look_id == "dao_si_luyen_khi":
        hemp = m("tunic", (0.52, 0.49, 0.42), "earth")
        trim = m("trim", (0.30, 0.26, 0.21), "earth")
        build_head(k, skin)
        build_hair(k, black_hair, m("tie", (0.62, 0.44, 0.26), "wood"), hair_hi=black_hi)
        build_body(k, skin, hemp)
        build_legs(k, m("trousers", (0.22, 0.19, 0.24), "hair"), m("wrap", (0.56, 0.50, 0.40), "earth"),
                   m("shoe", (0.22, 0.16, 0.12), "wood"), trouser_len=0.20, loose=0.068)
        upper_garment(k, "SM_tunic", hemp)
        skirt_panels(k, "SM_tunic_skirt", hemp, 0.40, flare=0.02)
        lapels(k, trim)
        belt(k, m("belt", (0.26, 0.18, 0.13), "wood"))
        sleeves(k, hemp, trim, to_elbow=True)
        forearm_wraps(k, m("wrap", (0.56, 0.50, 0.40), "earth"))

    elif look_id == "dao_si_truc_co":
        blue = m("jacket", (0.20, 0.34, 0.64), "blue")
        white = m("inner", (0.90, 0.91, 0.94), "bone")
        build_head(k, skin)
        build_hair(k, black_hair, m("tie", (0.22, 0.36, 0.66), "blue"), hair_hi=black_hi)
        build_body(k, skin, white)
        build_legs(k, white, m("boot", (0.18, 0.18, 0.24), "stone"), m("boot", (0.18, 0.18, 0.24), "stone"),
                   trouser_len=0.18, loose=0.064)
        upper_garment(k, "SM_inner", white)
        skirt_panels(k, "SM_inner_skirt", white, 0.30, flare=0.02, side_split=0.5)
        upper_garment(k, "SM_jacket", blue, grow=0.02, gap=0.5)
        skirt_panels(k, "SM_jacket_skirt", blue, 0.40, flare=0.03, grow=0.014, front_gap=0.55, side_split=0.4)
        lapels(k, white, width=0.016, out=0.03)
        belt(k, m("sash", (0.12, 0.15, 0.28), "blue"), tails=True)
        sleeves(k, blue, white, to_elbow=False, wide=0.006, cuff=white)

    elif look_id == "dao_si_ket_dan":
        green = m("robe", (0.13, 0.40, 0.24), "jade")
        dark = m("trim", (0.10, 0.30, 0.20), "jade")
        build_head(k, skin)
        build_hair(k, black_hair, m("tie", (0.12, 0.44, 0.40), "teal"), hair_hi=black_hi)
        build_body(k, skin, green)
        build_legs(k, m("trousers", (0.12, 0.24, 0.18), "jade"), m("boot", (0.12, 0.16, 0.14), "hair"),
                   m("boot", (0.12, 0.16, 0.14), "hair"), trouser_len=0.24, loose=0.062)
        upper_garment(k, "SM_robe", green)
        skirt_panels(k, "SM_robe_skirt", green, 0.17, flare=0.03, side_split=0.45)
        lapels(k, dark, width=0.018)
        belt(k, dark, tails=True)
        sleeves(k, green, dark, to_elbow=False, wide=0.012, cuff=dark)
        ribbons(k, m("ribbon", (0.10, 0.48, 0.44), "teal"))

    elif look_id == "dao_si_nguyen_anh":
        teal = m("robe", (0.08, 0.32, 0.38), "teal")
        dark = m("under", (0.08, 0.16, 0.24), "blue")
        build_head(k, skin)
        build_hair(k, black_hair, gold, hair_hi=black_hi)
        build_body(k, skin, teal)
        build_legs(k, m("trousers", (0.12, 0.17, 0.24), "steel"), m("boot", (0.14, 0.16, 0.22), "steel"),
                   m("boot", (0.14, 0.16, 0.22), "steel"), trouser_len=0.24, loose=0.062)
        upper_garment(k, "SM_robe", teal)
        skirt_panels(k, "SM_robe_skirt", teal, 0.17, flare=0.03, side_split=0.45)
        lapels(k, gold, width=0.016)
        belt(k, dark, knot_m=gold, tails=False)
        belt_plate(k, gold)
        sleeves(k, teal, gold, to_elbow=False, wide=0.01, cuff=gold)
        pauldrons(k, gold, trim=m("guard2", (0.85, 0.62, 0.22), "gold", metal=0.9, rough=0.35))
        crown(k, gold, gem=glow(p + "gem", (0.35, 0.95, 0.85), "spirit", 3.0, 0, 3.0))

    elif look_id == "dao_si_hoa_than":
        teal = m("robe", (0.18, 0.60, 0.58), "teal")
        purple = m("coat", (0.48, 0.30, 0.70), "purple")
        lining = m("lining", (0.20, 0.55, 0.55), "teal")
        hair = m("hair_violet", (0.44, 0.30, 0.68), "purple")
        hair_hi = m("hair_violet_hi", (0.66, 0.50, 0.88), "purple")
        tie = m("tie", (0.22, 0.75, 0.70), "teal")
        build_head(k, skin)
        build_hair(k, hair, tie, hair_hi=hair_hi, long=True, ornament=tie)
        build_body(k, skin, teal)
        boot = m("boot", (0.30, 0.22, 0.42), "purple")
        build_legs(k, m("trousers", (0.74, 0.76, 0.82), "bone"), boot, boot, trouser_len=0.27, loose=0.06)
        upper_garment(k, "SM_robe", teal)
        skirt_panels(k, "SM_robe_skirt", teal, 0.16, flare=0.025, side_split=0.45)
        lapels(k, gold, width=0.013)
        belt(k, lining, knot_m=gold, tails=True)
        coat_cape(k, purple, lining, gold, hem_z=0.30, opening=1.25, split=True)
        k.add("SM_collar", geo.lathe([(0.71, 0.075, 0.062, 0.006), (0.745, 0.068, 0.058, 0.006)], 8, phase=math.pi / 8,
                                     gap=1.2, cap_bottom=False, cap_top=False), lining, R.w_rigid("chest"), solid=0.01)
        wide_sleeves(k, purple, lining, gold)
        k.add("SM_mantle", geo.lathe([(0.615, 0.185, 0.115, 0.004), (0.665, 0.165, 0.10, 0.004),
                                      (0.715, 0.12, 0.082, 0.004), (0.745, 0.075, 0.062, 0.004)], 8, phase=math.pi / 8,
                                     gap=0.7, cap_bottom=False, cap_top=False), lining,
              R.w_near(["chest", "upper_arm.L", "upper_arm.R"], power=4), solid=0.012)
        halo(k, geo.material(p + "halo", (1.0, 0.84, 0.36), emit=(1.0, 0.84, 0.36), emit_strength=6.0,
                             glow="holy", halo=0, priority=2.5))

    elif look_id == "dao_si_luyen_hu":
        red = m("robe", (0.70, 0.15, 0.10), "red", light=0.7)
        dark = m("cape", (0.56, 0.12, 0.08), "red", light=0.6)
        lining = m("lining", (0.80, 0.42, 0.12), "gold")
        build_head(k, skin)
        build_hair(k, black_hair, gold, hair_hi=black_hi)
        ponytail(k, black_hair, black_hi)
        build_body(k, skin, red)
        boot = m("boot", (0.30, 0.10, 0.08), "red")
        build_legs(k, m("trousers", (0.36, 0.10, 0.09), "red"), boot, boot, trouser_len=0.24, loose=0.062)
        upper_garment(k, "SM_robe", red)
        skirt_panels(k, "SM_robe_skirt", red, 0.17, flare=0.03, side_split=0.45)
        coat_cape(k, dark, lining, gold, hem_z=0.14, opening=1.35)
        chest_plate(k, gold, gem=glow(p + "gem", (1.0, 0.40, 0.10), "flame", 3.0, 0, 3.0))
        pauldrons(k, gold, trim=m("guard2", (0.90, 0.55, 0.16), "gold", metal=0.9, rough=0.35), size=1.1)
        tassets(k, gold)
        bracers(k, gold)
        belt(k, m("belt", (0.36, 0.12, 0.08), "red"), knot_m=gold, tails=False)
        sleeves(k, red, gold, to_elbow=False, wide=0.004, cuff=gold)
        crown(k, gold)
        wings(k, "flame", wing_mats(m, "flame", glow, p))

    elif look_id == "dao_si_hop_the":
        steel = m("armour", (0.30, 0.42, 0.64), "blue", metal=0.6, rough=0.4, light=0.5, shadow=0.35)
        robe = m("robe", (0.18, 0.22, 0.34), "steel", light=0.6)
        cyan = glow(p + "edge", (0.50, 0.95, 1.0), "ice", 3.0, 0, 2.0)
        build_head(k, skin)
        build_hair(k, black_hair, cyan, hair_hi=black_hi)
        ponytail(k, black_hair, black_hi)
        build_body(k, skin, robe)
        boot = m("boot", (0.16, 0.22, 0.38), "blue")
        build_legs(k, m("trousers", (0.12, 0.15, 0.24), "steel"), boot, boot, trouser_len=0.24, loose=0.062)
        upper_garment(k, "SM_robe", robe)
        skirt_panels(k, "SM_robe_skirt", robe, 0.17, flare=0.03, side_split=0.45)
        coat_cape(k, m("cape", (0.10, 0.13, 0.24), "steel"), m("lining", (0.22, 0.40, 0.66), "blue"), cyan,
                  hem_z=0.14, opening=1.35)
        chest_plate(k, steel, gem=cyan)
        pauldrons(k, steel, size=1.1)
        tassets(k, steel, edge=cyan)
        bracers(k, steel)
        belt(k, m("belt", (0.10, 0.12, 0.20), "steel"), knot_m=cyan, tails=False)
        sleeves(k, robe, steel, to_elbow=False, wide=0.004, cuff=steel)
        edge_lights(k, cyan)
        crown(k, steel, gem=cyan)
        wings(k, "ice", wing_mats(m, "ice", glow, p))

    elif look_id == "dao_si_dai_thua":
        purple = m("robe", (0.32, 0.10, 0.56), "purple")
        cape = m("cape", (0.22, 0.08, 0.40), "purple")
        lining = m("lining", (0.96, 0.78, 0.34), "gold")
        stars = glow(p + "star", (1.0, 0.95, 0.78), "holy", 6.0, 0, 3.0)
        build_head(k, skin)
        build_hair(k, black_hair, gold, hair_hi=black_hi)
        ponytail(k, black_hair, black_hi)
        build_body(k, skin, purple)
        boot = m("boot", (0.28, 0.12, 0.44), "purple")
        build_legs(k, m("trousers", (0.24, 0.10, 0.38), "purple"), boot, boot, trouser_len=0.24, loose=0.062)
        upper_garment(k, "SM_robe", purple)
        skirt_panels(k, "SM_robe_skirt", purple, 0.16, flare=0.03, side_split=0.45)
        coat_cape(k, cape, lining, gold, hem_z=0.12, opening=1.25)
        chest_plate(k, gold, gem=glow(p + "gem", (0.80, 0.50, 1.0), "cosmic", 3.0, 0, 3.0))
        pauldrons(k, gold, trim=m("guard2", (0.88, 0.62, 0.22), "gold", metal=0.9, rough=0.35), size=1.15)
        tassets(k, gold)
        bracers(k, gold)
        belt(k, gold, knot_m=gold, tails=False)
        sleeves(k, purple, gold, to_elbow=False, wide=0.008, cuff=gold)
        crown(k, gold, gem=glow(p + "crown_gem", (0.85, 0.55, 1.0), "cosmic", 3.0, 0, 3.0))
        wf = R.w_skirt(WAIST, 0.12, top_fn=R.w_near(["spine", "chest"], power=3))
        for x, z in ((-0.12, 0.30), (0.05, 0.22), (0.15, 0.38), (-0.04, 0.44), (0.10, 0.52)):
            k.add("SM_star", star((x, 0.17 + 0.25 * (WAIST - z) * (z < WAIST), z), 0.04, facing=(0, 1, 0)), stars, wf)
        wings(k, "cosmic", wing_mats(m, "cosmic", glow, p), star_m=stars)
    return k.objs


def build_base(rig, col):
    """rig_base: the bare v2 body (neutral under-clothes, topknot), no outfit."""
    k = Kit(rig, col)
    skin = mat("MAT_skin", SKIN, "skin")
    under = mat("MAT_base_under", (0.78, 0.76, 0.70), "bone")
    build_head(k, skin)
    build_hair(k, mat("MAT_base_hair", (0.13, 0.11, 0.12), "hair"), mat("MAT_base_tie", (0.4, 0.35, 0.3), "wood"))
    build_body(k, skin, under)
    build_legs(k, mat("MAT_base_trousers", (0.30, 0.28, 0.28), "stone"), under, mat("MAT_base_shoe", (0.25, 0.2, 0.18), "wood"))
    return k.objs
