#!/usr/bin/env python3
"""A picture of a map, to look at a land before calling it done (docs/DAI_DIA_DO.md).

    python tools/preview_map.py loan_so_coc out.png                 the overview, 2 px per tile
    python tools/preview_map.py loan_so_coc out.png --scale 3
    python tools/preview_map.py loan_so_coc out.png --crop 150,210,30,17
                                                                     real tiles and props at the
                                                                     client's 2x zoom, x,y,w,h in tiles

The overview: the ground by tile colour, solid tiles darker, props as dots; khu borders and names
(white: a camp), monster areas tinted by band (green 1, amber 2, red 3; an elite's area outlined),
roads as they are painted, anchors (white cross), points of interest (yellow), signposts (cyan),
spawns and portals (magenta). The crop draws the ground with the v2 32 px tiles and every prop
with the picture the client would pick (magenta box: a sprite with no picture).
Made with pygame only (no Pillow, no numpy).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "server"))

import pygame  # noqa: E402

TILE = 16
COLORS = {
    "grass": (106, 153, 78), "flowers": (152, 176, 92), "path": (214, 190, 140), "water": (70, 130, 190),
    "bamboo_floor": (170, 160, 100), "stone": (150, 150, 145), "wood": (150, 105, 60), "plaza": (200, 190, 170),
    "dirt": (150, 120, 85), "dark_grass": (66, 110, 60), "ink": (40, 36, 60), "realm_floor": (120, 110, 150),
    "realm_wall": (60, 50, 80),
}
BAND = {0: (255, 255, 255), 1: (90, 220, 90), 2: (245, 180, 40), 3: (235, 60, 50)}
SOLID_SPRITES = {"tree", "ink_tree", "pine", "peach"}


def load(zone: str) -> dict:
    return json.loads((ROOT / "server" / "maps" / f"{zone}.tmj").read_text("utf-8"))


def props_of(o: dict) -> dict:
    return {p["name"]: p["value"] for p in o.get("properties", [])}


def font(size: int):
    path = ROOT / "client" / "assets" / "fonts" / "VT323-Regular.ttf"
    try:
        return pygame.font.Font(str(path), size)
    except (OSError, FileNotFoundError):
        return pygame.font.Font(None, size)


def solid_tiles(data: dict) -> set:
    out = set()
    for layer in data["layers"]:
        if layer["name"] != "collision":
            continue
        for o in layer["objects"]:
            if o["width"] >= TILE and o["height"] >= TILE:
                for ty in range(int(o["y"]) // TILE, (int(o["y"] + o["height"]) - 1) // TILE + 1):
                    for tx in range(int(o["x"]) // TILE, (int(o["x"] + o["width"]) - 1) // TILE + 1):
                        out.add((tx, ty))
    return out


def overview(zone: str, out: Path, scale: int = 2) -> None:
    from client.art.build import TILESET
    data = load(zone)
    W, H = data["width"], data["height"]
    names = [n for n, _ in TILESET]
    ground = next(l for l in data["layers"] if l["name"] == "ground")["data"]
    objs = next(l for l in data["layers"] if l["name"] == "objects")["objects"]
    hard = solid_tiles(data)
    s = scale
    img = pygame.Surface((W * s, H * s + 18 * 1))
    img.fill((20, 20, 20))
    for y in range(H):
        for x in range(W):
            gid = ground[y * W + x]
            c = COLORS.get(names[gid - 1], (255, 0, 255)) if gid else (0, 0, 0)
            if (x, y) in hard and names[gid - 1] not in ("water", "ink"):
                c = tuple(int(v * 0.62) for v in c)
            img.fill(c, (x * s, y * s, s, s))
    over = pygame.Surface(img.get_size(), pygame.SRCALPHA)
    for o in objs:
        p = props_of(o)
        if o["type"] == "monster_area":
            band = int(float(p.get("band", 0) or 0))
            col = BAND.get(band, (200, 200, 255))
            r = pygame.Rect(o["x"] / TILE * s, o["y"] / TILE * s, o["width"] / TILE * s, o["height"] / TILE * s)
            over.fill((*col, 60), r)
            if p.get("count") == "1":
                pygame.draw.rect(over, (*col, 230), r, 1)
    img.blit(over, (0, 0))
    for o in objs:
        p = props_of(o)
        fx, fy = (o["x"] + o["width"] / 2) / TILE * s, (o["y"] + o["height"]) / TILE * s
        if o["type"] == "prop" and p.get("sprite"):
            col = (25, 70, 30) if p["sprite"] in SOLID_SPRITES else (60, 60, 60)
            if p["sprite"] == "ink_tree":
                col = (30, 25, 45)
            img.fill(col, (int(fx), int(fy) - 1, max(1, s - 1), max(1, s - 1)))
    f = font(max(14, 7 * s))
    for o in objs:
        p = props_of(o)
        if o["type"] == "khu":
            band = int(float(p.get("band", 0) or 0))
            r = pygame.Rect(o["x"] / TILE * s, o["y"] / TILE * s, o["width"] / TILE * s, o["height"] / TILE * s)
            pygame.draw.rect(img, BAND[band], r, 1)
            ax, ay = float(p["anchor_x"]) / TILE * s, float(p["anchor_y"]) / TILE * s
            pygame.draw.line(img, (255, 255, 255), (ax - 3, ay), (ax + 3, ay))
            pygame.draw.line(img, (255, 255, 255), (ax, ay - 3), (ax, ay + 3))
            label = f.render(f"{p.get('name_vi', '')} [{band}]", True, BAND[band])
            img.blit(label, (r.x + 3, r.y + 2) if band else (r.right + 2, r.y))
    for o in objs:
        p = props_of(o)
        cx, cy = (o["x"] + o["width"] / 2) / TILE * s, (o["y"] + o["height"] / 2) / TILE * s
        if o["type"] == "poi":
            pygame.draw.circle(img, (255, 230, 60), (int(cx), int(cy)), max(3, s + 1), 1)
        elif o["type"] == "sign":
            img.fill((60, 230, 230), (int(cx) - 1, int(cy) - 1, 3, 3))
        elif o["type"] in ("spawn", "portal"):
            pygame.draw.circle(img, (255, 60, 255), (int(cx), int(cy)), 3)
        elif o["type"] in ("interact", "npc", "char"):
            pygame.draw.circle(img, (255, 255, 255), (int(cx), int(cy)), 2)
    legend = font(16).render(f"{zone}  {W}x{H}  - khu: band 1 green, 2 amber, 3 red, camp white; "
                             f"poi yellow, sign cyan, gate magenta", True, (230, 230, 230))
    img.blit(legend, (4, H * s + 1))
    pygame.image.save(img, str(out))


def crop(zone: str, out: Path, x0: int, y0: int, w: int, h: int) -> None:
    """Real tiles and props, as the client shows them at 2x zoom (one tile = 32 screen px)."""
    pygame.display.set_mode((1, 1))
    from client.engine import art2, sprites
    data = load(zone)
    W = data["width"]
    ground = next(l for l in data["layers"] if l["name"] == "ground")["data"]
    objs = next(l for l in data["layers"] if l["name"] == "objects")["objects"]
    z = 2
    ts = art2.tileset32()
    surf = pygame.Surface((w * TILE * z, h * TILE * z))
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            gid = ground[y * W + x]
            if ts is not None:
                surf.blit(ts.pick(gid - 1, x, y), ((x - x0) * 32, (y - y0) * 32))
    draw = []
    for o in objs:
        p = props_of(o)
        if not p.get("sprite") or o["type"] not in ("prop", "interact", "sign"):
            continue
        bx, by = (o["x"] + o["width"] / 2 - x0 * TILE) * z, (o["y"] + o["height"] - y0 * TILE) * z
        if not (-200 < bx < surf.get_width() + 200 and -200 < by < surf.get_height() + 300):
            continue
        pr = art2.prop_for(p["sprite"], int(p.get("variant", 0) or 0))
        if pr is not None:
            draw.append((by, pr.at(0), (int(bx - pr.pivot[0]), int(by - pr.pivot[1]))))
            continue
        try:
            im = sprites.prop(p["sprite"], int(p.get("variant", 0) or 0))
            im = pygame.transform.scale(im, (im.get_width() * z, im.get_height() * z))
            draw.append((by, im, (int(bx - im.get_width() / 2), int(by - im.get_height()))))
        except KeyError:
            miss = pygame.Surface((o["width"] * z, o["height"] * z))
            miss.fill((255, 0, 255))
            draw.append((by, miss, (int(bx - miss.get_width() / 2), int(by - miss.get_height()))))
    for _, im, pos in sorted(draw, key=lambda d: d[0]):
        surf.blit(im, pos)
    pygame.image.save(surf, str(out))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("zone")
    ap.add_argument("out")
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--crop", default=None, help="x,y,w,h in tiles: real tiles at 2x zoom")
    a = ap.parse_args(argv)
    pygame.init()
    if a.crop:
        crop(a.zone, Path(a.out), *[int(v) for v in a.crop.split(",")])
    else:
        overview(a.zone, Path(a.out), a.scale)
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
