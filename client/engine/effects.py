"""Small world-space effects: particles, floating text, the screen flash and shake.

Floating texts have a style (damage numbers that scale and ease): "hit" (a plain number),
"crit" (bigger, it punches in), "kill" (the number that killed: the biggest, red-gold), "parry"
(Phản Đòn: the loudest of all), "dodge", "combo", "miss" (small, grey, sinking) and "dim" (a blow
on a shield). A text without a style draws exactly as before."""
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


# style -> (font size, pop: how much bigger it starts, rise in px, life in s, outline)
STYLES = {
    "hit": (7, 0.6, 16, 1.0, False),
    "dim": (7, 0.0, 10, 0.9, False),
    "crit": (9, 1.1, 20, 1.2, True),
    "kill": (10, 1.3, 24, 1.4, True),
    "parry": (11, 1.4, 22, 1.6, True),
    "dodge": (8, 0.8, 16, 1.1, True),
    "combo": (8, 0.7, 16, 1.3, True),
    "miss": (7, 0.0, -6, 1.4, False),
}
KILL_COLOR = "#FF9A5C"


@dataclass
class FloatText:
    text: str
    x: float
    y: float
    color: str
    age: float = 0.0
    life: float = 1.6
    style: str | None = None


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

    def float_text(self, text: str, x: float, y: float, color: str = "#E9C46A", style: str | None = None) -> None:
        # a text that would land on a fresh one at the same spot goes above it instead of on it
        for _ in range(4 if self.stack_texts else 0):
            if not any(t.age < 0.6 and abs(t.x - x) < 30 and abs(t.y - y) < 5 for t in self.texts):
                break
            y -= 5
        st = STYLES.get(style or "")
        self.texts.append(FloatText(text, x, y, color, life=st[3] if st else 1.6, style=style if st else None))

    def restyle(self, x: float, style: str, within: float = 0.5) -> bool:
        """The newest number near x becomes `style` (the hit that turned out to kill)."""
        for t in reversed(self.texts):
            if t.age <= within and abs(t.x - x) < 10 and t.style in ("hit", "crit") and t.text.isdigit():
                st = STYLES[style]
                t.style, t.color, t.age, t.life = style, KILL_COLOR, 0.0, st[3]
                return True
        return False

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
            if ft.style:
                self._styled(surf, ft, ft.x - cx, ft.y - cy, 1, text_render)
                continue
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
            x, y = view.to_screen(ft.x, ft.y)
            if ft.style:
                self._styled(surf, ft, x, y, z, text_render)
                continue
            img = text_render(ft.text, ft.color)
            surf.blit(img, (int(x - img.get_width() / 2), int(y - ft.age * 14 * z)))
        if self.flash > 0:
            fl = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
            fl.fill((255, 255, 255, int(200 * min(1, self.flash))))
            surf.blit(fl, (0, 0))

    @staticmethod
    def _styled(surf: pygame.Surface, ft: FloatText, x: float, y: float, z: float, text_render) -> None:
        """A styled number: it punches in big and settles, rises with an ease, fades at the end;
        the loud ones get a dark outline so they read over any effect."""
        size, pop, rise, life, outline = STYLES[ft.style]
        try:
            img = text_render(ft.text, ft.color, size)
            dark = text_render(ft.text, "#1A1410", size) if outline else None
        except TypeError:                       # a caller whose renderer takes no size
            img = text_render(ft.text, ft.color)
            dark = None
        a = ft.age
        k = 1 + pop * max(0.0, 1 - a / 0.14) ** 2
        if k > 1.01:
            w, h = max(1, int(img.get_width() * k)), max(1, int(img.get_height() * k))
            img = pygame.transform.scale(img, (w, h))
            dark = pygame.transform.scale(dark, (w, h)) if dark is not None else None
        e = min(1.0, a / 0.7)
        up = rise * (1 - (1 - e) ** 3) * z
        fade = min(1.0, (life - a) / 0.35) if life > 0 else 1.0
        px, py = int(x - img.get_width() / 2), int(y - up - img.get_height() / 2)
        if fade < 1.0:
            img = img.copy()
            img.set_alpha(max(0, int(255 * fade)))
            if dark is not None:
                dark = dark.copy()
                dark.set_alpha(max(0, int(255 * fade)))
        if dark is not None:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                surf.blit(dark, (px + dx, py + dy))
        surf.blit(img, (px, py))
