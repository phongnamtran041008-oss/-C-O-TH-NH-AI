"""Thủ Thành Toán (M10, kế hoạch 4.3): the tower defense of the math edition, opened from the
"Thủ Thành" door of the math hub.

It is the board of the Ải Thủ Vườn (scenes/td.py, engine/td_sim.py) with towers instead of
plants. What changes is what a piece is and how it is earned:

  * every tower stands for an area of mathematics; the bar shows the ones the player may
    build, and the locked ones greyed with the reason (a floor not reached yet, a subject
    without questions);
  * clicking a cell with a tower chosen opens a math question of that tower's area (the
    math card of Động Phủ, MathQuizScene); the tower stands only after a right answer, and
    an upgrade works the same way. The board does not move while the card is open;
  * the log goes to /math/td/* and the server replays it before paying anything.
"""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..art.palette import rgb
from .base import Scene
from .math_practice import MathQuizScene
from .td import TdPlayScene, draw_stars, monster_frames, reward_text, stats_text

GREY = "#5A5A5A"


def role_hex(role: str) -> str:
    return T.TD_ROLE_COLORS.get(role, "#7D7468")


_TOWER: dict = {}


def tower_sprite(role: str, level: int) -> pygame.Surface:
    """A small stone tower in the colour of its behaviour; one more band per level."""
    key = (role, level)
    if key not in _TOWER:
        s = pygame.Surface((24, 26), pygame.SRCALPHA)
        body, dark = rgb(role_hex(role)), rgb("#5A4E3E")
        pygame.draw.rect(s, rgb("#8E877A"), (4, 18, 16, 6))                  # stone foot
        pygame.draw.rect(s, dark, (4, 18, 16, 6), 1)
        pygame.draw.rect(s, body, (7, 8, 10, 11))                           # the tower
        pygame.draw.rect(s, dark, (7, 8, 10, 11), 1)
        for i in range(3):                                                  # battlements
            pygame.draw.rect(s, body, (6 + i * 5, 5, 3, 4))
            pygame.draw.rect(s, dark, (6 + i * 5, 5, 3, 4), 1)
        for i in range(level - 1):                                          # gold bands per level
            pygame.draw.line(s, rgb("#E9C46A"), (8, 16 - i * 3), (15, 16 - i * 3), 1)
        _TOWER[key] = s
    return _TOWER[key]


# ------------------------------------------------------------------ the question card
class MathTdCard(MathQuizScene):
    """The math card over the board. It names what a right answer builds, has no "next" or
    "stop" (the board is waiting). After a right answer it closes itself a moment later;
    after a wrong one it stays until "Tiếp" (Enter), so the solution can be read - the board
    is not moving meanwhile. Like the word card of the garden trial, it ignores clicks and
    keys for a moment after it appears, so a click meant for the board picks nothing."""
    in_combat = True
    GUARD_SECONDS = 0.3
    CLOSE_AFTER = 1.6

    def __init__(self, game, question: dict, hint: str, on_result):
        super().__init__(game, question, run=None, on_result=None)
        self.hint = hint
        self.on_td_result = on_result
        self._done = False

    def update(self, dt, top):
        super().update(dt, top)
        if self.result and self.result.get("correct") and self.result_t >= self.CLOSE_AFTER:
            self.finish()

    def finish(self, stop: bool = False):
        if self._done:
            return
        self._done = True
        self.close()
        self.on_td_result(self.result or {"correct": False})

    def close(self):
        super().close()
        if not self._done:              # closed before the answer came back: it counts as wrong
            self._done = True
            self.on_td_result(self.result or {"correct": False})

    def draw_run(self, ui, x, y, w, h):
        ui.text(self.hint, x + 12, y + h - 12, 7, UICOL["accent"], anchor="midleft", max_w=w - 24)

    def draw_ui(self, ui):
        if self.t < self.GUARD_SECONDS and ui.enabled:
            ui.inp.clicked = False
            ui.inp.keys = []
        super().draw_ui(ui)
        if self.result:
            x, y, w, h = self.panel_rect()
            if ui.button("mtd_card_ok", x + w - 80, y + h - 22, 68, 16, T.MTD_CONTINUE, style="primary",
                         key=pygame.K_RETURN) or ui.key(pygame.K_SPACE):
                self.finish()


# ------------------------------------------------------------------ the board
class MathTdPlayScene(TdPlayScene):
    api_base = "/math/td"
    word_key = "tower_id"
    label_kind = "ui"
    SELL, PLACE_HINT, PICK_HINT = T.MTD_SELL, T.MTD_PLACE_HINT, T.MTD_PICK_HINT

    def __init__(self, game, run: dict, host):
        self.towers = {t["id"]: t for t in run.get("towers") or []}
        super().__init__(game, run, host)

    def question_hint(self, kind: str, word: str | None) -> str:
        q = self.params["qi"]
        if kind == "break":
            return T.MTD_BREAK_CARD.format(q=q["break_qi"])
        if kind == "tu_khi":
            return T.MTD_TU_KHI_CARD.format(q=q["tu_khi_qi"])
        name = self.params["plants"][word]["pinyin"]
        return (T.MTD_PLACE_CARD if kind == "place" else T.MTD_UPGRADE_CARD).format(name=name)

    def question_card(self, question: dict, hint: str, on_result) -> Scene:
        return MathTdCard(self.game, question, hint, on_result)

    def answer_entry(self, question: dict, kind: str, word: str | None, ok: bool) -> dict:
        """The power a right answer gives is fixed by the server when it asks (by tier)."""
        return {"kind": kind, "word": word or "", "ok": ok,
                "power": float((question.get("math_td") or {}).get("power", 1.0))}

    def answered(self, q: dict, kind: str, word, cell, res: dict) -> None:
        super().answered(q, kind, word, cell, res)
        if not res.get("correct") and kind in ("place", "upgrade"):
            self.game.toast(T.MTD_PLACE_WRONG if kind == "place" else T.MTD_UP_WRONG, "#BC4749")

    def piece_name(self, d: dict) -> str:
        return d.get("pinyin", d["hanzi"])

    def piece_image(self, pl, d: dict, frame: int) -> pygame.Surface:
        return tower_sprite(pl.role, pl.level)

    def card_tooltip(self, word: str, d: dict) -> str:
        t = self.towers.get(word) or {}
        area = T.MTD_AREA.format(subject=t.get("subject_name_vi", ""), floor=t.get("floor", "?"))
        return (f"{d.get('pinyin', '')} · {T.MTD_ROLE_NAMES.get(d['role'], d['role'])} · {area}\n"
                f"{t.get('desc_vi', '')}\n" + stats_text(d["role"], self.sim.roles[d["role"]], d["power"]))

    def draw_bar_extra(self, ui, top) -> None:
        """The towers this player cannot build yet, greyed, with the reason on hover."""
        locked = [t for t in self.towers.values() if not t["available"]]
        for i, t in enumerate(locked):
            cx, cy = 8 + (len(self.words) + i) * 36, 202
            if cx + 34 > 300:
                break
            ui.fill(cx, cy, 34, 52, "#B8AE9C")
            ui.border(cx, cy, 34, 52, "#8E877A")
            ui.text(t["label"], cx + 17, cy + 14, 14 if len(t["label"]) <= 2 else 7, "#6B6458", anchor="center")
            ui.text(T.MTD_LOCKED, cx + 17, cy + 31, 7, "#BC4749", anchor="center")
            ui.text(t["name_vi"].replace("Tháp ", ""), cx + 17, cy + 42, 5, "#5A5A5A", anchor="center", max_w=32)
            ui.widgets[f"mtd_locked_{t['id']}"] = ui.rect(cx, cy, 34, 52)
            if top and ui.hover(cx, cy, 34, 52):
                ui.set_tooltip(f"{t['name_vi']}\n{t['locked_vi']}")


# ------------------------------------------------------------------ the level screen
class MathTdScene(Scene):
    """The door of the math hub: the levels, every tower (locked ones with the reason), a run
    left unfinished, and the start button."""

    def __init__(self, game):
        super().__init__(game)
        self.data: dict | None = None
        self.sel: str | None = None
        self.speed = 1          # the last board speed, kept for the next run (TdPlayScene reads it)
        self.starting = False
        self.reload()

    def reload(self, select: str | None = None) -> None:
        def ok(d):
            self.data = d
            if select:
                self.sel = select
            if self.sel is None and d["levels"]:
                opened = [lv for lv in d["levels"] if lv["unlocked"]]
                pick = next((lv for lv in opened if lv["stars"] == 0), opened[-1] if opened else d["levels"][0])
                self.sel = pick["id"]
        self.api.get("/math/td", ok, self.game.api_error)

    def level(self, lid: str | None) -> dict | None:
        return next((lv for lv in (self.data or {}).get("levels", []) if lv["id"] == lid), None)

    def _play(self, path: str, body: dict) -> None:
        if self.starting:
            return
        self.starting = True

        def ok(r):
            self.starting = False
            self.game.push(MathTdPlayScene(self.game, r, self))

        def err(e):
            self.starting = False
            self.game.api_error(e)
            self.reload()
        self.api.post(path, body, ok, err)

    def start_level(self, lid: str) -> None:
        self._play("/math/td/start", {"level_id": lid})

    def resume(self) -> None:
        self._play("/math/td/resume", {})

    def drop_run(self) -> None:
        self.api.post("/math/td/cancel", {}, lambda r: self.reload(), self.game.api_error)

    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 14, 14, 452, 244
        ui.panel(x, y, w, h, T.MTD_TITLE)
        if ui.button("mtd_close", x + w - 52, y + 6, 44, 13, T.CLOSE, size=7, key=pygame.K_ESCAPE):
            self.close()
            return
        d = self.data
        if not d:
            return
        ui.text(T.MTD_INTRO, x + 10, y + 22, 6, GREY, max_w=w - 20)
        self.draw_levels(ui, x + 8, y + 42)
        self.draw_towers(ui, x + 232, y + 42, w - 240)
        run = d.get("active_run")
        if run:
            bx, by, bw = x + 8, y + h - 50, 216
            ui.fill(bx, by, bw, 44, "#FFF3C4")
            ui.border(bx, by, bw, 44, "#C99A3A")
            ui.text(T.TD_RESUME_TEXT.format(name=run["name_vi"], n=run["waves"]), bx + 5, by + 3, 6, max_w=bw - 10)
            if ui.button("mtd_resume", bx + 5, by + 25, 90, 14, T.TD_RESUME, size=7, style="primary"):
                self.resume()
            if ui.button("mtd_drop_run", bx + 101, by + 25, 70, 14, T.TD_DROP_RUN, size=7):
                self.drop_run()

    def draw_levels(self, ui, x, y):
        d = self.data
        ui.text(T.MTD_LEVELS, x, y, 8, "#BC4749")
        for i, lv in enumerate(d["levels"]):
            bx = x + i * 34
            style = "gold" if lv["stars"] == 3 else ("green" if lv["stars"] else "normal")
            if ui.button(f"mtd_lv_{lv['id']}", bx, y + 11, 28, 16, str(i + 1), size=9, style=style,
                         enabled=lv["unlocked"], selected=self.sel == lv["id"],
                         tooltip=lv["name_vi"] if lv["unlocked"] else lv.get("locked_vi")):
                self.sel = lv["id"]
            draw_stars(ui, bx + 14, y + 33, lv["stars"], r=3, gap=7)
        lv = self.level(self.sel)
        if lv is None:
            return
        px, py, pw, ph = x, y + 40, 216, 112 if not d.get("active_run") else 104
        ui.fill(px, py, pw, ph, "#FFFDF7")
        ui.border(px, py, pw, ph)
        ui.text(lv["name_vi"], px + 6, py + 4, 9)
        ui.text(T.MTD_WAVES.format(n=lv["waves"]), px + pw - 6, py + 6, 7, GREY, anchor="topright")
        yy = ui.text(lv["desc_vi"], px + 6, py + 17, 6, GREY, max_w=pw - 12).bottom + 2
        ui.text(T.TD_MONSTERS, px + 6, yy, 7, "#BC4749")
        for i, m in enumerate(lv["monsters"]):
            mx = px + 12 + i * 66
            ui.image(monster_frames(m["id"])[0], mx, yy + 16, 0.55, anchor="center")
            ui.text(m["name_vi"], mx + 9, yy + 12, 6)
        fr = lv["first_rewards"]
        ui.text(T.TD_FIRST_REWARDS.format(a=reward_text(fr[0]), b=reward_text(fr[1]), c=reward_text(fr[2])),
                px + 6, yy + 25, 6, "#8B5A2B", max_w=pw - 12)
        if not d.get("active_run"):
            ui.text(T.TD_DAILY.format(n=d["daily_left"], m=d["daily_max"]), x, py + ph + 8, 6, GREY)
        if ui.button("mtd_start", x + 216 - 74, py + ph + 4, 74, 16, T.TD_START, style="primary",
                     enabled=lv["unlocked"] and not self.starting, key=pygame.K_RETURN):
            self.start_level(lv["id"])

    def draw_towers(self, ui, x, y, w):
        ui.text(T.MTD_TOWERS, x, y, 8, "#BC4749")
        for i, t in enumerate(self.data["towers"]):
            ty = y + 12 + i * 31
            ok = t["available"]
            ui.fill(x, ty, w, 28, "#FFFDF7" if ok else "#E3DCCD")
            ui.border(x, ty, w, 28, role_hex(t["role"]) if ok else "#B8AE9C", 2 if ok else 1)
            ui.image(tower_sprite(t["role"], 1), x + 13, ty + 13, 0.9 if ok else 0.7, anchor="center")
            ui.text(t["label"], x + 13, ty + 22, 6, "#2B2B2B" if ok else "#8E877A", anchor="center")
            ui.text(t["name_vi"], x + 26, ty + 2, 8, "#2B2B2B" if ok else "#6B6458")
            ui.text(T.MTD_ROLE_NAMES.get(t["role"], t["role"]), x + w - 4, ty + 3, 6,
                    role_hex(t["role"]) if ok else "#8E877A", anchor="topright")
            if ok:
                ui.text(f"{T.MTD_AREA.format(subject=t['subject_name_vi'], floor=t['floor'])} · "
                        f"{T.MTD_COST.format(c=t['cost'])}", x + 26, ty + 15, 6, GREY, max_w=w - 30)
            else:
                ui.text(t["locked_vi"], x + 26, ty + 13, 5, "#BC4749", max_w=w - 30, line_gap=1.0)
            ui.widgets[f"mtd_tower_{t['id']}"] = ui.rect(x, ty, w, 28)
            if ui.hover(x, ty, w, 28):
                ui.set_tooltip(f"{t['name_vi']}: {t['desc_vi']}"
                               + ("" if ok else f"\n{t['locked_vi']}"))

