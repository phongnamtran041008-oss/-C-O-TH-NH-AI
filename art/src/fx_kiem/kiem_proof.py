"""Proof on the characters: a slashing cultivator of each realm with that tier's kiếm khí at the blade.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_kiem/kiem_proof.py

pygame only (no Pillow).  For tier T: character `dao_si_<look>` (clip `slash`, facing right, the frame at
`events.slash.hit`), its weapon layer `kiem_<grade>` drawn over it, then (additively, BLEND_RGB_ADD)
`kiem_khi_T` frame 1 with its pivot on the sword hand, and `kiem_song_T` frame 0 a little further right.
The sword hand is measured from the weapon layer itself: the weapon pixel nearest the body (the grip).
Writes art/preview/fx_kiem_on_char.png (3x, ten tiers in two rows of five) and
art/preview/fx_kiem_on_char_1x.png (1x, all ten side by side: how it reads in game before the 2x world zoom).
"""
import json
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
V2 = os.path.join(ROOT, "client", "assets", "v2")
GROUND = (52, 58, 54)            # mid-dark ground
#        tier: (look, sword grade)
CAST = {1: ("luyen_khi", 1), 2: ("luyen_khi", 2), 3: ("luyen_khi", 2), 4: ("truc_co", 3), 5: ("ket_dan", 4),
        6: ("nguyen_anh", 5), 7: ("hoa_than", 6), 8: ("luyen_hu", 7), 9: ("hop_the", 7), 10: ("dai_thua", 8)}
CELL_W, CELL_H = 236, 176        # 1x cell
CH_X, CH_Y = 36, 128             # where the character's pivot (feet) sits in the cell

pygame.init()
pygame.display.set_mode((1, 1))
_cache = {}


def sheet(kind, id):
    k = (kind, id)
    if k not in _cache:
        meta = json.load(open(os.path.join(V2, kind, id + ".json"), encoding="utf-8"))
        img = pygame.image.load(os.path.join(V2, kind, id + ".png")).convert_alpha()
        _cache[k] = (meta, img)
    return _cache[k]


def frame(kind, id, index):
    meta, img = sheet(kind, id)
    w, h = meta["frame"]["w"], meta["frame"]["h"]
    r, c = divmod(index, meta["cols"])
    return img.subsurface(pygame.Rect(c * w, r * h, w, h)).copy(), meta


def grip(surf, pivot):
    """the weapon pixel nearest the body centre (chest height) = the sword hand."""
    cx, cy = pivot[0], pivot[1] - 26
    best = None
    w, h = surf.get_size()
    for y in range(h):
        for x in range(w):
            if surf.get_at((x, y)).a > 0:
                d = (x - cx) ** 2 + (y - cy) ** 2
                if best is None or d < best[0]:
                    best = (d, x, y)
    return best[1], best[2]


def cell(t):
    look, grade = CAST[t]
    c = pygame.Surface((CELL_W, CELL_H))
    c.fill(GROUND)
    cid = "dao_si_" + look
    cmeta, _ = sheet("chars", cid)
    hit = cmeta.get("events", {}).get("slash", {}).get("hit", 3)
    idx = cmeta["clips"]["slash"]["frames"]["right"][hit]
    body, _ = frame("chars", cid, idx)
    wpn, wmeta = frame("weapons", "kiem_%d" % grade, idx)
    ox, oy = CH_X - cmeta["pivot"]["x"], CH_Y - cmeta["pivot"]["y"]
    c.blit(body, (ox, oy))
    c.blit(wpn, (ox, oy))
    hx, hy = grip(wpn, (cmeta["pivot"]["x"], cmeta["pivot"]["y"]))
    hx, hy = ox + hx, oy + hy
    k, km = frame("fx", "kiem_khi_%d" % t, 1)
    c.blit(k, (hx - km["pivot"]["x"], hy - km["pivot"]["y"]), special_flags=pygame.BLEND_RGB_ADD)
    s, sm = frame("fx", "kiem_song_%d" % t, 0) if t >= 2 else (None, None)
    if s is not None:
        sx = hx + int(km["frame"]["w"] * 0.62)
        c.blit(s, (sx - sm["pivot"]["x"], hy - sm["pivot"]["y"]), special_flags=pygame.BLEND_RGB_ADD)
    return c, (hx, hy)


def main():
    font = pygame.font.Font(None, 22)
    cells = [cell(t) for t in range(1, 11)]
    # 1x: all ten side by side
    one = pygame.Surface((10 * (CELL_W + 2), CELL_H))
    one.fill((10, 10, 16))
    for i, (c, _) in enumerate(cells):
        one.blit(c, (i * (CELL_W + 2), 0))
    pygame.image.save(one, os.path.join(ROOT, "art", "preview", "fx_kiem_on_char_1x.png"))
    # 3x: two rows of five
    Z, gap, lab = 3, 8, 24
    W = 5 * (CELL_W * Z + gap) + gap
    H = 2 * (CELL_H * Z + lab + gap) + gap
    out = pygame.Surface((W, H))
    out.fill((10, 10, 16))
    for i, (c, hand) in enumerate(cells):
        r, k = divmod(i, 5)
        x, y = gap + k * (CELL_W * Z + gap), gap + r * (CELL_H * Z + lab + gap)
        look, grade = CAST[i + 1]
        out.blit(font.render("T%d  %s  kiem_%d   hand %d,%d" % (i + 1, look, grade, hand[0], hand[1]), True, (210, 210, 225)), (x + 4, y + 4))
        out.blit(pygame.transform.scale(c, (CELL_W * Z, CELL_H * Z)), (x, y + lab))
    pygame.image.save(out, os.path.join(ROOT, "art", "preview", "fx_kiem_on_char.png"))
    print("wrote art/preview/fx_kiem_on_char.png", out.get_size(), "and fx_kiem_on_char_1x.png", one.get_size())


if __name__ == "__main__":
    main()
