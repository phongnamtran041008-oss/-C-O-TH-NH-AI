#!/usr/bin/env python3
"""Checks every map of the world (docs/DAI_DIA_DO.md); registered in tools/check_all.py.

    python tools/check_maps.py              every map: the problems, then OK or FAIL
    python tools/check_maps.py --report     also the khu table of every banded map

For every map in server/maps:

* the client's copy (client/assets/maps) is byte-identical, and its size is the one
  docs/DAI_DIA_DO.md lists;
* with the server's foot box (10 x 6 px, server/app/realtime/movement.py), walking from `spawn`
  reaches every spawn, portal, khu anchor, monster area (most of its walkable tiles), weapon spot,
  beast, NPC, interact and sign; a spot that `needs` Đạp Kiếm Lướt (world_plan.json) is reached
  by one glide of at most the glide's max_px over water or ink instead, and not on foot;
* every portal leads to a map and a spawn that exist; every prop's sprite has a picture;
* khu: ids unique in the whole world, band 0..3, the stage range of their band
  (data/math/dia_do.json), the anchor inside the khu; camps are band 0;
* monster areas of a banded map: inside the khu they name, with its band, a monster that exists,
  of this land (a land's creatures stay in their land), no boss, the quái lỗi sai only in band 1
  of Kiếm Trủng Sơn; an elite alone in its area; per khu at least two kinds and at most a handful
  of elites; nothing within the clearance of a gate, a spawn or a camp; the density of
  tiles_per_monster; at most max_monsters_per_land monsters on any map;
* every text a player reads on the map (khu, poi, signs) can be drawn by the game's fonts.
"""
from __future__ import annotations

import json
import re
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))

TILE = 16
SERVER_MAPS = ROOT / "server" / "maps"
CLIENT_MAPS = ROOT / "client" / "assets" / "maps"
DOC = ROOT / "docs" / "DAI_DIA_DO.md"
DATA = ROOT / "server" / "data"
SPRITES_PY = ROOT / "client" / "engine" / "sprites.py"
WIRING = ROOT / "client" / "assets" / "v2" / "wiring.json"
GLIDE_TOL = 1.0      # px


def _json(p: Path) -> dict:
    return json.loads(p.read_text("utf-8"))


def _props(o: dict) -> dict:
    return {p["name"]: p["value"] for p in o.get("properties", [])}


def _int(v, d: int = -1) -> int:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return d


def doc_sizes() -> dict[str, tuple[int, int]]:
    """zone -> (w, h) from the table of docs/DAI_DIA_DO.md: | `zone` | name | W x H | ..."""
    out = {}
    if not DOC.is_file():
        return out
    for line in DOC.read_text("utf-8").splitlines():
        mm = re.match(r"\|\s*`([a-z_0-9]+)`\s*\|[^|]*\|\s*(\d+)\s*[x×]\s*(\d+)\s*\|", line)
        if mm:
            out[mm.group(1)] = (int(mm.group(2)), int(mm.group(3)))
    return out


def known_sprites() -> set[str]:
    names = set(re.findall(r'name == "([a-z_]+)"', SPRITES_PY.read_text("utf-8")))
    w = _json(WIRING)
    for sec in ("props", "buildings"):
        names |= {k for k in w.get(sec, {}) if not k.startswith("_")}
    return names


# ------------------------------------------------------------------ walking
class Walk:
    """The tiles a character can stand on and walk between, from a start (four ways). A tile is
    walkable when the foot box at its middle (a little low) is free; a step between two tiles also
    needs the box free half way."""

    def __init__(self, zmap):
        self.z = zmap
        self.cols, self.rows = zmap.width_px // TILE, zmap.height_px // TILE
        self._ok: dict = {}

    def ok(self, x: int, y: int) -> bool:
        k = (x, y)
        if k not in self._ok:
            self._ok[k] = 0 <= x < self.cols and 0 <= y < self.rows and \
                not self.z.collider.blocked(x * TILE + TILE / 2, y * TILE + 12)
        return self._ok[k]

    def region(self, start: tuple[int, int]) -> set:
        if not self.ok(*start):
            return set()
        seen, q = {start}, deque([start])
        col = self.z.collider
        while q:
            x, y = q.popleft()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if (nx, ny) in seen or not self.ok(nx, ny):
                    continue
                mx, my = (x + nx) / 2 * TILE + TILE / 2, (y + ny) / 2 * TILE + 12
                if col.blocked(mx, my):
                    continue
                seen.add((nx, ny))
                q.append((nx, ny))
        return seen


def feet_tile(x: float, y: float) -> tuple[int, int]:
    return int(x // TILE), int((y - 1) // TILE)


def near_reached(foot: set, x0: float, y0: float, x1: float, y1: float, pad: int = 1) -> bool:
    """Is some tile of a rectangle (pixels), or right next to it, reached?"""
    for ty in range(int(y0 // TILE) - pad, int((y1 - 1) // TILE) + pad + 1):
        for tx in range(int(x0 // TILE) - pad, int((x1 - 1) // TILE) + pad + 1):
            if (tx, ty) in foot:
                return True
    return False


# ------------------------------------------------------------------ the checks
def check_map(zone: str, ctx: dict, report: list | None = None) -> list[str]:
    from app.realtime import maps as rmaps
    from app.learning import math_tree
    out: list[str] = []
    where = f"map {zone}"
    spath, cpath = SERVER_MAPS / f"{zone}.tmj", CLIENT_MAPS / f"{zone}.tmj"
    raw = spath.read_bytes()
    if not cpath.is_file() or cpath.read_bytes() != raw:
        out.append(f"{where}: client/assets/maps/{zone}.tmj is not byte-identical to server/maps (run tools/gen_maps.py)")
    data = json.loads(raw)
    size = (data["width"], data["height"])
    want = ctx["sizes"].get(zone)
    if want is None:
        out.append(f"{where}: docs/DAI_DIA_DO.md does not list its size ({size[0]} x {size[1]})")
    elif want != size:
        out.append(f"{where}: is {size[0]} x {size[1]}, docs/DAI_DIA_DO.md says {want[0]} x {want[1]}")
    objs = [o for l in data["layers"] if l["type"] == "objectgroup" and l["name"] != "collision" for o in l["objects"]]
    zmap = rmaps.parse(spath)
    zone_id = ctx["map_zone"].get(zone)
    land_id = ctx["zones"].get(zone_id, {}).get("land") if zone_id else None
    land = ctx["lands"].get(land_id) if land_id else None
    # ---- sprites
    for o in objs:
        sp = _props(o).get("sprite")
        if sp and sp not in ctx["sprites"]:
            out.append(f"{where}: object {o.get('name')!r} draws sprite {sp!r}, which has no picture")
    # ---- portals
    for p in zmap.portals:
        tgt, ts = p.props.get("target"), p.props.get("target_spawn")
        tz = ctx["zones"].get(tgt or "")
        tmap = (tz or {}).get("map") or (tgt if tz and (SERVER_MAPS / f"{tgt}.tmj").is_file() else None)
        if not tmap:
            out.append(f"{where}: portal {p.name} leads to {tgt!r}, no zone with a map")
            continue
        tm = rmaps.load(tmap) if (SERVER_MAPS / f"{tmap}.tmj").is_file() else None
        if tm is None or (ts and ts not in tm.spawns):
            out.append(f"{where}: portal {p.name} lands on spawn {ts!r}, which map {tmap} has not")
    if zone in ("bi_canh",):          # the rooms of a bí cảnh are not joined by corridors
        return out
    # ---- walking
    walk = Walk(zmap)
    start = zmap.spawns.get("spawn")
    if start is None:
        return out + [f"{where}: no `spawn`"]
    foot = walk.region(feet_tile(*start))
    if not foot:
        return out + [f"{where}: `spawn` stands on a solid tile"]
    for name, (x, y) in zmap.spawns.items():
        if feet_tile(x, y) not in foot and not near_reached(foot, x, y - 1, x + 1, y, 0):
            out.append(f"{where}: spawn {name} cannot be walked to from `spawn`")
    for p in zmap.portals:
        if not near_reached(foot, p.x, p.y, p.x + p.w, p.y + p.h, 1):
            out.append(f"{where}: portal {p.name} cannot be walked to")
    for o in objs:
        t = o.get("type")
        if t in ("npc", "interact", "sign"):
            if not near_reached(foot, o["x"], o["y"], o["x"] + o["width"], o["y"] + o["height"], 1):
                out.append(f"{where}: {t} {o.get('name')!r} at tile "
                           f"({int(o['x'] // TILE)}, {int(o['y'] // TILE)}) cannot be walked to")
    glide = ctx["glide"]
    gmax = float(glide.get("max_px", 80))

    def spot(kind: str, pos, needs) -> None:
        tx, ty = pos
        if not walk.ok(tx, ty):
            out.append(f"{where}: {kind} at {list(pos)} is not a walkable tile")
            return
        if not needs:
            if (tx, ty) not in foot:
                out.append(f"{where}: {kind} at {list(pos)} cannot be walked to from `spawn`")
            return
        if (tx, ty) in foot:
            out.append(f"{where}: {kind} at {list(pos)} needs {needs}, yet it can be walked to")
        elif needs == "dap_kiem_luot":
            g = dict(glide, max_px=min(gmax, float(glide.get("max_px", gmax))))
            if not math_tree.glide_reaches(zmap, foot, walk.region((tx, ty)), g):
                out.append(f"{where}: {kind} at {list(pos)} needs Đạp Kiếm Lướt, but no glide of at most "
                           f"{int(gmax)} px from where a player walks reaches it")
    if land_id:
        for p in ctx["plan"].get("weapons_placed", []):
            if p.get("land") == land_id and isinstance(p.get("pos"), list):
                spot(f"weapon spot {p['weapon']} {p['quality']}", p["pos"], p.get("needs"))
        for b in ctx["plan"].get("beasts", []):
            if b.get("land") == land_id and isinstance(b.get("pos"), list):
                spot(f"beast {b['id']}", b["pos"], b.get("needs"))
    # ---- khu
    band_rows = ctx["bands"]
    khu_rects = {}
    camps = []
    for k in zmap.khu:
        p = k.props
        kid = k.name
        w = f"{where}: khu {kid}"
        if kid in ctx["khu_seen"]:
            out.append(f"{w}: the id is already a khu of map {ctx['khu_seen'][kid]}")
        ctx["khu_seen"][kid] = zone
        band = _int(p.get("band"))
        realm = p.get("realm") or "luyen_khi"
        if band not in (0, 1, 2, 3):
            out.append(f"{w}: band must be 0..3")
        elif band:
            row = band_rows.get(realm, {}).get(str(band))
            if row is None:
                out.append(f"{w}: no band {band} in realm {realm} (data/math/dia_do.json)")
            elif (_int(p.get("stage_min")), _int(p.get("stage_max"))) != (row["stage_min"], row["stage_max"]):
                out.append(f"{w}: stages {p.get('stage_min')}-{p.get('stage_max')}, band {band} is "
                           f"{row['stage_min']}-{row['stage_max']}")
        else:
            camps.append((k.x, k.y, k.x + k.w, k.y + k.h))
            if str(p.get("safe", "")).lower() != "true":
                out.append(f"{w}: a band 0 khu is a safe place (safe=true)")
        if not p.get("name_vi"):
            out.append(f"{w}: needs name_vi")
        ax, ay = _int(p.get("anchor_x")), _int(p.get("anchor_y"))
        if not k.contains(ax, ay):
            out.append(f"{w}: its anchor ({ax}, {ay}) lies outside it")
        if feet_tile(ax, ay) not in foot:
            out.append(f"{w}: its anchor ({ax}, {ay}) cannot be walked to from `spawn`")
        khu_rects[kid] = (k, band, realm)
    # ---- monsters
    rules = ctx["rules"]
    clear = int(rules["clearance_tiles"]) * TILE
    keep_out = [(p.x, p.y, p.x + p.w, p.y + p.h) for p in zmap.portals]
    keep_out += [(x - 1, y - 1, x + 1, y + 1) for (x, y) in zmap.spawns.values()]
    keep_out += camps
    total = sum(int(a.props.get("count", 1)) for a in zmap.monster_areas)
    if total > int(rules["max_monsters_per_land"]):
        out.append(f"{where}: {total} monsters, more than max_monsters_per_land {rules['max_monsters_per_land']}")
    banded = bool(zmap.khu)
    per_khu: dict[str, dict] = {}
    lo, hi = rules["tiles_per_monster"]
    for a in zmap.monster_areas:
        p = a.props
        kind = p.get("monster")
        w = f"{where}: monster area {a.name}"
        info = ctx["monsters"].get(kind)
        if info is None:
            out.append(f"{w}: monster {kind!r} does not exist")
            continue
        if land and info.get("land") and info["land"] != land_id:
            out.append(f"{w}: {kind} belongs to land {info['land']}, not {land_id}")
        if not banded:
            continue
        kid = p.get("khu")
        if kid not in khu_rects:
            out.append(f"{w}: names khu {kid!r}, which this map has not")
            continue
        k, band, _realm = khu_rects[kid]
        if _int(p.get("band")) != band or band == 0:
            out.append(f"{w}: band {p.get('band')}, its khu {kid} is band {band}")
        if not (k.x <= a.x and k.y <= a.y and a.x + a.w <= k.x + k.w and a.y + a.h <= k.y + k.h):
            out.append(f"{w}: does not lie inside its khu {kid}")
        rank = info.get("rank", "normal")
        if rank == "boss":
            out.append(f"{w}: a boss ({kind}) in a wild land")
        if info.get("skill") and (land_id != "kiem_trung_son" or band != 1):
            out.append(f"{w}: the quái lỗi sai {kind} stay in band 1 of Kiếm Trủng Sơn")
        count = int(p.get("count", 1))
        if rank == "elite" and count != 1:
            out.append(f"{w}: an elite stands alone in its area (count {count})")
        for (x0, y0, x1, y1) in keep_out:
            dx = max(x0 - (a.x + a.w), a.x - x1, 0)
            dy = max(y0 - (a.y + a.h), a.y - y1, 0)
            if max(dx, dy) < clear:
                out.append(f"{w}: within {rules['clearance_tiles']} tiles of a gate, a spawn or a camp")
                break
        tiles = [(tx, ty) for ty in range(int(a.y // TILE), int((a.y + a.h - 1) // TILE) + 1)
                 for tx in range(int(a.x // TILE), int((a.x + a.w - 1) // TILE) + 1)]
        walkable = [t for t in tiles if walk.ok(*t)]
        reached = [t for t in walkable if t in foot]
        if not walkable or len(reached) < 0.6 * len(walkable):
            out.append(f"{w}: only {len(reached)} of its {len(walkable)} walkable tiles can be walked to")
        if count >= 2 and not (0.75 * lo <= len(walkable) / count <= 1.5 * hi):
            out.append(f"{w}: {len(walkable) / count:.0f} walkable tiles per monster (want about {lo}-{hi})")
        d = per_khu.setdefault(kid, {"kinds": {}, "elites": 0, "tiles": 0, "normal": 0})
        d["kinds"][kind] = d["kinds"].get(kind, 0) + count
        if rank == "elite":
            d["elites"] += count
        else:
            d["tiles"] += len(walkable)
            d["normal"] += count
    for kid, (k, band, _r) in khu_rects.items():
        d = per_khu.get(kid)
        if band == 0:
            if d:
                out.append(f"{where}: khu {kid} is a safe place but has monsters")
            continue
        if not d or len(d["kinds"]) < int(rules["min_kinds_per_khu"]):
            out.append(f"{where}: khu {kid} has {len(d['kinds']) if d else 0} kinds of monster "
                       f"(at least {rules['min_kinds_per_khu']})")
            continue
        if d["elites"] > int(rules["max_elites_per_khu"]):
            out.append(f"{where}: khu {kid} has {d['elites']} elites (at most {rules['max_elites_per_khu']})")
        if d["normal"] and not (lo <= d["tiles"] / d["normal"] <= hi):
            out.append(f"{where}: khu {kid} has {d['tiles'] / d['normal']:.0f} walkable tiles per monster "
                       f"in its areas (want {lo}-{hi})")
    if report is not None and banded:
        report.append(f"{zone} ({size[0]} x {size[1]}, {total} monsters)")
        for kid, (k, band, _r) in khu_rects.items():
            d = per_khu.get(kid, {"kinds": {}})
            kinds = ", ".join(f"{m} {c}" for m, c in sorted(d["kinds"].items()))
            report.append(f"  {kid} | {k.props.get('name_vi')} | band {band} | {int(k.w // TILE)} x "
                          f"{int(k.h // TILE)} | {kinds or '-'}")
    # ---- texts
    for o in objs:
        p = _props(o)
        for key in ("name_vi", "desc_vi", "text"):
            if p.get(key):
                ctx["texts"].append((f"{where} {o.get('type')} {o.get('name')}", p[key], banded))
    return out


def _fonts(texts, warnings: list | None = None) -> list[str]:
    """Problems of the texts of the maps: a character no font of the game draws, a Chinese
    character. On a giant land (banded) they are problems; on the older small maps, which the
    world builder does not own, they are warnings (printed, not failing the check)."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return []
    fdir = ROOT / "client" / "assets" / "fonts"
    try:
        pixel = set(TTFont(fdir / "VT323-Regular.ttf", fontNumber=0, lazy=True).getBestCmap())
        han = set(TTFont(fdir / "NotoSansSC-Game.otf", fontNumber=0, lazy=True).getBestCmap())
    except OSError:
        return []
    out, seen = [], set()
    for where, text, strict in texts:
        for ch in text:
            if (ch, strict) in seen or ch.isspace():
                continue
            seen.add((ch, strict))
            c = ord(ch)
            msg = None
            if 0x2E80 <= c < 0xA000:
                msg = f"{where}: {ch!r} is a Chinese character (no Hán tự on the maps)"
            elif not ((c < 0x2E80 and c in pixel) or c in han):
                msg = f"{where}: no font draws {ch!r} (U+{c:04X}), the game shows a box"
            if msg and strict:
                out.append(msg)
            elif msg and warnings is not None:
                warnings.append(msg)
    return out


def context() -> dict:
    zones = {k: v for k, v in _json(DATA / "zones.json").items() if not k.startswith("_")}
    plan = _json(DATA / "math" / "world_plan.json")
    monsters = {k: v for k, v in _json(DATA / "math" / "monsters.json").items() if not k.startswith("_")}
    monsters.update({k: v for k, v in _json(DATA / "creatures" / "monsters.json").items() if not k.startswith("_")})
    dd = _json(DATA / "math" / "dia_do.json")
    glide = next((u.get("glide") or {} for u in plan.get("unlocks", []) if u.get("id") == "dap_kiem_luot"), {})
    return {"zones": zones, "plan": plan, "lands": {l["id"]: l for l in plan.get("lands", [])},
            "map_zone": {z["map"]: zid for zid, z in zones.items() if z.get("map")},
            "monsters": monsters, "bands": dd["realms"], "rules": dd["distribution"], "glide": glide,
            "sizes": doc_sizes(), "sprites": known_sprites(), "khu_seen": {}, "texts": []}


def problems(report: list | None = None, warnings: list | None = None) -> list[str]:
    from app.realtime import dia_do
    out = [f"data/math/dia_do.json: {e}" for e in dia_do.validate()]
    ctx = context()
    for path in sorted(SERVER_MAPS.glob("*.tmj")):
        try:
            out += check_map(path.stem, ctx, report)
        except Exception as e:          # a broken map fails the check, it does not crash the run
            out.append(f"map {path.stem}: cannot be checked: {type(e).__name__}: {e}")
    for path in sorted(CLIENT_MAPS.glob("*.tmj")):
        if not (SERVER_MAPS / path.name).is_file():
            out.append(f"client/assets/maps/{path.name} has no server copy")
    out += _fonts(ctx["texts"], warnings)
    return out


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    report: list[str] = []
    warnings: list[str] = []
    errs = problems(report if "--report" in argv else None, warnings)
    for line in report:
        print(line)
    for w in warnings:
        print("  (warning)", w)
    for e in errs:
        print("  -", e)
    print(f"[{'FAIL' if errs else ' OK '}] {len(list(SERVER_MAPS.glob('*.tmj')))} maps, {len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
