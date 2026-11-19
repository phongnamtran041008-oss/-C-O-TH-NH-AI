"""The kit's public Blender-side API. Use inside a script started by kit.launcher:

    import kit.api as kit
    kit.render_animated(...), kit.render_layer(...), kit.render_icons(...),
    kit.render_fx(...), kit.render_tiles(...), kit.render_props(...)

See tools/blender/kit/README.md for worked examples.
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector

from . import pack, palette, paths, pixel
from . import palette as P
from .scene import SCALE, Cam, Capture, Staging, expand, prepare_materials, setup_render, world_bounds

ROOT = paths.ROOT
V2 = paths.ASSETS_V2
DIRS = {"down": 0.0, "left": 270.0, "up": 180.0, "right": 90.0}   # model turn per facing

# Clip tables from docs/ART_PIPELINE.md section 3.
PLAYER_CLIPS = {
    "idle": dict(frames=4, fps=6, loop=True),
    "walk": dict(frames=8, fps=10, loop=True),
    "slash": dict(frames=6, fps=14, loop=False, events={"hit": 3}),
    "cast": dict(frames=6, fps=12, loop=False, events={"hit": 3}),
    "shoot": dict(frames=6, fps=12, loop=False, events={"hit": 3}),
    "hit": dict(frames=3, fps=12, loop=False),
    "die": dict(frames=6, fps=10, loop=False),
    "meditate": dict(frames=4, fps=5, loop=True),
    "fly": dict(frames=4, fps=8, loop=True),
    "dodge": dict(frames=4, fps=14, loop=False),
}
MONSTER_CLIPS = {
    "idle": dict(frames=4, fps=6, loop=True),
    "walk": dict(frames=6, fps=10, loop=True),
    "windup": dict(frames=4, fps=8, loop=False),
    "attack": dict(frames=4, fps=12, loop=False, events={"hit": 2}),
    "hit": dict(frames=2, fps=12, loop=False),
    "die": dict(frames=6, fps=10, loop=False),
}
BOSS_EXTRA_CLIPS = {"special": dict(frames=8, fps=10, loop=False, events={"hit": 5})}

# Default framing per kind: (frame size, pivot, pixels per metre of screen).
FRAMING = {
    "player": ((64, 64), (32, 54), 38.0),
    "monster": ((48, 48), (24, 42), 38.0),
    "elite": ((64, 64), (32, 56), 38.0),
    "boss": ((96, 96), (48, 86), 38.0),
    "beast": ((48, 48), (24, 42), 38.0),
}
PPM = 38.0          # pixels per metre: a 1.0 m player is ~36 px tall on screen
TILE_M = 16 / PPM   # one 16 px ground tile is this many metres across

_log_t0 = time.time()


def log(*a):
    print(f"[kit {time.time() - _log_t0:7.1f}s]", *a, flush=True)


def args() -> list[str]:
    """The arguments given after `--` to kit.launcher.run_blender (sys.argv[1:])."""
    return sys.argv[1:]


def out_path(rel: str) -> Path:
    """Path under the repository (e.g. out_path('client/assets/v2/chars'))."""
    p = Path(rel)
    return p if p.is_absolute() else ROOT / p


def _pal(palette):
    return palette if isinstance(palette, P.Palette) else P.load(palette)


def _norm_clips(clips: dict) -> dict:
    out = {}
    for name, c in clips.items():
        c = dict(c)
        c.setdefault("fps", 8)
        c.setdefault("loop", True)
        c.setdefault("frames", 4)
        c.setdefault("action", name)
        out[name] = c
    return out


def _armature(objs):
    return next((o for o in objs if o.type == "ARMATURE"), None)


def _assign_action(target, name: str):
    act = bpy.data.actions.get(name)
    if target is None or act is None:
        return None
    if target.animation_data is None:
        target.animation_data_create()
    ad = target.animation_data
    ad.action = act
    try:
        if getattr(ad, "action_slot", None) is None and len(act.slots):
            ad.action_slot = act.slots[0]
    except (AttributeError, TypeError):
        pass
    return act


def _times(act, spec) -> list[float]:
    if spec.get("sample"):
        return [float(t) for t in spec["sample"]]
    n = int(spec["frames"])
    if act is None:
        f = bpy.context.scene.frame_current
        return [float(f)] * n
    a, b = (float(x) for x in act.frame_range)
    if n == 1:
        return [a]
    if spec.get("loop"):
        return [a + i * (b - a) / n for i in range(n)]
    return [a + i * (b - a) / (n - 1) for i in range(n)]


def _set_time(scene, t: float):
    f = int(math.floor(t))
    scene.frame_set(f, subframe=t - f)


def _render_frames(scene, staging, cam, mats, pal, restrict, pix, jobs, fx=False, fx_ramps=None,
                   ids_out=None):
    """jobs: iterable of (callable that poses the scene). Returns list of RGBA frames."""
    cap = Capture(scene, fx=fx)
    frames = []
    t0 = time.time()
    try:
        for pose in jobs:
            pose()
            albedo, data = cap.frame()
            if fx:
                frames.append(pixel.pixelise_fx(albedo, SCALE, pal, ramps=fx_ramps, **pix))
            else:
                frames.append(pixel.pixelise(albedo, data, SCALE, mats, pal, restrict,
                                             depth_range=cam.depth_hi - cam.depth_lo,
                                             ids_out=ids_out, **pix))
    finally:
        cap.cleanup()
    n = max(1, len(frames))
    log(f"  {len(frames)} frames, {(time.time() - t0) / n:.3f} s/frame")
    return frames


def _snap_point(name: str, objs):
    """A callable giving the current world position of bone `name` (in any armature of
    objs) or of the object called `name`."""
    for o in objs:
        if o.type == "ARMATURE" and name in o.pose.bones:
            return lambda o=o: o.matrix_world @ o.pose.bones[name].head
    ob = bpy.data.objects.get(name)
    if ob is None:
        raise KeyError(f"snap_to={name!r}: no bone or object of that name")
    return lambda: ob.matrix_world.to_translation()


def _material_ids(mats: dict, ign_objs, other_objs) -> set:
    """Material ids used only by the ignored objects (a material shared with the body
    cannot tell the two apart, so it is not ignored, with a warning)."""
    def names(objs):
        return {m.name for o in objs if hasattr(o.data, "materials") for m in o.data.materials if m}
    ign, other = names(ign_objs), names(other_objs)
    shared = ign & other
    if shared:
        log(f"  warning: qc_ignore materials also used by the body, not ignored: {sorted(shared)}")
    return {i for i, info in mats.items() if info["name"] in ign - shared}


def _qc_measure(rgba, mid, ign_ids: set, pivot) -> list:
    """[lowest row, feet x, bottom edge only touched by ignored pixels] of one frame with
    the qc_ignore pixels (and their outline) left out; same rule as qc.measure."""
    from . import qc
    alpha = rgba[..., 3] > 0
    ign = np.isin(mid, list(ign_ids)) if ign_ids else np.zeros(alpha.shape, bool)
    near = ign.copy()
    for dy, dx in pixel.N8:
        near |= pixel.nb(ign, dy, dx, False, False)
    ign_all = alpha & (ign | (near & (mid == 0)))
    body = alpha & ~ign_all
    h, w = alpha.shape
    bottom, feet = qc.measure(lambda x, y: bool(body[y, x]), w, h, float(pivot[0]))
    edge_ok = bool(alpha[-1].any() and not body[-1].any())
    return [bottom, feet, edge_ok]


# ======================================================================= animated
def render_animated(asset, asset_id: str, clips: dict, out_dir, name_vi: str | None = None,
                    kind: str = "player", frame=None, pivot=None, ppm: float | None = None,
                    holdout=None, dirs: dict | None = None, action_target=None,
                    palette=None, restrict: list[str] | None = None, on_frame=None,
                    layer: bool = False, exclude=None, ground_clips=None,
                    elevation: float = 35.0, snap: bool = False, snap_to: str = "head",
                    qc_ignore=None, **pixel_opts) -> dict:
    """Render every clip in four directions and pack an animated sheet + json.

    asset:   root object / collection / list (all descendants are rendered)
    clips:   {"idle": {"frames": 4, "fps": 6, "loop": True, "events": {"hit": 3},
                       "action": "idle"}, ...}   (PLAYER_CLIPS / MONSTER_CLIPS are ready-made)
    kind:    "player" | "monster" | "elite" | "boss" | "beast" -> default frame/pivot/ppm
    holdout: objects drawn as holes (used by render_layer)
    exclude: objects (with their children) left out, e.g. the weapon when rendering the body
    ground_clips: clips that lie down / collapse (QC allows a bigger footprint below the
             pivot for these only); written to the JSON as render.ground_clips
    on_frame(clip, direction, i): optional hook called after posing each frame
    elevation: camera angle above the horizon in degrees (default 35; players use 15)
    qc_ignore: objects baked into the sheet (a held weapon) that QC leaves out of the
             lowest-row / feet / bottom-edge checks; their names and per-frame measures
             are written to the JSON (render.qc_ignore, render.qc_frames)
    snap:    per frame, move the camera sideways/up by the sub-pixel amount that puts
             `snap_to` (a bone of the rig, or an object name) on the centre of a final
             pixel, so the face keeps the same pixel shape from frame to frame
    """
    fr, pv, pp = FRAMING.get(kind, FRAMING["player"])
    frame = tuple(frame or fr)
    pivot = tuple(pivot or pv)
    ppm = float(ppm or pp)
    dirs = dirs or DIRS
    clips = _norm_clips(clips)
    pal = _pal(palette)
    scene = setup_render()
    skip = set(expand(exclude))
    objs = [o for o in expand(asset) if o not in skip]
    hold = [o for o in expand(holdout) if o not in skip and o not in objs]
    target = action_target or _armature(objs + hold) or (objs[0] if objs else None)
    if isinstance(target, str):
        target = bpy.data.objects[target]
    cam = Cam("ground", frame[0], frame[1], ppm, pivot, elevation=elevation)
    snap_point = _snap_point(snap_to, objs + hold) if snap else None
    log(f"render_animated {asset_id}: {len(objs)} objects, clips {list(clips)}")
    frames, doc_clips, events = [], {}, {}
    with Staging(scene, objs, hold) as st:
        cam_obj = cam.apply(scene)
        mats = prepare_materials(objs, cam)
        ign_objs = [o for o in expand(qc_ignore)] if qc_ignore else []
        ign_ids = _material_ids(mats, ign_objs, [o for o in objs if o not in ign_objs]) if qc_ignore else None
        ids = [] if qc_ignore else None
        for cname, spec in clips.items():
            act = _assign_action(target, spec["action"])
            if act is None and bpy.data.actions:
                log(f"  warning: no action {spec['action']!r} for clip {cname!r}; rendering the current pose")
            times = _times(act, spec)
            doc_clips[cname] = {"fps": spec["fps"], "loop": bool(spec["loop"]), "frames": {}}
            if spec.get("events"):
                events[cname] = dict(spec["events"])
            for d in pack.DIR_ORDER:
                if d not in dirs:
                    continue

                def jobs(d=d, times=times, cname=cname):
                    for i, t in enumerate(times):
                        def pose(i=i, t=t):
                            st.turn_to(dirs[d])
                            _set_time(scene, t)
                            if on_frame:
                                on_frame(cname, d, i)
                            if snap_point is not None:
                                bpy.context.view_layer.update()
                                cam_obj.matrix_world = cam.snap_offset(snap_point())
                        yield pose

                start = len(frames)
                frames += _render_frames(scene, st, cam, mats, pal, restrict, pixel_opts, jobs(),
                                         ids_out=ids)
                doc_clips[cname]["frames"][d] = list(range(start, len(frames)))
    extra = {"render": {"ppm": ppm, "scale": SCALE, "kind": kind, "layer": bool(layer)}}
    if ground_clips:
        extra["render"]["ground_clips"] = list(ground_clips)
    if float(elevation) != 35.0:
        extra["render"]["elevation"] = float(elevation)
    if snap:
        extra["render"]["snap_to"] = snap_to
    if qc_ignore:
        extra["render"]["qc_ignore"] = [o.name for o in ign_objs]
        extra["render"]["qc_frames"] = [_qc_measure(f, m, ign_ids, pivot) for f, m in zip(frames, ids)]
    doc = pack.pack_animated(out_path(out_dir), asset_id, frames, doc_clips, frame, pivot,
                             name_vi, events, extra=extra)
    log(f"wrote {out_path(out_dir) / (asset_id + '.png')} ({len(frames)} frames)")
    return doc


def render_layer(layer, character, sheet_json, out_dir, layer_id: str,
                 name_vi: str | None = None, clips: dict | None = None, **kw) -> dict:
    """Render `layer` (e.g. a weapon parented to the hand socket) through the character's
    clips with the character's body as a holdout: same frame grid, pivot and order as the
    character sheet `sheet_json` (written by render_animated)."""
    doc = __import__("json").loads(out_path(sheet_json).read_text("utf-8"))
    base = clips or {}
    spec = {}
    for cname, c in doc["clips"].items():
        n = len(next(iter(c["frames"].values())))
        s = dict(frames=n, fps=c["fps"], loop=c["loop"])
        if cname in doc.get("events", {}):
            s["events"] = doc["events"][cname]
        s.update(base.get(cname, {}))
        spec[cname] = s
    layer_objs = expand(layer)
    body = [o for o in expand(character) if o not in layer_objs]
    r = doc.get("render", {})
    return render_animated(layer_objs, layer_id, spec, out_dir, name_vi=name_vi,
                           frame=(doc["frame"]["w"], doc["frame"]["h"]),
                           pivot=(doc["pivot"]["x"], doc["pivot"]["y"]),
                           ppm=r.get("ppm", PPM), holdout=body,
                           kind=r.get("kind", "player"), action_target=_armature(body),
                           ground_clips=r.get("ground_clips"),
                           elevation=r.get("elevation", 35.0),
                           snap=bool(r.get("snap_to")), snap_to=r.get("snap_to", "head"),
                           layer=True, **kw)


# ======================================================================= icons
def icon_pose(angle: float = 45.0, spin: float = 25.0, tilt: float = 0.0) -> Matrix:
    """Weapons are modelled along +Z (grip at the origin, blade up, facing -Y). The icon pose
    leans +Z to the upper right by `angle`, after turning the model `spin` degrees about
    its own long axis so the flat of the blade catches the light."""
    return (Matrix.Rotation(math.radians(angle), 4, "Y") @ Matrix.Rotation(math.radians(tilt), 4, "X")
            @ Matrix.Rotation(math.radians(spin), 4, "Z"))


def render_icons(set_name: str, icons: list[dict], out_dir, cell: int = 32, size: int = 26,
                 palette=None, restrict=None, cols: int = 8, **pixel_opts) -> dict:
    """icons: [{"id", "objects", "name_vi", "grade", optional "angle", "spin", "tilt",
    "frame", "size", "ppm"}]. Each is posed diagonally, fitted to `size` px (or rendered at a
    fixed `ppm` for a shared scale), centred in a `cell` px cell."""
    pal = _pal(palette)
    scene = setup_render()
    cells, meta = [], {}
    log(f"render_icons {set_name}: {len(icons)} icons")
    for n, ic in enumerate(icons):
        objs = expand(ic["objects"])
        if "frame" in ic:
            scene.frame_set(int(ic["frame"]))
        pose = icon_pose(ic.get("angle", 45.0), ic.get("spin", 25.0), ic.get("tilt", 0.0))
        with Staging(scene, objs) as st:
            st.turn_to(0.0, extra=pose)
            bpy.context.view_layer.update()
            probe = Cam("icon", cell, cell, 1.0, (cell / 2, cell / 2))
            pts = [probe.project(p) for p in world_bounds(objs)]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            ext = max(max(xs) - min(xs), max(ys) - min(ys), 1e-6)
            ppm = ic.get("ppm") or (ic.get("size", size) / ext)
            # world point at the middle of the projected bounds
            cx, cy = (min(xs) + max(xs)) / 2 - cell / 2, (min(ys) + max(ys)) / 2 - cell / 2
            center = probe.right * cx - probe.up * cy
            cam = Cam("icon", cell, cell, ppm, (cell / 2, cell / 2), center=center)
            cam.apply(scene)
            mats = prepare_materials(objs, cam)
            opts = dict(dict(coverage=0.3), **pixel_opts)
            cells += _render_frames(scene, st, cam, mats, pal, restrict, opts, [lambda: None])
        meta[ic["id"]] = {"index": n, "name_vi": ic.get("name_vi", ic["id"]),
                          "grade": int(ic.get("grade", 1))}
    doc = pack.pack_icons(out_path(out_dir), set_name, cells, meta, cell, cols)
    log(f"wrote {out_path(out_dir) / (set_name + '.png')}")
    return doc


# ======================================================================= fx
def render_fx(fx_id: str, objects, out_dir, frames: list[int], size: int = 64, pivot=None,
              ppm: float = PPM, fps: float = 12, loop: bool = False, blend: str = "add",
              ground: bool = False, ramps: list[str] | None = None, palette=None,
              mode: str = "ground", halo: int = 2, levels=None) -> dict:
    """FX sequence: emissive materials (colour x strength, Principled alpha soft) seen by the
    35 degree camera (mode="top" for a straight-down decal). `frames` are scene frame
    numbers. Colour picks the glow ramp (or one of `ramps`), brightness x coverage picks the
    position on it (halo / edge / core); soft alpha; `halo` soft rings (0-2). `levels` are
    the 4 intensity thresholds (default 0.08, 0.28, 0.50, 0.74)."""
    pal = _pal(palette)
    scene = setup_render()
    objs = expand(objects)
    pivot = tuple(pivot or (size // 2, size // 2))
    cam = Cam(mode, size, size, ppm, pivot)
    log(f"render_fx {fx_id}: {len(frames)} frames")
    with Staging(scene, objs) as st:
        cam.apply(scene)
        mats = prepare_materials(objs, cam, fx=True)
        jobs = [(lambda f=f: scene.frame_set(int(f))) for f in frames]
        fxo = {"halo": halo}
        if levels:
            fxo["levels"] = tuple(levels)
        out = _render_frames(scene, st, cam, mats, pal, None, fxo, jobs, fx=True, fx_ramps=ramps)
    doc = pack.pack_fx(out_path(out_dir), fx_id, out, (size, size), pivot, fps, loop, blend, ground,
                       extra={"render": {"ppm": ppm, "scale": SCALE}})
    log(f"wrote {out_path(out_dir) / (fx_id + '.png')}")
    return doc


# ======================================================================= tiles
def _wrap_copies(objs, tile_m: float):
    """Linked duplicates of the tile's meshes at the 8 neighbouring tile offsets, so what
    pokes over one edge comes back in on the other: tiles are seamless by construction."""
    made = []
    coll = bpy.context.scene.collection
    bpy.context.view_layer.update()          # matrix_world must reflect fresh edits
    for o in [o for o in objs if o.type == "MESH"]:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                c = o.copy()
                c.parent = None
                c.matrix_world = Matrix.Translation((dx * tile_m, dy * tile_m, 0)) @ o.matrix_world
                coll.objects.link(c)
                made.append(c)
    return made


def wrap_check(tile: np.ndarray) -> float:
    """How much more often neighbouring pixels differ across the wrap seam than inside the
    tile (1.0 = the seam looks like any other column/row; > 2 means a visible seam).
    Counts differing pixel pairs, so one sparse accent on the edge does not trip it."""
    t = tile.astype(np.int32)
    key = (t[..., 0] << 24) | (t[..., 1] << 16) | (t[..., 2] << 8) | t[..., 3]
    inner = ((key[:, 1:] != key[:, :-1]).mean() + (key[1:] != key[:-1]).mean()) / 2
    seam = ((key[:, 0] != key[:, -1]).mean() + (key[0] != key[-1]).mean()) / 2
    return float((seam + 0.05) / (inner + 0.05))


def render_tiles(region: str, tiles: dict, out_dir, tile_m: float = TILE_M, palette=None,
                 restrict=None, cols: int = 8, wrap: bool = True, **pixel_opts) -> dict:
    """tiles: {"grass": [entry, ...], "water": [...]}; each entry is objects (or
    {"objects": ..., "frame": n, "wrap": bool}) making ONE 16 px tile, modelled in a tile_m
    square centred on the origin, seen straight down. The json lists the indices per name."""
    pal = _pal(palette)
    scene = setup_render()
    cam = Cam("top", 16, 16, 16.0 / tile_m, (8, 8))
    images, names, scores = [], {}, {}
    log(f"render_tiles {region}: {sum(len(v) for v in tiles.values())} tiles")
    for name, entries in tiles.items():
        names[name] = []
        for k, e in enumerate(entries):
            e = e if isinstance(e, dict) else {"objects": e}
            objs = expand(e["objects"])
            w = e.get("wrap", wrap)
            copies = _wrap_copies(objs, tile_m) if w else []
            try:
                with Staging(scene, objs + copies) as st:
                    cam.apply(scene)
                    mats = prepare_materials(objs + copies, cam)
                    if "frame" in e:
                        scene.frame_set(int(e["frame"]))
                    opts = dict(dict(outline=False, inner_lines=False, wrap=w), **pixel_opts)
                    img = _render_frames(scene, st, cam, mats, pal, restrict, opts, [lambda: None])[0]
            finally:
                for c in copies:
                    bpy.data.objects.remove(c)
            if w:
                scores[f"{name}[{k}]"] = round(wrap_check(img), 2)
            names[name].append(len(images))
            images.append(img)
    doc = pack.pack_tiles(out_path(out_dir), region, images, names, cols,
                          extra={"render": {"tile_m": tile_m, "wrap_check": scores}})
    bad = {k: v for k, v in scores.items() if v > 2.0}
    log(f"wrote {out_path(out_dir) / (region + '.png')}; wrap check {scores}"
        + (f"  SEAM WARNING {bad}" if bad else ""))
    return doc


# ======================================================================= props
def render_props(region: str, props: list[dict], out_dir, ppm: float = PPM, margin: int = 2,
                 palette=None, restrict=None, **pixel_opts) -> dict:
    """props: [{"name", "objects", optional "frames": [scene frames], "solid": [x,y,w,h],
    "ppm"}]. Each prop is seen by the 35 degree camera, framed to its own size; the pivot
    is the projected origin (put the origin at the base of the prop)."""
    pal = _pal(palette)
    scene = setup_render()
    packed = []
    log(f"render_props {region}: {len(props)} props")
    for p in props:
        objs = expand(p["objects"])
        fl = p.get("frames") or [scene.frame_current]
        pp = float(p.get("ppm", ppm))
        with Staging(scene, objs) as st:
            probe = Cam("ground", 64, 64, pp, (0, 0))
            xs, ys = [], []
            for f in fl:
                scene.frame_set(int(f))
                for q in world_bounds(objs):
                    x, y = probe.project(q)
                    xs.append(x)
                    ys.append(y)
            x0, x1 = math.floor(min(xs)) - margin, math.ceil(max(xs)) + margin
            y0, y1 = math.floor(min(ys)) - margin, math.ceil(max(ys)) + margin
            w, h = x1 - x0, y1 - y0
            pivot = (-x0, -y0)
            cam = Cam("ground", w, h, pp, pivot)
            cam.apply(scene)
            mats = prepare_materials(objs, cam)
            jobs = [(lambda f=f: scene.frame_set(int(f))) for f in fl]
            frames = _render_frames(scene, st, cam, mats, pal, restrict, pixel_opts, jobs)
        packed.append({"name": p["name"], "frames": frames, "pivot": pivot, "solid": p.get("solid")})
    doc = pack.pack_props(out_path(out_dir), region, packed)
    log(f"wrote {out_path(out_dir) / (region + '.png')}")
    return doc


# ======================================================================= helpers
def swap_sheet(src_json, dst_id: str, mapping: dict[str, str], name_vi: str | None = None) -> Path:
    """Palette-swapped copy of a packed sheet (monster colour variants):
    swap_sheet('client/assets/v2/monsters/soi.json', 'soi_bang', {'earth': 'ice'})."""
    import json
    src = out_path(src_json)
    doc = json.loads(src.read_text("utf-8"))
    png_src = src.parent / doc["sheet"]
    doc["id"] = dst_id
    doc["sheet"] = f"{dst_id}.png"
    if name_vi:
        doc["name_vi"] = name_vi
    P.swap_png(png_src, src.parent / doc["sheet"], mapping)
    pack._write_json(src.parent / f"{dst_id}.json", doc)
    return src.parent / f"{dst_id}.json"


def save_blend(rel_path: str) -> Path:
    """Save the current scene to art/blender/... BEFORE rendering (the kit edits materials
    in memory while it renders)."""
    p = out_path(rel_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(p), compress=True)
    return p


def clear_scene():
    """Empty factory scene (objects, meshes, materials, actions)."""
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials, bpy.data.actions,
                 bpy.data.armatures, bpy.data.cameras, bpy.data.lights, bpy.data.curves):
        for x in list(coll):
            coll.remove(x)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
