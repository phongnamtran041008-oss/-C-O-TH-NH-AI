"""Rebuild the WEAPONS_C batch: models -> .blend -> kit icon render/pack -> QC -> contact sheet.

    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_c/build.py                 # 48 models + atlas
    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_c/build.py --only kich_3,roi_5
    "/e/TU TIÊN AI/.venv/Scripts/python.exe" art/src/weapons_c/build.py --layers --jobs 3
        # then the 48 in-hand layers through art/src/weapon_layers (and the layer previews)

(`--only` rebuilds those .blends and an atlas holding only those icons; run without it for the
full atlas. With `--layers`, `--only` limits the layers too.)
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools" / "blender"))

from kit import launcher, qc, palette  # noqa: E402

BATCH = "weapons_c"
ATLAS = ROOT / "client/assets/v2/icons/weapons_c"
TYPES = ["kich", "roi", "am_khi", "luan", "phu", "cam"]
ALL_IDS = [f"{t}_{g}" for t in TYPES for g in range(1, 9)]
SCALE = 3


def contact_sheet(out: Path, ref: bool = True):
    """Types in columns, grades in rows (like the reference), 3x nearest, dark background."""
    import os
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.init()
    doc = json.loads(ATLAS.with_suffix(".json").read_text(encoding="utf-8"))
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


def take(args, name, flag=False):
    if name not in args:
        return False if flag else None
    i = args.index(name)
    if flag:
        del args[i]
        return True
    v = args[i + 1]
    del args[i:i + 2]
    return v


def main(argv):
    argv = list(argv)
    layers = take(argv, "--layers", flag=True)
    jobs = take(argv, "--jobs") or "3"
    only = take(argv, "--only")
    code = launcher.run_blender(HERE / "scene.py", BATCH, ["--only", only] if only else [])
    if code:
        return code
    colors = palette.load().color_set
    problems = qc.check_file(ATLAS.with_suffix(".json"), colors)
    for p in problems:
        print(" -", p)
    print("qc weapons_c:", "FAIL" if problems else "OK", f"({len(problems)} problem(s))")
    if not only:
        contact_sheet(ROOT / "art/preview/weapons_c.png")
    if problems:
        return 1
    if layers:
        ids = only or ",".join(ALL_IDS)
        cmd = [sys.executable, str(ROOT / "art/src/weapon_layers/build.py"), "--only", ids, "--jobs", jobs]
        code = subprocess.call(cmd, cwd=str(ROOT))
        if code == 0 and not only:
            code = subprocess.call([sys.executable, str(HERE / "preview_layers.py")], cwd=str(ROOT))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
