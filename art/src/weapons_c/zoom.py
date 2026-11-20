"""Dev aid (venv python): icons of the weapons_c atlas at 5x, side by side, for look rounds.

    python art/src/weapons_c/zoom.py kich_1,kich_2 [out.png]     (default art/render/weapons_c/zoom.png)
"""
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
ATLAS = ROOT / "client/assets/v2/icons/weapons_c"


def main(argv):
    ids = argv[0].split(",")
    out = Path(argv[1]) if len(argv) > 1 else ROOT / "art/render/weapons_c/zoom.png"
    pygame.init()
    d = json.loads(ATLAS.with_suffix(".json").read_text("utf-8"))
    s = pygame.image.load(str(ATLAS.with_suffix(".png")))
    z, c = 5, d["cell"]
    img = pygame.Surface((len(ids) * (c * z + 4), c * z))
    img.fill((8, 8, 12))
    for k, i in enumerate(ids):
        n = d["icons"][i]["index"]
        cell = s.subsurface(((n % d["cols"]) * c, (n // d["cols"]) * c, c, c))
        img.blit(pygame.transform.scale(cell, (c * z, c * z)), (k * (c * z + 4), 0))
    out.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(img, str(out))
    print(out)


if __name__ == "__main__":
    main(sys.argv[1:])
