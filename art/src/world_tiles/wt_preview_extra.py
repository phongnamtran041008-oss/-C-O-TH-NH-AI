"""Proof images for the garden, bi canh, TD kit and the stone / dark-grass ground fixes."""
from __future__ import annotations

import random

from wt_preview32 import V2, PREVIEW, pg, load_tiles, load_props, player, autotile32, World, CELL

RARS = ("common", "rare", "epic", "legendary")


def _save(surf, name, scale):
    pygame = pg()
    PREVIEW.mkdir(parents=True, exist_ok=True)
    pygame.image.save(pygame.transform.scale(surf, (surf.get_width() * scale, surf.get_height() * scale)), str(PREVIEW / name))


def put(surf, props, name, x, y, frame=0):
    frames, pv = props[name]
    surf.blit(frames[frame % len(frames)], (x - pv[0], y - pv[1]))


def wither(spr):
    """The game's own withered() greying, applied to a v2 sprite (proves it works unchanged)."""
    pygame = pg()
    out = spr.copy()
    w, h = out.get_size()
    for y in range(h):
        for x in range(w):
            c = out.get_at((x, y))
            if c.a:
                g = (c.r + c.g + c.b) // 3
                k = 0.7
                out.set_at((x, y), (int(c.r * (1 - k) + (g * 0.6 + 90 * 0.4) * k), int(c.g * (1 - k) + (g * 0.6 + 90 * 0.4) * k),
                                    int(c.b * (1 - k) + (g * 0.6 + 90 * 0.4) * k), c.a))
    return out


# --------------------------------------------------------------------------- stone / plaza / dark grass test
def stone_test():
    pygame = pg()
    wd = World(15, 9, seed=5)
    wd.grass(0.0)
    stone = {(1, 1), (3, 2), (1, 4), (3, 6)} | {(x, 1) for x in range(5, 9)} | {(x, y) for x in (6, 7) for y in (4, 5)}
    plaza = {(10, 1), (12, 3), (10, 5)} | {(x, 7) for x in range(9, 13)} | {(x, y) for x in (13, 14) for y in (5, 6)}
    wd.blob(stone, "grass_stone", "stone")
    wd.blob(plaza, "grass_plaza", "plaza")
    dark = {(x, y) for x in range(0, 6) for y in (7, 8)} - {(0, 8)}
    wd.blob(dark, "grass_dark", "dark_grass")
    wd.blob({(2, 7), (3, 7), (2, 8), (3, 8)}, "dark_ink", "ink")
    surf = wd.surface()
    _save(surf, "world_stone_test.png", 2)


# --------------------------------------------------------------------------- garden
def garden():
    pygame = pg()
    g = load_props("garden")
    b32 = load_tiles("base32")
    rnd = random.Random(2)
    W, H = 720, 560
    surf = pygame.Surface((W, H))
    for y in range(0, H, CELL):
        for x in range(0, W, CELL):
            surf.blit(rnd.choice(b32["grass"]), (x, y))
    fams = ("herb", "flower", "root", "vine", "shroom", "shrub")
    cols = [(s, "common") for s in range(6)] + [(5, "rare"), (5, "epic"), (5, "legendary")]
    for r, fam in enumerate(fams):
        for c, (s, rar) in enumerate(cols):
            bx_, by_ = 20 + c * 72, 16 + r * 76
            surf.blit(g["plot_open"][0][0], (bx_, by_))
            name = f"{fam}_{s}" if s < 3 else f"{fam}_{s}_{rar}"
            fr, pv = g[name]
            surf.blit(fr[0], (bx_ + 32 - pv[0], by_ + 44 - pv[1]))
            if s >= 1:
                surf.blit(g["tag"][0][0], (bx_ + 2, by_ + 40))
    # locked / dry beds, a withered plant, seeds, eggs, decorations
    y0 = 16 + 6 * 76 + 6
    surf.blit(g["plot_locked"][0][0], (20, y0))
    surf.blit(g["plot_dry"][0][0], (92, y0))
    fr, pv = g["herb_4_rare"]
    surf.blit(wither(fr[0]), (92 + 32 - pv[0], y0 + 44 - pv[1]))
    for k, rar in enumerate(RARS):
        put(surf, g, f"seed_{rar}", 190 + k * 34, y0 + 40, k)
        put(surf, g, f"egg_{rar}", 190 + k * 34, y0 + 78, k % 3)
    put(surf, g, "hoa_sen", 360, y0 + 44, 1)
    put(surf, g, "chuong_gio", 410, y0 + 50, 2)
    put(surf, g, "co_phuong", 450, y0 + 56, 1)
    put(surf, load_props("buildings"), "lantern", 486, y0 + 56, 2)
    pl, ppv = player()
    surf.blit(pl, (600 - ppv[0], y0 + 60 - ppv[1]))
    _save(surf, "world_garden.png", 2)


# --------------------------------------------------------------------------- bi canh
def realm():
    pygame = pg()
    rp = load_props("realm")
    b32, t32 = load_tiles("base32"), load_tiles("terrain32")
    W, H = 640, 384
    surf = pygame.Surface((W, H))
    rnd = random.Random(8)
    for y in range(0, H, CELL):
        for x in range(0, W, CELL):
            surf.blit(rnd.choice(b32["realm_floor"]), (x, y))
    for x in range(0, W, CELL):                              # the north wall, two rows
        for y in (0, CELL):
            surf.blit(b32["realm_wall"][0], (x, y))
    items = [
        ("exit_closed", 160, 78, 0), ("exit_open", 480, 78, 1),
        ("rift", 320, 150, 3), ("statue", 90, 160, 1), ("mirror", 540, 190, 2),
        ("chest_closed", 60, 330, 0), ("chest_open", 120, 330, 0),
        ("pedestal_off", 220, 230, 0), ("pedestal_on", 270, 230, 0), ("pedestal_lit", 320, 230, 0),
    ]
    for tone in (1, 2, 3, 4):
        items.append((f"pillar_{tone}_off", 60 + tone * 60, 300, 0))
        items.append((f"pillar_{tone}_on", 340 + tone * 60, 300, 0))
    for k, st in enumerate(("off", "idle", "next", "done")):
        fr, pv = rp[f"rune_{st}"]
        surf.blit(fr[0], (380 + k * 44, 214))
    pl, ppv = player()
    items.append(("__player__", 230, 332, 0))
    for name, x, y, f in sorted(items, key=lambda t: t[2]):
        if name == "__player__":
            surf.blit(pl, (x - ppv[0], y - ppv[1]))
        else:
            put(surf, rp, name, x, y, f)
    _save(surf, "world_realm.png", 2)


# --------------------------------------------------------------------------- TD board (native 24 px cell, 12 x 7)
def td():
    pygame = pg()
    td_t = load_tiles("td24")
    tp = load_props("td")
    CELL_ = 24
    path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 6), (4, 6), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2),
            (5, 1), (5, 0), (6, 0), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (9, 6), (10, 6), (11, 6)]
    pset = set(path)
    W, H = 12 * CELL_, 7 * CELL_
    surf = pygame.Surface((W + 8, H + 8))
    surf.fill((233, 223, 200))
    rnd = random.Random(1)
    for y in range(7):
        for x in range(12):
            if (x, y) in pset:
                sides = "".join(s for s, d in (("n", (0, -1)), ("e", (1, 0)), ("s", (0, 1)), ("w", (-1, 0)))
                                if (x + d[0], y + d[1]) not in pset and 0 <= x + d[0] < 12 and 0 <= y + d[1] < 7)
                t = td_t[f"td_path_{sides or 'none'}"][0]
            else:
                t = rnd.choice(td_t["grass"])
            surf.blit(t, (4 + x * CELL_, 4 + y * CELL_))

    def cell(x, y):
        return 4 + x * CELL_ + 12, 4 + y * CELL_ + 21

    for name, c in (("td_spawn", (0, 0)), ("td_core", (11, 6))):
        fr, pv = tp[name]
        x, y = cell(*c)
        surf.blit(fr[1], (x - pv[0], y - pv[1] + 2))
    for c in ((0, 5), (10, 3), (11, 0), (11, 3)):
        fr, pv = tp[f"td_rock_{c[0] % 2}"]
        x, y = cell(*c)
        surf.blit(fr[0], (x - pv[0], y - pv[1] + 1))
    roles = ("hoa", "thuy", "kim", "son", "quang", "ho_tro", "moc")
    spots = [(1, 1), (3, 1), (4, 3), (6, 1), (7, 3), (9, 1), (10, 4),
             (1, 3), (3, 3), (6, 3), (9, 3), (4, 5), (7, 5), (10, 5),
             (1, 5), (3, 4), (6, 5), (9, 5), (4, 1), (7, 1), (0, 3)]
    k = 0
    for lv in (1, 2, 3):
        for role in roles:
            x, y = cell(*spots[k])
            fr, pv = tp[f"tower_{role}_{lv}"]
            surf.blit(fr[0], (x - pv[0], y - pv[1]))
            k += 1
    # projectiles and hits along the path
    for i, role in enumerate(("hoa", "thuy", "kim", "son", "quang")):
        fr, pv = tp[f"shot_{role}"]
        surf.blit(fr[i % len(fr)], (4 + (2 + i * 2) * CELL_ + 8 - pv[0], 4 + 2 * CELL_ + 12 - pv[1]))
        fr, pv = tp[f"hit_{role}"]
        surf.blit(fr[(i + 1) % 4], (4 + (3 + i * 2) * CELL_ - pv[0] + 12, 4 + 4 * CELL_ - pv[1] + 12))
    fr, pv = tp["hit_puff"]
    surf.blit(fr[2], (4 + 9 * CELL_ + 12 - pv[0], 4 + 6 * CELL_ - pv[1] + 6))
    _save(surf, "world_td.png", 3)


def make_all():
    stone_test()
    garden()
    realm()
    td()
