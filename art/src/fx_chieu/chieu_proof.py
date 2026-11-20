"""Contact sheets and proofs in context for the fx_chieu batch (pygame only, no Pillow / numpy).

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/fx_chieu/chieu_proof.py [--contact-only]

Writes
- art/preview/fx_chieu_<group>.png : one row per sheet, frames 3x nearest-neighbour on a dark background
  (left half of every row) and on grass tiles (right half), additive sheets drawn with BLEND_ADD.
- art/preview/fx_chieu_proof.png    : for each skill a small scene on grass at the game's 2x world zoom, then 2x again:
  the caster (dao_si_luyen_khi, clip cast, facing right) with its tu_khi_<element>, the skill mid-effect, a monster
  (phong_lang / thach_khoi, clip hit or idle, facing left) taking it.
- art/preview/fx_chieu_proof_1x.png: the same scenes at 1x (the art's own pixels).
"""
import json
import os
import sys

sys.dont_write_bytecode = True
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
V2 = os.path.join(ROOT, "client", "assets", "v2")
PREV = os.path.join(ROOT, "art", "preview")
sys.path.insert(0, HERE)
from ids import GROUPS  # noqa: E402

pygame.init()
pygame.display.set_mode((1, 1))
_cache = {}
BG = (14, 14, 24)


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
    index = index % meta["frames"] if kind == "fx" else index
    r, c = divmod(index, meta["cols"])
    return img.subsurface(pygame.Rect(c * w, r * h, w, h)).copy(), meta


def blit_fx(dst, id, index, x, y, scale=1.0, flip=False, rot=0.0, sx=None):
    """draw fx frame with its pivot at (x, y) (dst pixels), additive or alpha as the sheet says."""
    s, m = frame("fx", id, index)
    px, py = m["pivot"]["x"], m["pivot"]["y"]
    w, h = s.get_size()
    kx = sx if sx is not None else scale
    if kx != 1.0 or scale != 1.0:
        s = pygame.transform.scale(s, (max(1, round(w * kx)), max(1, round(h * scale))))
        px, py = px * kx, py * scale
    if flip:
        s = pygame.transform.flip(s, True, False)
        px = s.get_width() - px
    if rot:
        # rotate about the pivot
        import math
        cw, ch = s.get_size()
        ox, oy = px - cw / 2, py - ch / 2
        s = pygame.transform.rotate(s, rot)
        a = math.radians(rot)
        rx = ox * math.cos(a) + oy * math.sin(a)
        ry = -ox * math.sin(a) + oy * math.cos(a)
        px, py = s.get_width() / 2 + rx, s.get_height() / 2 + ry
    flags = pygame.BLEND_RGB_ADD if m["blend"] == "add" else 0
    dst.blit(s, (round(x - px), round(y - py)), special_flags=flags)


def grass(w, h, dark=False):
    meta = json.load(open(os.path.join(V2, "tiles", "base.json"), encoding="utf-8"))
    img = pygame.image.load(os.path.join(V2, "tiles", "base.png")).convert_alpha()
    idx = meta["tiles"]["dark_grass" if dark else "grass"]
    cols = meta["cols"]
    surf = pygame.Surface((w, h))
    for ty in range(0, h, 16):
        for tx in range(0, w, 16):
            i = idx[((tx // 16) * 7 + (ty // 16) * 3) % len(idx)]
            r, c = divmod(i, cols)
            surf.blit(img, (tx, ty), pygame.Rect(c * 16, r * 16, 16, 16))
    return surf


# ----------------------------------------------------------------------------- contact sheets
def contact(group, ids, zoom=3):
    font = pygame.font.Font(None, 22)
    rows = []
    for id in ids:
        try:
            meta, img = sheet("fx", id)
        except FileNotFoundError:
            continue
        w, h, n = meta["frame"]["w"], meta["frame"]["h"], meta["frames"]
        g = grass(w, h)
        row = pygame.Surface((2 * n * (w * zoom + 2) + 30, h * zoom + 22))
        row.fill((8, 8, 14))
        lab = "%s  %dx%d  %d fr  %d fps  %s  %s%s  pivot %d,%d" % (
            id, w, h, n, meta["fps"], "loop" if meta["loop"] else "once", meta["blend"],
            "  ground" if meta["ground"] else "", meta["pivot"]["x"], meta["pivot"]["y"])
        row.blit(font.render(lab, True, (215, 215, 230)), (4, 2))
        for bgi, base in enumerate((None, g)):
            for i in range(n):
                c = pygame.Surface((w, h))
                if base is None:
                    c.fill(BG)
                else:
                    c.blit(base, (0, 0))
                blit_fx(c, id, i, meta["pivot"]["x"], meta["pivot"]["y"])
                x = bgi * (n * (w * zoom + 2) + 30) + i * (w * zoom + 2)
                row.blit(pygame.transform.scale(c, (w * zoom, h * zoom)), (x, 20))
        rows.append(row)
    if not rows:
        return
    W = max(r.get_width() for r in rows)
    H = sum(r.get_height() + 6 for r in rows)
    out = pygame.Surface((W, H))
    out.fill((8, 8, 14))
    y = 0
    for r in rows:
        out.blit(r, (0, y))
        y += r.get_height() + 6
    path = os.path.join(PREV, "fx_chieu_%s.png" % group)
    pygame.image.save(out, path)
    print("wrote", os.path.relpath(path, ROOT), out.get_size())


# ----------------------------------------------------------------------------- proof in context
CELL_W, CELL_H = 240, 135              # what a 480x270 screen shows of the world at 2x zoom
CX, CY = 46, 100                       # caster's feet in the cell
MX, MY = 186, 100                      # monster's feet


def char_frame(clip, k, face="right"):
    meta, _ = sheet("chars", "dao_si_luyen_khi")
    idx = meta["clips"][clip]["frames"][face][k]
    f, _ = frame("chars", "dao_si_luyen_khi", idx)
    return f, meta


def mon_frame(mid, clip, k, face="left"):
    meta, _ = sheet("monsters", mid)
    fr = meta["clips"][clip]["frames"][face]
    f, _ = frame("monsters", mid, fr[k % len(fr)])
    return f, meta


def put(dst, surf, meta, x, y):
    dst.blit(surf, (x - meta["pivot"]["x"], y - meta["pivot"]["y"]))


# scenes: (title, element, monster, monster clip, [layers]); a layer is (when, id, frame, x, y, kw)
#   when: 'under' = before the characters (ground), 'mid' = between caster and monster, 'over' = after both
def scenes():
    hand = (CX + 12, CY - 30)             # the cast hand (facing right), measured on the cast hit frame
    chest = (CX, CY - 26)
    mon = (MX, MY - 18)
    S = []
    S.append(("Ngu Kiem Thuat", "kim", "phong_lang", "hit", [
        ("over", "ngu_kiem", 1, 120, CY - 28, {}),
        ("over", "ngu_kiem_xuyen", 1, MX - 2, MY - 18, {})]))
    S.append(("Van Kiem Quy Tong", "kim", "thach_khoi", "hit", [
        ("under", "van_kiem_vong", 2, MX - 8, MY - 2, {}),
        ("over", "van_kiem_troi", 6, MX - 8, MY - 2, {}),
        ("over", "van_kiem_roi", 4, MX - 8, MY - 2, {})]))
    S.append(("Bang Phong Thuat", "thuy", "phong_lang", "hit", [
        ("over", "bang_phong", 3, MX, MY + 2, {}),
        ("over", "bang_ket", 1, MX, MY, {})]))
    S.append(("Chuong Tam Loi", "loi", "phong_lang", "hit", [
        ("over", "loi_xich", 1, hand[0] + 2, hand[1], dict(sx=(MX - 4 - hand[0]) / 89.0, rot=-8)),
        ("over", "loi_cham", 1, MX - 4, MY - 18, {})]))
    S.append(("Hoa Long Thuat", "hoa", "phong_lang", "hit", [
        ("under", "hoa_long_vet", 2, 100, MY - 2, {}),
        ("over", "hoa_long", 2, 136, CY - 30, {})]))
    S.append(("Dia Liet Tram", "tho", "thach_khoi", "hit", [
        ("under", "dia_liet", 5, CX + 14, MY, {}),
        ("over", "dia_liet_no", 2, MX, MY + 1, {})]))
    S.append(("Thanh Dang Trien", "moc", "phong_lang", "hit", [
        ("over", "thanh_dang", 6, MX, MY + 2, {}),
        ("over", "thanh_dang_troi", 1, MX, MY, {})]))
    S.append(("Phong Nhan Thuat", "kim", "phong_lang", "hit", [
        ("over", "phong_nhan", 1, 110, CY - 34, dict(rot=8)),
        ("over", "phong_nhan", 2, 128, CY - 22, {}),
        ("over", "phong_nhan", 3, 116, CY - 10, dict(rot=-8)),
        ("over", "phong_xoay", 2, MX, MY + 1, {})]))
    S.append(("Kim Chung Trao", "kim", "thach_khoi", "idle", [
        ("over", "kim_chung_tru", 2, CX, CY, {}),
        ("over", "kim_chung_vang", 1, CX, CY, {})]))
    S.append(("Kiem Vuc", "kim", "phong_lang", "hit", [
        ("under", "kiem_vuc", 3, CX + 10, CY, {}),
        ("over", "kiem_vuc_xoay", 2, CX, CY, {})]))
    S.append(("Hoi Xuan Thuat", "moc", "phong_lang", "idle", [
        ("over", "hoi_xuan", 4, CX, CY, {})]))
    S.append(("Hoa Cau (hero)", "hoa", "phong_lang", "hit", [
        ("over", "hoa_cau_lon", 1, 118, CY - 28, {}),
        ("over", "hoa_cau_no", 2, MX, MY - 16, {})]))
    S.append(("Thien Loi Giang (hero)", "loi", "thach_khoi", "hit", [
        ("over", "thien_loi_giang", 1, MX, MY + 1, {})]))
    S.append(("Pha Me Kiem (hero)", "kim", "phong_lang", "hit", [
        ("over", "pha_me_kiem", 1, hand[0], hand[1], {})]))
    return S, chest


def cell(sc, chest):
    title, el, mid, mclip, layers = sc
    c = grass(CELL_W, CELL_H)
    for when, id, k, x, y, kw in layers:
        if when == "under" and os.path.exists(os.path.join(V2, "fx", id + ".json")):
            blit_fx(c, id, k, x, y, **kw)
    cmeta, _ = sheet("chars", "dao_si_luyen_khi")
    hit = cmeta.get("events", {}).get("cast", {}).get("hit", 3)
    body, _ = char_frame("cast", hit)
    put(c, body, cmeta, CX, CY)
    if os.path.exists(os.path.join(V2, "fx", "tu_khi_%s.json" % el)) and title != "Kim Chung Trao":
        blit_fx(c, "tu_khi_" + el, 2, chest[0] + 6, chest[1] - 2, scale=0.75)
    mf, mm = mon_frame(mid, mclip, 0)
    put(c, mf, mm, MX, MY)
    for when, id, k, x, y, kw in layers:
        if when == "over" and os.path.exists(os.path.join(V2, "fx", id + ".json")):
            blit_fx(c, id, k, x, y, **kw)
    return c


def proof():
    S, chest = scenes()
    cells = [(sc[0], cell(sc, chest)) for sc in S]
    font = pygame.font.Font(None, 30)
    ncol = 4
    nrow = (len(cells) + ncol - 1) // ncol
    for zoom, name in ((4, "fx_chieu_proof.png"), (1, "fx_chieu_proof_1x.png")):
        lab = 26 if zoom > 1 else 12
        f = font if zoom > 1 else pygame.font.Font(None, 14)
        W = ncol * (CELL_W * zoom + 6) + 6
        H = nrow * (CELL_H * zoom + lab + 6) + 6
        out = pygame.Surface((W, H))
        out.fill((10, 10, 16))
        for n, (t, c) in enumerate(cells):
            r, k = divmod(n, ncol)
            x, y = 6 + k * (CELL_W * zoom + 6), 6 + r * (CELL_H * zoom + lab + 6)
            out.blit(f.render(t, True, (220, 220, 232)), (x + 2, y))
            out.blit(pygame.transform.scale(c, (CELL_W * zoom, CELL_H * zoom)), (x, y + lab))
        pygame.image.save(out, os.path.join(PREV, name))
        print("wrote art/preview/" + name, out.get_size())


def look(ids, path, zoom=2):
    """review helper (not part of the build): each sheet as two rows, dark then grass, at `zoom`."""
    rows = []
    for id in ids:
        meta, img = sheet("fx", id)
        w, h, n = meta["frame"]["w"], meta["frame"]["h"], meta["frames"]
        g = grass(w, h)
        row = pygame.Surface((n * (w * zoom + 2), 2 * (h * zoom + 2)))
        row.fill((8, 8, 14))
        for bgi in (0, 1):
            for i in range(n):
                c = pygame.Surface((w, h))
                if bgi:
                    c.blit(g, (0, 0))
                else:
                    c.fill(BG)
                blit_fx(c, id, i, meta["pivot"]["x"], meta["pivot"]["y"])
                row.blit(pygame.transform.scale(c, (w * zoom, h * zoom)), (i * (w * zoom + 2), bgi * (h * zoom + 2)))
        rows.append(row)
    W = max(r.get_width() for r in rows)
    out = pygame.Surface((W, sum(r.get_height() + 8 for r in rows)))
    y = 0
    for r in rows:
        out.blit(r, (0, y))
        y += r.get_height() + 8
    pygame.image.save(out, path)


if __name__ == "__main__":
    if "--look" in sys.argv:
        a = sys.argv[sys.argv.index("--look") + 1:]
        look(a[0].split(","), a[1], int(a[2]) if len(a) > 2 else 2)
        sys.exit(0)
    for g, ids in GROUPS.items():
        contact(g, ids)
    if "--contact-only" not in sys.argv:
        proof()
