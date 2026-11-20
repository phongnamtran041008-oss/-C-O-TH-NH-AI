"""Thần thông of Luyện Khí (world_plan.json `unlocks`, wired section 'abilities'): what a stage of
Đạo Thụ opens out in the world. Every number is read from the unlock's own block in the plan.

* **Bày pháp trận** (phap_tran, `formation`): a circle laid on the ground at the feet for some
  seconds. A monster standing in it when it starts a blow winds it up `windup_mult` times
  slower (combat._monster_tick), so there is more time to step out or to get ready to answer.
* **Đạp Kiếm Lướt** (dap_kiem_luot, `glide`): a short glide on the sword over water and chasms
  (realtime/glide.py has the geometry). It rides in the movement stream under its own sequence
  number, like Né Đòn, and is checked again when the server reaches it there: from where the
  player really stands, the path may cross only free ground and the tiles the plan names, and
  the landing must be walkable - else it is refused and nothing moves.
* **Cưỡi linh thú** (cuoi_linh_thu, `ride`): riding the worn beast whose gift is a mount (Tiểu
  Long). The server moves a rider at `speed_mult` times the walking speed; a client cannot ask
  for more, it only sends the keys it holds (zone.ChannelZone._move_players). Mounting and
  dismounting ride in the movement stream too, so the client predicts the same speed change at
  the same step.
* **Thu phục linh thú** (thu_phuc_linh_thu): sealing a beast that yielded (realtime/beasts.py).
* **Ngự kiếm** (`flight`, two rungs): standing on the sword and flying under the player's own
  keys. The low rung comes with Đạp Kiếm Lướt (Luyện Khí tầng 6): `speed_mult` times the walking
  speed for as long as a gauge of `gauge_seconds` lasts (it refills on the ground in
  `refill_seconds`; a worn Kim Sí Điểu lengthens it, a linh căn with glide_cd refills it
  faster). The high rung, Ngự Kiếm Phi Hành (Trúc Cơ), has no gauge and is faster and higher.
  Taking off and landing ride in the movement stream like the glide; every airborne step is
  checked like a walking one, with glide.fly_step (over free ground, water and chasms, never a
  wall, a tree or a house). A landing must be on walkable ground; when the gauge runs dry over
  water the server carries the flyer back to the last ground it passed. In the air nobody
  attacks, casts, dodges, rides or seals, and a monster's blow on the ground misses - once the
  rise of `rise_ms` is over (struck while rising, the player is knocked off the sword). No
  take-off with a question open, nor within `hit_lock_seconds` of being struck.

An ability is open when its unlock says 'co' and the player's place in Đạo Thụ (the TreePos kept
on the session, lands.py) reaches its realm and stage. Nothing here works in a bí cảnh.
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ..learning import math_tree

if TYPE_CHECKING:
    from .zone import ChannelZone, Player

GLIDE, RIDE, FORMATION, SEAL = "dap_kiem_luot", "cuoi_linh_thu", "phap_tran", "thu_phuc_linh_thu"
SOAR = "ngu_kiem_phi_hanh"                    # the high rung of flight (the low one is GLIDE's)
FLIGHT_RUNGS = (GLIDE, SOAR)                  # flight level 1 and 2

REFUSALS_VI = {
    "fly_locked": "Ngự kiếm mở ở Luyện Khí tầng 6 trên Đạo Thụ.",
    "riding": "Xuống linh thú trước rồi hãy ngự kiếm.",
    "flying": "Đang ngự kiếm trên không: hạ kiếm xuống đã.",
    "struck": "Vừa trúng đòn, chưa kịp đạp kiếm bay lên.",
    "gauge_low": "Kiếm khí chưa hồi đủ để bay.",
    "no_landing": "Dưới chân không có chỗ đáp: bay tới đất liền đã.",
    "cannot": "Lúc này không dùng được.",
    "answering": "Con đang trả lời câu hỏi.",
    "cooldown": "Chưa hồi xong.",
    "glide_locked": "Đạp Kiếm Lướt mở ở Luyện Khí tầng 6 trên Đạo Thụ.",
    "ride_locked": "Cưỡi linh thú mở ở Luyện Khí tầng 8 trên Đạo Thụ.",
    "formation_locked": "Bày pháp trận mở ở Luyện Khí tầng 5 trên Đạo Thụ.",
    "no_mount": "Cần đeo một linh thú cưỡi được (Tiểu Long).",
    "too_far": "Kiếm không lướt xa được tới vậy.",
    "too_short": "Quãng lướt quá ngắn.",
    "bad_landing": "Chỗ ấy không đặt chân được.",
    "blocked": "Có vật cản trên đường lướt: kiếm chỉ lướt qua vực và mặt nước.",
}


def wired() -> bool:
    return math_tree.section_wired("abilities")


def unlock(uid: str) -> dict:
    return next((u for u in math_tree.world_plan().get("unlocks", []) if u["id"] == uid), {})


def glide_cfg() -> dict:
    return unlock(GLIDE).get("glide", {})


def glide_max_px(p: "Player | None") -> float:
    """How far this player's Đạp Kiếm Lướt flies: the plan's max_px, farther with the worn
    Kim Sí Điểu (gift glide_range)."""
    from ..systems import beasts
    return float(glide_cfg().get("max_px", 80)) * (1 + beasts.gift_value(getattr(p, "pet", None), "glide_range"))


def formation_cfg() -> dict:
    return unlock(FORMATION).get("formation", {})


def ride_cfg() -> dict:
    return unlock(RIDE).get("ride", {})


def pos_of(p: "Player"):
    s = p.session
    return getattr(s, "tree", None) if s is not None else None


def is_open(p: "Player", uid: str) -> bool:
    """Is this ability open to the player now (status 'co', the stage of Đạo Thụ reached)?"""
    from ..systems import weapons
    if not wired():
        return False
    pos = pos_of(p)
    return pos is not None and weapons.unlock_open(uid, (pos.realm, pos.stage))


def _usable(p: "Player | None") -> bool:
    ch = p.channel if p is not None else None
    return ch is not None and not ch.instance and not p.dead and not p.ghost


def _busy(p: "Player", now: float) -> bool:
    return p.protected(now) or p.q_pending or p.question is not None


# ------------------------------------------------------------------ riding
def mount_mult(p: "Player") -> float:
    """How much faster the worn beast carries its rider (its gift), 0 when it is no mount."""
    from ..systems import beasts
    return beasts.gift_value(getattr(p, "pet", None), ride_cfg().get("gift", "mount"), "speed_mult")


def ride_mult(p: "Player") -> float:
    """The walking speed multiplier of this player right now."""
    if not p.riding or p.channel is None or p.channel.instance:
        return 1.0
    m = mount_mult(p)
    return m if m > 0 else 1.0


def request_ride(p: "Player | None", seq: int, on: bool, now: float) -> str | None:
    """Mount (on) or get down. A refusal code, or None: the change is queued in the movement
    stream and happens when the server reaches it there."""
    if p is None or p.channel is None:
        return "cannot"
    code = None
    if on:
        if not _usable(p):
            code = "cannot"
        elif p.fly:
            code = "flying"
        elif not is_open(p, RIDE):
            code = "ride_locked"
        elif mount_mult(p) <= 0:
            code = "no_mount"
    if not p.channel.queue_special(p, seq, ("ride", bool(on and code is None))):
        return "cannot"
    return code


def apply_ride(ch: "ChannelZone", p: "Player", on: bool) -> None:
    if bool(p.riding) == bool(on) or (on and p.fly):
        return
    p.riding = bool(on)
    for other in ch.players.values():        # everyone who sees this player gets them again, mounted
        other.known.pop(p.eid, None)
    ch.event(k="ride", id=p.eid, on=int(p.riding), x=round(p.x, 1), y=round(p.y, 1))
    if p.session is not None:
        p.session.send({"t": "ride", "ok": True, "on": p.riding, "mult": ride_mult(p)})


# ------------------------------------------------------------------ the glide
def request_glide(p: "Player | None", seq: int, x: float, y: float, now: float) -> str | None:
    """Đạp Kiếm Lướt to (x, y). A refusal code, or None: the glide is queued in the movement
    stream (a refused one still takes its sequence number there, empty)."""
    if p is None or p.channel is None:
        return "cannot"
    code = None
    if not _usable(p):
        code = "cannot"
    elif _busy(p, now):
        code = "answering"
    elif p.fly:
        code = "flying"
    elif not is_open(p, GLIDE):
        code = "glide_locked"
    elif now < p.glide_ready:
        code = "cooldown"
    if not p.channel.queue_special(p, seq, None if code else ("glide", float(x), float(y))):
        return "cannot"
    if code is None:
        p.glide_ready = now + glide_cooldown(p)
    return code


def glide_cooldown(p: "Player") -> float:
    """Đạp Kiếm Lướt's cooldown, less the linh căn's glide_cd."""
    from ..systems import linh_can
    return float(glide_cfg().get("cooldown_seconds", 2.5)) * (1 - linh_can.fx(p, "glide_cd"))


def check_glide(ch: "ChannelZone", x0: float, y0: float, x1: float, y1: float,
                max_px: float | None = None) -> str | None:
    from . import glide
    c = glide_cfg()
    reach = float(c.get("max_px", 80)) if max_px is None else max_px
    return glide.check(ch.map.collider, ch.map.tile_name, set(c.get("over_tiles", [])), x0, y0, x1, y1,
                       reach, float(c.get("min_px", 0)))


def apply_glide(ch: "ChannelZone", p: "Player", x: float, y: float) -> str | None:
    """Reached in the movement stream: glide from where the player stands now, or refuse."""
    code = "flying" if p.fly else check_glide(ch, p.x, p.y, x, y, glide_max_px(p))
    if code is not None:
        if p.session is not None:
            p.session.send({"t": "glide", "ok": False, "code": code, "message_vi": REFUSALS_VI[code],
                            "x": round(p.x, 2), "y": round(p.y, 2)})
        return code
    x0, y0 = p.x, p.y
    dx, dy = x - x0, y - y0
    if abs(dx) > abs(dy):
        p.facing = "right" if dx > 0 else "left"
    elif dy:
        p.facing = "down" if dy > 0 else "up"
    p.x, p.y = x, y
    p.ground = (x, y)
    p.dirty = True
    p.moved_this_tick = True
    ms = float(glide_cfg().get("ms", 450))
    ch.event(k="glide", id=p.eid, x0=round(x0, 1), y0=round(y0, 1), x=round(x, 1), y=round(y, 1), ms=ms)
    if p.session is not None:
        p.session.send({"t": "glide", "ok": True, "x": round(x, 2), "y": round(y, 2), "ms": ms})
    return None


def apply_special(ch: "ChannelZone", p: "Player", action, now: float = 0.0) -> None:
    """An entry of the movement stream that is no walking (zone._move_players)."""
    if not action:
        return
    if action[0] == "glide":
        apply_glide(ch, p, action[1], action[2])
    elif action[0] == "ride":
        apply_ride(ch, p, action[1])
    elif action[0] == "fly":
        apply_fly(ch, p, action[1], now)


def speed_mult(p: "Player") -> float:
    """How much faster than walking the movement stream moves this player now: the sword's
    speed in the air, the mount's on its back, 1 on foot."""
    if p.fly:
        return float(flight_cfg(p.fly).get("speed_mult", 1.0))
    return ride_mult(p)


# ------------------------------------------------------------------ ngự kiếm (flight)
def flight_cfg(level: int) -> dict:
    """The `flight` block of rung `level` (1 Đạp Kiếm Lướt, 2 Ngự Kiếm Phi Hành), {} for 0."""
    if not 1 <= level <= len(FLIGHT_RUNGS):
        return {}
    return unlock(FLIGHT_RUNGS[level - 1]).get("flight", {})


def fly_over(level: int) -> set:
    """The ground tiles a flyer of this rung passes over (water, chasms of ink)."""
    return set(flight_cfg(level).get("over_tiles", []))


def fly_level(p: "Player") -> int:
    """The rung of flight open to this player: 2 free flight, 1 low flight, 0 none."""
    for level in range(len(FLIGHT_RUNGS), 0, -1):
        if flight_cfg(level) and is_open(p, FLIGHT_RUNGS[level - 1]):
            return level
    return 0


def sword_sheet(realm: str | None) -> str:
    """The flying sword drawn under a flyer of this realm: the last of the plan's `swords` whose
    realm the player has reached (phi_kiem_1 for Luyện Khí and Trúc Cơ, brighter ones later)."""
    swords = flight_cfg(1).get("swords") or [{"from": "luyen_khi", "sheet": glide_cfg().get("sheet", "phi_kiem_1")}]
    order = math_tree.tree().realm_order
    have = order.get(realm or "", 0)
    best = swords[0]["sheet"]
    for s in swords:
        if order.get(s.get("from"), 99) <= have:
            best = s["sheet"]
    return best


def gauge_max(p: "Player") -> float:
    """Seconds of low flight on a full gauge: the plan's, longer with the worn Kim Sí Điểu
    (its glide_range gift, which also lengthens the glide)."""
    from ..systems import beasts
    return float(flight_cfg(1).get("gauge_seconds", 0)) * (1 + beasts.gift_value(getattr(p, "pet", None), "glide_range"))


def refill_seconds(p: "Player") -> float:
    """Seconds an empty gauge takes to fill on the ground, shorter with a linh căn of glide_cd."""
    from ..systems import linh_can
    return max(0.1, float(flight_cfg(1).get("refill_seconds", 1)) * (1 - linh_can.fx(p, "glide_cd")))


def gauge(p: "Player") -> float:
    """Seconds of low flight left now (a gauge never seen yet is full)."""
    if p.fly_gauge < 0:
        p.fly_gauge = gauge_max(p)
    return p.fly_gauge


def airborne(p: "Player", now: float) -> bool:
    """High enough that a blow on the ground misses (in the air and done rising)."""
    return bool(p.fly) and now >= p.fly_safe_at


def request_fly(p: "Player | None", seq: int, on: bool, now: float) -> str | None:
    """Take off (on) or come down. A refusal code, or None: the change is queued in the movement
    stream (a refused take-off still takes its number there, empty). A landing is checked when
    the stream reaches it: over water it is refused there (no_landing) and the flight goes on."""
    if p is None or p.channel is None:
        return "cannot"
    code = None
    if on:
        level = fly_level(p) if _usable(p) else 0
        lock = float(flight_cfg(level).get("hit_lock_seconds", 0))
        if not _usable(p):
            code = "cannot"
        elif _busy(p, now):
            code = "answering"
        elif level == 0:
            code = "fly_locked"
        elif p.riding:
            code = "riding"
        elif now < p.struck_at + lock:
            code = "struck"
        elif level == 1 and gauge(p) < float(flight_cfg(1).get("min_gauge_seconds", 0)):
            code = "gauge_low"
    action = ("fly", bool(on)) if code is None else None
    if not p.channel.queue_special(p, seq, action):
        return "cannot"
    return code


def _fly_changed(ch: "ChannelZone", p: "Player", why: str, x0: float | None = None,
                 y0: float | None = None) -> None:
    """Tell everyone: the flyer took off or came down (why: up, land, gauge, fall, knocked, gone);
    a fall carries it from (x0, y0) back to the ground."""
    for other in ch.players.values():        # everyone who sees this player gets them again, in the air or not
        other.known.pop(p.eid, None)
    ev = {"k": "fly", "id": p.eid, "on": int(p.fly), "why": why, "x": round(p.x, 1), "y": round(p.y, 1),
          "sw": sword_sheet(p.realm)}
    if x0 is not None:
        ev.update(x0=round(x0, 1), y0=round(y0, 1))
    ch.event(**ev)
    if p.session is not None:
        p.session.send({"t": "fly", "ok": True, "on": int(p.fly), "why": why, "x": round(p.x, 2),
                        "y": round(p.y, 2), "gauge": round(gauge(p), 2)})


def _refuse_fly(p: "Player", code: str) -> None:
    if p.session is not None:
        p.session.send({"t": "fly", "ok": False, "code": code, "message_vi": REFUSALS_VI[code],
                        "on": int(p.fly), "x": round(p.x, 2), "y": round(p.y, 2)})


def apply_fly(ch: "ChannelZone", p: "Player", on: bool, now: float) -> None:
    """Reached in the movement stream: take off from where the player stands, or come down there."""
    from . import glide
    if on:
        if p.fly:
            return
        level = fly_level(p) if _usable(p) else 0
        if level == 0 or p.riding:
            _refuse_fly(p, "riding" if p.riding else "fly_locked")
            return
        p.fly = level
        p.fly_safe_at = now + float(flight_cfg(level).get("rise_ms", 0)) / 1000
        p.ground = (p.x, p.y)
        _fly_changed(ch, p, "up")
        return
    if not p.fly:
        return
    if not glide.land_ok(ch.map.collider, ch.map.tile_name, fly_over(p.fly), p.x, p.y):
        _refuse_fly(p, "no_landing")
        return
    p.fly = 0
    p.ground = (p.x, p.y)
    _fly_changed(ch, p, "land")


def land_down(ch: "ChannelZone", p: "Player", why: str) -> None:
    """The server brings a flyer down (why: gauge, knocked, gone): right there over walkable
    ground, else carried back to the last ground it passed (why becomes 'fall')."""
    from . import glide
    if not p.fly:
        return
    over = fly_over(p.fly)
    p.fly = 0
    if glide.land_ok(ch.map.collider, ch.map.tile_name, over, p.x, p.y):
        p.ground = (p.x, p.y)
        _fly_changed(ch, p, why)
        return
    x0, y0 = p.x, p.y
    p.x, p.y = p.ground
    p.dirty = True
    _fly_changed(ch, p, "fall", x0, y0)


def safe_xy(p: "Player") -> tuple[float, float]:
    """Where to keep this player when it leaves (a save, a channel): the ground under a flyer."""
    return (float(p.ground[0]), float(p.ground[1])) if p.fly else (p.x, p.y)


def tick(ch: "ChannelZone", dt: float, now: float) -> None:
    """Every tick: the gauge drains in low flight and refills on the ground; a flyer whose gauge
    ran dry, who fell or became a ghost comes down; the last ground under a flyer is kept."""
    from . import glide
    col, tile = ch.map.collider, ch.map.tile_name
    for p in list(ch.players.values()):
        if not p.fly:
            top = gauge_max(p)
            p.fly_gauge = min(top, gauge(p) + dt * top / refill_seconds(p))
            p.ground = (p.x, p.y)
            continue
        if p.dead or p.ghost or ch.instance:
            land_down(ch, p, "gone")
            continue
        if p.fly == 1:
            p.fly_gauge = gauge(p) - dt
            if p.fly_gauge <= 0:
                p.fly_gauge = 0.0
                land_down(ch, p, "gauge")
                continue
        if glide.land_ok(col, tile, fly_over(p.fly), p.x, p.y):
            p.ground = (p.x, p.y)


def flight_view(p: "Player") -> dict:
    """What the client needs to fly and to predict it: the rung open now and the numbers of
    each rung (levels[1], levels[2]), the gauge and the sword."""
    def rung(level):
        c = flight_cfg(level)
        return {"speed_mult": float(c.get("speed_mult", 1)), "lift": float(c.get("lift_px", 0)),
                "rise": float(c.get("rise_ms", 0)) / 1000, "over": sorted(fly_over(level)),
                "gauge": float(c.get("gauge_seconds", 0)) > 0}
    return {"level": fly_level(p), "levels": [{}] + [rung(i) for i in range(1, len(FLIGHT_RUNGS) + 1)],
            "gauge_max": gauge_max(p), "refill": refill_seconds(p),
            "min_gauge": float(flight_cfg(1).get("min_gauge_seconds", 0)),
            "hit_lock": float(flight_cfg(1).get("hit_lock_seconds", 0)),
            "sword": sword_sheet(p.realm), "flying": int(p.fly), "gauge_now": round(gauge(p), 2)}


# ------------------------------------------------------------------ the formation
def place_formation(p: "Player | None", now: float) -> str | None:
    """Bày pháp trận at the feet. A refusal code or None."""
    if not _usable(p):
        return "cannot"
    if _busy(p, now):
        return "answering"
    if not is_open(p, FORMATION):
        return "formation_locked"
    if now < p.tran_ready:
        return "cooldown"
    c = formation_cfg()
    ch = p.channel
    ch.formations = [f for f in ch.formations if f["until"] > now and f["by"] != p.eid]
    from ..systems import linh_can   # a linh căn of the formation path keeps it standing longer
    secs = float(c.get("seconds", 20)) * (1 + linh_can.fx(p, "tran_time"))
    ch.formations.append({"x": p.x, "y": p.y, "r": float(c.get("radius_px", 56)), "until": now + secs,
                          "by": p.eid, "mult": float(c.get("windup_mult", 1.5))})
    p.tran_ready = now + float(c.get("cooldown_seconds", 30))
    ch.event(k="tran", by=p.eid, x=round(p.x, 1), y=round(p.y, 1), r=float(c.get("radius_px", 56)), d=secs,
             fx=c.get("fx", ""))
    return None


def windup_mult(ch: "ChannelZone", m, now: float) -> float:
    """How much slower this monster winds up a blow: the strongest formation it stands in."""
    best = 1.0
    for f in getattr(ch, "formations", ()):
        if f["until"] > now and math.hypot(m.x - f["x"], m.y - f["y"]) <= f["r"]:
            best = max(best, f["mult"])
    return best


def formations_view(ch: "ChannelZone", now: float) -> list[dict]:
    return [{"x": round(f["x"], 1), "y": round(f["y"], 1), "r": f["r"], "left": round(f["until"] - now, 2),
             "by": f["by"]} for f in getattr(ch, "formations", ()) if f["until"] > now]


# ------------------------------------------------------------------ what the client is told
def view(p: "Player", now: float) -> dict | None:
    """Sent with the zone: which abilities are open and their numbers (None in a bí cảnh)."""
    if not wired() or p.channel is None or p.channel.instance:
        return None
    g, f = glide_cfg(), formation_cfg()
    out = {}
    for uid in (SEAL, FORMATION, GLIDE, RIDE, SOAR):
        u = unlock(uid)
        out[uid] = {"ok": is_open(p, uid), "name_vi": u.get("name_vi", uid),
                    "unlock": {"realm": u.get("realm"), "stage": int(u.get("stage", 0))}}
    out[GLIDE].update(max_px=glide_max_px(p), min_px=float(g.get("min_px", 0)),
                      ms=float(g.get("ms", 450)), cooldown=glide_cooldown(p),
                      over=list(g.get("over_tiles", [])), sheet=g.get("sheet", ""), flight=flight_view(p))
    out[FORMATION].update(radius=float(f.get("radius_px", 56)), seconds=float(f.get("seconds", 20)),
                          cooldown=float(f.get("cooldown_seconds", 30)), fx=f.get("fx", ""))
    out[RIDE].update(mult=mount_mult(p), riding=bool(p.riding))
    return out
