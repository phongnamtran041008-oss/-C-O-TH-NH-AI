"""Gear lying on the ground where a monster died (client/engine/ground_loot.py), the weapon spots'
glow, and the linh căn mark - with no server and no window."""
import json
from pathlib import Path
from types import SimpleNamespace

import pygame

from client.engine import ground_loot as G
from client.engine.view import View
from client.engine.vfx import Vfx

ROOT = Path(__file__).resolve().parents[2]


def piece(**kw):
    e = {"item": "kiem_2", "item_id": "kiem_2", "name_vi": "Thiết Kiếm", "rarity": "huyen", "color": "#4A7CC8",
         "quality": "thuong", "quality_vi": "Thượng phẩm", "weapon": True, "slot": "weapon", "x": 100.0, "y": 80.0}
    e.update(kw)
    return e


def test_a_piece_pops_lies_and_is_picked_up_with_its_toast_once():
    g, shown, vfx = G.GroundLoot(), [], Vfx()
    assert g.add(piece(), 10.0, ("Nhận Thiết Kiếm", "#4A7CC8"))
    d = g.drops[0]
    assert d.state == "pop"
    far = (200.0, 200.0)
    g.update(10.1, *far, shown.append)
    x, y, lift = g.where(d, 10.4, *far)
    assert lift > 2                                     # in the air, hopping out of the monster
    g.update(10.0 + G.WAIT + G.POP + 0.01, *far, lambda *a: shown.append(a))
    assert d.state == "lie" and not shown
    assert g.near(100.0, 100.0) == [d] and not g.near(*far)
    g.update(11.0, 104.0, 82.0, lambda *a: shown.append(a), vfx)      # the player walks onto it
    assert d.state == "pick" and not shown              # flying into the player: no toast yet
    g.update(11.0 + G.FLY + 0.01, 104.0, 82.0, lambda *a: shown.append(a), vfx)
    assert shown == [("Nhận Thiết Kiếm", "#4A7CC8")] and not g.drops
    assert any(it.fid == "roi_nhat" for it in vfx.live)
    g.update(20.0, 104.0, 82.0, lambda *a: shown.append(a))
    g.collect_all(lambda *a: shown.append(a))
    assert len(shown) == 1


def test_a_piece_without_a_place_is_not_taken():
    g = G.GroundLoot()
    assert not g.add(piece(x=None, y=None), 0.0, ("x", "#fff"))
    assert not g.add(piece(x="nowhere"), 0.0, ("x", "#fff"))
    assert not g.drops


def test_after_a_while_it_comes_to_the_player_by_itself():
    g, shown = G.GroundLoot(), []
    g.add(piece(), 0.0, ("t", "#fff"))
    g.update(1.0, 900.0, 900.0, lambda *a: shown.append(a))
    g.update(G.WAIT + G.TIMEOUT + 0.5, 900.0, 900.0, lambda *a: shown.append(a))
    assert g.drops[0].state == "pick"
    g.update(G.WAIT + G.TIMEOUT + 1.0, 900.0, 900.0, lambda *a: shown.append(a))
    assert shown == [("t", "#fff")]


def test_leaving_the_zone_collects_everything_and_still_toasts_each_once():
    from client.scenes.world import WorldScene
    ws = WorldScene.__new__(WorldScene)
    shown = []
    ws.game = SimpleNamespace(toast=lambda *a: shown.append(a), now=0.0,
                              enter_abode=lambda *a: shown.append("abode"))
    ws.ground_loot = G.GroundLoot()
    for i in range(3):
        ws.ground_loot.add(piece(name_vi=f"m{i}"), 0.0, (f"Nhận m{i}", "#fff"))
    ws.on_net({"t": "zone", "zone": "abode", "x": 0, "y": 0})
    assert shown == [("Nhận m0", "#fff"), ("Nhận m1", "#fff"), ("Nhận m2", "#fff"), "abode"]
    assert not ws.ground_loot.drops


def test_too_many_on_the_ground_the_oldest_goes_to_the_bag():
    g = G.GroundLoot()
    for i in range(G.MAX_LYING + 3):
        g.add(piece(), 0.0, (str(i), "#fff"))
    assert sum(1 for d in g.drops if d.state != "pick") == G.MAX_LYING


def test_every_rarity_draws_its_ring_column_and_icon():
    view = View(2)
    for r in G.RARITIES:
        g = G.GroundLoot()
        g.add(piece(rarity=r, x=60.0, y=60.0), 0.0, None)
        g.update(5.0, 500.0, 500.0, None)
        for layer in ("ground", "over"):
            s = pygame.Surface((240, 200))
            (g.draw_ground if layer == "ground" else g.draw_over)(s, view, 1.0, 5.0)
            assert pygame.image.tobytes(s, "RGB").strip(b"\x00"), (r, layer)
        assert g.drawables(view, 5.0, 500.0, 500.0), r


def test_the_colour_tables_agree_with_the_server_data():
    from client.scenes import world as W
    giai = json.loads((ROOT / "server" / "data" / "linh_can.json").read_text("utf-8"))["giai"]
    assert list(W.LC_COLORS) == [g["color"] for g in giai]
    plan = json.loads((ROOT / "server" / "data" / "math" / "world_plan.json").read_text("utf-8"))
    assert W.QUALITY_RARITY == {q["id"]: q["rarity"] for q in plan["qualities"]}
    assert W.spot_rarity("kiem_1_cuc") == "dia" and W.spot_rarity("am_khi_3_tuyet") == "thien"


def test_the_linh_can_mark_is_small_and_in_the_giai_colour():
    from client.scenes import world as W
    fills = []
    ui = SimpleNamespace(fill=lambda x, y, w, h, c: fills.append((w, h, c)))
    W.WorldScene.draw_lc_mark(ui, 50, 50, 3)
    assert max(w for w, h, c in fills) <= 7 and max(h for w, h, c in fills) <= 7
    assert any(c == W.LC_COLORS[2] for _, _, c in fills)
    ws = W.WorldScene.__new__(W.WorldScene)
    ws.game = SimpleNamespace(state=SimpleNamespace(me={"id": 1}, cult={"stats": {"lc": 7}}))
    ws.entities = {"p2": W.Ent("p2", "p", "x", lc=4), "m1": W.Ent("m1", "m", "y")}
    assert (ws.linh_can_of("p1"), ws.linh_can_of("p2"), ws.linh_can_of("m1"), ws.linh_can_of(None)) == (7, 4, 0, 0)
