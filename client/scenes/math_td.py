"""Thủ Thành Toán (M10, kế hoạch 4.3): the tower defence, opened from the "Thủ Thành" door of
the math hub and from the Cổng Thủ Thành in the village.

  * every tower stands for an area of mathematics; the bar shows the ones the player may
    build, and the locked ones greyed with the reason (a floor not reached yet, a subject
    without questions);
  * clicking a cell with a tower chosen opens a math question of that tower's area (the
    math card of Động Phủ, MathQuizScene); the tower stands only after a right answer, and
    an upgrade works the same way. The board does not move while the card is open;
  * the board runs engine/td_sim.py, the same file as the server. Every action (placing,
    selling, an upgrade, a Linh Khí question, starting a wave) is applied to the simulation
    and written to a log; the log goes to /math/td/* as it grows, and at the end the server
    plays it again before paying anything. Time only runs during a wave.
"""
from __future__ import annotations

import math

import pygame

from .. import strings_vi as T
from ..art import build as B
from ..art.palette import UI as UICOL
from ..art.palette import rgb
from ..engine import art2, td_sim
from .base import Scene
from .math_practice import MathQuizScene
from .td import draw_star, draw_stars, monster_frames, reward_text, role_color, stats_text

GREY = "#5A5A5A"
CELL = 24
BX, BY = 8, 24          # top-left of the board (12 x 7 cells)
BAR_Y = 202             # the tower cards
SPEEDS = [1, 2, 4, 8, 16, 32]
API = "/math/td"


def role_hex(role: str) -> str:
    return T.TD_ROLE_COLORS.get(role, "#7D7468")


_TOWER: dict = {}


def tower_sprite(role: str, level: int) -> pygame.Surface:
    """A small stone tower in the colour of its behaviour; one more band per level. With the
    v2 tower-defence kit: the tower of that role and level (props/td)."""
    pr = art2.td_prop(f"tower_{role}_{max(1, min(3, level))}")
    if pr is not None:
        return pr.img
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
    is not moving meanwhile. It ignores clicks and keys for a moment after it appears, so a
    click meant for the board picks nothing."""
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
class MathTdPlayScene(Scene):
    opaque = True
    draws_world = True
    toast_y = 26

    def __init__(self, game, run: dict, host):
        super().__init__(game)
        self.run, self.host = run, host
        self.towers = {t["id"]: t for t in run.get("towers") or []}
        self.params = run["params"]
        self.answers: dict = dict(run.get("answers") or {})
        self.events: list[dict] = list(run.get("events") or [])
        if self.events:   # continuing a run left unfinished: rebuild it from the saved log
            self.sim = td_sim.replay(self.params, self.answers, self.events, finish=False)
        else:
            self.sim = td_sim.Sim(self.params, self.answers)
        self.sim.record_fx = True
        self.saved = len(self.events)       # events the server has stored (/math/td/event)
        self.saving = False
        self.save_now = False
        self.saved_at = 0.0
        self.bar = list(self.params["plants"])   # tower ids the player may build, in bar order
        self.max_speed = int(run.get("max_speed", 2))
        self.speeds = [s for s in SPEEDS if s <= self.max_speed]
        self.speed = host.speed if host and host.speed in self.speeds else 1
        self.acc = 0.0
        self.t = 0.0
        self.card: str | None = None        # tower chosen in the bar
        self.picked: tuple[int, int] | None = None   # built cell chosen
        self.busy = False                   # a question is being asked
        self.break_left = 0
        self.sending = False
        self.result: dict | None = None
        self.fx: list[list] = []            # [kind, data, age, life]
        self.flash = 0.0
        self.monster_info = {m["id"]: m for m in run.get("monsters", [])}
        self.start_break()

    # ------------------------------------------------------------ actions
    def log(self, ev: dict) -> bool:
        ev = {"s": self.sim.step_n, **ev}
        try:
            self.sim.apply(ev)
        except td_sim.LogError as e:
            msg = {"no_qi": T.TD_NO_QI, "needs_path": T.TD_ON_PATH, "off_path": T.TD_OFF_PATH}.get(str(e), T.TD_CANT_PLACE)
            self.game.toast(msg, "#BC4749")
            return False
        self.events.append(ev)
        if ev["k"] in ("qi", "up", "wave"):
            self.save_now = True
        return True

    def start_break(self) -> None:
        if self.sim.phase == td_sim.BUILD and self.sim.wave < self.sim.total:
            self.break_left = self.params["qi"]["break_questions"] - self.sim.break_q
            if self.break_left > 0:
                self.ask("break")

    def question_hint(self, kind: str, tower: str | None) -> str:
        q = self.params["qi"]
        if kind == "break":
            return T.MTD_BREAK_CARD.format(q=q["break_qi"])
        if kind == "tu_khi":
            return T.MTD_TU_KHI_CARD.format(q=q["tu_khi_qi"])
        name = self.params["plants"][tower]["name_vi"]
        return (T.MTD_PLACE_CARD if kind == "place" else T.MTD_UPGRADE_CARD).format(name=name)

    def ask(self, kind: str, tower: str | None = None, cell: tuple[int, int] | None = None) -> None:
        if self.busy:
            return
        self.busy = True
        body = {"run_id": self.run["run_id"], "kind": kind}
        if tower:
            body["tower_id"] = tower

        def ok(question):
            hint = self.question_hint(kind, tower)
            self.game.push(MathTdCard(self.game, question, hint,
                                      lambda res: self.answered(question, kind, tower, cell, res)))

        def err(e):
            self.busy = False
            if kind == "break":
                self.break_left = 0
            self.game.api_error(e)
        self.api.post(f"{API}/question", body, ok, err)

    def answered(self, q: dict, kind: str, tower: str | None, cell, res: dict) -> None:
        sid = q["session_id"]
        ok = bool(res.get("correct"))
        # what the simulation is told (the server keeps its own copy): the power of a right
        # answer is fixed by the server when it asks (by tier)
        self.answers[sid] = {"kind": kind, "word": tower or "", "ok": ok,
                             "power": float((q.get("math_td") or {}).get("power", 1.0))}
        self.busy = False
        if kind == "place":         # a tower stands only after a right answer
            if self.log({"k": "place", "x": cell[0], "y": cell[1], "w": tower, "q": sid}) and ok:
                self.game.audio.play("discover")
                if self.card and self.sim.qi < self.sim.cost_to_place(self.card):
                    self.card = None
        elif kind == "upgrade":
            self.log({"k": "up", "x": cell[0], "y": cell[1], "q": sid})
            if ok:
                self.game.audio.play("discover")
        else:
            before = self.sim.qi
            self.log({"k": "qi", "q": sid})
            gain = int(round(self.sim.qi - before))
            if gain:
                self.fx.append(["text", (BX + 144, BY + 14, f"{gain:+d} Linh Khí", "#2E6B2E" if gain > 0 else "#BC4749"),
                                0.0, 1.2])
        if not ok and kind in ("place", "upgrade"):
            self.game.toast(T.MTD_PLACE_WRONG if kind == "place" else T.MTD_UP_WRONG, "#BC4749")
        if kind == "break":
            self.break_left -= 1
            if self.break_left > 0 and self.sim.phase == td_sim.BUILD:
                self.ask("break")

    def place(self, x: int, y: int) -> None:
        why = self.sim.can_place(x, y, self.card)
        if why:
            msg = {"no_qi": T.TD_NO_QI, "needs_path": T.TD_ON_PATH, "off_path": T.TD_OFF_PATH}.get(why, T.TD_CANT_PLACE)
            self.game.toast(msg, "#BC4749")
            return
        self.ask("place", self.card, (x, y))     # placing is a question first

    def upgrade(self) -> None:
        pl = self.sim.plants.get(self.picked) if self.picked else None
        if pl is None:
            return
        cost = self.sim.cost_to_upgrade(pl)
        if cost is None or self.sim.qi < cost:
            self.game.toast(T.TD_NO_QI, "#BC4749")
            return
        self.ask("upgrade", pl.word, (pl.x, pl.y))

    def sell(self) -> None:
        if self.picked and self.log({"k": "sell", "x": self.picked[0], "y": self.picked[1]}):
            self.picked = None

    def start_wave(self) -> None:
        if self.log({"k": "wave"}):
            self.break_left = 0
            self.game.audio.play("crack")

    def tu_khi_left(self) -> float:
        cd = self.sim.tu_khi_cd()
        return max(0.0, (cd - (self.sim.step_n - self.sim.last_tu_khi)) * td_sim.STEP_MS / 1000)

    def leave(self) -> None:
        def go():
            self.sending = True
            self.api.post(f"{API}/cancel", {}, None, lambda e: None)
            self.close()
            if self.host:
                self.host.reload()
        self.game.message(T.TD_LEAVE_CONFIRM, T.TD_LEAVE, ok=T.TD_LEAVE, cancel=T.BACK, on_ok=go)

    def send_finish(self) -> None:
        self.sending = True
        s = self.sim.summary()
        claim = {k: s[k] for k in ("result", "core_hp", "wave", "steps")}

        def ok(r):
            self.result = r
            self.game.refresh_me()
            self.game.refresh_inv()
            self.game.push(MathTdResultScene(self.game, self, r))

        def err(e):
            self.game.api_error(e)
            self.close()
            if self.host:
                self.host.reload()
        self.api.post(f"{API}/finish", {"run_id": self.run["run_id"], "events": self.events, "claim": claim}, ok, err)

    # ------------------------------------------------------------ time
    def update(self, dt, top):
        self.t += dt
        for f in list(self.fx):
            f[2] += dt
            if f[2] >= f[3]:
                self.fx.remove(f)
        self.flash = max(0.0, self.flash - dt)
        if self.sending:
            return
        sim = self.sim
        if sim.phase == td_sim.WAVE and not self.busy and top:
            self.acc += min(dt, 0.1) * 1000 * self.speed
            n = 0
            while self.acc >= td_sim.STEP_MS and sim.phase == td_sim.WAVE and n < 600:
                sim.step()
                self.acc -= td_sim.STEP_MS
                n += 1
            self.take_fx()
            if sim.phase == td_sim.BUILD:
                self.acc = 0.0
                self.start_break()
        if sim.phase in (td_sim.WON, td_sim.LOST) and not self.busy:
            self.send_finish()
        elif len(self.events) > self.saved and not self.saving and (self.save_now or self.t - self.saved_at > 2.0):
            self.save_log()

    def save_log(self) -> None:
        """Keep the server's copy of the log up to date, so a game closed in the middle can
        continue this run."""
        self.saving, self.save_now, self.saved_at = True, False, self.t
        start, part = self.saved, self.events[self.saved:]

        def ok(r):
            self.saving = False
            self.saved = max(self.saved, int(r.get("saved", start + len(part))))

        def err(e):
            self.saving = False
        self.api.post(f"{API}/event", {"run_id": self.run["run_id"], "start": start, "events": part}, ok, err)

    def take_fx(self) -> None:
        for f in self.sim.fx[-60:]:
            kind = f[0]
            if kind == "shot":
                self.fx.append(["shot", (f[1], f[2], f[3]), 0.0, 0.14])
            elif kind == "quake":
                self.fx.append(["ring", (f[1], f[2]), 0.0, 0.35])
            elif kind == "qi":
                self.fx.append(["text", (BX + f[1][0] * CELL + 12, BY + f[1][1] * CELL, "+", "#6A994E"), 0.0, 0.8])
            elif kind == "die":
                self.fx.append(["puff", f[1], 0.0, 0.35])
            elif kind == "leak":
                self.flash = 0.35
                self.game.audio.play("wrong")
        self.sim.fx = []

    # ------------------------------------------------------------ drawing: the board in pixels
    def board_v2(self) -> pygame.Surface | None:
        """The board's ground from the v2 kit at its native 24 px cell (td24): grass, the path with
        `td_path_<sides>` edges, the rocks. Built once per path; None without the kit."""
        tiles = art2.td_tiles()
        sim = self.sim
        if not tiles or "grass" not in tiles:
            return None
        key = (tuple(sim.path), tuple(sorted(sim.rocks)), sim.cols, sim.rows)
        if getattr(self, "_board_key", None) != key:
            path = set(sim.path)
            surf = pygame.Surface((sim.cols * CELL, sim.rows * CELL))
            for y in range(sim.rows):
                for x in range(sim.cols):
                    if (x, y) in path:
                        def grass(dx, dy):
                            nx, ny = x + dx, y + dy
                            return 0 <= nx < sim.cols and 0 <= ny < sim.rows and (nx, ny) not in path
                        name = art2.td_path_name(grass(0, -1), grass(1, 0), grass(0, 1), grass(-1, 0))
                        t = (tiles.get(name) or tiles.get("path"))
                    else:
                        t = tiles["grass"]
                    surf.blit(t[(x * 3 + y) % len(t)], (x * CELL, y * CELL))
                    if (x, y) in sim.rocks:
                        rk = art2.td_prop(f"td_rock_{x % 2}")
                        if rk is not None:
                            surf.blit(rk.img, (x * CELL + CELL // 2 - rk.pivot[0], y * CELL + CELL - 2 - rk.pivot[1]))
            self._board_key, self._board = key, surf
        return self._board

    def draw_world(self, surf):
        sim = self.sim
        surf.fill(rgb("#E9DFC8"))
        path = set(sim.path)
        board = self.board_v2()
        if board is not None:
            surf.blit(board, (BX, BY))
        for y in range(sim.rows if board is None else 0):
            for x in range(sim.cols):
                r = pygame.Rect(BX + x * CELL, BY + y * CELL, CELL, CELL)
                if (x, y) in path:
                    pygame.draw.rect(surf, rgb("#B8996B"), r)
                    pygame.draw.rect(surf, rgb("#A3865A"), r, 1)
                else:
                    shade = "#8DB360" if (x + y) % 2 else "#86AC5A"
                    pygame.draw.rect(surf, rgb(shade), r)
                if (x, y) in sim.rocks:
                    surf.blit(B.rock(x % 2), (r.x + 4, r.y + 4))
        if sim.lit:   # light on the path
            glow = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
            glow.fill((255, 236, 150, 70))
            for i in sim.lit:
                px, py = sim.path[i]
                surf.blit(glow, (BX + px * CELL, BY + py * CELL))
        gx, gy = sim.path[0]
        cx, cy = sim.path[-1]
        spawn, core = art2.td_prop("td_spawn"), art2.td_prop("td_core")
        if spawn is not None and core is not None:      # the v2 ink gate and spirit core
            for pr, (px, py) in ((spawn, (gx, gy)), (core, (cx, cy))):
                img = pr.at(self.t * 2)
                surf.blit(img, (BX + px * CELL + 12 - pr.pivot[0], BY + py * CELL + 12 - pr.pivot[1] + img.get_height() // 2))
        else:
            pygame.draw.circle(surf, rgb("#2B2B2B"), (BX + gx * CELL + 12, BY + gy * CELL + 12), 10)
            pygame.draw.circle(surf, rgb("#5A3E6E"), (BX + gx * CELL + 12, BY + gy * CELL + 12), 6 + int(self.t * 3) % 3)
            pulse = 2 * math.sin(self.t * 3)
            pygame.draw.circle(surf, rgb("#B5E3F0"), (BX + cx * CELL + 12, BY + cy * CELL + 12), int(9 + pulse))
            pygame.draw.circle(surf, rgb("#4A90C8"), (BX + cx * CELL + 12, BY + cy * CELL + 12), int(9 + pulse), 2)
        frame = int(self.t * 2) % 2
        # range preview
        hover = self.hover_cell()
        show = None
        if self.card and hover:
            show = (hover, self.sim.roles[self.params["plants"][self.card]["role"]].get("range", 0))
        elif self.picked and self.picked in sim.plants:
            pl = sim.plants[self.picked]
            show = (self.picked, sim.roles[pl.role].get("range", 0))
        if show and show[1]:
            (hx, hy), rr = show
            ring = pygame.Surface((480, 270), pygame.SRCALPHA)
            pygame.draw.circle(ring, (255, 255, 255, 50), (BX + hx * CELL + 12, BY + hy * CELL + 12), int(rr * CELL))
            pygame.draw.circle(ring, (255, 255, 255, 140), (BX + hx * CELL + 12, BY + hy * CELL + 12), int(rr * CELL), 1)
            surf.blit(ring, (0, 0))
        if self.card and hover:
            ok = sim.can_place(hover[0], hover[1], self.card) is None
            pygame.draw.rect(surf, rgb("#6A994E" if ok else "#BC4749"),
                             (BX + hover[0] * CELL, BY + hover[1] * CELL, CELL, CELL), 2)
        for c in sim.order:
            pl = sim.plants[c]
            rx, ry = BX + pl.x * CELL, BY + pl.y * CELL
            tw = art2.td_prop(f"tower_{pl.role}_{max(1, min(3, pl.level))}")
            if tw is not None:       # the v2 tower of the piece's role and level, standing on its cell
                img = tw.at(self.t)
                surf.blit(img, (rx + CELL // 2 - tw.pivot[0], ry + CELL - 3 - tw.pivot[1] + 3))
            else:
                img = tower_sprite(pl.role, pl.level)
                if pl.role == "moc":
                    pygame.draw.rect(surf, rgb("#5C4A2E"), (rx + 3, ry + 3, CELL - 6, CELL - 6))
                surf.blit(img, (rx, ry - 2))
            pygame.draw.rect(surf, role_color(pl.role), (rx + 1, ry + CELL - 3, CELL - 2, 2))
            for i in range(pl.level):
                pygame.draw.rect(surf, rgb("#E9C46A"), (rx + 2 + i * 4, ry + 2, 3, 3))
            if pl.role == "moc" and pl.max_hp:
                k = max(0.0, pl.hp / pl.max_hp)
                pygame.draw.rect(surf, rgb("#3A342C"), (rx + 2, ry + CELL - 6, CELL - 4, 2))
                pygame.draw.rect(surf, rgb("#6A994E"), (rx + 2, ry + CELL - 6, int((CELL - 4) * k), 2))
            if self.picked == c:
                pygame.draw.rect(surf, rgb("#E9C46A"), (rx, ry, CELL, CELL), 1)
        for m in sim.monsters:
            mx, my = sim.pos(m)
            img = monster_frames(m.kind)[frame % len(monster_frames(m.kind))]
            px, py = BX + mx * CELL + 12, BY + my * CELL + 12
            if sim.kinds[m.kind].get("hidden") and not sim.visible(m):
                img = img.copy()
                img.set_alpha(80)
            surf.blit(img, (int(px - img.get_width() / 2), int(py - img.get_height() / 2 - 2)))
            k = max(0.0, m.hp / m.max_hp)
            pygame.draw.rect(surf, rgb("#3A342C"), (int(px - 7), int(py - img.get_height() / 2 - 5), 14, 2))
            pygame.draw.rect(surf, rgb("#BC4749"), (int(px - 7), int(py - img.get_height() / 2 - 5), int(14 * k), 2))
            if m.stun_until > sim.step_n:
                pygame.draw.circle(surf, rgb("#E9C46A"), (int(px), int(py - 10)), 2)
            elif m.slow_until > sim.step_n:
                pygame.draw.circle(surf, rgb("#4A90C8"), (int(px + 6), int(py + 4)), 2)
        for kind, data, age, life in self.fx:
            if kind == "shot" and self.shot_v2(surf, data, age, life):
                continue
            if kind == "puff" and self.puff_v2(surf, data, age, life):
                continue
            if kind == "shot":
                role, (sx, sy), (tx, ty) = data
                pygame.draw.line(surf, role_color(role), (BX + sx * CELL + 12, BY + sy * CELL + 8),
                                 (int(BX + tx * CELL + 12), int(BY + ty * CELL + 12)), 2 if role == "kim" else 1)
                if role == "hoa":
                    pygame.draw.circle(surf, rgb("#E07A3F"), (int(BX + tx * CELL + 12), int(BY + ty * CELL + 12)),
                                       int(4 + age * 40), 1)
            elif kind == "ring":
                (rx, ry), rr = data
                pygame.draw.circle(surf, rgb("#9C7B4E"), (int(BX + rx * CELL + 12), int(BY + ry * CELL + 12)),
                                   max(2, int(rr * CELL * age / life)), 1)
            elif kind == "puff":
                px, py = data
                pygame.draw.circle(surf, rgb("#5A5A5A"), (int(BX + px * CELL + 12), int(BY + py * CELL + 12)),
                                   int(3 + age * 20), 1)
        if self.flash:
            veil = pygame.Surface((480, 270), pygame.SRCALPHA)
            veil.fill((188, 71, 73, int(120 * self.flash)))
            surf.blit(veil, (0, 0))

    def shot_v2(self, surf, data, age: float, life: float) -> bool:
        """A projectile of the v2 kit flying from the tower to its target, then its hit puff."""
        role, (sx, sy), (tx, ty) = data
        k = min(1.0, age / max(0.01, life))
        x0, y0 = BX + sx * CELL + 12, BY + sy * CELL + 8
        x1, y1 = BX + tx * CELL + 12, BY + ty * CELL + 12
        shot = art2.td_prop(f"shot_{role}")
        if shot is None:
            return False
        if k < 0.8:
            img = shot.at(age * 20)
            ang = -math.degrees(math.atan2(y1 - y0, x1 - x0))
            img = art2.rotated(img, ang)
            x, y = x0 + (x1 - x0) * k / 0.8, y0 + (y1 - y0) * k / 0.8
            surf.blit(img, (int(x - img.get_width() / 2), int(y - img.get_height() / 2)))
        else:
            hit = art2.td_prop(f"hit_{role}") or art2.td_prop("hit_puff")
            if hit is not None:
                img = hit.frames[min(len(hit.frames) - 1, int((k - 0.8) / 0.2 * len(hit.frames)))]
                surf.blit(img, (int(x1 - img.get_width() / 2), int(y1 - img.get_height() / 2)))
        return True

    def puff_v2(self, surf, data, age: float, life: float) -> bool:
        hit = art2.td_prop("hit_puff")
        if hit is None:
            return False
        px, py = data
        img = hit.frames[min(len(hit.frames) - 1, int(age / max(0.01, life) * len(hit.frames)))]
        surf.blit(img, (int(BX + px * CELL + 12 - img.get_width() / 2), int(BY + py * CELL + 12 - img.get_height() / 2)))
        return True

    def hover_cell(self) -> tuple[int, int] | None:
        mx, my = self.game.ui.inp.mouse
        x, y = int((mx - BX) // CELL), int((my - BY) // CELL)
        if 0 <= x < self.sim.cols and 0 <= y < self.sim.rows and mx >= BX and my >= BY:
            return x, y
        return None

    # ------------------------------------------------------------ drawing: HUD and input
    def draw_ui(self, ui):
        sim = self.sim
        top = self.game.top is self
        p = self.params
        # top bar
        ui.fill(0, 0, 480, 20, (43, 43, 43, 230))
        ui.text(self.run.get("name_vi", ""), 6, 10, 8, "#F4EBD9", anchor="midleft")
        ui.text(T.TD_WAVE.format(n=sim.wave, t=sim.total), 150, 10, 8, "#E9C46A", anchor="midleft")
        ui.text(T.TD_CORE.format(n=sim.hp, m=p["core_hp"]), 214, 10, 8, "#B5E3F0", anchor="midleft")
        ui.text(T.TD_QI.format(n=int(sim.qi)), 300, 10, 9, "#B5D67A", anchor="midleft")
        # tower labels on the board (crisp, at window resolution)
        for c in sim.order:
            pl = sim.plants[c]
            label = p["plants"][pl.word]["label"]
            tx, ty = BX + pl.x * CELL + CELL - 5, BY + pl.y * CELL + CELL - 8
            ui.fill(tx - 5, ty - 5, 10, 10, "#FFFDF7")
            ui.text(label[:2], tx, ty, 7 if len(label) == 1 else 4, anchor="center")
        for i in range(sim.rows):
            for j in range(sim.cols):
                ui.widgets[f"td_cell_{j}_{i}"] = ui.rect(BX + j * CELL, BY + i * CELL, CELL, CELL)
        for kind, data, age, life in self.fx:
            if kind == "text":
                x, y, txt, col = data
                ui.text(txt, x, y - age * 14, 8, col, anchor="center")
        self.draw_bar(ui, top)
        self.draw_side(ui, top)
        if self.sending and not self.result:
            ui.fill(120, 110, 240, 24, (20, 18, 15, 220))
            ui.text(T.TD_CHECKING, 240, 122, 8, "#F4EBD9", anchor="center")
        if not top or self.sending:
            return
        # monster card on hover
        mx, my = ui.inp.mouse
        for m in sim.monsters:
            px, py = sim.pos(m)
            if abs(BX + px * CELL + 12 - mx) < 9 and abs(BY + py * CELL + 12 - my) < 9:
                info = self.monster_info.get(m.kind) or {"name_vi": m.kind, "weakness_vi": ""}
                ui.set_tooltip(f"{info['name_vi']} — {T.TD_MONSTER_HP.format(hp=int(m.hp), sp=sim.kinds[m.kind]['speed'], lk=sim.kinds[m.kind]['leak'])}\n{info.get('weakness_vi', '')}")
                break
        cell = self.hover_cell()
        if ui.inp.right_clicked:
            self.card, self.picked = None, None
        if cell and ui.click_in(BX, BY, sim.cols * CELL, sim.rows * CELL):
            if self.card and not self.busy:
                self.place(*cell)
            elif cell in sim.plants:
                self.picked = cell
            else:
                self.picked = None
        if ui.key(pygame.K_SPACE) and sim.phase == td_sim.BUILD and not self.busy:
            self.start_wave()

    def draw_bar(self, ui, top):
        sim = self.sim
        ui.fill(0, BAR_Y - 4, 300, 72, (43, 43, 43, 200))
        for i, tid in enumerate(self.bar):
            d = self.params["plants"][tid]
            cx, cy = BX + i * 36, BAR_Y
            cost = sim.cost_to_place(tid)
            can = sim.qi >= cost
            ui.fill(cx, cy, 34, 52, "#FFF3C4" if self.card == tid else ("#FFFDF7" if can else "#CFC6B4"))
            ui.border(cx, cy, 34, 52, T.TD_ROLE_COLORS.get(d["role"], "#2B2B2B"), 2 if self.card == tid else 1)
            ui.text(d["label"], cx + 17, cy + 14, 14 if len(d["label"]) <= 2 else 7, anchor="center")
            ui.text(str(int(cost)), cx + 17, cy + 31, 7, "#2E6B2E", anchor="center")
            ui.text(f"{int(d['power'] * 100)}%", cx + 17, cy + 42, 6, "#5A5A5A", anchor="center")
            ui.widgets[f"td_card_{i}"] = ui.rect(cx, cy, 34, 52)
            if top and not self.sending:
                if ui.hover(cx, cy, 34, 52):
                    ui.set_tooltip(self.card_tooltip(tid, d))
                if ui.click_in(cx, cy, 34, 52) or ui.key(pygame.K_1 + i):
                    self.card = None if self.card == tid else tid
                    self.picked = None
        self.draw_locked(ui, top)

    def card_tooltip(self, tid: str, d: dict) -> str:
        t = self.towers.get(tid) or {}
        area = T.MTD_AREA.format(subject=t.get("subject_name_vi", ""), floor=t.get("floor", "?"))
        return (f"{d['name_vi']} · {T.MTD_ROLE_NAMES.get(d['role'], d['role'])} · {area}\n"
                f"{t.get('desc_vi', '')}\n" + stats_text(d["role"], self.sim.roles[d["role"]], d["power"]))

    def draw_locked(self, ui, top) -> None:
        """The towers this player cannot build yet, greyed, after the cards, with the reason on hover."""
        locked = [t for t in self.towers.values() if not t["available"]]
        for i, t in enumerate(locked):
            cx, cy = BX + (len(self.bar) + i) * 36, BAR_Y
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

    def draw_side(self, ui, top):
        sim = self.sim
        x, y, w = 304, 24, 170
        ui.fill(x, y, w, 238, (244, 235, 217, 235))
        ui.border(x, y, w, 238, "#8B5A2B")
        enabled = top and not self.sending
        yy = y + 6
        if self.picked and self.picked in sim.plants:
            pl = sim.plants[self.picked]
            d = self.params["plants"][pl.word]
            ui.text(d["label"], x + 16, yy + 12, 18 if len(d["label"]) <= 2 else 9, anchor="center")
            ui.text(f"{d['name_vi']} · {T.TD_LEVEL.format(n=pl.level)}", x + 34, yy + 4, 8, max_w=w - 40)
            ui.text(f"{int(d['power'] * pl.mult * 100)}%", x + 34, yy + 16, 7, "#5A5A5A")
            yy += 30
            yy = ui.text(stats_text(pl.role, sim.roles[pl.role], d["power"] * pl.mult, pl.level,
                                    self.params["upgrade"]["level_mult"]), x + 6, yy, 7, max_w=w - 12).bottom + 4
            cost = sim.cost_to_upgrade(pl)
            if cost is None:
                ui.button("td_upgrade", x + 6, yy, 76, 15, T.TD_UPGRADE_MAX, size=7, enabled=False)
            elif ui.button("td_upgrade", x + 6, yy, 76, 15, T.TD_UPGRADE.format(c=int(cost)), size=7, style="green",
                           enabled=enabled and not self.busy and sim.qi >= cost):
                self.upgrade()
            if ui.button("td_sell", x + 88, yy, 76, 15, T.MTD_SELL.format(c=int(pl.spent * self.params["sell_refund"])),
                         size=7, enabled=enabled and not self.busy):
                self.sell()
            yy += 22
        elif self.card:
            d = self.params["plants"][self.card]
            ui.text(T.MTD_PLACE_HINT.format(name=d["name_vi"]), x + 6, yy, 7, max_w=w - 12)
            yy += 22
            yy = ui.text(stats_text(d["role"], sim.roles[d["role"]], d["power"]), x + 6, yy, 7, max_w=w - 12).bottom + 4
        else:
            yy = ui.text(T.MTD_PICK_HINT, x + 6, yy, 7, "#5A5A5A", max_w=w - 12).bottom + 4
        by = y + 238 - 86
        can_wave = sim.phase == td_sim.BUILD and not self.busy and sim.wave < sim.total
        if ui.button("td_wave", x + 6, by, w - 12, 18, T.TD_START_WAVE, style="primary", enabled=enabled and can_wave):
            self.start_wave()
        left = self.tu_khi_left()
        can_tk = sim.phase == td_sim.WAVE and not self.busy and left <= 0
        label = T.TD_TU_KHI if left <= 0 or sim.phase != td_sim.WAVE else T.TD_TU_KHI_WAIT.format(n=int(math.ceil(left)))
        if ui.button("td_tukhi", x + 6, by + 22, w - 12, 18, label, style="green", enabled=enabled and can_tk,
                     key=pygame.K_q if enabled else None):
            self.ask("tu_khi")
        if ui.button("td_speed", x + 6, by + 44, (w - 18) / 2, 16, T.TD_SPEED.format(n=self.speed), size=7,
                     enabled=enabled):
            i = self.speeds.index(self.speed) if self.speed in self.speeds else 0
            self.speed = self.speeds[(i + 1) % len(self.speeds)]
            if self.host:
                self.host.speed = self.speed
        if ui.button("td_leave", x + 12 + (w - 18) / 2, by + 44, (w - 18) / 2, 16, T.TD_LEAVE, size=7,
                     enabled=enabled, key=pygame.K_ESCAPE if enabled else None):
            self.leave()


# ------------------------------------------------------------------ result
class MathTdResultScene(Scene):
    def __init__(self, game, play: MathTdPlayScene, r: dict):
        super().__init__(game)
        self.play, self.r = play, r
        self.t = 0.0
        game.audio.play("discover" if r.get("result") == "won" else "wrong")

    def update(self, dt, top):
        self.t += dt

    def back(self, then=None) -> None:
        self.close()
        self.play.close()
        host = self.play.host
        if host:
            host.reload(select=then)

    def draw_ui(self, ui):
        ui.dim(150)
        r = self.r
        x, y, w, h = 110, 50, 260, 170
        won = r.get("result") == "won"
        ui.panel(x, y, w, h, T.TD_WON if won else T.TD_LOST)
        k = min(1.0, self.t / 0.8)
        stars = r.get("stars", 0)
        for i in range(3):
            draw_star(ui, x + w / 2 - 34 + i * 34, y + 34, 13, i < stars and k >= (i + 1) / 3)
        ui.text(T.TD_RESULT_STARS.format(hp=r.get("core_hp", 0), m=self.play.params["core_hp"]), x + w / 2, y + 58,
                8, anchor="center")
        rew = r.get("rewards") or {}
        if rew and any(rew.get(k) for k in ("spirit_stones", "immortal_jade", "items")):
            line = T.TD_RESULT_REWARDS.format(r=reward_text(rew))
            ui.text(line, x + w / 2, y + 76, 8, "#8B5A2B", anchor="midtop", max_w=w - 24)
            if rew.get("replay"):
                ui.text(T.TD_RESULT_REPLAY.format(n=r.get("daily_left", 0)), x + w / 2, y + 100, 7, "#5A5A5A",
                        anchor="midtop")
        else:
            ui.text(T.TD_RESULT_NO_REWARD, x + w / 2, y + 80, 8, "#8E877A", anchor="midtop")
        bw = 76
        nxt = r.get("next_level")
        if nxt:
            if ui.button("td_result_next", x + 10, y + h - 24, bw, 16, T.TD_RESULT_NEXT, style="primary",
                         key=pygame.K_RETURN):
                self.back(then=nxt)
                return
        if ui.button("td_result_retry", x + w / 2 - bw / 2, y + h - 24, bw, 16, T.TD_RESULT_RETRY):
            self.back(then=self.play.params.get("level"))
            return
        if ui.button("td_result_map", x + w - bw - 10, y + h - 24, bw, 16, T.TD_RESULT_MAP, key=pygame.K_ESCAPE):
            self.back()


# ------------------------------------------------------------------ the level screen
class MathTdScene(Scene):
    """The door of the math hub and the Cổng Thủ Thành: the levels, every tower (locked ones
    with the reason), a run left unfinished, and the start button."""

    def __init__(self, game):
        super().__init__(game)
        self.data: dict | None = None
        self.sel: str | None = None
        self.speed = 1          # the last board speed, kept for the next run (the board reads it)
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
        self.api.get(API, ok, self.game.api_error)

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
        self._play(f"{API}/start", {"level_id": lid})

    def resume(self) -> None:
        self._play(f"{API}/resume", {})

    def drop_run(self) -> None:
        self.api.post(f"{API}/cancel", {}, lambda r: self.reload(), self.game.api_error)

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
