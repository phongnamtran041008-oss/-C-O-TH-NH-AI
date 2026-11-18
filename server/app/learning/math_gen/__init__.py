"""Question generators: one function per template, drawing new numbers each time.

A generator is listed in data/math/items/<subject>.json ("generators": id, micro-skill,
tier, type, reviewed) and its function is registered here under the same id:

    @generator("dstt_g1_giao")
    def giao(rng: random.Random) -> Draw: ...

The function uses only the rng it is given, so one seed always gives the same question.
`Draw.params` holds the numbers that were drawn, in plain JSON types: they become the
"numbers" part of the question's fingerprint (anti-repeat), and tools/math_verify.py
recomputes the answer from them with sympy, independently of the arithmetic done here.

Text rules are those of hand-written items: Vietnamese, math ASCII-safe (x^2, A x B, 2 . 3).
"""
from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass, field
from fractions import Fraction


@dataclass
class Draw:
    params: dict
    prompt_vi: str
    answer: object                        # bool | option index | numeric text
    solution_vi: list[str]
    options_vi: list[str] = field(default_factory=list)
    unordered: bool = False
    matrices: dict[str, list[list]] = field(default_factory=dict)


REGISTRY: dict[str, Callable[[random.Random], Draw]] = {}


def generator(gid: str):
    def register(fn):
        if gid in REGISTRY:
            raise ValueError(f"generator {gid} is registered twice")
        REGISTRY[gid] = fn
        return fn
    return register


# ------------------------------------------------------------------ writing math as text
def num(x) -> str:
    """A whole number or a fraction a/b."""
    f = Fraction(x)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def nums(xs) -> str:
    """Numbers as a typed answer: 1, 2, 3."""
    return ", ".join(num(x) for x in xs)


def paren(x) -> str:
    """A number ready to be multiplied or subtracted: negatives and fractions in brackets."""
    s = num(x)
    return f"({s})" if s.startswith("-") or "/" in s else s


def set_text(xs) -> str:
    return "{" + ", ".join(num(x) for x in xs) + "}"


def vec_text(xs) -> str:
    return "(" + ", ".join(num(x) for x in xs) + ")"


def linear_text(a, b, var: str = "x") -> str:
    """ax + b written the usual way: 2x + 1, -x - 3, x, 4."""
    a, b = Fraction(a), Fraction(b)
    if a == 0:
        return num(b)
    head = {1: var, -1: f"-{var}"}.get(a, f"{num(a)}{var}")
    if b == 0:
        return head
    return f"{head} {'+' if b > 0 else '-'} {num(abs(b))}"


def complex_text(re, im) -> str:
    """a + bi written the usual way: 3 - 2i, -i, 4i, 5, 0."""
    re, im = Fraction(re), Fraction(im)
    if im == 0:
        return num(re)
    mag = abs(im)
    unit = "i" if mag == 1 else (f"{num(mag)}i" if mag.denominator == 1 else f"({num(mag)})i")
    if re == 0:
        return unit if im > 0 else f"-{unit}"
    return f"{num(re)} {'+' if im > 0 else '-'} {unit}"


def sample_distinct(rng: random.Random, lo: int, hi: int, k: int) -> list[int]:
    """k different whole numbers from lo..hi, in increasing order."""
    return sorted(rng.sample(range(lo, hi + 1), k))


def nonzero(rng: random.Random, lo: int, hi: int) -> int:
    return rng.choice([v for v in range(lo, hi + 1) if v != 0])


def matrix(rng: random.Random, rows: int, cols: int, lo: int = -5, hi: int = 9) -> list[list[int]]:
    return [[rng.randint(lo, hi) for _ in range(cols)] for _ in range(rows)]


from . import dstt_floor1, dstt_floor2, dstt_floor3  # noqa: E402,F401  (register their generators)
from . import gt_floor1, gt_floor2, gt_floor3        # noqa: E402,F401  (M11: Giải Tích)
from . import xs_floor1, xs_floor2, xs_floor3        # noqa: E402,F401  (M11: Xác Suất và Thống Kê)
from . import tr_floor1, tr_floor2, tr_floor3        # noqa: E402,F401  (M11: Tối Ưu và Toán Rời Rạc)
