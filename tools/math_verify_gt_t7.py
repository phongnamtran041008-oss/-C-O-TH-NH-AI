"""The sympy recomputation of the generators of Giải Tích floors 7-9: generator id -> a
function of the drawn numbers (`Draw.params`) giving a bool for a true_false question, or a
list of Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED. This module
must not import math_verify (it is imported by it).

The generators work from hand-written antiderivatives and closed forms; here every answer
comes from another route: sp.integrate of the integrand itself (improper integrals with an
infinite bound, the absolute value split at the roots sympy finds), sp.apart for partial
fractions, the derivative of an integral with a variable bound taken after integrating,
sp.diff / sp.idiff for partial and implicit derivatives, sp.solve for stationary points and
the Lagrange system, the eigenvalues of sp.hessian to classify a stationary point, and the
directional derivative as the limit of a difference quotient."""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache

import sympy as sp

x = sp.Symbol("x", real=True)
y = sp.Symbol("y", real=True)
t = sp.Symbol("t", real=True)
xp = sp.Symbol("xp", positive=True)
lam = sp.Symbol("lam", real=True)


def _frac(v) -> Fraction:
    v = sp.nsimplify(sp.simplify(v))
    if not v.is_rational:
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _poly(coeffs, var=x) -> sp.Expr:
    return sp.Poly([sp.Integer(c) for c in coeffs], var).as_expr()


def _terms(terms) -> sp.Expr:
    return sum(sp.Integer(c) * x ** i * y ** j for c, i, j in terms)


# ------------------------------------------------------------------ floor 7
def _nguyen_ham_dk(p: dict) -> list[Fraction]:
    f = p["a"] * xp ** 2 + p["b"] * xp + p["c"] / xp ** 2
    # F(2) = F(1) + integral of f over [1, 2]
    return [_frac(p["d"] + sp.integrate(f, (xp, 1, 2)))]


def _doi_bien(p: dict) -> list[Fraction]:
    return [_frac(sp.integrate(p["k"] * x * (x ** 2 + p["p"]) ** p["n"], (x, 0, p["m"])))]


def _tung_phan(p: dict) -> list[Fraction]:
    value = sp.expand(sp.integrate((p["a"] * x + p["b"]) * sp.exp(x), (x, 0, 1)))
    e = sp.Symbol("e")
    poly = sp.Poly(value.subs(sp.E, e), e)
    return [_frac(poly.coeff_monomial(e)), _frac(poly.coeff_monomial(1))]


def _tach_phan_thuc(p: dict) -> list[Fraction]:
    r, s = p["r"], p["s"]
    parts = sp.apart((p["p"] * x + p["q"]) / ((x - r) * (x - s)), x)
    out = {}
    for term in sp.Add.make_args(parts):
        num, den = sp.fraction(sp.together(term))
        root = sp.solve(den, x)
        assert len(root) == 1
        out[root[0]] = num / sp.Poly(den, x).LC()
    return [_frac(out[r]), _frac(out[s])]


def _tri_tuyet_doi(p: dict) -> list[Fraction]:
    f = p["k"] * (x ** 2 - p["s"] * x)
    b = p["b"]
    cuts = sorted({0, b} | {r for r in sp.solve(f, x) if 0 < r < b})
    total = 0
    for lo, hi in zip(cuts, cuts[1:]):
        piece = sp.integrate(f, (x, lo, hi))
        total += abs(piece)
    return [_frac(total)]


def _can_bien(p: dict) -> list[Fraction]:
    g = t ** 2 + p["p"] * t + p["q"]
    F = sp.integrate(g, (t, x, x ** 2))            # integrate first, then differentiate
    return [_frac(sp.diff(F, x).subs(x, p["x0"]))]


# ------------------------------------------------------------------ floor 8
def _dien_tich(p: dict) -> list[Fraction]:
    f = _poly(p["coeffs"])
    roots = sorted(sp.solve(f, x))
    return [_frac(abs(sp.integrate(f, (x, roots[0], roots[-1]))))]


def _the_tich(p: dict) -> list[Fraction]:
    m = sp.Rational(p["m"])
    curve = p["c"] * xp ** m
    return [_frac(sp.integrate(sp.pi * curve ** 2, (xp, 0, p["d"])) / sp.pi)]


def _do_dai(p: dict) -> list[Fraction]:
    curve = sp.Rational(2, 3) * xp ** sp.Rational(3, 2)
    return [_frac(sp.integrate(sp.sqrt(1 + sp.diff(curve, xp) ** 2), (xp, p["a"], p["b"])))]


def _suy_rong(p: dict) -> list[Fraction]:
    if p["kind"] == "power":
        return [_frac(sp.integrate(p["c"] / xp ** p["n"], (xp, p["a"], sp.oo)))]
    return [_frac(sp.integrate(p["c"] * xp * sp.exp(-p["k"] * xp), (xp, 0, sp.oo)))]


def _loai_2(p: dict) -> list[Fraction]:
    return [_frac(sp.integrate(p["c"] * xp ** (-sp.Rational(p["p"])), (xp, 0, p["b"])))]


@lru_cache(maxsize=None)
def _converges(m: int, n: int) -> bool:
    # the integrand decays like x^(-q) with q = -lim ln f / ln x; integrable at +oo iff q > 1
    # (comparison with the p-integral; q comes from sympy's limit, not from n - m). A direct
    # sp.integrate to oo gives the same answers but takes over a minute for the 12 cases.
    f = xp ** m / (xp ** n + 1)
    q = -sp.limit(sp.log(f) / sp.log(xp), xp, sp.oo)
    return bool(q > 1)


# ------------------------------------------------------------------ floor 9
def _dao_ham_rieng(p: dict) -> list[Fraction]:
    f = _terms(p["terms"])
    a, b = (x if c == "x" else y for c in p["kind"])
    return [_frac(sp.diff(f, a, b).subs({x: p["x"], y: p["y"]}))]


def _ham_an(p: dict) -> list[Fraction]:
    F = x ** 2 + p["a"] * x * y + p["b"] * y ** 2 - p["c"]
    assert F.subs({x: p["x"], y: p["y"]}) == 0
    return [_frac(sp.idiff(F, y, x).subs({x: p["x"], y: p["y"]}))]


def _quad(p: dict) -> sp.Expr:
    return p["A"] * x ** 2 + p["B"] * x * y + p["C"] * y ** 2 + p["D"] * x + p["E"] * y


def _diem_dung(p: dict) -> list[Fraction]:
    f = _quad(p)
    sol = sp.solve([sp.diff(f, x), sp.diff(f, y)], [x, y], dict=True)
    assert len(sol) == 1
    return [_frac(sol[0][x]), _frac(sol[0][y])]


def _cuc_tri_tf(p: dict) -> bool:
    eig = list(sp.hessian(_quad(p), (x, y)).eigenvals())
    if all(e.is_positive for e in eig):
        kind = "cực tiểu"
    elif all(e.is_negative for e in eig):
        kind = "cực đại"
    else:
        kind = "yên ngựa"
    return kind == p["claim"]


def _lagrange(p: dict) -> list[Fraction]:
    f = p["p"] * x + p["q"] * y
    g = x ** 2 + y ** 2 - p["r"] ** 2
    sols = sp.solve([sp.diff(f, x) - lam * sp.diff(g, x), sp.diff(f, y) - lam * sp.diff(g, y), g],
                    [x, y, lam], dict=True)
    values = [f.subs(s) for s in sols]
    return [_frac(max(values)), _frac(min(values))]


def _dao_ham_huong(p: dict) -> list[Fraction]:
    f = _terms(p["terms"])
    u1, u2 = (sp.Rational(a, b) for a, b in p["u"])
    h = sp.Symbol("h", real=True)
    x0, y0 = p["x"], p["y"]
    quotient = (f.subs({x: x0 + h * u1, y: y0 + h * u2}) - f.subs({x: x0, y: y0})) / h
    return [_frac(sp.limit(quotient, h, 0))]


def _lan_truyen(p: dict) -> list[Fraction]:
    w, b = sp.symbols("w b", real=True)
    L = (w * p["x"] + b - p["t"]) ** 2
    at = {w: p["w"], b: p["b"]}
    return [_frac(L.subs(at)), _frac(sp.diff(L, w).subs(at)), _frac(sp.diff(L, b).subs(at))]


EXPECTED: dict = {
    # ---- floor 7
    "gt_g7_nguyen_ham_dk": _nguyen_ham_dk,
    "gt_g7_doi_bien": _doi_bien,
    "gt_g7_tung_phan": _tung_phan,
    "gt_g7_tach_phan_thuc": _tach_phan_thuc,
    "gt_g7_tri_tuyet_doi": _tri_tuyet_doi,
    "gt_g7_can_bien": _can_bien,
    # ---- floor 8
    "gt_g8_dien_tich": _dien_tich,
    "gt_g8_the_tich": _the_tich,
    "gt_g8_do_dai": _do_dai,
    "gt_g8_suy_rong": _suy_rong,
    "gt_g8_loai_2": _loai_2,
    "gt_g8_hoi_tu_tf": lambda p: _converges(p["m"], p["n"]),
    # ---- floor 9
    "gt_g9_dao_ham_rieng": _dao_ham_rieng,
    "gt_g9_ham_an": _ham_an,
    "gt_g9_diem_dung": _diem_dung,
    "gt_g9_cuc_tri_tf": _cuc_tri_tf,
    "gt_g9_lagrange": _lagrange,
    "gt_g9_dao_ham_huong": _dao_ham_huong,
    "gt_g9_lan_truyen": _lan_truyen,
}
