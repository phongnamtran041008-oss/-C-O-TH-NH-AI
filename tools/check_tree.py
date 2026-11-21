#!/usr/bin/env python3
"""Check the curriculum tree and the world plan, and write the readable version of them.

    python tools/check_tree.py            # check only; exit 1 on any problem
    python tools/check_tree.py --doc      # also (re)write docs/GIAO_TRINH_CAY.md

The data is `server/data/math/tree.json` and `server/data/math/world_plan.json`; the rules
are in `server/app/learning/math_tree.py`, Chính đạo (`main_path`, the one order of the main-path
nodes) included. The document is generated from the data, so it can
never say something different from what the game will read. tools/check_all.py runs the
same checks (and that every main-path node can be reached) as one of its checks.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_path, math_tree as mt  # noqa: E402

DOC = ROOT / "docs" / "GIAO_TRINH_CAY.md"
KIND_VI = {"toan": "Toán", "code": "Lập trình", "thuc_chien": "Thực chiến AI", "du_an": "Dự án",
           "hoc_may": "Học máy", "hoc_sau": "Học sâu", "he_thong": "Hệ thống",
           "nghien_cuu": "Nghiên cứu", "dan_dat": "Dẫn dắt"}
CONTENT_VI = {"co": "đã có câu hỏi", "dang_viet": "đang viết", "chua_co": "chưa có"}


def skill_names() -> dict[str, str]:
    return {s.id: s.name_vi for subj in math_path.subjects() for s in subj.skills.values()}


def build_doc() -> str:
    t, plan, names = mt.tree(), mt.world_plan(), skill_names()
    raw = t.raw
    branch = {b["id"]: b for b in raw["branches"]}
    skills = mt.subject_skills()
    status = [t.skill_status(s) for s in skills]
    out: list[str] = []
    w = out.append

    w("# Đạo Thụ — cây giáo trình và bản đồ mở khoá\n")
    w("> File này do `python tools/check_tree.py --doc` dựng từ `server/data/math/tree.json` và "
      "`server/data/math/world_plan.json`. Muốn đổi thì sửa hai file dữ liệu ấy rồi chạy lại, đừng sửa ở đây.\n")
    w(f"**Mục tiêu:** {raw['rules']['goal_vi']}\n")
    w("## Cách cây vận hành\n")
    w("- Không còn học hết môn này mới sang môn kia. Mỗi **nút** là một cụm bài nhỏ; nút mở khi các nút nó cần "
      "(kể cả của nhánh khác) đã xong, nên Đại Số, Giải Tích, Xác Suất, Thuật Toán và Lập Trình đi song song.")
    w("- Mỗi nút ghi rõ nó **ôn lại** những nút cũ nào: khoảng một phần tư số câu của nút lấy từ đó, để học cái mới "
      "mà cái cũ không mai một.")
    w("- Lên một **tầng** tu vi khi mọi nút chính đạo của tầng ấy xong — luôn gồm cả toán lẫn code.")
    w(f"- {raw['rules']['no_proof_items_vi']}")
    w("- **Bàng môn** là phần tuỳ chọn, không chặn gì. Phần **bị loại** không bao giờ được hỏi.")
    w("- **Chính đạo** (`main_path` trong tree.json) là thứ tự học duy nhất của các nút chính đạo: cảnh giới, tầng, "
      "rồi thứ tự trong tầng (cột #). Nút luôn đứng sau những nút nó cần; nút lập trình hay thực chiến đứng ngay "
      "sau phần toán nó dùng. Game dẫn người chơi đi đúng thứ tự ấy, mỗi lúc một việc.\n")
    w(f"Trong {len(skills)} vi kỹ năng của bốn bí cảnh: **{status.count('chinh')} chính đạo**, "
      f"{status.count('phu')} bàng môn (tuỳ chọn), {status.count('cut')} bị loại.\n")

    realms = sorted(raw["realms"], key=lambda r: r["order"])
    unlocks = plan["unlocks"]
    for realm in realms:
        w(f"## {realm['order']}. {realm['name_vi']} — {realm['theme_vi']}\n")
        entry = [u["name_vi"] for u in unlocks if u["realm"] == realm["id"] and u["stage"] == 0]
        if entry:
            w(f"Vừa độ kiếp lên {realm['name_vi']} là mở khoá: **{', '.join(entry)}**.\n")
        for stage in range(1, realm["stages"] + 1):
            here = [n for n in t.main_nodes(realm["id"]) if n.stage == stage]
            got = [u["name_vi"] for u in unlocks if u["realm"] == realm["id"] and u["stage"] == stage]
            head = f"### {realm['name_vi']} tầng {stage}"
            if got:
                head += f" — mở khoá: {', '.join(got)}"
            w(head + "\n")
            w("| # | Nút | Loại | Nhánh | Học gì | Cần xong trước | Ôn lại | Câu hỏi |")
            w("|---|---|---|---|---|---|---|---|")
            for i, n in enumerate(sorted(here, key=lambda n: t.path_rank[n.id]), 1):     # Chính đạo order
                what = ", ".join(names.get(s, s) for s in n.skills) or ", ".join(n.topics_vi)
                need = ", ".join(t.nodes[r].name_vi for r in n.requires) or "—"
                rev = ", ".join(t.nodes[r].name_vi for r in n.reinforces) or "—"
                w(f"| {i} | **{n.name_vi}** | {KIND_VI[n.kind]} | {branch[n.branch]['name_vi']} | {what} | {need} | {rev} "
                  f"| {CONTENT_VI[n.content]} |")
            w("")
        if realm["id"] == "luyen_khi":
            w("**Vì sao cần từng nút (Luyện Khí):**\n")
            for n in sorted(t.main_nodes("luyen_khi"), key=lambda n: t.path_rank[n.id]):
                w(f"- *{n.name_vi}* — {n.why_vi}")
            w("")

    w("## Bàng môn (tuỳ chọn, không chặn tu vi)\n")
    w("| Nút | Gồm | Vì sao để ngoài chính đạo |")
    w("|---|---|---|")
    for n in t.nodes.values():
        if not n.main:
            w(f"| {n.name_vi.replace('Bàng môn: ', '')} | {', '.join(names.get(s, s) for s in n.skills)} | {n.why_vi} |")
    w("")
    w("## Bị loại khỏi lộ trình\n")
    w(raw["cut"]["_comment"] + "\n")
    for s in raw["cut"]["skills"]:
        w(f"- {names.get(s, s)}")
    w("")
    w("## Tiên quyết được bỏ\n")
    for skill, wv in raw["waivers"].items():
        if skill.startswith("_"):
            continue
        dropped = ", ".join(names.get(d, d) for d in wv["drop"])
        w(f"- *{names.get(skill, skill)}* không còn cần *{dropped}*: {wv['why_vi']}")
    w("")
    w("## Tài liệu nên đọc kèm (chọn loại dễ hiểu nhất)\n")
    for b in raw["branches"]:
        w(f"- **{b['name_vi']}:** " + "; ".join(raw["sources"][b["id"]]))
    w("")

    w("# Thiên Địa Đồ — tu vi mở khoá gì\n")
    w("## Luật đánh quái mới\n")
    for line in plan["combat"]["rules_vi"]:
        w(f"- {line}")
    w("")
    w("## Mở khoá theo tu vi\n")
    w("| Tu vi | Mở khoá | Là gì |")
    w("|---|---|---|")
    rname = {r["id"]: r["name_vi"] for r in realms}
    for u in sorted(unlocks, key=lambda u: (t.realm_order[u["realm"]], u["stage"])):
        when = f"{rname[u['realm']]} tầng {u['stage']}" if u["stage"] else f"Vừa lên {rname[u['realm']]}"
        w(f"| {when} | **{u['name_vi']}** | {u['desc_vi']} |")
    w("")
    w("## Vùng đất, và binh khí riêng của từng vùng\n")
    wtype = {x["land"]: x for x in plan["weapon_types"] if x["land"] and not x.get("drop_only")}
    ky = {x["land"]: x for x in plan["weapon_types"] if x["land"] and x.get("drop_only")}
    w("| Vùng đất | Nhánh giáo trình | Binh khí | Kỳ binh (chỉ rơi từ tinh anh, trùm) | Mô tả |")
    w("|---|---|---|---|---|")
    for l in plan["lands"]:
        b = branch[l["branch"]]["name_vi"] if l["branch"] else "—"
        wt, kb = wtype.get(l["id"]), ky.get(l["id"])
        w(f"| **{l['name_vi']}** | {b} | {wt['name_vi'] if wt else '—'} | {kb['name_vi'] if kb else '—'} "
          f"| {l['desc_vi']} |")
    w("")
    for x in plan["weapon_types"]:
        wait = " *(chờ hình vẽ)*" if x.get("status") != "co" else ""
        w(f"- **{x['name_vi']}** ({branch[x['branch']]['name_vi']}){wait}: {x['why_vi']}")
    w("")
    w("Phẩm của binh khí, thấp đến cao: " + ", ".join(q["name_vi"] for q in plan["qualities"]) + ".")
    w("")
    w("## Binh khí rải trong thế giới\n")
    grade = {g["grade"]: g for g in plan["grades"]}
    quality = {q["id"]: q["name_vi"] for q in plan["qualities"]}
    lands = {l["id"]: l["name_vi"] for l in plan["lands"]}
    tname = {x["id"]: x["name_vi"] for x in plan["weapon_types"]}
    w("| Binh khí | Phẩm | Ở đâu | Yêu cầu tu vi | Yêu cầu giáo trình |")
    w("|---|---|---|---|---|")
    for p in plan["weapons_placed"]:
        kind, _, g = p["weapon"].rpartition("_")
        req = p["requires"]
        nodes = ", ".join(t.nodes[n].name_vi for n in req["nodes"])
        extra = f" (cần {next(u['name_vi'] for u in unlocks if u['id'] == p['needs'])})" if p.get("needs") else ""
        w(f"| {grade[int(g)]['prefix_vi']} {tname[kind]} | {quality[p['quality']]} | {lands[p['land']]}: {p['spot_vi']}{extra} "
          f"| {rname[req['realm']]} tầng {req['stage']} | {nodes} |")
    w("")
    w("## Linh thú\n")
    w(plan["beast_taming_vi"] + "\n")
    w("| Linh thú | Ở đâu | Từ tu vi | Phản Đòn để thu phục | Giúp gì |")
    w("|---|---|---|---|---|")
    for b in plan["beasts"]:
        req = b["requires"]
        w(f"| **{b['name_vi']}** | {lands[b['land']]}: {b['where_vi']} | {rname[req['realm']]} tầng {req['stage']} "
          f"| {b['parries_to_tame']} lần | {b['gift_vi']} |")
    w("")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--doc", action="store_true", help="write docs/GIAO_TRINH_CAY.md")
    args = ap.parse_args(argv)
    errs = mt.validate_all()
    if errs:
        print(f"check_tree: {len(errs)} problem(s)")
        for e in errs:
            print("  -", e)
        return 1
    t = mt.tree()
    print(f"check_tree: ok - {len(t.nodes)} nodes ({len(t.main_path())} on Chính đạo, in one order), "
          f"{len(mt.world_plan()['weapons_placed'])} weapons placed, {len(mt.world_plan()['beasts'])} beasts")
    if args.doc:
        DOC.write_text(build_doc(), "utf-8", newline="\n")
        print(f"wrote {DOC.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
