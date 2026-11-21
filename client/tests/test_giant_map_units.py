"""The engine on giant maps (Đại Địa Đồ): the ground in chunks draws exactly the old picture,
objects are found through buckets, khu and poi are never drawn, memory stays bounded.

The reference renderers below are the old whole-map code, kept here verbatim so the chunked
ground can be compared pixel for pixel on every map the game ships."""
import json
import random
from pathlib import Path

import pygame
import pytest

from client.art import build as B
from client.engine import art2, tilemap
from client.engine import autotile as A
from client.engine.tilemap import TileMap
from client.engine.view import View

ROOT = Path(__file__).resolve().parents[2]
MAPS = sorted((ROOT / "client" / "assets" / "maps").glob("*.tmj"))


@pytest.fixture(autouse=True)
def v2_art():
    art2.set_root(None)
    yield
    art2.set_root(None)


# ------------------------------------------------------------------ the old renderers
def old_surface16(m: TileMap) -> pygame.Surface:
    v2 = art2.tileset(len(B.TILESET)) if art2.on() else None
    surf = pygame.Surface((m.px_w, m.px_h))
    for i, gid in enumerate(m.ground):
        t = m._tiles.get(gid)
        if t is not None and v2 is not None:
            t = v2.pick(gid - 1, i % m.w, i // m.w)
        if t:
            surf.blit(t, ((i % m.w) * m.tw, (i // m.w) * m.th))
    return surf


def old_ground32(m: TileMap):
    ts = art2.tileset32(len(B.TILESET))
    terrain, _native = art2.terrain32()
    rules = art2.wiring().get("autotile") or {}
    names = [n for n, _ in B.TILESET]
    w, h, g = m.w, m.h, m.ground

    def cls(x, y):
        gid = g[y * w + x]
        return names[gid - 1] if 0 < gid <= len(names) else None
    surf = pygame.Surface((w * 32, h * 32))
    water_open, autotiled = [], 0
    for i, gid in enumerate(g):
        if not 0 < gid <= len(names):
            continue
        x, y = i % w, i // w
        tile = ts.pick(gid - 1, x, y)
        rule = rules.get(names[gid - 1])
        outer = set(rule.get("outer", [])) if isinstance(rule, dict) else None
        pieces = A.cell_pieces(cls, x, y, w, h, outer) if outer else (None,) * 4
        shape = A.whole(cls, x, y, w, h, outer) if outer else None
        special = terrain.get(f"{rule['pair']}_{shape}") if shape else None
        if special or any(pieces):
            near = [g[ny * w + nx] for nx, ny in ((x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
                    if 0 <= nx < w and 0 <= ny < h and cls(nx, ny) in outer]
            og = max(set(near), key=near.count) if near else None
            painted = rule.get("painted", "grass")
            same = og is None or names[og - 1] == painted or (
                painted == "grass" and names[og - 1] in ("grass", "flowers"))
            under = ts.pick(og - 1, x, y) if (not same and painted == "grass") else None
            whole_tile = special[(x * 3 + y) % len(special)] if special else None
            tile, _ok = A.compose(tile, pieces, terrain, rule["pair"], x * 3 + y, under, whole_tile)
            autotiled += 1
        elif gid == m._water_gid:
            water_open.append((x, y))
        surf.blit(tile, (x * 32, y * 32))
    return surf, water_open, list(ts.water) or None, ts.water_fps, autotiled


def old_draw16(m, full, target, cx, cy, t):
    target.blit(full, (0, 0), pygame.Rect(cx, cy, target.get_width(), target.get_height()))
    frame = m._water_frames[int(t * m._water_fps) % len(m._water_frames)]
    for x, y in m.water_cells:
        px, py = x * m.tw - cx, y * m.th - cy
        if -16 < px < target.get_width() and -16 < py < target.get_height():
            target.blit(frame, (px, py))


def old_draw32(old, target, ox, oy, t):
    g, water_open, frames, fps, _n = old
    target.blit(g, (0, 0), pygame.Rect(ox, oy, target.get_width(), target.get_height()))
    if frames:
        frame = frames[int(t * fps) % len(frames)]
        for x, y in water_open:
            px, py = x * 32 - ox, y * 32 - oy
            if -32 < px < target.get_width() and -32 < py < target.get_height():
                target.blit(frame, (px, py))


def same(a: pygame.Surface, b: pygame.Surface) -> bool:
    return a.get_size() == b.get_size() and pygame.image.tobytes(a, "RGB") == pygame.image.tobytes(b, "RGB")


def views(m: TileMap, zoom: int, n: int = 6):
    """Camera corners (screen pixels of the zoomed world) to compare at: the map's corners, a
    few random places, and off the map's edge (a small map centred on a large screen)."""
    rng = random.Random(m.w * 1000 + m.h)
    W, H = m.px_w * zoom, m.px_h * zoom
    out = [(0, 0), (max(0, W - 480), max(0, H - 270)), (-37, -21), (W - 300, H - 100)]
    out += [(rng.randrange(-40, max(1, W - 440)), rng.randrange(-30, max(1, H - 240))) for _ in range(n)]
    return out


# ------------------------------------------------------------------ pixel parity
@pytest.mark.parametrize("path", MAPS, ids=lambda p: p.stem)
def test_the_chunked_ground_is_the_old_picture_at_zoom_1_and_2(path):
    tilemap._CACHE.clear()
    tilemap._cache_bytes = 0
    m = TileMap(path)
    assert art2.on(), "this checkout has the v2 art"
    full16 = old_surface16(m)
    for t in (0.0, 0.6, 1.3):
        whole_new, whole_old = pygame.Surface((m.px_w, m.px_h)), pygame.Surface((m.px_w, m.px_h))
        m.draw_ground(whole_new, (0, 0), t)                      # the whole map at once
        old_draw16(m, full16, whole_old, 0, 0, t)
        assert same(whole_new, whole_old), (path.stem, 1, t)
    for cam in views(m, 1):
        a, b = pygame.Surface((480, 270)), pygame.Surface((480, 270))
        a.fill((1, 2, 3))
        b.fill((1, 2, 3))
        m.draw_ground(a, cam, 0.9)
        old_draw16(m, full16, b, *cam, 0.9)
        assert same(a, b), (path.stem, 1, cam)
    old = old_ground32(m)
    v = View(2)
    for t in (0.0, 0.6, 1.3):
        whole_new, whole_old = pygame.Surface((m.w * 32, m.h * 32)), pygame.Surface((m.w * 32, m.h * 32))
        v.ox = v.oy = 0
        m.draw_ground_view(whole_new, v, t)
        old_draw32(old, whole_old, 0, 0, t)
        assert same(whole_new, whole_old), (path.stem, 2, t)
    for cam in views(m, 2):
        a, b = pygame.Surface((480, 270)), pygame.Surface((480, 270))
        a.fill((1, 2, 3))
        b.fill((1, 2, 3))
        v.ox, v.oy = cam
        m.draw_ground_view(a, v, 1.1)
        old_draw32(old, b, *cam, 1.1)
        assert same(a, b), (path.stem, 2, cam)
    assert same(m.ground32(), old[0]) and m.autotiled == old[4]


def test_the_chunked_ground_is_the_old_picture_without_the_v2_art(tmp_path):
    art2.set_root(tmp_path)
    assert not art2.on()
    for name in ("truc_lam_thon", "ho_nghien_muc"):
        m = TileMap(ROOT / "client" / "assets" / "maps" / f"{name}.tmj")
        full16 = old_surface16(m)
        a, b = pygame.Surface((m.px_w, m.px_h)), pygame.Surface((m.px_w, m.px_h))
        m.draw_ground(a, (0, 0), 0.7)
        old_draw16(m, full16, b, 0, 0, 0.7)
        assert same(a, b), name
        v = View(2)
        v.ox, v.oy = 40, 30
        s1, s2 = pygame.Surface((480, 270)), pygame.Surface((480, 270))
        m.draw_ground_view(s1, v, 0.2)                           # zoom 2 without 2x tiles: the 16 px ground
        old_draw16(m, full16, s2, 40, 30, 0.2)
        assert same(s1, s2) and m.ground32() is None


def test_a_chunk_built_over_several_frames_is_the_same_chunk():
    m = TileMap(ROOT / "client" / "assets" / "maps" / "loan_so_coc.tmj")
    tilemap._CACHE.clear()
    tilemap._cache_bytes = 0
    ref = pygame.Surface(m._chunk(2, 1, 1).surf.get_size())
    ref.blit(m._chunk(2, 1, 1).surf, (0, 0))
    tilemap._CACHE.clear()
    tilemap._cache_bytes = 0
    ch = m._chunk(2, 1, 1, finish=False, deadline=0.0)          # out of time at once: a few cells only
    assert not ch.done and 0 < ch.cell < 256
    while not ch.done:
        m._chunk(2, 1, 1, finish=False, deadline=0.0)
    assert same(ch.surf, ref)


# ------------------------------------------------------------------ a giant synthetic map
def giant(tmp_path: Path, w: int = 320, h: int = 240) -> Path:
    rng = random.Random(5)
    names = [n for n, _ in B.TILESET]
    gid = {n: names.index(n) + 1 for n in names}
    g = [gid["grass"]] * (w * h)
    for _ in range(40):
        cx, cy, r = rng.randrange(w), rng.randrange(h), rng.randint(2, 8)
        kind = rng.choice(["water", "dirt", "path", "dark_grass"])
        for y in range(max(0, cy - r), min(h, cy + r)):
            for x in range(max(0, cx - r), min(w, cx + r)):
                g[y * w + x] = gid[kind]
    objs = [{"id": 1, "name": "spawn", "type": "spawn", "x": 2500, "y": 1900, "width": 0, "height": 0}]
    for i in range(3000):
        objs.append({"id": i + 2, "name": "tree", "type": "prop", "x": rng.randrange(w * 16 - 32),
                     "y": rng.randrange(h * 16 - 40), "width": 32, "height": 40,
                     "properties": [{"name": "sprite", "type": "string", "value": "tree"},
                                    {"name": "variant", "type": "string", "value": str(i)}]})
    objs.append({"id": 9001, "name": "kts_ngoai_vi", "type": "khu", "x": 0, "y": 0, "width": w * 16, "height": h * 16,
                 "properties": [{"name": "khu", "type": "string", "value": "kts_ngoai_vi"},
                                {"name": "sprite", "type": "string", "value": "tree"}]})
    objs.append({"id": 9002, "name": "Cổ Miếu", "type": "poi", "x": 2400, "y": 1800, "width": 64, "height": 64,
                 "properties": [{"name": "poi", "type": "string", "value": "landmark"}]})
    objs.append({"id": 9003, "name": "Lão Tiều", "type": "npc", "x": 2510, "y": 1880, "width": 16, "height": 24,
                 "properties": [{"name": "npc", "type": "string", "value": "guide"}]})
    solids = [{"id": 20000 + i, "name": "", "type": "solid", "x": rng.randrange(w * 16 - 20),
               "y": rng.randrange(h * 16 - 20), "width": 9, "height": 7} for i in range(4000)]
    doc = {"width": w, "height": h, "tilewidth": 16, "tileheight": 16,
           "layers": [{"type": "tilelayer", "name": "ground", "data": g},
                      {"type": "objectgroup", "name": "objects", "objects": objs},
                      {"type": "objectgroup", "name": "collision", "objects": solids}]}
    p = tmp_path / "giant.tmj"
    p.write_text(json.dumps(doc), "utf-8")
    return p


def test_a_giant_map_holds_a_bounded_ground(tmp_path):
    tilemap._CACHE.clear()
    tilemap._cache_bytes = 0
    m = TileMap(giant(tmp_path))
    v = View(2)
    s = pygame.Surface((480, 270))
    for i in range(400):                                         # flying corner to corner
        v.ox, v.oy = i * 25, i * 18
        m.draw_ground_view(s, v, i / 60)
        assert tilemap.cache_bytes() <= tilemap.CACHE_BYTES + 2 ** 20
    assert tilemap.ground_bytes(m) <= tilemap.CACHE_BYTES < 64 * 2 ** 20
    assert getattr(m, "_g32", None) is None                     # the whole-map picture was never made


def test_chunks_ahead_are_built_while_walking(tmp_path):
    tilemap._CACHE.clear()
    tilemap._cache_bytes = 0
    m = TileMap(giant(tmp_path))
    v = View(2)
    s = pygame.Surface((480, 270))
    v.ox, v.oy = 2000, 2000
    m.draw_ground_view(s, v, 0)
    for _ in range(40):                                          # walking east: the east column is built first
        v.ox += 4
        m.draw_ground_view(s, v, 0)
    east = tilemap._CACHE.get((m.uid, 2, (2000 + 480) // 512 + 1, 2000 // 512))
    assert east is not None and east.done


def test_khu_and_poi_are_never_drawn_nor_picked(tmp_path):
    m = TileMap(giant(tmp_path))
    every = m.drawables_in(-10, -10, m.px_w + 10, m.px_h + 10)
    assert {o.type for o in every} == {"prop", "npc"}
    near = m.interactables_near(2518, 1904, 30)
    assert [o.name for o in near] == ["Lão Tiều"]
    assert m.find("khu")[0].name == "kts_ngoai_vi" and m.find("poi")[0].props["poi"] == "landmark"
    assert not m.blocked(pygame.Rect(2400, 1800, 20, 20)) or any(
        r.colliderect(pygame.Rect(2400, 1800, 20, 20)) for r in m.solids)   # a poi is no wall


def test_buckets_give_exactly_what_a_full_scan_gives(tmp_path):
    m = TileMap(giant(tmp_path))
    rng = random.Random(2)
    for _ in range(200):
        x0, y0 = rng.uniform(-100, m.px_w), rng.uniform(-100, m.px_h)
        x1, y1 = x0 + rng.uniform(0, 700), y0 + rng.uniform(0, 500)
        want = [o for o in m.objects if tilemap.can_draw(o)
                and not (o.x + o.w < x0 or o.x > x1 or o.y + o.h < y0 or o.y > y1)]
        got = [o for o in m.drawables_in(x0, y0, x1, y1)
               if not (o.x + o.w < x0 or o.x > x1 or o.y + o.h < y0 or o.y > y1)]
        assert got == want
    for _ in range(200):                                          # pygame's own overlap, through the grid
        r = pygame.Rect(rng.randrange(-5, m.px_w), rng.randrange(-5, m.px_h), rng.randint(1, 40), rng.randint(1, 40))
        full = r.left < 0 or r.top < 0 or r.right > m.px_w or r.bottom > m.px_h or r.collidelist(m.solids) != -1
        assert m.blocked(r) == full
    col = m.collider()
    assert col is m.collider() and len(col.solids) == 4000


def test_load_map_keeps_a_few_maps_only():
    tilemap._MAPS.clear()
    names = [p.stem for p in MAPS][:tilemap.MAX_MAPS + 2]
    first = tilemap.load_map(names[0])
    v = View(1)
    first.draw_ground_view(pygame.Surface((64, 64)), v, 0)
    assert tilemap.ground_bytes(first) > 0
    for n in names[1:]:
        tilemap.load_map(n)
    assert len(tilemap._MAPS) == tilemap.MAX_MAPS and names[0] not in tilemap._MAPS
    assert tilemap.ground_bytes(first) == 0                      # its chunks went with it
    assert tilemap.load_map(names[-1]) is tilemap.load_map(names[-1])
