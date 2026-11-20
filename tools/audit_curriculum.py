#!/usr/bin/env python3
"""Audit the learning tree (Đạo Thụ) with numbers - pure Python, no network, re-runnable.

    python tools/audit_curriculum.py            # print the headline and write the tables
    python tools/audit_curriculum.py --quiet    # only write the tables
    python tools/audit_curriculum.py --json     # print the headline numbers as JSON

It reads the game's own data (tree.json, the four subject files, the items and generators, the
programming exercises, the library, the sources, monsters/skills/world plan/guide/achievements)
and writes `docs/GIAO_TRINH_RA_SOAT_SO_LIEU.md`: per branch and node the stage, prerequisites,
micro-skills and how many questions each micro-skill has at each tier it can be asked at; what can
never be asked; prerequisite problems; the workload of each stage; how the branches interleave;
how the nodes link to each other and how the spiral review samples old material; which nodes have
a library document and a source; which nodes nothing in the game touches. The headline numbers
(`headline()`) are what docs/GIAO_TRINH_RA_SOAT.md quotes before and after the fixes.

A **cell** is one micro-skill at one tier its floor can show (balance/math.json floor_tiers). Its
**capacity** is how many different questions the learner can meet there: each hand-written item
counts one, each generator counts the number of different questions 40 seeds give. A cell is
**thin** when its capacity is below THIN (the learner sees the same question again within a few
answers: the anti-repeat window is 50 answers over all micro-skills of the sitting).
"""
from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_items, math_library, math_path, math_problems, math_tree  # noqa: E402

MATH_DIR = ROOT / "server" / "data" / "math"
OUT = ROOT / "docs" / "GIAO_TRINH_RA_SOAT_SO_LIEU.md"
THIN = 10               # a cell with fewer different questions than this is thin
DRAWS = 40              # seeds used to measure how many different questions a generator gives
BRANCH_ORDER = ["ds", "gt", "xs", "tr", "lt", "ud", "ml", "dl", "ht", "nc"]


# ------------------------------------------------------------------ gathering
@lru_cache(maxsize=1)
def tree() -> math_tree.Tree:
    return math_tree.tree()


@lru_cache(maxsize=None)
def variety(gen_id: str) -> int:
    """How many different questions a generator gives over DRAWS seeds."""
    spec = math_items.generators()[gen_id]
    return len({math_items.draw(spec, random.Random(seed)).fingerprint for seed in range(DRAWS)})


def skill_floor() -> dict[str, int]:
    return {s.id: s.floor for subj in math_path.subjects() for s in subj.skills.values()}


def skill_name() -> dict[str, str]:
    return {s.id: s.name_vi for subj in math_path.subjects() for s in subj.skills.values()}


def skill_subject() -> dict[str, str]:
    return {s.id: subj.id for subj in math_path.subjects() for s in subj.skills.values()}


def cells() -> dict[tuple[str, int], dict]:
    """(skill, tier) -> {'items': n, 'gens': n, 'cap': n, 'types': set}, for every tier the skill's
    floor can show (also those without a template: they are the holes)."""
    floors, out = skill_floor(), {}
    for skill, floor in floors.items():
        for tier in math_path.allowed_tiers(floor):
            out[(skill, tier)] = {"items": 0, "gens": 0, "cap": 0, "types": set()}
    for it in math_items.bank().values():
        c = out.get((it.skill, it.tier))
        if c is None:
            c = out.setdefault((it.skill, it.tier), {"items": 0, "gens": 0, "cap": 0, "types": set(), "off": True})
        c["items"] += 1
        c["cap"] += 1
        c["types"].add(it.qtype)
    for g in math_items.generators().values():
        c = out.get((g.skill, g.tier))
        if c is None:
            c = out.setdefault((g.skill, g.tier), {"items": 0, "gens": 0, "cap": 0, "types": set(), "off": True})
        c["gens"] += 1
        c["cap"] += variety(g.id)
        c["types"].add(g.qtype)
    return out


def node_refs() -> dict[str, Counter]:
    """node id -> Counter of the places (file:section) that name it, outside tree.json."""
    ids = set(tree().nodes)
    refs: dict[str, Counter] = defaultdict(Counter)

    def walk(value, label: str):
        if isinstance(value, dict):
            for k, v in value.items():
                walk(v, label)
        elif isinstance(value, list):
            for v in value:
                walk(v, label)
        elif isinstance(value, str) and value in ids:
            refs[value][label] += 1

    files = {"monsters": MATH_DIR / "monsters.json", "chiêu": MATH_DIR / "skills.json",
             "world_plan": MATH_DIR / "world_plan.json",
             "thành tựu": ROOT / "server" / "data" / "achievements.json",
             "lộ trình": ROOT / "server" / "data" / "guide.json",
             "thả đồ": ROOT / "server" / "data" / "loot_tiers.json"}
    for label, path in files.items():
        if not path.is_file():
            continue
        raw = json.loads(path.read_text("utf-8"))
        if label == "world_plan" and isinstance(raw, dict):
            for section, body in raw.items():
                walk(body, f"world_plan.{section}")
        else:
            walk(raw, label)
    return refs


def sources_of(branch: str) -> dict:
    path = MATH_DIR / "sources" / f"{branch}.json"
    if not path.is_file():
        return {}
    raw = json.loads(path.read_text("utf-8"))
    return raw.get("nodes", {}) if isinstance(raw, dict) else {}


def templated_skills() -> set[str]:
    """The micro-skills that have at least one template (hand-written or generator), cut or not."""
    return {i.skill for i in math_items.bank().values()} | {g.skill for g in math_items.generators().values()}


# ------------------------------------------------------------------ analysis
def analyse() -> dict:
    t = tree()
    cut = t.cut_skills()
    floors, names, cell = skill_floor(), skill_name(), cells()
    have = templated_skills()
    refs = node_refs()
    sub = skill_subject()
    out: dict = {"cut": cut, "cell": cell}

    # ---- per node
    rows = []
    for n in t.nodes.values():
        sk = [s for s in n.skills if s not in cut]
        asked = [s for s in sk if s in have]
        rows.append({
            "node": n,
            "floors": sorted({floors[s] for s in n.skills}),
            "asked": asked,
            "unasked": [s for s in sk if s not in have],
            "docs": sum(1 for s in n.skills if math_library.for_skill(s) is not None),
            "source": bool(sources_of(n.branch).get(n.id, {}).get("primary")),
            "refs": refs.get(n.id, Counter()),
            "xbranch": sorted({t.nodes[r].branch for r in n.requires + n.reinforces
                               if t.nodes[r].branch != n.branch}),
            "real": ("co" if (asked or n.problems) else "chua_co"),
        })
    out["rows"] = rows

    # ---- cells
    reach = {}
    for (s, tier), c in cell.items():
        if c.get("off"):
            continue
        node = next((n for n in t.nodes.values() if s in n.skills), None)
        reach[(s, tier)] = (c, node)
    out["reach"] = reach
    asked_cells = [(k, c, node) for k, (c, node) in reach.items()
                   if k[0] not in cut and node is not None and node.main]
    out["main_cells"] = asked_cells
    out["thin"] = sorted(((k, c, node) for k, c, node in asked_cells if c["cap"] < THIN),
                         key=lambda r: (r[1]["cap"], r[2].stage or 99, r[0]))
    out["holes"] = [(k, c, node) for k, c, node in asked_cells if c["items"] + c["gens"] == 0]
    out["off_tier"] = [(k, c) for k, c in cell.items() if c.get("off")]
    out["opt_thin"] = [(k, c, node) for k, (c, node) in reach.items()
                       if k[0] not in cut and node is not None and not node.main and c["cap"] < THIN]

    # ---- what can never be asked
    dead_items = [i for i in math_items.bank().values() if i.skill in cut]
    dead_gens = [g for g in math_items.generators().values() if g.skill in cut]
    out["dead_items"], out["dead_gens"] = dead_items, dead_gens
    out["cut_by_floor"] = Counter((skill_subject()[s], floors[s]) for s in cut)
    # the owner's rule is "no proofs" (tree.json rules.no_proof_items): hand-written items on a path the
    # player really walks whose question asks for a proof
    main_skills = {s for n in t.nodes.values() if n.main for s in n.skills} - cut
    out["proof_items"] = sorted((i for i in math_items.bank().values()
                                 if i.skill in main_skills and "chứng minh" in i.prompt_vi.lower()),
                                key=lambda i: i.id)
    out["no_templates_main"] = [(n, s) for r in rows for n in [r["node"]] if n.main for s in r["unasked"]]
    out["no_templates_opt"] = [(r["node"], s) for r in rows if not r["node"].main for s in r["unasked"]]

    # ---- prerequisites (independent of math_tree.validate: it is a second pair of eyes)
    prob = []
    for n in t.nodes.values():
        for r in n.requires:
            q = t.nodes[r]
            if n.main and q.main and t.realm_order[q.realm] == t.realm_order[n.realm] and q.stage > n.stage:
                prob.append(f"{n.id} (stage {n.stage}) requires {r} (stage {q.stage})")
            if n.main and not q.main:
                prob.append(f"{n.id} (main) requires {r} (optional)")
        # floor order inside one subject: a node must not come before a node whose floors are higher
        for r in n.requires:
            q = t.nodes[r]
            if n.skills and q.skills and sub[n.skills[0]] == sub[q.skills[0]]:
                if max(floors[s] for s in q.skills) > max(floors[s] for s in n.skills):
                    prob.append(f"{n.id}: needs {r}, but {r} has floors "
                                f"{sorted({floors[s] for s in q.skills})} and {n.id} "
                                f"{sorted({floors[s] for s in n.skills})} (floor order inverted)")
        for r in n.reinforces:
            if not t.nodes[r].skills and not any(t.nodes[x].skills for x in t.nodes[r].requires):
                pass
    out["prereq_problems"] = prob
    # a node whose skills ask for older skills that a later-stage node owns is the validator's job

    # ---- stage workload (Luyện Khí main path)
    stage = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))     # stage -> branch -> [nodes, skills, exercises]
    for n in t.main_nodes("luyen_khi"):
        cellv = stage[n.stage][n.branch]
        cellv[0] += 1
        cellv[1] += len([s for s in n.skills if s not in cut])
        cellv[2] += len(n.problems)
    out["stage"] = stage

    # ---- interleave: how soon is the math of a node used by a code / thực chiến node
    use_gap = {}
    for n in t.main_nodes("luyen_khi"):
        if n.kind != "toan":
            continue
        users = [m for m in t.nodes.values() if m.main and m.kind in ("code", "thuc_chien", "du_an")
                 and (n.id in m.requires or n.id in m.reinforces or n.id in t.ancestors(m.id))
                 and m.realm == "luyen_khi"]
        direct = [m for m in users if n.id in m.requires or n.id in m.reinforces]
        use_gap[n.id] = (min((m.stage - n.stage for m in direct), default=None),
                         min((m.stage - n.stage for m in users), default=None))
    out["use_gap"] = use_gap

    # ---- cross links and the spiral review
    cross = Counter()
    for n in t.nodes.values():
        for r in n.requires + n.reinforces:
            if t.nodes[r].branch != n.branch:
                cross[(n.branch, t.nodes[r].branch)] += 1
    out["cross"] = cross
    reviewed_by = defaultdict(set)
    for n in t.nodes.values():
        for r in n.reinforces:
            reviewed_by[r].add(n.id)
    out["reviewed_by"] = reviewed_by
    review = {}
    for n in t.nodes.values():
        if not n.skills or not n.main:
            continue
        pool = [s for s in t.review_skills(n.id) if s not in cut and s in have]
        fallback = False
        if not pool:
            pool = [s for a in t.ancestors(n.id) for s in t.nodes[a].skills if s not in cut and s in have]
            fallback = True
        other = [s for s in pool if sub.get(s) != sub[n.skills[0]]]
        review[n.id] = {"pool": len(pool), "other": len(other), "fallback": fallback}
    out["review"] = review
    out["isolated"] = [n for n in t.main_nodes("luyen_khi")
                       if not any(t.nodes[r].branch != n.branch for r in n.requires + n.reinforces)
                       and not any(n.id in m.requires + m.reinforces and m.branch != n.branch
                                   for m in t.nodes.values())]

    # ---- touched by the game
    out["untouched"] = [r["node"] for r in rows
                        if r["node"].main and r["node"].realm == "luyen_khi" and not r["refs"]
                        and not r["node"].problems]
    return out


def headline(a: dict | None = None) -> dict:
    a = a or analyse()
    t = tree()
    nodes = list(t.nodes.values())
    lk = [n for n in nodes if n.realm == "luyen_khi" and n.main]
    return {
        "nodes": len(nodes),
        "nodes_luyen_khi_main": len(lk),
        "nodes_content_co": sum(n.content == "co" for n in nodes),
        "nodes_content_dang_viet": sum(n.content == "dang_viet" for n in nodes),
        "nodes_content_chua_co": sum(n.content == "chua_co" for n in nodes),
        "luyen_khi_main_nodes_without_questions_or_exercises":
            sum(1 for r in a["rows"] if r["node"].main and r["node"].realm == "luyen_khi" and r["real"] == "chua_co"),
        "skills_total": len(skill_floor()),
        "skills_cut": len(a["cut"]),
        "cells_main": len(a["main_cells"]),
        "cells_thin": len(a["thin"]),
        "cells_holes": len(a["holes"]),
        "cells_optional_thin": len(a["opt_thin"]),
        "cut_items": len(a["dead_items"]),
        "cut_generators": len(a["dead_gens"]),
        "main_skills_without_template": len(a["no_templates_main"]),
        "proof_questions_on_main_path": len(a["proof_items"]),
        "nodes_isolated_luyen_khi": len(a["isolated"]),
        "nodes_flag_wrong_luyen_khi": sum(1 for r in a["rows"] if r["node"].realm == "luyen_khi" and r["node"].main
                                          and (r["node"].content == "co") != (r["real"] == "co")),
        "prerequisite_problems": len(a["prereq_problems"]),
        "hand_items": len(math_items.bank()),
        "generators": len(math_items.generators()),
        "exercises": len(math_problems.bank()),
    }


# ------------------------------------------------------------------ the report
def md_table(head: list[str], rows: list[list]) -> list[str]:
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return out


def render(a: dict) -> str:
    t = tree()
    names, floors, cut = skill_name(), skill_floor(), a["cut"]
    h = headline(a)
    lines: list[str] = ["# Rà soát giáo trình: số liệu",
                        "",
                        "Tệp này do `tools/audit_curriculum.py` sinh ra, đừng sửa tay. "
                        "Chạy lại: `python tools/audit_curriculum.py`.",
                        "",
                        f"Một **ô** là một vi kỹ năng ở một bậc mà tầng của nó có thể hỏi. **Sức chứa** của ô là số câu "
                        f"khác nhau người học gặp được ở đó: mỗi câu viết tay tính 1, mỗi bộ sinh câu tính số câu khác "
                        f"nhau của {DRAWS} hạt giống. Ô **mỏng** là ô có sức chứa dưới {THIN}.",
                        "",
                        "## 1. Con số chính", ""]
    lines += md_table(["Chỉ số", "Giá trị"], [[k, v] for k, v in h.items()])

    # ---- per branch and node
    lines += ["", "## 2. Từng nhánh, từng nút", "",
              "Cột `Tầng` là tầng của Luyện Khí (— = nút phụ). `Thật` là nút có thật câu hỏi hay bài tập "
              "(so với cờ `content` trong tree.json). `Thư viện` = số vi kỹ năng có tài liệu. "
              "`Chạm` = nơi khác trong game nhắc tới nút (quái, chiêu, kế hoạch thế giới, thành tựu, lộ trình).", ""]
    by_branch = defaultdict(list)
    for r in a["rows"]:
        by_branch[r["node"].branch].append(r)
    for b in t.raw["branches"]:
        rs = by_branch.get(b["id"], [])
        if not rs:
            continue
        lines += [f"### {b['id']}: {b['name_vi']}", ""]
        rs.sort(key=lambda r: (not r["node"].main, t.realm_order[r["node"].realm], r["node"].stage or 99, r["node"].id))
        table = []
        for r in rs:
            n = r["node"]
            touch = ", ".join(f"{k}×{v}" for k, v in sorted(r["refs"].items())) or "—"
            table.append([f"`{n.id}`", n.realm.replace("luyen_khi", "LK") if n.realm == "luyen_khi" else n.realm,
                          n.stage or "—", "chính" if n.main else "phụ", n.kind, n.content, r["real"],
                          ", ".join(f"`{x}`" for x in n.requires) or "—",
                          f"{len(n.skills)} ({len(r['asked'])} có câu)" if n.skills else f"{len(n.problems)} bài",
                          ",".join(map(str, r["floors"])) or "—", r["docs"] or "—",
                          "có" if r["source"] else "—", touch])
        lines += md_table(["Nút", "Cảnh", "Tầng", "Loại", "Kiểu", "content", "Thật", "Cần", "Vi kỹ năng / bài",
                           "Tầng toán", "Thư viện", "Nguồn", "Chạm"], table)
        lines.append("")

    # ---- cell matrix
    lines += ["## 3. Vi kỹ năng × bậc", "",
              "Mỗi ô ghi `viết tay/bộ sinh→sức chứa`. Ô mỏng đánh dấu `!`. Vi kỹ năng thuộc danh sách cắt "
              "có ghi `cắt`.", ""]
    sub = skill_subject()
    for subj in math_path.subjects():
        lines += [f"### {subj.name_vi}", ""]
        head = ["Vi kỹ năng", "Nút", "Tầng toán", "Bậc 1", "Bậc 2", "Bậc 3", "Bậc 4", "Bậc 5"]
        rows = []
        for s in subj.skills.values():
            node = next((n for n in t.nodes.values() if s.id in n.skills), None)
            tiers = math_path.allowed_tiers(s.floor)
            cs = []
            for tier in range(1, 6):
                c = a["cell"].get((s.id, tier))
                if tier not in tiers or c is None:
                    cs.append("")
                else:
                    mark = "!" if c["cap"] < THIN and s.id not in cut else ""
                    cs.append(f"{c['items']}/{c['gens']}→{c['cap']}{mark}")
            rows.append([f"`{s.id}`" + (" cắt" if s.id in cut else ""), f"`{node.id}`" if node else "—",
                         s.floor] + cs)
        lines += md_table(head, rows) + [""]

    # ---- thin
    lines += ["## 4. Các ô mỏng nhất (nút chính)", "",
              f"{len(a['thin'])} ô có sức chứa dưới {THIN}, xếp từ mỏng nhất. `Thứ tự` = tầng của nút.", ""]
    lines += md_table(["Vi kỹ năng", "Bậc", "Viết tay", "Bộ sinh", "Sức chứa", "Nút", "Tầng nút"],
                      [[f"`{k[0]}`", k[1], c["items"], c["gens"], c["cap"], f"`{n.id}`", n.stage]
                       for k, c, n in a["thin"]])
    lines += ["", f"Ô mỏng thuộc nút phụ: {len(a['opt_thin'])}. Ô không có câu nào ở nút chính: {len(a['holes'])}.", ""]

    # ---- never asked
    lines += ["## 5. Câu hỏi không bao giờ được hỏi", "",
              f"- Danh sách cắt có {len(cut)} vi kỹ năng; trong kho vẫn còn {len(a['dead_items'])} câu viết tay và "
              f"{len(a['dead_gens'])} bộ sinh câu trên các vi kỹ năng đó.",
              "- Số vi kỹ năng cắt theo tầng: " + ", ".join(f"{s} tầng {f}: {n}" for (s, f), n in sorted(a["cut_by_floor"].items())),
              f"- Vi kỹ năng của nút chính chưa có câu nào: {len(a['no_templates_main'])}"
              + (": " + ", ".join(f"`{s}`" for _, s in a["no_templates_main"]) if a["no_templates_main"] else "."),
              f"- Vi kỹ năng của nút phụ chưa có câu nào: {len(a['no_templates_opt'])}"
              + (": " + ", ".join(f"`{s}`" for _, s in a["no_templates_opt"]) if a["no_templates_opt"] else "."),
              ""]
    vac = [r["node"] for r in a["rows"] if r["node"].main and r["node"].realm == "luyen_khi" and r["real"] == "chua_co"]
    lines += ["- Nút chính Luyện Khí không có câu hỏi lẫn bài tập (tính là 'đang biên soạn', coi như xong): "
              + (", ".join(f"`{n.id}`" for n in vac) if vac else "không có."),
              "- Nút các cảnh sau Luyện Khí: " + ", ".join(
                  f"{r}: {sum(1 for n in t.nodes.values() if n.realm == r)}" for r in t.realm_order if r != "luyen_khi")
              + " (tất cả `chua_co`: là thiết kế, chưa nối vào game).", ""]
    stale = [(r["node"], r["real"]) for r in a["rows"]
             if r["node"].realm == "luyen_khi" and r["node"].main and (r["node"].content == "co") != (r["real"] == "co")]
    lines += ["- Nút chính Luyện Khí có cờ `content` không khớp thực tế (có câu hỏi hay bài tập mà không phải `co`, "
              "hoặc `co` mà trống): "
              + (", ".join(f"`{n.id}` ({n.content}, thật: {real})" for n, real in stale) if stale else "không có."),
              f"- Câu hỏi bắt chứng minh trên đường chính (luật của tree.json là không hỏi chứng minh): "
              f"{len(a['proof_items'])} câu viết tay"
              + (": " + ", ".join(f"`{i.id}`" for i in a["proof_items"]) if a["proof_items"] else "") + ".", ""]

    # ---- prerequisites
    lines += ["## 6. Điều kiện tiên quyết", ""]
    lines += ([f"- {p}" for p in a["prereq_problems"]] if a["prereq_problems"]
              else ["Không có vấn đề: không vòng, không nút nào cần nút ở tầng sau, không nút chính cần nút phụ, "
                    "thứ tự tầng toán trong một môn khớp thứ tự nút."])
    lines.append("")

    # ---- stage workload
    lines += ["## 7. Khối lượng từng tầng (Luyện Khí, nút chính, không tính vi kỹ năng bị cắt)", "",
              "Mỗi ô: `số nút / số vi kỹ năng / số bài tập`.", ""]
    branches = [b for b in BRANCH_ORDER if any(b in a["stage"][s] for s in a["stage"])]
    table = []
    totals = {}
    for s in sorted(a["stage"]):
        tot = [0, 0, 0]
        row = [s]
        for b in branches:
            v = a["stage"][s].get(b, [0, 0, 0])
            row.append("—" if v == [0, 0, 0] else "/".join(map(str, v)))
            tot = [x + y for x, y in zip(tot, v)]
        row.append("/".join(map(str, tot)))
        totals[s] = tot
        table.append(row)
    lines += md_table(["Tầng"] + branches + ["Cộng"], table)
    skills_by_stage = [v[1] for v in totals.values()]
    med = statistics.median(skills_by_stage)
    walls = [s for s, v in totals.items() if v[1] > 1.4 * med]
    deserts = [s for s, v in totals.items() if v[1] < 0.6 * med]
    lines += ["", f"Số vi kỹ năng mỗi tầng: trung vị {med:g}, thấp nhất {min(skills_by_stage)}, cao nhất {max(skills_by_stage)}. "
              f"Tầng nặng (trên 1,4 lần trung vị): {walls or 'không'}. Tầng nhẹ (dưới 0,6 lần): {deserts or 'không'}.", ""]

    # ---- interleave
    lines += ["## 8. Lập trình chạy song song với toán", "",
              "Với mỗi nút toán của Luyện Khí: sau bao nhiêu tầng thì có một nút code/thực chiến dùng nó trực tiếp "
              "(cần hoặc ôn lại nó), và sau bao nhiêu tầng thì có nút code/thực chiến nào ở sau nó trên đường đi. "
              "`—` = chưa có nút code nào dùng.", ""]
    rows = []
    for nid, (d, anyg) in a["use_gap"].items():
        n = t.nodes[nid]
        rows.append([f"`{nid}`", n.branch, n.stage, "—" if d is None else d, "—" if anyg is None else anyg])
    lines += md_table(["Nút toán", "Nhánh", "Tầng", "Dùng trực tiếp sau (tầng)", "Dùng gián tiếp sau (tầng)"], rows)
    direct = [d for d, _ in a["use_gap"].values() if d is not None]
    lines += ["", f"{len(direct)}/{len(a['use_gap'])} nút toán có nút code/thực chiến dùng trực tiếp; "
              f"độ trễ trung vị {statistics.median(direct) if direct else '—'} tầng.", ""]
    ct = Counter()
    for n in t.main_nodes("luyen_khi"):
        ct[(n.stage, "toán" if n.kind == "toan" else "code")] += 1
    lines += md_table(["Tầng", "Nút toán", "Nút code / thực chiến / dự án"],
                      [[s, ct[(s, "toán")], ct[(s, "code")]] for s in range(1, 10)]) + [""]

    # ---- cross links
    lines += ["## 9. Liên kết giữa các nhánh và ôn tập cuốn chiếu", "",
              "Số cạnh `requires` + `reinforces` đi từ nhánh hàng sang nhánh cột:", ""]
    bs = [b["id"] for b in t.raw["branches"] if any((b["id"], c) in a["cross"] or (c, b["id"]) in a["cross"] for c in BRANCH_ORDER)]
    lines += md_table(["từ \\ sang"] + bs, [[x] + [a["cross"].get((x, y), "") or "·" for y in bs] for x in bs])
    lines += ["", f"Nút chính Luyện Khí không liên kết với nhánh khác (không cạnh ra, không cạnh vào): "
              + (", ".join(f"`{n.id}`" for n in a["isolated"]) if a["isolated"] else "không có."), ""]
    lines += ["Nút chính Luyện Khí chưa nút nào ôn lại (không có trong `reinforces` của nút nào) - dễ phai:", ""]
    unreviewed = [n for n in t.main_nodes("luyen_khi") if n.skills and not a["reviewed_by"].get(n.id)]
    lines += [", ".join(f"`{n.id}`" for n in unreviewed) or "không có.", ""]
    rv = a["review"]
    lines += ["Nguồn câu ôn của từng nút toán chính (vi kỹ năng có câu hỏi, lấy từ các nút trong `reinforces`; "
              "nếu rỗng thì lấy từ tổ tiên đã xong): `nguồn khác môn` là số vi kỹ năng thuộc môn khác.", ""]
    lines += md_table(["Nút", "Số vi kỹ năng ôn", "Khác môn", "Dùng tổ tiên thay thế"],
                      [[f"`{k}`", v["pool"], v["other"], "có" if v["fallback"] else ""] for k, v in rv.items()])
    empty = [k for k, v in rv.items() if v["pool"] == 0]
    lines += ["", f"Nút toán chính không có nguồn câu ôn nào (ôn tập im lặng): {empty or 'không'}. "
              f"Nút có ít hơn 3 vi kỹ năng để ôn: {[k for k, v in rv.items() if 0 < v['pool'] < 3] or 'không'}.", ""]

    # ---- library, source
    lines += ["## 10. Tài liệu và nguồn", ""]
    mathn = [r for r in a["rows"] if r["node"].main and r["node"].realm == "luyen_khi" and r["node"].skills]
    nodoc = [r["node"].id for r in mathn if r["docs"] < len(r["node"].skills)]
    nosrc = [r["node"].id for r in a["rows"] if r["node"].main and r["node"].realm == "luyen_khi" and not r["source"]]
    lines += [f"- Nút toán chính Luyện Khí có đủ tài liệu thư viện cho mọi vi kỹ năng: {len(mathn) - len(nodoc)}/{len(mathn)}"
              + (f"; thiếu: {nodoc}" if nodoc else "") + ".",
              f"- Nút chính Luyện Khí chưa có nguồn đọc (sources/*.json): {len(nosrc)}" + (f": {nosrc}" if nosrc else "") + ".", ""]

    # ---- touched
    lines += ["## 11. Nút nào trong game chạm tới", "",
              "Nút chính Luyện Khí mà không quái, chiêu, kế hoạch thế giới, thành tựu, lộ trình nào nhắc tới "
              "và không có bài tập: " + (", ".join(f"`{n.id}`" for n in a["untouched"]) or "không có") + ".", ""]
    byk = Counter()
    for r in a["rows"]:
        for k in r["refs"]:
            byk[k] += 1
    lines += ["Số nút được nhắc tới, theo nơi: " + ", ".join(f"{k}: {v}" for k, v in sorted(byk.items())) + ".", ""]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    a = analyse()
    h = headline(a)
    text = render(a)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    if args.json:
        print(json.dumps(h, ensure_ascii=False, indent=1))
    elif not args.quiet:
        for k, v in h.items():
            print(f"{k:55} {v}")
        print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
