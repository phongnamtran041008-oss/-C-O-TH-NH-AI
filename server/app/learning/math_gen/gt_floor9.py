"""Giải Tích, tầng 9 (hàm nhiều biến; mở rộng AI: gradient, lan truyền ngược): generators.
Ids start with `gt_g9_`. Every question here is tier 5.

A polynomial in x, y is a list of monomials [c, i, j] = c x^i y^j; its partial derivatives
are taken here term by term with the power rule, and quadratic functions are built from the
stationary point they should have. tools/math_verify_gt_t7.py redoes each answer with sympy
(diff, idiff, solve, hessian, a limit for the directional derivative)."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, nonzero, num, nums, paren


# ------------------------------------------------------------------ polynomials in x, y
def mono_text(terms) -> str:
    """[[3, 2, 1], [-2, 1, 1], [1, 0, 3]] -> 3x^2y - 2xy + y^3."""
    out = []
    for c, i, j in terms:
        if c == 0:
            continue
        body = ""
        for var, p in (("x", i), ("y", j)):
            if p == 1:
                body += var
            elif p > 1:
                body += f"{var}^{p}"
        mag = abs(c)
        text = num(mag) if not body else (body if mag == 1 else f"{num(mag)}{body}")
        if not out:
            out.append(f"-{text}" if c < 0 else text)
        else:
            out.append(f"{'-' if c < 0 else '+'} {text}")
    return " ".join(out) if out else "0"


def d_terms(terms, var: str):
    """Partial derivative of a monomial list by the power rule."""
    out = []
    for c, i, j in terms:
        if var == "x" and i > 0:
            out.append([c * i, i - 1, j])
        elif var == "y" and j > 0:
            out.append([c * j, i, j - 1])
    return out


def eval_terms(terms, x, y) -> Fraction:
    return sum((Fraction(c) * Fraction(x) ** i * Fraction(y) ** j for c, i, j in terms), Fraction(0))


def _quadratic(rng: random.Random):
    """A x^2 + B xy + C y^2 + D x + E y with a whole-number stationary point and 4AC != B^2."""
    while True:
        A, C = nonzero(rng, -3, 3), nonzero(rng, -3, 3)
        B = rng.randint(-4, 4)
        if 4 * A * C != B * B:
            break
    x0, y0 = rng.randint(-3, 3), rng.randint(-3, 3)
    D = -(2 * A * x0 + B * y0)
    E = -(B * x0 + 2 * C * y0)
    return A, B, C, D, E, x0, y0


def _quad_terms(A, B, C, D, E):
    return [[A, 2, 0], [B, 1, 1], [C, 0, 2], [D, 1, 0], [E, 0, 1]]


# ------------------------------------------------------------------ đạo hàm riêng
@generator("gt_g9_dao_ham_rieng")
def dao_ham_rieng(rng: random.Random) -> Draw:
    a = nonzero(rng, -3, 3)
    i, j = rng.randint(1, 3), rng.randint(1, 3)
    if (i, j) == (1, 1):                    # keep the monomials apart from the b . xy term
        j = 2
    b = nonzero(rng, -4, 4)
    c = rng.randint(-3, 3)
    terms = [[a, i, j], [b, 1, 1], [c, 0, 2]]
    x0, y0 = rng.choice([-2, -1, 1, 2]), rng.choice([-2, -1, 1, 2])
    kind = rng.choice(["xy", "xx", "yy"])
    first = d_terms(terms, kind[0])
    second = d_terms(first, kind[1])
    value = eval_terms(second, x0, y0)
    note = ", với f_xy = (f_x)_y" if kind == "xy" else ""
    return Draw(
        params={"terms": terms, "kind": kind, "x": x0, "y": y0},
        prompt_vi=f"Cho f(x, y) = {mono_text(terms)}. Tính f_{kind}({x0}, {y0}){note}.",
        answer=num(value),
        solution_vi=[f"f_{kind[0]} = {mono_text(first)} (giữ biến còn lại cố định).",
                     f"f_{kind} = {mono_text(second)}.",
                     f"Tại ({x0}, {y0}): f_{kind} = {num(value)}."])


# ------------------------------------------------------------------ hàm ẩn
@generator("gt_g9_ham_an")
def ham_an(rng: random.Random) -> Draw:
    while True:
        a = rng.randint(-3, 3)
        b = nonzero(rng, -2, 2)
        x0, y0 = nonzero(rng, -2, 2), nonzero(rng, -2, 2)
        Fx, Fy = 2 * x0 + a * y0, a * x0 + 2 * b * y0
        if Fy != 0:
            break
    c = x0 * x0 + a * x0 * y0 + b * y0 * y0
    value = Fraction(-Fx, Fy)
    lhs = mono_text([[1, 2, 0], [a, 1, 1], [b, 0, 2]])
    return Draw(
        params={"a": a, "b": b, "c": c, "x": x0, "y": y0},
        prompt_vi=(f"Phương trình {lhs} = {c} xác định một hàm ẩn y = y(x) gần điểm ({x0}, {y0}). "
                   f"Tính y'({x0})."),
        answer=num(value),
        solution_vi=[f"Với F(x, y) = {lhs} - {paren(c)}: F_x = {mono_text([[2, 1, 0], [a, 0, 1]])}, "
                     f"F_y = {mono_text([[a, 1, 0], [2 * b, 0, 1]])}.",
                     f"Tại ({x0}, {y0}): F_x = {Fx}, F_y = {Fy} (khác 0, nên hàm ẩn tồn tại).",
                     f"y' = -F_x / F_y = {num(value)}."])


# ------------------------------------------------------------------ cực trị
@generator("gt_g9_diem_dung")
def diem_dung(rng: random.Random) -> Draw:
    A, B, C, D, E, x0, y0 = _quadratic(rng)
    terms = _quad_terms(A, B, C, D, E)
    return Draw(
        params={"A": A, "B": B, "C": C, "D": D, "E": E},
        prompt_vi=f"Hàm f(x, y) = {mono_text(terms)} có đúng một điểm dừng (x0, y0). Nhập x0, y0 theo đúng thứ tự.",
        answer=nums([x0, y0]),
        solution_vi=[f"f_x = {mono_text([[2 * A, 1, 0], [B, 0, 1], [D, 0, 0]])} = 0 và "
                     f"f_y = {mono_text([[B, 1, 0], [2 * C, 0, 1], [E, 0, 0]])} = 0.",
                     f"Định thức của hệ: {2 * A} . {paren(2 * C)} - {paren(B)}^2 = {4 * A * C - B * B}, khác 0: nghiệm duy nhất.",
                     f"Giải hệ được x0 = {x0}, y0 = {y0} (thay lại vào hai phương trình để kiểm tra)."])


@generator("gt_g9_cuc_tri_tf")
def cuc_tri_tf(rng: random.Random) -> Draw:
    A, B, C, D, E, x0, y0 = _quadratic(rng)
    terms = _quad_terms(A, B, C, D, E)
    claim = rng.choice(["cực tiểu", "cực đại"])
    det = 4 * A * C - B * B
    kind = "yên ngựa" if det < 0 else ("cực tiểu" if A > 0 else "cực đại")
    return Draw(
        params={"A": A, "B": B, "C": C, "D": D, "E": E, "claim": claim},
        prompt_vi=(f"Điểm ({x0}, {y0}) là điểm dừng duy nhất của f(x, y) = {mono_text(terms)}, "
                   f"và f đạt {claim} địa phương tại đó."),
        answer=kind == claim,
        solution_vi=[f"f_xx = {2 * A}, f_yy = {2 * C}, f_xy = {B} tại mọi điểm.",
                     f"D = f_xx f_yy - f_xy^2 = {4 * A * C} - {B * B} = {det}.",
                     (f"D < 0: điểm yên ngựa, không phải cực trị." if det < 0 else
                      f"D > 0 và f_xx = {2 * A} {'> 0: cực tiểu' if A > 0 else '< 0: cực đại'}."),
                     f"Mệnh đề {'đúng' if kind == claim else 'sai'}."])


# ------------------------------------------------------------------ cực trị có điều kiện
TRIPLES = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (1, 0, 1), (0, 2, 2)]


@generator("gt_g9_lagrange")
def lagrange(rng: random.Random) -> Draw:
    p, q, n = rng.choice(TRIPLES)
    p, q = p * rng.choice([1, -1]), q * rng.choice([1, -1])
    r = rng.randint(1, 3)
    big = r * n
    px, py = Fraction(p * r, n), Fraction(q * r, n)
    f_text = mono_text([[p, 1, 0], [q, 0, 1]])
    return Draw(
        params={"p": p, "q": q, "r": r},
        prompt_vi=f"Tìm GTLN và GTNN của f(x, y) = {f_text} trên đường tròn x^2 + y^2 = {r * r}. Nhập GTLN rồi GTNN.",
        answer=nums([big, -big]),
        solution_vi=[f"Lagrange: ({p}, {q}) = lambda . (2x, 2y), nên (x, y) cùng phương với ({p}, {q}).",
                     f"Trên đường tròn bán kính {r}, độ dài của ({p}, {q}) là {n}: hai điểm ({num(px)}, {num(py)}) và ({num(-px)}, {num(-py)}).",
                     f"f({num(px)}, {num(py)}) = {paren(p)} . {paren(px)} + {paren(q)} . {paren(py)} = {big}; tại điểm đối xứng f = {-big}.",
                     f"GTLN = {big}, GTNN = {-big} (bằng bán kính {r} nhân độ dài {n} của ({p}, {q}), với dấu cộng và trừ)."])


# ------------------------------------------------------------------ gradient, lan truyền ngược
UNITS = [(Fraction(3, 5), Fraction(4, 5)), (Fraction(4, 5), Fraction(-3, 5)), (Fraction(-3, 5), Fraction(4, 5)),
         (Fraction(5, 13), Fraction(12, 13)), (Fraction(0), Fraction(1)), (Fraction(1), Fraction(0)),
         (Fraction(-4, 5), Fraction(-3, 5))]


@generator("gt_g9_dao_ham_huong")
def dao_ham_huong(rng: random.Random) -> Draw:
    a, b, c = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)
    d = rng.randint(-3, 3)
    if a == b == c == 0:
        a = 1
    terms = [[a, 2, 0], [b, 1, 1], [c, 0, 2], [d, 1, 0]]
    x0, y0 = rng.randint(-2, 2), rng.randint(-2, 2)
    u1, u2 = rng.choice(UNITS)
    gx = eval_terms(d_terms(terms, "x"), x0, y0)
    gy = eval_terms(d_terms(terms, "y"), x0, y0)
    value = gx * u1 + gy * u2
    return Draw(
        params={"terms": terms, "x": x0, "y": y0, "u": [[u1.numerator, u1.denominator], [u2.numerator, u2.denominator]]},
        prompt_vi=(f"Cho f(x, y) = {mono_text(terms)}. Tính đạo hàm của f tại ({x0}, {y0}) theo hướng vector đơn vị "
                   f"u = ({num(u1)}, {num(u2)})."),
        answer=num(value),
        solution_vi=[f"grad f = (f_x, f_y) = ({mono_text(d_terms(terms, 'x'))}, {mono_text(d_terms(terms, 'y'))}).",
                     f"Tại ({x0}, {y0}): grad f = ({num(gx)}, {num(gy)}).",
                     f"Đạo hàm theo hướng = grad f . u = {paren(gx)} . {paren(u1)} + {paren(gy)} . {paren(u2)} = {num(value)}."])


@generator("gt_g9_lan_truyen")
def lan_truyen(rng: random.Random) -> Draw:
    while True:
        w, b = nonzero(rng, -3, 3), rng.randint(-3, 3)
        x, t = nonzero(rng, -3, 3), rng.randint(-5, 5)
        z = w * x + b
        if z != t:                          # a zero loss would make every gradient 0
            break
    L = (z - t) ** 2
    g = 2 * (z - t)
    return Draw(
        params={"w": w, "b": b, "x": x, "t": t},
        prompt_vi=(f"Mô hình z = w . x + b với hàm mất mát L = (z - t)^2. Cho w = {w}, b = {b}, x = {x}, t = {t}. "
                   "Lan truyền xuôi rồi ngược: nhập L, dL/dw, dL/db theo đúng thứ tự."),
        answer=nums([L, g * x, g]),
        solution_vi=[f"Xuôi: z = {w} . {paren(x)} + {paren(b)} = {z}, L = ({z} - {paren(t)})^2 = {L}.",
                     f"Ngược: dL/dz = 2(z - t) = {g}; dz/dw = x = {x}, dz/db = 1.",
                     f"Dây chuyền: dL/dw = {g} . {paren(x)} = {g * x}, dL/db = {g}."])
