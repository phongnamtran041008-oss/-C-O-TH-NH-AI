"""Check the per-node learning sources (server/data/math/sources/<branch>.json) and build
docs/NGUON_HOC.md from them.

    python tools/check_sources.py                    # schema only
    python tools/check_sources.py --tree PATH        # + every node of the tree is covered
    python tools/check_sources.py --links            # + open every URL (slow, needs the network)
    python tools/check_sources.py --doc              # write docs/NGUON_HOC.md

The sources only name where to learn something: a title, where in it, a link, and one
sentence of our own on why. Nothing is copied from them (see CREDITS.md). The curriculum
tree itself (tree.json) belongs to another piece of work and is only read here, when given.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "server" / "data" / "math" / "sources"
DOC_PATH = ROOT / "docs" / "NGUON_HOC.md"
LINK_REPORT = SOURCES_DIR / "_links.json"

BRANCHES = ("ds", "gt", "xs", "tr", "lt", "ud", "ml", "dl", "ht", "nc")
MATH_BRANCHES = ("ds", "gt", "xs", "tr")
KINDS = {"video": "Video", "sach": "Sách", "khoa_hoc": "Khoá học", "bai_viet": "Bài viết",
         "tuong_tac": "Tương tác", "bai_tap": "Bài tập", "de_thi": "Đề thi", "code": "Code",
         "bai_bao": "Bài báo"}
LANGS = ("vi", "en")
FREQUENCIES = ("rất hay gặp", "hay gặp", "thỉnh thoảng")
PROJECT_KINDS = ("thuc_chien", "du_an")
MAX_SENTENCE = 260
# Places that host other people's books and exam papers without the right to: never link them.
BANNED_HOSTS = ("libgen", "z-lib", "zlibrary", "sci-hub", "scribd.com", "studocu", "123doc",
                "tailieu", "coursehero", "pdfdrive", "annas-archive", "vdoc.pub", "dokumen.pub",
                "epdf", "kupdf", "academia.edu")
_RESOURCE_KEYS = {"title", "author", "kind", "lang", "url", "where", "free", "minutes", "why_vi",
                  "checked", "license"}
_RESOURCE_NEEDED = {"title", "kind", "lang", "url", "free", "why_vi", "checked"}
_NODE_KEYS = {"primary", "also", "practice", "vi", "note_vi", "project"}
_FILE_KEYS = {"branch", "researched", "backbone", "nodes", "exam_proofs", "rejected"}
_VI_MARKS = set("ăâđêôơưáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ")


def _vietnamese(text: str) -> bool:
    """A Vietnamese sentence written without its diacritics is a mistake here."""
    return any(ch in _VI_MARKS for ch in text.lower())


def check_resource(res, here: str, errors: list[str]) -> None:
    if not isinstance(res, dict):
        errors.append(f"{here}: a resource must be an object")
        return
    for key in sorted(_RESOURCE_NEEDED - res.keys()):
        errors.append(f"{here}: missing '{key}'")
    for key in sorted(res.keys() - _RESOURCE_KEYS):
        errors.append(f"{here}: unknown key '{key}'")
    if res.get("kind") not in KINDS:
        errors.append(f"{here}: kind must be one of {', '.join(KINDS)}")
    if res.get("lang") not in LANGS:
        errors.append(f"{here}: lang must be vi or en")
    for key in ("free", "checked"):
        if key in res and not isinstance(res[key], bool):
            errors.append(f"{here}: '{key}' must be true or false")
    if res.get("minutes") is not None and not isinstance(res["minutes"], (int, float)):
        errors.append(f"{here}: minutes must be a number or null")
    url = res.get("url") or ""
    parsed = urlparse(url)
    if parsed.scheme not in ("https", "http") or "." not in parsed.netloc:
        errors.append(f"{here}: url must be a web link, got {url!r}")
    host = parsed.netloc.lower()
    for banned in BANNED_HOSTS:
        if banned in host:
            errors.append(f"{here}: {host} is not a legitimate source ({banned})")
    why = res.get("why_vi") or ""
    if not why.strip():
        errors.append(f"{here}: why_vi is empty")
    elif len(why) > MAX_SENTENCE:
        errors.append(f"{here}: why_vi is {len(why)} characters, at most {MAX_SENTENCE}")
    elif not _vietnamese(why):
        errors.append(f"{here}: why_vi is not Vietnamese with diacritics")
    if not (res.get("title") or "").strip():
        errors.append(f"{here}: title is empty")


def check_project(project, here: str, errors: list[str]) -> None:
    if not isinstance(project, dict):
        errors.append(f"{here}: project must be an object")
        return
    for key in ("datasets", "target_vi", "compute_vi"):
        if key not in project:
            errors.append(f"{here}: project is missing '{key}'")
    for i, ds in enumerate(project.get("datasets") or []):
        for key in ("name", "url", "license", "why_vi"):
            if not str(ds.get(key) or "").strip():
                errors.append(f"{here}: dataset {i} is missing '{key}'")
    for i, res in enumerate(project.get("reference_impl") or []):
        check_resource(res, f"{here} reference_impl[{i}]", errors)


def check_file(data, branch: str, errors: list[str]) -> None:
    here = f"{branch}.json"
    if not isinstance(data, dict):
        errors.append(f"{here}: must be an object")
        return
    for key in sorted(_FILE_KEYS - data.keys()):
        errors.append(f"{here}: missing '{key}'")
    if data.get("branch") != branch:
        errors.append(f"{here}: branch is {data.get('branch')!r}")
    for i, res in enumerate(data.get("backbone") or []):
        check_resource(res, f"{here} backbone[{i}]", errors)
    for node_id, node in (data.get("nodes") or {}).items():
        at = f"{here} {node_id}"
        if not isinstance(node, dict):
            errors.append(f"{at}: must be an object")
            continue
        for key in sorted(node.keys() - _NODE_KEYS):
            errors.append(f"{at}: unknown key '{key}'")
        if "primary" not in node:
            errors.append(f"{at}: no primary source")
        else:
            check_resource(node["primary"], f"{at} primary", errors)
        for group, most in (("also", 3), ("practice", 2), ("vi", 2)):
            items = node.get(group) or []
            if len(items) > most:
                errors.append(f"{at}: {group} has {len(items)} entries, at most {most}")
            for i, res in enumerate(items):
                check_resource(res, f"{at} {group}[{i}]", errors)
                if group == "vi" and isinstance(res, dict) and res.get("lang") != "vi":
                    errors.append(f"{at} vi[{i}]: is not a Vietnamese source")
        if "project" in node:
            check_project(node["project"], at, errors)
    proofs = data.get("exam_proofs") or []
    if branch not in MATH_BRANCHES and proofs:
        errors.append(f"{here}: only the math branches have exam_proofs")
    for i, proof in enumerate(proofs):
        at = f"{here} exam_proofs[{i}]"
        for key in ("node", "topic_vi", "type_vi", "frequency_vi", "sources"):
            if key not in proof:
                errors.append(f"{at}: missing '{key}'")
        if proof.get("frequency_vi") not in FREQUENCIES:
            errors.append(f"{at}: frequency_vi must be one of {', '.join(FREQUENCIES)}")
        if proof.get("node") not in (data.get("nodes") or {}):
            errors.append(f"{at}: node {proof.get('node')!r} is not a node of this branch")
        for j, res in enumerate(proof.get("sources") or []):
            check_resource(res, f"{at} sources[{j}]", errors)
    for i, item in enumerate(data.get("rejected") or []):
        if not (item.get("title") and item.get("why_vi")):
            errors.append(f"{here} rejected[{i}]: needs title and why_vi")


def check_against_tree(files: dict, tree: dict, errors: list[str]) -> None:
    by_branch: dict[str, list[dict]] = {}
    for node in tree["nodes"]:
        by_branch.setdefault(node["branch"], []).append(node)
    for branch in BRANCHES:
        have = set((files.get(branch) or {}).get("nodes") or {})
        want = {n["id"] for n in by_branch.get(branch, [])}
        for node_id in sorted(want - have):
            errors.append(f"{branch}.json: node {node_id} of the tree has no sources")
        for node_id in sorted(have - want):
            errors.append(f"{branch}.json: {node_id} is not a node of branch {branch}")
        for node in by_branch.get(branch, []):
            entry = (files.get(branch) or {}).get("nodes", {}).get(node["id"])
            if entry and node["kind"] in PROJECT_KINDS and "project" not in entry:
                errors.append(f"{branch}.json {node['id']}: a hands-on node needs a project")


def resources(data: dict):
    """Every resource of one file, with where it sits."""
    for i, res in enumerate(data.get("backbone") or []):
        yield f"backbone[{i}]", res
    for node_id, node in (data.get("nodes") or {}).items():
        if isinstance(node.get("primary"), dict):
            yield f"{node_id} primary", node["primary"]
        for group in ("also", "practice", "vi"):
            for i, res in enumerate(node.get(group) or []):
                yield f"{node_id} {group}[{i}]", res
        for i, res in enumerate((node.get("project") or {}).get("reference_impl") or []):
            yield f"{node_id} reference_impl[{i}]", res
    for i, proof in enumerate(data.get("exam_proofs") or []):
        for j, res in enumerate(proof.get("sources") or []):
            yield f"exam_proofs[{i}] sources[{j}]", res


def load_files() -> tuple[dict, list[str]]:
    files, errors = {}, []
    for branch in BRANCHES:
        path = SOURCES_DIR / f"{branch}.json"
        if not path.is_file():
            errors.append(f"{branch}.json: missing")
            continue
        try:
            files[branch] = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            errors.append(f"{branch}.json: not valid JSON ({exc})")
    return files, errors


# ------------------------------------------------------------------ links
def check_links(files: dict) -> dict:
    """Open every distinct URL once. Returns {url: status} where status is an HTTP code or
    an error name. 401/403/429 from a site that refuses robots is not proof the link is dead,
    so those are reported apart."""
    import asyncio

    import httpx

    urls = sorted({res.get("url") for data in files.values() for _, res in resources(data)
                   if isinstance(res, dict) and res.get("url")})
    for data in files.values():
        for node in (data.get("nodes") or {}).values():
            for ds in (node.get("project") or {}).get("datasets") or []:
                if ds.get("url") and ds["url"] not in urls:
                    urls.append(ds["url"])
    result: dict[str, object] = {}
    headers = {"User-Agent": "Mozilla/5.0 (link check)", "Accept": "text/html,*/*"}

    async def one(client, gate, url):
        async with gate:
            for attempt in range(2):
                try:
                    resp = await client.get(url)
                    result[url] = resp.status_code
                    return
                except httpx.HTTPError as exc:
                    result[url] = type(exc).__name__
                    await asyncio.sleep(1 + attempt)

    async def run():
        gate = asyncio.Semaphore(8)
        async with httpx.AsyncClient(follow_redirects=True, timeout=25, headers=headers) as client:
            await asyncio.gather(*(one(client, gate, url) for url in urls))

    asyncio.run(run())
    return result


def link_summary(result: dict) -> tuple[list[str], list[str]]:
    dead, blocked = [], []
    for url, status in sorted(result.items()):
        if status == 200:
            continue
        (blocked if status in (401, 403, 405, 429, 999) else dead).append(f"{status}  {url}")
    return dead, blocked


# ------------------------------------------------------------------ the document
def _line(res: dict, bad: set[str]) -> str:
    bits = [KINDS.get(res.get("kind"), "?"), "tiếng Việt" if res.get("lang") == "vi" else "tiếng Anh"]
    if not res.get("free"):
        bits.append("trả phí")
    if res.get("minutes"):
        minutes = int(res["minutes"])
        bits.append(f"{minutes} phút" if minutes < 120 else f"{round(minutes / 60)} giờ")
    if res.get("url") in bad:
        bits.append("**liên kết chưa mở được**")
    where = f" — {res['where']}" if res.get("where") else ""
    author = f", {res['author']}" if res.get("author") else ""
    return (f"[{res['title']}]({res['url']}){author}{where} ({', '.join(bits)}). "
            f"{res.get('why_vi', '')}")


def build_doc(files: dict, tree: dict | None, links: dict | None) -> str:
    bad = set()
    if links:
        dead, _ = link_summary(links)
        bad = {line.split("  ", 1)[1] for line in dead}
    names, order, branch_names = {}, {}, {}
    if tree:
        realm = {r["id"]: (r["order"], r["name_vi"]) for r in tree["realms"]}
        branch_names = {b["id"]: b["name_vi"] for b in tree["branches"]}
        for node in tree["nodes"]:
            r_order, r_name = realm.get(node.get("realm"), (99, "Bàng môn"))
            stage = node.get("stage")
            label = f"{r_name} tầng {stage}" if stage else r_name
            names[node["id"]] = (node["name_vi"], label)
            order[node["id"]] = (r_order, stage or 99)
    out = ["# Nguồn học tốt nhất cho từng nút của Đạo Thụ", "",
           "> File này do `python tools/check_sources.py --doc` dựng từ `server/data/math/sources/*.json`. "
           "Muốn đổi thì sửa các file dữ liệu ấy rồi chạy lại, đừng sửa ở đây.", "",
           "Mỗi nút có **một nguồn chính** (học từ đầu thì đọc/xem cái này), vài nguồn **xem thêm** cho một "
           "góc nhìn khác, chỗ **luyện tập** có đáp án, và nguồn **tiếng Việt** khi có nguồn thật sự tốt. "
           "Game chỉ dẫn tên và đường tới nguồn; không chép nội dung của nguồn nào.", ""]
    total = sum(1 for data in files.values() for _ in resources(data))
    out += [f"Tổng cộng {total} nguồn cho {sum(len(d.get('nodes') or {}) for d in files.values())} nút, "
            f"tra cứu ngày {max((d.get('researched') or '') for d in files.values())}.", ""]
    for branch in BRANCHES:
        data = files.get(branch)
        if not data:
            continue
        out += [f"## {branch_names.get(branch, branch)}", ""]
        if data.get("backbone"):
            out += ["**Xương sống của nhánh** (theo thứ tự nên dùng):", ""]
            out += [f"{i}. {_line(res, bad)}" for i, res in enumerate(data["backbone"], 1)]
            out.append("")
        node_ids = sorted(data.get("nodes") or {}, key=lambda n: order.get(n, (99, 99)))
        for node_id in node_ids:
            node = data["nodes"][node_id]
            title, label = names.get(node_id, (node_id, ""))
            out += [f"### {title}" + (f" · {label}" if label else ""), "", f"`{node_id}`", ""]
            if node.get("note_vi"):
                out += [f"*{node['note_vi']}*", ""]
            out.append(f"- **Chính:** {_line(node['primary'], bad)}")
            for group, label_vi in (("also", "Xem thêm"), ("practice", "Luyện tập"), ("vi", "Tiếng Việt")):
                for res in node.get(group) or []:
                    out.append(f"- **{label_vi}:** {_line(res, bad)}")
            project = node.get("project")
            if project:
                out += ["", "Thực chiến:", ""]
                for ds in project.get("datasets") or []:
                    size = f", {ds['size_mb']} MB" if ds.get("size_mb") is not None else ""
                    out.append(f"- Dữ liệu: [{ds['name']}]({ds['url']}) (giấy phép: {ds.get('license')}"
                               f"{size}). {ds.get('why_vi', '')}")
                for res in project.get("reference_impl") or []:
                    out.append(f"- Bản mẫu: {_line(res, bad)}")
                out.append(f"- Đích: {project.get('target_vi', '')}")
                out.append(f"- Chạy ở đâu: {project.get('compute_vi', '')}")
            out.append("")
        if data.get("exam_proofs"):
            out += [f"### Dạng tự luận hay gặp trong đề cuối kỳ — {branch_names.get(branch, branch)}", "",
                    "Các dạng này không nằm trên chính đạo; chúng là đề của Luận Đạo Đài "
                    "(`docs/LUAN_DAO_DAI.md`).", "",
                    "| Dạng | Thuộc nút | Hay gặp | Mô tả | Xem ở đâu |", "|---|---|---|---|---|"]
            for proof in data["exam_proofs"]:
                where = "; ".join(f"[{r['title']}]({r['url']})" for r in proof.get("sources") or []) or "—"
                node_name = names.get(proof["node"], (proof["node"], ""))[0]
                out.append(f"| **{proof['topic_vi']}** | {node_name} | {proof['frequency_vi']} | "
                           f"{proof['type_vi']} | {where} |")
            out.append("")
        if data.get("rejected"):
            out += ["**Đã xem và không chọn:**", ""]
            out += [f"- {item['title']}: {item['why_vi']}" for item in data["rejected"]]
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--tree", type=Path, help="tree.json to check node coverage against")
    parser.add_argument("--links", action="store_true", help="open every URL")
    parser.add_argument("--doc", action="store_true", help="write docs/NGUON_HOC.md")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    files, errors = load_files()
    for branch, data in files.items():
        check_file(data, branch, errors)
    tree = None
    if args.tree:
        tree = json.loads(args.tree.read_text(encoding="utf-8"))
        check_against_tree(files, tree, errors)
    links = None
    if args.links:
        links = check_links(files)
        LINK_REPORT.write_text(json.dumps(links, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                               encoding="utf-8")
    elif LINK_REPORT.is_file():
        links = json.loads(LINK_REPORT.read_text(encoding="utf-8"))
    if links:
        dead, blocked = link_summary(links)
        print(f"links: {len(links)} opened, {len(dead)} failed, {len(blocked)} refused the robot")
        for line in dead:
            print("  FAILED ", line)
        for line in blocked:
            print("  refused", line)
    count = sum(1 for data in files.values() for _ in resources(data))
    checked = sum(1 for data in files.values() for _, r in resources(data)
                  if isinstance(r, dict) and r.get("checked"))
    print(f"{len(files)} branch files, {sum(len(d.get('nodes') or {}) for d in files.values())} nodes, "
          f"{count} resources ({checked} marked checked by the researcher)")
    if args.doc and not errors:
        DOC_PATH.write_text(build_doc(files, tree, links), encoding="utf-8", newline="\n")
        print(f"wrote {DOC_PATH.relative_to(ROOT)}")
    for line in errors:
        print("ERROR", line)
    print("OK" if not errors else f"{len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
