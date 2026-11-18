"""Giải Tích, tầng 1 (hàm số, hàm hợp, hàm ngược, hàm sơ cấp): generators. Ids start with `gt_g1_`.

The small text helpers at the top (poly_text, frac_text) are shared with gt_floor2 and gt_floor3."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, linear_text, nonzero, num, nums, paren


# ------------------------------------------------------------------ writing polynomials
def poly_text(coeffs, var: str = "x") -> str:
    """A polynomial from its coefficients, highest power first: [1, -3, 2] -> x^2 - 3x + 2."""
    deg = len(coeffs) - 1
    out = []
    for k, c in enumerate(coeffs):
        c = Fraction(c)
        p = deg - k
        if c == 0:
            continue
        mag = abs(c)
        if p == 0:
            body = num(mag)
        else:
            power = var if p == 1 else f"{var}^{p}"
            body = power if mag == 1 else f"{num(mag)}{power}"
        if not out:
            out.append(f"-{body}" if c < 0 else body)
        else:
            out.append(f"{'-' if c < 0 else '+'} {body}")
    return " ".join(out) if out else "0"


def times_poly(a, b) -> list:
    """The coefficients of the product of two polynomials (highest power first)."""
    out = [0] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            out[i + j] += u * v
    return out


def root_poly(*roots) -> list:
    """(x - r1)(x - r2)... as coefficients."""
    out = [1]
    for r in roots:
        out = times_poly(out, [1, -r])
    return out


def factor_text(r) -> str:
    """The factor (x - r) written the usual way: (x - 2), (x + 3), x."""
    if r == 0:
        return "x"
    return f"(x {'-' if r > 0 else '+'} {num(abs(r))})"


def lin_text(p, q, var: str = "x") -> str:
    """px + q with fractions in brackets where they multiply x: (1/2)x - 3/2, -x + 4, 3."""
    p, q = Fraction(p), Fraction(q)
    if p == 0:
        return num(q)
    if p.denominator == 1:
        head = {1: var, -1: f"-{var}"}.get(p, f"{num(p)}{var}")
    else:
        head = f"{'-' if p < 0 else ''}({num(abs(p))}){var}"
    if q == 0:
        return head
    return f"{head} {'+' if q > 0 else '-'} {num(abs(q))}"


def value_at(coeffs, x) -> Fraction:
    v = Fraction(0)
    for c in coeffs:
        v = v * x + c
    return v


# ------------------------------------------------------------------ hàm số và tập xác định
@generator("gt_g1_gia_tri")
def gia_tri(rng: random.Random) -> Draw:
    a, b, c = nonzero(rng, -4, 4), rng.randint(-6, 6), rng.randint(-9, 9)
    k = rng.randint(-4, 4)
    value = a * k * k + b * k + c
    return Draw(
        params={"coeffs": [a, b, c], "x": k},
        prompt_vi=f"Cho hàm số f(x) = {poly_text([a, b, c])}. Tính f({k}).",
        answer=str(value),
        solution_vi=[f"Thay x = {k} vào mọi chỗ có x trong công thức.",
                     f"f({k}) = {paren(a)} . {paren(k)}^2 + {paren(b)} . {paren(k)} + {paren(c)}.",
                     f"= {a * k * k} + {paren(b * k)} + {paren(c)} = {value}."])


@generator("gt_g1_khong_xac_dinh")
def khong_xac_dinh(rng: random.Random) -> Draw:
    r, s = sorted(rng.sample(range(-6, 7), 2))
    p = rng.randint(-5, 5)
    den = root_poly(r, s)
    top = linear_text(1, p)
    return Draw(
        params={"p": p, "den": den},
        prompt_vi=(f"Hàm số f(x) = ({top}) / ({poly_text(den)}) không xác định tại những giá trị x nào? "
                   "Liệt kê các giá trị đó."),
        answer=nums([r, s]), unordered=True,
        solution_vi=["Một phân thức chỉ không có nghĩa khi mẫu bằng 0; tử bằng bao nhiêu cũng không ảnh hưởng.",
                     f"Giải {poly_text(den)} = 0: phân tích thành {factor_text(r)}{factor_text(s)} = 0.",
                     f"Mẫu bằng 0 tại x = {r} và x = {s}, nên f không xác định tại {nums([r, s])}."])


# ------------------------------------------------------------------ hàm chẵn, lẻ, tuần hoàn
@generator("gt_g1_chan_le")
def chan_le(rng: random.Random) -> Draw:
    pool = rng.choice([[1, 3, 5], [2, 4, 6], range(1, 7)])     # same parity two times in three
    m, n = sorted(rng.sample(list(pool), 2), reverse=True)
    a, b = nonzero(rng, -5, 5), nonzero(rng, -5, 5)
    claim = rng.choice(["chẵn", "lẻ"])
    expr = poly_text([a] + [0] * (m - n - 1) + [b] + [0] * n)
    parities = {m % 2, n % 2}
    if parities == {0}:
        kind = "chẵn"
    elif parities == {1}:
        kind = "lẻ"
    else:
        kind = "không chẵn không lẻ"
    steps = [f"Hàm x^k là hàm chẵn khi k chẵn và là hàm lẻ khi k lẻ, vì (-x)^k = x^k hoặc -x^k.",
             f"Hai số mũ ở đây là {m} và {n}."]
    if kind == "không chẵn không lẻ":
        steps.append("Một số mũ chẵn, một số mũ lẻ: f(-x) không bằng f(x) cũng không bằng -f(x), "
                     "chẳng hạn f(-1) khác cả f(1) lẫn -f(1).")
    else:
        steps.append(f"Cả hai số mũ cùng {'chẵn' if kind == 'chẵn' else 'lẻ'}, nên f(-x) = "
                     f"{'f(x)' if kind == 'chẵn' else '-f(x)'} với mọi x: f là hàm {kind}.")
    return Draw(params={"a": a, "m": m, "b": b, "n": n, "claim": claim},
                prompt_vi=f"Hàm số f(x) = {expr}, xác định trên R, là hàm {claim}.",
                answer=(kind == claim), solution_vi=steps)


@generator("gt_g1_chu_ky")
def chu_ky(rng: random.Random) -> Draw:
    fn = rng.choice(["sin", "cos", "tan"])
    a = rng.choice([v for v in range(-6, 7) if v not in (0,)])
    b = rng.randint(-3, 3)
    arg = linear_text(a, b)
    base = Fraction(1) if fn == "tan" else Fraction(2)
    k = base / abs(a)
    return Draw(
        params={"fn": fn, "a": a, "b": b},
        prompt_vi=(f"Chu kỳ cơ sở (chu kỳ dương nhỏ nhất) của f(x) = {fn}({arg}) là T = k . pi. "
                   "Tìm k."),
        answer=num(k),
        solution_vi=[f"Hàm {fn} x có chu kỳ cơ sở {'pi' if fn == 'tan' else '2pi'}.",
                     f"Nhân x với {a} làm đồ thị co lại {abs(a)} lần; cộng hằng số chỉ dịch đồ thị, không đổi chu kỳ.",
                     f"T = {'pi' if fn == 'tan' else '2pi'} / {abs(a)} = {num(k)} . pi, nên k = {num(k)}."])


# ------------------------------------------------------------------ hàm hợp
@generator("gt_g1_hop_gia_tri")
def hop_gia_tri(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -4, 4), rng.randint(-6, 6)
    c = rng.randint(-5, 5)
    k = rng.randint(-3, 3)
    order = rng.choice(["fg", "gf"])
    f_text, g_text = linear_text(a, b), poly_text([1, 0, c])
    if order == "fg":
        inner = k * k + c
        value = a * inner + b
        steps = [f"Tính từ trong ra ngoài: g({k}) = {paren(k)}^2 + {paren(c)} = {inner}.",
                 f"f(g({k})) = f({inner}) = {paren(a)} . {paren(inner)} + {paren(b)} = {value}."]
        ask = f"f(g({k}))"
    else:
        inner = a * k + b
        value = inner * inner + c
        steps = [f"Tính từ trong ra ngoài: f({k}) = {paren(a)} . {paren(k)} + {paren(b)} = {inner}.",
                 f"g(f({k})) = g({inner}) = {paren(inner)}^2 + {paren(c)} = {value}."]
        ask = f"g(f({k}))"
    return Draw(params={"f": [a, b], "c": c, "x": k, "order": order},
                prompt_vi=f"Cho f(x) = {f_text} và g(x) = {g_text}. Tính {ask}.",
                answer=str(value), solution_vi=steps)


@generator("gt_g1_hop_he_so")
def hop_he_so(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -5, 5), rng.randint(-6, 6)
    c, d = nonzero(rng, -5, 5), rng.randint(-6, 6)
    p, q = a * c, a * d + b
    return Draw(
        params={"f": [a, b], "g": [c, d]},
        prompt_vi=(f"Cho f(x) = {linear_text(a, b)} và g(x) = {linear_text(c, d)}. Hàm hợp f(g(x)) có dạng "
                   "px + q. Nhập p, q theo đúng thứ tự."),
        answer=nums([p, q]),
        solution_vi=["f(g(x)) nghĩa là thay cả biểu thức g(x) vào chỗ của x trong f.",
                     f"f(g(x)) = {paren(a)} . ({linear_text(c, d)}) + {paren(b)}.",
                     f"Nhân phân phối: {linear_text(p, a * d)} + {paren(b)} = {linear_text(p, q)}.",
                     f"Vậy p = {p}, q = {q}."])


# ------------------------------------------------------------------ hàm ngược
@generator("gt_g1_nguoc_bac_nhat")
def nguoc_bac_nhat(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -6, 6), rng.randint(-9, 9)
    p, q = Fraction(1, a), Fraction(-b, a)
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=(f"Hàm f(x) = {linear_text(a, b)} có hàm ngược f^(-1)(x) = px + q. "
                   "Nhập p, q theo đúng thứ tự (phân số viết a/b)."),
        answer=nums([p, q]),
        solution_vi=[f"Đặt y = {linear_text(a, b)} rồi giải theo x.",
                     f"{linear_text(a, 0)} = y - {paren(b)}, nên x = (y - {paren(b)}) / {paren(a)}.",
                     f"Đổi tên biến: f^(-1)(x) = {lin_text(p, q)}.",
                     f"Vậy p = {num(p)}, q = {num(q)}."])


@generator("gt_g1_nguoc_phan_thuc")
def nguoc_phan_thuc(rng: random.Random) -> Draw:
    while True:
        a, b = rng.randint(-5, 5), rng.randint(-6, 6)
        c, d = nonzero(rng, -3, 3), rng.randint(-5, 5)
        k = rng.randint(-6, 6)
        if a * d - b * c != 0 and a - k * c != 0:
            break
    x = Fraction(k * d - b, a - k * c)
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d, "k": k},
        prompt_vi=(f"Hàm f(x) = ({linear_text(a, b)}) / ({linear_text(c, d)}) có hàm ngược. "
                   f"Tính f^(-1)({k})."),
        answer=num(x),
        solution_vi=[f"f^(-1)({k}) là số x sao cho f(x) = {k}.",
                     f"Giải ({linear_text(a, b)}) / ({linear_text(c, d)}) = {k}: nhân chéo được "
                     f"{linear_text(a, b)} = {paren(k)} . ({linear_text(c, d)}).",
                     f"Chuyển các số hạng chứa x sang một vế: {linear_text(a - k * c, 0)} = {k * d - b}.",
                     f"x = {num(x)}, và mẫu {linear_text(c, d)} khác 0 tại đó, nên f^(-1)({k}) = {num(x)}."])


# ------------------------------------------------------------------ hàm sơ cấp
@generator("gt_g1_logarit")
def logarit(rng: random.Random) -> Draw:
    base = rng.choice([2, 3, 4, 5, 10])
    k = rng.choice([v for v in range(-3, 5) if v != 0 and abs(base ** abs(v)) <= 10000])
    n = Fraction(base) ** k
    return Draw(
        params={"base": base, "n": [n.numerator, n.denominator]},
        prompt_vi=f"Tính log_{base}({num(n)}).",
        answer=str(k),
        solution_vi=[f"log_{base}(N) là số mũ phải đặt lên {base} để được N.",
                     (f"{num(n)} = 1 / {base}^{-k} = {base}^({k})." if k < 0 else f"{num(n)} = {base}^{k}."),
                     f"Vậy log_{base}({num(n)}) = {k}."])


@generator("gt_g1_pt_logarit")
def pt_logarit(rng: random.Random) -> Draw:
    base = rng.choice([2, 3, 5])
    k = rng.randint(0, 3)
    p = rng.randint(-6, 6)
    x = base ** k - p
    return Draw(
        params={"base": base, "k": k, "p": p},
        prompt_vi=f"Giải phương trình log_{base}({linear_text(1, p)}) = {k}.",
        answer=str(x),
        solution_vi=[f"Điều kiện: {linear_text(1, p)} > 0.",
                     f"log_{base}(A) = {k} nghĩa là A = {base}^{k} = {base ** k}.",
                     f"{linear_text(1, p)} = {base ** k}, nên x = {x}.",
                     f"Kiểm tra điều kiện: {linear_text(1, p)} = {base ** k} > 0, thỏa. Nghiệm x = {x}."])
