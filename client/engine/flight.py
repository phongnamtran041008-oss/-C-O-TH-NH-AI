"""Ngự kiếm on the client: how high a flyer is drawn over its ground point, moment by moment.

The server decides who flies and where (server/app/realtime/abilities.py, the geometry shared in
engine/glide.py); this module is presentation only. A `Flyer` keeps one character's altitude in
world pixels: a take-off is a short crouch then an eased rise with a touch of overshoot to the
rung's cruising height, cruising bobs gently, a landing eases down, and a fall (the gauge ran dry
over water: the server carried the flyer back) sputters and drops. The shadow stays on the
ground and shrinks and fades as the flyer climbs: it is what sells the height.

Pure functions and a small class, so the curves can be tested without a window:

    takeoff_alt(k, lift)    altitude at k in 0..1 of a take-off (a crouch below 0 first)
    landing_alt(k, a0)      altitude at k of a landing from a0
    fall_alt(k, a0)         altitude at k of the sputtering fall back to the ground
    hop_alt(k)              Đạp Kiếm Lướt's tap: one leap over the gap
    shadow(alt)             (scale, alpha) of the ground shadow under a flyer that high
    wake(speed, top)        how long the sword's wake is (0 hovering still, 1 at full speed)
    Flyer                   one character: start(kind, now), alt(now), track(x, y, now) ...
"""
from __future__ import annotations

import math

HOLD_S = 0.22        # G held this long takes off; a quicker tap is the hop over a gap
CROUCH_S = 0.12      # the crouch before the sword lifts
LAND_S = 0.34        # an eased descent
FALL_S = 0.62        # the sputter and drop when the gauge runs dry over water
HOP_LIFT = 13.0      # world px at the top of the hop's arc
CROUCH_PX = 2.0      # how far the body sinks in the crouch
BOB_PX = 1.4         # cruising: the gentle up and down
BOB_HZ = 0.85
SHADOW_FAR = 36.0    # world px of height at which the shadow is smallest and faintest
WAKE_MIN = 8.0       # px/s under which a flyer counts as hovering still (no wake)


def _clamp(k: float) -> float:
    return 0.0 if k < 0 else 1.0 if k > 1 else k


def ease_out_back(u: float, s: float = 1.3) -> float:
    """0 -> 1 with a small overshoot near the end (the sword settles at its height)."""
    u = _clamp(u) - 1.0
    return 1.0 + (s + 1.0) * u * u * u + s * u * u


def takeoff_alt(k: float, lift: float, crouch: float = CROUCH_S / (CROUCH_S + 0.36)) -> float:
    """A take-off at k (0..1 of its time): the body sinks CROUCH_PX for the first `crouch` of it,
    then rises to `lift`, overshooting a little."""
    k = _clamp(k)
    if k < crouch:
        return -CROUCH_PX * math.sin(math.pi * k / crouch)
    return lift * ease_out_back((k - crouch) / (1.0 - crouch))


def landing_alt(k: float, a0: float) -> float:
    """A landing at k from height a0: eased in and out, down to the ground."""
    k = _clamp(k)
    return a0 * (1.0 - (3 * k * k - 2 * k * k * k))


def fall_alt(k: float, a0: float) -> float:
    """The fall back to the ground: a moment of sputtering (the sword wobbles), then a drop."""
    k = _clamp(k)
    wobble = math.sin(k * 38.0) * 2.0 * (1.0 - k)
    return max(0.0, a0 * (1.0 - k * k) + wobble * (1.0 - k))


def hop_alt(k: float, peak: float = HOP_LIFT) -> float:
    """Đạp Kiếm Lướt's tap: one leap, up and down over the gap."""
    return peak * math.sin(math.pi * _clamp(k))


def shadow(alt: float) -> tuple[float, float]:
    """(scale, alpha) of the shadow under a flyer `alt` world px up: full and dark on the ground,
    smaller and fainter the higher it flies."""
    h = _clamp(max(0.0, alt) / SHADOW_FAR)
    return 1.0 - 0.38 * h, 1.0 - 0.3 * h


def wake(speed: float, top: float) -> float:
    """How long the wake behind the sword is: nothing hovering still, longer the faster it goes."""
    if speed < WAKE_MIN or top <= 0:
        return 0.0
    return _clamp(0.35 + 0.75 * speed / top)


# where the tail of the flying sword is, screen px from the feet, per facing (phi_kiem_* fly frames:
# facing right the blade runs from x -25 to +36, tip forward; facing up it points away, tail low)
TAIL = {"right": (-22, -3), "left": (22, -3), "up": (0, 5), "down": (0, -10)}
SHADOW_BASE = 0.62          # phi_bong (64 px) under a character standing on the ground
WIND_FROM = 0.55            # the wind streaks show above this share of the wake
DARK_GROUND = ("ink", "stone", "realm_floor")   # ground tiles where the shadow gets the sword's light too
DARK_GROUND_IDS = ("muc", "da")                  # (the same, as tools/shot_vfx.py names its grounds)


def _travel(vx: float, vy: float, facing: str) -> tuple[float, float]:
    sp = math.hypot(vx, vy)
    if sp > 1e-6:
        return vx / sp, vy / sp
    return {"right": (1.0, 0.0), "left": (-1.0, 0.0), "up": (0.0, -1.0), "down": (0.0, 1.0)}.get(facing, (1.0, 0.0))


def _aim(ux: float, uy: float) -> tuple[float, bool]:
    """(angle, flip) that points a sheet drawn for travel to the right along (ux, uy): flipped for
    the left half, so a ribbon is never drawn upside down."""
    a = math.degrees(math.atan2(uy, ux))
    if ux < -0.01:
        return a - 180.0 if a > 0 else a + 180.0, True
    return a, False


def compose(view, realm: str | None, x: float, y: float, facing: str, t: float, weapon: str | None,
            sword: str, alt: float, vx: float = 0.0, vy: float = 0.0, top: float = 0.0, aura_t: float = 0.0,
            sheet=None, lean: bool = True, dark: bool = False) -> tuple[list, list]:
    """A character on its flying sword `alt` world px over the ground point (x, y): (the shadow's
    blits, to lie on the ground under every body; the body's blits in draw order - wind behind,
    mist, the wake from the sword's tail, the sword, the body). `dark`: the ground is ink or stone,
    where a shadow alone does not read. Each blit is (image, screen
    position, flags). Moving at (vx, vy) px/s against a top speed `top` sets the wake and wind."""
    from . import art2
    from . import vfx as V
    z = view.zoom
    sc, sa = shadow(alt)
    # the sheet is a soft 30-45 % shadow: laid twice it still reads on water, stone and dark ground
    shadows = V.attached("phi_bong", t, view, x, y, scale=SHADOW_BASE * sc, alpha=sa) * 2
    if dark and alt > 2:          # over ink or stone a shadow is lost: the sword's light on the ground shows the spot
        shadows += V.attached("phi_cat_canh", t, view, x, y, scale=0.34 * sc, alpha=0.35 * sa, hold=4)
    speed = math.hypot(vx, vy)
    k = wake(speed, top)
    ux, uy = _travel(vx, vy, facing)
    ang, flip = _aim(ux, uy)
    body: list = []
    if k > WIND_FROM:                             # wind streaks behind the body at speed
        body += V.attached("phi_gio", t, view, x - ux * 7, y - uy * 4, lift=alt + 13, angle=ang, flip=flip,
                           alpha=min(1.0, (k - WIND_FROM) / (1 - WIND_FROM)) * 0.85)
    body += V.attached("phi_may", t, view, x, y, lift=alt - 2, flip=flip, alpha=0.5 + 0.4 * k, scale=0.8)
    if k > 0:                                     # the wake, from the tail of the sword
        tx, ty = TAIL.get(facing, (0, 0))
        span = 0.45 + 0.75 * k
        span *= 0.45 + 0.55 * abs(ux)             # seen from above, a wake up or down the screen is foreshortened
        # a sword of its own colour may have its own wake (phi_vet_2 for phi_kiem_2...), else the cyan one
        wid = V.pick([("phi_vet_" + sword.rsplit("_", 1)[-1], 1), ("phi_vet", 1)])[0]
        body += V.attached(wid, t, view, x + tx / z, y + ty / z, lift=alt, size=(96 * span, 96),
                           angle=ang, flip=flip, shade=0.25, alpha=0.6 + 0.4 * k)
    sx, sy = view.to_screen(x, y - alt)
    ss = art2.weapon(sword)
    if ss is not None and ss.has("fly"):
        ox, oy = ss.offset()
        body.append((ss.frame(ss.index("fly", t, facing)), (sx + ox, sy + oy), 0))
    shift = int(round(max(-1.0, min(1.0, vx / top)) * 2)) if (lean and top > 0) else 0
    for img, (ox, oy), flags in art2.char_layers(realm, "fly", t, facing, weapon, aura_t=aura_t, sheet=sheet) or ():
        body.append((img, (sx + ox + shift, sy + oy), flags))
    return shadows, body


class Flyer:
    """The altitude of one character over its ground point. `kind` is None on the ground, 'up' in
    a take-off, 'cruise' in the air, 'down' landing, 'fall' falling back."""

    __slots__ = ("kind", "lift", "t0", "dur", "a0", "vx", "vy", "_lx", "_ly", "_lt", "_fx", "level")

    def __init__(self):
        self.kind: str | None = None
        self.level = 0
        self.lift = 0.0
        self.t0 = self.dur = self.a0 = 0.0
        self.vx = self.vy = 0.0
        self._lx = self._ly = None
        self._lt = 0.0
        self._fx = True              # the touch-down effect of the last landing was played

    # ------------------------------------------------------------ changes
    def take_off(self, now: float, level: int, lift: float, rise: float) -> None:
        if self.kind in ("up", "cruise") and self.level == level:
            return
        a = self.alt(now)
        self.kind, self.level, self.lift = "up", level, float(lift)
        self.t0, self.dur, self.a0 = now, CROUCH_S + max(0.25, rise), a

    def hover(self, now: float, level: int, lift: float) -> None:
        """Already in the air (a flyer first seen up there): no take-off to play."""
        self.kind, self.level, self.lift = "cruise", level, float(lift)
        self.t0, self.dur, self.a0 = now, 0.0, float(lift)

    def land(self, now: float, fall: bool = False) -> None:
        if self.kind in (None, "down", "fall") and not (fall and self.kind == "down"):
            return
        a = max(0.0, self.alt(now))
        self.kind, self.level = ("fall" if fall else "down"), 0
        self.t0, self.dur, self.a0 = now, FALL_S if fall else LAND_S, a
        self._fx = False

    def ground(self) -> None:
        self.kind, self.level, self.lift, self._fx = None, 0, 0.0, True

    # ------------------------------------------------------------ where it is
    def k(self, now: float) -> float:
        return _clamp((now - self.t0) / self.dur) if self.dur > 0 else 1.0

    def alt(self, now: float) -> float:
        """World px above the ground point now (below 0 only in the crouch)."""
        kind = self.kind
        if kind is None:
            return 0.0
        k = self.k(now)
        if kind == "up":
            if k >= 1.0:
                self.kind = "cruise"
                return self.lift + self.bob(now)
            crouch = CROUCH_S / self.dur if self.dur > 0 else 0.0
            return self.a0 + (takeoff_alt(k, self.lift - self.a0, crouch) if self.a0 <= 0.5 else
                              (self.lift - self.a0) * ease_out_back(k))
        if kind == "cruise":
            return self.lift + self.bob(now)
        if kind == "down":
            if k >= 1.0:
                return 0.0
            return landing_alt(k, self.a0)
        if k >= 1.0:
            return 0.0
        return fall_alt(k, self.a0)

    def bob(self, now: float) -> float:
        return BOB_PX * math.sin(now * 2 * math.pi * BOB_HZ)

    @property
    def flying(self) -> bool:
        return self.kind in ("up", "cruise")

    def shown(self, now: float) -> bool:
        """Drawn on its sword (in the air, or still coming down)."""
        if self.kind in ("down", "fall"):
            return self.k(now) < 1.0
        return self.kind is not None

    def touched_down(self, now: float) -> bool:
        """True once, when a landing or a fall reaches the ground (time for the dust)."""
        if self._fx or self.kind not in ("down", "fall") or self.k(now) < 1.0:
            return False
        self._fx = True
        self.kind = None
        return True

    # ------------------------------------------------------------ how it moves
    def track(self, x: float, y: float, now: float) -> None:
        """Follow the ground point: a smoothed velocity for the wake, the wind and the lean."""
        if self._lx is None or now <= self._lt:
            if self._lx is None:
                self._lx, self._ly, self._lt = x, y, now
            return
        dt = now - self._lt
        if dt > 0.5:                                  # a gap (a new zone, a jump): start again
            self.vx = self.vy = 0.0
        else:
            a = min(1.0, dt * 12.0)
            self.vx += ((x - self._lx) / dt - self.vx) * a
            self.vy += ((y - self._ly) / dt - self.vy) * a
        self._lx, self._ly, self._lt = x, y, now

    @property
    def speed(self) -> float:
        return math.hypot(self.vx, self.vy)
