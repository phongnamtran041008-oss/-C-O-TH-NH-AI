"""Giải Tích: generators added by the curriculum review (see rsdstt_floor1.py for why). Ids start
with `gt_gx_`, all on tier 5 of floors 7-8, where each cell had two hand-written questions and no
generator. Every answer is a fraction or a whole number worked out from a closed form by hand;
tools/math_verify_rasoat.py integrates and differentiates the same expressions with sympy."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, linear_text, nonzero, num, paren


def _poly(coeffs: list[int], var: str = "x") -> str:
    """Highest power first: [1, 0, -3] -> x^2 - 3."""
    parts = []
    n = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        p = n - i
        if c == 0:
            continue
        mag = abs(c)
        body = (str(mag) if p == 0 else (var if mag == 1 else f"{mag}{var}") if p == 1 else
                (f"{var}^{p}" if mag == 1 else f"{mag}{var}^{p}"))
        parts.append(("-" if c < 0 else "+", body))
    if not parts:
        return "0"
    first_sign, first = parts[0]
    text = ("-" if first_sign == "-" else "") + first
    for sign, body in parts[1:]:
        text += f" {sign} {body}"
    return text


@generator("gt_gx_nguyen_ham_hai_lan")
def nguyen_ham_hai_lan(rng: random.Random) -> Draw:
    """Two integrations with two conditions: f'' = a x + b, f'(1) = c, f(0) = d; find f(2)."""
    a = rng.choice([-6, -3, -2, 2, 3, 6, 4])
    b = rng.randint(-4, 4)
    c = rng.randint(-5, 5)
    d = rng.randint(-5, 5)
    c1 = Fraction(c) - Fraction(a, 2) - b               # f'(x) = a x^2/2 + b x + c1
    f2 = Fraction(a, 6) * 8 + Fraction(b, 2) * 4 + c1 * 2 + d
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d},
        prompt_vi=f"Độ dốc f'(x) của một đường cong thỏa f''(x) = {_poly([a, b])}. Biết f'(1) = {c} và f(0) = {d}. "
                  f"Tính f(2).",
        answer=num(f2),
        solution_vi=[f"Nguyên hàm một lần: f'(x) = ({num(Fraction(a, 2))})x^2 + ({b})x + C1.",
                     f"f'(1) = {num(Fraction(a, 2) + b)} + C1 = {c}, nên C1 = {num(c1)}.",
                     f"Nguyên hàm lần hai: f(x) = ({num(Fraction(a, 6))})x^3 + ({num(Fraction(b, 2))})x^2 + ({num(c1)})x + C2, "
                     f"và f(0) = C2 = {d}.",
                     f"f(2) = {paren(Fraction(a, 6) * 8)} + {paren(Fraction(b, 2) * 4)} + {paren(c1 * 2)} + {paren(d)} = {num(f2)}."])


@generator("gt_gx_doi_bien_phan_thuc")
def doi_bien_phan_thuc(rng: random.Random) -> Draw:
    """Substitution u = x^2 + c, in two shapes: x (x^2 + c)^k and x / (x^2 + c)^2, on [0, A]."""
    kind = rng.choice(["luy_thua", "nghich"])
    c = rng.randint(1, 4)
    big = rng.randint(1, 3)
    if kind == "luy_thua":
        k = rng.randint(2, 4)
        value = (Fraction(big * big + c) ** (k + 1) - Fraction(c) ** (k + 1)) / (2 * (k + 1))
        integrand = f"x . (x^2 + {c})^{k}"
        steps = [f"Đặt u = x^2 + {c}, du = 2x dx, nên x dx = du/2. Cận: x = 0 cho u = {c}; x = {big} cho u = {big * big + c}.",
                 f"Tích phân thành (1/2) . tích phân từ {c} đến {big * big + c} của u^{k} du = "
                 f"(1/2) . [u^{k + 1}/{k + 1}].",
                 f"= ({big * big + c}^{k + 1} - {c}^{k + 1})/{2 * (k + 1)} = {num(value)}."]
    else:
        value = Fraction(1, 2) * (Fraction(1, c) - Fraction(1, big * big + c))
        integrand = f"x/(x^2 + {c})^2"
        steps = [f"Đặt u = x^2 + {c}, du = 2x dx. Cận: u chạy từ {c} đến {big * big + c}.",
                 f"Tích phân thành (1/2) . tích phân của u^(-2) du = (1/2) . [-1/u] từ {c} đến {big * big + c}.",
                 f"= (1/2)(1/{c} - 1/{big * big + c}) = {num(value)}."]
    return Draw(
        params={"kind": kind, "c": c, "big": big, "k": k if kind == "luy_thua" else 0},
        prompt_vi=f"Tính tích phân từ 0 đến {big} của {integrand} dx. Nhập kết quả dạng số nguyên hoặc phân số.",
        answer=num(value),
        solution_vi=steps)


@generator("gt_gx_can_bien_thien_chuoi")
def can_bien_thien_chuoi(rng: random.Random) -> Draw:
    """F(x) = integral from x to x^2 of (t^2 + a t + b) dt; F'(x0) by the chain rule."""
    a, b = rng.randint(-3, 3), rng.randint(-3, 3)
    x0 = rng.choice([-2, -1, 1, 2, 3])
    g = lambda t: t * t + a * t + b           # noqa: E731
    dF = 2 * x0 * g(x0 * x0) - g(x0)
    return Draw(
        params={"a": a, "b": b, "x0": x0},
        prompt_vi=f"Cho F(x) = tích phân từ x đến x^2 của ({_poly([1, a, b], 't')}) dt. "
                  f"Tính F'({x0}).",
        answer=str(dF),
        solution_vi=["Với F(x) = tích phân từ u(x) đến v(x) của g(t) dt thì F'(x) = g(v(x)) . v'(x) - g(u(x)) . u'(x).",
                     f"Ở đây u = x, v = x^2, g(t) = {_poly([1, a, b], 't')}: F'(x) = g(x^2) . 2x - g(x) . 1.",
                     f"Tại x = {x0}: g({x0 * x0}) = {g(x0 * x0)}, g({x0}) = {g(x0)}.",
                     f"F'({x0}) = {g(x0 * x0)} . {2 * x0} - {g(x0)} = {dF}."])


@generator("gt_gx_suy_rong_nua_truc")
def suy_rong_nua_truc(rng: random.Random) -> Draw:
    """Improper integrals to +infinity with a closed rational value."""
    kind = rng.choice(["luy_thua", "mu"])
    if kind == "luy_thua":
        a, p, c = rng.randint(1, 3), rng.randint(2, 4), nonzero(rng, -4, 6)
        value = Fraction(c) * Fraction(a) ** (1 - p) / (p - 1)
        return Draw(
            params={"kind": kind, "a": a, "p": p, "c": c},
            prompt_vi=f"Tính tích phân từ {a} đến +vô cùng của {c}/x^{p} dx. Nhập kết quả dạng số nguyên hoặc phân số.",
            answer=num(value),
            solution_vi=[f"Tích phân từ {a} đến M của {c} x^(-{p}) dx = {c} . [x^(-{p - 1})/(-{p - 1})] = "
                         f"{c}/{p - 1} . (1/{a}^{p - 1} - 1/M^{p - 1}).",
                         f"Cho M tiến tới +vô cùng, 1/M^{p - 1} tiến tới 0: tích phân hội tụ.",
                         f"Giá trị: {c}/{p - 1} . 1/{a}^{p - 1} = {num(value)}."])
    k = rng.randint(1, 4)
    big_a, big_b = nonzero(rng, -3, 4), nonzero(rng, -3, 4)
    value = Fraction(big_a, k * k) + Fraction(big_b, k)
    return Draw(
        params={"kind": kind, "k": k, "A": big_a, "B": big_b},
        prompt_vi=f"Tính tích phân từ 0 đến +vô cùng của ({_poly([big_a, big_b])}) . e^(-{k}x) dx. "
                  f"Nhập kết quả dạng số nguyên hoặc phân số.",
        answer=num(value),
        solution_vi=[f"Tích phân từ 0 đến +vô cùng của e^(-{k}x) dx = 1/{k}, và của x . e^(-{k}x) dx = 1/{k}^2 "
                     "(tích phân từng phần, phần ngoài tiến tới 0).",
                     f"Giá trị: {big_a} . 1/{k * k} + {paren(big_b)} . 1/{k} = {num(value)}."])
