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
