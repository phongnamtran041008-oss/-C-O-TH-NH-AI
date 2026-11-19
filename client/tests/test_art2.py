"""The v2 art (client/assets/v2/, rendered out of Blender) and its wiring into the client.

* `wiring.json` is complete: every realm, monster, chiêu, weapon kind and TD creature of the
  game data has a picture, and every id it names exists on disk;
* the loader reads what the packers wrote (sheets, FX, icons, tiles, props) and the weapon
  layers and glow sheets sit on their character's exact frame grid;
* a checkout without the folder gets None everywhere, and the map still builds from the old
  code-drawn tiles.
"""
from __future__ import annotations

import json
import math
import types
from pathlib import Path

import pygame
import pytest

from client.engine import art2

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "client" / "assets" / "v2"
DATA = ROOT / "server" / "data"

pytestmark = pytest.mark.skipif(not (V2 / "wiring.json").exists(), reason="no v2 art in this checkout")


@pytest.fixture(autouse=True)
def fresh_loader():
    art2.set_root(None)
    yield
    art2.set_root(None)


def W() -> dict:
    return json.loads((V2 / "wiring.json").read_text("utf-8"))


def entries(section: dict) -> dict:
    return {k: v for k, v in section.items() if not k.startswith("_")}


def exists(folder: str, sid: str) -> bool:
    return (V2 / folder / f"{sid}.json").exists() and (V2 / folder / f"{sid}.png").exists()


def icon_ids(set_id: str) -> set:
    return set(json.loads((V2 / "icons" / f"{set_id}.json").read_text("utf-8"))["icons"])


def data(path: str) -> dict:
    return json.loads((DATA / path).read_text("utf-8"))


# ------------------------------------------------------------------ wiring.json: complete and real
def test_every_id_the_wiring_names_exists_on_disk():
    w = W()
    for realm, e in entries(w["realms"]).items():
        assert exists("chars", f"dao_si_{e['look']}"), realm
        if e["aura"]:
            assert exists("fx", f"aura_{e['aura']}_back") and exists("fx", f"aura_{e['aura']}_front"), realm
    assert exists("chars", f"dao_si_{w['default_look']}")
    for look, gid in entries(w["glow"]).items():
        assert exists("chars", f"dao_si_{look}") and exists("fx", gid), look
    sheets = list(entries(w["monsters"]).values()) + list(w["monster_default"].values())
    for subj in entries(w["monster_subjects"]).values():
        sheets += list(subj.values())
    sheets += [e["sheet"] for e in entries(w["td_monsters"]).values()] + w["monster_float"]
    for sid in sheets:
        assert exists("monsters", sid), sid
    nature = json.loads((V2 / "props" / "nature.json").read_text("utf-8"))["props"]
    for old, names in entries(w["props"]).items():
        assert names and all(n in nature for n in names), old
    for kind, e in entries(w["weapons"]).items():
        assert exists("weapons", e["layer"]) and e["clip"] in ("slash", "cast", "shoot"), kind
    for kind, bid in entries(w["pets"]).items():
        assert exists("beasts", bid), kind
    for kind, bid in entries(w["bees"]).items():
        assert exists("beasts", bid), kind
    for name, (atlas, pid) in w["garden"]["decorations"].items():
        assert pid in json.loads((V2 / "props" / f"{atlas}.json").read_text("utf-8"))["props"], name
    for fx_id, e in entries(w["skill_fx"]).items():
        assert e["kind"] in ("strike", "bolt", "circle", "ward") and exists("fx", e["fx"]) and exists("fx", e["impact"])
    for name, fid in w["combat_fx"].items():
        assert exists("fx", fid), name
    refs = list(entries(w["skill_icons"]).values()) + [w["item_icons"]["spirit_stone"]]
    for table in ("by_id", "by_weapon", "by_kind", "by_slot"):
        refs += list(w["item_icons"][table].values())
    for set_id, icon_id in refs:
        assert icon_id in icon_ids(set_id), (set_id, icon_id)


def test_every_server_monster_maps_to_a_v2_sheet():
    mapped = entries(W()["monsters"])
    for path in ("creatures/monsters.json", "math/monsters.json"):
        for mid, m in entries(data(path)).items():
            assert mid in mapped, f"{mid} ({path}) has no v2 sheet in wiring.json"
            sheet = art2.monster_for(mid, m.get("rank", "normal"))
            assert sheet is not None and sheet.has("windup") and sheet.has("die"), mid
            if m.get("rank") in ("elite", "boss"):
                assert mapped[mid].endswith("_di") or sheet.fw > 48, f"{mid}: an {m['rank']} should look it"


def test_an_unlisted_monster_goes_by_its_subject_and_rank():
    assert art2.monster_id("gt_khong_co", "normal", "giai_tich") == "van_xa"
    assert art2.monster_id("xx", "boss") == "loi_long"
    assert art2.monster_id("xx", "normal") == W()["monster_default"]["normal"]


def test_every_realm_the_server_knows_has_a_look():
    server = [r["id"] for r in data("realms_cultivation.json")["realms"]]
    assert server == ["pham_nhan", "luyen_khi", "truc_co", "kim_dan", "nguyen_anh", "hoa_than", "luyen_hu",
                      "hop_the", "dai_thua"]
    realms = set(server)
    doc = data("realms.json")          # the bí cảnh file: whatever realm ids it may list
    for key in ("realms", "order"):
        v = doc.get(key) if isinstance(doc, dict) else None
        if isinstance(v, list):
            realms |= {r if isinstance(r, str) else r.get("id") for r in v} - {None}
        elif isinstance(v, dict):
            realms |= set(v)
    want = {"pham_nhan": "luyen_khi", "luyen_khi": "luyen_khi", "kim_dan": "ket_dan"}
    for r in realms:
        assert art2.char_for(r) is not None, r
        if r in want:
            assert art2.look_for(r) == want[r]
    assert all(art2.char(look) is not None for look in
               ("luyen_khi", "truc_co", "ket_dan", "nguyen_anh", "hoa_than", "luyen_hu", "hop_the", "dai_thua"))


def test_every_server_realm_is_wired_to_its_own_look_and_an_aura_on_disk():
    """Each of the eight realms has its wiring entry (no fallback to the default look), its
    character sheet and both aura layers on disk; the four high realms also their glow."""
    wired = entries(W()["realms"])
    for r in data("realms_cultivation.json")["realms"]:
        rid = r["id"]
        assert rid in wired, rid
        look = wired[rid]["look"]
        assert exists("chars", f"dao_si_{look}") and art2.char_for(rid) is art2.char(look), rid
        if rid == "pham_nhan":
            assert art2.aura_for(rid) == (None, None)          # no aura before Luyện Khí
            continue
        aura = wired[rid]["aura"]
        assert exists("fx", f"aura_{aura}_back") and exists("fx", f"aura_{aura}_front"), rid
        back, front = art2.aura_for(rid)
        assert back is not None and front is not None, rid
        if rid in ("hoa_than", "luyen_hu", "hop_the", "dai_thua"):
            assert look == rid and art2.glow_for(look) is not None, rid
    looks = [wired[r["id"]]["look"] for r in data("realms_cultivation.json")["realms"][1:]]
    assert len(set(looks)) == len(looks) == 8                    # eight realms, eight looks


def test_every_chieu_has_an_effect_and_an_icon_and_every_weapon_kind_a_layer():
    from client.art import skill_fx
    for fx_id in skill_fx.FX_IDS:
        assert art2.skill_fx(fx_id) is not None, fx_id
    for sid in data("math/skills.json")["skills"]:
        img = art2.skill_icon(sid)
        assert img is not None and img.get_size() == (32, 32), sid
    for iid, it in data("items/equipment.json")["items"].items():
        if it.get("slot") == "weapon":
            layer, clip = art2.weapon_for(it["kind"])
            assert layer is not None, (iid, it["kind"])
        assert art2.item_icon({"item_id": iid, **it}) is not None, iid


def test_every_td_creature_and_every_map_nature_prop_has_v2_art():
    from client.scenes.td import SPRITE_OF
    for kind in SPRITE_OF:
        sheet, scale = art2.td_monster(kind)
        assert sheet is not None and 0 < scale <= 1, kind
    for old in ("bamboo", "tree", "ink_tree", "rock"):
        for v in range(6):
            assert art2.prop_for(old, v) is not None, (old, v)
    assert art2.prop_for("khong_co", 0) is None        # no mapping: the old sprite stays


# ------------------------------------------------------------------ the loader
def test_character_sheets_load_with_all_clips_and_stable_frames():
    s = art2.char("luyen_khi")
    assert (s.fw, s.fh, s.pivot) == (96, 96, (48.0, 82.0))
    for clip in ("idle", "walk", "slash", "cast", "shoot", "hit", "die", "meditate", "fly", "dodge"):
        assert s.has(clip) and s.seconds(clip) > 0, clip
    n = s.index("walk", 0.35, "left")
    assert s.frame(n) is s.frame(n)                      # cut once: caches keyed on it hold
    assert s.index("die", 99.0, "down") == s.clips["die"].frames["down"][-1]     # a one-shot holds its last frame
    w, h = art2.extent(s)
    assert 45 <= h <= 56 and 20 <= w <= 40, (w, h)        # ~50 px above the feet, as the batch says
    assert art2.portrait("luyen_khi").get_size() == tuple(W()["portrait"]["rect"][2:])


def test_weapon_layers_and_glow_sheets_sit_on_their_characters_grid():
    body = json.loads((V2 / "chars" / "dao_si_luyen_khi.json").read_text("utf-8"))
    for p in sorted((V2 / "weapons").glob("*.json")):
        doc = json.loads(p.read_text("utf-8"))
        assert doc["frame"] == body["frame"] and doc["pivot"] == body["pivot"], p.name
        for clip, c in doc["clips"].items():
            if p.stem.startswith("phi_kiem"):         # its own small sheet: the fly clip, frame for frame
                assert {d: len(f) for d, f in c["frames"].items()} == \
                    {d: len(f) for d, f in body["clips"][clip]["frames"].items()}, (p.name, clip)
            else:                                     # drawn with the character's own frame index
                assert c["frames"] == body["clips"][clip]["frames"], (p.name, clip)
        if not p.stem.startswith("phi_kiem"):
            assert doc["frames"] == body["frames"] and set(doc["clips"]) == set(body["clips"]), p.name
    for look, gid in entries(W()["glow"]).items():
        g = art2.fx(gid)
        c = art2.char(look)
        assert (g.fw, g.fh, g.pivot, g.total, g.cols) == (c.fw, c.fh, c.pivot, c.total, c.cols), look


def test_layers_come_in_the_draw_order_of_the_pipeline():
    sword, _ = art2.weapon_for("sword")
    na = art2.char("nguyen_anh")
    layers = art2.char_layers("nguyen_anh", "slash", 0.2, "right", "sword", aura_t=0.3)
    back, front = art2.aura_for("nguyen_anh")
    n = na.index("slash", 0.2, "right")
    assert [img for img, _, _ in layers] == [back.frame(back.fx_index(0.3)), na.frame(n), sword.frame(n),
                                             front.frame(front.fx_index(0.3))]
    assert layers[0][1] == (-64, -104) and layers[1][1] == (-48, -82)     # both pivots on the feet
    ht = art2.char_layers("hoa_than", "idle", 0, "down")
    assert len(ht) == 4 and ht[1][0] is art2.fx("glow_hoa_than").frame(art2.char("hoa_than").index("idle", 0, "down"))
    assert len(art2.char_layers("pham_nhan", "idle", 0, "down")) == 1      # a mortal: no aura, no weapon
    ghost = art2.char_layers("nguyen_anh", "idle", 0, "down", aura=False)
    assert len(ghost) == 1


def test_fx_honour_their_blend_and_one_shots_end():
    spark = art2.fx("hit_spark")
    assert spark.additive and spark.flags == pygame.BLEND_RGBA_ADD and not spark.loop
    warn = art2.fx("warn_circle_charge")
    assert not warn.additive and warn.flags == 0 and warn.ground
    surf = pygame.Surface((96, 96), pygame.SRCALPHA)
    surf.fill((60, 60, 60, 255))
    assert art2.draw_fx(surf, "hit_spark", 0.05, 48, 48)
    px = [surf.get_at((x, y)) for x in range(96) for y in range(96)]
    assert all(p.r >= 60 and p.g >= 60 and p.b >= 60 for p in px) and any(p.r > 120 for p in px)   # added light
    assert not art2.draw_fx(surf, "hit_spark", spark.duration + 0.1, 48, 48)
    assert art2.draw_fx(surf, "warn_circle_charge", 99.0, 48, 48, size=(40, 40))   # loops forever
    assert not art2.draw_fx(surf, "khong_co", 0, 0, 0)


def test_icons_tiles_and_props():
    assert art2.icon("weapons_a", "kiem_1").get_size() == (32, 32)
    assert art2.icon("weapons_a", "khong_co") is None and art2.icon("khong_co", "x") is None
    assert art2.item_icon({"item_id": "hoi_huyet_dan", "kind": None}) is art2.icon("dan_duoc", "dan_1")
    assert art2.item_icon({"item_id": "x", "kind": "sword", "slot": "weapon"}) is art2.icon("weapons_a", "kiem_1")
    assert art2.item_icon({"item_id": "x", "slot": "ring"}) is art2.icon("trang_bi", "nhan_1")
    assert art2.item_icon({"item_id": "x"}) is None
    from client.art import build as B
    ts = art2.tileset(len(B.TILESET))
    assert len(ts.tiles) == len(B.TILESET) and all(t.get_size() == (16, 16) for t in ts.tiles)
    assert len(ts.water) == 4 and ts.water_fps > 0
    assert len(ts.alternates[B.TILESET.index(("stone", 0))]) == 2           # the extra stone variant is used
    for name in ("bamboo_1", "tree_1", "dead_tree", "rock_2"):
        pr = art2.prop(name)
        w, h = pr.img.get_size()
        assert 0 < pr.pivot[0] < w and 0 < pr.pivot[1] <= h, name


def test_a_map_object_stands_on_its_prop_pivot_at_2x():
    from client.engine.view import View
    v = View(2)
    v.set(10, 20)
    o = types.SimpleNamespace(x=100, y=60, w=32, h=40, foot_y=100, type="", props={"sprite": "tree", "variant": 0})
    foot, img, pos = art2.prop_drawable(o, v)
    pr = art2.prop_for("tree", 0)
    assert img is pr.img and foot == 100
    assert (pos[0] + pr.pivot[0], pos[1] + pr.pivot[1]) == ((116 - 10) * 2, (100 - 20) * 2)   # bottom-centre


def test_the_hit_zone_covers_exactly_the_real_hit_radius():
    """The server hits everyone within r + 5 of the zone's point: that is the circle drawn."""
    from client.engine.view import View
    from client.scenes.world import WorldScene
    ws = WorldScene.__new__(WorldScene)
    ws.t = 0.0
    ws.view = View(2)                                   # the 2x world: the zone is drawn doubled
    ws.view.set(0, 0)
    r = 20
    ws.teles = [[50, 50, r, 0.4, 0.8, "m1"]]
    surf = pygame.Surface((200, 200))
    surf.fill((90, 160, 70))
    ws.draw_teles_v2(surf)
    changed = [(x, y) for x in range(200) for y in range(200) if surf.get_at((x, y))[:3] != (90, 160, 70)]
    xs, ys = [p[0] for p in changed], [p[1] for p in changed]
    want = (r + 5) * 2
    assert abs((max(xs) - min(xs)) / 2 - want) <= 3 and abs((max(ys) - min(ys)) / 2 - want) <= 3
    edge = surf.get_at((100 - want + 3, 100))[:3]
    assert edge[0] > edge[1] + 40                                           # a red-orange rim, not grass
    before = surf.copy()
    ws.draw_teles_v2(surf, over=True)                   # the second pass: a thin rim over the bodies
    rim = [(x, y) for x in range(200) for y in range(200) if surf.get_at((x, y)) != before.get_at((x, y))]
    assert rim and all(abs(math.hypot(x - 100, y - 100) - want) <= 2 for x, y in rim)


# ------------------------------------------------------------------ without the folder
def test_a_checkout_without_v2_gets_none_everywhere_and_the_old_tiles(tmp_path):
    art2.set_root(tmp_path)
    assert not art2.on() and art2.wiring() == {}
    assert art2.char("luyen_khi") is None and art2.char_for("truc_co") is None
    assert art2.monster_for("ink_slime") is None and art2.beast_for("rong") is None
    assert art2.fx("hit_spark") is None and not art2.draw_fx(pygame.Surface((8, 8)), "hit_spark", 0, 0, 0)
    assert art2.icon("weapons_a", "kiem_1") is None and art2.item_icon({"item_id": "hoi_huyet_dan"}) is None
    assert art2.skill_icon("thuong_quyen") is None and art2.portrait("luyen_khi") is None
    assert art2.tileset() is None and art2.prop("tree_1") is None and art2.prop_for("tree", 0) is None
    assert art2.char_layers("luyen_khi", "idle", 0, "down") is None
    from client.engine.view import View
    assert art2.walker_drawables("luyen_khi", 0, 0, "down", False, 0, 0, None, View(2)) is None
    assert art2.tileset32() is None and art2.terrain32() == ({}, False) and art2.npc("guide") is None
    assert art2.td_monster("muc_con") == (None, 1.0) and art2.weapon_for("sword") == (None, "slash")
    from client.art import build as B
    from client.engine.tilemap import TileMap
    m = TileMap(ROOT / "client" / "assets" / "maps" / "truc_lam_thon.tmj")
    old = B.tile(*B.TILESET[0])
    assert m._tiles[1].get_size() == old.get_size() and m._water_fps == 2.0
    assert pygame.image.tobytes(m._tiles[1], "RGBA") == pygame.image.tobytes(old, "RGBA")
    from client.scenes.td import monster_frames, _MON
    _MON.pop("muc_phi", None)
    assert monster_frames("muc_phi")[0].get_width() < 40          # the old tinted ink creature
    _MON.pop("muc_phi", None)


def test_a_broken_sheet_is_none_not_a_crash(tmp_path):
    (tmp_path / "chars").mkdir()
    (tmp_path / "wiring.json").write_text(json.dumps({"realms": {"luyen_khi": {"look": "x", "aura": None}}}))
    (tmp_path / "chars" / "dao_si_x.json").write_text("{not json")
    art2.set_root(tmp_path)
    assert art2.on() and art2.char_for("luyen_khi") is None
    (tmp_path / "chars" / "dao_si_y.json").write_text(json.dumps({"id": "y", "frame": {"w": 4, "h": 4}}))
    assert art2.char("y") is None                                  # json without its png


# ------------------------------------------------------------------ round 2: the 2x world
def test_world_and_screen_round_trip_through_the_view():
    from client.engine.view import View
    v = View(2)
    v.follow(300, 200, 896, 576, 480, 270)
    assert (v.x, v.y) == (180, 132.5)
    for wx, wy in ((300, 200), (181.5, 133.25), (420, 333)):
        sx, sy = v.to_screen(wx, wy)
        bx, by = v.to_world(sx, sy)
        assert abs(bx - wx) <= 0.5 and abs(by - wy) <= 0.5
    assert v.to_screen(300, 200) == (240, 135)
    v.follow(5, 5, 896, 576, 480, 270)                         # clamped to the map's corner
    assert (v.ox, v.oy) == (0, 0)
    v.follow(890, 570, 896, 576, 480, 270)
    assert v.to_screen(896, 576) == (480, 270)
    room = pygame.Rect(100, 100, 600, 300)                     # a bí cảnh room larger than the view
    v.follow(110, 110, 2000, 2000, 480, 270, bounds=room)
    assert (v.x, v.y) == (100, 100)
    small = pygame.Rect(100, 100, 200, 100)                    # smaller than the view: centred
    v.follow(110, 110, 2000, 2000, 480, 270, bounds=small)
    assert v.to_screen(200, 150) == (240, 135)
    one = View(1)                                              # zoom 1 is the old `int(x) - cam`
    one.ox, one.oy = 37, 12
    assert one.to_screen(100.7, 50.2) == (int(100.7) - 37, int(50.2) - 12)
    img = pygame.Surface((16, 24))
    assert v.img(img).get_size() == (32, 48) and v.img(img) is v.img(img) and one.img(img) is img


def test_mouse_picking_follows_the_zoom():
    from client.engine.view import View
    from client.scenes.world import Ent, WorldScene
    ws = WorldScene.__new__(WorldScene)
    ws.view = View(2)
    ws.view.set(100, 100)
    m = Ent("m1", "m", "Phần Tử Ma", mtype="dstt_phan_tu_ma")
    m.pos = (200.0, 180.0, 0, 0)
    ws.entities = {"m1": m}
    w, h = art2.extent(art2.monster_for("dstt_phan_tu_ma"))
    sx, sy = ws.world_to_screen(200, 180)
    assert (sx, sy) == (200, 160)
    for dy in (2, h // 2, h - 3):                            # anywhere on its picture, on screen
        assert ws.entity_at(*ws.screen_to_world(sx, sy - dy)) is m, dy
    assert ws.entity_at(*ws.screen_to_world(sx, sy - h - 6)) is None      # above its head
    assert ws.entity_at(*ws.screen_to_world(sx + w, sy - 4)) is None      # beside it


def test_autotile_quadrants_for_every_shape():
    from client.engine import autotile as A
    grid = ["ggggggg",
            "gdgpppg",
            "ggggpgg",
            "gwwwggg",
            "gwwwggg"]
    names = {"g": "grass", "d": "dirt", "p": "path", "w": "water"}
    h, w = len(grid), len(grid[0])

    def cls(x, y):
        return names[grid[y][x]]
    outer = {"grass"}
    assert A.cell_pieces(cls, 1, 1, w, h, outer) == ("nw", "ne", "sw", "se")       # a lone dirt cell: round
    assert A.whole(cls, 1, 1, w, h, outer) == "island"
    assert A.cell_pieces(cls, 4, 1, w, h, outer) == ("n", "n", "in_sw", "in_se")   # a T: notches by the stem
    assert A.cell_pieces(cls, 3, 1, w, h, outer) == ("nw", "n", "sw", "s")         # the west end of the bar
    assert A.whole(cls, 3, 1, w, h, outer) == "cap_w"
    assert A.whole(cls, 4, 2, w, h, outer) == "v" or A.whole(cls, 4, 2, w, h, outer) == "cap_s"
    assert A.cell_pieces(cls, 2, 4, w, h, outer) == (None, None, None, None)       # map edge never counts
    assert A.cell_pieces(cls, 2, 3, w, h, outer) == ("n", "n", None, None)
    assert A.mask(cls, 1, 1, w, h, outer) == 0xFF
    assert A.mask(cls, 4, 1, w, h, outer) & 0b1 and not A.mask(cls, 4, 1, w, h, outer) & 0b10000
    # composition: the quadrants come from the named transition tiles, the grass shows the real ground
    s = 32
    base = pygame.Surface((s, s)); base.fill((150, 110, 70))
    under = pygame.Surface((s, s)); under.fill((40, 70, 40))
    edge = pygame.Surface((s, s)); edge.fill((100, 170, 80))     # sheet grass ...
    pygame.draw.rect(edge, (150, 110, 70), (0, 8, s, s - 8))    # ... over the path
    out, ok = A.compose(base, ("n", "n", None, None), {"grass_path_n": [edge]}, "grass_path", 0, under)
    assert ok and out.get_at((5, 2))[:3] == (40, 70, 40) and out.get_at((5, 20))[:3] == (150, 110, 70)
    out, ok = A.compose(base, ("n", "n", None, None), {}, "grass_path", 0, under)
    assert not ok                                              # a missing transition tile is reported


def test_the_2x_ground_is_built_once_and_dirt_cells_are_no_longer_squares():
    from client.engine.tilemap import TileMap
    m = TileMap(ROOT / "client" / "assets" / "maps" / "loan_so_coc.tmj")
    g = m.ground32()
    assert g.get_size() == (m.w * 32, m.h * 32) and m.ground32() is g and m.autotiled > 50
    from client.art import build as B
    names = [n for n, _ in B.TILESET]
    lone = next(i for i, gid in enumerate(m.ground) if gid and names[gid - 1] == "dirt" and all(
        names[m.ground[(i // m.w + dy) * m.w + i % m.w + dx] - 1] in ("dark_grass", "grass")
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0))))
    x, y = (lone % m.w) * 32, (lone // m.w) * 32
    corner, middle = g.get_at((x + 1, y + 1)), g.get_at((x + 16, y + 16))
    assert corner != middle                                    # rounded: the corner is ground, not dirt


def test_buildings_npcs_and_their_wiring():
    w = W()
    if not (V2 / "props" / "buildings.json").exists():
        pytest.skip("props/buildings.* not on disk yet")
    doc = json.loads((V2 / "props" / "buildings.json").read_text("utf-8"))["props"]
    from client.engine import sprites
    from client.engine.view import View
    for old, names in entries(w["buildings"]).items():
        for i, n in enumerate(names):
            assert n in doc, (old, n)
            pr = art2.prop(n, "buildings")
            ow, oh = sprites.prop(old, i).get_size()
            assert pr.img.get_size() == (ow * 2, oh * 2), (n, pr.img.get_size(), (ow, oh))   # exactly 2x
            assert len(pr.frames) == int(doc[n].get("frames", 1))
    v = View(2)
    v.set(0, 0)
    o = types.SimpleNamespace(x=100, y=60, w=48, h=48, foot_y=108, type="", props={"sprite": "house", "variant": 1})
    foot, img, pos = art2.prop_drawable(o, v)
    assert img is art2.prop("house_1", "buildings").img and pos == (200, 120)   # the old top-left, doubled


def test_npc_sheets_from_the_wiring():
    missing = [k for k, sid in entries(W()["npcs"]).items() if not exists("npcs", sid)]
    if len(missing) == len(entries(W()["npcs"])):
        pytest.skip("npcs/* not on disk yet")
    from client.engine.view import View
    v = View(2)
    v.set(0, 0)
    for kind, sid in entries(W()["npcs"]).items():
        if kind in missing:
            continue
        s = art2.npc(kind)
        assert s is not None and s.has("idle") and (s.fw, s.fh, s.pivot) == (96, 96, (48.0, 82.0)), kind
        assert art2.npc_portrait(kind).get_size() == (20, 20)
    o = types.SimpleNamespace(x=100, y=60, w=16, h=24, foot_y=84, type="npc", props={"npc": "guide"})
    if "guide" not in missing:
        _, idle, pos = art2.npc_drawable(o, v, 0.0)
        _, talk, _ = art2.npc_drawable(o, v, 0.0, talking=True)
        s = art2.npc("guide")
        assert (pos[0] + 48, pos[1] + 82) == (216, 168)            # feet on the rect's bottom-centre, 2x
        assert talk is s.frame(s.index("talk", 0.0 + (100 % 7) * 0.11, "down")) or not s.has("talk")
        assert art2.object_height(o, v) == art2.extent(s)[1]


def test_without_32px_tiles_the_16px_ones_are_scaled(tmp_path):
    import shutil
    (tmp_path / "tiles").mkdir()
    for f in ("base.json", "base.png", "terrain.json", "terrain.png"):
        shutil.copy(V2 / "tiles" / f, tmp_path / "tiles" / f)
    shutil.copy(V2 / "wiring.json", tmp_path / "wiring.json")
    (tmp_path / "chars").mkdir()
    art2.set_root(tmp_path)
    ts = art2.tileset32()
    small = art2.tileset()
    assert ts is not None and not ts.native and all(t.get_size() == (32, 32) for t in ts.tiles)
    assert pygame.image.tobytes(ts.tiles[0], "RGB") == pygame.image.tobytes(
        pygame.transform.scale(small.tiles[0], (32, 32)), "RGB")
    terrain, native = art2.terrain32()
    assert not native and terrain["grass_path_n"][0].get_size() == (32, 32)
    o = types.SimpleNamespace(x=0, y=0, w=48, h=48, foot_y=48, type="", props={"sprite": "house", "variant": 0})
    from client.engine.view import View
    assert art2.prop_drawable(o, View(2)) is None             # no buildings atlas: the world draws the old one 2x


# ------------------------------------------------------------------ round 3: the rest of the old art
def test_every_pet_and_bee_species_has_its_own_sheet():
    pets = entries(data("creatures/pets.json")["species"])
    w = W()
    assert set(entries(w["pets"])) == set(pets)
    for sp in pets:
        s = art2.beast_for(sp)
        assert s is not None and s.id == f"pet_{sp}", sp                  # its own sheet, no borrowed beast
        assert all(s.has(c) for c in ("idle", "walk", "happy", "sleep")), sp
    bees = entries(data("creatures/bees.json"))
    assert set(entries(w["bees"])) == set(bees)
    for sp in bees:
        b = art2.bee(sp)
        assert b is not None and b.has("fly") and b.has("sting") and (b.fw, b.fh) == (32, 32), sp
        assert art2.bee_frame(sp, 0.1, True) is b.frame(b.index("fly", 0.1, "left"))
        assert art2.bee_frame(sp, 0.1, False, sting_t=0.05) is b.frame(b.index("sting", 0.05, "right"))


def test_the_garden_family_hash_is_stable_across_runs():
    import subprocess
    import sys
    keys = ["w_shui", "w_mu", "123", "Thủy", "a" * 40]
    here = [art2.plant_family(k) for k in keys]
    code = ("import sys, json; sys.path.insert(0, r'%s'); from client.engine import art2; "
            "print(json.dumps([art2.plant_family(k) for k in %r]))") % (ROOT, keys)
    for seed in ("1", "12345"):
        out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                             env={**__import__("os").environ, "PYTHONHASHSEED": seed}, check=True).stdout
        assert [tuple(x) for x in json.loads(out.strip().splitlines()[-1])] == here, seed
    fams = {art2.plant_family(f"k{i}")[0] for i in range(60)}
    assert fams == set(W()["garden"]["families"])                     # every family is used


def test_every_garden_realm_and_td_name_the_code_asks_for_exists():
    g = W()["garden"]
    for fam in g["families"]:
        for stage in range(6):
            for rar in g["rarities"]:
                key = next(k for k in (f"x{i}" for i in range(500)) if art2.plant_family(k)[0] == fam)
                assert art2.plant(stage, rar, key) is not None, (fam, stage, rar)
    assert art2.plant(5, "khong_co", "x0") is not None                 # an unknown rarity falls back
    for locked, dry in ((True, False), (False, False), (False, True)):
        assert art2.bed(locked, dry).get_size() == (64, 64)
    for rar in g["rarities"]:
        assert len(art2.seed_frames(rar)) == 3 and len(art2.egg_frames(rar)) == 3
    for bee_rarity in g["egg_by_bee_rarity"]:
        assert art2.egg_frames(bee_rarity)
    for deco in g["decorations"]:
        assert art2.decoration(deco) is not None, deco
    from client.scenes.realm import realm_v2_name
    calls = [("pedestal", a, b) for a in (True, False) for b in (True, False)] + \
        [("rune_tile", s) for s in ("off", "idle", "next", "done")] + \
        [("pillar", t, lit) for t in (1, 2, 3, 4) for lit in (True, False)] + \
        [("realm_exit", o, 1) for o in (True, False)] + [("chest", o) for o in (True, False)] + \
        [("statue", 1), ("mirror", 3), ("rift", 7)]
    from client.engine import sprites
    for call in calls:
        name, frame = realm_v2_name(*call)
        pr = art2.realm_prop(name)
        assert pr is not None and frame < len(pr.frames), call
        old = sprites.realm(*call)
        assert pr.img.get_size() == (old.get_width() * 2, old.get_height() * 2), (call, pr.img.get_size())
    td = W()["td"]
    for role in td["roles"]:
        for lv in (1, 2, 3):
            assert art2.td_prop(f"tower_{role}_{lv}") is not None, (role, lv)
    for role in td["shots"]:
        assert art2.td_prop(f"shot_{role}") and art2.td_prop(f"hit_{role}"), role
    for n in ("td_core", "td_spawn", "td_rock_0", "td_rock_1", "hit_puff"):
        assert art2.td_prop(n) is not None, n
    tiles = art2.td_tiles()
    assert tiles["grass"][0].get_size() == (24, 24)
    import itertools
    for sides in itertools.product((False, True), repeat=4):
        assert art2.td_path_name(*sides) in tiles, sides
    balance_roles = set(json.loads((DATA / "balance" / "td.json").read_text("utf-8"))["roles"])
    for role in balance_roles - set(td["roles"]):       # word-board roles with no v2 tower: the old plant stays
        assert art2.td_prop(f"tower_{role}_1") is None, role


def test_every_autotile_pair_has_its_tiles():
    terrain, native = art2.terrain32()
    assert native
    suffixes = ["nw", "n", "ne", "w", "e", "sw", "s", "se", "in_nw", "in_ne", "in_sw", "in_se"]
    whole = ["island", "h", "v", "cap_n", "cap_s", "cap_e", "cap_w"]
    from client.art import build as B
    names = {n for n, _ in B.TILESET}
    for cell, rule in entries(W()["autotile"]).items():
        assert cell in names and set(rule["outer"]) <= names, cell
        for suf in suffixes + (whole if rule["pair"] not in ("realm_edge", "shore") else []):
            assert f"{rule['pair']}_{suf}" in terrain, (cell, suf)


def test_stone_islands_are_round_and_dark_grass_gets_its_edge():
    from client.engine.tilemap import TileMap
    from client.art import build as B
    names = [n for n, _ in B.TILESET]
    m = TileMap(ROOT / "client" / "assets" / "maps" / "loan_so_coc.tmj")
    g = m.ground32()
    stone = [i for i, gid in enumerate(m.ground) if gid and names[gid - 1] == "stone"]
    lone = [i for i in stone if all(0 <= (i // m.w + dy) < m.h and 0 <= i % m.w + dx < m.w and
                                    names[m.ground[(i // m.w + dy) * m.w + i % m.w + dx] - 1] in ("grass", "dark_grass")
                                    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)))]
    assert lone, "the map has stone islands"
    x, y = (lone[0] % m.w) * 32, (lone[0] // m.w) * 32
    assert g.get_at((x + 1, y + 1)) != g.get_at((x + 16, y + 16))      # the corner is ground: rounded


CJK = __import__("re").compile(r"[⺀-鿿豈-﫿　-〿＀-￯]")
# Where a CJK character may stay in client code, and why. None of these reach the math game's screen
# as a hard-coded literal: comments, a regex that detects Chinese input, the full-width blank of the
# old word game's own Chinese sentences, and the protected strings file (listed in the report).
CJK_ALLOWED = {
    "client/art/sprites/people.py": "a code comment (the tone gag) - never drawn",
    "client/engine/td_sim.py": "code comments naming the old word combos - never drawn",
    "client/engine/text.py": "a docstring - never drawn",
    "client/scenes/quiz.py": "the CJK detector regex and the full-width blank inside the old word game's "
                             "own Chinese sentences (the sentence itself is Chinese)",
    "client/strings_vi.py": "protected file of another session - its Chinese is listed in the report",
}


def test_no_chinese_in_the_client_scene_and_ui_sources():
    bad = []
    for p in sorted((ROOT / "client").rglob("*.py")):
        rel = p.relative_to(ROOT).as_posix()
        if "/tests/" in rel or rel in CJK_ALLOWED:
            continue
        for i, line in enumerate(p.read_text("utf-8").splitlines(), 1):
            if CJK.search(line):
                bad.append(f"{rel}:{i}: {line.strip()[:80]}")
    assert not bad, "\n".join(bad)
