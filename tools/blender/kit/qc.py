#!/usr/bin/env python3
"""Quality gate for kit output folders (docs/ART_PIPELINE.md section 6).

    python tools/blender/kit/qc.py client/assets/v2/chars [more folders or .json files...]

Checks every .json in the folder(s), by kind:
  animated sheet  JSON and sheet agree, required clips in all 4 facings, pivot steady (feet
                  on the pivot row, no sideways drift in idle/walk), nothing cut at the frame
                  edge, transparent corners, hard alpha (0/255), colours in the palette
  FX sheet        same grid checks; soft alpha allowed; blend add|alpha
  icon atlas      every icon drawn, inside its cell with a margin, hard alpha, palette
  tileset         16 px grid, indices valid, seams (the wrap score the kit recorded), palette
  props atlas     rects inside the atlas, pivot inside the rect, hard alpha, palette
Pure Python (reads the PNGs itself): runs in the venv or in Blender. Exit code 0 = pass.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from kit import palette as P, png  # noqa: E402
else:
    from . import palette as P, png

DIRS = ("down", "left", "up", "right")
REQUIRED = {
    "player": ("idle", "walk", "slash", "cast", "shoot", "hit", "die", "meditate", "fly", "dodge"),
    "monster": ("idle", "walk", "windup", "attack", "hit", "die"),
    "elite": ("idle", "walk", "windup", "attack", "hit", "die"),
    "beast": ("idle", "walk", "windup", "attack", "hit", "die"),
    "boss": ("idle", "walk", "windup", "attack", "hit", "die", "special"),
}
STEADY_Y = ("idle", "walk", "slash", "cast", "shoot", "hit", "windup", "attack")
GROUND_CLIPS = ("die", "sleep")     # lying down: never held to the standing rule
STEADY_X = ("idle", "walk")
DRIFT_PX = 4        # feet centre may move this far sideways in idle/walk (64 px frames)
JITTER_PX = 2       # lowest row may move this much within one idle/walk facing (64 px)


def feet_limits(fh: int) -> tuple[float, float]:
    """(drift, jitter) in px: today's 4 / 2 for frames up to 64 px, scaled above that."""
    k = max(1.0, fh / 64.0)
    return DRIFT_PX * k, JITTER_PX * k


def measure(drawn, fw: int, fh: int, px: float):
    """(lowest row, feet x) of one frame; `drawn(x, y)` says whether a pixel counts.

    Up to 64 px: the lowest drawn row anywhere and the middle of the lowest 3 rows (the M8
    rule, unchanged). Above 64 px the *planted foot* is judged: only pixels within a
    quarter frame of the pivot x count, the lowest row there is the planted foot's row, and
    the feet x is the middle of the run of that row nearest the pivot (the other foot may
    swing freely in a long stride)."""
    if fh <= 64:
        bottom = -1
        for y in range(fh - 1, -1, -1):
            if any(drawn(x, y) for x in range(fw)):
                bottom = y
                break
        if bottom < 0:
            return None, None
        xs = [x for y in range(max(0, bottom - 2), bottom + 1) for x in range(fw) if drawn(x, y)]
        return bottom, ((min(xs) + max(xs)) / 2 if xs else None)
    half = fw / 4.0
    cols = [x for x in range(fw) if abs(x + 0.5 - px) <= half]
    bottom = -1
    for y in range(fh - 1, -1, -1):
        if any(drawn(x, y) for x in cols):
            bottom = y
            break
    if bottom < 0:
        return None, None
    runs, run = [], []
    for x in cols:
        if drawn(x, bottom):
            run.append(x)
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    best = min(runs, key=lambda r: abs((r[0] + r[-1]) / 2 + 0.5 - px))
    return bottom, (best[0] + best[-1]) / 2


class Img:
    def __init__(self, path: Path):
        self.w, self.h, self.px = png.read(path)

    def rgba(self, x, y):
        i = (y * self.w + x) * 4
        return self.px[i], self.px[i + 1], self.px[i + 2], self.px[i + 3]

    def alpha(self, x, y):
        return self.px[(y * self.w + x) * 4 + 3]


def cell_stats(img: Img, x0, y0, w, h, colors: set, soft_ok=False):
    """bbox of drawn pixels, soft-alpha count, off-palette colours, rows of feet."""
    left = top = 10 ** 9
    right = bottom = -1
    soft = 0
    off = set()
    for y in range(y0, y0 + h):
        base = (y * img.w + x0) * 4
        row = img.px[base:base + w * 4]
        for x in range(w):
            a = row[x * 4 + 3]
            if not a:
                continue
            if a != 255:
                soft += 1
            c = (row[x * 4], row[x * 4 + 1], row[x * 4 + 2])
            if c not in colors:
                off.add(c)
            left, right = min(left, x), max(right, x)
            top, bottom = min(top, y - y0), max(bottom, y - y0)
    box = None if right < 0 else (left, top, right, bottom)
    return box, soft, off


def check_grid(name, doc, img, fw, fh, total, cols, colors, soft_ok, out, below_ok=None):
    """below_ok: optional per-frame list; True = drawn pixels at the bottom edge belong to
    qc_ignore objects only (a resting sword tip) and are not reported."""
    rows = -(-total // cols)
    if (img.w, img.h) != (cols * fw, rows * fh):
        out.append(f"{name}: sheet is {img.w}x{img.h}, {total} frames of {fw}x{fh} at {cols} "
                   f"per row need {cols * fw}x{rows * fh}")
        return None
    boxes = []
    for n in range(total):
        x0, y0 = (n % cols) * fw, (n // cols) * fh
        box, soft, off = cell_stats(img, x0, y0, fw, fh, colors, soft_ok)
        where = f"{name} frame {n}"
        if box is None:
            out.append(f"{where}: empty")
        else:
            l, t, r, b = box
            low = b == fh - 1 and not (below_ok and below_ok[n])
            if l == 0 or t == 0 or r == fw - 1 or low:
                out.append(f"{where}: drawn pixels touch the frame edge (box {l},{t}..{r},{b})")
        if soft and not soft_ok:
            out.append(f"{where}: {soft} pixels with soft alpha (must be 0 or 255)")
        if off:
            out.append(f"{where}: {len(off)} colours not in the palette, e.g. {sorted(off)[:3]}")
        boxes.append(box)
    return boxes


def check_animated(path: Path, doc: dict, colors: set) -> list[str]:
    out = []
    name = doc.get("id", path.stem)
    img = Img(path.parent / doc["sheet"])
    fw, fh = int(doc["frame"]["w"]), int(doc["frame"]["h"])
    cols, total = int(doc["cols"]), int(doc["frames"])
    kind = doc.get("render", {}).get("kind")
    layer = doc.get("render", {}).get("layer", False)
    used = set()
    for clip in REQUIRED.get(kind, ()):
        c = doc["clips"].get(clip)
        if c is None:
            out.append(f"{name}: no {clip!r} clip (required for a {kind})")
        elif any(d not in c.get("frames", {}) for d in DIRS):
            out.append(f"{name}/{clip}: not all four facings")
    for clip, c in doc["clips"].items():
        if float(c.get("fps", 0)) <= 0:
            out.append(f"{name}/{clip}: fps {c.get('fps')!r}")
        counts = {len(v) for v in c.get("frames", {}).values()}
        if len(counts) > 1:
            out.append(f"{name}/{clip}: facings have different frame counts {counts}")
        for d, ids in c.get("frames", {}).items():
            for i in ids:
                if not 0 <= i < total:
                    out.append(f"{name}/{clip}/{d}: frame {i} outside the {total} in the sheet")
                used.add(i)
    for clip, ev in doc.get("events", {}).items():
        c = doc["clips"].get(clip)
        n = len(next(iter(c["frames"].values()))) if c else 0
        for k, v in ev.items():
            if not (c and 0 <= int(v) < n):
                out.append(f"{name}: event {clip}.{k}={v} is not a frame of that clip")
    if len(used) != total:
        out.append(f"{name}: {total - len(used)} frame(s) no clip shows")
    if out:
        return out
    px, py = float(doc["pivot"]["x"]), float(doc["pivot"]["y"])
    qf = doc.get("render", {}).get("qc_frames")      # kit-measured, qc_ignore objects left out
    if qf is not None and len(qf) != total:
        out.append(f"{name}: render.qc_frames has {len(qf)} entries for {total} frames")
        return out
    below_ok = [bool(f[2]) for f in qf] if qf else None
    boxes = check_grid(name, doc, img, fw, fh, total, cols, colors, False, out, below_ok)
    if boxes is None or layer:
        return out
    drift_px, jitter_px = feet_limits(fh)
    ground = set(doc.get("render", {}).get("ground_clips") or GROUND_CLIPS)
    elev = float(doc.get("render", {}).get("elevation", 35.0))
    for clip, c in doc["clips"].items():
        for d, ids in c["frames"].items():
            bottoms, feet = [], []
            for i in ids:
                if boxes[i] is None:
                    continue
                if qf:
                    bot, fx = qf[i][0], qf[i][1]
                else:
                    x0, y0 = (i % cols) * fw, (i // cols) * fh
                    bot, fx = measure(lambda x, y: img.alpha(x0 + x, y0 + y), fw, fh, px)
                if bot is None:
                    continue
                bottoms.append(bot)
                if clip in STEADY_X and fx is not None:
                    feet.append(fx)
            # Seen from 35 degrees, what stands in front of the origin draws below the
            # pivot, so the lowest row may sit a few px under it, but not far, and not above.
            # less ground shows at a flatter camera: scale the band with sin(elevation)
            foot = max(4.0, fh / 12 * math.sin(math.radians(elev)) / math.sin(math.radians(35.0)))
            if clip in STEADY_Y and clip in ground and bottoms:
                # a declared lying-down / collapsing clip: may spread up to a quarter of the
                # frame below the pivot, but must still not float above it
                below = max(b + 1 - py for b in bottoms)
                above = max(py - (b + 1) for b in bottoms)
                if below > max(foot, fh / 4) or above > foot:
                    out.append(f"{name}/{clip}/{d}: lowest row {below:.0f}px below / {above:.0f}px "
                               f"above the pivot y={py:.0f} (ground clip: max {max(foot, fh / 4):.0f} "
                               f"below, {foot:.0f} above)")
            elif clip in STEADY_Y and bottoms:
                worst = max(abs(b + 1 - py) for b in bottoms)
                if worst > foot:
                    out.append(f"{name}/{clip}/{d}: lowest row is {worst:.0f}px from the pivot "
                               f"y={py:.0f} (more than {foot:.0f}: it will float or sink)")
            if clip in STEADY_X and bottoms and max(bottoms) - min(bottoms) > jitter_px:
                out.append(f"{name}/{clip}/{d}: lowest row jumps {min(bottoms)}..{max(bottoms)} "
                           f"between frames (feet jitter)")
            if feet and max(abs(f - px) for f in feet) > drift_px:
                out.append(f"{name}/{clip}/{d}: feet drift sideways from pivot x={px:.0f} "
                           f"(feet at {min(feet):.0f}..{max(feet):.0f})")
    return out


def check_fx(path, doc, colors):
    out = []
    name = doc.get("id", path.stem)
    img = Img(path.parent / doc["sheet"])
    if doc.get("blend") not in ("add", "alpha"):
        out.append(f"{name}: blend must be add or alpha, not {doc.get('blend')!r}")
    for k in ("fps", "loop", "ground", "pivot", "frames", "cols"):
        if k not in doc:
            out.append(f"{name}: no {k!r}")
    if out:
        return out
    check_grid(name, doc, img, int(doc["frame"]["w"]), int(doc["frame"]["h"]),
               int(doc["frames"]), int(doc["cols"]), colors, True, out)
    return out


def check_icons(path, doc, colors):
    out = []
    img = Img(path.parent / doc["sheet"])
    cell, cols = int(doc["cell"]), int(doc["cols"])
    n = len(doc["icons"])
    idx = sorted(v["index"] for v in doc["icons"].values())
    if idx != list(range(n)):
        out.append(f"{path.stem}: icon indices are not 0..{n - 1}: {idx}")
    for iid, v in doc["icons"].items():
        if not 1 <= int(v.get("grade", 1)) <= 10:
            out.append(f"{path.stem}/{iid}: grade {v.get('grade')}")
        i = v["index"]
        x0, y0 = (i % cols) * cell, (i // cols) * cell
        if x0 + cell > img.w or y0 + cell > img.h:
            out.append(f"{path.stem}/{iid}: cell {i} outside the sheet")
            continue
        box, soft, off = cell_stats(img, x0, y0, cell, cell, colors)
        if box is None:
            out.append(f"{path.stem}/{iid}: empty")
            continue
        l, t, r, b = box
        if l == 0 or t == 0 or r == cell - 1 or b == cell - 1:
            out.append(f"{path.stem}/{iid}: touches the cell edge")
        if soft:
            out.append(f"{path.stem}/{iid}: soft alpha")
        if off:
            out.append(f"{path.stem}/{iid}: colours not in the palette {sorted(off)[:3]}")
    return out


def check_tiles(path, doc, colors):
    out = []
    img = Img(path.parent / doc["sheet"])
    cols = int(doc["cols"])
    count = (img.w // 16) * (img.h // 16)
    if img.w % 16 or img.h % 16:
        out.append(f"{path.stem}: sheet {img.w}x{img.h} is not on the 16 px grid")
    for name, ids in doc["tiles"].items():
        for i in ids:
            if not 0 <= i < count:
                out.append(f"{path.stem}/{name}: tile {i} outside the sheet")
                continue
            box, soft, off = cell_stats(img, (i % cols) * 16, (i // cols) * 16, 16, 16, colors)
            if box is None:
                out.append(f"{path.stem}/{name}: tile {i} empty")
            if soft:
                out.append(f"{path.stem}/{name}: tile {i} soft alpha")
            if off:
                out.append(f"{path.stem}/{name}: tile {i} colours not in the palette")
    for k, v in doc.get("render", {}).get("wrap_check", {}).items():
        if v > 2.0:
            out.append(f"{path.stem}/{k}: seam score {v} (> 2: visible seam when tiled)")
    return out


def check_props(path, doc, colors):
    out = []
    img = Img(path.parent / doc["sheet"])
    for name, p in doc["props"].items():
        x, y, w, h = p["rect"]
        n = int(p.get("frames", 1))
        if x < 0 or y < 0 or x + w * n > img.w or y + h > img.h:
            out.append(f"{path.stem}/{name}: rect outside the atlas")
            continue
        px, py = p["pivot"]
        if not (0 <= px <= w and 0 <= py <= h):
            out.append(f"{path.stem}/{name}: pivot {px},{py} outside {w}x{h}")
        for k in range(n):
            box, soft, off = cell_stats(img, x + k * w, y, w, h, colors)
            if box is None:
                out.append(f"{path.stem}/{name}: frame {k} empty")
                continue
            l, t, r, b = box
            if l == 0 or t == 0 or r == w - 1 or b == h - 1:
                out.append(f"{path.stem}/{name}: frame {k} touches its rect edge")
            if soft:
                out.append(f"{path.stem}/{name}: soft alpha")
            if off:
                out.append(f"{path.stem}/{name}: colours not in the palette {sorted(off)[:3]}")
    return out


def check_file(path: Path, colors: set) -> list[str]:
    try:
        doc = json.loads(path.read_text("utf-8"))
    except ValueError as e:
        return [f"{path.name}: {e}"]
    sheet = path.parent / doc.get("sheet", f"{path.stem}.png")
    if not sheet.exists():
        return [f"{path.name}: no sheet {sheet.name}"]
    try:
        if "clips" in doc:
            return check_animated(path, doc, colors)
        if "blend" in doc:
            return check_fx(path, doc, colors)
        if "icons" in doc:
            return check_icons(path, doc, colors)
        if "tiles" in doc:
            return check_tiles(path, doc, colors)
        if "props" in doc:
            return check_props(path, doc, colors)
    except (KeyError, TypeError, ValueError) as e:
        return [f"{path.name}: malformed ({e!r})"]
    return [f"{path.name}: unknown kind of json"]


def check_folder(folder: Path) -> tuple[int, list[str]]:
    """A folder (every .json under it) or a single .json file."""
    colors = P.load().color_set
    folder = Path(folder)
    if folder.is_file():
        files = [folder]
    elif folder.exists():
        files = sorted(folder.rglob("*.json"))
    else:
        return 0, [f"{folder}: no such file or folder"]
    probs = []
    for f in files:
        probs += check_file(f, colors)
    return len(files), probs


def report(folder: Path) -> int:
    n, probs = check_folder(folder)
    for p in probs:
        print(f" - {p}")
    print(f"qc {folder}: {'FAIL' if probs else 'OK'} ({n} file(s), {len(probs)} problem(s))")
    return len(probs)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    bad = sum(report(Path(a)) for a in argv)
    return 1 if bad else 0


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
