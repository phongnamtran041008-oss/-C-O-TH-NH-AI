"""Đạo Thụ in the math hub: the rows the hub lists and the card of one node.

The server (GET /math/tree) decides what is open, done or locked; nothing here repeats a rule.
This module only turns that answer into something to draw:

  * `tab_list`    - "Chính đạo" and one tab per branch that has nodes in the player's realm;
  * `main_step`, `main_label`, `main_chips`, `later_ids` ... - Chính đạo, the main quest: the one
                    next step the server names (GET /math/tree `main`) as the hub card draws it;
  * `node_rows`   - one row per part of a node (a node with no part, e.g. a vacant one, has one),
                    sorted by stage, optional nodes after the main path;
  * `row_state`, `locked_reason`, `row_label`, `stage_text` ... - what a row says;
  * `NodeCardScene` - the node's why, what it needs, what it reviews, what it teaches, its
                    exercises and the recommended source, with a button that opens the source in
                    the system browser (only when the player presses it) and, for a node with
                    exercises, one that opens them in the code scene.

The pure helpers take plain dicts, so the unit tests need no server and no window."""
from __future__ import annotations

import webbrowser
from dataclasses import dataclass
from urllib.parse import urlparse

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..ui.mathdraw import fit
from .base import Scene
from .math_code import ProblemListScene
from .math_library import line_h, scroll_rows

GREY = "#5A5A5A"
INK = "#2B2B2B"
PALE = "#9A9387"
NEXT_TAB = "next"                   # the id of the first tab, "Chính đạo"
LAST_STAGE = 99                     # sort key of a node without a stage (an optional one)


# ------------------------------------------------------------------ tabs and rows (pure)
def tab_list(tree: dict) -> list[dict]:
    """"Chính đạo" first, then one tab per branch that has a node in the realm the player is in,
    in the order the server lists the branches. `name_vi` is the short label of the tab;
    `subject` is the math subject of the branch (None for code, practice and projects)."""
    realm = (tree.get("stage") or {}).get("realm")
    have = {n["branch"] for n in tree.get("nodes", []) if n["realm"] == realm}
    tabs = [{"id": NEXT_TAB, "name_vi": T.TREE_TAB_NEXT, "subject": None}]
    for b in tree.get("branches", []):
        if b["id"] in have:
            tabs.append({"id": b["id"], "name_vi": T.TREE_TAB_SHORT.get(b["id"], b["name_vi"]),
                         "subject": b.get("subject")})
    return tabs


def first_tab(tree: dict) -> str:
    """"Chính đạo", unless a sitting was left open on a node that is not the current step of
    Chính đạo: then the tab of that node's branch, where its "Luyện tiếp" is."""
    run = tree.get("run") or {}
    m = main_step(tree)
    if m is not None and run.get("node_id") == m.get("node_id"):
        return NEXT_TAB
    node = next((n for n in tree.get("nodes", []) if n["id"] == run.get("node_id")), None)
    if node is not None and any(t["id"] == node["branch"] for t in tab_list(tree)):
        return node["branch"]
    return NEXT_TAB


@dataclass(frozen=True)
class Row:
    """One line of the list: a part of a node, or the whole node when it has no part."""
    node: dict
    part: dict | None
    index: int            # 1-based position among the node's parts
    count: int            # how many parts the node has
    first: bool           # the first row of its node


def node_sort_key(node: dict, position: int) -> tuple:
    """Main-path nodes by stage, then the optional ones; ties keep the order the server gave."""
    stage = node["stage"] if node.get("stage") is not None else LAST_STAGE
    return node["status"] != "chinh", stage, position


def rows_of(node: dict) -> list[Row]:
    parts = node.get("parts") or []
    if not parts:
        return [Row(node, None, 1, 1, True)]
    return [Row(node, p, i, len(parts), i == 1) for i, p in enumerate(parts, 1)]


def node_rows(tree: dict, tab_id: str) -> list[Row]:
    """The rows of a tab. "Nên học": the open main-path nodes in the order of `next`.
    A branch: its nodes of the player's realm by stage, optional ones last."""
    nodes = tree.get("nodes", [])
    if tab_id == NEXT_TAB:
        by_id = {n["id"]: n for n in nodes}
        chosen = [by_id[i] for i in tree.get("next", []) if i in by_id]
    else:
        realm = (tree.get("stage") or {}).get("realm")
        pos = {n["id"]: i for i, n in enumerate(nodes)}
        chosen = sorted((n for n in nodes if n["branch"] == tab_id and n["realm"] == realm),
                        key=lambda n: node_sort_key(n, pos[n["id"]]))
    return [r for n in chosen for r in rows_of(n)]


def node_by_id(tree: dict | None, node_id: str | None) -> dict | None:
    return next((n for n in (tree or {}).get("nodes", []) if n["id"] == node_id), None)


def names_of(tree: dict | None, ids: list[str]) -> list[str]:
    """The names of nodes, from the tree view; an id the tree does not know is left out."""
    return [n["name_vi"] for i in ids for n in [node_by_id(tree, i)] if n is not None]


# ------------------------------------------------------------------ Chính đạo, the main quest (pure)
STEPS = ("hoc", "luyen", "kiep", "code")


def main_step(tree: dict | None) -> dict | None:
    """The one next step on Chính đạo (GET /math/tree `main`), None from an older server."""
    m = (tree or {}).get("main")
    return m if isinstance(m, dict) and m.get("step") else None


def main_label(m: dict) -> str:
    """The label of the one primary button: Học bài, Luyện (Luyện tiếp), Độ Thiên kiếp nhỏ, Làm bài tập."""
    step = m["step"]
    if step == "luyen" and m.get("resume") == "practice":
        return T.PATH_RESUME["luyen"]
    if step == "kiep" and m.get("resume") == "trial":
        return T.PATH_RESUME["kiep"]
    return T.PATH_GO.get(step, "")


def main_head(m: dict) -> str:
    return T.PATH_HEAD.format(realm=m.get("realm_name_vi") or "", n=m.get("stage") or 0, i=m.get("index") or 0,
                              t=m.get("total") or 0)


def main_chips(m: dict) -> list[tuple[str, str]]:
    """(label, state) of the chips Hiểu -> Luyện -> Vượt cổng; state is done | now | later. A node of
    exercises only has one chip, its exercises."""
    if m["step"] == "code":
        return [(T.PATH_CHIP_CODE.format(d=m.get("problems_done", 0), t=m.get("problems_total", 0)), "now")]
    done = m.get("done") or {}
    out, now_given = [], False
    for key, label in zip(("hieu", "luyen", "kiep"), T.PATH_CHIPS):
        if done.get(key):
            out.append((label, "done"))
        elif not now_given:
            out.append((label, "now"))
            now_given = True
        else:
            out.append((label, "later"))
    return out


def main_progress(m: dict) -> str:
    """What is left inside the step: "Cổng 1/4" while practising, "Phần 1/2" of a two-part node."""
    bits = []
    part = m.get("part") or {}
    if part.get("count", 1) > 1:
        bits.append(T.PATH_PART.format(i=part["index"], n=part["count"]))
    gate = m.get("gate") or {}
    if m["step"] in ("luyen", "kiep") and gate.get("total"):
        bits.append(T.PATH_GATE.format(d=gate["done"], t=gate["total"]))
    return " · ".join(bits)


def main_step_line(m: dict) -> str:
    """One line for the HUD box: "Luyện · Cổng 1/4", "Học bài", "Làm bài tập 2/5"."""
    if m["step"] == "code":
        return f"{T.PATH_STEP_SHORT['code']} {m.get('problems_done', 0)}/{m.get('problems_total', 0)}"
    more = main_progress(m)
    return T.PATH_STEP_SHORT.get(m["step"], "") + (f" · {more}" if more else "")


def later_ids(tree: dict | None) -> set[str]:
    """Main-path nodes ahead of the current step on Chính đạo and not done yet: they carry the
    small "Để sau" mark in the branch tabs (they are not blocked)."""
    m = main_step(tree)
    if m is None:
        return set()
    here = m.get("path")
    out = set()
    for n in (tree or {}).get("nodes", []):
        if n.get("path") is None or n["state"] in ("done", "vacant"):
            continue
        if here is None or n["path"] > here:
            out.add(n["id"])
    return out if m["step"] != "done" else set()


def draw_chips(ui, x: float, y: float, m: dict) -> float:
    """The chips Hiểu > Luyện > Vượt cổng at (x, y), 13 high: done green, now gold, later pale.
    Returns the x after the last one."""
    for i, (label, state) in enumerate(main_chips(m)):
        tw = ui.text_size(label, 7)[0] + 10
        if i:
            ui.text(">", x - 5, y + 6.5, 7, GREY, anchor="center")
        fill, fg = {"done": (UICOL["green"], "#FFFFFF"), "now": ("#F6DFA0", INK)}.get(state, ("#EDE6D6", PALE))
        ui.fill(x, y, tw, 13, fill)
        ui.border(x, y, tw, 13, "#B8862E" if state == "now" else "#C9B48A")
        ui.text(label, x + tw / 2, y + 6.5, 7, fg, anchor="center")
        x += tw + 9
    return x


def fit_lines(ui, text: str, width: float, sizes=(8, 7, 6), lines: int = 2,
              height: float | None = None) -> tuple[float, list[str]]:
    """The largest size of `sizes` at which `text` fits in `lines` lines of `width`, and its lines -
    so a long name is shown whole on two lines or a size smaller, never cut with "...". Only when
    even the smallest size needs more lines is the last one cut. `height`: the room of a row -
    several lines are taken only at a size where they fit in it (two lines of 8 in a 16 px row
    would run into the next row)."""
    for size in sizes:
        if ui.text_size(text, size)[0] <= width:
            return size, [text]
    for size in sizes:
        got = ui.f.wrap(text, size, int(width * ui.s), ui.s)
        if len(got) <= lines and (height is None or len(got) * ui.text_size("Ag", size)[1] <= height + 0.5):
            return size, got
    size = sizes[-1]
    got = ui.f.wrap(text, size, int(width * ui.s), ui.s)[:lines]
    got[-1] = fit(ui, got[-1] + "...", size, width)
    return size, got


def header_text(stage: dict) -> str:
    """Where the player stands: "Luyện Khí tầng 2/9"."""
    if not stage.get("stage"):
        return T.TREE_STAGE_NONE.format(realm=stage.get("realm_name_vi", ""))
    return T.TREE_STAGE.format(realm=stage.get("realm_name_vi", ""), n=stage["stage"], t=stage.get("stages", "?"))


def progress_text(ui, stage: dict, room: float) -> str:
    """How far the player is inside the stage they are working on: "đã xong 1/4 nút của tầng 3",
    the shorter form when that does not fit in `room`, "" when there is nothing to say (the
    realm's last stage is reached, or an older server sent no progress)."""
    p = stage.get("progress")
    if not p:
        return ""
    for template in (T.TREE_STAGE_PROGRESS, T.TREE_STAGE_PROGRESS_SHORT):
        text = template.format(d=p["done"], t=p["total"], n=p["stage"])
        if ui.text_size(text, 7)[0] <= room:
            return text
    return ""


def stage_text(node: dict) -> str:
    return T.TREE_ROW_STAGE.format(n=node["stage"]) if node.get("stage") is not None else T.TREE_OPTIONAL


def locked_reason(node: dict) -> str:
    """What a locked node wants first: the first node it requires that is not done yet."""
    todo = next((r for r in node.get("requires", []) if not r["done"]), None)
    return T.TREE_NEEDS.format(name=todo["name_vi"]) if todo else T.MATH_LOCKED


def row_state(row: Row) -> str:
    """"vacant" | "locked" | "code" (a node of exercises only) | "part"."""
    state = row.node["state"]
    if state == "vacant":
        return "vacant"
    if state == "locked":
        return "locked"
    return "part" if row.part is not None else "code"


def part_playable(row: Row) -> bool:
    """A part may be practised when its node is open or done, or the part itself is passed."""
    return row.part is not None and (row.node["state"] in ("open", "done") or bool(row.part["passed"]))


def row_label(ui, row: Row, width: float) -> str:
    """The node's name, cut to `width`; a node with two parts keeps its "(1/2)" tail visible."""
    tail = " " + T.TREE_PART.format(i=row.index, n=row.count) if row.count > 1 else ""
    room = width - (ui.text_size(tail, 8)[0] if tail else 0)
    return fit(ui, row.node["name_vi"], 8, room) + tail


def break_long(ui, text: str, size: float, width: float) -> list[str]:
    """A word that is wider than the line (a URL) cut into pieces that fit."""
    out, cur = [], ""
    for ch in text:
        if cur and ui.text_size(cur + ch, size)[0] > width:
            out.append(cur)
            cur = ""
        cur += ch
    return out + [cur] if cur else out


# ------------------------------------------------------------------ the card of a node
def card_blocks(node: dict, name_of) -> list[tuple[str, str]]:
    """What the card says, as (kind, text): "h" a heading, "t" a paragraph, "b" a bullet,
    "u" a line that may be wider than the card (a URL). `name_of(id)` gives a node's name."""
    out: list[tuple[str, str]] = []
    if node.get("why_vi"):
        out.append(("t", node["why_vi"]))
    if node.get("chieu"):                # Chiêu Thức II: what finishing this node helps to open
        out.append(("h", T.NODE_OPENS_CHIEU))
        out += [("b", T.NODE_CHIEU_ITEM.format(name=c["name_vi"], el=T.ELEMENT_VI.get(c.get("element"), "")))
                for c in node["chieu"]]
    out.append(("h", T.NODE_SOURCE))
    src = node.get("source")
    if not src:
        out.append(("t", T.NODE_SRC_NONE))
    else:
        out.append(("t", src["title"]))
        if src.get("author"):
            out.append(("t", T.NODE_SRC_AUTHOR.format(a=src["author"])))
        if src.get("where"):
            out.append(("t", T.NODE_SRC_WHERE.format(w=src["where"])))
        out.append(("t", T.NODE_SRC_LANG.format(lang=T.NODE_LANG.get(src.get("lang"), src.get("lang") or "?"),
                                                kind=T.NODE_KIND.get(src.get("kind"), src.get("kind") or "?"))))
        if src.get("url"):
            out.append(("u", T.NODE_SRC_URL.format(u=src["url"])))
    out.append(("h", T.NODE_REQUIRES))
    if not node.get("requires"):
        out.append(("t", T.NODE_NO_REQUIRES))
    for r in node.get("requires", []):
        out.append(("b", f"{r['name_vi']} - {T.NODE_REQ_DONE if r['done'] else T.NODE_REQ_TODO}"))
    if node.get("reinforces"):
        out.append(("h", T.NODE_REINFORCES))
        out += [("b", name_of(i)) for i in node["reinforces"]]
    topics = list(node.get("topics_vi") or [])
    if not topics:
        topics = [k["name_vi"] for p in node.get("parts", []) for k in p.get("skills", [])]
    if topics:
        out.append(("h", T.NODE_TOPICS))
        out += [("b", t) for t in topics]
    if node.get("problems"):
        out.append(("h", T.NODE_PROBLEMS))
        out += [("b", f"{p['title_vi']} - {T.NODE_PROBLEM_SOLVED if p['solved'] else T.NODE_PROBLEM_TODO}")
                for p in node["problems"]]
    return out


def exercises_open(node: dict) -> bool:
    """The "Làm bài" button works when the node lists exercises and is not locked (R10: an
    exercise is open when its node is open or done)."""
    return bool(node.get("problems")) and node["state"] in ("open", "done")


def exercises_subject(node: dict) -> str | None:
    """The subject whose exercise list holds the node's exercises."""
    return next((p["subject_id"] for p in node.get("problems", []) if p.get("subject_id")), None)


def safe_url(url: str | None) -> bool:
    """Only a plain web address is ever handed to the system browser."""
    if not url:
        return False
    p = urlparse(url)
    return p.scheme in ("http", "https") and bool(p.netloc)


def open_in_browser(url: str) -> bool:
    """Opens `url` in the system browser; False when it was refused or the system could not."""
    if not safe_url(url):
        return False
    try:
        return bool(webbrowser.open(url))
    except Exception:           # (a missing browser must never take the game down)
        return False


class NodeCardScene(Scene):
    """A small card for one node of Đạo Thụ. The text scrolls (wheel, Up / Down); the button
    that opens the recommended reading in the browser is the only way a URL is ever opened."""

    PANEL = (40, 16, 400, 238)
    TOP, BOTTOM = 46, 28            # the text starts this far below the panel top, stops above the buttons

    def __init__(self, game, node: dict, tree: dict | None = None):
        super().__init__(game)
        self.node = node
        self.tree = tree or {}
        self.first = 0                      # the first line shown
        self.built_for: tuple | None = None
        self.lines: list[tuple[str, str]] = []      # (kind, text) of each wrapped line

    def name_of(self, node_id: str) -> str:
        n = node_by_id(self.tree, node_id)
        return n["name_vi"] if n else node_id

    def build(self, ui, width: float) -> None:
        lines: list[tuple[str, str]] = []
        for kind, text in card_blocks(self.node, self.name_of):
            if kind == "u":
                pieces = break_long(ui, text, 8, width - 8)
                lines += [("t", p) for p in pieces]
            elif kind == "b":
                lines += [("b" if i == 0 else "c", s) for i, s in
                          enumerate(ui.f.wrap(text, 8, int((width - 12) * ui.s), ui.s))]
            else:
                lines += [("h" if kind == "h" else "t", s) for s in ui.f.wrap(text, 8, int(width * ui.s), ui.s)]
        self.lines = lines
        self.built_for = (ui.s, self.node["id"])

    def open_source(self) -> None:
        src = self.node.get("source") or {}
        if not open_in_browser(src.get("url")):
            self.game.toast(T.NODE_SRC_FAILED, "#BC4749")

    def open_exercises(self) -> None:
        """The node's exercises in the code scene (the same list the Đại Số card's "Bài tập" opens,
        cut down to this node's)."""
        subject = exercises_subject(self.node)
        if subject:
            self.game.push(ProblemListScene(self.game, subject, only=[p["id"] for p in self.node["problems"]]))

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = self.PANEL
        n = self.node
        node_problems = bool(n.get("problems"))
        ui.panel(x, y, w, h, T.NODE_CARD_TITLE)
        ui.text(fit(ui, n["name_vi"], 10, w - 32), x + 16, y + 19, 10, INK)
        tags = [T.NODE_STATE.get(n["state"], n["state"]), stage_text(n)]
        if n["status"] != "chinh":
            tags.append(T.NODE_OPTIONAL_TAG)
        ui.text(" · ".join(tags), x + 16, y + 33, 7, UICOL["accent"], max_w=w - 32)

        cx, cw = x + 16, w - 40
        if self.built_for != (ui.s, n["id"]):
            self.build(ui, cw)
        top, bottom = y + self.TOP, y + h - self.BOTTOM
        lh = line_h(ui, 8)
        shown = max(1, int((bottom - top) // lh))
        self.first = scroll_rows(ui, self.first, len(self.lines), shown, x, top, w, bottom - top)
        cy = top
        for kind, text in self.lines[self.first:self.first + shown]:
            if kind == "h":
                ui.text(text, cx, cy, 8, UICOL["accent"])
            elif kind == "b":
                ui.fill(cx + 3, cy + lh / 2 - 1, 3, 3, UICOL["accent"])
                ui.text(text, cx + 12, cy, 8, INK)
            elif kind == "c":
                ui.text(text, cx + 12, cy, 8, INK)
            else:
                ui.text(text, cx, cy, 8, INK)
            cy += lh
        if len(self.lines) > shown:
            hint_x = 162 if node_problems else 100          # (right of the "Làm bài" button, when there is one)
            ui.text(T.TREE_SCROLL_MORE.format(a=self.first + 1, b=min(len(self.lines), self.first + shown),
                                              t=len(self.lines)), x + hint_x, y + h - 13, 7, GREY, anchor="midleft",
                    max_w=w - hint_x - 70)
            frac = shown / len(self.lines)
            ui.fill(x + w - 9, top, 3, bottom - top, "#DCD2BC")
            ui.fill(x + w - 9, top + (bottom - top) * (1 - frac) * self.first / max(1, len(self.lines) - shown),
                    3, max(8.0, (bottom - top) * frac), UICOL["accent"])

        url = (n.get("source") or {}).get("url")
        if ui.button("math_src_open", x + 12, y + h - 20, 80, 14, T.NODE_SRC_OPEN, size=7, style="gold",
                     enabled=safe_url(url)):
            self.open_source()
        if node_problems and ui.button("math_info_code", x + 98, y + h - 20, 56, 14, T.NODE_DO_PROBLEMS,
                                       size=7, style="primary", enabled=exercises_open(n)):
            self.open_exercises()
        if ui.button("math_info_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()
