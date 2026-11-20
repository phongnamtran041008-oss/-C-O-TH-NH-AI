"""The sympy recomputation of Tối Ưu và Toán Rời Rạc, floor 10 (phương pháp tính): the generators and the hand-written items.

generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a true_false question or a list of
Fractions for a numeric one; merged into tools/math_verify.py EXPECTED. This module must not import math_verify.

The generators use closed forms (a sum of terms, an inequality solved by a loop, a derivative written by hand). Here every
answer is found another way:
- the error of a sum, difference, product or quotient from the differential sum |df/dv| Delta_v of the function as a sympy
  expression; the error of f(x) from sympy's derivative;
- a trustworthy digit by comparing sympy Rationals digit by digit;
- the number of bisections from the sympy logarithm: the smallest n with L/2^(n + 1) <= e is ceiling(log2(L/e)) - 1;
- a bisection and an iteration run again over sympy Rationals (a bisection by the sign of sympy's f, not by a product);
- the contraction constant as sympy's maximum of g' on the interval, the verdict on a fixed point from |g'(x*)| after
  checking that x* is a fixed point;
- Newton's step as x - f/f' with the derivative taken by sympy.

`HAND` recomputes the numeric answers (and the verdicts and right options that a computation can decide) of the
hand-written items of data/math/items/toi_uu_roi_rac.t10.json; `hand_problems()` returns one line per answer that differs.
Answers are normalised to a list: a Fraction for a numeric answer, a bool for a true_false, the position of the right option
for a multiple_choice, in the order of the parts for a tribulation."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import Integer, Rational, Symbol
from sympy.calculus.util import maximum

ROOT = Path(__file__).resolve().parents[1]
ITEM_FILE = ROOT / "server" / "data" / "math" / "items" / "toi_uu_roi_rac.t10.json"
x_, y_ = Symbol("x", real=True), Symbol("y", real=True)


def _frac(v) -> Fraction:
    v = sp.simplify(sp.sympify(v))                       # (exact: no nsimplify, which can rewrite a big Rational)
    if not isinstance(v, sp.Rational):
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _r(text) -> Rational:
    return Rational(str(text))


# ------------------------------------------------------------------ errors
def _sai_so_phep_tinh(p: dict) -> list[Fraction]:
    x, y, dx, dy = _r(p["x"]), _r(p["y"]), _r(p["dx"]), _r(p["dy"])
    f = {"tong": x_ + y_, "hieu": x_ - y_, "tich": x_ * y_, "thuong": x_ / y_}[p["op"]]
    differential = sum(abs(sp.diff(f, v).subs({x_: x, y_: y})) * dv for v, dv in ((x_, dx), (y_, dy)))
    return [_frac(differential)]


def _sai_so_ham(p: dict) -> list[Fraction]:
    f = {"binh_phuong": x_ ** 2, "lap_phuong": x_ ** 3, "can": sp.sqrt(x_), "nghich_dao": 1 / x_}[p["kind"]]
    return [_frac(abs(sp.diff(f, x_).subs(x_, p["x0"])) * _r(p["dx"]))]


def _trustworthy(a: Rational, delta: Rational, decimals: int, top: int) -> int:
    """How many digits of a (weights top, top - 1, ..., -decimals) have delta <= 0.5 . 10^s, counted from the left."""
    count = 0
    for s in range(top, -decimals - 1, -1):
        if delta <= Rational(1, 2) * Integer(10) ** s:
            count += 1
        else:
            break
    return count


def _chu_so_dang_tin(p: dict) -> list[Fraction]:
    whole, _, fraction = p["a"].partition(".")
    return [Fraction(_trustworthy(_r(p["a"]), _r(p["delta"]), len(fraction), len(whole) - 1))]


# ------------------------------------------------------------------ bisection
def _chia_doi_so_buoc(p: dict) -> list[Fraction]:
    length, eps = Integer(p["length"]), _r(p["eps"])
    n = sp.ceiling(sp.log(length / eps, 2)) - 1
    assert length / 2 ** (n + 1) <= eps and (n == 0 or length / 2 ** n > eps)
    return [_frac(max(n, 0))]


def _chia_doi_dau_doan(p: dict) -> list[Fraction]:
    f = x_ ** 2 - p["c"]
    a, b = Integer(p["m"]), Integer(p["m"] + 1)
    for _ in range(p["steps"]):
        mid = (a + b) / 2
        s_mid, s_a = sp.sign(f.subs(x_, mid)), sp.sign(f.subs(x_, a))
        assert s_mid != 0
        if s_mid == s_a:
            a = mid                       # no sign change on [a, mid]: the root is on the right
        else:
            b = mid
    return [_frac(a if p["side"] == "trái" else b)]


# ------------------------------------------------------------------ fixed-point iteration
def _lap_don_buoc(p: dict) -> list[Fraction]:
    g = lambda t: Integer(p["a"]) + Integer(p["b"]) / t         # noqa: E731
    value = _r(p["x0"])
    for _ in range(p["k"]):
        value = sp.simplify(g(value))
    return [_frac(value)]


def _lap_don_he_so_co(p: dict) -> list[Fraction]:
    c, m, t = p["c"], p["m"], p["t"]
    g = (x_ ** 2 + c) / m if p["kind"] == "binh_phuong" else x_ ** 3 / m + c
    gp = sp.diff(g, x_)
    q = maximum(gp ** 2, x_, sp.Interval(0, t))                 # |g'| through its square (g' >= 0 here)
    return [_frac(sp.sqrt(q))]


def _lap_don_hoi_tu_tf(p: dict) -> bool:
    m, c, r = p["r1"] + p["r2"], p["r1"] * p["r2"], p["r"]
    g = (x_ ** 2 + c) / m
    assert g.subs(x_, r) == r                                   # r really is a fixed point of g
    return bool(abs(sp.diff(g, x_).subs(x_, r)) < 1)


# ------------------------------------------------------------------ Newton
def _newton_step(f, x0):
    return x0 - f.subs(x_, x0) / sp.diff(f, x_).subs(x_, x0)


def _newton_buoc(p: dict) -> list[Fraction]:
    f = x_ ** 2 - p["a"]
    value = _r(p["x0"])
    for _ in range(p["k"]):
        value = sp.simplify(_newton_step(f, value))
    return [_frac(value)]


def _newton_da_thuc(p: dict) -> list[Fraction]:
    f = x_ ** 3 + p["b"] * x_ ** 2 + p["c"] * x_ + p["d"]
    return [_frac(_newton_step(f, Integer(p["x0"])))]


EXPECTED: dict = {
    "tr_g10_sai_so_phep_tinh": _sai_so_phep_tinh,
    "tr_g10_sai_so_ham": _sai_so_ham,
    "tr_g10_chu_so_dang_tin": _chu_so_dang_tin,
    "tr_g10_chia_doi_so_buoc": _chia_doi_so_buoc,
    "tr_g10_chia_doi_dau_doan": _chia_doi_dau_doan,
    "tr_g10_lap_don_buoc": _lap_don_buoc,
    "tr_g10_lap_don_he_so_co": _lap_don_he_so_co,
    "tr_g10_lap_don_hoi_tu_tf": _lap_don_hoi_tu_tf,
    "tr_g10_newton_buoc": _newton_buoc,
    "tr_g10_newton_da_thuc": _newton_da_thuc,
}


# ------------------------------------------------------------------ the hand-written items
def _h_ss_01():
    return [_frac(_r("0.05") / _r("12.5"))]


def _h_ss_02():
    return [_frac(sum(abs(sp.diff(x_ * y_, v).subs({x_: 10, y_: 5})) * dv for v, dv in ((x_, _r("0.1")), (y_, _r("0.05")))))]


def _h_ss_03():
    x, y = _r("100.2"), _r("99.8")
    delta = _r("0.1") + _r("0.1")
    # the worst case over the two intervals really is delta, reached at the corners
    worst = max(abs((x + sx * _r("0.1")) - (y + sy * _r("0.1")) - (x - y)) for sx in (-1, 1) for sy in (-1, 1))
    assert worst == delta
    return [_frac(delta / (x - y))]


def _h_ss_04():
    return [_frac(abs(sp.diff(x_ ** 2, x_).subs(x_, 5)) * _r("0.01"))]


def _h_ss_05():
    x, y, dx, dy = Integer(10), Integer(4), _r("0.1"), _r("0.3")
    worst = max(abs((x + sx * dx) - (y + sy * dy) - (x - y)) for sx in (-1, 1) for sy in (-1, 1))
    return [worst == dx - dy]                                          # "the error of x - y is Delta_x - Delta_y": False


def _h_ss_06():
    x, y, dx, dy = Integer(10), Integer(5), _r("0.1"), _r("0.05")
    worst = max(abs((x + sx * dx) * (y + sy * dy) - x * y) / (x * y) for sx in (-1, 1) for sy in (-1, 1))
    return [bool(abs(worst - (dx / x + dy / y)) <= (dx / x) * (dy / y))]    # equal up to the product of the two (second order)


def _h_ss_07():
    return [0 if _trustworthy(_r("3.2467"), _r("0.004"), 4, 0) == 3 else -1]


def _h_ss_11():
    f = x_ * y_
    dx, dy = _r("0.05"), _r("0.02")
    x0, y0 = _r("12.5"), Integer(4)
    delta_a = sum(abs(sp.diff(f, v).subs({x_: x0, y_: y0})) * dv for v, dv in ((x_, dx), (y_, dy)))
    return [_frac(dx / x0), _frac(dy / y0), _frac(delta_a), bool(delta_a <= Rational(1, 2))]


def _h_ss_12():
    f = sp.sqrt(x_)
    d = abs(sp.diff(f, x_).subs(x_, 100))
    delta_f = d * _r("0.4")
    return [_frac(f.subs(x_, 100)), _frac(sp.diff(f, x_).subs(x_, 100)), _frac(delta_f),
            bool(delta_f / f.subs(x_, 100) == (_r("0.4") / 100) / 2)]


def _smallest_n(length, eps):
    return max(sp.ceiling(sp.log(Rational(length) / Rational(eps), 2)) - 1, 0)


def _bisect(f, a, b, steps):
    a, b = Rational(a), Rational(b)
    path = []
    for _ in range(steps):
        mid = (a + b) / 2
        fm = f.subs(x_, mid)
        path.append(fm)
        if sp.sign(fm) == sp.sign(f.subs(x_, a)):
            a = mid
        else:
            b = mid
    return a, b, path


def _h_cd_01():
    return [_frac(_smallest_n(1, "0.001"))]


def _h_cd_02():
    a, b, _ = _bisect(x_ ** 3 - 2, 1, 2, 2)
    return [_frac(a)]


def _h_cd_04():
    f = x_ ** 2 - 1
    assert f.subs(x_, -2) * f.subs(x_, 2) > 0                              # same sign at both ends of [-2, 2] ...
    roots = [r for r in sp.solve(f, x_) if -2 <= r <= 2]
    return [not roots]                                                     # ... and yet there are roots: "no root" is False


def _h_cd_05():
    n = _smallest_n(1, Rational(1, 10 ** 4))
    options = [13, 14, 4, 10000]
    assert n == 13 and 1 / 2 ** (n + 1) <= Rational(1, 10 ** 4) < 1 / 2 ** n
    return [options.index(n)]


def _h_cd_06():
    f = x_ ** 2 - 3
    assert f.subs(x_, 1) < 0 < f.subs(x_, 2) and f.subs(x_, Rational(3, 2)) < 0       # the root is on the right of 3/2
    return [2]


def _h_cd_09():
    f = x_ ** 3 + x_ - 3
    a, b, path = _bisect(f, 1, 2, 2)
    return [_frac(path[0]), _frac(Rational(3, 2)), _frac(path[1]), _frac(b - a)]


def _h_cd_10():
    return [_frac(Rational(2, 2 ** 5)), _frac(Rational(2, 2 ** 6)), _frac(_smallest_n(2, "0.01")),
            Rational(2, 2 ** 7) == Rational(2, 2 ** 6) / 2]


def _h_ld_01():
    value = Integer(1)
    for _ in range(3):
        value = 1 + 1 / value
    return [_frac(value)]


def _h_ld_02():
    g = (x_ ** 2 + 1) / 4
    q = sp.sqrt(maximum(sp.diff(g, x_) ** 2, x_, sp.Interval(0, 1)))
    assert g.subs(x_, 0) >= 0 and g.subs(x_, 1) <= 1                    # g maps [0, 1] into itself (g is increasing)
    return [_frac(q)]


def _h_ld_03():
    root = sp.nsolve(x_ ** 3 - x_ - 1, x_, 1.3, prec=30)
    candidates = [(x_ + 1) ** Rational(1, 3), x_ ** 3 - 1, 1 / (x_ ** 2 - 1), (x_ + 1) / x_ ** 2]
    for g in candidates:
        assert abs(g.subs(x_, root) - root) < 1e-20                     # all four are the same equation
    below_one = [abs(sp.diff(g, x_).subs(x_, root)) < 1 for g in candidates]
    return [below_one.index(True) if below_one.count(True) == 1 else -1]


def _h_ld_04():
    g = x_ ** 2
    assert g.subs(x_, 0) == 0 and sp.diff(g, x_).subs(x_, 0) == 0           # a fixed point with g' = 0 ...
    seq = [Integer(2)]
    for _ in range(4):
        seq.append(seq[-1] ** 2)                                            # ... yet x_0 = 2 runs off: 2, 4, 16, 256, 65536
    return [abs(seq[-1]) < 1]                                               # "converges for every x_0": False


def _h_ld_05():
    star = Integer(5)
    g = lambda t: star + Rational(3, 10) * (t - star)                    # a linear g with g' = 0.3 and fixed point 5
    e = [Integer(9) - star]
    value = Integer(9)
    for _ in range(3):
        value = g(value)
        e.append(value - star)
    return [all(b == Rational(3, 10) * a for a, b in zip(e, e[1:]))]


def _h_ld_06():
    g = x_ ** 2
    fixed = sp.solve(sp.Eq(g, x_), x_)
    derivs = {r: abs(sp.diff(g, x_).subs(x_, r)) for r in fixed}
    assert derivs == {0: 0, 1: 2}
    return [2]


def _h_ld_09():
    value = Integer(1)
    out = []
    for _ in range(3):
        value = 1 + 1 / value
        out.append(_frac(value))
    star = (1 + sp.sqrt(5)) / 2
    assert abs(sp.diff(1 + 1 / x_, x_).subs(x_, star)) < 1
    return out + [bool(sp.simplify(star ** 2 - star - 1) == 0)]


def _h_ld_10():
    g = (x_ ** 2 + 1) / 4
    q = sp.sqrt(maximum(sp.diff(g, x_) ** 2, x_, sp.Interval(0, 1)))
    x1 = g.subs(x_, 0)
    maps_into = g.subs(x_, 0) >= 0 and g.subs(x_, 1) <= 1
    bound = q ** 3 / (1 - q) * abs(x1 - 0)
    return [_frac(x1), _frac(q), bool(maps_into), _frac(bound)]


def _h_nw_01():
    return [_frac(_newton_step(x_ ** 2 - 2, Integer(1)))]


def _h_nw_02():
    value = Integer(1)
    for _ in range(2):
        value = _newton_step(x_ ** 2 - 2, value)
    return [_frac(value)]


def _h_nw_03():
    return [_frac(_newton_step(x_ ** 3 - 10, Integer(2)))]


def _h_nw_04():
    f = x_ ** 3 - 2 * x_ + 2
    seq = [Integer(0)]
    for _ in range(5):
        seq.append(_newton_step(f, seq[-1]))
    assert seq[:3] == [0, 1, 0]
    return [seq[-1] == seq[-2]]                                             # 0, 1, 0, 1, ...: it does not settle: False


def _h_nw_05():
    f = x_ ** 2 - 1
    return [bool(sp.diff(f, x_).subs(x_, 0) == 0 and f.subs(x_, 0) != 0)]        # at x_n = 0 the step is a division by 0


def _h_nw_06():
    f = x_ ** 2 - 2
    root = sp.sqrt(2)
    value, errs = Integer(1), []
    for _ in range(4):
        errs.append(sp.N(abs(value - root), 30))
        value = _newton_step(f, value)
    ratios = [errs[i + 1] / errs[i] ** 2 for i in range(3)]                       # about f''/(2 f') = 0.35: a bounded constant
    assert all(0.3 < r < 0.6 for r in ratios)
    return [0]


def _h_nw_07():
    f = x_ ** 2 - 3
    x1 = _newton_step(f, Integer(2))
    right = _newton_step(f, x1)
    stale = x1 - f.subs(x_, x1) / sp.diff(f, x_).subs(x_, 2)
    assert x1 == Rational(7, 4) and right == Rational(97, 56) and stale == Rational(111, 64)
    return [2]


def _h_nw_10():
    f = x_ ** 3 - 2
    x1 = _newton_step(f, Integer(1))
    x2 = _newton_step(f, x1)
    cbrt = sp.root(2, 3)
    return [_frac(sp.diff(f, x_).subs(x_, 1)), _frac(x1), _frac(x2), bool(abs(x2 - cbrt) < abs(x1 - cbrt))]


def _h_nw_11():
    f = x_ ** 2 - 2
    value = Integer(1)
    for _ in range(3):
        value = _newton_step(f, value)
    x2 = _newton_step(f, _newton_step(f, Integer(1)))
    root = sp.sqrt(2)
    return [_frac(value), bool(abs(x2 - root) < Rational(1, 100)), _frac(_smallest_n(1, Rational(1, 10 ** 6))),
            bool(abs(value - root) < Rational(1, 10 ** 5))]


HAND = {
    "tr_t10_ss_01": _h_ss_01, "tr_t10_ss_02": _h_ss_02, "tr_t10_ss_03": _h_ss_03, "tr_t10_ss_04": _h_ss_04,
    "tr_t10_ss_05": _h_ss_05, "tr_t10_ss_06": _h_ss_06, "tr_t10_ss_07": _h_ss_07, "tr_t10_ss_11": _h_ss_11,
    "tr_t10_ss_12": _h_ss_12,
    "tr_t10_cd_01": _h_cd_01, "tr_t10_cd_02": _h_cd_02, "tr_t10_cd_04": _h_cd_04, "tr_t10_cd_05": _h_cd_05,
    "tr_t10_cd_06": _h_cd_06, "tr_t10_cd_09": _h_cd_09, "tr_t10_cd_10": _h_cd_10,
    "tr_t10_ld_01": _h_ld_01, "tr_t10_ld_02": _h_ld_02, "tr_t10_ld_03": _h_ld_03, "tr_t10_ld_04": _h_ld_04,
    "tr_t10_ld_05": _h_ld_05, "tr_t10_ld_06": _h_ld_06, "tr_t10_ld_09": _h_ld_09, "tr_t10_ld_10": _h_ld_10,
    "tr_t10_nw_01": _h_nw_01, "tr_t10_nw_02": _h_nw_02, "tr_t10_nw_03": _h_nw_03, "tr_t10_nw_04": _h_nw_04,
    "tr_t10_nw_05": _h_nw_05, "tr_t10_nw_06": _h_nw_06, "tr_t10_nw_07": _h_nw_07, "tr_t10_nw_10": _h_nw_10,
    "tr_t10_nw_11": _h_nw_11,
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
        if isinstance(v, bool) or isinstance(v, int):
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
        got = _answers(items[iid])
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
