"""A Linh Thú trotting after its owner (stage 8): it keeps a few steps behind, turns to face
where it goes and stops when the owner stops. Purely visual; nothing here is sent.

The same companion may be one of the 12 con giáp (wiring "pets") or a linh thú of Thiên Địa Đồ
tamed in its land (wiring "spirit_beasts", world_plan.json `beasts`): both are drawn from their
own v2 sheet. A beast whose gift is a mount (Tiểu Long) is also what a rider sits on
(Cưỡi linh thú): `mount_drawables` draws it larger under the rider, who sits cross-legged."""
from __future__ import annotations

import math

from . import art2

MOUNT_SCALE = 2.0          # a ridden beast grows to carry its rider
MOUNT_LIFT = 22            # screen px: how high the rider sits above the ground (2x world)
RIDER_CLIP = "meditate"    # the cross-legged pose of the v2 body: sitting on the mount


class PetFollower:
    def __init__(self, x: float, y: float, kind: str = ""):
        self.kind = kind
        self.x, self.y = x - 12, y
        self.left = False
        self.moving = False
        self.walk_t = 0.0

    def update(self, dt: float, ox: float, oy: float, owner_facing: str = "down") -> None:
        back = {"up": (0, 10), "down": (-10, -4), "left": (12, 0), "right": (-12, 0)}.get(owner_facing, (-12, 0))
        tx, ty = ox + back[0], oy + back[1]
        dx, dy = tx - self.x, ty - self.y
        d = math.hypot(dx, dy)
        if d > 120:                          # left far behind (a portal, a respawn): jump there
            self.x, self.y = tx, ty
            d = 0
        self.moving = d > 3
        if self.moving:
            speed = min(d * 6, 140) * dt
            self.x += dx / d * speed
            self.y += dy / d * speed
            if abs(dx) > 1:
                self.left = dx < 0
            self.walk_t += dt
        else:
            self.walk_t = 0.0

    @property
    def frame(self) -> int:
        return int(self.walk_t * 8) % 2 if self.moving else 0


# ------------------------------------------------------------------ the v2 sheets of a companion
def is_spirit_beast(kind: str | None) -> bool:
    return bool(kind) and art2.on() and kind in (art2.wiring().get("spirit_beasts") or {})


def sheet(kind: str | None):
    """The v2 sheet of a companion: a con giáp (wiring pets) or a linh thú (wiring spirit_beasts)."""
    if not (kind and art2.on()):
        return None
    s = art2.beast_for(kind)
    if s is None:
        sid = (art2.wiring().get("spirit_beasts") or {}).get(kind)
        s = art2.beast(sid) if isinstance(sid, str) else None
    return s


def drawable(kind: str | None, x: float, y: float, moving: bool, walk_t: float, t: float, left: bool, view):
    """A companion following its owner, or None when its kind has no v2 sheet."""
    b = sheet(kind)
    if b is None:
        return None
    n = b.index("walk" if moving else "idle", walk_t if moving else t, "left" if left else "right")
    sx, sy = view.to_screen(x, y)
    return (y, b.frame(n), (int(sx - b.pivot[0]), int(sy - b.pivot[1])))


def picture(kind: str | None, t: float = 0.0, clip: str = "idle", facing: str = "down"):
    """A companion for a menu: the frame cut to its pixels, or None."""
    b = sheet(kind)
    if b is None:
        return None
    return art2.trim(b.frame(b.index(clip if b.has(clip) else "idle", t, facing)))


def mount_drawable(kind: str | None, x: float, y: float, facing: str, moving: bool, walk_t: float, t: float, view):
    """(y, image, position) of a ridden beast at the rider's feet, larger than when it follows."""
    b = sheet(kind)
    if b is None:
        return None
    n = b.index("walk" if moving else "idle", walk_t if moving else t, facing)
    w, h = int(b.fw * MOUNT_SCALE), int(b.fh * MOUNT_SCALE)
    img = art2.scaled(b.frame(n), w, h)
    sx, sy = view.to_screen(x, y)
    return (y, img, (int(sx - b.pivot[0] * MOUNT_SCALE), int(sy - b.pivot[1] * MOUNT_SCALE)))
