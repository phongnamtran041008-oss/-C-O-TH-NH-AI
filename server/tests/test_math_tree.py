"""The curriculum tree (data/math/tree.json) and the world plan hung on it
(data/math/world_plan.json): the shipped files are sound, and the checker really catches the
mistakes it claims to."""
import copy
import json

import pytest

from app.learning import math_tree as mt


@pytest.fixture(scope="module")
def raw():
    return json.loads((mt.MATH_DIR / mt.TREE_FILE).read_text("utf-8"))


@pytest.fixture(scope="module")
def plan():
    return json.loads((mt.MATH_DIR / mt.WORLD_FILE).read_text("utf-8"))


@pytest.fixture(scope="module")
def skills():
    return mt.subject_skills()


@pytest.fixture(scope="module")
def problems():
    return mt.problem_ids()


def check(raw, skills, problems):
    return mt.validate_tree(raw, skills, problems)


def node(raw, node_id):
    return next(n for n in raw["nodes"] if n["id"] == node_id)


# ------------------------------------------------------------------ the shipped files
def test_the_shipped_tree_and_world_plan_are_sound():
    assert mt.validate_all() == []


def test_every_micro_skill_is_placed_exactly_once(skills):
    t = mt.tree()
    placed = [s for n in t.nodes.values() for s in n.skills]
    assert len(placed) == len(set(placed))
    assert set(placed) | t.cut_skills() == set(skills)
    assert not set(placed) & t.cut_skills()


def test_the_cut_list_is_only_the_hidden_talent_floors(skills):
    """What is thrown away is the proof-heavy 'hệ tài năng' material, nothing else."""
    t = mt.tree()
    assert t.cut_skills()
    assert all("_t10_" in s for s in t.cut_skills())


def test_the_main_path_is_most_of_the_material_but_not_all_of_it(skills):
    t = mt.tree()
    status = [t.skill_status(s) for s in skills]
    assert status.count("chinh") > status.count("phu") > status.count("cut") > 0


def test_luyen_khi_has_nine_stages_each_with_math_and_code():
    t = mt.tree()
    assert t.realm_stages["luyen_khi"] == 9
    for stage in range(1, 10):
        here = [n for n in t.main_nodes("luyen_khi") if n.stage == stage]
        assert any(n.kind == "toan" for n in here), stage
        assert any(n.kind in ("code", "thuc_chien", "du_an") for n in here), stage


def test_branches_are_learned_side_by_side_not_one_after_another():
    """The point of the tree: a newcomer can start four math branches and programming at
    once, and plenty of nodes need a node of another branch."""
    t = mt.tree()
    first = [t.nodes[n] for n in t.open_nodes([]) if t.nodes[n].main]
    assert {n.branch for n in first} == {"ds", "gt", "xs", "tr", "lt"}
    cross = [n for n in t.main_nodes("luyen_khi")
             if any(t.nodes[r].branch != n.branch for r in n.requires)]
    assert len(cross) >= 20


def test_every_node_after_the_first_stage_reviews_something_older():
    t = mt.tree()
    for n in t.main_nodes():
        if n.requires:
            assert n.reinforces, n.id
            assert set(n.reinforces) <= t.ancestors(n.id), n.id


def test_eight_realms_as_the_author_listed_them():
    t = mt.tree()
    order = sorted(t.realm_order, key=t.realm_order.get)
    assert order == ["luyen_khi", "truc_co", "ket_dan", "nguyen_anh", "hoa_than",
                     "luyen_hu", "hop_the", "dai_thua"]


# ------------------------------------------------------------------ a player's position
def test_a_newcomer_is_at_stage_zero_and_sees_only_the_roots():
    t = mt.tree()
    assert t.stage_reached([]) == ("luyen_khi", 0)
    assert all(not t.nodes[n].requires for n in t.open_nodes([]))


def test_finishing_the_first_stage_needs_every_branch_including_code():
    t = mt.tree()
    stage1 = [n for n in t.main_nodes("luyen_khi") if n.stage == 1]
    math_skills = [s for n in stage1 for s in n.skills]
    code_nodes = [n.id for n in stage1 if not n.skills]
    assert code_nodes                                       # there is programming at stage 1
    assert t.stage_reached(math_skills) == ("luyen_khi", 0)             # math alone is not enough
    assert t.stage_reached(math_skills, code_nodes) == ("luyen_khi", 1)
    opened = t.open_nodes(math_skills, code_nodes)
    assert "ds_vecto_ma_tran" in opened and "ds_ngon_ngu" not in opened


def test_a_node_opens_only_when_the_other_branch_it_needs_is_done():
    """Continuous random variables need integrals: probability waits for calculus."""
    t = mt.tree()
    xs_before = [s for n in ("xs_dem_su_kien", "xs_xac_suat", "xs_dieu_kien", "xs_bnn_roi_rac")
                 for s in t.nodes[n].skills]
    assert "xs_bnn_lien_tuc" not in t.open_nodes(xs_before)
    gt = [s for n in ("gt_ham_so", "gt_gioi_han", "gt_dao_ham", "gt_tich_phan") for s in t.nodes[n].skills]
    assert "xs_bnn_lien_tuc" in t.open_nodes(xs_before + gt)


def test_finishing_everything_reaches_the_top():
    t = mt.tree()
    everything = [s for n in t.nodes.values() for s in n.skills]
    named = [n.id for n in t.nodes.values() if not n.skills]
    assert t.stage_reached(everything, named) == ("dai_thua", 3)
    assert t.open_nodes(everything, named) == []


def test_optional_nodes_never_hold_a_stage_back():
    t = mt.tree()
    main_skills = [s for n in t.main_nodes("luyen_khi") for s in n.skills]
    named = [n.id for n in t.main_nodes("luyen_khi") if not n.skills]
    assert t.stage_reached(main_skills, named) == ("truc_co", 0)


def test_review_skills_come_from_the_reinforced_nodes():
    t = mt.tree()
    got = t.review_skills("gt_nhieu_bien")
    assert set(got) == {s for r in t.nodes["gt_nhieu_bien"].reinforces for s in t.nodes[r].skills}
    assert any(s.startswith("dstt_") for s in got)          # calculus reviewing linear algebra


# ------------------------------------------------------------------ the checker bites
def test_a_cycle_is_caught(raw, skills, problems):
    bad = copy.deepcopy(raw)
    node(bad, "ds_ngon_ngu")["requires"] = ["ds_pca_svd"]
    assert any("circle" in e for e in check(bad, skills, problems))


def test_a_node_that_needs_a_later_stage_is_caught(raw, skills, problems):
    bad = copy.deepcopy(raw)
    node(bad, "tr_logic_dem")["requires"].append("ds_vecto_ma_tran")   # a stage-1 node, a stage-2 need
    assert any("comes later" in e for e in check(bad, skills, problems))


def test_a_skill_taught_before_its_prerequisite_is_caught(raw, skills, problems):
    bad = copy.deepcopy(raw)
    node(bad, "xs_bnn_lien_tuc")["requires"] = ["gt_tich_phan"]     # drops xs_bnn_roi_rac
    assert any("not learned before it" in e for e in check(bad, skills, problems))


def test_a_main_path_skill_leaning_on_an_optional_one_is_caught(raw, skills, problems):
    bad = copy.deepcopy(raw)
    del bad["waivers"]["gt_t6_don_dieu"]
    errs = check(bad, skills, problems)
    assert any("gt_t5_rolle_lagrange" in e for e in errs)


def test_a_forgotten_or_doubled_micro_skill_is_caught(raw, skills, problems):
    bad = copy.deepcopy(raw)
    node(bad, "ds_ngon_ngu")["skills"].remove("dstt_t1_tap_hop")
    assert any("nowhere in the tree" in e for e in check(bad, skills, problems))
    bad = copy.deepcopy(raw)
    node(bad, "gt_ham_so")["skills"].append("dstt_t1_tap_hop")
    assert any("more than once" in e for e in check(bad, skills, problems))


def test_a_dangling_node_is_caught(raw, skills, problems):
    bad = copy.deepcopy(raw)
    project = node(bad, "du_an_luyen_khi")
    project["requires"].remove("ud_ab_test")
    assert any("dangling" in e for e in check(bad, skills, problems))


def test_reviewing_something_not_yet_learned_is_caught(raw, skills, problems):
    bad = copy.deepcopy(raw)
    node(bad, "gt_ham_so")["reinforces"] = ["ds_pca_svd"]
    assert any("not one of its ancestors" in e for e in check(bad, skills, problems))


def test_a_stage_without_programming_is_caught(raw, skills, problems):
    bad = copy.deepcopy(raw)
    for n in bad["nodes"]:
        if n["realm"] == "luyen_khi" and n.get("stage") == 2 and n["kind"] == "code":
            n["stage"] = 3
    assert any("no programming" in e for e in check(bad, skills, problems))


# ------------------------------------------------------------------ the world plan
def test_questions_only_come_when_a_monster_lands_a_blow(plan):
    combat = plan["combat"]
    assert combat["question_rule"] == "on_hit"
    assert combat["right_answer"]["damage_taken"] == 0
    assert combat["hit_during_cooldown"]["question"] is False
    assert combat["question_cooldown_seconds"] > 0


def test_every_luyen_khi_branch_has_a_land_and_its_own_weapon(plan):
    t = mt.tree()
    types = {w["branch"]: w for w in plan["weapon_types"] if not w.get("drop_only")}   # kỳ binh only drop
    lands = {l["id"]: l for l in plan["lands"]}
    for branch in ("ds", "gt", "xs", "tr", "lt", "ud"):
        w = types[branch]
        assert lands[w["land"]]["branch"] == branch
        placed = [p for p in plan["weapons_placed"] if p["weapon"].startswith(w["id"] + "_")]
        assert len(placed) >= 4
        stages = [p["requires"]["stage"] for p in placed if p["requires"]["realm"] == "luyen_khi"]
        assert stages == sorted(stages) and stages[0] < stages[-1]
        for p in placed:                    # the requirement is a piece of that branch's syllabus
            assert all(n in t.nodes for n in p["requires"]["nodes"])


def test_flight_comes_with_truc_co_and_a_glide_before_it(plan):
    unlocks = {u["id"]: u for u in plan["unlocks"]}
    assert (unlocks["ngu_kiem_phi_hanh"]["realm"], unlocks["ngu_kiem_phi_hanh"]["stage"]) == ("truc_co", 0)
    assert unlocks["dap_kiem_luot"]["realm"] == "luyen_khi"
    sky = next(l for l in plan["lands"] if l["kind"] == "sky")
    assert sky["needs"] == "ngu_kiem_phi_hanh"


def test_every_realm_unlocks_something(plan):
    t = mt.tree()
    assert {u["realm"] for u in plan["unlocks"]} == set(t.realm_order)


def test_beasts_are_tamed_by_parrying_not_by_extra_questions(plan):
    assert len(plan["beasts"]) >= 6
    assert all(b["parries_to_tame"] >= 1 for b in plan["beasts"])


def test_the_world_checker_bites(plan):
    t = mt.tree()
    bad = copy.deepcopy(plan)
    bad["weapons_placed"][0]["requires"]["nodes"] = ["ds_pca_svd"]      # a stage-9 node at stage 1
    assert any("asks for ds_pca_svd" in e for e in mt.validate_world(bad, t))
    bad = copy.deepcopy(plan)
    bad["weapons_placed"][0]["weapon"] = "kiem_5"                       # far above the realm
    assert any("too high" in e for e in mt.validate_world(bad, t))
    bad = copy.deepcopy(plan)
    bad["beasts"][0]["needs"] = "ngu_kiem_phi_hanh"                     # flight before Trúc Cơ
    assert any("unlocks later" in e for e in mt.validate_world(bad, t))
    bad = copy.deepcopy(plan)
    bad["combat"]["question_rule"] = "always"
    assert any("question_rule" in e for e in mt.validate_world(bad, t))


def test_the_combat_lands_weapons_beasts_and_abilities_sections_are_wired(plan):
    """The owner's waves: the fight rule, the lands of Luyện Khí, the weapons (and their drops from
    monsters), the beasts of Luyện Khí with their taming and its thần thông run in the game; what
    lies beyond Luyện Khí does not."""
    assert plan["wired"] is False
    assert plan["wired_sections"] == ["combat", "lands", "weapons", "beasts", "abilities", "weapon_drops"]
    assert mt.wired_sections(plan) == ("combat", "lands", "weapons", "beasts", "abilities", "weapon_drops")
    assert all(mt.section_wired(s, plan) for s in mt.WIREABLE_SECTIONS)
    assert mt.wired_sections({"wired": False}) == ()
    assert mt.wired_sections({"wired": True}) == mt.WIREABLE_SECTIONS
    unlocks = {u["id"]: u for u in plan["unlocks"]}
    dodge = unlocks[plan["combat"]["dodge"]["unlock"]]
    assert (dodge["id"], dodge["realm"], dodge["stage"], dodge["status"]) == ("ne_don", "luyen_khi", 1, "co")


@pytest.mark.parametrize("change, message", [
    (lambda p: p.__setitem__("wired_sections", ["thu_cung"]), "wired_sections"),
    (lambda p: p.__setitem__("wired_sections", ["combat", "combat"]), "wired_sections"),
    (lambda p: p["combat"]["dodge"].pop("dash_px"), "dodge.dash_px"),
    (lambda p: p["combat"]["dodge"].__setitem__("invulnerable_seconds", 2), "shorter than cooldown"),
    (lambda p: p["combat"]["dodge"].__setitem__("unlock", "bay"), "unknown ability"),
    (lambda p: p["combat"]["right_answer"].__setitem__("counter_multiplier", 0.5), "counter_multiplier"),
    (lambda p: p["combat"]["right_answer"].__setitem__("gives_tu_vi", False), "gives_tu_vi"),
    (lambda p: p["combat"]["wrong_answer"].__setitem__("damage_taken", 1.5), "wrong_answer.damage_taken"),
    (lambda p: p["combat"]["hit_during_cooldown"].__setitem__("question", True), "hit_during_cooldown.question"),
    (lambda p: p["combat"]["telegraph"]["by_rank"].__setitem__("elite", ["spiral"]), "by_rank.elite"),
    (lambda p: p["combat"]["telegraph"]["by_rank"].pop("boss"), "by_rank"),
    (lambda p: p["combat"]["telegraph"].__setitem__("cone_degrees", 270), "cone_degrees"),
    (lambda p: p["combat"].__setitem__("shielded_ranks", ["normal", "elite"]), "shielded_ranks"),
    (lambda p: p["combat"].pop("question_wait_seconds"), "question_wait_seconds"),
])
def test_a_wired_combat_section_is_checked_number_by_number(plan, change, message):
    t = mt.tree()
    bad = copy.deepcopy(plan)
    change(bad)
    assert any(message in e for e in mt.validate_world(bad, t)), mt.validate_world(bad, t)


# ------------------------------------------------------------------ the lands (wired 2026-11-20)
def test_every_land_of_luyen_khi_is_built_and_the_sky_land_waits(plan):
    lands = {l["id"]: l for l in plan["lands"]}
    built = [l for l in plan["lands"] if l["realm"] == "luyen_khi"]
    assert len(built) == 8 and all(l["status"] == "co" and l["map"] for l in built)
    assert lands["van_hai_thien_dao"]["status"] == "chua_co" and lands["van_hai_thien_dao"]["map"] is None
    for p in plan["weapons_placed"]:
        assert ("pos" in p) == (lands[p["land"]]["status"] == "co"), p


@pytest.mark.parametrize("change, message", [
    (lambda p: p["weapons_placed"][0].pop("pos"), "needs a pos"),
    (lambda p: p["weapons_placed"][0].__setitem__("pos", [0, 0]), "not a walkable tile"),
    (lambda p: p["weapons_placed"][0].__setitem__("pos", [500, 2]), "off the map"),
    (lambda p: p["weapons_placed"][-1].__setitem__("pos", [3, 3]), "is not built"),
    (lambda p: p["lands"][1].__setitem__("map", "khong_co"), "draws map"),
    (lambda p: p["lands"][1].__setitem__("monsters", ["kiem_linh", "ma_gi_do"]), "does not exist"),
    (lambda p: p["lands"][1].__setitem__("monsters", ["kiem_linh", "van_xa"]), "never spawns"),
    (lambda p: p["lands"][-1].__setitem__("status", "co"), "built but has no map"),
    (lambda p: next(l for l in p["lands"] if l["id"] == "luu_van_coc").__setitem__("status", "chua_co"),
     "still says"),
])
def test_a_wired_lands_section_is_checked(plan, change, message):
    t = mt.tree()
    bad = copy.deepcopy(plan)
    change(bad)
    assert any(message in e for e in mt.validate_world(bad, t)), mt.validate_world(bad, t)


# ------------------------------------------------------------------ beasts and thần thông (wired 2026-11-20)
def beast_of(p: dict, bid: str) -> dict:
    return next(b for b in p["beasts"] if b["id"] == bid)


def unlock_of(p: dict, uid: str) -> dict:
    return next(u for u in p["unlocks"] if u["id"] == uid)


def test_the_beasts_and_thanthong_of_luyen_khi_are_built_and_later_ones_wait(plan):
    built = [b for b in plan["beasts"] if b["status"] == "co"]
    assert {b["id"] for b in built} == {"linh_ho", "huyen_quy", "bach_hac", "hoa_tuoc", "tieu_long"}
    assert all(b["requires"]["realm"] == "luyen_khi" and b["pos"] and b["gift"] for b in built)
    assert beast_of(plan, "ky_lan_con")["status"] == "chua_co" and "pos" not in beast_of(plan, "ky_lan_con")
    for u in plan["unlocks"]:
        assert u["status"] == ("co" if u["realm"] == "luyen_khi" else "chua_co"), u["id"]
    assert plan["beast_taming"]["seal_unlock"] == "thu_phuc_linh_thu"
    assert mt.validate_world(plan, mt.tree()) == []


@pytest.mark.parametrize("change, message", [
    (lambda p: beast_of(p, "linh_ho").__setitem__("pos", [0, 0]), "not a walkable tile"),
    (lambda p: beast_of(p, "linh_ho").pop("pos"), "needs a pos"),
    (lambda p: beast_of(p, "huyen_quy").__setitem__("gift", {"type": "bay"}), "gift.type"),
    (lambda p: beast_of(p, "bach_hac")["gift"].__setitem__("value", 1.5), "between 0 and 1"),
    (lambda p: beast_of(p, "tieu_long")["gift"].__setitem__("speed_mult", 9), "speed_mult"),
    (lambda p: beast_of(p, "linh_ho")["fight"].__setitem__("hp", 0), "fight.hp"),
    (lambda p: beast_of(p, "ky_lan_con").__setitem__("status", "co"), "is not"),
    (lambda p: beast_of(p, "ky_lan_con").__setitem__("pos", [3, 3]), "not built"),
    (lambda p: beast_of(p, "hoa_tuoc").__setitem__("pos", [51, 6]), "can be walked to"),
    (lambda p: beast_of(p, "linh_ho").__setitem__("needs", "dap_kiem_luot"), "can be walked to"),
    (lambda p: p["beast_taming"].__setitem__("talisman", "giay_trang"), "not an item"),
    (lambda p: p["beast_taming"].__setitem__("seal_unlock", "bay"), "unknown ability"),
    (lambda p: p["beast_taming"].pop("yield_seconds"), "yield_seconds"),
    (lambda p: p.pop("beast_taming"), "beast_taming must be an object"),
])
def test_a_wired_beasts_section_is_checked(plan, change, message):
    bad = copy.deepcopy(plan)
    change(bad)
    errs = mt.validate_world(bad, mt.tree())
    assert any(message in e for e in errs), errs


@pytest.mark.parametrize("change, message", [
    (lambda p: unlock_of(p, "phap_tran").__setitem__("status", "chua_co"), "status must be 'co'"),
    (lambda p: unlock_of(p, "thuan_di").__setitem__("status", "co"), "status must be 'chua_co'"),
    (lambda p: unlock_of(p, "phap_tran")["formation"].__setitem__("windup_mult", 0.5), "windup_mult"),
    (lambda p: unlock_of(p, "phap_tran").pop("formation"), "'formation' numbers"),
    (lambda p: unlock_of(p, "dap_kiem_luot")["glide"].__setitem__("over_tiles", ["lava"]), "over_tiles"),
    (lambda p: unlock_of(p, "dap_kiem_luot")["glide"].__setitem__("min_px", 200), "min_px"),
    (lambda p: unlock_of(p, "dap_kiem_luot")["glide"].__setitem__("max_px", 20), "no glide from where a player walks"),
    (lambda p: unlock_of(p, "cuoi_linh_thu")["ride"].__setitem__("gift", "sniff"), "ride.gift"),
])
def test_a_wired_abilities_section_is_checked(plan, change, message):
    bad = copy.deepcopy(plan)
    change(bad)
    errs = mt.validate_world(bad, mt.tree())
    assert any(message in e for e in errs), errs


def test_the_land_creatures_stand_for_nodes_of_their_own_branch(monkeypatch, plan):
    """A Đại Số land's creature asks only Đại Số nodes; a Lập Trình creature only the math its
    exercises reinforce; Lôi Long covers the four math branches."""
    t = mt.tree()
    assert mt.validate_world(plan, t) == []
    real = mt._read

    def patched(kind, change):
        def fake(name, folder):
            raw = real(name, folder)
            if name == "monsters.json" and folder == mt.MATH_DIR:
                raw = copy.deepcopy(raw)
                change(raw[kind])
            return raw
        monkeypatch.setattr(mt, "_read", fake)
        return mt.validate_world(plan, t)

    assert any("not of its land's branch" in e for e in patched("kiem_linh", lambda m: m["nodes"].append("gt_ham_so")))
    assert any("reinforced by no node of lt" in e
               for e in patched("co_quan_nhan", lambda m: m["nodes"].append("xs_kiem_dinh")))
    assert any("four math branches" in e
               for e in patched("loi_long", lambda m: m.__setitem__("nodes", ["ds_ngon_ngu", "gt_ham_so"])))
    assert any("not main-path nodes" in e
               for e in patched("van_xa", lambda m: m["nodes"].append("tc_phan_loai")))


def test_an_unwired_combat_section_is_only_a_design(plan):
    """Without `wired_sections` the numbers the game would read are not demanded yet."""
    t = mt.tree()
    loose = copy.deepcopy(plan)
    loose.pop("wired_sections")
    loose["combat"]["dodge"].pop("dash_px")
    assert mt.validate_world(loose, t) == []
