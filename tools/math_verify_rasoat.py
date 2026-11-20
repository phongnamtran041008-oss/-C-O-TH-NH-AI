"""The sympy recomputation of the generators the curriculum review added (rsdstt_floor1.py,
rsgt_floor1.py, rstr_floor1.py, rsxs_floor1.py): generator id -> a function of the drawn numbers
(`Draw.params`) giving a bool for a true_false question or a list of Fractions for a numeric one.
Merged into tools/math_verify.py EXPECTED. This module must not import math_verify.

Each answer is found another way than the generator found it: sympy Matrix products, rank and
nullspace, solve and integrate, a generating polynomial for a sample mean, an explicit stack for
DFS, Floyd-Warshall for BFS, powers of (I + A) for connectivity, the log-likelihood differentiated
symbolically, itertools for a place in the lexicographic list, bisection for "smallest n"."""
from __future__ import annotations

import itertools
import statistics
from fractions import Fraction

import sympy as sp
from sympy import Matrix, Rational, Symbol

x, y, z, t = sp.symbols("x y z t", real=True)


def _frac(v) -> Fraction:
    v = sp.simplify(sp.sympify(v))
    if not v.is_Rational:
        v = sp.nsimplify(v)
    if not v.is_rational:
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _rows(m: Matrix) -> list[Fraction]:
    return [_frac(m[r, c]) for r in range(m.rows) for c in range(m.cols)]


def _r(v) -> sp.Rational:
    return Rational(str(v))


def _least(pred, lo: int = 1, hi: int = 10 ** 7) -> int:
    """The smallest n in lo..hi with pred(n) true, pred being monotone (false then true)."""
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# ------------------------------------------------------------------ Đại Số Tuyến Tính
def _in_w(p: dict, v: tuple) -> bool:
    k, a, b, c = p["kind"], p["a"], p["b"], p["c"]
    if k == "line":
        return a * v[0] + b * v[1] == 0
    if k == "shifted":
        return a * v[0] + b * v[1] == c
    if k == "product":
        return v[0] * v[1] == 0
    if k == "halfplane":
        return v[0] >= 0
    if k == "plane3":
        return a * v[0] + b * v[1] - c * v[2] == 0
    if k == "shifted3":
        return v[0] + v[1] + v[2] == c
    return v[1] == v[0] ** 2                                   # "square"


def _is_subspace(p: dict) -> bool:
    dim = 3 if p["kind"] in ("plane3", "shifted3") else 2
    if not _in_w(p, (0,) * dim):
        return False
    grid = [v for v in itertools.product(range(-6, 7), repeat=dim) if _in_w(p, v)]
    for u in grid:
        for s in (-1, 2, 3):
            if not _in_w(p, tuple(s * c for c in u)):
                return False
    for u, v in itertools.product(grid[:60], repeat=2):
        if not _in_w(p, tuple(a + b for a, b in zip(u, v))):
            return False
    return True


def _in_span(p: dict) -> list[Fraction]:
    m = Symbol("m")
    det = Matrix([p["u"], p["v"], [p["w1"], m, p["w3"]]]).det()
    return [_frac(sol) for sol in sp.solve(det, m)]


def _coords(p: dict) -> list[Fraction]:
    pb = Matrix([p["b1"], p["b2"]]).T
    pc = Matrix([p["c1"], p["c2"]]).T
    return [_frac(v) for v in pc.inv() * (pb * Matrix([p["p"], p["q"]]))]


def _so_chieu(p: dict) -> list[Fraction]:
    ker, im, n = sp.symbols("ker im n")
    eq = sp.Eq(ker + im, n)
    known = {"ker": {n: p["n"], im: p["r"]}, "im": {n: p["n"], ker: p["n"] - p["r"]},
             "n": {ker: p["n"] - p["r"], im: p["r"]}}[p["ask"]]
    target = {"ker": ker, "im": im, "n": n}[p["ask"]]
    return [_frac(sp.solve(eq.subs(known), target)[0])]


# ------------------------------------------------------------------ Giải Tích
def _gt_hai_lan(p: dict) -> list[Fraction]:
    c1, c2 = sp.symbols("c1 c2")
    fp = sp.integrate(p["a"] * x + p["b"], x) + c1
    fp = fp.subs(c1, sp.solve(fp.subs(x, 1) - p["c"], c1)[0])
    f = sp.integrate(fp, x) + c2
    f = f.subs(c2, sp.solve(f.subs(x, 0) - p["d"], c2)[0])
    return [_frac(f.subs(x, 2))]


def _gt_doi_bien(p: dict) -> list[Fraction]:
    c, big = p["c"], p["big"]
    f = x * (x ** 2 + c) ** p["k"] if p["kind"] == "luy_thua" else x / (x ** 2 + c) ** 2
    return [_frac(sp.integrate(f, (x, 0, big)))]


def _gt_can(p: dict) -> list[Fraction]:
    big_f = sp.integrate(t ** 2 + p["a"] * t + p["b"], (t, x, x ** 2))
    return [_frac(sp.diff(big_f, x).subs(x, p["x0"]))]


def _gt_suy_rong(p: dict) -> list[Fraction]:
    if p["kind"] == "luy_thua":
        return [_frac(sp.integrate(p["c"] / x ** p["p"], (x, p["a"], sp.oo)))]
    return [_frac(sp.integrate((p["A"] * x + p["B"]) * sp.exp(-p["k"] * x), (x, 0, sp.oo)))]


# ------------------------------------------------------------------ Thuật Toán và Tối Ưu
def _adj(p: dict) -> Matrix:
    n = p["n"]
    m = sp.zeros(n, n)
    for a, b in p["edges"]:
        m[a - 1, b - 1] = m[b - 1, a - 1] = 1
    return m


def _tr_danh_sach_ke(p: dict) -> list[Fraction]:
    m = _adj(p)
    ask = p["ask"]
    if ask == "edges":
        return [_frac(sum(m) / 2)]
    if ask == "maxdeg":
        return [_frac(max(sum(m.row(i)) for i in range(m.rows)))]
    return [_frac(sum(m))]


def _tr_lien_thong(p: dict) -> list[Fraction]:
    n = p["n"]
    reach = (sp.eye(n) + _adj(p)) ** n                       # entry > 0 iff there is a walk of length <= n
    classes = {tuple(1 if reach[i, j] > 0 else 0 for j in range(n)) for i in range(n)}
    return [Fraction(len(classes) if p["ask"] == "count" else len(classes) - 1)]


def _floyd(p: dict) -> list[list[float]]:
    n = p["n"]
    inf = 10 ** 6
    d = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for a, b in p["edges"]:
        d[a - 1][b - 1] = d[b - 1][a - 1] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def _tr_bfs(p: dict) -> list[Fraction]:
    d = _floyd(p)
    if p["ask"] == "to":
        return [Fraction(d[p["src"] - 1][p["target"] - 1])]
    return [Fraction(sum(1 for v in range(p["n"]) if d[p["src"] - 1][v] == p["d"]))]


def _tr_dfs(p: dict) -> list[Fraction]:
    adj: dict[int, list[int]] = {v: [] for v in range(1, p["n"] + 1)}
    for a, b in p["edges"]:
        adj[a].append(b)
        adj[b].append(a)
    stack, seen, order = [1], set(), []
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(u)
        stack.extend(sorted(adj[u], reverse=True))
    return [Fraction(v) for v in order]


def _tr_cay(p: dict) -> list[Fraction]:
    if p["kind"] == "rung":
        return [Fraction(p["n"] - p["k"])]
    leaves = Symbol("leaves")
    sol = sp.solve(3 * p["a"] + 4 * p["b"] + 2 * p["c"] + leaves - 2 * (p["n"] - 1), leaves)
    assert sol[0] == p["n"] - p["a"] - p["b"] - p["c"]       # the vertex count agrees
    return [_frac(sol[0])]


# ------------------------------------------------------------------ Xác Suất và Thống Kê
def _xs_mau(p: dict) -> list[Fraction]:
    poly = sp.Poly(sp.expand(sum(x ** v for v in p["values"]) ** 2), x)
    need = 2 * _r(p["m"])
    good = sum(c for (e,), c in poly.terms() if e >= need)
    return [_frac(Rational(good, 9))]


def _xs_thieu(p: dict) -> list[Fraction]:
    n, mean = p["n"], p["mean"]
    missing = n * mean - sum(p["data"])
    s2 = statistics.variance([Fraction(v) for v in p["data"] + [missing]])      # exact Fraction
    return [Fraction(missing), Fraction(s2)]


def _xs_phan_phoi(p: dict) -> list[Fraction]:
    if p["kind"] == "n":
        n = Symbol("n", positive=True)
        return [_frac(sp.solve(sp.Eq(_r(p["sigma"]) / sp.sqrt(n), _r(p["d"])), n)[0])]
    return [_frac(Rational(p["var"], p["n"]))]


def _xs_khong_chech(p: dict) -> list[Fraction]:
    c = Symbol("c")
    cv = sp.solve(_r(p["a"]) + _r(p["b"]) + c - 1, c)[0]
    var = sum(w ** 2 for w in (_r(p["a"]), _r(p["b"]), cv)) * p["sigma2"]
    return [_frac(cv), _frac(var)]


def _xs_hop_ly(p: dict) -> list[Fraction]:
    lam = Symbol("lam", positive=True)
    if p["kind"] == "poisson":
        ll = sum(-lam + v * sp.log(lam) for v in p["data"])
    elif p["kind"] == "mu":
        ll = sum(sp.log(lam) - lam * v for v in p["data"])
    else:
        lam = Symbol("lam", positive=True)
        ll = sum(v * sp.log(lam) + (p["trials"] - v) * sp.log(1 - lam) for v in p["data"])
    return [_frac(sp.solve(sp.diff(ll, lam), lam)[0])]


def _xs_tin_cay_n(p: dict) -> list[Fraction]:
    n = Symbol("n", positive=True)
    eps = (_r(p["hi"]) - _r(p["lo"])) / 2
    return [_frac(sp.solve(sp.Eq(eps, _r(p["z"]) * _r(p["sigma"]) / sp.sqrt(n)), n)[0])]


def _xs_ty_le(p: dict) -> list[Fraction]:
    return [_frac((_r(p["lo"]) + _r(p["hi"])) / 2 * p["n"])]


def _xs_co_mau(p: dict) -> list[Fraction]:
    z2, eps = _r(p["z"]) ** 2, _r(p["eps"])
    return [Fraction(_least(lambda n: z2 / (4 * n) <= eps ** 2))]


def _xs_chebyshev(p: dict) -> list[Fraction]:
    s2, eps, delta = Rational(p["sigma2"]), _r(p["eps"]), _r(p["delta"])
    return [Fraction(_least(lambda n: s2 / (n * eps ** 2) <= delta))]


def _xs_clt(p: dict) -> list[Fraction]:
    return [_frac(p["n"] * p["mu"] + _r(p["z"]) * p["sigma"] * sp.sqrt(p["n"]))]


EXPECTED = {
    # ---- Đại Số Tuyến Tính
    "dstt_gx_tvh_tim_m": lambda p: [_frac(sp.solve(Symbol("m") * p["c"] + p["a"] * p["d"] + p["b"] * p["e"] - p["k"],
                                                   Symbol("m"))[0])],
    "dstt_gx_ab_tru_ba": lambda p: [_frac((Matrix(p["a"]) * Matrix(p["b"]) - Matrix(p["b"]) * Matrix(p["a"]))[
        p["i"] - 1, p["j"] - 1])],
    "dstt_gx_con_khong_gian": _is_subspace,
    "dstt_gx_thuoc_bao_tuyen_tinh": _in_span,
    "dstt_gx_toa_do_doi_co_so": _coords,
    "dstt_gx_doi_co_so_ma_tran": lambda p: _rows(Matrix(p["p"]).inv() * Matrix(p["a"]) * Matrix(p["p"])),
    "dstt_gx_hop_anh_xa_gia_tri": lambda p: [_frac(v) for v in Matrix(p["ag"]) * Matrix(p["af"]) * Matrix([p["p"], p["q"]])],
    "dstt_gx_nhan_va_anh": lambda p: [Fraction(len(Matrix(p["m"]).nullspace())),
                                      Fraction(len(Matrix(p["m"]).columnspace()))],
    "dstt_gx_so_chieu_nhan": _so_chieu,
    # ---- Giải Tích
    "gt_gx_nguyen_ham_hai_lan": _gt_hai_lan,
    "gt_gx_doi_bien_phan_thuc": _gt_doi_bien,
    "gt_gx_can_bien_thien_chuoi": _gt_can,
    "gt_gx_suy_rong_nua_truc": _gt_suy_rong,
    # ---- Thuật Toán và Tối Ưu
    "tr_gx_hoan_vi_thu_may": lambda p: [Fraction(sorted(itertools.permutations(range(1, p["n"] + 1))).index(
        tuple(p["perm"])) + 1)],
    "tr_gx_danh_sach_ke_dem": _tr_danh_sach_ke,
    "tr_gx_thanh_phan_lien_thong": _tr_lien_thong,
    "tr_gx_bfs_khoang_cach": _tr_bfs,
    "tr_gx_dfs_thu_tu": _tr_dfs,
    "tr_gx_cay_dem_la": _tr_cay,
    "tr_gx_ham_loi_hesse": lambda p: bool(Matrix([[2 * p["a"], p["b"]], [p["b"], 2 * (p["c"])]]).is_positive_semidefinite),
    # ---- Xác Suất và Thống Kê
    "xs_gx_rut_mau_cung_nhan": lambda p: [_frac(sp.binomial(p["good"], p["k"]) / sp.binomial(p["good"] + p["bad"], p["k"]))],
    "xs_gx_it_nhat_mot": lambda p: [_frac(1 - (1 - _r(p["miss"])) ** p["n"])],
    "xs_gx_mau_co_hoan_lai": _xs_mau,
    "xs_gx_gia_tri_thieu": _xs_thieu,
    "xs_gx_phan_phoi_trung_binh_mau": _xs_phan_phoi,
    "xs_gx_uoc_luong_khong_chech_trong_so": _xs_khong_chech,
    "xs_gx_hop_ly_tu_so_lieu": _xs_hop_ly,
    "xs_gx_tin_cay_tim_n": _xs_tin_cay_n,
    "xs_gx_tin_cay_ty_le_nguoc": _xs_ty_le,
    "xs_gx_co_mau_xau_nhat": _xs_co_mau,
    "xs_gx_chebyshev_tim_n": _xs_chebyshev,
    "xs_gx_clt_nguong": _xs_clt,
}
