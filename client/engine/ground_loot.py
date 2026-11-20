"""Gear lying on the ground where a monster died, glowing in the colour of its phẩm.

The server has already put the piece in the bag when its `loot` message arrives (docs/PROTOCOL.md,
"Trang bị rơi trong loot"); this is the picture of finding it. A piece with a place (`x`, `y`):

    pop    it hops out of the dying monster in a small arc onto (x, y)
    lie    its 32 px icon bobs on the ground: `roi_vong_<rarity>` (a ring, on the ground) under
           it, `roi_cot_<rarity>` (a column of light with glints) over it; its name in the rarity
           colour shows when the player is near
    pick   the player walks within PICK_PX (or TIMEOUT seconds pass): it flies into the player,
           `roi_nhat` flashes, and only then the "you got X" toast shows - once

Leaving the zone collects everything at once (the toasts still show). A piece with no place keeps
the old behaviour: its toast at once (the caller does that when `add` returns False).

Draw order (art/src/fx_tien_ich/README.md): rings with the ground layer, icons with the bodies
(y-sorted drawables), columns after the bodies. The `dia` ring and column are `alpha` sheets, the
others `add`: art2.draw_fx blends each sheet as it says.
"""
from __future__ import annotations

import math

from . import art2

RARITIES = ("pham", "linh", "huyen", "dia", "thien")
POP = 0.45            # seconds of the hop out of the monster
WAIT = 0.25           # it pops a beat after the blow, while the monster falls
FLY = 0.28            # seconds of the flight into the player
PICK_PX = 10.0        # world px: walking this close picks it up
NEAR_PX = 44.0        # world px: its name shows this close
TIMEOUT = 45.0        # it comes to the player by itself after this long
MAX_LYING = 24        # the oldest goes to the bag first beyond this many


class Drop:
    __slots__ = ("item", "name", "rarity", "color", "x", "y", "x0", "y0", "t0", "toast", "state", "t_pick",
                 "toasted", "entry")

    def __init__(self, entry: dict, x: float, y: float, t0: float, toast):
        self.item = str(entry.get("item") or entry.get("item_id") or "")
        self.name = str(entry.get("name_vi") or "")
        r = entry.get("rarity")
        self.rarity = r if r in RARITIES else "pham"
        self.color = str(entry.get("color") or "#C9C4B8")
        self.x, self.y = float(x), float(y)
        self.x0, self.y0 = self.x - 5.0, self.y - 2.0      # out of the monster's body
        self.t0 = t0
        self.toast = toast                                  # (text, colour) shown on pickup
        self.state = "pop"
        self.t_pick = 0.0
        self.toasted = False
        self.entry = entry


class GroundLoot:
    def __init__(self):
        self.drops: list[Drop] = []

    def add(self, entry: dict, now: float, toast) -> bool:
        """A piece of a `loot` message. False when it has no place: the caller toasts it now."""
        x, y = entry.get("x"), entry.get("y")
        if x is None or y is None:
            return False
        try:
            d = Drop(entry, float(x), float(y), now + WAIT, toast)
        except (TypeError, ValueError):
            return False
        self.drops.append(d)
        while sum(1 for o in self.drops if o.state != "pick") > MAX_LYING:
            old = next(o for o in self.drops if o.state != "pick")
            old.state, old.t_pick = "pick", now
        return True

    def update(self, now: float, px: float, py: float, show, vfx=None) -> None:
        """Advance every piece; `show(text, colour)` is called once per piece when it is picked up."""
        keep = []
        for d in self.drops:
            if d.state == "pop" and now >= d.t0 + POP:
                d.state = "lie"
            if d.state == "lie" and (math.hypot(px - d.x, py - d.y) <= PICK_PX or now - d.t0 > TIMEOUT):
                d.state, d.t_pick = "pick", now
            if d.state == "pick" and now - d.t_pick >= FLY:
                self._give(d, show)
                if vfx is not None:
                    vfx.spawn("roi_nhat", px, py, lift=12)
                continue
            keep.append(d)
        self.drops = keep

    def collect_all(self, show) -> None:
        """Leaving the zone: everything goes to the bag at once (its toasts still show)."""
        for d in self.drops:
            self._give(d, show)
        self.drops = []

    @staticmethod
    def _give(d: Drop, show) -> None:
        if not d.toasted:
            d.toasted = True
            if d.toast and show is not None:
                show(*d.toast)

    # ------------------------------------------------------------ where and what
    def where(self, d: Drop, now: float, px: float, py: float) -> tuple[float, float, float]:
        """(x, y, lift) of a piece now (world px)."""
        if d.state == "pop" or now < d.t0:
            k = max(0.0, min(1.0, (now - d.t0) / POP))
            return d.x0 + (d.x - d.x0) * k, d.y0 + (d.y - d.y0) * k, 10 * (1 - k) + math.sin(k * math.pi) * 14
        if d.state == "pick":
            k = max(0.0, min(1.0, (now - d.t_pick) / FLY)) ** 2
            return d.x + (px - d.x) * k, d.y + (py - d.y) * k, 2 + 10 * k
        return d.x, d.y, 2 + math.sin(now * 3 + d.x * 0.1) * 1.5

    def near(self, px: float, py: float) -> list[Drop]:
        return [d for d in self.drops if d.state == "lie" and math.hypot(px - d.x, py - d.y) <= NEAR_PX]

    @staticmethod
    def icon(d: Drop):
        return art2.weapon_icon(d.item) or art2.item_icon({**d.entry, "item_id": d.item})

    def draw_ground(self, surf, view, t: float, now: float) -> None:
        """The rings, under the bodies."""
        for d in self.drops:
            if d.state == "lie":
                sx, sy = view.to_screen(d.x, d.y)
                art2.draw_fx(surf, f"roi_vong_{d.rarity}", t, sx, sy + 2, scale=0.75)

    def drawables(self, view, now: float, px: float, py: float) -> list:
        """The icons, y-sorted with the bodies: (foot y, image, screen position)."""
        out = []
        for d in self.drops:
            if now < d.t0:
                continue
            img = self.icon(d)
            if img is None:
                continue
            x, y, lift = self.where(d, now, px, py)
            sx, sy = view.to_screen(x, y - lift)
            out.append((y + (8 if d.state == "pick" else 0), img,
                        (int(sx - img.get_width() / 2), int(sy - img.get_height() + 4))))
        return out

    def draw_over(self, surf, view, t: float, now: float) -> None:
        """The columns of light, after the bodies."""
        for d in self.drops:
            if d.state == "lie":
                sx, sy = view.to_screen(d.x, d.y)
                art2.draw_fx(surf, f"roi_cot_{d.rarity}", t + d.x * 0.01, sx, sy + 2, scale=0.8)
