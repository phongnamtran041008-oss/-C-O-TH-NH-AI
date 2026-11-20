"""The combat VFX engine: timed instances of the Blender-rendered FX sheets (client/assets/v2/fx/)
layered, scaled, turned, faded, moved and trailed, plus the camera's shake, the hit-stop and a
screen tint. Nothing here draws a picture by hand: every image is a frame of a sheet (or a frame
of a character / monster sheet, for afterimages and dissolves).

Public API (one `Vfx` per scene; the world scene keeps it in `self.vfx`):

    v = Vfx(reduced=False, web=False)
    v.spawn(fid, x, y, **opts)          -> Inst | None   a sheet instance at a world point
    v.sprite(img, pivot, x, y, **opts)  -> Inst | None   any surface (afterimage, dissolve)
    v.update(dt)                        advance the clock, run cues and emitters, retire the dead
    v.draw(surf, view, layer)           draw one layer ("ground" under the bodies, "over" above)
    v.shake(amount)                     add camera trauma (0..1); v.offset() -> (dx, dy) screen px
    v.hitstop(seconds)                  freeze the world picture a few frames (crits, kills, parries)
    v.tint(rgb, peak, life)             a full-screen wash; v.draw_tint(surf) draws it
    v.at(delay, fn)                     run fn() after `delay` seconds of the VFX clock (an impact)
    v.emit(tag, period, fn, life)       call fn() every `period` seconds for `life` seconds
    v.kill(tag)                         remove every instance / emitter carrying that tag
    v.clear()                           remove everything (a new zone)
    v.resolve = fn(key) -> (x, y)|None  where a followed thing is now (instances with follow=key)

    pick([(fid, scale), ...])            -> (fid, scale) | (None, 0)  the first sheet that exists:
                                         the fallback chain that lets new sheets light up untouched
    attached(fid, t, view, x, y, ...)    -> [(img, pos, flags)]  one frame stuck to a moving body,
                                         returned to be depth-sorted with it (ngự kiếm's wake)

spawn options (all optional): delay (s), life (s; default the sheet's one-shot length), lift
(world px above the point), to=(x, y) + lift1 + ease ("lin" | "out" | "in" | "inout") + arc
(world px of hump) for travel, scale (or scale=(a, b) grown over the life), size=(w, h) screen
px (stretch), angle (screen degrees the art's +x points to: 0 right, 90 down), fade_in /
fade_out (s), peak (0..1 brightness), fps (speed factor), frames=(a, b) (loop that range), hold
(one frame), shade (0..1: a dark plate under an additive sheet, so it keeps its colour on bright
grass), flip (mirror left-right about the pivot: a swing facing left), start (skip the first frames of a one-shot: the ring of a burst without its disc), trail=(n, gap) (afterimages n x `gap` seconds behind), layer, tag, follow, heavy
(dropped by "reduce effects" and first to go over the budget).

Coordinates are world pixels; the view (engine/view.py) puts them on screen. Positions, damage,
ranges and timing of the game never come from here: this is presentation only, and the
hit-stop only stops the picture (the VFX clock and the world frame), never input, the network or
a question card (they are other scenes, drawn and updated as before).

Budget: at most MAX_LIVE instances (MAX_LIVE_WEB in the browser build) and CACHE_MAX cached
transformed surfaces (scaled + turned + faded, rotation snapped to 15 degrees, sizes to 2 px,
fades to 16 levels), so a long fight never grows memory or per-frame work without bound.
"""
from __future__ import annotations

import math
from collections import OrderedDict

import pygame

from . import art2

MAX_LIVE = 120
MAX_LIVE_WEB = 56
CACHE_MAX = 700
CACHE_MAX_WEB = 300
HITSTOP_MAX = 0.11          # never longer than this, whatever asks for it
HITSTOP_GAP = 0.18          # and not again sooner than this after the last one ended
SHAKE_PX = 7.0              # screen pixels at full trauma
SHAKE_DECAY = 1.9           # trauma lost per second
ANGLE_STEP = 15

_cache: OrderedDict = OrderedDict()
_cache_max = CACHE_MAX


def pick(chain) -> tuple[str | None, float]:
    """The first (fid, scale) of `chain` whose sheet is on disk, else (None, 0.0)."""
    for fid, scale in chain:
        if fid and art2.fx(fid) is not None:
            return fid, float(scale)
    return None, 0.0


def has(fid: str | None) -> bool:
    return bool(fid) and art2.fx(fid) is not None


def cache_size() -> int:
    return len(_cache)


def clear_cache() -> None:
    _cache.clear()


def _xform(img: pygame.Surface, w: int, h: int, angle: int, level: int, additive: bool,
           flip: bool = False) -> pygame.Surface:
    """`img` scaled to (w, h), turned `angle` degrees (pygame: counter-clockwise) and faded to
    level/16 (additive art fades its colour, alpha art its alpha). Cached, bounded."""
    key = (img, w, h, angle, level, additive, flip)
    s = _cache.get(key)
    if s is not None:
        _cache.move_to_end(key)
        return s
    s = img if img.get_size() == (w, h) else pygame.transform.scale(img, (w, h))
    if flip:
        s = pygame.transform.flip(s, True, False)
    if angle:
        s = pygame.transform.rotate(s, angle)
    if level < 16:
        s = s.copy()
        k = level * 16
        s.fill((k, k, k, k) if additive else (255, 255, 255, k), special_flags=pygame.BLEND_RGBA_MULT)
    _cache[key] = s
    while len(_cache) > _cache_max:
        _cache.popitem(last=False)
    return s


def _premul(img: pygame.Surface) -> pygame.Surface:
    key = ("premul", img)
    s = _cache.get(key)
    if s is None:
        s = img.premul_alpha() if hasattr(img, "premul_alpha") else img
        _cache[key] = s
    return s


def _shadow(img: pygame.Surface, alpha: int) -> pygame.Surface:
    """The drawn area of `img` in black at `alpha` (0..255), cached."""
    a = max(0, min(255, alpha)) // 8 * 8
    key = ("shadow", img, a)
    s = _cache.get(key)
    if s is None:
        s = img.copy()
        s.fill((0, 0, 0, a), special_flags=pygame.BLEND_RGBA_MULT)
        _cache[key] = s
        while len(_cache) > _cache_max:
            _cache.popitem(last=False)
    return s


def attached(fid: str | None, t: float, view, x: float, y: float, lift: float = 0.0, scale: float = 1.0,
             size=None, angle: float = 0.0, alpha: float = 1.0, flip: bool = False, hold=None,
             shade: float = 0.0) -> list:
    """One frame of sheet `fid` stuck to something that moves every frame and is drawn in among
    the bodies (ngự kiếm's shadow, wake, wind and mist, engine/flight.py): the same scaling,
    turning, fading and bounded cache as an instance, but returned as blits to sort with the
    bodies - [(image, (screen x, screen y), flags)], empty when the sheet is missing. `lift` is
    in world px, `size` in screen px, `angle` in screen degrees (0 right, 90 down)."""
    s = art2.fx(fid)
    if s is None:
        return []
    n = max(0, min(s.total - 1, int(hold))) if hold is not None else s.fx_index(t)
    img, (px, py), fw, fh, additive = s.frame(n), s.pivot, s.fw, s.fh, s.additive
    w, h = (size[0] * scale, size[1] * scale) if size is not None else (fw * scale, fh * scale)
    w, h = max(2, int(w) // 2 * 2), max(2, int(h) // 2 * 2)
    level = min(16, int(round(max(0.0, alpha) * 16)))
    if level <= 0:
        return []
    a = int(round(-angle / ANGLE_STEP) * ANGLE_STEP) % 360
    out = _xform(img, w, h, a, level, additive, flip)
    kx, ky = w / fw, h / fh
    px, py = (fw - px if flip else px) * kx, py * ky
    if a:
        r = math.radians(-a)
        dx, dy = px - w / 2, py - h / 2
        px = out.get_width() / 2 + dx * math.cos(r) - dy * math.sin(r)
        py = out.get_height() / 2 + dx * math.sin(r) + dy * math.cos(r)
    sx, sy = view.to_screen(x, y - lift)
    pos = (int(sx - px), int(sy - py))
    blits = []
    if shade > 0 and additive:        # a dark plate first, so the light keeps its colour on bright grass
        blits.append((_shadow(out, int(shade * level * 16)), pos, 0))
    blits.append((out, pos, s.flags))
    return blits


def _ease(k: float, kind: str) -> float:
    k = max(0.0, min(1.0, k))
    if kind == "out":
        return 1 - (1 - k) ** 3
    if kind == "in":
        return k * k * k
    if kind == "inout":
        return 3 * k * k - 2 * k * k * k
    return k


class Inst:
    __slots__ = ("fid", "img", "pivot", "flags", "x", "y", "lift", "to", "lift1", "ease", "arc", "t0", "life",
                 "scale", "size", "angle", "fade_in", "fade_out", "peak", "fps", "frames", "hold", "trail",
                 "layer", "tag", "follow", "heavy", "ox", "oy", "start", "flip", "shade")

    def __init__(self):
        self.fid = None
        self.img = None
        self.pivot = (0, 0)
        self.flags = 0
        self.to = None
        self.lift = self.lift1 = 0.0
        self.ease, self.arc = "lin", 0.0
        self.scale = (1.0, 1.0)
        self.size = None
        self.angle = 0.0
        self.fade_in, self.fade_out, self.peak = 0.0, 0.0, 1.0
        self.fps, self.frames, self.hold, self.trail, self.start = 1.0, None, None, None, 0
        self.layer, self.tag, self.follow, self.heavy = "over", None, None, False
        self.ox = self.oy = 0.0           # offset from a followed thing
        self.flip = False                 # mirrored left-right about its pivot (a swing facing left)
        self.shade = 0.0                  # a dark plate under an additive sheet (bright ground)

    # where it is `t` seconds into its life (world px; z = lift)
    def pos(self, t: float, resolve) -> tuple[float, float, float]:
        x, y = self.x, self.y
        if self.follow is not None and resolve is not None:
            p = resolve(self.follow)
            if p is not None:
                x, y = p[0] + self.ox, p[1] + self.oy
        if self.to is None:
            return x, y, self.lift
        k = _ease(t / self.life if self.life > 0 else 1.0, self.ease)
        hump = math.sin(k * math.pi) * self.arc
        return x + (self.to[0] - x) * k, y + (self.to[1] - y) * k, self.lift + (self.lift1 - self.lift) * k + hump

    def alpha(self, t: float) -> float:
        a = self.peak
        if self.fade_in > 0:
            a *= max(0.0, min(1.0, t / self.fade_in))
        if self.fade_out > 0:
            a *= max(0.0, min(1.0, (self.life - t) / self.fade_out))
        return a


class Vfx:
    def __init__(self, reduced: bool = False, web: bool = False):
        global _cache_max
        self.reduced = reduced
        self.web = web
        self.cap = MAX_LIVE_WEB if web else MAX_LIVE
        _cache_max = CACHE_MAX_WEB if web else CACHE_MAX
        self.t = 0.0                   # the VFX clock (stops during a hit-stop)
        self.wall = 0.0                # real time seen by update()
        self.live: list[Inst] = []
        self.cues: list[tuple[float, object]] = []
        self.emitters: dict = {}
        self.trauma = 0.0
        self.stop_left = 0.0           # hit-stop seconds left
        self.stop_ready = 0.0          # wall time before which no new hit-stop starts
        self.freeze_pending = False    # the world should keep its next picture for the hit-stop
        self.tints: list[list] = []    # [r, g, b, peak, t0, life]
        self.resolve = None

    # ------------------------------------------------------------ making things
    def _admit(self, heavy: bool) -> bool:
        if heavy and self.reduced:
            return False
        if len(self.live) < self.cap:
            return True
        if heavy:
            return False
        for i, it in enumerate(self.live):       # make room: the oldest heavy one goes first
            if it.heavy:
                del self.live[i]
                return True
        del self.live[0]
        return True

    def _fill(self, it: Inst, x: float, y: float, delay: float, life: float | None, kw: dict) -> Inst:
        it.x, it.y = float(x), float(y)
        it.t0 = self.t + max(0.0, float(delay))
        it.lift = float(kw.get("lift", 0.0))
        to = kw.get("to")
        if to is not None:
            it.to = (float(to[0]), float(to[1]))
            it.lift1 = float(kw.get("lift1", it.lift))
            it.ease = kw.get("ease", "lin")
            it.arc = float(kw.get("arc", 0.0))
        sc = kw.get("scale", 1.0)
        it.scale = (float(sc[0]), float(sc[1])) if isinstance(sc, (tuple, list)) else (float(sc), float(sc))
        it.size = kw.get("size")
        it.angle = float(kw.get("angle", 0.0))
        it.fade_in = float(kw.get("fade_in", 0.0))
        it.fade_out = float(kw.get("fade_out", 0.0))
        it.peak = max(0.0, min(1.0, float(kw.get("peak", 1.0))))
        it.fps = float(kw.get("fps", 1.0)) or 1.0
        it.frames = kw.get("frames")
        it.hold = kw.get("hold")
        it.start = int(kw.get("start", 0))
        it.flip = bool(kw.get("flip", False))
        it.shade = float(kw.get("shade", 0.0))
        it.trail = kw.get("trail") if not self.reduced else None
        it.layer = kw.get("layer", "over")
        it.tag = kw.get("tag")
        it.follow = kw.get("follow")
        it.heavy = bool(kw.get("heavy", False))
        if it.follow is not None and self.resolve is not None:
            p = self.resolve(it.follow)
            if p is not None:
                it.ox, it.oy = it.x - p[0], it.y - p[1]
        it.life = float(life) if life is not None else 0.5
        return it

    def spawn(self, fid: str | None, x: float, y: float, delay: float = 0.0, life: float | None = None,
              **kw) -> Inst | None:
        """A sheet at a world point. None when the sheet is missing, or the budget / the
        "reduce effects" switch says no."""
        s = art2.fx(fid)
        if s is None or not self._admit(bool(kw.get("heavy"))):
            return None
        it = Inst()
        it.fid = fid
        if life is None:
            fps = float(kw.get("fps", 1.0)) or 1.0
            one_shot = not (s.loop or kw.get("frames") or kw.get("hold") is not None)
            frames_left = max(1, s.total - int(kw.get("start", 0)))
            life = frames_left / s.fps / fps if one_shot else 0.6
        self._fill(it, x, y, delay, life, kw)
        self.live.append(it)
        return it

    def sprite(self, img: pygame.Surface | None, pivot, x: float, y: float, delay: float = 0.0,
               life: float = 0.4, additive: bool = False, **kw) -> Inst | None:
        """Any surface (a character's frame for an afterimage, a monster's for its dissolve)."""
        if img is None or not self._admit(bool(kw.get("heavy"))):
            return None
        it = Inst()
        if additive:        # an additive blit ignores alpha: the see-through pixels must be black
            img = _premul(img)
        it.img, it.pivot = img, (float(pivot[0]), float(pivot[1]))
        it.flags = pygame.BLEND_RGBA_ADD if additive else 0
        self._fill(it, x, y, delay, life, kw)
        self.live.append(it)
        return it

    def at(self, delay: float, fn) -> None:
        self.cues.append((self.t + max(0.0, delay), fn))

    def emit(self, tag, period: float, fn, life: float) -> None:
        self.emitters[tag] = [self.t, period, fn, self.t + life]

    def kill(self, tag) -> None:
        self.live = [it for it in self.live if it.tag != tag]
        self.emitters.pop(tag, None)

    def clear(self) -> None:
        """Everything gone (a new zone)."""
        self.live.clear()
        self.cues.clear()
        self.emitters.clear()
        self.tints.clear()
        self.trauma = self.stop_left = 0.0
        self.freeze_pending = False

    def shake(self, amount: float) -> None:
        if not self.reduced:
            self.trauma = min(1.0, self.trauma + max(0.0, amount))

    def hitstop(self, seconds: float) -> None:
        """Hold the world's picture `seconds` (capped): a few frames of weight on a crit, a kill
        or a parry. Input, the network and the cards carry on - only the picture waits."""
        if self.reduced or seconds <= 0 or self.stop_left > 0 or self.wall < self.stop_ready:
            return
        self.stop_left = min(HITSTOP_MAX, seconds)
        self.freeze_pending = True

    @property
    def frozen(self) -> bool:
        return self.stop_left > 0

    def tint(self, rgb, peak: float = 0.25, life: float = 0.25, delay: float = 0.0) -> None:
        peak = peak * (0.5 if self.reduced else 1.0)
        self.tints.append([int(rgb[0]), int(rgb[1]), int(rgb[2]), max(0.0, min(0.8, peak)),
                           self.t + delay, max(0.02, life)])
        if len(self.tints) > 6:
            del self.tints[0]

    # ------------------------------------------------------------ time
    def update(self, dt: float) -> None:
        dt = max(0.0, min(0.25, dt))
        self.wall += dt
        if self.stop_left > 0:
            self.stop_left -= dt
            if self.stop_left <= 0:
                self.stop_left = 0.0
                self.freeze_pending = False
                self.stop_ready = self.wall + HITSTOP_GAP
            self.trauma = max(0.0, self.trauma - SHAKE_DECAY * dt)
            return
        self.t += dt
        self.trauma = max(0.0, self.trauma - SHAKE_DECAY * dt)
        if self.cues:
            due = [c for c in self.cues if c[0] <= self.t]
            if due:
                self.cues = [c for c in self.cues if c[0] > self.t]
                for _, fn in due:
                    fn()
        for tag, em in list(self.emitters.items()):
            if self.t > em[3]:
                del self.emitters[tag]
                continue
            if self.t >= em[0]:
                em[0] = self.t + em[1]
                em[2]()
        self.live = [it for it in self.live if self.t - it.t0 <= it.life]
        self.tints = [tn for tn in self.tints if self.t - tn[4] <= tn[5]]

    def offset(self) -> tuple[int, int]:
        """The camera shake now, in screen pixels (0, 0 with "reduce effects")."""
        if self.reduced or self.trauma <= 0:
            return 0, 0
        amp = SHAKE_PX * self.trauma * self.trauma
        w = self.wall
        return (int(round(amp * (math.sin(w * 53.0) * 0.6 + math.sin(w * 31.0 + 1.7) * 0.4))),
                int(round(amp * (math.sin(w * 47.0 + 0.6) * 0.6 + math.sin(w * 29.0 + 2.9) * 0.4))))

    # ------------------------------------------------------------ drawing
    def _frame(self, it: Inst, s, t: float) -> int:
        if it.hold is not None:
            return max(0, min(s.total - 1, int(it.hold)))
        if it.frames is not None:
            a, b = int(it.frames[0]), int(it.frames[1])
            n = b - a + 1
            return a + int(t * s.fps * it.fps) % max(1, n)
        return min(s.total - 1, s.fx_index(t * it.fps) + it.start)

    def _blit(self, surf, view, it: Inst, t: float, level_mul: float = 1.0, back: float = 0.0) -> int:
        tt = t - back
        if tt < 0:
            return 0
        if it.img is not None:
            img, (px, py), flags, fw, fh, additive = it.img, it.pivot, it.flags, it.img.get_width(), \
                it.img.get_height(), it.flags != 0
        else:
            s = art2.fx(it.fid)
            if s is None:
                return 0
            img, (px, py), flags, fw, fh, additive = s.frame(self._frame(it, s, tt)), s.pivot, s.flags, s.fw, s.fh, \
                s.additive
        k = _ease(t / it.life if it.life > 0 else 1.0, "out")
        sc = it.scale[0] + (it.scale[1] - it.scale[0]) * k
        if it.size is not None:
            w, h = it.size[0] * sc, it.size[1] * sc
        else:
            w, h = fw * sc, fh * sc
        w, h = max(2, int(w) // 2 * 2), max(2, int(h) // 2 * 2)
        level = int(round(it.alpha(t) * level_mul * 16))
        if level <= 0:
            return 0
        level = min(16, level)
        a = int(round(-it.angle / ANGLE_STEP) * ANGLE_STEP) % 360
        out = _xform(img, w, h, a, level, additive, it.flip)
        kx, ky = w / fw, h / fh
        px, py = (fw - px if it.flip else px) * kx, py * ky
        if a:
            r = math.radians(-a)
            dx, dy = px - w / 2, py - h / 2
            px = out.get_width() / 2 + dx * math.cos(r) - dy * math.sin(r)
            py = out.get_height() / 2 + dx * math.sin(r) + dy * math.cos(r)
        x, y, z = it.pos(tt, self.resolve)
        sx, sy = view.to_screen(x, y - z)
        if it.shade > 0 and additive:     # on bright grass additive light washes to white: a dark plate first
            surf.blit(_shadow(out, int(it.shade * level * 16)), (int(sx - px), int(sy - py)))
        surf.blit(out, (int(sx - px), int(sy - py)), special_flags=flags)
        return 1

    def draw(self, surf: pygame.Surface, view, layer: str = "over") -> int:
        """Draw one layer; returns how many images were blitted (tests count them)."""
        n = 0
        for it in self.live:
            if it.layer != layer:
                continue
            t = self.t - it.t0
            if t < 0 or t > it.life:
                continue
            if it.trail:
                count, gap = it.trail
                for i in range(int(count), 0, -1):
                    n += self._blit(surf, view, it, t, level_mul=0.55 * (1 - i / (count + 1)), back=i * gap)
            n += self._blit(surf, view, it, t)
        return n

    def draw_tint(self, surf: pygame.Surface) -> None:
        if not self.tints:
            return
        r = g = b = 0.0
        a = 0.0
        for tn in self.tints:
            t = self.t - tn[4]
            if t < 0:
                continue
            k = t / tn[5]
            w = tn[3] * (min(1.0, k * 6) if k < 0.16 else (1 - k) / 0.84)
            if w <= 0:
                continue
            r, g, b = r + tn[0] * w, g + tn[1] * w, b + tn[2] * w
            a += w
        if a <= 0.004:
            return
        col = (int(r / a), int(g / a), int(b / a))
        layer = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        layer.fill((*col, int(255 * min(0.8, a))))
        surf.blit(layer, (0, 0))
