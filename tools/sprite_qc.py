#!/usr/bin/env python3
"""Quality checks for the packed character sheets (M8, kế hoạch 7.3).

    python tools/sprite_qc.py          # every character in client/assets/chars/

The five things the plan asks for, and what each one really means in pixels:

1. **The pivot is the same between frames** - the character must not slide. The pivot is
   declared once per character (the camera's ground point), so what is checked here is that
   every frame is actually drawn around it: the middle of the drawn pixels stays within
   `DRIFT_PX` of the pivot's x, and the lowest drawn row within `FOOT_PX` of its y. A frame
   whose feet wander is a frame that will skate across the ground in game.
2. **Nothing is cut off at the frame edge** - no opaque pixel may touch the border, or an
   arm has been sliced by the camera.
3. **The background is really transparent** - the corners are empty and most of the frame
   is, too. A render that forgot "Film > Transparent" comes back with a grey sky that looks
   fine in a viewer and square in the game.
4. **The JSON and the sheet agree** - every frame index exists, every clip has a positive
   fps and at least one frame in each direction. Every character also has the clips the
   game plays by name (`REQUIRED_CLIPS`: idle, walk, slash, and M9's cast for the Pháp
   thuật / Trận pháp chiêu) in all four facings - the game falls back rather than crash
   when one is missing, but a fallback is a bug nobody sees, so the check says so.
5. **One frame size for every character** - so two characters stand the same height.

Exit code 0 when every character passes, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402

CHARS_DIR = ROOT / "client" / "assets" / "chars"
DRIFT_PX = 6.0          # how far the drawn middle may sit from the pivot's x
FOOT_PX = 4.0           # how far the lowest drawn row may sit from the pivot's y
ALPHA = 8               # below this, a pixel counts as empty
MIN_EMPTY = 0.35        # at least this share of a frame is background
MIN_DRAWN = 30          # a frame with fewer drawn pixels than this is empty, not a drawing
REQUIRED_CLIPS = ("idle", "walk", "slash", "cast")
DIRS = ("down", "up", "left", "right")


def _ready() -> None:
    """A surface cannot be converted before a display exists, even with the dummy driver -
    and these tools run from the command line, where nobody has opened a window."""
    if not pygame.display.get_init():
        pygame.display.init()
    if pygame.display.get_surface() is None:      # init() alone is not enough to convert
        pygame.display.set_mode((1, 1))


def _bbox(surf: pygame.Surface) -> tuple[int, int, int, int] | None:
    """(left, top, right, bottom) of the drawn pixels, or None when nothing is drawn."""
    w, h = surf.get_size()
    left, top, right, bottom = w, h, -1, -1
    drawn = 0
    for y in range(h):
        for x in range(w):
            if surf.get_at((x, y))[3] >= ALPHA:
                drawn += 1
                left, right = min(left, x), max(right, x)
                top, bottom = min(top, y), max(bottom, y)
    if right < 0 or drawn < MIN_DRAWN:
        return None
    return left, top, right, bottom


def _frame(sheet: pygame.Surface, n: int, fw: int, fh: int, cols: int) -> pygame.Surface:
    return sheet.subsurface(((n % cols) * fw, (n // cols) * fh, fw, fh))


def check_character(doc_path: Path) -> list[str]:
    """Every problem with this one character, as lines a person can act on."""
    out: list[str] = []
    _ready()
    name = doc_path.stem
    try:
        doc = json.loads(doc_path.read_text("utf-8"))
    except ValueError as e:
        return [f"{name}.json: {e}"]
    png = doc_path.parent / doc.get("sheet", "")
    if not png.exists():
        return [f"{name}: no sheet {doc.get('sheet')!r} next to the json"]
    sheet = pygame.image.load(str(png)).convert_alpha()
    fw, fh = int(doc["frame"]["w"]), int(doc["frame"]["h"])
    cols = int(doc["cols"])
    total = int(doc["frames"])
    rows = -(-total // cols)
    if sheet.get_size() != (cols * fw, rows * fh):
        out.append(f"{name}: the sheet is {sheet.get_size()}, but {total} frames of {fw}x{fh} "
                   f"at {cols} per row need {(cols * fw, rows * fh)}")
        return out

    # ---- 4: the JSON and the sheet agree
    used: set[int] = set()
    for clip in REQUIRED_CLIPS:
        c = doc["clips"].get(clip)
        if c is None:
            out.append(f"{name}: no {clip!r} clip (the game plays it by name)")
            continue
        missing = [d for d in DIRS if d not in (c.get("frames") or {})]
        if missing:
            out.append(f"{name}/{clip}: no frames facing {', '.join(missing)}")
    for clip, c in doc["clips"].items():
        if float(c.get("fps", 0)) <= 0:
            out.append(f"{name}/{clip}: fps is {c.get('fps')!r}")
        if not c.get("frames"):
            out.append(f"{name}/{clip}: no directions at all")
        for d, ids in (c.get("frames") or {}).items():
            if not ids:
                out.append(f"{name}/{clip}/{d}: no frames")
            for i in ids:
                if not 0 <= i < total:
                    out.append(f"{name}/{clip}/{d}: frame {i} is outside the {total} in the sheet")
                else:
                    used.add(i)
    if len(used) != total:
        out.append(f"{name}: {total - len(used)} frame(s) in the sheet no clip ever shows")
    if out:
        return out                      # the rest would only repeat a broken index

    px, py = float(doc["pivot"]["x"]), float(doc["pivot"]["y"])
    if not (0 <= px <= fw and 0 <= py <= fh):
        out.append(f"{name}: the pivot {px},{py} is outside the {fw}x{fh} frame")
    for n in sorted(used):
        f = _frame(sheet, n, fw, fh, cols)
        where = f"{name} frame {n}"
        # ---- 3: the background is really transparent
        corners = [f.get_at((0, 0)), f.get_at((fw - 1, 0)), f.get_at((0, fh - 1)),
                   f.get_at((fw - 1, fh - 1))]
        if any(c[3] >= ALPHA for c in corners):
            out.append(f"{where}: a corner is not transparent (alpha "
                       f"{[c[3] for c in corners]}) - was the render not set to transparent?")
            continue
        box = _bbox(f)
        if box is None:
            out.append(f"{where}: nothing is drawn in it")
            continue
        left, top, right, bottom = box
        empty = 1 - ((right - left + 1) * (bottom - top + 1)) / (fw * fh)
        if empty < MIN_EMPTY:
            out.append(f"{where}: the drawing fills {(1 - empty) * 100:.0f}% of the frame, "
                       f"so the camera is too close")
        # ---- 2: nothing is cut off at the edge
        if left == 0 or top == 0 or right == fw - 1 or bottom == fh - 1:
            out.append(f"{where}: drawn pixels touch the frame edge "
                       f"(box {left},{top}..{right},{bottom}) - something is cut off")
        # ---- 1: the pivot holds still
        mid = (left + right) / 2
        if abs(mid - px) > DRIFT_PX:
            out.append(f"{where}: its middle is at x={mid:.1f} but the pivot is {px} "
                       f"({abs(mid - px):.1f}px off, more than {DRIFT_PX}) - it will slide")
        if abs(bottom - py) > FOOT_PX:
            out.append(f"{where}: its lowest pixel is y={bottom} but the pivot is {py} "
                       f"({abs(bottom - py):.1f}px off, more than {FOOT_PX}) - it will float")
    return out


def check_all(chars_dir: Path = CHARS_DIR) -> list[str]:
    """Every problem with every character, plus the one rule that spans them (5)."""
    if not chars_dir.exists():
        return []                       # nothing rendered yet: M8 has not run here
    docs = sorted(chars_dir.glob("*.json"))
    out: list[str] = []
    sizes: dict[tuple[int, int], list[str]] = {}
    for d in docs:
        out += check_character(d)
        try:
            doc = json.loads(d.read_text("utf-8"))
            sizes.setdefault((int(doc["frame"]["w"]), int(doc["frame"]["h"])), []).append(doc["id"])
        except (ValueError, KeyError):
            pass                        # already reported by check_character
    if len(sizes) > 1:
        out.append("characters do not share one frame size: "
                   + "; ".join(f"{w}x{h}: {', '.join(ids)}" for (w, h), ids in sorted(sizes.items())))
    return out


def main(argv: list[str] | None = None) -> int:
    pygame.init()
    problems = check_all()
    if not (CHARS_DIR.exists() and list(CHARS_DIR.glob("*.json"))):
        print("sprite_qc: no character sheets yet (run tools/blender/render_character.py "
              "then tools/pack_sprites.py)")
        return 0
    for p in problems:
        print(f" - {p}")
    print(f"sprite_qc: {'FAIL' if problems else 'OK'} "
          f"({len(list(CHARS_DIR.glob('*.json')))} character(s), {len(problems)} problem(s))")
    return 1 if problems else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
