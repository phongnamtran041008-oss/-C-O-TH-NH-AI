"""The arrow of Chỉ Đường: a gold arrow drawn pixel by pixel (no art file) with a one-pixel dark
outline and a soft shadow, so it reads on grass, stone, water and dark ground. It circles the
player in the direction of the next leg of the way and nudges forward and back."""
from __future__ import annotations

import math

import pygame

STEPS = 32                     # directions drawn (one every 11.25 degrees)
SIZE = 25                      # the square each arrow is drawn in
FILL = (242, 193, 78)
LIGHT = (255, 232, 150)
EDGE = (43, 29, 14)
SHADOW = (0, 0, 0, 90)
STRAIGHT_FILL = (140, 184, 218)      # no way on foot: a straight arrow, in the colour of the gates
STRAIGHT_LIGHT = (214, 236, 250)
# pointing right, around (0, 0): a head and a short shaft
SHAPE = [(9, 0), (1, -6), (1, -2.4), (-8, -2.4), (-8, 2.4), (1, 2.4), (1, 6)]
SHINE = [(7, 0), (2, -4), (2, -1), (-7, -1), (-7, 0)]

_CACHE: dict = {}


def _rot(pts, a: float):
    c, s = math.cos(a), math.sin(a)
    return [(SIZE / 2 + x * c - y * s, SIZE / 2 + x * s + y * c) for x, y in pts]


def _silhouette(src: pygame.Surface, colour) -> pygame.Surface:
    m = pygame.mask.from_surface(src)
    return m.to_surface(setcolor=colour, unsetcolor=(0, 0, 0, 0))


def sprite(step: int, straight: bool = False) -> pygame.Surface:
    key = (step % STEPS, straight)
    s = _CACHE.get(key)
    if s is None:
        a = (step % STEPS) * 2 * math.pi / STEPS
        body = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        pygame.draw.polygon(body, STRAIGHT_FILL if straight else FILL, _rot(SHAPE, a))
        pygame.draw.polygon(body, STRAIGHT_LIGHT if straight else LIGHT, _rot(SHINE, a))
        s = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
        s.blit(_silhouette(body, SHADOW), (1, 2))
        edge = _silhouette(body, EDGE)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
            s.blit(edge, (dx, dy))
        s.blit(body, (0, 0))
        _CACHE[key] = s
    return s


def step_of(angle: float) -> int:
    return int(round(angle / (2 * math.pi) * STEPS)) % STEPS


def place(cx: float, cy: float, angle: float, z: float, t: float) -> tuple[float, float]:
    """Where the arrow sits: on an oval round the player's body (cx, cy), in its direction,
    nudged along it."""
    rx, ry = 16 * z, 13 * z
    bob = math.sin(t * 5.0) * 1.5
    return cx + math.cos(angle) * (rx + bob), cy + math.sin(angle) * (ry + bob)


def draw(surf: pygame.Surface, cx: float, cy: float, angle: float, z: float, t: float,
         straight: bool = False) -> tuple[int, int]:
    """Blit the arrow for a player whose body centre is at screen (cx, cy); returns its centre."""
    x, y = place(cx, cy, angle, z, t)
    img = sprite(step_of(angle), straight)
    surf.blit(img, (int(x - SIZE / 2), int(y - SIZE / 2)))
    return int(x), int(y)
