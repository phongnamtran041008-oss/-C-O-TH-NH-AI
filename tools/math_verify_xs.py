"""The sympy recomputation of every generator of Xác Suất và Thống Kê (M11): generator id -> a function
of the drawn numbers (`Draw.params`) giving a bool for a true_false question, or a list of
Fractions for a numeric one. Merged into tools/math_verify.py EXPECTED. This module must not
import math_verify (it is imported by it).

The generators count with formulas (product rule, n!, C(n, k), the addition and multiplication
rules, Bernoulli). Here every answer is found another way: the sample space is listed outcome by
outcome (itertools) and the favourable ones are counted, events are rebuilt from their
definitions as sympy sets, and the floor-3 probabilities use sympy.stats random variables."""
from __future__ import annotations

import itertools
from fractions import Fraction

import sympy as sp
from sympy import FiniteSet, Rational
from sympy.stats import Bernoulli, Binomial, Die, P


def _frac(v) -> Fraction:
    v = sp.simplify(sp.sympify(v))       # (no nsimplify: it may turn an exact Rational into a power product)
    if not isinstance(v, sp.Rational):
        raise ValueError(f"{v} is not a rational number")
    return Fraction(int(v.p), int(v.q))


def _count(outcomes, keep=lambda o: True) -> int:
    return sum(1 for o in outcomes if keep(o))


def _prob(outcomes, keep) -> list[Fraction]:
    """Classical probability over an equally likely list of outcomes."""
    outcomes = list(outcomes)
    return [_frac(Rational(_count(outcomes, keep), len(outcomes)))]


FACES = range(1, 7)

# ------------------------------------------------------------------ floor 1
# die events from their definitions (the generator reads a table of faces)
_DIE_TEST = {"chan": lambda f: f % 2 == 0, "le": lambda f: f % 2 == 1,
             "chia3": lambda f: f % 3 == 0, "nguyen_to": lambda f: sp.isprime(f)}


def _su_kien(p: dict) -> list[Fraction]:
    a = FiniteSet(*[f for f in FACES if _DIE_TEST[p["a"]](f)])
    b = FiniteSet(*[f for f in FACES if (f > p["k"] if p["side"] == ">" else f < p["k"])])
    event = sp.Intersection(a, b) if p["op"] == "tich" else sp.Union(a, b)
    return [Fraction(int(v)) for v in event]


def _ma_so(p: dict) -> list[Fraction]:
    codes = itertools.product(range(1, p["n"] + 1), repeat=p["k"])
    keep = (lambda c: True) if p["kind"] == "tu_do" else (lambda c: c[-1] % 2 == 1)
    return [Fraction(_count(codes, keep))]


def _hoan_vi(p: dict) -> list[Fraction]:
    rows = itertools.permutations(range(p["n"]))       # person 0 is Lan
    keep = (lambda r: r[0] == 0) if p["fixed"] else (lambda r: True)
    return [Fraction(_count(rows, keep))]


def _hai_nhom(p: dict) -> list[Fraction]:
    people = ["m"] * p["men"] + ["w"] * p["women"]
    teams = itertools.combinations(range(len(people)), p["a"] + p["b"])
    return [Fraction(_count(teams, lambda t: sum(people[i] == "m" for i in t) == p["a"]))]


def _thu_tu_tf(p: dict) -> bool:
    pick = itertools.permutations if p["ordered"] else itertools.combinations
    return _count(pick(range(p["n"]), p["k"])) == p["shown"]


# ------------------------------------------------------------------ floor 2
def _tong(p: dict) -> list[Fraction]:
    s = p["s"]
    test = {"=": lambda t: t == s, ">=": lambda t: t >= s, "<=": lambda t: t <= s}[p["kind"]]
    return _prob(itertools.product(FACES, FACES), lambda o: test(o[0] + o[1]))


# a card is (value 1..13, suit 0..3); suits 0, 1 are red (rô, cơ = suit 1), 1 is cơ; value 1 is át
def _card_test(kind: str):
    red = lambda c: c[1] in (0, 1)
    return {
        "co": lambda h: all(c[1] == 1 for c in h),
        "do": lambda h: all(red(c) for c in h),
        "at": lambda h: all(c[0] == 1 for c in h),
        "hinh": lambda h: all(c[0] in (11, 12, 13) for c in h),
        "cung_chat": lambda h: h[0][1] == h[1][1],
        "at_k": lambda h: sorted(c[0] for c in h) == [1, 13],
        "khac_mau": lambda h: red(h[0]) != red(h[1]),
        "dung_mot_co": lambda h: sum(c[1] == 1 for c in h) == 1,
        "it_nhat_mot_at": lambda h: any(c[0] == 1 for c in h),
        "cung_gia_tri": lambda h: h[0][0] == h[1][0],
    }[kind]


DECK = [(v, s) for v in range(1, 14) for s in range(4)]


def _rut_bai(p: dict) -> list[Fraction]:
    return _prob(itertools.combinations(DECK, 2), _card_test(p["kind"]))


def _rut_bi(p: dict) -> list[Fraction]:
    balls = ["r"] * p["red"] + ["b"] * p["blue"]
    return _prob(itertools.combinations(range(len(balls)), p["k"]),
                 lambda h: sum(balls[i] == "r" for i in h) == p["r"])


def _hoan_lai(p: dict) -> list[Fraction]:
    balls = ["w"] * p["white"] + ["k"] * p["black"]
    idx = range(len(balls))
    draws = itertools.product(idx, idx) if p["back"] else itertools.permutations(idx, 2)
    test = {"trang": lambda c: c == ("w", "w"), "den": lambda c: c == ("k", "k"),
            "khac_mau": lambda c: c[0] != c[1]}[p["event"]]
    return _prob(draws, lambda d: test((balls[d[0]], balls[d[1]])))


def _it_nhat_mot(p: dict) -> list[Fraction]:
    if p["kind"] == "ngua":
        return _prob(itertools.product("SN", repeat=p["n"]), lambda o: "N" in o)
    hit = (lambda f: f == 6) if p["kind"] == "sau" else (lambda f: f % 2 == 0)
    return _prob(itertools.product(FACES, repeat=p["n"]), lambda o: any(hit(f) for f in o))


def _tan_suat(p: dict) -> list[Fraction]:
    shots = [1] * sum(p["hits"]) + [0] * (sum(p["shots"]) - sum(p["hits"]))     # one entry per shot
    return [_frac(Rational(shots.count(0 if p["miss"] else 1), len(shots)))]


def _so_ca(p: dict) -> list[Fraction]:
    n = sp.Symbol("N", positive=True)
    return [_frac(sp.solve(sp.Eq(Rational(p["again"], p["caught"]), p["marked"] / n), n)[0])]


# ------------------------------------------------------------------ floor 3
def _chia_het(p: dict) -> list[Fraction]:
    nums = range(1, p["n"] + 1)
    a = FiniteSet(*[v for v in nums if v % p["a"] == 0])
    b = FiniteSet(*[v for v in nums if v % p["b"] == 0])
    return [_frac(Rational(len(a | b), p["n"]))]


def _cong_tim_giao(p: dict) -> list[Fraction]:
    pa, pb, given = Rational(p["pa"]), Rational(p["pb"]), Rational(p["given"])
    x = sp.Symbol("x")
    if p["kind"] == "giao":         # given = P(A + B): solve the addition rule for P(AB)
        return [_frac(sp.solve(sp.Eq(pa + pb - x, given), x)[0])]
    pab = given
    # neither A nor B: P(not A and not B) from a four-cell table that adds up to 1
    cells = sp.solve([sp.Eq(x + sp.Symbol("ab") + sp.Symbol("a_only") + sp.Symbol("b_only"), 1),
                      sp.Eq(sp.Symbol("ab"), pab), sp.Eq(sp.Symbol("a_only"), pa - pab),
                      sp.Eq(sp.Symbol("b_only"), pb - pab)],
                     [x, sp.Symbol("ab"), sp.Symbol("a_only"), sp.Symbol("b_only")], dict=True)[0]
    return [_frac(cells[x])]


def _bang(p: dict) -> list[Fraction]:
    m_d, m_t, f_d, f_t = p["table"]
    people = ([("nam", "dat")] * m_d + [("nam", "truot")] * m_t + [("nu", "dat")] * f_d + [("nu", "truot")] * f_t)
    event, cond = p["kind"].split("|")
    given = [x for x in people if cond in x]
    return [_frac(Rational(sum(event in x for x in given), len(given)))]


def _dieu_kien_xuc_xac(p: dict) -> list[Fraction]:
    x, y = Die("X", 6), Die("Y", 6)
    event = {"bang_nhau": sp.Eq(x, y), "co_sau": sp.Or(sp.Eq(x, 6), sp.Eq(y, 6)),
             "dau_lon_hon": x > y, "dau_chan": sp.Eq(x % 2, 0)}[p["kind"]]
    if p["kind"] == "dau_chan":           # sympy.stats has no Mod of a die: list the even faces instead
        event = sp.Or(*[sp.Eq(x, f) for f in (2, 4, 6)])
    return [_frac(P(event, sp.Eq(x + y, p["s"])))]


def _khong_hoan_lai(p: dict) -> list[Fraction]:
    lot = ["d"] * p["d"] + ["g"] * (p["n"] - p["d"])
    want = ("g",) * p["k"] if p["kind"] == "tat_ca_tot" else ("g", "d")
    return _prob(itertools.permutations(range(p["n"]), p["k"]), lambda o: tuple(lot[i] for i in o) == want)


def _doc_lap_ban(p: dict) -> list[Fraction]:
    a, b = Bernoulli("A", Rational(p["p1"])), Bernoulli("B", Rational(p["p2"]))
    event = {"it_nhat_mot": sp.Ge(a + b, 1), "dung_mot": sp.Eq(a + b, 1), "khong_ai": sp.Eq(a + b, 0)}[p["kind"]]
    return [_frac(P(event))]


_A_FACES = {"chan": (2, 4, 6), "le": (1, 3, 5), "chia3": (3, 6), "nguyen_to": (2, 3, 5), "tu5": (5, 6)}


def _doc_lap_tf(p: dict) -> bool:
    x = Die("X", 6)
    a = sp.Or(*[sp.Eq(x, f) for f in FACES if f in _A_FACES[p["a"]]])
    b = x <= p["k"]
    return sp.simplify(P(sp.And(a, b)) - P(a) * P(b)) == 0


def _bernoulli(p: dict) -> list[Fraction]:
    x = Binomial("X", p["n"], Rational(p["p"]))
    return [_frac(P(sp.Eq(x, p["k"])))]


def _bernoulli_it_nhat(p: dict) -> list[Fraction]:
    x = Binomial("X", p["n"], Rational(p["p"]))
    return [_frac(P(x >= p["k"]))]


EXPECTED: dict = {
    # ---- floor 1
    "xs_g1_khong_gian_mau": lambda p: [Fraction(_count(itertools.product(
        *([("S", "N")] * p["coins"] + [FACES] * p["dice"]))))],
    "xs_g1_su_kien": _su_kien,
    "xs_g1_thuc_don": lambda p: [Fraction(len(list(FiniteSet(*range(p["a"])) * FiniteSet(*range(p["b"]))
                                                   * FiniteSet(*range(p["c"])))))],
    "xs_g1_ma_so": _ma_so,
    "xs_g1_hoan_vi": _hoan_vi,
    "xs_g1_chinh_hop": lambda p: [Fraction(_count(itertools.permutations(range(p["n"]), p["k"])))],
    "xs_g1_to_hop": lambda p: [Fraction(_count(itertools.combinations(range(p["n"]), p["k"])))],
    "xs_g1_hai_nhom": _hai_nhom,
    "xs_g1_thu_tu_tf": _thu_tu_tf,
    # ---- floor 2
    "xs_g2_tong_hai_xuc_xac": _tong,
    "xs_g2_dong_xu": lambda p: _prob(itertools.product("SN", repeat=p["n"]), lambda o: o.count("N") == p["k"]),
    "xs_g2_rut_bi": _rut_bi,
    "xs_g2_rut_bai": _rut_bai,
    "xs_g2_hoan_lai": _hoan_lai,
    "xs_g2_it_nhat_mot": _it_nhat_mot,
    "xs_g2_tan_suat": _tan_suat,
    "xs_g2_uoc_luong_so_ca": _so_ca,
    # ---- floor 3
    "xs_g3_chia_het": _chia_het,
    "xs_g3_cong_tim_giao": _cong_tim_giao,
    "xs_g3_bang_dieu_kien": _bang,
    "xs_g3_dieu_kien_xuc_xac": _dieu_kien_xuc_xac,
    "xs_g3_khong_hoan_lai": _khong_hoan_lai,
    "xs_g3_doc_lap_ban": _doc_lap_ban,
    "xs_g3_doc_lap_tf": _doc_lap_tf,
    "xs_g3_bernoulli": _bernoulli,
    "xs_g3_bernoulli_it_nhat": _bernoulli_it_nhat,
}
