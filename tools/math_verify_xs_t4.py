"""The sympy recomputation of the generators of Xác Suất và Thống Kê, floors 4-6 (M11 round 2):
generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a true_false
question, or a list of Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED.
This module must not import math_verify (it is imported by it).

The generators use the closed formulas of the floors. Here every answer is found another way:
- floor 4: a population of products (or people) is built and counted, or every (die face,
  ball) outcome is listed with its weight; a complete system is checked with sympy sets;
- floor 5: the draws are listed one by one (itertools), F(x) is P(X < x) of a sympy.stats
  FiniteRV, the missing probability is solved for, and densities are integrated by sympy;
- floor 6: sympy.stats FiniteRV / Binomial / Poisson / Uniform with E, variance and P, and the
  Laplace table is rebuilt from erf (so a wrong table value in the generator is caught too)."""
from __future__ import annotations

import itertools
from fractions import Fraction

import sympy as sp
from sympy import FiniteSet, Rational
from sympy.stats import Binomial, E, FiniteRV, P, Poisson, Uniform, density, variance


def _frac(v) -> Fraction:
    v = sp.simplify(sp.sympify(v))
    if not isinstance(v, sp.Rational):
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _r(text) -> sp.Rational:
    return Rational(str(text))


# ------------------------------------------------------------------ floor 4
def _he_day_du(p: dict) -> bool:
    omega = FiniteSet(*range(1, 7))
    sets = [FiniteSet(*g) for g in p["groups"]]
    disjoint = all(sp.Intersection(a, b) == sp.S.EmptySet for a, b in itertools.combinations(sets, 2))
    return disjoint and sp.Union(*sets) == omega


def _cay_hai_hop(p: dict) -> list[Fraction]:
    boxes = {1: ["do"] * p["box1"][0] + ["xanh"] * p["box1"][1],
             2: ["do"] * p["box2"][0] + ["xanh"] * p["box2"][1]}
    total = Rational(0)
    for face in range(1, 7):                          # every (face, ball) outcome with its weight
        box = 1 if face <= p["k"] else 2
        for ball in boxes[box]:
            if box == p["box"] and ball == p["colour"]:
                total += Rational(1, 6) / len(boxes[box])
    return [_frac(total)]


def _population(p: dict) -> tuple[list[int], list[int], int]:
    """A whole factory whose counts are exactly the stated shares and rates."""
    shares, rates = [_r(s) for s in p["shares"]], [_r(r) for r in p["rates"]]
    n = sp.ilcm(*[s.q for s in shares], *[(s * r).q for s, r in zip(shares, rates)])
    made = [int(s * n) for s in shares]
    bad = [int(s * r * n) for s, r in zip(shares, rates)]
    assert sum(made) == n
    return made, bad, n


def _day_du(p: dict) -> list[Fraction]:
    _, bad, n = _population(p)
    return [_frac(Rational(sum(bad), n))]


def _bayes(p: dict) -> list[Fraction]:
    _, bad, _ = _population(p)
    return [_frac(Rational(bad[p["i"]], sum(bad)))]


def _chuyen_bi(p: dict) -> list[Fraction]:
    box1 = ["w"] * p["box1"][0] + ["k"] * p["box1"][1]
    box2 = ["w"] * p["box2"][0] + ["k"] * p["box2"][1]
    total = Rational(0)
    for moved in box1:                                # every (moved ball, drawn ball) outcome
        after = box2 + [moved]
        for ball in after:
            if ball == "w":
                total += Rational(1, len(box1)) * Rational(1, len(after))
    return [_frac(total)]


def _xet_nghiem(p: dict) -> list[Fraction]:
    prev, sens, fpos = _r(p["p"]), _r(p["s"]), _r(p["f"])
    n = sp.ilcm(prev.q, (prev * sens).q, ((1 - prev) * fpos).q)       # a town of n people
    sick_pos = prev * sens * n
    healthy_pos = (1 - prev) * fpos * n
    return [_frac(sick_pos / (sick_pos + healthy_pos))]


# ------------------------------------------------------------------ floor 5
def _bang_thieu(p: dict) -> list[Fraction]:
    q = sp.Symbol("p")
    probs = [q if s == "p" else _r(s) for s in p["shown"]]
    return [_frac(sp.solve(sp.Eq(sum(probs), 1), q)[0])]


def _rut_bi_bang(p: dict) -> list[Fraction]:
    balls = ["r"] * p["red"] + ["b"] * p["blue"]
    hands = list(itertools.combinations(range(len(balls)), p["m"]))
    good = sum(1 for h in hands if sum(balls[i] == "r" for i in h) == p["k"])
    return [_frac(Rational(good, len(hands)))]


def _finite(p: dict):
    return FiniteRV("X", {v: _r(q) for v, q in zip(p["values"], p["probs"])})


def _ham_phan_phoi(p: dict) -> list[Fraction]:
    x = _finite(p)
    return [_frac(P(x < p["c"]))]


def _density(p: dict, k=None):
    t = sp.Symbol("t", real=True)
    k = sp.Symbol("k", positive=True) if k is None else k
    return t, k, k * t ** p["n"]


def _hang_so(p: dict) -> list[Fraction]:
    t, k, f = _density(p)
    return [_frac(sp.solve(sp.Eq(sp.integrate(f, (t, 0, p["a"])), 1), k)[0])]


def _mat_do_tf(p: dict) -> bool:
    t, _, f = _density(p, _r(p["k"]))
    return sp.integrate(f, (t, 0, p["a"])) == 1


def _khoang(p: dict) -> list[Fraction]:
    t, k, f = _density(p)
    k_value = sp.solve(sp.Eq(sp.integrate(f, (t, 0, p["a"])), 1), k)[0]
    lo, hi = _r(p["lo"]), _r(p["hi"])
    lo_c, hi_c = sp.Max(lo, 0), sp.Min(hi, p["a"])          # the density is 0 outside [0, a]
    return [_frac(sp.integrate(f.subs(k, k_value), (t, lo_c, hi_c)))]


# ------------------------------------------------------------------ floor 6
def _ky_vong(p: dict) -> list[Fraction]:
    return [_frac(E(_finite(p)))]


def _phuong_sai(p: dict) -> list[Fraction]:
    return [_frac(variance(_finite(p)))]


def _bien_doi(p: dict) -> list[Fraction]:
    y = p["a"] * _finite(p) + p["b"]
    return [_frac(E(y) if p["ask"] == "E" else variance(y))]


def _nhi_thuc(p: dict) -> list[Fraction]:
    x = Binomial("X", p["n"], _r(p["p"]))
    if p["ask"] == "E":
        return [_frac(E(x))]
    if p["ask"] == "V":
        return [_frac(variance(x))]
    return [_frac(P(sp.Eq(x, p["k"])))]


def _poisson_ti_so(p: dict) -> list[Fraction]:
    x = Poisson("X", _r(p["lam"]))
    pmf = density(x)
    return [_frac(sp.simplify(pmf(p["k"]) / pmf(p["k"] - 1)))]


def _deu(p: dict) -> list[Fraction]:
    x = Uniform("X", p["a"], p["b"])
    if p["ask"] == "E":
        return [_frac(E(x))]
    if p["ask"] == "V":
        return [_frac(variance(x))]
    c, d = p["cd"]
    return [_frac(P(sp.And(x > c, x < d)))]


def _laplace(z: sp.Rational) -> Fraction:
    """Phi(|z|) to 4 decimals, computed from erf; odd in z."""
    value = sp.erf(abs(z) / sp.sqrt(2)) / 2
    rounded = Fraction(int(sp.floor(value * 10 ** 4 + Rational(1, 2))), 10 ** 4)
    return rounded if z >= 0 else -rounded


def _chuan(p: dict) -> list[Fraction]:
    mu, sigma = p["mu"], p["sigma"]
    event = p["event"].replace(" ", "")
    z = lambda c: (_r(c) - mu) / sigma                       # noqa: E731
    if "<X<" in event:
        lo, hi = event.split("<X<")
        return [_laplace(z(hi)) - _laplace(z(lo))]
    if event.startswith("X>"):
        return [Fraction(1, 2) - _laplace(z(event[2:]))]
    return [Fraction(1, 2) + _laplace(z(event[2:]))]


EXPECTED: dict = {
    # ---- floor 4
    "xs_g4_he_day_du_tf": _he_day_du,
    "xs_g4_cay_hai_hop": _cay_hai_hop,
    "xs_g4_day_du": _day_du,
    "xs_g4_bayes": _bayes,
    "xs_g4_chuyen_bi": _chuyen_bi,
    "xs_g4_xet_nghiem": _xet_nghiem,
    # ---- floor 5
    "xs_g5_bang_thieu": _bang_thieu,
    "xs_g5_rut_bi_bang": _rut_bi_bang,
    "xs_g5_ham_phan_phoi": _ham_phan_phoi,
    "xs_g5_hang_so": _hang_so,
    "xs_g5_mat_do_tf": _mat_do_tf,
    "xs_g5_khoang": _khoang,
    # ---- floor 6
    "xs_g6_ky_vong": _ky_vong,
    "xs_g6_phuong_sai": _phuong_sai,
    "xs_g6_bien_doi": _bien_doi,
    "xs_g6_nhi_thuc": _nhi_thuc,
    "xs_g6_poisson_ti_so": _poisson_ti_so,
    "xs_g6_deu": _deu,
    "xs_g6_chuan": _chuan,
}
