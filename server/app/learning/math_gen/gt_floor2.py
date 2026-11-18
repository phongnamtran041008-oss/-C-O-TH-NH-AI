"""Giải Tích, tầng 2 (dãy số, giới hạn, vô cùng bé và vô cùng lớn): generators. Ids start with `gt_g2_`."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, linear_text, nonzero, num, paren
from .gt_floor1 import factor_text, poly_text, root_poly, value_at


def _coef_x(c, var: str = "x") -> str:
    """cx written the usual way: x, -x, 3x."""
    return {1: var, -1: f"-{var}"}.get(c, f"{c}{var}")


# ------------------------------------------------------------------ giới hạn của dãy số
@generator("gt_g2_day_huu_ty")
def day_huu_ty(rng: random.Random) -> Draw:
    deg_den = rng.choice([1, 2])
    deg_num = rng.choice([deg_den, deg_den, deg_den - 1]) if deg_den == 2 else deg_den
    top = [nonzero(rng, -6, 6)] + [rng.randint(-5, 5) for _ in range(deg_num)]
    bottom = [rng.randint(1, 6)] + [rng.randint(0, 5) for _ in range(deg_den)]    # positive for every n >= 1
    limit = Fraction(top[0], bottom[0]) if deg_num == deg_den else Fraction(0)
    steps = [f"Chia cả tử và mẫu cho n^{deg_den}" if deg_den > 1 else "Chia cả tử và mẫu cho n",
             "Mọi số hạng có dạng (hằng số) / n^k với k >= 1 đều dần tới 0 khi n -> +vô cùng."]
    if deg_num == deg_den:
        steps.append(f"Chỉ còn lại tỉ số hai hệ số của lũy thừa cao nhất: {top[0]} / {bottom[0]} = {num(limit)}.")
    else:
        steps.append("Bậc của tử nhỏ hơn bậc của mẫu, nên sau khi chia, tử dần tới 0 còn mẫu dần tới "
                     f"{bottom[0]}: giới hạn bằng 0.")
    steps[0] += "."
    return Draw(
        params={"top": top, "bottom": bottom},
        prompt_vi=(f"Tính giới hạn của dãy u_n = ({poly_text(top, 'n')}) / ({poly_text(bottom, 'n')}) "
                   "khi n -> +vô cùng."),
        answer=num(limit), solution_vi=steps)


@generator("gt_g2_day_mu")
def day_mu(rng: random.Random) -> Draw:
    q, p = sorted(rng.sample([2, 3, 4, 5, 6], 2))
    a, c = nonzero(rng, -5, 5), nonzero(rng, 1, 6)
    while True:
        b, d = nonzero(rng, -5, 5), nonzero(rng, -5, 5)
        if all(c * p ** n + d * q ** n != 0 for n in range(1, 30)):     # u_n is defined for every n
            break
    limit = Fraction(a, c)

    def part(k, base):
        return f"{_coef(k)}{base}^n"

    top = f"{part(a, p)} {'+' if b > 0 else '-'} {_coef(abs(b))}{q}^n"
    bottom = f"{part(c, p)} {'+' if d > 0 else '-'} {_coef(abs(d))}{q}^n"
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d, "p": p, "q": q},
        prompt_vi=f"Tính giới hạn của dãy u_n = ({top}) / ({bottom}) khi n -> +vô cùng.",
        answer=num(limit),
        solution_vi=[f"Lũy thừa lớn nhất là {p}^n: chia cả tử và mẫu cho {p}^n.",
                     f"Còn lại ({a} {'+' if b > 0 else '-'} {abs(b)} . ({q}/{p})^n) / "
                     f"({c} {'+' if d > 0 else '-'} {abs(d)} . ({q}/{p})^n).",
                     f"Vì 0 < {q}/{p} < 1 nên ({q}/{p})^n -> 0.",
                     f"Giới hạn bằng {a} / {c} = {num(limit)}."])


def _coef(k) -> str:
    """The coefficient in front of a power: '' for 1, '-' for -1, '3 . ' otherwise."""
    return {1: "", -1: "-"}.get(k, f"{k} . ")


# ------------------------------------------------------------------ giới hạn hàm số tại một điểm
@generator("gt_g2_thay_so")
def thay_so(rng: random.Random) -> Draw:
    while True:
        a, b = nonzero(rng, -4, 4), rng.randint(-8, 8)
        c, d = nonzero(rng, -4, 4), rng.randint(-6, 6)
        k = rng.randint(-3, 4)
        if c * k + d != 0:
            break
    top_v, bot_v = a * k * k + b, c * k + d
    limit = Fraction(top_v, bot_v)
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d, "x0": k},
        prompt_vi=f"Tính giới hạn của ({poly_text([a, 0, b])}) / ({linear_text(c, d)}) khi x -> {k}.",
        answer=num(limit),
        solution_vi=[f"Tại x = {k} mẫu bằng {paren(c)} . {paren(k)} + {paren(d)} = {bot_v}, khác 0.",
                     "Hàm phân thức liên tục tại mọi điểm mẫu khác 0, nên chỉ cần thay số.",
                     f"Tử bằng {paren(a)} . {paren(k)}^2 + {paren(b)} = {top_v}.",
                     f"Giới hạn = {top_v} / {paren(bot_v)} = {num(limit)}."])


@generator("gt_g2_khu_00")
def khu_00(rng: random.Random) -> Draw:
    r, s, t = rng.sample(range(-5, 6), 3)
    top, bottom = root_poly(r, s), root_poly(r, t)
    limit = Fraction(r - s, r - t)
    return Draw(
        params={"top": top, "bottom": bottom, "x0": r},
        prompt_vi=f"Tính giới hạn của ({poly_text(top)}) / ({poly_text(bottom)}) khi x -> {r}.",
        answer=num(limit),
        solution_vi=[f"Thay x = {r}: tử và mẫu đều bằng 0, dạng 0/0, chưa kết luận được.",
                     f"Cả tử và mẫu đều có nghiệm x = {r}, nên đều chia hết cho {factor_text(r)}: "
                     f"tử = {factor_text(r)}{factor_text(s)}, mẫu = {factor_text(r)}{factor_text(t)}.",
                     f"Với x khác {r}, rút gọn được ({linear_text(1, -s)}) / ({linear_text(1, -t)}).",
                     f"Thay x = {r}: ({r - s}) / ({r - t}) = {num(limit)}."])


# ------------------------------------------------------------------ giới hạn ở vô cùng
@generator("gt_g2_vo_cuc_huu_ty")
def vo_cuc_huu_ty(rng: random.Random) -> Draw:
    deg_den = rng.choice([2, 3])
    deg_num = rng.choice([deg_den, deg_den - 1])
    top = [nonzero(rng, -7, 7)] + [rng.randint(-6, 6) for _ in range(deg_num)]
    bottom = [nonzero(rng, -5, 5)] + [rng.randint(-6, 6) for _ in range(deg_den)]
    side = rng.choice(["+", "-"])
    limit = Fraction(top[0], bottom[0]) if deg_num == deg_den else Fraction(0)
    last = (f"Bậc của tử bằng bậc của mẫu: giới hạn là tỉ số hai hệ số cao nhất {top[0]} / {paren(bottom[0])} = {num(limit)}."
            if deg_num == deg_den else "Bậc của tử nhỏ hơn bậc của mẫu, nên giới hạn bằng 0.")
    return Draw(
        params={"top": top, "bottom": bottom, "side": side},
        prompt_vi=(f"Tính giới hạn của ({poly_text(top)}) / ({poly_text(bottom)}) "
                   f"khi x -> {side}vô cùng."),
        answer=num(limit),
        solution_vi=[f"Chia cả tử và mẫu cho x^{deg_den}, lũy thừa cao nhất của mẫu.",
                     f"Mọi số hạng dạng (hằng số) / x^k với k >= 1 dần tới 0 khi x -> {side}vô cùng.",
                     last])


@generator("gt_g2_can_lien_hop")
def can_lien_hop(rng: random.Random) -> Draw:
    a = rng.randint(1, 3)
    b = nonzero(rng, -9, 9)
    c = rng.randint(0, 9)
    limit = Fraction(b, 2 * a)
    inside = poly_text([a * a, b, c])
    return Draw(
        params={"a": a, "b": b, "c": c},
        prompt_vi=f"Tính giới hạn của sqrt({inside}) - {_coef_x(a)} khi x -> +vô cùng.",
        answer=num(limit),
        solution_vi=["Dạng vô cùng trừ vô cùng: nhân và chia cho biểu thức liên hợp "
                     f"sqrt({inside}) + {_coef_x(a)}.",
                     f"Tử thành ({inside}) - {_coef_x(a * a, 'x^2')} = {poly_text([b, c])}.",
                     f"Chia tử và mẫu cho x: tử -> {b}, mẫu = sqrt({a * a} + ...) + {a} -> {a} + {a} = {2 * a}.",
                     f"Giới hạn bằng {b} / {2 * a} = {num(limit)}."])


# ------------------------------------------------------------------ hai giới hạn đáng nhớ
@generator("gt_g2_sin_x")
def sin_x(rng: random.Random) -> Draw:
    kind = rng.choice(["sin/x", "tan/x", "sin/sin", "x/tan"])
    a, b = nonzero(rng, -7, 7), nonzero(rng, -7, 7)
    while abs(a) == abs(b) and kind == "sin/sin":
        b = nonzero(rng, -7, 7)
    limit = Fraction(a, b)
    if kind == "sin/x":
        text, why = f"sin({_coef_x(a)}) / ({_coef_x(b)})", f"sin({_coef_x(a)}) ~ {_coef_x(a)}"
    elif kind == "tan/x":
        text, why = f"tan({_coef_x(a)}) / ({_coef_x(b)})", f"tan({_coef_x(a)}) ~ {_coef_x(a)}"
    elif kind == "sin/sin":
        text, why = (f"sin({_coef_x(a)}) / sin({_coef_x(b)})",
                     f"sin({_coef_x(a)}) ~ {_coef_x(a)} và sin({_coef_x(b)}) ~ {_coef_x(b)}")
    else:
        text, why = f"({_coef_x(a)}) / tan({_coef_x(b)})", f"tan({_coef_x(b)}) ~ {_coef_x(b)}"
        limit = Fraction(a, b)
    return Draw(
        params={"kind": kind, "a": a, "b": b},
        prompt_vi=f"Tính giới hạn của {text} khi x -> 0.",
        answer=num(limit),
        solution_vi=["Dùng sin u / u -> 1 khi u -> 0 (và tan u / u -> 1, vì tan u = sin u / cos u).",
                     f"Khi x -> 0: {why}, tức là tỉ số của chúng dần tới 1.",
                     f"Vậy giới hạn bằng {a} / {paren(b)} = {num(limit)}."])


@generator("gt_g2_mu_e")
def mu_e(rng: random.Random) -> Draw:
    b = nonzero(rng, -4, 4)
    kind = rng.choice(["a/n", "1/(an)"])
    if kind == "a/n":
        a = nonzero(rng, -4, 4)
        base = f"(1 + {a}/n)" if a > 0 else f"(1 - {-a}/n)"
        k = Fraction(a * b)
        why = (f"Đặt m = {'n' if a == 1 else f'n/{paren(a)}'}, thì {a}/n = 1/m và {_coef_x(b, 'n')} = {_coef_x(a * b, 'm')}, "
               f"nên dãy bằng [(1 + 1/m)^m]^({a * b})")
    else:
        a = rng.randint(2, 5)
        base = f"(1 + 1/({a}n))"
        k = Fraction(b, a)
        why = (f"Đặt m = {a}n, thì {_coef_x(b, 'n')} = ({num(k)})m, "
               f"nên dãy bằng [(1 + 1/m)^m]^({num(k)})")
    return Draw(
        params={"kind": kind, "a": a, "b": b},
        prompt_vi=(f"Khi n -> +vô cùng, dãy {base}^({_coef_x(b, 'n')}) dần tới e^k. Tìm k."),
        answer=num(k),
        solution_vi=["Giới hạn cơ bản: (1 + 1/m)^m -> e khi m -> vô cùng (m dương hay âm đều đúng).",
                     why + ".",
                     f"Phần trong ngoặc vuông dần tới e, nên dãy dần tới e^({num(k)}): k = {num(k)}."])


# ------------------------------------------------------------------ vô cùng bé, vô cùng lớn
@generator("gt_g2_vcb_cap")
def vcb_cap(rng: random.Random) -> Draw:
    kind = rng.choice(["poly", "x_sin", "x_cos"])
    if kind == "poly":
        m, n = sorted(rng.sample(range(1, 7), 2))
        a, b = nonzero(rng, -5, 5), nonzero(rng, -5, 5)
        text = poly_text([b] + [0] * (n - m - 1) + [a] + [0] * m)
        order = m
        def xp(k):
            return "x" if k == 1 else f"x^{k}"
        why = [f"Khi x -> 0, {xp(n)} nhỏ hơn {xp(m)} rất nhiều ({xp(n)} / {xp(m)} = {xp(n - m)} -> 0).",
               f"Số hạng quyết định là {_coef_x(a, f'x^{m}') if m > 1 else _coef_x(a)}, nên đây là vô cùng bé cấp {m}."]
        params = {"kind": kind, "a": a, "m": m, "b": b, "n": n}
    elif kind == "x_sin":
        m, a = rng.randint(1, 4), rng.randint(2, 6)
        text = f"{'x' if m == 1 else f'x^{m}'} . sin({a}x)"
        order = m + 1
        why = [f"sin({a}x) ~ {a}x khi x -> 0.",
               f"Vậy biểu thức tương đương {a}x^{m + 1}: vô cùng bé cấp {m + 1}."]
        params = {"kind": kind, "m": m, "a": a}
    else:
        m, a = rng.randint(0, 3), rng.randint(2, 6)
        text = f"1 - cos({a}x)" if m == 0 else f"{'x' if m == 1 else f'x^{m}'} . (1 - cos({a}x))"
        order = m + 2
        why = [f"1 - cos({a}x) ~ ({a}x)^2 / 2 = {num(Fraction(a * a, 2))}x^2 khi x -> 0.",
               f"Nhân thêm x^{m} thì được vô cùng bé cấp {m + 2}." if m else "Đây là vô cùng bé cấp 2."]
        params = {"kind": kind, "m": m, "a": a}
    return Draw(
        params=params,
        prompt_vi=(f"Khi x -> 0, a(x) = {text} là vô cùng bé cấp k so với x, nghĩa là a(x) / x^k dần tới "
                   "một số khác 0. Tìm k."),
        answer=str(order),
        solution_vi=why)


_EQUIV = {          # name -> (text with the coefficient c, coefficient of x in the equivalent cx)
    "sin": lambda c: f"sin({_coef_x(c)})",
    "tan": lambda c: f"tan({_coef_x(c)})",
    "ln": lambda c: f"ln(1 + {_coef_x(c)})" if c > 0 else f"ln(1 - {_coef_x(-c)})",
    "exp": lambda c: f"(e^({_coef_x(c)}) - 1)",
    "arcsin": lambda c: f"arcsin({_coef_x(c)})",
}


@generator("gt_g2_vcb_thay")
def vcb_thay(rng: random.Random) -> Draw:
    kind = rng.choice(["first", "first", "cos"])
    if kind == "first":
        f, g = rng.sample(sorted(_EQUIV), 2)
        a, b = nonzero(rng, -6, 6), nonzero(rng, -6, 6)
        top, bottom = _EQUIV[f](a), _EQUIV[g](b)
        limit = Fraction(a, b)
        steps = [f"Khi x -> 0: {top} ~ {_coef_x(a)} và {bottom} ~ {_coef_x(b)}.",
                 "Trong một thương, được thay mỗi vô cùng bé bằng một vô cùng bé tương đương.",
                 f"Giới hạn = lim ({_coef_x(a)}) / ({_coef_x(b)}) = {a} / {paren(b)} = {num(limit)}."]
        params = {"kind": kind, "f": f, "g": g, "a": a, "b": b}
    else:
        a = rng.randint(1, 6)
        g = rng.choice(["x^2", "x sin", "x ln"])
        b = nonzero(rng, -5, 5)
        top = f"(1 - cos({_coef_x(a)}))"
        bottom = "(" + {"x^2": f"{_coef_x(b, 'x^2')}", "x sin": f"x . sin({_coef_x(b)})",
                        "x ln": "x . " + _EQUIV["ln"](b)}[g] + ")"
        limit = Fraction(a * a, 2 * b)
        steps = [f"Khi x -> 0: 1 - cos({_coef_x(a)}) ~ ({_coef_x(a)})^2 / 2 = {num(Fraction(a * a, 2))}x^2.",
                 f"Mẫu tương đương {_coef_x(b, 'x^2')}.",
                 f"Giới hạn = ({num(Fraction(a * a, 2))}) / {paren(b)} = {num(limit)}."]
        params = {"kind": kind, "a": a, "g": g, "b": b}
    return Draw(
        params=params,
        prompt_vi=f"Dùng vô cùng bé tương đương, tính giới hạn của {top} / {bottom} khi x -> 0.",
        answer=num(limit), solution_vi=steps)
