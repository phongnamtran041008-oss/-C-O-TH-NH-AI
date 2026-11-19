"""Look-dev v2 figure: planar, tapered low-poly forms (runs inside Blender).

Flat-shaded facets, 6-8 sided limbs, a wedge torso and a boxy head: the kit's 3-tone
shading then gives each plane one clean tone instead of the blotches a round blob turns into
at 48 px. Face parts are separate pieces sized in whole final pixels (PX = 1/PPM metres) and
placed on the head relative to the head bone, which the kit snaps to the pixel grid.
"""
from __future__ import annotations

import math

from mathutils import Matrix, Vector

import geo
import rig as R
from ld_rig import PX


def V(*a):
    return Vector(a)


# ---------------------------------------------------------------- primitives
def cuboid(center, half, *, top_scale=(1.0, 1.0), rot=None):
    """A box (optionally tapered toward +Z) - 8 verts, 6 faces."""
    hx, hy, hz = half
    tx, ty = top_scale
    v = [V(-hx, -hy, -hz), V(hx, -hy, -hz), V(hx, hy, -hz), V(-hx, hy, -hz),
         V(-hx * tx, -hy * ty, hz), V(hx * tx, -hy * ty, hz), V(hx * tx, hy * ty, hz), V(-hx * tx, hy * ty, hz)]
    if rot is not None:
        v = [rot @ p for p in v]
    c = V(*center)
    v = [p + c for p in v]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return v, f


def limb(points, radii, sides=6, flat_y=1.0):
    """A faceted tapered prism along points (closed ends)."""
    rr = [(r, r * flat_y) for r in radii]
    return geo.sweep(points, rr, sides, tip=False, up=(0, -1, 0))


def faceted(verts, faces):
    return verts, faces


class Kit:
    """Adds flat-shaded pieces bound to the rig."""

    def __init__(self, rig, col):
        self.rig, self.col, self.objs = rig, col, []

    def add(self, name, part, mat, wfn, *, solid=0.0, smooth=False):
        ob = geo.mesh_object(name, part[0], part[1], mat, self.col, smooth=smooth, flat=not smooth,
                             subsurf=0, solidify=solid)
        R.bind(ob, self.rig, wfn)
        self.objs.append(ob)
        return ob


def mat(name, rgb, ramp=None, **kw):
    """Cloth and skin get wider light and shadow bands than the kit default, so every big
    piece shows all three tones (light on the upper-left planes, shadow under and right)."""
    kw.setdefault("shadow", 0.30)
    kw.setdefault("light", 0.78)
    return geo.material(name, rgb, ramp=ramp, **kw)


# ---------------------------------------------------------------- head and face
HEAD_FRONT = -0.090         # y of the flat face plane
EYE_Z = 0.818
FRINGE_Z = 0.885            # lowest point of the fringe over the forehead


def head_part():
    """An octagonal skull with a flat face, tapering to a narrow jaw and chin."""
    prof = [(0.748, 0.034, 0.030, -0.03), (0.768, 0.074, 0.062, -0.022), (0.800, 0.100, 0.086, -0.008),
            (0.845, 0.110, 0.097, 0.0), (0.895, 0.112, 0.100, 0.004), (0.945, 0.098, 0.092, 0.008),
            (0.980, 0.066, 0.066, 0.008), (0.995, 0.0, 0.0, 0.008)]
    return geo.lathe(prof, 8, phase=math.pi / 8)


def face_materials(skin_rgb):
    """The face is ONE clean skin tone (its shading pinned: never the shadow colour, never
    the light), and its only shading is drawn on purpose: a 1 px line under the fringe and
    the mouth, one tone darker (the same ramp pinned to its shadow tone)."""
    face = geo.material("MAT_face", skin_rgb, ramp="skin", shadow=-2.0, light=3.0)
    shade = geo.material("MAT_face_shade", skin_rgb, ramp="skin", shadow=2.0, light=3.0, priority=2.5)
    return face, shade


def build_head(k: Kit, skin, skin_rgb=(0.94, 0.72, 0.56), eye_col=(0.08, 0.06, 0.08), white=(0.97, 0.95, 0.92),
               brow_col=(0.12, 0.09, 0.08)):
    head = R.w_rigid("head")
    face, shade = face_materials(skin_rgb)
    k.add("SM_head", head_part(), face, head)
    k.add("SM_neck", limb([V(0, 0.005, 0.70), V(0, 0.0, 0.775)], [0.036, 0.033], 6), skin, R.w_near(["chest", "neck", "head"]))
    eye_m = mat("MAT_eye", eye_col, "hair", priority=4.0, shadow=2.0, light=3.0)
    white_m = mat("MAT_eye_white", (1.0, 0.86, 0.74), "skin", priority=3.5, shadow=-2.0, light=-1.0)
    brow_m = mat("MAT_brow", brow_col, "hair", priority=3.0, shadow=2.0, light=3.0)
    yf = HEAD_FRONT - 0.003
    for s in (1, -1):
        # eye: 1 px wide x 2 px tall, the two eyes 2 px apart; a light pixel above-outside
        xc = s * 1.5 * PX
        k.add("SM_eye", cuboid((xc, yf, EYE_Z), (0.5 * PX, 0.005, 1.0 * PX)), eye_m, head)
        k.add("SM_eye_light", cuboid((xc + s * PX, yf, EYE_Z + 1.5 * PX), (0.5 * PX, 0.004, 0.5 * PX)), white_m, head)
        # profile marks: thin plates on the side facets, edge-on (invisible) from the front
        k.add("SM_eye_side", cuboid((s * 0.074, -0.07, EYE_Z), (0.003, 0.5 * PX, 1.0 * PX)), eye_m, head)
        k.add("SM_brow_side", cuboid((s * 0.078, -0.066, EYE_Z + 2.0 * PX), (0.003, 0.8 * PX, 0.45 * PX)), brow_m, head)
        k.add("SM_ear", cuboid((s * 0.112, 0.005, 0.818), (0.014, 0.022, 0.03)), face, head)
    # the deliberate face shadow: one pixel line under the fringe, across the forehead
    k.add("SM_fringe_shadow", cuboid((0, yf + 0.001, FRINGE_Z - 0.5 * PX), (2.5 * PX, 0.004, 0.5 * PX)), shade, head)
    # nose (a profile bump on clean skin), mouth 1 px one tone darker, chin from the head shape
    k.add("SM_nose", cuboid((0, HEAD_FRONT - 0.013, 0.796), (0.010, 0.015, 0.017), top_scale=(0.5, 0.35)), face, head)
    k.add("SM_mouth", cuboid((0, yf, 0.772), (0.5 * PX, 0.004, 0.5 * PX)), shade, head)


def lock(base, direction, length, width, thick=0.016, side=(1, 0, 0), curl=0.0):
    """A pointed hair lock (a faceted shard)."""
    return geo.leaf(base, direction, length, width, side=side, thick=thick, shape="shard", segs=3, tip_curl=curl)


def build_hair(k: Kit, hair, tie, *, hair_hi=None, long=False, ornament=None):
    """Hair as locks, not a helmet: a crown, 3-4 pointed tufts at the crown and back, a
    fringe of three points, side locks standing off the cheeks, highlight locks on a
    one-tone-lighter material, a round topknot with its tie."""
    head = R.w_rigid("head")
    hi = hair_hi or hair
    crown = geo.lathe([(0.900, 0.116, 0.104, 0.014), (0.945, 0.112, 0.104, 0.014), (0.982, 0.088, 0.086, 0.014),
                       (1.006, 0.05, 0.05, 0.014), (1.014, 0.0, 0.0, 0.014)], 8, phase=math.pi / 8)
    k.add("SM_hair_crown", crown, hair, head)
    k.add("SM_hair_back", cuboid((0, 0.06, 0.875), (0.106, 0.045, 0.075), top_scale=(1.05, 1.0)), hair, head)
    # tufts breaking the silhouette at the crown and the back (pointing up / out / back)
    for x, y, z, d, ln, m in ((0.07, 0.02, 0.99, (0.6, 0.3, 0.75), 0.075, hair), (-0.075, 0.03, 0.985, (-0.65, 0.35, 0.65), 0.07, hi),
                              (0.09, 0.08, 0.92, (0.55, 0.75, 0.1), 0.065, hair), (-0.085, 0.085, 0.905, (-0.5, 0.8, -0.1), 0.06, hair),
                              (0.0, 0.10, 0.83, (0.05, 0.6, -0.8), 0.07, hair)):
        k.add("SM_hair_tuft", lock(V(x, y, z), d, ln, 0.045, thick=0.018), m, head)
    # fringe: three points over the forehead, parted a little off centre
    for x, d, ln, w, m in ((-0.06, (-0.35, -0.25, -1.0), 0.085, 0.05, hair), (0.012, (0.15, -0.2, -1.0), 0.07, 0.045, hi),
                           (0.07, (0.4, -0.25, -1.0), 0.08, 0.05, hair)):
        k.add("SM_hair_fringe", lock(V(x, -0.098, 0.97), d, ln, w, thick=0.012, side=(1, 0, 0)), m, head)
    # side locks: in front of the ears, standing off the cheeks so a gap of skin shows
    for s in (1, -1):
        k.add("SM_hair_side", lock(V(s * 0.122, -0.045, 0.93), (s * 0.12, -0.05, -1.0), 0.15, 0.03, thick=0.012,
                                   side=(0, 1, 0)), hair, head)
        k.add("SM_hair_lock", lock(V(s * 0.118, 0.04, 0.95), (s * 0.3, 0.5, -0.8), 0.13, 0.05, thick=0.016,
                                   side=(0, 1, 0)), hi if s > 0 else hair, head)
    # topknot: round, with a contrasting tie
    k.add("SM_hair_bun", geo.ellipsoid((0, 0.025, 1.045), (0.042, 0.04, 0.036), 8, 6), hair, head)
    k.add("SM_hair_bun_hi", geo.ellipsoid((-0.012, 0.0, 1.058), (0.018, 0.012, 0.015), 6, 4), hi, head)
    k.add("SM_hair_tie", geo.lathe([(1.0, 0.03, 0.03, 0.022), (1.016, 0.036, 0.036, 0.022)], 8), tie, head)
    if ornament is not None:
        k.add("SM_hair_ornament", cuboid((0, 0.0, 1.075), (0.016, 0.014, 0.02)), ornament, head)
    if long:
        # strands over the crown, running back from the parting, so the cap is not a helmet
        for x, m in ((-0.075, hair), (-0.035, hi), (0.005, hair), (0.045, hi), (0.08, hair)):
            pts = [V(x * 0.6, -0.06, 1.012), V(x * 1.0, 0.02, 1.02), V(x * 1.15, 0.085, 0.975), V(x * 1.2, 0.115, 0.9)]
            k.add("SM_hair_crown_lock", geo.sweep(pts, [(0.02, 0.008), (0.024, 0.01), (0.022, 0.01), (0.0, 0.008)], 4,
                                                  up=(0, 0, 1)), m, head)
        # long hair: five separate strands down the back, alternating light and base locks
        wf = R.w_chain(["hair_01", "hair_02", "hair_03"], 0.90, 0.48, top_bone="head")
        for x, w, zb, m in ((-0.085, 0.035, 0.55, hair), (-0.042, 0.035, 0.47, hi), (0.0, 0.04, 0.44, hair),
                            (0.045, 0.035, 0.48, hi), (0.088, 0.032, 0.56, hair)):
            pts = [V(x * 0.9, 0.08, 0.93), V(x * 1.1, 0.115, 0.82), V(x * 1.2, 0.124, 0.68), V(x * 1.15, 0.122, zb + 0.06),
                   V(x * 1.1, 0.118, zb)]
            k.add("SM_hair_long", geo.sweep(pts, [(w, 0.016), (w * 1.1, 0.018), (w, 0.016), (w * 0.7, 0.014), (0.0, 0.01)],
                                            4, up=(0, 1, 0)), m, wf)
        for s in (1, -1):     # a strand falling in front of each shoulder
            pts = [V(s * 0.125, -0.04, 0.90), V(s * 0.13, -0.045, 0.78), V(s * 0.135, -0.04, 0.67), V(s * 0.135, -0.03, 0.60)]
            k.add("SM_hair_front", geo.sweep(pts, [(0.016, 0.012), (0.016, 0.012), (0.013, 0.01), (0.0, 0.008)], 4,
                                             up=(s, 0, 0)), hi, R.w_chain(["head", "chest"], 0.76, 0.62))


# ---------------------------------------------------------------- body
def build_body(k: Kit, skin, under, *, bare_forearms=True):
    """Torso wedge, pelvis, faceted arms and legs, blocky fists. Clothes go over this."""
    k.add("SM_torso", geo.lathe([(0.535, 0.088, 0.062), (0.58, 0.084, 0.060), (0.635, 0.112, 0.068),
                                 (0.68, 0.135, 0.070), (0.705, 0.11, 0.060), (0.72, 0.045, 0.040)], 8, phase=math.pi / 8),
          under, R.w_near(["hips", "spine", "chest"], power=3))
    for s, side in ((1, "L"), (-1, "R")):
        sh = V(*R.BONES[f"upper_arm.{side}"][0])
        el = V(*R.BONES[f"forearm.{side}"][0])
        wr = V(*R.BONES[f"hand.{side}"][0])
        k.add(f"SM_shoulder.{side}", cuboid(sh + V(-s * 0.012, 0, 0.0), (0.04, 0.04, 0.03)), under,
              R.w_near(["chest", f"upper_arm.{side}"], power=3))
        k.add(f"SM_upperarm.{side}", limb([sh + V(0, 0, 0.01), el], [0.036, 0.031], 6), skin, R.w_rigid(f"upper_arm.{side}"))
        k.add(f"SM_forearm.{side}", limb([el + (el - wr).normalized() * 0.012, wr], [0.032, 0.026], 6), skin,
              R.w_rigid(f"forearm.{side}"))
        # fist: a block with the knuckles forward-down and a thumb on the inside
        fc = wr + V(s * 0.003, -0.012, -0.03)
        k.add(f"SM_fist.{side}", cuboid(fc, (0.027, 0.030, 0.032), top_scale=(0.9, 0.85)), skin, R.w_rigid(f"hand.{side}"))
        k.add(f"SM_thumb.{side}", cuboid(fc + V(-s * 0.022, -0.016, 0.01), (0.009, 0.011, 0.016)), skin,
              R.w_rigid(f"hand.{side}"))


def build_legs(k: Kit, trousers, shin_mat, shoe, *, trouser_len=0.18, loose=0.07):
    """Pelvis + legs: loose trousers to `trouser_len` above the ankle, then shins (bare or
    wrapped) and cloth shoes."""
    k.add("SM_pelvis", cuboid((0, 0.0, 0.50), (0.10, 0.068, 0.045), top_scale=(0.95, 0.95)), trousers,
          R.w_near(["hips", "thigh.L", "thigh.R"], power=3))
    for s, side in ((1, "L"), (-1, "R")):
        hp = V(*R.BONES[f"thigh.{side}"][0])
        kn = V(*R.BONES[f"shin.{side}"][0])
        an = V(*R.BONES[f"foot.{side}"][0])
        k.add(f"SM_thigh.{side}", limb([hp + V(0, 0, 0.03), kn], [0.058, loose], 7), trousers, R.w_rigid(f"thigh.{side}"))
        cut = an.lerp(kn, max(0.0, min(1.0, (trouser_len - an.z) / (kn.z - an.z))))
        k.add(f"SM_trouser_low.{side}", limb([kn + V(0, 0, 0.01), cut], [loose * 0.95, loose * 0.85], 7), trousers,
              R.w_rigid(f"shin.{side}"))
        k.add(f"SM_shin.{side}", limb([cut + V(0, 0, 0.01), an + V(0, 0, -0.005)], [0.036, 0.03], 6), shin_mat,
              R.w_rigid(f"shin.{side}"))
        # cloth shoe: a wedge, sole flat on the ground
        k.add(f"SM_shoe.{side}", cuboid((an.x, -0.035, 0.022), (0.03, 0.062, 0.022), top_scale=(0.9, 0.7)), shoe,
              R.w_rigid(f"foot.{side}"))
