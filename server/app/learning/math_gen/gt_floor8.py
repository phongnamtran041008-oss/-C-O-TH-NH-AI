"""Giải Tích, tầng 8 (diện tích, thể tích tròn xoay, độ dài cung, tích phân suy rộng, tiêu
chuẩn hội tụ): generators. Ids start with `gt_g8_`.

The answers come from the closed forms of the textbook cases (area under a parabola between
its roots |a|(s - r)^3/6, the p-integrals, the power rule); tools/math_verify_gt_t7.py
integrates the same integrands with sympy, improper ones with an infinite bound."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, nonzero, num, paren
from .gt_floor1 import factor_text, poly_text, root_poly

POWERS = {"1/2": Fraction(1, 2), "1/3": Fraction(1, 3), "2/3": Fraction(2, 3)}


def _pow(base: str, e) -> str:
    """base^e without the noise: x, x^4, x^(1/2)."""
    e = Fraction(e)
    if e == 1:
        return base
    return f"{base}^{num(e)}" if e.denominator == 1 else f"{base}^({num(e)})"


def _mono(c, e, base: str = "x") -> str:
    return _pow(base, e) if c == 1 else f"{c}{_pow(base, e)}"


# ------------------------------------------------------------------ diện tích
@generator("gt_g8_dien_tich")
def dien_tich(rng: random.Random) -> Draw:
    a = nonzero(rng, -3, 3)
    r = rng.randint(-3, 2)
    s = r + rng.randint(1, 4)
    coeffs = [a * c for c in root_poly(r, s)]
    w = s - r
    value = Fraction(abs(a) * w ** 3, 6)
    return Draw(
        params={"coeffs": coeffs},
        prompt_vi=f"Tính diện tích miền giới hạn bởi parabol y = {poly_text(coeffs)} và trục Ox.",
        answer=num(value),
        solution_vi=[f"Parabol cắt Ox tại x = {r} và x = {s}; giữa hai điểm đó nó nằm "
                     f"{'dưới' if a > 0 else 'trên'} trục Ox.",
                     f"S = |tích phân từ {r} đến {s} của {paren(a)}{factor_text(r)}{factor_text(s)} dx|.",
                     f"Với mọi parabol a(x - r)(x - s): tích phân từ r đến s bằng -a(s - r)^3/6, nên S = |a|(s - r)^3/6.",
                     f"S = {abs(a)} . {w}^3 / 6 = {num(value)}."])


# ------------------------------------------------------------------ thể tích tròn xoay
@generator("gt_g8_the_tich")
def the_tich(rng: random.Random) -> Draw:
    c = rng.randint(1, 3)
    d = rng.randint(1, 2)
    m = rng.choice(["1/2", "1", "2", "3"])
    e = Fraction(m)
    value = Fraction(c * c) * Fraction(d) ** (2 * e + 1) / (2 * e + 1)
    lead = "" if c == 1 else f"{c}"
    curve = f"{lead}{' ' if c != 1 else ''}sqrt(x)" if m == "1/2" else (f"{lead}x" if m == "1" else f"{lead}x^{m}")
    return Draw(
        params={"c": c, "d": d, "m": m},
        prompt_vi=(f"Quay miền giới hạn bởi y = {curve}, trục Ox và đường thẳng x = {d} quanh trục Ox. "
                   "Thể tích bằng k . pi. Tìm k."),
        answer=num(value),
        solution_vi=[f"Mặt cắt tại x là hình tròn bán kính y, diện tích pi . y^2 = pi . {_mono(c * c, 2 * e)}.",
                     f"V = pi . tích phân từ 0 đến {d} của {_mono(c * c, 2 * e)} dx = pi . {c * c} . {_pow(str(d), 2 * e + 1)} / {num(2 * e + 1)}.",
                     f"k = {num(value)}."])


# ------------------------------------------------------------------ độ dài cung
@generator("gt_g8_do_dai")
def do_dai(rng: random.Random) -> Draw:
    p, q = sorted(rng.sample(range(1, 7), 2))
    a, b = p * p - 1, q * q - 1
    value = Fraction(2 * (q ** 3 - p ** 3), 3)
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=f"Tính độ dài cung y = (2/3) x^(3/2) với {a} <= x <= {b}.",
        answer=num(value),
        solution_vi=["y' = x^(1/2), nên 1 + (y')^2 = 1 + x.",
                     f"L = tích phân từ {a} đến {b} của sqrt(1 + x) dx = [(2/3)(1 + x)^(3/2)] từ {a} đến {b}.",
                     f"1 + {b} = {q}^2 và 1 + {a} = {p}^2, nên L = (2/3)({q ** 3} - {p ** 3}) = {num(value)}."])


# ------------------------------------------------------------------ cận vô hạn
@generator("gt_g8_suy_rong")
def suy_rong(rng: random.Random) -> Draw:
    kind = rng.choice(["power", "power", "exp"])
    c = rng.randint(1, 6)
    if kind == "power":
        a = rng.randint(1, 3)
        n = rng.randint(2, 4)
        value = Fraction(c, (n - 1) * a ** (n - 1))
        return Draw(
            params={"kind": kind, "c": c, "a": a, "n": n},
            prompt_vi=f"Tính tích phân từ {a} đến +vô cùng của {c}/x^{n} dx.",
            answer=num(value),
            solution_vi=[f"Tích phân từ {a} đến R của {c}x^(-{n}) dx = [{c} . x^(-{n - 1}) / ({1 - n})] từ {a} đến R.",
                         f"= {num(Fraction(c, n - 1))} . (1/{_pow(str(a), n - 1)} - 1/{_pow('R', n - 1)}).",
                         f"Khi R -> +vô cùng, 1/{_pow('R', n - 1)} -> 0: tích phân hội tụ và bằng {num(value)}."])
    k = rng.randint(1, 3)
    value = Fraction(c, k * k)
    ek = "e^(-x)" if k == 1 else f"e^(-{k}x)"
    return Draw(
        params={"kind": kind, "c": c, "k": k},
        prompt_vi=f"Tính tích phân từ 0 đến +vô cùng của {'' if c == 1 else c}x {ek} dx.",
        answer=num(value),
        solution_vi=[f"Từng phần với u = x, dv = {ek} dx: một nguyên hàm của x {ek} là -(x/{k} + 1/{k * k}) {ek}.",
                     f"Tích phân từ 0 đến R = 1/{k * k} - (R/{k} + 1/{k * k}) e^(-{k}R), và R e^(-{k}R) -> 0.",
                     f"Nhân với {c}: {num(value)}."])


# ------------------------------------------------------------------ hàm không bị chặn
@generator("gt_g8_loai_2")
def loai_2(rng: random.Random) -> Draw:
    p = rng.choice(list(POWERS))
    e = POWERS[p]
    m = rng.randint(1, 3)
    b = m ** 2 if p == "1/2" else m ** 3
    c = rng.randint(1, 4)
    power = {"1/2": m, "1/3": m * m, "2/3": m}[p]   # b^(1 - p): sqrt(m^2), cbrt(m^3)^2, cbrt(m^3)
    value = Fraction(c * power) / (1 - e)
    shown = "sqrt(x)" if p == "1/2" else f"x^({p})"
    return Draw(
        params={"p": p, "b": b, "c": c},
        prompt_vi=f"Tính tích phân từ 0 đến {b} của {c}/{shown} dx (hàm không bị chặn gần 0).",
        answer=num(value),
        solution_vi=[f"Xét tích phân từ a đến {b} với a -> 0+. Nguyên hàm của x^(-{p}) là x^({num(1 - e)}) / ({num(1 - e)}).",
                     f"a^({num(1 - e)}) -> 0 vì số mũ dương, nên tích phân hội tụ.",
                     f"Giá trị: {c} . {b}^({num(1 - e)}) / ({num(1 - e)}) = {c} . {power} / ({num(1 - e)}) = {num(value)}."])


# ------------------------------------------------------------------ tiêu chuẩn hội tụ
@generator("gt_g8_hoi_tu_tf")
def hoi_tu_tf(rng: random.Random) -> Draw:
    m = rng.randint(0, 3)
    n = m + rng.randint(1, 3)
    ok = n - m > 1
    top = "1" if m == 0 else ("x" if m == 1 else f"x^{m}")
    cmp = "1/x" if n - m == 1 else f"1/x^{n - m}"
    xn = "x" if n == 1 else f"x^{n}"
    return Draw(
        params={"m": m, "n": n},
        prompt_vi=f"Tích phân từ 1 đến +vô cùng của {top}/({xn} + 1) dx hội tụ.",
        answer=ok,
        solution_vi=[f"Khi x -> +vô cùng: {top}/({xn} + 1) ~ {cmp} (tỉ số của chúng dần tới 1).",
                     f"Theo tiêu chuẩn so sánh giới hạn, tích phân hội tụ khi và chỉ khi tích phân của {cmp} hội tụ, tức {n - m} > 1.",
                     f"{n - m} {'>' if ok else '<='} 1: tích phân {'hội tụ, mệnh đề đúng' if ok else 'phân kỳ, mệnh đề sai'}."])
