"""The proof: weapon layers drawn over character sheets the way the game draws them.

    art/preview/weapon_layers.png      representative set, full action strip + flying swords
    art/preview/weapon_layers_all.png  all 64 weapons on their realm's character, strike frame, facing right

Run from build.py, or by hand:  python art/src/weapon_layers/preview.py   (venv python, pygame)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import composite as C  # noqa: E402
import pygame  # noqa: E402

ROOT = C.ROOT
PREVIEW = ROOT / "art" / "preview"
ATTACK = {"kiem": "slash", "dao": "slash", "chuy": "slash", "thuong": "slash",
          "truong": "cast", "phien": "cast", "ho_lo": "cast", "cung": "shoot"}
TYPES = ("kiem", "dao", "thuong", "chuy", "truong", "cung", "phien", "ho_lo")
# (weapon, realm index 0..7)
REPRESENTATIVE = [("kiem_1", 0), ("kiem_5", 4), ("dao_3", 2), ("thuong_2", 1), ("chuy_6", 5),
                  ("truong_4", 3), ("cung_7", 6), ("phien_8", 7), ("ho_lo_1", 0)]
FLY = [("phi_kiem_1", 1), ("phi_kiem_2", 2), ("phi_kiem_3", 4)]


def char_id(realm: int) -> str:
    return "dao_si_" + C.REALMS[realm]


def label(img: pygame.Surface, text: str, pos=(3, 2), color=(200, 200, 215)):
    f = pygame.font.SysFont("arial", 10)
    img.blit(f.render(text, True, color), pos)


def cell(w: str, realm: int, clip: str, d: str, k, under: bool = False) -> pygame.Surface:
    return C.compose(w, char_id(realm), clip, d, k, C.WEAPONS, under=under)


def row_for(w: str, realm: int) -> list:
    t = w.rsplit("_", 1)[0]
    a = ATTACK[t]
    n = C.load(C.WEAPONS, w).count(a)
    hit = C.load(C.CHARS, char_id(realm)).doc["events"][a]["hit"]
    return [
        cell(w, realm, "idle", "down", 0),
        cell(w, realm, "walk", "right", 2),
        cell(w, realm, a, "right", max(0, hit - 2)),     # wind-up
        cell(w, realm, a, "right", hit),                 # strike
        cell(w, realm, a, "right", n - 1),               # recovery
        cell(w, realm, a, "down", max(0, hit - 2)),
        cell(w, realm, a, "down", hit),
        cell(w, realm, a, "down", n - 1),
        cell(w, realm, "die", "right", "last"),
    ]


def write_main(path: Path):
    cols = 12
    cells, labels = [], []
    for w, r in REPRESENTATIVE:
        row = row_for(w, r)
        cells += row + [None] * (cols - len(row))
        labels.append(f"{w}  {C.REALM_NAME[r]}")
    row = []
    for w, r in FLY:
        for d in ("down", "right", "left", "up"):
            row.append(cell(w, r, "fly", d, 0, under=True))
    cells += row
    labels.append("phi_kiem 1-3")
    img = C.sheet_of_cells(cells, cols, scale=3, title="weapon layers over characters (3x): idle down | walk right | "
                           "wind-up, strike, recovery right | wind-up, strike, recovery down | die | "
                           "bottom row: flying swords 1-3 (down, right, left, up)", labels=None, label_w=0)
    step = 96 * 3 + 2
    for n, text in enumerate(labels[:len(REPRESENTATIVE)]):
        label(img, text, (2 + 9 * step + 8, 16 + n * step + 120), (230, 230, 240))
    label(img, "phi_kiem 1, 2, 3 under Truc Co, Ket Dan, Hoa Than",
          (2 + 8, 16 + len(REPRESENTATIVE) * step + 2), (230, 230, 240))
    pygame.image.save(img, str(path))
    print(path, img.get_size())


def write_all(path: Path):
    cells = []
    for t in TYPES:
        for g in range(1, 9):
            w = f"{t}_{g}"
            a = ATTACK[t]
            hit = C.load(C.CHARS, char_id(g - 1)).doc["events"][a]["hit"]
            cells.append(cell(w, g - 1, a, "right", hit))
    img = C.sheet_of_cells(cells, 8, scale=3, title="all 64 weapon layers on their realm's character: strike frame, facing right "
                           "(rows: kiem dao thuong chuy truong cung phien ho_lo; columns: grade 1-8 = Luyen Khi .. Dai Thua)")
    pygame.image.save(img, str(path))
    print(path, img.get_size())


def write_all_previews():
    PREVIEW.mkdir(parents=True, exist_ok=True)
    write_main(PREVIEW / "weapon_layers.png")
    write_all(PREVIEW / "weapon_layers_all.png")


if __name__ == "__main__":
    write_all_previews()
