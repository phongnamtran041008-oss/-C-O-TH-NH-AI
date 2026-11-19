"""Giải Tích, tầng 5 (định lý giá trị trung bình, Taylor, L'Hospital): generators. Ids start
with `gt_g5_`.

A limit whose value is e^k is asked as "giới hạn bằng e^k, tìm k", so every answer stays a
whole number or a fraction."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from . import Draw, generator, linear_text, nonzero, num, paren
from .gt_floor1 import poly_text, value_at


def _binom(alpha: Fraction, k: int) -> Fraction:
    """alpha (alpha - 1) ... (alpha - k + 1) / k! for any fraction alpha."""
    out = Fraction(1)
    for j in range(k):
        out *= (alpha - j)
    return out / math.factorial(k)


def _c(a) -> str:
    """A coefficient written in front of a function: 3sin, -sin, sin."""
    return {1: "", -1: "-"}.get(a, str(a))


def _pw(base: str, e: int) -> str:
    return base if e == 1 else f"{base}^{e}"


def _ax(a, var: str = "x") -> str:
    return linear_text(a, 0, var)


# ------------------------------------------------------------------ Rolle, Lagrange, Cauchy
@generator("gt_g5_lagrange")
def lagrange(rng: random.Random) -> Draw:
    kind = rng.choice(["quad", "inv"])
    if kind == "quad":
        p, q, r = nonzero(rng, -3, 3), rng.randint(-5, 5), rng.randint(-6, 6)
        u = rng.randint(-4, 3)
        v = rng.randint(u + 1, 5)
        c = Fraction(u + v, 2)
        slope = Fraction(value_at([p, q, r], v) - value_at([p, q, r], u), v - u)
        return Draw(
            params={"kind": kind, "coeffs": [p, q, r], "u": u, "v": v},
            prompt_vi=(f"Áp dụng định lý Lagrange cho f(x) = {poly_text([p, q, r])} trên đoạn [{u}, {v}]. "
                       f"Tìm điểm c thuộc ({u}, {v}) mà định lý nói tới."),
            answer=num(c),
            solution_vi=[f"Cần c với f'(c) = (f({v}) - f({u})) / ({v} - {paren(u)}).",
                         f"f({v}) = {num(value_at([p, q, r], v))}, f({u}) = {num(value_at([p, q, r], u))}, "
                         f"nên vế phải bằng {num(slope)}.",
                         f"f'(c) = {2 * p}c + {paren(q)} = {num(slope)} cho c = {num(c)}, đúng là trung điểm của đoạn.",
                         f"c = {num(c)} nằm trong ({u}, {v})."])
    p, q = sorted(rng.sample(range(1, 5), 2))
    d = rng.randint(1, 3)
    u, v = d * p * p, d * q * q
    c = d * p * q
    return Draw(
        params={"kind": kind, "u": u, "v": v},
        prompt_vi=(f"Áp dụng định lý Lagrange cho f(x) = 1/x trên đoạn [{u}, {v}]. "
                   f"Tìm điểm c thuộc ({u}, {v}) mà định lý nói tới."),
        answer=str(c),
        solution_vi=[f"f liên tục trên [{u}, {v}] và khả vi trên ({u}, {v}) vì 0 không nằm trong đoạn.",
                     f"(f({v}) - f({u})) / ({v} - {u}) = (1/{v} - 1/{u}) / {v - u} = -1 / ({u} . {v}) = "
                     f"{num(Fraction(-1, u * v))}.",
                     f"f'(c) = -1/c^2, nên c^2 = {u} . {v} = {u * v}.",
                     f"c > 0 nên c = {c}, và {c} nằm trong ({u}, {v})."])


@generator("gt_g5_rolle_tf")
def rolle_tf(rng: random.Random) -> Draw:
    u = rng.randint(-5, 2)
    v = rng.randint(u + 1, 5)
    ok = rng.random() < 0.5
    b = -(u + v) if ok else -(u + v) + nonzero(rng, -3, 3)
    c = rng.randint(-6, 6)
    coeffs = [1, b, c]
    fu, fv = value_at(coeffs, u), value_at(coeffs, v)
    steps = ["Định lý Rolle cần: f liên tục trên [a, b], khả vi trên (a, b), và f(a) = f(b).",
             f"f là đa thức nên hai điều đầu luôn đúng. Còn lại: f({u}) = {num(fu)}, f({v}) = {num(fv)}."]
    steps.append("Hai giá trị bằng nhau: f thỏa mọi giả thiết, mệnh đề đúng." if ok else
                 "Hai giá trị khác nhau: thiếu giả thiết f(a) = f(b), mệnh đề sai.")
    return Draw(
        params={"coeffs": coeffs, "u": u, "v": v},
        prompt_vi=f"Hàm f(x) = {poly_text(coeffs)} thỏa mọi giả thiết của định lý Rolle trên đoạn [{u}, {v}].",
        answer=ok, solution_vi=steps)


@generator("gt_g5_cauchy")
def cauchy(rng: random.Random) -> Draw:
    u = rng.randint(1, 5)
    v = rng.randint(u + 1, 8)
    c = Fraction(2 * (u * u + u * v + v * v), 3 * (u + v))
    ratio = Fraction(v ** 3 - u ** 3, v * v - u * u)
    return Draw(
        params={"u": u, "v": v},
        prompt_vi=(f"Áp dụng định lý Cauchy cho f(x) = x^3 và g(x) = x^2 trên đoạn [{u}, {v}]. "
                   f"Tìm điểm c thuộc ({u}, {v}) mà định lý nói tới."),
        answer=num(c),
        solution_vi=["Cần c với (f(b) - f(a)) / (g(b) - g(a)) = f'(c) / g'(c), và g'(x) = 2x khác 0 trên khoảng.",
                     f"Vế trái: ({v ** 3} - {u ** 3}) / ({v * v} - {u * u}) = {num(ratio)}.",
                     "Vế phải: 3c^2 / (2c) = 3c/2.",
                     f"3c/2 = {num(ratio)} cho c = {num(c)}, nằm trong ({u}, {v})."])


# ------------------------------------------------------------------ Taylor
@generator("gt_g5_taylor_he_so")
def taylor_he_so(rng: random.Random) -> Draw:
    coeffs = [nonzero(rng, -3, 3), rng.randint(-5, 5), rng.randint(-6, 6), rng.randint(-9, 9)]
    a = nonzero(rng, -2, 2)
    k = rng.randint(1, 3)
    # coefficient of (x - a)^k: sum over the powers j >= k of c_j . C(j, k) . a^(j - k)
    value = sum(Fraction(c) * math.comb(3 - n, k) * Fraction(a) ** (3 - n - k)
                for n, c in enumerate(coeffs) if 3 - n >= k)
    power = "(x - " + str(a) + ")" if a > 0 else f"(x + {-a})"
    return Draw(
        params={"coeffs": coeffs, "a": a, "k": k},
        prompt_vi=(f"Khai triển Taylor của p(x) = {poly_text(coeffs)} quanh x = {a}. Tìm hệ số của "
                   f"{power}^{k}." if k > 1 else
                   f"Khai triển Taylor của p(x) = {poly_text(coeffs)} quanh x = {a}. Tìm hệ số của {power}."),
        answer=num(value),
        solution_vi=[f"Hệ số của {power}^{k} là p^({k})({a}) / {k}!.",
                     "Lấy đạo hàm p đủ " + str(k) + " lần rồi thay x = " + str(a) + ".",
                     f"Được p^({k})({a}) = {num(value * math.factorial(k))}, chia cho {math.factorial(k)} "
                     f"ra {num(value)}."])


@generator("gt_g5_taylor_ln")
def taylor_ln(rng: random.Random) -> Draw:
    kind = rng.choice(["ln", "inv"])
    a = rng.randint(1, 4)
    k = rng.randint(2, 4)
    if kind == "ln":
        value = Fraction((-1) ** (k + 1), k * a ** k)
        name = "ln x"
        rule = (f"f^(k)(x) = (-1)^(k + 1) (k - 1)! / x^k, nên hệ số = f^(k)({a}) / k! = "
                f"(-1)^(k + 1) / (k . {a}^k).")
    else:
        value = Fraction((-1) ** k, a ** (k + 1))
        name = "1/x"
        rule = f"f^(k)(x) = (-1)^k k! / x^(k + 1), nên hệ số = f^(k)({a}) / k! = (-1)^k / {a}^(k + 1)."
    power = f"(x - {a})^{k}"
    return Draw(
        params={"kind": kind, "a": a, "k": k},
        prompt_vi=f"Khai triển Taylor của f(x) = {name} quanh x = {a}. Tìm hệ số của {power}.",
        answer=num(value),
        solution_vi=[f"Hệ số của {power} là f^({k})({a}) / {k}!.",
                     rule,
                     f"Với k = {k}: hệ số bằng {num(value)}."])


# ------------------------------------------------------------------ Maclaurin
def _series(kind: str, a, n: int) -> list[Fraction]:
    """The first n + 1 Maclaurin coefficients of one basic function."""
    if kind == "exp":
        return [Fraction(a) ** k / math.factorial(k) for k in range(n + 1)]
    if kind == "ln":
        return [Fraction(0)] + [Fraction((-1) ** (k + 1)) * Fraction(a) ** k / k for k in range(1, n + 1)]
    if kind == "sin":
        return [Fraction(0) if k % 2 == 0 else Fraction((-1) ** (k // 2)) * Fraction(a) ** k / math.factorial(k)
                for k in range(n + 1)]
    if kind == "cos":
        return [Fraction((-1) ** (k // 2)) * Fraction(a) ** k / math.factorial(k) if k % 2 == 0 else Fraction(0)
                for k in range(n + 1)]
    if kind == "pow":                       # (1 + x)^a with a a fraction
        return [_binom(Fraction(a), k) for k in range(n + 1)]
    raise ValueError(kind)


def _name(kind: str, a) -> str:
    if kind == "exp":
        return f"e^({_ax(a)})" if a != 1 else "e^x"
    if kind == "ln":
        return f"ln(1 + {_ax(a)})" if a > 0 else f"ln(1 - {_ax(-a)})"
    if kind in ("sin", "cos"):
        return f"{kind}({_ax(a)})" if a != 1 else f"{kind} x"
    return f"(1 + x)^({num(a)})"


_RULE = {"exp": "e^u = 1 + u + u^2/2! + u^3/3! + ...",
         "ln": "ln(1 + u) = u - u^2/2 + u^3/3 - ...",
         "sin": "sin u = u - u^3/3! + u^5/5! - ...",
         "cos": "cos u = 1 - u^2/2! + u^4/4! - ...",
         "pow": "(1 + x)^a = 1 + a x + a(a - 1)/2! x^2 + a(a - 1)(a - 2)/3! x^3 + ..."}


@generator("gt_g5_maclaurin")
def maclaurin(rng: random.Random) -> Draw:
    kind = rng.choice(["exp", "ln", "sin", "cos", "pow"])
    if kind == "pow":
        a = rng.choice([Fraction(1, 2), Fraction(-1, 2), Fraction(1, 3), Fraction(-1, 3), Fraction(3, 2), Fraction(-2)])
        k = rng.randint(2, 3)
    else:
        a = nonzero(rng, -3, 3)
        k = {"sin": rng.choice([3, 5]), "cos": rng.choice([2, 4])}.get(kind, rng.randint(2, 4))
    value = _series(kind, a, k)[k]
    return Draw(
        params={"kind": kind, "a": [Fraction(a).numerator, Fraction(a).denominator], "k": k},
        prompt_vi=f"Tìm hệ số của x^{k} trong khai triển Maclaurin của f(x) = {_name(kind, a)}.",
        answer=num(value),
        solution_vi=[f"Dùng khai triển {_RULE[kind]}" + ("." if kind == "pow" else f" với u = {_ax(a)}."),
                     (f"Số hạng chứa x^{k} là a(a - 1)...(a - {k - 1}) / {k}! . x^{k} với a = {num(a)}."
                      if kind == "pow" else
                      f"Số hạng chứa x^{k} đến từ u^{k} = {paren(a)}^{k} x^{k} = {poly_text([Fraction(a) ** k] + [0] * k)}."),
                     f"Hệ số của x^{k} là {num(value)}."])


@generator("gt_g5_maclaurin_tich")
def maclaurin_tich(rng: random.Random) -> Draw:
    a = nonzero(rng, -2, 2)
    other = rng.choice(["poly", "ln", "sin"])
    b = nonzero(rng, -2, 2)
    k = rng.randint(2, 4)
    left = _series("exp", a, k)
    if other == "poly":
        m = rng.randint(1, 3)
        right = [Fraction(math.comb(m, j)) * Fraction(b) ** j if j <= m else Fraction(0) for j in range(k + 1)]
        name = f"(1 + {_ax(b)})^{m}" if b > 0 else f"(1 - {_ax(-b)})^{m}"
        params = {"a": a, "other": other, "b": b, "m": m, "k": k}
    else:
        right = _series(other, b, k)
        name = _name(other, b)
        params = {"a": a, "other": other, "b": b, "k": k}
    value = sum(left[j] * right[k - j] for j in range(k + 1))
    terms = [f"{paren(left[j])} . {paren(right[k - j])}" for j in range(k + 1) if left[j] and right[k - j]]
    return Draw(
        params=params,
        prompt_vi=f"Tìm hệ số của x^{k} trong khai triển Maclaurin của f(x) = {_name('exp', a)} . {name}.",
        answer=num(value),
        solution_vi=[f"Khai triển từng thừa số tới x^{k}, rồi nhân: hệ số của x^{k} là tổng các tích "
                     f"(hệ số x^j của thừa số đầu) . (hệ số x^({k} - j) của thừa số sau).",
                     f"Hệ số của {_name('exp', a)}: " + ", ".join(num(c) for c in left) + f" (từ x^0 tới x^{k}).",
                     f"Hệ số của {name}: " + ", ".join(num(c) for c in right) + ".",
                     "Cộng các tích: " + (" + ".join(terms) if terms else "0") + f" = {num(value)}."])


# ------------------------------------------------------------------ L'Hospital
@generator("gt_g5_lhospital")
def lhospital(rng: random.Random) -> Draw:
    kind = rng.choice(["poly", "exp_sin", "ln_tan"])
    if kind == "poly":
        c = rng.choice([-2, -1, 1, 2])
        n, m = rng.sample(range(2, 6), 2)
        value = Fraction(n, m) * Fraction(c) ** (n - m)
        cn, cm = c ** n, c ** m
        return Draw(
            params={"kind": kind, "c": c, "n": n, "m": m},
            prompt_vi=(f"Tính giới hạn của ({poly_text([1] + [0] * (n - 1) + [-cn])}) / "
                       f"({poly_text([1] + [0] * (m - 1) + [-cm])}) khi x -> {c}."),
            answer=num(value),
            solution_vi=[f"Thay x = {c}: tử và mẫu đều bằng 0, dạng 0/0.",
                         f"L'Hospital: giới hạn bằng giới hạn của {n}{_pw('x', n - 1)} / ({m}{_pw('x', m - 1)}).",
                         f"Thay x = {c}: {n} . {_pw(paren(c), n - 1)} / ({m} . {_pw(paren(c), m - 1)}) = {num(value)}."])
    a, b = nonzero(rng, -5, 5), nonzero(rng, -5, 5)
    value = Fraction(a, b)
    if kind == "exp_sin":
        top, bottom, dtop, dbottom = f"e^({_ax(a)}) - 1", f"sin({_ax(b)})", f"{_c(a)}e^({_ax(a)})", f"{_c(b)}cos({_ax(b)})"
    else:
        top = f"ln(1 + {_ax(a)})" if a > 0 else f"ln(1 - {_ax(-a)})"
        bottom = f"tan({_ax(b)})"
        dtop, dbottom = f"{a} / (1 + {_ax(a)})" if a > 0 else f"{a} / (1 - {_ax(-a)})", f"{b} / cos^2({_ax(b)})"
    return Draw(
        params={"kind": kind, "a": a, "b": b},
        prompt_vi=f"Tính giới hạn của ({top}) / {bottom} khi x -> 0.",
        answer=num(value),
        solution_vi=["Thay x = 0: tử và mẫu đều bằng 0, dạng 0/0.",
                     f"L'Hospital: lấy đạo hàm riêng tử và riêng mẫu: ({dtop}) / ({dbottom}).",
                     f"Thay x = 0: {a} / {paren(b)} = {num(value)}."])


@generator("gt_g5_lhospital_bac2")
def lhospital_bac2(rng: random.Random) -> Draw:
    kind = rng.choice(["exp", "cos", "sin", "ln"])
    a = nonzero(rng, -4, 4)
    b = nonzero(rng, -3, 3) if kind == "cos" else 1
    minus_ax = f"- {_ax(a)}" if a > 0 else f"+ {_ax(-a)}"          # "- 3x" or "+ 3x"
    if kind == "exp":
        text, value = f"(e^({_ax(a)}) - 1 {minus_ax}) / x^2", Fraction(a * a, 2)
        steps = [f"Lần 1: ({_c(a)}e^({_ax(a)}) - {paren(a)}) / (2x), vẫn 0/0.",
                 f"Lần 2: {_c(a * a)}e^({_ax(a)}) / 2 -> {num(value)}."]
    elif kind == "cos":
        text, value = f"(1 - cos({_ax(a)})) / ({poly_text([b, 0, 0])})", Fraction(a * a, 2 * b)
        steps = [f"Lần 1: {_c(a)}sin({_ax(a)}) / ({2 * b}x), vẫn 0/0.",
                 f"Lần 2: {_c(a * a)}cos({_ax(a)}) / {paren(2 * b)} -> {num(value)}."]
    elif kind == "sin":
        text, value = f"({_ax(a)} - sin({_ax(a)})) / x^3", Fraction(a ** 3, 6)
        steps = [f"Lần 1: ({a} - {_c(a)}cos({_ax(a)})) / (3x^2), vẫn 0/0.",
                 f"Lần 2: {_c(a * a)}sin({_ax(a)}) / (6x), vẫn 0/0.",
                 f"Lần 3: {_c(a ** 3)}cos({_ax(a)}) / 6 -> {num(value)}."]
    else:
        inner = f"1 + {_ax(a)}" if a > 0 else f"1 - {_ax(-a)}"
        text, value = f"(ln({inner}) {minus_ax}) / x^2", Fraction(-a * a, 2)
        steps = [f"Lần 1: ({a}/({inner}) - {paren(a)}) / (2x), vẫn 0/0.",
                 f"Lần 2: ({-a * a}/({inner})^2) / 2 -> {num(value)}."]
    return Draw(
        params={"kind": kind, "a": a, "b": b},
        prompt_vi=f"Tính giới hạn của {text} khi x -> 0.",
        answer=num(value),
        solution_vi=["Thay x = 0 được dạng 0/0; lấy đạo hàm riêng tử và riêng mẫu cho tới khi hết dạng 0/0."] + steps)


# ------------------------------------------------------------------ dạng vô định khác
@generator("gt_g5_vo_dinh_tich")
def vo_dinh_tich(rng: random.Random) -> Draw:
    kind = rng.choice(["sin", "ln", "cot"])
    a = nonzero(rng, -6, 6) if kind != "ln" else rng.randint(1, 9)
    if kind == "sin":
        text, at, value = f"x . sin({num(a)}/x)", "+vô cùng", Fraction(a)
        steps = [f"Dạng vô cùng . 0. Đặt t = 1/x -> 0+: x . sin({num(a)}/x) = sin({_ax(a, 't')}) / t.",
                 f"Dạng 0/0; L'Hospital: {_c(a)}cos({_ax(a, 't')}) / 1 -> {a}."]
    elif kind == "ln":
        text, at, value = f"x . (ln(x + {a}) - ln x)", "+vô cùng", Fraction(a)
        steps = [f"Dạng vô cùng . 0: viết thành ln(1 + {a}/x) / (1/x), dạng 0/0.",
                 f"L'Hospital: tử có đạo hàm (-{a}/x^2) / (1 + {a}/x), mẫu có đạo hàm -1/x^2.",
                 f"Thương bằng {a} / (1 + {a}/x) -> {a}."]
    else:
        text, at, value = f"x . cot({_ax(a)})", "0", Fraction(1, a)
        steps = [f"Dạng 0 . vô cùng: viết thành x / tan({_ax(a)}), dạng 0/0.",
                 f"L'Hospital: 1 / ({a} / cos^2({_ax(a)})) -> 1/{paren(a)} = {num(value)}."]
    return Draw(
        params={"kind": kind, "a": a},
        prompt_vi=f"Tính giới hạn của {text} khi x -> {at}.",
        answer=num(value),
        solution_vi=["Đưa tích về một thương để có dạng 0/0 hoặc vô cùng/vô cùng."] + steps)


@generator("gt_g5_vo_dinh_mu")
def vo_dinh_mu(rng: random.Random) -> Draw:
    kind = rng.choice(["lin0", "linoo", "cos", "sin"])
    a, b = nonzero(rng, -4, 4), nonzero(rng, -3, 3)
    if kind == "lin0":
        text, at, k = f"(1 + {_ax(a)})^({b}/x)" if a > 0 else f"(1 - {_ax(-a)})^({b}/x)", "0", Fraction(a * b)
        inner = f"1 + {_ax(a)}" if a > 0 else f"1 - {_ax(-a)}"
        ln_step = f"ln của biểu thức = {b} . ln({inner}) / x, và ln({inner}) ~ {_ax(a)}."
    elif kind == "linoo":
        a = abs(a)
        text, at, k = f"(1 + {a}/x)^({_ax(b)})", "+vô cùng", Fraction(a * b)
        ln_step = f"ln của biểu thức = {_ax(b)} . ln(1 + {a}/x), và ln(1 + {a}/x) ~ {a}/x khi x -> +vô cùng."
    elif kind == "cos":
        a = abs(a)
        text, at, k = f"(cos({_ax(a)}))^({b}/x^2)", "0", Fraction(-a * a * b, 2)
        ln_step = (f"ln của biểu thức = {b} . ln(cos({_ax(a)})) / x^2, và ln(cos({_ax(a)})) ~ cos({_ax(a)}) - 1 "
                   f"~ -{a * a}x^2/2.")
    else:
        text, at, k = f"(1 + sin({_ax(a)}))^({b}/x)", "0", Fraction(a * b)
        ln_step = f"ln của biểu thức = {b} . ln(1 + sin({_ax(a)})) / x, và ln(1 + sin({_ax(a)})) ~ sin({_ax(a)}) ~ {_ax(a)}."
    return Draw(
        params={"kind": kind, "a": a, "b": b},
        prompt_vi=f"Giới hạn của {text} khi x -> {at} bằng e^k. Tìm k.",
        answer=num(k),
        solution_vi=["Dạng 1 mũ vô cùng: lấy ln để đưa về tích, rồi về thương.",
                     ln_step,
                     f"Số mũ dần tới {num(k)}, nên giới hạn bằng e^{paren(k)} và k = {num(k)}."])
