"""Where a player stands in Đạo Thụ, the curriculum tree - the only place that answers it.

The tree (data/math/tree.json, learning/math_tree.py) replaced "finish floor n of a subject to
open floor n+1". A *floor* is still the address of questions (templates, tier band, library
document); a *node* is what the player sees, opens, practises and clears. A math node is a set
of micro-skills, and those may live on more than one floor, so a node is made of **parts**:

    part = (node, subject, floor, the node's micro-skills that live on that floor)

A sitting (MathRun) is on one part (`node_id`); everything the engine does per floor - the
adaptive tier, the mastery gate, the Thiên kiếp nhỏ, anti-repeat, tâm ma, ladders - runs on
the part's micro-skills (systems/math_practice.py).

The rules (the contract of the Đạo Thụ milestone, R1-R12):

  * R1 the parts of a node: its micro-skills grouped by the floor they belong to, in floor
    order. A node without micro-skills has none.
  * R2 a part is passed by a passed Thiên kiếp nhỏ on it (a trial run with its `node_id`), or
    by the old rules, which cover a whole floor: a passed trial with no `node_id` on that floor
    (an old save), or the bài kiểm tra đầu vào skipped the floor.
  * R3 a node is done when every part that has questions is passed and every programming
    exercise it lists is fully solved. A node with neither (the Python, thực chiến and project
    nodes still to be written, a math node whose floor has no question) is **vacant**: it counts
    as done for `requires` and for the stage, and is shown as "đang biên soạn" - until the day
    it gets content, when it starts to count.
  * R4 a node is open when it is not done and every node it requires is done. Optional nodes
    follow the same rule and block nothing. Nothing else locks a node.
  * R5 the stage: math_tree.Tree.stage_reached over the done nodes. It is shown only; it does
    not change the cultivation realm or Tu Vi.
  * R6 a micro-skill of the tree's `cut` list is never asked (math_practice._templates drops
    it for every mode); an optional node's micro-skills only in that node's own sittings.
  * R9 outside a sitting the player's own place in subject S is the **frontier** of S: the
    first open main-path part of S in tree order (realm, stage, node id); else the last passed
    main part of S; else the first main part of S that has questions.
  * R10 a programming exercise is open when its micro-skill is in an open or done node.
  * R12 three primitives for the callers that used to read "the floor the player has
    reached": `frontier` (questions for this player now), `reached_floors` (which floors may be
    shown or entered) and `working_stage` (the floor number used as a level threshold).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..learning import math_library, math_mastery, math_path, math_problems, math_tree
from ..models import MathRun, MathSubmission, User

TRIAL = "trial"
OPEN, DONE, LOCKED, VACANT = "open", "done", "locked", "vacant"
SOURCES_DIR = math_tree.MATH_DIR / "sources"
SOURCE_KEYS = ("title", "author", "url", "where", "lang", "kind")
VACANT_VI = "Đang biên soạn"


# ------------------------------------------------------------------ parts (pure)
@dataclass(frozen=True)
class Part:
    """The micro-skills of one node that live on one floor. `node_id` is None only for the
    whole-floor stand-in of an old sitting that has no node."""
    node_id: str | None
    subject_id: str
    floor: int
    skills: tuple[str, ...]

    @property
    def key(self) -> tuple[str | None, str, int]:
        return self.node_id, self.subject_id, self.floor


_cache: dict = {}


def tree() -> math_tree.Tree:
    return math_tree.tree()


def _structure() -> dict:
    """The parts of every node and where every micro-skill lives, for the tree and the path
    as they are now (rebuilt when either object changes, e.g. a test swaps the tree)."""
    t, subjects = tree(), math_path.subjects()
    if _cache.get("tree") is t and _cache.get("subjects") is subjects:
        return _cache
    home = {s.id: (subj.id, f.number) for subj in subjects for f in subj.floors for s in f.skills}
    order = {subj.id: subj.order for subj in subjects}
    by_node: dict[str, list[Part]] = {}
    for node in t.nodes.values():
        groups: dict[tuple[str, int], set[str]] = {}
        for s in node.skills:
            if s in home:
                groups.setdefault(home[s], set()).add(s)
        out = []
        for subject_id, floor in sorted(groups, key=lambda k: (order.get(k[0], 99), k[1])):
            path_order = [k.id for k in math_path.subject(subject_id).floor(floor).skills]
            out.append(Part(node.id, subject_id, floor,
                            tuple(s for s in path_order if s in groups[(subject_id, floor)])))
        by_node[node.id] = out
    _cache.clear()
    _cache.update(tree=t, subjects=subjects, home=home, parts=by_node)
    return _cache


def skill_home() -> dict[str, tuple[str, int]]:
    """micro-skill -> (subject, floor) it lives on."""
    return _structure()["home"]


def parts(node: math_tree.Node | str) -> list[Part]:
    """R1: the parts of a node, in floor order; none for a node without micro-skills."""
    node_id = node if isinstance(node, str) else node.id
    return list(_structure()["parts"].get(node_id, []))


def node_order(node: math_tree.Node) -> tuple:
    """Tree order: realm, stage, node id (an optional node has no stage and comes last)."""
    return (not node.main, tree().realm_order[node.realm], node.stage or 99, node.id)


def all_parts(main_only: bool = False) -> list[Part]:
    """Every part of every node, in tree order."""
    t = tree()
    nodes = sorted((n for n in t.nodes.values() if n.main or not main_only), key=node_order)
    return [p for n in nodes for p in parts(n)]


def floor_parts(subject_id: str, floor: int) -> list[Part]:
    """The parts that live on this floor, main-path ones first, by stage."""
    return [p for p in all_parts() if p.subject_id == subject_id and p.floor == floor]


def part_of(subject_id: str, floor: int, node_id: str | None = None) -> Part | None:
    """The part of `node_id` on this floor. Without a node: the whole floor, as an old
    sitting with no node sees it (None for a floor that does not exist)."""
    if node_id is None:
        try:
            skills = tuple(k.id for k in math_path.subject(subject_id).floor(floor).skills)
        except KeyError:
            return None
        return Part(None, subject_id, floor, skills)
    return next((p for p in parts(node_id) if p.subject_id == subject_id and p.floor == floor), None)


def run_part(run: MathRun) -> Part | None:
    """The part a sitting is on (a whole floor for an old sitting without a node)."""
    return part_of(run.subject_id, run.floor, getattr(run, "node_id", None))


def _templates(subject_id: str, floor: int) -> list:
    from . import math_practice         # (it imports this module)
    return math_practice._templates(subject_id, floor)


def question_count(part: Part, bank: dict | None = None) -> int:
    """How many question templates this server has for the part's micro-skills."""
    key = (part.subject_id, part.floor)
    if bank is not None and key in bank:
        templates = bank[key]
    else:
        templates = _templates(*key)
        if bank is not None:
            bank[key] = templates
    skills = set(part.skills)
    return sum(1 for t in templates if t.skill in skills)


def problem_available(problem_id: str) -> bool:
    p = math_problems.bank().get(problem_id)
    return p is not None and (p.reviewed or settings.allow_unreviewed)


# ------------------------------------------------------------------ sources
@lru_cache(maxsize=32)
def _sources(branch: str) -> dict:
    try:
        raw = json.loads((SOURCES_DIR / f"{branch}.json").read_text("utf-8"))
    except (OSError, ValueError):
        return {}
    nodes = raw.get("nodes") if isinstance(raw, dict) else None
    return nodes if isinstance(nodes, dict) else {}


def source(node: math_tree.Node) -> dict | None:
    """The node's first suggested reading (its `primary` source), or None."""
    entry = _sources(node.branch).get(node.id)
    primary = entry.get("primary") if isinstance(entry, dict) else None
    if not isinstance(primary, dict):
        return None
    return {k: primary.get(k) for k in SOURCE_KEYS}


# ------------------------------------------------------------------ a player's position
@dataclass
class TreeState:
    tree: math_tree.Tree
    status: dict[str, str]                       # node -> open | done | locked | vacant
    passed_parts: set[tuple[str, str, int]]      # parts passed by a trial on the part itself
    legacy: dict[str, set[int]]                  # subject -> floors covered whole (old trial, placement)
    trial_floors: dict[str, set[int]]            # subject -> floors with any passed trial
    placement: dict[str, set[int]]               # subject -> floors skipped by the placement test
    solved: set[str]                             # programming exercises fully solved
    counts: dict[tuple, int] = field(default_factory=dict)     # part key -> question templates

    @property
    def vacant(self) -> set[str]:
        return {n for n, s in self.status.items() if s == VACANT}

    @property
    def done(self) -> set[str]:
        """Done for `requires` and for the stage (R3): finished, or vacant."""
        return {n for n, s in self.status.items() if s in (DONE, VACANT)}

    @property
    def open(self) -> list[str]:
        """The open nodes, main-path ones first, in tree order."""
        return [n.id for n in sorted(self.tree.nodes.values(), key=node_order) if self.status[n.id] == OPEN]

    @property
    def stage(self) -> tuple[str, int]:
        """The stage reached (R5). Vacant nodes count as done, so a realm that is not written
        at all would be walked straight through: the position stops at the end of the last
        realm that has anything to learn, instead of running on to the last realm of the tree."""
        done = self.done
        skills = [s for n in done for s in self.tree.nodes[n].skills]
        realm, stage = self.tree.stage_reached(skills, done)
        order = self.tree.realm_order
        written = [r for r in order if any(self.status[n.id] != VACANT for n in self.tree.main_nodes(r))]
        if written:
            last = max(written, key=order.get)
            if order[realm] > order[last]:
                return last, self.tree.realm_stages[last]
        return realm, stage

    def has_questions(self, part: Part) -> bool:
        return self.counts.get(part.key, 0) > 0

    def part_passed(self, part: Part) -> bool:
        return part.key in self.passed_parts or part.floor in self.legacy.get(part.subject_id, set())

    def part_open(self, part: Part) -> bool:
        """Open to learn: its node is open, it has questions and it is not passed yet."""
        return self.status.get(part.node_id) == OPEN and self.has_questions(part) and not self.part_passed(part)

    def playable(self, part: Part) -> bool:
        """May be practised: it has questions and its node is open or done, or it is passed."""
        return self.has_questions(part) and (
            self.status.get(part.node_id) in (OPEN, DONE) or self.part_passed(part))

    def missing(self, node_id: str) -> list[str]:
        """The nodes this one requires that are not done yet."""
        done = self.done
        return [r for r in self.tree.nodes[node_id].requires if r not in done]


async def _placement_floors(db: AsyncSession, user_id: int) -> dict[str, set[int]]:
    from . import math_practice
    return {s.id: await math_practice.placement_floors(db, user_id, s.id) for s in math_path.subjects()}


async def state(db: AsyncSession, user_id: int) -> TreeState:
    """Everything about this player's place in the tree, read in a few queries."""
    t = tree()
    rows = (await db.execute(select(MathRun.subject_id, MathRun.floor, MathRun.node_id).where(
        MathRun.user_id == user_id, MathRun.mode == TRIAL, MathRun.passed.is_(True)).distinct())).all()
    passed: set[tuple[str, str, int]] = set()
    legacy: dict[str, set[int]] = {}
    trials: dict[str, set[int]] = {}
    for subject_id, floor, node_id in rows:
        trials.setdefault(subject_id, set()).add(floor)
        if node_id is None:
            legacy.setdefault(subject_id, set()).add(floor)
        else:
            passed.add((node_id, subject_id, floor))
    placement = await _placement_floors(db, user_id)
    for subject_id, floors in placement.items():
        legacy.setdefault(subject_id, set()).update(floors)

    wanted = sorted({p for n in t.nodes.values() for p in n.problems if problem_available(p)})
    solved: set[str] = set()
    if wanted:
        for pid, ok, total in (await db.execute(select(
                MathSubmission.problem_id, MathSubmission.passed, MathSubmission.total).where(
                MathSubmission.user_id == user_id, MathSubmission.problem_id.in_(wanted),
                MathSubmission.judged_at.is_not(None)))).all():
            if total and ok >= total:
                solved.add(pid)

    st = TreeState(tree=t, status={}, passed_parts=passed, legacy=legacy, trial_floors=trials,
                   placement=placement, solved=solved)
    bank: dict = {}
    finished: dict[str, str] = {}
    for node in t.nodes.values():
        asked = []
        for p in parts(node):
            st.counts[p.key] = question_count(p, bank)
            if st.counts[p.key]:
                asked.append(p)
        problems = [p for p in node.problems if problem_available(p)]
        if not asked and not problems:
            finished[node.id] = VACANT
        elif all(st.part_passed(p) for p in asked) and all(p in solved for p in problems):
            finished[node.id] = DONE
    done = set(finished)
    for node in t.nodes.values():
        st.status[node.id] = finished.get(node.id) or (OPEN if set(node.requires) <= done else LOCKED)
    return st


# ------------------------------------------------------------------ R9, R12: the three primitives
async def _state(db: AsyncSession, user_id: int, st: TreeState | None) -> TreeState:
    return st if st is not None else await state(db, user_id)


def frontier_of(st: TreeState, subject_id: str) -> Part | None:
    mains = [p for p in all_parts(main_only=True) if p.subject_id == subject_id and st.has_questions(p)]
    first_open = next((p for p in mains if st.part_open(p)), None)
    if first_open is not None:
        return first_open
    passed = [p for p in mains if st.part_passed(p)]
    if passed:
        return passed[-1]
    return mains[0] if mains else None


async def frontier(db: AsyncSession, user_id: int, subject_id: str, st: TreeState | None = None) -> Part | None:
    """R9: where this player's questions of this subject come from outside a sitting."""
    return frontier_of(await _state(db, user_id, st), subject_id)


def reached_floors_of(st: TreeState, subject_id: str) -> set[int]:
    return {p.floor for p in all_parts(main_only=True) if p.subject_id == subject_id
            and (st.part_open(p) or (st.has_questions(p) and st.part_passed(p)))}


async def reached_floors(db: AsyncSession, user_id: int, subject_id: str,
                         st: TreeState | None = None) -> set[int]:
    """R12: the floors of this subject that hold a main-path part which is open or passed -
    the floors that may be shown or entered."""
    return reached_floors_of(await _state(db, user_id, st), subject_id)


def working_position_of(st: TreeState) -> tuple[str, int]:
    realm, stage = st.stage
    return realm, min(stage + 1, st.tree.realm_stages[realm])


async def working_stage(db: AsyncSession, user_id: int, st: TreeState | None = None) -> int:
    """R12: the stage being worked on in the player's current realm: one above the stage
    reached, never above the realm's last stage."""
    return working_position_of(await _state(db, user_id, st))[1]


async def working_position(db: AsyncSession, user_id: int, st: TreeState | None = None) -> tuple[str, int]:
    """(realm, working stage): `working_stage` with the realm it counts in."""
    return working_position_of(await _state(db, user_id, st))


def allowed_skills_of(st: TreeState, optional: bool = False) -> set[str]:
    cut = st.tree.cut_skills()
    return {s for n in st.tree.nodes.values()
            if st.status[n.id] in (OPEN, DONE, VACANT) and (n.main or optional)
            for s in n.skills if s not in cut}


def finished_optional_skills_of(st: TreeState) -> set[str]:
    """The micro-skills of optional nodes the player has finished. Their own sittings are
    behind them, so, like review (R6), a mode may ask them again - a tower whose area is an
    optional node opens this way."""
    cut = st.tree.cut_skills()
    return {s for n in st.tree.nodes.values() if not n.main and st.status[n.id] == DONE
            for s in n.skills if s not in cut}


async def allowed_skills(db: AsyncSession, user_id: int, st: TreeState | None = None,
                         optional: bool = False) -> set[str]:
    """The micro-skills of open or done nodes, minus the cut ones. Outside a node's own
    sittings an optional node's micro-skills are never asked (R6), so they are left out
    unless `optional` is set."""
    return allowed_skills_of(await _state(db, user_id, st), optional)


def cleared_floors_of(st: TreeState, subject_id: str) -> set[int]:
    out = set()
    try:
        subject = math_path.subject(subject_id)
    except KeyError:
        return out
    for f in subject.floors:
        here = [p for p in floor_parts(subject_id, f.number) if st.has_questions(p)]
        if not here:
            continue
        mains = [p for p in here if tree().nodes[p.node_id].main] or here
        if all(st.part_passed(p) for p in mains):
            out.add(f.number)
    return out


async def cleared_floors(db: AsyncSession, user_id: int, subject_id: str, st: TreeState | None = None) -> set[int]:
    """Compatibility only: the floors all of whose main-path parts are passed (a floor with
    only optional parts: all of them). Callers that need "where is the player" read the
    frontier, the reached floors or the working stage instead."""
    return cleared_floors_of(await _state(db, user_id, st), subject_id)


def floor_part(st: TreeState, subject_id: str, floor: int) -> Part | None:
    """R11: the part an old "sit down on floor n" means - the open part on that floor (the
    first by stage when several nodes share it), else the first one that may be practised;
    None when no part there is open or done."""
    here = [p for p in floor_parts(subject_id, floor) if st.has_questions(p)]
    return next((p for p in here if st.part_open(p)), None) or next((p for p in here if st.playable(p)), None)


def problem_open(st: TreeState, problem: math_problems.Problem) -> bool:
    """R10: an exercise is open when its micro-skill is in an open or done node."""
    owner = st.tree.node_of_skill().get(problem.skill)
    return owner is not None and st.status.get(owner) in (OPEN, DONE, VACANT)


def locked_message(st: TreeState, node_ids: list[str]) -> str:
    """Why a node (or a floor's first node) is shut, naming what to finish first."""
    t = st.tree
    missing: list[str] = []
    for nid in node_ids:
        for r in st.missing(nid):
            if r not in missing:
                missing.append(r)
    names = ", ".join(t.nodes[r].name_vi for r in missing)
    return f"Nút này chưa mở. Hãy học xong trước: {names}." if names else "Nút này chưa mở."


# ------------------------------------------------------------------ the view
def stage_view(st: TreeState) -> dict:
    realm, stage = st.stage
    raw = next(r for r in st.tree.raw["realms"] if r["id"] == realm)
    return {"realm": realm, "realm_name_vi": raw["name_vi"], "stage": stage, "stages": raw["stages"]}


async def part_view(db: AsyncSession, user_id: int, st: TreeState, part: Part, config: dict | None = None,
                    with_gate: bool = True) -> dict:
    from . import math_practice
    config = config or math_path.cfg()
    lo, hi = math_path.floor_tiers(part.floor, config)
    subject = math_path.subject(part.subject_id)
    docs = math_library.for_floor(part.subject_id, part.floor)
    gate = None
    if with_gate and st.playable(part):
        gate = (await math_practice.part_gate(db, user_id, part, config)).view()
    return {"subject_id": part.subject_id, "floor": part.floor, "questions": st.counts.get(part.key, 0),
            "tier_min": lo, "tier_max": hi, "passed": st.part_passed(part), "open": st.part_open(part),
            "gate": gate, "trial_total": math_mastery.trial_cfg(config)["questions_per_skill"] * len(part.skills),
            "doc_id": docs[0].id if docs else None,
            "skills": [{"id": s, "name_vi": subject.skills[s].name_vi} for s in part.skills]}


async def tree_view(db: AsyncSession, user: User) -> dict:
    """GET /math/tree: every node with its state, parts, exercises and suggested reading,
    the stage reached, the open nodes to do next and the sitting left open."""
    from . import math_practice
    st = await state(db, user.id)
    t = st.tree
    config = math_path.cfg()
    nodes = []
    for node in sorted(t.nodes.values(), key=node_order):
        status = st.status[node.id]
        nodes.append({
            "id": node.id, "branch": node.branch, "realm": node.realm, "stage": node.stage,
            "status": node.status, "kind": node.kind, "name_vi": node.name_vi, "why_vi": node.why_vi,
            "topics_vi": list(node.topics_vi), "state": status,
            "state_vi": VACANT_VI if status == VACANT else None,
            "requires": [{"id": r, "name_vi": t.nodes[r].name_vi, "done": r in st.done} for r in node.requires],
            "reinforces": list(node.reinforces),
            "parts": [await part_view(db, user.id, st, p, config, with_gate=status != LOCKED)
                      for p in parts(node) if st.has_questions(p)],
            "problems": [{"id": pid, "title_vi": math_problems.bank()[pid].title_vi, "solved": pid in st.solved}
                         for pid in node.problems if problem_available(pid)],
            "source": source(node)})
    run = await math_practice.open_run(db, user.id)
    return {"wired": bool(t.raw.get("wired")), "stage": stage_view(st),
            "branches": [{"id": b["id"], "name_vi": b["name_vi"], "subject": b.get("subject")}
                         for b in t.raw.get("branches", [])],
            "nodes": nodes,
            "next": [n for n in st.open if t.nodes[n].main],
            "run": math_practice.run_view(run) if run else None}
