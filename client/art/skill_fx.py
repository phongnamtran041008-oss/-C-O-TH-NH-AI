"""Effects of the chiêu thức (M9), drawn with code like the rest of client/art: no image files.

One effect per `fx` id that data/math/skills.json names (tools/check_all.py checks the two
lists against each other):

  * ``chem``      - a slash arc across the target;
  * ``kiem_khi``  - a crescent of sword-qi that flies from the caster to the target;
  * ``hoa_cau``   - a fireball that travels caster -> target and bursts;
  * ``tran_do``   - an array circle on the ground around the target, a mark for each of the
                    five elements turning inside it (the area chiêu);
  * ``ho_tran``   - a protective dome of light around the caster (the ward);
  * ``thien_loi`` - a lightning strike out of a dark cloud.

Every one is a pure function of (fx id, progress 0..1, positions): `draw` paints the picture
for that moment onto a surface and keeps no state, so the world scene only has to remember
when an effect began and a test can look at any moment of it with no window and no clock.
Positions are where the feet are, in the pixels of the surface drawn on (the caller has
already taken the camera off); each effect lifts itself to chest height where it needs to.

A chiêu that misses ("chiêu hụt") has its own picture, `ok=False`, shared by all six: grey
instead of colour, it starts the way the real one would, loses its strength half way and
ends in a few puffs of smoke. It must read as a fizzle at a glance, and never as a hit.
"""
from __future__ import annotations

import math

import pygame

FX_IDS = ("chem", "kiem_khi", "hoa_cau", "tran_do", "ho_tran", "thien_loi")

# seconds each effect lasts; the world scene keeps one for this long after the chiêu lands
DURATION = {"chem": 0.45, "kiem_khi": 0.7, "hoa_cau": 0.9, "tran_do": 1.4, "ho_tran": 1.6, "thien_loi": 0.9}
MISS_DURATION = 0.8
DEFAULT_RADIUS = {"tran_do": 60.0, "ho_tran": 40.0}      # when the event carries no `r`

# the five elements of the array: kim, mộc, thủy, hỏa, thổ
FIVE = ((236, 232, 208), (106, 153, 78), (74, 124, 200), (229, 83, 61), (201, 154, 58))
GREY = (200, 200, 200)
SMOKE = (205, 205, 205)


def duration(fx_id: str, ok: bool = True) -> float:
    return DURATION.get(fx_id, DURATION["chem"]) if ok else MISS_DURATION


def _rgba(c, a: float) -> tuple[int, int, int, int]:
    return int(c[0]), int(c[1]), int(c[2]), max(0, min(255, int(a * 255)))


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _fade(p: float, fade_in: float, fade_out: float) -> float:
    """1 in the middle of the effect, ramping up at the start and down at the end."""
    a = _clamp(p / fade_in) if fade_in > 0 else 1.0
    b = _clamp((1 - p) / fade_out) if fade_out > 0 else 1.0
    return min(a, b)


def _noise(i: int, salt: int = 0) -> float:
    """A repeatable pseudo-random number in -1..1 (so the same moment always looks the same)."""
    return math.sin((i + 1) * 12.9898 + salt * 78.233) * 0.5 + math.sin((i + 1) * 4.1414 + salt) * 0.5


def _glow(layer, c, pos, r: float, a: float) -> None:
    for k, f in ((1.0, 0.18), (0.66, 0.3), (0.36, 0.7)):
        pygame.draw.circle(layer, _rgba(c, a * f), (int(pos[0]), int(pos[1])), max(1, int(r * k)))


def _ellipse(layer, c, centre, rx: float, ry: float, width: int = 1) -> None:
    rect = pygame.Rect(0, 0, max(2, int(rx * 2)), max(2, int(ry * 2)))
    rect.center = (int(centre[0]), int(centre[1]))
    pygame.draw.ellipse(layer, c, rect, width)


def _polyline(layer, c, pts, width: int = 1) -> None:
    if len(pts) >= 2:
        pygame.draw.lines(layer, c, False, [(int(x), int(y)) for x, y in pts], width)


def _ground_point(cx: float, cy: float, rx: float, ry: float, ang: float) -> tuple[float, float]:
    return cx + math.cos(ang) * rx, cy + math.sin(ang) * ry


# ------------------------------------------------------------------ the six effects
def _chem(layer, p, src, dst, radius):
    """A slash: a bright arc swept across the target, a short tail behind its head."""
    cx, cy = dst[0], dst[1] - 12
    sweep = _clamp(p / 0.55)
    a = _fade(p, 0.05, 0.4)
    head = math.radians(-75 + 150 * sweep)
    for i in range(18):                                   # the tail: older = thinner and dimmer
        t = i / 17
        ang = head - math.radians(95) * t
        w = max(2, int(7 * (1 - t)))
        r = 20 - t * 3
        p0 = (cx + math.cos(ang) * r, cy + math.sin(ang) * r * 1.05)
        ang2 = ang - math.radians(8)
        p1 = (cx + math.cos(ang2) * r, cy + math.sin(ang2) * r * 1.05)
        col = (_lerp(255, 233, t), _lerp(250, 196, t), _lerp(235, 106, t))
        _polyline(layer, _rgba(col, a * (1 - t * 0.7)), [p0, p1], w)
    if sweep > 0.85:                                      # a few sparks where it lands
        for i in range(5):
            ang = math.radians(60 + i * 18 + _noise(i) * 8)
            d = 4 + (sweep - 0.85) * 60 + i
            _polyline(layer, _rgba((255, 236, 170), a), [(cx + math.cos(ang) * d, cy + math.sin(ang) * d),
                                                          (cx + math.cos(ang) * (d + 3), cy + math.sin(ang) * (d + 3))])


def _crescent(layer, c, centre, ang: float, r: float, a: float) -> None:
    """A filled crescent whose points trail back along `ang` (the way it flies)."""
    outer, inner = [], []
    for i in range(9):
        t = -1 + i / 4
        th = ang + t * math.radians(80)
        outer.append((centre[0] + math.cos(th) * r, centre[1] + math.sin(th) * r))
        inner.append((centre[0] + math.cos(th) * r * 0.62 - math.cos(ang) * r * 0.45,
                      centre[1] + math.sin(th) * r * 0.62 - math.sin(ang) * r * 0.45))
    pygame.draw.polygon(layer, _rgba(c, a), [(int(x), int(y)) for x, y in outer + inner[::-1]])


def _kiem_khi(layer, p, src, dst, radius):
    """A crescent of sword-qi in flight, then a ring where it bites."""
    a0 = (src[0], src[1] - 14)
    b0 = (dst[0], dst[1] - 12)
    ang = math.atan2(b0[1] - a0[1], b0[0] - a0[0])
    fly = _clamp(p / 0.72)
    if p < 0.72:
        for k in range(4, -1, -1):                        # three ghosts behind it
            t = _clamp(fly - k * 0.07)
            pos = (_lerp(a0[0], b0[0], t), _lerp(a0[1], b0[1], t))
            c = (150, 220, 240) if k else (235, 252, 255)
            _crescent(layer, c, pos, ang, 9 + (0 if k else 1), 0.9 - k * 0.18)
    else:
        t = (p - 0.72) / 0.28
        for k in range(2):
            r = 4 + t * (14 + k * 6)
            pygame.draw.circle(layer, _rgba((200, 240, 255), (1 - t) * (0.9 - k * 0.4)),
                               (int(b0[0]), int(b0[1])), int(r), 1)
        for i in range(6):
            th = ang + math.radians(180 + (i - 2.5) * 26)
            d = 3 + t * 16
            _polyline(layer, _rgba((235, 252, 255), 1 - t),
                      [(b0[0] + math.cos(th) * d, b0[1] + math.sin(th) * d),
                       (b0[0] + math.cos(th) * (d + 4), b0[1] + math.sin(th) * (d + 4))])


def _hoa_cau(layer, p, src, dst, radius):
    """A fireball that flies caster -> target (a little arc over the way), then bursts."""
    a0 = (src[0], src[1] - 14)
    b0 = (dst[0], dst[1] - 10)
    if p < 0.6:
        t = p / 0.6
        x, y = _lerp(a0[0], b0[0], t), _lerp(a0[1], b0[1], t) - math.sin(t * math.pi) * 9
        for i in range(10):                               # the flames it leaves
            tt = max(0.0, t - i * 0.035)
            fx_, fy_ = _lerp(a0[0], b0[0], tt), _lerp(a0[1], b0[1], tt) - math.sin(tt * math.pi) * 9
            fy_ += _noise(i, 1) * 2
            col = (255, _lerp(190, 80, i / 9), _lerp(70, 30, i / 9))
            pygame.draw.circle(layer, _rgba(col, 0.85 - i * 0.07), (int(fx_), int(fy_)), max(1, int(4 - i * 0.3)))
        _glow(layer, (255, 140, 50), (x, y), 8, 1.0)
        pygame.draw.circle(layer, (255, 236, 170, 255), (int(x), int(y)), 2)
    else:
        t = (p - 0.6) / 0.4
        a = 1 - t
        for k, col in enumerate(((200, 50, 40), (240, 110, 40), (255, 200, 70))):
            pygame.draw.circle(layer, _rgba(col, a * 0.95), (int(b0[0]), int(b0[1])),
                               max(1, int((6 + t * 17) * (1 - k * 0.24))))
        for i in range(10):
            th = i / 10 * math.tau + _noise(i) * 0.2
            d0, d1 = 6 + t * 16, 10 + t * 24
            _polyline(layer, _rgba((255, 224, 130), a),
                      [(b0[0] + math.cos(th) * d0, b0[1] + math.sin(th) * d0 * 0.8),
                       (b0[0] + math.cos(th) * d1, b0[1] + math.sin(th) * d1 * 0.8)], 2)


def _tran_do(layer, p, src, dst, radius):
    """An array on the ground: two rings, a pentagram, and one mark for each of the five elements."""
    r = radius or DEFAULT_RADIUS["tran_do"]
    cx, cy = dst[0], dst[1]
    ry = r * 0.5
    a = _fade(p, 0.15, 0.3)
    spin = p * math.pi * 1.2
    pygame.draw.ellipse(layer, _rgba((201, 154, 58), a * 0.18),
                        pygame.Rect(int(cx - r), int(cy - ry), int(r * 2), int(ry * 2)))
    _ellipse(layer, _rgba((233, 196, 106), a), (cx, cy), r, ry, 2)
    _ellipse(layer, _rgba((233, 196, 106), a * 0.8), (cx, cy), r * 0.78, ry * 0.78, 1)
    pts = [_ground_point(cx, cy, r * 0.78, ry * 0.78, spin - math.pi / 2 + i * math.tau / 5) for i in range(5)]
    for i in range(5):                                    # the pentagram
        _polyline(layer, _rgba((255, 236, 170), a * 0.8), [pts[i], pts[(i + 2) % 5]])
    for i, (px, py) in enumerate(pts):
        _glow(layer, FIVE[i], (px, py - 2), 6, a)
        pygame.draw.circle(layer, _rgba(FIVE[i], a), (int(px), int(py - 2)), 3)
        pygame.draw.circle(layer, _rgba((255, 255, 255), a), (int(px), int(py - 2)), 1)
    pulse = _clamp((p - 0.3) / 0.35)                      # the strike of the array: a ring that runs out
    if 0 < pulse < 1:
        _ellipse(layer, _rgba((255, 236, 170), (1 - pulse) * 0.9), (cx, cy), r * (0.2 + pulse * 0.85),
                 ry * (0.2 + pulse * 0.85), 2)
    for i in range(8):                                    # motes of light rising from the marks
        th = i / 8 * math.tau + spin
        mx = cx + math.cos(th) * r * 0.6
        my = cy + math.sin(th) * ry * 0.6 - ((p * 30 + i * 5) % 22)
        pygame.draw.circle(layer, _rgba(FIVE[i % 5], a * 0.8), (int(mx), int(my)), 1)


def _ho_tran(layer, p, src, dst, radius):
    """A dome of light round the caster: a ring on the ground, a half-shell above, the shell shimmering."""
    r = radius or DEFAULT_RADIUS["ho_tran"]
    r = min(r, 46.0)
    cx, cy = src[0], src[1]
    ry = r * 0.45
    h = r * 0.95
    a = _fade(p, 0.2, 0.3)
    pygame.draw.ellipse(layer, _rgba((140, 200, 240), a * 0.16),
                        pygame.Rect(int(cx - r), int(cy - ry), int(r * 2), int(ry * 2)))
    _ellipse(layer, _rgba((200, 235, 255), a), (cx, cy), r, ry, 2)
    shell = [(cx + math.cos(math.pi * (1 - i / 24)) * r, cy - math.sin(math.pi * (1 - i / 24)) * h)
             for i in range(25)]
    _polyline(layer, _rgba((220, 245, 255), a), shell, 2)
    for k in range(3):                                    # meridians of the shell, sliding sideways
        s = (p * 0.7 + k / 3) % 1.0
        _polyline(layer, _rgba((190, 230, 255), a * 0.35), [
            (cx + (s * 2 - 1) * r * math.sin(math.pi * i / 14), cy - h * math.sin(math.pi * i / 14) * 0.98)
            for i in range(15)])
    for i in range(6):                                    # sparks drifting up the shell
        u = (p * 0.9 + i / 6) % 1.0
        ang = math.pi * (0.1 + 0.8 * ((i * 0.37) % 1))
        x = cx + math.cos(ang) * r * 0.95
        y = cy - math.sin(ang) * h * 0.95 * u
        pygame.draw.circle(layer, _rgba((255, 250, 220), a * (1 - u)), (int(x), int(y)), 1)


def _bolt(layer, p, top, foot, seed: int):
    pts = [top]
    n = 7
    for i in range(1, n):
        t = i / n
        pts.append((_lerp(top[0], foot[0], t) + _noise(i, seed) * 9 * (1 - t * 0.4),
                    _lerp(top[1], foot[1], t)))
    pts.append(foot)
    return pts


def _thien_loi(layer, p, src, dst, radius):
    """A dark cloud, a forked bolt that flickers, white where it lands, scorched sparks after."""
    foot = (dst[0], dst[1] - 4)
    top = (dst[0] + 3, dst[1] - 118)
    cloud = _fade(p, 0.15, 0.3)
    for i, (dx, dy, w) in enumerate(((-16, 0, 22), (0, -4, 28), (16, 0, 22), (6, 4, 18))):
        pygame.draw.ellipse(layer, _rgba((60, 54, 84), cloud * 0.9),
                            pygame.Rect(int(top[0] + dx - w / 2), int(top[1] + dy - 7), w, 12))
    if 0.15 <= p < 0.6:
        seed = int(p * 18)
        pts = _bolt(layer, p, top, foot, seed)
        _polyline(layer, _rgba((140, 110, 230), 0.45), pts, 7)
        _polyline(layer, _rgba((190, 220, 255), 0.9), pts, 3)
        _polyline(layer, (255, 255, 255, 255), pts, 1)
        mid = pts[3]                                       # a fork
        fork = [mid, (mid[0] + 10 * (1 if seed % 2 else -1), mid[1] + 10), (mid[0] + 14 * (1 if seed % 2 else -1), mid[1] + 24)]
        _polyline(layer, _rgba((190, 220, 255), 0.8), fork, 1)
    if p >= 0.2:
        t = _clamp((p - 0.2) / 0.6)
        _glow(layer, (200, 210, 255), foot, 8 + 10 * (1 - t), (1 - t) * 0.9 if p < 0.6 else (1 - t))
        for i in range(8):
            th = math.pi + i / 7 * math.pi + _noise(i) * 0.15
            d = 4 + t * 20
            _polyline(layer, _rgba((220, 230, 255), 1 - t),
                      [(foot[0] + math.cos(th) * d, foot[1] + math.sin(th) * d * 0.7),
                       (foot[0] + math.cos(th) * (d + 4), foot[1] + math.sin(th) * (d + 4) * 0.7)])


# ------------------------------------------------------------------ the miss
# how far along the way to the target the real effect would have got when it fizzles
_REACH = {"chem": 0.15, "kiem_khi": 0.5, "hoa_cau": 0.5, "thien_loi": 1.0}
_AREA = ("tran_do", "ho_tran")


def _dashed_ring(layer, c, centre, rx: float, ry: float, phase: float) -> None:
    for i in range(12):
        if i % 2:
            continue
        a0 = (i / 12) * math.tau + phase
        pts = [(centre[0] + math.cos(a0 + k * 0.1) * rx, centre[1] + math.sin(a0 + k * 0.1) * ry) for k in range(4)]
        _polyline(layer, c, pts, 1)


def _fizzle(layer, fx_id, p, src, dst, radius):
    """The same chiêu, but it sputters: grey, it loses strength half way, smoke where it dies."""
    if fx_id in _AREA:
        r = (radius or DEFAULT_RADIUS[fx_id])
        centre = (dst[0], dst[1]) if fx_id == "tran_do" else (src[0], src[1])
        grow = math.sin(_clamp(p / 0.7) * math.pi) * 0.6 + 0.15 * (1 - p)
        a = _fade(p, 0.1, 0.4)
        _dashed_ring(layer, _rgba(GREY, a), centre, r * grow, r * grow * 0.5, p * 3 * (1 if fx_id == "tran_do" else -1))
        end = centre
    else:
        reach = _REACH.get(fx_id, 0.5)
        a0 = (src[0], src[1] - 14)
        b0 = (dst[0], dst[1] - 12 if fx_id != "thien_loi" else dst[1] - 100)
        run = _clamp(p / 0.5)
        end = (_lerp(a0[0], b0[0], reach), _lerp(a0[1], b0[1], reach))
        pos = (_lerp(a0[0], end[0], run), _lerp(a0[1], end[1], run))
        if p < 0.5:
            r = 8 * (1 - run * 0.7)
            flick = 0.5 + 0.5 * math.sin(p * 60)
            if fx_id == "kiem_khi":                        # the crescent thins out and goes out
                ang = math.atan2(b0[1] - a0[1], b0[0] - a0[0])
                for i in range(3, -1, -1):
                    tt = max(0.0, run - i * 0.1)
                    _crescent(layer, GREY, (_lerp(a0[0], end[0], tt), _lerp(a0[1], end[1], tt)), ang,
                              9 * (1 - run * 0.5), 0.85 - i * 0.2)
            elif fx_id == "chem":                          # half a slash, then nothing
                head = math.radians(-75 + 70 * run)
                for i in range(10):
                    ang = head - math.radians(60) * i / 9
                    _polyline(layer, _rgba(GREY, (1 - i / 9) * (1 - run * 0.6)),
                              [(dst[0] + math.cos(ang) * 17, dst[1] - 12 + math.sin(ang) * 17),
                               (dst[0] + math.cos(ang - 0.15) * 17, dst[1] - 12 + math.sin(ang - 0.15) * 17)], 3)
            elif fx_id == "thien_loi":                     # a cloud that only sputters: a stub of bolt, no strike
                for dx, dy, w in ((-12, 0, 20), (2, -3, 24), (14, 1, 18)):
                    pygame.draw.ellipse(layer, _rgba(GREY, 0.8),
                                        pygame.Rect(int(end[0] + dx - w / 2), int(end[1] + dy - 6), w, 11))
                if flick > 0.5:
                    stub = [(end[0], end[1] + 5), (end[0] - 3, end[1] + 11), (end[0] + 2, end[1] + 16)]
                    _polyline(layer, _rgba((235, 235, 235), 0.9), stub, 1)
            else:                                          # hoa_cau: the fireball sputters out
                for i in range(4):
                    tt = max(0.0, run - i * 0.08)
                    pygame.draw.circle(layer, _rgba(GREY, 0.9 - i * 0.18),
                                       (int(_lerp(a0[0], end[0], tt)), int(_lerp(a0[1], end[1], tt))), max(1, int(r - i)))
                _glow(layer, GREY, pos, r + 2, 0.7 * flick + 0.2)
    if p >= 0.45:                                          # smoke, and a droop of sparks
        t = (p - 0.45) / 0.55
        ex, ey = end[0], end[1]
        if t < 0.3:                                        # the "pfft": the last flicker as it dies
            for i in range(6):
                th = i / 6 * math.tau + 0.3
                d = 2 + t * 22
                _polyline(layer, _rgba((235, 235, 235), 1 - t * 2.5),
                          [(ex + math.cos(th) * d, ey + math.sin(th) * d), (ex + math.cos(th) * (d + 3), ey + math.sin(th) * (d + 3))])
        for i in range(4):
            drift = (i - 1.5) * 4
            pygame.draw.circle(layer, _rgba(SMOKE, min(1.0, (1 - t) * 1.1)),
                               (int(ex + drift + _noise(i) * 2), int(ey - t * 14 - i * 2)), int(3 + t * 4 + i % 2))
        if fx_id == "kiem_khi":                            # the broken crescent falls in shards
            ang0 = math.atan2(dst[1] - src[1], dst[0] - src[0])
            for i in range(3):
                _crescent(layer, (225, 225, 225), (ex + (i - 1) * 7, ey + 3 + t * 14 + i * 2), ang0 + i, 3,
                          1 - t)
        for i in range(5):
            th = math.radians(20 + i * 35)
            pygame.draw.circle(layer, _rgba((190, 190, 190), (1 - t)),
                               (int(ex + math.cos(th) * t * 14 * (1 if i % 2 else -1)),
                                int(ey + math.sin(th) * t * 10 + t * t * 10)), 1)


_EFFECTS = {"chem": _chem, "kiem_khi": _kiem_khi, "hoa_cau": _hoa_cau, "tran_do": _tran_do,
            "ho_tran": _ho_tran, "thien_loi": _thien_loi}


def draw(surf: pygame.Surface, fx_id: str, p: float, src, dst=None, ok: bool = True,
         radius: float = 0.0) -> bool:
    """Paint the effect `fx_id` at progress `p` (0 = it begins, 1 = it is over) onto `surf`.

    `src` is the caster's feet, `dst` the target's feet (None: a chiêu with no target - the
    effect is then drawn a little in front of the caster), `radius` the area/ward radius the
    server reported. An unknown id is drawn as the plain slash, never an error. Returns False
    when `p` is outside 0..1 and so nothing was drawn."""
    if not 0.0 <= p <= 1.0:
        return False
    if dst is None:
        dst = (src[0] + 28, src[1])
    layer = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    if ok:
        _EFFECTS.get(fx_id, _chem)(layer, p, src, dst, radius)
    else:
        _fizzle(layer, fx_id if fx_id in _EFFECTS else "chem", p, src, dst, radius)
    surf.blit(layer, (0, 0))
    return True
