"""The lands of a realm (the `lands` section of data/math/world_plan.json, "Thiên Địa Đồ"),
wired through `wired_sections`: which land a zone is, who may walk into it, and what its
monsters ask.

**Entry.** A land opens at a stage of Đạo Thụ in its realm (`opens.stage`) with some nodes
done (`opens.nodes`). "Tu vi" here is the player's place in the curriculum tree
(systems/math_tree_progress.py: the stage reached and the done nodes, a vacant node counting
as done as everywhere else), never the character's cultivation realm, which keeps its own
older rule (`recommended_realm` in zones.json, world.may_enter). The world checks it on
every way in - through a portal and when a reconnecting player is put back where they were -
so a client cannot walk around it; a refusal names in Vietnamese what is missing.

The check is synchronous (the world's join runs in the tick), so it reads a `TreePos` kept on
the session: loaded with the character (world._load_combat) and read again right before a
portal join into a gated land (world.handle), since nodes get done between two walks.

**Questions.** A zone that is a land of a branch carries a `question_source` (realtime/combat.py
calls it, for a blow that landed or for Vấn Đạo alike):

* a quái lỗi sai (data/math/monsters.json with a `skill`) keeps asking its own micro-skill;
* a land creature stands for some nodes of the tree (`nodes`): it asks a part of those nodes
  the player may practise (open or done), at the player's own tier;
* with none of them open yet - and for the old creatures that have no nodes - it asks where
  the player is learning in the land's branch (the frontier of its subject, R9);
* the Lập Trình and Thực Chiến nodes are programming exercises with no question: their
  creatures stand for the math nodes those nodes reinforce (`reinforces` in tree.json);
* `"ask": "branches"` (Thiên Kiếp Lôi Long, Lôi Kiếp Đài) asks the four math branches in turn,
  each time the hardest question this player may be asked there.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

from ..learning import math_tree

if TYPE_CHECKING:
    from .ai import Monster
    from .zone import Player

MATH_BRANCHES = ("ds", "gt", "xs", "tr")
NO_QUESTION_VI = ("Chưa có câu toán nào cho vùng đất này ở bậc của con. "
                  "Luyện ở Động Phủ một lúc rồi quay lại!")


def wired() -> bool:
    return math_tree.section_wired("lands")


@lru_cache(maxsize=1)
def _lands() -> dict[str, dict]:
    return {l["id"]: l for l in math_tree.world_plan().get("lands", [])}


def land(land_id: str | None) -> dict | None:
    return _lands().get(land_id) if land_id else None


def zone_land_id(zone_id: str | None) -> str | None:
    """The land a zone of zones.json is (its `land`), or None."""
    from .world import zone_defs
    z = zone_defs().get(zone_id or "")
    return z.get("land") if z else None


def zone_land(zone_id: str | None) -> dict | None:
    return land(zone_land_id(zone_id))


def zone_of(land_id: str) -> str | None:
    """The zone id of a land (the reused maps keep their old zone ids)."""
    from .world import zone_defs
    return next((zid for zid, z in zone_defs().items() if z.get("land") == land_id), None)


def gated(zone_id: str | None) -> bool:
    """Does walking into this zone depend on the player's place in Đạo Thụ?"""
    if not wired():
        return False
    l = zone_land(zone_id)
    if l is None:
        return False
    opens = l.get("opens") or {}
    return bool(opens.get("stage")) or bool(opens.get("nodes"))


# ------------------------------------------------------------------ entry
@dataclass(frozen=True)
class TreePos:
    """Where a player stands in Đạo Thụ, as far as the doors of the lands care."""
    realm: str
    stage: int
    done: frozenset

    @classmethod
    def newcomer(cls) -> "TreePos":
        t = math_tree.tree()
        first = min(t.realm_order, key=t.realm_order.get)
        return cls(first, 0, frozenset())


def pos_of(st) -> TreePos:
    """From a math_tree_progress.TreeState."""
    realm, stage = st.stage
    return TreePos(realm, int(stage), frozenset(st.done))


async def load_pos(db, user_id: int) -> TreePos:
    from ..systems import math_tree_progress
    return pos_of(await math_tree_progress.state(db, user_id))


def _realm_vi(realm: str) -> str:
    raw = math_tree.tree().raw
    return next((r["name_vi"] for r in raw.get("realms", []) if r["id"] == realm), realm)


def missing(l: dict, pos: TreePos | None) -> tuple[int | None, list[str]]:
    """(the stage still to reach or None, the nodes still to finish) for this land."""
    t = math_tree.tree()
    pos = pos or TreePos.newcomer()
    opens = l.get("opens") or {}
    need = int(opens.get("stage", 0) or 0)
    stage_short = None if t.reaches(l["realm"], need, (pos.realm, pos.stage)) else need
    nodes = [n for n in opens.get("nodes", []) if n not in pos.done]
    return stage_short, nodes


def refusal_vi(l: dict, pos: TreePos | None) -> str | None:
    """None when the player may walk in; else why not, naming what is missing."""
    stage, nodes = missing(l, pos)
    if stage is None and not nodes:
        return None
    pos = pos or TreePos.newcomer()
    t = math_tree.tree()
    pieces = []
    if stage is not None:
        here = f"tầng {pos.stage}" if pos.realm == l["realm"] else f"{_realm_vi(pos.realm)} tầng {pos.stage}"
        pieces.append(f"cần tu vi {_realm_vi(l['realm'])} tầng {stage} (con đang ở {here})")
    if nodes:
        pieces.append("học xong " + ", ".join(t.nodes[n].name_vi if n in t.nodes else n for n in nodes))
    return f"Chưa vào được {l['name_vi']}: " + " và ".join(pieces) + "."


def refusal(zone_id: str | None, pos: TreePos | None) -> str | None:
    """Why this player may not walk into this zone (None: they may)."""
    if not gated(zone_id):
        return None
    return refusal_vi(zone_land(zone_id), pos)


def view(pos: TreePos | None) -> list[dict]:
    """Every land of the plan with its zone and whether this player may walk in."""
    out = []
    for l in _lands().values():
        zid = zone_of(l["id"]) if l.get("status") == "co" else None
        why = refusal_vi(l, pos) if zid else None
        out.append({"id": l["id"], "name_vi": l["name_vi"], "branch": l.get("branch"), "zone": zid,
                    "built": zid is not None, "open": zid is not None and why is None, "reason_vi": why})
    return out


# ------------------------------------------------------------------ questions
def _subject(branch: str | None) -> str | None:
    if branch is None:
        return None
    raw = math_tree.tree().raw
    return next((b.get("subject") for b in raw.get("branches", []) if b["id"] == branch), None)


class LandAsker:
    """The `question_source` of a channel that is a land: see the module docstring."""

    def __init__(self, l: dict):
        self.land = l
        self.turns: dict[tuple[int, str], int] = {}   # (user, monster) -> boss questions asked

    async def __call__(self, db, user, p: "Player", m: "Monster | None", rng: random.Random):
        from ..systems import math_combat, math_tree_progress
        info = m.info if m is not None else {}
        if math_combat.is_mistake_monster(info):        # a quái lỗi sai keeps its own micro-skill
            from . import combat
            return await combat._math_question(db, user, p, info, rng)
        st = await math_tree_progress.state(db, user.id)
        q = None
        if info.get("ask") == "branches" and m is not None:
            q = await self._boss(db, user, st, p, m, info, rng)
        elif info.get("nodes"):
            q = await self._of_nodes(db, user, st, info["nodes"], rng)
        if q is None:
            q = await self._of_branch(db, user, st, info, rng)
        if q is None:
            from . import combat
            p.no_question_until = combat._world().mono() + 10
            if p.session is not None:
                p.session.send({"t": "error", "code": "no_math_question", "message_vi": NO_QUESTION_VI})
            return None
        q.meta["monster_vi"] = info.get("name_vi", "")
        q.meta["land_vi"] = self.land.get("name_vi", "")
        return math_combat.CONTEXT, q

    @staticmethod
    async def _pick(db, user, part, rng, highest: bool = False):
        from ..systems import math_ask, math_combat
        skills = list(part.skills)
        rng.shuffle(skills)
        return await math_ask.pick(db, user, part.subject_id, part.floor, skills=skills,
                                   qtypes=math_combat.QUICK_TYPES, highest=highest, rng=rng)

    def _playable(self, st, nodes) -> list:
        from ..systems import math_tree_progress
        return [part for n in nodes if n in st.tree.nodes for part in math_tree_progress.parts(n)
                if st.playable(part)]

    async def _of_nodes(self, db, user, st, nodes, rng):
        parts = self._playable(st, nodes)
        rng.shuffle(parts)
        for part in parts:
            q = await self._pick(db, user, part, rng)
            if q is not None:
                return q
        return None

    async def _frontier(self, db, user, st, subject: str, rng, highest: bool = False):
        from ..systems import math_tree_progress
        part = math_tree_progress.frontier_of(st, subject)
        return await self._pick(db, user, part, rng, highest) if part is not None else None

    async def _of_branch(self, db, user, st, info: dict, rng):
        """Where the player is learning in the land's branch; for a land of exercises, in the
        branches its creature's nodes come from."""
        subject = _subject(self.land.get("branch"))
        if subject:
            subjects = [subject]
        else:
            t = st.tree
            subjects = list(dict.fromkeys(_subject(t.nodes[n].branch) for n in info.get("nodes", [])
                                          if n in t.nodes))
            subjects = [s for s in subjects if s]
            rng.shuffle(subjects)
        for s in subjects:
            q = await self._frontier(db, user, st, s, rng)
            if q is not None:
                return q
        return None

    async def _boss(self, db, user, st, p, m, info: dict, rng):
        """The four math branches in turn, each time the hardest question this player may be
        asked there: the most advanced part of the branch they may practise, its highest tier."""
        key = (p.user_id, m.eid)
        i = self.turns.get(key, 0)
        self.turns[key] = i + 1
        order = MATH_BRANCHES[i % 4:] + MATH_BRANCHES[:i % 4]
        t = st.tree
        for b in order:
            nodes = [n for n in info.get("nodes", []) if n in t.nodes and t.nodes[n].branch == b]
            parts = self._playable(st, nodes)
            for part in reversed(parts):              # the most advanced first (tree order)
                q = await self._pick(db, user, part, rng, highest=True)
                if q is not None:
                    return q
            subject = _subject(b)
            q = await self._frontier(db, user, st, subject, rng, highest=True) if subject else None
            if q is not None:
                return q
        return None


def asker_for(zone_id: str | None) -> LandAsker | None:
    """The question source of a channel of this zone, or None (a zone that is no land, the hub)."""
    if not wired():
        return None
    l = zone_land(zone_id)
    if l is None or l.get("kind") == "hub":
        return None
    return LandAsker(l)
