"""Guard bees on a giant land: the monster a bee picks through the cells of `guard._Near` is the
one a scan of every monster picks (same candidates, same order, same choice). No database."""
import random

import pytest

from app.realtime import guard
from app.realtime import world as wmod
from app.realtime.world import World
from app.realtime.zone import ChannelZone, Player
from tests.test_giant_world import Mono, area, giant

ZONE = "rung_muc_loang"


@pytest.fixture(autouse=True)
def quiet_world(monkeypatch):
    monkeypatch.setattr(wmod, "world", World(mono=Mono()))


def test_a_bee_picks_through_the_cells_what_a_full_scan_picks(tmp_path):
    zmap = giant(tmp_path, [area(f"a{i}", 200 + (i % 8) * 480, 200 + (i // 8) * 480, 300, 300, "ink_slime", 6)
                            for i in range(64)])
    ch = ChannelZone(ZONE, 1, zmap, random.Random(2))
    assert len(ch.monsters) > 300
    rng = random.Random(5)
    p = Player(1, "Đạo Hữu", {}, "luyen_khi", 0.0, 0.0)
    r = float(guard.cfg()["range"])
    bee = guard.GuardBee(1, "ong_mat", 50, 5, 1.0)
    picked = 0
    for k in range(400):
        for m in ch.monsters:                     # the monsters anywhere (a respawn jumps), some shielded
            if rng.random() < 0.3:
                m.x, m.y = rng.uniform(0, 4096), rng.uniform(0, 4096)
            m.shield = rng.random() < 0.3
            m.engaged = {1} if rng.random() < 0.1 else set()
        if k % 7 == 0 and ch.monsters:            # two at the very same distance: the first in the list wins
            a, b = ch.monsters[3], ch.monsters[40]
            a.x, a.y, b.x, b.y = p.x + 10, p.y, p.x - 10, p.y
        p.x, p.y = rng.uniform(0, 4096), rng.uniform(0, 4096)
        bee.target = rng.choice(ch.monsters).eid if rng.random() < 0.3 else None
        near = guard._Near(ch.monsters, r)
        full = guard._pick(ch, p, bee, r)
        got = guard._pick(ch, p, bee, r, near)
        assert got is full
        picked += full is not None
    assert picked > 50
    near = guard._Near(ch.monsters, r / 4)        # cells narrower than the range: the whole list
    assert guard._pick(ch, p, bee, r, near) is guard._pick(ch, p, bee, r)
