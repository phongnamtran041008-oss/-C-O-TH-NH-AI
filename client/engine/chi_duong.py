"""Chỉ Đường: the destination being led to and the way to it, kept on the game across zone
changes (a zone change builds a new world scene; this does not move). docs/CHI_DUONG.md.

A destination is a dict like the server's (GET /nav/destinations, systems/navigation.py):
{kind, zone, khu, name_vi, land_vi, x, y, ...}. "home" has zone "abode" and ends at the abode's
gate in the village (`via`): walking in is the player's own step.

`update(scene)` runs every frame from the HUD: it finds the next gate (engine/navigator.py's
zone route), keeps one `Leg` for the scene's map and that gate or the final point, gives it a
few milliseconds, reads the way a few times a second and says "Đã tới ..." on arrival.
"""
from __future__ import annotations

import math

from .. import strings_nav_vi as N
from . import navigator as nv

BUDGET = 0.003            # seconds of search per frame
SEARCH_BUDGET = 0.005     # ... while there is no way yet (the arrow is pale): the first arrow sooner
READ_EVERY = 0.1          # seconds between two readings of the way
ROUTE_EVERY = 0.5         # ... of the way drawn on the maps
ROUTE_CELLS = 900         # how far down the way the maps draw (8 px cells)
ARRIVE_PX = 26
EXIT_PX = 30
REFRESH_EVERY = 20.0      # seconds between two GET /nav/destinations
FRESH = 3.0               # the picker and the big map ask again when the answer is older than this
HUB, HOME = "truc_lam_thon", "abode"


def of(game) -> "ChiDuong":
    nav = game.__dict__.get("_chi_duong")
    if nav is None:
        nav = game.__dict__["_chi_duong"] = ChiDuong(game)
    return nav


def scene_zone(scene) -> str | None:
    if getattr(scene, "realm", None) is not None:          # a bí cảnh: no leading there
        return None
    z = getattr(scene, "zone_id", None)
    if z:
        return z
    return HOME if type(scene).__name__ == "AbodeScene" else None


def khu_objects(tmap) -> list:
    """The khu of a map in map order: (rect (x, y, w, h), props) - the client reads the same map
    objects the server does (realtime/dia_do.py)."""
    cached = getattr(tmap, "_nav_khu", None)
    if cached is None:
        cached = [((o.x, o.y, o.w, o.h), o.props) for o in tmap.find("khu")]
        try:
            tmap._nav_khu = cached
        except AttributeError:
            pass
    return cached


def khu_at(tmap, x: float, y: float):
    for (rx, ry, rw, rh), props in khu_objects(tmap):
        if rx <= x <= rx + rw and ry <= y <= ry + rh:
            return (rx, ry, rw, rh), props
    return None


def num(v, default: int = 0) -> int:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return default


def khu_dest(zone: str, rect, props: dict, land_vi: str = "") -> dict:
    """A destination for a khu picked on the big map."""
    x, y, w, h = rect
    return {"kind": "khu", "zone": zone, "khu": props.get("khu") or "", "name_vi": props.get("name_vi") or "",
            "land_vi": land_vi, "band": num(props.get("band")), "stage_min": num(props.get("stage_min")),
            "stage_max": num(props.get("stage_max")),
            "x": num(props.get("anchor_x"), int(x + w / 2)), "y": num(props.get("anchor_y"), int(y + h / 2))}


class ChiDuong:
    def __init__(self, game):
        self.game = game
        self.data: dict | None = None          # the last GET /nav/destinations
        self.data_at = -1e9
        self.asking = False
        self.failed = False
        self.dest: dict | None = None
        self.leg: nv.Leg | None = None
        self.leg_key = None
        self.gates: list = []                  # the gates still to go through, the next one first
        self.reading: nv.Reading | None = None
        self.read_t = -1e9
        self.route_t = -1e9
        self.route: list = []                  # world points of the way in this zone (for the maps)
        self.after_px = 0.0                    # a guess of the walk beyond this zone
        self.zone: str | None = None
        self.status = ""                       # "" | searching | path | straight | here | exit | noroute
        self.khu_now = None                    # the khu the player stands in (its id), for the banner
        self.banner = None                     # (title, line, warn, until)
        self.khu_check_t = -1e9

    # ------------------------------------------------------------ the server's answer
    def refresh(self, force: bool = False, then=None) -> None:
        g = self.game
        if self.asking or (not force and g.now - self.data_at < REFRESH_EVERY and self.data is not None):
            if then and self.data is not None:
                then()
            return
        self.asking = True

        def ok(d):
            self.asking, self.failed = False, False
            if isinstance(d, dict):
                self.data, self.data_at = d, g.now
            if then:
                then()

        def err(e):
            self.asking, self.failed = False, True
        g.api.get("/nav/destinations", ok, err)

    @property
    def working_stage(self) -> int | None:
        st = (self.data or {}).get("stage") or {}
        return st.get("working")

    @property
    def realm_vi(self) -> str:
        return ((self.data or {}).get("stage") or {}).get("realm_vi") or N.REALM_DEFAULT

    # ------------------------------------------------------------ choosing
    def local(self, kind: str) -> dict:
        """home / village from the maps themselves (before the server answered, or offline)."""
        hub = nv.world_zones().get(HUB)
        if kind == "home":
            x, y = (hub.spawns.get("from_abode") if hub else None) or (0, 0)
            return {"kind": "home", "zone": HOME, "via": HUB, "khu": None, "name_vi": "Động Phủ", "x": x, "y": y}
        x, y = (hub.spawns.get("spawn") if hub else None) or (0, 0)
        return {"kind": "village", "zone": HUB, "khu": None, "name_vi": "Trúc Lâm Thôn", "x": x, "y": y}

    def pick(self, kind: str) -> dict:
        d = (self.data or {}).get(kind)
        return d if isinstance(d, dict) else self.local(kind)

    def set_dest(self, d: dict | None, here: str | None = None) -> bool:
        """Lead to `d` (None: stop). `here` is the zone the player stands in."""
        g = self.game
        self._reset()
        if d is None:
            self.dest = None
            g.toast(N.OFF, "#8E877A")
            return False
        if d.get("kind") == "home" and here == HOME:
            self.dest = None
            g.toast(N.ALREADY_HOME, "#8E877A")
            return False
        self.dest = dict(d)
        name = self.label()
        if nv.zone_route(nv.world_zones(), here or self.final_zone(), self.final_zone()) is None:
            g.toast(N.NO_ROUTE.format(name=name), "#BC4749")
        else:
            g.toast(N.SET.format(name=name), "#C99A3A")
        return True

    def clear(self) -> None:
        self._reset()
        self.dest = None

    def _reset(self) -> None:
        self.leg = None
        self.leg_key = None
        self.reading = None
        self.route = []
        self.gates = []
        self.status = ""
        self.read_t = self.route_t = -1e9

    def final_zone(self) -> str | None:
        d = self.dest
        if d is None:
            return None
        if d.get("kind") == "home":
            return d.get("via") or HUB
        return d.get("zone")

    def label(self) -> str:
        d = self.dest or {}
        if d.get("kind") == "home":
            return "Động Phủ"
        name = d.get("name_vi") or ""
        land = d.get("land_vi") or ""
        return f"{name} ({land})" if land and land != name else name

    # ------------------------------------------------------------ every frame
    def update(self, scene) -> None:
        g = self.game
        zone = scene_zone(scene)
        if zone != self.zone and zone is not None and self.data is not None:
            self.refresh()                   # a new zone: the stage may have moved (throttled)
        self.zone = zone
        if zone is not None and getattr(scene, "map", None) is not None:
            self._watch_khu(scene, zone)
        if self.dest is None or zone is None:
            return
        tmap = scene.map
        final = self.final_zone()
        p = scene.player
        point = (float(self.dest.get("x", 0)), float(self.dest.get("y", 0)))
        if zone == final:
            gate = None
            key = ("point", id(tmap), point)
        else:
            route = nv.zone_route(nv.world_zones(), zone, final)
            if not route:
                self.status = "noroute"
                return
            gate = route[0]
            key = ("gate", id(tmap), gate.rect)
            self.gates = route
        if key != self.leg_key:
            self.leg_key = key
            grid = nv.grid_for(tmap)
            self.leg = nv.Leg(grid, goal_rect=gate.rect if gate else None, goal_point=None if gate else point)
            self.reading = None
            self.route = []
            self.read_t = self.route_t = -1e9
            self.after_px = nv.estimate_after(nv.world_zones(), self.gates, point) if gate else 0.0
            if gate is None:
                self.gates = []
        self.leg.step(BUDGET if self.leg.ready or self.status == "path" else SEARCH_BUDGET)
        now = g.now
        if now - self.read_t >= READ_EVERY or self.reading is None:
            self.read_t = now
            want_route = now - self.route_t >= ROUTE_EVERY
            r = self.leg.read(p.x, p.y, route_cells=ROUTE_CELLS if want_route else 0)
            if want_route and r.mode == "path":
                self.route_t = now
                self.route = r.route
            elif r.mode != "path":
                self.route = []
            self.reading = r
            self.status = r.mode
        if gate is None:
            if self._arrived(scene, tmap, p, point):
                self._arrive()
        elif gate.kind == "exit":            # the abode's gate is pressed (E), not walked into
            gx, gy, gw, gh = gate.rect
            dx = max(gx - p.x, 0.0, p.x - (gx + gw))
            dy = max(gy - p.y, 0.0, p.y - (gy + gh))
            if math.hypot(dx, dy) < EXIT_PX or (self.reading is not None and self.reading.mode == "here"):
                self.status = "exit"

    def _arrived(self, scene, tmap, p, point) -> bool:
        """At the point (a khu's anchor: its heart, on its road - not its border, which on a
        giant land may lie behind a wall from where the player stands)."""
        if math.hypot(point[0] - p.x, point[1] - p.y) < ARRIVE_PX:
            return True
        return self.reading is not None and self.reading.mode == "here"

    def _arrive(self) -> None:
        d = self.dest
        msg = N.ARRIVED_HOME if d.get("kind") == "home" else N.ARRIVED.format(name=self.label())
        self.game.toast(msg, "#6A994E", 3.5)
        self.clear()

    # ------------------------------------------------------------ the khu the player is in
    def _watch_khu(self, scene, zone: str) -> None:
        g = self.game
        if g.now - self.khu_check_t < 0.25:
            return
        self.khu_check_t = g.now
        hit = khu_at(scene.map, scene.player.x, scene.player.y)
        kid = (zone, hit[1].get("khu")) if hit else None
        if kid == self.khu_now:
            return
        self.khu_now = kid
        if hit is None:
            return
        props = hit[1]
        lo, hi = num(props.get("stage_min")), num(props.get("stage_max"))
        band = num(props.get("band"))
        if band == 0 or str(props.get("safe", "")).lower() == "true":
            line, warn = N.SAFE, False
        else:
            fmt = N.BAND_FIT_ONE if lo == hi else N.BAND_FIT
            line = fmt.format(realm=self.realm_vi, lo=lo, hi=hi)
            ws = self.working_stage
            warn = ws is not None and lo > ws
            if warn:                         # plainly: above the stage, the monsters are stronger
                rng = f"{lo}-{hi}" if lo != hi else f"{lo}"
                line = N.WARN_LINE.format(realm=self.realm_vi, r=rng)
        title = props.get("name_vi") or props.get("khu") or ""
        band_vi = N.BAND_NAMES.get(band, "")
        if band_vi and band_vi not in title:
            title = f"{title} · {band_vi}"
        self.banner = (title, line, warn, None)      # the HUD shows it when the toasts allow

    # ------------------------------------------------------------ what the HUD shows
    def arrow(self, scene):
        """(angle in radians on screen, mode) of the arrow, or None (nothing to show)."""
        if self.dest is None or self.reading is None or self.status in ("", "noroute"):
            return None
        p = scene.player
        ax, ay = self.reading.aim
        if self.status in ("here",):
            return None
        return math.atan2(ay - p.y, ax - p.x), self.status

    def distance_px(self) -> float | None:
        if self.reading is None:
            return None
        return self.reading.dist_px + self.after_px

    def above_stage(self, lo) -> bool:
        """Does a khu starting at stage `lo` lie above the player's working stage?"""
        ws = self.working_stage
        return ws is not None and lo is not None and num(lo) > ws

    def plate(self) -> tuple[str, str, str, bool] | None:
        """(the goal's name, its distance ("60 trượng" / "ngay đây"), a second line or "", is that
        line a warning). The name is the khu's alone: the land is in the second line while there
        are gates to go through, the khu's band and stages once in its land."""
        d = self.dest
        if d is None:
            return None
        name = "Động Phủ" if d.get("kind") == "home" else (d.get("name_vi") or self.label())
        dist = self.distance_px()
        tr = nv.truong(dist) if dist is not None else 0
        far = N.PLATE_DIST.format(d=tr) if tr else N.PLATE_HERE
        sub, warn = "", False
        if self.status == "searching":
            sub = N.SEARCHING
        elif self.status == "straight":
            sub, warn = N.STRAIGHT, True
        elif self.status == "exit":
            sub = N.PRESS_EXIT
        elif self.gates:
            from .. import strings_vi as T
            sub = N.VIA_GATE.format(zone=T.ZONE_NAMES.get(self.gates[0].target, self.gates[0].target))
        elif d.get("khu") and num(d.get("band")) > 0:
            lo, hi = num(d.get("stage_min")), num(d.get("stage_max"))
            fit = (N.BAND_FIT_ONE if lo == hi else N.BAND_FIT).format(realm=self.realm_vi, lo=lo, hi=hi)
            sub = f"{N.BAND_NAMES.get(num(d.get('band')), '')} · {fit}"
            if self.above_stage(lo):
                sub = f"{N.BAND_NAMES.get(num(d.get('band')), '')} · tầng {lo}-{hi} · {N.TOO_HIGH_SHORT}"
                warn = True
        return name, far, sub, warn

    def draw_on_minimap(self, ui, mm, x: float, y: float, scene) -> None:
        """The way and the goal on a minimap (engine/minimap.py), clipped to it by the caller."""
        from .minimap import ROUTE, polyline
        if self.dest is None:
            return
        run: list = []                  # only the pieces of the way inside the window (and one point past)
        prev = None
        for px, py in self.route:
            a, b = mm.to_mm(px, py)
            q = (x + a, y + b)
            if mm.inside(a, b, 6):
                if not run and prev is not None:
                    run.append(prev)
                run.append(q)
            elif run:
                run.append(q)
                polyline(ui, run, ROUTE, 1)
                run = []
            prev = q
        if len(run) >= 2:
            polyline(ui, run, ROUTE, 1)
        goal = None
        if self.leg is not None:
            goal = self.leg.aim
        if goal is None:
            return
        gx, gy = mm.to_mm(*goal)
        w, h = mm.size
        pulse = 1 if int(self.game.now * 3) % 2 else 0
        if mm.inside(gx, gy):
            r = 2 + pulse
            ui.fill(x + gx - r - 1, y + gy - r - 1, 2 * r + 2, 2 * r + 2, "#2B1D0E")
            ui.fill(x + gx - r, y + gy - r, 2 * r, 2 * r, "#F2C14E")
        else:                       # off the window: a mark on its edge, toward the goal
            cx, cy = w / 2, h / 2
            dx, dy = gx - cx, gy - cy
            s = min((w / 2 - 2) / abs(dx) if dx else 1e9, (h / 2 - 2) / abs(dy) if dy else 1e9)
            ex, ey = cx + dx * s, cy + dy * s
            ui.fill(x + ex - 2, y + ey - 2, 4, 4, "#2B1D0E")
            ui.fill(x + ex - 1, y + ey - 1, 2 + pulse, 2 + pulse, "#F2C14E")
