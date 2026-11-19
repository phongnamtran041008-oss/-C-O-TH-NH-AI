"""Proof sheet: back aura + character + front aura, composited for real (pygame, additive for blend: add).

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx/aura_proof.py [--crop x0,y0,x1,y1 out.png]

Writes art/preview/aura_on_chars.png : 8 realms (rows), at 4x, on a dark background AND on grass
(client/assets/v2/tiles/base.png); the three winged realms also facing right, facing up and on the
slash hit frame.  Character frame 96x96 pivot (48,82), aura frame 128x128 pivot (64,104).
"""
import json
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FX = os.path.join(ROOT, "client", "assets", "v2", "fx")
CH = os.path.join(ROOT, "client", "assets", "v2", "chars")
REALMS = ["luyen_khi", "truc_co", "ket_dan", "nguyen_anh", "hoa_than", "luyen_hu", "hop_the", "dai_thua"]
WINGED = ("luyen_hu", "hop_the", "dai_thua")
Z = 4
DARK = (14, 14, 24)

pygame.init()
pygame.display.set_mode((1, 1))
_cache = {}


def sheet(dirname, id):
    k = (dirname, id)
    if k not in _cache:
        meta = json.load(open(os.path.join(dirname, id + ".json"), encoding="utf-8"))
        img = pygame.image.load(os.path.join(dirname, id + ".png")).convert_alpha()
        _cache[k] = (meta, img)
    return _cache[k]


def frame(dirname, id, index):
    meta, img = sheet(dirname, id)
    w, h = meta["frame"]["w"], meta["frame"]["h"]
    r, c = divmod(index, meta["cols"])
    return img.subsurface(pygame.Rect(c * w, r * h, w, h)).copy(), meta


def grass_bg(w, h):
    meta = json.load(open(os.path.join(ROOT, "client", "assets", "v2", "tiles", "base.json"), encoding="utf-8"))
    img = pygame.image.load(os.path.join(ROOT, "client", "assets", "v2", "tiles", "base.png")).convert_alpha()
    cols = meta["cols"]
    idx = meta["tiles"]["grass"]
    s = pygame.Surface((w, h))
    for ty in range(0, h, 16):
        for tx in range(0, w, 16):
            i = idx[((tx // 16) * 5 + (ty // 16) * 3) % len(idx)]
            r, c = divmod(i, cols)
            s.blit(img, (tx, ty), pygame.Rect(c * 16, r * 16, 16, 16))
    return s


def compose(realm, facing, clip, step, af, bg):
    """128x128 cell: back aura, character, front aura."""
    cell = pygame.Surface((128, 128))
    if bg == "dark":
        cell.fill(DARK)
    else:
        cell.blit(grass_bg(128, 128), (0, 0))
    cmeta, _ = sheet(CH, "dao_si_" + realm)
    idx = cmeta["clips"][clip]["frames"][facing][step]
    ch, _ = frame(CH, "dao_si_" + realm, idx)
    ox, oy = 64 - cmeta["pivot"]["x"], 104 - cmeta["pivot"]["y"]
    for layer in ("back", "front"):
        id = "aura_%s_%s" % (realm, layer)
        a, meta = frame(FX, id, af)
        if layer == "front":
            if os.path.exists(os.path.join(FX, "glow_%s.json" % realm)):      # glow cut from the character frame itself
                g, _ = frame(FX, "glow_" + realm, idx)
                cell.blit(g, (ox, oy))
            cell.blit(ch, (ox, oy))
        cell.blit(a, (0, 0), special_flags=pygame.BLEND_RGB_ADD if meta["blend"] == "add" else 0)
    return cell


def main():
    font = pygame.font.Font(None, 30)
    cols_max = 6
    cw = 128 * Z
    rows = len(REALMS)
    gap = 8
    W = cols_max * (cw + gap) + gap
    H = rows * (cw + 34 + gap) + gap
    sheet_ = pygame.Surface((W, H))
    sheet_.fill((10, 10, 16))
    for r, realm in enumerate(REALMS):
        cmeta, _ = sheet(CH, "dao_si_" + realm)
        hit = cmeta.get("events", {}).get("slash", {}).get("hit", 3)
        cells = [("idle down, dark", compose(realm, "down", "idle", 1, 2, "dark")),
                 ("idle down, grass", compose(realm, "down", "idle", 2, 5, "grass"))]
        if realm in WINGED:
            cells += [("right", compose(realm, "right", "idle", 1, 3, "dark")),
                      ("up", compose(realm, "up", "idle", 1, 6, "dark")),
                      ("slash hit", compose(realm, "right", "slash", hit, 4, "dark")),
                      ("fly", compose(realm, "right", "fly", 1, 6, "dark"))]
        elif realm == "hoa_than":
            cells += [("right", compose(realm, "right", "idle", 1, 3, "dark")), ("up", compose(realm, "up", "idle", 1, 6, "dark"))]
        y = gap + r * (cw + 34 + gap)
        sheet_.blit(font.render("%s" % realm, True, (210, 210, 225)), (gap, y + 2))
        for c, (label, cell) in enumerate(cells):
            x = gap + c * (cw + gap)
            sheet_.blit(pygame.transform.scale(cell, (cw, cw)), (x, y + 30))
            if c:
                sheet_.blit(font.render(label, True, (150, 150, 170)), (x + 4, y + 8))
    out = os.path.join(ROOT, "art", "preview", "aura_on_chars.png")
    pygame.image.save(sheet_, out)
    print("wrote", out, sheet_.get_size())
    if "--crop" in sys.argv:
        i = sys.argv.index("--crop")
        x0, y0, x1, y1 = [int(v) for v in sys.argv[i + 1].split(",")]
        pygame.image.save(sheet_.subsurface(pygame.Rect(x0, y0, x1 - x0, y1 - y0)).copy(), sys.argv[i + 2])


if __name__ == "__main__":
    main()
