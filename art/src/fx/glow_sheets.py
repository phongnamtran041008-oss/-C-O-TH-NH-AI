"""Per-frame outer glow of the wings (and Hoa Than's halo + hair), cut from the packed character sheets.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx/glow_sheets.py

For every frame of client/assets/v2/chars/dao_si_<realm>.png: take the opaque silhouette, keep the part that
belongs to the wings (upper body, outside the torso column; behind the body when seen from the side) - or for
hoa_than the head / halo / hair - blur it, and tint it with the realm's glow colours from art/palette.json.
Written on EXACTLY the character's frame grid (same cols / frames / pivot / index) as
client/assets/v2/fx/glow_<realm>.png + .json, blend "alpha", layer "back": draw frame i of the glow directly
behind frame i of the character with a normal alpha blit.  Pure pygame (no numpy / Pillow).
"""
import json
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CH = os.path.join(ROOT, "client", "assets", "v2", "chars")
OUT = os.path.join(ROOT, "client", "assets", "v2", "fx")

# realm -> (outer colour, highlight colour, mode, outer alpha, highlight alpha, name)   colours are palette entries
REALMS = {
    "luyen_hu": ("#e0601a", "#ffae3a", "wings", 0.62, 0.8, "Anh sang canh Luyen Hu"),
    "hop_the": ("#6aa8e8", "#b0dcff", "wings", 0.62, 0.8, "Anh sang canh Hop The"),
    "dai_thua": ("#8a3ce0", "#ffe27a", "wings", 0.62, 0.75, "Anh sang canh Dai Thua"),
    "hoa_than": ("#8456be", "#e8b02a", "halo", 0.4, 0.5, "Anh sang vong sang Hoa Than"),
}


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def gblur(surf, r):
    try:
        return pygame.transform.gaussian_blur(surf, r)
    except AttributeError:
        return pygame.transform.box_blur(surf, r)


def facing_map(meta):
    m = {}
    for clip in meta["clips"].values():
        for f, idxs in clip["frames"].items():
            for i in idxs:
                m[i] = f
    return m


def region(mode, facing, px, pivot):
    """list of rects (x, y, w, h) that belong to the wings / halo."""
    cx, py = pivot
    if mode == "halo":
        return [(cx - 26, py - 62, 52, 40)]
    top, h = py - 62, 52
    if facing in ("down", "up"):
        return [(0, top, cx - 11, h), (cx + 11, top, px - cx - 11, h)]
    if facing == "right":
        return [(0, top, cx - 3, h)]
    return [(cx + 3, top, px - cx - 3, h)]


def build_table(levels, top):
    t = bytearray(256)
    for v in range(256):
        a = min(1.0, v / 255.0 * top)
        q = round(a * levels) / levels
        t[v] = int(q * 255 + 0.5) if q >= 1.0 / levels else 0
    return bytes(t)


def make(realm):
    ca, cb, mode, ao_top, ai_top, name = REALMS[realm]
    A, B = hexrgb(ca), hexrgb(cb)
    meta = json.load(open(os.path.join(CH, "dao_si_%s.json" % realm), encoding="utf-8"))
    sheet = pygame.image.load(os.path.join(CH, "dao_si_%s.png" % realm))
    w, h = meta["frame"]["w"], meta["frame"]["h"]
    cols, n = meta["cols"], meta["frames"]
    pivot = (meta["pivot"]["x"], meta["pivot"]["y"])
    face = facing_map(meta)
    rows = (n + cols - 1) // cols
    out = pygame.Surface((cols * w, rows * h), pygame.SRCALPHA)
    tab_o = build_table(4, 2.4 * ao_top / 0.62 * 0.62)
    tab_i = build_table(1, 1.0)
    for i in range(n):
        r, c = divmod(i, cols)
        fr = sheet.subsurface(pygame.Rect(c * w, r * h, w, h)).copy()
        sil = pygame.mask.from_surface(fr, 20)
        sel = pygame.Surface((w, h), pygame.SRCALPHA)
        for rect in region(mode, face.get(i, "down"), w, pivot):
            pygame.draw.rect(sel, (255, 255, 255, 255), rect)
        part = sil.overlap_mask(pygame.mask.from_surface(sel, 20), (0, 0))
        if part.count() < 25:
            part = sil
        base = part.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
        big = gblur(base, 5)
        mid = gblur(base, 2)
        ao = pygame.image.tobytes(big, "RGBA")[3::4]
        ai = pygame.image.tobytes(mid, "RGBA")[3::4]
        aoq = ao.translate(build_table(4, ao_top * 2.6))
        aiq = ai.translate(tab_i if False else build_table(1, 2.0))
        buf = bytearray(w * h * 4)
        for p in range(w * h):
            hi = aiq[p]
            lo = aoq[p]
            if hi and ai[p] > 150:
                buf[p * 4:p * 4 + 4] = bytes((B[0], B[1], B[2], int(ai_top * 255)))
            elif lo:
                buf[p * 4:p * 4 + 4] = bytes((A[0], A[1], A[2], lo))
        for q in range(w):                       # nothing may touch the frame edge (kit qc): clear a 2 px border
            for e in (0, 1, h - 2, h - 1):
                buf[(e * w + q) * 4 + 3] = 0
        for q in range(h):
            for e in (0, 1, w - 2, w - 1):
                buf[(q * w + e) * 4 + 3] = 0
        img = pygame.image.frombytes(bytes(buf), (w, h), "RGBA")
        out.blit(img, (c * w, r * h))
    id = "glow_" + realm
    pygame.image.save(out, os.path.join(OUT, id + ".png"))
    doc = {"id": id, "name_vi": name, "frame": {"w": w, "h": h}, "pivot": meta["pivot"], "sheet": id + ".png",
           "cols": cols, "frames": n, "fps": 10, "loop": False, "blend": "alpha", "ground": False, "layer": "back",
           "follows": "dao_si_" + realm,
           "draw": "frame i is drawn directly BEHIND frame i of dao_si_%s (same index, same pivot) with a normal alpha blit" % realm}
    json.dump(doc, open(os.path.join(OUT, id + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", id, n, "frames")


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1, 1))
    for r in REALMS:
        make(r)
