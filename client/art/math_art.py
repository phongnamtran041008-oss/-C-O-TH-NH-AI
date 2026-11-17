"""Art for the quái lỗi sai of Loạn Số Cốc (M7), drawn with code like the rest of client/art.

Three shapes, one per floor of Đại Số Tuyến Tính, each tinted per monster so two mistakes of
the same floor are still told apart at a glance:

  * ``tap_hop``  - a brace that closes around nothing: a set that miscounts itself;
  * ``so_phuc``  - two halves orbiting, one real and one imaginary;
  * ``ma_tran``  - a small grid whose rows and columns argue about which comes first.

The colours live here, next to the pixels, the way every other creature's look does; the
server's data/math/monsters.json carries the same ``shape`` and ``look`` so the two can be
checked against each other (tools/check_all.py does that).
"""
from __future__ import annotations

import math

import pygame

SIZE = (20, 22)

# kind -> (shape, body, mark, eye). The same values as data/math/monsters.json "look".
MONSTERS: dict[str, tuple[str, str, str, str]] = {
    "dstt_phan_tu_ma": ("tap_hop", "#3C5A74", "#D8E6F0", "#F4EBD9"),
    "dstt_nghich_hieu_ma": ("tap_hop", "#4A3C74", "#E6D8F0", "#F4EBD9"),
    "dstt_anh_trung_ma": ("tap_hop", "#2F6B5E", "#D8F0E6", "#F4EBD9"),
    "dstt_phan_ao_ma": ("so_phuc", "#6B2F4A", "#F0D8E0", "#F4EBD9"),
    "dstt_binh_phuong_ma": ("so_phuc", "#74502F", "#F0E6D8", "#F4EBD9"),
    "dstt_modun_ma": ("so_phuc", "#2F4A74", "#D8E0F0", "#F4EBD9"),
    "dstt_chi_so_ma": ("ma_tran", "#50746B", "#E0F0EA", "#F4EBD9"),
    "dstt_chuyen_vi_ma": ("ma_tran", "#6B4A2F", "#F0E0D8", "#F4EBD9"),
    "dstt_doi_xung_ma": ("ma_tran", "#742F3C", "#F0D8DC", "#F4EBD9"),
}


def _s() -> pygame.Surface:
    return pygame.Surface(SIZE, pygame.SRCALPHA)


def _hex(c: str) -> tuple[int, int, int]:
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def _eyes(s: pygame.Surface, eye: tuple[int, int, int], y: int) -> None:
    for x in (6, 12):
        pygame.draw.rect(s, eye, (x, y, 2, 2))


def tap_hop(frame: int, body, mark, eye) -> pygame.Surface:
    """A pair of braces holding a blob that cannot decide how many it is."""
    s = _s()
    squash = (0, 1)[frame % 2]
    pygame.draw.ellipse(s, body, (4, 6 + squash, 12, 12 - squash))
    pygame.draw.ellipse(s, mark, (4, 6 + squash, 12, 12 - squash), 1)
    for x, flip in ((1, False), (16, True)):          # the braces { }
        pts = [(x + (3 if flip else 0), 4), (x + (0 if flip else 3), 8),
               (x + (0 if flip else 3), 13), (x + (3 if flip else 0), 17)]
        pygame.draw.lines(s, mark, False, pts, 1)
    pygame.draw.rect(s, mark, (9, 3, 2, 2))           # one element floating outside
    _eyes(s, eye, 10 + squash)
    return s


def so_phuc(frame: int, body, mark, eye) -> pygame.Surface:
    """Two halves going round each other: the real part and the one it keeps mislaying."""
    s = _s()
    a = frame * math.pi / 2
    cx, cy = 10, 12
    for r, col in ((5, body), (3, mark)):
        dx, dy = int(round(math.cos(a) * 4)), int(round(math.sin(a) * 2))
        pygame.draw.circle(s, col, (cx + dx, cy + dy), r)
        a += math.pi
    pygame.draw.line(s, mark, (3, 19), (17, 19), 1)   # the real axis
    pygame.draw.line(s, mark, (10, 2), (10, 6), 1)    # and the imaginary one
    _eyes(s, eye, 10)
    return s


def ma_tran(frame: int, body, mark, eye) -> pygame.Surface:
    """A 2x2 grid that shuffles a cell every frame: rows and columns out of order."""
    s = _s()
    pygame.draw.rect(s, body, (3, 4, 14, 14))
    pygame.draw.rect(s, mark, (3, 4, 14, 14), 1)
    for i in range(2):                                 # the brackets of a matrix
        pygame.draw.line(s, mark, (1, 4 + i * 13), (3, 4 + i * 13), 1)
        pygame.draw.line(s, mark, (17, 4 + i * 13), (19, 4 + i * 13), 1)
    pygame.draw.line(s, mark, (1, 4), (1, 17), 1)
    pygame.draw.line(s, mark, (19, 4), (19, 17), 1)
    cells = [(6, 7), (12, 7), (6, 13), (12, 13)]
    for n, (x, y) in enumerate(cells):
        if n == frame % len(cells):                    # the cell that wandered off
            y += 1
        pygame.draw.rect(s, mark, (x - 1, y - 1, 2, 2))
    _eyes(s, eye, 9)
    return s


SHAPES = {"tap_hop": tap_hop, "so_phuc": so_phuc, "ma_tran": ma_tran}


def monster_frames(kind: str) -> list[pygame.Surface]:
    shape, body, mark, eye = MONSTERS[kind]
    fn = SHAPES[shape]
    return [fn(f, _hex(body), _hex(mark), _hex(eye)) for f in range(2)]
