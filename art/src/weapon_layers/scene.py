"""Weapon layers, Blender side. Started by build.py through kit.launcher with
art/blender/chars/rig_base.blend already open.

    argv: --only id,id   --out <dir>   --clips idle,slash   --dirs down,right   --char <sheet id>
          --flying   (render phi_kiem_1..3 instead of the hand weapons)

Every weapon (art/blender/weapons/<id>.blend) is appended, parented to a "carry" empty under one
of the character's sockets, and rendered through kit.render_layer. A hook moves the weapon
between the sockets and applies the per-frame offsets of offsets.py (hand / back rule).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Euler, Matrix, Vector

import kit.api as kit
from kit.scene import Cam, world_bounds

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import offsets as OFF            # noqa: E402

ARGV = kit.args()


def opt(name, default=None):
    return ARGV[ARGV.index(name) + 1] if name in ARGV else default


ONLY = [x for x in (opt("--only") or "").split(",") if x]
OUT = opt("--out", "client/assets/v2/weapons")
CLIPS = [x for x in (opt("--clips") or "").split(",") if x]
DIRS = [x for x in (opt("--dirs") or "").split(",") if x]
CHAR = opt("--char", "dao_si_luyen_khi")
FLYING = "--flying" in ARGV
CHAR_JSON = f"client/assets/v2/chars/{CHAR}.json"

ALL = [f"{t}_{g}" for t in ("kiem", "dao", "thuong", "chuy", "truong", "cung", "phien", "ho_lo",
                             "kich", "roi", "am_khi", "luan", "phu", "cam")
       for g in range(1, 9)]


def rig_objects():
    rig = bpy.data.objects["ARM_dao_si"]
    socks = {"r": bpy.data.objects["SOCKET_weapon_r"], "l": bpy.data.objects["SOCKET_weapon_l"],
             "back": bpy.data.objects["SOCKET_back"], "mount": bpy.data.objects["SOCKET_mount"]}
    return rig, socks


def make_carries(rig, socks):
    """One empty per attachment: the weapon is re-parented between them while rendering."""
    carries = {}
    coll = bpy.data.collections["COL_dao_si"]
    for k, s in socks.items():
        c = bpy.data.objects.new(f"CARRY_{k}", None)
        coll.objects.link(c)
        c.parent = s
        c.matrix_parent_inverse = Matrix.Identity(4)
        carries[k] = c
    c = bpy.data.objects.new("CARRY_aim", None)      # rig space, no bone
    coll.objects.link(c)
    c.parent = rig
    c.matrix_parent_inverse = Matrix.Identity(4)
    carries["aim"] = c
    return carries


def load_weapon(path: Path):
    before_m = set(bpy.data.materials)
    before_me = set(bpy.data.meshes)
    with bpy.data.libraries.load(str(path), link=False) as (src, dst):
        dst.objects = list(src.objects)
    objs = [o for o in dst.objects if o]
    for o in objs:
        bpy.context.scene.collection.objects.link(o)
    roots = [o for o in objs if o.parent is None]
    assert len(roots) == 1, (path, roots)
    new_m = set(bpy.data.materials) - before_m
    new_me = set(bpy.data.meshes) - before_me
    return roots[0], objs, new_m, new_me


def unload(objs, new_m, new_me):
    for o in objs:
        bpy.data.objects.remove(o)
    for me in new_me:
        if me.users == 0:
            bpy.data.meshes.remove(me)
    for m in new_m:
        if m.users == 0:
            bpy.data.materials.remove(m)


def _proj(v, z):
    v = Vector(v)
    return v - z * v.dot(z)


def aim_matrix(spec):
    """Rotation taking the weapon's +Z to `aim` (rig space). Width axis (local X) is the
    projection of `xdir` if given; else the broad side (-Y) faces `face` if given; else the
    width axis is vertical (edge up). Then `roll` degrees about the blade."""
    z = Vector(spec["aim"]).normalized()
    x = None
    if spec.get("xdir") is not None:
        x = _proj(spec["xdir"], z)
        if x.length > 1e-4:
            x.normalize()
            y = z.cross(x)
        else:
            x = None
    if x is None and spec.get("face") is not None:
        y = _proj(Vector(spec["face"]) * -1.0, z)
        if y.length > 1e-4:
            y.normalize()
            x = y.cross(z)
        else:
            x = None
    if x is None:
        x = _proj((0, 0, 1), z)
        if x.length < 1e-3:
            x = Vector((1, 0, 0))
        x.normalize()
        y = z.cross(x)
    m = Matrix((x, y, z)).transposed().to_4x4()
    return m @ Matrix.Rotation(math.radians(spec["roll"]), 4, "Z")


def basis_for(spec, rig, socks):
    """(carry name, matrix_basis of the weapon under that carry) for one spec."""
    at = spec["at"]
    if spec["aim"] is not None:
        bpy.context.view_layer.update()
        pos = rig.matrix_world.inverted() @ socks[at].matrix_world.translation + Vector(spec["off"])
        base = Matrix.Translation(pos) @ aim_matrix(spec)
        name = "aim"
    else:
        base = Matrix.Identity(4)
        name = at
    rot = Euler([math.radians(a) for a in spec["rot"]], "XYZ").to_matrix().to_4x4()
    s = spec["scale"]
    m = (base @ Matrix.Translation(spec["loc"]) @ rot @ Matrix.Diagonal((s, s, s, 1.0))
         @ Matrix.Translation((0, 0, -spec["grip"])))
    return name, m


def apply_spec(weapon, carries, rig, socks, spec):
    name, m = basis_for(spec, rig, socks)
    weapon.parent = carries[name]
    weapon.matrix_parent_inverse = Matrix.Identity(4)
    weapon.matrix_basis = m


def pose_of(root, spec):
    """Weapons with pose meshes (weapons_c: the whip coiled / swung / lashed, the darts in the
    fist / in flight) show one pose per frame: spec["pose"], else the model's pose_default.
    None for every other weapon (no meshes carry a "pose" property)."""
    if not root.get("poses"):
        return None
    return spec.get("pose") or root.get("pose_default") or None


def pose_objects(objs, pose):
    return [o for o in objs if pose is None or o.get("pose") in (None, pose)]


def set_pose(objs, pose):
    if pose is None:
        return
    for o in objs:
        if o.get("pose") is not None:
            o.hide_render = o.get("pose") != pose


# ------------------------------------------------------------------ keeping it in the frame
_DOC = json.loads(kit.out_path(CHAR_JSON).read_text("utf-8"))
FW, FH = _DOC["frame"]["w"], _DOC["frame"]["h"]
CAM = Cam("ground", FW, FH, _DOC["render"]["ppm"], (_DOC["pivot"]["x"], _DOC["pivot"]["y"]),
          elevation=_DOC["render"].get("elevation", 35.0))
LIM = (2.5, FW - 2.5)      # drawn pixels (incl. the 1 px outline and the head snap) must stay inside


def weapon_points(root, objs):
    """Vertices of every mesh of the weapon in the root's frame (numpy N x 3)."""
    import numpy as np
    bpy.context.view_layer.update()
    inv = root.matrix_world.inverted()
    pts = []
    for o in objs:
        if o.type != "MESH":
            continue
        n = len(o.data.vertices)
        v = np.empty(n * 3, np.float32)
        o.data.vertices.foreach_get("co", v)
        m = np.array(inv @ o.matrix_world)
        v = v.reshape(-1, 3) @ m[:3, :3].T + m[:3, 3]
        pts.append(v)
    p = np.concatenate(pts)
    if len(p) > 4000:                       # extremes matter, not density
        p = p[:: len(p) // 4000 + 1]
    return p


def _screen(world):
    import numpy as np
    loc = np.array(CAM.matrix.to_translation())
    d = world - loc
    x = CAM.w / 2 + d @ np.array(CAM.right) * CAM.ppm
    y = CAM.h / 2 - d @ np.array(CAM.up) * CAM.ppm
    return x, y


def overshoot(pts, parent_world, basis, turn_deg_list):
    """Total pixels outside LIM over all facings (0 = fits)."""
    import numpy as np
    m = np.array(parent_world @ basis)
    w = pts @ m[:3, :3].T + m[:3, 3]
    tot = 0.0
    for deg in turn_deg_list:
        r = math.radians(deg)
        c, s = math.cos(r), math.sin(r)
        wx = w[:, 0] * c - w[:, 1] * s
        wy = w[:, 0] * s + w[:, 1] * c
        ww = np.stack([wx, wy, w[:, 2]], 1)
        x, y = _screen(ww)
        tot += max(0.0, LIM[0] - x.min()) + max(0.0, x.max() - LIM[1])
        tot += max(0.0, LIM[0] - y.min()) + max(0.0, y.max() - (FH - 2.5))
    return tot


def fit_plan(wid, root, objs, carries, rig, socks, clips_frames):
    """Per (clip, frame): slide the grip along the shaft (then shrink) until the weapon fits
    the 64 px frame in all four facings. Returns {(clip, i): (grip, scale)}; the changes are
    smoothed along the clip so the hand does not jitter along the shaft."""
    pts_of = {}

    def points(spec):
        p = pose_of(root, spec)
        if p not in pts_of:
            pts_of[p] = weapon_points(root, pose_objects(objs, p))
        return pts_of[p]
    scene = bpy.context.scene
    turns = [kit.DIRS[d] for d in (DIRS or ("down", "left", "up", "right"))]
    out = {}
    for clip, (n, loop) in clips_frames.items():
        act = kit._assign_action(rig, clip)
        times = kit._times(act, dict(frames=n, loop=loop))
        specs = OFF.plan(wid, clip, n)
        raw = []
        for i, t in enumerate(times):
            kit._set_time(scene, t)
            bpy.context.view_layer.update()
            spec = specs[i]
            pts = points(spec)
            best, least = None, (1e9, (0.0, 0.7))
            slides = ([0.0] + [k * 0.05 * sgn for k in range(1, 10) for sgn in (1, -1)]
                      if OFF.weapon_type(wid) in OFF.SLIDE else [0.0])
            cands = [(g, sc) for sc in (1.0, 0.92, 0.84, 0.76, 0.68, 0.6) for g in slides]
            for g, sc in cands:
                sp = dict(spec, grip=spec["grip"] + g, scale=spec["scale"] * sc)
                name, m = basis_for(sp, rig, socks)
                ov = overshoot(pts, carries[name].matrix_world, m, turns)
                if ov == 0.0:
                    best = (g, sc)
                    break
                if ov < least[0]:
                    least = (ov, (g, sc))
            raw.append(best or least[1])
        # smooth the slide (not the scale), keeping only values that still fit
        gs = [r[0] for r in raw]
        sm = list(gs)
        for i in range(len(gs)):
            lo, hi = max(0, i - 1), min(len(gs) - 1, i + 1)
            sm[i] = (gs[lo] + 2 * gs[i] + gs[hi]) / 4.0
        for i, t in enumerate(times):
            g, sc = raw[i]
            if sm[i] != g and sc == 1.0:
                kit._set_time(scene, t)
                bpy.context.view_layer.update()
                sp = dict(specs[i], grip=specs[i]["grip"] + sm[i])
                name, m = basis_for(sp, rig, socks)
                if overshoot(points(sp), carries[name].matrix_world, m, turns) == 0.0:
                    g = sm[i]
            out[(clip, i)] = (g, sc)
    return out


def render_weapon(wid, carries, rig, socks, sheet):
    root, objs, new_m, new_me = load_weapon(kit.out_path(f"art/blender/weapons/{wid}.blend"))
    name_vi = root.get("name_vi", wid)
    doc = json.loads(kit.out_path(sheet).read_text("utf-8"))
    frames = {c: (len(next(iter(v["frames"].values()))), bool(v["loop"])) for c, v in doc["clips"].items()}
    plans = {}
    fits = {}
    try:
        if "--nofit" not in ARGV:
            fits = fit_plan(wid, root, objs, carries, rig, socks, frames)
            moved = {k: v for k, v in fits.items() if v != (0.0, 1.0)}
            kit.log(f"fit {wid}: {len(moved)} of {len(fits)} frames adjusted")

        def hook(clip, d, i):
            if clip not in plans:
                plans[clip] = OFF.plan(wid, clip, OFF.FRAMES[clip])
            spec = dict(plans[clip][i])
            g, sc = fits.get((clip, i), (0.0, 1.0))
            spec["grip"] += g
            spec["scale"] *= sc
            apply_spec(root, carries, rig, socks, spec)
            set_pose(objs, pose_of(root, spec))

        kw = {}
        if DIRS:
            kw["dirs"] = {d: kit.DIRS[d] for d in DIRS}
        kit.render_layer([root] + list(carries.values()),
                         [bpy.data.collections["COL_dao_si"], bpy.data.collections["COL_body"]],
                         sheet, OUT, wid, name_vi=name_vi, on_frame=hook, **kw)
    finally:
        root.parent = None
        unload(objs, new_m, new_me)


def filtered_sheet():
    """A copy of the character json with only the wanted clips (dev renders)."""
    if not CLIPS:
        return CHAR_JSON
    doc = json.loads(kit.out_path(CHAR_JSON).read_text("utf-8"))
    doc["clips"] = {k: v for k, v in doc["clips"].items() if k in CLIPS}
    doc["events"] = {k: v for k, v in doc.get("events", {}).items() if k in CLIPS}
    tmp = kit.out_path(f"art/render/weapon_layers/_sheet_{CHAR}.json")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(doc), "utf-8")
    return str(tmp)


def main():
    rig, socks = rig_objects()
    carries = make_carries(rig, socks)
    if FLYING:
        import flying
        flying.run(rig, socks, ONLY, OUT, ARGV)
        return
    sheet = filtered_sheet()
    for wid in (ONLY or ALL):
        kit.log(f"weapon {wid}")
        render_weapon(wid, carries, rig, socks, sheet)


main()
