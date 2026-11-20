"""Proofs in context (pygame composites; run with the venv python):
    art/preview/fx_tien_ich_roi_proof.png        five weapon icons on grass, each in its rarity's ring + column (1x and 3x)
    art/preview/fx_tien_ich_phi_proof.png        the fly clip standing on phi_kiem_1, lifted 24 px: shadow, clouds, wake, wind (6 steps, 3x)
    art/preview/fx_tien_ich_linh_can_proof.png   the Trac Linh Thach with the nine reveals and pillars (2x)
Draw order = what the game should do.  blend 'add' sheets are blitted with BLEND_RGB_ADD (their RGB is premultiplied)."""
import json
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
V2 = os.path.join(ROOT, "client", "assets", "v2")
FX, CH, WP = (os.path.join(V2, d) for d in ("fx", "chars", "weapons"))
PREV = os.path.join(ROOT, "art", "preview")
pygame.init()
pygame.display.set_mode((1, 1))
pygame.font.init()
FONT = pygame.font.Font(None, 22)
_c = {}


def sheet(d, id):
    k = (d, id)
    if k not in _c:
        meta = json.load(open(os.path.join(d, id + ".json"), encoding="utf-8"))
        _c[k] = (meta, pygame.image.load(os.path.join(d, id + ".png")).convert_alpha())
    return _c[k]


def frame(d, id, i):
    meta, img = sheet(d, id)
    w, h = meta["frame"]["w"], meta["frame"]["h"]
    r, c = divmod(i % meta["frames"], meta["cols"])
    return img.subsurface(pygame.Rect(c * w, r * h, w, h)), meta


def put(dst, d, id, i, at, flags=None):
    """blit frame i of a sheet so its PIVOT lands on `at`; fx sheets honour their blend mode."""
    fr, meta = frame(d, id, i)
    f = pygame.BLEND_RGB_ADD if (d == FX and meta.get("blend") == "add") else 0
    dst.blit(fr, (at[0] - meta["pivot"]["x"], at[1] - meta["pivot"]["y"]), special_flags=f)


def grass(w, h):
    meta = json.load(open(os.path.join(V2, "tiles", "base.json"), encoding="utf-8"))
    img = pygame.image.load(os.path.join(V2, "tiles", "base.png")).convert_alpha()
    idx = meta["tiles"]["grass"]
    s = pygame.Surface((w, h))
    for ty in range(0, h, 16):
        for tx in range(0, w, 16):
            i = idx[((tx // 16) * 5 + (ty // 16) * 3) % len(idx)]
            r, c = divmod(i, meta["cols"])
            s.blit(img, (tx, ty), pygame.Rect(c * 16, r * 16, 16, 16))
    return s


def label(surf, text, x, y):
    surf.blit(FONT.render(text, True, (225, 225, 235)), (x, y))


# ------------------------------------------------------------------------------ roi
def roi_proof():
    rar = ["pham", "linh", "huyen", "dia", "thien"]
    icons = ["kiem_1", "kiem_3", "kiem_4", "kiem_6", "kiem_8"]
    imeta = json.load(open(os.path.join(V2, "icons", "weapons_a.json"), encoding="utf-8"))
    iimg = pygame.image.load(os.path.join(V2, "icons", "weapons_a.png")).convert_alpha()
    cell = 96
    base = pygame.Surface((cell * 5, cell))
    base.blit(grass(cell * 5, cell), (0, 0))

    def scene(step):
        s = base.copy()
        for k, (r, ic) in enumerate(zip(rar, icons)):
            G = (k * cell + 48, 84)
            put(s, FX, "roi_vong_" + r, step, (G[0], G[1] - 2))
            n = imeta["icons"][ic]["index"]
            rr, cc = divmod(n, imeta["cols"])
            s.blit(iimg, (G[0] - 16, G[1] - 32), pygame.Rect(cc * 32, rr * 32, 32, 32))
            put(s, FX, "roi_cot_" + r, step, G)
        return s
    s0, s1 = scene(2), scene(5)
    W = cell * 5 * 3 + 20
    out = pygame.Surface((W, cell + cell * 3 + 90))
    out.fill((14, 14, 24))
    label(out, "1x  (step 2 and step 5 of the loop)    pham | linh | huyen | dia | thien", 10, 4)
    out.blit(s0, (10, 24))
    out.blit(s1, (10 + cell * 5 + 10, 24))
    label(out, "3x", 10, cell + 34)
    out.blit(pygame.transform.scale(s0, (cell * 15, cell * 3)), (10, cell + 54))
    pygame.image.save(out, os.path.join(PREV, "fx_tien_ich_roi_proof.png"))


# ------------------------------------------------------------------------------ phi
def phi_proof():
    cm, _ = sheet(CH, "dao_si_truc_co")
    ids = cm["clips"]["fly"]["frames"]["right"]
    steps = 6
    cw, chh = 128, 112
    LIFT = 24
    out = pygame.Surface((cw * 3 * 3 + 20, chh * 3 * 2 + 50))
    out.fill((14, 14, 24))
    label(out, "ngu kiem phi hanh: fly clip on phi_kiem_1, lifted 24 px; shadow, clouds, wake, wind  (6 steps, 3x)", 10, 4)
    for k in range(steps):
        s = pygame.Surface((cw, chh))
        s.blit(grass(cw, chh), (0, 0))
        G = (64, 92)                                  # ground point under the flyer
        head = (G[0], G[1] - LIFT)                    # character pivot (feet on the sword)
        put(s, FX, "phi_bong", k, G)                  # shadow (ground, alpha), smaller because it is high
        sh, _ = frame(FX, "phi_bong", k)
        put(s, FX, "phi_may", k, (head[0], head[1] + 6))
        put(s, FX, "phi_vet", k, (head[0] - 12, head[1] - 1))
        ci = ids[k % 4]
        put(s, FX, "phi_gio", k, (head[0] - 6, head[1] - 22))      # wind: behind the character
        put(s, CH, "dao_si_truc_co", ci, head)
        put(s, WP, "phi_kiem_1", ci, head)
        r, c = divmod(k, 3)
        out.blit(pygame.transform.scale(s, (cw * 3, chh * 3)), (10 + c * (cw * 3 + 0), 24 + r * (chh * 3 + 4)))
    pygame.image.save(out, os.path.join(PREV, "fx_tien_ich_phi_proof.png"))
    # take-off and landing on the ground (one-shot) in a second strip
    n1, n2 = 7, 6
    s = pygame.Surface((96 * (n1 + n2), 96))
    s.blit(grass(96 * (n1 + n2), 96), (0, 0))
    for i in range(n1):
        put(s, FX, "phi_cat_canh", i, (i * 96 + 48, 48))
    for i in range(n2):
        put(s, FX, "phi_ha_canh", i, ((n1 + i) * 96 + 48, 48))
    big = pygame.transform.scale(s, (s.get_width() * 2, s.get_height() * 2))
    pygame.image.save(big, os.path.join(PREV, "fx_tien_ich_phi_ground_proof.png"))


# ------------------------------------------------------------------------------ linh can
def linh_proof():
    Z = 2
    cw = 128
    rows = [("burst frame 3", "linh_can_%d", 3), ("burst frame 7", "linh_can_%d", 7), ("pillar", "linh_can_tru_%d", 2)]
    W = 9 * cw * Z + 20
    H = len(rows) * (cw * Z + 6) + 30
    out = pygame.Surface((W, H))
    out.fill((10, 10, 16))
    names = ["1 Pham", "2 Hoang", "3 Huyen", "4 Dia", "5 Thien", "6 Thanh", "7 Tien", "8 Than", "9 Hon Don"]
    for ri, (lab, pat, fr) in enumerate(rows):
        for g in range(1, 10):
            s = pygame.Surface((cw, cw))
            s.fill((20, 20, 32))
            pygame.draw.rect(s, (30, 30, 44), (0, 108, cw, 20))           # hall floor
            B = (64, 108)
            put(s, FX, "trac_linh_thach", fr, B)
            put(s, FX, pat % g, fr, B)
            out.blit(pygame.transform.scale(s, (cw * Z, cw * Z)), (10 + (g - 1) * cw * Z, 24 + ri * (cw * Z + 6)))
            if ri == 0:
                label(out, names[g - 1], 14 + (g - 1) * cw * Z, 6)
        label(out, lab, 14, 24 + ri * (cw * Z + 6) + 4)
    pygame.image.save(out, os.path.join(PREV, "fx_tien_ich_linh_can_proof.png"))


if __name__ == "__main__":
    roi_proof()
    phi_proof()
    linh_proof()
    print("proofs written to", PREV)
