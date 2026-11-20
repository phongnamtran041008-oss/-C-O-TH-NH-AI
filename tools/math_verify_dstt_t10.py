"""The sympy recomputation of Đại Số Tuyến Tính, floor 10 (Tài Năng): the generators and the hand-written items.

generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a true_false question or a list of
Fractions for a numeric one; merged into tools/math_verify.py EXPECTED. This module must not import math_verify.

The generators use closed formulas (n/gcd(a, n), phi(n), -x/(1 + kx), a hand-made expansion). Here every answer is found
another way: relations as 0/1 matrices (reflexive = trace n, symmetric = M equals its transpose, transitive = the Boolean
square of M lies under M); the identity and the inverse of an operation by solving the defining equation with sympy;
associativity and commutativity by expanding the two sides as polynomials; orders and inverses by sympy's n_order and
mod_inverse or by running through the multiples; counts of units and zero divisors over every pair (a, b); bilinear forms
as sympy matrix products and the symmetric matrix of a quadratic form as half its Hessian.

`HAND` recomputes every numeric answer (and the verdicts and the right options that a computation can decide) of the
hand-written items of data/math/items/dai_so_tuyen_tinh.t10.json; `hand_problems()` returns one line per answer that
differs. Answers are normalised to a list: a Fraction for a numeric answer, a bool for a true_false, the position of the
right option for a multiple_choice, in the order of the parts for a tribulation."""
from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp
from sympy import Integer, Matrix, Rational, Symbol
from sympy import totient
from sympy.ntheory import n_order

ROOT = Path(__file__).resolve().parents[1]
ITEM_FILE = ROOT / "server" / "data" / "math" / "items" / "dai_so_tuyen_tinh.t10.json"
a_, b_, c_, e_, y_ = (Symbol(s) for s in "a b c e y".split())


def _frac(v) -> Fraction:
    v = sp.simplify(sp.sympify(v))                       # (exact: no nsimplify, which can rewrite a big Rational)
    if not isinstance(v, sp.Rational):
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


# ------------------------------------------------------------------ relations as 0/1 matrices
def _matrix(rel, n: int) -> Matrix:
    m = sp.zeros(n, n)
    for a, b in rel:
        m[a - 1, b - 1] = 1
    return m


def _is_reflexive(m: Matrix) -> bool:
    return m.trace() == m.shape[0]


def _is_symmetric(m: Matrix) -> bool:
    return m == m.T


def _is_transitive(m: Matrix) -> bool:
    sq = m * m
    return all(sq[i, j] == 0 or m[i, j] == 1 for i in range(m.shape[0]) for j in range(m.shape[1]))


def _quan_he_tf(p: dict) -> bool:
    m = _matrix(p["rel"], 4)
    r, s, t = _is_reflexive(m), _is_symmetric(m), _is_transitive(m)
    return {"phản xạ": r, "đối xứng": s, "bắc cầu": t, "là một quan hệ tương đương": r and s and t}[p["prop"]]


def _so_lop(p: dict) -> list[Fraction]:
    m, n, x = p["m"], p["n"], p["x"]
    rel = [(a, b) for a in range(1, n + 1) for b in range(1, n + 1) if (a - b) % m == 0]
    if p["ask"] == "so_cap":
        return [Fraction(len(rel))]
    classes = {frozenset(b for a2, b in rel if a2 == a) for a in range(1, n + 1)}
    if p["ask"] == "so_lop":
        return [Fraction(len(classes))]
    return [Fraction(len([b for a2, b in rel if a2 == x]))]


# ------------------------------------------------------------------ operations
def _op(p: dict, x, y):
    return x + y + p["k"] if p["kind"] == "cong_hang" else x + y + p["k"] * x * y


def _trung_hoa(p: dict) -> list[Fraction]:
    sols = sp.solve(sp.Eq(_op(p, a_, e_), a_), e_)
    assert len(sols) == 1 and sols[0].is_number or len(sols) == 1, sols             # e does not depend on a
    e = sols[0]
    assert not e.has(a_)
    if p["ask"] == "trung_hoa":
        return [_frac(e)]
    sol = sp.solve(sp.Eq(_op(p, Integer(p["x"]), y_), e), y_)
    assert len(sol) == 1
    assert sp.simplify(_op(p, sol[0], Integer(p["x"])) - e) == 0                   # also from the other side
    return [_frac(sol[0])]


def _ket_hop_tf(p: dict) -> bool:
    f = lambda x, y: p["p"] * x + p["q"] * y + p["r"]                              # noqa: E731
    if p["which"] == "giao hoán":
        return sp.expand(f(a_, b_) - f(b_, a_)) == 0
    return sp.expand(f(f(a_, b_), c_) - f(a_, f(b_, c_))) == 0


# ------------------------------------------------------------------ groups, rings
def _cap_cong(p: dict) -> list[Fraction]:
    n, a = p["n"], p["a"]
    return [Fraction(next(k for k in itertools.count(1) if k * a % n == 0))]


def _cap_nhan(p: dict) -> list[Fraction]:
    return [Fraction(int(n_order(p["a"], p["p"])))]


def _dem_don_vi(p: dict) -> list[Fraction]:
    n = p["n"]
    if p["ask"] == "uoc_cua_0":
        return [Fraction(sum(1 for a in range(1, n) if any(a * b % n == 0 for b in range(1, n))))]
    units = sum(1 for a in range(1, n) if any(a * b % n == 1 for b in range(1, n)))
    assert units == int(totient(n))
    return [Fraction(units)]


def _nghich_dao_mod(p: dict) -> list[Fraction]:
    return [Fraction(int(sp.mod_inverse(p["a"], p["n"])))]


# ------------------------------------------------------------------ bilinear forms
def _ma_tran_song_tuyen(p: dict) -> list[Fraction]:
    a, u, v = Matrix(p["a"]), Matrix(p["u"]), Matrix(p["v"])
    return [_frac((u.T * a * v)[0, 0])]


def _he_so_cheo(p: dict) -> list[Fraction]:
    x1, x2 = sp.symbols("x1 x2")
    q = p["a"] * x1 ** 2 + p["b"] * x1 * x2 + p["c"] * x2 ** 2
    b = sp.hessian(q, (x1, x2)) / 2                                                  # the symmetric matrix of q
    if p["ask"] == "b12":
        return [_frac(b[0, 1])]
    if p["ask"] == "dinh_thuc":
        return [_frac(b.det())]
    return [_frac(q.subs({x1: p["u"][0], x2: p["u"][1]}))]


EXPECTED: dict = {
    "dstt_g10_quan_he_tf": _quan_he_tf,
    "dstt_g10_so_lop": _so_lop,
    "dstt_g10_trung_hoa": _trung_hoa,
    "dstt_g10_ket_hop_tf": _ket_hop_tf,
    "dstt_g10_cap_cong": _cap_cong,
    "dstt_g10_cap_nhan": _cap_nhan,
    "dstt_g10_dem_don_vi": _dem_don_vi,
    "dstt_g10_nghich_dao_mod": _nghich_dao_mod,
    "dstt_g10_ma_tran_song_tuyen": _ma_tran_song_tuyen,
    "dstt_g10_he_so_cheo": _he_so_cheo,
}


# ------------------------------------------------------------------ the hand-written items
def _brute_relations():
    """(reflexive, symmetric, equivalence) counts over all 512 relations on {1, 2, 3}, via matrices."""
    cells = [(i, j) for i in range(3) for j in range(3)]
    n_r = n_s = n_e = 0
    for mask in range(512):
        m = sp.zeros(3, 3)
        for k, (i, j) in enumerate(cells):
            m[i, j] = (mask >> k) & 1
        r, s, t = _is_reflexive(m), _is_symmetric(m), _is_transitive(m)
        n_r += r
        n_s += s
        n_e += r and s and t
    return Fraction(n_r), Fraction(n_s), Fraction(n_e)


def _h_qh_01():
    classes = {frozenset(b for b in range(1, 13) if (a - b) % 5 == 0) for a in range(1, 13)}
    assert len(classes) == 5
    return [Fraction(len([b for b in range(1, 13) if (3 - b) % 5 == 0]))]


def _h_qh_02():
    r = Matrix([[1 if a <= b else 0 for b in range(1, 5)] for a in range(1, 5)])      # <= on 1..4
    return [_is_reflexive(r) and _is_symmetric(r) and _is_transitive(r)]               # "<= is an equivalence": False


def _h_qh_03():
    s = range(1, 7)
    r = Matrix([[1 if b % a == 0 else 0 for b in s] for a in s])
    anti = all(not (r[i, j] and r[j, i]) for i in range(6) for j in range(6) if i != j)
    total = all(r[i, j] or r[j, i] for i in range(6) for j in range(6))
    assert _is_reflexive(r) and _is_transitive(r) and anti and not _is_symmetric(r) and not total
    return [0]


def _h_qh_04():
    x, y, z = Rational(0), Rational(3, 5), Rational(6, 5)
    rel = lambda s, t: abs(s - t) < 1                                                   # noqa: E731
    assert rel(x, y) and rel(y, z) and not rel(x, z)
    return [2]


def _h_qh_07():
    m = _matrix([(1, 1), (2, 2), (3, 3), (1, 2), (2, 1), (2, 3), (3, 2)], 3)
    assert _is_reflexive(m) and _is_symmetric(m) and not _is_transitive(m)
    # the smallest equivalence relation containing R: the transitive closure (a symmetric reflexive R stays so)
    closure = m
    for _ in range(3):
        closure = (closure + closure * closure).applyfunc(lambda v: 1 if v else 0)
    assert _is_reflexive(closure) and _is_symmetric(closure) and _is_transitive(closure)
    return [True, True, False, Fraction(int(sum(closure) - sum(m)))]


def _h_qh_08():
    n_r, n_s, n_e = _brute_relations()
    return [n_r, n_s, n_e, True]


def _h_pt_01():
    return [_frac(sp.solve(sp.Eq(a_ + e_ - 3, a_), e_)[0])]


def _h_pt_02():
    return [_frac(sp.solve(sp.Eq(2 + y_ + 2 * y_, 0), y_)[0])]


def _h_pt_03():
    f = lambda x, y: x + 2 * y                                                          # noqa: E731
    commutative = sp.expand(f(a_, b_) - f(b_, a_)) == 0
    associative = sp.expand(f(f(a_, b_), c_) - f(a_, f(b_, c_))) == 0
    return [commutative and associative]


def _h_pt_08():
    op = lambda x, y: x + y - 2 * x * y                                                 # noqa: E731
    e = sp.solve(sp.Eq(op(a_, e_), a_), e_)[0]
    inv = sp.solve(sp.Eq(op(Integer(3), y_), e), y_)[0]
    half = sp.solve(sp.Eq(op(Rational(1, 2), y_), e), y_)                              # no inverse of 1/2
    assert sp.expand(op(op(a_, b_), c_) - op(a_, op(b_, c_))) == 0                      # associative, as the item says
    return [_frac(op(3, 4)), _frac(e), _frac(inv), bool(half)]                           # (1/2 has no inverse: "every number has one" is False)


def _h_pt_09():
    op = lambda x, y: x + y + 1                                                         # noqa: E731
    assoc = sp.expand(op(op(a_, b_), c_) - op(a_, op(b_, c_))) == 0
    e = sp.solve(sp.Eq(op(a_, e_), a_), e_)[0]
    inv5 = sp.solve(sp.Eq(op(5, y_), e), y_)[0]
    inv_a = sp.solve(sp.Eq(op(a_, y_), e), y_)[0]                                       # y = -a - 2, whole when a is
    return [assoc, _frac(e), _frac(inv5), assoc and inv_a == -a_ - 2]


def _h_pt_10():
    return [True]                                                                       # proved in the item (e = e * e' = e')


def _h_nh_01():
    return [Fraction(next(k for k in itertools.count(1) if 8 * k % 12 == 0))]


def _h_nh_02():
    units = [a for a in range(1, 18) if any(a * b % 18 == 1 for b in range(1, 18))]
    assert len(units) == int(totient(18))
    return [Fraction(len(units))]


def _h_nh_03():
    s = {1, 2, 3, 4, 5}
    return [all(a * b % 6 in s for a in s for b in s)]                                  # "it is a group" needs closure first: False


def _h_nh_04():
    return [[6, 8, 5, 24].index(next(d for d in (6, 8, 5, 24) if 12 % d == 0))]


def _h_nh_08():
    subgroup = {8 * k % 12 for k in range(12)}
    gens = [a for a in range(12) if {a * k % 12 for k in range(12)} == set(range(12))]
    orders = {len({a * k % 12 for k in range(12)}) for a in range(12)}
    return [Fraction(len(subgroup)), Fraction(len(subgroup)), Fraction(len(gens)), 5 in orders]


def _h_nh_09():
    g = [a for a in range(1, 9) if sp.gcd(a, 9) == 1]
    orders = {a: int(n_order(a, 9)) for a in g}
    gens = [a for a in g if orders[a] == len(g)]
    return [Fraction(len(g)), Fraction(orders[2]), bool(gens), Fraction(len(gens))]


def _h_nh_10():
    h, k = {x for x in range(-30, 31) if x % 2 == 0}, {x for x in range(-30, 31) if x % 3 == 0}
    union = h | k
    return [all((x + y) in union for x in union for y in union if abs(x + y) <= 30)]


def _h_vt_01():
    return [Fraction(sum(1 for a in range(1, 12) if any(a * b % 12 == 0 for b in range(1, 12))))]


def _h_vt_02():
    def is_field(n):
        return all(any(a * b % n == 1 for b in range(1, n)) for a in range(1, n))
    return [all(is_field(n) == sp.isprime(n) for n in range(2, 30))]


def _h_vt_03():
    def is_field(n):
        return all(any(a * b % n == 1 for b in range(1, n)) for a in range(1, n))
    return [[is_field(7), False, is_field(6), False].index(True)]                       # Z, M_2(R): argued in the item


def _h_vt_07():
    units = sum(1 for a in range(1, 10) if any(a * b % 10 == 1 for b in range(1, 10)))
    zd = sum(1 for a in range(1, 10) if any(a * b % 10 == 0 for b in range(1, 10)))
    field = units == 9
    return [Fraction(units), Fraction(zd), field, Fraction(int(sp.mod_inverse(3, 10)))]


def _h_vt_08():
    inv3 = int(sp.mod_inverse(3, 7))
    x = next(x for x in range(7) if 3 * x % 7 == 4)
    return [Fraction(inv3), Fraction(x), Fraction(sum(1 for t in range(7) if t * t % 7 == 1)),
            sum(1 for t in range(8) if t * t % 8 == 1) == 2]


def _h_vt_09():
    # Z has no zero divisors but 2 is not a unit; a finite ring without zero divisors is a field (checked on Z_n)
    no_zero_divisors = not [(a, b) for a in range(-9, 10) for b in range(-9, 10) if a and b and a * b == 0]
    two_has_inverse = any(2 * b == 1 for b in range(-9, 10))
    return [not (no_zero_divisors and not two_has_inverse)]                              # Z is a counterexample: False


def _h_ds_01():
    a = Matrix([[2, -1], [3, 4]])
    u, v = Matrix([1, 2]), Matrix([3, -1])
    assert (v.T * a * u)[0, 0] == -11
    return [_frac((u.T * a * v)[0, 0])]


def _h_ds_02():
    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2")
    f = x1 * y1 + 2 * x1 * y2 + 3 * x2 * y1 + 4 * x2 * y2
    m = sp.Matrix(2, 2, lambda i, j: sp.diff(f, [x1, x2][i], [y1, y2][j]))
    assert m.tolist() == [[1, 2], [3, 4]]
    return [0]


def _h_ds_03():
    x1, x2 = sp.symbols("x1 x2")
    f = 2 * x1 * x1 + 3 * x1 * x2 - x2 * x1 + 4 * x2 * x2                               # f(x, x) with y = x
    return [_frac(sp.Poly(sp.expand(f), x1, x2).coeff_monomial(x1 * x2))]


def _h_ds_04():
    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2")
    f = x1 * y2
    swapped = f.subs({x1: y1, x2: y2, y1: x1, y2: x2}, simultaneous=True)
    return [sp.expand(f - swapped) == 0]


def _h_ds_05():
    x1, x2 = sp.symbols("x1 x2")
    q = x1 ** 2 + 6 * x1 * x2 + 5 * x2 ** 2
    b = sp.hessian(q, (x1, x2)) / 2
    assert b.tolist() == [[1, 3], [3, 5]]
    return [2]


def _h_ds_07():
    x1, x2 = sp.symbols("x1 x2")
    q = 3 * x1 ** 2 - 8 * x1 * x2 + 5 * x2 ** 2
    b = sp.hessian(q, (x1, x2)) / 2
    assert b.tolist() == [[3, -4], [-4, 5]] and q.subs({x1: 2, x2: 1}) == 1
    assert (Matrix([2, 1]).T * b * Matrix([2, 1]))[0, 0] == 1
    return [True]


def _h_ds_08():
    a = Matrix([[1, 2], [0, 3]])
    f = lambda u, v: (Matrix(u).T * a * Matrix(v))[0, 0]                                 # noqa: E731
    return [_frac(f([1, 1], [1, -1])), _frac(f([1, -1], [1, 1])), a == a.T, _frac(f([1, 1], [1, 1]))]


def _h_ds_09():
    x1, x2 = sp.symbols("x1 x2")
    q = 2 * x1 ** 2 - 6 * x1 * x2 + 5 * x2 ** 2
    b = sp.hessian(q, (x1, x2)) / 2
    definite = all(m.det() > 0 for m in (b[:1, :1], b))                                  # Sylvester
    return [_frac(b[0, 1]), _frac(b.det()), definite, _frac(q.subs({x1: 3, x2: 2}))]


def _h_ds_10():
    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2")
    f, g = x1 * y2, x2 * y1
    return [sp.expand(f.subs({y1: x1, y2: x2}) - g.subs({y1: x1, y2: x2})) == 0 and sp.expand(f - g) != 0]


HAND = {
    "dstt_t10_qh_01": _h_qh_01, "dstt_t10_qh_02": _h_qh_02, "dstt_t10_qh_03": _h_qh_03, "dstt_t10_qh_04": _h_qh_04,
    "dstt_t10_qh_07": _h_qh_07, "dstt_t10_qh_08": _h_qh_08,
    "dstt_t10_pt_01": _h_pt_01, "dstt_t10_pt_02": _h_pt_02, "dstt_t10_pt_03": _h_pt_03, "dstt_t10_pt_08": _h_pt_08,
    "dstt_t10_pt_09": _h_pt_09, "dstt_t10_pt_10": _h_pt_10,
    "dstt_t10_nh_01": _h_nh_01, "dstt_t10_nh_02": _h_nh_02, "dstt_t10_nh_03": _h_nh_03, "dstt_t10_nh_04": _h_nh_04,
    "dstt_t10_nh_08": _h_nh_08, "dstt_t10_nh_09": _h_nh_09, "dstt_t10_nh_10": _h_nh_10,
    "dstt_t10_vt_01": _h_vt_01, "dstt_t10_vt_02": _h_vt_02, "dstt_t10_vt_03": _h_vt_03, "dstt_t10_vt_07": _h_vt_07,
    "dstt_t10_vt_08": _h_vt_08, "dstt_t10_vt_09": _h_vt_09,
    "dstt_t10_ds_01": _h_ds_01, "dstt_t10_ds_02": _h_ds_02, "dstt_t10_ds_03": _h_ds_03, "dstt_t10_ds_04": _h_ds_04,
    "dstt_t10_ds_05": _h_ds_05, "dstt_t10_ds_07": _h_ds_07, "dstt_t10_ds_08": _h_ds_08, "dstt_t10_ds_09": _h_ds_09,
    "dstt_t10_ds_10": _h_ds_10,
}
def _answers(item: dict) -> list:
    """What the item carries, as a list: Fractions, bools, option or line positions."""
    if item["type"] == "tribulation":
        out = []
        for part in item["parts"]:
            out.append([Fraction(v.strip()) for v in part["answer"].split(",")][0] if part["type"] == "numeric" else part["answer"])
        return out
    if item["type"] == "numeric":
        return [Fraction(v.strip()) for v in item["answer"].split(",")]
    return [item["answer"]]


def hand_problems(path: Path = ITEM_FILE) -> list[str]:
    """One line per hand-written answer of floor 10 that sympy does not reproduce (empty = all confirmed). A
    recomputation that asserts a claim of an item without an answer key (an ordering) fails the same way."""
    raw = json.loads(path.read_text("utf-8"))
    items = {it["id"]: it for it in raw["items"]}
    problems: list[str] = []
    for iid, fn in HAND.items():
        if iid not in items:
            problems.append(f"{iid}: listed in HAND but not in the item file")
            continue
        try:
            want = fn()
        except AssertionError as e:
            problems.append(f"{iid}: a claim of the item fails ({e})")
            continue
        item = items[iid]
        if item["type"] in ("ordering", "matching"):
            continue                                              # (no answer key: the assertions above are the check)
        got = _answers(item)
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
