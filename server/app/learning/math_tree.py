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
not wired yet (`"wired": false` in world_plan.json): its lands, weapons and beasts are a design.
One part of it is: `"wired_sections": ["combat"]` names the sections the game already runs on
although the whole plan is not (the combat rule "questions only when a monster hits you",
realtime/combat.py). A wired section is checked harder - every number the game reads must be
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
WIREABLE_SECTIONS = ("combat",)    # the parts of world_plan.json the game can run on by themselves
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


def validate_world(plan: dict, t: Tree) -> list[str]:
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
    return validate_world(plan, build(raw))
