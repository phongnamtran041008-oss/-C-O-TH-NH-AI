"""Look-dev v2 rig: a slender young cultivator, ~3.4 heads in 1.0 m (runs inside Blender).

Reuses the solver of ../rig.py (FK + baked two-bone IK, chest-frame arm aims, weapon
`blade` aims) by swapping its bone table for the v2 proportions before anything is built.
Import this module before ../clips.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import rig as R  # noqa: E402

PPM = 48.0                # final pixels per metre (figure ~48 px)
PX = 1.0 / PPM            # one final pixel, in metres

# name: (head, tail, parent, deform), final proportions (metres, faces -Y, +X = own left)
BONES = {
    "root":       ((0, 0, 0), (0, 0.15, 0), None, False),
    "mount":      ((0, 0, 0), (0, -0.12, 0), "root", False),
    "qi":         ((0, 0, 0.45), (0, 0, 0.55), "root", True),
    "hips":       ((0, 0, 0.47), (0, 0, 0.56), "root", True),
    "spine":      ((0, 0, 0.56), (0, 0, 0.63), "hips", True),
    "chest":      ((0, 0, 0.63), (0, 0, 0.71), "spine", True),
    "neck":       ((0, 0, 0.71), (0, 0, 0.755), "chest", True),
    "head":       ((0, 0, 0.755), (0, 0, 0.98), "neck", True),
    "hair_01":    ((0, 0.085, 0.93), (0, 0.115, 0.82), "head", True),
    "hair_02":    ((0, 0.115, 0.82), (0, 0.125, 0.67), "hair_01", True),
    "hair_03":    ((0, 0.125, 0.67), (0, 0.125, 0.50), "hair_02", True),
    "ribbon_01.L": ((0.03, 0.05, 1.0), (0.06, 0.10, 0.92), "head", True),
    "ribbon_02.L": ((0.06, 0.10, 0.92), (0.08, 0.13, 0.80), "ribbon_01.L", True),
    "ribbon_01.R": ((-0.03, 0.05, 1.0), (-0.06, 0.10, 0.92), "head", True),
    "ribbon_02.R": ((-0.06, 0.10, 0.92), (-0.08, 0.13, 0.80), "ribbon_01.R", True),
    "halo":       ((0, 0, 0.86), (0, 0, 0.96), "head", True),
    "upper_arm.L": ((0.15, 0, 0.685), (0.168, 0.005, 0.515), "chest", True),
    "forearm.L":  ((0.168, 0.005, 0.515), (0.178, -0.012, 0.375), "upper_arm.L", True),
    "hand.L":     ((0.178, -0.012, 0.375), (0.181, -0.018, 0.315), "forearm.L", True),
    "sleeve.L":   ((0.17, 0.0, 0.50), (0.19, 0.02, 0.40), "forearm.L", True),
    "upper_arm.R": ((-0.15, 0, 0.685), (-0.168, 0.005, 0.515), "chest", True),
    "forearm.R":  ((-0.168, 0.005, 0.515), (-0.178, -0.012, 0.375), "upper_arm.R", True),
    "hand.R":     ((-0.178, -0.012, 0.375), (-0.181, -0.018, 0.315), "forearm.R", True),
    "sleeve.R":   ((-0.17, 0.0, 0.50), (-0.19, 0.02, 0.40), "forearm.R", True),
    "thigh.L":    ((0.068, 0, 0.47), (0.071, -0.012, 0.262), "hips", True),
    "shin.L":     ((0.071, -0.012, 0.262), (0.072, 0, 0.055), "thigh.L", True),
    "foot.L":     ((0.072, 0, 0.055), (0.072, -0.10, 0.018), "shin.L", True),
    "thigh.R":    ((-0.068, 0, 0.47), (-0.071, -0.012, 0.262), "hips", True),
    "shin.R":     ((-0.071, -0.012, 0.262), (-0.072, 0, 0.055), "thigh.R", True),
    "foot.R":     ((-0.072, 0, 0.055), (-0.072, -0.10, 0.018), "shin.R", True),
    "hem_F":      ((0, -0.07, 0.54), (0, -0.09, 0.33), "hips", True),
    "hem_B":      ((0, 0.065, 0.54), (0, 0.085, 0.33), "hips", True),
    "hem.L":      ((0.09, 0, 0.54), (0.12, 0, 0.33), "hips", True),
    "hem.R":      ((-0.09, 0, 0.54), (-0.12, 0, 0.33), "hips", True),
    "cape_01":    ((0, 0.07, 0.70), (0, 0.095, 0.52), "chest", True),
    "cape_02":    ((0, 0.095, 0.52), (0, 0.11, 0.34), "cape_01", True),
    "cape_03":    ((0, 0.11, 0.34), (0, 0.12, 0.16), "cape_02", True),
    "wing_01.L":  ((0.04, 0.08, 0.62), (0.14, 0.15, 0.72), "chest", True),
    "wing_02.L":  ((0.14, 0.15, 0.72), (0.28, 0.22, 0.88), "wing_01.L", True),
    "wing_01.R":  ((-0.04, 0.08, 0.62), (-0.14, 0.15, 0.72), "chest", True),
    "wing_02.R":  ((-0.14, 0.15, 0.72), (-0.28, 0.22, 0.88), "wing_01.R", True),
}


def install():
    """Swap the v2 table into ../rig.py (identity proportion map: designed at final size)."""
    R.BONES.clear()
    R.BONES.update(BONES)
    R.ZMAP[:] = [(0.0, 0.0), (1.0, 1.0)]
    R.NECK_OLD = R.NECK_NEW = 0.755
    R.HEAD_K = 1.0
    R.ORDER[:] = R.bone_order()
    R.RIG_BONES.clear()
    R.RIG_BONES.update({n: (h, t, p, d) for n, (h, t, p, d) in BONES.items()})


install()
