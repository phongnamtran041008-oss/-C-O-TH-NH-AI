"""Tổ đội and bí cảnh on the client (stage 9, spec 14, 15.3).

- PartyScene (key Y): members with their health, invite by name, leave, kick, promote.
- RealmGateScene: the Cổng Bí Cảnh in Trúc Lâm Thôn (or a Khe Nứt Mực rift in the wild):
  the party realms (opening hours, entries left today, enter with the party or join the
  queue), the always-open math realm with its room guide, and the forge that turns Mảnh Bảo
  Vật into the Mặc Ảnh set. Every realm is a math bí cảnh: the card shows the player's floor.
- RealmView: lives inside the WorldScene while it shows the bi_canh map. It keeps what the
  server said about the run (room, its Trận Nhãn seals or the boss), draws the seals on the
  stones of the borrowed room, the room banner, the room card and the result.
Everything is decided by the server; the client only shows it (a seal asks whoever stands on it).
"""
from __future__ import annotations

import math

import pygame

from .. import strings_vi as T
from ..engine import sprites
from .base import Scene


def realm_v2_name(name: str, *args) -> tuple[str, int]:
    """(v2 prop name in props/realm, frame) for an old realm_art call (see wiring.realm_props)."""
    if name == "pedestal":
        active, lit = args[0], args[1]
        return ("pedestal_lit" if lit else "pedestal_on") if active else "pedestal_off", 0
    if name == "rune_tile":
        return f"rune_{args[0]}", 0
    if name == "pillar":
        return f"pillar_{max(1, min(4, int(args[0])))}_{'on' if len(args) > 1 and args[1] else 'off'}", 0
    if name == "realm_exit":
        return ("exit_open" if args[0] else "exit_closed"), int(args[1]) if len(args) > 1 else 0
    if name == "chest":
        return ("chest_open" if args[0] else "chest_closed"), 0
    return name, int(args[0]) if args else 0          # statue, mirror, rift: (frame)


def realm_img(v, name: str, *args) -> pygame.Surface:
    """A bí cảnh piece through the View: the v2 piece (exactly 2x the old sprite, so it sits on the
    same top-left) when the world is zoomed and the atlas has it, else the old sprite at the zoom."""
    if v.zoom != 1:
        from ..engine import art2
        pname, frame = realm_v2_name(name, *args)
        pr = art2.realm_prop(pname)
        if pr is not None:
            return pr.frames[frame % len(pr.frames)]
    return v.img(sprites.realm(name, *args))


def fmt_time(secs: float) -> str:
    secs = max(0, int(secs))
    return T.REALM_TIME.format(m=secs // 60, s=secs % 60)


def fmt_wait(secs: float) -> str:
    secs = max(0, int(secs))
    h, m = secs // 3600, (secs % 3600) // 60
    return f"{h} giờ {m} phút" if h else f"{max(1, m)} phút"


# ------------------------------------------------------------------ the party
class PartyScene(Scene):
    def draw_ui(self, ui):
        g = self.game
        ui.dim(100)
        x, y, w, h = 120, 34, 240, 200
        ui.panel(x, y, w, h, T.PARTY_TITLE)
        party = g.state.party
        me = g.state.me.get("id")
        cy = y + 14
        if not party:
            ui.text(T.PARTY_NONE, x + 12, cy, 7, "#5A5A5A", max_w=w - 24)
            cy += 30
        else:
            leader = party["leader"]
            for m in party["members"]:
                ui.fill(x + 10, cy, w - 20, 22, "#EFE6D2")
                r = ui.text(m["name"], x + 14, cy + 2, 8, "#2B2B2B")
                if m["uid"] == leader:
                    ui.text(T.PARTY_LEADER, r.right + 4, cy + 3, 6, "#C99A3A")
                sub = T.REALMS.get(m.get("realm") or "", "") if m["online"] else T.PARTY_OFFLINE
                if m.get("zone"):
                    sub += " · " + T.ZONE_NAMES.get(m["zone"], m["zone"])
                ui.text(sub, x + 14, cy + 12, 6, "#6A994E" if m["online"] else "#8E877A")
                if m.get("hp") is not None:
                    ui.progress(x + 120, cy + 4, 50, 5, m["hp"] / 100, "#8C8C8C" if m.get("ghost") else "#BC4749")
                if me == leader and m["uid"] != me:
                    if ui.button(f"pt_kick_{m['uid']}", x + w - 64, cy + 3, 48, 8, T.PARTY_KICK, size=6):
                        self.send("kick", uid=m["uid"])
                    if ui.button(f"pt_lead_{m['uid']}", x + w - 64, cy + 12, 48, 8, T.PARTY_PROMOTE, size=6):
                        self.send("promote", uid=m["uid"])
                cy += 24
            if ui.button("pt_leave", x + 12, cy + 2, 70, 14, T.PARTY_LEAVE):
                self.send("leave")
            cy += 20
        invites = [i for i in g.party_invites if i["until"] > g.now]
        if invites:
            ui.text(T.PARTY_PENDING, x + 12, cy, 7, "#8B5A2B")
            cy += 10
            for inv in invites[:2]:
                ui.text(inv["name"], x + 14, cy + 3, 8)
                if ui.button(f"pt_acc_{inv['uid']}", x + w - 120, cy, 52, 13, T.PARTY_ACCEPT, style="green"):
                    g.answer_invite(inv["uid"], True)
                if ui.button(f"pt_dec_{inv['uid']}", x + w - 64, cy, 52, 13, T.PARTY_DECLINE):
                    g.answer_invite(inv["uid"], False)
                cy += 16
        if not party or party["leader"] == me:
            name = ui.input_box("pt_name", x + 12, y + h - 50, w - 84, 14, T.PARTY_INVITE_PH, max_len=20)
            if (ui.button("pt_invite", x + w - 66, y + h - 50, 54, 14, T.PARTY_INVITE_BTN, style="primary")
                    or ui.submitted("pt_name")) and name.strip():
                self.send("invite", name=name.strip())
                ui.set_value("pt_name", "")
        ui.text(T.PARTY_HINT, x + 12, y + h - 32, 6, "#5A5A5A", max_w=w - 24)
        if ui.button("pt_close", x + w / 2 - 30, y + h - 17, 60, 13, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def send(self, op: str, **kw) -> None:
        if self.game.net is not None:
            self.game.net.send({"t": "party", "op": op, **kw})


def draw_party_frames(ui, game, x: float, y: float) -> None:
    """Small health bars of the other members under the player card (spec 15.3)."""
    party = game.state.party
    if not party:
        return
    me = game.state.me.get("id")
    for m in party["members"]:
        if m["uid"] == me:
            continue
        ui.fill(x, y, 96, 11, (20, 18, 15, 150))
        col = "#F4EBD9" if m["online"] else "#8E877A"
        if m["uid"] == party["leader"]:
            ui.fill(x + 2, y + 4, 3, 3, "#E9C46A")
        ui.text(m["name"][:14], x + 7, y + 5.5, 6, col, anchor="midleft")
        if m.get("hp") is not None:
            ui.progress(x + 60, y + 3, 33, 4, m["hp"] / 100, "#8C8C8C" if m.get("ghost") else "#BC4749")
        y += 12


# ------------------------------------------------------------------ the gate
class RealmGateScene(Scene):
    def __init__(self, game, rift: dict | None = None):
        super().__init__(game)
        self.rift = rift          # {"id", "realm", "n", "left"} when opened at a Khe Nứt Mực
        self.data: dict | None = None
        self.tab = "realms"
        self.next_fetch = 0.0
        self.busy = False

    def on_enter(self) -> None:
        self.fetch()

    def fetch(self) -> None:
        self.next_fetch = self.game.now + 3.0
        self.game.api.get("/realms", self._got, lambda e: None)

    def _got(self, d: dict) -> None:
        self.data = d
        self.game.state.party = d.get("party") if d.get("party") is not None else self.game.state.party
        self.game.state.realm_queue = d.get("queue")

    def update(self, dt, top):
        if self.game.now >= self.next_fetch:
            self.fetch()

    def send(self, msg: dict) -> None:
        if self.game.net is not None:
            self.game.net.send(msg)

    def draw_ui(self, ui):
        g = self.game
        ui.dim(110)
        x, y, w, h = 40, 18, 400, 234
        ui.panel(x, y, w, h, T.REALM_RIFT_TITLE if self.rift else T.REALM_GATE_TITLE)
        if not self.rift:
            tx = x + 10
            for key, label in (("realms", T.REALM_TAB_REALMS), ("math", T.REALM_TAB_MATH),
                               ("forge", T.REALM_TAB_FORGE)):
                bw = ui.text_size(label, 8)[0] + 14
                if ui.button(f"rg_tab_{key}", tx, y + 8, bw, 13, label, selected=self.tab == key):
                    self.tab = key
                tx += bw + 4
        body_y = y + 26 if not self.rift else y + 12
        if self.data is None:
            ui.text("...", x + w / 2, y + h / 2, 9, anchor="center")
        elif self.tab == "realms":
            self.draw_realms(ui, x, body_y, w)
        elif self.tab == "math":
            self.draw_math(ui, x, body_y, w)
        else:
            self.draw_forge(ui, x, body_y, w)
        if ui.button("rg_party", x + 12, y + h - 18, 70, 13, f"{T.PARTY_TITLE} (Y)", key=pygame.K_y):
            g.push(PartyScene(g))
        if ui.button("rg_close", x + w - 72, y + h - 18, 60, 13, T.CLOSE, key=pygame.K_ESCAPE):
            self.close()

    def draw_realms(self, ui, x, y, w):
        g = self.game
        party = g.state.party
        me = g.state.me.get("id")
        queue = g.state.realm_queue
        realms = self.data["realms"]
        if self.rift:
            realms = [r for r in realms if r["id"] == self.rift["realm"]]
        for r in realms:
            ui.fill(x + 10, y, w - 20, 74, "#EFE6D2")
            ui.text(r["name_vi"], x + 16, y + 4, 10, "#2B2B2B")
            ui.text(r["desc_vi"], x + 16, y + 16, 7, "#5A5A5A", max_w=w - 40)
            floor = r.get("floor") or 0
            ui.text(T.REALM_INFO.format(p=r["puzzles"], m=r["time_limit_minutes"], n=r.get("party_min", 2)),
                    x + 16, y + 38, 7, "#5A5A5A")
            ui.text(T.REALM_MATH_FLOOR.format(f=floor) if floor else T.REALM_MATH_NO_FLOOR, x + 16, y + 62, 7,
                    "#6A994E" if r["realm_ok"] else "#BC4749")
            ui.text(T.REALM_ENTRIES.format(n=r["entries_left"], d=r["daily"]), x + w - 18, y + 38, 7,
                    "#2B2B2B", anchor="topright")
            is_rift = r["kind"] == "rift"
            if is_rift and not self.rift:
                ui.text(T.REALM_RIFT_ONLY, x + 16, y + 50, 7, "#8E5AC8", max_w=w - 40)
            else:
                if is_rift:
                    left = self.rift.get("left", 0) - (g.now - self.rift.get("seen", g.now))
                    status, col = T.REALM_RIFT_LEFT.format(t=fmt_time(left)), "#8E5AC8"
                    is_open = left > 0
                elif r.get("open"):
                    status = T.REALM_OPEN.format(m=(r["closes_in"] or 0) // 60) if r.get("closes_in") else T.REALM_OPEN_ALWAYS
                    col, is_open = "#6A994E", True
                else:
                    status, col, is_open = T.REALM_CLOSED.format(t=fmt_wait(r.get("opens_in") or 0)), "#BC4749", False
                ui.text(status, x + 16, y + 50, 7, col)
                target = {"rift": self.rift["id"]} if is_rift else {"realm": r["id"]}
                ok = is_open and r["realm_ok"] and r["entries_left"] > 0
                bx = x + w - 18
                if party:
                    leader = party["leader"] == me
                    bw = 110
                    if ui.button(f"rg_enter_{r['id']}", bx - bw, y + 56, bw, 14,
                                 T.REALM_RIFT_ENTER if is_rift else T.REALM_ENTER, style="primary",
                                 enabled=ok and leader and len(party["members"]) >= 2,
                                 tooltip=None if leader else T.REALM_NEED_LEADER):
                        self.send({"t": "realm", "op": "enter", **target})
                        g.toast(T.REALM_ENTERING.format(name=r["name_vi"]), "#4A7CC8")
                else:
                    in_q = queue is not None and queue.get("realm") == r["id"]
                    bw = 110
                    if in_q:
                        ui.text(T.REALM_QUEUED.format(n=queue.get("waiting", 1)), bx - bw - 6, y + 63, 7, "#4A7CC8",
                                anchor="midright")
                        if ui.button(f"rg_unq_{r['id']}", bx - bw, y + 56, bw, 14, T.REALM_UNQUEUE):
                            self.send({"t": "realm", "op": "unqueue"})
                            g.state.realm_queue = None
                    elif ui.button(f"rg_q_{r['id']}", bx - bw, y + 56, bw, 14,
                                   T.REALM_RIFT_QUEUE if is_rift else T.REALM_QUEUE, style="gold", enabled=ok,
                                   tooltip=T.REALM_NEED_PARTY):
                        self.send({"t": "realm", "op": "queue", **target})
            y += 80
        if party:
            names = ", ".join(m["name"] for m in party["members"])
            ui.text(T.REALM_PARTY.format(names=names), x + 14, y + 2, 7, "#2B2B2B", max_w=w - 28)

    def draw_math(self, ui, x, y, w):
        """M10: the math bí cảnh. Entered alone or by the party's leader; each member is asked at
        their own floor, which the card shows."""
        g = self.game
        party = g.state.party
        me = g.state.me.get("id")
        for r in self.data.get("math_realms", []):
            ui.fill(x + 10, y, w - 20, 74, "#EFE6D2")
            ui.text(r["name_vi"], x + 16, y + 4, 10, "#2B2B2B")
            ui.text(r["desc_vi"], x + 16, y + 16, 7, "#5A5A5A", max_w=w - 40)
            floor = r.get("floor") or 0
            ui.text(T.REALM_MATH_FLOOR.format(f=floor) if floor else T.REALM_MATH_NO_FLOOR, x + 16, y + 40, 7,
                    "#6A994E" if floor else "#BC4749")
            ui.text(T.REALM_MATH_INFO.format(p=r["puzzles"], m=r["time_limit_minutes"]), x + 16, y + 51, 7, "#5A5A5A")
            ui.text(T.REALM_ENTRIES.format(n=r["entries_left"], d=r["daily"]), x + w - 18, y + 40, 7,
                    "#2B2B2B", anchor="topright")
            ok = bool(r.get("open")) and r["realm_ok"] and r["entries_left"] > 0
            leader = party is None or party["leader"] == me
            label = T.REALM_MATH_PARTY if party else T.REALM_MATH_SOLO
            if ui.button(f"rg_enter_{r['id']}", x + w - 128, y + 54, 110, 14, label, style="primary",
                         enabled=ok and leader, tooltip=None if leader else T.REALM_NEED_LEADER):
                self.send({"t": "realm", "op": "enter", "realm": r["id"]})
                g.toast(T.REALM_ENTERING.format(name=r["name_vi"]), "#4A7CC8")
            y += 80
        puzzles = self.data.get("puzzles", {})
        for kind in ("seal", "boss"):
            p = puzzles.get(kind)
            if not p:
                continue
            ui.text(p["name_vi"], x + 14, y, 8, "#2B2B2B")
            rr = ui.text(p["how_vi"], x + 14, y + 10, 6.5, "#5A5A5A", max_w=w - 28)
            y = max(y + 22, rr.bottom + 4)

    def draw_forge(self, ui, x, y, w):
        f = self.data["forge"]
        ui.text(T.REALM_FORGE_HINT.format(set=f["set_vi"], rarity=f["rarity_vi"]), x + 14, y + 2, 8, max_w=w - 28)
        ui.text(T.REALM_FORGE_HAVE.format(have=f["have"], need=f["fragments"], stones=f["stones"]), x + 14, y + 18, 8,
                "#6A994E" if f["have"] >= f["fragments"] else "#BC4749")
        ui.text(T.REALM_FORGE_BONUS.format(b2=f["bonus_vi"].get("2", ""), b4=f["bonus_vi"].get("4", "")),
                x + 14, y + 30, 7, "#8E5AC8")
        cy = y + 46
        for p in f["pieces"]:
            ui.fill(x + 14, cy, w - 28, 20, "#EFE6D2")
            ui.text(f"{p['name_vi']} · {p['slot_vi']}", x + 20, cy + 10, 8, anchor="midleft")
            if ui.button(f"rg_forge_{p['id']}", x + w - 84, cy + 3, 64, 14, T.REALM_FORGE_BTN, style="gold",
                         enabled=f["have"] >= f["fragments"] and not self.busy):
                self.forge(p)
            cy += 24

    def forge(self, piece: dict) -> None:
        g = self.game
        self.busy = True

        def ok(r):
            self.busy = False
            e = r["equipment"]
            g.state.me["spirit_stones"] = r.get("spirit_stones", g.state.me.get("spirit_stones"))
            g.toast(T.REALM_FORGE_DONE.format(name=e["name_vi"], rarity=e["rarity_vi"]), e.get("color", "#C99A3A"))
            g.refresh_inv()
            self.fetch()

        def err(e):
            self.busy = False
            g.api_error(e)
        g.api.post("/realm/forge", {"piece": piece["id"]}, ok, err)


# ------------------------------------------------------------------ inside a bí cảnh
class RealmView:
    MARKS = ("!", "→", "?", "OK")

    def __init__(self, scene):
        self.scene = scene
        self.game = scene.game
        self.run: dict | None = None
        self.room: dict | None = None
        self.puzzle: dict | None = None
        self.ended: dict | None = None
        self.loot: list[dict] = []
        self.left = 0.0                 # seconds left in the run, counted down locally
        self.left_at = 0.0
        self.room_shown = 0.0           # when the room started (for the "how to" banner)
        self.cleared_at: float | None = None
        self.cleared_in = 0.0
        self.end_at = 0.0
        self.notes: list[tuple[str, str, float]] = []
        self.marks: list[list] = []     # [x, y, icon, until]
        self.objs = [o for o in scene.map.objects if o.type == "realm_obj"]
        self.puzzle_at = 0.0

    # ------------------------------------------------------------ messages
    def note(self, text: str, color: str = "#F4EBD9") -> None:
        self.notes.append((text, color, self.game.now + 5.0))
        self.notes = self.notes[-4:]

    def on_net(self, m: dict) -> None:
        g = self.game
        ev = m.get("event")
        if ev == "start":
            self.run = m["run"]
            self.left, self.left_at = float(self.run.get("left", 0)), g.now
        elif ev == "room":
            self.room, self.puzzle = m, m.get("puzzle")
            self.left, self.left_at = float(m.get("left", self.left)), g.now
            self.room_shown, self.cleared_at, self.puzzle_at = g.now, None, g.now
        elif ev == "puzzle" and self.room and m.get("i") == self.room.get("i"):
            self.puzzle, self.puzzle_at = m.get("puzzle"), g.now
        elif ev == "cleared":
            self.cleared_at, self.cleared_in = g.now, float(m.get("next_in", 4))
            g.audio.play("coin")
        elif ev == "end":
            self.ended = m
            self.end_at = g.now + float(m.get("exit_in", 30))
            g.refresh_inv()
            g.refresh_me()
        elif ev == "loot":
            lt = m["loot"]
            self.loot.append(lt)
            g.on_xp(lt.get("xp"))
            if "spirit_stones" in lt:
                g.state.me["spirit_stones"] = lt["spirit_stones"]
            if lt.get("stage", "").startswith("room"):
                self.note(T.REALM_ROOM_LOOT.format(i=int(lt["stage"][4:]) + 1, n=lt.get("stones", 0)), "#E9C46A")
            if lt.get("locked"):
                self.note(T.locked_text(lt["locked"]), "#B8AE9A")
            g.refresh_inv()
        elif ev == "seal":      # someone answered a Trận Nhãn seal
            self.note((T.REALM_SEAL_OK if m.get("ok") else T.REALM_SEAL_BAD).format(by=m.get("by", "")),
                      "#B5D67A" if m.get("ok") else "#F08A8C")
        elif ev == "hint":
            self.note(m.get("text_vi", ""), "#E3D5BA")
        elif ev == "member_left":
            self.note(T.REALM_MEMBER_LEFT.get(m.get("reason"), "{name}").format(name=m.get("name", "")), "#F08A8C")
        elif ev == "revived":
            self.scene.ghost = False
            g.toast(T.REALM_REVIVED.format(hp=m.get("hp", 0)), "#6A994E")

    def on_fx(self, ev: dict) -> None:
        k = ev.get("k")
        fx = self.scene.fx
        x, y = ev.get("x", 0.0), ev.get("y", 0.0)
        if k == "mark":
            self.marks.append([x, y, self.MARKS[int(ev.get("i", 0)) % 4], self.game.now + 3.0])
        elif k == "pz":
            e = ev.get("e")
            if e in ("solve", "open", "seal"):
                fx.ink_to_light(x, y - 8)
            elif e == "fail":
                fx.burst(x, y - 8, "r", 16, 30)
                fx.shake = 0.3
            elif e == "ask":
                fx.burst(x, y - 4, "o", 10, 20)
            elif e == "wave":
                r = ev.get("r", 40)
                for i in range(18):
                    a = i / 18 * 6.283
                    fx.burst(x + math.cos(a) * r, y + math.sin(a) * r * 0.6, "K", 2, 16)
        elif k == "gshield":
            fx.float_text(f"{ev.get('n')}/{ev.get('need')}", x, y - 50, "#8CB8DA")

    # ------------------------------------------------------------ helpers
    @property
    def kind(self) -> str | None:
        return self.room.get("kind") if self.room else None

    @property
    def place(self) -> str | None:
        """The room of the map this room is played in (a seal room borrows one)."""
        return (self.room.get("place") or self.kind) if self.room else None

    def seal(self, o) -> dict | None:
        """Trận Nhãn: what the server says about this map object as a seal, if it is one."""
        if self.kind != "seal":
            return None
        return next((s for s in (self.puzzle or {}).get("seals", []) if s["name"] == o.name), None)

    def my_floor(self) -> int | None:
        me = self.game.state.me.get("id")
        return next((m.get("floor") for m in (self.run or {}).get("members", []) if m["uid"] == me), None)

    def room_objs(self, kind: str | None = None) -> list:
        return [o for o in self.objs if o.props.get("room") == self.place and (kind is None or o.props.get("kind") == kind)]

    def room_rect(self) -> pygame.Rect | None:
        """The current room with its walls, in world pixels."""
        if not self.place:
            return None
        o = next((o for o in self.scene.map.objects if o.type == "realm_room" and o.props.get("kind") == self.place), None)
        return pygame.Rect(int(o.x) - 16, int(o.y) - 16, int(o.w) + 32, int(o.h) + 32) if o else None

    def outside(self, surf, cx: int, cy: int) -> None:
        """Only the room the party stands in exists: the rest of the map is black."""
        r = self.room_rect()
        if r is None:
            return
        r = self.scene.view.rect(r)          # the camera's zoom (2x with the v2 art)
        w, h = surf.get_size()
        black = (10, 9, 12)
        for rect in ((0, 0, w, max(0, r.top)), (0, r.bottom, w, max(0, h - r.bottom)),
                     (0, r.top, max(0, r.left), r.height), (r.right, r.top, max(0, w - r.right), r.height)):
            if rect[2] > 0 and rect[3] > 0:
                surf.fill(black, rect)

    def time_left(self) -> float:
        return self.left - (self.game.now - self.left_at)

    def mark(self, wx: float, wy: float, icon: int = 0) -> None:
        if self.game.net is not None:
            self.game.net.send({"t": "mark", "x": max(0.0, wx), "y": max(0.0, wy), "i": icon})

    def leave(self) -> None:
        g = self.game

        def go():
            if g.net is not None:
                g.net.send({"t": "realm", "op": "leave"})
        if self.ended:
            go()
        else:
            g.message(T.REALM_LEAVE_CONFIRM, T.REALM_LEAVE, ok=T.REALM_LEAVE, cancel=T.CANCEL, on_ok=go)

    # ------------------------------------------------------------ drawing in the world
    def floor(self, surf, cx: int, cy: int, frame: int) -> None:
        """Props lying on the floor, drawn under everyone: the seals (the stones of the borrowed
        room: pedestals or the row of floor stones), the den's chest and the door."""
        kind = self.kind
        v = self.scene.view
        for o in self.room_objs():
            k = o.props.get("kind")
            x, y = v.to_screen(o.x, o.y)
            st = self.seal(o)
            if st is not None and k == "pedestal":   # glowing while unbroken, gold once broken
                surf.blit(realm_img(v, "pedestal", not st["broken"], st["busy"] or st["broken"]), (x, y))
            elif st is not None and k == "tile":
                state = "done" if st["broken"] else ("next" if st["busy"] else "idle")
                surf.blit(realm_img(v, "rune_tile", state), (x, y))
            elif k == "chest" and kind == "boss" and self.ended and self.ended.get("result") == "won":
                surf.blit(realm_img(v, "chest", True), (x, y))
            elif k == "exit":
                surf.blit(realm_img(v, "realm_exit", self.cleared_at is not None, frame % 2), (x, y - int(v.len(8))))

    def drawables(self, cx: int, cy: int, frame: int) -> list:
        """Standing props, sorted with the characters by their feet: the pillars (lit once their
        seal is broken or asking) and the statue of the pillar room."""
        out = []
        v = self.scene.view
        for o in self.room_objs():
            k = o.props.get("kind")
            if k == "pillar":
                st = self.seal(o)
                lit = st is not None and (st["broken"] or st["busy"])
                out.append((o.y + o.h, realm_img(v, "pillar", int(o.props.get("tone", 1)), lit), v.to_screen(o.x, o.y)))
            elif k == "statue":
                out.append((o.y + o.h, realm_img(v, "statue", frame % 2), v.to_screen(o.x, o.y)))
        return out

    # ------------------------------------------------------------ the HUD
    def draw_ui(self, ui, top: bool) -> None:
        g = self.game
        v = self.scene.view
        now = g.now
        for o in self.room_objs():   # the seal marks (sharp, at window resolution)
            st = self.seal(o)
            if st is not None:
                ox, oy = v.to_screen(o.x + o.w / 2, o.y + o.h / 2)
                ui.text(T.REALM_SEAL_BROKEN if st["broken"] else T.REALM_SEAL_MARK, ox, oy, 7,
                        "#6A994E" if st["broken"] else "#2B2B2B", anchor="center")
        for mk in list(self.marks):
            if mk[3] < now:
                self.marks.remove(mk)
                continue
            bob = math.sin(now * 8) * 2
            mx_, my_ = v.to_screen(mk[0], mk[1])
            ui.text(mk[2], mx_, my_ - v.len(30) + bob, 12, "#E9C46A", anchor="center")
        if self.run:
            name = self.run.get("name_vi", "")
            if self.room:
                label = T.REALM_ROOM.format(name=name, i=self.room["i"] + 1, n=self.room["n"], room=self.room["name_vi"])
            else:
                label = name
            label += "   " + fmt_time(self.time_left())
            w = ui.text_size(label, 8)[0] + 14
            ui.fill(240 - w / 2, 4, w, 13, (20, 18, 15, 200))
            ui.text(label, 240, 10.5, 8, "#F4EBD9" if self.time_left() > 60 else "#F08A8C", anchor="center")
        if self.room and now - self.room_shown < 8 and not self.ended:   # how this room works, for a while
            how = self.room.get("how_vi", "")
            ui.fill(100, 176, 280, 30, (20, 18, 15, 200))
            ui.text(how, 106, 179, 7, "#F4EBD9", max_w=268)
        y = 20
        for text, col, until in self.notes:
            if until > now:
                tw = ui.text_size(text, 7)[0] + 10
                ui.fill(240 - tw / 2, y, tw, 10, (20, 18, 15, 170))
                ui.text(text, 240, y + 5, 7, col, anchor="center")
                y += 11
        if self.cleared_at is not None and not self.ended:
            n = max(0, int(self.cleared_in - (now - self.cleared_at)) + 1)
            ui.text(T.REALM_CLEARED.format(n=n), 240, 110, 10, "#E9C46A", anchor="center")
        self.draw_card(ui)
        if self.ended:
            self.draw_result(ui, top)
        elif top and ui.button("realm_leave", 400, 238, 76, 12, T.REALM_LEAVE, size=7, style="dark"):
            self.leave()

    def draw_card(self, ui) -> None:
        """The room card, top right: the seals broken so far, or the boss's phase and shield."""
        if not self.room or self.ended:
            return
        pz = self.puzzle or {}
        x, y, w = 346, 22, 130
        lines: list[tuple] = []          # (text, size, color)
        kind = self.kind
        if kind == "seal":
            lines.append((T.REALM_SEAL_COUNT.format(n=pz.get("broken", 0), need=pz.get("need", 0)), 8, "#E9C46A"))
            if not pz.get("solved"):
                lines.append((T.REALM_SEAL_HOW, 7, "#F4EBD9"))
                missing = pz.get("missing") or []
                if missing and len((self.run or {}).get("members", [])) > 1:
                    lines.append((T.REALM_SEAL_WAIT.format(names=self._names(missing)), 7, "#8CB8DA"))
            if self.my_floor():
                lines.append((T.REALM_MATH_FLOOR.format(f=self.my_floor()), 7, "#B5D67A"))
        elif kind == "boss":
            lines.append((T.REALM_BOSS_PHASE.format(p=min(4, pz.get("phase", 1))), 8, "#F08A8C"))
            lines.append((T.REALM_BOSS_TONG_HOP, 7, "#E3D5BA"))
            if pz.get("shield"):
                lines.append((T.REALM_BOSS_SHIELD.format(n=pz.get("hits", 0), need=pz.get("need", 1)), 7, "#8CB8DA"))
            elif "hp" in pz:
                lines.append((T.REALM_BOSS_OPEN, 7, "#E9C46A"))
        if pz.get("fails"):
            lines.append((T.REALM_FAILS.format(n=pz["fails"]), 6, "#F08A8C"))

        def height(text: str, size: float) -> float:
            n = len(ui.f.wrap(text, size, int((w - 12) * ui.s), ui.s)) or 1
            return n * size * 1.4 + 1
        h = 20 + sum(height(t, size) for t, size, _ in lines) + (8 if kind == "boss" and "hp" in pz else 0)
        ui.fill(x, y, w, h, (20, 18, 15, 200))
        ui.border(x, y, w, h, "#8B5A2B")
        ui.text(self.room.get("name_vi", ""), x + 6, y + 4, 8, "#E9C46A")
        cy = y + 16
        for text, size, col in lines:
            r = ui.text(text, x + 6, cy, size, col, max_w=w - 12)
            cy += max(height(text, size), r.h + 1)
        if kind == "boss" and "hp" in pz:
            ui.progress(x + 6, y + h - 9, w - 12, 4, pz["hp"] / 100, "#BC4749")

    def _names(self, uids: list[int]) -> str:
        me = self.game.state.me.get("id")
        names = []
        for uid in uids:
            if uid == me:
                names.append(T.REALM_YOUR)
            else:
                m = next((x for x in (self.run or {}).get("members", []) if x["uid"] == uid), None)
                names.append(m["name"] if m else "?")
        return ", ".join(names)

    def draw_result(self, ui, top: bool) -> None:
        g = self.game
        e = self.ended
        ui.dim(120)
        x, y, w, h = 110, 30, 260, 206
        won = e.get("result") == "won"
        ui.panel(x, y, w, h, T.REALM_RESULT.get(e.get("result"), ""))
        secs = int(e.get("time", 0))
        ui.text(T.REALM_RESULT_INFO.format(m=secs // 60, s=secs % 60, f=e.get("flawless", 0), p=e.get("puzzles", 0)),
                x + w / 2, y + 8, 8, anchor="midtop")
        cy = y + 22
        if won and e.get("fast"):
            ui.text(T.REALM_FAST, x + w / 2, cy, 7, "#6A994E", anchor="midtop")
            cy += 11
        if won and e.get("fragments"):
            ui.text(T.REALM_FRAGMENTS.format(n=e.get("fragments", 0)), x + w / 2, cy, 8, "#8E5AC8", anchor="midtop")
            cy += 13
        ui.text(T.REALM_YOUR_LOOT, x + 12, cy, 8, "#8B5A2B")
        cy += 12
        stones = sum(lt.get("stones", 0) for lt in self.loot)
        jade = sum(lt.get("jade", 0) for lt in self.loot)
        items: dict[str, int] = {}
        for lt in self.loot:
            for it in lt.get("items", []):
                items[it["name_vi"]] = items.get(it["name_vi"], 0) + it["qty"]
        parts = [T.REALM_LOOT_STONES.format(n=stones)] + ([T.REALM_LOOT_JADE.format(n=jade)] if jade else [])
        parts += [f"{k} ×{v}" for k, v in items.items()]
        ui.text(" · ".join(parts), x + 12, cy, 7, "#2B2B2B", max_w=w - 24)
        cy += 30
        for lt in self.loot:
            for eq in lt.get("equipment", []):
                ui.text(f"{eq['name_vi']} · {eq.get('rarity_vi', '')}", x + 12, cy, 8, eq.get("color", "#6A994E"))
                cy += 11
        left = max(0, int(self.end_at - g.now))
        if ui.button("realm_back", x + w / 2 - 60, y + h - 20, 120, 14, T.REALM_BACK.format(n=left), style="primary",
                     enabled=top, key=pygame.K_RETURN if top else None):
            self.leave()
