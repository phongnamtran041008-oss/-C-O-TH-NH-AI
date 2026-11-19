"""Bí cảnh, the live part (spec 14, M10): matchmaking, Khe Nứt Mực rifts, and one instance per run.

An instance is a private copy of the `bi_canh` map (a ChannelZone of its own, so movement,
Vấn Đạo combat, guard bees and snapshots work exactly as in the world). A run is the Trận Nhãn
rooms its realm lists in data/realms.json (`math.rooms`) and then the boss's den; the party is
moved from room to room when one is cleared (its seals broken and its Mặc Quái beaten). Every
question of a run - a monster's, a seal's, the boss's - is a math question at the answering
player's own floor (app/systems/math_realm.py).

Every realm is a math bí cảnh; its `kind` only says how it is entered: "math" at the Cổng Bí
Cảnh whenever the gate is there, "scheduled" at the gate during the opening hours of
balance/realm.json, "rift" through a Khe Nứt Mực that opens now and then in the wild.

Like the rest of the tick, nothing here waits for the database: entering a run and paying loot
run as background tasks (app/systems/secret_realm.py).
"""
from __future__ import annotations

import datetime as dt
import itertools
import logging
import math
import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .. import balance, clock
from . import ai, combat, maps, protocol
from .maps import Area
from .zone import ChannelZone, Player

if TYPE_CHECKING:
    from .world import Session, World

log = logging.getLogger("toan_tu_tien.realm")
MAP = "bi_canh"
VILLAGE = "truc_lam_thon"
GATE_KINDS = ("math", "scheduled")      # entered at the Cổng Bí Cảnh (a "rift" realm only through a rift)


def cfg() -> dict:
    return balance.load("realm")


def realm_defs() -> dict:
    from ..systems import secret_realm
    return secret_realm.realms()


def puzzle_info(kind: str) -> dict:
    from ..systems import secret_realm
    return secret_realm.puzzle_info(kind)


def dist(ax: float, ay: float, bx: float, by: float) -> float:
    return math.hypot(ax - bx, ay - by)


def anchor(a: Area) -> tuple[float, float]:
    """Where a prop stands: the middle of its bottom edge."""
    return a.x + a.w / 2, a.y + a.h


# ------------------------------------------------------------------ the schedule (spec 14.1)
def window_status(now: dt.datetime) -> dict:
    """Is the scheduled realm open? Fixed hours in UTC+7, `open_minutes` long."""
    c = cfg()
    if c.get("always_open"):
        return {"open": True, "opens_in": 0, "closes_in": None}
    sch = c["schedule"]
    local = now + clock.VN_OFFSET
    length = dt.timedelta(minutes=sch["open_minutes"])
    starts = sorted(dt.datetime.combine(local.date() + dt.timedelta(days=d), dt.time(h))
                    for d in (-1, 0, 1) for h in sch["hours_local"])
    for st in starts:
        if st <= local < st + length:
            return {"open": True, "opens_in": 0, "closes_in": int((st + length - local).total_seconds())}
    nxt = next(st for st in starts if st > local)
    return {"open": False, "opens_in": int((nxt - local).total_seconds()), "closes_in": None}


@dataclass
class Member:
    uid: int
    name: str
    state: str = "in"                # in | left
    floor: int | None = None         # the floor this player's questions come from


@dataclass
class Rift:
    """A Khe Nứt Mực: seen by whoever walks near it in a public zone for a few minutes."""
    id: str
    realm_id: str
    channel: ChannelZone
    x: float
    y: float
    expires: float
    now: float = 0.0

    def state(self) -> list:
        return [self.id, round(self.x, 1), round(self.y, 1), 0, 0]

    def full(self) -> dict:
        r = realm_defs()[self.realm_id]
        return {"id": self.id, "k": "r", "x": round(self.x, 1), "y": round(self.y, 1), "realm": self.realm_id,
                "n": r["name_vi"], "left": int(max(0.0, self.expires - self.now))}


# ------------------------------------------------------------------ rooms
class Puzzle:
    kind = ""

    def __init__(self, inst: "RealmInstance"):
        self.inst = inst
        self.rng = inst.rng
        self.solved = False
        self.mistakes = 0

    def public(self, now: float) -> dict:
        return {"kind": self.kind, "solved": self.solved, "fails": self.mistakes}

    def tick(self, dt_: float, now: float) -> None:
        pass

    def solve(self, now: float) -> None:
        self.solved = True
        x, y = self.inst.room_center()
        self.inst.event(k="pz", e="solve", x=x, y=y)
        self.inst.push_puzzle(now)

    def mistake(self, now: float, x: float | None = None, y: float | None = None) -> None:
        self.mistakes += 1
        cx, cy = self.inst.room_center()
        self.inst.event(k="pz", e="fail", x=cx if x is None else x, y=cy if y is None else y)


class BossPuzzle(Puzzle):
    """The den: solved when the Nghiên Ma falls (its shield rules live in combat.py)."""
    kind = "boss"

    def public(self, now: float) -> dict:
        b = self.inst.boss
        out = super().public(now)
        if b is not None:
            out.update({"boss": b.eid, "hp": b.hp_pct(), "shield": int(b.shield), "phase": 4 - len(b.regen),
                        "hits": len(b.group_hits), "need": self.inst.group_need(b)})
        return out

    def tick(self, dt_: float, now: float) -> None:
        b = self.inst.boss
        if b is not None and not b.alive and not self.solved:
            self.solved = True


class SealPuzzle(Puzzle):
    """Trận Nhãn (M10): seals lie on the floor of the room. Whoever stands on an unbroken one
    is asked one question of *their own* floor (math_ask.pick_own, never the room's or a
    monster's); a right answer breaks the seal, a wrong one (or running out of time) hurts the
    one who answered and the seal holds.

    The room opens when the party has broken `need` seals - `base`, plus `per_member` for
    every other member who can be asked, never more than the room has - and at least
    min(members, need) *different* members broke one. So a seal room is cleared together,
    never by the strongest player alone; alone, `base` seals are enough. A member who has
    already broken one is not asked by a further seal when that would leave too few for the
    ones who have not, so the room can always still be finished."""
    kind = "seal"

    def __init__(self, inst: "RealmInstance", now: float):
        super().__init__(inst)
        self.obj_kind = inst.room_spec().get("seal", "pedestal")
        self.names = [o.name for o in inst.objs(self.obj_kind)]
        self.broken: dict[str, int] = {}          # seal -> who broke it
        self.asking: dict[int, str] = {}          # uid -> the seal whose question they hold
        self.cool: dict[int, float] = {}          # uid -> not asked again before this
        self.on_seal: dict[int, str | None] = {}  # uid -> the seal they stood on last tick

    # ------------------------------------------------------------ the rule
    def askers(self) -> list[Player]:
        """Whom the room waits for: everyone standing who can be asked a question at all."""
        return [p for p in self.inst.active() if p.user_id not in self.inst.no_question]

    def need(self) -> int:
        c = cfg()["seal"]
        n = max(1, len(self.askers()))
        return max(1, min(len(self.names), c["base"] + c["per_member"] * (n - 1)))

    def missing(self) -> list[int]:
        done = set(self.broken.values())
        return [p.user_id for p in self.askers() if p.user_id not in done]

    def done(self) -> bool:
        askers = self.askers()
        if not askers:
            return False
        need = self.need()
        breakers = {p.user_id for p in askers} & set(self.broken.values())
        return len(self.broken) >= need and len(breakers) >= min(len(askers), need)

    def may_take(self, p: Player) -> bool:
        """A member who already broke a seal leaves enough unbroken ones for those who have not."""
        if p.user_id not in set(self.broken.values()):
            return True
        missing = [u for u in self.missing() if u != p.user_id]
        held = sum(1 for u in self.asking if u != p.user_id and u not in missing)
        return len(self.names) - len(self.broken) - held - 1 >= len(missing)

    def obj(self, name: str) -> Area | None:
        return next((o for o in self.inst.objs(self.obj_kind) if o.name == name), None)

    # ------------------------------------------------------------ what everyone sees
    def public(self, now: float) -> dict:
        busy = set(self.asking.values())
        return {**super().public(now), "seal_kind": self.obj_kind, "broken": len(self.broken), "need": self.need(),
                "seals": [{"name": n, "broken": n in self.broken, "busy": n in busy} for n in self.names],
                "missing": self.missing()}

    # ------------------------------------------------------------ the tick
    def tick(self, dt_: float, now: float) -> None:
        if self.solved:
            return
        inst = self.inst
        for uid in list(self.asking):   # a question that went away (fell, left, ran out) frees its seal
            p = inst.players.get(uid)
            if p is None or p.dead or (p.question is None and not p.q_pending):
                del self.asking[uid]
                self.inst.push_puzzle(now)
        if self.done():
            self.solve(now)
            return
        objs = {o.name: o for o in inst.objs(self.obj_kind)}
        for p in inst.active():
            here = next((n for n, o in objs.items() if n not in self.broken and inst.on(p, o)), None)
            before = self.on_seal.get(p.user_id)
            self.on_seal[p.user_id] = here
            if (here is None or p.user_id in self.asking or p.question is not None or p.q_pending
                    or here in self.asking.values() or now < self.cool.get(p.user_id, 0.0)
                    or now < p.no_question_until):
                continue
            if not self.may_take(p):
                if here != before and p.session is not None:
                    p.session.send({"t": "realm", "event": "hint", "code": "seal_share",
                                    "text_vi": "Con đã phá một ấn rồi, nhường ấn này cho đạo hữu chưa phá."})
                continue
            self.asking[p.user_id] = here
            p.q_pending = True
            inst.world.spawn(self._ask(p, here))
            inst.push_puzzle(now)

    async def _ask(self, p: Player, name: str) -> None:
        from .. import balance as bal
        from ..systems import math_realm
        inst = self.inst
        made = None
        try:
            made = await math_realm.seal_session(inst, p, name)
        except Exception:
            log.exception("could not create a seal question")
        p.q_pending = False
        now = inst.world.mono()
        if made is None:
            if self.asking.get(p.user_id) == name:
                del self.asking[p.user_id]
            self.cool[p.user_id] = now + cfg()["seal"]["retry_seconds"]
            inst.push_puzzle(now)
            return
        out, limit = made
        if (inst.puzzle is not self or self.solved or name in self.broken or self.asking.get(p.user_id) != name
                or p.dead or p.channel is not inst or p.session is None or p.question is not None):
            if self.asking.get(p.user_id) == name:
                del self.asking[p.user_id]
            return   # the room went on while the question was written; it simply expires
        deadline = now + limit + bal.quiz()["network_grace"]
        p.question = {"sid": out["session_id"], "mid": None, "deadline": deadline, "asked": now, "limit": limit,
                      "timeout_sent": False, "seal": name, "ch": inst.key}
        p.protect_until = deadline
        p.inputs.clear()
        p.queued_ms = 0
        p.session.send({"t": "q", "mid": None, "q": out, "first_meet": False, "seal": name})
        o = self.obj(name)
        if o is not None:
            self.inst.event(k="pz", e="ask", x=o.x + o.w / 2, y=o.y + o.h / 2, by=p.eid)

    # ------------------------------------------------------------ the answer (graded by app/systems/math_realm.py)
    def answer(self, p: Player, sid: str, correct: bool) -> dict:
        q = p.question
        if q is None or q["sid"] != sid or not q.get("seal"):
            return {"stale": True}
        p.question = None
        p.protect_until = 0.0
        name = q["seal"]
        if self.asking.get(p.user_id) == name:
            del self.asking[p.user_id]
        now = self.inst.world.mono()
        if self.solved or name in self.broken or name not in self.names or p.dead:
            return {"seal": name, "stale": True}
        o = self.obj(name)
        x, y = (o.x + o.w / 2, o.y + o.h / 2) if o is not None else (p.x, p.y)
        self.inst.send_all({"t": "realm", "event": "seal", "ok": bool(correct), "by": p.name})
        if correct:
            self.broken[name] = p.user_id
            self.inst.event(k="pz", e="seal", x=x, y=y, by=p.eid)
            if self.done():
                self.solve(now)
            else:
                self.inst.push_puzzle(now)
            return {"seal": name, "broken": True, "count": len(self.broken), "need": self.need()}
        hp = p.hp
        self.inst.hurt(p, cfg()["seal"]["fail_pct"], now)
        self.mistake(now, x, y)
        self.cool[p.user_id] = now + cfg()["seal"]["retry_seconds"]
        self.inst.push_puzzle(now)
        return {"seal": name, "broken": False, "hurt": int(round(hp - p.hp)), "hp": max(0, int(round(p.hp)))}

    def solve(self, now: float) -> None:
        for uid in list(self.asking):   # the seals the others were still being asked about need no answer now
            p = self.inst.players.get(uid)
            if p is not None and p.question and p.question.get("seal"):
                combat.end_question(p, "solved")
        self.asking.clear()
        super().solve(now)


PUZZLES = {"seal": SealPuzzle}      # the rooms before the boss a realm may list in `math.rooms`


# ------------------------------------------------------------------ one run
class RealmInstance(ChannelZone):
    instance = True

    def __init__(self, world: "World", run_id: int, realm_id: str, members: dict[int, Member],
                 rng: random.Random | None = None, rooms: list[str] | None = None):
        super().__init__(MAP, run_id, maps.load(MAP), rng or random.Random())
        self.monsters = []
        self.world = world
        self.run_id, self.realm_id = run_id, realm_id
        self.rdef = realm_defs()[realm_id]
        self.members = members
        # every question of the run is asked at the answering player's own floor, whatever asks
        # it (combat.py calls `question_source` instead of the monster's own question)
        self.math = True
        self.question_source = self.math_question
        self.no_question: set[int] = set()     # members the bank has no question for right now
        self.rooms = list(rooms) if rooms else self._pick_rooms()
        self.room_specs = self._room_specs()
        self.room_i = -1
        self.puzzle: Puzzle | None = None
        self.phase = "starting"            # starting | running | advancing | ended
        self.started = world.mono()
        self.deadline = self.started + self.rdef["time_limit_minutes"] * 60
        self.advance_at = 0.0
        self.end_at = 0.0
        self.flawless = 0
        self.result: str | None = None
        self.boss: ai.Monster | None = None
        self.boss_wake = 0.0
        self.next_aoe = 0.0
        self.aoes: list[tuple] = []
        self._mid = itertools.count()

    def _pick_rooms(self) -> list[str]:
        """The rooms the realm's data lists, in that order, then the boss."""
        return [r["kind"] for r in self.rdef["math"]["rooms"]] + ["boss"]

    def _room_specs(self) -> list[dict]:
        """Where each room is played. A room borrows a room of the bi_canh map and its stones, as
        realms.json says ({"kind": "seal", "place": "compose", "seal": "pedestal"}); the boss has
        its own den."""
        spec = [dict(r) for r in (self.rdef.get("math") or {}).get("rooms", [])]
        out, used = [], set()
        for k in self.rooms:
            if k == "boss":
                out.append({"kind": k, "place": k})
                continue
            mine = [j for j, r in enumerate(spec) if r["kind"] == k]
            if not mine:
                raise ValueError(f"realm {self.realm_id}: no place for a {k} room")
            j = next((j for j in mine if j not in used), mine[0])
            used.add(j)
            out.append({**spec[j], "place": spec[j].get("place", k)})
        return out

    # ------------------------------------------------------------ places and people
    @property
    def kind(self) -> str | None:
        return self.rooms[self.room_i] if 0 <= self.room_i < len(self.rooms) else None

    @property
    def place(self) -> str | None:
        """The room of the map the current room is played in."""
        return self.room_specs[self.room_i]["place"] if 0 <= self.room_i < len(self.rooms) else None

    def room_spec(self) -> dict:
        return self.room_specs[self.room_i] if 0 <= self.room_i < len(self.rooms) else {}

    def objs(self, kind: str) -> list[Area]:
        return [o for o in self.map.realm_objs if o.props.get("room") == self.place and o.props.get("kind") == kind]

    def room_center(self) -> tuple[float, float]:
        a = self.map.rooms[self.place]
        return a.x + a.w / 2, a.y + a.h / 2

    def on(self, p: Player, a: Area, pad: float | None = None) -> bool:
        pad = cfg()["stand_pad"] if pad is None else pad
        return a.x - pad <= p.x <= a.x + a.w + pad and a.y - pad <= p.y <= a.y + a.h + pad

    def present(self) -> list[Player]:
        return [p for p in self.players.values()
                if (m := self.members.get(p.user_id)) is not None and m.state == "in"]

    def active(self) -> list[Player]:
        """Who can play right now: connected, standing (not a ghost)."""
        return [p for p in self.present() if p.session is not None and not p.dead]

    def group_need(self, m: ai.Monster) -> int:
        """Spec 14.2: the boss's big shield needs as many right answers (from different players)
        as there are members still alive. A member the bank has no question for cannot answer,
        so the shield does not wait for them."""
        return max(1, len([p for p in self.active() if p.user_id not in self.no_question]))

    # ------------------------------------------------------------ questions
    async def math_question(self, db, user, p: Player, m: "ai.Monster | None", rng: random.Random):
        """combat.py's question for a monster of this run: at this player's own floor; the
        boss asks their "bài tổng hợp" (the hardest question they may be asked)."""
        from ..systems import math_realm
        boss = m is not None and bool(m.info.get("group_shield"))
        q = await math_realm.question_for(db, user, self.rdef, "boss" if boss else "monster", rng,
                                          who_vi=m.info.get("name_vi", "") if m is not None else "")
        if not self.got_question(p, q):
            return None
        return math_realm.CONTEXT, q

    def got_question(self, p: Player, q) -> bool:
        """Notes whether the bank had a question for this player; tells them when it did not."""
        if q is not None:
            self.no_question.discard(p.user_id)
            return True
        self.no_question.add(p.user_id)
        p.no_question_until = self.world.mono() + 10
        if p.session is not None:
            p.session.send({"t": "error", "code": "no_math_question",
                            "message_vi": "Chưa có câu toán nào ở tầng của con. Luyện ở Động Phủ một lúc "
                                          "rồi quay lại; đội vẫn đi tiếp được mà không chờ con."})
        return False

    def exit_pos(self) -> tuple[float, float]:
        from .world import zone_defs
        return maps.load(zone_defs()[VILLAGE]["map"]).spawn("from_realm")

    # ------------------------------------------------------------ messages
    def send_all(self, msg: dict) -> None:
        for p in self.present():
            if p.session is not None:
                p.session.send(msg)

    def run_msg(self, now: float) -> dict:
        return {"t": "realm", "event": "start", "run": {
            "id": self.run_id, "realm": self.realm_id, "name_vi": self.rdef["name_vi"],
            "left": int(max(0, self.deadline - now)), "math": True,
            "rooms": [{"kind": k, "name_vi": puzzle_info(k).get("name_vi", k)} for k in self.rooms],
            "members": [{"uid": m.uid, "name": m.name, "in": m.state == "in", "floor": m.floor}
                        for m in self.members.values()]}}

    def room_msg(self, uid: int, now: float) -> dict:
        info = puzzle_info(self.kind)
        return {"t": "realm", "event": "room", "i": self.room_i, "n": len(self.rooms), "kind": self.kind,
                "place": self.place, "math": True, "name_vi": info.get("name_vi", self.kind),
                "how_vi": info.get("how_vi", ""), "left": int(max(0, self.deadline - now)), "phase": self.phase,
                "puzzle": self.puzzle.public(now) if self.puzzle else None}

    def push_puzzle(self, now: float) -> None:
        if self.puzzle is not None:
            self.send_all({"t": "realm", "event": "puzzle", "i": self.room_i, "puzzle": self.puzzle.public(now)})

    def resync(self, p: Player) -> None:
        """A player came back after losing the connection (spec 14.3): everything again."""
        now = self.world.mono()
        if p.session is None:
            return
        p.session.send(self.run_msg(now))
        if self.kind is not None:
            p.session.send(self.room_msg(p.user_id, now))
        if self.phase == "ended":
            p.session.send(self.end_msg(now))

    # ------------------------------------------------------------ effects on players
    def hurt(self, p: Player, pct: float, now: float, kind: str = "mk") -> None:
        if not p.dead:
            combat.hurt_player(self, p, p.max_hp * pct / 100, now, kind=kind, by="pz")

    def _ghost_changed(self, p: Player) -> None:
        for other in self.players.values():
            other.known.pop(p.eid, None)   # everyone gets this player again, drawn as a ghost (or not)

    def on_down(self, p: Player, now: float) -> None:
        """Out of health in a bí cảnh: a ghost that follows the party until the next room."""
        p.dead, p.ghost, p.hp = True, True, 0.0
        p.respawn_at = float("inf")
        for m in self.monsters:
            m.engaged.discard(p.user_id)
        if p.question:
            combat.end_question(p, "dead")
        p.next_q = None
        self.event(k="die", id=p.eid, x=p.x, y=p.y)
        self._ghost_changed(p)
        if p.session is not None:
            p.session.send({"t": "dead", "ghost": 1, "respawn_in": 0})

    def revive(self, p: Player, pct: float | None = None) -> None:
        if not p.ghost and not p.dead:
            return
        p.dead = p.ghost = False
        p.hp = max(1.0, p.max_hp * (cfg()["revive_hp_pct"] if pct is None else pct) / 100)
        p.respawn_at = 0.0
        self._ghost_changed(p)
        self.event(k="heal", id=p.eid, v=int(p.hp), x=p.x, y=p.y)
        if p.session is not None:
            p.session.send({"t": "realm", "event": "revived", "hp": int(p.hp)})

    # ------------------------------------------------------------ the run
    def begin(self, now: float) -> None:
        self.phase = "running"
        x, y = self.map.spawn(f"{self.room_specs[0]['place']}_entry")
        for i, (uid, m) in enumerate(self.members.items()):
            s = self.world.sessions.get(uid)
            if s is None:
                self._member_gone(m, "disconnected")
                continue
            self.world.put(s, self, *self._spread(x, y, i), "up")
        self.send_all(self.run_msg(now))
        self._start_room(0, now)

    def _spread(self, x: float, y: float, i: int) -> tuple[float, float]:
        dx = (0, -26, 26, -52, 52)[i % 5]
        return (x + dx, y) if not self.map.collider.blocked(x + dx, y) else (x, y)

    def _teleport(self, p: Player, x: float, y: float) -> None:
        p.x, p.y, p.facing = float(x), float(y), "up"
        p.inputs.clear()
        p.queued_ms = 0
        p.budget_ms = 0.0
        p.moving = False
        p.known = {}   # the client forgets everyone on a zone message: send them all again
        if p.session is not None:
            self.world._send_zone(p.session, p)

    def _spawn_monsters(self, now: float) -> None:
        area = self.map.rooms[self.place]
        if self.kind == "boss":
            bs = self.objs("boss_spawn")[0]
            m = ai.Monster(f"m{self.run_id}_{next(self._mid)}", self.rdef["boss"], area, bs.x + 8, bs.y + 12)
            extra = max(0, len(self.present()) - 1)
            m.hp_scale = self.rdef.get("boss_hp_mult", 1.0) * (1 + cfg()["boss"]["hp_per_extra_member"] * extra)
            m.reset()
            self.boss = m
            self.monsters.append(m)
            self.boss_wake = now + 3.0
            self.next_aoe = now + cfg()["boss"]["aoe_every"]
            return
        for mkind, count in self.rdef["room_monsters"].items():
            for _ in range(int(count)):
                x, y = self._free_spot(area)
                m = ai.Monster(f"m{self.run_id}_{next(self._mid)}", mkind, area, x, y)
                m.idle = self.rng.uniform(0.5, 2.0)
                self.monsters.append(m)

    def _free_spot(self, a: Area) -> tuple[float, float]:
        for _ in range(40):   # the far half of the room, away from the entrance
            x = self.rng.uniform(a.x + 24, a.x + a.w - 24)
            y = self.rng.uniform(a.y + 20, a.y + a.h * 0.45)
            if not self.map.collider.blocked(x, y):
                return x, y
        return a.x + a.w / 2, a.y + 40

    def _start_room(self, i: int, now: float) -> None:
        self.room_i = i
        self.monsters = []
        self.boss, self.aoes = None, []
        self.puzzle = None
        x, y = self.map.spawn(f"{self.place}_entry")
        if i > 0:   # (the first room: begin() just put everyone there)
            for n, p in enumerate(self.present()):
                self._teleport(p, *self._spread(x, y, n))
        self._spawn_monsters(now)
        self._rebuild_grid()   # the snapshot of this very tick already sees everyone in the new room
        self.puzzle = BossPuzzle(self) if self.kind == "boss" else PUZZLES[self.kind](self, now)
        self.phase = "running"
        for p in self.present():
            if p.session is not None:
                p.session.send(self.room_msg(p.user_id, now))

    def _room_cleared(self, now: float) -> None:
        i, kind = self.room_i, self.kind
        flawless = self.puzzle.mistakes == 0
        if kind != "boss" and flawless:
            self.flawless += 1
        for uid, m in self.members.items():
            if m.state == "in":
                self.world.spawn(self._pay_room(uid, i, kind))
        x, y = anchor(self.objs("exit")[0])
        self.event(k="pz", e="open", x=x, y=y)
        if kind == "boss":
            self._finish("won", now)
            return
        self.phase = "advancing"
        self.advance_at = now + cfg()["advance_seconds"]
        self.send_all({"t": "realm", "event": "cleared", "i": i, "flawless": flawless,
                       "next_in": cfg()["advance_seconds"]})

    def _advance(self, now: float) -> None:
        for p in self.present():   # spec 14.2: ghosts come back when the party moves on
            self.revive(p)
        self._start_room(self.room_i + 1, now)

    def end_msg(self, now: float) -> dict:
        elapsed = (self.end_at - cfg()["exit_seconds"]) - self.started
        return {"t": "realm", "event": "end", "result": self.result, "time": int(elapsed), "flawless": self.flawless,
                "puzzles": len(self.rooms) - 1, "fast": self._fast(), "fragments": self._fragments(),
                "exit_in": int(max(0, self.end_at - now))}

    def _fast(self) -> bool:
        took = (self.end_at - cfg()["exit_seconds"]) - self.started
        return self.result == "won" and took <= self.rdef["time_limit_minutes"] * 60 * cfg()["fast_fraction"]

    def _fragments(self) -> int:
        if self.result != "won":
            return 0
        c = cfg()
        chest = c["chest"][self.realm_id]
        return chest["fragments"] + self.flawless * chest.get("flawless_fragments", c["flawless_fragments"])

    def _finish(self, result: str, now: float) -> None:
        if self.phase == "ended":
            return
        from ..systems import secret_realm
        self.phase, self.result = "ended", result
        self.end_at = now + cfg()["exit_seconds"]
        for m in self.monsters:
            m.engaged = set()
            m.tele = None
        self.aoes = []
        for p in self.players.values():
            if p.question:
                combat.end_question(p, "realm_end")
            p.next_q = None
            self.revive(p)
        inside = [uid for uid, m in self.members.items() if m.state == "in"]
        if result == "won":
            for uid in inside:
                self.world.spawn(self._pay_chest(uid, self._fragments(), self._fast()))
        self.world.spawn(secret_realm.finish_run(self.run_id, result, inside))
        self.send_all(self.end_msg(now))

    async def _pay_room(self, uid: int, i: int, kind: str) -> None:
        from ..systems import secret_realm
        try:
            loot = await secret_realm.claim_room(self.run_id, uid, i, kind, self.realm_id)
        except Exception:
            log.exception("room loot failed")
            return
        if loot is not None:
            self.world.notify(uid, {"t": "realm", "event": "loot", "loot": loot})

    async def _pay_chest(self, uid: int, fragments: int, fast: bool) -> None:
        from ..systems import secret_realm
        try:
            loot = await secret_realm.claim_chest(self.run_id, uid, self.realm_id, fragments, fast)
        except Exception:
            log.exception("chest loot failed")
            return
        if loot is not None:
            self.world.notify(uid, {"t": "realm", "event": "loot", "loot": loot})

    # ------------------------------------------------------------ leaving
    def _member_gone(self, m: Member, why: str) -> None:
        if m.state != "in":
            return
        from ..systems import secret_realm
        m.state = "left"
        self.world.spawn(secret_realm.member_left(self.run_id, m.uid, why))
        self.send_all({"t": "realm", "event": "member_left", "uid": m.uid, "name": m.name, "reason": why})

    def leave(self, p: Player, now: float) -> None:
        """The player walks out (keeping the loot of the rooms already cleared)."""
        m = self.members.get(p.user_id)
        if m is not None:
            self._member_gone(m, "left")
        if p.question:   # an open question stays behind (it may still be answered: that is only logged)
            combat.end_question(p, "left")
        p.next_q = None
        self._exit(p)

    def member_lost(self, p: Player) -> None:
        """Called by the world when a disconnected member did not come back in time."""
        m = self.members.get(p.user_id)
        if m is not None:
            self._member_gone(m, "disconnected")
        self.revive(p)

    def _exit(self, p: Player) -> None:
        self.revive(p)
        if p.session is not None:
            x, y = self.exit_pos()
            self.world._place(p.session, VILLAGE, x, y, "down")
            p.session.send({"t": "realm", "event": "left"})
        else:
            self.world._leave_world(p)

    # ------------------------------------------------------------ tick
    def _boss_tick(self, now: float) -> None:
        b = self.boss
        if b is None or not b.alive or now < self.boss_wake:
            return
        c = cfg()["boss"]
        for p in self.active():
            if p.user_id not in b.engaged:
                combat.engage(self, b, p, now)
        if b.shield and b.group_hits and len(b.group_hits) >= self.group_need(b):
            combat.break_shield(self, b, None, now)   # someone fell: the ones left already did enough
        if now >= self.next_aoe:
            self.next_aoe = now + c["aoe_every"]
            targets = self.active()
            if targets:   # Mặc Triều: a wide red circle under someone, then a wave of ink
                t = self.rng.choice(targets)
                self.aoes.append((t.x, t.y, c["aoe_radius"], now + c["aoe_delay"]))
                self.event(k="tele", id=b.eid, x=round(t.x, 1), y=round(t.y, 1), r=c["aoe_radius"],
                           d=c["aoe_delay"], big=1)
        for a in list(self.aoes):
            x, y, r, land = a
            if now < land:
                continue
            self.aoes.remove(a)
            self.event(k="pz", e="wave", x=x, y=y, r=r)
            for p in self.active():
                if dist(p.x, p.y, x, y) <= r + 5:
                    combat.hurt_player(self, p, p.max_hp * c["aoe_pct"] / 100, now, by=b.eid)
        if self.puzzle is not None and self.tick_count % 10 == 0:
            self.push_puzzle(now)   # boss health, phase and shield progress twice a second

    def tick(self, dt_: float, now: float) -> None:
        super().tick(dt_, now)
        if self.phase == "ended":
            if now >= self.end_at:
                for p in list(self.players.values()):
                    m = self.members.get(p.user_id)
                    if m is not None and m.state == "in":
                        m.state = "left"
                    self._exit(p)
            return
        if self.phase == "starting":
            return
        if not any(m.state == "in" for m in self.members.values()) or not self.players:
            self._finish("abandoned", now)
            return
        if now >= self.deadline:
            self._finish("timeout", now)
            return
        present = self.present()
        if present and all(p.dead for p in present):
            self._finish("failed", now)
            return
        if self.phase == "advancing":
            if now >= self.advance_at:
                self._advance(now)
            return
        if self.puzzle is not None:
            self.puzzle.tick(dt_, now)
        if self.kind == "boss":
            self._boss_tick(now)
        if self.puzzle is not None and self.puzzle.solved and self.phase == "running" \
                and all(not m.alive for m in self.monsters):
            self._room_cleared(now)


# ------------------------------------------------------------------ the service in the world
class RealmService:
    def __init__(self, world: "World"):
        self.world = world
        self.instances: dict[int, RealmInstance] = {}
        self.rifts: dict[str, Rift] = {}
        self.queues: dict[str, list[list]] = {}          # key (realm id or 'rift:<id>') -> [[uid, since]]
        self.queued: dict[int, str] = {}                 # uid -> key
        self.starting: set[int] = set()                  # players whose entry is being written
        self.rng = random.Random()
        self.room_order: list[str] | None = None         # tests: a fixed room order
        self.seed: int | None = None                     # tests and bots: the next runs' random monsters
        self._rift_ids = itertools.count(1)
        self._next_rift = 0.0
        self._next_queue = 0.0
        self._next_announce = 0.0
        self._announced: set[tuple] = set()

    def instance_of(self, p: Player | None) -> RealmInstance | None:
        ch = p.channel if p is not None else None
        return ch if isinstance(ch, RealmInstance) else None

    # ------------------------------------------------------------ checks
    def _err(self, s: "Session", code: str, text: str) -> None:
        s.send(protocol.error(code, text))

    def check_members(self, uids: list[int], rdef: dict, starting_ok: bool = False) -> str | None:
        """Can these players step in right now? (Nothing here reads the cultivation realms: every
        question is asked at the player's own math floor.)"""
        for uid in uids:
            s = self.world.sessions.get(uid)
            p = self.world.players.get(uid)
            if s is None:
                return "Có thành viên đang ngoại tuyến."
            if p is None or p.channel is None:
                return f"{s.name} đang ở động phủ, hãy ra Trúc Lâm Thôn trước."
            if self.instance_of(p) is not None:
                return f"{s.name} đang ở trong một bí cảnh khác."
            if p.dead:
                return f"{s.name} đang trọng thương."
            if uid in self.starting and not starting_ok:
                return f"{s.name} đang vào một bí cảnh khác."
        return None

    def _near_gate(self, p: Player) -> bool:
        if p.channel is None or p.channel.zone_id != VILLAGE or self.instance_of(p):
            return False
        gate = p.channel.map.interacts.get("realm")
        return gate is not None and dist(p.x, p.y, *gate) <= 90

    def _near_rift(self, p: Player, r: Rift) -> bool:
        return p.channel is r.channel and dist(p.x, p.y, r.x, r.y) <= cfg()["rift"]["use_radius"]

    def _target(self, s: "Session", m: protocol.RealmCmd) -> tuple[str, str] | None:
        """(realm id, queue key) of what the player asks for, or None after an error."""
        p = s.player
        if m.rift:
            r = self.rifts.get(m.rift)
            if r is None or r.expires <= self.world.mono():
                self._err(s, "rift_gone", "Khe nứt đã khép lại mất rồi.")
                return None
            if p is None or not self._near_rift(p, r):
                self._err(s, "too_far", "Hãy đứng sát khe nứt.")
                return None
            return r.realm_id, f"rift:{r.id}"
        rdef = realm_defs().get(m.realm or "")
        if rdef is None or rdef["kind"] not in GATE_KINDS:
            self._err(s, "no_realm", "Không có bí cảnh này.")
            return None
        if rdef["kind"] == "scheduled" and not window_status(clock.now())["open"]:
            self._err(s, "realm_closed", "Bí cảnh chưa mở cửa. Xem giờ mở ở Cổng Bí Cảnh.")
            return None
        if p is None or not self._near_gate(p):
            self._err(s, "too_far", "Hãy tới Cổng Bí Cảnh ở Trúc Lâm Thôn.")
            return None
        return m.realm, m.realm

    # ------------------------------------------------------------ messages
    def handle(self, s: "Session", m: protocol.RealmCmd) -> None:
        now = self.world.mono()
        if m.op == "leave":
            inst = self.instance_of(s.player)
            if inst is None:
                self._err(s, "not_in_realm", "Bạn không ở trong bí cảnh.")
            else:
                inst.leave(s.player, now)
            return
        if m.op == "unqueue":
            self.unqueue(s.user_id)
            return
        target = self._target(s, m)
        if target is None:
            return
        realm_id, key = target
        rdef = realm_defs()[realm_id]
        party = self.world.parties.party_of(s.user_id)
        if m.op == "queue":
            if party is not None:
                self._err(s, "in_party", "Tổ đội thì đội trưởng bấm Vào bí cảnh; hàng chờ dành cho người đi một mình.")
                return
            err = self.check_members([s.user_id], rdef)
            if err:
                self._err(s, "cannot_enter", err)
                return
            self.unqueue(s.user_id, notify=False)
            self.queues.setdefault(key, []).append([s.user_id, now])
            self.queued[s.user_id] = key
            self._queue_news(key)
            return
        c = cfg()
        pmin = int(rdef.get("party_min", c["party_min"]))
        if party is None and pmin <= 1:   # a realm one may also enter alone
            err = self.check_members([s.user_id], rdef)
            if err:
                self._err(s, "cannot_enter", err)
                return
            self.start([s.user_id], realm_id)
            return
        if party is None or len(party.members) < pmin:
            self._err(s, "need_party", f"Cần tổ đội {pmin}-{c['party_max']} người. "
                                       "Mời bạn vào đội, hoặc vào hàng chờ ghép đội.")
            return
        if party.leader != s.user_id:
            self._err(s, "not_leader", "Chỉ đội trưởng mới dẫn đội vào bí cảnh.")
            return
        err = self.check_members(party.members, rdef)
        if err:
            self._err(s, "cannot_enter", err)
            return
        self.start(list(party.members), realm_id)

    # ------------------------------------------------------------ entering
    def start(self, uids: list[int], realm_id: str) -> None:
        self.starting |= set(uids)
        for uid in uids:
            self.unqueue(uid, notify=False)
            self.world.notify(uid, {"t": "realm", "event": "entering", "realm": realm_id,
                                    "name_vi": realm_defs()[realm_id]["name_vi"]})
        self.world.spawn(self._start(list(uids), realm_id))

    async def _start(self, uids: list[int], realm_id: str) -> None:
        from .. import db as dbm
        from ..systems import secret_realm
        rdef = realm_defs()[realm_id]
        try:
            try:
                async with dbm.SessionLocal() as db:
                    over = await secret_realm.over_limit(db, uids, realm_id)
                    if over:
                        names = ", ".join(self.world.sessions[u].name for u in over if u in self.world.sessions)
                        for uid in uids:
                            self.world.notify(uid, protocol.error(
                                "daily_limit", f"{names} đã vào {rdef['name_vi']} "
                                               f"{secret_realm.daily_limit(realm_id)} lần hôm nay rồi."))
                        return
                    floors = await secret_realm.math_floors(db, uids)   # everyone must have a floor with questions
                    none = [u for u in uids if floors.get(u) is None]
                    if none:
                        names = ", ".join(self.world.sessions[u].name for u in none if u in self.world.sessions)
                        for uid in uids:
                            self.world.notify(uid, protocol.error(
                                "no_math_question", f"{names} chưa có tầng toán nào có câu hỏi."))
                        return
                    run_id = await secret_realm.create_run(db, realm_id, uids)
                    await db.commit()
            except Exception:
                log.exception("could not open a realm run")
                for uid in uids:
                    self.world.notify(uid, protocol.error("realm_error", "Bí cảnh chưa mở được, thử lại sau nhé."))
                return
            err = self.check_members(uids, rdef, starting_ok=True)
            if err:   # someone walked off while the gate was opening: nobody loses an entry
                await secret_realm.abort_run(run_id)
                for uid in uids:
                    self.world.notify(uid, protocol.error("cannot_enter", err))
                return
            members = {uid: Member(uid, self.world.sessions[uid].name, floor=floors.get(uid)) for uid in uids}
            try:
                rng = random.Random(self.seed) if self.seed is not None else random.Random()
                inst = RealmInstance(self.world, run_id, realm_id, members, rng, rooms=self.room_order)
            except Exception:
                log.exception("could not build a realm run")
                await secret_realm.abort_run(run_id)
                for uid in uids:
                    self.world.notify(uid, protocol.error("realm_error", "Bí cảnh chưa mở được, thử lại sau nhé."))
                return
            self.instances[run_id] = inst
            inst.begin(self.world.mono())
        finally:
            self.starting -= set(uids)

    # ------------------------------------------------------------ the queue (spec 14.1)
    def unqueue(self, uid: int, notify: bool = True) -> None:
        key = self.queued.pop(uid, None)
        if key is None:
            return
        self.queues[key] = [e for e in self.queues.get(key, []) if e[0] != uid]
        if not self.queues[key]:
            del self.queues[key]
        if notify:
            self.world.notify(uid, {"t": "realm", "event": "unqueued"})
        if key in self.queues:
            self._queue_news(key)

    def queue_of(self, uid: int) -> dict | None:
        key = self.queued.get(uid)
        if key is None:
            return None
        realm_id = self.rifts[key[5:]].realm_id if key.startswith("rift:") and key[5:] in self.rifts else key
        return {"key": key, "realm": realm_id, "waiting": len(self.queues.get(key, []))}

    def _queue_news(self, key: str) -> None:
        for e in self.queues.get(key, []):
            self.world.notify(e[0], {"t": "realm", "event": "queued", **(self.queue_of(e[0]) or {})})

    def _queue_tick(self, now: float) -> None:
        """Solo players waiting for the same realm (or rift) become a party once `party_max`
        wait, or `party_min` have waited `fill_seconds`. Nobody is grouped by cultivation realm:
        each one is asked at their own floor."""
        c = cfg()
        pmin, pmax, fill = c["party_min"], c["party_max"], c["queue"]["fill_seconds"]
        for key in list(self.queues):
            rift = self.rifts.get(key[5:]) if key.startswith("rift:") else None
            realm_id = rift.realm_id if rift else key
            keep = []
            for e in self.queues[key]:
                p = self.world.players.get(e[0])
                ok = (e[0] in self.world.sessions and p is not None and p.channel is not None and not p.dead
                      and self.instance_of(p) is None and e[0] not in self.starting
                      and self.world.parties.party_of(e[0]) is None
                      and (rift is not None and self._near_rift(p, rift) if key.startswith("rift:") else True))
                if ok:
                    keep.append(e)
                else:
                    self.queued.pop(e[0], None)
                    self.world.notify(e[0], {"t": "realm", "event": "unqueued"})
            taken: set[int] = set()
            if len(keep) >= pmax or (len(keep) >= pmin and now - min(x[1] for x in keep) >= fill):
                g = sorted(keep, key=lambda x: x[1])[:pmax]
                uids = [x[0] for x in g]
                taken = set(uids)
                for uid in uids:
                    self.queued.pop(uid, None)
                self.world.parties.form(uids)
                err = self.check_members(uids, realm_defs()[realm_id])
                if err:
                    for uid in uids:
                        self.world.notify(uid, protocol.error("cannot_enter", err))
                else:
                    self.start(uids, realm_id)
            self.queues[key] = [e for e in keep if e[0] not in taken]
            if not self.queues[key]:
                del self.queues[key]

    # ------------------------------------------------------------ rifts (spec 14.1)
    def spawn_rift(self, ch: ChannelZone, now: float, x: float | None = None, y: float | None = None) -> Rift:
        rc = cfg()["rift"]
        if x is None or y is None:
            players = list(ch.players.values())
            base = self.rng.choice(players) if players else None
            x, y = (base.x, base.y) if base else (ch.map.width_px / 2, ch.map.height_px / 2)
            for _ in range(40):
                a, d = self.rng.uniform(0, 6.283), self.rng.uniform(70, 170)
                tx, ty = x + math.cos(a) * d, y + math.sin(a) * d
                if 24 < tx < ch.map.width_px - 24 and 24 < ty < ch.map.height_px - 24 and not ch.map.collider.blocked(tx, ty):
                    x, y = tx, ty
                    break
        r = Rift(f"r{next(self._rift_ids)}", rc["realm"], ch, float(x), float(y), now + rc["life_seconds"], now)
        self.rifts[r.id] = r
        ch.extras.append(r)
        name = realm_defs()[r.realm_id]["name_vi"]
        for p in ch.players.values():
            if p.session is not None and dist(p.x, p.y, r.x, r.y) <= 420:
                p.session.send({"t": "notice", "text": f"Một {name} vừa rách ra gần đây! Rủ nhau vào trước khi nó khép lại."})
        return r

    def _rift_tick(self, now: float) -> None:
        for rid, r in list(self.rifts.items()):
            r.now = now
            if now >= r.expires:
                del self.rifts[rid]
                if r in r.channel.extras:
                    r.channel.extras.remove(r)
        if now < self._next_rift:
            return
        rc = cfg()["rift"]
        self._next_rift = now + rc["check_seconds"]
        for zone_id in rc["zones"]:
            for ch in self.world.channels.get(zone_id, []):
                if len(self.rifts) >= rc["max_open"]:
                    return
                if ch.players and not any(r.channel is ch for r in self.rifts.values()) \
                        and self.rng.random() < rc["chance"]:
                    self.spawn_rift(ch, now)

    # ------------------------------------------------------------ announcements (spec 14.1)
    def _announce_tick(self) -> None:
        c = cfg()
        if c.get("always_open"):
            return
        st = window_status(clock.now())
        names = [r["name_vi"] for r in realm_defs().values() if r["kind"] == "scheduled"]
        if not names:
            return
        if st["open"]:
            key = ("open", int(clock.now().timestamp() + st["closes_in"]) // 60)
            text = f"{', '.join(names)} đã mở cửa ở Cổng Bí Cảnh (Trúc Lâm Thôn), còn {st['closes_in'] // 60} phút!"
        elif st["opens_in"] <= c["schedule"]["announce_minutes"] * 60:
            key = ("soon", int(clock.now().timestamp() + st["opens_in"]) // 60)
            text = f"{', '.join(names)} sẽ mở cửa sau {max(1, round(st['opens_in'] / 60))} phút. Lập tổ đội đi thôi!"
        else:
            return
        if key in self._announced:
            return
        self._announced.add(key)
        for s in list(self.world.sessions.values()):
            s.send({"t": "notice", "text": text})

    # ------------------------------------------------------------ tick
    def tick(self, dt_: float, now: float, server_time: float, snap_every: int) -> None:
        for inst in list(self.instances.values()):
            inst.tick(dt_, now)
            if inst.tick_count % snap_every == 0 and inst.awake:
                for p in inst.players.values():
                    if p.session is not None:
                        p.session.send(inst.snapshot_for(p, server_time))
                inst.events = []
            elif not inst.awake:
                inst.events = []
            if inst.phase == "ended" and not inst.players:
                del self.instances[inst.run_id]
        self._rift_tick(now)
        if now >= self._next_queue:
            self._next_queue = now + cfg()["queue"]["check_seconds"]
            self._queue_tick(now)
        if now >= self._next_announce:
            self._next_announce = now + 5.0
            self._announce_tick()
