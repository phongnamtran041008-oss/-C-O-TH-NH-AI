"""A bot that plays a bí cảnh through the real protocol (stage 9 test criterion: three players
clear a realm together). It only uses what a player has: the messages its own session gets
and the map file every client has. It moves with `in` messages, fights with `atk`, steps on
the Trận Nhãn seals and answers the math questions through POST /quiz/answer like the game
does (the answer key standing in for a player who studied).

Bots in a team share what they see on screen, like players talking in the party chat: the
`Team` object is that chat.
"""
from __future__ import annotations

import math
from collections import deque

from app.realtime import maps
from tests.test_math_loop import right_answer as math_right_answer

STEP = 4   # path grid in pixels


def right_answer_any(q: dict, key: dict) -> dict:
    """The right answer to what a bí cảnh asks (always a math question)."""
    return math_right_answer(q, key)


def path(col, start, goal, avoid=()) -> list[tuple[float, float]]:
    """Breadth-first path over a 4 px grid of foot positions the collider allows.

    `avoid` keeps the route out of places the bot must not tread on the way - the other seals of
    a Trận Nhãn, say. What it must not do is keep the bot *where it already is*: a bot that
    has just stepped on a stone is standing inside one of those places, and forbidding it outright
    leaves the search with no legal first step at all, so the bot stays on that stone for ever and
    the room never finishes. So when no route is found, look again while allowing the places the
    bot is standing in: it may walk out of the one it is in, never into the others.
    """
    def covers(a, x, y) -> bool:
        return a.x - 2 <= x <= a.x + a.w + 2 and a.y - 2 <= y <= a.y + a.h + 2

    def search(keep_out) -> list[tuple[float, float]]:
        def ok(x, y):
            if col.blocked(x, y):
                return False
            return not any(covers(a, x, y) for a in keep_out)

        # cell centres sit in the middle of one-tile corridors (feet x = tile + 8, y = tile + 11)
        def cell(x, y):
            return round(x / STEP), round((y - 3) / STEP)

        def center(c):
            return c[0] * STEP + 0.0, c[1] * STEP + 3.0
        s, g = cell(*start), cell(*goal)
        if not ok(*center(g)):   # the exact goal is inside something: the nearest open cell
            best = None
            for r in range(1, 8):
                for dx in range(-r, r + 1):
                    for dy in range(-r, r + 1):
                        c = (g[0] + dx, g[1] + dy)
                        if ok(*center(c)) and (best is None or abs(dx) + abs(dy) < best[0]):
                            best = (abs(dx) + abs(dy), c)
                if best:
                    break
            if best is None:
                return []
            g = best[1]
        prev = {s: None}
        q = deque([s])
        while q:
            c = q.popleft()
            if c == g:
                break
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + d[0], c[1] + d[1])
                if n not in prev and ok(*center(n)):
                    prev[n] = c
                    q.append(n)
        if g not in prev:
            return []
        out, c = [], g
        while c is not None and c != s:
            out.append(center(c))
            c = prev[c]
        return list(reversed(out))

    out = search(list(avoid))
    if out or not any(covers(a, *start) for a in avoid):
        return out
    return search([a for a in avoid if not covers(a, *start)])


class Team:
    def __init__(self):
        self.bots: list["Bot"] = []
        self.assign: dict[int, object] = {}


class Bot:
    def __init__(self, world, client, headers, uid, session, team: Team, answer):
        self.w, self.client, self.h, self.uid, self.s = world, client, headers, uid, session
        self.team = team
        team.bots.append(self)
        self.answer = answer          # async (session, question) -> grade result
        self.seen = 0
        self.room: dict | None = None
        self.puzzle: dict | None = None
        self.run: dict | None = None
        self.ended: dict | None = None
        self.loot: list[dict] = []
        self.qs: list[dict] = []
        self.answered: set[str] = set()
        self.seq = 0
        self.goal = None
        self.route: list = []
        self.next_atk = 0.0
        self.log: list[str] = []

    @property
    def p(self):
        return self.w.players.get(self.uid)

    @property
    def inst(self):
        return self.w.realms.instance_of(self.p)

    def send(self, msg: dict):
        return self.w.handle(self.s, msg)

    # ------------------------------------------------------------ reading the screen
    def read(self) -> None:
        for m in self.s.sent[self.seen:]:
            t, ev = m.get("t"), m.get("event")
            if t == "q":
                self.qs.append(m)
            elif t == "realm" and ev == "start":
                self.run = m["run"]
            elif t == "realm" and ev == "room":
                self.room, self.puzzle = m, m["puzzle"]
                self.goal, self.route = None, []
            elif t == "realm" and ev == "puzzle":
                self.puzzle = m["puzzle"]
            elif t == "realm" and ev == "end":
                self.ended = m
            elif t == "realm" and ev == "loot":
                self.loot.append(m["loot"])
        self.seen = len(self.s.sent)

    # ------------------------------------------------------------ moving
    def go(self, x: float, y: float, avoid=()) -> None:
        p = self.p
        if p is None:
            return
        if self.goal is None or math.hypot(self.goal[0] - x, self.goal[1] - y) > 1 or not self.route:
            self.goal = (x, y)
            self.route = path(p.channel.map.collider, (p.x, p.y), (x, y), avoid)

    def stop(self) -> None:
        self.goal, self.route = None, []

    async def move(self) -> None:
        p = self.p
        if p is None or not self.route or p.protected(self.w.mono()):
            return
        while self.route and math.hypot(self.route[0][0] - p.x, self.route[0][1] - p.y) < 0.2:
            self.route.pop(0)
        if not self.route:
            return
        tx, ty = self.route[0]
        dx, dy = tx - p.x, ty - p.y
        if abs(dy) > 0.1:
            d, step = abs(dy), (0, 1 if dy > 0 else -1)
        else:
            d, step = abs(dx), (1 if dx > 0 else -1, 0)
        ms = max(1, min(50, int(round(d / 74.0 * 1000))))
        await self.send({"t": "in", "s": self.seq, "k": [[step[0], step[1], ms]]})
        self.seq += 1

    def near(self, x, y, r=3.0) -> bool:
        p = self.p
        return p is not None and math.hypot(p.x - x, p.y - y) <= r

    # ------------------------------------------------------------ fighting
    async def answer_questions(self) -> None:
        for q in self.qs:
            sid = q["q"]["session_id"]
            if sid in self.answered:
                continue
            self.answered.add(sid)
            await self.answer(self, q["q"])
        self.qs = []

    async def fight(self, monsters) -> bool:
        """Walks to the nearest living monster and hits it. False when none is left."""
        p = self.p
        alive = [m for m in monsters if m.alive]
        if not alive or p is None:
            return False
        m = min(alive, key=lambda m: math.hypot(m.x - p.x, m.y - p.y))
        if math.hypot(m.x - p.x, m.y - 6 - (p.y - 6)) > 18:
            self.goal, self.route = None, []
            self.go(m.x, m.y + 6)
        elif self.w.mono() >= self.next_atk:
            self.next_atk = self.w.mono() + 0.7
            await self.send({"t": "atk", "id": m.eid})
        return True

    # ------------------------------------------------------------ the rooms
    def standby(self):
        a = self.inst.map.rooms[self.inst.place]
        i = self.team.bots.index(self)
        return a.x + a.w / 2 - 40 + 40 * i, a.y + a.h - 30

    async def think(self) -> None:
        self.read()
        await self.answer_questions()
        inst, p = self.inst, self.p
        if inst is None or p is None or self.room is None or inst.phase != "running" or p.dead:
            await self.move()
            return
        if await self.fight(inst.monsters) or inst.kind == "boss":
            await self.move()
            return
        getattr(self, f"play_{inst.kind}")()
        await self.move()

    def play_seal(self) -> None:
        """Trận Nhãn (M10): the ones who have not broken a seal yet pick first, one seal each;
        everybody walks round the other seals so as not to be asked on the way."""
        pz = self.puzzle or {}
        seals = {o.name: o for o in self.inst.objs(pz.get("seal_kind", "pedestal"))}
        open_ = [s["name"] for s in pz.get("seals", []) if not s["broken"] and s["name"] in seals]
        if not open_:
            self.go(*self.standby(), avoid=list(seals.values()))
            return
        missing = set(pz.get("missing", []))
        order = sorted(self.team.bots, key=lambda b: (b.uid not in missing, self.team.bots.index(b)))
        target = open_[order.index(self) % len(open_)]
        o = seals[target]
        self.go(o.x + o.w / 2, o.y + o.h / 2, avoid=[x for n, x in seals.items() if n != target])



def realm_map():
    return maps.load("bi_canh")
