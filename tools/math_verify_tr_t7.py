"""The recomputation of every generator of Tối Ưu và Toán Rời Rạc, floors 7-9 (M11, second
round): generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a
true_false question, or a list of Fractions for a numeric one. Merged into tools/math_verify.py
EXPECTED. This module must not import math_verify (it is imported by it).

The generators solve their instances the way the floors teach (Kruskal with union-find, Prim,
Dijkstra, augmenting paths, closed formulas, Cramer's rule, the vertices of the feasible
polygon, one simplex pivot, complementary slackness, the Lagrange system by hand). Here every
answer is found another way: sympy equations for the handshake count, the rank of the
incidence matrix for a spanning forest, the matrix-tree theorem, every spanning tree, every
simple path and Floyd-Warshall for distances, every s-t cut for a maximum flow, sympy diff /
solve / hessian / eigenvals / solveset for calculus and convexity, sympy's own simplex
(lpmax, lpmin) for linear programmes and duals, a tableau pivot with sympy matrices, and
gradient steps redone with diff and Rationals."""
from __future__ import annotations

import itertools
from fractions import Fraction

import sympy as sp
from sympy.solvers.simplex import lpmax, lpmin

X, Y, LAM = sp.symbols("x y lambda", real=True)


def _fr(v) -> Fraction:
    v = sp.nsimplify(v)
    return Fraction(int(v.p), int(v.q))


def _list(*vals) -> list[Fraction]:
    return [_fr(v) for v in vals]


def _rat(text) -> sp.Rational:
    return sp.Rational(str(text))


# ------------------------------------------------------------------ floor 7: trees and graphs
def _leaves(p: dict) -> list[Fraction]:
    if p["kind"] == "rung":
        # build one such forest (a path through n - k + 1 vertices, the others alone), check it
        # has k components and no cycle from the rank of its incidence matrix, count its edges
        n, k = p["n"], p["k"]
        edges = [(v, v + 1) for v in range(1, n - k + 1)]
        rank = _incidence_rank(n, edges)
        assert rank == len(edges) and n - rank == k
        return _list(len(edges))
    L = sp.Symbol("L", positive=True)
    inner = p["c2"] + p["c3"] + p["c4"]
    degree_sum = 2 * p["c2"] + 3 * p["c3"] + 4 * p["c4"] + L
    leaves = sp.solve(sp.Eq(degree_sum, 2 * (inner + L - 1)), L)[0]
    return _list(leaves if p["kind"] == "la" else inner + leaves)


def _incidence_rank(n: int, edges) -> int:
    """Rank of the oriented incidence matrix (n - number of components of the subgraph), by
    Gaussian elimination over the rationals (sympy's rank is too slow for every 6-edge subset)."""
    rows = [[Fraction(0)] * len(edges) for _ in range(n)]
    for j, (u, v) in enumerate(edges):
        rows[u - 1][j], rows[v - 1][j] = Fraction(1), Fraction(-1)
    rank, col = 0, 0
    while rank < n and col < len(edges):
        pivot = next((r for r in range(rank, n) if rows[r][col] != 0), None)
        if pivot is None:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(n):
            if r != rank and rows[r][col] != 0:
                k = rows[r][col] / rows[rank][col]
                rows[r] = [a - k * b for a, b in zip(rows[r], rows[rank])]
        rank, col = rank + 1, col + 1
    return rank


def _cycle_rank(p: dict) -> list[Fraction]:
    return _list(len(p["edges"]) - _incidence_rank(p["n"], p["edges"]))


def _kirchhoff(p: dict) -> list[Fraction]:
    n = p["n"]
    lap = sp.zeros(n, n)
    for u, v in p["edges"]:
        lap[u - 1, v - 1] -= 1
        lap[v - 1, u - 1] -= 1
        lap[u - 1, u - 1] += 1
        lap[v - 1, v - 1] += 1
    return _list(lap[1:, 1:].det())


def _all_spanning_trees(n: int, wedges) -> list[tuple]:
    """Every set of n - 1 edges whose incidence matrix has rank n - 1 (no cycle, so a tree)."""
    out = []
    for sub in itertools.combinations([tuple(e) for e in wedges], n - 1):
        if _incidence_rank(n, [(u, v) for u, v, _ in sub]) == n - 1:
            out.append(sub)
    return out


def _mst(n: int, wedges) -> tuple:
    trees = _all_spanning_trees(n, wedges)
    weights = [sum(w for _, _, w in t) for t in trees]
    best = min(weights)
    assert weights.count(best) == 1, "the minimum spanning tree is not unique"
    return trees[weights.index(best)]


def _mst_total(p: dict) -> list[Fraction]:
    return _list(sum(w for _, _, w in _mst(p["n"], p["wedges"])))


def _mst_total_and_heaviest(p: dict) -> list[Fraction]:
    tree = _mst(p["n"], p["wedges"])
    return _list(sum(w for _, _, w in tree), max(w for _, _, w in tree))


def _prim_order(p: dict) -> list[Fraction]:
    """O(n^2) Prim with a weight matrix and key labels; its edges must be the brute-force MST."""
    n, s = p["n"], p["start"]
    inf = sp.oo
    w = sp.Matrix(n, n, lambda i, j: inf)
    for u, v, c in p["wedges"]:
        w[u - 1, v - 1] = w[v - 1, u - 1] = c
    key = {v: w[s - 1, v - 1] for v in range(1, n + 1)}
    parent = {v: s for v in range(1, n + 1)}
    order, inside, used = [s], {s}, set()
    for _ in range(n - 1):
        v = min((x for x in key if x not in inside), key=lambda x: key[x])
        inside.add(v)
        order.append(v)
        used.add((min(v, parent[v]), max(v, parent[v])))
        for x in range(1, n + 1):
            if x not in inside and w[v - 1, x - 1] < key[x]:
                key[x], parent[x] = w[v - 1, x - 1], v
    assert used == {(u, v) for u, v, _ in _mst(n, p["wedges"])}
    return [Fraction(v) for v in order]


def _simple_paths_shortest(n: int, wedges, s: int, t: int) -> int:
    adj = {}
    for u, v, w in wedges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    best = None
    stack = [(s, 0, {s})]
    while stack:
        u, d, seen = stack.pop()
        if u == t:
            best = d if best is None else min(best, d)
            continue
        for v, w in adj.get(u, []):
            if v not in seen:
                stack.append((v, d + w, seen | {v}))
    return best


def _distance(p: dict) -> list[Fraction]:
    return _list(_simple_paths_shortest(p["n"], p["wedges"], 1, p["t"]))


def _floyd(p: dict) -> list[Fraction]:
    n = p["n"]
    d = sp.Matrix(n, n, lambda i, j: 0 if i == j else sp.oo)
    for u, v, w in p["wedges"]:
        d[u - 1, v - 1] = d[v - 1, u - 1] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i, j] = sp.Min(d[i, j], d[i, k] + d[k, j])
    s = p["s"]
    return [_fr(d[s - 1, v - 1]) for v in range(1, n + 1) if v != s]


def _min_cut(n: int, arcs) -> int:
    inner = list(range(2, n))
    best = None
    for r in range(len(inner) + 1):
        for extra in itertools.combinations(inner, r):
            side = {1, *extra}
            cap = sum(c for u, v, c in arcs if u in side and v not in side)
            best = cap if best is None else min(best, cap)
    return best


def _cut_claim(p: dict) -> bool:
    side = set(p["side"])
    cap = sum(c for u, v, c in p["arcs"] if u in side and v not in side)
    return cap == _min_cut(p["n"], p["arcs"])


# ------------------------------------------------------------------ floor 8: convexity and optima
def _fence(p: dict) -> list[Fraction]:
    k = p["d"] + 2
    x = sp.Symbol("x", positive=True)
    y = (p["L"] - k * x) if p["river"] else (p["L"] - k * x) / 2
    area = x * y
    crit = [c for c in sp.solve(sp.diff(area, x), x) if 0 < c < sp.Rational(p["L"], k)]
    assert sp.diff(area, x, 2) < 0
    return _list(max(area.subs(x, c) for c in crit))


def _box(p: dict) -> list[Fraction]:
    a, b = p["a"], p["b"]
    x = sp.Symbol("x", real=True)
    vol = x * (a - 2 * x) * (b - 2 * x)
    top = sp.Rational(min(a, b), 2)
    crit = [c for c in sp.solve(sp.diff(vol, x), x) if 0 < c < top]
    best = max(crit, key=lambda c: vol.subs(x, c))
    assert vol.subs(x, best) > 0 == vol.subs(x, 0) == vol.subs(x, top)
    return _list(best, vol.subs(x, best))


def _level_set_convex(p: dict) -> bool:
    x = sp.Symbol("x", real=True)
    expr = p["a"] * x ** 2 + p["b"] * x + p["c"]
    rel = expr <= 0 if p["sign"] == "<=" else expr >= 0
    s = sp.solveset(rel, x, domain=sp.S.Reals)
    return isinstance(s, sp.Interval) or s in (sp.S.Reals, sp.S.EmptySet) or isinstance(s, sp.FiniteSet) and len(s) <= 1


def _barycentric(p: dict) -> list[Fraction]:
    a, b, c = sp.symbols("a b c")
    A, B, C, P = p["A"], p["B"], p["C"], p["P"]
    sol = sp.solve([a + b + c - 1, a * A[0] + b * B[0] + c * C[0] - P[0], a * A[1] + b * B[1] + c * C[1] - P[1]],
                   [a, b, c], dict=True)[0]
    return _list(sol[a], sol[b], sol[c])


def _quad2(p: dict):
    return p["a"] * X ** 2 + p["b"] * X * Y + p["c"] * Y ** 2 + p["d"] * X + p["e"] * Y


def _convex2(p: dict) -> bool:
    h = sp.hessian(_quad2(p), (X, Y))
    return all(ev >= 0 for ev in h.eigenvals())


def _concave_interval(p: dict) -> list[Fraction]:
    x = sp.Symbol("x", real=True)
    r1, r2 = p["r1"], p["r2"]
    f = x ** 4 - 2 * (r1 + r2) * x ** 3 + 6 * r1 * r2 * x ** 2 + p["C"] * x + p["D"]
    s = sp.solveset(sp.diff(f, x, 2) <= 0, x, domain=sp.S.Reals)
    assert isinstance(s, sp.Interval)
    return _list(s.inf, s.sup)


def _stationary(p: dict) -> list[Fraction]:
    f = _quad2(p)
    sol = sp.solve([sp.diff(f, X), sp.diff(f, Y)], [X, Y], dict=True)
    assert len(sol) == 1
    return _list(sol[0][X], sol[0][Y])


def _minimum(p: dict) -> list[Fraction]:
    f = _quad2(p)
    h = sp.hessian(f, (X, Y))
    assert all(ev > 0 for ev in h.eigenvals())
    sol = sp.solve([sp.diff(f, X), sp.diff(f, Y)], [X, Y], dict=True)[0]
    return _list(f.subs(sol))


def _global_min(p: dict) -> bool:
    f = _quad2(p)
    pt = {X: _rat(p["x"]), Y: _rat(p["y"])}
    grad_zero = sp.diff(f, X).subs(pt) == 0 and sp.diff(f, Y).subs(pt) == 0
    psd = all(ev >= 0 for ev in sp.hessian(f, (X, Y)).eigenvals())
    return bool(grad_zero and psd)


def _min_of_max(p: dict) -> list[Fraction]:
    z = sp.Symbol("z")
    cons = [z >= a * X + b for a, b in p["lines"]]
    value, _ = lpmin(z, cons)
    return _list(value)


# ------------------------------------------------------------------ floor 9: programmes
def _lp(p: dict):
    c, cons = p["c"], p["cons"]
    return lpmax(c[0] * X + c[1] * Y, [a * X + b * Y <= r for a, b, r in cons] + [X >= 0, Y >= 0])


def _lp_value(p: dict) -> list[Fraction]:
    return _list(_lp(p)[0])


def _lp_point(p: dict) -> list[Fraction]:
    _, sol = _lp(p)
    return _list(sol[X], sol[Y])


def _slack(p: dict) -> bool:
    _, sol = _lp(p)
    a, b, r = p["cons"][p["k"]]
    return bool(a * sol[X] + b * sol[Y] < r)


def _pivot(p: dict) -> list[Fraction]:
    """One simplex iteration on the tableau [A | I | b] with the cost row, by sympy row operations."""
    c, cons = p["c"], p["cons"]
    m = len(cons)
    t = sp.zeros(m + 1, 2 + m + 1)
    for i, (a, b, r) in enumerate(cons):
        t[i, 0], t[i, 1], t[i, 2 + i], t[i, -1] = a, b, 1, r
    t[m, 0], t[m, 1] = -c[0], -c[1]
    col = min(range(2), key=lambda j: t[m, j])                    # most negative reduced cost
    rows = [i for i in range(m) if t[i, col] > 0]
    row = min(rows, key=lambda i: t[i, -1] / t[i, col])
    t[row, :] = t[row, :] / t[row, col]
    for i in range(m + 1):
        if i != row:
            t[i, :] = t[i, :] - t[i, col] * t[row, :]
    return _list(t[row, -1], t[m, -1])


def _dual(p: dict):
    c, ((a1, b1, r1), (a2, b2, r2)) = p["c"], p["cons"]
    u, v = sp.symbols("u v")
    value, sol = lpmin(r1 * u + r2 * v, [a1 * u + a2 * v >= c[0], b1 * u + b2 * v >= c[1], u >= 0, v >= 0])
    return value, sol, (u, v)


def _dual_value(p: dict) -> list[Fraction]:
    return _list(_dual(p)[0])


def _dual_point(p: dict) -> list[Fraction]:
    value, sol, (u, v) = _dual(p)
    return _list(sol[u], sol[v])


def _lagrange(p: dict) -> list[Fraction]:
    if p["kind"] == "min":
        f = p["a"] * X ** 2 + p["b"] * Y ** 2
        g = p["p"] * X + p["q"] * Y - p["r"]
    else:
        f = X * Y
        g = p["p"] * X + p["q"] * Y - p["r"]
    lag = f - LAM * g
    sol = sp.solve([sp.diff(lag, X), sp.diff(lag, Y), g], [X, Y, LAM], dict=True)
    assert len(sol) == 1
    s = sol[0]
    return _list(s[X], s[Y], f.subs(s))


def _kkt(p: dict) -> bool:
    a, b, pp, q, r = p["a"], p["b"], p["p"], p["q"], p["r"]
    f = (X - a) ** 2 + (Y - b) ** 2
    g = pp * X + q * Y - r
    mu = sp.Symbol("mu")
    # the KKT system: grad f + mu grad g = 0, mu g = 0, g <= 0, mu >= 0 - solve both cases
    cands = []
    for active in (False, True):
        eqs = [sp.diff(f + mu * g, X), sp.diff(f + mu * g, Y), g if active else mu]
        for s in sp.solve(eqs, [X, Y, mu], dict=True):
            if g.subs(s) <= 0 and s[mu] >= 0:
                cands.append((s[X], s[Y], s[mu]))
    assert len(set(cands)) == 1
    x, y, m = cands[0]
    if p["kind"] == "chat":
        return bool(g.subs({X: x, Y: y}) == 0)
    if p["kind"] == "tam":
        return bool((x, y) == (a, b))
    t = sp.Rational(pp * a + q * b - r, pp * pp + q * q)
    return bool((x, y) == (a - t * pp, b - t * q))


def _gd_step(p: dict) -> list[Fraction]:
    f = p["a"] * X ** 2 + p["b"] * Y ** 2 + p["c"] * X + p["d"] * Y
    eta = _rat(p["eta"])
    pt = sp.Matrix([p["x0"], p["y0"]])
    grad = sp.Matrix([sp.diff(f, X), sp.diff(f, Y)])
    for _ in range(p["n"]):
        pt = pt - eta * grad.subs({X: pt[0], Y: pt[1]})
    return _list(pt[0], pt[1])


def _gd_converges(p: dict) -> bool:
    x0 = sp.Symbol("x0", real=True)
    f = p["a"] * (X - p["m"]) ** 2
    x1 = x0 - _rat(p["eta"]) * sp.diff(f, X).subs(X, x0)
    ratio = sp.simplify((x1 - p["m"]) / (x0 - p["m"]))
    if p["kind"] == "hoi_tu":
        return bool(abs(ratio) < 1)
    start = p["x0"]
    return bool(f.subs(X, x1.subs(x0, start)) < f.subs(X, start))


def _least_squares(p: dict) -> list[Fraction]:
    w = sp.Symbol("w", real=True)
    loss = sum((w * x - y) ** 2 for x, y in zip(p["xs"], p["ys"]))
    w1 = p["w0"] - _rat(p["eta"]) * sp.diff(loss, w).subs(w, p["w0"])
    (wstar,) = sp.solve(sp.diff(loss, w), w)
    return _list(w1, wstar)


EXPECTED: dict = {
    # ---- floor 7
    "tr_g7_dem_la": _leaves,
    "tr_g7_xoa_canh": _cycle_rank,
    "tr_g7_dem_cay_khung": _kirchhoff,
    "tr_g7_kruskal_tong": _mst_total,
    "tr_g7_kruskal_cuoi": _mst_total_and_heaviest,
    "tr_g7_prim": _prim_order,
    "tr_g7_dijkstra": _distance,
    "tr_g7_dijkstra_moi": _floyd,
    "tr_g7_luong_max": lambda p: _list(_min_cut(p["n"], p["arcs"])),
    "tr_g7_lat_cat": _cut_claim,
    # ---- floor 8
    "tr_g8_hang_rao": _fence,
    "tr_g8_hop": _box,
    "tr_g8_tap_muc": _level_set_convex,
    "tr_g8_to_hop_loi": _barycentric,
    "tr_g8_hesse": _convex2,
    "tr_g8_khoang_lom": _concave_interval,
    "tr_g8_diem_dung": _stationary,
    "tr_g8_cuc_tieu": _minimum,
    "tr_g8_toan_cuc": _global_min,
    "tr_g8_max_duong": _min_of_max,
    # ---- floor 9
    "tr_g9_san_xuat": _lp_value,
    "tr_g9_gia_tri_qhtt": _lp_value,
    "tr_g9_dinh_qhtt": _lp_point,
    "tr_g9_rang_buoc_long": _slack,
    "tr_g9_don_hinh": _pivot,
    "tr_g9_doi_ngau_gia_tri": _dual_value,
    "tr_g9_doi_ngau_nghiem": _dual_point,
    "tr_g9_lagrange": _lagrange,
    "tr_g9_kkt": _kkt,
    "tr_g9_gd_buoc": _gd_step,
    "tr_g9_gd_hoi_tu": _gd_converges,
    "tr_g9_mat_mat": _least_squares,
}
