"""The sympy recomputation of Xác Suất và Thống Kê, floor 10 (Tài Năng): the generators and the hand-written items.

generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a true_false question or a list
of Fractions for a numeric one; merged into tools/math_verify.py EXPECTED. This module must not import
math_verify (it is imported by it).

The generators use closed formulas (row and column sums, E(XY) - E(X)E(Y), a^2 V(X) + b^2 V(Y) + 2ab Cov, Sxy/Sxx).
Here every answer is found another way:
- the law of Y = g(X): X as a sympy.stats FiniteRV and P(Eq(g(X), y0)) or E(g(X)) from it;
- probabilities of a joint table: a sum over the cells (atoms) that satisfy a predicate, a conditional probability
  as P(A and B)/P(B) over those atoms, independence as "the matrix of the table has rank 1";
- covariance by its definition E[(X - E X)(Y - E Y)], the variance of aX + bY by the definition of variance of the
  variable Z = aX + bY enumerated over the cells;
- the regression line from the normal equations (the gradient of the sum of squares set to 0) solved by sympy.

`HAND` does the same for the numeric answers (and a few verdicts) of the hand-written items of
data/math/items/xac_suat_thong_ke.t10.json; `hand_problems()` returns one line per answer that differs."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import Integer, Matrix, Rational
from sympy.stats import E, FiniteRV, P, variance

ROOT = Path(__file__).resolve().parents[1]
ITEM_FILE = ROOT / "server" / "data" / "math" / "items" / "xac_suat_thong_ke.t10.json"


def _frac(v) -> Fraction:
    v = sp.nsimplify(sp.simplify(sp.sympify(v)))
    if not isinstance(v, sp.Rational):
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _cells(counts, total, xs, ys):
    """Every atom of the table: (x value, y value, probability), as sympy Rationals."""
    return [(Integer(xs[i]), Integer(ys[j]), Rational(counts[i][j], total))
            for i in range(len(xs)) for j in range(len(ys))]


def _prob(cells, pred) -> sp.Rational:
    return sum((p for x, y, p in cells if pred(x, y)), Rational(0))


def _expect(cells, f) -> sp.Rational:
    return sum((f(x, y) * p for x, y, p in cells), Rational(0))


# ------------------------------------------------------------------ generators
def _ham_roi_rac(p: dict) -> list[Fraction]:
    X = FiniteRV("X", {Integer(x): Rational(w, 20) for x, w in zip(p["xs"], p["w"])})
    c = p["c"]
    g = {"binh_phuong": X ** 2, "tuyet_doi": sp.Abs(X - c), "lech_binh_phuong": (X - c) ** 2}[p["kind"]]
    if p["ask"] == "xac_suat":
        return [_frac(P(sp.Eq(g, p["y0"])))]
    return [_frac(E(g))]


def _bang_bien(p: dict) -> list[Fraction]:
    rows, cols = len(p["counts"]), len(p["counts"][0])
    cells = _cells(p["counts"], p["total"], list(range(rows)), list(range(cols)))
    i, j, kind = p["i"], p["j"], p["kind"]
    if kind == "bien_x":
        return [_frac(_prob(cells, lambda x, y: x == i))]
    if kind == "bien_y":
        return [_frac(_prob(cells, lambda x, y: y == j))]
    if kind == "dieu_kien_y":
        return [_frac(_prob(cells, lambda x, y: x == i and y == j) / _prob(cells, lambda x, y: x == i))]
    if kind == "dieu_kien_x":
        return [_frac(_prob(cells, lambda x, y: x == i and y == j) / _prob(cells, lambda x, y: y == j))]
    return [_frac(_prob(cells, lambda x, y: x + y == p["s"]))]


def _doc_lap(p: dict) -> bool:
    return Matrix(p["counts"]).rank() == 1        # a table is a product pi_i qj exactly when it has rank 1


def _hiep_phuong_sai(p: dict) -> list[Fraction]:
    cells = _cells(p["counts"], p["total"], p["xs"], p["ys"])
    mx, my = _expect(cells, lambda x, y: x), _expect(cells, lambda x, y: y)
    return [_frac(_expect(cells, lambda x, y: (x - mx) * (y - my)))]


def _phuong_sai_tong(p: dict) -> list[Fraction]:
    cells = _cells(p["counts"], p["total"], p["xs"], p["ys"])
    z = lambda x, y: p["a"] * x + p["b"] * y                                      # noqa: E731
    mean = _expect(cells, z)
    return [_frac(_expect(cells, lambda x, y: (z(x, y) - mean) ** 2))]


def _least_squares(xs, ys) -> tuple[sp.Rational, sp.Rational]:
    a, b = sp.symbols("a b")
    loss = sum(((Rational(y) - a - b * Rational(x)) ** 2 for x, y in zip(xs, ys)), Rational(0))
    sol = sp.solve([sp.diff(loss, a), sp.diff(loss, b)], [a, b], dict=True)[0]
    return sol[a], sol[b]


def _hoi_quy(p: dict) -> list[Fraction]:
    a, b = _least_squares(p["xs"], p["ys"])
    return [_frac({"he_so_goc": b, "he_so_chan": a, "du_doan": a + b * p["x0"]}[p["ask"]])]


EXPECTED: dict = {
    "xs_g10_ham_roi_rac": _ham_roi_rac,
    "xs_g10_bang_bien": _bang_bien,
    "xs_g10_doc_lap_tf": _doc_lap,
    "xs_g10_hiep_phuong_sai": _hiep_phuong_sai,
    "xs_g10_phuong_sai_tong": _phuong_sai_tong,
    "xs_g10_hoi_quy": _hoi_quy,
}


# ------------------------------------------------------------------ the hand-written items
def _law(values, probs):
    return FiniteRV("X", {Integer(v): Rational(q) for v, q in zip(values, probs)})


def _table(rows, xs, ys):
    """A table of sympy numbers given as strings 'a/b' (or whole numbers)."""
    counts = [[Rational(str(v)) for v in r] for r in rows]
    return [(Integer(xs[i]), Integer(ys[j]), counts[i][j]) for i in range(len(xs)) for j in range(len(ys))]


def _hb_01():
    X = _law([-1, 0, 1, 2, 3], ["1/10", "2/5", "1/5", "1/10", "1/5"])
    return [_frac(P(sp.Eq((X - 1) ** 2, 1)))]


def _hb_02():
    X = _law([0, 1, 2], ["1/2", "1/3", "1/6"])
    assert _frac(E(X ** 2)) == 1 and _frac(E(X) ** 2) == Fraction(4, 9)
    return [_frac(E(X ** 2))]                                    # option 0 is "1"


def _hb_08():
    X = _law([-2, -1, 0, 1, 2], ["1/10", "1/5", "3/10", "1/5", "1/5"])
    Y = X ** 2
    return [_frac(P(sp.Eq(Y, 1))), _frac(E(Y)), _frac(variance(Y)), _frac(E(Y)) == _frac(E(X) ** 2)]


def _hb_09():
    x, y = sp.symbols("x y", positive=True)
    f = 2 * x
    p_x = sp.integrate(f, (x, 0, Rational(1, 2)))
    p_y = sp.integrate(f, (x, 0, sp.sqrt(Rational(1, 4))))                       # X^2 < 1/4 <=> X < 1/2 (X > 0)
    cdf_y = sp.integrate(f, (x, 0, sp.sqrt(y)))                                  # F_Y(y) for 0 < y < 1
    assert sp.simplify(cdf_y - y) == 0                                           # uniform on (0, 1): option a
    return [_frac(p_x), _frac(p_y), _frac(sp.integrate(x ** 2 * f, (x, 0, 1)))]


def _densities():
    """hb_03 / hb_05 / hb_06 / hb_07: the distribution functions of the images of a uniform variable."""
    x, y = sp.symbols("x y", positive=True)
    # Y = 2X + 1, X uniform (0, 1): F = P(X < (y - 1)/2)
    assert sp.simplify(sp.diff((y - 1) / 2, y) - Rational(1, 2)) == 0
    # Y = X^2, X uniform (-1, 1): F = P(-sqrt y < X < sqrt y)
    f_y = sp.diff(sp.integrate(Rational(1, 2), (x, -sp.sqrt(y), sp.sqrt(y))), y)
    assert sp.simplify(f_y - 1 / (2 * sp.sqrt(y))) == 0
    assert sp.integrate(1 / (4 * sp.sqrt(y)), (y, 0, 1)) == Rational(1, 2)       # the wrong line of hb_05
    # Y = X^2, X uniform (0, 1)
    f_y = sp.diff(sp.integrate(1, (x, 0, sp.sqrt(y))), y)
    assert sp.simplify(f_y - 1 / (2 * sp.sqrt(y))) == 0 and sp.integrate(f_y, (y, 0, 1)) == 1
    # Y = -ln X is exponential(1): P(Y < y) = P(X > e^-y)
    assert sp.simplify(sp.integrate(1, (x, sp.exp(-y), 1)) - (1 - sp.exp(-y))) == 0
    return []


def _hb_10():
    phi_1 = sp.erf(1 / sp.sqrt(2)) / 2                                           # the table value Phi(1)
    assert abs(phi_1 - Rational(3413, 10000)) < Rational(1, 10000)
    return [_frac(2 * Rational(3413, 10000))]


def _vt_01():
    a = sp.Symbol("a")
    cells = [Rational(1, 10), a, Rational(1, 10), Rational(1, 5), Rational(1, 10), Rational(3, 10)]
    a_val = sp.solve(sum(cells) - 1, a)[0]
    return [_frac(a_val + Rational(1, 10))]


def _vt_02():
    cells = _table([["1/12", "1/6", "1/12"], ["1/4", "1/12", "1/3"]], [0, 1], [0, 1, 2])
    return [_frac(_prob(cells, lambda x, y: x == 0 and y == 1) / _prob(cells, lambda x, y: x == 0))]       # option 0 is 1/2


def _vt_independence():
    ok = Matrix([[Rational(1, 6), Rational(1, 12), Rational(1, 12)], [Rational(1, 3), Rational(1, 6), Rational(1, 6)]]).rank() == 1
    bad = Matrix([[Rational(1, 6), Rational(1, 4), Rational(1, 12)], [Rational(1, 6), Rational(1, 12), Rational(1, 4)]]).rank() == 1
    four = Matrix([[Rational(1, 8), Rational(1, 8)], [Rational(3, 8), Rational(3, 8)]]).rank() == 1
    return [ok, not bad, four]                                                   # vt_03 true, vt_04 not independent, vt_06 true


def _vt_07():
    a = sp.Symbol("a")
    rows = [[Rational(1, 10), Rational(1, 5), a], [Rational(1, 5), Rational(1, 10), Rational(3, 10)]]
    a_val = sp.solve(sum(sum(r) for r in rows) - 1, a)[0]
    cells = _table([[str(v) for v in r] for r in [[Rational(1, 10), Rational(1, 5), a_val],
                                                  [Rational(1, 5), Rational(1, 10), Rational(3, 10)]]], [0, 1], [0, 1, 2])
    indep = Matrix([[c[2] for c in cells[:3]], [c[2] for c in cells[3:]]]).rank() == 1
    return [_frac(a_val), _frac(_prob(cells, lambda x, y: x + y == 2)),
            _frac(_prob(cells, lambda x, y: x == 0 and y == 1) / _prob(cells, lambda x, y: x == 0)), indep]


def _vt_08():
    cells = _table([["1/4", "1/8"], ["1/8", "1/4"], ["1/8", "1/8"]], [0, 1, 2], [0, 1])
    p_y1 = _prob(cells, lambda x, y: y == 1)
    cond = lambda i: _prob(cells, lambda x, y: x == i and y == 1) / _prob(cells, lambda x, y: x == i)   # noqa: E731
    indep = Matrix([[c[2] for c in cells[2 * i:2 * i + 2]] for i in range(3)]).rank() == 1
    return [_frac(_prob(cells, lambda x, y: x == 1)),
            _frac(_prob(cells, lambda x, y: x == 0 and y == 1) / p_y1), cond(2) == p_y1, indep]


def _cov_table(rows, xs, ys):
    cells = _table(rows, xs, ys)
    mx, my = _expect(cells, lambda x, y: x), _expect(cells, lambda x, y: y)
    return (_expect(cells, lambda x, y: (x - mx) * (y - my)),
            _expect(cells, lambda x, y: (x - mx) ** 2), _expect(cells, lambda x, y: (y - my) ** 2), _expect(cells, lambda x, y: x * y))


def _tq_01():
    return [_frac(_cov_table([["1/4", "1/6", "1/12"], ["1/12", "1/6", "1/4"]], [0, 1], [0, 1, 2])[0])]


def _tq_02():
    return [_frac(Rational(-3) / (sp.sqrt(4) * sp.sqrt(9)))]


def _tq_05():
    vx, vy, c, ax, by = sp.symbols("vx vy c ax by")
    # V(aX + bY) = E[(a dX + b dY)^2] with E[dX^2] = vx, E[dY^2] = vy, E[dX dY] = c
    expr = sp.expand((2 * ax - by) ** 2).subs({ax ** 2: vx, by ** 2: vy, ax * by: c})
    val = expr.subs({vx: 3, vy: 5, c: 1})
    return [_frac(val)]


def _tq_06():
    return [_frac(_cov_table([["1/3", "1/6"], ["1/6", "1/3"]], [0, 1], [0, 1])[0])]


def _tq_08():
    cov, vx, vy, _ = _cov_table([["1/2", "1/8"], ["1/8", "1/4"]], [0, 1], [0, 1])
    return [_frac(cov / sp.sqrt(vx * vy))]


def _tq_09():
    cov, vx, vy, exy = _cov_table([["3/8", "1/8"], ["1/8", "3/8"]], [0, 1], [0, 1])
    return [_frac(exy), _frac(cov), _frac(cov / sp.sqrt(vx * vy)), False]       # |rho| < 1: Y is not a linear function of X


def _tq_10():
    cells = _table([[0, "1/3"], ["1/3", 0], [0, "1/3"]], [-1, 0, 1], [0, 1])
    cov, _, _, exy = _cov_table([[0, "1/3"], ["1/3", 0], [0, "1/3"]], [-1, 0, 1], [0, 1])
    indep = Matrix([[c[2] for c in cells[2 * i:2 * i + 2]] for i in range(3)]).rank() == 1
    return [_frac(exy), _frac(cov), indep, 0]            # (part d is a multiple choice: option 0, argued in the item)


def _tq_11():
    a, b, c, d, cov = sp.symbols("a b c d cov")
    # Cov(aX + b, cY + d) = E[(a dX)(c dY)] = a c Cov, the constants b and d cancel in the deviations
    return [_frac((a * c * cov).subs({a: 3, c: -1, cov: 5}))]


def _hq(xs, ys):
    a, b = _least_squares(xs, ys)
    return a, b


def _hq_01():
    return [_frac(_hq([1, 2, 3, 4, 5], [2, 3, 5, 4, 6])[1])]


def _hq_02():
    a, b = _hq([2, 4, 6, 8], [3, 5, 4, 8])
    return [_frac(a + 10 * b)]


def _hq_05():
    return [_frac(Rational(9, 10))]                                              # Sxy/Sxx; the other options are Sxy/Syy, r, Sxy/n


def _hq_06():
    a, b = _hq([1, 2, 3, 4, 5], [1, 3, 2, 5, 4])
    return [_frac(b), _frac(a)]


def _hq_08():
    a, b = _hq([0, 1, 2, 3, 4], [0, 2, 2, 3, 3])
    return [_frac(b), _frac(a)]


def _hq_09():
    a, b = _hq([1, 2, 3, 4], [2, 2, 4, 4])
    return [_frac(Rational(4)), _frac(b), _frac(a), _frac(a + 5 * b)]            # Sxy = 4 is checked in _hq_09_sxy


def _hq_10():
    r, sy, sx, xb, yb = Rational(1, 2), 6, 2, 10, 20
    b = r * sy / sx
    a = yb - b * xb
    return [_frac(b), _frac(a), r ** 2 == Rational(1, 4), _frac(a + b * 12)]


def _hq_checks():
    """Sxy and Sxx taken from the data themselves, as the normal equations give them."""
    for xs, ys, sxx, sxy in (([1, 2, 3, 4, 5], [2, 3, 5, 4, 6], 10, 9), ([2, 4, 6, 8], [3, 5, 4, 8], 20, 14),
                             ([1, 2, 3, 4, 5], [1, 3, 2, 5, 4], 10, 8), ([0, 1, 2, 3, 4], [0, 2, 2, 3, 3], 10, 7),
                             ([1, 2, 3, 4], [2, 2, 4, 4], 5, 4)):
        a, b = _least_squares(xs, ys)
        assert b == Rational(sxy, sxx)
        assert sum(Rational(y) - a - b * x for x, y in zip(xs, ys)) == 0           # the residuals sum to 0 (hq_11)
        xb, yb = a * 0 + Rational(sum(xs), len(xs)), Rational(sum(ys), len(ys))
        assert a + b * xb == yb                                                    # the line passes through the means (hq_03)
    return []


def _td_01():
    options = [(Rational(1, 2), Rational(1, 3), Rational(1, 6)), (Rational(1, 2),) * 3,
               (Rational(3, 4), Rational(-1, 4), Rational(1, 2)), (Rational(1, 3), Rational(1, 3), Rational(1, 4))]
    return [[all(v >= 0 for v in o) and sum(o) == 1 for o in options].index(True)]


def _td_03():
    return [_frac(Rational(1, 2) + Rational(1, 3) - Rational(3, 4))]


def _td_06():
    c = sp.Symbol("c")
    c_val = sp.solve(sum(c * k for k in (1, 2, 3, 4)) - 1, c)[0]
    return [_frac(c_val), _frac(c_val * 3), _frac(c_val * 7), True]


# item id -> function giving the expected answers: for numeric / true_false / multiple_choice the single answer,
# for a tribulation the answers of its parts in order, each as the list of Fractions (a numeric answer) or bool
HAND = {
    "xs_t10_hb_01": _hb_01, "xs_t10_hb_02": _hb_02, "xs_t10_hb_08": _hb_08, "xs_t10_hb_09": _hb_09,
    "xs_t10_hb_10": _hb_10, "xs_t10_vt_01": _vt_01, "xs_t10_vt_02": _vt_02, "xs_t10_vt_07": _vt_07,
    "xs_t10_vt_08": _vt_08, "xs_t10_tq_01": _tq_01, "xs_t10_tq_02": _tq_02, "xs_t10_tq_05": _tq_05,
    "xs_t10_tq_06": _tq_06, "xs_t10_tq_08": _tq_08, "xs_t10_tq_09": _tq_09, "xs_t10_tq_10": _tq_10,
    "xs_t10_tq_11": _tq_11, "xs_t10_hq_01": _hq_01, "xs_t10_hq_02": _hq_02, "xs_t10_hq_05": _hq_05,
    "xs_t10_hq_06": _hq_06, "xs_t10_hq_08": _hq_08, "xs_t10_hq_09": _hq_09, "xs_t10_hq_10": _hq_10,
    "xs_t10_td_01": _td_01, "xs_t10_td_03": _td_03, "xs_t10_td_06": _td_06,
}
# the worked claims that are not a single answer of an item (a derivation, a verdict): each function asserts
EXTRA_CHECKS = (_densities, _vt_independence, _hq_checks)


def _fractions(text: str) -> list[Fraction]:
    return [Fraction(v.strip()) for v in text.split(",")]


def _decide(item: dict, wants: list) -> list[str]:
    """Compare the expected values with the answers an item (or the parts of a tribulation) carries."""
    got: list = []
    if item["type"] == "tribulation":
        for part in item["parts"]:
            got.append(part["answer"] if part["type"] != "numeric" else _fractions(part["answer"]))
    else:
        got = [_fractions(item["answer"]) if item["type"] == "numeric" else item["answer"]]
    problems = []
    if item["type"] == "tribulation":
        pairs = list(zip(got, wants))
        if len(wants) != len(got):
            return [f"{item['id']}: {len(got)} parts but {len(wants)} recomputed values"]
        for k, (g, w) in enumerate(pairs, 1):
            ok = (g == w) if isinstance(w, int) else (g == [w] if not isinstance(w, list) else g == w)
            if not ok:
                problems.append(f"{item['id']} part {k}: item says {g!r}, sympy gets {w!r}")
    else:
        w = wants[0]
        g = got[0]
        ok = (g == w) if isinstance(w, int) else (g == [w] if not isinstance(w, list) else g == w)
        if not ok:
            problems.append(f"{item['id']}: item says {g!r}, sympy gets {w!r}")
    return problems


MULTIPLE_CHOICE = {"xs_t10_hb_02", "xs_t10_hb_10", "xs_t10_vt_02", "xs_t10_tq_05", "xs_t10_hq_05"}   # the right option's value
MENTIONS = {"xs_t10_hq_06", "xs_t10_hq_08", "xs_t10_tq_06", "xs_t10_tq_08"}   # find_mistake / ordering: the text must state the values


def _option_value(item: dict) -> Fraction:
    """The number an option starts with ('4/9: nhầm ...' is 4/9)."""
    return Fraction(item["options_vi"][item["answer"]].split(":")[0].strip())


def hand_problems(path: Path = ITEM_FILE) -> list[str]:
    """One line per hand-written answer of floor 10 that sympy does not reproduce (empty = all confirmed)."""
    raw = json.loads(path.read_text("utf-8"))
    items = {it["id"]: it for it in raw["items"]}
    problems: list[str] = []
    for iid, fn in HAND.items():
        if iid not in items:
            problems.append(f"{iid}: listed in HAND but not in the item file")
            continue
        item, wants = items[iid], fn()
        if iid == "xs_t10_td_01":                           # the position of the one option that is a probability
            if item["answer"] != wants[0]:
                problems.append(f"{iid}: the right option is {wants[0]}, the item says {item['answer']}")
        elif iid in MULTIPLE_CHOICE:
            if _option_value(item) != wants[0]:
                problems.append(f"{iid}: the right option is {_option_value(item)}, sympy gets {wants[0]}")
        elif iid in MENTIONS:
            text = " ".join(item.get("lines_vi", []) + item.get("steps_vi", []) + item["solution_vi"])
            for w in wants:
                if num_text(w) not in text:
                    problems.append(f"{iid}: the value {num_text(w)} from sympy is not in the text")
        elif iid == "xs_t10_hb_09":                         # the third part is a multiple choice (option 0 = uniform, proved above)
            p_x, p_y, e_y = wants
            parts = item["parts"]
            if not (_fractions(parts[0]["answer"]) == [p_x] and _fractions(parts[1]["answer"]) == [p_y]
                    and parts[2]["answer"] == 0 and _fractions(parts[3]["answer"]) == [e_y]):
                problems.append(f"{iid}: a part differs from sympy {wants}")
        else:
            problems += _decide(item, wants)
    for check in EXTRA_CHECKS:
        try:
            check()
        except AssertionError as e:
            problems.append(f"{check.__name__}: a derivation fails ({e})")
    return problems


def num_text(x) -> str:
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


if __name__ == "__main__":
    import sys
    problems = hand_problems()
    for line in problems:
        print(" -", line)
    print("hand-written answers of floor 10:", "all confirmed" if not problems else f"{len(problems)} differ")
    sys.exit(1 if problems else 0)
