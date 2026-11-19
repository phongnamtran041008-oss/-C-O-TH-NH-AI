"""Rebuild the whole WEAPONS_A batch: models -> .blend -> kit render -> pack -> QC -> contact sheet.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_a/build.py [--only kiem_3,dao_5]

The icon folder is shared with other batches, so QC and the sheet look only at our own atlas.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

from kit import launcher, qc, palette  # noqa: E402

BATCH = "weapons_a"
ATLAS = ROOT / "client/assets/v2/icons/weapons_a"
TYPES = ["kiem", "dao", "thuong", "chuy"]
TYPE_VI = {"kiem": "Kiếm", "dao": "Đao", "thuong": "Thương", "chuy": "Chùy"}
SCALE = 3


def contact_sheet(out: Path):
    """Types in columns, grades in rows (like the reference), 3x nearest, dark background."""
    import os
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    doc = json.loads(ATAZ_JSON.read_text(encoding="utf-8"))
    sheet = pygame.image.load(str(ATLAS.with_suffix(".png")))
    cell, cols = doc["cell"], doc["cols"]
    cs = cell * SCALE
    pad, head = 6, 22
    W = pad + len(TYPES) * (cs + pad)
    H = head + pad + 8 * (cs + pad)
    img = pygame.Surface((W, H))
    img.fill((8, 8, 12))
    font = pygame.font.Font(None, 20)
    for c, t in enumerate(TYPES):
        x = pad + c * (cs + pad)
        img.blit(font.render(t, True, (200, 200, 210)), (x, 4))
        for g in range(1, 9):
            ic = doc["icons"].get(f"{t}_{g}")
            if not ic:
                continue
            i = ic["index"]
            src = sheet.subsurface(pygame.Rect((i % cols) * cell, (i // cols) * cell, cell, cell))
            big = pygame.transform.scale(src, (cs, cs))
            img.blit(big, (x, head + pad + (g - 1) * (cs + pad)))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print("contact sheet:", out)


ATAZ_JSON = ATLAS.with_suffix(".json")


def main(argv):
    code = launcher.run_blender(Path(__file__).with_name("scene.py"), BATCH, argv)
    if code:
        return code
    colors = palette.load().color_set
    problems = qc.check_file(ATAZ_JSON, colors)
    for p in problems:
        print(" -", p)
    print("qc weapons_a:", "FAIL" if problems else "OK", f"({len(problems)} problem(s))")
    contact_sheet(ROOT / "art/preview/weapons_a.png")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
