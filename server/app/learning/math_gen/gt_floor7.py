"""Giải Tích, tầng 7 (nguyên hàm, đổi biến, từng phần, hàm hữu tỉ, Newton-Leibniz, cận biến
thiên): generators. Ids start with `gt_g7_`.

Every answer is worked out here from a closed-form antiderivative written by hand (so each
number is a fraction, or the rational coefficients of e); tools/math_verify_gt_t7.py
integrates the same integrand with sympy instead."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, nonzero, num, nums, paren
from .gt_floor1 import factor_text, lin_text, poly_text


# ------------------------------------------------------------------ nguyên hàm với điều kiện
@generator("gt_g7_nguyen_ham_dk")
def nguyen_ham_dk(rng: random.Random) -> Draw:
    a = rng.choice([-6, -3, 3, 6, 9])
    b = rng.choice([-4, -2, 0, 2, 4])
    c = nonzero(rng, -4, 4)
    d = rng.randint(-5, 5)
    # F(x) = (a/3)x^3 + (b/2)x^2 - c/x + C, with F(1) = d
    F = lambda t: Fraction(a, 3) * t ** 3 + Fraction(b, 2) * t ** 2 - Fraction(c) / t   # noqa: E731
    C = d - F(Fraction(1))
    value = F(Fraction(2)) + C
    f_text = f"{poly_text([a, b, 0])} {'+' if c > 0 else '-'} {abs(c)}/x^2"
    F_text = f"{poly_text([Fraction(a, 3), Fraction(b, 2), 0, 0])} {'-' if c > 0 else '+'} {abs(c)}/x + C"
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d},
        prompt_vi=f"F là nguyên hàm của f(x) = {f_text} trên (0, +vô cùng) và F(1) = {d}. Tính F(2).",
        answer=num(value),
        solution_vi=[f"Nguyên hàm tổng quát: F(x) = {F_text} (nguyên hàm của 1/x^2 là -1/x).",
                     f"F(1) = {num(F(Fraction(1)))} + C = {d}, nên C = {num(C)}.",
                     f"F(2) = {num(F(Fraction(2)))} + {paren(C)} = {num(value)}."])


# ------------------------------------------------------------------ đổi biến
@generator("gt_g7_doi_bien")
def doi_bien(rng: random.Random) -> Draw:
    k = rng.choice([1, 2, 4])
    m = rng.randint(1, 3)
    p = rng.randint(1, 3)
    n = rng.randint(1, 3)
    hi = m * m + p
    value = Fraction(k * (hi ** (n + 1) - p ** (n + 1)), 2 * (n + 1))
    lead = "" if k == 1 else str(k)
    pw = "" if n == 1 else f"^{n}"
    return Draw(
        params={"k": k, "m": m, "p": p, "n": n},
        prompt_vi=f"Tính tích phân từ 0 đến {m} của {lead}x(x^2 + {p}){pw} dx.",
        answer=num(value),
        solution_vi=[f"Đặt u = x^2 + {p}: du = 2x dx, nên x dx = du/2. Đổi cận: x = 0 thì u = {p}, x = {m} thì u = {hi}.",
                     f"Tích phân = ({num(Fraction(k, 2))}) . tích phân từ {p} đến {hi} của u{pw} du "
                     f"= ({num(Fraction(k, 2))}) . [u^{n + 1}/{n + 1}] từ {p} đến {hi}.",
                     f"= {num(Fraction(k, 2 * (n + 1)))} . ({hi ** (n + 1)} - {p ** (n + 1)}) = {num(value)}."])


# ------------------------------------------------------------------ từng phần
@generator("gt_g7_tung_phan")
def tung_phan(rng: random.Random) -> Draw:
    a = nonzero(rng, -4, 4)
    b = rng.randint(-4, 4)
    # antiderivative (ax + b - a) e^x: at 1 it is b . e, at 0 it is b - a
    p, q = b, a - b
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=(f"Tích phân từ 0 đến 1 của ({lin_text(a, b)}) e^x dx bằng p . e + q với p, q hữu tỉ. "
                   "Nhập p, q theo đúng thứ tự."),
        answer=nums([p, q]),
        solution_vi=[f"Từng phần: u = {lin_text(a, b)}, dv = e^x dx, nên du = {a} dx, v = e^x.",
                     f"Nguyên hàm: ({lin_text(a, b)}) e^x - {paren(a)} e^x = ({lin_text(a, b - a)}) e^x.",
                     f"Tại x = 1: {b} . e. Tại x = 0: {b - a}.",
                     f"Tích phân = {b} . e - {paren(b - a)}: p = {p}, q = {q}."])


# ------------------------------------------------------------------ tách phân thức
@generator("gt_g7_tach_phan_thuc")
def tach_phan_thuc(rng: random.Random) -> Draw:
    r, s = sorted(rng.sample(range(-3, 4), 2))
    A, B = nonzero(rng, -4, 4), nonzero(rng, -4, 4)
    # A/(x - r) + B/(x - s) = ((A + B)x - (A s + B r)) / ((x - r)(x - s))
    top = lin_text(A + B, -(A * s + B * r))
    den = f"{factor_text(r)}{factor_text(s)}"
    return Draw(
        params={"r": r, "s": s, "p": A + B, "q": -(A * s + B * r)},
        prompt_vi=(f"Viết ({top}) / ({den}) = A/{factor_text(r)} + B/{factor_text(s)}. "
                   "Nhập A, B theo đúng thứ tự."),
        answer=nums([A, B]),
        solution_vi=[f"Nhân hai vế với mẫu: {top} = A{factor_text(s)} + B{factor_text(r)}.",
                     f"Thay x = {r}: {num(A * (r - s))} = A . {paren(r - s)}, nên A = {A}.",
                     f"Thay x = {s}: {num(B * (s - r))} = B . {paren(s - r)}, nên B = {B}."])


# ------------------------------------------------------------------ tích phân của trị tuyệt đối
@generator("gt_g7_tri_tuyet_doi")
def tri_tuyet_doi(rng: random.Random) -> Draw:
    k = rng.randint(1, 3)
    s = rng.randint(1, 4)
    b = s + rng.randint(1, 3)
    left = Fraction(k * s ** 3, 6)                                 # k . (s x - x^2) on [0, s]
    right = k * (Fraction(b ** 3 - s ** 3, 3) - Fraction(s * (b * b - s * s), 2))   # k(x^2 - s x) on [s, b]
    value = left + right
    inner = poly_text([k, -k * s, 0])
    return Draw(
        params={"k": k, "s": s, "b": b},
        prompt_vi=f"Tính tích phân từ 0 đến {b} của |{inner}| dx.",
        answer=num(value),
        solution_vi=[f"{inner} = {'' if k == 1 else k}x(x - {s}) âm trên (0, {s}) và dương trên ({s}, {b}): tách tại x = {s}.",
                     f"Tích phân từ 0 đến {s} của -({inner}) dx = {num(left)}.",
                     f"Tích phân từ {s} đến {b} của ({inner}) dx = {num(right)}.",
                     f"Tổng: {num(value)}."])


# ------------------------------------------------------------------ cận biến thiên
@generator("gt_g7_can_bien")
def can_bien(rng: random.Random) -> Draw:
    p = rng.randint(-3, 3)
    q = rng.randint(-3, 3)
    x0 = rng.choice([-2, -1, 1, 2])
    g = lambda t: t * t + p * t + q                                  # noqa: E731
    value = 2 * x0 * g(x0 * x0) - g(x0)
    g_text = poly_text([1, p, q], "t")
    return Draw(
        params={"p": p, "q": q, "x0": x0},
        prompt_vi=f"Cho F(x) = tích phân từ x đến x^2 của ({g_text}) dt. Tính F'({x0}).",
        answer=str(value),
        solution_vi=["Với g(t) là hàm dưới dấu tích phân và G là một nguyên hàm của g: F(x) = G(x^2) - G(x).",
                     "Dây chuyền: F'(x) = g(x^2) . 2x - g(x).",
                     f"g({x0 * x0}) = {g(x0 * x0)} và g({x0}) = {g(x0)}.",
                     f"F'({x0}) = {g(x0 * x0)} . {paren(2 * x0)} - {paren(g(x0))} = {value}."])
