"""Where each weapon type sits in each clip (pure Python, no bpy: also read by build.py).

A *carry spec* says how a weapon is attached for one frame of one clip:

    at     "r"    right fist  (SOCKET_weapon_r)
           "l"    left fist   (SOCKET_weapon_l)
           "back" slung on the back (SOCKET_back)
    rot    (x, y, z) degrees, XYZ Euler, in the socket's own frame, applied to the weapon
    loc    (x, y, z) metres in the socket's frame (z slides the weapon along its own length)
    scale  uniform scale of the weapon about its grip
    grip   model z the hand holds (slides the weapon along its own length)
    off    (x, y, z) metres in the character's frame added to the socket position (aim mode)
    face   direction (character frame) the weapon's broad (-Y) side should face (aim mode)
    xdir   direction its local +X should take (bows: the way the belly bulges = the shot)
    aim    optional (dx, dy, dz) direction in the character's own frame (x = its left,
           -y = forward, z = up). With `aim` the weapon follows the socket's POSITION but is
           pointed along that direction (`roll` degrees about it) instead of the hand's
           orientation: used where the hand's own twist is wrong (die, fly, back carry).

A clip entry is one spec, a list with one spec per frame, or a list of (frame, spec) keys that
are interpolated. Frames are 0 based; `hit` (strike) is frame 3 of slash / cast / shoot.
"""
from __future__ import annotations

import copy
import math

BASE = dict(at="r", rot=(0.0, 0.0, 0.0), loc=(0.0, 0.0, 0.0), scale=1.0, aim=None, roll=0.0,
            off=(0.0, 0.0, 0.0), face=None, xdir=None, grip=0.0)


def S(**kw):
    d = copy.deepcopy(BASE)
    d.update(kw)
    return d


def _lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def _mix(a, b, t):
    out = dict(a)
    for k in ("rot", "loc", "off"):
        out[k] = _lerp(a[k], b[k], t)
    out["scale"] = a["scale"] + (b["scale"] - a["scale"]) * t
    out["grip"] = a["grip"] + (b["grip"] - a["grip"]) * t
    out["roll"] = a["roll"] + (b["roll"] - a["roll"]) * t
    for k in ("aim", "face", "xdir"):
        if a[k] is not None and b[k] is not None:
            out[k] = _lerp(a[k], b[k], t)
        elif b[k] is not None and t >= 0.5:
            out[k] = b[k]
    return out


def keys(pairs, n):
    """[(frame, spec), ...] -> n specs, linear between the keys."""
    pairs = sorted(pairs, key=lambda p: p[0])
    out = []
    for i in range(n):
        if i <= pairs[0][0]:
            out.append(pairs[0][1])
        elif i >= pairs[-1][0]:
            out.append(pairs[-1][1])
        else:
            for (f0, s0), (f1, s1) in zip(pairs, pairs[1:]):
                if f0 <= i <= f1:
                    out.append(_mix(s0, s1, (i - f0) / (f1 - f0)) if s0["at"] == s1["at"] else s0)
                    break
    return out


def expand(entry, n):
    if isinstance(entry, dict):
        return [entry] * n
    if entry and isinstance(entry[0], tuple):
        return keys(entry, n)
    assert len(entry) == n, (len(entry), n)
    return list(entry)


# --------------------------------------------------------------------------- tables
# Filled in below; see README.md for the rule table.
HAND = {}      # type -> {clip: entry}
FRAMES = {"idle": 4, "walk": 8, "slash": 6, "cast": 6, "shoot": 6, "hit": 3, "die": 6,
          "meditate": 4, "fly": 4, "dodge": 4}

# which clips a type holds in hand (everything else = on the back)
IN_HAND = {
    "kiem": {"idle", "walk", "slash", "cast", "hit", "die", "dodge"},
    "dao": {"idle", "walk", "slash", "cast", "hit", "die", "dodge"},
    "chuy": {"idle", "walk", "slash", "cast", "hit", "die", "dodge"},
    "thuong": {"idle", "walk", "slash", "cast", "hit", "die", "dodge"},
    "truong": {"idle", "walk", "cast", "slash", "hit", "die", "dodge"},
    "phien": {"idle", "walk", "cast", "slash", "hit", "die", "dodge"},
    "ho_lo": {"idle", "walk", "cast", "slash", "hit", "die", "dodge"},
    "cung": {"idle", "walk", "shoot", "hit", "die", "dodge"},          # left hand
}


def weapon_type(wid: str) -> str:
    return wid.rsplit("_", 1)[0]


def plan(wid: str, clip: str, n: int, direction: str | None = None) -> list[dict]:
    """The n carry specs of weapon `wid` in `clip`."""
    t = weapon_type(wid)
    table = TABLE[t]
    entry = table.get(clip)
    if entry is None:
        entry = table["_default"]
    out = expand(entry, n)
    res = []
    for s in out:
        d = dict(copy.deepcopy(BASE), **s)
        d["scale"] *= TYPE_SCALE.get(t, 1.0)
        res.append(d)
    return res


TABLE: dict[str, dict] = {}

# the model is shrunk a little for the 64 px frame (the character is ~36 px tall)
TYPE_SCALE = {"kiem": 0.85, "dao": 0.85, "chuy": 0.85, "phien": 1.3}
# types whose hand may slide along the shaft to keep them inside the frame; the rest shrink
SLIDE = {"thuong", "truong"}



# ---------------------------------------------------------------- helpers for the tables
def A(aim, at="r", **kw):
    return S(at=at, aim=aim, **kw)


def T(rot=(0, 0, 0), at="r", **kw):
    return S(at=at, rot=rot, **kw)


BACK = S(at="back")


def melee_table(carry, slash, cast, die, back=BACK):
    return {"idle": carry, "walk": carry, "hit": carry, "dodge": carry, "slash": slash,
            "cast": cast, "die": die, "shoot": back, "fly": back, "meditate": back}


def lying(carry, side=-1.0):
    """die: the weapon drops with the hand and ends lying on the ground beside the body."""
    return [(0, carry), (1, A((-0.7, -0.4, 0.0))), (2, A((-0.5, -0.8, 0.0))),
            (3, A((side * 0.3, -1.0, 0.1))), (5, A((side * 0.2, -1.0, 0.0)))]


# ---------------------------------------------------------------- the tables
SWORD_CARRY = T((0, 18, 0))
SWORD_CAST = [(0, A((-0.55, -0.1, 0.83))), (2, A((-0.5, -0.2, 0.84))), (3, A((-0.1, -1.0, 0.15))),
              (4, A((-0.1, -1.0, 0.1))), (5, A((-0.43, -0.74, -0.52)))]
for _t in ("kiem", "dao"):
    TABLE[_t] = melee_table(SWORD_CARRY, S(), SWORD_CAST, lying(SWORD_CARRY))

HAMMER_CARRY = A((-0.5, -0.2, 0.85))
TABLE["chuy"] = melee_table(HAMMER_CARRY, S(),
                            [(0, A((-0.55, -0.1, 0.83))), (2, A((-0.5, -0.3, 0.8))), (3, A((-0.1, -1.0, 0.3))),
                             (4, A((-0.1, -1.0, 0.1))), (5, HAMMER_CARRY)], lying(HAMMER_CARRY))

SPEAR_CARRY = A((-0.3, -0.2, 0.93), grip=0.15)
TABLE["thuong"] = melee_table(
    SPEAR_CARRY,
    [(0, A((-0.3, -0.3, 0.9), grip=0.3)), (2, A((-0.2, -0.5, 0.8), grip=0.45)),
     (3, A((-0.15, -0.85, 0.5), grip=0.45)), (4, A((-0.15, -0.8, 0.5), grip=0.4)),
     (5, SPEAR_CARRY)],
    [(0, A((-0.3, -0.3, 0.9), grip=0.3)), (2, A((-0.2, -0.5, 0.8), grip=0.45)),
     (3, A((-0.15, -0.85, 0.5), grip=0.45)), (5, SPEAR_CARRY)],
    lying(SPEAR_CARRY))

STAFF_CARRY = A((-0.35, -0.15, 0.92))
TABLE["truong"] = melee_table(
    STAFF_CARRY, S(grip=0.2),
    [(0, A((-0.55, -0.1, 0.83))), (2, A((-0.5, -0.2, 0.84))), (3, A((-0.1, -0.9, 0.72))),
     (4, A((-0.1, -0.9, 0.72))), (5, STAFF_CARRY)], lying(STAFF_CARRY))

FAN_BACK = A((-0.5, 0.25, 0.8), at="back", off=(-0.2, 0.0, -0.12), face=(-0.7, 0.7, 0.0))
FAN_FACE = (-0.8, -0.6, 0.0)
FAN_CARRY = A((-0.4, -0.3, 0.85), face=FAN_FACE)
TABLE["phien"] = melee_table(
    FAN_CARRY, S(),
    [(0, A((-0.6, -0.3, 0.75), face=FAN_FACE)), (2, A((-0.4, -0.6, 0.7), face=FAN_FACE)),
     (3, A((-0.1, -1.0, 0.55), face=(-0.6, -0.4, 0.7))), (4, A((-0.1, -1.0, 0.55), face=(-0.6, -0.4, 0.7))),
     (5, FAN_CARRY)],
    lying(FAN_CARRY), back=FAN_BACK)

GOURD_CARRY = A((0, 0, 1))
TABLE["ho_lo"] = melee_table(
    GOURD_CARRY, S(),
    [(0, A((-0.3, -0.2, 1.0))), (2, A((-0.3, -0.3, 1.0))), (3, A((-0.1, -0.9, 0.75))), (4, A((-0.1, -0.9, 0.7))),
     (5, GOURD_CARRY)], lying(GOURD_CARRY),
    back=A((0.0, 0.0, 1.0), at="back", off=(-0.2, 0.05, -0.2)))

BOW_CARRY = A((0.1, -0.1, 1.0), at="l", xdir=(0, -1, 0))
TABLE["cung"] = {"idle": BOW_CARRY, "walk": BOW_CARRY, "hit": BOW_CARRY, "dodge": BOW_CARRY,
                 "shoot": A((0.0, -0.05, 1.0), at="l", xdir=(0, -1, 0)),
                 "die": [(0, BOW_CARRY), (1, A((0.4, -0.6, 0.6), at="l", xdir=(0, -1, 0))),
                         (2, A((0.6, -0.5, 0.2), at="l", xdir=(0, -1, 0))),
                         (3, A((1.0, -0.2, 0.0), at="l", xdir=(0, 0, 1))),
                         (5, A((1.0, -0.2, 0.0), at="l", xdir=(0, 0, 1)))],
                 "slash": BACK, "cast": BACK, "fly": BACK, "meditate": BACK}


# ---------------------------------------------------------------- WEAPONS_C: the six "ky binh"
# (art/src/weapons_c). Extra spec key used only here: `pose` = which pose meshes of the model
# are shown on that frame (whip: coil / arc / lash; darts: hand / fly). Thrown weapons (am_khi,
# luan) leave the hand on the strike frame (3) and frame 4 of `shoot`, and are back in the hand
# on frame 5 (a fresh fan of darts; the chakram caught on its return).
IN_HAND.update({
    "kich": {"idle", "walk", "slash", "cast", "hit", "die", "dodge"},
    "phu": {"idle", "walk", "slash", "cast", "hit", "die", "dodge"},
    "roi": {"idle", "walk", "slash", "cast", "hit", "die", "dodge"},
    "am_khi": {"idle", "walk", "shoot", "cast", "slash", "hit", "die", "dodge"},
    "luan": {"idle", "walk", "shoot", "cast", "slash", "hit", "die", "dodge"},
    "cam": {"cast"},                                   # held in front; on the back otherwise
})
TYPE_SCALE.update({"kich": 0.84, "phu": 0.82, "roi": 1.0, "am_khi": 1.15, "luan": 1.1, "cam": 0.9})
SLIDE.add("kich")

F45 = (-0.7, -0.7, 0.0)          # broad side half toward the viewer in every facing

# halberd: carried like the spear, crescent turned half to the viewer; slash = a wide sweep
# (raised over the right shoulder -> around the right side -> level across the front -> past the left)
KICH_CARRY = A((-0.3, -0.2, 0.93), grip=0.15, face=F45)
TABLE["kich"] = melee_table(
    KICH_CARRY,
    [(0, A((-0.35, -0.2, 0.9), grip=0.25, face=F45)), (1, A((-0.55, 0.45, 0.7), grip=0.35)),
     (2, A((-0.85, 0.05, 0.5), grip=0.4)), (3, A((-0.3, -0.93, 0.18), grip=0.42)),
     (4, A((0.45, -0.85, -0.05), grip=0.38)), (5, KICH_CARRY)],
    [(0, A((-0.3, -0.3, 0.9), grip=0.3, face=F45)), (2, A((-0.2, -0.5, 0.8), grip=0.45, face=F45)),
     (3, A((-0.15, -0.85, 0.5), grip=0.45)), (5, KICH_CARRY)],
    lying(KICH_CARRY))

# battle axe: carried like the mace, edge forward-out; slash = a heavy overhead chop: lifted,
# held high behind the head, driven down through the strike, still low on the recovery
AXE_X = (-0.55, -0.83, 0.0)
AXE_CARRY = A((-0.5, -0.2, 0.85), xdir=AXE_X)
TABLE["phu"] = melee_table(
    AXE_CARRY,
    [A((-0.45, 0.3, 0.84), xdir=(0, -1, 0.3)),
     A((-0.3, 0.68, 0.67), xdir=(0, -0.7, 0.7)),
     A((-0.2, 0.15, 0.97), xdir=(0, -1, 0.1)),
     A((-0.15, -0.95, 0.1), xdir=(0, 0, -1)),
     A((-0.1, -0.55, -0.8), xdir=(0, 0.8, -0.55)),
     A((-0.35, -0.5, 0.2), xdir=(0, -0.4, -0.9))],
    [(0, A((-0.55, -0.1, 0.83), xdir=AXE_X)), (2, A((-0.5, -0.3, 0.8), xdir=AXE_X)),
     (3, A((-0.1, -1.0, 0.3), xdir=(0, 0, -1))), (4, A((-0.1, -1.0, 0.1), xdir=(0, 0, -1))), (5, AXE_CARRY)],
    lying(AXE_CARRY))

# whip: coiled in the right hand; slash = swung back over the head (arc), lashed straight out
# on the strike, still out (dipping) on frame 4, coiled again on the recovery
ROI_CARRY = A((-0.25, -0.25, 0.93), xdir=(-0.6, 0.8, 0.0), pose="coil")
ROI_BACK = A((0.0, 0.0, 1.0), at="back", off=(-0.2, 0.05, -0.2), xdir=(0, 1, 0), pose="coil")
TABLE["roi"] = melee_table(
    ROI_CARRY,
    [ROI_CARRY,
     A((-0.3, 0.45, 0.84), xdir=(0, -1, 0.2), pose="arc"),
     A((-0.25, 0.1, 0.96), xdir=(0, -1, 0.0), pose="arc"),
     A((-0.12, -0.99, 0.08), xdir=(0, 0, 1), pose="lash"),
     A((-0.08, -0.96, -0.22), xdir=(0, 0, 1), pose="lash"),
     ROI_CARRY],
    [(0, A((-0.55, -0.1, 0.83), xdir=(0, -1, 0), pose="coil")), (2, A((-0.5, -0.2, 0.84), xdir=(0, -1, 0), pose="coil")),
     (3, A((-0.1, -1.0, 0.15), xdir=(0, 0, 1), pose="lash")), (4, A((-0.1, -1.0, 0.1), xdir=(0, 0, 1), pose="lash")),
     (5, ROI_CARRY)],
    lying(ROI_CARRY), back=ROI_BACK)

# hidden darts: a fan held up between the fingers; shoot = drawn back past the ear, the fan
# leaves the hand on the strike (pose "fly": blades side by side, flying forward), farther on
# frame 4, a fresh fan in the hand on frame 5
DART_FACE = (-0.8, -0.6, 0.0)
DART_CARRY = A((-0.4, -0.3, 0.85), face=DART_FACE, pose="hand")
DART_BACK = A((0.0, 0.0, 1.0), at="back", off=(-0.2, 0.05, -0.2), face=(-1, 0, 0), pose="hand")
TABLE["am_khi"] = {
    "idle": DART_CARRY, "walk": DART_CARRY, "hit": DART_CARRY, "dodge": DART_CARRY,
    "slash": DART_CARRY, "cast": DART_CARRY,
    "shoot": [DART_CARRY,
              A((-0.45, 0.55, 0.7), face=DART_FACE, pose="hand"),
              A((-0.35, 0.3, 0.88), face=DART_FACE, pose="hand"),
              A((0.0, -1.0, 0.04), xdir=(0, 0, 1), off=(0.0, -0.26, 0.04), pose="fly"),
              A((0.0, -1.0, 0.0), xdir=(0, 0, 1), off=(0.0, -0.5, 0.06), pose="fly"),
              DART_CARRY],
    "die": lying(DART_CARRY), "fly": DART_BACK, "meditate": DART_BACK}

# chakram: held by its wrapped grip at the side; shoot = drawn back, thrown spinning forward
# (the grip spins about the wheel's centre, `grip` = its radius), caught again on frame 5
LUAN_CARRY = A((-0.35, -0.2, 0.9), face=F45)
LUAN_BACK = A((0.0, 0.1, 1.0), at="back", off=(-0.05, 0.08, -0.05), face=(0, 1, 0))
TABLE["luan"] = {
    "idle": LUAN_CARRY, "walk": LUAN_CARRY, "hit": LUAN_CARRY, "dodge": LUAN_CARRY,
    "slash": LUAN_CARRY, "cast": LUAN_CARRY,
    "shoot": [LUAN_CARRY,
              A((-0.5, 0.6, 0.6), face=F45),
              A((-0.4, 0.3, 0.86), face=F45),
              A((0.0, 0.0, 1.0), face=F45, off=(0.0, -0.3, 0.06), grip=0.17, rot=(0, 50, 0)),
              A((0.0, 0.0, 1.0), face=F45, off=(0.0, -0.55, 0.1), grip=0.17, rot=(0, 115, 0)),
              LUAN_CARRY],
    "die": lying(LUAN_CARRY), "fly": LUAN_BACK, "meditate": LUAN_BACK}

# zither: slung across the back; cast = brought round in front of the chest (following the
# body, not the hand), held level and angled so the strings face the viewer, plucked: it
# bobs on the wind-up and the strike frame is a hard strum (tilted, dipped)
CAM_BACK = A((-0.6, 0.12, 0.79), at="back", off=(0.0, 0.03, -0.02), face=(0.0, 1.0, 0.0))
CAM_FRONT = dict(at="back", aim=(0.75, -0.6, -0.1), face=(-0.4, -0.6, 0.7))
TABLE["cam"] = {
    "idle": CAM_BACK, "walk": CAM_BACK, "hit": CAM_BACK, "dodge": CAM_BACK, "slash": CAM_BACK,
    "shoot": CAM_BACK, "die": CAM_BACK, "fly": CAM_BACK, "meditate": CAM_BACK,
    "cast": [S(**dict(CAM_FRONT, off=(-0.05, -0.27, 0.0))),
             S(**dict(CAM_FRONT, off=(-0.05, -0.28, 0.03))),
             S(**dict(CAM_FRONT, off=(-0.05, -0.28, 0.04))),
             S(**dict(CAM_FRONT, off=(-0.05, -0.28, -0.01), roll=-12.0)),
             S(**dict(CAM_FRONT, off=(-0.05, -0.27, 0.0), roll=-6.0)),
             S(**dict(CAM_FRONT, off=(-0.05, -0.27, 0.0)))],
}
