"""Linh thú and thần thông on the client side, without a server: the glide geometry is the
server's own, the tile names agree, and every beast of Thiên Địa Đồ is drawn from its v2 sheet."""
from __future__ import annotations

import json
import sys

from client.engine import art2, petfollow
from client.engine import glide as cg
from client.tests.driver import ROOT

sys.path.insert(0, str(ROOT / "server"))

from app.realtime import maps  # noqa: E402

PLAN = json.loads((ROOT / "server" / "data" / "math" / "world_plan.json").read_text("utf-8"))


def test_the_glide_geometry_is_the_servers_line_for_line():
    """Prediction and the landing the client picks only hold if both sides compute the same."""
    a = (ROOT / "server" / "app" / "realtime" / "glide.py").read_text("utf-8").splitlines()
    b = (ROOT / "client" / "engine" / "glide.py").read_text("utf-8").splitlines()
    assert a == b


def test_the_ground_tiles_are_named_alike():
    from client.art import build as B
    assert tuple(n for n, _ in B.TILESET) == maps.TILE_NAMES


def test_the_client_picks_the_landing_the_server_accepts():
    g = next(u for u in PLAN["unlocks"] if u["id"] == "dap_kiem_luot")["glide"]
    over = set(g["over_tiles"])
    for name, (tx, ty) in (("loan_so_coc", (51, 6)), ("luu_van_coc", (20, 6))):
        z = maps.load(name)
        x, y = tx * 16 + 8.0, ty * 16 + 12.0
        to = cg.pick(z.collider, z.tile_name, over, x, y, 0, -1, g["max_px"], g["min_px"])
        assert to is not None, name
        assert cg.check(z.collider, z.tile_name, over, x, y, *to, g["max_px"], g["min_px"]) is None
        assert int((to[1] - 1) // 16) < ty - 2, "it lands past the gap"


def test_every_built_beast_has_its_own_sheet_with_the_fight_clips():
    built = [b for b in PLAN["beasts"] if b["status"] == "co"]
    assert len(built) == 5
    for b in built:
        s = petfollow.sheet(b["id"])
        assert s is not None and s.id == b["id"], b["id"]
        for clip in ("idle", "walk", "windup", "attack", "hit", "die", "happy"):
            assert s.has(clip), (b["id"], clip)
        assert petfollow.is_spirit_beast(b["id"]) and petfollow.picture(b["id"]) is not None
    assert not petfollow.is_spirit_beast("cho") and petfollow.sheet("cho") is art2.beast_for("cho")


def test_the_mount_is_drawn_larger_under_its_rider():
    from client.engine.view import View
    v = View(2)
    small = petfollow.drawable("tieu_long", 100, 100, False, 0, 0, False, v)
    big = petfollow.mount_drawable("tieu_long", 100, 100, "right", False, 0, 0, v)
    assert big[1].get_width() == int(small[1].get_width() * petfollow.MOUNT_SCALE)
    body = art2.char("luyen_khi")
    assert body.has(petfollow.RIDER_CLIP) and body.has("fly")
    sword = art2.weapon(next(u for u in PLAN["unlocks"] if u["id"] == "dap_kiem_luot")["glide"]["sheet"])
    assert sword is not None and sword.has("fly")
    tran = next(u for u in PLAN["unlocks"] if u["id"] == "phap_tran")["formation"]["fx"]
    assert art2.fx(tran) is not None and art2.fx("capture_seal") is not None
