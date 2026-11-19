"""The sympy recomputation of every generator of Đại Số Tuyến Tính, floors 7-9 (M11 round 2):
generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a true_false
question, or a list of Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED.
This module must not import math_verify (it is imported by it).

Each answer is worked out by another route than the generator, which only knows how it built
its numbers: membership in a span by solving det = 0 for the unknown, independence from
nullspace, dimension from columnspace, coordinates with LUsolve, images through the inverse of
the basis matrix, kernels from nullspace, matrices of maps by symbolic substitution, a change
of basis by solving P B = A P, eigenvalues with eigenvals, diagonalisability with
is_diagonalizable, powers directly, Gram-Schmidt with sympy's GramSchmidt, definiteness with
is_positive_definite (Cholesky-type test) and projections as a sum over an orthonormal basis."""
from __future__ import annotations

from fractions import Fraction

import sympy as sp
from sympy import Matrix

x, y, z, M = sp.symbols("x y z M")


def _frac(v) -> Fraction:
    v = sp.nsimplify(sp.simplify(v))
    if not v.is_rational:
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _rows(m: Matrix) -> list[Fraction]:
    return [_frac(m[r, c]) for r in range(m.rows) for c in range(m.cols)]


def _cols(vectors) -> Matrix:
    return Matrix.hstack(*[Matrix(v) for v in vectors])


# ------------------------------------------------------------------ floor 7
def _to_hop(p: dict) -> list[Fraction]:
    w = list(p["w12"]) + [M]
    sol = sp.solve(sp.Eq(_cols([p["u"], p["v"], w]).det(), 0), M)
    if len(sol) != 1:
        raise ValueError(f"no single m: {sol}")
    return [_frac(sol[0])]


def _toa_do(p: dict) -> list[Fraction]:
    return [_frac(v) for v in _cols(p["basis"]).LUsolve(Matrix(p["x"]))]


# ------------------------------------------------------------------ floor 8
def _anh_vecto(p: dict) -> list[Fraction]:
    a = _cols([p["p"], p["q"]]) * _cols([p["b1"], p["b2"]]).inv()      # the standard matrix of f
    return [_frac(v) for v in a * Matrix(p["v"])]


def _so_chieu_nhan(p: dict) -> list[Fraction]:
    a = Matrix(p["a"])
    kernel = len(a.nullspace())
    return [Fraction(kernel if p["which"] == "ker" else a.cols - kernel)]


def _ma_tran_co_so(p: dict) -> list[Fraction]:
    f = Matrix(p["f"]) * Matrix([x, y, z])
    cols = [f.subs({x: b[0], y: b[1], z: b[2]}) for b in p["basis"]]
    return _rows(Matrix.hstack(*cols))


def _hop(p: dict) -> list[Fraction]:
    f = Matrix(p["f"]) * Matrix([x, y])
    g = Matrix(p["g"]) * Matrix([x, y])
    first, second = (f, g) if p["order"] == "gf" else (g, f)
    composed = second.subs({x: first[0], y: first[1]}, simultaneous=True)
    return _rows(composed.jacobian([x, y]))


def _doi_co_so(p: dict) -> list[Fraction]:
    a, pm = Matrix(p["a"]), Matrix(p["p"])
    bs = sp.symbols("b0:4")
    b = Matrix(2, 2, bs)
    sol = sp.solve(list(pm * b - a * pm), bs, dict=True)[0]
    return _rows(b.subs(sol))


# ------------------------------------------------------------------ floor 9
def _tri_rieng(p: dict) -> list[Fraction]:
    vals = Matrix(p["a"]).eigenvals()
    if sum(vals.values()) != 3 or len(vals) != 3:
        raise ValueError(f"not three distinct eigenvalues: {vals}")
    return [_frac(v) for v in vals]


def _gram_schmidt(p: dict) -> list[Fraction]:
    vs = sp.GramSchmidt([Matrix(u) for u in p["u"]])
    return [_frac(v) for v in vs[2]]


def _chieu(p: dict) -> list[Fraction]:
    e = sp.GramSchmidt([Matrix(p["a1"]), Matrix(p["a2"])], True)
    b = Matrix(p["b"])
    proj = sum(((b.dot(q)) * q for q in e), sp.zeros(3, 1))
    return [_frac(v) for v in proj]


EXPECTED = {
    # ---- floor 7
    "dstt_g7_to_hop": _to_hop,
    "dstt_g7_doc_lap": lambda p: not _cols([p["u"], p["v"], p["w"]]).nullspace(),
    "dstt_g7_so_chieu": lambda p: [Fraction(len(_cols(p["vectors"]).columnspace()))],
    "dstt_g7_toa_do": _toa_do,
    # ---- floor 8
    "dstt_g8_anh_vecto": _anh_vecto,
    "dstt_g8_so_chieu_nhan": _so_chieu_nhan,
    "dstt_g8_ma_tran_co_so": _ma_tran_co_so,
    "dstt_g8_hop": _hop,
    "dstt_g8_doi_co_so": _doi_co_so,
    # ---- floor 9
    "dstt_g9_tri_rieng": _tri_rieng,
    "dstt_g9_cheo_hoa": lambda p: Matrix(p["a"]).is_diagonalizable(reals_only=True),
    "dstt_g9_luy_thua": lambda p: [_frac((Matrix(p["a"]) ** p["n"])[p["i"] - 1, p["j"] - 1])],
    "dstt_g9_gram_schmidt": _gram_schmidt,
    "dstt_g9_xac_dinh": lambda p: bool(Matrix(p["a"]).is_positive_definite),
    "dstt_g9_chieu": _chieu,
}
