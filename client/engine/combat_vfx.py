"""What a fight looks like: kiếm khí that grows with tu vi, the attacks of every weapon family, the
seventeen chiêu thức, hits, deaths, Phản Đòn, Né Đòn, stage-ups and breakthroughs - as recipes over
engine/vfx.py. Every picture is a frame of a Blender sheet (client/assets/v2/fx/); this module
only decides which sheets, where, how big, turned which way, when, and how hard the camera kicks.

The tier ladder (the cultivation realm and stage, server Character.realm / realm_stage):

    T1 Phàm Nhân, Luyện Khí 1-3   T2 Luyện Khí 4-6   T3 Luyện Khí 7-9   T4 Trúc Cơ   T5 Kết Đan
    T6 Nguyên Anh   T7 Hóa Thần   T8 Luyện Hư   T9 Hợp Thể   T10 Đại Thừa
    tier group g: 1 = T1-3, 2 = T4-5, 3 = T6-7, 4 = T8-10

Sheets (the art contract; each one is looked up through a fallback chain, so the game draws
from what is on disk today and the new sheets light up the moment they are merged):

    kiem_khi_<T>     the swing arc at the attacker        else slash_<element> scaled by tier
    kiem_song_<T>    the qi wave flying to the target     else a held slash crescent + sword_trail
    kiem_no_<g>      the impact                           else hit_spark / burst_<el> / hit_crit
    kiem_ngan_<1-3>  the scar on the ground               else crack_ground
    thuong_dam_<g>   thrust streak (thương, kích)          else sword_trail stretched to the reach
    chuy_chan_<g>    ground shock ring (chùy, phủ)         else crack_ground + burst_tho + dust_step
    cung_ten_<g>     arrow of light (cung, ám khí, luân)   else bolt_<el> + sword_trail
    phap_dan_<g>     spell orb (hồ lô, trượng, phiến, cầm) else bolt_<el> with afterimages
    uy_ap            the pressure shockwave on the ground  else burst_<el> stretched flat

The recipes return the seconds until the blow visibly lands on the target, so the scene can show
the server's damage number at that moment instead of before the blade arrives.
"""
from __future__ import annotations

import math

from . import art2
from .vfx import Vfx, has

REALM_ORDER = ("pham_nhan", "luyen_khi", "truc_co", "kim_dan", "nguyen_anh", "hoa_than", "luyen_hu",
               "hop_the", "dai_thua")
_REALM_TIER = {"pham_nhan": 1, "truc_co": 4, "kim_dan": 5, "ket_dan": 5, "nguyen_anh": 6, "hoa_than": 7,
               "luyen_hu": 8, "hop_the": 9, "dai_thua": 10}

FAMILY_OF_TYPE = {
    "kiem": "blade", "dao": "blade", "roi": "blade", "sword": "blade", "sabre": "blade",
    "thuong": "thrust", "kich": "thrust", "spear": "thrust",
    "chuy": "smash", "phu": "smash", "hammer": "smash", "mace": "smash",
    "cung": "shot", "am_khi": "shot", "luan": "shot", "bow": "shot",
    "ho_lo": "spell", "truong": "spell", "phien": "spell", "cam": "spell", "brush": "spell", "staff": "spell",
    "fan": "spell", "gourd": "spell",
}
FAMILY_OF_CLIP = {"slash": "blade", "shoot": "shot", "cast": "spell"}
FAMILIES = ("blade", "thrust", "smash", "shot", "spell")

# the colour of the qi by tier when it is drawn from today's element sheets
ELEMENT = {1: "kim", 2: "kim", 3: "kim", 4: "thuy", 5: "tho", 6: "thuy", 7: "hoa", 8: "loi", 9: "loi", 10: "kim"}
ELEMENT2 = {6: "kim", 7: "tho", 8: "kim", 9: "hoa", 10: "loi"}         # the second arc from Nguyên Anh on
RGB = {"kim": (255, 244, 214), "thuy": (130, 196, 255), "tho": (246, 196, 96), "hoa": (255, 128, 64),
       "loi": (176, 128, 255), "moc": (132, 226, 128)}

ARC_SCALE = (0, 0.70, 0.84, 1.0, 1.12, 1.24, 1.36, 1.48, 1.6, 1.74, 1.9)
WAVE_SCALE = (0, 0, 0.55, 0.72, 0.86, 0.98, 1.04, 1.12, 1.2, 1.3, 1.44)
WAVES = (0, 0, 1, 1, 1, 1, 2, 3, 3, 3, 3)
OVERSHOOT = (0, 0, 12, 16, 20, 24, 28, 34, 44, 54, 70)     # world px a wave flies on past the target
AFTERIMAGES = (0, 0, 0, 2, 2, 3, 3, 3, 4, 4, 4)
SHAKE = (0, 0, 0, 0.0, 0.12, 0.16, 0.22, 0.28, 0.36, 0.44, 0.6)
FAN_DEG = 13.0
CREST = -60.0      # where the convex side of today's slash crescents points (screen degrees)
CHEST = 10.0       # world px above the feet where a blade swings
REACH = 12.0       # world px in front of the body where the arc is centred


# ------------------------------------------------------------------ who swings how hard
def tier(realm: str | None, stage: int | None = 0) -> int:
    """T1..T10 from the cultivation realm and stage (unknown realms are T1)."""
    r = realm or "pham_nhan"
    if r == "luyen_khi":
        s = int(stage or 1)
        return 1 if s <= 3 else (2 if s <= 6 else 3)
    return _REALM_TIER.get(r, 1)


def group(t: int) -> int:
    return 1 if t <= 3 else (2 if t <= 5 else (3 if t <= 7 else 4))


def family(weapon: str | None) -> str:
    """The weapon family of a weapon id ('<type>_<grade>' or an old kind): blade, thrust, smash,
    shot or spell. An unknown type goes by the clip its art plays; bare hands strike a palm of qi
    (blade)."""
    if not weapon:
        return "blade"
    w = str(weapon)
    t, _, grade = w.rpartition("_")
    kind = t if grade.isdigit() else w
    if kind in FAMILY_OF_TYPE:
        return FAMILY_OF_TYPE[kind]
    return FAMILY_OF_CLIP.get(art2.weapon_for(w)[1], "blade")


def strike_delay(realm: str | None, weapon: str | None) -> float:
    """Seconds from the start of the attack clip to its strike frame (events.hit of the sheet)."""
    clip = art2.weapon_for(weapon)[1] if weapon else "slash"
    s = art2.char_for(realm) if art2.on() else None
    if s is None or not s.has(clip):
        return 0.2
    c = s.clips[clip]
    hit = (s.events.get(clip) or {}).get("hit", 3)
    return max(0.05, float(hit) / max(1.0, c.fps))


def _choose(chain):
    """[(fid, scale, angle offset)] -> the first that exists, and whether it is the first."""
    for i, (fid, scale, rot) in enumerate(chain):
        if has(fid):
            return fid, scale, rot, i == 0
    return None, 0.0, 0.0, False


def _unit(src, dst) -> tuple[float, float, float, float]:
    dx, dy = dst[0] - src[0], dst[1] - src[1]
    d = math.hypot(dx, dy)
    if d < 0.01:
        return 1.0, 0.0, 0.0, 0.0
    return dx / d, dy / d, d, math.degrees(math.atan2(dy, dx))


def _turn(ux: float, uy: float, deg: float) -> tuple[float, float]:
    r = math.radians(deg)
    return ux * math.cos(r) - uy * math.sin(r), ux * math.sin(r) + uy * math.cos(r)


# ------------------------------------------------------------------ the pieces
def _impact(v: Vfx, t: int, x: float, y: float, lift: float, delay: float, el: str, tag=None) -> None:
    g = group(t)
    fid, sc, _r, primary = _choose([(f"kiem_no_{g}", 1.0, 0)])
    if primary:
        v.spawn(fid, x, y, delay, lift=lift, tag=tag)
        return
    if g == 1:
        v.spawn("hit_spark", x, y, delay, lift=lift, scale=0.8 + 0.12 * t, tag=tag)
        return
    # a star at the point of the blow, then the ring of the burst (its frames from 3 on: the
    # full white disc of the first frames would blot the monster out at these sizes)
    if g >= 3:
        v.spawn("hit_crit", x, y, delay, lift=lift, scale=(0.55 + 0.05 * t, 0.5 + 0.04 * t), peak=0.75, tag=tag)
    v.spawn("hit_spark", x, y, delay, lift=lift, scale=0.9 + 0.07 * t, tag=tag)
    v.spawn("burst_" + el, x, y, delay + 0.02, lift=lift, scale=(0.5 + 0.1 * t, 0.7 + 0.13 * t), start=3,
            fade_out=0.08, peak=0.9, tag=tag)
    if g >= 4:      # a second, wider ring a beat later: the blow keeps going
        v.spawn("burst_" + ELEMENT2.get(t, el), x, y, delay + 0.09, lift=lift, scale=(1.2, 1.9 + 0.12 * (t - 8)),
                start=3, peak=0.6, fade_out=0.1, heavy=True, tag=tag)


def _scar(v: Vfx, t: int, x: float, y: float, deg: float, delay: float, z: float, tag=None) -> None:
    if t < 4:
        return
    s = 1 if t <= 5 else (2 if t <= 7 else 3)
    if has(f"kiem_ngan_{s}"):
        v.spawn(f"kiem_ngan_{s}", x, y, delay, angle=deg, layer="ground", tag=tag)
        return
    sc = (0.36, 0.52, 0.74)[s - 1]
    v.spawn("crack_ground", x, y + 1, delay, life=1.3, scale=sc, fade_out=0.8, peak=0.6, layer="ground", tag=tag)


def _wave_chain(t: int, el: str):
    return [(f"kiem_song_{t}", 1.0, 0.0), ("slash_" + el, WAVE_SCALE[t], -CREST), ("slash_kim", WAVE_SCALE[t], -CREST)]


def _feel(v: Vfx, t: int, at: float, el: str, mine: bool) -> None:
    """Shake, tint and weight when the blow lands (only your own blows move your camera)."""
    if not mine:
        return
    if SHAKE[t] > 0:
        v.at(at, lambda: v.shake(SHAKE[t]))
    if t >= 9:      # a breath of colour over the screen only at the very top (basic attacks repeat)
        v.tint(RGB.get(el, (255, 255, 255)), 0.04 * (t - 8), 0.14, delay=at)


# ------------------------------------------------------------------ the rendered kiếm khí sheets
# art/src/fx_kiem/README.md: kiem_khi pivot = the sword hand, spawned on the hit frame; the wave
# leaves at FX frame 2 (100 ms later); facing left = mirror (never turn 180), up / down = -/+ 90.
# Low tiers stay modest on purpose: T1 an arc and a tiny spark, T2 a short needle of qi, T3 a
# crescent wave and kiem_no_1; the impact star and ring only from T4; at any moment one bright
# core on the target, and the sheets' own colours (flame T8, frost T9, cosmic T10) carry the tier.
TIER_TINT = {8: (255, 140, 60), 9: (140, 200, 255), 10: (170, 120, 255)}
# how dark a plate goes under a tier's sheets: the colour of high tiers survives bright grass
SHADE = (0, 0.0, 0.0, 0.15, 0.25, 0.3, 0.35, 0.45, 0.5, 0.55, 0.6)
HAND = {"right": (6.5, 12.0), "left": (-6.5, 12.0), "up": (3.0, 15.0), "down": (-3.0, 9.0)}
IMPACT_SCALE = {2: 0.72, 3: 0.62, 4: 0.55}   # kiem_no_g: a ring about the monster's width, its body still reads


def _within(t: int) -> float:
    """A little more size for each tier inside a tier group (the group sheets are shared)."""
    return 1.0 + 0.07 * (t - (1, 4, 6, 8)[group(t) - 1])


def _face(ux: float, uy: float) -> str:
    return ("right" if ux >= 0 else "left") if abs(ux) >= abs(uy) else ("down" if uy > 0 else "up")


def _pose(face: str) -> tuple[float, bool]:
    """(screen angle, mirrored) of a sheet drawn pointing right, for a swing facing `face`."""
    return {"right": (0.0, False), "left": (0.0, True), "up": (-90.0, False), "down": (90.0, False)}[face]


def _real_impact(v: Vfx, t: int, x: float, y: float, lift: float, delay: float) -> None:
    """The one bright core on the target: a spark for T1-T2, kiem_no_1 at T3, kiem_no_g from T4."""
    if t <= 2:
        v.spawn("hit_spark", x, y, delay, lift=lift, scale=0.42 if t == 1 else 0.55, peak=0.6 if t == 1 else 0.8)
        return
    fid = "kiem_no_1" if t == 3 else f"kiem_no_{group(t)}"
    if not v.spawn(fid, x, y, delay, lift=lift, scale=0.6 if t == 3 else IMPACT_SCALE[group(t)], peak=0.85,
                   shade=SHADE[t] * 0.7):
        v.spawn("hit_spark", x, y, delay, lift=lift, scale=0.7)


def _real_scar(v: Vfx, t: int, x: float, y: float, delay: float) -> None:
    if t >= 4:
        v.spawn(f"kiem_ngan_{1 if t <= 5 else (2 if t <= 7 else 3)}", x, y + 1, delay, layer="ground",
                scale=0.8, peak=0.8)


def _real_feel(v: Vfx, t: int, at: float, mine: bool) -> None:
    if not mine:
        return
    if SHAKE[t] > 0:
        v.at(at, lambda: v.shake(SHAKE[t]))
    if t >= 8:
        v.tint(TIER_TINT[t], 0.03 + 0.02 * (t - 8), 0.14, delay=at)


def _blade_real(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    ux, uy, dist, deg = _unit(src, dst)
    face = _face(ux, uy)
    ang, flip = _pose(face)
    hx, hy = HAND[face]
    v.spawn(f"kiem_khi_{t}", src[0] + hx, src[1], strike, lift=hy, angle=ang, flip=flip, follow=follow,
            shade=SHADE[t])
    land = strike + 0.05
    if t >= 2 and has(f"kiem_song_{t}"):
        launch = strike + 0.1
        sx, sy = src[0] + hx, src[1]
        span = max(6.0, dist - abs(hx))
        over = 0.0 if t == 2 else OVERSHOOT[t]          # T2: a short needle that dies on the target
        speed = 300.0 + 20.0 * t
        travel = max(0.1, (span + over) / speed)
        land = launch + travel * span / (span + over)
        offs = [0.0] if t < 8 else [0.0, 8.0 if t < 10 else -8.0]
        for i, off in enumerate(offs):
            wx, wy = _turn(ux, uy, off)
            ex, ey = sx + wx * (span + over), sy + wy * (span + over)
            v.spawn(f"kiem_song_{t}", sx, sy, launch + i * 0.05, life=travel, to=(ex, ey), lift=hy,
                    lift1=dst_lift, angle=deg + off, scale=0.7 if t == 2 else 1.0, peak=1.0 if i == 0 else 0.45,
                    fade_in=0.03, fade_out=min(0.1, travel * 0.4) if over else 0.04, heavy=i > 0,
                    shade=SHADE[t] if i == 0 else 0.0)
    _real_impact(v, t, dst[0], dst[1], dst_lift, land)
    _real_scar(v, t, dst[0], dst[1], land)
    _real_feel(v, t, land, mine)
    if t == 10:                         # the sky is cut: the arc again, falling through the target
        v.spawn("kiem_khi_10", dst[0] - 4, dst[1], land + 0.05, lift=dst_lift + 34, angle=90.0, peak=0.55,
                heavy=True)
    if t >= 8 and garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - dst_lift, ELEMENT[t], 6 + 2 * (t - 8), 40))
    return land


def _thrust_real(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    """thuong_dam_g: a lance of light from the hand along the blow (its pivot is the hand)."""
    ux, uy, dist, deg = _unit(src, dst)
    hx, hy = HAND[_face(ux, uy)]
    g = group(t)
    s = art2.fx(f"thuong_dam_{g}")
    reach = s.fw * 0.68 / z if s is not None else 30.0          # the lance is 0.68 of its frame
    want = max(12.0, dist - abs(hx) + 6)
    k = max(0.55, min(1.4, want / max(1.0, reach))) * _within(t)
    v.spawn(f"thuong_dam_{g}", src[0] + hx, src[1], strike, lift=hy, angle=deg, scale=k, follow=follow)
    land = strike + 0.06
    _real_impact(v, t, dst[0], dst[1], dst_lift, land)
    _real_scar(v, t, dst[0], dst[1], land)
    _real_feel(v, t, land, mine)
    return land


def _smash_real(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    """chuy_chan_g: the shock ring on the GROUND under the target; a small gold arc at the hand."""
    ux, uy, dist, deg = _unit(src, dst)
    hx, hy = HAND[_face(ux, uy)]
    g = group(t)
    land = strike + 0.03
    v.spawn("slash_tho", src[0] + hx + ux * 4, src[1] + uy * 4, strike - 0.03, lift=hy, scale=0.5 + 0.03 * t,
            angle=deg + 50 - CREST, peak=0.6, heavy=True)
    v.spawn(f"chuy_chan_{g}", dst[0], dst[1] + 1, land, layer="ground", scale=(0.72 if g == 1 else 0.95) * _within(t))
    if t >= 6:
        _real_impact(v, t, dst[0], dst[1], dst_lift * 0.6, land + 0.02)
    else:
        v.spawn("hit_spark", dst[0], dst[1], land, lift=dst_lift * 0.6, scale=0.45 + 0.04 * t, peak=0.8)
    if mine:
        v.at(land, lambda: v.shake(0.1 + SHAKE[t] * 1.2))
    if garnish is not None and t >= 4:
        v.at(land, lambda: garnish(dst[0], dst[1] - 2, "tho", 4 + t, 28))
    return land


def _volley_real(v, t, src, dst, strike, dst_lift, mine, z, kind: str) -> float:
    """cung_ten_g (arrow, its head forward) or phap_dan_g (orb with its tail) flying to the target."""
    ux, uy, dist, deg = _unit(src, dst)
    hx, hy = HAND[_face(ux, uy)]
    g = group(t)
    fid = f"cung_ten_{g}" if kind == "shot" else f"phap_dan_{g}"
    speed = (320.0 + 20 * t) if kind == "shot" else (210.0 + 14 * t)
    n = (1, 1, 2, 3)[g - 1] if kind == "shot" else (1, 1, 1, 2)[g - 1]
    sx, sy = src[0] + hx, src[1]
    span = max(6.0, dist - abs(hx))
    travel = max(0.08, min(0.5, span / speed))
    land = strike + travel
    offs = [0.0] if n == 1 else ([-6.0, 6.0] if n == 2 else [-8.0, 0.0, 8.0])
    for i, off in enumerate(offs):
        wx, wy = _turn(ux, uy, off * 0.5)
        v.spawn(fid, sx, sy, strike + i * 0.045, life=travel, to=(sx + wx * span, sy + wy * span), lift=hy,
                lift1=dst_lift, angle=deg + off * 0.5, arc=0.0 if kind == "shot" else 4.0, fade_in=0.03,
                scale=(0.8 if g <= 2 else 0.75) * _within(t), peak=1.0 if i == 0 else 0.7, heavy=i > 0)
    _real_impact(v, t, dst[0], dst[1], dst_lift, land + 0.01 * (n - 1))
    if t >= 6:
        _real_scar(v, t, dst[0], dst[1], land)
    _real_feel(v, t, land, mine)
    return land


def _shot_real(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    return _volley_real(v, t, src, dst, strike, dst_lift, mine, z, "shot")


def _spell_real(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    return _volley_real(v, t, src, dst, strike, dst_lift, mine, z, "spell")


def _real(fam: str, t: int):
    """The recipe drawn from the rendered sheets for this family and tier, or None (the stand-ins)."""
    g = group(t)
    want = {"blade": f"kiem_khi_{t}", "thrust": f"thuong_dam_{g}", "smash": f"chuy_chan_{g}",
            "shot": f"cung_ten_{g}", "spell": f"phap_dan_{g}"}[fam]
    if not has(want):
        return None
    return {"blade": _blade_real, "thrust": _thrust_real, "smash": _smash_real, "shot": _shot_real,
            "spell": _spell_real}[fam]


# ------------------------------------------------------------------ basic attacks
def swing(v: Vfx, weapon: str | None, t: int, src, dst, strike: float = 0.2, dst_lift: float = 10.0,
          follow=None, mine: bool = True, z: float = 2.0, garnish=None) -> float:
    """One basic attack of tier `t` with `weapon` from `src` (the attacker's feet) at `dst` (the
    target's feet), its strike frame `strike` seconds from now. Returns when it lands."""
    fam = family(weapon)
    t = max(1, min(10, int(t)))
    fn = _real(fam, t) or {"blade": _blade, "thrust": _thrust, "smash": _smash, "shot": _shot, "spell": _spell}[fam]
    return fn(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish)


def _blade(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    ux, uy, dist, deg = _unit(src, dst)
    el = ELEMENT[t]
    ax, ay = src[0] + ux * REACH, src[1] + uy * REACH
    fid, sc, rot, primary = _choose([(f"kiem_khi_{t}", 1.0, 0.0), ("slash_" + el, ARC_SCALE[t], -CREST),
                                     ("slash_kim", ARC_SCALE[t], -CREST)])
    if fid is None:
        return strike
    v.spawn(fid, ax, ay, strike, lift=CHEST, scale=(sc * 0.9, sc), angle=deg + rot, follow=follow)
    if not primary and t >= 6:      # a second arc in another colour, a hair later and larger
        el2 = ELEMENT2.get(t, "kim")
        v.spawn("slash_" + el2, ax + ux * 2, ay + uy * 2, strike + 0.035, lift=CHEST,
                scale=(sc * 1.0, sc * 1.12), angle=deg + rot + 8, peak=0.5, follow=follow, heavy=True)
    if not primary and t >= 6:      # the light of the arc lingers a moment
        v.spawn(fid, ax, ay, strike + 0.12, life=0.42, lift=CHEST, scale=sc * 1.05, angle=deg + rot,
                hold=2, peak=0.3, fade_out=0.35, follow=follow, heavy=True)
    land = strike + 0.03
    if WAVES[t]:
        land = _waves(v, t, el, src, dst, ux, uy, dist, deg, strike, dst_lift)
    _impact(v, t, dst[0], dst[1], dst_lift, land, el)
    _scar(v, t, dst[0], dst[1], deg, land, z)
    _feel(v, t, land, el, mine)
    if t >= 8 and garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - dst_lift, el, 10 + 3 * (t - 8), 46))
    if t == 10:
        _sky_cut(v, dst, dst_lift, land, mine)
    return land


def _waves(v, t, el, src, dst, ux, uy, dist, deg, strike, dst_lift) -> float:
    """The qi waves leaving the blade: one from T2, a fan of two or three from Nguyên Anh on,
    flying on past the target at the top tiers. Returns when the middle one reaches the target."""
    over = OVERSHOOT[t]
    speed = 230.0 + 22.0 * t
    if t == 2:
        chain = [(f"kiem_song_{t}", 1.0, 0.0), ("sword_trail", 0.62, 0.0)]
    else:
        chain = _wave_chain(t, el)
    fid, sc, rot, primary = _choose(chain)
    n = WAVES[t]
    sx, sy = src[0] + ux * (REACH - 2), src[1] + uy * (REACH - 2)
    span = max(4.0, dist - REACH + 2)
    total = span + over
    travel = max(0.14, min(0.42, total / speed))
    # eased "out" (1 - (1 - k)^3): the wave reaches the target when that equals span / total
    land = strike + 0.02 + travel * (1 - (1 - span / total) ** (1 / 3))
    if fid is None:
        return land
    offsets = [0.0] if n == 1 else ([-FAN_DEG / 2, FAN_DEG / 2] if n == 2 else [-FAN_DEG, 0.0, FAN_DEG])
    for i, off in enumerate(offsets):
        wx, wy = _turn(ux, uy, off)
        ex, ey = sx + wx * total, sy + wy * total
        side = off != 0.0
        lead = n != 2 and not side or (n == 2 and i == 0)
        d0 = strike + 0.02 + abs(off) * 0.002
        kw = dict(to=(ex, ey), lift=CHEST, lift1=dst_lift, ease="out", angle=deg + off + rot,
                  fade_out=travel * 0.45, peak=1.0 if lead else 0.8, heavy=side)
        if not primary and fid != "sword_trail":
            kw.update(frames=(1, 2), trail=(AFTERIMAGES[t], 0.024) if lead else None)
        v.spawn(fid, sx, sy, d0, life=travel, scale=sc if lead else sc * 0.85, **kw)
        if not primary and fid != "sword_trail" and t >= 3 and lead:      # the streak behind the crescent
            v.spawn("sword_trail", sx, sy, d0, life=travel, scale=0.5 + 0.06 * t, to=(ex, ey), lift=CHEST,
                    lift1=dst_lift, ease="out", angle=deg + off, peak=0.7, fade_out=travel * 0.5, heavy=True)
    return land


def _sky_cut(v, dst, dst_lift, land, mine) -> None:
    """Đại Thừa: the sky is cut - a slash taller than the screen comes down through the target."""
    # one long blade of light from above the screen down through the target, a beat after the
    # waves: sword_trail drawn as a thin beam, its head on the ground
    if has("sword_trail"):
        v.spawn("sword_trail", dst[0] + 12, dst[1] - 110, land + 0.05, life=0.3, size=(300, 26), scale=(0.6, 1.0),
                to=(dst[0] + 3, dst[1] - 72), lift=0, angle=78, fade_out=0.18, heavy=True)
        v.spawn("sword_trail", dst[0] + 12, dst[1] - 110, land + 0.05, life=0.22, size=(300, 10), scale=1.0,
                to=(dst[0] + 3, dst[1] - 72), lift=0, angle=78, fade_out=0.12, heavy=True)
    v.spawn("loi_kiep", dst[0], dst[1], land + 0.08, scale=1.1, peak=0.8, heavy=True)
    v.spawn("crack_ground", dst[0], dst[1] + 1, land + 0.1, life=1.5, scale=0.95, fade_out=0.8, layer="ground",
            heavy=True)


def _thrust(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    ux, uy, dist, deg = _unit(src, dst)
    el = ELEMENT[t]
    g = group(t)
    over = OVERSHOOT[t] * 0.6 + 6
    reach = max(10.0, dist + over - REACH)
    fid, sc, rot, primary = _choose([(f"thuong_dam_{g}", 1.0, 0.0), ("sword_trail", 1.0, 0.0)])
    land = strike + 0.05
    if fid is not None:
        cx, cy = src[0] + ux * (REACH + reach / 2), src[1] + uy * (REACH + reach / 2)
        if primary:
            v.spawn(fid, src[0] + ux * REACH, src[1] + uy * REACH, strike, lift=CHEST, angle=deg)
        else:
            w = reach * z * (1.0 + 0.04 * t)
            h = 22 + 3.2 * t
            v.spawn(fid, cx, cy, strike, life=0.2 + 0.012 * t, size=(w, h), scale=(0.7, 1.0), lift=CHEST,
                    angle=deg, fade_out=0.12)
            if t >= 4:      # a second, thinner jab of qi straight after
                v.spawn(fid, cx + ux * 6, cy + uy * 6, strike + 0.07, life=0.18, size=(w * 1.15, h * 0.6), lift=CHEST,
                        angle=deg, peak=0.7, fade_out=0.1, heavy=True)
            v.spawn("slash_" + el, src[0] + ux * REACH, src[1] + uy * REACH, strike, lift=CHEST,
                    scale=ARC_SCALE[t] * 0.6, angle=deg - CREST, peak=0.6, heavy=True)
    _impact(v, t, dst[0], dst[1], dst_lift, land, el)
    _scar(v, t, dst[0], dst[1], deg, land, z)
    _feel(v, t, land, el, mine)
    return land


def _smash(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    ux, uy, dist, deg = _unit(src, dst)
    g = group(t)
    land = strike + 0.03
    gx, gy = dst[0] - ux * 3, dst[1] - uy * 3
    fid, sc, rot, primary = _choose([(f"chuy_chan_{g}", 1.0, 0.0)])
    if primary:
        v.spawn(fid, gx, gy, land, layer="ground")
    else:
        v.spawn("crack_ground", gx, gy + 1, land, life=1.1, scale=0.32 + 0.09 * t, fade_out=0.7, layer="ground")
        v.spawn("burst_tho", gx, gy, land, lift=2, size=(64 * (0.7 + 0.14 * t), 30 * (0.7 + 0.14 * t)),
                peak=0.85, fade_out=0.1)
        v.spawn("dust_step", gx - 8, gy + 2, land + 0.02, scale=0.6 + 0.07 * t)
        v.spawn("dust_step", gx + 8, gy + 2, land + 0.04, scale=0.6 + 0.07 * t, heavy=True)
    if g >= 3:
        _shockwave(v, gx, gy, land + 0.05, 0.9 + 0.25 * (t - 6), ELEMENT[t])
    v.spawn("slash_tho", src[0] + ux * REACH, src[1] + uy * REACH, strike - 0.03, lift=CHEST + 4,
            scale=ARC_SCALE[t] * 0.7, angle=deg + 50 - CREST, peak=0.7, heavy=True)
    _impact(v, t, dst[0], dst[1], dst_lift * 0.6, land, ELEMENT[t])
    if mine:
        v.at(land, lambda: v.shake(0.1 + SHAKE[t] * 1.2))
    if garnish is not None and t >= 4:
        v.at(land, lambda: garnish(gx, gy - 2, "tho", 6 + t, 30))
    return land


def _ground_ring(v, x, y, delay, k, el) -> None:
    """A flat ring of light running out over the ground (a burst's ring frames squashed flat)."""
    v.spawn("burst_" + el, x, y, delay, size=(64 * 1.6 * k, 64 * 0.7 * k), scale=(0.6, 1.4), start=3, peak=0.45,
            fade_out=0.1, layer="ground", heavy=True)


def _shockwave(v, x, y, delay, k, el) -> None:
    """The flat ring of pressure on the ground: uy_ap, else a burst squashed onto the ground."""
    if has("uy_ap"):
        v.spawn("uy_ap", x, y, delay, layer="ground", scale=0.6 * k, heavy=True)
        return
    v.spawn("burst_" + el, x, y, delay, size=(64 * 1.6 * k, 64 * 0.7 * k), scale=(0.6, 1.4), start=3, peak=0.7,
            fade_out=0.1, layer="ground", heavy=True)


def _volley(v, t, src, dst, strike, dst_lift, mine, z, kind: str) -> float:
    ux, uy, dist, deg = _unit(src, dst)
    el = ELEMENT[t]
    g = group(t)
    if kind == "shot":
        chain = [(f"cung_ten_{g}", 1.0, 0.0), ("bolt_" + el, 0.42 + 0.06 * t, 0.0)]
        speed, n, spread, arc = 300.0 + 20 * t, (1, 1, 2, 3)[g - 1], 9.0, 0.0
    else:
        chain = [(f"phap_dan_{g}", 1.0, 0.0), ("bolt_" + el, 0.5 + 0.07 * t, 0.0)]
        speed, n, spread, arc = 190.0 + 14 * t, (1, 1, 2, 2)[g - 1], 16.0, 6.0
    fid, sc, rot, primary = _choose(chain)
    sx, sy = src[0] + ux * 8, src[1] + uy * 8
    span = max(6.0, dist - 8)
    travel = max(0.08, min(0.5, span / speed))
    land = strike + travel
    if fid is None:
        return land
    offs = [0.0] if n == 1 else ([-spread / 2, spread / 2] if n == 2 else [-spread, 0.0, spread])
    for i, off in enumerate(offs):
        wx, wy = _turn(ux, uy, off * 0.6)
        ex, ey = sx + wx * span, sy + wy * span
        d0 = strike + i * 0.045
        kw = dict(to=(ex, ey), lift=CHEST + 1, lift1=dst_lift, angle=deg + off * 0.6, arc=arc * (1 + i * 0.4),
                  heavy=i > 0)
        if not primary:
            kw["trail"] = (2 + g, 0.024) if kind == "spell" else None
        v.spawn(fid, sx, sy, d0, life=travel, scale=sc, **kw)
        if not primary and kind == "shot":
            v.spawn("sword_trail", sx, sy, d0, life=travel, scale=0.45 + 0.05 * t, to=(ex, ey), lift=CHEST + 1,
                    lift1=dst_lift, angle=deg + off * 0.6, peak=0.8, heavy=True)
    if kind == "spell" and not primary:      # the orb gathers at the hand first
        v.spawn("bolt_" + el, sx, sy, max(0.0, strike - 0.12), life=0.14, lift=CHEST + 1, scale=(sc * 0.3, sc),
                peak=0.8, heavy=True)
    _impact(v, t, dst[0], dst[1], dst_lift, land + 0.01 * (n - 1), el)
    if t >= 6:
        _scar(v, t, dst[0], dst[1], deg, land, z)
    _feel(v, t, land, el, mine)
    return land


def _shot(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    return _volley(v, t, src, dst, strike, dst_lift, mine, z, "shot")


def _spell(v, t, src, dst, strike, dst_lift, follow, mine, z, garnish) -> float:
    return _volley(v, t, src, dst, strike, dst_lift, mine, z, "spell")


# ------------------------------------------------------------------ chiêu thức
# every chiêu: charge (qi gathers in the hand - tu_khi_<element> - and a rune circle under the
# feet) -> release -> travel -> impact with weight -> linger; the tier makes it a little bigger.
# The sequencing, pivots and timings of the hero sheets follow art/src/fx_chieu/README.md
# ("Notes for the programmer"). `ex` carries what the server's event says beyond one target:
# hits [(x, y) feet of every monster struck, in the order struck], end (x, y) of a line, d the
# seconds what it leaves behind lasts (freeze, root, burn, bell, domain).
CHIEU_EL = {"chem": "tho", "kiem_khi": "kim", "hoa_cau": "hoa", "tran_do": "moc", "ho_tran": "thuy",
            "thien_loi": "loi", "ngu_kiem": "kim", "van_kiem": "kim", "bang_phong": "thuy", "loi_xich": "loi",
            "hoa_long": "hoa", "dia_liet": "tho", "thanh_dang": "moc", "phong_nhan": "moc", "kim_chung": "kim",
            "kiem_vuc": "kim", "hoi_xuan": "moc"}
CHIEU_CIRCLE = {"chem": "tran_1", "kiem_khi": "tran_5", "hoa_cau": "tran_4", "tran_do": "tran_3",
                "ho_tran": "tran_2", "thien_loi": "tran_8", "ngu_kiem": "tran_5", "van_kiem": "tran_7",
                "bang_phong": "tran_2", "loi_xich": "tran_8", "hoa_long": "tran_4", "dia_liet": "tran_1",
                "thanh_dang": "tran_3", "phong_nhan": "tran_3", "kim_chung": "tran_5", "kiem_vuc": "tran_7",
                "hoi_xuan": "tran_6"}
CHARGE = {"chem": 0.12, "kiem_khi": 0.3, "hoa_cau": 0.36, "tran_do": 0.34, "ho_tran": 0.3, "thien_loi": 0.5,
          "ngu_kiem": 0.3, "van_kiem": 0.55, "bang_phong": 0.32, "loi_xich": 0.28, "hoa_long": 0.4,
          "dia_liet": 0.16, "thanh_dang": 0.3, "phong_nhan": 0.22, "kim_chung": 0.2, "kiem_vuc": 0.55,
          "hoi_xuan": 0.26}
TUYET_KY = ("thien_loi", "van_kiem", "kiem_vuc")       # charged at full size, they shake and tint the screen
NO_CIRCLE = ("chem", "ho_tran", "kim_chung", "hoi_xuan", "kiem_vuc")
SELF_CAST = ("ho_tran", "kim_chung", "hoi_xuan", "kiem_vuc")   # no target: drawn on the caster


def _k(t: int) -> float:
    return 1.0 + 0.04 * (max(1, min(10, t)) - 1)


def _hand(src, dst) -> tuple[float, float, float, str]:
    """(x, y, lift, facing) of the casting hand of a caster at `src` turned towards `dst`."""
    ux, uy, _d, _deg = _unit(src, dst)
    face = _face(ux, uy)
    ox, lift = HAND[face]
    return src[0] + ox, src[1], lift, face


def _aim(deg: float) -> tuple[float, bool]:
    """(angle, mirrored) for art that points right flying at `deg`: leftwards it is mirrored
    instead of turned upside down (the dragon, the fireball)."""
    if math.cos(math.radians(deg)) < -1e-6:
        return deg - 180.0, True
    return deg, False


def _charge(v: Vfx, fx_id: str, src, dst, charge: float, follow) -> None:
    """tu_khi_<element> gathering at the hand for the charge (0.75 for a short cast, 1.0 for a
    tuyệt kỹ), stopped as the chiêu is released."""
    if charge <= 0.03:
        return
    hx, hy, lift, _face_ = _hand(src, dst)
    big = fx_id in TUYET_KY
    v.spawn(f"tu_khi_{CHIEU_EL.get(fx_id, 'kim')}", hx, hy, 0.0, life=charge + 0.04, lift=lift,
            scale=1.0 if big else 0.75, fade_in=0.05, fade_out=0.08, follow=follow)


def _hits(ex: dict, dst) -> list[tuple[float, float]]:
    pts = [(float(h[0]), float(h[1])) for h in (ex.get("hits") or [])]
    return pts or [dst]


def channel(v: Vfx, fx_id: str, follow, x: float, y: float, t: int = 1) -> None:
    """A chiêu being channelled (its question is open): the rune circle under the caster and
    tu_khi gathering in the hand, until `v.kill(("chan", follow))`."""
    tag = ("chan", follow)
    v.kill(tag)
    circle = CHIEU_CIRCLE.get(fx_id, "tran_1")
    k = 0.42 + 0.03 * t
    v.spawn(circle, x, y, life=60.0, layer="ground", scale=(k * 0.5, k), fade_in=0.25, peak=0.85, follow=follow,
            tag=tag)
    el = CHIEU_EL.get(fx_id, "kim")
    ox, lift = HAND["right"]
    if not v.spawn(f"tu_khi_{el}", x + ox, y, life=60.0, lift=lift, scale=1.0 if fx_id in TUYET_KY else 0.75,
                   fade_in=0.15, follow=follow, tag=tag):
        v.spawn("bolt_" + el, x, y, life=60.0, lift=CHEST, scale=(0.2, 0.45), peak=0.5, follow=follow, tag=tag)


def chieu(v: Vfx, fx_id: str, src, dst, t: int = 1, radius: float = 0.0, charged: bool = False,
          follow=None, mine: bool = True, z: float = 2.0, garnish=None, dst_lift: float = 10.0,
          ex: dict | None = None) -> float:
    """A landed chiêu thức from `src` (the caster's feet) at `dst` (the target's feet; None for a
    chiêu with no target). `charged`: its channel was already shown (a bí cảnh question), so the
    charge is short. `ex`: hits / end / d from the server's event. Returns the seconds until it
    lands on the (first) target."""
    t = max(1, min(10, int(t)))
    ex = ex or {}
    v.kill(("chan", follow))
    if dst is None:
        dst = (src[0] + 14, src[1])
    charge = 0.1 if charged else CHARGE.get(fx_id, 0.3)
    if fx_id not in NO_CIRCLE:
        k = 0.42 + 0.03 * t
        v.spawn(CHIEU_CIRCLE.get(fx_id, "tran_1"), src[0], src[1], life=charge + 0.45, layer="ground",
                scale=(k * (0.9 if charged else 0.4), k), fade_in=0.08, fade_out=0.3, peak=0.85, follow=follow)
    _charge(v, fx_id, src, dst, charge, follow)
    fn = RECIPES.get(fx_id, _c_chem)
    return fn(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex)


def _gather(v, x, y, el, charge, follow, n=6) -> None:
    """Qi streaming into the caster during the charge (thin streaks under the tu_khi)."""
    for i in range(n):
        ang = i * (360.0 / n) + 20
        ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        v.spawn("sword_trail", x + ux * 30, y + uy * 18, i * charge / (n + 2), life=max(0.12, charge * 0.6),
                to=(x, y), lift=CHEST + 8, lift1=CHEST, ease="in", angle=ang + 180, scale=0.44, peak=0.55,
                follow=follow, heavy=True)


def _c_chem(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Thường Quyền: an earthen cross cut - two heavy golden-brown arcs crossing on the target."""
    ux, uy, dist, deg = _unit(src, dst)
    k = 1.0 + 0.07 * (t - 1)
    land = charge + 0.04
    v.spawn("dust_step", src[0] - ux * 4, src[1] + 2, 0.0, scale=0.7)
    v.spawn("slash_tho", dst[0], dst[1], charge, lift=dst_lift, scale=(1.1 * k, 1.3 * k), angle=deg + 35 - CREST)
    v.spawn("slash_tho", dst[0], dst[1], charge + 0.08, lift=dst_lift, scale=(1.1 * k, 1.3 * k),
            angle=deg - 35 + 180 - CREST)
    if t >= 6:
        v.spawn("slash_kim", dst[0], dst[1], charge + 0.13, lift=dst_lift, scale=1.2 * k, angle=deg - CREST,
                peak=0.7, heavy=True)
    v.spawn("hit_spark", dst[0], dst[1], land + 0.06, lift=dst_lift, scale=1.0 * k)
    v.spawn("crack_ground", dst[0], dst[1] + 1, land + 0.06, life=1.0, scale=0.42 * k, fade_out=0.6,
            layer="ground")
    v.spawn("dust_step", dst[0] + 6, dst[1] + 2, land + 0.1, scale=0.8 * k, heavy=True)
    if mine:
        v.at(land + 0.06, lambda: v.shake(0.14 + 0.02 * t))
    return land + 0.06


def _c_kiem_khi(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Phá Mê Kiếm Quyết: pha_me_kiem - one straight cut of sword light from the sword hand that
    flashes a cross glint as it passes through the target (mirrored left, turned up / down)."""
    ux, uy, dist, deg = _unit(src, dst)
    hx, hy, lift, face = _hand(src, dst)
    ang, flip = _pose(face)
    k = _k(t)
    land = charge + 0.05                                  # damage on frame 1 (20 fps)
    if not v.spawn("pha_me_kiem", hx, hy, charge, lift=lift, angle=ang, flip=flip, scale=k, follow=follow):
        v.spawn("slash_kim", src[0] + ux * REACH, src[1] + uy * REACH, charge, lift=CHEST, scale=1.3 * k,
                angle=deg - CREST, follow=follow)
    v.spawn("slash_kim", dst[0], dst[1], land + 0.02, lift=dst_lift, scale=0.9 * k, angle=deg + 90 - CREST,
            peak=0.8)
    v.spawn("hit_spark", dst[0], dst[1], land + 0.03, lift=dst_lift, scale=1.0)
    if t >= 4:
        _scar(v, t, dst[0], dst[1], deg, land, z)
    if mine:
        v.at(land, lambda: v.shake(0.18 + 0.03 * t))
    return land


def _c_hoa_cau(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Hỏa Cầu Thuật: hoa_cau_lon - the big fireball with its tail - arcs over to the target and
    bursts as hoa_cau_no (damage on its frames 1-2)."""
    hx, hy, lift, face = _hand(src, dst)
    ux, uy, dist, deg = _unit((hx, hy), dst)
    k = _k(t)
    speed = 170.0 + 8 * t
    travel = max(0.16, min(0.6, dist / speed))
    ang, flip = _aim(deg)
    if not v.spawn("hoa_cau_lon", hx, hy, charge, life=travel, to=(dst[0], dst[1]), lift=lift, lift1=dst_lift,
                   arc=6 + dist * 0.08, angle=ang, flip=flip, scale=0.8 * k, fade_in=0.04):
        v.spawn("bolt_hoa", hx, hy, charge, life=travel, to=(dst[0], dst[1]), lift=lift, lift1=dst_lift,
                arc=10 + dist * 0.12, angle=deg, scale=1.05 * k, trail=(5, 0.028))
    land = charge + travel + 0.06
    if not v.spawn("hoa_cau_no", dst[0], dst[1], charge + travel, lift=dst_lift, scale=0.8 * k):
        v.spawn("burst_hoa", dst[0], dst[1], charge + travel, lift=dst_lift, scale=(1.2 * k, 1.7 * k), fade_out=0.12)
    v.spawn("crack_ground", dst[0], dst[1] + 1, land, life=1.2, scale=0.5 * k, fade_out=0.7, layer="ground")
    if mine:
        v.at(land, lambda: v.shake(0.24 + 0.03 * t))
        v.tint(RGB["hoa"], 0.06, 0.2, delay=land)
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - dst_lift, "hoa", 12, 50))
    return land


def _c_tran_do(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Ngũ Hành Trận: the array opens on the ground round the target, then its five marks erupt
    one after another in the five colours and the centre bursts."""
    r = radius or 60.0
    k = 1.0 + 0.04 * (t - 1)
    arr = art2.fx("tran_3")
    d = 2 * r * z * (arr.fw / 90.0 if arr is not None else 1.07)
    land = charge + 0.3
    v.spawn("tran_3", dst[0], dst[1], charge, life=1.3, size=(d, d * (arr.fh / arr.fw if arr else 1)),
            scale=(0.3, 1.0), fade_out=0.4, layer="ground")
    order = ("kim", "moc", "thuy", "hoa", "tho")
    for i, el in enumerate(order):
        a = math.radians(-90 + i * 72)
        px, py = dst[0] + math.cos(a) * r * 0.62, dst[1] + math.sin(a) * r * 0.31
        v.spawn("burst_" + el, px, py, charge + 0.12 + i * 0.05, lift=6, scale=(0.6 * k, 0.9 * k), start=2, fade_out=0.08)
        if t >= 4:
            v.spawn("slash_" + el, px, py, charge + 0.14 + i * 0.05, lift=10, scale=0.6 * k, angle=-90 - CREST,
                    peak=0.7, heavy=True)
    v.spawn("burst_moc", dst[0], dst[1], land, lift=dst_lift, scale=(1.2 * k, 1.6 * k), fade_out=0.12)
    _shockwave(v, dst[0], dst[1], land + 0.04, r / 40.0, "moc")
    if mine:
        v.at(land, lambda: v.shake(0.2 + 0.02 * t))
        v.tint(RGB["moc"], 0.05, 0.25, delay=land)
    return land


def _c_ho_tran(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Hộ Thân Trận: the ward - a ring the size of its reach on the ground, a honeycomb dome that
    pops up round the caster, a wave of water-blue running outward."""
    x, y = src
    r = min(radius or 40.0, 70.0)      # the ring shows the ward, not its whole reach (it would fill the screen)
    k = 1.0 + 0.05 * (t - 1)
    ring = art2.fx("tran_2")
    d = 2 * r * z * (ring.fw / 90.0 if ring is not None else 1.07)
    v.spawn("tran_2", x, y, 0.0, life=charge + 1.0, size=(d, d * (ring.fh / ring.fw if ring else 1)),
            scale=(0.2, 1.0), fade_in=0.1, fade_out=0.5, peak=0.4, layer="ground", follow=follow)
    v.spawn("linh_thuan", x, y, charge, life=1.5, lift=CHEST, scale=(0.5 * k, 1.35 * k), fade_in=0.06, fade_out=0.5,
            follow=follow)
    v.spawn("heal", x, y, charge + 0.1, life=0.9, lift=CHEST + 4, scale=0.9 * k, fade_out=0.3, follow=follow,
            heavy=True)
    _shockwave(v, x, y, charge + 0.04, r / 45.0, "thuy")
    if mine:
        v.tint(RGB["thuy"], 0.05, 0.3, delay=charge)
    return charge


def _c_thien_loi(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Thiên Lôi Tuyệt Kỹ: the sky darkens while the caster calls, then thien_loi_giang - the
    main bolt - comes down on the target (damage on its frame 1), the ground cracks and the
    screen goes white for a blink."""
    ux, uy, dist, deg = _unit(src, dst)
    k = _k(t)
    if mine:
        v.tint((40, 24, 80), 0.2, charge + 0.5)
    land = charge + 1 / 16
    if has("sword_trail"):      # the release: a bolt of qi thrown up into the clouds
        v.spawn("sword_trail", src[0], src[1], charge - 0.06, life=0.16, to=(src[0] + 4, src[1]), lift=CHEST + 10,
                lift1=CHEST + 90, angle=-86, size=(90, 22), ease="in", peak=0.9)
    if not v.spawn("thien_loi_giang", dst[0], dst[1], charge, scale=k):
        v.spawn("loi_kiep", dst[0], dst[1], charge, scale=1.5 * k)
    if t >= 6:
        v.spawn("loi_kiep", dst[0] - 15, dst[1] + 2, charge + 0.18, scale=0.9 * k, peak=0.7, heavy=True)
    v.spawn("crack_ground", dst[0], dst[1] + 1, land, life=1.5, scale=0.7 * k, fade_out=0.8, layer="ground")
    _shockwave(v, dst[0], dst[1], land + 0.06, 1.3 * k, "loi")
    if mine:
        v.tint((236, 230, 255), 0.22, 0.1, delay=land)
        v.at(land, lambda: (v.shake(0.5), v.hitstop(0.08)))
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - dst_lift, "loi", 16, 56))
    return land


# ------------------------------------------------------------------ Chiêu Thức II
def _c_ngu_kiem(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Ngự Kiếm Thuật: the flying sword leaves the hand along the line, pierces every monster on
    it (ngu_kiem_xuyen, its rings across the line, on each as it passes) and flies back."""
    ex = ex or {}
    hx, hy, lift, face = _hand(src, dst)
    end = ex.get("end") or (dst[0] + (dst[0] - src[0]) * 0.6, dst[1] + (dst[1] - src[1]) * 0.6)
    ux, uy, dist, deg = _unit((hx, hy), end)
    k = _k(t)
    speed = 240.0 + 6 * t
    out = max(0.12, dist / speed)
    v.spawn("ngu_kiem", hx, hy, charge, life=out, to=end, lift=lift, lift1=dst_lift, angle=deg, scale=0.85 * k,
            fade_in=0.03)
    back = max(0.12, min(0.45, dist / 340.0))
    v.spawn("ngu_kiem", end[0], end[1], charge + out, life=back, to=(src[0], src[1]), lift=dst_lift, lift1=lift,
            angle=deg + 180, scale=0.75 * k, fade_out=0.12, heavy=True)
    first = None
    for i, (x, y) in enumerate(_hits(ex, dst)):
        along = max(0.0, (x - hx) * ux + (y - hy) * uy)
        at = charge + along / speed
        first = at if first is None else min(first, at)
        v.spawn("ngu_kiem_xuyen", x, y, at, lift=dst_lift, angle=deg, scale=0.85 * k, peak=0.75)   # the body reads through
        if mine and i == 0:
            v.at(at, lambda: v.shake(0.16 + 0.02 * t))
    return first if first is not None else charge + out


def _c_van_kiem(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Vạn Kiếm Quy Tông: the sword compass opens on the ground (the telegraph), the ring of
    swords forms in the sky over it (van_kiem_troi) and rains down (van_kiem_roi; the swords
    land on its frames 1-6). Never turned; scaled with the area, but kept under the screen."""
    ex = ex or {}
    r = radius or 70.0
    s = max(0.9, min(1.4, r / 52.0)) * (1.0 + 0.02 * (t - 1))     # (a whole-area sigil would bury the fight)
    troi = art2.fx("van_kiem_troi")
    roi = art2.fx("van_kiem_roi")
    t_troi = troi.duration if troi is not None else 0.57
    t_roi = roi.duration if roi is not None else 0.63
    v.spawn("van_kiem_vong", dst[0], dst[1], charge * 0.4, life=charge * 0.6 + t_troi + t_roi + 0.25,
            layer="ground", scale=s, fade_in=0.15, fade_out=0.3, peak=0.65)
    v.spawn("van_kiem_troi", dst[0], dst[1], charge, scale=s)
    v.spawn("van_kiem_roi", dst[0], dst[1], charge + t_troi, scale=s)
    land = charge + t_troi + 2 / 16
    for i, (x, y) in enumerate(_hits(ex, dst)):
        v.spawn("hit_spark", x, y, land + 0.04 * i, lift=dst_lift, scale=0.8, peak=0.8)
    if mine:
        v.tint((255, 226, 140), 0.1, 0.4, delay=land)
        v.at(land, lambda: (v.shake(0.45), v.hitstop(0.06)))
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - 4, "kim", 18, 60))
    return land


def _c_bang_phong(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Băng Phong Thuật: ice bursts up round the target (bang_phong: frames 0-2 burst, 3-5 hold,
    6-7 shatter; the ring of spikes keeps the middle clear), then from its frame 5 every frozen
    monster wears bang_ket for the freeze."""
    ex = ex or {}
    k = _k(t)
    s = max(0.9, min(1.3, (radius or 50.0) / 42.0)) * k
    sh = art2.fx("bang_phong")
    fps = sh.fps if sh is not None else 14.0
    v.spawn("bang_phong", dst[0], dst[1], charge, scale=s)
    land = charge + 3 / fps
    hold = float(ex.get("d") or 4.0)
    for i, (x, y) in enumerate(_hits(ex, dst)):
        v.spawn("bang_ket", x, y, charge + 5 / fps + 0.03 * i, life=max(0.3, hold - 5 / fps), fade_in=0.08,
                fade_out=0.4)
    if mine:
        v.at(land, lambda: v.shake(0.2 + 0.02 * t))
        v.tint(RGB["thuy"], 0.05, 0.25, delay=land)
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - 6, "thuy", 10, 40))
    return land


def _c_loi_xich(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Chưởng Tâm Lôi: lightning from the palm to the first monster and on from monster to monster:
    one loi_xich per link (its pivot on A, turned to B, stretched to |B - A|), one link every
    70 ms, loi_cham on every monster it reaches."""
    ex = ex or {}
    hx, hy, lift, face = _hand(src, dst)
    pts = [(hx, hy, lift)] + [(x, y, dst_lift) for x, y in _hits(ex, dst)]
    sh = art2.fx("loi_xich")
    fw, fh = (sh.fw, sh.fh) if sh is not None else (96, 32)
    span = 89.0                                      # the segment's length in the sheet (pivot 3 -> 92)
    for i in range(len(pts) - 1):
        (ax, ay, al), (bx, by, bl) = pts[i], pts[i + 1]
        dx, dy = bx - ax, (by - bl) - (ay - al)
        d = math.hypot(dx, dy)
        deg = math.degrees(math.atan2(dy, dx))
        delay = charge + 0.07 * i
        w = max(8.0, d * z * fw / span)
        v.spawn("hit_spark", bx, by, delay + 0.05, lift=bl, scale=0.6, peak=0.7)      # the scorch it leaves
        v.spawn("loi_xich", ax, ay, delay, life=0.42, lift=al, angle=deg, size=(w, fh * (1.25 if i == 0 else 1.0)),
                fade_out=0.14, frames=(0, 3))
        v.spawn("loi_cham", bx, by, delay + 0.03, lift=bl, scale=_k(t))
    land = charge + 0.03
    if mine:
        v.at(land, lambda: v.shake(0.18 + 0.02 * t))
        v.tint(RGB["loi"], 0.04, 0.18, delay=land)
    return land


def _c_hoa_long(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Hỏa Long Thuật: the fire dragon surges from the caster along the line (mirrored, never
    upside down, when it flies left) and leaves hoa_long_vet - burning ground - every ~35 world
    px under its path, which burns as long as the server's strip (d) and fades."""
    ex = ex or {}
    hx, hy, lift, face = _hand(src, dst)
    end = ex.get("end") or (dst[0] + (dst[0] - src[0]) * 0.5, dst[1] + (dst[1] - src[1]) * 0.5)
    ux, uy, dist, deg = _unit((hx, hy), end)
    k = _k(t)
    speed = 200.0 + 6 * t
    travel = max(0.2, dist / speed)
    ang, flip = _aim(deg)
    hx, hy = hx + ux * 14, hy + uy * 14          # (its tail would lie over the caster)
    v.spawn("hoa_long", hx, hy, charge, life=travel, to=end, lift=lift + 2, lift1=lift + 2, angle=ang, flip=flip,
            scale=0.8 * k, fade_in=0.06, fade_out=0.14)
    burn = float(ex.get("d") or 2.0)
    fx_, fy_ = src
    gx, gy, gd, gdeg = _unit(src, end)
    step = 35.0
    n = max(1, int(gd / step))
    for i in range(n):
        a = step * (i + 0.5)
        v.spawn("hoa_long_vet", fx_ + gx * a, fy_ + gy * a + 1, charge + a / speed, life=burn + 0.3,
                layer="ground", angle=gdeg if abs(gdeg) <= 90 else gdeg - 180, fade_in=0.08, fade_out=0.6, peak=0.9)
    first = None
    for x, y in _hits(ex, dst):
        at = charge + max(0.0, (x - hx) * ux + (y - hy) * uy) / speed
        first = at if first is None else min(first, at)
        v.spawn("burst_hoa", x, y, at, lift=dst_lift, scale=(0.6 * k, 0.9 * k), start=2, peak=0.8, fade_out=0.1)
    land = first if first is not None else charge + travel
    if mine:
        v.at(land, lambda: v.shake(0.26 + 0.02 * t))
        v.tint(RGB["hoa"], 0.06, 0.3, delay=land)
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - dst_lift, "hoa", 12, 50))
    return land


def _c_dia_liet(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Địa Liệt Trảm: the fissure (dia_liet, ground) races out from the front foot along the aim,
    stretched to the line's length, and dia_liet_no erupts under each monster as its head passes."""
    ex = ex or {}
    end = ex.get("end") or (dst[0] + (dst[0] - src[0]) * 0.4, dst[1] + (dst[1] - src[1]) * 0.4)
    ux, uy, dist, deg = _unit(src, end)
    fx0, fy0 = src[0] + ux * 5, src[1] + uy * 5 + 1
    L = max(10.0, dist - 5)
    sh = art2.fx("dia_liet")
    reach = (112.0 if sh is None else sh.fw - 16) / z        # world px the crack covers in the sheet
    kx = max(0.8, min(2.4, L / reach))
    head = 0.25 * min(1.6, kx)                              # seconds the head takes to the end
    ang, flip = _aim(deg)
    if sh is not None:
        v.spawn("dia_liet", fx0, fy0, charge, layer="ground", size=(sh.fw * kx, sh.fh * (1.0 + 0.15 * min(kx, 2))),
                angle=ang, flip=flip, life=sh.duration + 0.5, fade_out=0.5)
    first = None
    for i, (x, y) in enumerate(_hits(ex, dst)):
        frac = max(0.0, min(1.0, ((x - fx0) * ux + (y - fy0) * uy) / L))
        at = charge + head * frac
        first = at if first is None else min(first, at)
        v.spawn("dia_liet_no", x, y + 1, at, scale=_k(t))
        if mine:
            v.at(at, lambda i=i: v.shake(0.14 if i == 0 else 0.06))
    land = first if first is not None else charge + head
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - 2, "tho", 8, 30))
    return land


def _c_thanh_dang(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Thanh Đằng Triền: vines grow up round the target (thanh_dang, frames 0-4) and from its
    frame 5 every held monster wears thanh_dang_troi for as long as it is held."""
    ex = ex or {}
    k = _k(t)
    sh = art2.fx("thanh_dang")
    fps = sh.fps if sh is not None else 12.0
    v.spawn("thanh_dang", dst[0], dst[1], charge, scale=k)
    hold = float(ex.get("d") or 3.0)
    for i, (x, y) in enumerate(_hits(ex, dst)):
        v.spawn("thanh_dang_troi", x, y, charge + 5 / fps + 0.04 * i, life=max(0.3, hold - 5 / fps), fade_in=0.08,
                fade_out=0.3)
    land = charge + 2 / fps
    if mine:
        v.at(land, lambda: v.shake(0.12))
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - 4, "moc", 8, 30))
    return land


def _c_phong_nhan(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Phong Nhận Thuật: a fan of wind blades (three, five from Nguyên Anh on) leaves the hand,
    ±12° apart; where a blade meets a monster a whirl (phong_xoay) spins up."""
    ex = ex or {}
    hx, hy, lift, face = _hand(src, dst)
    ux, uy, dist, deg = _unit((hx, hy), dst)
    n = 3 if t < 6 else 5
    speed = 260.0
    reach = dist + 26
    travel = max(0.12, reach / speed)
    for i in range(n):
        off = (i - (n - 1) / 2) * 12.0
        wx, wy = _turn(ux, uy, off)
        v.spawn("phong_nhan", hx, hy, charge + abs(off) * 0.002, life=travel, to=(hx + wx * reach, hy + wy * reach),
                lift=lift, lift1=dst_lift, angle=deg + off, scale=_k(t) * (1.0 if off == 0 else 0.85),
                fade_in=0.03, fade_out=0.08, heavy=off != 0)
    first = None
    for x, y in _hits(ex, dst):
        at = charge + math.hypot(x - hx, y - hy) / speed
        first = at if first is None else min(first, at)
        v.spawn("phong_xoay", x, y + 1, at, scale=_k(t))
    land = first if first is not None else charge + travel
    if mine:
        v.at(land, lambda: v.shake(0.12))
    return land


def _c_kim_chung(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Kim Chung Tráo: the golden bell drops over the caster (kim_chung), then stays round them,
    translucent (kim_chung_tru), for the shield's duration; bell_block rings it on a blocked hit."""
    ex = ex or {}
    x, y = src
    k = _k(t)
    sh = art2.fx("kim_chung")
    drop = sh.duration if sh is not None else 0.57
    v.spawn("kim_chung", x, y, charge, scale=k, follow=follow)
    hold = float(ex.get("d") or 6.0)
    v.spawn("kim_chung_tru", x, y, charge + drop - 0.05, life=max(0.3, hold - drop), scale=k, fade_in=0.06,
            fade_out=0.4, peak=0.85, follow=follow, tag=("bell", follow))
    land = charge + drop * 0.6
    if mine:
        v.at(land, lambda: v.shake(0.14))
        v.tint(RGB["kim"], 0.05, 0.25, delay=land)
    return land


def bell_block(v: Vfx, x: float, y: float, follow=None) -> None:
    """A hit taken while the golden bell is up: it rings."""
    v.spawn("kim_chung_vang", x, y, 0.0, follow=follow)


def _c_kiem_vuc(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Kiếm Vực: the sword domain opens round the caster - kiem_vuc on the ground (its circle
    marks the domain's reach) and the cage of orbiting swords (kiem_vuc_xoay) over them - and
    follows them for the domain's duration."""
    ex = ex or {}
    x, y = src
    r = radius or 60.0
    s = max(1.0, min(2.0, r / 30.0))
    hold = float(ex.get("d") or 6.0)
    v.spawn("kiem_vuc", x, y, charge, life=hold, layer="ground", scale=s, fade_in=0.12, fade_out=0.5, peak=0.65,
            follow=follow, tag=("domain", follow))
    v.spawn("kiem_vuc_xoay", x, y, charge, life=hold, scale=min(1.5, s * 0.8), fade_in=0.2, fade_out=0.5,
            follow=follow, tag=("domain", follow))
    if mine:
        v.tint((255, 226, 140), 0.06, 0.35, delay=charge)
        v.at(charge, lambda: v.shake(0.35))
    return charge


def _c_hoi_xuan(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift, ex=None) -> float:
    """Hồi Xuân Thuật: a spiral of spring rises from the healed one's feet; the heal number shows
    on its bloom (frame 4)."""
    x, y = src
    sh = art2.fx("hoi_xuan")
    fps = sh.fps if sh is not None else 12.0
    v.spawn("hoi_xuan", x, y, charge, scale=1.15 * _k(t), follow=follow)
    land = charge + 4 / fps
    if mine:
        v.tint(RGB["moc"], 0.06, 0.4, delay=land)
    if garnish is not None:
        v.at(land, lambda: garnish(x, y - CHEST, "moc", 10, 30))
    return land


RECIPES = {"chem": _c_chem, "kiem_khi": _c_kiem_khi, "hoa_cau": _c_hoa_cau, "tran_do": _c_tran_do,
           "ho_tran": _c_ho_tran, "thien_loi": _c_thien_loi, "ngu_kiem": _c_ngu_kiem, "van_kiem": _c_van_kiem,
           "bang_phong": _c_bang_phong, "loi_xich": _c_loi_xich, "hoa_long": _c_hoa_long, "dia_liet": _c_dia_liet,
           "thanh_dang": _c_thanh_dang, "phong_nhan": _c_phong_nhan, "kim_chung": _c_kim_chung,
           "kiem_vuc": _c_kiem_vuc, "hoi_xuan": _c_hoi_xuan}


def fizzle(v: Vfx, fx_id: str, src, dst, follow=None) -> None:
    """Chiêu hụt: the channel dies (its circle goes out) and a grey puff where it gave up.
    The grey code-drawn fizzle of client/art/skill_fx.py stays the picture of the miss."""
    v.kill(("chan", follow))
    x, y = (dst if dst is not None and fx_id not in SELF_CAST else src)
    mx, my = (src[0] + x) / 2, (src[1] + y) / 2
    v.spawn("dust_step", mx, my + 2, 0.4, scale=0.8, peak=0.7)


# ------------------------------------------------------------------ hits, deaths, parries
def crit(v: Vfx, x: float, y: float, lift: float, mine: bool) -> None:
    """A critical hit: a bigger star, a gold ring, a short hit-stop and a kick of the camera."""
    v.spawn("hit_crit", x, y, 0.0, lift=lift, scale=(0.95, 0.75), peak=0.8)
    if mine:
        v.hitstop(0.05)
        v.shake(0.22)


def death(v: Vfx, x: float, y: float, lift: float, body=None, after: float = 0.5, mine: bool = False) -> None:
    """A monster goes down: a burst at its chest now; when its die clip ends, its last frame
    turns to light, rises and fades (`body` = (frame, white frame, pivot))."""
    v.spawn("burst_kim", x, y, 0.0, lift=lift, scale=(0.8, 1.4), start=2, peak=0.8, fade_out=0.1)
    v.spawn("hit_spark", x, y, 0.0, lift=lift + 4, scale=1.0)
    if body is not None:
        img, white, pivot = body
        v.sprite(img, pivot, x, y, delay=after, life=0.55, to=(x, y), lift=0, lift1=5, fade_out=0.55)
        v.sprite(white, pivot, x, y, delay=after, life=0.5, additive=True, to=(x, y), lift=0, lift1=10, peak=0.55,
                 fade_in=0.1, fade_out=0.35, heavy=True)
        v.spawn("burst_kim", x, y, after + 0.1, lift=lift * 0.6, scale=(0.5, 1.1), peak=0.5, fade_out=0.2, heavy=True)
    if mine:
        v.hitstop(0.06)
        v.shake(0.16)


def recoil(e_pos, by_pos, now: float, strength: float = 3.0):
    """(dx, dy, t0, strength) that pushes a struck body away from the striker for a moment."""
    ux, uy, d, _ = _unit(by_pos, e_pos)
    return (ux, uy, now, strength)


def recoil_offset(kick, now: float) -> tuple[float, float]:
    """World px offset of a recoil `kick` now (a quick shove out, eased back in 0.18 s)."""
    if not kick:
        return 0.0, 0.0
    ux, uy, t0, strength = kick
    t = now - t0
    if t < 0 or t > 0.18:
        return 0.0, 0.0
    k = (t / 0.04) if t < 0.04 else (1 - (t - 0.04) / 0.14)
    return ux * strength * k, uy * strength * k


def parry(v: Vfx, mx: float, my: float, px: float, py: float, t: int, weapon: str | None, mine: bool,
          m_lift: float = 12.0, garnish=None) -> float:
    """Phản Đòn - a right answer under pressure turns the blow back. The clash flashes gold and
    blue, the world holds its breath (the longest hit-stop), a ring of force runs out over the
    ground, and the player's own kiếm khí of their tier answers into the monster."""
    cx, cy = (mx + px) / 2, (my + py) / 2
    # the clash: a compact core (the world freezes on it), then rings running out of it
    v.spawn("parry", cx, cy, 0.0, lift=CHEST + 2, scale=(0.8, 1.0), start=1, shade=0.35)
    v.spawn("hit_crit", cx, cy, 0.0, lift=CHEST + 2, scale=(0.6, 0.45), peak=0.7)
    v.spawn("parry", cx, cy, 0.08, lift=CHEST + 2, scale=(1.2, 2.0), start=3, peak=0.45, fade_out=0.12, heavy=True,
            shade=0.3)
    _ground_ring(v, px, py, 0.04, 1.4, "kim")
    # the riposte: the player's own sword qi, at their tier, from them into the monster
    land = swing(v, weapon, max(2, t), (px, py), (mx, my), strike=0.14, dst_lift=m_lift, mine=mine, garnish=garnish)
    if mine:
        v.hitstop(0.1)
        v.shake(0.38)
        v.tint((255, 226, 140), 0.12, 0.3)
    if garnish is not None:
        garnish(cx, cy - CHEST, "kim", 18, 60)
    return land


def dodge(v: Vfx, x: float, y: float, dx: float, dy: float, follow=None) -> None:
    """Né Đòn starts: a puff where the feet left, streaks along the way."""
    v.spawn("dust_step", x, y + 1, 0.0, scale=0.9)
    d = math.hypot(dx, dy) or 1.0
    ux, uy = dx / d, dy / d
    ang = math.degrees(math.atan2(uy, ux))
    # the streaks trail behind the body (the sheet's streaks run to its right edge)
    v.spawn("dash_trail", x - ux * 12, y - uy * 12, 0.03, lift=CHEST, angle=ang, scale=1.0, peak=0.8,
            follow=follow)


def dodged(v: Vfx, x: float, y: float, mine: bool) -> None:
    """The blow went through empty air: a cool ring where it would have landed, a breath of time."""
    v.spawn("parry", x, y, 0.0, lift=CHEST, scale=(0.9, 1.7), start=2, peak=0.6, fade_out=0.15)
    if mine:
        v.hitstop(0.05)
        v.tint((160, 220, 255), 0.14, 0.3)


def uy_ap(v: Vfx, x: float, y: float, k: float = 1.0) -> None:
    """Uy áp: the pressure of a cultivator's realm runs out over the ground (a Phản Đòn kill)."""
    _shockwave(v, x, y, 0.05, 1.6 * k, "kim")


def struck(v: Vfx, x: float, y: float, heavy: bool) -> None:
    """The player is hit (a Mặc Kích when `heavy`): the camera takes it."""
    v.shake(0.45 if heavy else 0.25)


# ------------------------------------------------------------------ progress
def stage_up(v: Vfx, x: float, y: float, follow=None) -> None:
    """A stage of the realm climbed: the golden ring of thang_cap rises round the player."""
    v.spawn("thang_cap", x, y, 0.0, follow=follow, scale=1.1)
    v.spawn("heal", x, y, 0.15, life=0.9, lift=CHEST, follow=follow, peak=0.7,
            fade_out=0.4, heavy=True)
    v.tint((255, 226, 140), 0.12, 0.4)


def breakthrough(v: Vfx, x: float, y: float, follow=None, garnish=None) -> None:
    """A realm broken through: heaven's tribulation strikes, the qi collapses inward (dot_pha),
    then bursts out over the ground."""
    v.tint((30, 20, 60), 0.3, 1.0)
    v.spawn("loi_kiep", x, y, 0.0, scale=1.3, follow=follow)
    v.spawn("loi_kiep", x - 16, y + 2, 0.25, scale=1.0, peak=0.8, follow=follow, heavy=True)
    v.spawn("dot_pha", x, y, 0.15, scale=1.4, follow=follow)
    v.spawn("crack_ground", x, y + 1, 0.15, life=1.6, scale=0.8, fade_out=0.8, layer="ground")
    _shockwave(v, x, y, 0.75, 2.0, "tho")
    v.at(0.75, lambda: (v.shake(0.5), v.tint((255, 240, 190), 0.28, 0.4)))
    if garnish is not None:
        v.at(0.75, lambda: garnish(x, y - CHEST, "tho", 24, 60))
