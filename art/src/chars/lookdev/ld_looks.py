"""Look-dev v2 outfits: Luyện Khí (row 1) and Hóa Thần (row 5), as fitted separate layers
with their own materials, so the kit draws inner lines between them (runs inside Blender)."""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

import geo
import rig as R
from ld_body import V, Kit, build_body, build_hair, build_head, build_legs, cuboid, limb, mat

WAIST = 0.535
TORSO = [(0.52, 0.098, 0.074), (0.58, 0.096, 0.072), (0.635, 0.124, 0.080), (0.68, 0.146, 0.082),
         (0.708, 0.12, 0.070), (0.722, 0.06, 0.05)]


def grown(prof, g):
    return [(z, rx + g, ry + g) for z, rx, ry in prof]


def torso_front(x, z, out=0.0):
    """y of the clothed chest surface (front) at (x, z)."""
    for (z0, ax, ay), (z1, bx, by) in zip(TORSO, TORSO[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            rx, ry = ax + (bx - ax) * t, ay + (by - ay) * t
            return -ry * math.sqrt(max(0.0, 1 - (x / rx) ** 2)) - out
    return -0.07 - out


def upper_garment(k: Kit, name, m, grow=0.012, gap=0.0, lining=None):
    part = geo.lathe(grown(TORSO, grow), 8, phase=math.pi / 8, gap=gap, cap_bottom=False, cap_top=False)
    mats = m if lining is None else [m, lining]
    return k.add(name, part, mats, R.w_near(["hips", "spine", "chest"], power=3), solid=0.01)


def skirt_panels(k: Kit, name, m, hem_z, *, flare=0.03, grow=0.0, front_gap=0.0, side_split=0.5, lining=None,
                 top_z=WAIST + 0.015):
    """Front and back skirt panels from the waist to hem_z, split at both sides (the legs
    show in a stride), optionally open at the front (a coat)."""
    rx0, ry0 = 0.105 + grow, 0.078 + grow
    rx1, ry1 = rx0 + flare + 0.02, ry0 + flare
    prof = []
    for t in (0.0, 0.5, 1.0):
        z = hem_z + (top_z - hem_z) * t
        prof.append((z, rx1 + (rx0 - rx1) * t, ry1 + (ry0 - ry1) * t))
    mats = m if lining is None else [m, lining]
    wfn = R.w_skirt(top_z, hem_z, top_fn=R.w_near(["hips"]))
    half_side = side_split / 2
    # front panel: centred on -Y, spanning (pi - side_split) minus any front opening
    span = math.pi - side_split
    if front_gap > 0:
        for s in (1, -1):    # a coat: two front flaps
            w = (span - front_gap) / 2
            centre = -math.pi / 2 + s * (front_gap / 2 + w / 2)
            part = geo.lathe(prof, 4, gap=math.tau - w, gap_at=centre + math.pi, cap_bottom=False, cap_top=False)
            k.add(f"{name}_front", part, mats, wfn, solid=0.01)
    else:
        part = geo.lathe(prof, 6, gap=math.tau - span, gap_at=math.pi / 2, cap_bottom=False, cap_top=False)
        k.add(f"{name}_front", part, mats, wfn, solid=0.01)
    part = geo.lathe(prof, 6, gap=math.tau - span, gap_at=-math.pi / 2, cap_bottom=False, cap_top=False)
    k.add(f"{name}_back", part, mats, wfn, solid=0.01)


def lapels(k: Kit, m, width=0.016, z_bottom=0.55, out=0.016):
    """Crossed collar: a band from each side of the neck down to the opposite side of the
    waist, right over left, as dark trim lines."""
    for s, z_end in ((1, z_bottom), (-1, z_bottom + 0.05)):
        pts = []
        for t in (0.0, 0.5, 1.0):
            x = s * 0.04 + (-s * 0.06 - s * 0.04) * t
            z = 0.715 + (z_end - 0.715) * t
            pts.append(V(x, torso_front(x, z, out), z))
        k.add("SM_lapel", geo.sweep(pts, [(width, 0.004)] * 3, 4, up=(0, -1, 0), tip=False), m,
              R.w_near(["spine", "chest"], power=3))


def belt(k: Kit, m, knot_m=None, h=0.03, tails=True):
    z = WAIST
    k.add("SM_belt", geo.lathe([(z - h / 2, 0.113, 0.088), (z + h / 2, 0.111, 0.086)], 8, phase=math.pi / 8,
                               cap_bottom=False, cap_top=False), m, R.w_near(["hips", "spine"]), solid=0.012)
    km = knot_m or m
    kx = 0.035
    k.add("SM_belt_knot", cuboid((kx, -0.098, z), (0.016, 0.012, 0.016)), km, R.w_rigid("hips"))
    if tails:
        for dx, zl in ((0.0, 0.42), (0.02, 0.45)):
            pts = [V(kx + dx, -0.10, z - 0.01), V(kx + dx + 0.006, -0.108, (z + zl) / 2), V(kx + dx + 0.01, -0.11, zl)]
            k.add("SM_belt_tail", geo.sweep(pts, [(0.011, 0.003)] * 3, 4, up=(0, -1, 0), tip=False), km,
                  R.w_skirt(z, zl, top_fn=R.w_near(["hips"])))


def sleeves(k: Kit, m, trim, *, to_elbow=True, wide=0.0, cuff=None):
    for s, side in ((1, "L"), (-1, "R")):
        sh = V(*R.BONES[f"upper_arm.{side}"][0])
        el = V(*R.BONES[f"forearm.{side}"][0])
        wr = V(*R.BONES[f"hand.{side}"][0])
        if to_elbow:
            end = sh.lerp(el, 0.82)
            k.add(f"SM_sleeve.{side}", limb([sh + V(-s * 0.01, 0, 0.02), end], [0.05, 0.05 + wide], 6), m,
                  R.w_rigid(f"upper_arm.{side}"))
            k.add(f"SM_sleeve_trim.{side}", limb([end - (end - sh).normalized() * 0.012, end + (end - sh).normalized() * 0.004],
                                                 [0.053 + wide, 0.053 + wide], 6), trim, R.w_rigid(f"upper_arm.{side}"))
        else:
            k.add(f"SM_sleeve_up.{side}", limb([sh + V(-s * 0.01, 0, 0.02), el], [0.05, 0.052], 6), m,
                  R.w_rigid(f"upper_arm.{side}"))
            end = wr + (wr - el).normalized() * 0.005
            k.add(f"SM_sleeve_low.{side}", limb([el - (wr - el).normalized() * 0.012, end], [0.052, 0.055 + wide], 6), m,
                  R.w_rigid(f"forearm.{side}"))
            if cuff is not None:
                k.add(f"SM_cuff.{side}", limb([end - (end - el).normalized() * 0.018, end + (end - el).normalized() * 0.003],
                                              [0.058 + wide, 0.06 + wide], 6), cuff, R.w_rigid(f"forearm.{side}"))


def coat_cape(k: Kit, m, lining, trim, hem_z=0.12, opening=0.80, cols=14, split=False):
    """An open coat that sweeps back like a cape: a pleated sheet from the shoulders round the
    back to the hem, wide open at the front (the teal robe is the front mass), flaring out and
    back toward the hem. Alternate columns stand in and out, so its panels catch the light
    and the shadow in turn; the lining shows on the inside, gold runs down both edges."""
    a0, a1 = -math.pi / 2 + opening, 3 * math.pi / 2 - opening
    rows = []
    zs = [0.705, 0.66, 0.60, WAIST, 0.42, 0.30, 0.20, hem_z]
    for z in zs:
        t = max(0.0, (WAIST - z) / (WAIST - hem_z))
        top = max(0.0, (z - WAIST) / (0.705 - WAIST))
        rx = 0.132 + 0.03 * top + 0.11 * t
        ry = 0.098 + 0.10 * t
        row = []
        for j in range(cols + 1):
            a = a0 + (a1 - a0) * j / cols
            pleat = 1 + (0.06 + 0.20 * t) * (1 if j % 2 else -1)
            back = max(0.0, math.sin(a))
            row.append(V(math.cos(a) * rx * pleat, math.sin(a) * ry * pleat + 0.02 * t * back, z - 0.01 * t * back))
        rows.append(row)
    wf = R.w_skirt(WAIST, hem_z, top_fn=R.w_near(["spine", "chest"], power=3))
    if split:      # a slit up the back below the waist: two tails, the robe shows between
        mid = cols // 2
        top_rows = [r for r, z in enumerate(zs) if z >= WAIST]
        for half in (range(0, mid), range(mid + 1, cols + 1)):
            sub = [[rows[r][c] for c in half] for r in range(len(rows))]
            k.add("SM_coat", geo.sheet(sub), [m, lining], wf, solid=0.012)
        k.add("SM_coat_mid", geo.sheet([[rows[r][c] for c in (mid - 1, mid, mid + 1)] for r in top_rows]),
              [m, lining], wf, solid=0.012)
    else:
        k.add("SM_coat", geo.sheet(rows), [m, lining], wf, solid=0.012)
    for row_end in (0, cols):
        pts = [rows[r][row_end] + V(0, -0.004, 0) for r in range(len(rows))]
        k.add("SM_coat_trim", geo.sweep(pts, [(0.012, 0.005)] * len(pts), 4, tip=False), trim, wf)


def wide_sleeves(k: Kit, m, lining, cuff):
    """Wide open sleeves: the cloth flares from the elbow past the wrist, lining inside."""
    for s, side in ((1, "L"), (-1, "R")):
        sh = V(*R.BONES[f"upper_arm.{side}"][0])
        el = V(*R.BONES[f"forearm.{side}"][0])
        wr = V(*R.BONES[f"hand.{side}"][0])
        k.add(f"SM_sleeve_up.{side}", limb([sh + V(-s * 0.01, 0, 0.02), el], [0.052, 0.056], 6), m,
              R.w_rigid(f"upper_arm.{side}"))
        d = (wr - el).normalized()
        end = wr + d * 0.01
        v, f = geo.sweep([el - d * 0.015, el.lerp(end, 0.5), end], [0.056, 0.068, 0.085], 7, tip=False, cap=False)
        ob = k.add(f"SM_sleeve_low.{side}", (v, f), [m, lining], R.w_rigid(f"forearm.{side}"), solid=0.01)
        k.add(f"SM_cuff.{side}", geo.sweep([end - d * 0.012, end + d * 0.002], [0.088, 0.089], 7, tip=False, cap=False),
              cuff, R.w_rigid(f"forearm.{side}"), solid=0.008)


def forearm_wraps(k: Kit, m):
    for side in "LR":
        el = V(*R.BONES[f"forearm.{side}"][0])
        wr = V(*R.BONES[f"hand.{side}"][0])
        k.add(f"SM_wrap_arm.{side}", limb([el.lerp(wr, 0.45), wr + (wr - el).normalized() * 0.006], [0.031, 0.029], 6), m,
              R.w_rigid(f"forearm.{side}"))


def halo(k: Kit, m):
    c = V(0, 0.15, 0.80)
    r = 0.29
    n = 36
    pts = [c + V(math.cos(a) * r, 0, math.sin(a) * r) for a in (math.tau * i / n for i in range(n + 1))]
    k.add("SM_halo", geo.sweep(pts, 0.0105, 6, tip=False, cap=False), m, R.w_rigid("halo"))


def sword(col, socket):
    """A plain wooden practice sword for the look-dev (grip at origin, blade along +Z)."""
    wood = mat("MAT_sword_wood", (0.62, 0.42, 0.24), "wood")
    dark = mat("MAT_sword_grip", (0.30, 0.20, 0.13), "wood")
    guard = mat("MAT_sword_guard", (0.40, 0.27, 0.16), "wood")
    parts = [(cuboid((0, 0, 0.33), (0.021, 0.008, 0.235), top_scale=(0.7, 0.8)), wood),
             (cuboid((0, 0, 0.087), (0.045, 0.016, 0.011)), guard),
             (cuboid((0, 0, 0.02), (0.012, 0.012, 0.058)), dark),
             (cuboid((0, 0, -0.045), (0.017, 0.016, 0.012)), guard)]
    obs = []
    for (v, f), m in parts:
        ob = geo.mesh_object("SM_wooden_sword", v, f, m, col, subsurf=0, flat=True)
        ob.parent = socket
        ob.matrix_parent_inverse.identity()
        obs.append(ob)
    return obs


LOOKS = {
    "dao_si_luyen_khi": "Đạo Sĩ Luyện Khí",
    "dao_si_hoa_than": "Đạo Sĩ Hóa Thần",
}


def build(rig, col, look_id):
    k = Kit(rig, col)
    skin = mat("MAT_skin", (0.94, 0.72, 0.56), "skin")
    if look_id == "dao_si_luyen_khi":
        hemp = mat("MAT_lk_tunic", (0.52, 0.49, 0.42), "earth")
        trim = mat("MAT_lk_trim", (0.30, 0.26, 0.21), "earth")
        beltm = mat("MAT_lk_belt", (0.26, 0.18, 0.13), "wood")
        trous = mat("MAT_lk_trousers", (0.22, 0.19, 0.24), "hair")
        wrap = mat("MAT_lk_wrap", (0.56, 0.50, 0.40), "earth")
        shoe = mat("MAT_lk_shoe", (0.22, 0.16, 0.12), "wood")
        hair = mat("MAT_lk_hair", (0.13, 0.11, 0.11), "hair")
        hair_hi = mat("MAT_lk_hair_hi", (0.24, 0.20, 0.25), "hair")
        tie = mat("MAT_lk_tie", (0.62, 0.44, 0.26), "wood")
        build_head(k, skin)
        build_hair(k, hair, tie, hair_hi=hair_hi)
        build_body(k, skin, hemp)
        build_legs(k, trous, wrap, shoe, trouser_len=0.20, loose=0.068)
        upper_garment(k, "SM_tunic", hemp)
        skirt_panels(k, "SM_tunic_skirt", hemp, 0.40, flare=0.02)
        lapels(k, trim)
        belt(k, beltm)
        sleeves(k, hemp, trim, to_elbow=True)
        forearm_wraps(k, wrap)
    else:
        teal = mat("MAT_ht_robe", (0.18, 0.60, 0.58), "teal")
        purple = mat("MAT_ht_coat", (0.48, 0.30, 0.70), "purple")
        lining = mat("MAT_ht_lining", (0.20, 0.55, 0.55), "teal")
        gold = mat("MAT_ht_gold", (0.98, 0.80, 0.34), "gold", metal=0.9, rough=0.35)
        trous = mat("MAT_ht_trousers", (0.74, 0.76, 0.82), "bone")
        boot = mat("MAT_ht_boot", (0.30, 0.22, 0.42), "purple")
        hair = mat("MAT_ht_hair", (0.44, 0.30, 0.68), "purple")
        tie = mat("MAT_ht_tie", (0.22, 0.75, 0.70), "teal")
        halo_m = geo.material("MAT_ht_halo", (1.0, 0.84, 0.36), emit=(1.0, 0.84, 0.36), emit_strength=6.0,
                              glow="holy", halo=0, priority=2.5)
        hair_hi = mat("MAT_ht_hair_hi", (0.66, 0.50, 0.88), "purple")
        sash = mat("MAT_ht_sash", (0.36, 0.20, 0.52), "purple")
        build_head(k, skin)
        build_hair(k, hair, tie, hair_hi=hair_hi, long=True, ornament=tie)
        build_body(k, skin, teal)
        build_legs(k, trous, boot, boot, trouser_len=0.27, loose=0.06)
        # the teal robe is the main front mass, collar to hem; boots show under it
        upper_garment(k, "SM_robe", teal)
        skirt_panels(k, "SM_robe_skirt", teal, 0.16, flare=0.025, side_split=0.45)
        lapels(k, gold, width=0.013)
        belt(k, gold, knot_m=sash, tails=True)
        coat_cape(k, purple, lining, gold, hem_z=0.11, opening=1.05)
        k.add("SM_collar", geo.lathe([(0.71, 0.075, 0.062, 0.006), (0.745, 0.068, 0.058, 0.006)], 8, phase=math.pi / 8,
                                     gap=1.2, cap_bottom=False, cap_top=False), lining, R.w_rigid("chest"), solid=0.01)
        wide_sleeves(k, purple, lining, gold)
        # the teal shoulder mantle with its stand-up collar (row 5 of the reference)
        k.add("SM_mantle", geo.lathe([(0.615, 0.185, 0.115, 0.004), (0.665, 0.165, 0.10, 0.004),
                                      (0.715, 0.12, 0.082, 0.004), (0.745, 0.075, 0.062, 0.004)], 8, phase=math.pi / 8,
                                     gap=0.7, cap_bottom=False, cap_top=False), lining,
              R.w_near(["chest", "upper_arm.L", "upper_arm.R"], power=4), solid=0.012)
        halo(k, halo_m)
    return k.objs
