"""The recomputation of every generator of Tối Ưu và Toán Rời Rạc, floors 4-6 (M11, second
round): generator id -> a function of the drawn numbers (`Draw.params`) giving a bool for a
true_false question, or a list of Fractions for a numeric one. Merged into tools/math_verify.py
EXPECTED. This module must not import math_verify (it is imported by it).

The generators solve their instances the way the floors teach (dynamic programming, greedy
choices, closed formulas, BFS with a queue, recursive DFS, graphs built to have a property).
Here every answer is found another way: optima by trying every subset or permutation, loop
counts by running the loops, growth rates by sympy limits, graph facts from the adjacency
matrix with sympy (degrees from row sums, edges from trace(A^2), walks from powers of A,
components from the rank of the Laplacian, reachability from (I + A)^(n-1), odd cycles from
the traces of odd powers), DFS with an explicit stack, degree sequences by Erdős-Gallai, and
Hamilton cycles by trying every permutation."""
from __future__ import annotations

import itertools
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


def _one(x) -> list[Fraction]:
    return [Fraction(int(x))]


# ------------------------------------------------------------------ floor 4
def _count_solutions(p: dict) -> list[Fraction]:
    n = p["n"]
    if p["kind"] == "tui":
        return _one(sum(1 for _ in itertools.product((0, 1), repeat=n)))
    if p["kind"] == "du_lich":
        return _one(sum(1 for t in itertools.permutations(range(1, n + 1)) if t[0] == 1))
    return _one(sum(1 for _ in itertools.permutations(range(n))))


def _knapsack(p: dict) -> list[Fraction]:
    w, c, cap = p["weights"], p["values"], p["cap"]
    best = max(sum(c[i] for i in s) for r in range(len(w) + 1) for s in itertools.combinations(range(len(w)), r)
               if sum(w[i] for i in s) <= cap)
    return _one(best)


_PAIRS = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


def _tsp(p: dict) -> list[Fraction]:
    """Held-Karp dynamic programming over (set of visited cities, last city)."""
    d = {}
    for (a, b), v in zip(_PAIRS, p["d"]):
        d[(a, b)] = d[(b, a)] = v
    others = (2, 3, 4)
    best = {(frozenset([c]), c): d[(1, c)] for c in others}
    for size in (2, 3):
        for subset in itertools.combinations(others, size):
            s = frozenset(subset)
            for last in subset:
                best[(s, last)] = min(best[(s - {last}, prev)] + d[(prev, last)] for prev in subset if prev != last)
    full = frozenset(others)
    return _one(min(best[(full, last)] + d[(last, 1)] for last in others))


def _assignment(p: dict) -> list[Fraction]:
    """Dynamic programming over the set of jobs already given to persons 1..k."""
    cost = p["cost"]

    @lru_cache(maxsize=None)
    def go(k: int, used: frozenset) -> int:
        if k == 3:
            return 0
        return min(cost[k][j] + go(k + 1, used | {j}) for j in range(3) if j not in used)

    return _one(go(0, frozenset()))


def _branch_cut(p: dict) -> bool:
    w, c, cap, x = p["weights"], p["values"], p["cap"], p["x"]
    v = sum(sp.Integer(c[i] * x[i]) for i in range(2))
    left = cap - sum(w[i] * x[i] for i in range(2))
    best_ratio = max(sp.Rational(c[i], w[i]) for i in (2, 3))          # the items still to decide
    return bool(v + left * best_ratio <= p["record"])


def _greedy_coins(p: dict) -> bool:
    a, b, x = p["a"], p["b"], p["x"]
    fewest = min(i + j + (x - i * b - j * a) for i in range(x // b + 1) for j in range((x - i * b) // a + 1))
    i = x // b
    j = (x - i * b) // a
    return (i + j + (x - i * b - j * a)) == fewest


def _talks(p: dict) -> list[Fraction]:
    talks = [tuple(t) for t in p["talks"]]

    def fits(group) -> bool:
        return all(s1 >= f2 or s2 >= f1 for (s1, f1), (s2, f2) in itertools.combinations(group, 2))

    return _one(max(r for r in range(len(talks) + 1) for g in itertools.combinations(talks, r) if fits(g)))


def _run_loops(p: dict) -> list[Fraction]:
    n, kind, x = p["n"], p["kind"], 0
    if kind == "full":
        for _ in range(n):
            for _ in range(n):
                x += 1
    elif kind == "tri":
        for i in range(1, n + 1):
            for _ in range(i, n + 1):
                x += 1
    elif kind == "strict":
        for i in range(1, n + 1):
            for _ in range(i + 1, n + 1):
                x += 1
    elif kind == "seq":
        for _ in range(n):
            x += 1
        for _ in range(n):
            for _ in range(n):
                x += 1
    else:
        for _ in range(n):
            j = 1
            while j <= n:
                j *= 2
                x += 1
    return _one(x)


_N = sp.Symbol("n", positive=True)


def _big_o(p: dict) -> bool:
    if p["kind"] == "poly":
        f = p["a"] * _N ** p["p"] + p["b"] * _N ** p["q"]
        g = _N ** p["k"]
    else:
        f = p["a"] * sp.Integer(p["c"]) ** _N + p["b"] * _N ** p["p"]
        g = sp.Integer(p["d"]) ** _N
    return sp.limit(f / g, _N, sp.oo).is_finite


# ------------------------------------------------------------------ graphs from the adjacency matrix
def adjacency(n: int, edges) -> sp.Matrix:
    a = sp.zeros(n, n)
    for u, v in edges:
        a[u - 1, v - 1] = a[v - 1, u - 1] = 1
    return a


def _degrees(a: sp.Matrix) -> list[int]:
    return [int(sum(a.row(i))) for i in range(a.rows)]


def _reach(a: sp.Matrix) -> sp.Matrix:
    """(I + A)^(n-1): entry (u, v) is positive exactly when v can be reached from u."""
    return (sp.eye(a.rows) + a) ** max(a.rows - 1, 1)


def _components(a: sp.Matrix) -> int:
    lap = sp.diag(*_degrees(a)) - a
    return a.rows - lap.rank()


# ------------------------------------------------------------------ floor 5
def _complete(p: dict) -> list[Fraction]:
    kind = p["kind"]
    if kind == "kn":
        return _one(sum(1 for _ in itertools.combinations(range(p["n"]), 2)))
    if kind == "kmn":
        return _one(sum(1 for _ in itertools.product(range(p["a"]), range(p["b"]))))
    if kind == "bu":
        return _one(sum(1 for _ in itertools.combinations(range(p["n"]), 2)) - p["m"])
    return _one(sum(1 for _ in itertools.permutations(range(p["n"]), 2)))


def _bipartite(p: dict) -> bool:
    a = adjacency(p["n"], p["edges"])
    return all((a ** k).trace() == 0 for k in range(1, p["n"] + 1, 2))


def _edges_from_degrees(p: dict) -> list[Fraction]:
    a = adjacency(p["n"], p["edges"])
    return [Fraction(int((a ** 2).trace()), 2)]


def _erdos_gallai(p: dict) -> bool:
    d = sorted(p["seq"], reverse=True)
    n = len(d)
    if sum(d) % 2:
        return False
    return all(sum(d[:k]) <= k * (k - 1) + sum(min(x, k) for x in d[k:]) for k in range(1, n + 1))


def _walks(p: dict, length: int) -> list[Fraction]:
    a = adjacency(p["n"], p["edges"])
    return _one((a ** length)[p["u"] - 1, p["v"] - 1])


def _matrix_question(p: dict) -> list[Fraction]:
    a = adjacency(4, p["edges"])
    if p["kind"] == "edges":
        return [Fraction(int((a ** 2).trace()), 2)]
    return _one(sum(a.row(p["w"] - 1)))


def _in_degree(p: dict) -> list[Fraction]:
    n = p["n"]
    a = sp.zeros(n, n)
    for u, v in p["arcs"]:
        a[u - 1, v - 1] = 1
    return _one(sum(a.col(p["w"] - 1)))


# ------------------------------------------------------------------ floor 6
def _bfs_levels(p: dict) -> list[Fraction]:
    """Distances from the powers of A; then each level in order of (first earlier-visited
    neighbour on the level above, label) - which is exactly the order a queue produces."""
    n, s = p["n"], p["s"]
    a = adjacency(n, p["edges"])
    dist, power = {s: 0}, sp.eye(n)
    for k in range(1, n):
        power = power * a
        for v in range(1, n + 1):
            if v not in dist and power[s - 1, v - 1] > 0:
                dist[v] = k
    order = [s]
    for k in range(1, max(dist.values()) + 1):
        level = [v for v in dist if dist[v] == k]
        key = {v: (min(order.index(u) for u in order if a[u - 1, v - 1] and dist[u] == k - 1), v) for v in level}
        order += sorted(level, key=lambda v: key[v])
    return [Fraction(v) for v in order]


def _distance(p: dict) -> list[Fraction]:
    a = adjacency(p["n"], p["edges"])
    power = sp.eye(p["n"])
    for k in range(0, p["n"]):
        if power[p["s"] - 1, p["t"] - 1] > 0:
            return _one(k)
        power = power * a
    raise ValueError("t cannot be reached")


def _dfs_stack(p: dict) -> list[Fraction]:
    """DFS with an explicit stack: push the neighbours in decreasing order, mark on pop.
    This visits the vertices in the same order as the recursive DFS with increasing order."""
    a = adjacency(p["n"], p["edges"])
    seen, order, stack = set(), [], [p["s"]]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        order.append(u)
        for v in range(p["n"], 0, -1):
            if a[u - 1, v - 1] and v not in seen:
                stack.append(v)
    return [Fraction(v) for v in order]


def _reachable(p: dict) -> bool:
    return _reach(adjacency(p["n"], p["edges"]))[p["u"] - 1, p["v"] - 1] > 0


def _component_question(p: dict) -> list[Fraction]:
    a = adjacency(p["n"], p["edges"])
    if p["kind"] == "count":
        return _one(_components(a))
    r = _reach(a)
    return _one(sum(1 for j in range(p["n"]) if r[p["w"] - 1, j] > 0))


def _euler_circuit(p: dict) -> bool:
    a = adjacency(p["n"], p["edges"])
    used = [i for i, d in enumerate(_degrees(a)) if d > 0]
    sub = a.extract(used, used)
    connected = _components(sub) == 1
    return connected and all(d % 2 == 0 for d in _degrees(a))


def _odd_vertices(p: dict) -> list[Fraction]:
    a = adjacency(p["n"], p["edges"])
    odd = [i + 1 for i, d in enumerate(_degrees(a)) if d % 2]
    if len(odd) != 2 or _components(a) != 1:
        raise ValueError("the graph has no Euler path that is not a circuit")
    return [Fraction(v) for v in odd]


def _hamilton_cycle(p: dict) -> bool:
    n, es = p["n"], {tuple(e) for e in p["edges"]}
    adj = lambda u, v: (min(u, v), max(u, v)) in es     # noqa: E731
    for rest in itertools.permutations(range(2, n + 1)):
        cyc = (1,) + rest + (1,)
        if all(adj(cyc[i], cyc[i + 1]) for i in range(n)):
            return True
    return False


@lru_cache(maxsize=None)
def _count_hamilton(kind: str, n: int) -> int:
    if kind == "kn":
        verts, adj = list(range(n)), lambda u, v: u != v                         # noqa: E731
    else:
        verts, adj = list(range(2 * n)), lambda u, v: (u < n) != (v < n)         # noqa: E731
    found = 0
    for rest in itertools.permutations(verts[1:]):
        cyc = (verts[0],) + rest + (verts[0],)
        if all(adj(cyc[i], cyc[i + 1]) for i in range(len(verts))):
            found += 1
    return found // 2


EXPECTED: dict = {
    # ---- floor 4
    "tr_g4_so_phuong_an": _count_solutions,
    "tr_g4_cai_tui": _knapsack,
    "tr_g4_nguoi_du_lich": _tsp,
    "tr_g4_phan_viec": _assignment,
    "tr_g4_nhanh_can": _branch_cut,
    "tr_g4_tham_lam_xu": _greedy_coins,
    "tr_g4_lich": _talks,
    "tr_g4_dem_vong_lap": _run_loops,
    "tr_g4_o_lon": _big_o,
    # ---- floor 5
    "tr_g5_day_du": _complete,
    "tr_g5_hai_phia": _bipartite,
    "tr_g5_bat_tay": _edges_from_degrees,
    "tr_g5_day_bac": _erdos_gallai,
    "tr_g5_lien_thong": lambda p: _one(_components(adjacency(p["n"], p["edges"]))),
    "tr_g5_hanh_trinh_2": lambda p: _walks(p, 2),
    "tr_g5_hanh_trinh_3": lambda p: _walks(p, 3),
    "tr_g5_ma_tran_canh": _matrix_question,
    "tr_g5_ban_bac_vao": _in_degree,
    # ---- floor 6
    "tr_g6_bfs_thu_tu": _bfs_levels,
    "tr_g6_bfs_khoang_cach": _distance,
    "tr_g6_dfs_thu_tu": _dfs_stack,
    "tr_g6_noi_duoc": _reachable,
    "tr_g6_thanh_phan": _component_question,
    "tr_g6_euler": _euler_circuit,
    "tr_g6_euler_duong": _odd_vertices,
    "tr_g6_hamilton": _hamilton_cycle,
    "tr_g6_dem_hamilton": lambda p: _one(_count_hamilton(p["kind"], p["n"])),
}
