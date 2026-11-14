"""Đại Số Tuyến Tính, tầng 1 (tập hợp và ánh xạ): generators."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from . import Draw, generator, linear_text, nonzero, num, nums, paren, sample_distinct, set_text


def _two_sets(rng: random.Random, ok) -> tuple[list[int], list[int]]:
    """Two different sets of 3-5 numbers from 1..9 that pass `ok(a, b)`."""
    while True:
        a = sample_distinct(rng, 1, 9, rng.randint(3, 5))
        b = sample_distinct(rng, 1, 9, rng.randint(3, 5))
        if a != b and ok(a, b):
            return a, b


# ------------------------------------------------------------------ tập hợp và phần tử
@generator("dstt_g1_thuoc")
def thuoc(rng: random.Random) -> Draw:
    els = sample_distinct(rng, 1, 15, rng.randint(4, 6))
    inside = rng.random() < 0.5
    k = rng.choice(els) if inside else rng.choice([v for v in range(1, 16) if v not in els])
    return Draw(
        params={"elements": els, "k": k},
        prompt_vi=f"Cho A = {set_text(els)}. Số {k} thuộc A.",
        answer=inside,
        solution_vi=[f"Các phần tử của A là {nums(els)}.",
                     f"Số {k} {'có' if inside else 'không có'} trong danh sách đó nên {k} "
                     f"{'thuộc' if inside else 'không thuộc'} A."])


@generator("dstt_g1_so_tap_con")
def so_tap_con(rng: random.Random) -> Draw:
    n = rng.randint(3, 6)
    els = sample_distinct(rng, 1, 12, n)
    return Draw(
        params={"elements": els},
        prompt_vi=f"Tập A = {set_text(els)} có bao nhiêu tập con, kể cả tập rỗng và chính A?",
        answer=str(2 ** n),
        solution_vi=[f"A có {n} phần tử.",
                     "Khi lập một tập con, mỗi phần tử có 2 khả năng: được chọn hoặc không được chọn.",
                     f"Số tập con là 2^{n} = {2 ** n}."])


# ------------------------------------------------------------------ phép toán trên tập hợp
@generator("dstt_g1_giao")
def giao(rng: random.Random) -> Draw:
    a, b = _two_sets(rng, lambda a, b: 1 <= len(set(a) & set(b)) < min(len(a), len(b)))
    inter = sorted(set(a) & set(b))
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=f"Cho A = {set_text(a)} và B = {set_text(b)}. Liệt kê các phần tử của A giao B.",
        answer=nums(inter), unordered=True,
        solution_vi=["A giao B gồm các phần tử thuộc cả A và B.",
                     f"Các phần tử có mặt trong cả hai tập: {nums(inter)}.",
                     f"A giao B = {set_text(inter)}."])


@generator("dstt_g1_hop_dem")
def hop_dem(rng: random.Random) -> Draw:
    a, b = _two_sets(rng, lambda a, b: len(set(a) & set(b)) >= 1)
    union = sorted(set(a) | set(b))
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=f"Cho A = {set_text(a)} và B = {set_text(b)}. A hợp B có bao nhiêu phần tử?",
        answer=str(len(union)),
        solution_vi=["A hợp B gồm các phần tử thuộc A hoặc thuộc B, mỗi phần tử chỉ tính một lần.",
                     f"A hợp B = {set_text(union)}.",
                     f"Có {len(union)} phần tử."])


@generator("dstt_g1_hieu")
def hieu(rng: random.Random) -> Draw:
    a, b = _two_sets(rng, lambda a, b: 1 <= len(set(a) - set(b)) < len(a))
    diff = sorted(set(a) - set(b))
    common = sorted(set(a) & set(b))
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=f"Cho A = {set_text(a)} và B = {set_text(b)}. Liệt kê các phần tử của hiệu A \\ B.",
        answer=nums(diff), unordered=True,
        solution_vi=["A \\ B gồm các phần tử thuộc A nhưng không thuộc B.",
                     f"Bỏ khỏi A các phần tử cũng thuộc B: {nums(common)}.",
                     f"A \\ B = {set_text(diff)}."])


# ------------------------------------------------------------------ tích Descartes
@generator("dstt_g1_tich_dem")
def tich_dem(rng: random.Random) -> Draw:
    m, n = rng.randint(2, 5), rng.randint(2, 5)
    a = sample_distinct(rng, 0, 9, m)
    b = sorted(rng.sample("abcdefgh", n))
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=f"Cho A = {set_text(a)} và B = {{{', '.join(b)}}}. Tích Descartes A x B có bao nhiêu phần tử?",
        answer=str(m * n),
        solution_vi=["Mỗi phần tử của A x B là một cặp (x, y) với x thuộc A và y thuộc B.",
                     f"Có {m} cách chọn x và {n} cách chọn y.",
                     f"Số cặp là {m} . {n} = {m * n}."])


@generator("dstt_g1_tich_nguoc")
def tich_nguoc(rng: random.Random) -> Draw:
    m, n = rng.randint(2, 7), rng.randint(2, 9)
    return Draw(
        params={"pairs": m * n, "a_size": m},
        prompt_vi=f"Tập A x B có {m * n} phần tử và A có {m} phần tử. B có bao nhiêu phần tử?",
        answer=str(n),
        solution_vi=["Số phần tử của A x B bằng số phần tử của A nhân với số phần tử của B.",
                     f"Gọi n là số phần tử của B: {m} . n = {m * n}.",
                     f"n = {n}."])


# ------------------------------------------------------------------ ánh xạ, ảnh và tạo ảnh
@generator("dstt_g1_anh_bac_nhat")
def anh_bac_nhat(rng: random.Random) -> Draw:
    a, b, c = nonzero(rng, -5, 5), rng.randint(-9, 9), rng.randint(-5, 5)
    value = a * c + b
    return Draw(
        params={"a": a, "b": b, "x": c},
        prompt_vi=f"Cho ánh xạ f: R -> R, f(x) = {linear_text(a, b)}. Tính f({c}).",
        answer=str(value),
        solution_vi=[f"Thay x = {c} vào công thức của f.",
                     f"f({c}) = {paren(a)} . {paren(c)} + {paren(b)} = {value}."])


@generator("dstt_g1_anh_tap")
def anh_tap(rng: random.Random) -> Draw:
    c = rng.randint(-3, 5)
    k = rng.randint(1, 3)
    others = rng.sample([v for v in range(-3, 4) if abs(v) != k], rng.randint(2, 3))
    dom = sorted({k, -k, *others})
    expr = "x^2" if c == 0 else f"x^2 {'+' if c > 0 else '-'} {abs(c)}"
    image = sorted({x * x + c for x in dom})
    return Draw(
        params={"c": c, "domain": dom},
        prompt_vi=f"Cho f: R -> R, f(x) = {expr} và A = {set_text(dom)}. Liệt kê các phần tử của ảnh f(A).",
        answer=nums(image), unordered=True,
        solution_vi=["f(A) gồm ảnh của mọi phần tử thuộc A.",
                     "; ".join(f"f({x}) = {x * x + c}" for x in dom) + ".",
                     f"Mỗi giá trị chỉ viết một lần: f(A) = {set_text(image)}."])


# ------------------------------------------------------------------ đơn ánh, toàn ánh, song ánh
@generator("dstt_g1_don_anh")
def don_anh(rng: random.Random) -> Draw:
    kind = rng.choice(["linear", "square", "cube", "abs"])
    c = rng.randint(-9, 9)
    tail = "" if c == 0 else f" {'+' if c > 0 else '-'} {abs(c)}"
    if kind == "linear":
        a = nonzero(rng, -5, 5)
        expr, injective = linear_text(a, c), True
        steps = [f"Nếu f(u) = f(v) thì {linear_text(a, c, 'u')} = {linear_text(a, c, 'v')}, suy ra u = v.",
                 "Hai phần tử khác nhau luôn có ảnh khác nhau, nên f là đơn ánh."]
        params = {"kind": kind, "a": a, "c": c}
    elif kind == "cube":
        expr, injective = "x^3" + tail, True
        steps = ["Hàm x^3 tăng ngặt trên R, cộng thêm một hằng số thì vẫn tăng ngặt.",
                 "Hàm tăng ngặt cho hai phần tử khác nhau hai ảnh khác nhau, nên f là đơn ánh."]
        params = {"kind": kind, "c": c}
    else:
        expr, injective = ("x^2" if kind == "square" else "|x|") + tail, False
        steps = [f"f(1) = f(-1) = {1 + c} dù 1 khác -1.",
                 "Có hai phần tử khác nhau cùng một ảnh, nên f không phải là đơn ánh."]
        params = {"kind": kind, "c": c}
    return Draw(params=params, prompt_vi=f"Ánh xạ f: R -> R, f(x) = {expr} là đơn ánh.",
                answer=injective, solution_vi=steps)


@generator("dstt_g1_dem_don_anh")
def dem_don_anh(rng: random.Random) -> Draw:
    m = rng.randint(2, 4)
    n = rng.randint(m, 6)
    value = math.perm(n, m)
    return Draw(
        params={"m": m, "n": n},
        prompt_vi=f"Có bao nhiêu đơn ánh từ một tập có {m} phần tử vào một tập có {n} phần tử?",
        answer=str(value),
        solution_vi=[f"Ảnh của phần tử thứ nhất có {n} cách chọn.",
                     "Đơn ánh không cho hai phần tử chung một ảnh, nên mỗi phần tử tiếp theo có ít hơn một cách chọn.",
                     f"Số đơn ánh là {' . '.join(str(n - i) for i in range(m))} = {value}."])


# ------------------------------------------------------------------ ánh xạ hợp và ánh xạ ngược
@generator("dstt_g1_hop_thanh")
def hop_thanh(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -4, 4), rng.randint(-6, 6)
    c, d = nonzero(rng, -4, 4), rng.randint(-6, 6)
    k = rng.randint(-4, 4)
    inner = a * k + b
    value = c * inner + d
    return Draw(
        params={"f": [a, b], "g": [c, d], "x": k},
        prompt_vi=f"Cho f(x) = {linear_text(a, b)} và g(x) = {linear_text(c, d)}. Tính g(f({k})).",
        answer=str(value),
        solution_vi=[f"Tính từ trong ra ngoài: f({k}) = {inner}.",
                     f"g(f({k})) = g({inner}) = {value}."])


@generator("dstt_g1_nguoc")
def nguoc(rng: random.Random) -> Draw:
    a, b, y = nonzero(rng, -5, 5), rng.randint(-9, 9), rng.randint(-12, 12)
    x = Fraction(y - b, a)
    return Draw(
        params={"a": a, "b": b, "y": y},
        prompt_vi=(f"Cho song ánh f: R -> R, f(x) = {linear_text(a, b)}. Tìm x sao cho f(x) = {y}, "
                   f"tức là giá trị của ánh xạ ngược tại {y}."),
        answer=num(x),
        solution_vi=[f"Giải phương trình {linear_text(a, b)} = {y}.",
                     f"{linear_text(a, 0)} = {y - b} nên x = {num(x)}.",
                     f"Ánh xạ ngược của f nhận giá trị {num(x)} tại {y}."])
