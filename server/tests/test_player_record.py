"""What other players are told about a player when it comes into view (the snapshot's `add`)."""
from app.realtime.zone import Player


def test_the_add_record_carries_the_realm_and_its_stage():
    """The client draws another player's kiếm khí by tier, which needs the stage as well as the
    realm (docs/PROTOCOL.md, Snapshot)."""
    p = Player(7, "Lão Mai", {}, "luyen_khi", 10.0, 20.0, stage=8)
    rec = p.full()
    assert rec["realm"] == "luyen_khi" and rec["stage"] == 8
    p.realm, p.stage = "truc_co", 1
    assert (p.full()["realm"], p.full()["stage"]) == ("truc_co", 1)
