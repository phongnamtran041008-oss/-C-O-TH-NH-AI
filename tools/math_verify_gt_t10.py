"""The sympy recomputation of Giải Tích, floor 10 (Tài Năng): the generators and the hand-written items.

generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a true_false question or a list of
Fractions for a numeric one; merged into tools/math_verify.py EXPECTED. This module must not import math_verify.

The generators use closed formulas (read-off bounds, the endpoint rule for a monotone function, the root of f'', a
polynomial gap). Here every answer is found another way:
- sup and inf of a monotone sequence as the larger and smaller of its first term and its sympy limit (after checking that
  it is monotone term by term), of an interval from sympy's solveset of the inequality;
- limsup and liminf as the extreme sympy limits of the subsequences n = k m + r;
- Darboux sums with sympy's maximum and minimum of f on every sub-interval (no use of monotonicity);
- the convexity point as the root of f'' that separates f'' < 0 from f'' > 0;
- a Jensen gap from the two sides of the inequality, and a check that it is not negative;
- the norm of a difference as sympy's Matrix.norm for the orders 1, 2 and infinity;
- the verdict on a candidate metric by a search over a grid of exact rationals for a violated axiom: a candidate that is
  not a metric is caught by a counterexample, one that is a metric passes the whole grid (a grid is not a proof, so the
  positive verdicts also rest on the one-line reasons in the generator).

`HAND` recomputes the numeric answers (and the verdicts and right options that a computation can decide) of the
hand-written items of data/math/items/giai_tich.t10.json; `hand_problems()` returns one line per answer that differs.
Answers are normalised to a list: a Fraction for a numeric answer, a bool for a true_false, the position of the right
option for a multiple_choice, in the order of the parts for a tribulation."""
from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import Integer, Rational, Symbol
from sympy.calculus.util import maximum, minimum

ROOT = Path(__file__).resolve().parents[1]
ITEM_FILE = ROOT / "server" / "data" / "math" / "items" / "giai_tich.t10.json"
n_, m_, x_, y_ = Symbol("n", positive=True, integer=True), Symbol("m", positive=True, integer=True), Symbol("x", real=True), Symbol("y", real=True)


def _frac(v) -> Fraction:
    v = sp.nsimplify(sp.simplify(sp.sympify(v)))
    if not isinstance(v, sp.Rational):
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


# ------------------------------------------------------------------ sup and inf
def _monotone_bounds(expr) -> tuple[sp.Basic, sp.Basic]:
    """(sup, inf) of the terms of expr(n), n >= 1, for a sequence that is monotone: the larger and the smaller of the
    first term and the limit (the monotonicity is checked on the first 60 terms, exactly)."""
    terms = [expr.subs(n_, k) for k in range(1, 61)]
    ups = all(b >= a for a, b in zip(terms, terms[1:]))
    downs = all(b <= a for a, b in zip(terms, terms[1:]))
    assert ups or downs, expr
    first, limit = terms[0], sp.limit(expr, n_, sp.oo)
    return sp.Max(first, limit), sp.Min(first, limit)


def _sup_inf(p: dict) -> list[Fraction]:
    kind, ask = p["kind"], p["ask"]
    if kind == "khoang":
        c, d = p["c"], p["d"]
        interval = sp.solveset(sp.Abs(x_ - c) < d, x_, sp.S.Reals)
        return [_frac(interval.sup if ask == "sup" else interval.inf)]
    expr = Integer(p["a"]) + Integer(p["b"]) / n_ if kind == "a_cong_b_n" else n_ / (n_ + p["m"])
    sup, inf = _monotone_bounds(expr)
    return [_frac(sup if ask == "sup" else inf)]


# ------------------------------------------------------------------ limsup and liminf
def _subsequence_limits(p: dict) -> list:
    if p["kind"] == "dau":
        a, b = Integer(p["a"]), Integer(p["b"])
        term = lambda k: a + b * (-1) ** k * (1 + sp.Integer(1) / k)           # noqa: E731
        expr = lambda mm, r: sp.expand(a + b * (-1) ** r * (1 + 1 / (2 * mm + r)))  # noqa: E731  (n = 2m + r, so (-1)^n = (-1)^r)
        return [sp.limit(expr(m_, r), m_, sp.oo) for r in (0, 1)]
    u = p["u"]
    return [sp.limit(Integer(u[r]) + 1 / (3 * m_ + r), m_, sp.oo) for r in (0, 1, 2)]      # n = 3m + r


def _gioi_han_tren(p: dict) -> list[Fraction]:
    limits = _subsequence_limits(p)
    return [_frac(max(limits) if p["ask"] == "limsup" else min(limits))]


# ------------------------------------------------------------------ Darboux sums
def _tong_darboux(p: dict) -> list[Fraction]:
    a, b, kind = p["a"], p["b"], p["kind"]
    f = {"tuyen_tinh_tang": a * x_ + b, "tuyen_tinh_giam": b - a * x_, "binh_phuong": x_ ** 2, "lap_phuong": x_ ** 3}[kind]
    pts = p["pts"]
    upper = lower = Rational(0)
    for lo, hi in zip(pts, pts[1:]):
        interval = sp.Interval(lo, hi)
        upper += maximum(f, x_, interval) * (hi - lo)
        lower += minimum(f, x_, interval) * (hi - lo)
    return [_frac({"U": upper, "L": lower, "U_tru_L": upper - lower}[p["ask"]])]


# ------------------------------------------------------------------ convex functions
def _diem_uon_so(p: dict) -> list[Fraction]:
    f = p["a"] * x_ ** 3 + p["b"] * x_ ** 2 + p["c"] * x_ + p["d"]
    f2 = sp.diff(f, x_, 2)
    (root,) = sp.solve(f2, x_)
    assert f2.subs(x_, root + 1) > 0 > f2.subs(x_, root - 1)                  # f'' < 0 on the left, > 0 on the right
    return [_frac(root)]


def _jensen_hieu(p: dict) -> list[Fraction]:
    f = lambda t: Rational(t) ** p["power"]                                    # noqa: E731
    lam, x, y = Rational(p["lam"]), Integer(p["x"]), Integer(p["y"])
    left = f(lam * x + (1 - lam) * y)
    right = lam * f(x) + (1 - lam) * f(y)
    assert right - left >= 0
    return [_frac(right - left)]


# ------------------------------------------------------------------ norms and metrics
def _chuan_vecto(p: dict) -> list[Fraction]:
    diff = sp.Matrix(p["u"]) - sp.Matrix(p["v"])
    order = {"d1": 1, "d2": 2, "dinf": sp.oo}[p["which"]]
    return [_frac(diff.norm(order))]


_CANDIDATES = {
    "|x - y|": lambda a, b: sp.Abs(a - b),
    "(x - y)^2": lambda a, b: (a - b) ** 2,
    "|x^2 - y^2|": lambda a, b: sp.Abs(a ** 2 - b ** 2),
    "|x - y|/(1 + |x - y|)": lambda a, b: sp.Abs(a - b) / (1 + sp.Abs(a - b)),
    "min(|x - y|, 1)": lambda a, b: sp.Min(sp.Abs(a - b), 1),
    "sqrt(|x - y|)": lambda a, b: sp.sqrt(sp.Abs(a - b)),
    "2|x - y|": lambda a, b: 2 * sp.Abs(a - b),
    "|x - y|^3": lambda a, b: sp.Abs(a - b) ** 3,
    "max(x - y, 0)": lambda a, b: sp.Max(a - b, 0),
    "|x^3 - y^3|": lambda a, b: sp.Abs(a ** 3 - b ** 3),
}
GRID = [Rational(k, 2) for k in range(-6, 7)]
EPS = 1e-15


def _violation(d) -> str | None:
    """The first violated axiom of d on the grid, or None. Comparisons use 30 digits, so a violation is real."""
    value = {}
    for a, b in itertools.product(GRID, repeat=2):
        value[(a, b)] = sp.N(d(a, b), 30)
    for a, b in value:
        v = value[(a, b)]
        if v < -EPS:
            return "negative"
        if (a == b) != (abs(v) < EPS):
            return "zero exactly on the diagonal"
        if abs(v - value[(b, a)]) > EPS:
            return "symmetry"
    for a, b, c in itertools.product(GRID, repeat=3):
        if value[(a, c)] > value[(a, b)] + value[(b, c)] + EPS:
            return "triangle inequality"
    return None


def _metric_tf(p: dict) -> bool:
    return _violation(_CANDIDATES[p["text"]]) is None


EXPECTED: dict = {
    "gt_g10_sup_inf": _sup_inf,
    "gt_g10_gioi_han_tren": _gioi_han_tren,
    "gt_g10_tong_darboux": _tong_darboux,
    "gt_g10_diem_uon_so": _diem_uon_so,
    "gt_g10_jensen_hieu": _jensen_hieu,
    "gt_g10_chuan_vecto": _chuan_vecto,
    "gt_g10_metric_tf": _metric_tf,
}


# ------------------------------------------------------------------ the hand-written items
def _sup_of(expr):
    return _monotone_bounds(expr)


def _h_ts_01():
    return [_frac(_sup_of(1 - 1 / n_)[0])]


def _h_ts_02():
    return [_frac(_sup_of(3 + 2 / n_)[1])]


def _h_ts_03():
    values = [(-1) ** k + Rational(1, k) for k in range(1, 400)]
    assert max(values) == Rational(3, 2) and sp.limit((-1) ** (2 * m_) + 1 / (2 * m_), m_, sp.oo) == 1
    return [_frac(max(values))]                                                        # the largest term is attained at n = 2


def _h_ts_06():
    interval = sp.Interval.open(-2, 3)
    return [0 if interval.sup == 3 and 3 not in interval else -1]


def _h_ts_10():
    seq = n_ / (n_ + 1)
    sup, inf = _monotone_bounds(seq)
    terms = [seq.subs(n_, k) for k in range(1, 200)]
    return [_frac(sup), sup in terms, _frac(inf), inf in terms]


def _h_ts_11():
    bounded = all(Rational(k, 10) ** 2 < 2 for k in range(0, 15)) and Rational(2) ** 2 >= 2     # 2 bounds A from above
    return [bounded, Integer(sp.ceiling(sp.sqrt(2))), sp.sqrt(2).is_rational, sp.sqrt(2).is_real]


def _h_gh_01():
    return [_frac(max(_subsequence_limits({"kind": "dau", "a": 0, "b": 1})))]


def _h_gh_02():
    values = {sp.cos(2 * sp.pi * r / 3) for r in (1, 2, 3)}
    return [_frac(min(values))]


def _h_gh_05():
    limits = [sp.limit((-1) ** r + 1 / (2 * m_ + r), m_, sp.oo) for r in (0, 1)]       # n = 2m + r
    return [0 if (max(limits), min(limits)) == (1, -1) else -1]


def _h_gh_09():
    limits = _subsequence_limits({"kind": "dau", "a": 0, "b": 1})
    return [_frac(limits[0]), _frac(limits[1]), _frac(max(limits)), max(limits) == min(limits)]


def _h_gh_10():
    values = [sp.sin(k * sp.pi / 2) for k in range(1, 5)]                               # period 4
    return [len(set(values)) == 1, _frac(max(values)), _frac(min(values)), min(values) <= max(values)]


def _h_gh_04():
    a_limsup = max(sp.limit((-1) ** r, m_, sp.oo) for r in (0, 1))
    s_limsup = max(sp.limit((-1) ** r + (-1) ** (r + 1), m_, sp.oo) for r in (0, 1))
    return [s_limsup == 2 * a_limsup]                                                   # the claimed equality: False


def _darboux(f, pts):
    upper = lower = Rational(0)
    for lo, hi in zip(pts, pts[1:]):
        iv = sp.Interval(lo, hi)
        upper += maximum(f, x_, iv) * (hi - lo)
        lower += minimum(f, x_, iv) * (hi - lo)
    return upper, lower


def _h_kt_01():
    return [_frac(_darboux(x_ ** 2, [0, 1, 2])[0])]


def _h_kt_02():
    upper, lower = _darboux(x_ ** 2, [Rational(k, 2) for k in range(5)])
    return [_frac(upper - lower)]


def _h_kt_09():
    f = 3 * x_ + 1
    upper, lower = _darboux(f, [0, 1, 2])
    integral = sp.integrate(f, (x_, 0, 2))
    return [_frac(upper), _frac(lower), lower <= integral <= upper, _frac(upper - lower)]


def _h_kt_10():
    # on every sub-interval of positive length there is a rational (sup D = 1) and an irrational (inf D = 0)
    pts = [0, Rational(1, 3), Rational(2, 3), 1]
    return [_frac(sum(1 * (b - a) for a, b in zip(pts, pts[1:]))), _frac(Integer(0)), False, _frac(Integer(1))]


def _h_kt_06():
    n = Symbol("n", positive=True, integer=True)
    k = Symbol("k", positive=True, integer=True)
    upper = sp.summation((k / n) * (1 / n), (k, 1, n))
    lower = sp.summation(((k - 1) / n) * (1 / n), (k, 1, n))
    assert sp.simplify(upper - (n + 1) / (2 * n)) == 0 and sp.simplify(upper - lower - 1 / n) == 0
    return [1]                                                                          # the wrong line is the second one


def _h_hl_01():
    (root,) = sp.solve(sp.diff(x_ ** 3 - 3 * x_ ** 2 + 1, x_, 2), x_)
    return [_frac(root)]


def _h_hl_03():
    f2 = sp.diff(x_ ** 4, x_, 2)
    return [not sp.solveset(f2 < 0, x_, sp.S.Reals) is sp.S.EmptySet]                   # "f is not convex" is False


def _h_hl_04():
    triples = [(1, 1, 8), (2, 2, 2), (1, 2, 3), (4, 4, 1)]
    options = [lambda a, b, c: Rational(a + b + c, 3) >= sp.root(a * b * c, 3),
               lambda a, b, c: Rational(a + b + c, 3) <= sp.root(a * b * c, 3),
               lambda a, b, c: Rational(a + b + c, 3) >= a * b * c,
               lambda a, b, c: Rational(a + b + c, 3) >= Rational(a * a + b * b + c * c, 3)]
    always = [all(bool(o(*t)) for t in triples) for o in options]
    return [always.index(True) if always.count(True) == 1 else -1]


def _h_hl_08():
    f = x_ ** 3 - 6 * x_ ** 2 + 2
    f2 = sp.diff(f, x_, 2)
    (root,) = sp.solve(f2, x_)
    return [_frac(f2.subs(x_, 3)), _frac(root), bool(f2.subs(x_, 0) >= 0), _frac(f.subs(x_, root))]


def _h_hl_09():
    f = lambda t: Rational(t) ** 2                                                      # noqa: E731
    lam, a, b = Rational(1, 4), 1, 5
    left = f(lam * a + (1 - lam) * b)
    right = lam * f(a) + (1 - lam) * f(b)
    return [_frac(left), _frac(right), bool(left <= right), _frac(right - left)]


def _h_hl_10():
    g = sp.diff(x_ * (-x_), x_, 2)                                                      # f g = -x^2: f'' = -2 < 0, concave
    return [bool(g >= 0)]


def _h_hl_02():
    pts = [Rational(k, 2) for k in range(-6, 7)]
    lams = [Rational(k, 5) for k in range(6)]
    return [all(sp.Abs(l * a + (1 - l) * b) <= l * sp.Abs(a) + (1 - l) * sp.Abs(b) for a in pts for b in pts for l in lams)]


def _h_mt_01():
    return [_frac(sp.Matrix([1 - 4, 2 + 2]).norm(1))]


def _h_mt_02():
    return [_frac((sp.Matrix([-3, 5, 0]) - sp.Matrix([2, 1, 4])).norm(sp.oo))]


def _h_mt_03():
    return [_frac(sp.Matrix([3, -4, 12]).norm(2))]


def _h_mt_04():
    return [_metric_tf({"text": "(x - y)^2"})]


def _h_mt_05():
    return [_metric_tf({"text": "|x^2 - y^2|"})]


def _h_mt_06():
    texts = ["|x - y|/(1 + |x - y|)", "(x - y)^2", None, "|x^2 - y^2|"]                # the third, d = x - y, is not even >= 0
    ok = [t is not None and _metric_tf({"text": t}) for t in texts]
    assert ok == [True, False, False, False]
    return [0]


def _h_mt_10():
    diff = sp.Matrix([1, 0, 2]) - sp.Matrix([4, 4, -10])
    ordering = True
    for vec in itertools.product(range(-3, 4), repeat=3):
        v = sp.Matrix(vec)
        ordering = ordering and v.norm(sp.oo) <= v.norm(2) <= v.norm(1)
    return [_frac(diff.norm(1)), _frac(diff.norm(2)), _frac(diff.norm(sp.oo)), ordering]


def _h_mt_11():
    pts = ["a", "b", "c"]
    d = lambda s, t: 0 if s == t else 1                                                 # noqa: E731
    triangle = all(d(s, u) <= d(s, t) + d(t, u) for s in pts for t in pts for u in pts)
    ball = [s for s in pts if d("a", s) < 1]
    ns = range(1, 12)
    cauchy = all(d(i, j) < Rational(1, 2) for i in ns for j in ns)                      # 1/m versus 1/n, e = 1/2
    return [Fraction(d("a", "b")), triangle, Fraction(len(ball)), cauchy]


HAND = {
    "gt_t10_ts_01": _h_ts_01, "gt_t10_ts_02": _h_ts_02, "gt_t10_ts_03": _h_ts_03, "gt_t10_ts_06": _h_ts_06,
    "gt_t10_ts_10": _h_ts_10, "gt_t10_ts_11": _h_ts_11,
    "gt_t10_gh_01": _h_gh_01, "gt_t10_gh_02": _h_gh_02, "gt_t10_gh_04": _h_gh_04, "gt_t10_gh_05": _h_gh_05,
    "gt_t10_gh_09": _h_gh_09, "gt_t10_gh_10": _h_gh_10,
    "gt_t10_kt_01": _h_kt_01, "gt_t10_kt_02": _h_kt_02, "gt_t10_kt_06": _h_kt_06, "gt_t10_kt_09": _h_kt_09,
    "gt_t10_kt_10": _h_kt_10,
    "gt_t10_hl_01": _h_hl_01, "gt_t10_hl_02": _h_hl_02, "gt_t10_hl_03": _h_hl_03, "gt_t10_hl_04": _h_hl_04,
    "gt_t10_hl_08": _h_hl_08, "gt_t10_hl_09": _h_hl_09, "gt_t10_hl_10": _h_hl_10,
    "gt_t10_mt_01": _h_mt_01, "gt_t10_mt_02": _h_mt_02, "gt_t10_mt_03": _h_mt_03, "gt_t10_mt_04": _h_mt_04,
    "gt_t10_mt_05": _h_mt_05, "gt_t10_mt_06": _h_mt_06, "gt_t10_mt_10": _h_mt_10, "gt_t10_mt_11": _h_mt_11,
}


def _answers(item: dict) -> list:
    """What the item carries, as a list: Fractions, bools, option or line positions."""
    if item["type"] == "tribulation":
        return [Fraction(part["answer"].strip()) if part["type"] == "numeric" else part["answer"] for part in item["parts"]]
    if item["type"] == "numeric":
        return [Fraction(v.strip()) for v in item["answer"].split(",")]
    return [item["answer"]]


def _normalise(values: list) -> list:
    out = []
    for v in values:
        if isinstance(v, (bool, int)) and not isinstance(v, sp.Basic):
            out.append(v)
        elif isinstance(v, (sp.logic.boolalg.BooleanTrue, sp.logic.boolalg.BooleanFalse)):
            out.append(bool(v))
        elif isinstance(v, Fraction):
            out.append(v)
        elif isinstance(v, sp.Basic) and v.is_Rational:
            out.append(Fraction(int(v.p), int(v.q)))
        else:
            out.append(v)
    return out


def hand_problems(path: Path = ITEM_FILE) -> list[str]:
    """One line per hand-written answer of floor 10 that sympy does not reproduce (empty = all confirmed)."""
    raw = json.loads(path.read_text("utf-8"))
    items = {it["id"]: it for it in raw["items"]}
    problems: list[str] = []
    for iid, fn in HAND.items():
        if iid not in items:
            problems.append(f"{iid}: listed in HAND but not in the item file")
            continue
        try:
            want = _normalise(fn())
        except AssertionError as e:
            problems.append(f"{iid}: a claim of the item fails ({e})")
            continue
        item = items[iid]
        got = _answers(item)
        if item["type"] == "tribulation":
            got = [Fraction(g) if isinstance(g, str) else g for g in got]
        if got != want:
            problems.append(f"{iid}: the item says {got!r}, sympy gets {want!r}")
    return problems


if __name__ == "__main__":
    import sys
    problems = hand_problems()
    for line in problems:
        print(" -", line)
    print("hand-written answers of floor 10:", "all confirmed" if not problems else f"{len(problems)} differ")
    sys.exit(1 if problems else 0)
