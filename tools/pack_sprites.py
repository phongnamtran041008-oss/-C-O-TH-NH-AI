#!/usr/bin/env python3
"""Pack rendered character frames into one sprite sheet plus a JSON the game reads (M8,
kế hoạch 7.1 bước 4).

    python tools/pack_sprites.py dao_si            # art/render/dao_si -> client/assets/chars/
    python tools/pack_sprites.py --all

**What it eats.** A folder written by tools/blender/render_character.py:

    art/render/<id>/render.json
    art/render/<id>/<clip>_<dir>_0000.png ...      (RGBA, rendered big)

`render.json` is the renderer's own account of what it did, and the packer trusts it for the
things pixels cannot tell you:

    {"id": "dao_si", "name_vi": "Đạo Sĩ", "render_px": 256, "frame_px": 64,
     "pivot_px": [128, 232],            # where the camera put the character's feet
     "dirs": ["down", "up", "left", "right"],
     "clips": {"idle": {"fps": 6, "loop": true, "count": 4}, ...}}

The **pivot comes from the camera, never from the pixels**: it is the ground point under the
rig, projected by the same orthographic camera every frame, so it cannot drift. Guessing it
from the drawn pixels would make a character that waves its sleeve walk sideways.

**What it writes.** `client/assets/chars/<id>.png` (frames laid out in a grid, row-major) and
`client/assets/chars/<id>.json`:

    {"id", "name_vi", "frame": {"w", "h"}, "pivot": {"x", "y"}, "sheet", "cols",
     "clips": {"<clip>": {"fps", "loop", "frames": {"<dir>": [index, ...]}}}}

Frames are indices into that grid, so two clips may share a frame and a direction may be a
different number of frames from its neighbours.

Scaling down is nearest-neighbour on purpose (plan 7.1 bước 3): the game is pixel art, and
smooth scaling turns a 3-pixel sword into grey soup.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

RENDER_DIR = ROOT / "art" / "render"
OUT_DIR = ROOT / "client" / "assets" / "chars"
DIRS = ("down", "up", "left", "right")


def _ready() -> None:
    """A surface cannot be converted before a display exists, even with the dummy driver -
    and these tools run from the command line, where nobody has opened a window."""
    if not pygame.display.get_init():
        pygame.display.init()
    if pygame.display.get_surface() is None:      # init() alone is not enough to convert
        pygame.display.set_mode((1, 1))


class PackError(Exception):
    pass


def _meta(folder: Path) -> dict:
    f = folder / "render.json"
    if not f.exists():
        raise PackError(f"{folder.name}: no render.json (did the render finish?)")
    try:
        return json.loads(f.read_text("utf-8"))
    except ValueError as e:
        raise PackError(f"{folder.name}/render.json: {e}") from None


def _frames(folder: Path, clip: str, direction: str, count: int) -> list[Path]:
    out = []
    for n in range(count):
        p = folder / f"{clip}_{direction}_{n:04d}.png"
        if not p.exists():
            raise PackError(f"{folder.name}: {p.name} is missing")
        out.append(p)
    return out


def pack(folder: Path, out_dir: Path = OUT_DIR) -> dict:
    """Pack one character. Returns the JSON that was written."""
    _ready()
    meta = _meta(folder)
    render_px, frame_px = int(meta["render_px"]), int(meta["frame_px"])
    if render_px % frame_px:
        raise PackError(f"{folder.name}: render_px {render_px} is not a whole multiple of "
                        f"frame_px {frame_px}, so nearest-neighbour would blur it")
    scale = render_px // frame_px
    dirs = list(meta.get("dirs") or DIRS)
    clips = meta["clips"]

    surfaces: list[pygame.Surface] = []
    index: dict[str, dict[str, list[int]]] = {}
    for clip, c in clips.items():
        index[clip] = {}
        for d in dirs:
            ids = []
            for p in _frames(folder, clip, d, int(c["count"])):
                img = pygame.image.load(str(p)).convert_alpha()
                if img.get_size() != (render_px, render_px):
                    raise PackError(f"{p.name} is {img.get_size()}, not "
                                    f"{(render_px, render_px)}")
                small = pygame.Surface((frame_px, frame_px), pygame.SRCALPHA)
                pygame.transform.scale(img, (frame_px, frame_px), small)   # nearest neighbour
                ids.append(len(surfaces))
                surfaces.append(small)
            index[clip][d] = ids

    cols = max(1, min(8, len(surfaces)))
    rows = math.ceil(len(surfaces) / cols)
    sheet = pygame.Surface((cols * frame_px, rows * frame_px), pygame.SRCALPHA)
    for n, s in enumerate(surfaces):
        sheet.blit(s, ((n % cols) * frame_px, (n // cols) * frame_px))

    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{meta['id']}.png"
    pygame.image.save(sheet, str(png))
    px, py = meta["pivot_px"]
    doc = {
        "_comment": "Built by tools/pack_sprites.py from art/render/. Do not edit by hand.",
        "id": meta["id"],
        "name_vi": meta.get("name_vi", meta["id"]),
        "source": meta.get("source", ""),
        "frame": {"w": frame_px, "h": frame_px},
        "pivot": {"x": round(px / scale, 2), "y": round(py / scale, 2)},
        "sheet": png.name,
        "cols": cols,
        "frames": len(surfaces),
        "clips": {clip: {"fps": float(c["fps"]), "loop": bool(c.get("loop", True)),
                         "frames": index[clip]}
                  for clip, c in clips.items()},
    }
    (out_dir / f"{meta['id']}.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1) + "\n", "utf-8", newline="\n")
    return doc


def pack_all(out_dir: Path = OUT_DIR) -> list[dict]:
    if not RENDER_DIR.exists():
        raise PackError(f"nothing rendered yet: {RENDER_DIR} does not exist")
    folders = sorted(p for p in RENDER_DIR.iterdir() if (p / "render.json").exists())
    if not folders:
        raise PackError(f"no character folder with a render.json under {RENDER_DIR}")
    return [pack(f, out_dir) for f in folders]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ids", nargs="*", help="character ids under art/render/")
    ap.add_argument("--all", action="store_true", help="pack every character that was rendered")
    args = ap.parse_args(argv)
    pygame.init()
    try:
        docs = pack_all() if args.all or not args.ids else [pack(RENDER_DIR / i) for i in args.ids]
    except PackError as e:
        print(f"pack_sprites: {e}", file=sys.stderr)
        return 1
    for d in docs:
        clips = ", ".join(f"{k} x{len(v['frames'][next(iter(v['frames']))])}"
                          for k, v in d["clips"].items())
        print(f"wrote {d['id']}: {d['frames']} frames of {d['frame']['w']}px "
              f"({d['cols']} per row), pivot {d['pivot']['x']},{d['pivot']['y']} | {clips}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
