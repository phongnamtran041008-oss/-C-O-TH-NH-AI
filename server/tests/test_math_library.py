"""M4: Tàng Thư Các of the math game - the document format, the plain-text form of a
formula, the validator, and the two endpoints that serve a document."""
import json

import pytest

from app.learning import math_items as mi
from app.learning import math_library as ml
from app.learning import math_path as mp
from app.systems import math_practice
from tests.helpers import answer_key, register
from tests.test_math_loop import ask, make, play, right_answer, start

SUBJECT = "dai_so_tuyen_tinh"
WRITTEN_FLOORS = tuple(range(1, 10))        # of every subject: all but the hidden floor 10
SUBJECTS = [SUBJECT, "giai_tich", "xac_suat_thong_ke", "toi_uu_roi_rac"]

DOC = """---
id: thu_nghiem
title_vi: Trang thử
subject: dai_so_tuyen_tinh
floor: 1
summary_vi: Một dòng tóm tắt.
skills: [a_mot, a_hai]
---
## Mục một
Đoạn văn thứ nhất,
viết trên hai dòng.

- gạch đầu dòng một
- gạch đầu dòng hai

1. bước một
2. bước hai

$$ A^{T} $$

:::matrix
A = 1 2 ; 3 -4
B = 0 1 ; 1 0
:::

> Lỗi thường gặp: quên mất.

### Tiểu mục
Đoạn cuối.

## Mục hai
Hết.
"""


def parse(text: str = DOC):
    return ml.parse_document(text)


def kinds(doc) -> list[str]:
    return [b["type"] for b in doc.blocks]


# ------------------------------------------------------------------ a formula in plain text
@pytest.mark.parametrize("tex,plain", [
    (r"A^{T}", "A^T"),
    (r"i^{2} = -1", "i^2 = -1"),
    (r"A \cap B", "A giao B"),
    (r"A \cup B", "A hop B"),
    (r"A \setminus B", "A \\ B"),
    (r"x \in A", "x thuoc A"),
    (r"x \notin A", "x khong thuoc A"),
    (r"\varnothing \subset A", "{} con cua A"),
    (r"A \times B", "A x B"),
    (r"\frac{1}{2}", "1/2"),
    (r"\frac{a + bi}{c + di}", "(a + bi)/(c + di)"),
    (r"\sqrt{a^{2} + b^{2}}", "can(a^2 + b^2)"),
    (r"\begin{pmatrix} 1 & 2 \\ 3 & -4 \end{pmatrix}", "[1, 2; 3, -4]"),
    (r"f : \mathbb{R} \to \mathbb{R}", "f : R -> R"),
    (r"(g \circ f)(x) = g(f(x))", "(g o f)(x) = g(f(x))"),
    (r"\text{tr}(A)", "tr(A)"),
    (r"\overline{z} = a - bi", "z = a - bi"),
    (r"z^{n} = r^{n}(\cos n\varphi + i \sin n\varphi)", "z^n = r^n(cos nphi + i sin nphi)"),
    (r"1 \le i \le m", "1 <= i <= m"),
    (r"a \ne b \Rightarrow c", "a != b => c"),
])
def test_tex_in_plain_text(tex, plain):
    assert ml.tex_to_ascii(tex) == plain


@pytest.mark.parametrize("tex", [r"\oint f", r"\frac{a}{b", r"x \heartsuit y", r"\begin{array}{c} 1 \end{array}"])
def test_a_formula_with_no_plain_text_form_is_refused(tex):
    with pytest.raises(ml.TexError):
        ml.tex_to_ascii(tex)


def test_the_plain_text_form_is_always_showable():
    for doc in ml.documents().values():
        for block in doc.formulas:
            assert mp.text_problem(block["alt"]) is None, block


def test_the_same_formula_always_has_the_same_picture_name():
    assert ml.formula_key(r"A^{T}") == ml.formula_key("A^{T} ") == ml.formula_key("A^{T}")
    assert ml.formula_key(r"A^{T}") != ml.formula_key(r"A^{2}")
    assert len(ml.formula_key("x")) == ml.KEY_LEN


# ------------------------------------------------------------------ parsing
def test_a_document_parses_into_the_blocks_the_game_draws():
    doc, problems = parse()
    assert problems == []
    assert (doc.id, doc.floor, doc.subject) == ("thu_nghiem", 1, SUBJECT)
    assert doc.skills == ("a_mot", "a_hai") and doc.summary_vi == "Một dòng tóm tắt."
    assert kinds(doc) == ["section", "text", "bullets", "steps", "formula", "matrices", "note",
                          "heading", "text", "section", "text"]
    assert doc.blocks[0] == {"type": "section", "title_vi": "Mục một", "skill": "a_mot"}
    assert doc.blocks[1]["text"] == "Đoạn văn thứ nhất, viết trên hai dòng."
    assert doc.blocks[2]["items"] == ["gạch đầu dòng một", "gạch đầu dòng hai"]
    assert doc.blocks[3]["items"] == ["bước một", "bước hai"]
    assert doc.blocks[4] == {"type": "formula", "key": ml.formula_key("A^{T}"), "tex": "A^{T}", "alt": "A^T"}
    assert doc.blocks[5]["matrices"] == [{"name": "A", "rows": [["1", "2"], ["3", "-4"]]},
                                         {"name": "B", "rows": [["0", "1"], ["1", "0"]]}]
    assert doc.blocks[6]["text"] == "Lỗi thường gặp: quên mất."
    assert doc.blocks[7] == {"type": "heading", "title_vi": "Tiểu mục"}
    assert doc.section_of("a_hai") == 9 and doc.section_of("a_mot") == 0 and doc.section_of("khong") == 0


def test_a_formula_may_run_over_several_lines():
    doc, problems = parse(DOC.replace("$$ A^{T} $$", "$$\n(A + B)^{T} =\nA^{T} + B^{T}\n$$"))
    assert problems == []
    formula = doc.formulas[0]
    assert formula["tex"] == "(A + B)^{T} = A^{T} + B^{T}" and formula["alt"] == "(A + B)^T = A^T + B^T"


@pytest.mark.parametrize("text,problem", [
    ("khong co front matter", "must start with a --- front matter"),
    ("---\nid: x\n", "never closed by ---"),
    ("---\nid x\n---\n## A\n", "front matter needs 'key: value'"),
])
def test_a_broken_file_is_reported_in_one_line(text, problem):
    doc, problems = parse(text)
    assert any(problem in p for p in problems), problems


@pytest.mark.parametrize("edit,problem", [
    (lambda t: t.replace("skills: [a_mot, a_hai]", "skills: [a_mot]"), "section 2"),
    (lambda t: t.replace("## Mục hai\nHết.\n", ""), "only 1 sections for 2"),
    (lambda t: t.replace("$$ A^{T} $$", "$$ A^{T}"), "never closed"),
    (lambda t: t.replace(":::\n\n> Lỗi", "\n> Lỗi"), "never closed by :::"),
    (lambda t: t.replace("A = 1 2 ; 3 -4", "A = 1 2 ; 3"), "same number of entries"),
    (lambda t: t.replace("A = 1 2 ; 3 -4", "1 2 ; 3 4"), "write it as"),
    (lambda t: t.replace("A = 1 2 ; 3 -4", "A = x+1 2 ; 3 4"), "must be a number"),
    (lambda t: t.replace("$$ A^{T} $$", r"$$ \oint x $$"), "no plain-text form"),
    (lambda t: t.replace(":::matrix", ":::bang"), "unknown block"),
])
def test_the_parser_reports_a_broken_block(edit, problem):
    _, problems = parse(edit(DOC))
    assert any(problem in p for p in problems), problems


def test_an_empty_matrix_block_is_reported():
    _, problems = parse(DOC.replace("A = 1 2 ; 3 -4\nB = 0 1 ; 1 0", ""))
    assert any("no matrix in it" in p for p in problems), problems


# ------------------------------------------------------------------ the shipped documents
def test_the_shipped_library_is_valid():
    assert ml.validate_all() == []
    assert ml.manifest_problems() == []


def test_one_document_per_written_floor_covering_every_micro_skill():
    assert [s.id for s in mp.subjects()] == SUBJECTS                   # four subjects, each written to floor 9
    assert len(ml.documents()) == len(SUBJECTS) * len(WRITTEN_FLOORS)
    for sid in SUBJECTS:
        subject = mp.subject(sid)
        assert sorted(d.floor for d in ml.documents().values() if d.subject == sid) == list(WRITTEN_FLOORS)
        for floor in WRITTEN_FLOORS:
            (doc,) = ml.for_floor(sid, floor)
            assert list(doc.skills) == [s.id for s in subject.floor(floor).skills]
            sections = [b for b in doc.blocks if b["type"] == "section"]
            assert [b["skill"] for b in sections] == list(doc.skills)
            assert any(b["type"] == "note" for b in doc.blocks), doc.id
            for skill in doc.skills:
                assert ml.for_skill(skill) is doc
    assert all(d.formulas for d in ml.documents().values() if d.subject == SUBJECT)


def test_every_formula_has_a_picture_that_fits_the_page():
    manifest = ml.load_manifest()
    for doc in ml.documents().values():
        for block in doc.view()["blocks"]:
            if block["type"] != "formula":
                continue
            assert manifest[block["key"]]["tex"] == block["tex"]
            assert 0 < block["w"] <= ml.MAX_FORMULA_WIDTH and 0 < block["h"] <= ml.MAX_FORMULA_HEIGHT


def test_no_floor_that_has_questions_is_left_without_a_document(monkeypatch):
    assert ml._coverage_problems({s: "x" for d in ml.documents().values() for s in d.skills}) == []
    none_at_all = ml._coverage_problems({})
    assert len(none_at_all) == len(WRITTEN_FLOORS) * len(SUBJECTS)
    assert "floor 1 has questions but no document" in none_at_all[0]
    half = {s: "x" for d in ml.documents().values() for s in d.skills if d.floor != 1}
    half["dstt_t1_tap_hop"] = "x"
    problems = ml._coverage_problems(half)
    assert any("explains only part of its micro-skills" in p for p in problems), problems


def test_the_validator_catches_a_document_that_does_not_match_its_floor():
    doc, problems = parse()
    errors = ml.validate_document(doc, problems, SUBJECT, ml.load_manifest())
    assert any("`skills` must be every micro-skill of floor 1" in e for e in errors), errors
    assert any("no picture was built" in e for e in errors), errors


def test_the_validator_catches_a_picture_that_is_too_big():
    doc, _ = parse()
    key = doc.formulas[0]["key"]
    wide = {key: {"tex": "A^{T}", "alt": "A^T", "w": ml.MAX_FORMULA_WIDTH + 1, "h": 10}}
    errors = ml.validate_document(doc, [], SUBJECT, wide)
    assert any("wide, at most" in e for e in errors), errors
    other = {key: {"tex": "B^{T}", "alt": "B^T", "w": 10, "h": 10}}
    assert any("built from another formula" in e for e in ml.validate_document(doc, [], SUBJECT, other))


def test_manifest_problems_report_a_missing_or_stray_picture(tmp_path):
    keys = {b["key"] for d in ml.documents().values() for b in d.formulas}
    problems = ml.manifest_problems(assets_dir=tmp_path)
    assert len(problems) == len(keys) and all("is missing" in p for p in problems)
    (tmp_path / "deadbeefdeadbeef.png").write_bytes(b"x" * 200)
    assert any("belongs to no document any more" in p for p in ml.manifest_problems(assets_dir=tmp_path))
    assert any("is not used by any document" in p
               for p in ml.manifest_problems(manifest={**ml.load_manifest(), "cafe": {"tex": "x"}}))


# ------------------------------------------------------------------ the endpoints
async def test_the_library_lists_every_document(client):
    h, _ = await make(client)
    r = await client.get("/math/library", headers=h)
    assert r.status_code == 200
    listed = r.json()["subjects"]
    assert [s["id"] for s in listed] == SUBJECTS                       # in play order (M11: four subjects)
    for s in listed:
        assert [d["floor"] for d in s["documents"]] == list(WRITTEN_FLOORS), s["id"]
        assert all(d["title_vi"] and d["summary_vi"] and d["sections"] for d in s["documents"])
    subject = listed[0]
    first = subject["documents"][0]
    assert first["title_vi"] and first["summary_vi"] and len(first["sections"]) == 6
    assert (await client.get("/math/library")).status_code == 401


async def test_a_document_arrives_ready_to_draw(client):
    h, _ = await make(client)
    r = await client.get("/math/library/dstt_lib_t3", headers=h)
    assert r.status_code == 200
    doc = r.json()
    assert doc["floor"] == 3 and doc["title_vi"]
    formulas = [b for b in doc["blocks"] if b["type"] == "formula"]
    matrices = [b for b in doc["blocks"] if b["type"] == "matrices"]
    assert formulas and matrices
    assert all(b["w"] > 0 and b["h"] > 0 and b["alt"] for b in formulas)
    assert all(isinstance(v, str) for b in matrices for m in b["matrices"] for row in m["rows"] for v in row)
    assert (await client.get("/math/library/khong_co", headers=h)).json()["error"]["code"] == "no_doc"


async def test_the_floor_list_points_at_its_document(client):
    h, _ = await make(client)
    floors = (await client.get("/math/path", headers=h)).json()["subjects"][0]["floors"]
    assert [f["doc_id"] for f in floors] == [f"dstt_lib_t{n}" for n in range(1, 10)] + [None]   # hidden 10: none


async def test_a_question_carries_the_way_into_the_library(client):
    h, _ = await make(client)
    run_id = await start(client, h)
    q = await ask(client, h, run_id)
    doc = q["math"]["doc"]
    assert doc["id"] == "dstt_lib_t1" and doc["title_vi"]
    blocks = ml.documents()["dstt_lib_t1"].blocks
    assert blocks[doc["block"]]["skill"] == q["math"]["skill"]


def test_a_micro_skill_with_no_document_has_no_link():
    assert math_practice.doc_link("dstt_t9_khong_co") is None
    assert math_practice.doc_link("dstt_t1_tap_hop")["id"] == "dstt_lib_t1"
