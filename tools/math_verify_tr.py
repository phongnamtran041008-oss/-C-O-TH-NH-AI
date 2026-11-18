"""The sympy recomputation of every generator of Tối Ưu và Toán Rời Rạc (M11): generator id -> a function
of the drawn numbers (`Draw.params`) giving a bool for a true_false question, or a list of
Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED. This module must not
import math_verify (it is imported by it).

The generators use closed formulas and the generation rules the floor teaches; here the
answers are found the other way: logic by sympy.logic (satisfiability, truth tables), counts
by listing every configuration (itertools, sympy.utilities.iterables), ranks and successors
by looking the configuration up in the full ordered list or with sympy's Permutation, sums
by sympy.summation, recurrences by a power of their companion matrix."""
from __future__ import annotations

import itertools
import math
from collections import deque
from fractions import Fraction

import sympy as sp
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup
from sympy.logic.boolalg import And, Equivalent, Implies, Not, Or, Xor, truth_table
from sympy.logic.inference import satisfiable
from sympy.utilities.iterables import multiset_permutations

_SYMS = {name: sp.Symbol(name) for name in ("p", "q", "r", "a", "b", "c")}
_OPS = {"and": And, "or": Or, "imp": Implies, "iff": Equivalent}


def logic(f):
    """The JSON proposition of tr_floor1 as a sympy.logic expression (no evaluation)."""
    if isinstance(f, str):
        return _SYMS[f]
    if f[0] == "not":
        return Not(logic(f[1]), evaluate=False)
    return _OPS[f[0]](logic(f[1]), logic(f[2]), evaluate=False)


def _truth(f, env: dict) -> bool:
    expr = logic(f).subs({_SYMS[k]: sp.true if v else sp.false for k, v in env.items()})
    return bool(sp.simplify_logic(expr))


def _equivalent(p: dict) -> bool:
    return satisfiable(Xor(logic(p["x"]), logic(p["y"]))) is False


def _true_rows(p: dict) -> list[Fraction]:
    names = [_SYMS[v] for v in ("p", "q", "r")]
    return [Fraction(sum(1 for _, v in truth_table(logic(p["f"]), names) if v))]


def _count(it) -> list[Fraction]:
    return [Fraction(sum(1 for _ in it))]


def _paths(p: dict) -> list[Fraction]:
    """List every route A -> C in the road map: (A-B road, B-C road) pairs plus direct roads."""
    roads = [("A", "B", i) for i in range(p["ab"])] + [("B", "C", i) for i in range(p["bc"])] + \
            [("A", "C", i) for i in range(p["ac"])]
    routes = []

    def walk(at, path):
        if at == "C":
            routes.append(tuple(path))
            return
        for road in roads:
            if road[0] == at:
                walk(road[1], path + [road])

    walk("A", [])
    return [Fraction(len(routes))]


_BINARY_TESTS = {
    "all": lambda s: True,
    "start1": lambda s: s.startswith("1"),
    "same_ends": lambda s: s[0] == s[-1],
    "end01": lambda s: s.endswith("01"),
}


def _binary(p: dict) -> list[Fraction]:
    test = _BINARY_TESTS[p["kind"]]
    return _count(s for s in ("".join(t) for t in itertools.product("01", repeat=p["n"])) if test(s))


def _alphabet(p: dict) -> list[Fraction]:
    words = itertools.product(range(p["k"]), repeat=p["n"])
    test = {"same_ends": lambda w: w[0] == w[-1],
            "no_repeat_neighbour": lambda w: all(a != b for a, b in zip(w, w[1:])),
            "no_a": lambda w: 0 not in w}[p["kind"]]
    return _count(w for w in words if test(w))


_i = sp.Symbol("i", integer=True, positive=True)
_TERMS = {
    "natural": _i, "odd": 2 * _i - 1, "even": 2 * _i,
    "squares": _i ** 2, "cubes": _i ** 3, "products": _i * (_i + 1),
    "powers": 2 ** (_i - 1), "telescoping": 1 / (_i * (_i + 1)),
}


def _sum(p: dict) -> list[Fraction]:
    v = sp.summation(_TERMS[p["kind"]], (_i, 1, p["n"]))
    v = sp.Rational(v)
    return [Fraction(int(v.p), int(v.q))]


# ------------------------------------------------------------------ floor 2
def _anagrams(p: dict) -> list[Fraction]:
    letters = [c for c, k in zip("RBY", p["counts"]) for _ in range(k)]
    return _count(multiset_permutations(letters))


def _adjacent(p: dict) -> list[Fraction]:
    n = p["n"]

    def together(row) -> bool:
        return abs(row.index(0) - row.index(1)) == 1

    return _count(row for row in itertools.permutations(range(n)) if together(row) != p["apart"])


def _two_groups(p: dict) -> list[Fraction]:
    m = list(itertools.combinations(range(p["m"]), p["a"]))
    w = list(itertools.combinations(range(p["w"]), p["b"]))
    return _count(itertools.product(m, w))


def _solutions(k: int, n: int, low: int) -> list[Fraction]:
    return _count(x for x in itertools.product(range(low, n + 1), repeat=k) if sum(x) == n)


def _divisible_by_either(p: dict) -> list[Fraction]:
    return _count(x for x in range(1, p["n"] + 1) if x % p["a"] == 0 or x % p["b"] == 0)


def _divisible_by_none(p: dict) -> list[Fraction]:
    return _count(x for x in range(1, p["n"] + 1) if all(x % d for d in p["divisors"]))


def _recurrence(p: dict) -> list[Fraction]:
    m = sp.Matrix([[p["c1"], p["c2"]], [1, 0]])
    v = (m ** (p["n"] - 1)) * sp.Matrix([p["a1"], p["a0"]])
    return [Fraction(int(v[0]))]


def _no_run(p: dict) -> list[Fraction]:
    banned = "1" * p["run"]
    return _count(s for s in ("".join(t) for t in itertools.product("01", repeat=p["n"])) if banned not in s)


# ------------------------------------------------------------------ floor 3
def _pigeons_needed(p: dict) -> list[Fraction]:
    n = 1
    while sp.ceiling(sp.Rational(n, p["k"])) < p["m"]:
        n += 1
    return [Fraction(n)]


def _fullest_box(p: dict) -> list[Fraction]:
    """Deal the objects one by one into the emptiest box: the fullest box at the end is the
    smallest maximum any placement can have."""
    boxes = [0] * p["k"]
    for _ in range(p["n"]):
        boxes[boxes.index(min(boxes))] += 1
    return [Fraction(max(boxes))]


def _pair_rule(kind: str, n: int):
    if kind == "sum":
        return lambda a, b: a + b == 2 * n + 1
    if kind == "next":
        return lambda a, b: abs(a - b) == 1
    return lambda a, b: abs(a - b) == n


def _forced_pair(p: dict) -> list[Fraction]:
    """The smallest t such that every t numbers of 1..2n contain a pair, by trying subsets."""
    n, bad = p["n"], _pair_rule(p["kind"], p["n"])
    pool = range(1, 2 * n + 1)
    for t in range(2, 2 * n + 1):
        if all(any(bad(a, b) for a, b in itertools.combinations(c, 2)) for c in itertools.combinations(pool, t)):
            return [Fraction(t)]
    raise ValueError("no size forces a pair")


def _board(p: dict) -> bool:
    nums = list(range(1, p["n"] + 1))
    while len(nums) > 1:            # one particular way of playing: the parity cannot depend on it
        a, b = nums.pop(), nums.pop(0)
        nums.append(a + b if p["op"] == "sum" else abs(a - b))
    return (nums[0] % 2 == 1) == p["claim_odd"]


def _cups(p: dict) -> bool:
    """Breadth-first search over the number of cups facing down."""
    n, k = p["n"], p["k"]
    seen, todo = {p["d"]}, deque([p["d"]])
    while todo:
        d = todo.popleft()
        for down in range(0, k + 1):           # how many of the k flipped cups were facing down
            if down <= d and k - down <= n - d:
                e = d - down + (k - down)
                if e not in seen:
                    seen.add(e)
                    todo.append(e)
    return 0 in seen


def _perm(xs) -> Permutation:
    return Permutation([v - 1 for v in xs])


def _next_binary(p: dict) -> list[Fraction]:
    n = len(p["bits"])
    words = ["".join(t) for t in itertools.product("01", repeat=n)]
    nxt = words[words.index("".join(str(b) for b in p["bits"])) + 1]
    return [Fraction(int(c)) for c in nxt]


def _next_subset(p: dict) -> list[Fraction]:
    subsets = list(itertools.combinations(range(1, p["n"] + 1), len(p["subset"])))
    return [Fraction(v) for v in subsets[subsets.index(tuple(p["subset"])) + 1]]


def _next_perm(p: dict) -> list[Fraction]:
    nxt = _perm(p["p"]).next_lex()
    return [Fraction(v + 1) for v in nxt.array_form]


def _binary_rank(p: dict) -> list[Fraction]:
    words = [list(t) for t in itertools.product([0, 1], repeat=len(p["bits"]))]
    return [Fraction(words.index(p["bits"]) + 1)]


def _subset_rank(p: dict) -> list[Fraction]:
    subsets = list(itertools.combinations(range(1, p["n"] + 1), len(p["subset"])))
    return [Fraction(subsets.index(tuple(p["subset"])) + 1)]


def _bounded_triples(p: dict) -> list[Fraction]:
    return _count(x for x in itertools.product(range(p["b"] + 1), repeat=3) if sum(x) == p["s"])


def _subset_sums(p: dict) -> list[Fraction]:
    items = range(1, p["n"] + 1)
    return _count(c for r in range(1, p["n"] + 1) for c in itertools.combinations(items, r) if sum(c) == p["s"])


EXPECTED: dict = {
    # ---- floor 1
    "tr_g1_chan_tri": lambda p: _truth(p["f"], p["env"]),
    "tr_g1_chan_tri_hop": lambda p: _truth(p["f"], p["env"]),
    "tr_g1_tuong_duong": _equivalent,
    "tr_g1_dem_dong_dung": _true_rows,
    "tr_g1_quy_tac_nhan": lambda p: _count(itertools.product(*(range(s) for s in p["sizes"]))),
    "tr_g1_quy_tac_cong": _paths,
    "tr_g1_xau_nhi_phan": _binary,
    "tr_g1_dem_cau_hinh": _alphabet,
    "tr_g1_tong_quy_nap": _sum,
    "tr_g1_tong_quy_nap_2": _sum,
    # ---- floor 2
    "tr_g2_chinh_hop_lap": lambda p: _count(itertools.product(range(p["n"]), repeat=p["k"])),
    "tr_g2_chinh_hop": lambda p: _count(itertools.permutations(range(p["n"]), p["k"])),
    "tr_g2_hoan_vi": lambda p: [Fraction(int(SymmetricGroup(p["n"]).order()))],
    "tr_g2_hoan_vi_lap": _anagrams,
    "tr_g2_canh_nhau": _adjacent,
    "tr_g2_to_hop": lambda p: _count(itertools.combinations(range(p["n"]), p["k"])),
    "tr_g2_hai_nhom": _two_groups,
    "tr_g2_nghiem_nguyen": lambda p: _solutions(p["k"], p["n"], 0),
    "tr_g2_nghiem_can_duoi": lambda p: _solutions(p["k"], p["n"], p["m"]),
    "tr_g2_bu_tru_hai_so": _divisible_by_either,
    "tr_g2_bu_tru_ba_so": _divisible_by_none,
    "tr_g2_truy_hoi": _recurrence,
    "tr_g2_xau_cam": _no_run,
    # ---- floor 3
    "tr_g3_dirichlet_min": _pigeons_needed,
    "tr_g3_dirichlet_tran": _fullest_box,
    "tr_g3_dirichlet_cap": _forced_pair,
    "tr_g3_bat_bien": _board,
    "tr_g3_lat_coc": _cups,
    "tr_g3_so_sanh": lambda p: _perm(p["x"]).rank() < _perm(p["y"]).rank(),
    "tr_g3_xau_ke_tiep": _next_binary,
    "tr_g3_tap_con_ke_tiep": _next_subset,
    "tr_g3_hoan_vi_ke_tiep": _next_perm,
    "tr_g3_hang_xau": _binary_rank,
    "tr_g3_hang_hoan_vi": lambda p: [Fraction(int(_perm(p["p"]).rank()) + 1)],
    "tr_g3_hang_tap_con": _subset_rank,
    "tr_g3_quay_lui_tong": _bounded_triples,
    "tr_g3_quay_lui_tap_con": _subset_sums,
}
