"""Cửu Vĩ Hồ: the nine-tailed fox. Runs inside Blender (see scene.py).

Slender and elegant, cream fur with a white chest ruff, gold socks, tall ears with gold
insides, a narrow muzzle, gold almond eyes with red kitsune marks at the outer corners and a
red mark on the brow. Behind it NINE tails fan out like a peacock's train: each is a
skinned tube on its own two bones (base and tip) ending in a soft gold glow, and adjacent
tails use two materials of the same cream so the kit draws a separating line between them
(the tails read as many tails, not one blob). Every clip sways the tails out of phase (the
tips lag the bases); windup flares the fan, attack sweeps it back, die lets it droop, sleep
folds it round the body. The body is the shared quadruped rig (IK legs, paws level).
"""
from __future__ import annotations

import math

from mathutils import Vector

from common import (S, att, aim, ball, cute_eyes, eye_mats, eyes_bone, finish, glow, hexc, mat, merge,
                    quad_armature, quad_extra_poses, quad_poses, set_ramp, skin, tube, use_collection)

N_TAILS = 9
FAN = [-92 + 184 * k / (N_TAILS - 1) for k in range(N_TAILS)]     # degrees from straight up
BASE = Vector((0, 0.11, 0.33))


def tail_points(a_deg):
    """Base, knee, end of the fluffy part and the glowing tip of a tail fanned at a_deg."""
    a = math.radians(a_deg)
    f = Vector((math.sin(a), 0, math.cos(a)))
    d1 = (0.3 * f + Vector((0, 0.85, 0.42))).normalized()      # all leave the rump back-up as one bundle
    d2 = (0.9 * f + Vector((0, 0.25, 0.3))).normalized()      # then open into a sunburst behind the head
    d3 = (0.85 * f + Vector((0, 0.05, 0.5))).normalized()     # and the tips curl up
    p1 = BASE + d1 * 0.12
    p2 = p1 + d2 * 0.22
    p3 = p2 + d3 * 0.10
    return BASE.copy(), p1, p2, p3


def build():
    use_collection("COL_cuu_vi_ho")
    fur = mat("MAT_cv_fur", "#cfcbd3", "bone")
    fur_sh = mat("MAT_cv_fur_shade", "#9894a2", "bone")
    ruff = mat("MAT_cv_ruff", "#f5ead0", "paper")
    sock = mat("MAT_cv_sock", "#9894a2", "bone")
    inner = mat("MAT_cv_inner", "#e6b83a", "gold")
    red = mat("MAT_cv_red_mark", "#c8553a", "red")
    nose = mat("MAT_cv_nose", "#2e2834", "hair")
    tails = [mat("MAT_cv_tail_a", "#ead9b0", "paper"), mat("MAT_cv_tail_b", "#e6b83a", "gold")]
    tip = glow("MAT_cv_tailtip", "#ffe27a", "holy", 2.5, halo=0)
    eyes = eye_mats("cv", hexc("#b9821a"))
    set_ramp(eyes[0], "gold")

    HY, HZ = -0.18, 0.50
    P = {"h": 0.30, "yf": -0.06, "yb": 0.085, "x": 0.07, "knee": 0.15,
         "head": (-0.11, 0.37), "hlen": 0.2, "jaw": (-0.26, 0.46),
         "tail": ((0.11, 0.33), (0.18, 0.40), (0.24, 0.46))}
    extra = [eyes_bone(HY - 0.1, HZ + 0.02)]
    pts = {}
    for k, a in enumerate(FAN):
        p0, p1, p2, p3 = tail_points(a)
        pts[k] = (p0, p1, p2, p3)
        extra += [(f"t{k}a", tuple(p0), tuple(p1), "pelvis"), (f"t{k}b", tuple(p1), tuple(p2), f"t{k}a")]
    arm = quad_armature("cuu_vi_ho", P, extra=extra)

    att(arm, "chest", ball("cv_chest", (0.105, 0.12, 0.10), (0, -0.03, 0.34), fur),
        ball("cv_ruff", (0.09, 0.07, 0.10), (0, -0.10, 0.36), ruff),
        aim("cv_neck", fur, (0, -0.06, 0.36), (0, -0.13, 0.46), 0.065, 0.06, seg=10, smooth=True))
    att(arm, "pelvis", ball("cv_rump", (0.095, 0.11, 0.095), (0, 0.07, 0.33), fur))
    hd = [ball("cv_head", (0.155, 0.145, 0.135), (0, HY, HZ), fur),
          aim("cv_muzzle", fur, (0, HY - 0.07, HZ - 0.04), (0, HY - 0.23, HZ - 0.065), 0.062, 0.018, seg=10, smooth=True),
          ball("cv_nose", (0.02, 0.018, 0.016), (0, HY - 0.23, HZ - 0.06), nose, seg=8, rings=5),
          ball("cv_chin", (0.04, 0.06, 0.025), (0, HY - 0.12, HZ - 0.085), ruff, seg=8, rings=5),
          aim("cv_brow_mark", red, (0, HY - 0.135, HZ + 0.06), (0, HY - 0.12, HZ + 0.11), 0.018, 0.0, seg=6)]
    for s in (1, -1):
        hd += [aim(f"cv_ear{s}", fur, (s * 0.075, HY + 0.02, HZ + 0.09), (s * 0.15, HY + 0.05, HZ + 0.31), 0.066, 0.0, seg=6),
               aim(f"cv_eari{s}", inner, (s * 0.078, HY + 0.0, HZ + 0.11), (s * 0.14, HY + 0.028, HZ + 0.27), 0.04, 0.0, seg=6),
               aim(f"cv_cheek{s}", fur, (s * 0.08, HY - 0.02, HZ - 0.06), (s * 0.19, HY + 0.04, HZ - 0.08), 0.045, 0.0, seg=6),
               # red kitsune liner sweeping up from the outer corner of each eye
               aim(f"cv_liner_mark{s}", red, (s * 0.098, HY - 0.112, HZ + 0.025), (s * 0.14, HY - 0.08, HZ + 0.065), 0.012, 0.004, seg=5)]
    att(arm, "head", *hd)
    att(arm, "eyes", *cute_eyes("cv", 0.062, HY - 0.124, HZ + 0.012, 0.047, eyes))
    att(arm, "jaw", aim("cv_jaw", fur_sh, (0, HY - 0.06, HZ - 0.08), (0, HY - 0.18, HZ - 0.09), 0.03, 0.015, seg=8))
    for side, sx in (("l", 1), ("r", -1)):
        for leg, y in (("f", P["yf"]), ("b", P["yb"])):
            x = sx * P["x"]
            att(arm, f"{leg}{side}1", aim(f"cv_{leg}{side}up", fur, (x, y, 0.29), (x, y, 0.15), 0.042 if leg == "b" else 0.036, 0.028, seg=8))
            att(arm, f"{leg}{side}2", aim(f"cv_{leg}{side}lo", fur, (x, y, 0.16), (x, y, 0.07), 0.024, 0.022, seg=8),
                aim(f"cv_{leg}{side}sock", sock, (x, y, 0.08), (x, y, 0.03), 0.025, 0.024, seg=8))
            att(arm, f"{leg}{side}3", ball(f"cv_{leg}{side}paw", (0.03, 0.04, 0.024), (x, y - 0.008, 0.022), sock, seg=8, rings=5))
    # the nine tails
    for k in range(N_TAILS):
        p0, p1, p2, p3 = pts[k]
        m = tails[k % 2]
        body = tube(f"cv_tail{k}", [p0, p0.lerp(p1, 0.5), p1, p1.lerp(p2, 0.5), p2, p2.lerp(p3, 0.4)],
                    [0.02, 0.03, 0.04, 0.05, 0.046, 0.04], m, seg=10)
        skin(body, arm, [f"t{k}a", f"t{k}b"], power=3.0)
        att(arm, f"t{k}b", aim(f"cv_tailtip{k}", tip, tuple(p2.lerp(p3, 0.3)), tuple(p3), 0.04, 0.0, seg=8))

    # ------------------------------------------------------------------ poses
    A = {"stride": 0.03, "lift": 0.045, "hop": 0.06, "crouch": 0.06, "drop": 0.14, "lunge": 0.02}
    poses = quad_poses(P, A)
    poses.update(quad_extra_poses(P, drop=0.14, tail_wrap=60.0, head_rest=(14, 0, 50)))

    def fan(i, n, amp=7.0, lag=10.0, spread=1.0, lift=0.0, speed=1.0, base=0.0):
        """Tail entries for frame i of n: each tail sways about the fan axis out of phase
        with its neighbours, the tip a beat behind the base; `spread` opens / closes the
        fan, `lift` tips the whole fan back (-) or forward (+)."""
        out = {}
        for k, a in enumerate(FAN):
            ph = TAU_K * k
            th = (spread - 1.0) * a + amp * S(i * speed, n, ph) + base
            out[f"t{k}a"] = {"r": (lift, th, 0)}
            out[f"t{k}b"] = {"r": (lift * 0.4, lag * S(i * speed, n, ph - 1.2), 0)}
        return out

    TAU_K = 0.75
    deco = {"idle": dict(amp=6, lag=9), "walk": dict(amp=8, lag=12, lift=-6),
            "windup": dict(amp=3, lag=6, spread=1.06, lift=8), "attack": dict(amp=4, lag=14, spread=0.9, lift=-20),
            "hit": dict(amp=10, lag=16, spread=1.08, lift=10), "die": dict(amp=2, lag=4),
            "happy": dict(amp=14, lag=18, spread=1.06), "sleep": dict(amp=2, lag=3, spread=0.75, lift=-40)}
    for clip_name, frames in poses.items():
        n = len(frames)
        for i, p in enumerate(frames):
            kw = dict(deco[clip_name])
            if clip_name == "die":       # the fan sinks as it faints
                kw["lift"] = -35 * min(1.0, i / 3)
                kw["spread"] = 1.0 - 0.15 * min(1.0, i / 3)
            p.update(fan(i, n, **kw))
    for i, p in enumerate(poses["idle"]):
        p["eyes"] = {"s": (1, 0.2 if i == 3 else 1.0, 1)}
    for p in poses["die"][3:]:
        p["eyes"] = {"s": (1, 0.12, 1)}
    finish(arm, poses, walk_fps=11)
    return arm
