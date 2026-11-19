"""The sympy recomputation of every generator of Đại Số Tuyến Tính, floors 4-6 (M11 round 2):
generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a true_false
question, or a list of Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED.
This module must not import math_verify (it is imported by it).

Each answer is worked out by another route than the generator's own list arithmetic: products
with sympy Matrix (and sizes from products of zero matrices), row operations as elementary
matrices, systems with linsolve, the number of solutions from linsolve's answer set, free
variables from nullspace, determinants with Matrix.det (Bareiss) and Matrix.cofactor,
unknowns with solve, ranks with Matrix.rank, inverses with Matrix.inv."""
from __future__ import annotations

from fractions import Fraction

import sympy as sp
from sympy import Matrix

x, y, z, X = sp.symbols("x y z X")


def _frac(v) -> Fraction:
    v = sp.nsimplify(sp.simplify(v))
    if not v.is_rational:
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _rows(m: Matrix) -> list[Fraction]:
    return [_frac(m[r, c]) for r in range(m.rows) for c in range(m.cols)]


def _only_solution(a: Matrix, b: Matrix) -> list[Fraction]:
    sols = list(sp.linsolve((a, b), *sp.symbols(f"v0:{a.cols}")))
    if len(sols) != 1 or any(v.free_symbols for v in sols[0]):
        raise ValueError(f"the system has no unique solution: {sols}")
    return [_frac(v) for v in sols[0]]


# ------------------------------------------------------------------ floor 4
def _co_tich_ba(p: dict) -> list[Fraction]:
    a, b, c = sp.zeros(p["m"], p["n"]), sp.zeros(p["n"], p["p"]), sp.zeros(p["p"], p["q"])
    prod = a * b * c if p["order"] == "ABC" else c.T * b.T * a.T
    return [Fraction(prod.rows), Fraction(prod.cols)]


def _nhan_duoc(p: dict) -> bool:
    try:
        sp.zeros(*p["a"]) * sp.zeros(*p["b"])
    except sp.ShapeError:
        return False
    return True


def _luy_thua_n(p: dict) -> list[Fraction]:
    a = Matrix([[1, p["a"]], [0, 1]]) if p["kind"] == "upper" else Matrix([[1, 0], [p["a"], 1]])
    power = a ** p["n"]
    return [_frac(power[0, 1] if p["kind"] == "upper" else power[1, 0])]


# ------------------------------------------------------------------ floor 5
def _cong_boi_hang(p: dict) -> list[Fraction]:
    e = sp.eye(3)
    e[p["i"] - 1, p["j"] - 1] = p["k"]               # the elementary matrix of R_i <- R_i + k R_j
    return [_frac(v) for v in (e * Matrix(p["a"])).row(p["i"] - 1)]


def _so_nghiem(p: dict) -> bool:
    m = Matrix(p["rows"])
    sols = sp.linsolve((m[:, :3], m[:, 3]), x, y, z)
    if sols == sp.EmptySet:
        kind = "none"
    else:
        kind = "many" if any(v.free_symbols for v in next(iter(sols))) else "unique"
    return kind == p["claim"]


def _tham_so(p: dict) -> list[Fraction]:
    m = sp.Symbol("m")
    values = sp.solve(Matrix([[p["p"], p["q"]], [p["r"], m]]).det(), m)
    return [_frac(v) for v in values]


def _an_tu_do(p: dict) -> list[Fraction]:
    return [Fraction(len(Matrix(p["a"]).nullspace()))]


# ------------------------------------------------------------------ floor 6
def _tim_x_det(p: dict) -> list[Fraction]:
    m = Matrix([[X if v == "x" else v for v in row] for row in p["rows"]])
    return [_frac(v) for v in sp.solve(sp.Eq(m.det(), p["target"]), X)]


def _khai_trien_4(p: dict) -> list[Fraction]:
    return [_frac(Matrix(p["a"]).det(method="berkowitz"))]


def _tinh_chat(p: dict) -> list[Fraction]:
    n, d = p["n"], p["d"]
    a = sp.diag(d, *([1] * (n - 1)))                    # a concrete matrix with det A = d
    b = sp.diag(p["e"], *([1] * (n - 1)))
    m = {"kA": p["k"] * a, "AT": a.T, "A2": a * a, "inv": a.inv(), "neg": -a, "AB": a.T * b}[p["kind"]]
    return [_frac(m.det())]


def _cramer(p: dict) -> list[Fraction]:
    sol = _only_solution(Matrix(p["a"]), Matrix(p["b"]))
    return [sol[0] if p["which"] == "x" else sol[1]]


EXPECTED = {
    # ---- floor 4
    "dstt_g4_tich_vo_huong": lambda p: [_frac((Matrix([p["u"]]) * Matrix(p["v"]))[0, 0])],
    "dstt_g4_nhan_duoc": _nhan_duoc,
    "dstt_g4_co_tich_ba": _co_tich_ba,
    "dstt_g4_phan_tu_tich": lambda p: [_frac((Matrix(p["a"]) * Matrix(p["b"]))[p["i"] - 1, p["j"] - 1])],
    "dstt_g4_tich_2x2": lambda p: _rows(Matrix(p["a"]) * Matrix(p["b"])),
    "dstt_g4_giao_hoan": lambda p: (Matrix(p["a"]) * Matrix(p["b"]) - Matrix(p["b"]) * Matrix(p["a"])).is_zero_matrix,
    "dstt_g4_chuyen_vi_tich": lambda p: [_frac((Matrix(p["b"]).T * Matrix(p["a"]).T)[p["i"] - 1, p["j"] - 1])],
    "dstt_g4_binh_phuong": lambda p: _rows(Matrix(p["a"]) ** 2),
    "dstt_g4_luy_thua_n": _luy_thua_n,
    # ---- floor 5
    "dstt_g5_tim_b": lambda p: [_frac(v) for v in sum((p["x"][k] * Matrix(p["a"]).col(k) for k in range(3)),
                                                      sp.zeros(3, 1))],
    "dstt_g5_cong_boi_hang": _cong_boi_hang,
    "dstt_g5_giai_he_2": lambda p: _only_solution(Matrix(p["a"]), Matrix(p["b"])),
    "dstt_g5_giai_he_3": lambda p: _only_solution(Matrix(p["a"]), Matrix(p["b"])),
    "dstt_g5_so_nghiem": _so_nghiem,
    "dstt_g5_tham_so": _tham_so,
    "dstt_g5_tam_thuong": lambda p: not Matrix(p["a"]).nullspace(),
    "dstt_g5_an_tu_do": _an_tu_do,
    # ---- floor 6
    "dstt_g6_dinh_thuc_3": lambda p: [_frac(Matrix(p["a"]).det())],
    "dstt_g6_tim_x_det": _tim_x_det,
    "dstt_g6_phan_bu": lambda p: [_frac(Matrix(p["a"]).cofactor(p["i"] - 1, p["j"] - 1))],
    "dstt_g6_khai_trien_4": _khai_trien_4,
    "dstt_g6_tinh_chat": _tinh_chat,
    "dstt_g6_hang": lambda p: [Fraction(Matrix(p["a"]).rank())],
    "dstt_g6_nghich_dao_2": lambda p: _rows(Matrix(p["a"]).inv()),
    "dstt_g6_kha_nghich": lambda p: Matrix(p["a"]).rank() == 3,
    "dstt_g6_cramer": _cramer,
    "dstt_g6_giai_he_nd": lambda p: _only_solution(Matrix(p["a"]), Matrix(p["b"])),
}
