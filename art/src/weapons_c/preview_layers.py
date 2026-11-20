"""Contact sheets of the WEAPONS_C in-hand layers, drawn over the character sheets the way the
game draws them (art/src/weapon_layers/composite.py), 3x:

    art/preview/weapon_layers_c.png      each type (grade 1 and 5) on Luyen Khi: idle down, idle right,
                                         walk right, the whole attack clip facing right, the strike
                                         facing down / left / up, cast or back-carry frame, die
    art/preview/weapon_layers_c_all.png  all 48 on their realm's character, strike frame, facing right
    art/preview/weapon_layers_c_dai_thua.png  the six grade-8 weapons on Dai Thua, attack clip, right

    python art/src/weapons_c/preview_layers.py [--dir art/render/weapon_layers/dev] [--grades 1,5] [--types kich,roi]
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "weapon_layers"))
import composite as C  # noqa: E402
import pygame  # noqa: E402

ROOT = C.ROOT
PREVIEW = ROOT / "art" / "preview"
ATTACK = {"kich": "slash", "roi": "slash", "am_khi": "shoot", "luan": "shoot", "phu": "slash", "cam": "cast"}
TYPES = ("kich", "roi", "am_khi", "luan", "phu", "cam")
COLS = 15


def char_id(realm: int) -> str:
    return "dao_si_" + C.REALMS[realm]


def label(img, text, pos, color=(225, 225, 235)):
    f = pygame.font.SysFont("arial", 12)
    img.blit(f.render(text, True, color), pos)


def row_for(w: str, realm: int, wdir: Path) -> list:
    t = w.rsplit("_", 1)[0]
    a = ATTACK[t]
    ch = char_id(realm)
    n = C.load(C.CHARS, ch).count(a)
    hit = C.load(C.CHARS, ch).doc["events"][a]["hit"]

    def cell(clip, d, k):
        return C.compose(w, ch, clip, d, k, wdir)
    other = "slash" if a != "slash" else "cast"
    have = C.load(wdir, w).doc["clips"]
    row = [cell("idle", "down", 0), cell("idle", "right", 0), cell("walk", "right", 2)]
    row += [cell(a, "right", k) for k in range(n)]
    row += [cell(a, "down", hit), cell(a, "left", hit), cell(a, "up", hit)]
    row += [cell(other, "right", hit) if other in have else None,
            cell("meditate", "down", 0) if "meditate" in have else None,
            cell("die", "right", "last") if "die" in have else None]
    return row


def write(path: Path, rows, title):
    cells, labels = [], []
    for w, r, wdir in rows:
        row = row_for(w, r, wdir)
        cells += row + [None] * (COLS - len(row))
        labels.append(f"{w}  {C.REALM_NAME[r]}")
    img = C.sheet_of_cells(cells, COLS, scale=3, title=title)
    step = 96 * 3 + 2
    for k, text in enumerate(labels):
        label(img, text, (6, 16 + k * step + 4))
    pygame.image.save(img, str(path))
    print(path, img.get_size())


def write_all(path: Path, wdir: Path):
    cells = []
    for t in TYPES:
        for g in range(1, 9):
            w = f"{t}_{g}"
            a = ATTACK[t]
            hit = C.load(C.CHARS, char_id(g - 1)).doc["events"][a]["hit"]
            cells.append(C.compose(w, char_id(g - 1), a, "right", hit, wdir))
    img = C.sheet_of_cells(cells, 8, scale=3, title="all 48 ky binh layers on their realm's character: strike frame, "
                           "facing right (rows: kich roi am_khi luan phu cam; columns: grade 1-8 = Luyen Khi .. Dai Thua)")
    pygame.image.save(img, str(path))
    print(path, img.get_size())


TITLE = ("ky binh layers over characters (3x): idle down | idle right | walk right | attack clip frames 0-5 facing right "
         "(strike = 3) | strike down, left, up | other attack clip | meditate (back carry) | die")


def main(argv):
    wdir = C.WEAPONS
    if "--dir" in argv:
        wdir = ROOT / argv[argv.index("--dir") + 1]
    grades = [1, 5]
    if "--grades" in argv:
        grades = [int(x) for x in argv[argv.index("--grades") + 1].split(",")]
    types = TYPES
    if "--types" in argv:
        types = argv[argv.index("--types") + 1].split(",")
    out = PREVIEW / "weapon_layers_c.png"
    if "--out" in argv:
        out = ROOT / argv[argv.index("--out") + 1]
    PREVIEW.mkdir(parents=True, exist_ok=True)
    rows = [(f"{t}_{g}", 0, wdir) for t in types for g in grades]
    write(out, rows, TITLE)
    if wdir == C.WEAPONS and "--out" not in argv:
        write(PREVIEW / "weapon_layers_c_dai_thua.png", [(f"{t}_8", 7, wdir) for t in TYPES],
              TITLE.replace("over characters", "grade 8 on Dai Thua"))
        write_all(PREVIEW / "weapon_layers_c_all.png", wdir)


if __name__ == "__main__":
    main(sys.argv[1:])
