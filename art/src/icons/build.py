"""Rebuild the ICONS batch: models -> one .blend per atlas -> kit render -> pack -> QC -> sheets.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/icons/build.py [--only cong_phap,misc]
    ... build.py --dev sach_3,dan_5 [--scale 6]     # look at a few icons only (art/render/icons_dev)

Atlases: cong_phap (24), dan_duoc (16), linh_thao (12), trang_bi (24), misc (10).  A partial run
(--only) rewrites only those atlases and their sheets; the other atlases (this batch's or any
other batch's) are never touched.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

from kit import launcher, palette, qc  # noqa: E402

BATCH = "icons"
ICON_DIR = ROOT / "client/assets/v2/icons"
ALL = ["cong_phap", "dan_duoc", "linh_thao", "trang_bi", "misc"]


def contact_sheet(atlas_json: Path, out: Path, scale: int = 3, title: str = ""):
    """Rows = grade (1 at the top), icons of one grade side by side, 3x nearest, dark background."""
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    doc = json.loads(atlas_json.read_text(encoding="utf-8"))
    sheet = pygame.image.load(str(atlas_json.with_suffix(".png")))
    cell, cols = doc["cell"], doc["cols"]
    cs = cell * scale
    pad, head = 6, 22
    rows = {}
    for iid, ic in doc["icons"].items():
        rows.setdefault(ic["grade"], []).append((ic["index"], iid))
    grades = sorted(rows)
    ncol = max(len(v) for v in rows.values())
    W = pad + ncol * (cs + pad)
    H = head + pad + len(grades) * (cs + pad)
    img = pygame.Surface((W, H))
    img.fill((8, 8, 12))
    font = pygame.font.Font(None, 20)
    img.blit(font.render(title or atlas_json.stem, True, (200, 200, 210)), (pad, 4))
    for r, g in enumerate(grades):
        for c, (i, iid) in enumerate(sorted(rows[g])):
            src = sheet.subsurface(pygame.Rect((i % cols) * cell, (i // cols) * cell, cell, cell))
            img.blit(pygame.transform.scale(src, (cs, cs)), (pad + c * (cs + pad), head + pad + r * (cs + pad)))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print("contact sheet:", out)


def main(argv):
    only = ALL
    if "--only" in argv:
        only = argv[argv.index("--only") + 1].split(",")
    dev = "--dev" in argv
    scale = int(argv[argv.index("--scale") + 1]) if "--scale" in argv else (5 if dev else 3)
    args = ["--only", ",".join(only)]
    out_dir = ICON_DIR
    if dev:
        args += ["--dev", argv[argv.index("--dev") + 1], "--outdir", "art/render/icons_dev"]
        out_dir = ROOT / "art/render/icons_dev"
    code = launcher.run_blender(Path(__file__).with_name("scene.py"), BATCH, args)
    if code:
        return code
    colors = palette.load().color_set
    bad = 0
    for name in only:
        js = out_dir / (name + ".json")
        if not js.exists() or (dev and not js.exists()):
            continue
        problems = qc.check_file(js, colors)
        for p in problems:
            print(" -", name, p)
        print("qc", name, "FAIL" if problems else "OK", f"({len(problems)} problem(s))")
        bad += len(problems)
        sheet = (ROOT / "art/render/icons_dev" / f"dev_{name}.png") if dev else (ROOT / "art/preview" / f"icons_{name}.png")
        contact_sheet(js, sheet, scale, title=name)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
