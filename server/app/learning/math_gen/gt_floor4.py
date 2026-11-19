"""Giải Tích, tầng 4 (đạo hàm và vi phân): generators. Ids start with `gt_g4_`.

Derivatives are written f'(x), f''(x), f^(n)(x); a limit as "giới hạn của ... khi h -> 0".
Every answer is a whole number or a fraction: the functions are chosen so that the value
asked for is rational (polynomials, quotients, ln of a polynomial, 1/(x + p))."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from . import Draw, generator, linear_text, nonzero, num, nums, paren
from .gt_floor1 import poly_text, value_at


def _pow(base: str, e: int) -> str:
    return base if e == 1 else f"{base}^{e}"


def _derivative(coeffs) -> list:
    """The coefficients of p' (highest power first)."""
    deg = len(coeffs) - 1
    return [c * (deg - k) for k, c in enumerate(coeffs[:-1])] or [0]


# ------------------------------------------------------------------ đạo hàm theo định nghĩa
@generator("gt_g4_ti_so_gia")
def ti_so_gia(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -3, 3), rng.randint(-6, 6)
    x0 = nonzero(rng, -3, 3)
    coeffs = [a, 0, b, 0]
    d =3 * a * x0 * x0 + b
    return Draw(
        params={"a": a, "b": b, "x0": x0},
        prompt_vi=(f"Cho f(x) = {poly_text(coeffs)}. Tính giới hạn của (f({x0} + h) - f({x0})) / h "
                   "khi h -> 0."),
        answer=str(d),
        solution_vi=["Giới hạn này chính là định nghĩa của f'(" + str(x0) + ").",
                     f"Khai triển: f({x0} + h) - f({x0}) = {paren(a)}[({x0} + h)^3 - {paren(x0)}^3] + {paren(b)}h "
                     f"= {paren(a)}(3 . {paren(x0 * x0)} . h + 3 . {paren(x0)} . h^2 + h^3) + {paren(b)}h.",
                     f"Chia cho h rồi cho h -> 0, các số hạng còn h biến mất: "
                     f"{paren(a)} . 3 . {paren(x0 * x0)} + {paren(b)} = {d}.",
                     f"Kiểm tra bằng quy tắc: f'(x) = {poly_text(_derivative(coeffs))}, f'({x0}) = {d}."])


@generator("gt_g4_tiep_tuyen")
def tiep_tuyen(rng: random.Random) -> Draw:
    a, b, c = nonzero(rng, -3, 3), rng.randint(-5, 5), rng.randint(-6, 6)
    x0 = rng.randint(-3, 3)
    coeffs = [a, b, c]
    y0 = value_at(coeffs, x0)
    p = 2 * a * x0 + b
    q = y0 - p * x0
    return Draw(
        params={"coeffs": coeffs, "x0": x0},
        prompt_vi=(f"Tiếp tuyến của đồ thị y = {poly_text(coeffs)} tại điểm có hoành độ x = {x0} có phương "
                   "trình y = px + q. Nhập p, q theo đúng thứ tự."),
        answer=nums([p, q]),
        solution_vi=[f"Tiếp điểm: y({x0}) = {num(y0)}.",
                     f"Hệ số góc là đạo hàm tại {x0}: y' = {poly_text(_derivative(coeffs))}, nên p = y'({x0}) = {p}.",
                     f"Tiếp tuyến y = {paren(p)}(x - {paren(x0)}) + {paren(y0)} = {linear_text(p, q)}.",
                     f"Vậy p = {p}, q = {num(q)}."])


# ------------------------------------------------------------------ quy tắc tính
@generator("gt_g4_da_thuc")
def da_thuc(rng: random.Random) -> Draw:
    coeffs = [nonzero(rng, -4, 4), rng.randint(-6, 6), rng.randint(-9, 9), rng.randint(-9, 9)]
    k = rng.randint(-3, 3)
    d = _derivative(coeffs)
    value = value_at(d, k)
    return Draw(
        params={"coeffs": coeffs, "x": k},
        prompt_vi=f"Cho f(x) = {poly_text(coeffs)}. Tính f'({k}).",
        answer=num(value),
        solution_vi=["Đạo hàm từng số hạng: (x^n)' = n . x^(n - 1), hằng số có đạo hàm 0.",
                     f"f'(x) = {poly_text(d)}.",
                     f"f'({k}) = {num(value)}."])


@generator("gt_g4_thuong")
def thuong(rng: random.Random) -> Draw:
    while True:
        a, b = rng.randint(-5, 5), rng.randint(-6, 6)
        c, d = nonzero(rng, -3, 3), rng.randint(-5, 5)
        k = rng.randint(-3, 3)
        if a * d - b * c != 0 and c * k + d != 0:
            break
    den = c * k + d
    value = Fraction(a * d - b * c, den * den)
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d, "x": k},
        prompt_vi=f"Cho f(x) = ({linear_text(a, b)}) / ({linear_text(c, d)}). Tính f'({k}).",
        answer=num(value),
        solution_vi=["Quy tắc thương: (u/v)' = (u'v - uv') / v^2.",
                     f"u = {linear_text(a, b)}, u' = {a}; v = {linear_text(c, d)}, v' = {c}.",
                     f"Tử: {paren(a)}({linear_text(c, d)}) - {paren(c)}({linear_text(a, b)}) = {a * d - b * c} "
                     "(các số hạng chứa x triệt tiêu).",
                     f"f'(x) = {a * d - b * c} / ({linear_text(c, d)})^2, nên f'({k}) = {a * d - b * c} / "
                     f"{paren(den)}^2 = {num(value)}."])


# ------------------------------------------------------------------ quy tắc dây chuyền
@generator("gt_g4_luy_thua_hop")
def luy_thua_hop(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -3, 3), rng.randint(-4, 4)
    n = rng.randint(2, 5)
    k = rng.randint(-2, 2)
    inner = a * k + b
    value = n * a * inner ** (n - 1)
    return Draw(
        params={"a": a, "b": b, "n": n, "x": k},
        prompt_vi=f"Cho f(x) = ({linear_text(a, b)})^{n}. Tính f'({k}).",
        answer=str(value),
        solution_vi=[f"Hàm ngoài u^{n}, hàm trong u = {linear_text(a, b)} có u' = {a}.",
                     f"Quy tắc dây chuyền: f'(x) = {n}({linear_text(a, b)})^{n - 1} . {paren(a)}.",
                     f"Tại x = {k}: u = {inner}, nên f'({k}) = {n} . {paren(inner)}^{n - 1} . {paren(a)} = {value}."])


@generator("gt_g4_day_chuyen_tf")
def day_chuyen_tf(rng: random.Random) -> Draw:
    while True:
        a, b = nonzero(rng, -3, 3), rng.randint(-4, 4)
        n = rng.randint(2, 4)
        k = nonzero(rng, -2, 2)
        inner = a * k * k + b
        if 2 * a * k != 1 and inner != 0:
            break
    right = n * inner ** (n - 1) * 2 * a * k
    forgot = n * inner ** (n - 1)                      # the inner derivative left out
    ok = rng.random() < 0.5
    claim = right if ok else forgot
    steps = [f"Hàm trong u = {poly_text([a, 0, b])} có u' = {poly_text([2 * a, 0])}; tại x = {k}: u = {inner}, "
             f"u' = {2 * a * k}.",
             f"f'({k}) = {n} . {_pow('u', n - 1)} . u' = {n} . {_pow(paren(inner), n - 1)} . {paren(2 * a * k)} = {right}."]
    steps.append("Số đã cho đúng bằng f'(" + str(k) + "): mệnh đề đúng." if ok else
                 f"Số {claim} là kết quả khi quên nhân đạo hàm trong u': mệnh đề sai.")
    return Draw(
        params={"a": a, "b": b, "n": n, "x": k, "claim": claim},
        prompt_vi=f"Cho f(x) = ({poly_text([a, 0, b])})^{n}. Khi đó f'({k}) = {claim}.",
        answer=ok, solution_vi=steps)


@generator("gt_g4_ln_hop")
def ln_hop(rng: random.Random) -> Draw:
    while True:
        a, b, c = rng.randint(1, 3), rng.randint(-5, 5), rng.randint(-4, 9)
        k = rng.randint(-3, 3)
        inner = a * k * k + b * k + c
        if inner > 0 and 2 * a * k + b != 0:
            break
    value = Fraction(2 * a * k + b, inner)
    coeffs = [a, b, c]
    return Draw(
        params={"coeffs": coeffs, "x": k},
        prompt_vi=f"Cho f(x) = ln({poly_text(coeffs)}). Tính f'({k}).",
        answer=num(value),
        solution_vi=["(ln u)' = u' / u.",
                     f"u = {poly_text(coeffs)}, u' = {poly_text(_derivative(coeffs))}.",
                     f"Tại x = {k}: u = {inner} > 0 và u' = {2 * a * k + b}.",
                     f"f'({k}) = {2 * a * k + b} / {inner}" + ("." if Fraction(2 * a * k + b, inner).denominator == inner else f" = {num(value)}.")])


# ------------------------------------------------------------------ hàm ngược, tham số
@generator("gt_g4_tham_so")
def tham_so(rng: random.Random) -> Draw:
    while True:
        a, b = nonzero(rng, -3, 3), rng.randint(-4, 4)
        c, d = nonzero(rng, -2, 2), rng.randint(-5, 5)
        t0 = rng.randint(-2, 2)
        dx, dy = 2 * a * t0 + b, 3 * c * t0 * t0 + d
        if dx != 0:
            break
    value = Fraction(dy, dx)
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d, "t": t0},
        prompt_vi=(f"Đường cong cho bởi x = {poly_text([a, b, 0], 't')}, y = {poly_text([c, 0, d, 0], 't')}. "
                   f"Tính dy/dx tại t = {t0}."),
        answer=num(value),
        solution_vi=["dy/dx = y'(t) / x'(t) khi x'(t) khác 0.",
                     f"x'(t) = {poly_text([2 * a, b], 't')}, y'(t) = {poly_text([3 * c, 0, d], 't')}.",
                     f"Tại t = {t0}: x' = {dx}, y' = {dy}.",
                     f"dy/dx = {dy} / {paren(dx)} = {num(value)}."])


@generator("gt_g4_nguoc")
def nguoc(rng: random.Random) -> Draw:
    a, b = rng.randint(1, 5), rng.randint(-6, 6)
    k = rng.randint(-3, 3)
    coeffs = [1, 0, a, b]
    y0 = value_at(coeffs, k)
    d = 3 * k * k + a
    return Draw(
        params={"a": a, "b": b, "x": k},
        prompt_vi=(f"Hàm f(x) = {poly_text(coeffs)} tăng ngặt trên R nên có hàm ngược f^(-1). "
                   f"Tính (f^(-1))'({num(y0)})."),
        answer=num(Fraction(1, d)),
        solution_vi=[f"Tìm x0 với f(x0) = {num(y0)}: thử x0 = {k}, f({k}) = {num(y0)}.",
                     f"f'(x) = 3x^2 + {a}, nên f'({k}) = {d} (khác 0).",
                     f"(f^(-1))'({num(y0)}) = 1 / f'({k}) = 1/{d}."])


# ------------------------------------------------------------------ vi phân, đạo hàm cấp cao
@generator("gt_g4_xap_xi")
def xap_xi(rng: random.Random) -> Draw:
    kind = rng.choice(["sqrt", "cbrt"])
    a = rng.randint(2, 10) if kind == "sqrt" else rng.randint(2, 5)
    d = nonzero(rng, -4, 4)
    if kind == "sqrt":
        x0, approx = a * a, a + Fraction(d, 2 * a)
        name, deriv, fprime = "sqrt(x)", "1 / (2 sqrt(x))", Fraction(1, 2 * a)
        target = f"sqrt({a * a + d})"
    else:
        x0, approx = a ** 3, a + Fraction(d, 3 * a * a)
        name, deriv, fprime = "căn bậc ba của x", "1 / (3 x^(2/3))", Fraction(1, 3 * a * a)
        target = f"căn bậc ba của {a ** 3 + d}"
    return Draw(
        params={"kind": kind, "a": a, "d": d},
        prompt_vi=(f"Dùng vi phân của f(x) = {name} tại x0 = {x0} để tính gần đúng {target}. "
                   "Nhập kết quả (phân số a/b)."),
        answer=num(approx),
        solution_vi=[f"f(x0 + dx) xấp xỉ f(x0) + f'(x0) . dx, với x0 = {x0} và dx = {d}.",
                     f"f(x0) = {a}; f'(x) = {deriv}, nên f'({x0}) = {num(fprime)}.",
                     f"{target} xấp xỉ {a} + {num(fprime)} . {paren(d)} = {num(approx)}."])


@generator("gt_g4_cap_cao")
def cap_cao(rng: random.Random) -> Draw:
    kind = rng.choice(["inv", "poly"])
    if kind == "inv":
        p = rng.randint(-3, 3)
        n = rng.randint(2, 5)
        k = rng.choice([v for v in range(-3, 4) if v + p not in (0,) and abs(v + p) <= 3])
        value = Fraction((-1) ** n * math.factorial(n), (k + p) ** (n + 1))
        f_text = f"1 / ({linear_text(1, p)})" if p else "1/x"
        return Draw(
            params={"kind": kind, "p": p, "n": n, "x": k},
            prompt_vi=f"Cho f(x) = {f_text}. Tính đạo hàm cấp {n} f^({n})({k}).",
            answer=num(value),
            solution_vi=[f"Viết f(x) = ({linear_text(1, p)})^(-1). Mỗi lần lấy đạo hàm, số mũ giảm 1 và "
                         "xuất hiện thêm một thừa số bằng số mũ cũ.",
                         f"f^(n)(x) = (-1)^n . n! / ({linear_text(1, p)})^(n + 1).",
                         f"Với n = {n}, x = {k}: {paren((-1) ** n)} . {math.factorial(n)} / "
                         f"{paren(k + p)}^{n + 1} = {num(value)}."])
    m = rng.randint(3, 6)
    c = nonzero(rng, -4, 4)
    n = rng.randint(2, m)
    k = rng.randint(-2, 2)
    # f(x) = x^m + c x^(m - 1)
    v1 = Fraction(math.perm(m, n)) * Fraction(k) ** (m - n)
    v2 = Fraction(c * math.perm(m - 1, n)) * (Fraction(k) ** (m - 1 - n) if n <= m - 1 else 0)
    value = v1 + v2
    coeffs = [1, c] + [0] * (m - 1)
    return Draw(
        params={"kind": kind, "m": m, "c": c, "n": n, "x": k},
        prompt_vi=f"Cho f(x) = {poly_text(coeffs)}. Tính đạo hàm cấp {n} f^({n})({k}).",
        answer=num(value),
        solution_vi=[f"Đạo hàm cấp {n} của x^m là m(m - 1)...(m - {n} + 1) x^(m - {n}), và bằng 0 khi m < {n}.",
                     f"Số hạng x^{m} cho {_mono(math.perm(m, n), m - n)}; số hạng {poly_text([c] + [0] * (m - 1))} cho "
                     + (f"{_mono(c * math.perm(m - 1, n), m - 1 - n)}." if n <= m - 1 else
                        "0 vì bậc của nó nhỏ hơn cấp đạo hàm."),
                     f"Thay x = {k}: {num(v1)} + {paren(v2)} = {num(value)}."])


def _mono(c, p: int) -> str:
    """c x^p written the usual way: 12x^2, -6x, 24."""
    return poly_text([c] + [0] * p)
