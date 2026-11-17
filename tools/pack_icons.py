#!/usr/bin/env python3
"""Pack the rendered item icons into one sheet the game loads (M8).

    python tools/pack_icons.py                 # art/render_items -> client/assets/icons/

Reads `art/render_items/items.json` (written by tools/blender/render_item.py) and writes:

    client/assets/icons/items.png     every icon in a grid, 32x32 each
    client/assets/icons/items.json    name -> index, plus where each one came from

Several models can answer to the same name - three swords, two bows - so the sheet keeps
them all and the JSON lists them per name: `kiem` has three, and whatever picks an icon can
take the first or vary them. The licence of each model travels with it, because a CC-BY
model still needs its credit when its picture ships in the game.

Scaling down is nearest-neighbour, like the character sheets: smooth scaling turns a
3-pixel sword into grey soup.
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

SRC = ROOT / "art" / "render_items"
OUT = ROOT / "client" / "assets" / "icons"
CELL = 32
MIN_DRAWN = 12          # fewer opaque pixels than this and the icon is blank


class IconError(Exception):
    pass


def _ready() -> None:
    if not pygame.display.get_init():
        pygame.display.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))


def pack(src: Path = SRC, out: Path = OUT, cell: int = CELL) -> dict:
    _ready()
    index_file = src / "items.json"
    if not index_file.exists():
        raise IconError(f"no {index_file} (run tools/blender/render_item.py first)")
    icons = json.loads(index_file.read_text("utf-8"))["icons"]
    if not icons:
        raise IconError("items.json lists no icons")

    icons = sorted(icons, key=lambda i: (i["kind"], i["slug"], i["file"]))
    surfaces, entries, blank = [], {}, []
    for n, it in enumerate(icons):
        png = src / it["file"]
        if not png.exists():
            raise IconError(f"{it['file']} is missing")
        big = pygame.image.load(str(png)).convert_alpha()
        small = pygame.Surface((cell, cell), pygame.SRCALPHA)
        pygame.transform.scale(big, (cell, cell), small)      # nearest neighbour
        drawn = sum(1 for y in range(cell) for x in range(cell) if small.get_at((x, y))[3] > 8)
        if drawn < MIN_DRAWN:
            blank.append(f"{it['kind']}/{it['slug']} ({it['title']})")
            continue
        surfaces.append(small)
        entries.setdefault(it["slug"], []).append({
            "index": len(surfaces) - 1, "kind": it["kind"], "title": it["title"],
            "creator": it["creator"], "licence": it["licence"]})
    if blank:
        raise IconError("these rendered blank, so they are not packed: " + "; ".join(blank))

    cols = min(8, len(surfaces))
    rows = math.ceil(len(surfaces) / cols)
    sheet = pygame.Surface((cols * cell, rows * cell), pygame.SRCALPHA)
    for n, s in enumerate(surfaces):
        sheet.blit(s, ((n % cols) * cell, (n // cols) * cell))
    out.mkdir(parents=True, exist_ok=True)
    pygame.image.save(sheet, str(out / "items.png"))
    doc = {
        "_comment": "Built by tools/pack_icons.py from art/render_items/. Do not edit by hand. "
                    "Models that are CC-BY keep their credit in CREDITS.md.",
        "sheet": "items.png", "cell": cell, "cols": cols, "count": len(surfaces),
        "icons": entries,
    }
    (out / "items.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                                    "utf-8", newline="\n")
    return doc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--cell", type=int, default=CELL)
    args = ap.parse_args(argv)
    pygame.init()
    try:
        doc = pack(cell=args.cell)
    except IconError as e:
        print(f"pack_icons: {e}", file=sys.stderr)
        return 1
    names = ", ".join(f"{k}×{len(v)}" if len(v) > 1 else k for k, v in sorted(doc["icons"].items()))
    by = sum(1 for v in doc["icons"].values() for i in v if i["licence"] != "CC0"
             and i["licence"] != "own work")
    print(f"wrote {doc['count']} icons of {doc['cell']}px ({doc['cols']} per row) "
          f"to client/assets/icons/")
    print(f"  names: {names}")
    print(f"  {by} of them are CC-BY and must keep their credit in CREDITS.md")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
