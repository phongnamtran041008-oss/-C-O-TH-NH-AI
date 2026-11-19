"""The twelve zodiac pets (Linh Thú gacha, server/data/creatures/pets.json), as cute spirit
animals. Runs inside Blender.

Small on purpose: in the game a beast sheet is drawn at 2x while the player sheet is drawn
at 1x, so a pet about 0.4 m tall reaches the player's knee-to-hip. That makes the face the
whole read, so eyes are big (iris, pupil, white catch-light at top pixel priority), and each
species keeps its strongest marks: rat's round ears and thin tail, ox's horns and muzzle,
tiger's stripes, cat's pointed ears and patch, horse's mane, goat's curled horns and beard,
monkey's heart face and curled tail, dog's floppy ears, pig's snout, dragon's antlers and
mane, rooster's comb, snake's coil. Each has one small xianxia touch (a glowing mark, a
bell, a tassel, a circlet, a pearl, a wisp).

Colours come from each species' `look` in pets.json (body / belly / nose / stripes /
patch / mane / beard / face / comb); the kit snaps them to the nearest palette ramp. One
look per species (the data defines no colour variants or rarity looks).

Clips: idle 4, walk 6, happy 4 (hop and quarter-turn spin, loops), sleep 4 (curled up,
breathing, loops). 48x48, four facings, kind "pet".
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from beasts import cute_eyes, eye_mats, extra_quad_clips
from quadrupeds import Legs, quad_armature
from rig import (aim, armature, attach, ball, box, clip, cone, lerp_pose, material, merge,
                 tube, skin, use_collection)

TAU = 2 * math.pi
PET_SCALE = 1.15          # knee-to-hip of the player at the game's drawing scale
ROOT = Path(__file__).resolve().parents[3]
DATA = json.loads((ROOT / "server" / "data" / "creatures" / "pets.json").read_text("utf-8"))["species"]


def S(i, n, ph=0.0):
    return math.sin(TAU * i / n + ph)


def C(i, n, ph=0.0):
    return math.cos(TAU * i / n + ph)


def att(arm, bone, *objs):
    for o in objs:
        attach(o, arm, bone)


def hexrgb(h):
    """'#RRGGBB' (sRGB, as the data writes colours) -> linear RGB for Blender's Base Color
    (the kit renders raw albedo and converts back to sRGB before snapping to the palette)."""
    h = h.lstrip("#")
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))


def col(name, hexcode, ramp=None):
    c = hexrgb(hexcode)
    return material(name, c, c, ramp=ramp)


def pcol(sid, part, hexcode, ramp=None):
    """A material for one part of species `sid`, pinned to its ramp (RAMPS)."""
    hexcode = TINT.get(sid, {}).get(part, hexcode)
    return col(f"MAT_{sid}_{part}", hexcode, ramp or RAMPS.get(sid, {}).get(part))


def glow(name, ramp, c, strength=3.0, halo=1):
    m = material(name, c, c, emit=strength, glow=ramp)
    m["kit_halo"] = halo
    return m


# ------------------------------------------------------------------ quadruped pets
# per species: body size (length, girth), leg height, head radius, features
# palette ramps that keep each species' look colour recognisable after snapping
# (part -> ramp; parts not listed snap to the nearest ramp)
RAMPS = {
    "chuot": {"body": "stone", "belly": "paper", "nose": "pink", "tail": "pink"},
    "trau": {"body": "wood", "belly": "earth", "nose": "earth"},
    "ho": {"body": "gold", "belly": "bone", "stripes": "hair"},
    "meo": {"body": "paper", "belly": "bone", "patch": "wood"},
    "rong": {"body": "jade", "belly": "gold", "mane": "red"},
    "ran": {"body": "leaf", "belly": "grass"},
    "ngua": {"body": "wood", "belly": "wood", "mane": "hair", "tail": "hair"},
    "de": {"body": "bone", "belly": "paper", "beard": "earth", "horn": "earth"},
    "khi": {"body": "wood", "belly": "skin", "face": "skin"},
    "ga": {"body": "paper", "belly": "gold"},
    "cho": {"body": "wood", "belly": "paper", "nose": "hair", "ear": "wood"},
    "lon": {"body": "pink", "belly": "pink", "nose": "red"},
}
# body colours that read better a shade off the data (the hue the data names, on the palette)
TINT = {"ho": {"body": "#D8902A", "belly": "#F4F0E8"}, "rong": {"body": "#4FA678"}, "lon": {"body": "#E89AB0"}}


QUADS = {
    "chuot": dict(scale=0.9, ears="round", tail="thin", snout="short", whiskers=True, touch="tailglow"),
    "trau": dict(scale=1.12, girth=1.25, ears="side", horns="ox", tail="tuft", snout="muzzle", touch="noseRing"),
    "ho": dict(scale=1.05, head=1.15, ears="round", tail="tiger", snout="cat", whiskers=True, stripes=True,
               cheeks=True, chest=True, touch="browGlow"),
    "meo": dict(scale=0.95, ears="point", tail="long", snout="cat", whiskers=True, patch=True, touch="bell"),
    "rong": dict(scale=1.05, length=1.3, ears="none", horns="antler", tail="dragon", snout="dragon", mane=True,
                 touch="pearl", spines=True),
    "ngua": dict(scale=1.1, leg=1.35, ears="point", tail="horse", snout="horse", mane=True, touch="maneWisp"),
    "de": dict(scale=1.0, ears="side", horns="goat", tail="fluffy", snout="goat", beard=True, touch="hornTassel"),
    "khi": dict(scale=1.0, ears="monkey", tail="monkey", snout="monkey", face=True, chest=True, touch="circlet"),
    "cho": dict(scale=1.0, ears="flop", tail="wag", snout="dog", chest=True, touch="collarTassel"),
    "lon": dict(scale=1.05, girth=1.2, leg=0.85, ears="pig", tail="curl", snout="pig", touch="browMark"),
}


def build_quad_pet(sid):
    F = dict(QUADS[sid])
    L = DATA[sid]["look"]
    use_collection(f"COL_pet_{sid}")
    body = pcol(sid, "body", L["body"])
    belly = pcol(sid, "belly", L.get("belly", L["body"]))
    nose = pcol(sid, "nose", L.get("nose", "#2B2B2B"))
    dark = col(f"MAT_{sid}_mouth", "#2B2B2B", ramp="hair")
    pink = col(f"MAT_{sid}_inner", "#F4C2CF", ramp="pink")
    mats = eye_mats(f"p{sid}", (0.42, 0.35, 0.28))
    lg = F.get("leg", 1.0)
    ln = F.get("length", 1.0)
    gi = F.get("girth", 1.0)
    h = 0.15 * lg
    HY, HZ = -0.12 * ln, h + 0.15
    P = {"h": h, "yf": -0.045 * ln, "yb": 0.06 * ln, "x": 0.05 * gi, "knee": 0.075 * lg,
         "head": (-0.075 * ln, h + 0.04), "hlen": 0.12, "jaw": (HY - 0.06, HZ - 0.04),
         "tail": ((0, 0.09 * ln, h + 0.02)[1:], (0.15 * ln, h + 0.06), (0.19 * ln, h + 0.12))}
    P["tail"] = ((0.09 * ln, h + 0.02), (0.15 * ln, h + 0.06), (0.19 * ln, h + 0.12))
    arm = quad_armature(f"pet_{sid}", P, extra=[("eyes", (0, HY - 0.09, HZ - 0.02), (0, HY - 0.09, HZ + 0.05), "head")])

    # body and legs
    att(arm, "chest", ball(f"{sid}_chest", (0.075 * gi, 0.075 * ln, 0.068 * gi), (0, -0.015 * ln, h + 0.005), body),
        ball(f"{sid}_bellyf", (0.055 * gi, 0.05, 0.04), (0, -0.04 * ln, h - 0.035), belly))
    att(arm, "pelvis", ball(f"{sid}_rump", (0.07 * gi, 0.075 * ln, 0.065 * gi), (0, 0.045 * ln, h), body))
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side}1", aim(f"{sid}_{leg}{side}up", body, (x, y, h - 0.02), (x, y, P["knee"]), 0.03 * gi, 0.024, seg=8))
            att(arm, f"{leg}{side}2", aim(f"{sid}_{leg}{side}lo", body, (x, y, P["knee"] + 0.005), (x, y, 0.03), 0.022, 0.02, seg=8))
            att(arm, f"{leg}{side}3", ball(f"{sid}_{leg}{side}paw", (0.026, 0.03, 0.02), (x, y - 0.004, 0.018),
                                           belly if sid in ("meo", "cho", "ngua") else body, seg=8, rings=5))
    # head
    hs = F.get("head", 1.0)
    hd = [ball(f"{sid}_head", (0.12 * hs, 0.105, 0.105 * (1 + (hs - 1) * 0.5)), (0, HY, HZ), body)]
    if F.get("cheeks"):      # tiger: white cheek ruffs
        wc = pcol(sid, "belly", L.get("belly", "#F4EBD9"))
        hd += [ball(f"{sid}_cheek{s}", (0.055, 0.045, 0.045), (s * 0.075, HY - 0.06, HZ - 0.035), wc, seg=10, rings=6) for s in (1, -1)]
    if F.get("chest"):       # a pale bib that shows from the front
        bib = pcol(sid, "face", L.get("face", L["belly"])) if sid == "khi" else belly
        att(arm, "chest", ball(f"{sid}_bib", (0.055 * gi, 0.03, 0.055), (0, -0.075 * ln, h - 0.005), bib, seg=10, rings=6))
    sn = F["snout"]
    if sn in ("short", "cat"):
        hd += [ball(f"{sid}_muzzle", (0.045, 0.03, 0.03), (0, HY - 0.095, HZ - 0.035), belly, seg=10, rings=6),
               ball(f"{sid}_nose", (0.015, 0.012, 0.012), (0, HY - 0.12, HZ - 0.02), nose, seg=6, rings=4)]
    elif sn in ("dog", "horse", "dragon", "goat"):
        long_ = {"dog": 0.07, "horse": 0.10, "dragon": 0.09, "goat": 0.07}[sn]
        hd += [aim(f"{sid}_snout", belly if sn != "dragon" else body, (0, HY - 0.06, HZ - 0.03),
                   (0, HY - 0.06 - long_, HZ - 0.05), 0.045, 0.035, seg=10, smooth=True),
               ball(f"{sid}_nose", (0.02, 0.015, 0.015), (0, HY - 0.07 - long_, HZ - 0.035), nose, seg=6, rings=4)]
    elif sn == "muzzle":     # ox: a broad pale muzzle with nostrils
        hd += [box(f"{sid}_muzzle", (0.11, 0.06, 0.06), (0, HY - 0.09, HZ - 0.04), nose, bevel=0.025),
               ball(f"{sid}_nostl", (0.012,) * 3, (0.025, HY - 0.12, HZ - 0.03), dark, seg=5, rings=4),
               ball(f"{sid}_nostr", (0.012,) * 3, (-0.025, HY - 0.12, HZ - 0.03), dark, seg=5, rings=4)]
    elif sn == "pig":
        hd += [cone(f"{sid}_snout", 0.04, 0.04, 0.035, (0, HY - 0.105, HZ - 0.03), nose, rot=(90, 0, 0), seg=12),
               ball(f"{sid}_nostl", (0.01, 0.006, 0.014), (0.015, HY - 0.124, HZ - 0.03), dark, seg=5, rings=4),
               ball(f"{sid}_nostr", (0.01, 0.006, 0.014), (-0.015, HY - 0.124, HZ - 0.03), dark, seg=5, rings=4)]
    elif sn == "monkey":
        pass
    if F.get("face"):        # monkey: pale heart-shaped face
        face = pcol(sid, "face", L.get("face", L["belly"]))
        hd += [ball(f"{sid}_face", (0.085, 0.04, 0.07), (0, HY - 0.075, HZ - 0.01), face, seg=12, rings=6),
               ball(f"{sid}_facel", (0.045, 0.03, 0.04), (0.035, HY - 0.08, HZ + 0.03), face, seg=10, rings=5),
               ball(f"{sid}_facer", (0.045, 0.03, 0.04), (-0.035, HY - 0.08, HZ + 0.03), face, seg=10, rings=5),
               ball(f"{sid}_nose", (0.014, 0.01, 0.01), (0, HY - 0.115, HZ - 0.02), dark, seg=6, rings=4)]
    ears = F["ears"]
    for s in (1, -1):
        if ears == "round":
            big = 1.35 if sid == "chuot" else 1.0      # a rat is all ears
            hd += [ball(f"{sid}_ear{s}", (0.045 * big, 0.02, 0.045 * big), (s * 0.085 * big, HY + 0.01, HZ + 0.09 * big), body, seg=10, rings=6),
                   ball(f"{sid}_eari{s}", (0.03 * big, 0.01, 0.03 * big), (s * 0.085 * big, HY - 0.01, HZ + 0.09 * big), pink, seg=8, rings=5)]
        elif ears == "point":
            hd += [aim(f"{sid}_ear{s}", body, (s * 0.06, HY + 0.01, HZ + 0.07), (s * 0.085, HY + 0.02, HZ + 0.16), 0.04, 0.0, seg=6),
                   aim(f"{sid}_eari{s}", pink, (s * 0.06, HY - 0.005, HZ + 0.075), (s * 0.08, HY + 0.005, HZ + 0.135), 0.022, 0.0, seg=6)]
        elif ears == "side":
            hd += [ball(f"{sid}_ear{s}", (0.04, 0.02, 0.022), (s * 0.12, HY + 0.01, HZ + 0.03), body, rot=(0, s * -20, 0), seg=8, rings=5)]
        elif ears == "flop":
            em = pcol(sid, "ear", "#7A4A2A")
            hd += [ball(f"{sid}_ear{s}", (0.035, 0.03, 0.08), (s * 0.125, HY + 0.01, HZ - 0.015), em,
                        rot=(0, s * 18, 0), seg=10, rings=6)]
        elif ears == "pig":
            hd += [aim(f"{sid}_ear{s}", body, (s * 0.07, HY + 0.0, HZ + 0.07), (s * 0.10, HY - 0.04, HZ + 0.12), 0.035, 0.0, seg=6)]
        elif ears == "monkey":
            hd += [ball(f"{sid}_ear{s}", (0.035, 0.02, 0.045), (s * 0.12, HY + 0.0, HZ + 0.02), pcol(sid, "face", L.get("face", L["belly"])), seg=8, rings=5)]
    horns = F.get("horns")
    hornm = pcol(sid, "horn", {"goat": "#8C7458", "antler": "#E9C46A"}.get(horns, "#F4EBD9"),
                 ramp=RAMPS.get(sid, {}).get("horn") or ("gold" if horns == "antler" else "paper"))
    for s in (1, -1):
        if horns == "ox":
            hd += [aim(f"{sid}_horn{s}", hornm, (s * 0.07, HY + 0.01, HZ + 0.08), (s * 0.15, HY + 0.0, HZ + 0.11), 0.026, 0.012, seg=6),
                   aim(f"{sid}_horntip{s}", hornm, (s * 0.15, HY + 0.0, HZ + 0.11), (s * 0.155, HY - 0.01, HZ + 0.16), 0.012, 0.0, seg=5)]
        elif horns == "goat":
            hd += [aim(f"{sid}_horn{s}", hornm, (s * 0.04, HY - 0.0, HZ + 0.09), (s * 0.07, HY + 0.06, HZ + 0.14), 0.022, 0.014, seg=6),
                   aim(f"{sid}_horn2{s}", hornm, (s * 0.07, HY + 0.06, HZ + 0.14), (s * 0.09, HY + 0.09, HZ + 0.08), 0.014, 0.004, seg=6)]
        elif horns == "antler":
            hd += [aim(f"{sid}_horn{s}", hornm, (s * 0.05, HY + 0.01, HZ + 0.09), (s * 0.08, HY + 0.05, HZ + 0.17), 0.016, 0.006, seg=5),
                   aim(f"{sid}_tine{s}", hornm, (s * 0.065, HY + 0.03, HZ + 0.13), (s * 0.11, HY + 0.03, HZ + 0.15), 0.01, 0.0, seg=5)]
    if F.get("whiskers"):
        wm = col(f"MAT_{sid}_whisker", "#F4EBD9", ramp="bone")
        for s in (1, -1):
            hd.append(aim(f"{sid}_whisk{s}", wm, (s * 0.04, HY - 0.105, HZ - 0.03), (s * 0.12, HY - 0.10, HZ - 0.02), 0.006, 0.003, seg=4))
    if F.get("stripes"):     # tiger: dark stripes over brow, back and flanks
        sm = pcol(sid, "stripes", L.get("stripes", "#2B2B2B"))
        for k, x in enumerate((-0.045, 0.0, 0.045)):
            hd.append(box(f"{sid}_brow{k}", (0.022, 0.03, 0.05), (x, HY - 0.085, HZ + 0.07), sm, rot=(30, 0, x * 250)))
        for s in (1, -1):    # stripes on the cheeks of the head
            hd.append(box(f"{sid}_hstripe{s}", (0.02, 0.05, 0.022), (s * 0.12, HY, HZ + 0.02), sm, rot=(0, s * 30, 0)))
        bands = []
        for k, y in enumerate((-0.05, -0.01)):
            bands += [box(f"{sid}_stripec{k}", (0.17 * gi, 0.03, 0.035), (0, y * ln, h + 0.055), sm),
                      box(f"{sid}_stripecl{k}", (0.02, 0.03, 0.075), (0.075 * gi, y * ln, h + 0.01), sm),
                      box(f"{sid}_stripecr{k}", (0.02, 0.03, 0.075), (-0.075 * gi, y * ln, h + 0.01), sm)]
        att(arm, "chest", *bands)
        bands = []
        for k, y in enumerate((0.035, 0.075)):
            bands += [box(f"{sid}_stripep{k}", (0.16 * gi, 0.03, 0.035), (0, y * ln, h + 0.05), sm),
                      box(f"{sid}_stripepl{k}", (0.02, 0.03, 0.07), (0.07 * gi, y * ln, h + 0.005), sm),
                      box(f"{sid}_stripepr{k}", (0.02, 0.03, 0.07), (-0.07 * gi, y * ln, h + 0.005), sm)]
        att(arm, "pelvis", *bands)
    if F.get("patch"):       # cat: orange patches
        pm = pcol(sid, "patch", L.get("patch", "#E9A15A"))
        hd.append(ball(f"{sid}_headpatch", (0.06, 0.05, 0.05), (0.05, HY + 0.02, HZ + 0.06), pm, seg=10, rings=6))
        att(arm, "pelvis", ball(f"{sid}_patch", (0.05, 0.05, 0.04), (-0.04, 0.05, h + 0.04), pm, seg=10, rings=6))
    if F.get("mane"):
        mm = pcol(sid, "mane", L.get("mane", "#2B2B2B"))
        for k in range(3):
            hd.append(ball(f"{sid}_mane{k}", (0.035, 0.04, 0.04), (0, HY + 0.06 + 0.03 * k, HZ + 0.06 - 0.04 * k), mm, seg=8, rings=5))
        att(arm, "chest", ball(f"{sid}_manen", (0.03, 0.06, 0.04), (0, -0.04 * ln, h + 0.07), mm, seg=8, rings=5))
    if F.get("beard"):
        bm = pcol(sid, "beard", L.get("beard", "#C9B48A"))
        hd.append(aim(f"{sid}_beard", bm, (0, HY - 0.12, HZ - 0.06), (0, HY - 0.12, HZ - 0.12), 0.022, 0.0, seg=6))
    if F.get("spines"):
        sp = glow(f"MAT_{sid}_spine", "verdant", (0.48, 0.92, 0.60), 2.0, 0)
        att(arm, "chest", *[cone(f"{sid}_spinec{k}", 0.018, 0.0, 0.035, (0, y, h + 0.075), sp, seg=5) for k, y in enumerate((-0.05, 0.0))])
        att(arm, "pelvis", cone(f"{sid}_spinep", 0.016, 0.0, 0.03, (0, 0.06, h + 0.07), sp, seg=5))
    # the xianxia touch
    t = F["touch"]
    if t == "browGlow":
        hd.append(box(f"{sid}_mark", (0.02, 0.012, 0.02), (0, HY - 0.098, HZ + 0.045), glow(f"MAT_{sid}_mark", "holy", (1.0, 0.89, 0.48), 4.0), rot=(0, 45, 0)))
    elif t == "browMark":
        hd.append(box(f"{sid}_mark", (0.02, 0.012, 0.02), (0, HY - 0.1, HZ + 0.045), glow(f"MAT_{sid}_mark", "verdant", (0.48, 0.92, 0.6), 4.0), rot=(0, 45, 0)))
    elif t == "noseRing":
        gm = col(f"MAT_{sid}_gold", "#E9C46A", ramp="gold")
        gm["kit_metal"] = 1
        hd.append(cone(f"{sid}_ring", 0.022, 0.022, 0.008, (0, HY - 0.125, HZ - 0.06), gm, rot=(90, 0, 0), seg=10))
        hd.append(box(f"{sid}_mark", (0.02, 0.012, 0.02), (0, HY - 0.09, HZ + 0.05), glow(f"MAT_{sid}_mark", "holy", (1.0, 0.89, 0.48), 3.0), rot=(0, 45, 0)))
    elif t in ("bell", "collarTassel"):
        red = col(f"MAT_{sid}_collar", "#BC4749", ramp="red")
        gm = col(f"MAT_{sid}_gold", "#E9C46A", ramp="gold")
        gm["kit_metal"] = 1
        ring = [(0.06 * math.cos(TAU * k / 12), HY + 0.035 + 0.05 * math.sin(TAU * k / 12), HZ - 0.085) for k in range(13)]
        hd.append(tube(f"{sid}_collar", ring, [0.012] * 13, red, seg=5, up=(0, 0, 1)))
        if t == "bell":
            hd.append(ball(f"{sid}_bell", (0.022,) * 3, (0, HY - 0.03, HZ - 0.105), gm, seg=8, rings=5))
        else:
            hd.append(aim(f"{sid}_tassel", red, (0, HY - 0.02, HZ - 0.09), (0, HY - 0.03, HZ - 0.15), 0.01, 0.02, seg=5))
            hd.append(ball(f"{sid}_knot", (0.014,) * 3, (0, HY - 0.02, HZ - 0.09), gm, seg=6, rings=4))
    elif t == "circlet":
        gm = col(f"MAT_{sid}_gold", "#E9C46A", ramp="gold")
        gm["kit_metal"] = 1
        gm["kit_priority"] = 3.0
        ring = [(0.112 * math.cos(TAU * k / 16), HY + 0.10 * math.sin(TAU * k / 16), HZ + 0.06) for k in range(17)]
        hd.append(tube(f"{sid}_circlet", ring, [0.018] * 17, gm, seg=5, up=(0, 0, 1)))
        hd.append(ball(f"{sid}_jewel", (0.02,) * 3, (0, HY - 0.105, HZ + 0.065), glow(f"MAT_{sid}_jewel", "holy", (1.0, 0.89, 0.48), 3.0), seg=6, rings=4))
    elif t == "hornTassel":
        red = col(f"MAT_{sid}_tassel", "#BC4749", ramp="red")
        hd.append(aim(f"{sid}_tassel", red, (0.08, HY + 0.08, HZ + 0.11), (0.09, HY + 0.08, HZ + 0.03), 0.008, 0.02, seg=5))
    elif t == "pearl":
        hd.append(ball(f"{sid}_pearl", (0.025,) * 3, (0, HY - 0.15, HZ - 0.07), glow(f"MAT_{sid}_pearl", "ice", (0.85, 0.97, 1.0), 4.0), seg=8, rings=5))
    elif t == "maneWisp":
        wm = glow(f"MAT_{sid}_wisp", "flame", (1.0, 0.68, 0.23), 2.5)
        hd.append(aim(f"{sid}_wisp", wm, (0, HY + 0.05, HZ + 0.09), (0, HY + 0.12, HZ + 0.14), 0.02, 0.0, seg=5))
    att(arm, "head", *hd)
    att(arm, "eyes", *cute_eyes(f"p{sid}", 0.048, HY - 0.085, HZ + 0.01, 0.036, mats))
    att(arm, "jaw", ball(f"{sid}_chin", (0.03, 0.025, 0.012), (0, HY - 0.085, HZ - 0.06), belly, seg=8, rings=5))
    # tails
    tl = F["tail"]
    t0 = (0, 0.09 * ln, h + 0.02)
    if tl == "thin":
        tm = pcol(sid, "tail", L.get("nose", L["body"]) if sid == "chuot" else L["body"])
        att(arm, "tail1", aim(f"{sid}_tail1", tm, t0, (0, 0.16 * ln, h + 0.05), 0.018, 0.014, seg=5))
        tip = [aim(f"{sid}_tail2", tm, (0, 0.16 * ln, h + 0.05), (0, 0.21 * ln, h + 0.12), 0.014, 0.008, seg=5)]
        if t == "tailglow":
            tip.append(ball(f"{sid}_tailglow", (0.02,) * 3, (0, 0.19 * ln, h + 0.125), glow(f"MAT_{sid}_tailglow", "spirit", (0.35, 0.88, 0.96), 4.0), seg=6, rings=4))
        att(arm, "tail2", *tip)
    elif tl == "tuft":
        att(arm, "tail1", aim(f"{sid}_tail1", body, t0, (0, 0.15 * ln, h + 0.03), 0.012, 0.01, seg=5))
        att(arm, "tail2", ball(f"{sid}_tuft", (0.022, 0.022, 0.03), (0, 0.16 * ln, h + 0.0), dark, seg=6, rings=4))
    elif tl == "long":
        sm = col(f"MAT_{sid}_stripes", L.get("stripes", L["body"])) if F.get("stripes") else body
        att(arm, "tail1", aim(f"{sid}_tail1", body, t0, (0, 0.15 * ln, h + 0.06), 0.022, 0.02, seg=6))
        att(arm, "tail2", aim(f"{sid}_tail2", body, (0, 0.15 * ln, h + 0.06), (0, 0.19 * ln, h + 0.12), 0.02, 0.016, seg=6),
            ball(f"{sid}_tailtip", (0.02,) * 3, (0, 0.19 * ln, h + 0.12), sm, seg=6, rings=4))
    elif tl in ("fluffy", "horse"):
        tc = pcol(sid, "tail", L.get("mane", L["body"])) if tl == "horse" else belly
        att(arm, "tail1", aim(f"{sid}_tail1", tc, t0, (0, 0.14 * ln, h + 0.0), 0.02, 0.03, seg=6))
        att(arm, "tail2", ball(f"{sid}_tail2", (0.035, 0.04, 0.05), (0, 0.15 * ln, h - 0.03 if tl == "horse" else h + 0.03), tc, seg=8, rings=5))
    elif tl == "tiger":      # a thick tail ringed in black, black tip
        sm = pcol(sid, "stripes", L.get("stripes", "#2B2B2B"))
        att(arm, "tail1", aim(f"{sid}_tail1", body, t0, (0, 0.15 * ln, h + 0.06), 0.03, 0.028, seg=8),
            ball(f"{sid}_tring1", (0.034, 0.016, 0.034), (0, 0.12 * ln, h + 0.04), sm, rot=(-35, 0, 0), seg=10, rings=5))
        att(arm, "tail2", aim(f"{sid}_tail2", body, (0, 0.15 * ln, h + 0.06), (0, 0.19 * ln, h + 0.13), 0.028, 0.024, seg=8),
            ball(f"{sid}_tring2", (0.031, 0.015, 0.031), (0, 0.17 * ln, h + 0.095), sm, rot=(-55, 0, 0), seg=10, rings=5),
            ball(f"{sid}_ttip", (0.028,) * 3, (0, 0.19 * ln, h + 0.135), sm, seg=8, rings=5))
    elif tl == "monkey":     # a long tail rising behind, curled at the top, seen over the shoulder
        att(arm, "tail1", aim(f"{sid}_tail1", body, t0, (0.05, 0.14 * ln, h + 0.16), 0.018, 0.016, seg=6))
        curl = [(0.05 + 0.04 * math.sin(a), 0.14 * ln + 0.035 * math.cos(a) - 0.035, h + 0.2 + 0.045 * math.sin(a) * 0 + 0.04 * (1 - math.cos(a)))
                for a in [TAU * k / 10 for k in range(9)]]
        att(arm, "tail2", aim(f"{sid}_tail2", body, (0.05, 0.14 * ln, h + 0.16), (0.06, 0.13 * ln, h + 0.24), 0.016, 0.014, seg=6),
            ball(f"{sid}_curl", (0.035, 0.016, 0.035), (0.075, 0.13 * ln, h + 0.27), body, rot=(0, 0, 90), seg=10, rings=6),
            ball(f"{sid}_curlin", (0.018, 0.018, 0.018), (0.075, 0.125 * ln, h + 0.27), belly, seg=8, rings=5))
    elif tl == "wag":        # dog: a thick upright tail with a pale tip, wagging in idle
        att(arm, "tail1", aim(f"{sid}_tail1", body, t0, (0, 0.14 * ln, h + 0.09), 0.024, 0.02, seg=6))
        att(arm, "tail2", aim(f"{sid}_tail2", body, (0, 0.14 * ln, h + 0.09), (0, 0.16 * ln, h + 0.15), 0.02, 0.014, seg=6),
            ball(f"{sid}_tailtip", (0.022,) * 3, (0, 0.16 * ln, h + 0.155), belly, seg=8, rings=5))
    elif tl == "curl":
        att(arm, "tail1", aim(f"{sid}_tail1", body, t0, (0, 0.13 * ln, h + 0.07), 0.016, 0.014, seg=6))
        att(arm, "tail2", ball(f"{sid}_curl", (0.012, 0.03, 0.03), (0, 0.13 * ln, h + 0.1), body, seg=10, rings=6),
            ball(f"{sid}_curl2", (0.012, 0.02, 0.02), (0, 0.11 * ln, h + 0.1), belly, seg=8, rings=5))
    elif tl == "dragon":
        att(arm, "tail1", aim(f"{sid}_tail1", body, t0, (0, 0.17 * ln, h + 0.03), 0.04, 0.03, seg=8, smooth=True))
        mm = pcol(sid, "mane", L.get("mane", "#BC4749"))
        att(arm, "tail2", aim(f"{sid}_tail2", body, (0, 0.17 * ln, h + 0.03), (0, 0.22 * ln, h + 0.09), 0.03, 0.012, seg=8, smooth=True),
            ball(f"{sid}_tailtuft", (0.03, 0.03, 0.035), (0, 0.22 * ln, h + 0.11), mm, seg=8, rings=5))
    arm.scale = (F["scale"] * PET_SCALE,) * 3
    pet_quad_clips(arm, P, wag=40.0 if tl == "wag" else 18.0)
    return arm


def pet_quad_clips(arm, P, wag=18.0):
    L = Legs(P)
    idle = []
    for i in range(4):
        breath = 0.003 * (0.5 - 0.5 * C(i, 4))
        p = L.plant(drop=breath)
        p.update({"pelvis": {"l": (0, 0, -breath)}, "head": {"r": (3 * S(i, 4, 0.6), 0, 8 * S(i, 4, -0.5))},
                  "eyes": {"s": (1, 0.2 if i == 3 else 1.0, 1)},
                  "tail1": {"r": (6 * C(i, 4), 0, wag * S(i, 4))}, "tail2": {"r": (8 * C(i, 4, -1), 0, wag * 1.3 * S(i, 4, -1.1))}})
        idle.append(p)
    walk = []
    s, lift = 0.022, 0.03
    from quadrupeds import gait
    for i in range(6):
        ph = i / 6
        legs, lifts = {}, {}
        for k, off in (("fl", 0.0), ("br", 0.0), ("fr", 0.5), ("bl", 0.5)):
            legs[k], lifts[k] = gait(ph + off, s, lift)
        bob = 0.008 * abs(C(i, 6))
        p = L.plant(drop=-bob, front=(legs["fl"], legs["fr"]), back=(legs["bl"], legs["br"]), lift=lifts)
        p.update({"pelvis": {"l": (0, 0, bob), "r": (0, 4 * S(i, 6), 0)}, "chest": {"r": (0, -4 * S(i, 6), 0)},
                  "head": {"r": (4 * abs(S(i, 6)) - 2, 0, -6 * S(i, 6))},
                  "tail1": {"r": (-6, 0, 20 * S(i, 6, 0.8))}, "tail2": {"r": (-4, 0, 26 * S(i, 6, -0.3))}})
        walk.append(p)
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, 10, True)
    arm.animation_data.action = None
    extra_quad_clips(arm, P, drop=P["h"] - 0.06, tail_wrap=70.0, head_rest=(2, 0, 55))


# ------------------------------------------------------------------ Gà (rooster)
def build_ga():
    sid = "ga"
    L = DATA[sid]["look"]
    use_collection("COL_pet_ga")
    body = pcol("ga", "body", L["body"])
    belly = pcol("ga", "belly", L["belly"])
    comb = col("MAT_ga_comb", L["comb"], ramp="red")
    beak = col("MAT_ga_beak", "#E9C46A", ramp="gold")
    tail_m = col("MAT_ga_tail", "#3E6A90", ramp="teal")
    flame = glow("MAT_ga_flame", "flame", (1.0, 0.68, 0.23), 3.0)
    leg = col("MAT_ga_leg", "#E9A15A", ramp="gold")
    mats = eye_mats("pga", (0.42, 0.35, 0.28))
    arm = armature("pet_ga", [
        ("root", (0, 0, 0), (0, 0, 0.06), None),
        ("body", (0, 0.01, 0.10), (0, 0.01, 0.24), "root"),
        ("head", (0, -0.05, 0.24), (0, -0.05, 0.38), "body"),
        ("eyes", (0, -0.12, 0.30), (0, -0.12, 0.36), "head"),
        ("tail", (0, 0.08, 0.20), (0, 0.14, 0.30), "body"),
        ("wing_l", (0.08, 0.0, 0.20), (0.09, 0.08, 0.16), "body"),
        ("wing_r", (-0.08, 0.0, 0.20), (-0.09, 0.08, 0.16), "body"),
        ("leg_l", (0.035, 0.0, 0.10), (0.035, 0.0, 0.0), "body"),
        ("leg_r", (-0.035, 0.0, 0.10), (-0.035, 0.0, 0.0), "body"),
    ])
    att(arm, "body", ball("ga_body", (0.09, 0.1, 0.085), (0, 0.01, 0.17), body),
        ball("ga_breast", (0.07, 0.05, 0.065), (0, -0.05, 0.16), belly))
    att(arm, "head", ball("ga_head", (0.075, 0.07, 0.075), (0, -0.06, 0.30), body),
        aim("ga_beak", beak, (0, -0.12, 0.30), (0, -0.165, 0.29), 0.024, 0.0, seg=6),
        ball("ga_wattle", (0.016, 0.014, 0.025), (0, -0.13, 0.26), comb, seg=6, rings=4),
        *[ball(f"ga_comb{k}", (0.016, 0.03, 0.03), (0, -0.07 + 0.03 * k, 0.375 - 0.008 * abs(k)), comb, seg=8, rings=5) for k in (-1, 0, 1)],
        ball("ga_combglow", (0.012,) * 3, (0, -0.075, 0.41), flame, seg=6, rings=4))
    att(arm, "eyes", *cute_eyes("pga", 0.04, -0.115, 0.31, 0.03, mats))
    att(arm, "tail", *[aim(f"ga_tail{k}", tail_m, (0, 0.08, 0.19), (x, 0.17, 0.33 - abs(x)), 0.03, 0.006, seg=6) for k, x in enumerate((-0.04, 0.0, 0.04))],
        ball("ga_tailglow", (0.014,) * 3, (0, 0.17, 0.335), flame, seg=6, rings=4))
    for s, b in ((1, "wing_l"), (-1, "wing_r")):
        att(arm, b, ball(f"ga_{b}", (0.025, 0.07, 0.05), (s * 0.085, 0.03, 0.18), belly, seg=8, rings=5))
    for s, b in ((1, "leg_l"), (-1, "leg_r")):
        att(arm, b, aim(f"ga_{b}", leg, (s * 0.035, 0.0, 0.10), (s * 0.035, 0.0, 0.015), 0.012, 0.012, seg=5),
            *[aim(f"ga_{b}toe{k}", leg, (s * 0.035, 0.0, 0.01), (s * 0.035 + (k - 1) * 0.02, -0.035, 0.006), 0.01, 0.004, seg=4) for k in range(3)])
    idle = [{"body": {"l": (0, 0, 0.003 * S(i, 4))}, "head": {"r": (10 * max(0.0, S(i, 4)), 0, 6 * S(i, 4, 1))},
             "tail": {"r": (0, 0, 8 * S(i, 4))}, "eyes": {"s": (1, 0.2 if i == 3 else 1.0, 1)}} for i in range(4)]
    walk = []
    for i in range(6):
        s = S(i, 6)
        walk.append({"body": {"l": (0, 0, 0.008 * abs(s)), "r": (0, 0, 6 * s)},
                     "head": {"l": (0, -0.012 * C(i, 6), 0)},
                     "leg_l": {"r": (-24 * s, 0, 0), "l": (0, 0, 0.015 * max(0.0, s) - 0.008 * abs(s))},
                     "leg_r": {"r": (24 * s, 0, 0), "l": (0, 0, 0.015 * max(0.0, -s) - 0.008 * abs(s))},
                     "tail": {"r": (6 * s, 0, 0)}})
    happy = [{"root": {"r": (0, 0, 90 * i), "l": (0, 0, z)}, "eyes": {"s": (1, 0.35, 1)}, "head": {"r": (-12, 0, 0)},
              "wing_l": {"r": (0, -60 - 20 * S(i, 4), 0)}, "wing_r": {"r": (0, 60 + 20 * S(i, 4), 0)}}
             for i, z in enumerate((0.0, 0.04, 0.05, 0.015))]
    sleep = [{"body": {"l": (0, 0, -0.07), "s": (1.04, 1.0, 1.0 + 0.02 * S(i, 4))},
              "leg_l": {"s": 0.3, "l": (0, 0, 0.07)}, "leg_r": {"s": 0.3, "l": (0, 0, 0.07)},
              "head": {"r": (40, 0, 40), "l": (0, 0.03, -0.04)}, "eyes": {"s": (1, 0.12, 1)}} for i in range(4)]
    arm.scale = (PET_SCALE,) * 3
    write4(arm, idle, walk, happy, sleep)
    return arm


# ------------------------------------------------------------------ Rắn (snake)
def build_ran():
    sid = "ran"
    L = DATA[sid]["look"]
    use_collection("COL_pet_ran")
    body = pcol("ran", "body", L["body"])
    belly = pcol("ran", "belly", L["belly"])
    tongue = col("MAT_ran_tongue", "#BC4749", ramp="red")
    dot = glow("MAT_ran_dot_mark", "verdant", (0.48, 0.92, 0.60), 3.0, 0)
    mats = eye_mats("pran", (0.42, 0.35, 0.28))
    N, SEG = 5, 0.05
    bones = [("root", (0, 0, 0), (0, 0, 0.05), None)]
    for k in range(1, N + 1):
        bones.append((f"n{k}", (0, -0.02, 0.05 + (k - 1) * SEG), (0, -0.02, 0.05 + k * SEG), "root" if k == 1 else f"n{k - 1}"))
    top = 0.05 + N * SEG
    bones += [("head", (0, -0.02, top), (0, -0.02, top + 0.1), f"n{N}"),
              ("eyes", (0, -0.09, top + 0.03), (0, -0.09, top + 0.08), "head"),
              ("tongue", (0, -0.12, top + 0.01), (0, -0.17, top + 0.01), "head")]
    arm = armature("pet_ran", bones)
    ring = [(0.07 * math.sin(math.radians(-60 + 26 * k)), -0.07 * math.cos(math.radians(-60 + 26 * k)) + 0.02, 0.035)
            for k in range(13)]
    att(arm, "root", tube("ran_coil", ring, [0.045 - 0.0025 * k for k in range(13)], body, seg=10, up=(0, 0, 1)))
    pts = [(0, -0.02, 0.03)] + [(0, -0.02, 0.05 + k * SEG) for k in range(1, N + 1)]
    tb = tube("ran_body", pts, [0.045] * len(pts), body, seg=10, up=(0, -1, 0))
    skin(tb, arm, [f"n{k}" for k in range(1, N + 1)] + ["root"], power=4)
    for k in range(1, N + 1):
        z = 0.05 + (k - 0.5) * SEG
        att(arm, f"n{k}", ball(f"ran_belly{k}", (0.025, 0.012, 0.022), (0, -0.052, z), belly, seg=8, rings=5),
            ball(f"ran_dot{k}", (0.01,) * 3, (0, 0.012, z), dot, seg=5, rings=4))
    att(arm, "head", ball("ran_head", (0.095, 0.10, 0.075), (0, -0.06, top + 0.045), body),
        ball("ran_jaw", (0.07, 0.06, 0.03), (0, -0.085, top + 0.0), belly, seg=10, rings=5))
    att(arm, "eyes", *cute_eyes("pran", 0.05, -0.13, top + 0.065, 0.036, mats))
    att(arm, "tongue", aim("ran_tongue", tongue, (0, -0.12, top + 0.01), (0, -0.16, top + 0.0), 0.008, 0.004, seg=4))

    def sway(i, n, amp, extra=None):
        out, prev = {}, 0.0
        for k in range(1, N + 1):
            th = amp * math.sin(TAU * i / n - k * 1.1)
            out[f"n{k}"] = {"r": (0, th - prev, 0)}
            prev = th
        out["head"] = {"r": (0, -prev, 0)}
        out.update(extra or {})
        return out
    idle = [sway(i, 4, 14, {"tongue": {"s": (1, 1.0 if i == 1 else 0.2, 1)}, "eyes": {"s": (1, 0.2 if i == 3 else 1, 1)}}) for i in range(4)]
    walk = [sway(i, 6, 22, {"root": {"r": (0, 0, 6 * S(i, 6))}, "tongue": {"s": (1, 0.2, 1)}}) for i in range(6)]
    happy = [sway(i, 4, 20, {"root": {"r": (0, 0, 90 * i), "l": (0, 0, z)}, "eyes": {"s": (1, 0.35, 1)},
                             "tongue": {"s": (1, 1.0, 1)}}) for i, z in enumerate((0.0, 0.03, 0.04, 0.01))]
    sleep = []
    for i in range(4):
        p = {f"n{k}": {"r": (0, 0, 0), "s": 1.0} for k in range(1, N + 1)}
        p["n1"] = {"r": (-14, 0, 0)}
        p["n2"] = {"r": (-10, 0, 0), "s": 0.85}
        p["n3"] = {"r": (8, 0, 0), "s": 0.85}
        p["n4"] = {"s": 0.85}
        p["head"] = {"r": (56, 0, 14)}
        p["root"] = {"l": (0, 0, 0.002 * S(i, 4))}
        p["eyes"] = {"s": (1, 0.12, 1)}
        p["tongue"] = {"s": (1, 0.2, 1)}
        sleep.append(p)
    arm.scale = (PET_SCALE,) * 3
    write4(arm, idle, walk, happy, sleep)
    return arm


def write4(arm, idle, walk, happy, sleep):
    clip(arm, "idle", idle, 6, True)
    clip(arm, "walk", walk, 10, True)
    clip(arm, "happy", happy, 8, True)
    clip(arm, "sleep", sleep, 4, True)
    arm.animation_data.action = None


def _builder(sid):
    if sid == "ga":
        return build_ga
    if sid == "ran":
        return build_ran
    return lambda: build_quad_pet(sid)


PETS = {f"pet_{sid}": (DATA[sid]["name_vi"], 48, _builder(sid)) for sid in DATA}
