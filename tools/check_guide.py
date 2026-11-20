#!/usr/bin/env python3
"""Check the Lộ Trình Tu Tiên content (server/data/guide.json):

    python tools/check_guide.py         # exit 1 and one line per problem

It runs the server's own validator (app/systems/guide.py `validate`): the shape of every
chapter, step and handbook page; the text-length limits the board lays out; ids unique among
chapters and steps (generated `<chapter>_s<k>` ones included); only known check types with
their parameters, GOTO ids, seen keys the client sends and handbook pages that exist;
reward item ids that exist in the catalog; one stage reward per stage of the realm on
Đạo Thụ; no Hanzi. Then every `_vi` string must be drawable by the game's fonts, the same
rule as the font check of tools/check_all.py (which also runs this validator).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))

FONT_DIR = ROOT / "client" / "assets" / "fonts"
CJK_START = 0x2E80


def _vi_strings(node, where: str = "") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{where}.{key}" if where else str(key)
            if str(key).endswith("_vi"):
                out += [(here, t) for t in _strings(value)]
            else:
                out += _vi_strings(value, here)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            out += _vi_strings(value, f"{where}[{i}]")
    return out


def _strings(node) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, (list, tuple)):
        return [t for v in node for t in _strings(v)]
    if isinstance(node, dict):
        return [t for v in node.values() for t in _strings(v)]
    return []


def check_fonts(raw: dict) -> list[str]:
    try:
        from fontTools.ttLib import TTFont
    except ImportError as e:
        return [f"cannot read the fonts: {e} (pip install -r server/requirements-dev.txt)"]
    fonts = []
    for name in ("VT323-Regular.ttf", "NotoSansSC-Game.otf"):
        if not (FONT_DIR / name).is_file():
            return [f"client/assets/fonts/{name} is missing (run python tools/fetch_assets.py)"]
        fonts.append(set(TTFont(FONT_DIR / name, fontNumber=0, lazy=True).getBestCmap()))
    pixel, han = fonts
    out, seen = [], set()
    for where, text in _vi_strings(raw):
        for ch in text:
            code = ord(ch)
            if ch in seen or ch.isspace() or (code < CJK_START and code in pixel) or code in han:
                continue
            seen.add(ch)
            out.append(f"{where}: no font draws {ch!r} (U+{code:04X}), the game would show a box")
    return out


def check() -> list[str]:
    try:
        from app.systems import guide
    except Exception as e:      # noqa: BLE001 - an import problem is a finding, not a crash
        return [f"cannot load app/systems/guide.py: {type(e).__name__}: {e}"]
    try:
        raw = json.loads(guide.FILE.read_text("utf-8"))
    except (OSError, ValueError) as e:
        return [f"{guide.FILE.name} cannot be read: {e}"]
    try:
        out = guide.validate(raw)
    except Exception as e:      # noqa: BLE001 - a malformed file must fail the check, not crash it
        return [f"validate() raised {type(e).__name__}: {e}"]
    return out + check_fonts(raw)


def main() -> int:
    problems = check()
    for p in problems:
        print(f"- {p}")
    print(f"guide.json: {len(problems)} problem(s)" if problems else "guide.json: OK")
    return 1 if problems else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
