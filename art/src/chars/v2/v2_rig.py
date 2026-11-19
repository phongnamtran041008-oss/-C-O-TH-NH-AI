"""Production v2 rig (runs inside Blender): the approved look-dev body (~3.4 heads in 1.0 m,
96x96 frame, 15 degree camera) with wing bones placed for big wings angled ~35 degrees back.
Import before ../clips.py."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (HERE, HERE.parent / "lookdev", HERE.parent):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import ld_rig  # noqa: E402  (installs the look-dev bone table)
import rig as R  # noqa: E402

PPM = ld_rig.PPM
PX = ld_rig.PX
FRAME = (96, 96)
PIVOT = (48, 82)
ELEVATION = 15.0

BONES = dict(ld_rig.BONES)
# Wing arm: three bones from the shoulder blade, in a plane turned 35 degrees back from the
# body: upper arm up and out (~60 deg), forearm out and a little up, hand out and down. The
# wrist (wing_02 tail) is the high point of the arched leading edge.
import math as _m

_BACK = _m.radians(35)


def _wing_bones(s):
    out = (s * _m.cos(_BACK), _m.sin(_BACK), 0.0)

    def step(p, ang, ln):
        a = _m.radians(ang)
        return (p[0] + out[0] * _m.cos(a) * ln, p[1] + out[1] * _m.cos(a) * ln, p[2] + _m.sin(a) * ln)
    root = (s * 0.05, 0.075, 0.64)
    shoulder = step(root, 65, 0.28)
    wrist = step(shoulder, 35, 0.28)
    tip = step(wrist, -12, 0.20)
    side = "L" if s > 0 else "R"
    return {f"wing_01.{side}": (root, shoulder, "chest", True),
            f"wing_02.{side}": (shoulder, wrist, f"wing_01.{side}", True),
            f"wing_03.{side}": (wrist, tip, f"wing_02.{side}", True)}


BONES.update(_wing_bones(1))
BONES.update(_wing_bones(-1))


def install():
    ld_rig.BONES.clear()
    ld_rig.BONES.update(BONES)
    ld_rig.install()


install()
