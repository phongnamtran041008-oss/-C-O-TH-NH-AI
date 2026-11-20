"""Đạo Thụ: the curriculum as a tree instead of one subject after another.

`data/math/tree.json` groups the micro-skills of the four subject files (plus programming and
"thực chiến AI" nodes that have no micro-skills yet) into **nodes**. A node opens when every
node it `requires` is done - including nodes of other branches, which is what lets the
branches be learned side by side - and it names the older nodes it `reinforces`, where its
review questions come from. `data/math/world_plan.json` hangs the game on the same nodes:
lands, the weapons lying in them, spirit beasts and the abilities a realm stage unlocks.

This module only reads and checks those two files and answers questions about them with pure
functions. The **tree is wired** (`"wired": true` in tree.json, approved by the author on
2026-11-19): systems/math_tree_progress.py reads it to decide which nodes a player has open
and done, and the question loop (systems/math_practice.py) sits down on the parts of a node
(a floor of math_path.py is still the address of the questions). The world plan as a whole is
not wired yet (`"wired": false` in world_plan.json): what lies beyond Luyện Khí is a design.
Parts of it are: `"wired_sections"` names the sections the game already runs on although the
whole plan is not (the combat rule "questions only when a monster hits you", realtime/combat.py;
the lands of Luyện Khí - their maps, creatures and doors, realtime/lands.py; the weapons lying in
them, systems/weapons.py; the beasts of Luyện Khí and their taming, realtime/beasts.py; the thần
thông of Luyện Khí, realtime/abilities.py). A wired section is checked harder - every number the game reads must be
there and make sense - because a typo in it is a bug in the game, not in a design document.

What `validate()` guarantees, because a wrong tree would teach things in the wrong order:

* every micro-skill of every subject is in exactly one place: a main-path node (`chinh`), an
  optional node (`phu`) or the `cut` list;
* a node never needs something that comes later: no cycles, and a required node is in the
  same realm at the same or an earlier stage, or in an earlier realm;
* the tree agrees with the micro-skill prerequisites inside the subject files: every
  prerequisite of a node's skill is in the node itself or in one of its ancestors - unless a
  `waiver` drops it by name, and a main-path skill never leans on an optional one;
* `reinforces` only names ancestors (you cannot review what you have not learned);
* every main-path node of a realm leads to that realm's project (`du_an`), so nothing dangles;
* the world plan only names real nodes, lands, weapons and unlocks, and never asks for a
  node that belongs to a later stage than the one it says it needs.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from . import math_path

MATH_DIR = math_path.MATH_DIR
TREE_FILE = "tree.json"
WORLD_FILE = "world_plan.json"

STATUSES = ("chinh", "phu")
CONTENT = ("co", "dang_viet", "chua_co")
KINDS = ("toan", "code", "thuc_chien", "du_an", "hoc_may", "hoc_sau", "he_thong", "nghien_cuu", "dan_dat")
QUESTION_RULES = ("on_hit",)
# the parts of world_plan.json the game can run on by themselves: 'beasts' is the beasts with their
# taming rule (beast_taming), 'abilities' the thần thông of the unlocks that have content
WIREABLE_SECTIONS = ("combat", "lands", "weapons", "beasts", "abilities")
GIFT_TYPES = ("sniff", "wrong_guard", "dodge_cooldown", "parry_fire", "mount")
ABILITY_BLOCKS = {"phap_tran": "formation", "dap_kiem_luot": "glide", "cuoi_linh_thu": "ride"}
TELEGRAPH_SHAPES = ("circle", "cone", "line")
RANKS = ("normal", "elite", "boss")


# ------------------------------------------------------------------ data
@dataclass(frozen=True)
class Node:
    id: str
    branch: str
    realm: str
    stage: int | None
    status: str
    kind: str
    content: str
    name_vi: str
    why_vi: str
    skills: tuple[str, ...]
    requires: tuple[str, ...]
    reinforces: tuple[str, ...]
    topics_vi: tuple[str, ...] = ()
    problems: tuple[str, ...] = ()

    @property
    def main(self) -> bool:
        return self.status == "chinh"


@dataclass(frozen=True)
class Tree:
    raw: dict
    nodes: dict[str, Node]
    realm_order: dict[str, int]
    realm_stages: dict[str, int]

    # ---- structure
    def ancestors(self, node_id: str) -> set[str]:
        """Every node that must be done before this one, directly or not."""
        seen: set[str] = set()
        stack = list(self.nodes[node_id].requires)
        while stack:
            n = stack.pop()
            if n in seen or n not in self.nodes:
                continue
            seen.add(n)
            stack.extend(self.nodes[n].requires)
        return seen

    def main_nodes(self, realm: str | None = None) -> list[Node]:
        return [n for n in self.nodes.values() if n.main and (realm is None or n.realm == realm)]

    def node_of_skill(self) -> dict[str, str]:
        return {s: n.id for n in self.nodes.values() for s in n.skills}

    def cut_skills(self) -> set[str]:
        return set(self.raw.get("cut", {}).get("skills", []))

    def waived(self, skill_id: str) -> set[str]:
        w = self.raw.get("waivers", {}).get(skill_id)
        return set(w.get("drop", [])) if isinstance(w, dict) else set()

    def skill_status(self, skill_id: str) -> str:
        """'chinh', 'phu' or 'cut' - where the tree puts a micro-skill."""
        if skill_id in self.cut_skills():
            return "cut"
        owner = self.node_of_skill().get(skill_id)
        if owner is None:
            raise KeyError(f"the tree does not place the micro-skill {skill_id!r}")
        return self.nodes[owner].status

    # ---- a player's position
    def node_done(self, node_id: str, mastered_skills: Iterable[str], done_nodes: Iterable[str] = ()) -> bool:
        """A node with micro-skills is done when all of them are mastered. A node without
        (code, thực chiến, project) is done when it is named in `done_nodes` - the caller
        decides what finishing such a node means (its exercises, its project)."""
        node = self.nodes[node_id]
        if node.skills:
            return set(node.skills) <= set(mastered_skills)
        return node_id in set(done_nodes)

    def done(self, mastered_skills: Iterable[str], done_nodes: Iterable[str] = ()) -> set[str]:
        mastered, named = set(mastered_skills), set(done_nodes)
        return {n for n in self.nodes if self.node_done(n, mastered, named)}

    def open_nodes(self, mastered_skills: Iterable[str], done_nodes: Iterable[str] = ()) -> list[str]:
        """Nodes the player may study now: not done, and everything they require is done.
        Main-path nodes first, in stage order, so the list reads as 'what to do next'."""
        finished = self.done(mastered_skills, done_nodes)
        out = [n for n in self.nodes.values()
               if n.id not in finished and set(n.requires) <= finished]
        out.sort(key=lambda n: (not n.main, self.realm_order[n.realm], n.stage or 99, n.branch, n.id))
        return [n.id for n in out]

    def stage_reached(self, mastered_skills: Iterable[str], done_nodes: Iterable[str] = ()) -> tuple[str, int]:
        """(realm, stage): the highest stage whose main-path nodes, and all before it, are
        done. ('luyen_khi', 0) is a newcomer; finishing a realm's last stage puts the player
        at stage 0 of the next realm."""
        finished = self.done(mastered_skills, done_nodes)
        realms = sorted(self.realm_order, key=self.realm_order.get)
        for i, realm in enumerate(realms):
            for stage in range(1, self.realm_stages[realm] + 1):
                need = [n.id for n in self.main_nodes(realm) if n.stage == stage]
                if not set(need) <= finished:
                    return realm, stage - 1
            if i == len(realms) - 1:
                return realm, self.realm_stages[realm]
        return realms[0], 0

    def review_skills(self, node_id: str) -> list[str]:
        """The micro-skills a node's review questions are drawn from: those of the nodes it
        reinforces, in the order they are named."""
        out: list[str] = []
        for r in self.nodes[node_id].reinforces:
            out.extend(self.nodes[r].skills)
        return out

    def reaches(self, realm: str, stage: int, at: tuple[str, int]) -> bool:
        """Is (realm, stage) at or below the position `at`?"""
        a, b = self.realm_order[realm], self.realm_order[at[0]]
        return a < b or (a == b and stage <= at[1])


# ------------------------------------------------------------------ loading
def _read(name: str, math_dir: Path) -> dict:
    return json.loads((math_dir / name).read_text("utf-8"))


def build(raw: dict) -> Tree:
    nodes = {}
    for n in raw.get("nodes", []):
        nodes[n["id"]] = Node(
            id=n["id"], branch=n["branch"], realm=n["realm"], stage=n.get("stage"),
            status=n["status"], kind=n["kind"], content=n["content"], name_vi=n["name_vi"],
            why_vi=n.get("why_vi", ""), skills=tuple(n.get("skills", [])),
            requires=tuple(n.get("requires", [])), reinforces=tuple(n.get("reinforces", [])),
            topics_vi=tuple(n.get("topics_vi", [])), problems=tuple(n.get("problems", [])))
    realms = raw.get("realms", [])
    return Tree(raw=raw, nodes=nodes,
                realm_order={r["id"]: r["order"] for r in realms},
                realm_stages={r["id"]: r["stages"] for r in realms})


@lru_cache(maxsize=1)
def tree() -> Tree:
    return build(_read(TREE_FILE, MATH_DIR))


@lru_cache(maxsize=1)
def world_plan() -> dict:
    return _read(WORLD_FILE, MATH_DIR)


def wired_sections(plan: dict | None = None) -> tuple[str, ...]:
    """The sections of the world plan the game runs on: all of them once `wired` is true,
    else only the ones named in `wired_sections`."""
    plan = world_plan() if plan is None else plan
    if plan.get("wired") is True:
        return WIREABLE_SECTIONS
    named = plan.get("wired_sections", [])
    return tuple(s for s in named if s in WIREABLE_SECTIONS) if isinstance(named, list) else ()


def section_wired(name: str, plan: dict | None = None) -> bool:
    return name in wired_sections(plan)


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _wired_combat_problems(combat: dict, unlocks: dict) -> list[str]:
    """Everything realtime/combat.py reads from the combat section, checked once it is wired."""
    errs: list[str] = []

    def number(where: str, v, lo: float, hi: float | None = None, lo_ok: bool = False) -> None:
        if not _num(v) or v < lo or (v == lo and not lo_ok) or (hi is not None and v > hi):
            span = f"{'>=' if lo_ok else '>'} {lo}" + (f" and <= {hi}" if hi is not None else "")
            errs.append(f"combat.{where} must be a number {span}")

    shapes = combat.get("telegraph_shapes")
    if not isinstance(shapes, list) or not shapes or any(x not in TELEGRAPH_SHAPES for x in shapes):
        errs.append(f"combat.telegraph_shapes must be a non-empty list out of {TELEGRAPH_SHAPES}")
        shapes = []
    tele = combat.get("telegraph")
    if not isinstance(tele, dict):
        errs.append("combat.telegraph must be an object")
    else:
        number("telegraph.cone_degrees", tele.get("cone_degrees"), 0, 180)
        for key in ("cone_reach_mult", "line_width", "line_reach_mult"):
            number(f"telegraph.{key}", tele.get(key), 0)
        by_rank = tele.get("by_rank")
        if not isinstance(by_rank, dict) or set(by_rank) != set(RANKS):
            errs.append(f"combat.telegraph.by_rank must name every rank: {RANKS}")
        else:
            for rank, used in by_rank.items():
                if not isinstance(used, list) or not used or any(x not in shapes for x in used):
                    errs.append(f"combat.telegraph.by_rank.{rank} must be a non-empty list of telegraph_shapes")
    number("question_wait_seconds", combat.get("question_wait_seconds"), 0)
    right = combat.get("right_answer", {})
    number("right_answer.counter_multiplier", right.get("counter_multiplier"), 1, lo_ok=True)
    number("right_answer.stun_seconds", right.get("stun_seconds"), 0, lo_ok=True)
    number("right_answer.linh_luc_gain", right.get("linh_luc_gain"), 0, lo_ok=True)
    if right.get("gives_tu_vi") is not True:
        errs.append("combat.right_answer.gives_tu_vi must be true: a Phản Đòn is a right answer")
    wrong = combat.get("wrong_answer", {})
    number("wrong_answer.damage_taken", wrong.get("damage_taken"), 0, 1)
    if wrong.get("shows_solution") is not True:
        errs.append("combat.wrong_answer.shows_solution must be true: a wrong answer shows its solution")
    rest = combat.get("hit_during_cooldown", {})
    number("hit_during_cooldown.damage_taken", rest.get("damage_taken"), 0, 1, lo_ok=True)
    if rest.get("question") is not False:
        errs.append("combat.hit_during_cooldown.question must be false")
    dodge = combat.get("dodge", {})
    for key in ("invulnerable_seconds", "cooldown_seconds", "dash_px", "dash_ms"):
        number(f"dodge.{key}", dodge.get(key), 0)
    if dodge.get("unlock") not in unlocks:
        errs.append(f"combat.dodge.unlock: unknown ability {dodge.get('unlock')!r}")
    if _num(dodge.get("invulnerable_seconds")) and _num(dodge.get("cooldown_seconds")) \
            and dodge["invulnerable_seconds"] >= dodge["cooldown_seconds"]:
        errs.append("combat.dodge: invulnerable_seconds must be shorter than cooldown_seconds")
    if combat.get("elite_shield_breaks_on") != "parry":
        errs.append("combat.elite_shield_breaks_on must be 'parry'")
    ranks = combat.get("shielded_ranks")
    if not isinstance(ranks, list) or any(r not in RANKS for r in ranks) or "normal" in ranks:
        errs.append("combat.shielded_ranks must list elite and/or boss only: a normal monster falls to plain hits")
    return errs


TILE = 16
MATH_BRANCHES = ("ds", "gt", "xs", "tr")


def _tile_walkable(zmap, x: int, y: int) -> bool:
    """Can a character stand on tile (x, y)? Its feet at the middle of the tile, a little low,
    the collision box of realtime/movement.py."""
    return not zmap.collider.blocked(x * TILE + TILE / 2, y * TILE + 12)


def _wired_lands_problems(plan: dict, t: Tree, math_dir: Path) -> list[str]:
    """What realtime/lands.py, the world and the client read about a built land (`status: co`),
    checked once the lands section is wired: a zone of zones.json is that land, its map is on
    disk for the server and the client, every creature named spawns there and stands for real
    nodes of the land's own branch, and every weapon lying in it has a `pos` on a walkable tile."""
    from ..realtime import maps as rmaps   # reads Tiled files only (no world, no database)
    errs: list[str] = []
    data_dir = math_dir.parent
    maps_dir = data_dir.parent / "maps"
    client_maps = data_dir.parents[1] / "client" / "assets" / "maps"
    try:
        zones = {k: v for k, v in _read("zones.json", data_dir).items() if not k.startswith("_")}
        creatures = {k: v for k, v in _read("monsters.json", math_dir).items() if not k.startswith("_")}
        creatures.update({k: v for k, v in _read("monsters.json", data_dir / "creatures").items()
                          if not k.startswith("_")})
    except (OSError, ValueError) as e:
        return [f"lands: cannot read zones or monsters: {e}"]
    branches = {b["id"]: b for b in t.raw.get("branches", [])}
    lands = {l["id"]: l for l in plan.get("lands", [])}
    built: dict[str, object] = {}
    for lid, l in lands.items():
        if l.get("status") != "co":
            continue
        where = f"land {lid}"
        if not l.get("map"):
            errs.append(f"{where}: built but has no map")
            continue
        zids = [zid for zid, z in zones.items() if z.get("land") == lid]
        if len(zids) != 1:
            errs.append(f"{where}: {len(zids)} zones of zones.json are this land (one is needed)")
            continue
        z = zones[zids[0]]
        if z.get("map") != l["map"]:
            errs.append(f"{where}: its zone {zids[0]} draws map {z.get('map')!r}, the plan says {l['map']!r}")
        if (l.get("kind") == "hub") != (z.get("kind") == "hub"):
            errs.append(f"{where}: kind {l.get('kind')!r} but its zone is {z.get('kind')!r}")
        path = maps_dir / f"{l['map']}.tmj"
        if not path.is_file():
            errs.append(f"{where}: no map file server/maps/{l['map']}.tmj")
            continue
        if not (client_maps / f"{l['map']}.tmj").is_file():
            errs.append(f"{where}: the client has no client/assets/maps/{l['map']}.tmj")
        zmap = rmaps.parse(path)
        built[lid] = zmap
        if l.get("kind") == "hub":
            continue
        spawned = {a.props.get("monster") for a in zmap.monster_areas}
        for kind in l.get("monsters", []):
            if kind not in creatures:
                errs.append(f"{where}: monster {kind!r} does not exist")
            elif kind not in spawned:
                errs.append(f"{where}: monster {kind} never spawns on map {l['map']}")
        for kind in sorted(k for k in spawned if k in creatures and creatures[k].get("land")):
            if creatures[kind]["land"] != lid:
                errs.append(f"{where}: {kind} belongs to land {creatures[kind]['land']!r} but spawns here")
        for kind in sorted(k for k in spawned if k and k not in creatures):
            errs.append(f"{where}: map {l['map']} spawns {kind!r}, which is no monster")
    zone_lands = {z.get("land") for z in zones.values() if z.get("land")}
    for lid in sorted(zone_lands - set(lands)):
        errs.append(f"zones.json: land {lid!r} is not a land of the plan")
    for lid in sorted(zone_lands & set(lands)):
        if lands[lid].get("status") != "co":
            errs.append(f"land {lid}: a zone is this land but the plan still says {lands[lid].get('status')!r}")

    # the creatures of the lands: real nodes of the land's own branch
    for kind, m in sorted(creatures.items()):
        if not m.get("land"):
            continue
        where = f"monster {kind}"
        l = lands.get(m["land"])
        if l is None:
            errs.append(f"{where}: unknown land {m['land']!r}")
            continue
        if m.get("branch") != l.get("branch"):
            errs.append(f"{where}: branch {m.get('branch')!r}, its land is of {l.get('branch')!r}")
        if m.get("rank", "normal") not in RANKS:
            errs.append(f"{where}: unknown rank {m.get('rank')!r}")
        nodes = m.get("nodes") or []
        if not nodes:
            errs.append(f"{where}: stands for no node, so it has nothing of its own to ask")
        bad = [n for n in nodes if n not in t.nodes or not t.nodes[n].main or t.nodes[n].realm != l.get("realm")]
        if bad:
            errs.append(f"{where}: {', '.join(bad)} are not main-path nodes of {l.get('realm')}")
            continue
        if any(not t.nodes[n].skills for n in nodes):
            errs.append(f"{where}: a node without questions ({', '.join(n for n in nodes if not t.nodes[n].skills)})")
        branch = l.get("branch")
        if m.get("ask") == "branches":
            have = {t.nodes[n].branch for n in nodes}
            if not set(MATH_BRANCHES) <= have:
                errs.append(f"{where}: asks the four math branches in turn but has no node of "
                            f"{', '.join(sorted(set(MATH_BRANCHES) - have))}")
        elif m.get("ask", "nodes") != "nodes":
            errs.append(f"{where}: ask must be 'nodes' or 'branches'")
        elif branch in branches and branches[branch].get("subject"):
            other = [n for n in nodes if t.nodes[n].branch != branch]
            if other:
                errs.append(f"{where}: {', '.join(other)} are not of its land's branch {branch}")
        elif branch in branches:
            # a branch of exercises: its creatures ask the math its nodes reinforce
            fed = {r for n in t.nodes.values() if n.branch == branch for r in n.reinforces}
            other = [n for n in nodes if n not in fed]
            if other:
                errs.append(f"{where}: {', '.join(other)} are reinforced by no node of {branch}")
        for d in m.get("drops", []):
            if not isinstance(d.get("chance"), (int, float)) or not 0 < d["chance"] <= 1:
                errs.append(f"{where}: a drop chance must be in (0, 1]")

    # where the weapons lie
    for i, p in enumerate(plan.get("weapons_placed", [])):
        where = f"weapons_placed[{i}] {p.get('weapon')} {p.get('quality')}"
        lid = p.get("land")
        pos = p.get("pos")
        if lid not in built:
            if pos is not None and lands.get(lid, {}).get("status") != "co":
                errs.append(f"{where}: has a pos but land {lid} is not built")
            continue
        if not (isinstance(pos, list) and len(pos) == 2 and all(isinstance(v, int) and not isinstance(v, bool)
                                                                for v in pos)):
            errs.append(f"{where}: needs a pos [x, y] (a tile of map {lands[lid]['map']})")
            continue
        zmap = built[lid]
        x, y = pos
        if not (0 <= x < zmap.width_px // TILE and 0 <= y < zmap.height_px // TILE):
            errs.append(f"{where}: pos {pos} is off the map")
        elif not _tile_walkable(zmap, x, y):
            errs.append(f"{where}: pos {pos} is not a walkable tile")
    return errs


def _walk_region(zmap, start: tuple[int, int]) -> set[tuple[int, int]]:
    """The tiles a character can walk to from `start` (four ways, the movement collider)."""
    from collections import deque
    cols, rows = zmap.width_px // TILE, zmap.height_px // TILE
    if not (0 <= start[0] < cols and 0 <= start[1] < rows) or not _tile_walkable(zmap, *start):
        return set()
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= n[0] < cols and 0 <= n[1] < rows and n not in seen and _tile_walkable(zmap, *n):
                seen.add(n)
                q.append(n)
    return seen


def glide_reaches(zmap, foot: set, target: set, glide: dict) -> bool:
    """Can a player walking the tiles `foot` reach the tiles `target` by one Đạp Kiếm Lướt
    (realtime/glide.py), from the middle of a tile, in one of eight directions?"""
    from ..realtime import glide as g
    over = set(glide.get("over_tiles", []))
    reach = int(float(glide.get("max_px", 0)) // TILE) + 2
    near = [t for t in foot if any(abs(t[0] - a) <= reach and abs(t[1] - b) <= reach for a, b in target)]
    for tx, ty in near:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                land = g.pick(zmap.collider, zmap.tile_name, over, tx * TILE + TILE / 2, ty * TILE + 12, dx, dy,
                              float(glide.get("max_px", 0)), float(glide.get("min_px", 0)))
                if land is not None and (int(land[0] // TILE), int((land[1] - 1) // TILE)) in target:
                    return True
    return False


def _wired_beasts_problems(plan: dict, math_dir: Path) -> list[str]:
    """What realtime/beasts.py and systems/beasts.py read, checked once 'beasts' is wired: the
    taming rule's numbers, a talisman that is an item, and for every built beast a built land of
    Luyện Khí, a walkable `pos` (on foot from the land's gate, unless it `needs` an ability -
    then not on foot but by that ability), sane fighting numbers and a gift of a known type."""
    from ..realtime import maps as rmaps
    errs: list[str] = []
    data_dir = math_dir.parent
    tm = plan.get("beast_taming")
    if not isinstance(tm, dict):
        return ["beast_taming must be an object (the taming rule of the beasts)"]
    unlocks = {u.get("id"): u for u in plan.get("unlocks", [])}
    lands = {l["id"]: l for l in plan.get("lands", [])}
    items: set[str] = set()
    for f in sorted((data_dir / "items").glob("*.json")):
        items |= {k for k in _read(f.name, data_dir / "items") if not k.startswith("_")}
    if tm.get("talisman") not in items:
        errs.append(f"beast_taming.talisman: {tm.get('talisman')!r} is not an item of data/items")
    if tm.get("seal_unlock") not in unlocks:
        errs.append(f"beast_taming.seal_unlock: unknown ability {tm.get('seal_unlock')!r}")
    elif unlocks[tm["seal_unlock"]].get("status") != "co":
        errs.append(f"beast_taming.seal_unlock: {tm['seal_unlock']} is wired, so its status must be 'co'")
    for key in ("seal_reach_px", "yield_seconds", "roam_tiles"):
        if not _num(tm.get(key)) or tm[key] <= 0:
            errs.append(f"beast_taming.{key} must be a positive number")
    if list(tm.get("gift_types", [])) != list(GIFT_TYPES):
        errs.append(f"beast_taming.gift_types must be {list(GIFT_TYPES)} (the gifts the game knows)")
    abilities = unlocks
    glide = (abilities.get("dap_kiem_luot") or {}).get("glide", {})
    zmaps: dict[str, object] = {}
    for b in plan.get("beasts", []):
        where = f"beast {b.get('id')}"
        if b.get("status") not in CONTENT[::2]:
            errs.append(f"{where}: status must be 'co' or 'chua_co'")
            continue
        land = lands.get(b.get("land"), {})
        if b["status"] != "co":
            if b.get("pos") is not None:
                errs.append(f"{where}: has a pos but is not built")
            continue
        if land.get("status") != "co" or not land.get("map"):
            errs.append(f"{where}: built, but its land {b.get('land')} is not")
            continue
        if land.get("realm") != b.get("requires", {}).get("realm"):
            errs.append(f"{where}: requires a realm other than its land's")
        f = b.get("fight")
        if not isinstance(f, dict):
            errs.append(f"{where}: built, so it needs 'fight' (hp, atk, def, speed, attack_radius, aggro_radius)")
        else:
            for key in ("hp", "atk", "speed", "attack_radius", "aggro_radius"):
                if not _num(f.get(key)) or f[key] <= 0:
                    errs.append(f"{where}: fight.{key} must be a positive number")
            if not _num(f.get("def")) or f["def"] < 0:
                errs.append(f"{where}: fight.def must be a number >= 0")
        gift = b.get("gift")
        if not isinstance(gift, dict) or gift.get("type") not in GIFT_TYPES:
            errs.append(f"{where}: gift.type must be one of {GIFT_TYPES}")
        else:
            gt = gift["type"]
            if gt == "sniff" and (not _num(gift.get("radius_tiles")) or gift["radius_tiles"] <= 0):
                errs.append(f"{where}: gift sniff needs a positive radius_tiles")
            if gt in ("wrong_guard", "dodge_cooldown", "parry_fire") and \
                    (not _num(gift.get("value")) or not 0 < gift["value"] < 1):
                errs.append(f"{where}: gift {gt} needs a value between 0 and 1 (a small effect)")
            if gt == "mount" and (not _num(gift.get("speed_mult")) or not 1 < gift["speed_mult"] <= 2.5):
                errs.append(f"{where}: gift mount needs a speed_mult above 1 and at most 2.5")
        pos = b.get("pos")
        if not (isinstance(pos, list) and len(pos) == 2 and all(isinstance(v, int) and not isinstance(v, bool)
                                                                for v in pos)):
            errs.append(f"{where}: needs a pos [x, y] (a tile of map {land['map']})")
            continue
        path = data_dir.parent / "maps" / f"{land['map']}.tmj"
        if not path.is_file():
            continue          # (the lands check names a missing map)
        zmap = zmaps.get(land["map"]) or zmaps.setdefault(land["map"], rmaps.parse(path))
        if not _tile_walkable(zmap, *pos):
            errs.append(f"{where}: pos {pos} is not a walkable tile")
            continue
        gate = zmap.spawn("from_village")
        foot = _walk_region(zmap, (int(gate[0] // TILE), int(gate[1] // TILE)))
        if not b.get("needs"):
            if tuple(pos) not in foot:
                errs.append(f"{where}: pos {pos} cannot be walked to from the gate of {land['map']}")
        elif tuple(pos) in foot:
            errs.append(f"{where}: needs {b['needs']}, yet pos {pos} can be walked to")
        elif b["needs"] == "dap_kiem_luot" and not glide_reaches(zmap, foot, _walk_region(zmap, tuple(pos)), glide):
            errs.append(f"{where}: needs Đạp Kiếm Lướt, but no glide from where a player walks reaches pos {pos}")
    return errs


def _wired_abilities_problems(plan: dict, math_dir: Path) -> list[str]:
    """What realtime/abilities.py reads, checked once 'abilities' is wired: every unlock of a realm
    with a built land has content ('co') and every other one waits ('chua_co'); the numbers of the
    formation, the glide and the ride; and every weapon spot behind a chasm or water that
    needs Đạp Kiếm Lướt can really be reached by one glide."""
    from ..realtime import maps as rmaps
    errs: list[str] = []
    data_dir = math_dir.parent
    lands = {l["id"]: l for l in plan.get("lands", [])}
    built_realms = {l.get("realm") for l in lands.values() if l.get("status") == "co"}
    unlocks = {u.get("id"): u for u in plan.get("unlocks", [])}
    for uid, u in unlocks.items():
        if u.get("status") not in CONTENT[::2]:
            errs.append(f"unlock {uid}: status must be 'co' or 'chua_co'")
        elif (u.get("status") == "co") != (u.get("realm") in built_realms):
            want = "co" if u.get("realm") in built_realms else "chua_co"
            errs.append(f"unlock {uid}: status must be '{want}' (realm {u.get('realm')} "
                        f"{'has' if want == 'co' else 'has no'} built land)")
    for uid, block in ABILITY_BLOCKS.items():
        u = unlocks.get(uid)
        if u is None:
            errs.append(f"unlock {uid}: missing (the game runs it)")
            continue
        if u.get("status") != "co":
            continue
        c = u.get(block)
        if not isinstance(c, dict):
            errs.append(f"unlock {uid}: needs its '{block}' numbers")
            continue
        if block == "formation":
            for key in ("radius_px", "seconds", "cooldown_seconds"):
                if not _num(c.get(key)) or c[key] <= 0:
                    errs.append(f"unlock {uid}: formation.{key} must be a positive number")
            if not _num(c.get("windup_mult")) or not 1 < c["windup_mult"] <= 3:
                errs.append(f"unlock {uid}: formation.windup_mult must be above 1 (slower) and at most 3")
        elif block == "glide":
            for key in ("max_px", "ms", "cooldown_seconds"):
                if not _num(c.get(key)) or c[key] <= 0:
                    errs.append(f"unlock {uid}: glide.{key} must be a positive number")
            if not _num(c.get("min_px")) or c["min_px"] < 0 or (_num(c.get("max_px")) and c["min_px"] >= c["max_px"]):
                errs.append(f"unlock {uid}: glide.min_px must be >= 0 and below max_px")
            over = c.get("over_tiles")
            if not isinstance(over, list) or not over or any(t not in rmaps.TILE_NAMES for t in over):
                errs.append(f"unlock {uid}: glide.over_tiles must name ground tiles out of {sorted(set(rmaps.TILE_NAMES))}")
        elif block == "ride":
            mounts = [b for b in plan.get("beasts", []) if b.get("status") == "co"
                      and (b.get("gift") or {}).get("type") == c.get("gift")]
            if c.get("gift") != "mount" or not mounts:
                errs.append(f"unlock {uid}: ride.gift must be 'mount' and some built beast must have it")
    glide = (unlocks.get("dap_kiem_luot") or {}).get("glide", {})
    if (unlocks.get("dap_kiem_luot") or {}).get("status") == "co" and isinstance(glide, dict) and _num(glide.get("max_px")):
        for p in plan.get("weapons_placed", []):
            land = lands.get(p.get("land"), {})
            if p.get("needs") != "dap_kiem_luot" or land.get("status") != "co" or not p.get("pos"):
                continue
            path = data_dir.parent / "maps" / f"{land['map']}.tmj"
            if not path.is_file():
                continue
            zmap = rmaps.parse(path)
            gate = zmap.spawn("from_village")
            foot = _walk_region(zmap, (int(gate[0] // TILE), int(gate[1] // TILE)))
            if not glide_reaches(zmap, foot, _walk_region(zmap, tuple(p["pos"])), glide):
                errs.append(f"weapons_placed {p.get('weapon')} {p.get('quality')}: needs Đạp Kiếm Lướt, "
                            f"but no glide from where a player walks reaches pos {p['pos']}")
    return errs


def subject_skills(math_dir: Path = MATH_DIR) -> dict[str, tuple[str, ...]]:
    """Every micro-skill id of the four subject files -> its prerequisites."""
    out: dict[str, tuple[str, ...]] = {}
    index = math_path.load_index(math_dir)
    for entry in index.get("subjects", []):
        if not entry.get("file"):
            continue
        raw = _read(entry["file"], math_dir)
        for floor in raw.get("floors", []):
            for s in floor.get("skills", []):
                out[s["id"]] = tuple(s.get("requires", []))
    return out


def problem_ids(math_dir: Path = MATH_DIR) -> set[str]:
    out: set[str] = set()
    folder = math_dir / "problems"
    for f in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        out.update(p["id"] for p in json.loads(f.read_text("utf-8")).get("problems", []))
    return out


# ------------------------------------------------------------------ checks
def _dupes(items: Iterable[str]) -> list[str]:
    seen, out = set(), []
    for i in items:
        if i in seen and i not in out:
            out.append(i)
        seen.add(i)
    return out


def validate_tree(raw: dict, skills: dict[str, tuple[str, ...]], problems: set[str]) -> list[str]:
    errs: list[str] = []
    realms = raw.get("realms", [])
    realm_ids = [r.get("id") for r in realms]
    branch_ids = [b.get("id") for b in raw.get("branches", [])]
    if _dupes(realm_ids):
        errs.append(f"realms: duplicate ids {_dupes(realm_ids)}")
    if sorted(r.get("order") for r in realms) != list(range(1, len(realms) + 1)):
        errs.append("realms: 'order' must run 1..n without gaps")
    if _dupes(branch_ids):
        errs.append(f"branches: duplicate ids {_dupes(branch_ids)}")

    node_list = raw.get("nodes", [])
    ids = [n.get("id") for n in node_list]
    if _dupes(ids):
        errs.append(f"nodes: duplicate ids {_dupes(ids)}")
    for n in node_list:
        nid = n.get("id", "?")
        for key in ("id", "branch", "realm", "status", "kind", "content", "name_vi", "why_vi"):
            if not n.get(key):
                errs.append(f"{nid}: missing '{key}'")
        if n.get("branch") not in branch_ids:
            errs.append(f"{nid}: unknown branch {n.get('branch')!r}")
        if n.get("realm") not in realm_ids:
            errs.append(f"{nid}: unknown realm {n.get('realm')!r}")
        if n.get("status") not in STATUSES:
            errs.append(f"{nid}: status must be one of {STATUSES}")
        if n.get("kind") not in KINDS:
            errs.append(f"{nid}: kind must be one of {KINDS}")
        if n.get("content") not in CONTENT:
            errs.append(f"{nid}: content must be one of {CONTENT}")
        if not n.get("skills") and not n.get("topics_vi"):
            errs.append(f"{nid}: a node with no micro-skills must say what it teaches in 'topics_vi'")
        for p in n.get("problems", []):
            if p not in problems:
                errs.append(f"{nid}: unknown programming exercise {p!r}")
    if errs:
        return errs                     # the structural checks below need well-formed nodes

    t = build(raw)
    stages = t.realm_stages
    for n in t.nodes.values():
        if n.main:
            if not isinstance(n.stage, int) or not 1 <= n.stage <= stages[n.realm]:
                errs.append(f"{n.id}: a main-path node needs a stage in 1..{stages[n.realm]}")
        elif n.stage is not None:
            errs.append(f"{n.id}: an optional node has no stage (it never gates one)")
        for r in n.requires + n.reinforces:
            if r not in t.nodes:
                errs.append(f"{n.id}: unknown node {r!r}")
        if _dupes(n.requires):
            errs.append(f"{n.id}: 'requires' repeats {_dupes(n.requires)}")
    if errs:
        return errs

    cycle = math_path.find_cycle({n.id: list(n.requires) for n in t.nodes.values()})
    if cycle:
        return errs + [f"nodes: 'requires' goes round in a circle: {' -> '.join(cycle)}"]

    # order: nothing needs something later
    for n in t.nodes.values():
        for r in n.requires:
            req = t.nodes[r]
            if n.main and not req.main:
                errs.append(f"{n.id}: a main-path node may not require the optional node {r}")
            ro, no = t.realm_order[req.realm], t.realm_order[n.realm]
            if ro > no or (ro == no and n.main and req.main and req.stage > n.stage):
                errs.append(f"{n.id} (stage {n.stage}) requires {r}, which comes later (stage {req.stage})")
        anc = t.ancestors(n.id)
        for r in n.reinforces:
            if r not in anc:
                errs.append(f"{n.id}: reinforces {r}, which is not one of its ancestors")

    # coverage: each micro-skill in exactly one place
    placed = [s for n in t.nodes.values() for s in n.skills]
    cut = list(raw.get("cut", {}).get("skills", []))
    for s in _dupes(placed + cut):
        errs.append(f"micro-skill {s} is placed more than once")
    for s in placed + cut:
        if s not in skills:
            errs.append(f"micro-skill {s} is not in any subject file")
    for s in sorted(set(skills) - set(placed) - set(cut)):
        errs.append(f"micro-skill {s} is in a subject file but nowhere in the tree")

    # the tree agrees with the micro-skill prerequisites
    owner = t.node_of_skill()
    waivers = {k: v for k, v in raw.get("waivers", {}).items() if not k.startswith("_")}
    for skill, w in waivers.items():
        if skill not in skills:
            errs.append(f"waivers: unknown micro-skill {skill}")
            continue
        for d in w.get("drop", []):
            if d not in skills.get(skill, ()):
                errs.append(f"waivers: {d} is not a prerequisite of {skill}")
            elif owner.get(d) and owner.get(skill) and (
                    owner[d] == owner[skill] or owner[d] in t.ancestors(owner[skill])) \
                    and t.nodes[owner[d]].main:
                errs.append(f"waivers: {skill} need not drop {d}, it is already learned before")
        if not w.get("why_vi"):
            errs.append(f"waivers: {skill} needs a reason ('why_vi')")
    for n in t.nodes.values():
        anc = t.ancestors(n.id)
        for s in n.skills:
            for pre in skills.get(s, ()):
                if pre in t.waived(s):
                    continue
                home = owner.get(pre)
                if home is None:
                    errs.append(f"{n.id}: {s} needs {pre}, which the tree has cut")
                elif home != n.id and home not in anc:
                    errs.append(f"{n.id}: {s} needs {pre} (node {home}), which is not learned before it")
                elif n.main and not t.nodes[home].main:
                    errs.append(f"{n.id}: main-path {s} needs the optional {pre}")

    # every main-path node of a realm leads to the realm's project
    for realm in t.realm_order:
        mains = t.main_nodes(realm)
        projects = [n for n in mains if n.kind == "du_an"]
        if len(projects) != 1:
            errs.append(f"realm {realm}: needs exactly one project node (kind du_an), has {len(projects)}")
            continue
        last = projects[0]
        if last.stage != stages[realm]:
            errs.append(f"{last.id}: the realm's project belongs to its last stage")
        anc = t.ancestors(last.id)
        for n in mains:
            if n.id != last.id and n.id not in anc:
                errs.append(f"{n.id}: nothing on the way to {last.id} needs it (dangling node)")
        for stage in range(1, stages[realm] + 1):
            here = [n for n in mains if n.stage == stage]
            if not here:
                errs.append(f"realm {realm}: stage {stage} has no node")
            elif realm == "luyen_khi" and not any(n.kind in ("code", "thuc_chien", "du_an") for n in here):
                errs.append(f"realm {realm}: stage {stage} has no programming or thực chiến node")
    for b in raw.get("branches", []):
        if b["id"] not in raw.get("sources", {}):
            errs.append(f"sources: branch {b['id']} has no suggested reading")
    return errs


def _req_problems(t: Tree, where: str, req: dict) -> list[str]:
    errs = []
    realm, stage = req.get("realm"), req.get("stage")
    if realm not in t.realm_order:
        return [f"{where}: unknown realm {realm!r}"]
    if not isinstance(stage, int) or not 0 <= stage <= t.realm_stages[realm]:
        return [f"{where}: stage must be 0..{t.realm_stages[realm]}"]
    for nid in req.get("nodes", []):
        node = t.nodes.get(nid)
        if node is None:
            errs.append(f"{where}: unknown node {nid!r}")
        elif not node.main:
            errs.append(f"{where}: {nid} is optional; a requirement must be on the main path")
        elif not t.reaches(node.realm, node.stage, (realm, stage)):
            errs.append(f"{where}: asks for {nid} (stage {node.stage}) at stage {stage}")
    return errs


def validate_world(plan: dict, t: Tree, math_dir: Path = MATH_DIR) -> list[str]:
    errs: list[str] = []
    combat = plan.get("combat", {})
    if combat.get("question_rule") not in QUESTION_RULES:
        errs.append(f"combat.question_rule must be one of {QUESTION_RULES}")
    for key in ("question_cooldown_seconds", "telegraph_min_seconds"):
        if not isinstance(combat.get(key), (int, float)) or combat[key] <= 0:
            errs.append(f"combat.{key} must be a positive number")
    if combat.get("right_answer", {}).get("damage_taken") != 0:
        errs.append("combat.right_answer.damage_taken must be 0: a right answer is a parry")
    named = plan.get("wired_sections", [])
    if not isinstance(named, list) or any(s not in WIREABLE_SECTIONS for s in named) \
            or len(set(named)) != len(named):
        errs.append(f"wired_sections must be a list of distinct sections out of {WIREABLE_SECTIONS}")
    if section_wired("combat", plan):
        errs += _wired_combat_problems(combat, {u.get("id"): u for u in plan.get("unlocks", [])})
    if section_wired("lands", plan):
        errs += _wired_lands_problems(plan, t, math_dir)
    if section_wired("beasts", plan):
        errs += _wired_beasts_problems(plan, math_dir)
    if section_wired("abilities", plan):
        errs += _wired_abilities_problems(plan, math_dir)

    grades = {g["grade"]: g for g in plan.get("grades", [])}
    if sorted(grades) != list(range(1, len(t.realm_order) + 1)):
        errs.append("grades: one grade per realm, numbered from 1")
    for g in grades.values():
        if t.realm_order.get(g.get("realm")) != g["grade"]:
            errs.append(f"grades: grade {g['grade']} must belong to realm number {g['grade']}")
    qualities = {q["id"] for q in plan.get("qualities", [])}
    unlocks = {u["id"]: u for u in plan.get("unlocks", [])}
    lands = {l["id"]: l for l in plan.get("lands", [])}
    types = {w["id"]: w for w in plan.get("weapon_types", [])}
    branches = {b["id"] for b in t.raw.get("branches", [])}

    for u in plan.get("unlocks", []):
        errs += _req_problems(t, f"unlock {u.get('id')}", {"realm": u.get("realm"), "stage": u.get("stage")})
    for l in plan.get("lands", []):
        if l.get("branch") is not None and l["branch"] not in branches:
            errs.append(f"land {l['id']}: unknown branch {l['branch']!r}")
        opens = dict(l.get("opens", {}), realm=l.get("realm"))
        errs += _req_problems(t, f"land {l['id']}", opens)
        if l.get("needs") and l["needs"] not in unlocks:
            errs.append(f"land {l['id']}: unknown ability {l['needs']!r}")
    for w in plan.get("weapon_types", []):
        if w.get("branch") not in branches:
            errs.append(f"weapon type {w['id']}: unknown branch {w.get('branch')!r}")
        if w.get("land") is not None and w["land"] not in lands:
            errs.append(f"weapon type {w['id']}: unknown land {w['land']!r}")

    seen = set()
    for i, p in enumerate(plan.get("weapons_placed", [])):
        where = f"weapons_placed[{i}] {p.get('weapon')}"
        kind, _, grade = str(p.get("weapon", "")).rpartition("_")
        if kind not in types or not grade.isdigit() or int(grade) not in grades:
            errs.append(f"{where}: not <weapon type>_<grade>")
            continue
        if p.get("quality") not in qualities:
            errs.append(f"{where}: unknown quality {p.get('quality')!r}")
        if p.get("land") not in lands:
            errs.append(f"{where}: unknown land {p.get('land')!r}")
        if p.get("needs") and p["needs"] not in unlocks:
            errs.append(f"{where}: unknown ability {p['needs']!r}")
        if (p["weapon"], p.get("quality")) in seen:
            errs.append(f"{where}: {p.get('quality')} is placed twice")
        seen.add((p["weapon"], p.get("quality")))
        req = p.get("requires", {})
        errs += _req_problems(t, where, req)
        if req.get("realm") in t.realm_order:
            # a weapon one grade above the realm may be found at the realm's end, not higher
            if int(grade) > t.realm_order[req["realm"]] + 1:
                errs.append(f"{where}: grade {grade} is too high for realm {req['realm']}")
            branch = types[kind]["branch"]
            named = [t.nodes[n] for n in req.get("nodes", []) if n in t.nodes]
            if named and not any(n.branch == branch for n in named) and p.get("land") == types[kind].get("land"):
                errs.append(f"{where}: none of its nodes is of the weapon's own branch ({branch})")
        if p.get("needs") in unlocks and req.get("realm") in t.realm_order:
            u = unlocks[p["needs"]]
            if not t.reaches(u["realm"], u["stage"], (req["realm"], req.get("stage", 0))):
                errs.append(f"{where}: needs {p['needs']}, which unlocks later than the weapon")
    for b in plan.get("beasts", []):
        where = f"beast {b.get('id')}"
        if b.get("land") not in lands:
            errs.append(f"{where}: unknown land {b.get('land')!r}")
        errs += _req_problems(t, where, b.get("requires", {}))
        if b.get("needs"):
            u = unlocks.get(b["needs"])
            if u is None:
                errs.append(f"{where}: unknown ability {b['needs']!r}")
            elif not t.reaches(u["realm"], u["stage"], (b["requires"]["realm"], b["requires"]["stage"])):
                errs.append(f"{where}: needs {b['needs']}, which unlocks later than the beast")
        if not isinstance(b.get("parries_to_tame"), int) or b["parries_to_tame"] < 1:
            errs.append(f"{where}: parries_to_tame must be a positive whole number")
    return errs


def validate_all(math_dir: Path = MATH_DIR) -> list[str]:
    try:
        raw = _read(TREE_FILE, math_dir)
        plan = _read(WORLD_FILE, math_dir)
    except (OSError, ValueError) as e:
        return [f"cannot read the tree: {e}"]
    errs = validate_tree(raw, subject_skills(math_dir), problem_ids(math_dir))
    if errs:
        return errs
    return validate_world(plan, build(raw), math_dir)
