"""Proofs for the 32 px world: world_village.png (480x270 at 3x, real player sprite for scale) and world_dirt_test.png
(dirt islands / strips in grass, a 6x6 block of dirt). Also the autotile rule used by the mock-ups, written down in code."""
from __future__ import annotations

import json
import os
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
V2 = ROOT / "client" / "assets" / "v2"
PREVIEW = ROOT / "art" / "preview"
CELL = 32


def pg():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    if not pygame.display.get_surface():
        pygame.display.set_mode((8, 8))
    return pygame


def load_tiles(region: str) -> dict:
    pygame = pg()
    doc = json.loads((V2 / "tiles" / f"{region}.json").read_text("utf-8"))
    img = pygame.image.load(str(V2 / "tiles" / doc["sheet"])).convert_alpha()
    cols, c = doc["cols"], doc["cell"]
    return {n: [img.subsurface(((i % cols) * c, (i // cols) * c, c, c)).copy() for i in idx] for n, idx in doc["tiles"].items()}


def load_props(name: str) -> dict:
    pygame = pg()
    doc = json.loads((V2 / "props" / f"{name}.json").read_text("utf-8"))
    img = pygame.image.load(str(V2 / "props" / doc["sheet"])).convert_alpha()
    out = {}
    for n, p in doc["props"].items():
        x, y, w, h = p["rect"]
        frames = [img.subsurface((x + k * w, y, w, h)).copy() for k in range(p["frames"])]
        out[n] = (frames, p["pivot"])
    return out


def player():
    pygame = pg()
    doc = json.loads((V2 / "chars" / "dao_si_luyen_khi.json").read_text("utf-8"))
    img = pygame.image.load(str(V2 / "chars" / doc["sheet"])).convert_alpha()
    fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
    i = doc["clips"]["idle"]["frames"]["down"][0]
    return img.subsurface(((i % cols) * fw, (i // cols) * fh, fw, fh)).copy(), (doc["pivot"]["x"], doc["pivot"]["y"])


def autotile32(mask, prefix, center):
    """THE AUTOTILE RULE for an isolated or thin material (path / dirt) inside grass. `mask` = set of (x, y) cells (y down).
    n, s, e, w = whether the 4 neighbours belong to the mask.
      0 neighbours                      -> <prefix>_island
      1 neighbour (an end of a strip)   -> N present: _cap_s, S: _cap_n, E: _cap_w, W: _cap_e   (the cap faces the open side)
      2 opposite (a straight strip)     -> N+S: _v, E+W: _h
      2 adjacent (a corner)             -> _<missing sides> in the order n s w e: _sw, _se, _nw, _ne (convex corner tile)
      3 neighbours                      -> _<the missing side>: _n _s _w _e (edge tile)
      4 neighbours                      -> a missing diagonal gives _in_<nw|ne|sw|se> (first missing in that order), else the centre.
    Strips are 8 px wide, blob edges sit 5 px inside the tile: paint paths 2 cells wide where they turn or branch."""
    out = {}
    for (x, y) in mask:
        n, s, e, w = ((x, y - 1) in mask, (x, y + 1) in mask, (x + 1, y) in mask, (x - 1, y) in mask)
        k = n + s + e + w
        if k == 0:
            out[(x, y)] = f"{prefix}_island"
        elif k == 1:
            out[(x, y)] = f"{prefix}_" + ("cap_s" if n else "cap_n" if s else "cap_w" if e else "cap_e")
        elif k == 2 and n == s:
            out[(x, y)] = f"{prefix}_v" if n else f"{prefix}_h"
        elif k == 4:
            for key, d in (("in_nw", (-1, -1)), ("in_ne", (1, -1)), ("in_sw", (-1, 1)), ("in_se", (1, 1))):
                if (x + d[0], y + d[1]) not in mask:
                    out[(x, y)] = f"{prefix}_{key}"
                    break
            else:
                out[(x, y)] = center
        else:
            out[(x, y)] = f"{prefix}_" + ("n" if not n else "") + ("s" if not s else "") + ("w" if not w else "") + ("e" if not e else "")
    return out


class World:
    def __init__(self, W, H, seed=3):
        self.pygame = pg()
        self.W, self.H = W, H
        self.rnd = random.Random(seed)
        self.base, self.terr = load_tiles("base32"), load_tiles("terrain32")
        self.grid = [[None] * W for _ in range(H)]
        self.items = []

    def T(self, name, k=None):
        sheet = self.terr if name in self.terr else self.base
        lst = sheet[name]
        return lst[self.rnd.randrange(len(lst)) if k is None else k]

    def grass(self, flowers=0.03):
        for y in range(self.H):
            for x in range(self.W):
                self.grid[y][x] = self.T("flowers") if self.rnd.random() < flowers else self.T("grass")

    def blob(self, mask, prefix, center_name):
        for c, n in autotile32(mask, prefix, center_name).items():
            if 0 <= c[0] < self.W and 0 <= c[1] < self.H:
                self.grid[c[1]][c[0]] = self.T(center_name) if n == center_name else self.T(n)

    def surface(self, w=None, h=None):
        pygame = self.pygame
        s = pygame.Surface((self.W * CELL, self.H * CELL))
        for y in range(self.H):
            for x in range(self.W):
                if self.grid[y][x] is not None:
                    s.blit(self.grid[y][x], (x * CELL, y * CELL))
        return s


def village():
    pygame = pg()
    wd = World(15, 9, seed=4)
    wd.grass(0.02)
    for y in range(3, 6):                                   # the square: flagstones with a cobbled rim
        for x in range(5, 10):
            wd.grid[y][x] = wd.T("plaza") if (x + y) % 2 else wd.T("stone")
    path = {(x, y) for x in (7, 8) for y in range(6, 10)} | {(x, y) for x in range(-1, 7) for y in (6, 7)}
    wd.blob(path, "grass_path", "path")
    for y in range(3, 6):
        for x in range(5, 10):
            if wd.grid[y][x] is not None and (x + y) % 2 == 0:
                wd.grid[y][x] = wd.T("plaza")
    surf = wd.surface()
    bld, nat = load_props("buildings"), load_props("nature")
    pl, ppv = player()
    items = []

    def add(src, name, x, y, frame=0):
        frames, pv = src[name]
        items.append((y, frames[frame % len(frames)], x - pv[0], y - pv[1]))

    add(bld, "library", 78, 104)
    add(bld, "house_0", 196, 100)
    add(bld, "house_1", 302, 100)
    add(bld, "house_2", 408, 100)
    add(bld, "well", 240, 160)
    add(bld, "lantern", 168, 128, 1)
    add(bld, "lantern", 312, 128, 2)
    add(bld, "stall_0", 112, 172)
    add(bld, "stall_1", 372, 172)
    add(bld, "board", 22, 150)
    add(bld, "table", 150, 210)
    add(bld, "mat", 196, 222)
    add(bld, "sign", 64, 190)
    add(bld, "tablet", 440, 168)
    add(bld, "furnace", 330, 236, 1)
    add(bld, "anvil", 384, 240)
    add(bld, "portal", 446, 258, 2)
    add(bld, "hive", 30, 248)
    add(nat, "tree_1", 18, 232)
    add(nat, "pine_1", 300, 262)
    add(nat, "bamboo_1", 106, 262)
    add(nat, "bamboo_2", 124, 258)
    add(nat, "bamboo_3", 90, 258)
    add(nat, "peach_tree", 190, 258)
    add(nat, "bush_1", 255, 238)
    add(nat, "linh_thao_1", 220, 240)
    add(nat, "linh_thao_3", 272, 256)
    items.append((118, pl, 302 - ppv[0] + 22, 118 - ppv[1]))  # the player stands by the door of the middle house
    for _, spr, x, y in sorted(items, key=lambda t: t[0]):
        surf.blit(spr, (x, y))
    out = surf.subsurface((0, 0, 480, 270)).copy()
    PREVIEW.mkdir(parents=True, exist_ok=True)
    pygame.image.save(pygame.transform.scale(out, (1440, 810)), str(PREVIEW / "world_village.png"))
    pygame.image.save(out, str(PREVIEW / "world_village_1x.png"))


def dirt_test():
    pygame = pg()
    wd = World(15, 9, seed=9)
    wd.grass(0.0)
    cells = set()
    cells |= {(1, 1), (4, 2), (2, 5), (6, 6)}                                # single-cell islands
    cells |= {(x, 1) for x in range(6, 11)}                                  # a horizontal strip with two ends
    cells |= {(13, y) for y in range(1, 6)}                                  # a vertical strip
    cells |= {(x, y) for x in range(8, 11) for y in range(4, 7)}             # a small 3x3 patch
    cells |= {(x, y) for x in (3, 4) for y in (7, 8)}                        # a 2x2 patch
    wd.blob(cells, "grass_dirt", "dirt")
    surf = wd.surface()
    # a 6x6 block of dirt: the three variants side by side, no grid
    big = pygame.Surface((6 * CELL, 6 * CELL))
    for y in range(6):
        for x in range(6):
            big.blit(wd.T("dirt"), (x * CELL, y * CELL))
    sheet = pygame.Surface((surf.get_width() + 6 * CELL + 12, max(surf.get_height(), 6 * CELL)))
    sheet.fill((20, 20, 28))
    sheet.blit(surf, (0, 0))
    sheet.blit(big, (surf.get_width() + 12, 0))
    pygame.image.save(pygame.transform.scale(sheet, (sheet.get_width() * 2, sheet.get_height() * 2)), str(PREVIEW / "world_dirt_test.png"))


def make_all():
    village()
    dirt_test()
