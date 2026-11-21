"""Chỉ Đường (systems/navigation.py): which khu or land fits this player's place in Đạo Thụ.

The rule is pure (`recommend`) and is tested on synthetic lands and khu - no map has khu yet -
plus once through the real route for a newcomer and for a player further in the tree.
"""
from __future__ import annotations

import pytest

from app.realtime import lands
from app.systems import math_tree_progress, navigation as nav
from app.systems.navigation import BranchPos, Learning
from tests.helpers import register

ORDER = {"luyen_khi": 1, "truc_co": 2}
BRANCH_LANDS = [("kiem_trung_son", "loan_so_coc", "ds"), ("luu_van_coc", "luu_van_coc", "gt"),
                ("van_tuong_trach", "ho_nghien_muc", "xs"), ("me_do_lam", "rung_muc_loang", "tr")]


def land(lid, zone, branch, open_=True, kind="wild", reason=None):
    return {"id": lid, "name_vi": lid.replace("_", " ").title(), "branch": branch, "kind": kind,
            "realm": "luyen_khi", "zone": zone, "built": True, "open": open_, "reason_vi": reason}


def world_rows(**extra):
    rows = [land("truc_lam_thon", "truc_lam_thon", None, kind="hub")]
    rows += [land(l, z, b) for l, z, b in BRANCH_LANDS]
    rows += [land("thien_cong_phuong", "thien_cong_phuong", "lt", open_=False, reason="Chưa vào được: cần tầng 1."),
             land("linh_xa_nguyen", "linh_xa_nguyen", "ud", open_=False, reason="Chưa vào được: cần tầng 2."),
             land("loi_kiep_dai", "loi_kiep_dai", None, open_=False, kind="boss", reason="Chưa vào được: tầng 9."),
             {**land("van_hai", None, "ml"), "built": False, "zone": None}]
    for r in rows:
        r.update(extra.get(r["id"], {}))
    return rows


def khu(kid, zone, band, lo, hi, anchor=(100, 200), safe=False):
    return {"id": kid, "zone": zone, "name_vi": f"Khu {kid}", "band": band, "stage_min": lo, "stage_max": hi,
            "anchor": list(anchor), "rect": [0, 0, 10, 10], "safe": safe}


GIANT = {"loan_so_coc": (khu("kts_an", "loan_so_coc", 0, 0, 0, (5, 5), safe=True),
                         khu("kts_ngoai", "loan_so_coc", 1, 1, 3, (300, 400)),
                         khu("kts_trung", "loan_so_coc", 2, 4, 6, (1500, 900)),
                         khu("kts_tham", "loan_so_coc", 3, 7, 9, (3000, 2000))),
         "luu_van_coc": (khu("lvc_ngoai", "luu_van_coc", 1, 1, 3, (40, 50)),
                         khu("lvc_trung", "luu_van_coc", 2, 4, 6, (60, 70)))}


def khu_of(zone):
    return GIANT.get(zone, ())


def spawn_of(zone, name):
    return {"from_village": (11, 22), "spawn": (448, 336), "from_abode": (448, 528)}[name]


def learner(stage=0, **branches) -> Learning:
    return Learning("luyen_khi", stage, "Luyện Khí", 9,
                    {b: BranchPos("luyen_khi", s, f"Nút {b} {s}") for b, s in branches.items()})


def plan(learn, rows=None, khus=khu_of):
    return nav.recommend(learn, rows or world_rows(), khus, spawn_of, ORDER, {"ds": "Đại Số Tuyến Tính"})


# ------------------------------------------------------------------ the pure rule
def test_a_newcomer_goes_to_band_1_of_the_first_land():
    out = plan(learner())                       # nothing done: no branch position at all
    r = out["recommended"]
    assert (r["kind"], r["land"], r["zone"], r["khu"]) == ("recommended", "kiem_trung_son", "loan_so_coc", "kts_ngoai")
    assert (r["band"], r["stage_min"], r["stage_max"], r["x"], r["y"]) == (1, 1, 3, 300, 400)
    assert r["fit_vi"] == "hợp Luyện Khí tầng 1-3" and r["reason_vi"]
    assert out["stage"] == {"realm": "luyen_khi", "realm_vi": "Luyện Khí", "stage": 0, "working": 1}


def test_without_khu_the_destination_is_the_land_at_its_village_entry():
    out = plan(learner(ds=1, gt=1, xs=1, tr=1), khus=lambda z: ())
    r = out["recommended"]
    assert (r["land"], r["khu"], r["band"], r["x"], r["y"]) == ("kiem_trung_son", None, None, 11, 22)
    assert r["name_vi"] == r["land_vi"] and "quái" in r["reason_vi"] and "Đại Số Tuyến Tính" in r["reason_vi"]


def test_the_lowest_frontier_wins_and_ties_go_ds_gt_xs_tr():
    assert plan(learner(ds=5, gt=2, xs=3, tr=2))["recommended"]["land"] == "luu_van_coc"     # gt beats tr on a tie
    assert plan(learner(ds=4, gt=4, xs=1, tr=4))["recommended"]["land"] == "van_tuong_trach"
    assert plan(learner(ds=2, gt=2, xs=2, tr=2))["recommended"]["land"] == "kiem_trung_son"


def test_the_khu_holds_the_learning_stage():
    r = plan(learner(stage=4, ds=5, gt=6, xs=7, tr=8))["recommended"]
    assert (r["khu"], r["stage_min"], r["stage_max"]) == ("kts_trung", 4, 6)
    assert r["fit_vi"] == "hợp Luyện Khí tầng 4-6" and "Khu kts_trung" in r["reason_vi"]
    r = plan(learner(stage=7, ds=8, gt=9, xs=9, tr=9))["recommended"]
    assert r["khu"] == "kts_tham" and (r["x"], r["y"]) == (3000, 2000)


def test_a_stage_outside_every_khu_takes_the_deepest_below_else_the_shallowest():
    gappy = (khu("a", "z", 1, 2, 3), khu("b", "z", 2, 6, 7), khu("c", "z", 3, 9, 9))
    assert nav.fit_khu(gappy, 5)["id"] == "a"
    assert nav.fit_khu(gappy, 8)["id"] == "b"
    assert nav.fit_khu(gappy, 1)["id"] == "a"
    assert nav.fit_khu((khu("safe", "z", 0, 1, 9, safe=True),), 3) is None     # a safe khu is never a goal


def test_every_other_open_land_is_an_alternative_and_the_locked_ones_say_why():
    out = plan(learner(ds=1, gt=4, xs=2, tr=3))
    assert [d["land"] for d in out["lands"]] == ["luu_van_coc", "van_tuong_trach", "me_do_lam"]
    gt = out["lands"][0]
    assert gt["khu"] == "lvc_trung" and gt["kind"] == "land"          # its own branch's stage: 4
    assert [d["land"] for d in out["locked"]] == ["thien_cong_phuong", "linh_xa_nguyen", "loi_kiep_dai"]
    assert all(d["reason_vi"].startswith("Chưa vào được") and not d["open"] for d in out["locked"])
    assert "van_hai" not in {d["land"] for d in out["lands"] + out["locked"]}           # not built
    assert "truc_lam_thon" not in {d["land"] for d in out["lands"]}                     # the hub is the village


def test_home_ends_at_the_abode_gate_and_the_village_at_its_centre():
    out = plan(learner())
    assert (out["home"]["zone"], out["home"]["via"], out["home"]["x"], out["home"]["y"]) == \
        ("abode", "truc_lam_thon", 448, 528)
    assert (out["village"]["zone"], out["village"]["x"], out["village"]["y"]) == ("truc_lam_thon", 448, 336)


def test_the_exercise_lands_compete_by_their_own_nodes_when_open():
    rows = world_rows(thien_cong_phuong={"open": True, "reason_vi": None})
    out = plan(learner(stage=2, ds=3, gt=3, xs=3, tr=3, lt=2), rows)
    assert out["recommended"]["land"] == "thien_cong_phuong" and out["recommended"]["learning_stage"] == 2
    out = plan(learner(stage=2, ds=2, gt=3, xs=3, tr=3, lt=2), rows)      # a math branch wins the tie
    assert out["recommended"]["land"] == "kiem_trung_son"


def test_loi_kiep_dai_comes_first_once_open_at_the_last_stage():
    rows = world_rows(loi_kiep_dai={"open": True, "reason_vi": None})
    out = plan(learner(stage=9, ds=9, gt=9, xs=9, tr=9), rows)
    assert out["recommended"]["land"] == "loi_kiep_dai" and "Lôi Kiếp Đài" in out["recommended"]["reason_vi"]
    assert plan(learner(stage=8, ds=9, gt=9, xs=9, tr=9), rows)["recommended"]["land"] != "loi_kiep_dai"


def test_a_frontier_in_a_later_realm_counts_as_the_last_stage_of_the_land():
    assert nav.stage_in(BranchPos("truc_co", 1), "luyen_khi", ORDER) == 9
    assert nav.stage_in(None, "luyen_khi", ORDER) == 1
    assert nav.stage_in(BranchPos("luyen_khi", 0), "luyen_khi", ORDER) == 1


def test_no_open_land_means_no_recommendation():
    rows = [r | {"open": False} for r in world_rows()]
    out = plan(learner(), rows)
    assert out["recommended"] is None and out["lands"] == [] and out["home"] and out["village"]


# ------------------------------------------------------------------ through the real tree and route
async def test_the_route_sends_a_newcomer_to_kiem_trung_son(client):
    h, _ = await register(client, "chiduong1")
    r = await client.get("/nav/destinations", headers=h)
    assert r.status_code == 200, r.text
    out = r.json()
    rec = out["recommended"]
    assert rec["land"] == "kiem_trung_son" and rec["zone"] == lands.zone_of("kiem_trung_son")
    assert rec["khu"] is None or rec["band"] == 1                  # band 1 once the map has khu
    assert rec["reason_vi"] and out["stage"]["stage"] == 0
    zones = {d["zone"] for d in out["lands"]} | {d["zone"] for d in out["locked"]} | {rec["zone"]}
    assert {"luu_van_coc", "ho_nghien_muc", "rung_muc_loang", "thien_cong_phuong"} <= zones
    assert any(d["land"] == "thien_cong_phuong" and "tầng 1" in d["reason_vi"] for d in out["locked"])
    assert out["home"]["zone"] == "abode" and out["village"]["zone"] == "truc_lam_thon"
    assert (await client.get("/nav/destinations")).status_code == 401


async def test_learning_of_reads_the_frontier_of_every_branch(client, db):
    await register(client, "chiduong2")
    from sqlalchemy import select
    from app.models import User
    user = (await db.execute(select(User).where(User.username == "chiduong2"))).scalar_one()
    st = await math_tree_progress.state(db, user.id)
    learn = nav.learning_of(st)
    assert (learn.realm, learn.stage, learn.working) == ("luyen_khi", 0, 1)
    for b in ("ds", "gt", "xs", "tr"):
        assert learn.by_branch[b].stage == 1 and learn.by_branch[b].node_vi, (b, learn.by_branch.get(b))


@pytest.mark.parametrize("zone", ["loan_so_coc", "truc_lam_thon"])
def test_the_spawns_it_walks_to_exist(zone):
    from app.realtime import maps
    from app.realtime.world import zone_defs
    m = maps.load(zone_defs()[zone]["map"])
    name = "from_village" if zone != "truc_lam_thon" else "from_abode"
    assert name in m.spawns
