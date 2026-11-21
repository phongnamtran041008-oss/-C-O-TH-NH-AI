"""The curriculum review (2026-11-20, tools/audit_curriculum.py): what it measured stays fixed, the
generators it added are right (sympy recomputes them), and the NumPy-without-NumPy exercises exist."""
import random
import sys
from pathlib import Path

import pytest

from app.learning import math_items, math_path, math_problems, math_tree

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import audit_curriculum as audit          # noqa: E402
import math_verify                         # noqa: E402
import math_verify_rasoat                  # noqa: E402

REVIEW_GENERATORS = sorted(math_verify_rasoat.EXPECTED)


@pytest.fixture(scope="module")
def numbers():
    return audit.headline()


def test_the_audit_finds_no_hole_no_dead_main_skill_no_bad_prerequisite_and_no_lying_flag(numbers):
    assert numbers["cells_holes"] == 0
    assert numbers["main_skills_without_template"] == 0
    assert numbers["prerequisite_problems"] == 0
    assert numbers["nodes_flag_wrong_luyen_khi"] == 0
    assert numbers["luyen_khi_main_nodes_without_questions_or_exercises"] == 0
    assert numbers["nodes_content_dang_viet"] == 0


def test_thin_cells_only_go_down(numbers):
    """72 cells of Luyện Khí had fewer than 10 different questions before the review; 41 generators later it
    was 30. A new thin cell (a new micro-skill with two hand-written items and no generator) should be a choice,
    not an accident: raise this number on purpose."""
    assert numbers["cells_thin"] <= 31


def test_the_review_added_generators_for_all_four_subjects():
    assert len(REVIEW_GENERATORS) >= 40
    assert {g.split("_")[0] for g in REVIEW_GENERATORS} == {"dstt", "gt", "tr", "xs"}
    for gid in REVIEW_GENERATORS:
        spec = math_items.generators()[gid]
        assert not spec.reviewed, gid                          # the owner reviews new content himself
        assert spec.qtype in ("numeric", "true_false"), gid     # the only types sympy can check
        assert spec.tier in math_path.allowed_tiers(spec.floor), gid


@pytest.mark.parametrize("generator_id", REVIEW_GENERATORS)
def test_every_review_generator_is_right_varied_and_explains_itself(generator_id):
    spec = math_items.generators()[generator_id]
    seen = set()
    for seed in range(40):
        item = math_items.draw(spec, random.Random(seed))
        assert math_items.draw_problems(spec, item) == [], (generator_id, seed)
        assert math_verify.mismatch(item) is None, (generator_id, seed)
        assert len(item.solution_vi) >= 2, "the explanation must show the working"
        seen.add(item.fingerprint)
    assert len(seen) >= 8, f"{generator_id} gave only {len(seen)} different questions in 40 draws"


def test_a_review_generator_is_deterministic_for_one_seed():
    for gid in REVIEW_GENERATORS[:8]:
        spec = math_items.generators()[gid]
        a, b = math_items.draw(spec, random.Random(7)), math_items.draw(spec, random.Random(7))
        assert (a.prompt_vi, a.answer, a.numbers) == (b.prompt_vi, b.answer, b.numbers)


def test_numpy_has_five_exercises_on_plain_lists_and_the_node_says_so():
    node = math_tree.tree().nodes["lt_numpy"]
    assert node.content == "co" and len(node.problems) == 5
    for pid in node.problems:
        p = math_problems.problem(pid)
        text = " ".join(p.statement_vi)
        assert "NumPy" in text and "Python thuần" in text, pid
        assert "import numpy" not in text.lower() and not p.reviewed
    assert "không cài NumPy" in node.why_vi
