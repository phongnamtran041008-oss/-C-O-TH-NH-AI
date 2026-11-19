"""NPC clips: idle 4 (with a characteristic gesture), walk 8, talk 4 (runs inside Blender).
Same conventions as ../v2/v2_clips.py. `install(npc_id)` puts this NPC's three clips in
../clips.py so build_actions makes them."""
from __future__ import annotations

import math

import clips as C
import rig as R
import v2_clips as P
from ld_clips import AZ, FOOT_FLAT, V, setrot
from npc_looks import STYLE


def stance(st) -> dict:
    """A calm civilian stance: feet a little apart, arms down; the old stoop forward and look
    up a little; the hands per character (clasped, behind the back, fists, scroll, staff)."""
    stoop = st.get("stoop", 0)
    p = {
        "neck": {},
        "hips": {"loc": V(0, 0.0, -0.015 - 0.0015 * max(0, stoop)), "rot": R.euler(z=-6)},
        "spine": {"rot": R.euler(x=stoop * 0.5, z=2)},
        "chest": {"rot": R.euler(x=stoop * 0.5, z=3)},
        "head": {"rot": R.euler(x=-6 - stoop * 0.9, z=3)},
        "upper_arm.L": {"aim": V(0.22, 0.02, -1)}, "forearm.L": {"aim": V(0.12, -0.25, -1)},
        "upper_arm.R": {"aim": V(-0.22, 0.02, -1)}, "forearm.R": {"aim": V(-0.12, -0.25, -1)},
        "hand.R": {}, "hand.L": {},
        "legs": {"L": {"ankle": V(0.075, -0.02, AZ), "pole": V(0.2, -1, 0), "foot": V(0.2, -0.93, -0.36)},
                 "R": {"ankle": V(-0.075, 0.02, AZ), "pole": V(-0.2, -1, 0), "foot": V(-0.2, -0.93, -0.36)}},
        "wind": V(0, 0, 0), "wing": (0, 0, 0, 0), "qi_angle": 0.0,
    }
    hands = st.get("hands")
    if st.get("wide"):
        p["legs"]["L"]["ankle"].x, p["legs"]["R"]["ankle"].x = 0.1, -0.1
        p["upper_arm.L"]["aim"], p["upper_arm.R"]["aim"] = V(0.34, 0.02, -1), V(-0.34, 0.02, -1)
    if hands == "clasp":           # hands together in front of the belly
        p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(0.1, -0.35, -1), V(-0.7, -0.6, -0.2)
        p["upper_arm.R"]["aim"], p["forearm.R"]["aim"] = V(-0.1, -0.35, -1), V(0.7, -0.6, -0.2)
    elif hands == "behind":        # hands clasped behind the back
        p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(0.25, 0.45, -1), V(-0.6, 0.7, -0.3)
        p["upper_arm.R"]["aim"], p["forearm.R"]["aim"] = V(-0.25, 0.45, -1), V(0.6, 0.7, -0.3)
    elif hands == "scroll":        # the scroll held at the chest in the left hand
        p["upper_arm.L"]["aim"], p["forearm.L"]["aim"] = V(0.15, -0.35, -1), V(-0.45, -0.75, 0.5)
        p["hand.L"] = {"rot": R.euler(z=-20)}
    elif hands == "staff":         # the staff stands on the ground beside the right foot
        p["upper_arm.R"]["aim"], p["forearm.R"]["aim"] = V(-0.30, -0.35, -1), V(-0.15, -0.9, 0.1)
        p["hand.R"] = {"blade": V(0.0, -0.08, 1.0)}
    return p


def idle(st):
    g = st.get("idle")

    def fn(i, n):
        p = stance(st)
        b = math.cos(math.tau * i / n)
        sn = math.sin(math.tau * i / n)
        stoop = st.get("stoop", 0)
        p["hips"]["loc"] = p["hips"]["loc"] + V(0, 0, 0.003 * b)
        setrot(p, "chest", R.euler(x=stoop * 0.5 - 1.2 * b, z=3))
        if g == "nod":                                  # the shopkeeper nods, smiling at you
            setrot(p, "head", R.euler(x=-6 + [0, 7, 2, 0][i], z=3))
        elif g == "shift":                              # the smith shifts his weight
            p["hips"]["loc"] = V(0.022 * sn, 0, -0.018 - 0.006 * abs(sn))
            setrot(p, "hips", R.euler(z=-6, y=-4 * sn))
            setrot(p, "chest", R.euler(z=3, y=3 * sn))
        elif g == "bounce":                             # the guide sways, cheerful
            setrot(p, "hips", R.euler(z=-6 + 6 * sn, y=3 * sn))
            setrot(p, "head", R.euler(x=-8, y=6 * sn, z=3))
            p["hips"]["loc"] = V(0, 0, -0.012 + 0.008 * abs(sn))
        elif g == "tilt":                               # the librarian tilts her head, reading
            setrot(p, "head", R.euler(x=-2 + 3 * b, y=6, z=8))
        elif g == "beard":                              # the elder strokes his beard
            stroke = [0.0, 0.5, 1.0, 0.5][i]
            p["upper_arm.L"]["aim"] = V(0.10, -0.55, -0.75)
            p["forearm.L"]["aim"] = V(-0.35, -0.75, 0.55 - 0.45 * stroke)
            p["hand.L"] = {"rot": R.euler(x=-20)}
        elif g == "bob":                                # the old fisher rocks a little
            p["hips"]["loc"] = p["hips"]["loc"] + V(0, 0, 0.006 * b)
            setrot(p, "spine", R.euler(x=stoop * 0.5 + 2 * b))
        elif g == "sway":                               # the alchemist sways, thinking
            setrot(p, "hips", R.euler(z=-6 + 4 * sn))
            setrot(p, "head", R.euler(x=-6 - stoop * 0.9, z=3 - 6 * sn))
        p["wind"] = V(0, 0.06 * sn, 0)
        return p
    return fn


def walk(st):
    def fn(i, n):
        p = P.walk(i, n)
        base = stance(st)
        stoop = st.get("stoop", 0)
        S = 0.085 if stoop < 8 else 0.065                  # the old walk with a shorter step
        ph = i / n
        for s, off in (("L", 0.0), ("R", 0.5)):
            q = (ph + off) % 1.0
            leg = p["legs"][s]
            if q < 0.5:
                leg["ankle"].y = -S + 2 * S * (q / 0.5)
            else:
                t = (q - 0.5) / 0.5
                leg["ankle"].y = S - 2 * S * (t * t * (3 - 2 * t))
        setrot(p, "spine", R.euler(x=3 + stoop * 0.5))
        setrot(p, "chest", R.euler(x=2 + stoop * 0.5, z=6 * math.cos(math.tau * ph)))
        setrot(p, "head", R.euler(x=-6 - stoop * 0.9))
        p["hand.R"] = {}
        hands = st.get("hands")
        if hands in ("clasp", "behind", "scroll", "staff"):
            for key in ("upper_arm.L", "forearm.L", "hand.L") if hands != "staff" else ():
                p[key] = base[key]
            if hands in ("clasp", "behind"):
                for key in ("upper_arm.R", "forearm.R"):
                    p[key] = base[key]
            if hands == "staff":                         # the staff swings forward with each step
                c = math.cos(math.tau * ph)
                p["upper_arm.R"] = {"aim": V(-0.30, -0.45 - 0.2 * c, -1)}
                p["forearm.R"] = {"aim": V(-0.15, -0.95, 0.1)}
                p["hand.R"] = {"blade": V(0.0, -0.25 - 0.15 * c, 1.0)}
        p["wing"] = (0, 0, 0, 0)
        return p
    return fn


def talk(st):
    """A gentle gesture while speaking: the right hand opens, palm up, rising and falling;
    the head nods with the words. Hands that hold something keep holding it."""
    def fn(i, n):
        p = stance(st)
        k = [0.0, 1.0, 0.6, 0.2][i]
        stoop = st.get("stoop", 0)
        setrot(p, "head", R.euler(x=-6 - stoop * 0.9 + [0, 5, 0, 3][i], z=3 + [0, 2, -2, 0][i]))
        if st.get("hands") == "staff":                   # the elder gestures with the free left hand
            p["upper_arm.L"] = {"aim": V(0.25, -0.55, -0.75)}
            p["forearm.L"] = {"aim": V(0.35, -0.85, 0.05 + 0.35 * k)}
            p["hand.L"] = {"rot": R.euler(x=-50)}
        else:
            p["upper_arm.R"] = {"aim": V(-0.25, -0.55, -0.75)}
            p["forearm.R"] = {"aim": V(-0.35, -0.85, 0.05 + 0.35 * k)}
            p["hand.R"] = {"rot": R.euler(x=-50)}
        setrot(p, "chest", R.euler(x=stoop * 0.5 + 2 * k, z=3 - 4 * k))
        return p
    return fn


def install(npc_id: str):
    st = STYLE[npc_id]
    C.CLIPS.clear()
    C.CLIPS.update({
        "idle": (4, 6, True, None, idle(st)),
        "walk": (8, 10, True, None, walk(st)),
        "talk": (4, 6, True, None, talk(st)),
    })


KIT_CLIPS = {"idle": dict(frames=4, fps=6, loop=True), "walk": dict(frames=8, fps=10, loop=True),
             "talk": dict(frames=4, fps=6, loop=True)}
