"""Hầm ngục (M10, kế hoạch 4.3): a short chain of rooms grown from a seed, one question type
per room, opened from the math hub's "Hầm Ngục" door.

Three screens in one scene: the gate (pick a floor already reached, type a seed or leave it
empty), the map of the run (the rooms as a chain, which are cleared, the tâm lực, the seed, the
room being played and who guards it), and the result once the run is over. The questions use
the hub's own card (MathQuizScene); the thin subclass below only changes the line along its
bottom and what the buttons after an answer lead to.

The client knows only what the server sends: the layout of the run, never an answer."""
from __future__ import annotations

import pygame

from .. import strings_vi as T
from ..art.palette import UI as UICOL
from ..ui.mathdraw import fit
from .base import Scene
from .math_practice import MathQuizScene

GREY = "#5A5A5A"
PALE = "#9A9387"
RED = "#BC4749"
GREEN = "#6A994E"
GOLD = "#C99A3A"
INK = "#2B2B2B"
ROOM_FILL = {"cleared": "#E8F2DC", "current": "#FBEFD0", "ahead": "#EDE6D6", "lost": "#F6E0DE", "left": "#EDE6D6"}
ROOM_EDGE = {"cleared": GREEN, "current": GOLD, "ahead": "#B8AE9A", "lost": RED, "left": "#B8AE9A"}


def loot_text(stones: int, items: list[dict]) -> str:
    parts = ([T.DG_STONES.format(n=stones)] if stones else []) + [T.DG_ITEM.format(name=i["name_vi"], n=i["qty"])
                                                                  for i in items]
    return ", ".join(parts) or T.DG_NOTHING


class DungeonQuizScene(MathQuizScene):
    """The hub's math card with the run along its bottom: which room, how many right answers
    it still wants, the tâm lực left. After an answer it says what the answer did (a room
    cleared, a tâm lực lost, the chest) and offers the next question or the map."""

    in_combat = True            # (the base card draws no buttons of its own after an answer)
    solution_margin = 52        # room for the line of what the answer did, above the buttons

    def input_margin(self) -> int:
        """The run is written along the bottom of the card: a matching / ordering board (its
        buttons and key hint included) stays above that line."""
        return 30

    def __init__(self, game, question: dict, run: dict, on_result=None):
        super().__init__(game, question, run=run, on_result=on_result)

    def run_line(self, r: dict, answered: bool) -> str:
        """While asking: the room, its name, the right answers it still wants and the tâm lực.
        After the answer the line shares the bottom row with the buttons: room and tâm lực only."""
        i = min(r["room"], len(r["rooms"]) - 1)
        room = r["rooms"][i]
        where = T.DG_ROOM_N.format(i=i + 1, n=len(r["rooms"]))
        if answered:
            return T.DG_LINE_SHORT.format(room=where, h=r["hearts"], m=r["max_hearts"])
        return T.DG_LINE.format(room=where, name=room["name_vi"], p=room["progress"], n=room["need"],
                                h=r["hearts"], m=r["max_hearts"])

    def draw_math_result(self, ui, x, y, w, h):
        super().draw_math_result(ui, x, y, w, h)
        d = (self.result or {}).get("dungeon") or {}
        run = d.get("run") or self.run
        if run and not d.get("stale"):
            ui.text(self.run_line(run, answered=True), x + 12, y + h - 12, 7, GREY, anchor="midleft")
        notes, colour = [], GREEN
        if d.get("chest"):
            notes.append(f"{T.DG_CHEST_OPEN} {loot_text(d['chest']['stones'], d['chest']['items'])}")
        elif d.get("room_cleared"):
            reward = d.get("reward") or {}
            notes.append(f"{T.DG_ROOM_CLEARED} {loot_text(reward.get('stones', 0), reward.get('items', []))}")
        got = d.get("chest") or d.get("reward") or {}
        if got.get("locked"):
            notes.append(T.locked_text(got["locked"]))
        if d.get("heart_lost"):
            notes.append(T.DG_HEART_LOST)
            colour = RED
        if notes:
            ui.text("   ".join(notes), x + 16, y + h - 38, 8, colour, max_w=w - 32)
        over = bool(run and run.get("ended")) or bool(d.get("stale"))
        to_map = over or d.get("room_cleared")
        if not to_map and ui.button("math_stop", x + w - 180, y + h - 22, 68, 16, T.DG_BACK_TO_MAP,
                                    key=pygame.K_ESCAPE):
            self.finish(stop=True)
            return
        label = T.DG_SEE_RESULT if over else (T.DG_BACK_TO_MAP if to_map else T.DG_NEXT)
        if (ui.button("math_next", x + w - 108, y + h - 22, 96, 16, label, style="primary")
                or ui.key(pygame.K_RETURN) or ui.key(pygame.K_SPACE)):
            self.finish(stop=bool(to_map))


class MathDungeonScene(Scene):
    """The gate, the map of the run and the result."""

    def __init__(self, game):
        super().__init__(game)
        self.data: dict | None = None        # GET /math/dungeon
        self.run: dict | None = None         # the open run
        self.result: dict | None = None      # the run that just ended
        self.floor: int | None = None
        self.busy = False

    def on_enter(self):
        self.load()

    # ------------------------------------------------------------ server calls
    def load(self):
        self.busy = True

        def ok(data):
            self.busy = False
            self.data = data
            self.run = data.get("run")
            open_floors = [f["floor"] for f in data.get("floors", []) if f["open"]]
            if self.floor not in open_floors:
                self.floor = data.get("own_floor")
        self.api.get("/math/dungeon", ok, self.fail)

    def fail(self, err):
        self.busy = False
        self.game.api_error(err)

    def start(self, seed: int | None, floor: int | None):
        if self.busy:
            return
        self.busy = True
        self.result = None
        body = {k: v for k, v in (("seed", seed), ("floor", floor)) if v is not None}

        def ok(res):
            self.busy = False
            self.run = res["run"]
            self.game.ui.set_value("dungeon_seed", "")
        self.api.post("/math/dungeon/start", body, ok, self.fail)

    def start_from_box(self):
        text = self.game.ui.value("dungeon_seed").strip()
        top = (self.data or {}).get("seed_max", 999999)
        if text and (not text.isdigit() or int(text) > top):
            self.game.toast(T.DG_SEED_BAD.format(n=top), RED)
            return
        self.start(int(text) if text else None, self.floor)

    def enter(self):
        """Into the current room: its next question (or the one left open)."""
        if self.busy or not self.run:
            return
        self.busy = True

        def ok(res):
            self.busy = False
            self.run = res["run"]
            if res.get("question") is None:          # a timeout settled just now ended the run
                self.finished(self.run)
                return
            self.game.push(DungeonQuizScene(self.game, res["question"], res["run"], on_result=self.on_result))
        self.api.post("/math/dungeon/next", {"run_id": self.run["run_id"]}, ok, self.fail)

    def on_result(self, res: dict, stop: bool):
        d = res.get("dungeon") or {}
        if d.get("run"):
            self.run = d["run"]
        if self.run and self.run.get("ended"):
            self.finished(self.run)
        elif d.get("stale"):
            self.load()
        elif not stop:
            self.enter()

    def finished(self, run: dict):
        """The run is over: read its final numbers (the Tu Vi of the last answer included)."""
        self.busy = True

        def ok(res):
            self.busy = False
            self.result, self.run = res["run"], None
            if self.result["stones_gained"] or self.result["items_gained"]:
                self.game.refresh_me()          # the Linh Thạch on the HUD
                self.game.refresh_inv()
            self.load()
        self.api.get(f"/math/dungeon/run/{run['run_id']}", ok, self.fail)

    def abandon(self):
        if self.busy or not self.run:
            return
        self.busy = True

        def ok(res):
            self.busy = False
            self.result, self.run = res["run"], None
            self.game.refresh_me()
            self.load()
        self.api.post("/math/dungeon/abandon", {"run_id": self.run["run_id"]}, ok, self.fail)

    # ------------------------------------------------------------ drawing
    def draw_ui(self, ui):
        ui.dim()
        x, y, w, h = 40, 16, 400, 238
        ui.panel(x, y, w, h, T.DG_TITLE)
        if self.result:
            self.draw_result(ui, x, y, w, h)
        elif self.data is None:
            ui.text(T.DG_LOADING, x + w / 2, y + h / 2, 9, GREY, anchor="center")
        elif self.run:
            self.draw_map(ui, x, y, w, h)
        else:
            self.draw_gate(ui, x, y, w, h)
        if ui.button("dungeon_close", x + w - 62, y + h - 20, 50, 14, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_hearts(self, ui, right: float, cy: float, hearts: int, top: int):
        for i in range(top):
            hx = right - (top - i) * 11
            ui.fill(hx, cy - 4, 8, 8, RED if i < hearts else "#E3D5BA", radius=2)
            ui.border(hx, cy - 4, 8, 8, "#7A2E2F" if i < hearts else PALE)
        ui.text(T.DG_HEARTS, right - top * 11 - 4, cy, 7, GREY, anchor="midright")

    def draw_gate(self, ui, x, y, w, h):
        d = self.data
        cy = y + 24
        cy += ui.text(T.DG_INTRO, x + 16, cy, 7, GREY, max_w=w - 32).h + 8
        floors = d.get("floors", [])
        open_floors = [f for f in floors if f["open"]]
        if not open_floors:
            ui.text(next((f["locked_vi"] for f in floors), ""), x + w / 2, cy + 20, 9, PALE, anchor="center")
            return
        i = next((n for n, f in enumerate(open_floors) if f["floor"] == self.floor), len(open_floors) - 1)
        f = open_floors[i]
        if ui.button("dungeon_floor_prev", x + 16, cy, 16, 16, "<", enabled=i > 0, key=pygame.K_LEFT):
            self.floor = open_floors[i - 1]["floor"]
        ui.text(fit(ui, T.DG_FLOOR.format(n=f["floor"], title=f["title_vi"]), 9, w - 84), x + w / 2, cy + 8, 9, INK,
                anchor="center")
        if ui.button("dungeon_floor_next", x + w - 32, cy, 16, 16, ">", enabled=i < len(open_floors) - 1,
                     key=pygame.K_RIGHT):
            self.floor = open_floors[i + 1]["floor"]
        cy += 20
        shut = next((g for g in floors if not g["open"]), None)
        if shut:                              # rule 5: what is not there yet says so, and why
            ui.text(T.DG_FLOOR_LOCKED.format(n=shut["floor"], reason=shut["locked_vi"]), x + w / 2, cy, 7, PALE,
                    anchor="midtop", max_w=w - 40)
        cy += 18
        ui.text(T.DG_SEED, x + 92, cy + 9, 8, INK, anchor="midright")
        ui.input_box("dungeon_seed", x + 98, cy, 120, 18, placeholder=T.DG_SEED_HINT, max_len=9)
        go = ui.button("dungeon_start", x + 232, cy, 80, 18, T.DG_START, style="primary", enabled=not self.busy)
        if (go or ui.submitted("dungeon_seed") or ui.key(pygame.K_RETURN)) and not self.busy:
            self.start_from_box()
        cy += 30
        self.draw_hearts(ui, x + w / 2 + 40, cy + 4, d["hearts"], d["hearts"])
        cy += 16
        left = d.get("rewards_left", 0)
        ui.text(T.DG_REWARDS_LEFT.format(n=left, t=d.get("rewards_per_day", 0)) if left else T.DG_NO_REWARD,
                x + w / 2, cy, 7, GOLD if left else PALE, anchor="midtop", max_w=w - 40)

    def draw_chain(self, ui, run: dict, x, y, w):
        """The rooms left to right, then the chest. Green = cleared, gold = the room being
        played, red = where the run was lost."""
        rooms = run["rooms"]
        n = len(rooms) + 1
        gap = 6
        bw = min(56.0, (w - gap * (n - 1)) / n)
        x0 = x + (w - (bw * n + gap * (n - 1))) / 2
        for i, r in enumerate(rooms):
            bx = x0 + i * (bw + gap)
            st = r["state"]
            ui.fill(bx, y, bw, 34, ROOM_FILL[st])
            ui.border(bx, y, bw, 34, ROOM_EDGE[st], 2 if st == "current" else 1)
            ui.text(str(i + 1), bx + 3, y + 2, 7, GREY)
            label = T.DG_WARDEN if r["warden"] else r["short_vi"]
            ui.text(fit(ui, label, 7, bw - 4), bx + bw / 2, y + 15, 7, RED if r["warden"] else INK, anchor="center")
            ui.text(fit(ui, r["qtype_vi"], 6, bw - 4), bx + bw / 2, y + 26, 6, GREY, anchor="center")
            if i < n - 1:
                ui.fill(bx + bw, y + 16, gap, 2, "#B8AE9A")
        cx = x0 + len(rooms) * (bw + gap)
        opened = run.get("chest_opened")
        ui.fill(cx, y, bw, 34, "#F6E7B8" if opened else "#EDE6D6")
        ui.border(cx, y, bw, 34, GOLD, 2 if opened else 1)
        ui.text(T.DG_CHEST, cx + bw / 2, y + 12, 8, GOLD, anchor="center")
        ui.text(fit(ui, run["chest"]["name_vi"], 6, bw - 4), cx + bw / 2, y + 25, 6, GREY, anchor="center")

    def draw_map(self, ui, x, y, w, h):
        run = self.run
        ui.text(f"{T.DG_FLOOR.format(n=run['floor'], title=run.get('floor_title_vi', ''))} · "
                f"{T.DG_SEED_SHOWN.format(n=run['seed'])}", x + 12, y + 22, 7, GREY, max_w=w - 130)
        self.draw_hearts(ui, x + w - 12, y + 26, run["hearts"], run["max_hearts"])
        self.draw_chain(ui, run, x + 10, y + 36, w - 20)
        room = run["rooms"][min(run["room"], len(run["rooms"]) - 1)]
        cy = y + 80
        title = f"{T.DG_ROOM_N.format(i=room['index'] + 1, n=len(run['rooms']))} · {room['name_vi']}"
        if room["warden"]:
            title += f" · {T.DG_WARDEN}"
        ui.text(title, x + 14, cy, 10, RED if room["warden"] else UICOL["accent"])
        cy += 14
        cy += ui.text(room["desc_vi"], x + 14, cy, 7, GREY, max_w=w - 28).h + 3
        ui.text(T.DG_QTYPE.format(name=room["qtype_vi"]), x + 14, cy, 7, INK)
        cy += 10
        skill = T.DG_SKILL.format(name=room["skill_name_vi"]) if room["skill"] else T.DG_SKILL_ALL
        cy += ui.text(skill, x + 14, cy, 7, INK, max_w=w - 28).h + 3
        cy += ui.text(T.DG_GUARD.format(name=room["guardian_vi"], flavour=room["flavour_vi"]), x + 14, cy, 7,
                      "#7A6A4F", max_w=w - 28).h + 3
        ui.text(T.DG_PROGRESS.format(p=room["progress"], n=room["need"]), x + 14, cy, 7, GREEN)
        cy += 14
        rr = run["room_reward"]
        ui.text(f"{T.DG_ROOM_REWARD.format(n=rr['stones'])}   {T.DG_CHEST_REWARD.format(name=run['chest']['name_vi'])}"
                if run["rewarded"] else T.DG_NO_REWARD, x + 14, cy, 7, GOLD if run["rewarded"] else PALE,
                max_w=w - 28)
        cy += 10
        ui.text(T.DG_EARNED.format(what=loot_text(run["stones_gained"], run["items_gained"])), x + 14, cy, 7, GOLD,
                max_w=w - 28)
        if ui.button("dungeon_abandon", x + 12, y + h - 20, 64, 14, T.DG_ABANDON, size=7, enabled=not self.busy):
            self.abandon()
        if ui.button("dungeon_enter", x + w / 2 - 50, y + h - 22, 100, 18, T.DG_ENTER, style="primary",
                     enabled=not self.busy) or (ui.key(pygame.K_RETURN) and not self.busy):
            self.enter()

    def draw_result(self, ui, x, y, w, h):
        r = self.result
        colour = GREEN if r["state"] == "cleared" else (RED if r["state"] == "failed" else GREY)
        ui.text(T.DG_RESULT_TITLE.get(r["state"], ""), x + w / 2, y + 30, 12, colour, anchor="center")
        ui.text(f"{T.DG_FLOOR.format(n=r['floor'], title=r.get('floor_title_vi', ''))} · "
                f"{T.DG_SEED_SHOWN.format(n=r['seed'])}", x + w / 2, y + 42, 7, GREY, anchor="midtop", max_w=w - 30)
        self.draw_chain(ui, r, x + 10, y + 56, w - 20)
        lines = [(T.DG_RESULT_ROOMS.format(c=r["rooms_cleared"], t=r["total_rooms"], x=r["correct"], y=r["asked"]), INK),
                 (T.DG_RESULT_XP.format(n=r["xp_gained"]), GOLD)]
        if r["rewarded"]:
            lines.append((T.DG_RESULT_LOOT.format(what=loot_text(r["stones_gained"], r["items_gained"])), GOLD))
        else:
            lines.append((T.DG_NO_REWARD, PALE))
        if r["state"] != "cleared":
            lines.append((T.DG_RESULT_KEEP, GREY))
        cy = y + 100
        for text, col in lines:
            cy += ui.text(text, x + w / 2, cy, 9, col, anchor="midtop", max_w=w - 40).h + 5
        if ui.button("dungeon_replay", x + w / 2 - 130, y + h - 44, 140, 16, T.DG_REPLAY, style="gold",
                     enabled=not self.busy):
            self.start(r["seed"], r["floor"])
        if ui.button("dungeon_back", x + w / 2 + 20, y + h - 44, 80, 16, T.DG_BACK, style="primary",
                     key=pygame.K_RETURN):
            self.result = None
