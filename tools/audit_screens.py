#!/usr/bin/env python3
"""Open every screen of the game headlessly with realistic worst-case data and report what is
cut, covered, clipped, outside its panel or drawn with a missing glyph:

    SDL_VIDEODRIVER=dummy python tools/audit_screens.py [--scales 2,3] [--only hub,guide] [--shots DIR]

Each case builds one scene the way the game does, with a fake game whose api answers GET/POST
synchronously with payloads shaped like the server's (built from the server's own data files
and pure helpers: tree.json, guide.json, achievements.json, linh_can.json, td.json, ...), the
longest real strings put where they hurt most. The scene is drawn twice (the first frame may
settle a tab or a scroll), with the kit's audit recorder on (client/ui/kit.py), and the
records go through client/ui/audit.py plus three checks of this tool:

    glyph     a character neither VT323 nor the Noto fallback can draw (it would be a box), or
              a Chinese character (the game never shows any)
    ellipsis  a text drawn cut with "..." (mathdraw.fit and friends do not call note_cut)
    label     a button whose label is wider than the button

`ALLOWED` lists the cuts that are meant (a list row whose whole text is one click or one
hover away), each with its reason; they are reported apart and are not hard problems.

Writes tools/reports/screens_audit.md (counts per screen, every problem) unless --no-report.
Exit code 1 when a hard problem is left."""
from __future__ import annotations

import argparse
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "server"))
sys.path.insert(0, str(ROOT / "tools"))

import screens_data  # noqa: E402,F401 - first: it points the server at its own throw-away database

import pygame  # noqa: E402

from client.engine.display import Display  # noqa: E402
from client.engine.text import Fonts  # noqa: E402
from client.ui import audit  # noqa: E402
from client.ui.kit import UI  # noqa: E402
from client.ui.mathtext import MARKERS  # noqa: E402

REPORT = ROOT / "tools" / "reports" / "screens_audit.md"
EXTRA_HARD = ("glyph", "ellipsis", "label")
HARD = tuple(audit.HARD) + EXTRA_HARD

# (screen, text it contains) -> why the cut is meant. A cut not listed here is a hard problem.
ALLOWED: dict[tuple[str, str], str] = {
    ("hub", "Thiên kiếp Trúc Cơ: một bài toán"): "a Chính đạo stage list row in two columns (the tool puts the "
    "longest name of the tree there): the whole name is in the card above it and on hover",
    ("achievements", "Linh Thạch, "): "the reward list of a tier keeps to two lines beside the claim button; "
    "the whole list is the card's tooltip",
    ("guide", "Thiên kiếp Trúc Cơ: một bài toán"): "the stage list under the Chính đạo entry in two columns "
    "(the tool puts the longest name there): whole in the entry's title and on hover",
    ("bag", "trên Đạo Thụ (đang ở"): "why a weapon is still locked, on its 18 px row: whole on hover",
    ("cong_phap", ""): "a chiêu name in its 64 px cell: whole on hover and in the details when picked",
}


# ------------------------------------------------------------------ the fake game
class FakeApi:
    """GET / POST answered at once from `routes` (path prefix -> payload or callable(body))."""

    def __init__(self, routes: dict | None = None):
        self.routes = routes or {}
        self.calls: list[tuple[str, str]] = []

    def _answer(self, path: str, body, ok):
        self.calls.append(("call", path))
        for prefix in sorted(self.routes, key=len, reverse=True):
            if path.startswith(prefix):
                v = self.routes[prefix]
                ok(v(body) if callable(v) else v)
                return

    def get(self, path, ok=None, err=None, *a, **k):
        if ok:
            self._answer(path, None, ok)

    def post(self, path, body=None, ok=None, err=None, *a, **k):
        if ok:
            self._answer(path, body, ok)


def fake_game(ui: UI, routes: dict | None = None, **state):
    st = SimpleNamespace(guide=None, me={"spirit_stones": 1234567, "immortal_jade": 88, "tutorial_step": 5,
                                         "title": None},
                         pets=None, character={"realm": "truc_co"}, inv=None, guide_welcome=True)
    for k, v in state.items():
        setattr(st, k, v)
    noop = lambda *a, **k: None  # noqa: E731
    g = SimpleNamespace(ui=ui, api=FakeApi(routes), audio=SimpleNamespace(play=noop), state=st, scenes=[],
                        toast=noop, push=lambda s: g.scenes.append(s), pop=noop, api_error=noop, on_xp=noop,
                        refresh_me=noop, refresh_cult=noop, refresh_inv=noop, refresh_guide=noop, refresh_pets=noop,
                        set_guide=noop, open_guide=noop, guide_seen=noop, open_math=noop, open_char=noop, now=0.0)
    g.top = None
    g.game = g
    return g


# ------------------------------------------------------------------ the extra checks
class Glyphs:
    def __init__(self, fonts: Fonts):
        self.f = fonts
        self.cache: dict[str, bool] = {}
        fb = fonts.font("fallback", 16)
        nd = fb.render("", False, (255, 255, 255))
        self.notdef = (nd.get_size(), pygame.image.tobytes(nd, "RGBA"))

    def ok(self, ch: str) -> bool:
        if ch not in self.cache:
            if 0x3400 <= ord(ch) <= 0x9FFF or 0xF900 <= ord(ch) <= 0xFAFF or 0x20000 <= ord(ch):
                self.cache[ch] = False                      # Chinese: never in this game
            elif ch in " \n\t" or ch in MARKERS or self.f._ui_has(ch):
                self.cache[ch] = True
            else:
                g = self.f.font("fallback", 16).render(ch, False, (255, 255, 255))
                self.cache[ch] = (g.get_size(), pygame.image.tobytes(g, "RGBA")) != self.notdef
        return self.cache[ch]


def extra_problems(records, glyphs: Glyphs) -> list[audit.Problem]:
    out = []
    buttons = {r["id"]: r for r in records if r.get("kind") == "button"}
    for r in records:
        if r.get("kind") != "text":
            continue
        txt = r.get("text") or ""
        bad = sorted({c for c in txt if not glyphs.ok(c)})
        if bad:
            out.append(audit.Problem("glyph", txt, r.get("ink"), " ".join(f"U+{ord(c):04X}" for c in bad)))
        flat = txt.replace("\n", " ").strip()
        if (flat.endswith("...") or flat.endswith("…")) and flat not in ("...", "…"):
            out.append(audit.Problem("ellipsis", txt, r.get("ink")))
        own = buttons.get(r.get("owner"))
        if own is not None and r.get("ink") and txt.strip():
            ink, box = r["ink"], own["rect"]
            if ink[2] > box[2] + 0.5 or ink[3] > box[3] + 1.0:
                out.append(audit.Problem("label", txt, ink, own["id"]))
    return out


def allowed(screen: str, p: audit.Problem) -> str | None:
    if p.kind not in ("ellipsis", "cut"):
        return None
    for (scr, prefix), why in ALLOWED.items():
        if scr == screen and prefix in p.text.replace("\n", " "):
            return why
    return None


# ------------------------------------------------------------------ server data, as the server shapes it
def _tree():
    from app.learning import math_tree
    return math_tree.tree()


def longest_node_texts() -> tuple[str, str]:
    nodes = list(_tree().nodes.values())
    name = max(nodes, key=lambda n: len(n.name_vi)).name_vi
    why = max(nodes, key=lambda n: len(n.why_vi or "")).why_vi
    return name, why


def tree_payload(realm: str = "luyen_khi", stage: int = 5, step: str = "luyen", longest: bool = True,
                 run_on: str | None = None) -> dict:
    """GET /math/tree for a player working on `stage` of `realm`: the stages before are done,
    the first main node of the stage is the current one (Chính đạo), the other nodes of the
    stage open, later stages locked; optional nodes open. Parts, gates, sources, exercises and
    chiêu are the real ones of the data files."""
    from app.learning import math_path, math_problems
    from app.systems import math_skills
    from app.systems import math_tree_progress as tp
    t = _tree()
    cfg = math_path.cfg()
    realms = {r["id"]: r for r in t.raw["realms"]}
    order = t.realm_order
    branch_vi = {b["id"]: b["name_vi"] for b in t.raw["branches"]}
    opens: dict = {}
    for sid, sk in math_skills.skills().items():
        for nid in sk["unlock"].get("nodes", []):
            opens.setdefault(nid, []).append({"id": sid, "name_vi": sk["name_vi"], "element": sk["element"]})
    mains = sorted((n for n in t.main_nodes(realm) if n.stage == stage), key=tp.node_order)
    current = mains[0]

    def state_of(n) -> str:
        if not n.main:
            return "open"
        if order[n.realm] < order[realm] or (n.realm == realm and (n.stage or 0) < stage):
            return "done"
        if n.realm == realm and n.stage == stage:
            return "open"
        return "locked"
    states = {n.id: state_of(n) for n in t.nodes.values()}
    bank = math_problems.bank()
    nodes = []
    for node in sorted(t.nodes.values(), key=tp.node_order):
        s = states[node.id]
        parts = []
        for p in tp.parts(node):
            if tp.question_count(p) <= 0:
                continue
            lo, hi = math_path.floor_tiers(p.floor, cfg)
            subj = math_path.subject(p.subject_id)
            skills = [{"skill": k, "tier": hi - 1, "top_tier": hi, "at_top": False, "answered": 7, "correct": 5,
                       "needed": 8, "window": 10, "ok": i == 0} for i, k in enumerate(p.skills)]
            gate = None if s == "locked" else {"floor": p.floor, "ok": False, "skills": skills, "weak": []}
            parts.append({"subject_id": p.subject_id, "floor": p.floor, "questions": tp.question_count(p),
                          "tier_min": lo, "tier_max": hi, "passed": s == "done", "open": s == "open",
                          "gate": gate, "trial_total": 2 * len(p.skills), "doc_id": "doc_" + p.subject_id,
                          "skills": [{"id": k, "name_vi": subj.skills[k].name_vi} for k in p.skills]})
        if node.id == mains[1].id if len(mains) > 1 else False:
            for p in parts:                          # one node of the stage has its gate open
                if p["gate"]:
                    p["gate"]["ok"] = True
        nodes.append({
            "id": node.id, "branch": node.branch, "realm": node.realm, "stage": node.stage, "status": node.status,
            "kind": node.kind, "name_vi": node.name_vi, "why_vi": node.why_vi, "path": t.path_rank.get(node.id),
            "topics_vi": list(node.topics_vi), "state": s, "state_vi": None,
            "requires": [{"id": r, "name_vi": t.nodes[r].name_vi, "done": states[r] == "done"} for r in node.requires],
            "reinforces": list(node.reinforces), "parts": parts,
            "problems": [{"id": pid, "title_vi": bank[pid].title_vi, "solved": False, "subject_id": bank[pid].subject}
                         for pid in node.problems if pid in bank],
            "source": tp.source(node), "chieu": opens.get(node.id, [])})
    by_id = {n["id"]: n for n in nodes}
    stage_nodes = [{"id": n.id, "name_vi": n.name_vi, "branch": n.branch, "branch_vi": branch_vi.get(n.branch, n.branch),
                    "kind": n.kind, "state": "now" if n.id == current.id else "later"} for n in mains]
    name, why = (longest_node_texts() if longest else (current.name_vi, current.why_vi))
    if longest:
        stage_nodes[0]["name_vi"] = name
        by_id[current.id]["name_vi"], by_id[current.id]["why_vi"] = name, why
    cur_parts = by_id[current.id]["parts"]
    part = cur_parts[0] if cur_parts else None
    main = {"node_id": current.id, "path": t.path_rank.get(current.id), "name_vi": name, "why_vi": why,
            "branch": current.branch, "branch_vi": branch_vi.get(current.branch, current.branch), "kind": current.kind,
            "realm": realm, "realm_name_vi": realms[realm]["name_vi"], "stage": stage,
            "index": 1, "total": len(mains), "step": step,
            "done": {"hieu": step != "hoc", "luyen": step in ("kiep", "code"), "kiep": step == "code"},
            "part": ({"subject_id": part["subject_id"], "floor": part["floor"], "index": 2, "count": 2}
                     if part else None),
            "gate": {"done": 3, "total": 7, "ok": step == "kiep"}, "doc_id": "doc1", "block": 2,
            "subject_id": part["subject_id"] if part else None, "floor": part["floor"] if part else 1,
            "problems": [], "problems_done": 0, "problems_total": 0, "resume": None, "stage_nodes": stage_nodes,
            "path_done": sum(1 for n in t.main_nodes(realm) if states[n.id] == "done"),
            "path_total": len(t.main_nodes(realm))}
    if step == "code":
        main.update(problems=[{"id": "p", "title_vi": "Bài tập", "solved": False}] * 7, problems_done=3,
                    problems_total=7, part=None, gate=None)
    if step == "done":
        main = {**main, "node_id": None, "name_vi": None, "why_vi": None, "stage_nodes": [], "index": 0, "total": 0}
    run = None
    if run_on:
        n = by_id[run_on]
        p = n["parts"][0]
        run = {"run_id": 7, "subject_id": p["subject_id"], "floor": p["floor"], "mode": "practice",
               "node_id": run_on, "node_name_vi": n["name_vi"]}
    return {"wired": True, "stage": {"realm": realm, "realm_name_vi": realms[realm]["name_vi"], "stage": stage - 1,
                                     "stages": realms[realm]["stages"],
                                     "progress": {"stage": stage, "done": 0, "total": len(mains)}},
            "branches": [{"id": b["id"], "name_vi": b["name_vi"], "subject": b.get("subject")} for b in t.raw["branches"]],
            "nodes": nodes, "next": [n.id for n in mains], "main": main, "run": run}


def path_payload(placement: str = "offered") -> dict:
    """GET /math/path, the parts the hub reads: subjects with their exercise count and the
    bài kiểm tra đầu vào brief."""
    from app.learning import math_path
    out = []
    for s in math_path.subjects():
        out.append({"id": s.id, "name_vi": s.name_vi, "order": s.order, "floors": [], "cleared": [],
                    "next_floor": 2, "problems": 6,
                    "placement": {"status": placement, "offered": placement == "offered", "planned": 24,
                                  "run_id": 3 if placement == "in_progress" else None, "start_floor": None,
                                  "abandoned": None}})
    return {"subjects": out, "run": None, "tree": {}, "tiers": {}}


def longest_branch_tab(tree: dict) -> str:
    """The branch whose tab lists the most rows (the most to scroll, the most to cut)."""
    from client.scenes import math_tree as MT
    tabs = [t["id"] for t in MT.tab_list(tree) if t["id"] != MT.NEXT_TAB]
    return max(tabs, key=lambda b: len(MT.node_rows(tree, b)))


# ------------------------------------------------------------------ the cases
# A case: (screen, name, builder(ui) -> (scene, panel or None)). Builders get a fresh fake game.
CASES: list[tuple[str, str, object]] = []


def case(screen: str, name: str):
    def deco(fn):
        CASES.append((screen, name, fn))
        return fn
    return deco


HUB = (40, 16, 400, 238)


def hub_scene(ui, tree, path=None, tab=None, summary=None, trial=None):
    from client.scenes.math_practice import MathPracticeScene
    g = fake_game(ui, {"/math/path": path or path_payload(), "/math/tree": tree})
    hub = MathPracticeScene(g)
    hub.on_enter()
    if tab:
        hub.tab = tab
    if summary is not None:
        hub.summary, hub.trial = summary, trial
    return hub


for _step in ("hoc", "luyen", "kiep", "code"):
    def _mk(step):
        def build(ui):
            return hub_scene(ui, tree_payload(step=step)), HUB
        return build
    case("hub", f"chinh_dao_{_step}_longest")(_mk(_step))


@case("hub", "chinh_dao_real_stage5")
def _hub_real(ui):
    return hub_scene(ui, tree_payload(step="luyen", longest=False)), HUB


@case("hub", "chinh_dao_done")
def _hub_done(ui):
    return hub_scene(ui, tree_payload(step="done")), HUB


def _branch_cases():
    from client.scenes import math_tree as MT
    tree = tree_payload()
    for tab in MT.tab_list(tree):
        if tab["id"] == MT.NEXT_TAB:
            continue

        def build(ui, tid=tab["id"]):
            return hub_scene(ui, tree_payload(), tab=tid), HUB
        case("hub", f"tab_{tab['id']}")(build)

        def build_end(ui, tid=tab["id"]):           # the list scrolled to its end
            h = hub_scene(ui, tree_payload(), tab=tid)
            h.first = 999
            return h, HUB
        case("hub", f"tab_{tab['id']}_end")(build_end)


_branch_cases()


@case("hub", "tab_placement_in_progress")
def _hub_place(ui):
    tree = tree_payload()
    return hub_scene(ui, tree, path=path_payload("in_progress"), tab="ds"), HUB


def summary_payload(longest=True) -> dict:
    name, _ = longest_node_texts()
    return {"run_id": 7, "subject_id": "giai_tich", "floor": 3, "mode": "practice", "node_id": "gt_x",
            "node_name_vi": name if longest else "Đạo hàm", "tier": 4, "tier_name_vi": "Thành thạo", "tier_min": 2,
            "tier_max": 5, "combo": 3, "best_combo": 17, "asked": 40, "correct": 33, "review_asked": 6,
            "xp_gained": 1260, "passed": None, "ended": True, "ladders": 3}


@case("summary", "sitting_longest")
def _sum_sitting(ui):
    tree = tree_payload()
    cur = tree["main"]["node_id"]
    s = summary_payload()
    parts = next(n for n in tree["nodes"] if n["id"] == cur)["parts"]
    s["node_id"], s["floor"] = cur, (parts[0]["floor"] if parts else 1)
    return hub_scene(ui, tree, summary=s), HUB


@case("summary", "trial_passed_opens_many")
def _sum_trial(ui):
    tree = tree_payload()
    opened = sorted((n for n in tree["nodes"] if n["state"] == "open"), key=lambda n: -len(n["name_vi"]))[:6]
    trial = {"passed": True, "correct": 14, "asked": 15, "node_done": True, "opened": [n["id"] for n in opened]}
    return hub_scene(ui, tree, summary=summary_payload(), trial=trial), HUB


@case("summary", "trial_failed")
def _sum_trial_failed(ui):
    trial = {"passed": False, "correct": 9, "asked": 15, "node_done": False, "opened": []}
    return hub_scene(ui, tree_payload(), summary=summary_payload(), trial=trial), HUB


# -------- the node card
def node_card(ui, node_id=None, pick=None):
    from client.scenes.math_tree import NodeCardScene
    tree = tree_payload()
    nodes = tree["nodes"]
    node = next(n for n in nodes if n["id"] == node_id) if node_id else pick(nodes)
    return NodeCardScene(fake_game(ui), node, tree), NodeCardScene.PANEL


@case("node_card", "longest_name")
def _nc_name(ui):
    return node_card(ui, pick=lambda ns: max(ns, key=lambda n: len(n["name_vi"])))


@case("node_card", "longest_why")
def _nc_why(ui):
    return node_card(ui, pick=lambda ns: max(ns, key=lambda n: len(n["why_vi"] or "")))


@case("node_card", "most_requires")
def _nc_req(ui):
    return node_card(ui, pick=lambda ns: max(ns, key=lambda n: len(n["requires"])))


@case("node_card", "most_lines_scrolled_end")
def _nc_long(ui):
    scene, panel = node_card(ui, pick=lambda ns: max(ns, key=lambda n: len(n["requires"]) + len(n["problems"])
                                                     + len(n["topics_vi"]) + len(n["chieu"]) + len(n["why_vi"] or "") / 60))
    scene.first = 999
    return scene, panel


@case("node_card", "with_exercises")
def _nc_ex(ui):
    return node_card(ui, pick=lambda ns: max(ns, key=lambda n: len(n["problems"])))


@case("node_card", "locked_optional")
def _nc_opt(ui):
    return node_card(ui, pick=lambda ns: next((n for n in ns if n["status"] != "chinh" and n["state"] == "locked"),
                                              next(n for n in ns if n["status"] != "chinh")))


@case("node_card", "longest_source_url")
def _nc_url(ui):
    return node_card(ui, pick=lambda ns: max(ns, key=lambda n: len((n["source"] or {}).get("url") or "")
                                             + len((n["source"] or {}).get("where") or "")))


# ------------------------------------------------------------------ the other screens, on real payloads
# (tools/screens_data.py runs the server in this process and GETs what each screen reads)
AUTO = "auto"           # the panel: the largest one the scene drew


def payload(path: str) -> dict:
    import copy

    import screens_data
    got = screens_data.harvest()
    if path not in got:
        raise RuntimeError(f"no payload for {path}: {got.get('_failed', {}).get(path, 'not fetched')}")
    return copy.deepcopy(got[path])


def real_game(ui, **state):
    """A fake game whose api answers every GET / POST with the harvested payload of its path."""
    import screens_data
    routes = {k: v for k, v in screens_data.harvest().items() if not k.startswith("_")}
    return fake_game(ui, routes, **state)


def _longest(items, key):
    return max(items, key=lambda i: len(str(i.get(key) or ""))) if items else None


# -------- the guide board, its handbook and the HUD tracker
def _guide(ui, tab="road", topic=None, longest=True):
    from client.scenes.guide import GuideScene
    view = payload("/guide")
    if longest:
        name, why = longest_node_texts()
        m = view.get("main") or {}
        if isinstance(m, dict) and m.get("title"):
            m["title"] = name
    g = real_game(ui, guide=view)
    s = GuideScene(g, tab=tab, topic=topic)
    try:
        s.on_enter()
    except Exception:           # noqa: BLE001 - on_enter only refreshes
        pass
    return s, AUTO


case("guide", "road")(lambda ui: _guide(ui))
case("guide", "road_real")(lambda ui: _guide(ui, longest=False))


def _guide_topics():
    try:
        topics = [t["id"] for t in (payload("/guide").get("handbook") or [])]
    except Exception:           # noqa: BLE001 - reported by the case itself
        topics = []
    for tid in topics:
        case("guide", f"book_{tid}")(lambda ui, tid=tid: _guide(ui, tab="book", topic=tid))


class _TrackerScene:
    """The HUD tracker of the guide, where the world draws it."""

    def __init__(self, game):
        self.game = game

    def draw_ui(self, ui):
        from client.scenes import guide
        ui.panel(476 - guide.TRACKER_W - 4, 0, guide.TRACKER_W + 8, 90)      # (a frame for the audit only)
        guide.draw_tracker(ui, self.game, 476 - guide.TRACKER_W, 4, True)


@case("guide", "hud_tracker_welcome")
def _tracker(ui):
    return _TrackerScene(real_game(ui, guide=payload("/guide"))), None


def _main_led(step="luyen"):
    """The guide once Chính đạo leads, its entry the current node with the longest name and why."""
    view = payload("/guide")
    view["lead"] = "main"
    view["main"] = tree_payload(step=step)["main"]
    view["claimable"] = 3
    return view


@case("guide", "hud_tracker_main_longest")
def _tracker_main(ui):
    return _TrackerScene(real_game(ui, guide=_main_led())), None


@case("guide", "road_main_longest")
def _guide_main(ui):
    from client.scenes.guide import GuideScene
    s = GuideScene(real_game(ui, guide=_main_led()), tab="road")
    return s, AUTO


# -------- the other hubs of the maths
@case("placement", "intro")
def _placement(ui):
    from client.scenes.math_placement import PlacementScene
    subj = next(s for s in payload("/math/path")["subjects"] if s["id"] == "giai_tich")
    s = PlacementScene(real_game(ui), subj)
    s.on_enter()
    return s, AUTO


@case("dungeon", "gate")
def _dungeon(ui):
    from client.scenes.math_dungeon import MathDungeonScene
    s = MathDungeonScene(real_game(ui))
    s.on_enter()
    return s, AUTO


@case("td", "gate")
def _td(ui):
    from client.scenes.math_td import MathTdScene
    return MathTdScene(real_game(ui)), AUTO


@case("td", "gate_last_level")
def _td_last(ui):
    from client.scenes.math_td import MathTdScene
    s = MathTdScene(real_game(ui))
    if s.data and s.data.get("levels"):
        s.sel = _longest(s.data["levels"], "name_vi")["id"]
    return s, AUTO


@case("fortune", "gate")
def _fortune(ui):
    from client.scenes.math_fortune import MathFortuneScene
    return MathFortuneScene(real_game(ui)), AUTO


# -------- the code screens (Xạ Trường is the scored kind of the same screen)
def _code(ui, scored: bool, result: bool):
    import tempfile

    from client.tests import test_code_editor as CE
    from app.learning import math_problems
    bank = [p for p in math_problems.bank().values() if bool(p.scored) == scored]
    best = max(bank, key=lambda p: sum(len(s) for s in p.statement_vi) + len(p.input_vi) + len(p.output_vi))
    s = CE.code_scene(ui, Path(tempfile.mkdtemp()), problem=best.view())
    s.game = fake_game(ui)
    s.game.session = SimpleNamespace(path=Path(tempfile.mkdtemp()) / "session.json")
    if result:
        s.result = CE.failing_result(s.problem)
        s.outputs = ["1 2 3\n" * 4] * len(s.problem["samples"])
        s.show_detail = True
    return s, (6, 4, 468, 262)


case("code", "statement_longest")(lambda ui: _code(ui, False, False))
case("code", "failing_run_detail")(lambda ui: _code(ui, False, True))
case("xa_truong", "statement_longest")(lambda ui: _code(ui, True, False))


# -------- the character's screens
@case("linh_can", "main")
def _lc(ui):
    from client.scenes.linh_can import LinhCanScene
    return LinhCanScene(real_game(ui)), AUTO


@case("linh_can", "book")
def _lc_book(ui):
    from client.scenes.linh_can import LinhCanScene
    s = LinhCanScene(real_game(ui))
    s.tab = "book"
    return s, AUTO


def _ach_cases():
    try:
        cats = [c["id"] for c in payload("/achievements")["categories"]]
    except Exception:           # noqa: BLE001
        cats = []
    from client.scenes import achievements as A
    for cid in cats + [getattr(A, "TITLES", "titles")]:
        def build(ui, cid=cid):
            s = A.AchievementsScene(real_game(ui), tab=cid)
            return s, AUTO
        case("achievements", f"tab_{cid}")(build)


@case("cong_phap", "all_chieu")
def _cp(ui):
    from client.scenes.cong_phap import CongPhapScene
    d = payload("/math/skills")
    from client.scenes.world import WorldScene
    world = SimpleNamespace(mskills=d.get("skills") or [], mskill_loadout=d.get("loadout") or [])
    world.draw_mskill_icon = lambda *a: WorldScene.draw_mskill_icon(world, *a)     # the world's own drawing
    s = CongPhapScene(real_game(ui), world)
    s.look = (_longest(s.skills, "desc_vi") or {}).get("id", s.look)
    return s, CongPhapScene.PANEL


def _tabbed(screen, cls_path, tabs, attr="tab"):
    mod, cls = cls_path.rsplit(".", 1)
    for t in tabs:
        for end in (False, True):
            def build(ui, t=t, end=end):
                import importlib
                C = getattr(importlib.import_module(mod), cls)
                s = C(real_game(ui, inv=payload("/inventory"), pets=payload("/pets")))
                setattr(s, attr, t)
                if end:
                    for a in ("scroll", "first", "page"):
                        if isinstance(getattr(s, a, None), int):
                            setattr(s, a, 999)
                return s, AUTO
            case(screen, f"{t}{'_end' if end else ''}")(build)


_tabbed("bag", "client.scenes.bag.BagScene", ["items", "gear", "weapons"])
_tabbed("shop", "client.scenes.shop.ShopScene", ["buy", "gear", "sell"])


@case("pets", "list")
def _pets(ui):
    from client.scenes.pets import PetScene
    return PetScene(real_game(ui, pets=payload("/pets"))), AUTO


@case("pets", "book")
def _pet_book(ui):
    from client.scenes.pets import PetBookScene
    return PetBookScene(real_game(ui, pets=payload("/pets"))), AUTO


_guide_topics()
_ach_cases()

# Screens that have no scene to open: listed in the report instead of skipped silently.
NOT_COVERED = {
    "essay hall (Luận Đạo Đài)": "no scene in the client: essay grading by the API was dropped (2026-11-20), "
                                 "so there is nothing to open",
}


# ------------------------------------------------------------------ main
def frame(ui: UI, scene) -> list:
    ui.win.fill((0, 0, 0))                  # (a screenshot shows this case alone)
    ui.audit = []
    ui.begin([], 0.016)
    scene.draw_ui(ui)
    ui.end()
    rec, ui.audit = ui.audit, None
    return rec


def run(scales=(2, 3), only: set[str] | None = None, shots: Path | None = None, quiet: bool = False,
        cases=None) -> dict:
    """{(screen, case, scale): {"hard": [...], "allowed": [(Problem, why)], "soft": [...]}} plus
    "_errors": [(screen, case, scale, message)] for a case that could not be opened."""
    pygame.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((480, 270))
    fonts = Fonts()
    glyphs = Glyphs(fonts)
    out: dict = {"_errors": []}
    todo = [c for c in (cases or CASES) if not only or c[0] in only or f"{c[0]}/{c[1]}" in only]
    t0 = time.time()
    for scale in scales:
        ui = UI(Display(0, False, size=(480 * scale, 270 * scale)), fonts)
        for screen, name, build in todo:
            try:
                ui.inputs.clear()
                scene, panel = build(ui)
                frame(ui, scene)
                rec = frame(ui, scene)
            except Exception as e:                       # noqa: BLE001 - reported, never hidden
                out["_errors"].append((screen, name, scale, f"{type(e).__name__}: {e}"))
                continue
            if panel == AUTO:
                boxes = [r["rect"] for r in rec if r.get("kind") == "panel"]
                panel = max(boxes, key=lambda b: b[2] * b[3]) if boxes else None
            if panel is not None:                   # (ui.panel draws its title box 6 px above the panel)
                panel = (panel[0], panel[1] - 7, panel[2], panel[3] + 7)
            found = audit.problems(rec, panel=panel) + extra_problems(rec, glyphs)
            got = {"hard": [], "allowed": [], "soft": []}
            for p in found:
                why = allowed(screen, p)
                if why:
                    got["allowed"].append((p, why))
                elif p.kind in HARD:
                    got["hard"].append(p)
                else:
                    got["soft"].append(p)
            out[(screen, name, scale)] = got
            if shots is not None:
                shots.mkdir(parents=True, exist_ok=True)
                pygame.image.save(ui.win, str(shots / f"{screen}__{name}__x{scale}.png"))
        if not quiet:
            print(f"scale {scale}: {len(todo)} cases, {time.time() - t0:.1f} s", flush=True)
    return out


def counts(result: dict) -> dict:
    """screen -> {"cases": n, "hard": n, "allowed": n, kind -> n}."""
    per: dict = defaultdict(lambda: defaultdict(int))
    for key, got in result.items():
        if key == "_errors":
            continue
        screen = key[0]
        per[screen]["frames"] += 1
        per[screen]["hard"] += len(got["hard"])
        per[screen]["allowed"] += len(got["allowed"])
        for p in got["hard"]:
            per[screen][p.kind] += 1
    for screen, *_ in result["_errors"]:
        per[screen]["errors"] += 1
    return per


def write_report(result: dict, scales, path: Path = REPORT, before: dict | None = None, notes: str = "") -> None:
    per = counts(result)
    lines = ["# Screens audit", "",
             f"Written by `tools/audit_screens.py` (scales {', '.join(map(str, scales))}); checks of "
             "`client/ui/audit.py` plus glyph / ellipsis / label (see the tool's docstring).", ""]
    if notes:
        lines += [notes, ""]
    lines += ["## Hard problems per screen", "", "| screen | frames | hard now | " +
              ("hard before | " if before else "") + "meant cuts | kinds now |",
              "|---|---|---|" + ("---|" if before else "") + "---|---|"]
    for screen in sorted(set(per) | set(before or {})):
        c = per.get(screen, {})
        kinds = ", ".join(f"{k} {v}" for k, v in sorted(c.items()) if k not in ("frames", "hard", "allowed")) or "-"
        row = f"| {screen} | {c.get('frames', 0)} | {c.get('hard', 0)} | "
        if before:
            row += f"{before.get(screen, {}).get('hard', 0)} | "
        lines.append(row + f"{c.get('allowed', 0)} | {kinds} |")
    if result["_errors"]:
        lines += ["", "## Cases that could not be opened", ""]
        lines += [f"- {s}/{n} x{sc}: {m}" for s, n, sc, m in result["_errors"]]
    lines += ["", "## Hard problems left", ""]
    left = [(k, p) for k, got in result.items() if k != "_errors" for p in got["hard"]]
    if not left:
        lines.append("None.")
    for (screen, name, scale), p in left[:300]:
        lines.append(f"- {screen}/{name} x{scale}: {p.describe()}")
    lines += ["", "## Meant cuts (not hard)", ""]
    meant = defaultdict(set)
    for k, got in result.items():
        if k == "_errors":
            continue
        for p, why in got["allowed"]:
            meant[(k[0], why)].add(p.text.replace("\n", " ")[:60])
    if not meant:
        lines.append("None.")
    for (screen, why), texts in sorted(meant.items()):
        lines.append(f"- {screen}: {why} ({len(texts)} texts, e.g. {sorted(texts)[0]!r})")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scales", default="2,3")
    ap.add_argument("--only", default="", help="comma-separated screens or screen/case")
    ap.add_argument("--shots", default="", help="save a PNG of every frame into this folder")
    ap.add_argument("--no-report", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list:
        for s, n, _ in CASES:
            print(f"{s}/{n}")
        return 0
    scales = [int(s) for s in args.scales.split(",")]
    only = set(filter(None, args.only.split(","))) or None
    result = run(scales, only, Path(args.shots) if args.shots else None)
    for screen, c in sorted(counts(result).items()):
        kinds = ", ".join(f"{k} {v}" for k, v in sorted(c.items()) if k not in ("frames", "hard", "allowed"))
        print(f"{screen:12s} frames {c['frames']:3d}  hard {c['hard']:4d}  meant {c['allowed']:3d}  {kinds}")
    for s, n, sc, m in result["_errors"]:
        print(f"  could not open {s}/{n} x{sc}: {m}")
    if os.environ.get("AUDIT_VERBOSE"):
        for k, got in result.items():
            if k != "_errors":
                for p in got["hard"]:
                    print(f"  {k[0]}/{k[1]} x{k[2]}: {p.describe()}")
    if not args.no_report and not only:
        write_report(result, scales)
    hard = sum(len(g["hard"]) for k, g in result.items() if k != "_errors")
    return 1 if hard or result["_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
