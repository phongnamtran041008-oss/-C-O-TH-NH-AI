#!/usr/bin/env python3
"""Render every fetched model into a game icon (M8, kế hoạch 7.1).

    blender -b --factory-startup --python tools/blender/render_item.py -- --out art/render_items

Reads `art/models/manifest.json` (written by tools/fetch_models.py) and leaves one PNG per
model in the output folder, plus `items.json` listing what was rendered.

The rules that make an icon an icon:

* **One camera for all of them.** Orthographic, straight on, framed from each model's own
  bounding box with the same margin, so a dagger and a greatsword end up the same size on
  screen and a row of them lines up.
* **Turned, not skewed.** Every model is parented to an empty at its own centre and that
  empty is turned, so a model made of ten separate meshes rotates as one piece. glTF files
  arrive Y-up with a rotated root, which is exactly where rotating the mesh itself goes
  wrong.
* **Lit the same every time**, transparent film, no anti-aliasing: a soft edge turns to mud
  when the frame is scaled down to 32 px.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "art" / "models" / "manifest.json"

# How far each group is turned for its icon. A long weapon reads best on the reference
# sheet's diagonal; a chest piece or a helmet has to be seen straight on, or it turns into
# a crumpled rag the moment it is 32 pixels wide.
TILT = {"vu_khi": 38.0, "trang_bi": 0.0, "dan_duoc": 0.0, "cong_phap": 12.0}


def clear() -> None:
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def setup(px: int) -> bpy.types.Object:
    scene = bpy.context.scene
    for want in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
        try:
            scene.render.engine = want
            break
        except TypeError:
            continue
    cam_data = bpy.data.cameras.new("icon_cam")
    cam_data.type = "ORTHO"
    cam = bpy.data.objects.new("icon_cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    cam.rotation_euler = (math.radians(90), 0, 0)
    for name, loc, energy, rot in (("key", (-3, -4, 4), 4.0, (50, 0, -35)),
                                   ("fill", (4, -3, 1.5), 2.0, (70, 0, 45)),
                                   ("rim", (0, 4, 3), 2.0, (-60, 0, 0))):
        d = bpy.data.lights.new(name, "SUN")
        d.energy = energy
        o = bpy.data.objects.new(name, d)
        scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = [math.radians(a) for a in rot]
    world = bpy.data.worlds.new("World")
    scene.world = world
    try:
        world.use_nodes = True              # gone in Blender 6: nodes are always on
    except (AttributeError, DeprecationWarning):
        pass
    nodes = getattr(getattr(world, "node_tree", None), "nodes", [])
    bg = next((n for n in nodes if n.type == "BACKGROUND"), None)
    if bg:
        bg.inputs["Color"].default_value = (0.6, 0.63, 0.7, 1)
        bg.inputs["Strength"].default_value = 1.0
    scene.render.resolution_x = scene.render.resolution_y = px
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.filter_size = 0.0
    try:
        scene.eevee.taa_render_samples = 16
    except AttributeError:
        pass
    return cam


def sane_meshes(meshes: list) -> list:
    """Drop the parts that are wildly bigger than the rest of the model.

    Some library models carry a stray mesh far from everything else - one came in 431 km
    across - and framing on it renders an empty icon. Measuring each part and keeping the
    ones near the median size is enough to spot that, and it leaves normal models alone.
    """
    if len(meshes) < 2:
        return meshes
    diag = {}
    for o in meshes:
        cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
        lo = Vector((min(c.x for c in cs), min(c.y for c in cs), min(c.z for c in cs)))
        hi = Vector((max(c.x for c in cs), max(c.y for c in cs), max(c.z for c in cs)))
        diag[o.name] = (hi - lo).length
    ordered = sorted(diag.values())
    median = ordered[len(ordered) // 2] or 1e-6
    keep = [o for o in meshes if diag[o.name] <= median * 20]
    dropped = len(meshes) - len(keep)
    if dropped:
        print(f"     (ignored {dropped} outsized part(s); median {median:.2f} m)")
    return keep or meshes


def bounds(objs, trim: float = 0.02) -> tuple[Vector, Vector]:
    """Where the model really is, ignoring stray vertices.

    A bounding box is the wrong tool here: one library mace carries a handful of vertices
    431 km from the handle, and framing on its box renders an empty icon. Taking the 2nd and
    98th percentile of the actual vertices throws those away and leaves ordinary models
    untouched (their percentiles sit on the box anyway).
    """
    pts = []
    for o in objs:
        if o.type != "MESH":
            continue
        mw = o.matrix_world
        verts = o.data.vertices
        step = max(1, len(verts) // 4000)          # a sample is plenty to find the edges
        pts += [mw @ v.co for v in verts[::step]]
    if not pts:
        cs = [o.matrix_world @ Vector(c) for o in objs if o.type == "MESH" for c in o.bound_box]
        return (Vector((min(c.x for c in cs), min(c.y for c in cs), min(c.z for c in cs))),
                Vector((max(c.x for c in cs), max(c.y for c in cs), max(c.z for c in cs))))
    lo, hi = [], []
    for axis in range(3):
        vals = sorted(p[axis] for p in pts)
        k = int(len(vals) * trim)
        lo.append(vals[k])
        hi.append(vals[-1 - k])
    return Vector(lo), Vector(hi)


def render_one(glb: Path, out: Path, tilt: float, px: int) -> dict | None:
    # clear() deletes the camera and the lights too, so the rig is rebuilt per model rather
    # than held in a Python variable: a reference to a removed object raises on next touch
    clear()
    cam = setup(px)
    before = set(bpy.data.objects)
    try:
        bpy.ops.import_scene.gltf(filepath=str(glb))
    except Exception as e:                       # a broken download should not stop the batch
        print(f"  !! {glb.name}: {e}")
        return None
    new = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in new if o.type == "MESH"]
    if not meshes:
        print(f"  !! {glb.name}: no mesh inside")
        return None

    meshes = sane_meshes(meshes)
    lo, hi = bounds(meshes)
    pivot = bpy.data.objects.new("pivot", None)
    bpy.context.scene.collection.objects.link(pivot)
    pivot.location = (lo + hi) / 2
    for o in new:
        if o.parent is None:
            o.parent = pivot
            o.matrix_parent_inverse = pivot.matrix_world.inverted()
    pivot.rotation_euler = (0, math.radians(tilt), 0)   # the icon diagonal, in the camera plane
    bpy.context.view_layer.update()

    lo, hi = bounds(meshes)
    centre = (lo + hi) / 2
    span = max(hi.x - lo.x, hi.z - lo.z)
    if span <= 0:
        print(f"  !! {glb.name}: no size at all, no icon made")
        return None
    cam.data.ortho_scale = span * 1.18
    back = max(5.0, span * 3)
    cam.location = (centre.x, lo.y - back, centre.z)
    # Library models come at any scale - one mace is 400 km across - and a camera still on
    # its 100 m default clip renders a blank frame. Clip from the model, not from Blender.
    cam.data.clip_start = max(0.001, span * 0.001)
    cam.data.clip_end = back + span * 6
    bpy.context.scene.render.filepath = str(out / glb.stem)
    bpy.ops.render.render(write_still=True)
    return {"file": glb.stem + ".png", "span_m": round(span, 3)}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default="art/render_items")
    ap.add_argument("--px", type=int, default=256)
    ap.add_argument("--tilt", type=float, default=None,
                    help="degrees, same for every group; the default is per group (see TILT)")
    args = ap.parse_args(argv)

    if not MANIFEST.exists():
        print("render_item: no art/models/manifest.json (run tools/fetch_models.py first)",
              file=sys.stderr)
        return 1
    models = json.loads(MANIFEST.read_text("utf-8"))["models"]
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    done = []
    for m in models:
        glb = ROOT / m["file"]
        if not glb.exists():
            print(f"  !! missing {m['file']}")
            continue
        tilt = args.tilt if args.tilt is not None else TILT.get(m["kind"], 0.0)
        info = render_one(glb, out, tilt, args.px)
        if info is None:
            continue
        done.append({**info, "tilt": tilt, "kind": m["kind"], "slug": m["slug"], "title": m["title"],
                     "creator": m["creator"], "licence": m["licence"]})
        print(f"  {m['kind']}/{m['slug']}: {m['title']} -> {info['file']}")
    (out / "items.json").write_text(json.dumps({"icons": done}, ensure_ascii=False, indent=1) + "\n",
                                    "utf-8", newline="\n")
    print(f"rendered {len(done)}/{len(models)} icons at {args.px}px into {args.out}")
    return 0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
