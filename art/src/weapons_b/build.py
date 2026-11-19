"""Rebuild WEAPONS_B: .blend per weapon -> kit icon render/pack -> kit QC -> contact sheet.

    python art/src/weapons_b/build.py                # everything
    python art/src/weapons_b/build.py --only cung_5  # rebuild only that .blend (atlas is always re-rendered whole)
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools" / "blender"))
from kit import launcher, paths, qc  # noqa: E402

ICONS = ROOT / "client" / "assets" / "v2" / "icons"
TYPES = ["truong", "cung", "phien", "ho_lo"]


def blends(only):
    cmd = [paths.BLENDER_EXE, "-b", "--factory-startup", "--python", str(HERE / "make_blends.py"), "--"] + only
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace")
    for line in r.stdout.splitlines():
        if line.startswith("MODEL"):
            print(line)
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-2000:], file=sys.stderr)
    return r.returncode


def contact_sheet(out):
    """Types in columns, grades in rows, 4x nearest-neighbour, dark background (like the reference)."""
    import os
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    doc = json.loads((ICONS / "weapons_b.json").read_text("utf-8"))
    sheet = pygame.image.load(str(ICONS / doc["sheet"]))
    c, cols, z = doc["cell"], doc["cols"], 4
    pad, head = 8, 26
    W = len(TYPES) * (c * z + pad) + pad
    H = 8 * (c * z + pad) + pad + head
    img = pygame.Surface((W, H))
    img.fill((10, 9, 14))
    font = pygame.font.Font(None, 20)
    for ci, t in enumerate(TYPES):
        x0 = pad + ci * (c * z + pad)
        img.blit(font.render(t, True, (190, 186, 200)), (x0, 6))
        for g in range(1, 9):
            ic = doc["icons"]["%s_%d" % (t, g)]
            i = ic["index"]
            cell = sheet.subsurface(((i % cols) * c, (i // cols) * c, c, c))
            big = pygame.transform.scale(cell, (c * z, c * z))
            y0 = head + pad + (g - 1) * (c * z + pad)
            pygame.draw.rect(img, (20, 19, 26), (x0, y0, c * z, c * z))
            img.blit(big, (x0, y0))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print("contact sheet:", out)


def main():
    args = sys.argv[1:]
    only = []
    if "--only" in args:
        only = [a for a in args[args.index("--only") + 1:] if not a.startswith("--")]
    code = blends(only)
    if code:
        return code
    code = launcher.run_blender(HERE / "scene.py", "weapons_b", [])
    if code:
        return code
    problems = qc.report(ICONS / "weapons_b.json") if hasattr(qc, "report") else 0
    contact_sheet(ROOT / "art" / "preview" / "weapons_b.png")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
