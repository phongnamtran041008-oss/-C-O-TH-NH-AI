"""What a fight looks like: kiếm khí that grows with tu vi, the attacks of every weapon family, the
six chiêu thức, hits, deaths, Phản Đòn, Né Đòn, stage-ups and breakthroughs - as recipes over
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


# ------------------------------------------------------------------ basic attacks
def swing(v: Vfx, weapon: str | None, t: int, src, dst, strike: float = 0.2, dst_lift: float = 10.0,
          follow=None, mine: bool = True, z: float = 2.0, garnish=None) -> float:
    """One basic attack of tier `t` with `weapon` from `src` (the attacker's feet) at `dst` (the
    target's feet), its strike frame `strike` seconds from now. Returns when it lands."""
    fam = family(weapon)
    t = max(1, min(10, int(t)))
    fn = {"blade": _blade, "thrust": _thrust, "smash": _smash, "shot": _shot, "spell": _spell}[fam]
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
# every chiêu: charge (qi gathers, a rune circle under the feet) -> release -> travel with a
# trail -> impact with weight -> a short linger; the tier makes it bigger and adds layers
CHIEU_EL = {"chem": "tho", "kiem_khi": "kim", "hoa_cau": "hoa", "tran_do": "moc", "ho_tran": "thuy",
            "thien_loi": "loi"}
CHIEU_CIRCLE = {"chem": "tran_1", "kiem_khi": "tran_5", "hoa_cau": "tran_4", "tran_do": "tran_3",
                "ho_tran": "tran_2", "thien_loi": "tran_8"}
CHARGE = {"chem": 0.12, "kiem_khi": 0.3, "hoa_cau": 0.36, "tran_do": 0.34, "ho_tran": 0.3, "thien_loi": 0.5}


def channel(v: Vfx, fx_id: str, follow, x: float, y: float, t: int = 1) -> None:
    """A chiêu being channelled (its question is open): the rune circle under the caster and qi
    streaming in, until `v.kill(("chan", follow))`."""
    tag = ("chan", follow)
    v.kill(tag)
    circle = CHIEU_CIRCLE.get(fx_id, "tran_1")
    k = 0.42 + 0.03 * t
    v.spawn(circle, x, y, life=60.0, layer="ground", scale=(k * 0.5, k), fade_in=0.25, peak=0.85, follow=follow,
            tag=tag)
    el = CHIEU_EL.get(fx_id, "kim")
    state = {"i": 0}

    def gather():
        i = state["i"] = state["i"] + 1
        ang = (i * 137.5) % 360
        ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d = 26 + (i % 3) * 5
        v.spawn("sword_trail", x + ux * d, y + uy * d * 0.6, life=0.3, to=(x, y), lift=CHEST + 6, lift1=CHEST,
                ease="in", angle=ang + 180, scale=0.42, peak=0.7, fade_in=0.08, follow=follow, tag=tag, heavy=True)
        if i % 2 == 0:
            v.spawn("bolt_" + el, x, y, life=0.3, lift=CHEST, scale=(0.2, 0.45), peak=0.5, fade_out=0.2,
                    follow=follow, tag=tag, heavy=True)
    v.emit(tag, 0.11, gather, 60.0)


def chieu(v: Vfx, fx_id: str, src, dst, t: int = 1, radius: float = 0.0, charged: bool = False,
          follow=None, mine: bool = True, z: float = 2.0, garnish=None, dst_lift: float = 10.0) -> float:
    """A landed chiêu thức from `src` (the caster's feet) at `dst` (the target's feet; None for a
    ward). `charged`: its channel was already shown (a bí cảnh question), so the charge is short.
    Returns the seconds until it lands on the target."""
    t = max(1, min(10, int(t)))
    v.kill(("chan", follow))
    if dst is None:
        dst = (src[0] + 14, src[1])
    charge = 0.1 if charged else CHARGE.get(fx_id, 0.3)
    if fx_id != "chem" and fx_id != "ho_tran":
        k = 0.42 + 0.03 * t
        v.spawn(CHIEU_CIRCLE.get(fx_id, "tran_1"), src[0], src[1], life=charge + 0.45, layer="ground",
                scale=(k * (0.9 if charged else 0.4), k), fade_in=0.08, fade_out=0.3, peak=0.85, follow=follow)
    fn = {"chem": _c_chem, "kiem_khi": _c_kiem_khi, "hoa_cau": _c_hoa_cau, "tran_do": _c_tran_do,
          "ho_tran": _c_ho_tran, "thien_loi": _c_thien_loi}.get(fx_id, _c_chem)
    return fn(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift)


def _gather(v, x, y, el, charge, follow, n=6) -> None:
    """Qi streaming into the caster during the charge."""
    for i in range(n):
        ang = i * (360.0 / n) + 20
        ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        v.spawn("sword_trail", x + ux * 30, y + uy * 18, i * charge / (n + 2), life=max(0.12, charge * 0.6),
                to=(x, y), lift=CHEST + 8, lift1=CHEST, ease="in", angle=ang + 180, scale=0.44, peak=0.75,
                follow=follow, heavy=i % 2 == 1)


def _c_chem(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift) -> float:
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


def _c_kiem_khi(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift) -> float:
    """Phá Mê Kiếm Quyết: white-gold crescents of sword qi fly from the blade and cross on the
    target (three from Nguyên Anh on)."""
    ux, uy, dist, deg = _unit(src, dst)
    _gather(v, src[0], src[1], "kim", charge, follow)
    k = 1.0 + 0.06 * (t - 1)
    v.spawn("slash_kim", src[0] + ux * REACH, src[1] + uy * REACH, charge, lift=CHEST, scale=1.3 * k,
            angle=deg - CREST, follow=follow)
    n = 1 if t < 4 else (2 if t < 6 else 3)
    speed = 260.0 + 10 * t
    sx, sy = src[0] + ux * 12, src[1] + uy * 12
    span = max(8.0, dist - 12)
    travel = max(0.1, min(0.45, (span + 18) / speed))
    land = charge + 0.03 + travel * span / (span + 18)
    offs = [0.0] if n == 1 else ([-8.0, 8.0] if n == 2 else [-14.0, 0.0, 14.0])
    for i, off in enumerate(offs):
        wx, wy = _turn(ux, uy, off)
        ex, ey = sx + wx * (span + 18), sy + wy * (span + 18)
        d0 = charge + 0.03 + i * 0.04
        v.spawn("slash_kim", sx, sy, d0, life=travel, to=(ex, ey), lift=CHEST, lift1=dst_lift, ease="out",
                angle=deg + off - CREST, scale=1.05 * k, frames=(1, 2), trail=(4, 0.02), fade_out=0.1,
                heavy=i > 0 and n == 3)
        v.spawn("sword_trail", sx, sy, d0, life=travel, to=(ex, ey), lift=CHEST, lift1=dst_lift, ease="out",
                angle=deg + off, scale=0.9 * k, peak=0.8, fade_out=travel * 0.4, heavy=True)
    v.spawn("slash_kim", dst[0], dst[1], land, lift=dst_lift, scale=1.25 * k, angle=deg + 90 - CREST)
    v.spawn("burst_kim", dst[0], dst[1], land + 0.03, lift=dst_lift, scale=0.95 * k, fade_out=0.12)
    v.spawn("hit_spark", dst[0], dst[1], land + 0.05, lift=dst_lift, scale=1.1)
    if t >= 4:
        _scar(v, t, dst[0], dst[1], deg, land, z)
    if mine:
        v.at(land, lambda: v.shake(0.18 + 0.03 * t))
    return land


def _c_hoa_cau(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift) -> float:
    """Hỏa Cầu Thuật: a fireball swells in the hand, arcs over with a tail of fire and bursts."""
    ux, uy, dist, deg = _unit(src, dst)
    k = 1.0 + 0.07 * (t - 1)
    hx, hy = src[0] + ux * 7, src[1] + uy * 7
    v.spawn("bolt_hoa", hx, hy, 0.0, life=charge, lift=CHEST + 2, scale=(0.25 * k, 1.0 * k), angle=deg,
            follow=follow)
    _gather(v, src[0], src[1], "hoa", charge, follow, n=4)
    speed = 170.0 + 8 * t
    travel = max(0.16, min(0.6, dist / speed))
    land = charge + travel
    v.spawn("bolt_hoa", hx, hy, charge, life=travel, to=(dst[0], dst[1]), lift=CHEST + 2, lift1=dst_lift,
            arc=10 + dist * 0.12, angle=deg, scale=1.05 * k, trail=(5, 0.028))
    if t >= 6:   # a second, smaller fireball close behind
        v.spawn("bolt_hoa", hx, hy, charge + 0.08, life=travel, to=(dst[0], dst[1]), lift=CHEST + 2,
                lift1=dst_lift, arc=4, angle=deg, scale=0.7 * k, trail=(3, 0.03), heavy=True)
    v.spawn("burst_hoa", dst[0], dst[1], land, lift=dst_lift, scale=(1.2 * k, 1.7 * k), fade_out=0.12)
    v.spawn("hit_crit", dst[0], dst[1], land + 0.02, lift=dst_lift, scale=0.9 * k, peak=0.85)
    v.spawn("burst_hoa", dst[0], dst[1], land + 0.12, lift=dst_lift - 2, scale=(1.6 * k, 2.3 * k), peak=0.5,
            fade_out=0.2, heavy=True)
    v.spawn("crack_ground", dst[0], dst[1] + 1, land, life=1.2, scale=0.5 * k, fade_out=0.7, layer="ground")
    v.spawn("dust_step", dst[0], dst[1] + 3, land + 0.2, scale=0.8 * k, peak=0.45, heavy=True)
    if mine:
        v.at(land, lambda: v.shake(0.24 + 0.03 * t))
        v.tint(RGB["hoa"], 0.07, 0.2, delay=land)
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - dst_lift, "hoa", 12, 50))
    return land


def _c_tran_do(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift) -> float:
    """Ngũ Hành Trận: the array opens on the ground round the target, then its five marks erupt
    one after another in the five colours and the centre bursts."""
    r = radius or 60.0
    k = 1.0 + 0.04 * (t - 1)
    _gather(v, src[0], src[1], "moc", charge, follow, n=5)
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
        v.tint(RGB["moc"], 0.06, 0.25, delay=land)
    return land


def _c_ho_tran(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift) -> float:
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
    v.spawn("burst_thuy", x, y, charge, lift=CHEST, scale=(0.8, 2.2 * k), start=2, peak=0.6, fade_out=0.2, heavy=True)
    _shockwave(v, x, y, charge + 0.04, r / 45.0, "thuy")
    if mine:
        v.tint(RGB["thuy"], 0.06, 0.3, delay=charge)
    return charge


def _c_thien_loi(v, t, src, dst, charge, radius, follow, mine, z, garnish, dst_lift) -> float:
    """Thiên Lôi Tuyệt Kỹ: the sky darkens while the caster calls, then purple lightning pillars
    come down on the target, the ground cracks and the screen goes white for a blink."""
    ux, uy, dist, deg = _unit(src, dst)
    k = 1.0 + 0.05 * (t - 1)
    v.spawn("bolt_loi", src[0] + ux * 4, src[1], 0.0, life=charge, lift=CHEST + 14, scale=(0.3, 0.9 * k),
            follow=follow)
    _gather(v, src[0], src[1], "loi", charge, follow, n=8)
    if mine:
        v.tint((40, 24, 80), 0.22, charge + 0.5)
    land = charge + 0.08
    if has("sword_trail"):      # the release: a bolt of qi thrown up into the clouds
        v.spawn("sword_trail", src[0], src[1], charge - 0.06, life=0.16, to=(src[0] + 4, src[1]), lift=CHEST + 10,
                lift1=CHEST + 90, angle=-86, size=(90, 22), ease="in", peak=0.9)
    v.spawn("slash_loi", src[0] + ux * 6, src[1], charge - 0.08, lift=CHEST + 8, scale=0.9 * k, angle=-90 - CREST,
            peak=0.8, follow=follow)
    v.spawn("loi_kiep", dst[0], dst[1], charge, scale=1.5 * k)
    v.spawn("loi_kiep", dst[0] - 14, dst[1] + 3, charge + 0.12, scale=1.1 * k, peak=0.85)
    if t >= 6:
        v.spawn("loi_kiep", dst[0] + 15, dst[1] - 2, charge + 0.2, scale=1.0 * k, peak=0.8, heavy=True)
    v.spawn("burst_loi", dst[0], dst[1], land, lift=dst_lift, scale=(1.4 * k, 2.0 * k), fade_out=0.12)
    v.spawn("hit_crit", dst[0], dst[1], land + 0.02, lift=dst_lift, scale=1.1 * k, peak=0.8)
    v.spawn("crack_ground", dst[0], dst[1] + 1, land, life=1.5, scale=0.75 * k, fade_out=0.8, layer="ground")
    _shockwave(v, dst[0], dst[1], land + 0.06, 1.4 * k, "loi")
    if mine:
        v.tint((236, 230, 255), 0.24, 0.1, delay=land)
        v.at(land, lambda: (v.shake(0.5), v.hitstop(0.08)))
    if garnish is not None:
        v.at(land, lambda: garnish(dst[0], dst[1] - dst_lift, "loi", 16, 56))
    return land


def fizzle(v: Vfx, fx_id: str, src, dst, follow=None) -> None:
    """Chiêu hụt: the channel dies (its circle goes out) and a grey puff where it gave up.
    The grey code-drawn fizzle of client/art/skill_fx.py stays the picture of the miss."""
    v.kill(("chan", follow))
    x, y = (dst if dst is not None and fx_id not in ("ho_tran",) else src)
    mx, my = (src[0] + x) / 2, (src[1] + y) / 2
    v.spawn("dust_step", mx, my + 2, 0.4, scale=0.8, peak=0.7)


# ------------------------------------------------------------------ hits, deaths, parries
def crit(v: Vfx, x: float, y: float, lift: float, mine: bool) -> None:
    """A critical hit: a bigger star, a gold ring, a short hit-stop and a kick of the camera."""
    v.spawn("hit_crit", x, y, 0.0, lift=lift, scale=(1.3, 1.0))
    v.spawn("burst_kim", x, y, 0.02, lift=lift, scale=(0.7, 1.3), peak=0.7, fade_out=0.12, heavy=True)
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
    v.spawn("parry", cx, cy, 0.0, lift=CHEST + 2, scale=(1.05, 1.35))
    v.spawn("hit_crit", cx, cy, 0.0, lift=CHEST + 2, scale=(0.8, 0.6), peak=0.85)
    v.spawn("parry", cx, cy, 0.08, lift=CHEST + 2, scale=(1.5, 2.6), start=3, peak=0.6, fade_out=0.12, heavy=True)
    v.spawn("burst_kim", cx, cy, 0.05, lift=CHEST + 2, scale=(1.0, 2.0), start=3, peak=0.8, fade_out=0.1)
    _shockwave(v, px, py, 0.04, 1.4, "kim")
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
