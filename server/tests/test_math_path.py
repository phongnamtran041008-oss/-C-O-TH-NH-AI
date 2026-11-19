"""The learning path of the math game (plan section 3): which tiers each floor may show,
the time limits, the micro-skill graph of Đại Số Tuyến Tính, and a validator that
catches broken data before it reaches the game."""
import copy
import json
import sys
from pathlib import Path

import pytest

from app.learning import math_path as mp

ROOT = Path(__file__).resolve().parents[2]
LA = "dai_so_tuyen_tinh"

# The numbers of the plan, written out a second time on purpose: editing math.json by
# mistake must fail here, and changing a rule means changing it in both places.
PLAN_FLOOR_TIERS = {1: (1, 2), 2: (1, 2), 3: (2, 3), 4: (2, 3), 5: (3, 4), 6: (3, 4),
                    7: (4, 5), 8: (4, 5), 9: (5, 5), 10: (5, 5)}
PLAN_TIME_LIMITS = {
    "true_false":      [10, 15, 20, 30, 40],
    "multiple_choice": [20, 30, 60, 90, 120],
    "numeric":         [45, 90, 150, 240, 360],
    "matching":        [45, 75, 120, 180, 240],
    "ordering":        [45, 75, 120, 180, 240],
    "find_mistake":    [None, 90, 150, 240, 300],
    "tribulation":     [None, None, None, 8 * 60, 12 * 60],
    "programming":     [10 * 60, 15 * 60, 20 * 60, 30 * 60, 45 * 60],
}


def la() -> mp.Subject:
    return mp.subject(LA)


def raw_la() -> dict:
    return json.loads((mp.MATH_DIR / f"{LA}.json").read_text("utf-8"))


def skill(raw: dict, skill_id: str) -> dict:
    return next(s for f in raw["floors"] for s in f["skills"] if s["id"] == skill_id)


def floor(raw: dict, number: int) -> dict:
    return next(f for f in raw["floors"] if f["floor"] == number)


def config() -> dict:
    return copy.deepcopy(mp.cfg())


# ------------------------------------------------------------------ tiers and time
def test_floor_tiers_match_the_plan():
    c = mp.cfg()
    assert c["main_floors"] == 9 and c["hidden_floor"] == 10
    assert {n: mp.floor_tiers(n) for n in range(1, 11)} == PLAN_FLOOR_TIERS
    assert mp.allowed_tiers(1) == [1, 2] and mp.allowed_tiers(6) == [3, 4] and mp.allowed_tiers(9) == [5]


def test_no_tier_1_from_floor_3_and_the_last_floors_are_tier_5_only():
    for n in range(3, 11):
        assert not mp.tier_allowed(n, 1), f"floor {n} still shows tier 1"
    assert mp.allowed_tiers(9) == mp.allowed_tiers(10) == [5]


def test_floors_never_get_easier_going_up():
    ranges = [mp.floor_tiers(n) for n in range(1, 11)]
    for below, above in zip(ranges, ranges[1:]):
        assert above[0] >= below[0] and above[1] >= below[1]


def test_tier_allowed():
    assert mp.tier_allowed(3, 2) and mp.tier_allowed(3, 3)
    assert not mp.tier_allowed(3, 4) and not mp.tier_allowed(7, 3)
    assert not mp.tier_allowed(0, 1) and not mp.tier_allowed(11, 5)      # no such floor


def test_time_limits_match_the_plan():
    assert set(mp.question_types()) == set(PLAN_TIME_LIMITS)
    for qtype, limits in PLAN_TIME_LIMITS.items():
        assert [mp.time_limit(qtype, t) for t in mp.TIERS] == limits, qtype
    assert mp.time_limit("find_mistake", 1) is None          # no tier-1 "find the mistake"
    assert mp.time_limit("tribulation", 4) == 480 and mp.time_limit("tribulation", 5) == 720
    for bad in (0, 6):
        with pytest.raises(ValueError):
            mp.time_limit("numeric", bad)


def test_rule_numbers_match_the_plan():
    c = mp.cfg()
    assert c["adaptive"]["up_after_correct_streak"] == 2 and c["adaptive"]["down_after_wrong_streak"] == 2
    assert c["tier_unlock"]["correct_at_previous_tier"] == 3
    assert c["mastery_gate"]["window"] == 5 and c["mastery_gate"]["min_correct_pct"] == 80
    assert (c["spiral_review"]["share_min"], c["spiral_review"]["share_max"]) == (0.20, 0.25)
    assert c["spiral_review"]["intervals_days"] == [1, 3, 7, 14]
    assert c["anti_repeat_window"] == 50
    assert (c["placement_test"]["min_questions"], c["placement_test"]["max_questions"]) == (10, 15)
    assert (c["placement_test"]["per_floor"], c["placement_test"]["pass_pct"],
            c["placement_test"]["retake_after_days"]) == (5, 80, 7)          # M11: rule 7
    assert c["timeout"]["counts_as_wrong"] is True and c["timeout"]["resets_combo"] is True
    assert (c["skills_per_floor"]["min"], c["skills_per_floor"]["max"]) == (3, 6)
    assert [c["tiers"][str(t)]["name_vi"] for t in mp.TIERS] == \
        ["Nhập môn", "Cơ bản", "Vận dụng", "Nâng cao", "Thử thách"]


# ------------------------------------------------------------------ the shipped path
def test_shipped_data_is_valid():
    assert mp.validate_all() == []


FOUR = [LA, "giai_tich", "xac_suat_thong_ke", "toi_uu_roi_rac"]


def test_luyen_khi_has_four_subjects_and_all_four_are_written():
    index = mp.load_index()
    assert index["cultivation_realm"] == "luyen_khi"
    by_order = sorted(index["subjects"], key=lambda e: e["order"])
    assert [e["id"] for e in by_order] == FOUR
    assert [e["file"] for e in by_order] == [f"{sid}.json" for sid in FOUR]      # M11 wrote the other three
    assert [s.id for s in mp.subjects()] == FOUR
    assert [s.name_vi for s in mp.subjects()] == ["Đại Số Tuyến Tính", "Giải Tích", "Xác Suất và Thống Kê",
                                                  "Tối Ưu và Toán Rời Rạc"]
    for s in mp.subjects():
        assert [f.number for f in s.main_floors] == list(range(1, 10)) and s.hidden_floor.number == 10
    with pytest.raises(KeyError):
        mp.subject("hinh_hoc")


def test_linear_algebra_has_nine_main_floors_and_a_hidden_tenth():
    s = la()
    assert [f.number for f in s.main_floors] == list(range(1, 10))
    assert s.hidden_floor is not None and s.hidden_floor.number == 10
    assert [f.number for f in s.floors if f.hidden] == [10]
    assert s.floor(4).title_vi == "Nhân ma trận" and s.floor(9).tiers == [5]
    with pytest.raises(KeyError):
        s.floor(11)


def test_every_floor_has_three_to_six_micro_skills():
    for f in la().floors:
        assert 3 <= len(f.skills) <= 6, f"floor {f.number} has {len(f.skills)}"
        assert all(sk.floor == f.number for sk in f.skills)


def test_micro_skill_ids_are_unique():
    s = la()
    assert len(s.skills) == sum(len(f.skills) for f in s.floors)


def test_prerequisites_have_no_cycle():
    s = la()
    order = s.learning_order()
    assert sorted(order) == sorted(s.skills)
    position = {sid: i for i, sid in enumerate(order)}
    for sk in s.skills.values():
        for r in sk.requires:
            assert position[r] < position[sk.id], f"{sk.id} comes before its prerequisite {r}"


def test_prerequisites_never_come_from_a_later_floor():
    s = la()
    for sk in s.skills.values():
        for r in sk.requires:
            assert s.skills[r].floor <= sk.floor, f"{sk.id} needs {r} from a later floor"


def test_the_hidden_floor_never_blocks_a_main_floor():
    s = la()
    hidden = {sk.id for sk in s.hidden_floor.skills}
    for f in s.main_floors:
        for sk in f.skills:
            assert not hidden & set(sk.requires), f"{sk.id} depends on the hidden floor"


def test_the_path_can_be_walked_floor_by_floor():
    """Mastering floors in order always leaves something to learn next: no floor needs a
    skill the player could not have yet, and the nine main floors need nothing from floor 10."""
    s = la()
    mastered: set[str] = set()
    for f in [*s.main_floors, s.hidden_floor]:
        todo = {sk.id for sk in f.skills}
        while todo:
            ready = [sid for sid in todo if s.is_unlocked(sid, mastered)]
            assert ready, f"floor {f.number} is stuck at {sorted(todo)}"
            mastered.update(ready)
            todo.difference_update(ready)
    assert mastered == set(s.skills)


def test_a_skill_unlocks_only_when_its_prerequisites_are_mastered():
    s = la()
    start = s.unlocked([])
    assert start and all(not s.skills[sid].requires for sid in start)
    target = "dstt_t4_nhan_ma_tran"
    assert not s.is_unlocked(target, [])
    assert not s.is_unlocked(target, ["dstt_t4_tich_vo_huong"])
    assert s.is_unlocked(target, ["dstt_t4_tich_vo_huong", "dstt_t4_dieu_kien_kich_thuoc"])
    assert target in s.unlocked(["dstt_t4_tich_vo_huong", "dstt_t4_dieu_kien_kich_thuoc"])


def _ancestors(s: mp.Subject, skill_id: str) -> set[str]:
    out: set[str] = set()
    todo = list(s.skills[skill_id].requires)
    while todo:
        r = todo.pop()
        if r not in out:
            out.add(r)
            todo.extend(s.skills[r].requires)
    return out


def test_matrix_multiplication_needs_dot_product_and_reading_entries():
    """The example of plan 3.1."""
    assert {"dstt_t4_tich_vo_huong", "dstt_t3_kich_thuoc_phan_tu"} <= _ancestors(la(), "dstt_t4_nhan_ma_tran")


def test_gauss_elimination_is_taught_before_the_determinant():
    s = la()
    assert s.skills["dstt_t5_bac_thang"].floor < s.skills["dstt_t6_dinh_thuc_cap_2_3"].floor
    assert "dstt_t5_bac_thang" in _ancestors(s, "dstt_t6_nghich_dao")    # the inverse is found by elimination


def test_ai_extensions_are_marked_and_only_on_floor_nine():
    marked = {sk.id: sk.floor for sk in la().skills.values() if sk.extension == "ai"}
    assert marked == {"dstt_t9_phep_chieu": 9, "dstt_t9_pca_svd": 9}


# ------------------------------------------------------------------ graph helpers
def test_find_cycle_and_topological_order():
    assert mp.find_cycle({"a": [], "b": ["a"], "c": ["a", "b"]}) is None
    assert mp.topological_order({"c": ["a", "b"], "b": ["a"], "a": []}) == ["a", "b", "c"]
    cycle = mp.find_cycle({"a": ["b"], "b": ["c"], "c": ["a"], "d": []})
    assert cycle[0] == cycle[-1] and set(cycle) == {"a", "b", "c"} and len(cycle) == 4
    assert mp.find_cycle({"a": ["a"]}) == ["a", "a"]
    with pytest.raises(ValueError, match="cycle"):
        mp.topological_order({"a": ["b"], "b": ["a"]})


# ------------------------------------------------------------------ the validator catches broken floors
def _break_two_skill_cycle(raw):
    skill(raw, "dstt_t3_vecto_rn")["requires"] = ["dstt_t3_cong_nhan_vo_huong"]


def _break_long_cycle(raw):       # Ax = b -> ... -> hệ thuần nhất -> Ax = b, all on floor 5
    skill(raw, "dstt_t5_dang_ma_tran")["requires"] = ["dstt_t5_he_thuan_nhat"]


def _break_unknown_prerequisite(raw):
    skill(raw, "dstt_t2_chia")["requires"].append("dstt_t2_khong_co")


def _break_forward_prerequisite(raw):
    skill(raw, "dstt_t3_vet")["requires"] = ["dstt_t4_nhan_ma_tran"]


def _break_main_floor_needs_hidden_floor(raw):
    skill(raw, "dstt_t9_pca_svd")["requires"].append("dstt_t10_nhom")


def _break_requires_itself(raw):
    skill(raw, "dstt_t1_anh_xa")["requires"].append("dstt_t1_anh_xa")


def _break_duplicate_id(raw):
    skill(raw, "dstt_t7_toa_do")["id"] = "dstt_t7_co_so_so_chieu"


def _break_too_few_skills(raw):
    del floor(raw, 10)["skills"][2:]


def _break_too_many_skills(raw):
    floor(raw, 10)["skills"].extend(
        {"id": f"dstt_t10_them_{i}", "name_vi": "Thêm", "desc_vi": "Thêm.", "requires": []} for i in range(2))


def _break_missing_floor(raw):
    raw["floors"].remove(floor(raw, 5))


def _break_hidden_flag_on_a_main_floor(raw):
    floor(raw, 2)["hidden"] = True


def _break_floor_ten_not_hidden(raw):
    del floor(raw, 10)["hidden"]


def _break_empty_name(raw):
    skill(raw, "dstt_t1_tap_hop")["name_vi"] = "  "


def _break_math_symbol_not_ascii_safe(raw):
    skill(raw, "dstt_t4_khong_giao_hoan")["name_vi"] = "AB ≠ BA"


def _break_decomposed_vietnamese(raw):         # "ậ" typed as a + combining marks
    skill(raw, "dstt_t1_tap_hop")["name_vi"] = "Tập hợp"


def _break_misspelt_key(raw):
    s = skill(raw, "dstt_t6_hang")
    s["require"] = s.pop("requires")


def _break_unknown_extension(raw):
    skill(raw, "dstt_t9_pca_svd")["extension"] = "ml"


SUBJECT_BREAKS = [
    (_break_two_skill_cycle, "prerequisite cycle"),
    (_break_long_cycle, "prerequisite cycle"),
    (_break_unknown_prerequisite, "dstt_t2_khong_co, which does not exist"),
    (_break_forward_prerequisite, "from the later floor 4"),
    (_break_main_floor_needs_hidden_floor, "the hidden floor may never block a main floor"),
    (_break_requires_itself, "requires itself"),
    (_break_duplicate_id, "used twice"),
    (_break_too_few_skills, "has 2 micro-skills, need 3 to 6"),
    (_break_too_many_skills, "has 7 micro-skills, need 3 to 6"),
    (_break_missing_floor, "must be numbered 1..9 in order"),
    (_break_hidden_flag_on_a_main_floor, "\"hidden\" must be true for floor 10"),
    (_break_floor_ten_not_hidden, "\"hidden\" must be true for floor 10"),
    (_break_empty_name, "name_vi is missing or empty"),
    (_break_math_symbol_not_ascii_safe, "U+2260"),
    (_break_decomposed_vietnamese, "U+0323"),
    (_break_misspelt_key, "unknown key 'require'"),
    (_break_unknown_extension, "extension must be one of"),
]


@pytest.mark.parametrize("breaker, expected", SUBJECT_BREAKS,
                         ids=[b.__name__.removeprefix("_break_") for b, _ in SUBJECT_BREAKS])
def test_validator_catches_a_broken_subject(breaker, expected):
    raw = raw_la()
    assert mp.validate_subject(raw, mp.cfg()) == []
    breaker(raw)
    errors = mp.validate_subject(raw, mp.cfg())
    assert any(expected in e for e in errors), errors


def test_a_reported_cycle_names_the_skills_in_it():
    raw = raw_la()
    _break_long_cycle(raw)
    line = next(e for e in mp.validate_subject(raw, mp.cfg()) if "prerequisite cycle" in e)
    for sid in ("dstt_t5_dang_ma_tran", "dstt_t5_he_thuan_nhat", "dstt_t5_bac_thang"):
        assert sid in line


# ------------------------------------------------------------------ the validator catches a broken config
def _cfg_tier_out_of_range(c):
    c["floor_tiers"]["9"] = [5, 6]


def _cfg_low_above_high(c):
    c["floor_tiers"]["3"] = [3, 2]


def _cfg_floor_easier_than_the_one_below(c):
    c["floor_tiers"]["5"] = [1, 2]


def _cfg_hidden_floor_not_top_tier_only(c):
    c["floor_tiers"]["9"] = [4, 5]
    c["floor_tiers"]["10"] = [4, 5]


def _cfg_floor_missing(c):
    del c["floor_tiers"]["7"]


def _cfg_tier_missing(c):
    del c["tiers"]["5"]


def _cfg_four_time_limits(c):
    c["question_types"]["numeric"]["time_limit"] = [45, 90, 150, 240]


def _cfg_less_time_at_a_higher_tier(c):
    c["question_types"]["numeric"]["time_limit"] = [45, 90, 80, 240, 360]


def _cfg_null_above_a_time(c):
    c["question_types"]["matching"]["time_limit"] = [45, None, 120, 180, 240]


def _cfg_zero_seconds(c):
    c["question_types"]["true_false"]["time_limit"][0] = 0


def _cfg_tier_with_no_question_type(c):
    for q in c["question_types"].values():
        if isinstance(q, dict):
            q["time_limit"][0] = None


def _cfg_streak_zero(c):
    c["adaptive"]["up_after_correct_streak"] = 0


def _cfg_mastery_over_100(c):
    c["mastery_gate"]["min_correct_pct"] = 120


def _cfg_spiral_share_backwards(c):
    c["spiral_review"]["share_min"] = 0.5


def _cfg_intervals_not_growing(c):
    c["spiral_review"]["intervals_days"] = [1, 3, 3, 14]


def _cfg_skill_count_backwards(c):
    c["skills_per_floor"] = {"min": 6, "max": 3}


def _cfg_timeout_not_a_flag(c):
    c["timeout"]["counts_as_wrong"] = "yes"


def _cfg_placement_too_short(c):
    c["placement_test"]["max_questions"] = 8         # fewer than the 9 main floors (M11)
    c["placement_test"]["min_questions"] = 8


def _cfg_placement_pass_zero(c):
    c["placement_test"]["pass_pct"] = 0


def _cfg_placement_retake_negative(c):
    c["placement_test"]["retake_after_days"] = -1


CONFIG_BREAKS = [
    (_cfg_placement_too_short, "placement_test: max_questions must allow one question for every main floor"),
    (_cfg_placement_pass_zero, "placement_test.pass_pct"),
    (_cfg_placement_retake_negative, "placement_test.retake_after_days"),
    (_cfg_tier_out_of_range, "floor_tiers[9]: must be [low, high]"),
    (_cfg_low_above_high, "floor_tiers[3]: must be [low, high]"),
    (_cfg_floor_easier_than_the_one_below, "floor_tiers[5]: is easier than the floor below it"),
    (_cfg_hidden_floor_not_top_tier_only, "the hidden floor is tier 5 only"),
    (_cfg_floor_missing, "floor_tiers: must have exactly the floors"),
    (_cfg_tier_missing, "tiers: must be exactly 1, 2, 3, 4, 5"),
    (_cfg_four_time_limits, "numeric.time_limit: must list 5 values"),
    (_cfg_less_time_at_a_higher_tier, "numeric.time_limit: tier 3 has less time than the tier below"),
    (_cfg_null_above_a_time, "matching.time_limit: tier 2 is null above a tier that has a time"),
    (_cfg_zero_seconds, "true_false.time_limit: tier 1 must be whole seconds above 0"),
    (_cfg_tier_with_no_question_type, "no question type can be asked at tier 1"),
    (_cfg_streak_zero, "adaptive.up_after_correct_streak: must be a whole number >= 1"),
    (_cfg_mastery_over_100, "mastery_gate.min_correct_pct"),
    (_cfg_spiral_share_backwards, "spiral_review: need 0 <= share_min <= share_max < 1"),
    (_cfg_intervals_not_growing, "spiral_review.intervals_days"),
    (_cfg_skill_count_backwards, "skills_per_floor: min is above max"),
    (_cfg_timeout_not_a_flag, "timeout.counts_as_wrong: must be true or false"),
]


@pytest.mark.parametrize("breaker, expected", CONFIG_BREAKS,
                         ids=[b.__name__.removeprefix("_cfg_") for b, _ in CONFIG_BREAKS])
def test_validator_catches_a_broken_config(breaker, expected):
    c = config()
    assert mp.validate_config(c) == []
    breaker(c)
    errors = mp.validate_config(c)
    assert any(expected in e for e in errors), errors


def test_a_broken_config_stops_validate_all_with_the_file_name():
    c = config()
    _cfg_tier_out_of_range(c)
    errors = mp.validate_all(config=c)
    assert errors and all(e.startswith("balance/math.json: ") for e in errors)


# ------------------------------------------------------------------ the index and several subjects
def _write_math_dir(tmp_path: Path, entries: list[dict], files: dict[str, dict]) -> Path:
    (tmp_path / "subjects.json").write_text(
        json.dumps({"cultivation_realm": "luyen_khi", "subjects": entries}, ensure_ascii=False), "utf-8")
    for name, raw in files.items():
        (tmp_path / name).write_text(json.dumps(raw, ensure_ascii=False), "utf-8")
    return tmp_path


def _entry(sid: str, order: int, file: str | None) -> dict:
    return {"id": sid, "order": order, "name_vi": "Môn thử", "courses": ["MI0000"], "file": file}


def test_validate_all_on_a_copy_of_the_shipped_folder_is_clean(tmp_path):
    d = _write_math_dir(tmp_path, [_entry(LA, 1, f"{LA}.json"), _entry("giai_tich", 2, None)],
                        {f"{LA}.json": raw_la()})
    assert mp.validate_all(d) == []


def test_index_problems_are_reported(tmp_path):
    d = _write_math_dir(tmp_path, [_entry(LA, 1, "khong_co.json"), _entry(LA, 1, None)], {})
    errors = mp.validate_all(d)
    assert any("file 'khong_co.json' is not in" in e for e in errors)
    assert any("this id is used twice" in e for e in errors)
    assert any("order must be a whole number" in e for e in errors)
    assert all(e.startswith("math/subjects.json: ") for e in errors)


def test_unknown_cultivation_realm_is_reported(tmp_path):
    d = _write_math_dir(tmp_path, [_entry(LA, 1, f"{LA}.json")], {f"{LA}.json": raw_la()})
    index = json.loads((d / "subjects.json").read_text("utf-8"))
    index["cultivation_realm"] = "phi_thang"                  # not a realm of the game
    (d / "subjects.json").write_text(json.dumps(index), "utf-8")
    assert any("cultivation_realm: 'phi_thang' is not a realm" in e for e in mp.validate_all(d))


def test_file_id_must_match_the_index_and_skill_ids_are_unique_across_subjects(tmp_path):
    other = raw_la()
    other["id"] = "giai_tich"
    wrong_id = raw_la()
    wrong_id["id"] = "ten_khac"
    d = _write_math_dir(tmp_path, [_entry(LA, 1, "a.json"), _entry("giai_tich", 2, "b.json")],
                        {"a.json": wrong_id, "b.json": other})
    errors = mp.validate_all(d)
    assert any(e.startswith("math/a.json: its id is 'ten_khac'") for e in errors)
    assert any("micro-skill dstt_t1_tap_hop is already used in math/a.json" in e for e in errors)


def test_a_json_typo_is_one_line_of_the_report_not_a_crash(tmp_path):
    d = _write_math_dir(tmp_path, [_entry(LA, 1, f"{LA}.json")], {})
    (d / f"{LA}.json").write_text('{"id": "dai_so_tuyen_tinh", "floors": [],}', "utf-8")   # stray comma
    errors = mp.validate_all(d)
    assert len(errors) == 1 and errors[0].startswith(f"math/{LA}.json: cannot be read as JSON")
    (d / "subjects.json").write_text("[]", "utf-8")
    assert mp.validate_all(d) == ["math/subjects.json: must be a JSON object"]


# ------------------------------------------------------------------ tools/check_all.py
@pytest.fixture
def check_all():
    sys.path.insert(0, str(ROOT / "tools"))
    try:
        import check_all as module
        yield module
    finally:
        sys.path.remove(str(ROOT / "tools"))


def test_check_all_passes_on_the_shipped_data(check_all, capsys):
    assert check_all.main([]) == 0
    assert "FAIL" not in capsys.readouterr().out


def test_check_all_fails_the_build_when_a_check_fails(check_all, capsys, monkeypatch):
    monkeypatch.setattr(mp, "validate_all", lambda: ["math/x.json: prerequisite cycle: a -> b -> a"])
    assert check_all.main([]) == 1
    out = capsys.readouterr().out
    assert "FAIL" in out and "prerequisite cycle: a -> b -> a" in out
