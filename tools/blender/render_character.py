#!/usr/bin/env python3
"""Render a character's clips to PNG frames, four directions each (M8, kế hoạch 7.1 bước 3).

    blender -b art/blender/dao_si.blend --python tools/blender/render_character.py -- --id dao_si

Writes `art/render/<id>/<clip>_<dir>_0000.png ...` plus the `render.json` that
tools/pack_sprites.py reads.

Three things here matter more than they look:

* **Orthographic camera, never moved.** Every frame of every clip and every direction is
  shot with the same camera, so the character cannot change size or slide between frames.
  The four directions come from turning the *rig*, not the camera, which also keeps the
  light coming from the same side in all four.
* **The pivot is computed, not guessed.** The ground point under the rig (the world origin)
  is projected through that camera once, and written into render.json as `pivot_px`. That is
  what makes "the feet stay put" true by construction instead of something to check later.
* **Transparent film and no anti-aliasing.** The game is pixel art: a soft edge becomes mud
  when the frame is scaled down, and a non-transparent film puts a grey box behind every
  character.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
RENDER_DIR = ROOT / "art" / "render"
# How far to turn the rig for each facing. The rig faces -y, toward the camera, and turning
# it +90 degrees points its face at +x, which is the RIGHT of the picture - so "right" is 90
# and "left" is 270. M8 had these two the other way round, which nobody saw while the game
# only drew characters facing down; M9 plays the cast clip in the caster's own facing, so
# a character walking left that turned to face right would have been plain to see. (The
# key order stays down, left, up, right: it is the order the frames are packed in.)
DIRS = {"down": 0.0, "left": 270.0, "up": 180.0, "right": 90.0}
ELEVATION = 35.0          # degrees above the ground: the game's own three-quarter view
ORTHO_SCALE = 1.58        # metres across the frame. Wide enough that the widest character
                          # (Đại Thừa, wings out) keeps a margin, and the **same for every
                          # character**, which is what makes them all one size in game.


# The one-shot clips (slash, cast) play at 12 fps; the loops are slower so they read as calm.
FPS = {"idle": 6.0, "walk": 10.0, "slash": 12.0, "cast": 12.0}
LOOP = {"idle": True, "walk": True, "slash": False, "cast": False}
# The order clips are rendered in, which is also the order the packer lays their frames out
# in. M8 rendered by name (idle, slash, walk); cast came in M9 and goes after them, so every
# frame index the M8 sheets had still points at the same picture. A clip not listed here
# comes after these, by name. The order also decides what pose a bone that a clip does not
# key starts from (whatever the clip before it left), which is a second reason not to
# reshuffle it.
CLIP_ORDER = ("idle", "slash", "walk", "cast")


def clip_rank(action) -> tuple[int, str]:
    name = action.name
    return (CLIP_ORDER.index(name) if name in CLIP_ORDER else len(CLIP_ORDER), name)


def pick_engine() -> str:
    """Workbench if this build has it: flat colours, no lighting to set up, and fast."""
    scene = bpy.context.scene
    current = scene.render.engine
    for want in ("BLENDER_WORKBENCH", "BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
        try:
            scene.render.engine = want
            return want
        except TypeError:
            continue
    return current


def setup_camera(px: int) -> bpy.types.Object:
    scene = bpy.context.scene
    cam_data = bpy.data.cameras.new("sprite_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = ORTHO_SCALE
    cam = bpy.data.objects.new("sprite_cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    # looking at the middle of the figure from the front, tilted down
    el = math.radians(ELEVATION)
    dist = 4.0
    target = Vector((0, 0, 0.52))
    cam.location = target + Vector((0, -math.cos(el), math.sin(el))) * dist
    cam.rotation_euler = (math.radians(90) - el, 0, 0)
    scene.render.resolution_x = scene.render.resolution_y = px
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.filter_size = 0.0                    # no blur between pixels
    try:
        scene.display.render_aa = "OFF"               # Workbench: hard edges
        # Flat, not studio-lit. A 32-pixel sprite has no room for a gradient: smooth shading
        # turns every rounded form into grey mush, while flat object colour keeps the shapes
        # readable, which is how the reference pixel art is drawn.
        scene.display.shading.light = "FLAT"
        scene.display.shading.color_type = "OBJECT"
        scene.display.shading.show_object_outline = True
        scene.display.shading.object_outline_color = (0.05, 0.04, 0.06)
    except (AttributeError, TypeError):
        pass
    return cam


def pivot_pixels(cam: bpy.types.Object, px: int) -> tuple[int, int]:
    """Where the ground under the rig lands in the rendered frame."""
    scene = bpy.context.scene
    co = world_to_camera_view(scene, cam, Vector((0.0, 0.0, 0.0)))
    return int(round(co.x * px)), int(round((1.0 - co.y) * px))


def render_clips(rig: bpy.types.Object, cam: bpy.types.Object, out: Path, px: int) -> dict:
    scene = bpy.context.scene
    clips: dict[str, dict] = {}
    out.mkdir(parents=True, exist_ok=True)
    for action in sorted(bpy.data.actions, key=clip_rank):
        name = action.name
        rig.animation_data.action = action
        first, last = (int(action.frame_range[0]), int(action.frame_range[1]))
        count = last - first + 1
        clips[name] = {"fps": FPS.get(name, 8.0), "loop": LOOP.get(name, True), "count": count}
        for direction, turn in DIRS.items():
            rig.rotation_euler = (0.0, 0.0, math.radians(turn))
            for n in range(count):
                scene.frame_set(first + n)
                scene.render.filepath = str(out / f"{name}_{direction}_{n:04d}")
                bpy.ops.render.render(write_still=True)
    return clips


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--id", default="dao_si")
    ap.add_argument("--name-vi", default="Đạo Sĩ")
    ap.add_argument("--render-px", type=int, default=256)
    ap.add_argument("--frame-px", type=int, default=32,
                    help="the size the packer scales down to (plan 7.1: render big, then "
                         "nearest-neighbour down to pixel-art size)")
    ap.add_argument("--out", default="")
    args = ap.parse_args(argv)

    rig = bpy.data.objects.get("rig")
    if rig is None:
        print("render_character: this .blend has no object called 'rig' "
              "(run tools/blender/build_character.py first)", file=sys.stderr)
        return 1
    if args.render_px % args.frame_px:
        print(f"render_character: --render-px {args.render_px} is not a whole multiple of "
              f"--frame-px {args.frame_px}", file=sys.stderr)
        return 1

    engine = pick_engine()
    cam = setup_camera(args.render_px)
    out = Path(args.out) if args.out else RENDER_DIR / args.id
    clips = render_clips(rig, cam, out, args.render_px)
    meta = {"id": args.id, "name_vi": args.name_vi, "source": "tools/blender/render_character.py",
            "engine": engine, "render_px": args.render_px, "frame_px": args.frame_px,
            "pivot_px": list(pivot_pixels(cam, args.render_px)),
            "dirs": list(DIRS), "clips": clips}
    (out / "render.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n",
                                     "utf-8", newline="\n")
    total = sum(c["count"] for c in clips.values()) * len(DIRS)
    print(f"rendered {args.id} with {engine}: {total} frames of {args.render_px}px "
          f"({', '.join(clips)}), pivot {meta['pivot_px']}")
    print(f"wrote {out / 'render.json'}")
    return 0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(argv))
