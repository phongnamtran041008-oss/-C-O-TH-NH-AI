"""Luận Đạo Đài: the essay bank, what each view gives away, and the marking rule
(docs/LUAN_DAO_DAI.md). Pure data and rules: no database, no route yet."""
import copy
import json

import pytest

from app.learning import math_essays as es

ESSAY = "gt_tl_dao_ham_dinh_nghia"          # rubric 2 + 3 + 2 + 2 + 1


def all_marks(essay, value):
    return {item.id: value for item in essay.rubric}


# ------------------------------------------------------------------ the data
def test_the_bank_is_valid():
    assert es.validate_all() == []
    assert len(es.bank()) == 20
    assert {e.subject for e in es.bank().values()} == set(es.SUBJECT_PREFIX)


def test_every_rubric_adds_up_to_ten():
    for essay in es.bank().values():
        assert sum(item.points for item in essay.rubric) == es.RUBRIC_TOTAL, essay.id


def test_the_public_view_gives_nothing_away():
    essay = es.essay(ESSAY)
    public = essay.public_view()
    assert public["statement_vi"] and public["hints_vi"] and public["why_vi"]
    assert public["max_points"] == 10
    for key in ("solution_vi", "rubric", "fatal_vi"):
        assert key not in public
    text = json.dumps(public, ensure_ascii=False)
    for line in essay.solution_vi + essay.fatal_vi + tuple(i.need_vi for i in essay.rubric):
        assert line not in text


def test_the_marking_view_has_what_a_marker_needs():
    view = es.essay(ESSAY).marking_view()
    assert [item["points"] for item in view["rubric"]] == [2, 3, 2, 2, 1]
    assert view["solution_vi"] and view["fatal_vi"] and view["fatal_cap"] == 4.0


def test_unknown_essay():
    with pytest.raises(KeyError):
        es.essay("gt_tl_khong_co")


def test_open_essays_follow_the_finished_nodes():
    assert es.open_essays(set(), True) == []
    got = es.open_essays({"gt_gioi_han"}, True)
    assert {e.id for e in got} == {"gt_tl_gioi_han_epsilon_delta", "gt_tl_lien_tuc_tham_so"}
    assert es.open_essays({"gt_gioi_han"}, False) == []       # nothing is reviewed yet


# ------------------------------------------------------------------ marking
def test_score_adds_the_points_up():
    essay = es.essay(ESSAY)
    assert es.score(essay, all_marks(essay, "du")) == 10
    assert es.score(essay, all_marks(essay, "mot_phan")) == 5
    assert es.score(essay, all_marks(essay, "khong")) == 0
    assert es.score(essay, {"r1": "du", "r2": "mot_phan", "r3": "khong"}) == 2 + 1.5


def test_a_mark_that_is_missing_or_made_up_is_worth_nothing():
    essay = es.essay(ESSAY)
    assert es.score(essay, {}) == 0
    assert es.score(essay, None) == 0
    assert es.score(essay, {"r1": "xuat_sac", "r2": 3, "r99": "du"}) == 0
    assert es.clean_marks(essay, {"r1": "du", "r99": "du"}) == {
        "r1": "du", "r2": "khong", "r3": "khong", "r4": "khong", "r5": "khong"}


def test_a_fatal_mistake_caps_the_essay():
    essay = es.essay(ESSAY)
    assert es.score(essay, all_marks(essay, "du"), fatal=True) == es.FATAL_CAP
    assert es.score(essay, {"r1": "du"}, fatal=True) == 2          # the cap never raises a mark


def test_dao_tam_pays_for_the_improvement_only():
    essay = es.essay(ESSAY)                                         # level 1: worth 10
    assert es.dao_tam(essay, 10) == 10
    assert es.dao_tam(essay, 5) == 5
    assert es.dao_tam(essay, 8, best_before=5) == 3
    assert es.dao_tam(essay, 5, best_before=8) == 0
    assert es.dao_tam(essay, 10, best_before=10) == 0
    hard = es.essay("tr_tl_hoi_tu_ha_gradient")                     # level 3: worth 30
    assert es.dao_tam(hard, 10) == 30


def test_mark_puts_it_together():
    essay = es.essay(ESSAY)
    marking = es.mark(essay, "tu_cham", {"r1": "du", "r2": "du", "r3": "mot_phan"}, fatal=False)
    assert marking.points == 6 and marking.dao_tam == 6 and marking.marker == "tu_cham"
    assert marking.view()["marks"]["r4"] == "khong" and marking.view()["max_points"] == 10
    with pytest.raises(ValueError):
        es.mark(essay, "thay_giao", {})
    with pytest.raises(ValueError):                                    # the AI marker was dropped
        es.mark(essay, "ai", {})


def test_answer_problem():
    assert es.answer_problem("") == "empty"
    assert es.answer_problem("   \n ") == "empty"
    assert es.answer_problem(None) == "empty"
    assert es.answer_problem("x" * (es.MAX_ANSWER_CHARS + 1)) == "too_long"
    assert es.answer_problem("Voi h khac 0 ...") is None


# ------------------------------------------------------------------ the checks catch mistakes
@pytest.fixture
def raw():
    data = json.loads(es.essays_path("giai_tich").read_text("utf-8"))
    return copy.deepcopy(next(e for e in data["essays"] if e["id"] == ESSAY))


def problems(raw, nodes=None):
    return es.validate_essay("giai_tich", raw, nodes)


def test_validate_accepts_the_real_thing(raw):
    assert problems(raw) == []
    assert problems(raw, {"gt_dao_ham"}) == []


def test_validate_rubric_total(raw):
    raw["rubric"][0]["points"] = 3
    assert any("adds up to 11" in line for line in problems(raw))


def test_validate_rubric_shape(raw):
    raw["rubric"][1]["id"] = "r1"
    assert any("rubric ids repeat" in line for line in problems(raw))
    raw["rubric"] = raw["rubric"][:2]
    assert any("at least 3 items" in line for line in problems(raw))


def test_validate_names_and_nodes(raw):
    raw["id"] = "ds_tl_dao_ham"
    assert any("gt_tl_<name>" in line for line in problems(raw))
    raw["id"] = ESSAY
    raw["node"] = "ds_khong_gian"
    assert any("not a node of giai_tich" in line for line in problems(raw))
    raw["node"] = "gt_khong_co"
    assert problems(raw) == []                                      # without the tree: the prefix is all we know
    assert any("not in the curriculum tree" in line for line in problems(raw, {"gt_dao_ham"}))


def test_validate_text_the_game_can_draw(raw):
    raw["solution_vi"][0] = "Với h ≠ 0 thì tỉ số bằng |h|."          # the font has no U+2260
    assert any("solution_vi line 1" in line for line in problems(raw))


def test_validate_fields(raw):
    raw["kind"] = "trac_nghiem"
    raw["level"] = 4
    raw["minutes"] = 0
    raw["extra"] = 1
    del raw["why_vi"]
    got = "\n".join(problems(raw))
    for piece in ("kind must be", "level must be", "minutes must be", "unknown key extra", "missing why_vi"):
        assert piece in got


def test_validate_all_reads_a_folder(tmp_path, raw):
    folder = tmp_path / es.ESSAYS_DIR_NAME
    folder.mkdir()
    (folder / "giai_tich.json").write_text(json.dumps(
        {"subject": "giai_tich", "wired": False, "essays": [raw, raw]}, ensure_ascii=False), "utf-8")
    errors = es.validate_all(tmp_path)
    assert errors == [f"giai_tich.json: {ESSAY} is used twice"]
    assert list(es.load_bank(tmp_path)) == [ESSAY]
