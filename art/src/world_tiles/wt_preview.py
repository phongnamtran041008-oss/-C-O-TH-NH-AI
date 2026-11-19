"""Contact sheets and the two mock-up scenes. Runs in the venv (pygame only), reads the packed sheets
in client/assets/v2/, so what is shown is exactly what the game will load."""
from __future__ import annotations

import json
import os
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TILES = ROOT / "client" / "assets" / "v2" / "tiles"
PROPS = ROOT / "client" / "assets" / "v2" / "props"
PREVIEW = ROOT / "art" / "preview"
TILE = 16


def pg():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    if not pygame.display.get_surface():
        pygame.display.set_mode((8, 8))
    return pygame


def load_sheet(region: str) -> dict[str, list]:
    pygame = pg()
    doc = json.loads((TILES / f"{region}.json").read_text("utf-8"))
    img = pygame.image.load(str(TILES / doc["sheet"])).convert_alpha()
    cols = doc["cols"]
    out = {}
    for name, idxs in doc["tiles"].items():
        out[name] = [img.subsurface(((i % cols) * TILE, (i // cols) * TILE, TILE, TILE)).copy() for i in idxs]
    return out


def load_props():
    pygame = pg()
    doc = json.loads((PROPS / "nature.json").read_text("utf-8"))
    img = pygame.image.load(str(PROPS / doc["sheet"])).convert_alpha()
    out = {}
    for n, p in doc["props"].items():
        out[n] = (img.subsurface(pygame.Rect(p["rect"])).copy(), p["pivot"])
    return out


def contact_sheets():
    pygame = pg()
    font = pygame.font.Font(None, 15)
    S = 3
    bg = (22, 20, 30)
    base, terr = load_sheet("base"), load_sheet("terrain")

    def block(sheet, title, cols=8):
        items = [(f"{n}{'' if len(l) == 1 else k}", s) for n, l in sheet.items() for k, s in enumerate(l)]
        rows = (len(items) + cols - 1) // cols
        cell = TILE * S + 6
        surf = pygame.Surface((cols * cell + 4, rows * (cell + 12) + 22))
        surf.fill(bg)
        surf.blit(font.render(title, True, (230, 220, 190)), (4, 4))
        for i, (n, t) in enumerate(items):
            x, y = 4 + (i % cols) * cell, 20 + (i // cols) * (cell + 12)
            surf.blit(pygame.transform.scale(t, (TILE * S, TILE * S)), (x, y))
            surf.blit(font.render(n[:12], True, (140, 140, 160)), (x, y + TILE * S + 1))
        return surf

    parts = [block(base, "base.png"), block(terr, "terrain.png", cols=10)]
    width = max(p.get_width() for p in parts)
    out = pygame.Surface((width, sum(p.get_height() for p in parts)))
    out.fill(bg)
    y = 0
    for p in parts:
        out.blit(p, (0, y))
        y += p.get_height()
    PREVIEW.mkdir(parents=True, exist_ok=True)
    pygame.image.save(out, str(PREVIEW / "world_tiles.png"))
    props = load_props()
    cw, ch, cols = 120, 236, 8
    rows = (len(props) + cols - 1) // cols
    ps = pygame.Surface((cols * cw, rows * ch))
    ps.fill((58, 106, 38))
    for i, (n, (spr, pv)) in enumerate(props.items()):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        ps.blit(pygame.transform.scale(spr, (spr.get_width() * 3, spr.get_height() * 3)),
                (x0 + cw // 2 - pv[0] * 3, y0 + ch - 24 - pv[1] * 3))
        ps.blit(font.render(n, True, (230, 240, 210)), (x0 + 4, y0 + 4))
    pygame.image.save(ps, str(PREVIEW / "world_props.png"))


def autotile(mask, prefix, center):
    """Tile name for every cell of `mask` (a set of (x, y)); y grows downwards."""
    out = {}
    for (x, y) in mask:
        n, s, e, w = ((x, y - 1) in mask, (x, y + 1) in mask, (x + 1, y) in mask, (x - 1, y) in mask)
        if n and s and e and w:
            for key, d in (("in_nw", (-1, -1)), ("in_ne", (1, -1)), ("in_sw", (-1, 1)), ("in_se", (1, 1))):
                if (x + d[0], y + d[1]) not in mask:
                    out[(x, y)] = f"{prefix}_{key}"
                    break
            else:
                out[(x, y)] = center
            continue
        name = ("n" if not n else "") + ("s" if not s else "") + ("w" if not w else "") + ("e" if not e else "")
        out[(x, y)] = f"{prefix}_{name}"
    return out


class Scene:
    def __init__(self, W=30, H=17, seed=11):
        self.pygame = pg()
        self.W, self.H = W, H
        self.rnd = random.Random(seed)
        self.base, self.terr = load_sheet("base"), load_sheet("terrain")
        self.props = load_props()
        self.grid = [[None] * W for _ in range(H)]
        self.items = []

    def T(self, name, k=None):
        sheet = self.terr if name in self.terr else self.base
        lst = sheet[name]
        return lst[self.rnd.randrange(len(lst)) if k is None else k]

    def grass(self, flowers=0.05):
        for y in range(self.H):
            for x in range(self.W):
                r = self.rnd.random()
                self.grid[y][x] = self.T("flowers") if r < flowers else self.T("grass")

    def plateau(self, x0, x1, y0, y1, stairs_x=None, stairs=True):
        """Raised land: back row y0, top rows, the two rows of the face, the shadow row. Returns the shadow row index."""
        T = self.T
        for x in range(x0, x1 + 1):
            e = "l" if x == x0 else "r" if x == x1 else ""
            side = "w" if x == x0 else "e" if x == x1 else ""
            self.grid[y0][x] = T("cliff_" + ("nw" if x == x0 else "ne" if x == x1 else "n"))
            for y in range(y0 + 1, y1 - 1):
                self.grid[y][x] = T("cliff_" + side) if side else T("plateau_top")
            alt = "2" if x % 2 else ""
            fa, fb = (f"cliff_face_a_{e}", f"cliff_face_b_{e}") if e else (f"cliff_face_a{alt}", f"cliff_face_b{alt}")
            self.grid[y1 - 1][x] = T(fa)
            self.grid[y1][x] = T(fb)
            self.grid[y1 + 1][x] = T("cliff_shadow" + ("_" + e if e else ""))
        if stairs_x is not None:
            self.grid[y1 - 1][stairs_x] = T("stairs_a")
            self.grid[y1][stairs_x] = T("stairs_b")
            self.grid[y1 + 1][stairs_x] = T("grass")

    def blob(self, mask, prefix, center, fill=None):
        for c, n in autotile(mask, prefix, center).items():
            if 0 <= c[0] < self.W and 0 <= c[1] < self.H:
                self.grid[c[1]][c[0]] = fill(c) if (n == center and fill) else self.T(n)

    def put(self, name, x, y):
        self.items.append((y, name, x, y))

    def render(self, out_name):
        pygame = self.pygame
        scene = pygame.Surface((self.W * TILE, self.H * TILE))
        for y in range(self.H):
            for x in range(self.W):
                if self.grid[y][x] is not None:
                    scene.blit(self.grid[y][x], (x * TILE, y * TILE))
        for _, name, x, y in sorted(self.items):
            spr, pv = self.props[name]
            scene.blit(spr, (x - pv[0], y - pv[1]))
        PREVIEW.mkdir(parents=True, exist_ok=True)
        pygame.image.save(scene, str(PREVIEW / f"{out_name}_1x.png"))
        pygame.image.save(pygame.transform.scale(scene, (self.W * TILE * 3, self.H * TILE * 3)), str(PREVIEW / f"{out_name}.png"))


def mockup_village():
    """A path through grass to a pond with a bridge, a plateau with stairs, bamboo and trees, a few herbs."""
    s = Scene()
    s.grass(0.025)
    s.plateau(8, 15, 1, 5, stairs_x=11)
    path = {(x, y) for x in (11, 12) for y in range(6, 12)} | {(x, y) for x in range(-2, 20) for y in (10, 11)}
    s.blob(path, "grass_path", "path", fill=lambda c: s.T("path"))
    s.blob({(x, y) for x in range(2, 7) for y in range(13, 16)}, "grass_dirt", "dirt", fill=lambda c: s.T("dirt"))
    pond = {(x, y) for x in range(20, 28) for y in range(7, 15)} - {(20, 7), (27, 7), (20, 14), (27, 14)}
    s.blob(pond, "shore", "water", fill=lambda c: s.T("water_anim", 0))
    for x in range(20, 28):
        s.grid[11][x] = s.T("bridge_h_w" if x == 20 else "bridge_h_e" if x == 27 else "bridge_h")
    for x in range(14, 18):                                   # a small flagged yard
        for y in (13, 14):
            s.grid[y][x] = s.T("plaza" if (x + y) % 3 else "stone")
    for n, x, y in [
        ("bamboo_1", 22, 50), ("bamboo_2", 46, 40), ("bamboo_3", 70, 56), ("bamboo_1", 34, 74), ("bamboo_2", 62, 84),
        ("bamboo_3", 18, 98), ("bamboo_1", 84, 100), ("bamboo_2", 48, 112), ("bamboo_3", 10, 62),
        ("peach_tree", 158, 62), ("pine_1", 216, 58), ("crystal_1", 190, 44), ("rock_1", 150, 44), ("bush_1", 224, 46),
        ("tree_1", 110, 150), ("rock_2", 96, 140), ("bush_2", 232, 136), ("tall_grass", 120, 136), ("tall_grass", 240, 148),
        ("linh_thao_1", 104, 125), ("linh_thao_2", 226, 128), ("stump", 36, 150), ("log", 304, 150),
        ("pine_2", 20, 216), ("tree_2", 130, 240), ("bush_1", 100, 236), ("mushroom_ring", 170, 218), ("linh_thao_3", 200, 232),
        ("boulder", 252, 246), ("linh_thao_4", 62, 232), ("rock_3", 78, 202),
        ("pine_1", 440, 70), ("pine_2", 462, 100), ("dead_tree", 456, 182), ("bush_1", 420, 160), ("tree_1", 300, 110),
        ("lotus", 352, 132), ("lotus", 410, 206), ("linh_thao_1", 308, 212), ("rock_1", 330, 228), ("peach_tree", 452, 238),
        ("bamboo_2", 280, 90), ("bamboo_1", 292, 96),
    ]:
        s.put(n, x, y)
    s.render("world_mockup")


def mockup_cliff():
    """A larger plateau: natural cliff, stairs cut into it, a tree and a crystal on top."""
    s = Scene(seed=5)
    s.grass(0.02)
    s.plateau(4, 25, 1, 8, stairs_x=14)
    path = {(x, y) for x in (14, 15) for y in range(9, 19)}
    s.blob(path, "grass_path", "path", fill=lambda c: s.T("path"))
    for n, x, y in [
        ("peach_tree", 110, 86), ("crystal_1", 192, 66), ("pine_1", 300, 70), ("rock_2", 246, 78), ("bush_1", 150, 92),
        ("linh_thao_2", 170, 96), ("tree_1", 380, 94), ("rock_1", 330, 100), ("linh_thao_1", 224, 100), ("bush_2", 84, 100),
        ("crystal_2", 420, 80), ("tall_grass", 260, 100),
        ("pine_2", 40, 230), ("pine_1", 440, 236), ("bush_1", 120, 214), ("tree_2", 330, 232), ("boulder", 80, 252),
        ("rock_3", 280, 244), ("linh_thao_4", 190, 250), ("bamboo_1", 400, 192), ("bamboo_2", 420, 196), ("bamboo_3", 452, 188),
    ]:
        s.put(n, x, y)
    s.render("world_mockup_cliff")


def make_all():
    contact_sheets()
    mockup_village()
    mockup_cliff()
