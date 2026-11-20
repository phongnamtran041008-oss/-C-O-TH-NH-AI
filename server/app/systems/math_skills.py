"""Chiêu thức gắn câu hỏi (M9, kế hoạch 4.4): a chiêu is cast by answering one math question -
in a bí cảnh. Out in the wild (world_plan.json "combat": questions only when a monster hits
you) a chiêu is cast freely (`_cast_free`): the same unlock, qi, cooldown, range and formula,
no question, no fast-answer crit, it never breaks an elite's Mặc Thuẫn (only a Phản Đòn does),
and its combo is the run of Phản Đòn in a row (`p.mcombo`, kept by realtime/combat.py).
Everything below describes the question rule of a bí cảnh.

The chiêu live in data/math/skills.json. Pressing one (`{"t": "mskill"}` on the WebSocket)
does not hit anything yet: it asks the caster one question of the chiêu's type, through the
same quiz service and the same `p.question` slot as Vấn Đạo, so while it is open the caster
has Hộ Thể and cannot open a second one. The qi and the cooldown are spent when the cast is
accepted - before the answer - because the question *is* the chiêu being channelled.

  * Right -> the chiêu lands: damage to the target, damage + slow to everything around it,
    or a ward on the caster's group. A landed chiêu breaks the target's Mặc Thuẫn like any
    right answer (and a bí cảnh boss's group shield counts it as this player's answer, no
    more). Right casts in a row build a combo; a fast answer is a crit like Ngộ Đạo.
  * Wrong or out of time -> "chiêu hụt": nothing happens, the combo is back to 0, and -
    unlike a missed Vấn Đạo - there is no Mặc Kích. Missing a chiêu you chose to cast costs
    the qi and the cooldown, never health. The fight then goes on as before: the monster,
    still shielded, asks its own question a few seconds later.

Which question: a type of the chiêu's `qtypes`, about the target's own micro-skill when the
target is a quái lỗi sai (else another micro-skill of its floor that the player has open),
otherwise about the player's own part of Đạo Thụ (the frontier, math_tree_progress). The tier
is the player's own for that micro-skill (math_combat.tier_for) and never above it. The answer
goes to `math_answers` with no run, like M7, so the learning path counts it.

Unlocking reads only the learning path, never the cultivation realm: a chiêu's
`unlock.floor` n opens at Luyện Khí tầng n of Đạo Thụ, read against the stage the player is
working on (math_tree_progress.working_stage; one above the stage reached).
"""
from __future__ import annotations

import datetime as dt
import json
import logging
import math
import random
from functools import lru_cache
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import balance
from .. import db as dbm
from ..config import DATA_DIR
from ..learning import math_items, math_path, math_tree, quiz
from ..models import MathAnswer, QuizSession, User
from . import linh_can, math_combat, math_practice, math_tree_progress

if TYPE_CHECKING:
    from ..realtime.zone import ChannelZone, Player

log = logging.getLogger("toan_tu_tien.math_skills")

CONTEXT = "math_skill"
SKILLS_FILE = DATA_DIR / "math" / "skills.json"

KINDS = ("Đòn thường", "Kiếm quyết", "Pháp thuật", "Trận pháp", "Tuyệt kỹ")
ELEMENTS = ("kim", "moc", "thuy", "hoa", "tho", "loi")
# the extra numbers each effect needs, each with its range lo < value <= hi
EFFECT_KEYS = {
    "damage": {},
    "area": {"radius": (0, 1000), "slow": (0, 0.95), "duration": (0, 120)},
    "ward": {"radius": (0, 1000), "duration": (0, 120), "reduce": (0, 0.95), "heal_pct": (0, 100)},
    # Chiêu Thức II: the effects of the eleven chiêu earned on Đạo Thụ (skills.json _comment)
    "line": {"width": (0, 200), "pierce": (0, 20)},
    "chain": {"hops": (0, 10), "hop_range": (0, 400), "falloff": (0, 1)},
    "cone": {"angle": (0, 180)},
    "root": {"radius": (0, 1000), "duration": (0, 30)},
    "shield": {"duration": (0, 120), "reduce": (0, 0.95)},
    "heal": {"radius": (0, 1000), "heal_pct": (0, 100)},
    "domain": {"radius": (0, 1000), "every": (0.1, 5), "duration": (0, 30)},
}
INT_KEYS = ("pierce", "hops")                       # whole numbers
TARGETLESS = ("ward", "shield", "heal", "domain")   # no target, range 0
NO_POWER = ("ward", "shield", "heal")              # power 0: they deal no damage
EFFECT_PARAMS = sorted({k for v in EFFECT_KEYS.values() for k in v})
BURN_KEYS = {"power": (0, 5), "every": (0.1, 5), "duration": (0, 20)}    # line only: the strip keeps burning
LOADOUT_SLOTS = 6
_REQUIRED = ("name_vi", "kind_vi", "element", "qtypes", "min_tier", "qi", "cooldown", "range", "effect",
             "power", "anim", "fx", "icon", "unlock", "desc_vi")
_OPTIONAL = {"reviewed", "icon_variant", "burn"} | set(EFFECT_PARAMS)
UNLOCK_KEYS = {"floor", "nodes", "share"}
NO_BRANCHES = ("ml", "dl")          # branches with nothing in the game yet: no chiêu may need them

REFUSALS_VI = {
    "unknown": "Không có chiêu này.",
    "cannot": "Lúc này không thi triển chiêu được.",
    "answering": "Con đang trả lời một câu khác.",
    "cooldown": "Chiêu này chưa hồi xong.",
    "no_qi": "Không đủ linh khí.",
    "no_target": "Hãy chọn một con quái làm mục tiêu.",
    "too_far": "Mục tiêu ở quá xa.",
    "tier_low": "Bậc câu hỏi con đã mở chưa đủ cho chiêu này. Luyện thêm ở Động Phủ nhé!",
    "no_question": "Chưa có câu hỏi loại này ở tầng của con.",
    "flying": "Đang ngự kiếm trên không: hạ kiếm xuống rồi hãy thi triển.",
    "not_slotted": "Chiêu này chưa được xếp vào thanh Công Pháp.",
}
LOADOUT_ERRORS_VI = {
    "bad_slots": "Thanh Công Pháp có đúng sáu ô.",
    "unknown": "Không có chiêu này.",
    "twice": "Một chiêu chỉ xếp được vào một ô.",
    "locked": "Chưa lĩnh ngộ chiêu này nên chưa xếp được.",
}


# ------------------------------------------------------------------ the data
def _read() -> dict:
    return json.loads(SKILLS_FILE.read_text("utf-8"))


@lru_cache(maxsize=1)
def data() -> dict:
    """skills.json without its comment. It is checked by validate() in the tests and in
    tools/check_all.py, so the game itself trusts it."""
    return {k: v for k, v in _read().items() if not k.startswith("_")}


def skills() -> dict[str, dict]:
    return data()["skills"]


def combo_cfg() -> dict:
    return data()["combo"]


def _number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def validate(raw: dict | None = None, config: dict | None = None) -> list[str]:
    """One readable line per problem in skills.json; empty when it is sound."""
    raw = _read() if raw is None else raw
    qtypes = math_path.question_types(config)
    out: list[str] = []
    combo = raw.get("combo")
    if not isinstance(combo, dict) or not _number(combo.get("per_streak")) or not _number(combo.get("max_mult")):
        out.append("combo must be {per_streak: number, max_mult: number}")
    elif combo["per_streak"] < 0 or combo["max_mult"] < 1:
        out.append("combo: per_streak must be >= 0 and max_mult >= 1")
    table = raw.get("skills")
    if not isinstance(table, dict) or not table:
        return out + ["skills must be a non-empty object"]
    for sid, s in table.items():
        here = f"skill {sid}"
        if not isinstance(s, dict):
            out.append(f"{here}: must be an object")
            continue
        missing = [k for k in _REQUIRED if k not in s]
        if missing:
            out.append(f"{here}: missing {', '.join(missing)}")
            continue
        extra = sorted(set(s) - set(_REQUIRED) - _OPTIONAL)
        if extra:
            out.append(f"{here}: unknown keys {', '.join(extra)}")
        variant = s.get("icon_variant", 0)
        if not isinstance(variant, int) or isinstance(variant, bool) or variant < 0:
            out.append(f"{here}: icon_variant must be a whole number >= 0")
        for key in ("name_vi", "desc_vi", "anim", "fx", "icon"):
            if not isinstance(s[key], str) or not s[key].strip():
                out.append(f"{here}: {key} must be a non-empty string")
        if s["kind_vi"] not in KINDS:
            out.append(f"{here}: kind_vi must be one of {', '.join(KINDS)}")
        if s["element"] not in ELEMENTS:
            out.append(f"{here}: element must be one of {', '.join(ELEMENTS)}")
        tier = s["min_tier"]
        if not isinstance(tier, int) or isinstance(tier, bool) or tier not in math_path.TIERS:
            out.append(f"{here}: min_tier must be a tier 1..{math_path.TOP_TIER}")
            tier = None
        if not isinstance(s["qtypes"], list) or not s["qtypes"]:
            out.append(f"{here}: qtypes must be a non-empty list")
        else:
            for q in s["qtypes"]:
                if q not in qtypes:
                    out.append(f"{here}: {q!r} is not a question type of balance/math.json")
                elif tier is not None and all(lim is None for lim in qtypes[q]["time_limit"][tier - 1:]):
                    out.append(f"{here}: a {q} question exists at no tier from {tier} up")
        for key in ("qi", "cooldown", "range", "power"):
            if not _number(s[key]) or s[key] < 0:
                out.append(f"{here}: {key} must be a number >= 0")
        if _number(s["cooldown"]) and s["cooldown"] <= 0:
            out.append(f"{here}: cooldown must be > 0")
        effect = s["effect"]
        if effect not in EFFECT_KEYS:
            out.append(f"{here}: effect must be one of {', '.join(EFFECT_KEYS)}")
        else:
            if effect not in NO_POWER and _number(s["power"]) and s["power"] <= 0:
                out.append(f"{here}: a {effect} chiêu needs power > 0")
            if effect in NO_POWER and _number(s["power"]) and s["power"] != 0:
                out.append(f"{here}: a {effect} chiêu deals no damage: power must be 0")
            if effect not in TARGETLESS and _number(s["range"]) and s["range"] <= 0:
                out.append(f"{here}: a {effect} chiêu needs range > 0")
            for key, (lo, hi) in EFFECT_KEYS[effect].items():
                v = s.get(key)
                if not _number(v) or not (lo < v <= hi):
                    out.append(f"{here}: a {effect} chiêu needs {key} > {lo} and <= {hi}")
                elif key in INT_KEYS and not isinstance(v, int):
                    out.append(f"{here}: {key} must be a whole number")
            stray = sorted(k for k in EFFECT_PARAMS if k in s and k not in EFFECT_KEYS[effect])
            if stray:
                out.append(f"{here}: {', '.join(stray)} mean nothing for a {effect} chiêu")
            if "burn" in s:
                burn = s["burn"]
                if effect != "line":
                    out.append(f"{here}: burn means nothing for a {effect} chiêu")
                elif not isinstance(burn, dict) or set(burn) != set(BURN_KEYS):
                    out.append(f"{here}: burn must be {{power, every, duration}}")
                else:
                    for key, (lo, hi) in BURN_KEYS.items():
                        if not _number(burn[key]) or not (lo < burn[key] <= hi):
                            out.append(f"{here}: burn.{key} must be > {lo} and <= {hi}")
        out += unlock_problems(here, s["unlock"])
        if s.get("reviewed", False) not in (True, False):
            out.append(f"{here}: reviewed must be true or false")
    rr = raw.get("root_rank_mult")
    if rr is not None and (not isinstance(rr, dict) or set(rr) != {"normal", "elite", "boss"}
                           or not all(_number(v) and 0 < v <= 1 for v in rr.values())):
        out.append("root_rank_mult must be {normal, elite, boss} each > 0 and <= 1")
    if any(isinstance(s, dict) and s.get("effect") == "root" for s in table.values()) and rr is None:
        out.append("a root chiêu needs root_rank_mult")
    return out


def unlock_problems(here: str, unlock, t: "math_tree.Tree | None" = None) -> list[str]:
    """What is wrong with one chiêu's `unlock`: a floor of Luyện Khí, and optionally Đạo Thụ
    nodes and a share of a branch - each of which a player can really reach today (a node with
    content `co`, in Luyện Khí, of a branch that exists in the game, whose every ancestor is in
    Luyện Khí or before; a branch with at least one such node)."""
    out: list[str] = []
    floor = unlock.get("floor") if isinstance(unlock, dict) else None
    if (not isinstance(unlock, dict) or "floor" not in unlock or set(unlock) - UNLOCK_KEYS
            or not isinstance(floor, int) or isinstance(floor, bool) or floor < 1):
        return [f"{here}: unlock must be {{\"floor\": n}} with n >= 1 (and optionally nodes, share)"]
    t = t or math_tree.tree()
    order = t.realm_order.get(UNLOCK_REALM)
    if order is None:
        return [f"{here}: the tree has no realm {UNLOCK_REALM}"]
    if floor > t.realm_stages[UNLOCK_REALM]:
        out.append(f"{here}: unlock floor {floor} is above Luyện Khí's last stage")
    nodes = unlock.get("nodes", [])
    if not isinstance(nodes, list) or (("nodes" in unlock) and not nodes) or \
            not all(isinstance(n, str) for n in nodes):
        out.append(f"{here}: unlock.nodes must be a non-empty list of Đạo Thụ node ids")
        nodes = []
    if len(set(nodes)) != len(nodes):
        out.append(f"{here}: unlock.nodes names a node twice")
    for nid in nodes:
        node = t.nodes.get(nid)
        if node is None:
            out.append(f"{here}: unlock node {nid!r} is not in Đạo Thụ")
            continue
        if node.realm != UNLOCK_REALM:
            out.append(f"{here}: unlock node {nid} is not in Luyện Khí")
        if node.content != "co":
            out.append(f"{here}: unlock node {nid} has no content yet ({node.content}), so nobody can finish it")
        if node.branch in NO_BRANCHES:
            out.append(f"{here}: unlock node {nid} is on branch {node.branch}, which the game does not have yet")
        if node.stage is not None and node.stage > floor:
            out.append(f"{here}: unlock floor {floor} is below the stage {node.stage} of its node {nid}")
        late = [a for a in t.ancestors(nid) if t.realm_order.get(t.nodes[a].realm, 99) > order]
        if late:
            out.append(f"{here}: unlock node {nid} needs nodes after Luyện Khí: {', '.join(sorted(late))}")
    share = unlock.get("share")
    if share is not None:
        branches = {b["id"] for b in t.raw.get("branches", [])}
        if not isinstance(share, dict) or set(share) != {"branch", "at_least"}:
            out.append(f"{here}: unlock.share must be {{branch, at_least}}")
        elif share["branch"] not in branches or share["branch"] in NO_BRANCHES:
            out.append(f"{here}: unlock.share names a branch the game does not have: {share['branch']!r}")
        elif not _number(share["at_least"]) or not 0 < share["at_least"] <= 1:
            out.append(f"{here}: unlock.share.at_least must be > 0 and <= 1")
        elif not any(n.branch == share["branch"] and n.content == "co" for n in t.main_nodes(UNLOCK_REALM)):
            out.append(f"{here}: branch {share['branch']} has nothing to learn in Luyện Khí yet")
    return out


def castable_floors(sk: dict, allow_unreviewed: bool = True) -> list[tuple[str, int]]:
    """(subject, floor) pairs at or above the chiêu's unlock floor where some template of one
    of its question types can really be asked at a tier the chiêu accepts. Empty means the
    chiêu cannot be cast by anyone today (tools/check_all.py reads this)."""
    out = []
    qtypes = set(sk["qtypes"]) & set(math_items.PLAYABLE_TYPES)
    for subject in math_path.subjects():
        for floor in subject.main_floors:
            if floor.number < sk["unlock"]["floor"]:
                continue
            templates = math_items.floor_templates(subject.id, floor.number, allow_unreviewed)
            if any(t.qtype in qtypes and t.tier >= sk["min_tier"] for t in templates):
                out.append((subject.id, floor.number))
    return out


# ------------------------------------------------------------------ unlocking
UNLOCK_REALM = "luyen_khi"      # a chiêu's unlock "floor" n is Luyện Khí tầng n of Đạo Thụ (R12)


async def working_position(db: AsyncSession, user_id: int) -> tuple[str, int]:
    """(realm, stage) the player is working on in Đạo Thụ (math_tree_progress.working_stage)."""
    return await math_tree_progress.working_position(db, user_id)


def branch_share(st: "math_tree_progress.TreeState", branch: str) -> tuple[int, int]:
    """(done, total) main Luyện Khí nodes of a branch that have anything to learn (a vacant
    node, "Đang biên soạn", is in neither number)."""
    nodes = [n for n in st.tree.main_nodes(UNLOCK_REALM)
             if n.branch == branch and st.status.get(n.id) != math_tree_progress.VACANT]
    return sum(1 for n in nodes if st.status.get(n.id) == math_tree_progress.DONE), len(nodes)


def missing_parts(sk: dict, where: tuple[str, int], st: "math_tree_progress.TreeState | None" = None) -> dict:
    """What this player still lacks for a chiêu: {floor: n|None, nodes: [ids], share: {...}|None}.
    Every part empty/None means it is open. `st` is needed only when the unlock names nodes or a
    share (the old six name only a floor)."""
    u = sk["unlock"]
    t = math_tree.tree()
    out: dict = {"floor": None, "nodes": [], "share": None}
    if not t.reaches(UNLOCK_REALM, u["floor"], where):
        out["floor"] = u["floor"]
    if st is not None:
        done = st.done
        out["nodes"] = [n for n in u.get("nodes", []) if n not in done]
        share = u.get("share")
        if share:
            have, total = branch_share(st, share["branch"])
            if total and have < share["at_least"] * total - 1e-9:
                out["share"] = {"branch": share["branch"], "at_least": share["at_least"], "done": have, "total": total}
    elif u.get("nodes") or u.get("share"):
        out["nodes"] = list(u.get("nodes", []))
    return out


def _branch_name(branch: str) -> str:
    return next((b["name_vi"] for b in math_tree.tree().raw.get("branches", []) if b["id"] == branch), branch)


def locked_text(miss: dict, where: tuple[str, int]) -> str | None:
    """The sentence the hotbar and the Công Pháp screen show for what is missing."""
    t = math_tree.tree()
    bits = []
    if miss["nodes"]:
        bits.append("Còn thiếu nút: " + ", ".join(t.nodes[n].name_vi for n in miss["nodes"]) + ".")
    if miss["share"]:
        sh = miss["share"]
        bits.append(f"Còn thiếu: học xong {round(sh['at_least'] * 100)}% nhánh {_branch_name(sh['branch'])} "
                    f"(con mới xong {sh['done']}/{sh['total']} nút).")
    if miss["floor"] is not None:
        bits.append(f"Mở khi tu tới Luyện Khí tầng {miss['floor']} trên Đạo Thụ (con đang ở tầng {where[1]}).")
    return " ".join(bits) or None


def locked_reason(sk: dict, where: tuple[str, int], st: "math_tree_progress.TreeState | None" = None) -> str | None:
    """None when the chiêu is open for this player, else why not (the working position (realm,
    stage) for the floor - a player past Luyện Khí has every stage behind them - and the tree
    state for the nodes and the share)."""
    return locked_text(missing_parts(sk, where, st), where)


def unlocked_ids(where: tuple[str, int], st) -> list[str]:
    return [sid for sid, s in skills().items() if locked_reason(s, where, st) is None]


def default_loadout() -> list[str | None]:
    ids = list(skills())[:LOADOUT_SLOTS]
    return ids + [None] * (LOADOUT_SLOTS - len(ids))


def loadout_of(hotbar: dict | None) -> list[str | None]:
    """The six slots of a Character.hotbar (default: the first six chiêu of the data, so an old
    player keeps the hotbar they had). A chiêu that left the data is dropped from its slot."""
    slots = (hotbar or {}).get("chieu")
    if not isinstance(slots, list) or len(slots) != LOADOUT_SLOTS:
        return default_loadout()
    known = skills()
    return [s if isinstance(s, str) and s in known else None for s in slots]


def check_loadout(slots, open_ids) -> str | None:
    """None when `slots` may be saved, else a code of LOADOUT_ERRORS_VI."""
    if not isinstance(slots, list) or len(slots) != LOADOUT_SLOTS:
        return "bad_slots"
    ids = [s for s in slots if s is not None]
    if any(not isinstance(s, str) or s not in skills() for s in ids):
        return "unknown"
    if len(set(ids)) != len(ids):
        return "twice"
    if any(s not in open_ids for s in ids):
        return "locked"
    return None


class LoadoutError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.status, self.code, self.message_vi = 400, code, LOADOUT_ERRORS_VI[code]


def _slot_new(slots: list, sid: str, open_ids: set) -> list:
    """A chiêu just learned goes into the first empty slot, else the first slot holding one the
    player has not learned yet; with six learned ones in place it waits in the Công Pháp list."""
    out = list(slots)
    if sid in out:
        return out
    for i, s in enumerate(out):
        if s is None:
            out[i] = sid
            return out
    for i, s in enumerate(out):
        if s not in open_ids:
            out[i] = sid
            return out
    return out


async def _character(db: AsyncSession, uid: int):
    from ..models import Character
    return await db.get(Character, uid)


async def view(db: AsyncSession, user: User) -> dict:
    """GET /math/skills: every chiêu in data order, and whether this player has it.
    `open_floor` is the working stage of Đạo Thụ (the number a chiêu's unlock is read against).
    `loadout` is the six slots of the Công Pháp bar. `new` names the chiêu learned since the last
    look (the client announces them once): the first look of an old save only remembers what is
    open, silently."""
    st = await math_tree_progress.state(db, user.id)
    where = math_tree_progress.working_position_of(st)
    types = math_path.question_types()
    out = []
    open_ids: list[str] = []
    t = math_tree.tree()
    for sid, s in skills().items():
        miss = missing_parts(s, where, st)
        reason = locked_text(miss, where)
        if reason is None:
            open_ids.append(sid)
        u = s["unlock"]
        need = {"floor": u["floor"],
                "nodes": [{"id": n, "name_vi": t.nodes[n].name_vi, "branch": t.nodes[n].branch,
                           "stage": t.nodes[n].stage, "done": n not in miss["nodes"]} for n in u.get("nodes", [])]}
        if u.get("share"):
            have, total = branch_share(st, u["share"]["branch"])
            need["share"] = {**u["share"], "name_vi": _branch_name(u["share"]["branch"]), "done": have, "total": total}
        row = {"id": sid, **{k: s[k] for k in ("name_vi", "kind_vi", "element", "min_tier", "qi", "cooldown",
                                                 "range", "effect", "power", "anim", "fx", "icon",
                                                 "desc_vi")},
               "icon_variant": int(s.get("icon_variant", 0)),
               "qtypes": list(s["qtypes"]),
               "qtype_vi": ", ".join(types[q]["name_vi"] for q in s["qtypes"]),
               "unlock": need, "unlocked": reason is None, "locked_vi": reason,
               "missing_nodes": list(miss["nodes"])}
        row.update({k: s[k] for k in EFFECT_KEYS[s["effect"]]})
        if "burn" in s:
            row["burn"] = dict(s["burn"])
        out.append(row)
    loadout, new = default_loadout(), []
    ch = await _character(db, user.id)
    if ch is not None:
        hb = dict(ch.hotbar or {})
        loadout = loadout_of(hb)
        known = hb.get("known")
        if not isinstance(known, list):            # an old save: remember silently
            hb["known"] = list(open_ids)
            ch.hotbar = hb
        else:
            fresh = [sid for sid in open_ids if sid not in known]
            if fresh:
                for sid in fresh:
                    loadout = _slot_new(loadout, sid, set(open_ids))
                hb["known"] = list(dict.fromkeys(known + fresh))
                hb["chieu"] = loadout
                ch.hotbar = hb
                new = [{"id": sid, "name_vi": skills()[sid]["name_vi"]} for sid in fresh]
                from . import achievements
                await achievements.on_event(db, user.id, "chieu_unlock", count=len(open_ids))
    return {"combo": dict(combo_cfg()), "open_floor": where[1], "stage": {"realm": where[0], "stage": where[1]},
            "skills": out, "loadout": loadout, "slots": LOADOUT_SLOTS, "new": new}


async def save_loadout(db: AsyncSession, user: User, slots) -> dict:
    """POST /math/skills/loadout: the six slots of the Công Pháp bar (a chiêu id or null each),
    only chiêu this player has learned, each at most once. Returns the view."""
    st = await math_tree_progress.state(db, user.id)
    where = math_tree_progress.working_position_of(st)
    code = check_loadout(slots, set(unlocked_ids(where, st)))
    if code is not None:
        raise LoadoutError(code)
    ch = await _character(db, user.id)
    if ch is None:
        raise LoadoutError("bad_slots")
    hb = dict(ch.hotbar or {})
    hb["chieu"] = list(slots)
    ch.hotbar = hb
    await db.flush()
    return await view(db, user)


async def cast_check(db: AsyncSession, uid: int, k: str) -> tuple[str | None, str | None]:
    """(refusal code, message) for casting `k` now as far as the database says (the unlock on
    Đạo Thụ, then the Công Pháp loadout), or (None, None)."""
    st = await math_tree_progress.state(db, uid)
    where = math_tree_progress.working_position_of(st)
    reason = locked_reason(skills()[k], where, st)
    if reason is not None:
        return "locked", reason
    ch = await _character(db, uid)
    if ch is not None and k not in loadout_of(ch.hotbar):
        return "not_slotted", None
    return None, None


# ------------------------------------------------------------------ the formula
def combo_mult(streak_before: int, combo: dict | None = None) -> float:
    """x1 for the first right cast, +per_streak for each right cast before it, capped."""
    c = combo or combo_cfg()
    return min(float(c["max_mult"]), 1.0 + float(c["per_streak"]) * max(0, streak_before))


def is_fast(answer_ms: int | None, limit: float) -> bool:
    """The same rule as Ngộ Đạo: answered within fast_answer_fraction of the time limit."""
    c = balance.load("combat")
    return answer_ms is not None and answer_ms <= c["fast_answer_fraction"] * limit * 1000


def damage(base: float, sk: dict, streak_before: int, fast: bool, p=None) -> float:
    """base_damage x power x combo x fast-answer crit (skills.json _comment), x the caster's
    linh căn bonus for the chiêu's element (chieu_<element>) when the caster is given."""
    crit = float(balance.load("combat")["fast_answer_crit_mult"]) if fast else 1.0
    elem = linh_can.chieu_mult(p, sk.get("element")) if p is not None else 1.0
    return base * float(sk["power"]) * combo_mult(streak_before) * crit * elem


def qi_cost(p, sk: dict) -> float:
    """The linh lực of a cast: the chiêu's own, less the linh căn's qi_cost."""
    return float(sk["qi"]) * (1 - linh_can.fx(p, "qi_cost"))


def cooldown(p, sk: dict) -> float:
    """The cooldown of a cast: the chiêu's own, less the linh căn's chieu_cd."""
    return float(sk["cooldown"]) * (1 - linh_can.fx(p, "chieu_cd"))


# ------------------------------------------------------------------ which question
async def _recent_fingerprints(db: AsyncSession, user_id: int, config: dict) -> dict[str, int]:
    rows = (await db.execute(select(MathAnswer.fingerprint).where(MathAnswer.user_id == user_id)
                             .order_by(MathAnswer.id.desc())
                             .limit(config["anti_repeat_window"]))).scalars().all()
    return {f: n for n, f in enumerate(reversed(list(rows)))}


async def _groups(db: AsyncSession, user_id: int, info: dict | None,
                  rng: random.Random) -> list[tuple[str, int, list[str]]]:
    """(subject, floor, micro-skills) to try in order of preference: a quái lỗi sai's own
    micro-skill, then the others of its floor that the player has open (R6); otherwise the
    player's own part of Đạo Thụ (the frontier of the first subject with questions, R9)."""
    if math_combat.is_mistake_monster(info):
        subject, floor = info["subject"], int(info["floor"])
        allowed = await math_tree_progress.allowed_skills(db, user_id)
        others = [k.id for k in math_path.subject(subject).floor(floor).skills
                  if k.id != info["skill"] and k.id in allowed]
        rng.shuffle(others)
        return [(subject, floor, [info["skill"]]), (subject, floor, others)]
    from . import math_ask
    part = await math_ask.own_part(db, user_id)
    if part is None:
        return []
    ids = list(part.skills)
    rng.shuffle(ids)
    return [(part.subject_id, part.floor, ids)]


async def question_for(db: AsyncSession, user: User, sk: dict, info: dict | None,
                       rng: random.Random | None = None) -> tuple[math_items.MathQuestion | None, str | None]:
    """The question that casts this chiêu, or (None, refusal code). The type is one of the
    chiêu's qtypes; the tier is the player's own for the micro-skill, else the nearest lower
    tier with a template, never below min_tier ("tier_low" when only that is missing)."""
    rng = rng or random.Random()
    config = math_path.cfg()
    qtypes = set(sk["qtypes"]) & set(math_items.PLAYABLE_TYPES)
    min_tier = int(sk["min_tier"])
    too_low = False
    seen_at = None
    for subject_id, floor, skill_ids in await _groups(db, user.id, info, rng):
        templates = [t for t in math_practice._templates(subject_id, floor) if t.qtype in qtypes]
        for skill_id in skill_ids:
            mine = [t for t in templates if t.skill == skill_id]
            if not mine:
                continue
            tier = await math_combat.tier_for(db, user.id, skill_id, floor, config)
            usable = sorted({t.tier for t in mine if min_tier <= t.tier <= tier})
            if not usable:
                too_low = True
                continue
            if seen_at is None:
                seen_at = await _recent_fingerprints(db, user.id, config)
            item = math_practice._pick([t for t in mine if t.tier == usable[-1]], seen_at, rng)
            if item is None:
                continue
            question = math_items.to_question(item, rng, config)
            question.meta["doc"] = math_practice.doc_link(item.skill)
            if math_combat.is_mistake_monster(info):
                question.meta["mistake_vi"] = info.get("mistake_vi", "")
                question.meta["monster_vi"] = info.get("name_vi", "")
            question.meta["cast_vi"] = sk["name_vi"]
            return question, None
    return None, ("tier_low" if too_low else "no_question")


# ------------------------------------------------------------------ casting (in memory + one task)
def _world():
    from ..realtime.world import world
    return world


def _target_code(p: "Player", sk: dict, eid: str | None):
    """(monster or None, refusal code or None) for this chiêu's target."""
    if sk["effect"] in TARGETLESS:
        return None, None
    m = p.channel.monster(eid) if eid else None
    if m is None or not m.alive:
        return None, "no_target"
    from ..realtime import combat
    if combat.dist(p.x, p.y, m.x, m.y) > sk["range"]:
        return None, "too_far"
    return m, None


def _ready_code(p: "Player", k: str, eid: str | None, now: float) -> str | None:
    """Everything that can be checked in memory, in the order the player should hear it."""
    sk = skills()[k]
    if now < p.mskill_ready.get(k, 0.0):
        return "cooldown"
    if p.qi < qi_cost(p, sk):
        return "no_qi"
    return _target_code(p, sk, eid)[1]


def refuse(p: "Player", k: str, code: str, message_vi: str | None = None) -> None:
    if p.session is not None:
        p.session.send({"t": "mcast", "k": k, "ok": False, "code": code,
                        "message_vi": message_vi or REFUSALS_VI.get(code, REFUSALS_VI["cannot"])})


def request(p: "Player", k: str, eid: str | None, now: float) -> str | None:
    """The `mskill` message. Returns a refusal code at once, or None when the question is
    being written in the background (which may still refuse: locked, cooldown, no_qi, ...
    tier_low, no_question). Nothing is spent until the question exists."""
    if k not in skills():
        return "unknown"
    if p.channel is None or p.dead or p.ghost or p.session is None:
        return "cannot"
    if p.question is not None or p.q_pending or p.protected(now):
        return "answering"
    if getattr(p, "fly", 0):          # ngự kiếm: no chiêu from up on the sword
        return "flying"
    from ..realtime import combat
    if combat.on_hit_rule(p.channel):     # the wild: a chiêu is cast freely, no question
        # (cooldown, qi and target are checked after the unlock, so a locked chiêu always says so)
        if k in p.free_casting:
            return "cooldown"
        p.free_casting.add(k)
        _world().spawn(_cast_free(p, p.channel, k, eid))
        return None
    p.q_pending = True
    _world().spawn(_create(p, p.channel, k, eid))
    return None


async def _cast_free(p: "Player", ch: "ChannelZone", k: str, eid: str | None) -> None:
    """The open-world rule (world_plan.json "combat"): the chiêu lands at once. Only its unlock
    needs the database (the learning path); qi, cooldown and target are checked again after.
    The damage multiplier is the combo of Phản Đòn in a row (p.mcombo), no fast-answer crit, and
    a chiêu never breaks an elite's Mặc Thuẫn here - only a Phản Đòn does."""
    w = _world()
    sk = skills()[k]
    try:
        async with dbm.SessionLocal() as db:
            code, reason = await cast_check(db, p.user_id, k)
    except Exception:
        log.exception("could not check a chiêu's unlock")
        p.free_casting.discard(k)
        refuse(p, k, "cannot")
        return
    p.free_casting.discard(k)
    if code is not None:
        refuse(p, k, code, reason)
        return
    now = w.mono()
    code = None
    if p.dead or p.ghost or p.channel is not ch or p.session is None or w.players.get(p.user_id) is not p:
        code = "cannot"
    elif p.question is not None or p.q_pending or p.protected(now):
        code = "answering"
    else:
        code = _ready_code(p, k, eid, now)
    if code is not None:
        refuse(p, k, code)
        return
    from ..realtime import combat
    m = _target_code(p, sk, eid)[0]
    p.qi -= qi_cost(p, sk)
    p.mskill_ready[k] = now + cooldown(p, sk)
    if m is not None:
        dx, dy = m.x - p.x, m.y - p.y
        p.facing = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")
        combat.engage(ch, m, p, now)
    p.last_combat = now
    ev = _event(p, k, sk, m)
    out = _land(p, ch, k, sk, m, ev, now, streak=p.mcombo, fast=False, combo=p.mcombo, may_break=False)
    p.session.send({"t": "mcast", "k": k, "ok": True, "ready_in": cooldown(p, sk), "qi": round(p.qi, 1),
                    "free": True, "result": out})


async def _create(p: "Player", ch: "ChannelZone", k: str, eid: str | None) -> None:
    from ..realtime import combat
    w = _world()
    sk = skills()[k]
    rng = random.Random()
    try:
        async with dbm.SessionLocal() as db:
            user = await db.get(User, p.user_id)
            code, reason = await cast_check(db, p.user_id, k)
            if code is not None:
                p.q_pending = False
                refuse(p, k, code, reason)
                return
            code = _ready_code(p, k, eid, w.mono()) if p.channel is ch else "cannot"
            if code is not None:
                p.q_pending = False
                refuse(p, k, code)
                return
            m0 = ch.monster(eid) if (eid and sk["effect"] not in TARGETLESS) else None
            # M10: in a bí cảnh toán every question is at the answering player's own floor,
            # whoever is hit (plan 4.3) - so the target's own floor and micro-skill are not used
            own_floor = getattr(ch, "question_source", None) is not None
            info = m0.info if (m0 is not None and not own_floor) else None
            question, code = await question_for(db, user, sk, info, rng)
            if question is None:
                p.q_pending = False
                refuse(p, k, code)
                return
            mid = m0.eid if m0 is not None else None
            out = await quiz.create_session(db, user, CONTEXT, question, ref=f"{ch.key}|{mid or ''}|{k}")
            await db.commit()
    except Exception:
        log.exception("could not create a cast question")
        p.q_pending = False
        refuse(p, k, "cannot")
        return
    p.q_pending = False
    now = w.mono()
    # the world went on while the question was written: check everything again
    code = None
    if p.dead or p.ghost or p.channel is not ch or p.session is None or w.players.get(p.user_id) is not p:
        code = "cannot"
    elif p.question is not None:
        code = "answering"
    else:
        code = _ready_code(p, k, mid, now)
    if code is not None:
        refuse(p, k, code)
        return   # the question is never shown; it simply expires
    m = ch.monster(mid) if mid else None
    p.qi -= qi_cost(p, sk)
    p.mskill_ready[k] = now + cooldown(p, sk)
    limit = float(question.time_limit)
    deadline = now + limit + balance.quiz()["network_grace"]
    p.question = {"sid": out["session_id"], "mid": mid, "deadline": deadline, "asked": now, "limit": limit,
                  "timeout_sent": False, "cast": k, "ch": ch.key}
    p.protect_until = deadline
    p.inputs.clear()
    p.queued_ms = 0
    if m is not None:
        dx, dy = m.x - p.x, m.y - p.y
        p.facing = ("right" if dx > 0 else "left") if abs(dx) > abs(dy) else ("down" if dy > 0 else "up")
        combat.engage(ch, m, p, now)
    p.session.send({"t": "mcast", "k": k, "ok": True, "ready_in": cooldown(p, sk),
                    "qi": round(p.qi, 1)})
    p.session.send({"t": "q", "mid": mid, "q": out, "first_meet": False,
                    "cast": {"k": k, "name_vi": sk["name_vi"]}})
    ch.event(k="mcast", by=p.eid, s=k, anim=sk["anim"], x=p.x, y=p.y)


# ------------------------------------------------------------------ the answer
def _block(k: str, **kw) -> dict:
    out = {"cast": k, "correct": False, "missed": False, "timed_out": False, "damage": 0, "crit": False,
           "combo": 0, "combo_mult": 1.0, "shield_broken": False, "monster_hp": 0, "killed": False}
    out.update(kw)
    return out


def resolve(p: "Player", sid: str, correct: bool, answer_ms: int | None, timed_out: bool) -> dict:
    """The cast question was graded (in memory): the chiêu lands or misses."""
    from ..realtime import combat
    q = p.question
    if q is None or q["sid"] != sid or not q.get("cast"):
        return {"stale": True}
    k = q["cast"]
    ch = p.channel
    p.question = None
    p.protect_until = 0.0
    if ch is None or ch.key != q["ch"] or p.dead or k not in skills():
        return {"cast": k, "stale": True}
    sk = skills()[k]
    now = _world().mono()
    m = ch.monster(q["mid"]) if q["mid"] else None
    if sk["effect"] not in TARGETLESS and (m is None or not m.alive):
        return {"cast": k, "stale": True, "gone": True, "correct": correct}   # the target went away meanwhile
    ev = _event(p, k, sk, m)
    if not correct:   # chiêu hụt: no damage, the combo is gone, and no Mặc Kích
        p.mcombo = 0
        ch.event(**ev, ok=0, combo=0)
        if m is not None and m.alive and m.shield and p.user_id in m.engaged:
            p.next_q = (m.eid, now + combat.cfg()["next_question_delay"])   # the fight goes on
        return _block(k, missed=True, timed_out=bool(timed_out),
                      monster_hp=max(0, m.hp_pct()) if m is not None else 0)
    streak = p.mcombo
    p.mcombo = streak + 1
    fast = is_fast(answer_ms, q["limit"])
    return _land(p, ch, k, sk, m, ev, now, streak=streak, fast=fast, combo=p.mcombo, may_break=True)


def _land(p: "Player", ch: "ChannelZone", k: str, sk: dict, m, ev: dict, now: float, *, streak: int,
          fast: bool, combo: int, may_break: bool) -> dict:
    """A chiêu lands: damage x power x combo_mult(streak) (x the fast crit), the area's slow,
    or the ward. `may_break`: Vấn Đạo - a landed chiêu breaks the target's Mặc Thuẫn like a
    right answer; in the open world it does not (only a Phản Đòn does)."""
    from ..realtime import combat
    mult = combo_mult(streak)
    ev.update(ok=1, combo=combo)
    effect = sk["effect"]
    if effect == "ward":
        healed = _ward(ch, p, sk, now)
        ch.event(**ev)
        return _block(k, correct=True, crit=fast, combo=combo, combo_mult=mult, ward=healed)
    if effect == "shield":       # the stronger guard wins while two overlap, like Hộ Thân Trận
        before = p.guard_reduce if now < p.guard_until else 0.0
        p.guard_until = max(p.guard_until, now + float(sk["duration"]))
        p.guard_reduce = max(float(sk["reduce"]), before)
        ch.event(**ev)
        return _block(k, correct=True, crit=fast, combo=combo, combo_mult=mult,
                      shield={"duration": sk["duration"], "reduce": sk["reduce"]})
    if effect == "heal":
        healed = _heal(ch, p, sk)
        ch.event(**ev)
        return _block(k, correct=True, crit=fast, combo=combo, combo_mult=mult, heal=healed)
    if effect == "domain":
        _zones(ch).append({"kind": "domain", "uid": p.user_id, "k": k, "left": _ticks(sk["duration"], sk["every"]),
                           "next": now, "every": float(sk["every"]), "radius": float(sk["radius"]),
                           "power": float(sk["power"]), "streak": streak, "fast": fast})
        ch.event(**ev)
        return _block(k, correct=True, crit=fast, combo=combo, combo_mult=mult,
                      domain={"duration": sk["duration"], "radius": sk["radius"]})
    if effect in ("line", "chain", "cone", "root"):
        return _land_many(p, ch, k, sk, m, ev, now, streak=streak, fast=fast, combo=combo, may_break=may_break)
    if may_break and m.shield and m.info.get("group_shield"):
        progress = combat.group_hit(ch, m, p)
        if progress is not None:   # the others still have to answer: the boss's shield holds
            ch.event(**ev)
            return _block(k, correct=True, crit=fast, combo=combo, combo_mult=mult,
                          shield_progress=list(progress), monster_hp=max(0, m.hp_pct()))
    broke = may_break and m.shield
    if broke:
        combat.break_shield(ch, m, p, now)
    if sk["effect"] == "area":
        m.slow_until, m.slow_mult = now + sk["duration"], sk["slow"]
    dealt = combat.hurt_monster(ch, m, p, damage(combat.base_damage(p, m), sk, streak, fast, p), fast, now)
    if sk["effect"] == "area":
        cx, cy = ev["tx"], ev["ty"]
        ev["hits"] = [[m.eid, round(m.x, 1), round(m.y, 1)]]      # every monster in it (Chiêu Thức II)
        for o in list(ch.monsters):
            if o is m or not o.alive or combat.dist(cx, cy, o.x, o.y) > sk["radius"]:
                continue
            ev["hits"].append([o.eid, round(o.x, 1), round(o.y, 1)])
            o.slow_until, o.slow_mult = now + sk["duration"], sk["slow"]
            combat.engage(ch, o, p, now)
            combat.hurt_monster(ch, o, p, damage(combat.base_damage(p, o), sk, streak, fast, p), fast, now)
    ch.event(**ev)
    return _block(k, correct=True, damage=int(round(dealt)), crit=fast, combo=combo, combo_mult=mult,
                  shield_broken=broke, monster_hp=max(0, m.hp_pct()), killed=not m.alive)


def _ward(ch: "ChannelZone", p: "Player", sk: dict, now: float) -> dict:
    """Hộ Thân Trận: the caster and the party members standing near take less damage for a
    while (the stronger ward wins when two overlap) and are healed a little."""
    from ..realtime import combat
    near = [p] + [o for uid in _world().parties.mates(p.user_id)
                  if (o := ch.players.get(uid)) is not None and not o.dead
                  and combat.dist(p.x, p.y, o.x, o.y) <= sk["radius"]]
    healed = 0
    for o in near:
        reduce = float(sk["reduce"])
        if now < o.guard_until:
            reduce = max(reduce, o.guard_reduce)
        o.guard_until = max(o.guard_until, now + float(sk["duration"]))
        o.guard_reduce = reduce
        amount = min(o.max_hp - o.hp, o.max_hp * float(sk["heal_pct"]) / 100)
        if amount > 0:
            o.hp += amount
            healed += amount
            ch.event(k="heal", id=o.eid, v=int(round(amount)), x=o.x, y=o.y)
    return {"players": len(near), "heal": int(round(healed)), "duration": sk["duration"], "reduce": sk["reduce"]}


def _near_mates(ch: "ChannelZone", p: "Player", radius: float) -> list:
    from ..realtime import combat
    return [p] + [o for uid in _world().parties.mates(p.user_id)
                  if (o := ch.players.get(uid)) is not None and not o.dead
                  and combat.dist(p.x, p.y, o.x, o.y) <= radius]


def _heal(ch: "ChannelZone", p: "Player", sk: dict) -> dict:
    """Hồi Xuân Thuật: the caster and the party members standing near are healed."""
    near = _near_mates(ch, p, float(sk["radius"]))
    healed = 0.0
    for o in near:
        amount = min(o.max_hp - o.hp, o.max_hp * float(sk["heal_pct"]) / 100)
        if amount > 0:
            o.hp += amount
            healed += amount
            ch.event(k="heal", id=o.eid, v=int(round(amount)), x=o.x, y=o.y)
    return {"players": len(near), "heal": int(round(healed))}


# ------------------------------------------------------------------ Chiêu Thức II: the shapes
def _event(p: "Player", k: str, sk: dict, m) -> dict:
    """The `mskill` event of a cast (filled in by _land: ok, combo, and the targets struck).
    tx/ty: the chosen target; r: radius (area, ward, root, heal, domain); d: how long what it
    leaves lasts (area/root hold, shield, domain, burn); ex/ey/w: the end and width of a line."""
    ev = {"k": "mskill", "by": p.eid, "s": k, "fx": sk["fx"], "anim": sk["anim"], "x": p.x, "y": p.y}
    if m is not None and sk["effect"] not in TARGETLESS:
        ev.update(tx=m.x, ty=m.y)
    if "radius" in EFFECT_KEYS[sk["effect"]]:
        ev["r"] = sk["radius"]
    if sk["effect"] in ("area", "root", "shield", "domain"):
        ev["d"] = sk["duration"]
    if sk["effect"] == "line" and m is not None:
        ux, uy = _dir(p.x, p.y, m.x, m.y)
        ev.update(ex=round(p.x + ux * sk["range"], 1), ey=round(p.y + uy * sk["range"], 1), w=sk["width"])
        if "burn" in sk:
            ev["d"] = sk["burn"]["duration"]
    return ev


def _dir(ax: float, ay: float, bx: float, by: float) -> tuple[float, float]:
    d = math.hypot(bx - ax, by - ay)
    return ((bx - ax) / d, (by - ay) / d) if d > 1e-6 else (1.0, 0.0)


def seg_dist(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> tuple[float, float]:
    """(distance from P to the segment AB, how far along AB its foot is in 0..1)."""
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 <= 1e-9 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
    return math.hypot(px - (ax + dx * t), py - (ay + dy * t)), t


def line_targets(ch: "ChannelZone", p: "Player", m, sk: dict) -> list:
    """line: the first `pierce` live monsters, in the order the line meets them, within width/2
    of the segment that runs `range` px from the caster through the target (the target itself
    is always among them)."""
    ux, uy = _dir(p.x, p.y, m.x, m.y)
    ex, ey = p.x + ux * sk["range"], p.y + uy * sk["range"]
    found = []
    for o in ch.monsters:
        if not o.alive:
            continue
        d, t = seg_dist(o.x, o.y, p.x, p.y, ex, ey)
        if o is m or d <= sk["width"] / 2:
            found.append((t, o))
    found.sort(key=lambda x: x[0])
    picked = [o for _, o in found][: int(sk["pierce"])]
    if m not in picked:
        picked = picked[:-1] + [m]
        picked.sort(key=lambda o: seg_dist(o.x, o.y, p.x, p.y, ex, ey)[1])
    return picked


def cone_targets(ch: "ChannelZone", p: "Player", m, sk: dict) -> list:
    """cone: every live monster within `range` of the caster and within angle/2 of the aim."""
    from ..realtime import combat
    aim = math.atan2(m.y - p.y, m.x - p.x)
    half = math.radians(sk["angle"]) / 2
    out = [m]
    for o in ch.monsters:
        if o is m or not o.alive or combat.dist(p.x, p.y, o.x, o.y) > sk["range"]:
            continue
        a = math.atan2(o.y - p.y, o.x - p.x) - aim
        a = (a + math.pi) % (2 * math.pi) - math.pi
        if abs(a) <= half:
            out.append(o)
    return out


def chain_targets(ch: "ChannelZone", m, sk: dict, rng: random.Random) -> list:
    """chain: the target, then up to `hops` more, each a random live monster not struck yet
    within `hop_range` of the last one (Xác Suất: the lightning chooses)."""
    from ..realtime import combat
    out = [m]
    for _ in range(int(sk["hops"])):
        last = out[-1]
        near = [o for o in ch.monsters if o.alive and o not in out
                and combat.dist(last.x, last.y, o.x, o.y) <= sk["hop_range"]]
        if not near:
            break
        out.append(rng.choice(sorted(near, key=lambda o: o.eid)))
    return out


def root_mult(m) -> float:
    rr = data().get("root_rank_mult") or {}
    return float(rr.get(m.info.get("rank", "normal"), 1.0))


def _hold(m, now: float, seconds: float, mult: float) -> None:
    """Slow (or, at mult 0, hold in place) a monster; a stronger hold still running is kept."""
    if now < m.slow_until and m.slow_mult < mult:
        return
    m.slow_until, m.slow_mult = now + seconds, mult


def _land_many(p: "Player", ch: "ChannelZone", k: str, sk: dict, m, ev: dict, now: float, *, streak: int,
               fast: bool, combo: int, may_break: bool) -> dict:
    """line, chain, cone and root: several monsters struck at once. The chosen target alone may
    have its Mặc Thuẫn broken (a right bí cảnh answer); the others take the chiêu like the
    others of an area chiêu (a scratch while shielded). A chain hop deals falloff x the hop
    before it."""
    from ..realtime import combat
    mult = combo_mult(streak)
    effect = sk["effect"]
    if effect == "line":
        struck = line_targets(ch, p, m, sk)
    elif effect == "cone":
        struck = cone_targets(ch, p, m, sk)
    elif effect == "chain":
        struck = chain_targets(ch, m, sk, ch.rng)
    else:   # root: like an area round the target
        struck = [m] + [o for o in ch.monsters if o is not m and o.alive
                        and combat.dist(m.x, m.y, o.x, o.y) <= sk["radius"]]
    ev["hits"] = [[o.eid, round(o.x, 1), round(o.y, 1)] for o in struck]
    group = may_break and m.shield and m.info.get("group_shield")
    progress = combat.group_hit(ch, m, p) if group else None
    broke = may_break and m.shield and progress is None
    if broke:
        combat.break_shield(ch, m, p, now)
    dealt = 0.0
    scale = 1.0
    for i, o in enumerate(struck):
        if not o.alive:
            continue
        if effect == "root":
            _hold(o, now, float(sk["duration"]) * root_mult(o), 0.0)
        if o is not m:
            combat.engage(ch, o, p, now)
        hit = damage(combat.base_damage(p, o), sk, streak, fast, p) * scale
        if effect == "chain":
            scale *= float(sk["falloff"])
        got = combat.hurt_monster(ch, o, p, hit, fast, now)
        if o is m:
            dealt = got
    if effect == "line" and "burn" in sk and "ex" in ev:
        b = sk["burn"]
        _zones(ch).append({"kind": "burn", "uid": p.user_id, "k": k, "x0": p.x, "y0": p.y, "x1": ev["ex"],
                           "y1": ev["ey"], "width": float(sk["width"]), "left": _ticks(b["duration"], b["every"]),
                           "next": now + float(b["every"]), "every": float(b["every"]), "power": float(b["power"]),
                           "streak": streak, "fast": fast})
    ch.event(**ev)
    out = _block(k, correct=True, damage=int(round(dealt)), crit=fast, combo=combo, combo_mult=mult,
                 shield_broken=bool(broke), monster_hp=max(0, m.hp_pct()), killed=not m.alive,
                 hits=len(struck))
    if progress is not None:
        out["shield_progress"] = list(progress)
    return out


# ------------------------------------------------------------------ what stays on the ground
def _zones(ch: "ChannelZone") -> list:
    """The burning strips and sword domains of a channel (made on demand: any ChannelZone)."""
    z = getattr(ch, "chieu_zones", None)
    if z is None:
        z = ch.chieu_zones = []
    return z


def _ticks(duration: float, every: float) -> int:
    """How many times a zone strikes: once every `every` s for `duration` s."""
    return max(1, int(round(float(duration) / float(every))))


def tick_zones(ch: "ChannelZone", now: float) -> None:
    """realtime/combat.tick: every `every` seconds a burn strip or a domain strikes every
    monster inside it (base x its power x the cast's combo and crit and the caster's linh căn):
    a domain from the moment it is cast, a burn strip one `every` later, duration / every times
    in all. A domain follows its caster; any zone ends early when its caster falls or leaves."""
    from ..realtime import combat
    zones = getattr(ch, "chieu_zones", None)
    if not zones:
        return
    keep = []
    for z in zones:
        p = ch.players.get(z["uid"])
        if z["left"] <= 0 or p is None or p.dead or z["k"] not in skills():
            continue
        if now < z["next"] - 1e-6:
            keep.append(z)
            continue
        z["next"] += z["every"]
        z["left"] -= 1
        if z["left"] > 0:
            keep.append(z)
        sk = skills()[z["k"]]
        for o in list(ch.monsters):
            if not o.alive:
                continue
            if z["kind"] == "domain":
                inside = combat.dist(p.x, p.y, o.x, o.y) <= z["radius"]
            else:
                inside = seg_dist(o.x, o.y, z["x0"], z["y0"], z["x1"], z["y1"])[0] <= z["width"] / 2
            if not inside:
                continue
            combat.engage(ch, o, p, now)
            hit = damage(combat.base_damage(p, o), {**sk, "power": z["power"]}, z["streak"], z["fast"], p)
            combat.hurt_monster(ch, o, p, hit, False, now)
    ch.chieu_zones = keep


async def math_skill_handler(db: AsyncSession, user: User, s: QuizSession, correct: bool,
                             now: dt.datetime) -> dict:
    """Grading a cast question (answered or timed out): the learning log first, then the fight."""
    out: dict = {"math": await math_combat.record(db, user, s, correct, now)}
    p = _world().players.get(user.id)
    if p is not None:
        out["combat"] = resolve(p, s.id, correct, s.answer_ms, out["math"]["timed_out"])
        out["combat"].setdefault("cast", (s.ref or "").rsplit("|", 1)[-1])   # ref = "<channel>|<mid>|<chiêu>"
    return out


quiz.register_handler(CONTEXT, math_skill_handler)
quiz.register_xp_rule(CONTEXT, math_combat.xp_rule)
