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

An ability is open when its unlock says 'co' and the player's place in Đạo Thụ (the TreePos kept
on the session, lands.py) reaches its realm and stage. Nothing here works in a bí cảnh.
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ..learning import math_tree
from ..systems import achievements

if TYPE_CHECKING:
    from .zone import ChannelZone, Player

GLIDE, RIDE, FORMATION, SEAL = "dap_kiem_luot", "cuoi_linh_thu", "phap_tran", "thu_phuc_linh_thu"

REFUSALS_VI = {
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
        elif not is_open(p, RIDE):
            code = "ride_locked"
        elif mount_mult(p) <= 0:
            code = "no_mount"
    if not p.channel.queue_special(p, seq, ("ride", bool(on and code is None))):
        return "cannot"
    return code


def apply_ride(ch: "ChannelZone", p: "Player", on: bool) -> None:
    if bool(p.riding) == bool(on):
        return
    p.riding = bool(on)
    if p.riding:
        achievements.bump(p.user_id, "ride")   # Thành Tựu
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


def check_glide(ch: "ChannelZone", x0: float, y0: float, x1: float, y1: float) -> str | None:
    from . import glide
    c = glide_cfg()
    return glide.check(ch.map.collider, ch.map.tile_name, set(c.get("over_tiles", [])), x0, y0, x1, y1,
                       float(c.get("max_px", 80)), float(c.get("min_px", 0)))


def apply_glide(ch: "ChannelZone", p: "Player", x: float, y: float) -> str | None:
    """Reached in the movement stream: glide from where the player stands now, or refuse."""
    code = check_glide(ch, p.x, p.y, x, y)
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
    p.dirty = True
    p.moved_this_tick = True
    ms = float(glide_cfg().get("ms", 450))
    ch.event(k="glide", id=p.eid, x0=round(x0, 1), y0=round(y0, 1), x=round(x, 1), y=round(y, 1), ms=ms)
    achievements.bump(p.user_id, "glide")      # Thành Tựu
    if p.session is not None:
        p.session.send({"t": "glide", "ok": True, "x": round(x, 2), "y": round(y, 2), "ms": ms})
    return None


def apply_special(ch: "ChannelZone", p: "Player", action) -> None:
    """An entry of the movement stream that is no walking (zone._move_players)."""
    if not action:
        return
    if action[0] == "glide":
        apply_glide(ch, p, action[1], action[2])
    elif action[0] == "ride":
        apply_ride(ch, p, action[1])


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
    achievements.bump(p.user_id, "formation")  # Thành Tựu
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
    for uid in (SEAL, FORMATION, GLIDE, RIDE):
        u = unlock(uid)
        out[uid] = {"ok": is_open(p, uid), "name_vi": u.get("name_vi", uid),
                    "unlock": {"realm": u.get("realm"), "stage": int(u.get("stage", 0))}}
    out[GLIDE].update(max_px=float(g.get("max_px", 80)), min_px=float(g.get("min_px", 0)),
                      ms=float(g.get("ms", 450)), cooldown=glide_cooldown(p),
                      over=list(g.get("over_tiles", [])), sheet=g.get("sheet", ""))
    out[FORMATION].update(radius=float(f.get("radius_px", 56)), seconds=float(f.get("seconds", 20)),
                          cooldown=float(f.get("cooldown_seconds", 30)), fx=f.get("fx", ""))
    out[RIDE].update(mult=mount_mult(p), riding=bool(p.riding))
    return out
