"""Lộ Trình: the roadmap board, the "Việc tiếp theo" box on the HUD and Trúc Lão's welcome.

The server (GET /guide, see systems/guide.py) derives every step from what the player has
already done, so nothing here decides whether a step is finished: this module only turns the
view into something to draw and sends two kinds of messages, "seen" facts and claims.

  * `GuideScene`     - the modal board, two tabs. "Lộ trình": the chapters on the left (and a
                       small "Đang học" box), the steps of the selected chapter on the right
                       with the detail of the selected step under them. "Cẩm nang": the
                       handbook topics. Opens on the step that is current (F1 or the HUD box).
  * `draw_tracker`   - the small box on the HUD that names the next step; one click opens the board.
  * `hud_update`     - called every frame by the two HUD scenes: the first time a player is
                       on the HUD, Trúc Lão speaks, then the board opens.
  * `resume_refresh` - the HUD scenes call it when a panel closed, so a step the player just
                       finished is noticed (the "Xong" toast) without waiting.

WELCOME is a switch: with it off (the tests that were written for the old word-game tutorial)
nothing here starts by itself. The pure helpers take plain dicts, so the unit tests need no
server and no window."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..ui.dialog import DialogScene
from ..ui.mathdraw import fit
from .base import Scene
from .math_tree import draw_chips, fit_lines, main_head, main_label, main_progress, main_step_line

WELCOME = True                      # False: no welcome dialog, no automatic board (tests)

INK = "#2B2B2B"
GREY = "#5A5A5A"
PALE = "#8E877A"
GOLD_TEXT = "#B8862E"               # gold that stays readable on paper
GREEN = "#6A994E"
BONUS = "@bonus"                    # the key of the chapter bonus row (a step id never has an "@")
MAIN = "@main"                      # the first entry of the board: Chính đạo, the main quest
GOTO_IDS = ("math", "library", "dungeon", "td", "fortune", "char")
TRACKER_W, TRACKER_H = 142, 35     # narrow enough to stay clear of a "Xong: ..." toast in the world


# ------------------------------------------------------------------ pure helpers
def find_chapter(view: dict | None, chapter_id: str | None) -> dict | None:
    return next((c for c in (view or {}).get("chapters", []) if c["id"] == chapter_id), None)


def list_items(ch: dict) -> list[str]:
    """The rows of a chapter: its steps in order, then the chapter bonus when it has one."""
    keys = [s["id"] for s in ch["steps"]]
    return keys + [BONUS] if ch.get("rewards_vi") else keys


def chapter_claimable(ch: dict) -> bool:
    """Something inside the chapter waits to be claimed (a step, or the chapter bonus)."""
    return ch["state"] == "done" or any(s["state"] == "done" for s in ch["steps"])


def chapter_pick(ch: dict, current: dict | None) -> str:
    """The row selected when a chapter is opened: the current step, else the first required
    step still to do, a step waiting to be claimed, the bonus, an optional step, the first step."""
    if current and current.get("chapter_id") == ch["id"]:
        return current["step_id"]
    steps = ch["steps"]
    for pred in (lambda s: s["state"] == "active" and not s["optional"], lambda s: s["state"] == "done"):
        hit = next((s for s in steps if pred(s)), None)
        if hit:
            return hit["id"]
    if ch["state"] == "done" and ch.get("rewards_vi"):
        return BONUS
    hit = next((s for s in steps if s["state"] == "active"), None)
    return (hit or steps[0])["id"] if steps else BONUS


def default_selection(view: dict) -> tuple[str, str]:
    """(chapter id, row key) the board opens on: Chính đạo once it leads; else the current step;
    with none, the first chapter that still has something to do or to claim, else the first one."""
    if leads_with_main(view):
        return MAIN, MAIN
    cur = view.get("current")
    chapters = view["chapters"]
    if cur and find_chapter(view, cur["chapter_id"]):
        return cur["chapter_id"], cur["step_id"]
    ch = next((c for c in chapters if c["state"] != "claimed" or chapter_claimable(c)), chapters[0])
    return ch["id"], chapter_pick(ch, None)


def row_parts(step: dict) -> tuple[str, str, str]:
    """(title, tag, mark) of a step row: "n/c" while active, "Nhận" when done, "Xong" once claimed."""
    mark = {"done": T.GUIDE_MARK_CLAIM, "claimed": T.GUIDE_MARK_DONE}.get(step["state"],
                                                                         f"{step['progress']}/{step['count']}")
    return step["title_vi"], (T.GUIDE_OPTIONAL if step.get("optional") else ""), mark


def bonus_mark(ch: dict) -> str:
    return {"done": T.GUIDE_MARK_CLAIM, "claimed": T.GUIDE_MARK_DONE}.get(ch["state"], f"{ch['done']}/{ch['total']}")


def remaining_line(step: dict) -> str:
    """"Còn: A, B, C": the nodes of a generated step's stage that are not done (vacant ones are
    skipped: the server counts them as done); "" for any other step or when none is left."""
    names = [n["name_vi"] for n in step.get("nodes") or [] if n["state"] not in ("done", "vacant")]
    return T.GUIDE_REMAINING.format(names=", ".join(names)) if names else ""


def detail_of(ch: dict, key: str) -> dict | None:
    """What the detail area shows for a row: title, desc, how[], progress, count, rewards_vi,
    state, remaining, claim (the id to POST, or None while there is nothing to claim), goto, help."""
    if key == BONUS:
        return {"title": T.GUIDE_BONUS_ROW, "desc": T.GUIDE_BONUS_DESC, "how": [], "progress": ch["done"],
                "count": ch["total"], "rewards_vi": ch.get("rewards_vi") or [], "state": ch["state"],
                "remaining": "", "claim": ch["id"] if ch["state"] == "done" else None, "goto": None, "help": None}
    s = next((x for x in ch["steps"] if x["id"] == key), None)
    if s is None:
        return None
    return {"title": s["title_vi"], "desc": s["desc_vi"], "how": list(s["how_vi"]), "progress": s["progress"],
            "count": s["count"], "rewards_vi": s["rewards_vi"], "state": s["state"], "remaining": remaining_line(s),
            "claim": s["id"] if s["state"] == "done" else None,
            "goto": s["goto"] if s.get("goto") in GOTO_IDS else None, "help": s.get("help")}


def newly_done(old: dict | None, new: dict | None) -> list[str]:
    """Titles of the steps that went from active to done between two views (never on a first load)."""
    if not old or not new:
        return []
    before = {s["id"]: s["state"] for c in old["chapters"] for s in c["steps"]}
    return [s["title_vi"] for c in new["chapters"] for s in c["steps"]
            if s["state"] == "done" and before.get(s["id"]) == "active"]


def stage_line(stage: dict | None) -> str:
    if not stage:
        return ""
    return T.GUIDE_STAGE.format(realm=stage.get("realm_name_vi", ""), n=stage.get("stage") or 0,
                                t=stage.get("stages", "?"))


def leads_with_main(view: dict | None) -> bool:
    """Chính đạo leads the HUD box and the board once the welcome steps are done (server `lead`)."""
    m = (view or {}).get("main")
    return bool((view or {}).get("lead") == "main" and isinstance(m, dict) and m.get("step"))


def tracker_model(view: dict) -> dict:
    """What the HUD box says: header, title, "n/c" (only when c > 1), hint, and `body` - the text
    shown in place of title and hint when no step is current (the study line, or all done).
    Once Chính đạo leads: header "Chính đạo 2/5 · F1", the node's name as title, the step as hint
    ("Luyện · Cổng 1/4") and `claim` ("Nhận 2") when rewards wait on the board."""
    n = view.get("claimable") or 0
    if leads_with_main(view):
        m = view["main"]
        claim = T.GUIDE_HUD_MAIN_CLAIM.format(n=n) if n else ""
        if m["step"] == "done":
            return {"header": T.GUIDE_HUD_MAIN_DONE, "title": "", "count": "", "hint": "",
                    "body": T.PATH_DONE_TITLE, "claim": claim, "main": True}
        return {"header": T.GUIDE_HUD_MAIN.format(i=m.get("index") or 0, t=m.get("total") or 0),
                "title": m.get("name_vi") or "", "count": "", "hint": main_step_line(m), "body": "",
                "claim": claim, "main": True}
    cur, study = view.get("current"), view.get("study")
    if n > 0:
        header = T.GUIDE_HUD_CLAIM.format(n=n)
    else:
        header = T.GUIDE_HUD_NEXT if cur or not study else T.GUIDE_HUD_STUDY
    if cur:
        count = f"{cur['progress']}/{cur['count']}" if cur.get("count", 1) > 1 else ""
        return {"header": header, "title": cur["title_vi"], "count": count, "hint": cur.get("hint_vi") or "",
                "body": "", "claim": "", "main": False}
    return {"header": header, "title": "", "count": "", "hint": "",
            "body": study["text_vi"] if study else T.GUIDE_HUD_ALL_DONE, "claim": "", "main": False}


def main_detail(view: dict) -> dict | None:
    """What the board shows for the Chính đạo entry: the same step as the hub card."""
    m = (view or {}).get("main")
    if not isinstance(m, dict) or not m.get("step"):
        return None
    if m["step"] == "done":
        return {"title": T.PATH_DONE_TITLE, "head": T.GUIDE_MAIN_SUB, "why": T.PATH_DONE_BODY, "step": "",
                "hint": "", "stage": "", "goto": False}
    stage = T.GUIDE_MAIN_STAGE.format(realm=m.get("realm_name_vi") or "", n=m.get("stage") or 0,
                                      i=m.get("index") or 0, t=m.get("total") or 0, d=m.get("path_done") or 0,
                                      a=m.get("path_total") or 0)
    return {"title": m.get("name_vi") or "", "head": main_head(m), "why": m.get("why_vi") or "",
            "step": main_label(m), "hint": T.PATH_HINT.get(m["step"], ""), "progress": main_progress(m),
            "stage": stage, "goto": True}


# ------------------------------------------------------------------ HUD pieces
def hint_size(ui, text: str, width: float) -> float:
    """The hint line of the HUD box: 7, or 6 when that is what keeps it whole."""
    return 7 if ui.text_size(text, 7)[0] <= width else 6


def draw_hint(ui, lines: list[str], x: float, y: float, width: float, colour) -> None:
    """The hint of the HUD box: one line at 7 or 6, or two lines at 6 (the box grew for them)."""
    if not lines:
        return
    if len(lines) == 1:
        hs = hint_size(ui, lines[0], width)
        ui.text(fit(ui, lines[0], hs, width), x, y, hs, colour)
        return
    ui.text("\n".join(lines), x, y, 6, colour, line_gap=1.0)


def draw_tracker(ui, game, x: float, y: float, enabled: bool) -> int:
    """The "Việc tiếp theo" box at (x, y), TRACKER_W wide; one button, widget id `hud_guide`.
    Returns its height (0 while the guide has not arrived: nothing is drawn)."""
    view = game.state.guide
    if view is None:
        return 0
    m = tracker_model(view)
    w, h = TRACKER_W, TRACKER_H
    title = None
    top = 12                                # where the title starts (one more pixel over two lines:
    if m.get("main") and m["title"]:        # the marks of its first line would touch the header)
        size, lines = fit_lines(ui, m["title"], w - 8, sizes=(8, 7), lines=2)
        title = (size, lines)
        if len(lines) > 1:
            h += ui.text_size("Ag", size)[1] + 1
            top = 13
    hint_lines = [m["hint"]] if m["hint"] else []
    if hint_lines and ui.text_size(m["hint"], 6)[0] > w - 8:     # a long hint: two lines, never cut
        hint_lines = ui.f.wrap(m["hint"], 6, int((w - 8) * ui.s), ui.s)[:2]
        h += ui.text_size("Ag", 6)[1]
    # not ui.button: a ghost button that is disabled would still paint itself grey
    ui.widgets["hud_guide"] = ui.rect(x, y, w, h)
    hov = enabled and ui.hover(x, y, w, h)
    ui.fill(x, y, w, h, (244, 235, 217, 235))
    ui.border(x, y, w, h, "#8B5A2B")
    if m.get("main"):                       # Chính đạo leads: a gold edge, like the hub card
        ui.fill(x, y, 2, h, UICOL["gold"])
    if hov:
        ui.fill(x, y, w, h, (255, 255, 255, 70))
        ui.hot = "hud_guide"
    ui.text(m["header"], x + 4, y + 3, 7, GOLD_TEXT)
    if m.get("claim"):
        ui.text(m["claim"], x + w - 4, y + 3, 7, GREEN, anchor="topright")
    if title is not None:
        size, lines = title
        lh = ui.text_size("Ag", size)[1]
        ui.text("\n".join(lines), x + 4, y + top, size, INK, line_gap=1.0)
        draw_hint(ui, hint_lines, x + 4, y + top + lh * len(lines) + 1, w - 8, "#A33B2B")
    elif m["body"]:
        lines = ui.f.wrap(m["body"], 7, int((w - 8) * ui.s), ui.s)[:2]
        if len(lines) == 2 and len(ui.f.wrap(m["body"], 7, int((w - 8) * ui.s), ui.s)) > 2:
            lines[1] = fit(ui, lines[1] + "...", 7, w - 8)
        ui.text("\n".join(lines), x + 4, y + 14, 7, INK)
    else:
        room = w - 8 - (ui.text_size(m["count"], 8)[0] + 4 if m["count"] else 0)
        ui.text(fit(ui, m["title"], 8, room), x + 4, y + 12, 8, INK)
        if m["count"]:
            ui.text(m["count"], x + w - 4, y + 12, 8, GREEN, anchor="topright")
        draw_hint(ui, hint_lines, x + 4, y + 23, w - 8, GREY)
    if enabled and ui.click_in(x, y, w, h):
        if ui.sfx:
            ui.sfx("click")
        game.open_guide()
    return h


def hud_update(game, scene) -> None:
    """Called each frame by the abode and the world: the first time the player is on the HUD
    and has not met Trúc Lão, he speaks (WELCOME on), then the board opens."""
    st = game.state
    view = st.guide
    if not WELCOME or st.guide_welcome or view is None or view["welcome"]["seen"]:
        return
    if game.top is not scene or getattr(scene, "realm", None) is not None:
        return
    st.guide_welcome = True
    w = view["welcome"]
    game.push(DialogScene(game, w["lines_vi"], speaker=w["speaker_vi"], on_done=lambda: _welcome_done(game, scene)))


def _welcome_done(game, scene) -> None:
    """The welcome replaces the old word-game tutorial, which must never start for this player."""
    game.guide_seen("welcome")
    if game.state.me.get("tutorial_step", 0) < 5:
        game.state.me["tutorial_step"] = 5
        game.api.post("/tutorial", {"step": 5}, lambda r: None, lambda e: None)
    if hasattr(scene, "tutorial_step"):
        scene.tutorial_step = 5
    game.open_guide()


def resume_refresh(game, gap: float = 2.0) -> None:
    """A panel closed over a HUD scene: look at the guide again, at most once per `gap` seconds."""
    game.refresh_guide(min_gap=gap)


# ------------------------------------------------------------------ the board
class GuideScene(Scene):
    """The board. The view is always read from `game.state.guide`, so a claim, a refresh or a
    "seen" answer shows at once. Keys: F1 or Esc close, Up / Down move the selected step, the
    wheel scrolls (the steps, or the text of a handbook page)."""

    PANEL = (20, 6, 440, 258)
    LEFT_W = 118                    # the chapters and the "Đang học" box
    CH_ROW = 24
    ROW = 13                        # a step row
    ROWS = 5                        # rows of the step list
    TOPIC_ROW = 13

    def __init__(self, game, tab: str = "road", topic: str | None = None):
        super().__init__(game)
        self.tab = tab
        self.ch_id: str | None = None
        self.sel: str | None = None
        self.picked = False         # the player chose a chapter: Chính đạo no longer takes the selection
        self.first = 0              # the first step row shown
        self.show_sel = True        # scroll the list so the selected row is visible
        self.topic = topic
        self.tfirst = 0             # the first line of the handbook page shown
        self.lfirst = 0             # the first topic shown
        self.show_topic = True
        self.busy = False
        self.cache: tuple | None = None
        self.lines: list[tuple[str, float]] = []

    def on_enter(self):
        self.game.guide_seen("board")

    # ------------------------------------------------------------ actions
    def select_chapter(self, ch: dict) -> None:
        self.picked = True
        self.ch_id, self.first, self.show_sel = ch["id"], 0, True
        self.sel = chapter_pick(ch, (self.game.state.guide or {}).get("current"))

    def go_help(self, topic: str) -> None:
        self.tab, self.topic, self.tfirst, self.show_topic = "book", topic, 0, True

    def go_to(self, where: str) -> None:
        """Close the board and open the panel the step is about."""
        g = self.game
        self.close()
        if where == MAIN:                   # Chính đạo: the hub, doing what its card's button does
            from .math_practice import MathPracticeScene
            g.guide_seen("math_hub")
            g.push(MathPracticeScene(g, act=True))
        elif where == "math":
            g.open_math()
        elif where == "char":
            g.open_char()
        elif where == "library":
            from .math_library import LibraryListScene
            g.push(LibraryListScene(g, None))
        else:
            from .math_dungeon import MathDungeonScene
            from .math_fortune import MathFortuneScene
            from .math_td import MathTdScene
            g.push({"dungeon": MathDungeonScene, "td": MathTdScene, "fortune": MathFortuneScene}[where](g))

    def claim(self, claim_id: str, rewards_vi: list[str]) -> None:
        self.busy = True

        def ok(r):
            self.busy = False
            rw = r.get("rewards") or {}
            me = self.game.state.me
            for k in ("spirit_stones", "immortal_jade"):
                if k in rw:
                    me[k] = rw[k]
            self.game.set_guide(r.get("guide"))
            self.game.toast(T.GUIDE_CLAIMED.format(r=", ".join(rewards_vi)) if rewards_vi else T.GUIDE_MARK_DONE,
                            "#6A994E")
            self.game.audio.play("coin")
            self.game.on_xp(rw.get("xp"))
            self.game.refresh_me()
            self.game.refresh_cult()
            self.game.refresh_inv()

        def err(e):
            self.busy = False
            self.game.api_error(e)
        self.api.post("/guide/claim", {"id": claim_id}, ok, err)

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        if ui.key(pygame.K_F1):
            self.close()
            return
        ui.dim()
        x, y, w, h = self.PANEL
        view = self.game.state.guide
        ui.panel(x, y, w, h, (view or {}).get("title_vi") or T.GUIDE_TITLE)
        for i, (k, label) in enumerate((("road", T.GUIDE_TAB_ROAD), ("book", T.GUIDE_TAB_BOOK))):
            if ui.button(f"guide_tab_{k}", x + 10 + i * 84, y + 8, 80, 13, label, size=7, selected=self.tab == k):
                self.tab = k
        if view is None:
            ui.text(T.GUIDE_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        else:
            if view.get("claimable"):
                ui.text(T.GUIDE_CLAIMABLE.format(n=view["claimable"]), x + w - 12, y + 10, 7, GOLD_TEXT,
                        anchor="topright")
            if self.tab == "road":
                self.draw_road(ui, view, x, y, w, h)
            else:
                self.draw_book(ui, view, x, y, w, h)
        if ui.button("guide_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    # -------- the road tab
    def draw_road(self, ui, view, x, y, w, h) -> None:
        chapters = view["chapters"]
        if not chapters:
            return
        has_main = main_detail(view) is not None
        if self.ch_id == MAIN and not has_main:
            self.ch_id = None
        if not self.picked and leads_with_main(view) and self.ch_id != MAIN:
            self.ch_id, self.sel = MAIN, MAIN   # (Chính đạo began to lead while the board was open)
        if self.ch_id != MAIN and find_chapter(view, self.ch_id) is None:
            self.ch_id, self.sel = default_selection(view)
            self.show_sel = True
        shown = 4 if has_main else 5
        self.draw_chapters(ui, view, x + 10, y + 25, has_main, shown)
        rows = len(chapters[:shown]) + (1 if has_main else 0)
        self.draw_study(ui, view, x + 10, y + 25 + rows * (self.CH_ROW + 2) + 3, y + h - 25)
        rx, rw = x + self.LEFT_W + 16, w - self.LEFT_W - 26
        if self.ch_id == MAIN:
            self.draw_main(ui, view, x, y, w, h, rx, rw)
            return
        ch = find_chapter(view, self.ch_id)
        if self.sel not in list_items(ch):
            self.sel = chapter_pick(ch, view.get("current"))
        items = list_items(ch)
        self.draw_steps(ui, view, ch, items, rx, y + 25, rw)
        ui.fill(rx, y + 25 + self.ROW * self.ROWS + 2, rw, 1, "#D8CBAE")
        detail = detail_of(ch, self.sel)
        if detail:
            self.draw_detail(ui, detail, rx, y + 25 + self.ROW * self.ROWS + 6, rw, y + h - 24)
            bx = x + 12
            by = y + h - 20
            if detail["claim"] and ui.button("guide_claim", bx, by, 84, 14, T.GUIDE_CLAIM, style="gold",
                                             enabled=not self.busy):
                self.claim(detail["claim"], detail["rewards_vi"])
            if detail["claim"]:
                bx += 90
            if detail["goto"] and ui.button("guide_goto", bx, by, 60, 14, T.GUIDE_GOTO, size=7):
                self.go_to(detail["goto"])
                return
            if detail["goto"]:
                bx += 66
            if detail["help"] and ui.button("guide_help", bx, by, 60, 14, T.GUIDE_HELP, size=7):
                self.go_help(detail["help"])

    def draw_main(self, ui, view, x, y, w, h, rx, rw) -> None:
        """The Chính đạo entry: the same one step as the hub card, and "Đi tới" doing what the
        card's button does (the lesson, the sitting, the trial or the exercises)."""
        d = main_detail(view)
        m = view["main"]
        cy = y + 25
        ui.text(T.GUIDE_MAIN_SUB, rx, cy, 7, GOLD_TEXT)
        cy += 10
        size, lines = fit_lines(ui, d["title"], rw, sizes=(10, 9, 8), lines=2)
        ui.text("\n".join(lines), rx, cy, size, INK, line_gap=1.0)
        cy += ui.text_size("Ag", size)[1] * len(lines) + 2
        if d["goto"]:
            ui.text(d["head"], rx, cy, 7, UICOL["accent"])
            cy += 11
        cy = ui.text(d["why"], rx, cy, 8, INK, max_w=rw).bottom + 5
        if d["goto"]:
            end = draw_chips(ui, rx, cy, m)
            if d["progress"]:
                ui.text(d["progress"], end, cy + 6.5, 7, GREY, anchor="midleft")
            cy += 18
            ui.text("-", rx + 1, cy, 7, GREY)
            cy = ui.text(T.GUIDE_MAIN_STEP.format(step=d["step"], hint=d["hint"]), rx + 7, cy, 7, GREY,
                         max_w=rw - 7).bottom + 3
            ui.text(fit(ui, d["stage"], 7, rw), rx, cy, 7, GREEN)
            self.draw_main_nodes(ui, m, rx, cy + 12, rw, y + h - 26)
        bx, by = x + 12, y + h - 20
        if d["goto"] and ui.button("guide_goto", bx, by, 60, 14, T.GUIDE_GOTO, size=7, style="primary",
                                   key=pygame.K_RETURN):
            self.go_to(MAIN)
            return
        if ui.button("guide_help", bx + 66, by, 60, 14, T.GUIDE_HELP, size=7):
            self.go_help("chinh_dao")

    @staticmethod
    def draw_main_nodes(ui, m, x, y, w, bottom) -> None:
        """The stage's main nodes in path order under the Chính đạo entry: done, now, later."""
        nodes = m.get("stage_nodes") or []
        if not nodes or bottom - y < 10:
            return
        cols = 1 if (bottom - y) / len(nodes) >= 10 else 2
        per = -(-len(nodes) // cols)
        pitch = min(10.0, (bottom - y) / per)
        colw = w / cols
        for i, n in enumerate(nodes):
            c, r = divmod(i, per)
            rx, ry = x + c * colw, y + r * pitch
            col = {"done": GREEN, "now": INK}.get(n["state"], PALE)
            ui.fill(rx, ry + pitch / 2 - 2, 4, 4, {"done": GREEN, "now": UICOL["gold"]}.get(n["state"], "#CFC6B4"))
            size, lines = fit_lines(ui, f"{i + 1}. {n['name_vi']}", colw - 12, sizes=(7, 6, 5), lines=1)
            ui.text(lines[0], rx + 7, ry + pitch / 2, size, col, anchor="midleft")
            if lines[0].endswith("...") and ui.hover(rx, ry, colw, pitch):
                ui.set_tooltip(n["name_vi"])        # a name cut in two columns: whole on hover

    def draw_chapters(self, ui, view, x, y, has_main: bool = False, shown: int = 5) -> None:
        if has_main:                        # Chính đạo first: the main quest
            sel = self.ch_id == MAIN
            if ui.button("guide_ch_main", x, y, self.LEFT_W, self.CH_ROW, "", style="ghost", selected=sel,
                         tooltip=T.GUIDE_MAIN_INTRO):
                self.ch_id, self.sel = MAIN, MAIN
            if not sel:
                ui.fill(x, y, self.LEFT_W, self.CH_ROW, "#FBF0C8")
                ui.border(x, y, self.LEFT_W, self.CH_ROW, UICOL["gold"])
            ui.fill(x, y, 3, self.CH_ROW, UICOL["gold"])
            m = view["main"]
            ui.text(T.GUIDE_MAIN_CHAPTER, x + 6, y + 2, 8, "#FFFFFF" if sel else INK)
            sub = main_step_line(m) if m["step"] != "done" else T.GUIDE_MARK_DONE
            ui.text(fit(ui, sub, 7, self.LEFT_W - 10), x + 6, y + 14, 7, "#E3D5BA" if sel else GREY)
            y += self.CH_ROW + 2
        for i, ch in enumerate(view["chapters"][:shown]):
            ry = y + i * (self.CH_ROW + 2)
            sel = ch["id"] == self.ch_id
            if ui.button(f"guide_ch_{ch['id']}", x, ry, self.LEFT_W, self.CH_ROW, "", style="ghost", selected=sel,
                         tooltip=ch["intro_vi"]):
                self.select_chapter(ch)
            fg = "#FFFFFF" if sel else (PALE if ch["state"] == "claimed" else INK)
            if not sel:
                ui.border(x, ry, self.LEFT_W, self.CH_ROW, "#C9B48A")
            ui.text(fit(ui, ch["title_vi"], 8, self.LEFT_W - 22), x + 5, ry + 3, 8, fg)
            frac = ch["done"] / ch["total"] if ch["total"] else 1.0
            ui.progress(x + 5, ry + 15, 66, 4, frac, GREEN, back="#6B6358" if sel else "#CFC6B4")
            ui.text(f"{ch['done']}/{ch['total']}", x + 76, ry + 13, 7, "#E3D5BA" if sel else GREY)
            if chapter_claimable(ch):        # a gold mark: something inside waits to be claimed
                ui.fill(x + self.LEFT_W - 12, ry + 4, 7, 7, UICOL["gold"])
                ui.border(x + self.LEFT_W - 12, ry + 4, 7, 7, INK)
            elif ch["state"] == "claimed":
                ui.text(T.GUIDE_MARK_DONE, x + self.LEFT_W - 5, ry + 3, 6, "#B5D67A" if sel else GREEN,
                        anchor="topright")

    def draw_study(self, ui, view, x, y, bottom) -> None:
        """"Đang học": the node to study now, and where the player stands on the tree."""
        w = self.LEFT_W
        if bottom - y < 24:
            return
        ui.fill(x, y, w, bottom - y, "#EDE4D2")
        ui.border(x, y, w, bottom - y, "#C9B48A")
        ui.text(T.GUIDE_STUDYING, x + 5, y + 3, 7, GOLD_TEXT)
        study = view.get("study")
        m = view.get("main")
        if isinstance(m, dict) and m.get("node_id"):        # Chính đạo: the node and its step
            text = T.GUIDE_STUDY_MAIN.format(name=m["name_vi"], step=main_step_line(m))
        else:
            text = study["text_vi"] if study else T.GUIDE_STUDY_NONE
        line_h = ui.text_size("Ag", 7)[1] * 1.15
        room = int((bottom - y - 26) // line_h)
        lines = ui.f.wrap(text, 7, int((w - 10) * ui.s), ui.s)
        if len(lines) > room:
            lines = lines[:max(1, room)]
            lines[-1] = fit(ui, lines[-1] + "...", 7, w - 10)
        ui.text("\n".join(lines), x + 5, y + 13, 7, INK)
        st = stage_line(view.get("stage"))
        if st:
            ui.text(fit(ui, st, 7, w - 10), x + 5, bottom - 11, 7, GREEN)

    def draw_steps(self, ui, view, ch, items, x, y, w) -> None:
        """The scrolling list of the chapter's rows."""
        most = max(0, len(items) - self.ROWS)
        if self.show_sel and self.sel in items:
            i = items.index(self.sel)
            self.first = min(max(self.first, i - self.ROWS + 1), i)
            self.show_sel = False
        if ui.hover(x, y, w, self.ROW * self.ROWS) and ui.inp.wheel:
            self.first -= ui.inp.wheel
            ui.inp.wheel = 0
        if self.sel in items:
            move = (1 if ui.key(pygame.K_DOWN) else 0) - (1 if ui.key(pygame.K_UP) else 0)
            if move:
                self.sel = items[max(0, min(len(items) - 1, items.index(self.sel) + move))]
                self.show_sel = True
        self.first = max(0, min(self.first, most))
        cur = view.get("current") or {}
        rw = w - (6 if most else 0)
        for n, key in enumerate(items[self.first:self.first + self.ROWS]):
            ry = y + n * self.ROW
            if key == BONUS:
                self.draw_row(ui, f"guide_bonus_{ch['id']}", x, ry, rw, key == self.sel, T.GUIDE_BONUS_ROW, "",
                              bonus_mark(ch), ch["state"], False)
                continue
            s = next(s for s in ch["steps"] if s["id"] == key)
            title, tag, mark = row_parts(s)
            self.draw_row(ui, f"guide_step_{key}", x, ry, rw, key == self.sel, title, tag, mark, s["state"],
                          cur.get("step_id") == key)
        if most:
            ui.fill(x + w - 3, y, 3, self.ROW * self.ROWS, "#DCD2BC")
            frac = self.ROWS / len(items)
            ui.fill(x + w - 3, y + self.ROW * self.ROWS * (1 - frac) * self.first / most, 3,
                    max(8.0, self.ROW * self.ROWS * frac), UICOL["accent"])

    def draw_row(self, ui, wid, x, y, w, sel, title, tag, mark, state, current) -> None:
        h = self.ROW - 1
        ui.fill(x, y, w, h, "#FBF0C8" if current else ("#F3E3B0" if state == "done" else
                                                       "#EDE4D2" if state == "claimed" else "#FFFDF7"))
        if ui.button(wid, x, y, w, h, "", style="ghost", selected=sel):
            self.sel = wid.split("_", 2)[2] if not wid.startswith("guide_bonus_") else BONUS
            self.show_sel = True
        if current and not sel:
            ui.border(x, y, w, h, UICOL["gold"])
        ui.fill(x, y, 3, h, UICOL["gold"] if current or state == "done" else "#C9B48A")
        dim = state == "claimed"
        fg = "#FFFFFF" if sel else (PALE if dim else INK)
        mark_col = {"done": "#B5D67A" if sel else GREEN, "claimed": "#B8AE9C" if sel else PALE}.get(
            state, "#E3D5BA" if sel else GREY)
        mw = ui.text_size(mark, 8)[0]
        ui.text(mark, x + w - 4, y + h / 2, 8, mark_col, anchor="midright")
        room = w - 12 - mw - 8
        if tag:
            tw = ui.text_size(tag, 6)[0]
            ui.text(tag, x + w - 4 - mw - 5, y + h / 2, 6, "#C9C0AE" if sel else PALE, anchor="midright")
            room -= tw + 4
        ui.text(fit(ui, title, 8, room), x + 8, y + h / 2, 8, fg, anchor="midleft")

    def draw_detail(self, ui, d, x, y, w, bottom) -> None:
        """The selected row: title and state, what and why, how, progress, reward, what is left."""
        state = T.GUIDE_STATE.get(d["state"], "")
        sw = ui.text_size(state, 7)[0]
        ui.text(fit(ui, d["title"], 9, w - sw - 8), x, y, 9, INK)
        ui.text(state, x + w, y + 2, 7, GREEN if d["state"] != "active" else GREY, anchor="topright")
        y += 14                                     # (a size-9 title with marks is 13 tall)
        y = ui.text(d["desc"], x, y, 8, INK, max_w=w).bottom + 3
        for line in d["how"]:
            ui.text("-", x + 1, y, 7, GREY)
            y = ui.text(line, x + 7, y, 7, GREY, max_w=w - 7).bottom + 1
        y += 2
        pw = 150
        ui.progress(x, y + 1, pw, 6, d["progress"] / d["count"] if d["count"] else 1.0,
                    UICOL["gold"] if d["state"] != "active" else UICOL["blue"], back="#CFC6B4")
        ui.text(f"{d['progress']}/{d['count']}", x + pw + 5, y, 7, INK)
        y += 11
        if d["rewards_vi"]:
            y = ui.text(T.GUIDE_REWARDS.format(r=", ".join(d["rewards_vi"])), x, y, 7, GOLD_TEXT, max_w=w).bottom + 2
        if d["remaining"]:
            lh = ui.text_size("Ag", 7)[1] * 1.15
            lines = ui.f.wrap(d["remaining"], 7, int(w * ui.s), ui.s)
            room = max(1, int((bottom - y) // lh))
            if len(lines) > room:
                lines = lines[:room]
                lines[-1] = fit(ui, lines[-1] + "...", 7, w)
            ui.text("\n".join(lines), x, y, 7, INK)

    # -------- the handbook tab
    def draw_book(self, ui, view, x, y, w, h) -> None:
        topics = view.get("handbook") or []
        if not topics:
            return
        if self.topic not in [t["id"] for t in topics]:
            self.topic = topics[0]["id"]
        lw = self.LEFT_W + 8
        top, bottom = y + 25, y + h - 24
        shown = int((bottom - top) // self.TOPIC_ROW)
        most = max(0, len(topics) - shown)
        if self.show_topic:
            i = [t["id"] for t in topics].index(self.topic)
            self.lfirst = min(max(self.lfirst, i - shown + 1), i)
            self.show_topic = False
        if ui.hover(x + 10, top, lw, bottom - top) and ui.inp.wheel:
            self.lfirst -= ui.inp.wheel
            ui.inp.wheel = 0
        self.lfirst = max(0, min(self.lfirst, most))
        for n, t in enumerate(topics[self.lfirst:self.lfirst + shown]):
            ry = top + n * self.TOPIC_ROW
            if ui.button(f"guide_topic_{t['id']}", x + 10, ry, lw, self.TOPIC_ROW - 1, "", style="ghost",
                         selected=t["id"] == self.topic):
                self.topic, self.tfirst = t["id"], 0
            ui.text(fit(ui, t["title_vi"], 8, lw - 10), x + 15, ry + (self.TOPIC_ROW - 1) / 2, 8,
                    "#FFFFFF" if t["id"] == self.topic else INK, anchor="midleft")
        topic = next(t for t in topics if t["id"] == self.topic)
        rx, rw = x + lw + 20, w - lw - 40
        ui.text(fit(ui, topic["title_vi"], 10, rw), rx, top, 10, UICOL["accent"])
        ui.fill(rx, top + 13, rw, 1, "#D8CBAE")
        if self.cache != (ui.s, topic["id"]):
            self.cache = (ui.s, topic["id"])
            self.lines = [(ln, 3.0 if j == 0 and k else 0.0) for k, line in enumerate(topic["lines_vi"])
                          for j, ln in enumerate(ui.f.wrap(line, 8, int(rw * ui.s), ui.s))]
        lh = ui.text_size("Ag", 8)[1] * 1.15
        area = bottom - (top + 17)
        # the last first-line from which everything still fits
        acc, last = 0.0, len(self.lines)
        while last > 0 and acc + lh + self.lines[last - 1][1] <= area:
            acc += lh + self.lines[last - 1][1]
            last -= 1
        if ui.hover(rx, top, rw, bottom - top) and ui.inp.wheel:
            self.tfirst -= ui.inp.wheel
            ui.inp.wheel = 0
        self.tfirst = max(0, min(self.tfirst + (1 if ui.key(pygame.K_DOWN) else 0) -
                                 (1 if ui.key(pygame.K_UP) else 0), last))
        cy = top + 17
        n_shown = 0
        for ln, gap in self.lines[self.tfirst:]:
            if cy + gap + lh > bottom + 0.5:
                break
            cy += gap
            ui.text(ln, rx, cy, 8, INK)
            cy += lh
            n_shown += 1
        if last > 0:
            frac = n_shown / len(self.lines)
            ui.fill(x + w - 9, top + 17, 3, area, "#DCD2BC")
            ui.fill(x + w - 9, top + 17 + area * (1 - frac) * self.tfirst / max(1, last), 3, max(8.0, area * frac),
                    UICOL["accent"])
