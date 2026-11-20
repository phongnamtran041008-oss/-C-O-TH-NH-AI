"""Linh thú out in their lands (world_plan.json `beasts` and `beast_taming`, wired section 'beasts').

A built beast lives in one channel of its land as a `Beast`, a monster of realtime/ai.py with
three differences:

  * it shows itself only to a player whose place in Đạo Thụ meets its `requires`, who has the
    ability its `needs` names and who has not tamed it yet (`shows_to`): the others never get
    it in a snapshot, are never aimed at and their blows never reach it;
  * it fights by the open-world rule like the creatures of its land (a telegraphed blow; when it
    lands, a question on the nodes those creatures stand for, systems/beasts.land_nodes), but
    it never dies: plain hits wear it down to 1 HP at most;
  * a right answer to its blow - a Phản Đòn - counts for that player (`on_parry`). At
    `parries_to_tame` it **yields** to them: it stops fighting them and waits `yield_seconds`
    for their Phong Ấn Phù (POST /beasts/seal, `seal_target`). The count starts over when the
    fight breaks off (the beast goes home).

Sealing turns it into a Linh Thú of the player (systems/beasts.seal); from then on it no longer
shows itself to them in the wild.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..systems import beasts as data
from .ai import Monster
from .maps import Area

if TYPE_CHECKING:
    from .zone import ChannelZone, Player

SEAL_REFUSALS_VI = {
    "not_here": "Linh thú này không ở gần con.",
    "not_yielded": "Linh thú chưa chịu phục: hãy Phản Đòn đủ số lần trước.",
    "too_far": "Đứng gần linh thú hơn rồi hãy phong ấn.",
    "locked": "Thu phục linh thú mở ở Luyện Khí tầng 3 trên Đạo Thụ.",
}


@dataclass
class Beast(Monster):
    beast: bool = True
    parries: dict = field(default_factory=dict)      # user id -> Phản Đòn counted in this fight
    yielded: dict = field(default_factory=dict)      # user id -> until when it waits for their seal

    @property
    def info(self) -> dict:
        return data.fight_info(self.kind)

    @property
    def plan(self) -> dict:
        return data._data()["all"][self.kind]

    @property
    def need(self) -> int:
        return int(self.plan["parries_to_tame"])

    def reset(self) -> None:
        kept = dict(getattr(self, "yielded", {}) or {})
        super().reset()
        self.shield, self.regen = False, []
        self.parries = {}
        self.yielded = kept

    def shows_to(self, p: "Player") -> bool:
        s = p.session
        if s is None:
            return False
        return data.can_meet(self.plan, getattr(s, "tree", None), getattr(s, "tamed", set()))

    def yielded_to(self, uid: int, now: float) -> bool:
        until = self.yielded.get(uid)
        if until is None:
            return False
        if now >= until:
            self.yielded.pop(uid, None)
            return False
        return True

    def fights(self, p: "Player") -> bool:
        """It fights everyone it shows itself to, except who it yielded to (while it waits)."""
        until = self.yielded.get(p.user_id)
        return self.shows_to(p) and (until is None or p.now >= until)

    def full(self) -> dict:
        return {**super().full(), "beast": 1, "need": self.need}


def wired() -> bool:
    return data.wired()


def spawn_for(zone_id: str, number: int) -> list[Beast]:
    """The beasts of the land this zone is, for one channel of it."""
    if not wired():
        return []
    from . import lands
    land_id = lands.zone_land_id(zone_id)
    roam = float(data.taming().get("roam_tiles", 2)) * 16
    out = []
    for bid, b in data.built().items():
        if b["land"] != land_id or not b.get("pos"):
            continue
        tx, ty = b["pos"]
        x, y = tx * 16 + 8, ty * 16 + 12
        area = Area(f"beast_{bid}", x - roam, y - roam, 2 * roam, 2 * roam, {"monster": bid})
        m = Beast(f"b{number}_{bid}", bid, area, float(x), float(y))
        m.on_hit = True
        m.reset()
        out.append(m)
    return out


def is_beast(m) -> bool:
    return isinstance(m, Beast)


def on_parry(ch: "ChannelZone", m, p: "Player", now: float) -> dict | None:
    """A Phản Đòn against a beast: count it; at the plan's number the beast yields to this player."""
    if not isinstance(m, Beast) or not m.alive:
        return None
    need = m.need
    n = m.parries.get(p.user_id, 0) + 1
    done = n >= need
    if done:
        from . import combat
        m.parries.pop(p.user_id, None)
        m.yielded[p.user_id] = now + float(data.taming().get("yield_seconds", 90))
        combat.disengage(ch, m, p.user_id, now)
        m.tele = None
        if not m.engaged:
            m.mode = "return"
    else:
        m.parries[p.user_id] = n
    ch.event(k="tame", id=m.eid, by=p.eid, n=min(n, need), need=need, ok=int(done), x=round(m.x, 1), y=round(m.y, 1))
    return {"beast": m.kind, "name_vi": m.plan["name_vi"], "n": min(n, need), "need": need, "yielded": done}


def seal_target(p: "Player | None", eid: str, now: float):
    """The beast a player may seal right now, or a refusal code (SEAL_REFUSALS_VI)."""
    from . import abilities
    ch = p.channel if p is not None else None
    m = ch.monster(eid) if ch is not None else None
    if p is None or not isinstance(m, Beast) or not m.shows_to(p):
        return "not_here"
    if not m.yielded_to(p.user_id, now):
        return "not_yielded"
    if math.hypot(m.x - p.x, m.y - p.y) > float(data.taming().get("seal_reach_px", 56)):
        return "too_far"
    if not abilities.is_open(p, data.taming().get("seal_unlock", "thu_phuc_linh_thu")):
        return "locked"
    return m


def sealed(ch: "ChannelZone", m: Beast, p: "Player") -> None:
    """The seal worked: the beast is the player's now and leaves their world."""
    m.yielded.pop(p.user_id, None)
    if p.session is not None:
        p.session.tamed = set(getattr(p.session, "tamed", set())) | {m.kind}
    ch.event(k="seal", id=m.eid, by=p.eid, x=round(m.x, 1), y=round(m.y, 1))
