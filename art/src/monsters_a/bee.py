"""The spirit bee (Linh Phong, server/data/creatures/bees.json). Runs inside Blender.

Seen side-on (the kit's camera lowered to 12 degrees: bees fly, they do not stand on the
ground). An abdomen with three bands of stripe colour, each about 2 px wide with 2 px of
body colour between them; a dark round thorax; a head with one big eye and a light pixel;
pale wings above the back beating between up and down; a small stinger; two antennae whose
tips glow in the colour of the species' element. About 0.5 m long: 19 px at the kit's
38 px/m, in a 32x32 frame with the pivot on the body centre (16,16).

Clips: `fly` 4 frames (wing beat, a little bob; loops) and `sting` 2 frames (lunge with the
abdomen curled forward, then recoil; events.hit = 0). Facings: right and left only.

Colours: every species is rendered as its own sheet `bee_<id>` (18 renders of the same rig).
The four `look` colours of bees.json drive the materials: body -> head and abdomen,
stripe -> the three abdomen bands and the thorax, wing -> both wings (lightened 35 % toward
white), eye -> both eyes. TWEAK gives near-identical pairs one visible difference. The kit snaps each to
the nearest palette ramp, so the shading, outline and catch-light stay right per species,
which a flat recolour of one key-coloured sheet cannot do at this size.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from rig import aim, armature, attach, ball, clip, cone, material, use_collection

TAU = 2 * math.pi
ROOT = Path(__file__).resolve().parents[3]
DATA = {k: v for k, v in json.loads((ROOT / "server" / "data" / "creatures" / "bees.json").read_text("utf-8")).items()
        if not k.startswith("_")}
# element -> glow ramp of the antenna tips
ELEMENT_GLOW = {"mac": "cosmic", "moc": "verdant", "thuy": "spirit", "hoa": "flame", "phong": "ice",
                "tho": "holy", "kim": "holy", "bang": "ice", "loi": "thunder", "quang": "holy"}
GLOW_RGB = {"cosmic": (0.78, 0.55, 1.0), "verdant": (0.48, 0.92, 0.60), "spirit": (0.35, 0.88, 0.96),
            "flame": (1.0, 0.68, 0.23), "ice": (0.69, 0.86, 1.0), "holy": (1.0, 0.89, 0.48),
            "thunder": (0.72, 0.75, 1.0)}


def hexrgb(h):
    """'#RRGGBB' (sRGB, as the data writes colours) -> linear RGB for Blender's Base Color
    (the kit renders raw albedo and converts back to sRGB before snapping to the palette)."""
    h = h.lstrip("#")
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


MATS = {}


def build_bee():
    """Side-on spirit bee, head toward -y (the kit turns it to face right / left)."""
    use_collection("COL_bee")
    M = MATS
    M["body"] = material("MAT_bee_body", (0.80, 0.55, 0.10))
    M["stripe"] = material("MAT_bee_stripe", (0.02, 0.02, 0.02))
    M["wing"] = material("MAT_bee_wing", (0.85, 0.90, 0.95))
    M["eye"] = material("MAT_bee_eye_iris", (0.02, 0.02, 0.02))
    M["eye"]["kit_priority"] = 3.0
    M["shine"] = material("MAT_bee_shine_pip", (0.97, 0.96, 0.97), ramp="bone")
    M["shine"]["kit_priority"] = 3.0
    M["dark"] = material("MAT_bee_dark", (0.11, 0.10, 0.13), ramp="hair")
    M["tip"] = material("MAT_bee_tip", (1.0, 0.89, 0.48), emit=4.0, glow="holy")
    M["tip"]["kit_priority"] = 3.0
    M["tip"]["kit_halo"] = 0
    # seen from the side and lit from the upper left, keep the body and bands on their base
    # tone so the species colours stay true; the wings stay light
    for k in ("body", "stripe"):
        M[k]["kit_light"] = 0.97
        M[k]["kit_shadow"] = 0.15
    M["wing"]["kit_light"] = 0.35
    M["wing"]["kit_shadow"] = -1.0

    arm = armature("bee", [
        ("root", (0, 0, -0.05), (0, 0, 0.05), None),
        ("body", (0, 0, -0.04), (0, 0, 0.06), "root"),
        ("abdomen", (0, 0.02, 0.0), (0, 0.36, 0.0), "body"),
        ("head", (0, -0.06, 0.0), (0, -0.17, 0.0), "body"),
        ("wing_l", (0.02, -0.02, 0.07), (0.02, 0.10, 0.07), "body"),
        ("wing_r", (-0.02, -0.02, 0.07), (-0.02, 0.10, 0.07), "body"),
    ])
    # the abdomen: three bands of stripe colour, each about 2 px wide at 38 px/m, with
    # 2 px of body colour between them and a body-coloured tip
    ay, ry_, rr = 0.16, 0.18, 0.105
    parts = [ball("bee_abdomen", (rr, ry_, rr * 0.95), (0, ay, 0.0), M["body"], seg=18, rings=12)]
    for k, yc in enumerate((0.0575, 0.1675, 0.2775)):
        f = max(0.0, 1 - ((yc - ay) / ry_) ** 2) ** 0.5
        # a short cylinder a little wider than the body there, so the whole band shows
        r_band = rr * f + 0.006
        parts.append(cone(f"bee_band{k}", r_band, r_band, 0.058, (0, yc, 0.0), M["stripe"], rot=(90, 0, 0), seg=18))
    parts.append(aim("bee_sting", M["dark"], (0, 0.335, -0.01), (0, 0.39, -0.03), 0.02, 0.0, seg=5))
    att(arm, "abdomen", *parts)
    # thorax and head; one big eye on each side with a light pixel
    att(arm, "body", ball("bee_thorax", (0.075, 0.075, 0.075), (0, -0.04, 0.01), M["stripe"], seg=14, rings=8),
        *[aim(f"bee_leg{k}{s}", M["dark"], (s * 0.03, y, -0.05), (s * 0.035, y + 0.02, -0.11), 0.01, 0.006, seg=4)
          for k, y in enumerate((-0.06, -0.02)) for s in (1, -1)])
    att(arm, "head", ball("bee_head", (0.065, 0.065, 0.068), (0, -0.125, 0.0), M["body"], seg=14, rings=8),
        ball("bee_eyel", (0.03, 0.04, 0.048), (0.048, -0.14, 0.008), M["eye"], seg=10, rings=6),
        ball("bee_eyer", (0.03, 0.04, 0.048), (-0.048, -0.14, 0.008), M["eye"], seg=10, rings=6),
        ball("bee_shinel", (0.016,) * 3, (0.07, -0.152, 0.026), M["shine"], seg=6, rings=4),
        ball("bee_shiner", (0.016,) * 3, (-0.07, -0.152, 0.026), M["shine"], seg=6, rings=4),
        aim("bee_antl", M["dark"], (0.02, -0.15, 0.05), (0.03, -0.21, 0.11), 0.009, 0.007, seg=4),
        aim("bee_antr", M["dark"], (-0.02, -0.15, 0.05), (-0.03, -0.21, 0.11), 0.009, 0.007, seg=4),
        ball("bee_tipl", (0.018,) * 3, (0.03, -0.215, 0.115), M["tip"], seg=6, rings=4),
        ball("bee_tipr", (0.018,) * 3, (-0.03, -0.215, 0.115), M["tip"], seg=6, rings=4))
    # wings: flat, pale, standing above the back; they hinge at the thorax and beat
    # between up (raised behind the head) and down (swept back along the body)
    for s, b in ((1, "wing_l"), (-1, "wing_r")):
        att(arm, b, ball(f"bee_{b}", (0.008, 0.13, 0.036), (s * 0.02, 0.08, 0.13), M["wing"], rot=(-38, 0, 0), seg=12, rings=8),
            ball(f"bee_{b}2", (0.007, 0.09, 0.026), (s * 0.02, 0.10, 0.085), M["wing"], rot=(-18, 0, 0), seg=10, rings=6))

    def wings(a):
        return {"wing_l": {"r": (a, 0, 0)}, "wing_r": {"r": (a, 0, 0)}}
    fly = []
    for i, (a, z) in enumerate(((-40, 0.0), (-5, 0.012), (35, 0.018), (-5, 0.008))):
        p = {"body": {"l": (0, 0, z), "r": (-4, 0, 0)}, "abdomen": {"r": (3 * math.sin(TAU * i / 4), 0, 0)}}
        p.update(wings(a))
        fly.append(p)
    sting = [dict({"root": {"l": (0, -0.01, 0.0)}, "body": {"r": (8, 0, 0)}, "abdomen": {"r": (-34, 0, 0)}}, **wings(-35)),
             dict({"root": {"l": (0, 0.01, 0.01)}, "body": {"r": (-8, 0, 0)}, "abdomen": {"r": (-8, 0, 0)}}, **wings(25))]
    clip(arm, "fly", fly, 12, True)
    clip(arm, "sting", sting, 12, False, hit=0)
    arm.animation_data.action = None
    return arm


# pairs whose looks are near-identical once snapped to the palette get one visible
# difference (a band or wing tint), so every species can be told apart
TWEAK = {"tra": {"wing": "#F4E2B0"}, "thao": {"wing": "#D8F0C0"},
         "nguyet_quang": {"wing": "#FFF0B0"}, "bang_tam": {"wing": "#C8E4FF"},
         "vu": {"wing": "#E8F4FF"}, "thuy_linh": {"stripe": "#C8E4FF"},
         "hoang_kim": {"wing": "#FFF4C8"}, "kim_o": {"wing": "#FFD8B0"}}


def lighten(rgb, k=0.35):
    return tuple(c + (1.0 - c) * k for c in rgb)


def recolour(look: dict, element: str, sid: str = ""):
    """Point the shared materials at one species' look (and its element glow). The wing
    colour is lightened so the wings read as pale and translucent next to the body."""
    from rig import _set_mat
    look = {**look, **TWEAK.get(sid, {})}
    for key in ("body", "stripe", "wing", "eye"):
        m = MATS[key]
        c = hexrgb(look[key])
        m["col_base"] = list(lighten(c) if key == "wing" else c)
        _set_mat(m, "base")
    g = ELEMENT_GLOW.get(element, "holy")
    t = MATS["tip"]
    t["col_base"] = list(GLOW_RGB[g])
    t["ecol_base"] = list(GLOW_RGB[g])
    t["glow_base"] = g
    _set_mat(t, "base")
