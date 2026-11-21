"""Tàng Thư Các as visual cards (format 2): the new blocks, the lesson budget, the figures
the server lays out, and the safe evaluator behind every curve."""
import math
import re
from pathlib import Path

import pytest

from app.learning import math_figures as mf
from app.learning import math_library as ml

CARD = """---
id: the_thu
title_vi: Thẻ thử
subject: dai_so_tuyen_tinh
floor: 1
format: 2
summary_vi: Một dòng tóm tắt.
skills: [a_mot, a_hai]
---
## Mục một

:::hook
Vì sao: một tình huống cụ thể.
:::

:::figure numberline
caption: Một điểm trên trục số.
range: 0 4
point 2 do "a"
:::

:::core
Một câu bản chất.
:::

Ví dụ ngắn.

1. bước một
2. bước hai

> Lỗi thường gặp: quên.

:::check
Q: Hỏi gì?
A: Đáp án.
:::

## Mục hai

:::matrix
A = 1 2 ; 3 4
:::

:::core
Câu thứ hai.
:::

:::check
Q: Hỏi nữa?
A: Ừ.
:::
"""


def parse(text: str = CARD):
    return ml.parse_document(text)


def fig(kind: str, body: str) -> dict:
    return mf.parse_figure(kind, [ln for ln in body.strip().splitlines()])


def fig_error(kind: str, body: str) -> str:
    with pytest.raises(mf.FigureError) as e:
        fig(kind, body)
    return str(e.value)


# ------------------------------------------------------------------ the new blocks
def test_a_card_parses_into_its_blocks():
    doc, problems = parse()
    assert problems == []
    assert doc.format == 2 and doc.view()["format"] == 2
    kinds = [b["type"] for b in doc.blocks]
    assert kinds == ["section", "hook", "figure", "core", "text", "steps", "note", "check",
                     "section", "matrices", "core", "check"]
    assert doc.blocks[1] == {"type": "hook", "text": "Vì sao: một tình huống cụ thể."}
    assert doc.blocks[3] == {"type": "core", "text": "Một câu bản chất."}
    assert doc.blocks[7] == {"type": "check", "question": "Hỏi gì?", "answer": "Đáp án."}
    figure = doc.blocks[2]
    assert figure["kind"] == "numberline" and figure["caption"] == "Một điểm trên trục số."
    assert 0 < figure["w"] <= mf.MAX_W and 0 < figure["h"] <= mf.MAX_H and figure["prims"]
    assert doc.section_of("a_hai") == 8
    assert [len(s) for s in doc.section_blocks()] == [8, 4]


def test_an_old_document_is_still_format_1_and_free_of_the_budget():
    old = CARD.replace("format: 2\n", "").replace(":::core\nCâu thứ hai.\n:::\n", "")
    doc, problems = parse(old)
    assert problems == [] and doc.format == 1 and doc.view()["format"] == 1


@pytest.mark.parametrize("edit,problem", [
    (lambda t: t.replace("format: 2", "format: 3"), "format: 3 is not a format"),
    (lambda t: t.replace("Vì sao: một tình huống cụ thể.", "x " * 120), ":::hook is 239 characters"),
    (lambda t: t.replace("Một câu bản chất.", "y " * 100), ":::core is 199 characters"),
    (lambda t: t.replace("A: Đáp án.\n", ""), "one Q: line and one A: line"),
    (lambda t: t.replace("Q: Hỏi gì?\nA: Đáp án.\n:::", "Q: Hỏi gì?\nA: Đáp án.\n"), "never closed"),
    (lambda t: t.replace(":::hook", ":::hook to"), "takes nothing after its name"),
    (lambda t: t.replace(":::figure numberline", ":::figure"), "needs exactly one kind"),
    (lambda t: t.replace(":::figure numberline", ":::figure banh"), "unknown figure kind 'banh'"),
])
def test_a_broken_card_block_is_reported(edit, problem):
    _, problems = parse(edit(CARD))
    assert any(problem in p for p in problems), problems


# ------------------------------------------------------------------ the budget of a card
@pytest.mark.parametrize("edit,problem", [
    (lambda t: t.replace(":::core\nMột câu bản chất.\n:::\n", ""), "needs exactly one :::core (it has 0)"),
    (lambda t: t.replace(":::core\nCâu thứ hai.\n:::", ":::core\nMột.\n:::\n\n:::core\nHai.\n:::"),
     "needs exactly one :::core (it has 2)"),
    (lambda t: t.replace(":::matrix\nA = 1 2 ; 3 4\n:::\n", ""), "needs a :::figure or a :::matrix"),
    (lambda t: t.replace(":::check\nQ: Hỏi nữa?\nA: Ừ.\n:::\n", ""), "needs a :::check"),
    (lambda t: t.replace("Ví dụ ngắn.", "chữ " * 111), "111 words of text and bullets"),
    (lambda t: t.replace("Ví dụ ngắn.", "- " + "ý " * 60 + "\n- " + "ý " * 60), "120 words"),
    (lambda t: t.replace("Ví dụ ngắn.", "$$ A^{T} $$\n\n$$ A^{T} $$\n\n$$ A^{T} $$"), "3 formulas, at most 2"),
    (lambda t: t.replace("2. bước hai", "2. b\n3. b\n4. b\n5. b\n6. b"), "a list of 6 steps, at most 5"),
    (lambda t: t.replace(":::hook\nVì sao: một tình huống cụ thể.\n:::\n", ""), "first section needs a :::hook"),
])
def test_a_card_over_its_budget_is_reported(edit, problem):
    _, problems = parse(edit(CARD))
    assert any(problem in p for p in problems), problems


def test_the_budget_does_not_count_hook_core_steps_notes_or_checks():
    long = "chữ " * 100
    text = CARD.replace("bước một", long).replace("Lỗi thường gặp: quên.", long)
    _, problems = parse(text)
    assert problems == []


# ------------------------------------------------------------------ the safe evaluator
@pytest.mark.parametrize("text,x,value", [
    ("x^2", 3, 9), ("x**2 - 2*x", 3, 3), ("-x", 2, -2), ("sin(pi/2)", 0, 1), ("e^x", 1, math.e),
    ("ln(e)", 0, 1), ("log(100)", 0, 2), ("sqrt(abs(x))", -4, 2), ("tan(0) + cos(0) + exp(0)", 0, 2),
    ("(x + 1)/(x - 1)", 3, 2), ("+x", 5, 5),
])
def test_the_evaluator_computes(text, x, value):
    assert mf.Expr(text)(x) == pytest.approx(value)


@pytest.mark.parametrize("text,x", [("1/x", 0), ("sqrt(x)", -1), ("ln(x)", 0), ("x^(1/2)", -4), ("2^x", 1e6),
                                    ("exp(x)", 1e6)])
def test_outside_its_domain_an_expression_has_no_value(text, x):
    assert mf.Expr(text)(x) is None


@pytest.mark.parametrize("text,why", [
    ("y + 1", "unknown name 'y'"),
    ("__import__('os')", "only sin, cos"),
    ("x.real", "Attribute is not allowed"),
    ("(1).__class__", "Attribute is not allowed"),
    ("eval('1')", "only sin, cos"),
    ("open(x)", "only sin, cos"),
    ("sin(x, 2)", "exactly one argument"),
    ("sin(x=1)", "exactly one argument"),
    ("[x][0]", "not allowed"),
    ("lambda: 1", "not allowed"),
    ("x if x else 1", "not allowed"),
    ("x < 1", "not allowed"),
    ("'abc'", "only numbers"),
    ("True", "only numbers"),
    ("x % 2", "not allowed"),
    ("x // 2", "not allowed"),
    ("2x", "write 2*x"),
    ("", "empty"),
    ("x + " * 30 + "1", "longer than"),
])
def test_the_evaluator_refuses_anything_but_plain_maths(text, why):
    with pytest.raises(mf.FigureError) as e:
        mf.Expr(text)
    assert why in str(e.value)


def test_a_number_may_be_a_small_expression_but_never_a_name():
    assert mf.number("1/2") == 0.5 and mf.number("-pi/2") == pytest.approx(-math.pi / 2)
    for bad in ("x", "_", "do", "1/0", "abc"):
        with pytest.raises(mf.FigureError):
            mf.number(bad)


# ------------------------------------------------------------------ every kind of figure
def labels(f: dict) -> list[str]:
    return [p["s"] for p in f["prims"] if p["t"] == "text"]


def check_fits(f: dict) -> None:
    assert 0 < f["w"] <= mf.MAX_W and 0 < f["h"] <= mf.MAX_H
    assert mf.figure_problems(f) == []
    assert f["caption"]


def test_plane():
    f = fig("plane", """
caption: Một đồ thị.
x: -1 3
y: -1 5
curve "x^2" xanh "f"
area "x^2" 0 1 vang
tangent "x^2" 1 do "tiếp tuyến"
vector 0 0 1 2 luc "u"
segment 0 0 2 0 xam dash
line 0 1 1 2
point 1 1 muc "A"
drop 2 4
poly 0 0 1 0 1 1 tim
param "cos(t)" "sin(t)" 0 pi
text 2 2 "chữ" pos=n
""")
    check_fits(f)
    kinds = {p["t"] for p in f["prims"]}
    assert {"arrow", "polyline", "poly", "line", "circle", "text"} <= kinds
    assert {"f", "tiếp tuyến", "u", "A", "chữ", "O"} <= set(labels(f))
    assert any(p.get("dash") for p in f["prims"] if p["t"] == "line")


def test_a_vector_plane_keeps_one_unit_for_both_axes():
    f = fig("plane", "caption: c\nx: 0 4\ny: 0 2\nvector 0 0 4 2")
    arrow = next(p for p in f["prims"] if p["t"] == "arrow" and p["c"] == "do")
    assert abs((arrow["x2"] - arrow["x1"]) - 2 * (arrow["y1"] - arrow["y2"])) < 0.5


def test_a_curve_breaks_at_a_jump_and_stays_inside_the_plot():
    f = fig("plane", "caption: c\nx: -2 2\ny: -3 3\ncurve \"1/x\"")
    runs = [p for p in f["prims"] if p["t"] == "polyline"]
    assert len(runs) == 2                                   # one on each side of the asymptote
    xs0 = [q[0] for q in runs[0]["pts"]]
    xs1 = [q[0] for q in runs[1]["pts"]]
    assert max(xs0) < min(xs1)
    plot_top = min(q[1] for r in runs for q in r["pts"])
    plot_bottom = max(q[1] for r in runs for q in r["pts"])
    assert 0 <= plot_top and plot_bottom <= f["h"]
    tan = fig("plane", "caption: c\nx: -3 3\ny: -3 3\ncurve \"tan(x)\"")
    assert len([p for p in tan["prims"] if p["t"] == "polyline"]) == 3


def test_bars():
    f = fig("bars", """
caption: Ba đồng xu.
bar 0 1/8
bar 1 3/8
bar 2 3/8
bar 3 1/8 do
mark 1.5 do "E(X) = 1.5"
""")
    check_fits(f)
    assert len([p for p in f["prims"] if p["t"] == "rect"]) == 4
    assert {"1/8", "3/8", "E(X) = 1.5", "0", "3"} <= set(labels(f))       # values as written
    neg = fig("bars", "caption: c\nbar a 2\nbar b -1")
    check_fits(neg)


@pytest.mark.parametrize("layout", ["free", "circle", "tree", "ltr"])
def test_graph(layout):
    f = fig("graph", f"""
caption: Một đồ thị.
layout: {layout}
directed: yes
node A 0 0
node B 1 1 "Bờ"
node C 2 0 do
node D 1 -1
edge A B 3 do
edge A C "1/2"
edge C D
edge A D dash
""")
    check_fits(f)
    assert len([p for p in f["prims"] if p["t"] == "arrow"]) == 4
    assert {"A", "Bờ", "C", "D", "3", "1/2"} <= set(labels(f))


def test_sets():
    two = fig("sets", """
caption: Hai tập.
universe: "Omega"
set A "A" xanh
set B "B" do
shade A&B vang
in A-B "1"
in A&B "2"
in ~(A|B) "5"
""")
    check_fits(two)
    spans = [p for p in two["prims"] if p["t"] == "spans"]
    assert len(spans) == 1 and any(spans[0]["rows"])
    three = fig("sets", "caption: Ba tập.\nset A\nset B\nset C\nshade A&B&C\nshade (A|B)-C luc\nin A&B&C \"x\"")
    check_fits(three)
    assert len([p for p in three["prims"] if p["t"] == "spans"]) == 2


def test_a_label_in_a_region_lands_inside_that_region():
    f = fig("sets", "caption: c\nset A\nset B\nin A-B \"a\"\nin A&B \"b\"\nin B-A \"c\"")
    circles = [p for p in f["prims"] if p["t"] == "circle" and p.get("edge")]
    (ax, ay, ar), (bx, by, br) = [(c["x"], c["y"], c["r"]) for c in circles]
    where = {p["s"]: (p["x"], p["y"]) for p in f["prims"] if p["t"] == "text" and p["s"] in "abc"}
    inside = lambda p, x, y, r: math.hypot(p[0] - x, p[1] - y) < r    # noqa: E731
    assert inside(where["a"], ax, ay, ar) and not inside(where["a"], bx, by, br)
    assert inside(where["b"], ax, ay, ar) and inside(where["b"], bx, by, br)
    assert inside(where["c"], bx, by, br) and not inside(where["c"], ax, ay, ar)


def test_map():
    f = fig("map", """
caption: g sau f.
col "X" 1 2 3
col "Y" a b
col "Z" p q luc
gap 1 "f"
gap 2 "g"
1 -> a
2 -> b do
3 -> b
a -> p
b -> q
""")
    check_fits(f)
    assert len([p for p in f["prims"] if p["t"] == "arrow"]) == 5
    assert {"X", "Y", "Z", "f", "g", "1", "a", "q"} <= set(labels(f))


def test_grid():
    f = fig("grid", """
caption: Hàng nhân cột.
style: matrix
table "A"
row 1 2
row 3 4
mark row 1 do
op "x"
table "B"
head c1 c2
side r1 r2
row 5 6
row 7 8
mark col 2 xanh
mark cell 1 2 vang
mark diag
""")
    check_fits(f)
    assert {"A", "B", "x", "1", "8", "c1", "r2"} <= set(labels(f))
    table = fig("grid", "caption: Chân trị.\nhead p q\nrow Đ S\nrow S Đ\nmark row 2 luc")
    check_fits(table)
    assert any(p["t"] == "line" for p in table["prims"])


def test_numberline():
    f = fig("numberline", """
caption: Trục số.
range: -1 5
point 0 do "a" open
interval 1 3 [ ) xanh "I"
interval 4 inf ( luc
nbhd 2 0.5 tim "e"
seq "1/n" 1 6
""")
    check_fits(f)
    assert {"a", "I", "e", "-1", "5"} <= set(labels(f))


def test_flow_wraps_to_a_second_row():
    short = fig("flow", "caption: c\nbox \"x\"\nlink \"f\"\nbox \"y\" do")
    check_fits(short)
    boxes = "\n".join(f'box "buoc so {i} rat dai"' for i in range(8))
    long = fig("flow", "caption: c\n" + boxes)
    check_fits(long)
    rects = [p for p in long["prims"] if p["t"] == "rect"]
    assert len({p["y"] for p in rects}) >= 2                 # it did not fit one row
    assert any(p["t"] == "polyline" for p in long["prims"])  # the arrow down to the next row


# ------------------------------------------------------------------ every problem in one line
@pytest.mark.parametrize("kind,body,why", [
    ("plane", "x: 0 1\ny: 0 1", "needs a caption"),
    ("plane", "caption: c\nbanh 1 2", "unknown command 'banh'"),
    ("plane", "caption: c\nmau: do", "unknown setting mau:"),
    ("plane", "caption: c\npoint 1 abc", "'abc' is not a number"),
    ("plane", "caption: c\nx: 0 2\ny: 0 2\npoint 5 1", "is outside x: and y:"),
    ("plane", "caption: c\ncurve \"y^2\"", "unknown name 'y'"),
    ("plane", "caption: c\ncurve \"__import__('os')\"", "only sin, cos"),
    ("plane", "caption: c\ntext 1 1 \"chưa đóng", "never closed"),
    ("plane", "caption: c\npoint 1 1 do xanh", "two colours"),
    ("plane", "caption: c\n" + "point 0 0\n" * 21, "at most 20"),
    ("plane", "caption: c\nsize: 500 100", "outside 20..400"),
    ("plane", "caption: c\ntext 1 1 \"中\"", "the label"),
    ("plane", "caption: c中", "the caption"),
    ("bars", "caption: c", "1 to 12 bars"),
    ("bars", "caption: c\nbar a 1\nmark 5", "outside the bars"),
    ("graph", "caption: c\nnode A\nedge A B", "no node B"),
    ("graph", "caption: c\nlayout: tree\nnode A\nnode B", "joined to A"),
    ("sets", "caption: c\nset A", "2 or 3 sets"),
    ("sets", "caption: c\nset A\nset B\nshade A&C", "no set C"),
    ("map", "caption: c\ncol X 1\ncol Y a\n1 -> b", "not in two columns side by side"),
    ("grid", "caption: c\nrow 1 2\nrow 3", "same number of cells"),
    ("grid", "caption: c\nrow 1 2\nmark cell 3 1", "is outside it"),
    ("grid", "caption: c\n" + "row " + "1 " * 9, "at most 8 rows and 8 columns"),
    ("grid", "caption: c\n" + "\n".join("row " + "123456789012 " * 8 for _ in range(8)), "at most 400 x 130"),
    ("numberline", "caption: c\nrange: 0 1\npoint 2", "outside range:"),
    ("flow", "caption: c\nbox \"x\"", "2 to 9 boxes"),
    ("flow", "caption: c\nbox \"x\"\nlink \"f\"", "no box after it"),
])
def test_a_broken_figure_is_one_readable_line(kind, body, why):
    message = fig_error(kind, body)
    assert why in message and "\n" not in message


def test_validate_all_reports_a_broken_figure_with_its_file(tmp_path, monkeypatch):
    folder = tmp_path / "dai_so_tuyen_tinh"
    folder.mkdir()
    (folder / "t1.md").write_text(CARD.replace("point 2 do", "point 9 do"), "utf-8")
    errors = ml.validate_all(library_dir=tmp_path, manifest={})
    assert any(e.startswith("math/library/dai_so_tuyen_tinh/t1.md:") and "outside range:" in e for e in errors)


# ------------------------------------------------------------------ the two gold-standard lessons
@pytest.mark.parametrize("doc_id", ["dstt_lib_t3", "gt_lib_t4"])
def test_the_exemplar_lessons_are_cards(doc_id):
    doc = ml.documents()[doc_id]
    assert doc.format == 2
    for section in doc.section_blocks():
        kinds = [b["type"] for b in section]
        assert kinds[1] == "hook", section[0]["title_vi"]                  # every page opens with "why"
        assert kinds.index("core") < kinds.index("check")
        assert "steps" in kinds and "note" in kinds
        first_visual = min(kinds.index(k) for k in ("figure", "matrices") if k in kinds)
        assert first_visual < kinds.index("core")                           # see it before the essence
        if "formula" in kinds:
            assert kinds.index("formula") > kinds.index("core")             # the formula after the intuition


def test_the_exemplars_use_at_least_five_kinds_of_figure():
    kinds = {f["kind"] for d in ("dstt_lib_t3", "gt_lib_t4") for f in ml.documents()[d].figures}
    assert len(kinds) >= 5, kinds


def test_a_comment_may_follow_a_line_but_not_hide_a_label():
    f = fig("plane", 'caption: c\nx: 0 2   # the x range\n# a whole line\ntext 1 1 "so #1"')
    assert "so #1" in labels(f)


def test_every_example_of_the_writers_guide_parses():
    guide = Path(__file__).resolve().parents[2] / "docs" / "BAI_GIANG_TRUC_QUAN.md"
    blocks = re.findall(r"```\n(:::figure .*?)\n```", guide.read_text("utf-8"), re.S)
    assert {b.splitlines()[0].split()[1] for b in blocks} == set(mf.KINDS)
    for block in blocks:
        lines = block.splitlines()
        check_fits(mf.parse_figure(lines[0].split()[1], lines[1:-1]))
