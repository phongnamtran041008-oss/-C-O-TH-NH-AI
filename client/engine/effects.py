"""Small world-space effects: particles, floating text, the screen flash and shake."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

import pygame

from ..art.palette import rgb


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    color: tuple
    size: int = 1
    age: float = 0.0
    gravity: float = 0.0


@dataclass
class FloatText:
    text: str
    x: float
    y: float
    color: str
    age: float = 0.0
    life: float = 1.6


@dataclass
class Effects:
    particles: list = field(default_factory=list)
    texts: list = field(default_factory=list)
    flash: float = 0.0
    shake: float = 0.0
    stack_texts: bool = False   # v2 world: a new floating text never lands on a fresh one

    def burst(self, x: float, y: float, color: str, n: int = 14, speed: float = 40, up: bool = True) -> None:
        r = random.Random()
        for _ in range(n):
            a = r.uniform(0, math.tau)
            sp = r.uniform(speed * 0.4, speed)
            self.particles.append(Particle(x, y, math.cos(a) * sp, math.sin(a) * sp - (20 if up else 0),
                                           r.uniform(0.5, 1.1), rgb(color), r.choice((1, 1, 2)), gravity=30))

    def sparkle(self, x: float, y: float, color: str = "o") -> None:
        r = random.Random()
        self.particles.append(Particle(x + r.uniform(-6, 6), y + r.uniform(-6, 2), 0, -8,
                                       r.uniform(0.4, 0.8), rgb(color), 1))

    def ink_to_light(self, x: float, y: float) -> None:
        """Ink mist dissolving into bright motes (a right answer clears the ink)."""
        self.burst(x, y, "k", 10, 25)
        self.burst(x, y, "o", 14, 35)

    def float_text(self, text: str, x: float, y: float, color: str = "#E9C46A") -> None:
        # a text that would land on a fresh one at the same spot goes above it instead of on it
        for _ in range(4 if self.stack_texts else 0):
            if not any(t.age < 0.6 and abs(t.x - x) < 30 and abs(t.y - y) < 5 for t in self.texts):
                break
            y -= 5
        self.texts.append(FloatText(text, x, y, color))

    def update(self, dt: float) -> None:
        for p in list(self.particles):
            p.age += dt
            if p.age > p.life:
                self.particles.remove(p)
                continue
            p.vy += p.gravity * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
        for t in list(self.texts):
            t.age += dt
            if t.age > t.life:
                self.texts.remove(t)
        self.flash = max(0.0, self.flash - dt * 2.5)
        self.shake = max(0.0, self.shake - dt * 3)

    def draw(self, surf: pygame.Surface, cam: tuple[int, int], text_render, t: float, view=None) -> None:
        """`view` (engine/view.py): a zoomed world - positions go through it, sprites and particles
        grow with the zoom, text stays its size. Without it, the old `world - cam`."""
        if view is not None and view.zoom != 1:
            self._draw_view(surf, view, text_render)
            return
        cx, cy = cam
        for p in self.particles:
            a = 1 - p.age / p.life
            if a > 0.1:
                pygame.draw.rect(surf, p.color, (int(p.x - cx), int(p.y - cy), p.size, p.size))
        for ft in self.texts:
            img = text_render(ft.text, ft.color)
            y = ft.y - cy - ft.age * 14
            surf.blit(img, (int(ft.x - cx - img.get_width() / 2), int(y)))
        if self.flash > 0:
            fl = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            fl.fill((255, 255, 255, int(200 * min(1, self.flash))))
            surf.blit(fl, (0, 0))

    def _draw_view(self, surf: pygame.Surface, view, text_render) -> None:
        z = view.zoom
        for p in self.particles:
            a = 1 - p.age / p.life
            if a > 0.1:
                x, y = view.to_screen(p.x, p.y)
                pygame.draw.rect(surf, p.color, (x, y, p.size * z, p.size * z))
        for ft in self.texts:
            img = text_render(ft.text, ft.color)
            x, y = view.to_screen(ft.x, ft.y)
            surf.blit(img, (int(x - img.get_width() / 2), int(y - ft.age * 14 * z)))
        if self.flash > 0:
            fl = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            fl.fill((255, 255, 255, int(200 * min(1, self.flash))))
            surf.blit(fl, (0, 0))
