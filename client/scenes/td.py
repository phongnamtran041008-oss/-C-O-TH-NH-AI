"""Drawing helpers of the tower-defence board (Thủ Thành Toán, scenes/math_td.py), shared with
the books that show its monsters and tower numbers (scenes/rpg.py, scenes/library.py): the
Mặc Quái sprites, the stars, a reward line and a tower's numbers."""
from __future__ import annotations

import math

import pygame

from .. import strings_vi as T
from ..art.palette import rgb
from ..engine import art2, sprites

SPRITE_OF = {"muc_con": ("ink_slime", None, 1.0), "muc_phi": ("ink_slime", (90, 150, 210), 0.8),
             "muc_dac": ("ink_slime", (40, 30, 60), 1.3), "muc_an": ("tone_wisp", None, 1.0),
             "thach_mac": ("ink_fox", (120, 120, 120), 1.1), "mac_vuong": ("ink_fox", (110, 20, 30), 1.8)}


def role_color(role: str):
    return rgb(T.TD_ROLE_COLORS.get(role, "#7D7468"))


_MON: dict = {}


def monster_frames(kind: str) -> list[pygame.Surface]:
    """Mặc Quái of the tower defence: the world's ink monsters, tinted and resized by kind."""
    if kind in _MON:
        return _MON[kind]
    v2, scale = art2.td_monster(kind)
    if v2 is not None:      # a creature rendered out of Blender, walking, shrunk to the 24 px cells
        clip = v2.clips.get("walk") or v2.clips.get("idle")
        frames = []
        for n in clip.frames.get("right") or clip.frames.get("down"):
            f = v2.frame(n)                 # whole frames: the feet stay put
            frames.append(pygame.transform.scale(f, (max(1, int(f.get_width() * scale)),
                                                     max(1, int(f.get_height() * scale)))))
        _MON[kind] = frames
        return frames
    base, tint, k = SPRITE_OF.get(kind, ("ink_slime", None, 1.0))
    frames = []
    for f in sprites.monster(base):
        s = f.copy()
        if tint:
            px = pygame.PixelArray(s)
            w, h = s.get_size()
            for yy in range(h):
                for xx in range(w):
                    c = s.unmap_rgb(px[xx, yy])
                    if c.a and c.r + c.g + c.b < 240:     # tint the ink, keep eyes and highlights
                        px[xx, yy] = (min(255, c.r // 2 + tint[0] // 2), min(255, c.g // 2 + tint[1] // 2),
                                      min(255, c.b // 2 + tint[2] // 2), c.a)
            del px
        if k != 1.0:
            s = pygame.transform.scale(s, (int(s.get_width() * k), int(s.get_height() * k)))
        frames.append(s)
    _MON[kind] = frames
    return frames


def draw_star(ui, cx: float, cy: float, r: float, on: bool) -> None:
    """A five-pointed star (the fonts have no star glyph)."""
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(ui.d.to_window(cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    pygame.draw.polygon(ui.win, rgb("#E9C46A" if on else "#E3D5BA"), pts)
    pygame.draw.polygon(ui.win, rgb("#8B5A2B" if on else "#B8AE9C"), pts, max(1, ui.s // 2))


def draw_stars(ui, cx: float, cy: float, n: int, r: float = 3.5, gap: float = 8) -> None:
    for i in range(3):
        draw_star(ui, cx + (i - 1) * gap, cy, r, i < n)


def reward_text(r: dict) -> str:
    parts = []
    if r.get("spirit_stones"):
        parts.append(f"{r['spirit_stones']} Linh Thạch")
    if r.get("immortal_jade"):
        parts.append(f"{r['immortal_jade']} Tiên Ngọc")
    for it in r.get("items") or []:
        if isinstance(it, dict):
            parts.append(f"{it.get('qty', 1)} {it.get('name_vi', it.get('item'))}")
    if isinstance(r.get("items"), dict):
        parts.extend(f"{n} {k}" for k, n in r["items"].items())
    return ", ".join(parts) or "—"


def stats_text(role: str, st: dict, power: float, level: int = 1, mult: list | None = None) -> str:
    """A tower's numbers at this power and level; "" for a role without numbers."""
    k = power * ((mult or [1.0])[level - 1] if mult else 1.0)
    if role == "moc":
        return T.TD_STATS_MOC.format(hp=int(st["hp"] * k), t=round(st["thorns"] * k, 1))
    if role == "sinh_khi":
        return T.TD_STATS_QI.format(q=round(st["qi"] * k, 1), cd=st["cd"])
    if role == "ho_tro":
        return T.TD_STATS_SUPPORT.format(h=int(st["haste"] * k * 100), hl=round(st["heal"] * k, 1))
    if "dmg" not in st:
        return ""
    return T.TD_STATS_DMG.format(d=round(st["dmg"] * k, 1), r=st["range"], cd=st["cd"])
