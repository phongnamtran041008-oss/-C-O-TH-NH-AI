"""Giải Tích, tầng 3 (hàm liên tục và điểm gián đoạn): generators. Ids start with `gt_g3_`.

A function given by several formulas is written on one line, its pieces separated by ';':
"f(x) = 2x + 1 nếu x < 1; f(x) = x^2 + 3 nếu x >= 1"."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, linear_text, nonzero, num, nums, paren
from .gt_floor1 import factor_text, poly_text, root_poly, value_at


# ------------------------------------------------------------------ liên tục tại một điểm
@generator("gt_g3_lien_tuc_tf")
def lien_tuc_tf(rng: random.Random) -> Draw:
    r, s = rng.sample(range(-5, 6), 2)
    top = root_poly(r, s)
    limit = r - s
    ok = rng.random() < 0.5
    v = limit if ok else limit + nonzero(rng, -3, 3)
    steps = [f"f(x) liên tục tại {r} khi giới hạn của f tại {r} bằng f({r}) = {v}.",
             f"Với x khác {r}: tử = {factor_text(r)}{factor_text(s)}, nên f(x) = {linear_text(1, -s)}.",
             f"Giới hạn khi x -> {r} là {r} - {paren(s)} = {limit}."]
    steps.append(f"Giới hạn bằng f({r}), nên f liên tục tại {r}." if ok else
                 f"Giới hạn {limit} khác f({r}) = {v}, nên f không liên tục tại {r}.")
    return Draw(
        params={"top": top, "x0": r, "value": v},
        prompt_vi=(f"Cho f(x) = ({poly_text(top)}) / ({linear_text(1, -r)}) nếu x khác {r}; f({r}) = {v}. "
                   f"Hàm f liên tục tại x = {r}."),
        answer=ok, solution_vi=steps)


@generator("gt_g3_thac_trien")
def thac_trien(rng: random.Random) -> Draw:
    r = nonzero(rng, -4, 4)
    n = rng.choice([2, 3, 4])
    c = rng.randint(1, 4)
    # f(x) = c (x^n - r^n) / (x - r): its limit at r is c n r^(n-1)
    value = c * n * r ** (n - 1)
    top = poly_text([c] + [0] * (n - 1) + [-c * r ** n])
    split = ("x^2 - a^2 = (x - a)(x + a), gồm 2 số hạng" if n == 2 else
             f"x^{n} - a^{n} = (x - a)(x^{n - 1} + ... + a^{n - 1}), gồm {n} số hạng")
    return Draw(
        params={"c": c, "n": n, "r": r},
        prompt_vi=(f"Hàm f(x) = ({top}) / ({linear_text(1, -r)}) không xác định tại x = {r}. "
                   f"Phải gán f({r}) bằng bao nhiêu để f liên tục tại {r}?"),
        answer=str(value),
        solution_vi=[f"Cần f({r}) bằng giới hạn của f khi x -> {r}.",
                     f"Tử = {c if c != 1 else ''}(x^{n} - {paren(r)}^{n}) chia hết cho {linear_text(1, -r)}: "
                     f"{split}.",
                     f"Sau khi rút gọn, cho x -> {r}: mỗi số hạng trong ngoặc dần tới "
                     f"{paren(r) if n == 2 else f'{paren(r)}^{n - 1}'} = {r ** (n - 1)}.",
                     f"Giới hạn = {c} . {n} . {paren(r ** (n - 1))} = {value}, nên gán f({r}) = {value}."])


# ------------------------------------------------------------------ giới hạn một phía
@generator("gt_g3_mot_phia")
def mot_phia(rng: random.Random) -> Draw:
    c = rng.randint(-3, 3)
    a, b = nonzero(rng, -4, 4), rng.randint(-6, 6)
    d, e = nonzero(rng, -3, 3), rng.randint(-6, 6)
    left, right = a * c + b, d * c * c + e
    return Draw(
        params={"left": [a, b], "right": [d, e], "c": c},
        prompt_vi=(f"Cho f(x) = {linear_text(a, b)} nếu x < {c}; f(x) = {poly_text([d, 0, e])} nếu x >= {c}. "
                   f"Nhập giới hạn trái rồi giới hạn phải của f tại x = {c}."),
        answer=nums([left, right]),
        solution_vi=[f"Giới hạn trái dùng công thức của phía x < {c}: {paren(a)} . {paren(c)} + {paren(b)} = {left}.",
                     f"Giới hạn phải dùng công thức của phía x >= {c}: {paren(d)} . {paren(c)}^2 + {paren(e)} = {right}.",
                     f"Đáp án: {left}, {right}."])


@generator("gt_g3_tri_tuyet_doi")
def tri_tuyet_doi(rng: random.Random) -> Draw:
    c = rng.randint(-4, 4)
    p = rng.randint(-5, 5)
    while c + p == 0:
        p = rng.randint(-5, 5)
    k = nonzero(rng, -3, 3)
    # f(x) = k |x - c| (x + p) / (x - c): -k (x + p) on the left, k (x + p) on the right
    left, right = -k * (c + p), k * (c + p)
    kx = {1: "", -1: "-"}.get(k, f"{k}")
    return Draw(
        params={"k": k, "c": c, "p": p},
        prompt_vi=(f"Cho f(x) = {kx}|{linear_text(1, -c)}| . ({linear_text(1, p)}) / ({linear_text(1, -c)}) "
                   f"với x khác {c}. Nhập giới hạn trái rồi giới hạn phải của f tại x = {c}."),
        answer=nums([left, right]),
        solution_vi=[f"Khi x < {c}: |{linear_text(1, -c)}| = -({linear_text(1, -c)}), nên f(x) = "
                     f"{paren(-k)} . ({linear_text(1, p)}).",
                     f"Khi x > {c}: |{linear_text(1, -c)}| = {linear_text(1, -c)}, nên f(x) = {paren(k)} . ({linear_text(1, p)}).",
                     f"Cho x -> {c}: giới hạn trái = {paren(-k)} . {paren(c + p)} = {left}, "
                     f"giới hạn phải = {paren(k)} . {paren(c + p)} = {right}."])


# ------------------------------------------------------------------ tìm tham số
@generator("gt_g3_tham_so")
def tham_so(rng: random.Random) -> Draw:
    r, s = rng.sample(range(-5, 6), 2)
    top = root_poly(r, s)
    m = r - s
    return Draw(
        params={"top": top, "x0": r},
        prompt_vi=(f"Cho f(x) = ({poly_text(top)}) / ({linear_text(1, -r)}) nếu x khác {r}; f({r}) = m. "
                   "Tìm m để f liên tục trên R."),
        answer=str(m),
        solution_vi=[f"Tại mọi x khác {r}, f là phân thức có mẫu khác 0 nên liên tục; chỉ cần xét x = {r}.",
                     f"Tử có nghiệm {r}: {poly_text(top)} = {factor_text(r)}{factor_text(s)}.",
                     f"Với x khác {r}, f(x) = {linear_text(1, -s)}, nên giới hạn tại {r} là {m}.",
                     f"Cần m = f({r}) = {m}."])


@generator("gt_g3_tham_so_hai_nhanh")
def tham_so_hai_nhanh(rng: random.Random) -> Draw:
    c = nonzero(rng, -3, 3)
    p, q = nonzero(rng, -4, 4), rng.randint(-6, 6)
    t = rng.randint(-6, 6)
    m = Fraction(p * c + q - t, c * c)
    return Draw(
        params={"p": p, "q": q, "t": t, "c": c},
        prompt_vi=(f"Cho f(x) = {linear_text(p, q)} nếu x < {c}; f(x) = mx^2 {'+' if t >= 0 else '-'} {abs(t)} "
                   f"nếu x >= {c}. Tìm m để f liên tục trên R."),
        answer=num(m),
        solution_vi=[f"Mỗi mảnh là đa thức nên liên tục; chỉ cần hai mảnh nối liền tại x = {c}.",
                     f"Giới hạn trái: {paren(p)} . {paren(c)} + {paren(q)} = {p * c + q}.",
                     f"Giới hạn phải và f({c}): m . {paren(c)}^2 + {paren(t)} = {c * c}m + {paren(t)}.",
                     f"Cho bằng nhau: {c * c}m = {p * c + q - t}, nên m = {num(m)}."])


# ------------------------------------------------------------------ phân loại điểm gián đoạn
@generator("gt_g3_buoc_nhay")
def buoc_nhay(rng: random.Random) -> Draw:
    while True:
        c = rng.randint(-3, 3)
        a, b = nonzero(rng, -4, 4), rng.randint(-6, 6)
        d, e = nonzero(rng, -4, 4), rng.randint(-6, 6)
        jump = (d * c + e) - (a * c + b)
        if jump != 0:
            break
    return Draw(
        params={"left": [a, b], "right": [d, e], "c": c},
        prompt_vi=(f"Cho f(x) = {linear_text(a, b)} nếu x < {c}; f(x) = {linear_text(d, e)} nếu x >= {c}. "
                   f"x = {c} là điểm gián đoạn loại một. Tính bước nhảy: giới hạn phải trừ giới hạn trái."),
        answer=str(jump),
        solution_vi=[f"Giới hạn trái: {paren(a)} . {paren(c)} + {paren(b)} = {a * c + b}.",
                     f"Giới hạn phải: {paren(d)} . {paren(c)} + {paren(e)} = {d * c + e}.",
                     f"Hai giới hạn đều hữu hạn nhưng khác nhau: gián đoạn loại một.",
                     f"Bước nhảy = {d * c + e} - {paren(a * c + b)} = {jump}."])


@generator("gt_g3_khu_duoc")
def khu_duoc(rng: random.Random) -> Draw:
    r, s, t = rng.sample(range(-5, 6), 3)
    top, bottom = root_poly(r, t), root_poly(r, s)
    limit = Fraction(r - t, r - s)
    return Draw(
        params={"top": top, "bottom": bottom},
        prompt_vi=(f"Hàm f(x) = ({poly_text(top)}) / ({poly_text(bottom)}) có hai điểm gián đoạn. Nhập điểm "
                   "gián đoạn khử được rồi giới hạn của f tại điểm đó."),
        answer=nums([r, limit]),
        solution_vi=[f"Mẫu = {factor_text(r)}{factor_text(s)} bằng 0 tại x = {r} và x = {s}.",
                     f"Tử = {factor_text(r)}{factor_text(t)} cũng bằng 0 tại x = {r}, nhưng khác 0 tại x = {s}.",
                     f"Tại x = {s}: tử khác 0, mẫu -> 0, nên f -> vô cùng: gián đoạn loại hai.",
                     f"Tại x = {r}: rút gọn được ({linear_text(1, -t)}) / ({linear_text(1, -s)}), giới hạn "
                     f"({r - t}) / ({r - s}) = {num(limit)} hữu hạn: gián đoạn khử được.",
                     f"Đáp án: {r}, {num(limit)}."])


# ------------------------------------------------------------------ giá trị trung gian
def _increasing_cubic(rng: random.Random) -> tuple[int, int]:
    """x^3 + ax + b with a >= 1 (strictly increasing, so exactly one real root), whose root
    is not a whole number in -6..6."""
    while True:
        a, b = rng.randint(1, 6), rng.randint(-30, 30)
        if all(value_at([1, 0, a, b], k) != 0 for k in range(-7, 8)) and value_at([1, 0, a, b], -6) < 0 < value_at([1, 0, a, b], 6):
            return a, b


@generator("gt_g3_doi_dau")
def doi_dau(rng: random.Random) -> Draw:
    a, b = _increasing_cubic(rng)
    u = rng.randint(-4, 3)
    pu, pv = value_at([1, 0, a, b], u), value_at([1, 0, a, b], u + 1)
    inside = pu < 0 < pv
    text = poly_text([1, 0, a, b])
    steps = [f"p(x) = {text} liên tục trên R; vì p'(x) = 3x^2 + {a} > 0 nên p tăng ngặt và có đúng một nghiệm.",
             f"p({u}) = {num(pu)} và p({u + 1}) = {num(pv)}."]
    if inside:
        steps.append(f"Hai giá trị trái dấu, nên theo định lý giá trị trung gian có nghiệm trong ({u}, {u + 1}).")
    else:
        steps.append(f"Hai giá trị cùng dấu; p tăng ngặt nên p không đổi dấu trên ({u}, {u + 1}), không có nghiệm ở đó.")
    return Draw(
        params={"a": a, "b": b, "u": u},
        prompt_vi=f"Phương trình {text} = 0 có một nghiệm nằm trong khoảng ({u}, {u + 1}).",
        answer=inside, solution_vi=steps)


@generator("gt_g3_khoang_nghiem")
def khoang_nghiem(rng: random.Random) -> Draw:
    a, b = _increasing_cubic(rng)
    k = next(k for k in range(-6, 6) if value_at([1, 0, a, b], k) < 0 < value_at([1, 0, a, b], k + 1))
    text = poly_text([1, 0, a, b])
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=(f"Phương trình {text} = 0 có đúng một nghiệm thực. Tìm số nguyên k sao cho nghiệm đó "
                   "nằm trong khoảng (k, k + 1)."),
        answer=str(k),
        solution_vi=[f"p(x) = {text} tăng ngặt (p'(x) = 3x^2 + {a} > 0), nên chỉ đổi dấu một lần.",
                     "Tính p tại các số nguyên liên tiếp cho tới khi thấy đổi dấu.",
                     f"p({k}) = {num(value_at([1, 0, a, b], k))} < 0 và p({k + 1}) = "
                     f"{num(value_at([1, 0, a, b], k + 1))} > 0.",
                     f"Theo định lý giá trị trung gian, nghiệm nằm trong ({k}, {k + 1}): k = {k}."])
