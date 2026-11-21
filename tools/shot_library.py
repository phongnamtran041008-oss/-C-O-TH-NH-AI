#!/usr/bin/env python3
"""Screenshots and checks every page of Tàng Thư Các, headless.

    python tools/shot_library.py <outdir> [doc_id ...]      # PNGs of every page, then the check
    python tools/shot_library.py --check [doc_id ...]       # only the check, no PNG
    python tools/shot_library.py <outdir> path/to/draft.md  # a file, even before it is valid

Each document is opened in the real reader (client/scenes/math_library.DocScene) with a
stand-in for the game that hands it the parsed document, so neither the server nor an
account is needed. Every page is laid out and drawn at window scale 3 (and checked again
at scale 2), with its self-check answers hidden and then shown, and the tool fails,
listing each page, when something leaves the content box, sits on top of something else,
is wider than its column, or a figure label leaves its figure or covers another label.

A page taller than the panel is saved as several PNGs, one per screen, as the player
scrolls: <doc_id>_p<page>.png, <doc_id>_p<page>_2.png, ...
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = Path(__file__).resolve().parents[1]
for p in (str(ROOT), str(ROOT / "server")):
    if p not in sys.path:
        sys.path.insert(0, p)

import pygame  # noqa: E402

from app.learning import math_library  # noqa: E402

BASE_W, BASE_H = 480, 270
SCALES = (3, 2)          # screenshots at the first, checks at all


class _Api:
    def __init__(self, docs: dict):
        self.docs = docs

    def get(self, path: str, ok, err=None) -> None:
        doc_id = path.rsplit("/", 1)[-1]
        if doc_id in self.docs:
            ok(self.docs[doc_id].view())
        elif err:
            err({"code": "no_doc"})


class _Game:
    """Just what DocScene asks of the game."""

    def __init__(self, docs: dict):
        self.api = _Api(docs)

    def guide_seen(self, key: str) -> None: ...
    def api_error(self, err) -> None: ...
    def pop(self, scene) -> None: ...
    def push(self, scene): return scene


def _ui(scale: int):
    from client.engine.display import Display
    from client.engine.text import Fonts
    from client.ui.kit import UI
    display = Display(scale, False, (BASE_W * scale, BASE_H * scale))
    fonts = Fonts()
    if fonts.missing:
        raise SystemExit("the game fonts are missing (client/assets/fonts)")
    return UI(display, fonts)


def _frame(ui, scene) -> None:
    ui.begin([], 1 / 60)
    ui.win.fill((40, 36, 30))
    scene.draw_ui(ui)
    ui.end()


def check_documents(doc_ids: list[str] | None = None, outdir: Path | None = None,
                    scales: tuple[int, ...] = SCALES) -> tuple[list[str], int]:
    """(problems, pages checked). Problems are one line each: '<doc> page <n> x<scale>: ...'."""
    pygame.init()
    from client.scenes.math_library import DocScene
    docs = dict(math_library.documents())
    problems: list[str] = []
    ids = []
    for d in doc_ids or list(docs):
        if d.endswith(".md"):                 # a draft: shown even if it is not valid yet
            doc, bad = math_library.parse_document(Path(d).read_text("utf-8"), Path(d).name)
            problems += [f"{Path(d).name}: {p}" for p in bad]
            if doc is None:
                continue
            docs[doc.id] = doc
            d = doc.id
        ids.append(d)
    unknown = [d for d in ids if d not in docs]
    problems += [f"{d}: no such document (or it does not parse: run tools/check_all.py)" for d in unknown]
    ids = [d for d in ids if d in docs]
    game = _Game(docs)
    pages = 0
    if outdir is not None:
        outdir.mkdir(parents=True, exist_ok=True)
    for scale in scales:
        ui = _ui(scale)
        for doc_id in ids:
            if scale == scales[0] and outdir is not None:      # no stale screens from an older run
                for old in outdir.glob(f"{doc_id}_p*.png"):
                    old.unlink()
            scene = DocScene(game, doc_id)
            for page in range(len(scene.pages)):
                scene.revealed = set()
                scene.go_page(page)
                where = f"{doc_id} page {page + 1} x{scale}"
                for state in ("hidden", "shown"):
                    if state == "shown":
                        scene.revealed = {n for n in range(*scene.pages[page])
                                          if scene.doc["blocks"][n]["type"] == "check"}
                        if not scene.revealed:
                            break
                    scene.built_for = None
                    _frame(ui, scene)         # also proves that drawing raises nothing
                    problems += [f"{where}{' (answers shown)' if state == 'shown' else ''}: {p}"
                                 for p in scene.layout_problems(ui)]
                    if scale == scales[0] and outdir is not None and state == "hidden":
                        _save_screens(ui, scene, outdir / f"{doc_id}_p{page + 1}")
                if scale == scales[0]:
                    pages += 1
    return problems, pages


def _save_screens(ui, scene, stem: Path) -> None:
    _, _, _, ch = scene.content_box()
    shot, n = 0.0, 1
    while True:
        scene.scroll = scene.clamp(shot)
        _frame(ui, scene)
        pygame.image.save(ui.win, str(stem) + ("" if n == 1 else f"_{n}") + ".png")
        if scene.at_bottom() or n >= 8:
            break
        shot += ch - 24
        n += 1
    scene.scroll = 0.0


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    args = [a for a in argv if a != "--check"]
    outdir = None
    if not check_only:
        if not args:
            print(__doc__)
            return 2
        outdir = Path(args.pop(0))
    problems, pages = check_documents(args or None, outdir)
    for p in problems:
        print(" -", p)
    where = f", screenshots in {outdir}" if outdir else ""
    print(f"{pages} pages checked at scales {', '.join(map(str, SCALES))}: "
          f"{len(problems)} problems{where}")
    return 1 if problems else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
