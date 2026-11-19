"""The sympy recomputation of the generators of Giải Tích floors 4-6: generator id -> a
function of the drawn numbers (`Draw.params`) giving a bool for a true_false question, or a
list of Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED. This module
must not import math_verify (it is imported by it).

Each answer is worked out by another route than the generator's own arithmetic: derivatives
with sp.diff or as the limit of a difference quotient, the inverse function by implicit
differentiation (sp.idiff), Taylor and Maclaurin coefficients with sp.series, limits with
sp.limit, critical points with sp.solve of f' = 0, intervals of monotonicity with
solve_univariate_inequality, extreme values on an interval with sp.maximum / sp.minimum, and
numbers of real roots with sp.real_roots."""
from __future__ import annotations

from fractions import Fraction

import sympy as sp

x = sp.Symbol("x", real=True)
t = sp.Symbol("t", real=True)
h = sp.Symbol("h", real=True)
y = sp.Symbol("y", real=True)


def _frac(v) -> Fraction:
    v = sp.nsimplify(sp.simplify(v))
    if not v.is_rational:
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _poly(coeffs, var=x) -> sp.Expr:
    return sp.Poly([sp.Integer(c) for c in coeffs], var).as_expr()


def _rat(pair) -> sp.Rational:
    return sp.Rational(pair[0], pair[1])


# ------------------------------------------------------------------ floor 4
def _ti_so_gia(p: dict) -> list[Fraction]:
    f = p["a"] * x ** 3 + p["b"] * x
    x0 = p["x0"]
    return [_frac(sp.limit((f.subs(x, x0 + h) - f.subs(x, x0)) / h, h, 0))]


def _tiep_tuyen(p: dict) -> list[Fraction]:
    f = _poly(p["coeffs"])
    x0 = p["x0"]
    slope = sp.limit((f.subs(x, x0 + h) - f.subs(x, x0)) / h, h, 0)     # by the definition
    line = sp.expand(slope * (x - x0) + f.subs(x, x0))
    return [_frac(line.coeff(x, 1)), _frac(line.coeff(x, 0))]


def _thuong(p: dict) -> list[Fraction]:
    f = (p["a"] * x + p["b"]) / (p["c"] * x + p["d"])
    return [_frac(sp.diff(f, x).subs(x, p["x"]))]


def _day_chuyen_tf(p: dict) -> bool:
    f = (p["a"] * x ** 2 + p["b"]) ** p["n"]
    return sp.diff(f, x).subs(x, p["x"]) == p["claim"]


def _tham_so(p: dict) -> list[Fraction]:
    X = p["a"] * t ** 2 + p["b"] * t
    Y = p["c"] * t ** 3 + p["d"] * t
    t0 = p["t"]
    # the slope of the chord through the points at t0 and t, as t -> t0
    chord = (Y - Y.subs(t, t0)) / (X - X.subs(t, t0))
    return [_frac(sp.limit(chord, t, t0))]


def _nguoc(p: dict) -> list[Fraction]:
    f = x ** 3 + p["a"] * x + p["b"]
    y0 = f.subs(x, p["x"])
    # the inverse g satisfies f(g(y)) = y; differentiate that relation implicitly
    g = sp.Symbol("g", real=True)
    dg = sp.idiff(f.subs(x, g) - y, g, y)
    roots = [r for r in sp.real_roots(sp.Poly(f - y0, x))]
    assert len(roots) == 1
    return [_frac(dg.subs(g, roots[0]))]


def _xap_xi(p: dict) -> list[Fraction]:
    a, d = p["a"], p["d"]
    f = sp.sqrt(x) if p["kind"] == "sqrt" else sp.root(x, 3)
    x0 = a ** 2 if p["kind"] == "sqrt" else a ** 3
    df = sp.diff(f, x).subs(x, x0) * d                 # the differential at x0
    return [_frac(f.subs(x, x0) + df)]


def _cap_cao(p: dict) -> list[Fraction]:
    if p["kind"] == "inv":
        f = 1 / (x + p["p"])
    else:
        f = x ** p["m"] + p["c"] * x ** (p["m"] - 1)
    return [_frac(sp.diff(f, x, p["n"]).subs(x, p["x"]))]


# ------------------------------------------------------------------ floor 5
def _lagrange(p: dict) -> list[Fraction]:
    c = sp.Symbol("c", real=True)
    f = _poly(p["coeffs"]) if p["kind"] == "quad" else 1 / x
    u, v = p["u"], p["v"]
    slope = (f.subs(x, v) - f.subs(x, u)) / (v - u)
    sols = [s for s in sp.solve(sp.Eq(sp.diff(f, x).subs(x, c), slope), c) if u < s < v]
    assert len(sols) == 1
    return [_frac(sols[0])]


def _rolle_tf(p: dict) -> bool:
    f = _poly(p["coeffs"])
    return sp.simplify(f.subs(x, p["u"]) - f.subs(x, p["v"])) == 0


def _cauchy(p: dict) -> list[Fraction]:
    c = sp.Symbol("c", real=True)
    u, v = p["u"], p["v"]
    f, g = x ** 3, x ** 2
    eq = sp.Eq((f.subs(x, v) - f.subs(x, u)) * sp.diff(g, x).subs(x, c),
               (g.subs(x, v) - g.subs(x, u)) * sp.diff(f, x).subs(x, c))
    sols = [s for s in sp.solve(eq, c) if u < s < v]
    assert len(sols) == 1
    return [_frac(sols[0])]


def _series_coeff(f, k: int, at=0) -> Fraction:
    s = sp.series(f, x, at, k + 1).removeO()
    if at != 0:
        u = sp.Symbol("u", real=True)
        s = sp.expand(s.subs(x, u + at))
        return _frac(s.coeff(u, k))
    return _frac(sp.expand(s).coeff(x, k))


def _taylor_he_so(p: dict) -> list[Fraction]:
    return [_series_coeff(_poly(p["coeffs"]), p["k"], p["a"])]


def _taylor_ln(p: dict) -> list[Fraction]:
    f = sp.log(x) if p["kind"] == "ln" else 1 / x
    return [_series_coeff(f, p["k"], p["a"])]


def _basic(kind: str, a) -> sp.Expr:
    return {"exp": lambda: sp.exp(a * x), "ln": lambda: sp.log(1 + a * x), "sin": lambda: sp.sin(a * x),
            "cos": lambda: sp.cos(a * x), "pow": lambda: (1 + x) ** a}[kind]()


def _maclaurin(p: dict) -> list[Fraction]:
    return [_series_coeff(_basic(p["kind"], _rat(p["a"])), p["k"])]


def _maclaurin_tich(p: dict) -> list[Fraction]:
    left = sp.exp(p["a"] * x)
    right = (1 + p["b"] * x) ** p["m"] if p["other"] == "poly" else _basic(p["other"], p["b"])
    return [_series_coeff(left * right, p["k"])]


def _lhospital(p: dict) -> list[Fraction]:
    if p["kind"] == "poly":
        c = p["c"]
        expr = (x ** p["n"] - sp.Integer(c) ** p["n"]) / (x ** p["m"] - sp.Integer(c) ** p["m"])
        return [_frac(sp.limit(expr, x, c))]
    a, b = p["a"], p["b"]
    expr = ((sp.exp(a * x) - 1) / sp.sin(b * x) if p["kind"] == "exp_sin"
            else sp.log(1 + a * x) / sp.tan(b * x))
    return [_frac(sp.limit(expr, x, 0))]


def _lhospital_bac2(p: dict) -> list[Fraction]:
    a, b = p["a"], p["b"]
    expr = {"exp": (sp.exp(a * x) - 1 - a * x) / x ** 2,
            "cos": (1 - sp.cos(a * x)) / (b * x ** 2),
            "sin": (a * x - sp.sin(a * x)) / x ** 3,
            "ln": (sp.log(1 + a * x) - a * x) / x ** 2}[p["kind"]]
    return [_frac(sp.limit(expr, x, 0))]


def _vo_dinh_tich(p: dict) -> list[Fraction]:
    a = p["a"]
    if p["kind"] == "sin":
        return [_frac(sp.limit(x * sp.sin(sp.Integer(a) / x), x, sp.oo))]
    if p["kind"] == "ln":
        return [_frac(sp.limit(x * (sp.log(x + a) - sp.log(x)), x, sp.oo))]
    return [_frac(sp.limit(x * sp.cot(a * x), x, 0))]


def _vo_dinh_mu(p: dict) -> list[Fraction]:
    a, b = p["a"], p["b"]
    expr, at = {"lin0": ((1 + a * x) ** (sp.Integer(b) / x), 0),
                "linoo": ((1 + sp.Integer(a) / x) ** (b * x), sp.oo),
                "cos": (sp.cos(a * x) ** (sp.Integer(b) / x ** 2), 0),
                "sin": ((1 + sp.sin(a * x)) ** (sp.Integer(b) / x), 0)}[p["kind"]]
    lim = sp.limit(expr, x, at)
    return [_frac(sp.log(lim))]


# ------------------------------------------------------------------ floor 6
def _don_dieu(p: dict) -> list[Fraction]:
    fp = sp.diff(_poly(p["coeffs"]), x)
    rel = fp <= 0 if p["k"] > 0 else fp >= 0
    interval = sp.solve_univariate_inequality(rel, x, relational=False)
    assert isinstance(interval, sp.Interval)
    return [_frac(interval.start), _frac(interval.end)]


def _dong_bien_tf(p: dict) -> bool:
    fp = sp.diff(_poly(p["coeffs"]), x)
    return bool(sp.minimum(fp, x, sp.S.Reals) >= 0)


def _extrema(f) -> dict:
    """{point: 'max' | 'min'} by the sign of f' just left and right of each root of f' = 0."""
    fp = sp.diff(f, x)
    out = {}
    for r in sorted(set(sp.solve(fp, x))):
        eps = sp.Rational(1, 1000)
        left, right = fp.subs(x, r - eps), fp.subs(x, r + eps)
        if left > 0 > right:
            out[r] = "max"
        elif left < 0 < right:
            out[r] = "min"
    return out


def _cuc_tri(p: dict) -> list[Fraction]:
    f = _poly(p["coeffs"])
    want = "max" if p["ask"] == "cực đại" else "min"
    points = [r for r, kind in _extrema(f).items() if kind == want]
    assert len(points) == 1
    return [_frac(f.subs(x, points[0]))]


def _so_cuc_tri(p: dict) -> list[Fraction]:
    return [Fraction(len(_extrema(_poly(p["coeffs"]))))]


def _gtln(p: dict) -> list[Fraction]:
    f = _poly(p["coeffs"])
    dom = sp.Interval(p["u"], p["v"])
    return [_frac(sp.maximum(f, x, dom)), _frac(sp.minimum(f, x, dom))]


def _x_nghich(p: dict) -> list[Fraction]:
    f = x + sp.Integer(p["m"]) / x
    dom = sp.Interval(p["u"], p["v"])
    return [_frac(sp.maximum(f, x, dom)), _frac(sp.minimum(f, x, dom))]


def _diem_uon(p: dict) -> list[Fraction]:
    f = _poly(p["coeffs"])
    f2 = sp.diff(f, x, 2)
    roots = sp.solve(f2, x)
    assert len(roots) == 1
    x0 = roots[0]
    assert f2.subs(x, x0 - 1) * f2.subs(x, x0 + 1) < 0          # f'' really changes sign
    return [_frac(x0), _frac(f.subs(x, x0))]


def _uon_tf(p: dict) -> bool:
    f2 = sp.diff(_poly(p["coeffs"]), x, 2)
    inflections = 0
    for r in set(sp.real_roots(sp.Poly(f2, x))):
        eps = sp.Rational(1, 10 ** 6)
        if sp.sign(f2.subs(x, r - eps)) * sp.sign(f2.subs(x, r + eps)) < 0:
            inflections += 1
    has_two = inflections == 2
    assert inflections in (0, 2)
    return has_two if p["claim"] == "có hai điểm uốn" else inflections == 0


def _tiem_can(p: dict) -> list[Fraction]:
    f = (p["a"] * x + p["b"]) / (p["c"] * x + p["d"])
    poles = [r for r in sp.solve(sp.denom(sp.together(f)), x) if sp.limit(f, x, r, "+").is_infinite]
    assert len(poles) == 1
    return [_frac(poles[0]), _frac(sp.limit(f, x, sp.oo))]


def _tiem_can_xien(p: dict) -> list[Fraction]:
    f = _poly(p["top"]) / (x - p["d"])
    slope = sp.limit(f / x, x, sp.oo)
    return [_frac(slope), _frac(sp.limit(f - slope * x, x, sp.oo))]


def _so_nghiem(p: dict) -> list[Fraction]:
    roots = set(sp.real_roots(sp.Poly(_poly(p["coeffs"]) - p["m"], x)))
    return [Fraction(len(roots))]


EXPECTED: dict = {
    # ---- floor 4
    "gt_g4_ti_so_gia": _ti_so_gia,
    "gt_g4_tiep_tuyen": _tiep_tuyen,
    "gt_g4_da_thuc": lambda p: [_frac(sp.diff(_poly(p["coeffs"]), x).subs(x, p["x"]))],
    "gt_g4_thuong": _thuong,
    "gt_g4_luy_thua_hop": lambda p: [_frac(sp.diff((p["a"] * x + p["b"]) ** p["n"], x).subs(x, p["x"]))],
    "gt_g4_day_chuyen_tf": _day_chuyen_tf,
    "gt_g4_ln_hop": lambda p: [_frac(sp.diff(sp.log(_poly(p["coeffs"])), x).subs(x, p["x"]))],
    "gt_g4_tham_so": _tham_so,
    "gt_g4_nguoc": _nguoc,
    "gt_g4_xap_xi": _xap_xi,
    "gt_g4_cap_cao": _cap_cao,
    # ---- floor 5
    "gt_g5_lagrange": _lagrange,
    "gt_g5_rolle_tf": _rolle_tf,
    "gt_g5_cauchy": _cauchy,
    "gt_g5_taylor_he_so": _taylor_he_so,
    "gt_g5_taylor_ln": _taylor_ln,
    "gt_g5_maclaurin": _maclaurin,
    "gt_g5_maclaurin_tich": _maclaurin_tich,
    "gt_g5_lhospital": _lhospital,
    "gt_g5_lhospital_bac2": _lhospital_bac2,
    "gt_g5_vo_dinh_tich": _vo_dinh_tich,
    "gt_g5_vo_dinh_mu": _vo_dinh_mu,
    # ---- floor 6
    "gt_g6_don_dieu": _don_dieu,
    "gt_g6_dong_bien_tf": _dong_bien_tf,
    "gt_g6_cuc_tri": _cuc_tri,
    "gt_g6_so_cuc_tri": _so_cuc_tri,
    "gt_g6_gtln": _gtln,
    "gt_g6_x_nghich": _x_nghich,
    "gt_g6_diem_uon": _diem_uon,
    "gt_g6_uon_tf": _uon_tf,
    "gt_g6_tiem_can": _tiem_can,
    "gt_g6_tiem_can_xien": _tiem_can_xien,
    "gt_g6_so_nghiem": _so_nghiem,
}
