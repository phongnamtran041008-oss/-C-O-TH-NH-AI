"""The sympy recomputation of every generator of Giải Tích (M11): generator id -> a function
of the drawn numbers (`Draw.params`) giving a bool for a true_false question, or a list of
Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED. This module must not
import math_verify (it is imported by it).

Each answer is worked out by another route than the generator's own arithmetic: limits with
sp.limit (never by cancelling a factor by hand), compositions by substitution, inverses with
sp.solve, periods with sp.periodicity, continuity by comparing one-sided limits, the root of a
cubic with sp.real_roots."""
from __future__ import annotations

from fractions import Fraction

import sympy as sp

x = sp.Symbol("x", real=True)
n = sp.Symbol("n", positive=True, integer=True)


def _frac(v) -> Fraction:
    v = sp.nsimplify(sp.simplify(v))
    if not v.is_rational:
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _poly(coeffs, var=x) -> sp.Expr:
    return sp.Poly([sp.Integer(c) for c in coeffs], var).as_expr()


# ------------------------------------------------------------------ floor 1
def _chan_le(p: dict) -> bool:
    f = p["a"] * x ** p["m"] + p["b"] * x ** p["n"]
    even = sp.simplify(f.subs(x, -x) - f) == 0
    odd = sp.simplify(f.subs(x, -x) + f) == 0
    return even if p["claim"] == "chẵn" else odd


def _chu_ky(p: dict) -> list[Fraction]:
    fn = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}[p["fn"]]
    return [_frac(sp.periodicity(fn(p["a"] * x + p["b"]), x) / sp.pi)]


def _hop_gia_tri(p: dict) -> list[Fraction]:
    f = p["f"][0] * x + p["f"][1]
    g = x ** 2 + p["c"]
    h = f.subs(x, g) if p["order"] == "fg" else g.subs(x, f)
    return [_frac(h.subs(x, p["x"]))]


def _hop_he_so(p: dict) -> list[Fraction]:
    h = sp.expand((p["f"][0] * x + p["f"][1]).subs(x, p["g"][0] * x + p["g"][1]))
    return [_frac(h.coeff(x, 1)), _frac(h.coeff(x, 0))]


def _nguoc_bac_nhat(p: dict) -> list[Fraction]:
    y = sp.Symbol("y")
    inv = sp.solve(sp.Eq(y, p["a"] * x + p["b"]), x)[0].subs(y, x)
    inv = sp.expand(inv)
    return [_frac(inv.coeff(x, 1)), _frac(inv.coeff(x, 0))]


def _nguoc_phan_thuc(p: dict) -> list[Fraction]:
    f = (p["a"] * x + p["b"]) / (p["c"] * x + p["d"])
    sols = [s for s in sp.solve(sp.Eq(f, p["k"]), x) if (p["c"] * x + p["d"]).subs(x, s) != 0]
    assert len(sols) == 1
    return [_frac(sols[0])]


# ------------------------------------------------------------------ floor 2
def _day_mu(p: dict) -> list[Fraction]:
    u = (p["a"] * sp.Integer(p["p"]) ** n + p["b"] * sp.Integer(p["q"]) ** n) / \
        (p["c"] * sp.Integer(p["p"]) ** n + p["d"] * sp.Integer(p["q"]) ** n)
    return [_frac(sp.limit(u, n, sp.oo))]


def _vo_cuc(p: dict) -> list[Fraction]:
    target = sp.oo if p["side"] == "+" else -sp.oo
    return [_frac(sp.limit(_poly(p["top"]) / _poly(p["bottom"]), x, target))]


def _sin_x(p: dict) -> list[Fraction]:
    a, b = p["a"], p["b"]
    expr = {"sin/x": sp.sin(a * x) / (b * x), "tan/x": sp.tan(a * x) / (b * x),
            "sin/sin": sp.sin(a * x) / sp.sin(b * x), "x/tan": (a * x) / sp.tan(b * x)}[p["kind"]]
    return [_frac(sp.limit(expr, x, 0))]


def _mu_e(p: dict) -> list[Fraction]:
    a, b = p["a"], p["b"]
    base = 1 + sp.Rational(a) / n if p["kind"] == "a/n" else 1 + 1 / (a * n)
    lim = sp.limit(base ** (b * n), n, sp.oo)
    return [_frac(sp.log(lim))]


def _vcb_cap(p: dict) -> list[Fraction]:
    if p["kind"] == "poly":
        expr = p["a"] * x ** p["m"] + p["b"] * x ** p["n"]
    elif p["kind"] == "x_sin":
        expr = x ** p["m"] * sp.sin(p["a"] * x)
    else:
        expr = x ** p["m"] * (1 - sp.cos(p["a"] * x))
    lead = sp.series(expr, x, 0, 12).removeO()
    order = min(m[0] for m in sp.Poly(lead, x).monoms())
    lim = sp.limit(expr / x ** order, x, 0)        # finite and not 0: really that order
    assert lim.is_finite and lim != 0
    return [Fraction(int(order))]


_VCB = {"sin": lambda c: sp.sin(c * x), "tan": lambda c: sp.tan(c * x), "ln": lambda c: sp.log(1 + c * x),
        "exp": lambda c: sp.exp(c * x) - 1, "arcsin": lambda c: sp.asin(c * x)}


def _vcb_thay(p: dict) -> list[Fraction]:
    if p["kind"] == "first":
        expr = _VCB[p["f"]](p["a"]) / _VCB[p["g"]](p["b"])
    else:
        b = p["b"]
        den = {"x^2": b * x ** 2, "x sin": x * sp.sin(b * x), "x ln": x * sp.log(1 + b * x)}[p["g"]]
        expr = (1 - sp.cos(p["a"] * x)) / den
    return [_frac(sp.limit(expr, x, 0))]


# ------------------------------------------------------------------ floor 3
_h = sp.Symbol("h", positive=True)


def _limit_both(expr, at) -> tuple:
    """(left limit, right limit) at `at`: x = at - h and x = at + h with h -> 0+. Substituting
    first lets a Piecewise settle on its branch (sympy's limit of a Piecewise is not reliable)."""
    return (sp.limit(sp.piecewise_fold(expr.subs(x, at - _h)), _h, 0, "+"),
            sp.limit(sp.piecewise_fold(expr.subs(x, at + _h)), _h, 0, "+"))


def _lien_tuc_tf(p: dict) -> bool:
    f = _poly(p["top"]) / (x - p["x0"])
    left, right = _limit_both(f, p["x0"])
    return left == right == p["value"]


def _thac_trien(p: dict) -> list[Fraction]:
    f = p["c"] * (x ** p["n"] - sp.Integer(p["r"]) ** p["n"]) / (x - p["r"])
    left, right = _limit_both(f, p["r"])
    assert left == right
    return [_frac(left)]


def _piecewise(left, right, c) -> sp.Piecewise:
    return sp.Piecewise((left, x < c), (right, True))


def _mot_phia(p: dict) -> list[Fraction]:
    f = _piecewise(p["left"][0] * x + p["left"][1], p["right"][0] * x ** 2 + p["right"][1], p["c"])
    return [_frac(v) for v in _limit_both(f, p["c"])]


def _tri_tuyet_doi(p: dict) -> list[Fraction]:
    f = p["k"] * sp.Abs(x - p["c"]) * (x + p["p"]) / (x - p["c"])
    return [_frac(v) for v in _limit_both(f, p["c"])]


def _tham_so(p: dict) -> list[Fraction]:
    m = sp.Symbol("m")
    f = _poly(p["top"]) / (x - p["x0"])
    left, right = _limit_both(f, p["x0"])
    assert left == right
    return [_frac(sp.solve(sp.Eq(m, left), m)[0])]


def _tham_so_hai_nhanh(p: dict) -> list[Fraction]:
    m = sp.Symbol("m")
    f = _piecewise(p["p"] * x + p["q"], m * x ** 2 + p["t"], p["c"])
    left, right = _limit_both(f, p["c"])
    return [_frac(sp.solve(sp.Eq(left, right), m)[0])]


def _buoc_nhay(p: dict) -> list[Fraction]:
    f = _piecewise(p["left"][0] * x + p["left"][1], p["right"][0] * x + p["right"][1], p["c"])
    left, right = _limit_both(f, p["c"])
    return [_frac(right - left)]


def _khu_duoc(p: dict) -> list[Fraction]:
    f = _poly(p["top"]) / _poly(p["bottom"])
    poles = sp.solve(_poly(p["bottom"]), x)
    removable = []
    for a in poles:
        left, right = _limit_both(f, a)
        if left.is_finite and left == right:
            removable.append((a, left))
    assert len(poles) == 2 and len(removable) == 1
    return [_frac(removable[0][0]), _frac(removable[0][1])]


def _cubic_root(p: dict):
    roots = sp.real_roots(_poly([1, 0, p["a"], p["b"]]))
    assert len(roots) == 1
    return roots[0]


def _doi_dau(p: dict) -> bool:
    root = _cubic_root(p)
    return bool(p["u"] < root < p["u"] + 1)


EXPECTED: dict = {
    # ---- floor 1
    "gt_g1_gia_tri": lambda p: [_frac(_poly(p["coeffs"]).subs(x, p["x"]))],
    "gt_g1_khong_xac_dinh": lambda p: [_frac(v) for v in sp.solve(_poly(p["den"]), x)],
    "gt_g1_chan_le": _chan_le,
    "gt_g1_chu_ky": _chu_ky,
    "gt_g1_hop_gia_tri": _hop_gia_tri,
    "gt_g1_hop_he_so": _hop_he_so,
    "gt_g1_nguoc_bac_nhat": _nguoc_bac_nhat,
    "gt_g1_nguoc_phan_thuc": _nguoc_phan_thuc,
    "gt_g1_logarit": lambda p: [_frac(sp.log(sp.Rational(*p["n"]), p["base"]))],
    "gt_g1_pt_logarit": lambda p: [_frac(v) for v in sp.solve(sp.Eq(sp.log(x + p["p"], p["base"]), p["k"]), x)],
    # ---- floor 2
    "gt_g2_day_huu_ty": lambda p: [_frac(sp.limit(_poly(p["top"], n) / _poly(p["bottom"], n), n, sp.oo))],
    "gt_g2_day_mu": _day_mu,
    "gt_g2_thay_so": lambda p: [_frac(sp.limit((p["a"] * x ** 2 + p["b"]) / (p["c"] * x + p["d"]), x, p["x0"]))],
    "gt_g2_khu_00": lambda p: [_frac(sp.limit(_poly(p["top"]) / _poly(p["bottom"]), x, p["x0"]))],
    "gt_g2_vo_cuc_huu_ty": _vo_cuc,
    "gt_g2_can_lien_hop": lambda p: [_frac(sp.limit(sp.sqrt(p["a"] ** 2 * x ** 2 + p["b"] * x + p["c"]) - p["a"] * x,
                                                    x, sp.oo))],
    "gt_g2_sin_x": _sin_x,
    "gt_g2_mu_e": _mu_e,
    "gt_g2_vcb_cap": _vcb_cap,
    "gt_g2_vcb_thay": _vcb_thay,
    # ---- floor 3
    "gt_g3_lien_tuc_tf": _lien_tuc_tf,
    "gt_g3_thac_trien": _thac_trien,
    "gt_g3_mot_phia": _mot_phia,
    "gt_g3_tri_tuyet_doi": _tri_tuyet_doi,
    "gt_g3_tham_so": _tham_so,
    "gt_g3_tham_so_hai_nhanh": _tham_so_hai_nhanh,
    "gt_g3_buoc_nhay": _buoc_nhay,
    "gt_g3_khu_duoc": _khu_duoc,
    "gt_g3_doi_dau": _doi_dau,
    "gt_g3_khoang_nghiem": lambda p: [Fraction(int(sp.floor(_cubic_root(p))))],
}
