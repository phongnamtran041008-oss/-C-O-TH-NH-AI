#!/usr/bin/env python3
"""CHARS batch (v2): the player - one body, one rig, eight realm looks, ten clips.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/chars/build.py [--only <id> ...] [--gate] [--jobs N]

Each look is built from art/src/chars/v2/*.py (+ the look-dev pieces in lookdev/ and the
solver in rig.py / clips.py), saved to art/blender/chars/<id>.blend, then rendered and packed
through tools/blender/kit: 96x96 frames, pivot (48,82), 48 px/m, camera 15 degrees, head snapped
to the pixel grid. rig_base.blend = body + rig + all actions, no outfit (for weapon layers).

--gate renders only idle (all facings) into art/render/chars/gate/ and writes the
reference-beside-ours overview art/preview/chars_overview.png - the self-review gate before
the full render.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

from kit import launcher  # noqa: E402

BATCH = "chars"
LOOKS = ["dao_si_luyen_khi", "dao_si_truc_co", "dao_si_ket_dan", "dao_si_nguyen_anh",
         "dao_si_hoa_than", "dao_si_luyen_hu", "dao_si_hop_the", "dao_si_dai_thua"]
REF_ROW = {lid: i for i, lid in enumerate(LOOKS)}
OUT = "client/assets/v2/chars"
GATE = "art/render/chars/gate"
BLEND_DIR = "art/blender/chars"
PREVIEW = ROOT / "art" / "preview"
REF = ROOT / "art" / "reference" / "nhan_vat" / "nhan_vat_8_canh_gioi.webp"
Z = 4


def build_one(look_id: str, out_dir: str | None, clips: str = "") -> int:
    args = ["--look", look_id, "--out", f"{BLEND_DIR}/{look_id}.blend"]
    if out_dir and look_id != "rig_base":
        args += ["--render", out_dir]
        if clips:
            args += ["--clips", clips]
    code = launcher.run_blender(HERE / "v2" / "v2_main.py", BATCH, args)
    print(f"[chars] {look_id}: {'ok' if code == 0 else f'FAILED ({code})'}", flush=True)
    return code


def _pygame():
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    return pygame


def _cells(pg, folder, lid, picks):
    js = ROOT / folder / f"{lid}.json"
    if not js.exists():
        return None, None
    doc = json.loads(js.read_text("utf-8"))
    sh = pg.image.load(str(js.with_name(doc["sheet"])))
    fw, fh, cols = doc["frame"]["w"], doc["frame"]["h"], doc["cols"]
    out = []
    for c, d, i in picks:
        if c == "cast" and i == "hit":
            i = doc.get("events", {}).get("cast", {}).get("hit", 3)
        if c == "slash" and i == "hit":
            i = doc.get("events", {}).get("slash", {}).get("hit", 3)
        n = doc["clips"][c]["frames"][d][i]
        cell = sh.subsurface(((n % cols) * fw, (n // cols) * fh, fw, fh))
        out.append(pg.transform.scale(cell, (fw * Z, fh * Z)))
    return out, doc


def overview(folder: str, picks, out: Path, title: str) -> None:
    """Per look: the matching reference row (first two cells, scaled to our figure height)
    and our frames, all at 4x nearest-neighbour on a dark background."""
    pg = _pygame()
    ref = pg.image.load(str(REF))
    k = 48 / 104.0
    rows = []
    for lid in LOOKS:
        cells, doc = _cells(pg, folder, lid, picks)
        if cells is None:
            continue
        strip = ref.subsurface((0, REF_ROW[lid] * 128, 256, 128))
        small = pg.transform.smoothscale(strip, (round(256 * k), round(128 * k)))
        refimg = pg.transform.scale(small, (small.get_width() * Z, small.get_height() * Z))
        rows.append((doc.get("name_vi", lid), refimg, cells))
    if not rows:
        return
    cw = 96 * Z
    rw = rows[0][1].get_width()
    width = rw + 16 + len(picks) * cw
    height = 40 + len(rows) * (cw + 30)
    surf = pg.Surface((width, height))
    surf.fill((14, 13, 18))
    font = pg.font.SysFont(None, 30)
    surf.blit(font.render(title, True, (200, 196, 210)), (8, 8))
    y = 40
    for name, refimg, cells in rows:
        surf.blit(font.render(name, True, (170, 166, 180)), (8, y + 4))
        surf.blit(refimg, (0, y + 30 + (cw - refimg.get_height()) // 2))
        for j, c in enumerate(cells):
            surf.blit(c, (rw + 16 + j * cw, y + 30))
        y += cw + 30
    out.parent.mkdir(parents=True, exist_ok=True)
    pg.image.save(surf, str(out))
    print(f"[chars] {out}")


GATE_PICKS = [("idle", "down", 0), ("idle", "right", 0), ("idle", "up", 0)]
FINAL_PICKS = [("idle", "down", 0), ("idle", "right", 0), ("idle", "up", 0), ("walk", "right", 2),
               ("slash", "right", "hit"), ("slash", "down", "hit"), ("cast", "right", "hit"),
               ("fly", "right", 1), ("meditate", "down", 0)]


def cleanup_old() -> None:
    """The rejected 64 px build: v1-only previews and the kit's old whole-folder sheet."""
    for name in ("chars.png",):
        p = PREVIEW / name
        if p.exists():
            p.unlink()


def main(argv) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--sheets-only", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args(argv)
    ids = a.only or (["rig_base"] + LOOKS)
    if a.gate:
        ids = [i for i in ids if i != "rig_base"]
        if not a.sheets_only:
            with ThreadPoolExecutor(max_workers=a.jobs) as ex:
                codes = list(ex.map(lambda i: build_one(i, GATE, "idle"), ids))
            if any(codes):
                return 1
        overview(GATE, GATE_PICKS, PREVIEW / "chars_overview.png", "GATE: reference row | ours idle down, right")
        return 0
    if not a.sheets_only:
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            codes = list(ex.map(lambda i: build_one(i, OUT), ids))
        if any(codes):
            return 1
    from kit import contact, qc
    problems = qc.report(ROOT / OUT)
    for lid in LOOKS:
        js = ROOT / OUT / f"{lid}.json"
        if js.exists():
            contact.write([js], PREVIEW / f"chars_{lid[len('dao_si_'):]}.png", title=lid)
    overview(OUT, FINAL_PICKS, PREVIEW / "chars_overview.png",
             "reference | idle down, right, up | walk right | slash strike right, down | cast release | fly | meditate")
    cleanup_old()
    print(f"[chars] QC problems: {problems}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
