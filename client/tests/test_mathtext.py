"""mathtext.pretty: maths that reads like maths, with conservative rules, only glyphs the two
shipped fonts have, and text rendering that understands the superscript / subscript markers."""
import pytest

from client.engine.text import Fonts
from client.tests.test_skill_fx import make_ui
from client.ui import mathtext as M
from client.ui.mathtext import END, SUB, SUP, pretty


def show(s: str) -> str:
    return s.replace(SUP, "^{").replace(SUB, "_{").replace(END, "}")


@pytest.mark.parametrize("before, after", [
    ("x^2", "x^{2}"), ("x^(n-1)", "x^{n-1}"), ("e^(2x)", "e^{2x}"), ("A^T", "A^{T}"), ("R^n", "R^{n}"),
    ("2^10", "2^{10}"), ("a_ij", "a_{ij}"), ("x_1", "x_{1}"), ("u_n", "u_{n}"), ("C_n^k", "C_{n}^{k}"),
    ("log_2(8)", "log_{2}(8)"), ("sqrt(x^2 + 1)", "√(x^{2} + 1)"), ("a <= b", "a ≤ b"), ("a >= b", "a ≥ b"),
    ("a != b", "a ≠ b"), ("x -> 0", "x → 0"), ("pi/2", "π/2"), ("2pi", "2π"), ("2*x", "2·x"),
    ("(AB)^T = B^T A^T", "(AB)^{T} = B^{T} A^{T}"), ("x_(n+1) = x_n - 1", "x_{n+1} = x_{n} - 1"),
    ("(x_i - x_tb)^2", "(x_{i} - x_{tb})^{2}"), ("mu_0", "μ_{0}"), ("Delta_x", "Δ_{x}"), ("sqrt(n)", "√n"),
    ("căn(5)", "√5"), ("0.5 . 10^s", "0.5 · 10^{s}"), ("x +- y", "x ± y"), ("[x]_B", "[x]_{B}"),
    ("e^(-x^2/2)", "e^{-x²/2}"), ("f^(-1)", "f^{-1}"),
])
def test_the_rules(before, after):
    assert show(pretty(before)) == after


@pytest.mark.parametrize("text", [
    "so_luong", "max_len", "data_file.csv", "bai_tap_1.py", "x ^ 2", "a _ b", "^", "_", "p => q", "q <=> r",
    "R2 <- R2 - R1", "R1 <-> R3", "a * b = a + b - 5", "x^Ty", "wx_i", "Câu này không có toán.", "kết thúc. Tiếp",
    "Phân tích đa thức thành nhân tử", "if x != 0 == y: print(x ** 2)", "def f(x_1): return x_1 ** 2",
    "X ~ N(0, 1)", "lambda", "x*", "pip install", "api_key", "mũ", "Mu Cang Chải",
])
def test_what_is_left_alone(text):
    assert pretty(text) == text


def test_pretty_is_idempotent_and_plain_gives_the_text_back():
    for s in ["x^2 + y_1 <= sqrt(n)", "e^(-lambda) lambda^j / j!", "P(H_1) . P(A|H_1)"]:
        once = pretty(s)
        assert pretty(once) == once
        assert "^" not in M.plain(once) and "_" not in M.plain(once)


def test_pretty_only_emits_glyphs_one_of_the_fonts_has():
    fontTools = pytest.importorskip("fontTools.ttLib")
    from client.config import assets_dir
    have = set()
    for name in ("VT323-Regular.ttf", "NotoSansSC-Game.otf"):
        have |= set(fontTools.TTFont(str(assets_dir() / "fonts" / name)).getBestCmap())
    for ch in M.SYMBOLS:
        assert ord(ch) in have, f"U+{ord(ch):04X} {ch} is in no shipped font"
    sample = ("x^2 <= y >= z != 1 -> 2 +- 3 sqrt(4) căn(5) pi mu Delta 2*x a . b e^(-x^2) e^(x^3) a_ij")
    for ch in pretty(sample):
        if ch not in M.MARKERS:
            assert ord(ch) in have, f"pretty emitted U+{ord(ch):04X} {ch!r}, which no font has"


def test_a_marked_run_is_drawn_smaller_and_never_broken_across_lines():
    ui = make_ui()
    f: Fonts = ui.f
    plain_w = f.size("x2", 9, ui.s)[0]
    sup_w = f.size(pretty("x^2"), 9, ui.s)[0]
    assert sup_w < plain_w                                    # the 2 is smaller
    assert f.size(pretty("x^2"), 9, ui.s)[1] == f.size("Ag", 9, ui.s)[1]     # the line keeps its height
    text = pretty("đặt t = x^(n + 1) rồi tính tiếp tổng các số hạng của dãy")
    for width in range(40, 400, 7):
        for line in f.wrap(text, 8, width * ui.s, ui.s):
            assert line.count(SUP) == line.count(END)          # a run starts and ends on the same line
    assert all(c not in M.plain(text) for c in M.MARKERS)


def test_the_markers_are_never_drawn():
    ui = make_ui()
    a = ui.f.render(pretty("a_1"), 8, "#000000", ui.s)
    b = ui.f.render("a", 8, "#000000", ui.s)
    c = ui.f.render("1", 8 * 0.8, "#000000", ui.s)
    assert a.get_width() <= b.get_width() + c.get_width() + 1
