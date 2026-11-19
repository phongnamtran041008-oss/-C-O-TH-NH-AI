#!/usr/bin/env python3
"""Rebuild the MONSTERS_A batch: models, rigs, clips, .blend files, sprite sheets, QC and
contact sheets. Run with the game's venv python:

    python art/src/monsters_a/build.py                 # all six creatures
    python art/src/monsters_a/build.py --only van_xa   # one (or a comma list)
    python art/src/monsters_a/build.py --jobs 2        # Blenders at once (default 3)
    python art/src/monsters_a/build.py --no-render     # only the .blend files

Each creature is built and rendered in its own headless Blender (scene.py through
kit.launcher), so several run side by side. Output:

    art/blender/monsters/<id>.blend
    client/assets/v2/monsters/<id>.png/.json and <id>_di.png/.json
    art/preview/monsters_a_<id>.png    every clip, both looks
    art/preview/monsters_a.png         overview: idle / windup / attack, facing down + right
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

from kit import contact, launcher, qc  # noqa: E402
from kit import palette as P  # noqa: E402

SETS = {
    "a": ["kiem_linh", "thach_khoi", "ma_tran_thu", "van_xa", "phong_lang", "tam_ma"],
    "b": ["dau_tu_oa", "ho_lo_tinh", "tri_chu_tinh", "moc_yeu", "co_quan_nhan", "loi_long"],
}
SETS["beasts"] = ["linh_ho", "huyen_quy", "bach_hac", "hoa_tuoc", "tieu_long", "ky_lan_con"]
SETS["pets"] = ["pet_" + s for s in ("chuot", "trau", "ho", "meo", "rong", "ran", "ngua", "de", "khi", "ga", "cho", "lon")]
IDS = SETS["a"] + SETS["b"] + SETS["beasts"] + SETS["pets"]
PREFIX = {i: (f"monsters_{s}" if s not in ("beasts", "pets") else s) for s, ids in SETS.items() for i in ids}
BEAST_OUT = ROOT / "client" / "assets" / "v2" / "beasts"


def out_dir(mid):
    return BEAST_OUT if mid in SETS["beasts"] or mid in SETS["pets"] else OUT


def looks(mid):
    return [mid] if mid in SETS["beasts"] or mid in SETS["pets"] else [mid, f"{mid}_di"]


BEE_SCENE = Path(__file__).with_name("bee_scene.py")


def bee_ids():
    data = json.loads((ROOT / "server" / "data" / "creatures" / "bees.json").read_text("utf-8"))
    return [k for k in data if not k.startswith("_")]


def bees_overview(out: Path):
    """All bee species at 4x: fly (right) x4 and sting (right) x2, on dark and on grass."""
    import pygame
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))
    tiles = json.loads((ROOT / "client" / "assets" / "v2" / "tiles" / "base32.json").read_text("utf-8"))
    tsheet = pygame.image.load(str(ROOT / "client" / "assets" / "v2" / "tiles" / tiles["sheet"]))
    tc = tiles.get("tile", 32)
    names = tiles["tiles"]
    key = "grass" if "grass" in names else next((k for k in names if "grass" in k), next(iter(names)))
    grass = [contact._cell(tsheet, i, tiles["cols"], tc, tc) for i in names[key]]
    Z, pad, lab = 4, 6, 150
    fs = 32
    rows = []
    ones = []
    for sid in bee_ids():
        f = BEAST_OUT / f"bee_{sid}.json"
        if not f.exists():
            continue
        doc = json.loads(f.read_text("utf-8"))
        sheet = pygame.image.load(str(BEAST_OUT / doc["sheet"]))
        cl = doc["clips"]
        picks = cl["fly"]["frames"]["right"] + cl["sting"]["frames"]["right"] + [cl["fly"]["frames"]["left"][0]]
        fs = doc["frame"]["w"]
        rows.append((f"{doc.get('name_vi', sid)}", [contact._cell(sheet, i, doc["cols"], fs, fs) for i in picks]))
        ones.append(contact._cell(sheet, cl["fly"]["frames"]["right"][0], doc["cols"], fs, fs))
    cell = fs * Z
    n = len(rows[0][1]) if rows else 7
    width = lab + 2 * (n * (cell + 2) + 12) + pad
    strip = 2 * tc + 24          # the 1x strip on grass, as the player sees them
    height = 30 + strip + len(rows) * (cell + 4) + pad
    img = pygame.Surface((width, height))
    img.fill(contact.BG)
    img.blit(contact._font(14).render("BEES  top: all 18 at 1x on grass  |  then x4: fly right x4 | sting right x2 | fly left, on dark | on grass", True, contact.TEXT), (pad, 8))
    gw = len(ones) * (fs + 4) + 16
    for gx in range(0, gw, tc):
        for gy in range(0, 2 * tc, tc):
            img.blit(grass[(gx // tc + gy // tc) % len(grass)], (pad + gx, 30 + gy))
    for k, s1 in enumerate(ones):
        img.blit(s1, (pad + 8 + k * (fs + 4), 30 + (k % 2) * 14 + 8))
    for r, (name, cells) in enumerate(rows):
        y = 30 + strip + r * (cell + 4)
        img.blit(contact._font(12).render(name, True, contact.DIM), (pad, y + 6))
        for half in (0, 1):
            x0 = lab + half * (n * (cell + 2) + 12)
            for c, s in enumerate(cells):
                x = x0 + c * (cell + 2)
                if half:
                    g = pygame.transform.scale(grass[(r + c) % len(grass)], (cell, cell))
                    img.blit(g, (x, y))
                else:
                    pygame.draw.rect(img, contact.PANEL, (x, y, cell, cell))
                img.blit(pygame.transform.scale(s, (cell, cell)), (x, y))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"bees overview: {out}")


def build_bees(no_render: bool) -> int:
    code = launcher.run_blender(BEE_SCENE, "monsters_a", ["--no-render"] if no_render else [])
    print(f"[monsters_a] bees: blender exit {code}", flush=True)
    if code or no_render:
        return code
    colors = P.load().color_set
    bad = 0
    for sid in bee_ids():
        f = BEAST_OUT / f"bee_{sid}.json"
        probs = qc.check_file(f, colors) if f.exists() else [f"bee_{sid}: missing"]
        for pr in probs:
            print(f" - {pr}")
        bad += len(probs)
    print(f"qc bees: {'FAIL' if bad else 'OK'} ({len(bee_ids())} sheets, {bad} problem(s))")
    bees_overview(PREVIEW / "bees.png")
    return 1 if bad else 0


def pets_overview(ids, out: Path):
    """Each pet: idle down / right, a walk cycle (right), happy and sleep, at 3x; the
    Luyện Khí player beside the first row at the same 3x (the game draws beast and player
    sheets at the same scale per sheet pixel; compare art/preview/game_hub_idle.png)."""
    import pygame
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))
    rows = []
    for mid in ids:
        f = BEAST_OUT / f"{mid}.json"
        if not f.exists():
            continue
        doc = json.loads(f.read_text("utf-8"))
        sheet = pygame.image.load(str(BEAST_OUT / doc["sheet"]))
        fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
        cl = doc["clips"]
        picks = [cl["idle"]["frames"]["down"][0], cl["idle"]["frames"]["right"][0]] + cl["walk"]["frames"]["right"] \
            + [cl["happy"]["frames"]["down"][1], cl["sleep"]["frames"]["down"][0]]
        rows.append((doc.get("name_vi", mid), [contact._cell(sheet, i, cols, fw, fh) for i in picks]))
    Z, pad, lab = 3, 6, 120
    cell = 48 * Z
    player = None
    pj = ROOT / "client" / "assets" / "v2" / "chars" / "dao_si_luyen_khi.json"
    if pj.exists():
        pd = json.loads(pj.read_text("utf-8"))
        ps = pygame.image.load(str(pj.parent / pd["sheet"]))
        pf = contact._cell(ps, pd["clips"]["idle"]["frames"]["down"][0], pd["cols"], pd["frame"]["w"], pd["frame"]["h"])
        player = (pygame.transform.scale(pf, (pf.get_width() * Z, pf.get_height() * Z)), pd["pivot"])
    pw = player[0].get_width() + pad if player else 0
    top = 30 + (max(0, int(player[1]["y"] * Z) - 42 * Z) if player else 0)   # room for the player's head
    width = lab + pw + 10 * (cell + 2) + pad
    height = top + len(rows) * (cell + 4) + pad
    img = pygame.Surface((width, height))
    img.fill(contact.BG)
    f = contact._font(14)
    img.blit(f.render("PETS  idle down | idle right | walk (right) x6 | happy | sleep   (x3; player x3 = in-game scale)", True, contact.TEXT), (pad, 8))
    for r, (name, cells) in enumerate(rows):
        y = top + r * (cell + 4)
        img.blit(contact._font(12).render(name, True, contact.DIM), (pad, y + 6))
        x0 = lab + pw
        for c, s in enumerate(cells):
            pygame.draw.rect(img, contact.PANEL, (x0 + c * (cell + 2), y, cell, cell))
            img.blit(pygame.transform.scale(s, (cell, cell)), (x0 + c * (cell + 2), y))
        if r == 0 and player:
            pimg, pv = player
            # stand the player on the same ground line as the pet's pivot (y 42 of 48)
            gy = y + 42 * Z
            img.blit(pimg, (lab, gy - int(pv["y"] * Z)))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"pets overview: {out}")
OUT = ROOT / "client" / "assets" / "v2" / "monsters"
PREVIEW = ROOT / "art" / "preview"
SCENE = Path(__file__).with_name("scene.py")


def build_one(mid: str, no_render: bool) -> int:
    args = ["--id", mid] + (["--no-render"] if no_render else [])
    code = launcher.run_blender(SCENE, "monsters_a", args)
    print(f"[monsters_a] {mid}: blender exit {code}", flush=True)
    return code


def run_qc(ids) -> int:
    colors = P.load().color_set
    bad = 0
    for mid in ids:
        for name in looks(mid):
            f = out_dir(mid) / f"{name}.json"
            if not f.exists():
                print(f" - {name}: missing")
                bad += 1
                continue
            probs = qc.check_file(f, colors)
            for p in probs:
                print(f" - {p}")
            bad += len(probs)
    print(f"qc monsters_a: {'FAIL' if bad else 'OK'} ({sum(len(looks(m)) for m in ids)} sheets, {bad} problem(s))")
    return bad


def overview(ids, out: Path):
    """idle (first frame), windup (the held pose) and attack (the hit frame), facing down
    and right, normal look then dị chủng."""
    import pygame
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))
    cv = contact.Canvas()
    cv.title(f"{out.stem.upper()}  idle / windup / attack(hit) [/ special | happy / sleep]  facing down | right   (x3)")
    for mid in ids:
        for name in looks(mid):
            f = out_dir(mid) / f"{name}.json"
            if not f.exists():
                continue
            doc = json.loads(f.read_text("utf-8"))
            sheet = pygame.image.load(str(out_dir(mid) / doc["sheet"]))
            fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
            pv = (doc["pivot"]["x"], doc["pivot"]["y"])
            hit = doc.get("events", {}).get("attack", {}).get("hit", 1)
            cells = []
            for d in ("down", "right"):
                extra = (("special", doc.get("events", {}).get("special", {}).get("hit", 0)),) \
                    if "special" in doc["clips"] else ()
                extra += tuple((c, 1) for c in ("happy", "sleep") if c in doc["clips"])
                for clip, k in (("idle", 0), ("windup", -1), ("attack", hit)) + extra:
                    i = doc["clips"][clip]["frames"][d][k]
                    cells.append(contact._cell(sheet, i, cols, fw, fh))
            cv.strip(name, cells, [pv] * len(cells))
    img = cv.render()
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(f"overview: {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--set", default="all", choices=["a", "b", "beasts", "pets", "bees", "all"])
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()
    if a.set == "bees":
        return build_bees(a.no_render)
    ids = [i for i in a.only.split(",") if i] or (IDS if a.set == "all" else SETS[a.set])
    for i in ids:
        if i not in IDS:
            sys.exit(f"unknown id {i!r}; one of {IDS}")
    with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
        codes = list(ex.map(lambda m: build_one(m, a.no_render), ids))
    if any(codes):
        print("[monsters_a] some Blender runs failed; see art/render/monsters_a/*.log")
        return 1
    if a.no_render:
        return 0
    bad = run_qc(ids)
    for mid in ids:
        out = PREVIEW / f"{PREFIX[mid]}_{mid}.png"
        contact.write([out_dir(mid) / f"{n}.json" for n in looks(mid)], out, title=f"{PREFIX[mid]} {mid}")
        print(f"contact sheet: {out}")
    for s in sorted({s for s, members in SETS.items() if set(members) & set(ids)}):
        if s == "pets":
            pets_overview(SETS["pets"], PREVIEW / "pets.png")
            continue
        overview([m for m in SETS[s] if (out_dir(m) / f"{m}.json").exists()],
                 PREVIEW / (f"monsters_{s}.png" if s != "beasts" else "beasts.png"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
