"""Chỉ Đường: where should this player go? (docs/CHI_DUONG.md)

"Tu vi" for places is the player's place in Đạo Thụ (systems/math_tree_progress.py), never the
character's cultivation realm. The answer is a list of destinations, the recommended one first:

* **the rule** (`recommend`): for every land of a branch that this player may walk into, the stage
  of the node where they are learning in that branch (the frontier of its subject, R9; for the
  Lập Trình and Thực Chiến branches, which have no subject, their first open main node). The land
  whose branch has the **lowest** such stage comes first - the weakest branch is the one to train;
  ties go in the order ds, gt, xs, tr, lt, ud (the four math branches before the exercise lands).
  Lôi Kiếp Đài wins over everything when it is open and the player has reached the last stage of
  its realm (Luyện Khí tầng 9).
* **the place inside a land** (`fit_khu`): the khu (realtime/dia_do.py) whose [stage_min, stage_max]
  holds that stage; with no khu holding it, the deepest khu below it, else the shallowest one; a
  zone with no khu at all (today's small maps) is the land itself, walked to at its
  ``from_village`` spawn. A khu of band 0 (a safe place) is never a destination.
* a newcomer, with nothing done, learns tầng 1 of every branch: band 1 of the first land (ds).

The rest: one alternative per other open land (its own fitting khu), the locked lands with the
Vietnamese reason of their door, home (Động Phủ: the walk ends at its gate in the village) and the
village.

`learning_of` is the one place that decides "where is this player learning in each branch". A
later "next step" of the Lộ Trình can replace it without touching the rule.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

BRANCH_ORDER = ("ds", "gt", "xs", "tr", "lt", "ud")
HUB = "truc_lam_thon"
HOME = "abode"
BOSS_LAND = "loi_kiep_dai"
HOME_GATE_SPAWN = "from_abode"          # in front of the abode's gate in the village
ENTRY_SPAWN = "from_village"            # where a land is entered from the village
BAND_NAMES_VI = {0: "An Toàn", 1: "Ngoại Vi", 2: "Trung Vực", 3: "Thâm Xứ"}


# ------------------------------------------------------------------ the input of the rule
@dataclass(frozen=True)
class BranchPos:
    """Where the player is learning in one branch."""
    realm: str
    stage: int
    node_vi: str = ""


@dataclass(frozen=True)
class Learning:
    realm: str                     # the stage reached (math_tree_progress.TreeState.stage)
    stage: int
    realm_vi: str = ""
    last_stage: int = 9            # the last stage of that realm
    by_branch: dict = field(default_factory=dict)      # branch id -> BranchPos

    @property
    def working(self) -> int:
        """The stage being worked on: one above the stage reached, never above the last."""
        return min(self.stage + 1, self.last_stage)


def learning_of(st) -> Learning:
    """From a math_tree_progress.TreeState. The plug-in point for a later "next step" API."""
    from . import math_tree_progress as mtp
    t = st.tree
    raw = t.raw
    subjects = {b["id"]: b.get("subject") for b in raw.get("branches", [])}
    realm, stage = st.stage
    realm_vi = next((r["name_vi"] for r in raw.get("realms", []) if r["id"] == realm), realm)
    by: dict[str, BranchPos] = {}
    for b in BRANCH_ORDER:
        node = None
        if subjects.get(b):
            part = mtp.frontier_of(st, subjects[b])
            node = t.nodes.get(part.node_id) if part is not None and part.node_id else None
        else:                               # Lập Trình, Thực Chiến: their own main nodes
            mains = sorted((n for n in t.nodes.values() if n.main and n.branch == b), key=mtp.node_order)
            node = next((n for n in mains if st.status.get(n.id) == mtp.OPEN), None)
            if node is None:
                done = [n for n in mains if st.status.get(n.id) in (mtp.DONE, mtp.VACANT)]
                node = done[-1] if done else (mains[0] if mains else None)
        if node is not None and node.stage:
            by[b] = BranchPos(node.realm, int(node.stage), node.name_vi)
    return Learning(realm, int(stage), realm_vi, t.realm_stages.get(realm, 9), by)


# ------------------------------------------------------------------ the pure rule
def stage_in(pos: BranchPos | None, land_realm: str, realm_order: dict, last: int = 9) -> int:
    """The branch's learning stage as a stage of the land's realm (1 for a newcomer; beyond the
    land's realm counts as its last stage)."""
    if pos is None:
        return 1
    a, b = realm_order.get(pos.realm, 0), realm_order.get(land_realm, 0)
    if a > b:
        return last
    if a < b:
        return 1
    return max(1, pos.stage)


def fit_khu(khus, stage: int) -> dict | None:
    """The khu of a land that fits a learning stage (see the module docstring)."""
    cand = [k for k in khus if int(k.get("band") or 0) > 0 and not k.get("safe")]
    if not cand:
        return None
    inside = [k for k in cand if k["stage_min"] <= stage <= k["stage_max"]]
    if inside:
        return inside[0]
    below = [k for k in cand if k["stage_max"] < stage]
    if below:
        top = max(k["stage_max"] for k in below)
        return next(k for k in below if k["stage_max"] == top)
    low = min(k["stage_min"] for k in cand)
    return next(k for k in cand if k["stage_min"] == low)


def _range_vi(realm_vi: str, lo: int, hi: int) -> str:
    return f"{realm_vi} tầng {lo}" if lo == hi else f"{realm_vi} tầng {lo}-{hi}"


def _dest(kind: str, land: dict, stage: int, khus, spawn_of, realm_vi: str) -> dict:
    zone = land["zone"]
    k = fit_khu(khus, stage)
    if k is not None:
        x, y = k["anchor"]
        return {"kind": kind, "land": land["id"], "zone": zone, "khu": k["id"], "name_vi": k["name_vi"],
                "land_vi": land["name_vi"], "band": k["band"], "band_vi": BAND_NAMES_VI.get(k["band"], ""),
                "stage_min": k["stage_min"], "stage_max": k["stage_max"], "x": int(x), "y": int(y),
                "branch": land.get("branch"), "learning_stage": stage, "open": True,
                "fit_vi": "hợp " + _range_vi(realm_vi, k["stage_min"], k["stage_max"])}
    x, y = spawn_of(zone, ENTRY_SPAWN)
    return {"kind": kind, "land": land["id"], "zone": zone, "khu": None, "name_vi": land["name_vi"],
            "land_vi": land["name_vi"], "band": None, "band_vi": "", "stage_min": None, "stage_max": None,
            "x": int(x), "y": int(y), "branch": land.get("branch"), "learning_stage": stage, "open": True,
            "fit_vi": ""}


def _reason(d: dict, learn: Learning, branch_vi: dict, boss: bool) -> str:
    if boss:
        return (f"Con đã tới {learn.realm_vi} tầng {learn.stage}: Lôi Kiếp Đài đang chờ con độ kiếp.")
    pos = learn.by_branch.get(d.get("branch"))
    where = f"nhánh {branch_vi.get(d.get('branch'), '')}".strip()
    node = f"đang học {pos.node_vi} (tầng {d['learning_stage']})" if pos and pos.node_vi else \
        f"đang ở tầng {d['learning_stage']}"
    if d["khu"]:
        return f"Con {node} của {where}: {d['name_vi']} ở {d['land_vi']} {d['fit_vi']}."
    return f"Con {node} của {where}: quái ở {d['land_vi']} hỏi đúng nhánh ấy."


def recommend(learn: Learning, lands: list[dict], khu_of: Callable[[str], tuple], spawn_of: Callable,
              realm_order: dict, branch_vi: dict | None = None) -> dict:
    """The destinations for this player, pure: `lands` are rows of lands.view plus the land's
    `kind` and `realm` ({id, name_vi, branch, kind, realm, zone, built, open, reason_vi}),
    `khu_of(zone)` the khu of a zone (dia_do.khu_list), `spawn_of(zone, name)` a spawn point."""
    branch_vi = branch_vi or {}
    open_lands, locked = [], []
    for l in lands:
        if l.get("kind") == "hub" or not l.get("built") or not l.get("zone"):
            continue
        (open_lands if l.get("open") else locked).append(l)
    rank = {b: i for i, b in enumerate(BRANCH_ORDER)}
    dests = []
    for l in open_lands:
        stage = stage_in(learn.by_branch.get(l.get("branch")), l.get("realm") or learn.realm, realm_order,
                         learn.last_stage) if l.get("branch") else learn.working
        dests.append(_dest("land", l, stage, khu_of(l["zone"]), spawn_of, learn.realm_vi or ""))

    def boss_ready(d) -> bool:
        return d["land"] == BOSS_LAND and learn.stage >= learn.last_stage

    best = next((d for d in dests if boss_ready(d)), None)
    branched = [d for d in dests if d.get("branch") in rank]
    if best is None and branched:
        best = min(branched, key=lambda d: (d["learning_stage"], rank[d["branch"]]))
    if best is None and dests:
        best = dests[0]
    others = []
    for d in dests:
        d["reason_vi"] = _reason(d, learn, branch_vi, boss_ready(d))
        if d is best:
            d["kind"] = "recommended"
        else:
            others.append(d)
    others.sort(key=lambda d: rank.get(d.get("branch"), len(rank)))
    hub_x, hub_y = spawn_of(HUB, "spawn")
    gate_x, gate_y = spawn_of(HUB, HOME_GATE_SPAWN)
    return {
        "stage": {"realm": learn.realm, "realm_vi": learn.realm_vi, "stage": learn.stage, "working": learn.working},
        "recommended": best,
        "lands": others,
        "locked": [{"kind": "locked", "land": l["id"], "zone": l["zone"], "name_vi": l["name_vi"],
                    "branch": l.get("branch"), "open": False, "reason_vi": l.get("reason_vi") or ""}
                   for l in locked],
        "home": {"kind": "home", "land": None, "zone": HOME, "via": HUB, "khu": None, "name_vi": "Động Phủ",
                 "land_vi": "Trúc Lâm Thôn", "x": int(gate_x), "y": int(gate_y), "open": True,
                 "reason_vi": "Con đường về Động Phủ: tới cổng nhà mình ở Trúc Lâm Thôn, bước vào là về."},
        "village": {"kind": "village", "land": HUB, "zone": HUB, "khu": None, "name_vi": "Trúc Lâm Thôn",
                    "land_vi": "Trúc Lâm Thôn", "x": int(hub_x), "y": int(hub_y), "open": True,
                    "reason_vi": "Về giữa làng Trúc Lâm Thôn."},
    }


# ------------------------------------------------------------------ the world as it is
def land_rows(pos) -> list[dict]:
    """lands.view with the land's kind and realm, and the door decided as the world decides it
    (lands.refusal: no door at all while the lands are not wired)."""
    from ..realtime import lands
    out = []
    for v in lands.view(pos):
        l = lands.land(v["id"]) or {}
        why = lands.refusal(v["zone"], pos) if v["zone"] else v.get("reason_vi")
        out.append({**v, "kind": l.get("kind"), "realm": l.get("realm"),
                    "open": bool(v["zone"]) and why is None, "reason_vi": why})
    return out


def spawn_point(zone: str, name: str) -> tuple[float, float]:
    from ..realtime import maps
    from ..realtime.world import zone_defs
    z = zone_defs().get(zone) or {}
    if not z.get("map"):
        return 0.0, 0.0
    return maps.load(z["map"]).spawn(name)


async def destinations(db, user) -> dict:
    """GET /nav/destinations."""
    from ..learning import math_tree
    from ..realtime import dia_do, lands
    from . import math_tree_progress
    st = await math_tree_progress.state(db, user.id)
    learn = learning_of(st)
    rows = land_rows(lands.pos_of(st))
    branch_vi = {b["id"]: b["name_vi"] for b in math_tree.tree().raw.get("branches", [])}
    return recommend(learn, rows, dia_do.khu_list, spawn_point, st.tree.realm_order, branch_vi)
