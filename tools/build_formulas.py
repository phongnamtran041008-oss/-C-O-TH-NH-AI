#!/usr/bin/env python3
"""Build the formula pictures of Tàng Thư Các.

Every `$$ ... $$` of server/data/math/library/ becomes one PNG that ships with the game,
so a player never needs a formula renderer, a network connection or a maths font:

    python tools/build_formulas.py              # build what is missing or has changed
    python tools/build_formulas.py --force      # build every formula again
    python tools/build_formulas.py --prune      # also delete pictures no document uses
    python tools/build_formulas.py --check      # change nothing, only say what is missing

Pictures go to client/assets/formulas/<key>.png (the key comes from the formula itself,
so the same formula is never built twice) and their sizes to server/data/math/formulas.json,
which the server sends to the game with each document.

Needs Node once, for `tools/formulas` (MathJax + resvg):

    cd tools/formulas && npm install

tools/check_all.py only reads what this wrote, so the build and the checks need neither
Node nor the internet.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))

from app.learning import math_library  # noqa: E402

NODE_DIR = ROOT / "tools" / "formulas"
PNG_DIR = ROOT / "client" / "assets" / "formulas"
MANIFEST = ROOT / "server" / "data" / "math" / "formulas.json"
SUPERSAMPLE = 3          # the PNG is this many times the size the game draws it at
EX_IN_BASE = 4.5         # base units per ex: how big a formula looks next to the text


def wanted_formulas() -> dict[str, str]:
    """key -> TeX, for every formula in every document."""
    out: dict[str, str] = {}
    for doc in math_library.documents().values():
        for block in doc.formulas:
            out[block["key"]] = block["tex"]
    return out


def read_manifest() -> dict:
    if MANIFEST.is_file():
        return json.loads(MANIFEST.read_text("utf-8")).get("formulas", {})
    return {}


def write_manifest(formulas: dict) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "_comment": "Built by tools/build_formulas.py from the $$...$$ formulas of math/library/. "
                    "key -> the formula, its plain-text form and the size of its picture in the game's "
                    "base units (its screen is 480 x 270 of them). The picture itself is "
                    f"client/assets/formulas/<key>.png, {SUPERSAMPLE} times that size. Do not edit by hand.",
        "supersample": SUPERSAMPLE,
        "ex_in_base": EX_IN_BASE,
        "formulas": dict(sorted(formulas.items())),
    }
    MANIFEST.write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", "utf-8", newline="\n")


def node_ready() -> str | None:
    if not (NODE_DIR / "node_modules").is_dir():
        return f"{NODE_DIR.relative_to(ROOT)}/node_modules is missing: cd tools/formulas && npm install"
    if shutil.which("node") is None:
        return "node is not installed (https://nodejs.org)"
    return None


def render(jobs: list[dict]) -> tuple[list[dict], list[str]]:
    """Run the Node renderer on these formulas; returns (built, errors)."""
    if not jobs:
        return [], []
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        jobs_file = Path(tmp) / "jobs.json"
        jobs_file.write_text(json.dumps({"supersample": SUPERSAMPLE, "ex_in_base": EX_IN_BASE, "jobs": jobs}),
                             "utf-8")
        proc = subprocess.run(["node", str(NODE_DIR / "render.mjs"), str(jobs_file), str(PNG_DIR)],
                              capture_output=True, text=True, cwd=NODE_DIR, encoding="utf-8")
    if proc.returncode != 0:
        return [], [f"the renderer failed: {(proc.stderr or proc.stdout).strip()[:500]}"]
    try:
        out = json.loads(proc.stdout)
    except ValueError:
        return [], [f"the renderer printed something unexpected: {proc.stdout[:300]}"]
    return out["built"], out["errors"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="build every formula again")
    ap.add_argument("--prune", action="store_true", help="delete pictures no document uses")
    ap.add_argument("--check", action="store_true", help="change nothing, only report")
    args = ap.parse_args(argv)

    problems = math_library.validate_all()
    blocking = [p for p in problems if "no picture was built" not in p and "formulas.json" not in p]
    if blocking:
        print("The documents have problems; fix them first:")
        for p in blocking[:20]:
            print(" -", p)
        return 1

    wanted = wanted_formulas()
    manifest = read_manifest()
    stale = [k for k, tex in wanted.items()
             if args.force or manifest.get(k, {}).get("tex") != tex or not (PNG_DIR / f"{k}.png").is_file()]
    unused = sorted(set(manifest) - set(wanted))

    if args.check:
        for key in stale:
            print(f"needs building: {wanted[key]}")
        for key in unused:
            print(f"unused: {key}")
        print(f"{len(wanted)} formulas, {len(stale)} to build, {len(unused)} unused")
        return 1 if stale else 0

    if stale:
        why = node_ready()
        if why:
            print(f"{len(stale)} formulas need building but {why}")
            return 1
        built, errors = render([{"key": k, "tex": wanted[k]} for k in stale])
        for e in errors:
            print(" -", e)
        for entry in built:
            key = entry["key"]
            manifest[key] = {"tex": wanted[key], "alt": math_library.tex_to_ascii(wanted[key]),
                             "w": entry["w"], "h": entry["h"]}
            print(f"built {key}.png  {entry['px_w']}x{entry['px_h']}px  "
                  f"({entry['w']} x {entry['h']} base)  {wanted[key]}")
        if errors:
            write_manifest(manifest)
            return 1

    if args.prune:
        for key in unused:
            manifest.pop(key, None)
            (PNG_DIR / f"{key}.png").unlink(missing_ok=True)
            print(f"removed {key}")
        for png in sorted(PNG_DIR.glob("*.png")) if PNG_DIR.is_dir() else []:
            if png.stem not in wanted:
                png.unlink()
                print(f"removed {png.name}")
    elif unused:
        print(f"{len(unused)} pictures are no longer used (--prune removes them)")

    write_manifest(manifest)
    math_library.load_manifest.cache_clear()
    left = math_library.manifest_problems(assets_dir=PNG_DIR)
    for p in left:
        print(" -", p)
    print(f"{len(wanted)} formulas in {len(math_library.documents())} documents; "
          f"{len(stale)} built now; pictures in {PNG_DIR.relative_to(ROOT)}")
    return 1 if left else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
