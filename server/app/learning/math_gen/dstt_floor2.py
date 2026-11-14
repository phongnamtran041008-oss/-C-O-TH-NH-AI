"""Đại Số Tuyến Tính, tầng 2 (số phức): generators. A complex answer is typed as two
numbers: the real part, then the imaginary part."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, complex_text, generator, nonzero, num, nums, paren

RE_IM = "Nhập phần thực và phần ảo, cách nhau bằng dấu phẩy."
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (20, 21, 29)]
# direction of z -> (argument in degrees, where the point is)
DIRECTIONS = [
    ((1, 0), 0, "trên tia dương của trục thực"),
    ((1, 1), 45, "trên tia phân giác của góc phần tư thứ nhất"),
    ((0, 1), 90, "trên tia dương của trục ảo"),
    ((-1, 1), 135, "trên tia phân giác của góc phần tư thứ hai"),
    ((-1, 0), 180, "trên tia âm của trục thực"),
    ((-1, -1), 225, "trên tia phân giác của góc phần tư thứ ba"),
    ((0, -1), 270, "trên tia âm của trục ảo"),
    ((1, -1), 315, "trên tia phân giác của góc phần tư thứ tư"),
]


def _mul(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


# ------------------------------------------------------------------ dạng đại số
@generator("dstt_g2_phan_thuc_ao")
def phan_thuc_ao(rng: random.Random) -> Draw:
    a, b = rng.randint(-9, 9), nonzero(rng, -9, 9)
    part = rng.choice(["re", "im"])
    name = "thực" if part == "re" else "ảo"
    value = a if part == "re" else b
    return Draw(
        params={"re": a, "im": b, "part": part},
        prompt_vi=f"Cho số phức z = {complex_text(a, b)}. Phần {name} của z bằng bao nhiêu?",
        answer=str(value),
        solution_vi=[f"Viết z ở dạng a + bi với a = {a} và b = {b}.",
                     "Phần thực là a; phần ảo là b, tức là hệ số của i (không kèm i).",
                     f"Phần {name} của z là {value}."])


@generator("dstt_g2_luy_thua_i")
def luy_thua_i(rng: random.Random) -> Draw:
    n = rng.randint(5, 60)
    r = n % 4
    re, im = [(1, 0), (0, 1), (-1, 0), (0, -1)][r]
    cycle = (f"{n} chia hết cho 4, nên i^{n} = 1." if r == 0
             else f"{n} chia 4 dư {r}, nên i^{n} = i^{r} = {complex_text(re, im)}.")
    return Draw(
        params={"n": n},
        prompt_vi=f"Tính i^{n}. {RE_IM}",
        answer=nums([re, im]),
        solution_vi=["Lũy thừa của i lặp lại theo chu kỳ 4: i^1 = i, i^2 = -1, i^3 = -i, i^4 = 1.",
                     cycle,
                     f"Phần thực là {re}, phần ảo là {im}."])


# ------------------------------------------------------------------ cộng, trừ, nhân
@generator("dstt_g2_cong_tru")
def cong_tru(rng: random.Random) -> Draw:
    a, b = rng.randint(-9, 9), nonzero(rng, -9, 9)
    c, d = rng.randint(-9, 9), nonzero(rng, -9, 9)
    op = rng.choice(["+", "-"])
    sign = 1 if op == "+" else -1
    re, im = a + sign * c, b + sign * d
    verb = "Cộng" if op == "+" else "Trừ"
    return Draw(
        params={"z": [a, b], "w": [c, d], "op": op},
        prompt_vi=f"Cho z = {complex_text(a, b)} và w = {complex_text(c, d)}. Tính z {op} w. {RE_IM}",
        answer=nums([re, im]),
        solution_vi=[f"{verb} riêng phần thực với phần thực, phần ảo với phần ảo.",
                     f"Phần thực: {paren(a)} {op} {paren(c)} = {re}. Phần ảo: {paren(b)} {op} {paren(d)} = {im}.",
                     f"z {op} w = {complex_text(re, im)}."])


@generator("dstt_g2_nhan")
def nhan(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -5, 5), nonzero(rng, -5, 5)
    c, d = nonzero(rng, -5, 5), nonzero(rng, -5, 5)
    re, im = _mul((a, b), (c, d))
    return Draw(
        params={"z": [a, b], "w": [c, d]},
        prompt_vi=f"Tính ({complex_text(a, b)})({complex_text(c, d)}). {RE_IM}",
        answer=nums([re, im]),
        solution_vi=[f"Nhân từng số hạng. Không chứa i: {paren(a)} . {paren(c)} = {a * c}. "
                     f"Chứa i: {paren(a)} . {paren(d)} + {paren(b)} . {paren(c)} = {a * d + b * c}. "
                     f"Chứa i^2: {paren(b)} . {paren(d)} = {b * d}.",
                     f"Vì i^2 = -1, số hạng chứa i^2 đổi dấu rồi nhập vào phần thực: {a * c} - {paren(b * d)} = {re}.",
                     f"Kết quả: {complex_text(re, im)}."])


# ------------------------------------------------------------------ liên hợp và môđun
@generator("dstt_g2_modun")
def modun(rng: random.Random) -> Draw:
    x, y, r = rng.choice(TRIPLES)
    if rng.random() < 0.5:
        x, y = y, x
    a, b = x * rng.choice([1, -1]), y * rng.choice([1, -1])
    return Draw(
        params={"re": a, "im": b},
        prompt_vi=f"Tính môđun của số phức z = {complex_text(a, b)}.",
        answer=str(r),
        solution_vi=["Môđun của z = a + bi là căn bậc hai của a^2 + b^2.",
                     f"a^2 + b^2 = {a * a} + {b * b} = {a * a + b * b}.",
                     f"|z| = {r}."])


@generator("dstt_g2_lien_hop")
def lien_hop(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -7, 7), nonzero(rng, -7, 7)
    kind = rng.choice(["product", "sum"])
    z, conj = complex_text(a, b), complex_text(a, -b)
    if kind == "product":
        value = a * a + b * b
        ask = "Tính tích của z với số phức liên hợp của nó."
        steps = [f"Số phức liên hợp của z là {conj}.",
                 "Tích của a + bi với a - bi bằng a^2 + b^2.",
                 f"{a * a} + {b * b} = {value}."]
    else:
        value = 2 * a
        ask = "Tính tổng của z và số phức liên hợp của nó."
        steps = [f"Số phức liên hợp của z là {conj}.",
                 "Khi cộng, hai phần ảo triệt tiêu nhau và phần thực được nhân đôi.",
                 f"Tổng là 2 . {paren(a)} = {value}."]
    return Draw(params={"re": a, "im": b, "kind": kind}, prompt_vi=f"Cho z = {z}. {ask}",
                answer=str(value), solution_vi=steps)


# ------------------------------------------------------------------ chia
@generator("dstt_g2_chia_i")
def chia_i(rng: random.Random) -> Draw:
    a, b = nonzero(rng, -9, 9), nonzero(rng, -9, 9)
    z = complex_text(a, b)
    return Draw(
        params={"z": [a, b]},
        prompt_vi=f"Tính ({z}) / i. {RE_IM}",
        answer=nums([b, -a]),
        solution_vi=["Nhân cả tử và mẫu với -i, là số phức liên hợp của i: mẫu thành i . (-i) = 1.",
                     f"Tử thành ({z}) . (-i) = {complex_text(b, -a)}.",
                     f"Phần thực là {b}, phần ảo là {-a}."])


@generator("dstt_g2_chia")
def chia(rng: random.Random) -> Draw:
    a, b = rng.randint(-6, 6), nonzero(rng, -6, 6)
    c, d = nonzero(rng, -4, 4), nonzero(rng, -4, 4)
    n = c * c + d * d
    top_re, top_im = _mul((a, b), (c, -d))
    re, im = Fraction(top_re, n), Fraction(top_im, n)
    z, w, conj = complex_text(a, b), complex_text(c, d), complex_text(c, -d)
    return Draw(
        params={"z": [a, b], "w": [c, d]},
        prompt_vi=(f"Tính ({z}) / ({w}). Nhập phần thực và phần ảo (có thể là phân số), "
                   "cách nhau bằng dấu phẩy."),
        answer=nums([re, im]),
        solution_vi=[f"Nhân cả tử và mẫu với số phức liên hợp của mẫu là {conj}.",
                     f"Mẫu: {c * c} + {d * d} = {n}.",
                     f"Tử: ({z})({conj}) = {complex_text(top_re, top_im)}.",
                     f"Chia cho {n}: phần thực {num(re)}, phần ảo {num(im)}."])


# ------------------------------------------------------------------ dạng lượng giác, Moivre
@generator("dstt_g2_acgumen")
def acgumen(rng: random.Random) -> Draw:
    (dx, dy), degrees, where = rng.choice(DIRECTIONS)
    k = rng.randint(1, 6)
    a, b = dx * k, dy * k
    return Draw(
        params={"re": a, "im": b},
        prompt_vi=(f"Tìm acgumen của số phức z = {complex_text(a, b)}, tính bằng độ, "
                   "trong khoảng từ 0 đến dưới 360."),
        answer=str(degrees),
        solution_vi=[f"Điểm biểu diễn z trên mặt phẳng phức là ({a}, {b}).",
                     f"Điểm này nằm {where}.",
                     f"Góc quay từ tia dương của trục thực đến tia đó là {degrees} độ."])


@generator("dstt_g2_moivre")
def moivre(rng: random.Random) -> Draw:
    base = rng.choice([(1, 1), (1, -1), (-1, 1), (-1, -1)])
    n = rng.randint(2, 10)
    degrees = next(deg for d, deg, _ in DIRECTIONS if d == base)
    value = (1, 0)
    for _ in range(n):
        value = _mul(value, base)
    return Draw(
        params={"base": list(base), "n": n},
        prompt_vi=f"Dùng dạng lượng giác và công thức Moivre, tính ({complex_text(*base)})^{n}. {RE_IM}",
        answer=nums(value),
        solution_vi=[f"{complex_text(*base)} có môđun là căn bậc hai của 2 và acgumen {degrees} độ.",
                     f"Theo công thức Moivre, lũy thừa bậc {n} có môđun (căn bậc hai của 2)^{n} và acgumen "
                     f"{n} . {degrees} = {n * degrees} độ, cùng hướng với góc {n * degrees % 360} độ.",
                     f"Kết quả: {complex_text(*value)}."])


# ------------------------------------------------------------------ căn bậc n
@generator("dstt_g2_so_nghiem")
def so_nghiem(rng: random.Random) -> Draw:
    n = rng.randint(2, 9)
    a, b = rng.randint(-6, 6), rng.randint(-6, 6)
    if a == 0 and b == 0:
        a = 1
    return Draw(
        params={"n": n, "c": [a, b]},
        prompt_vi=f"Phương trình z^{n} = {complex_text(a, b)} có bao nhiêu nghiệm phức phân biệt?",
        answer=str(n),
        solution_vi=["Nghiệm của phương trình là các căn bậc n của vế phải.",
                     "Mọi số phức khác 0 có đúng n căn bậc n phân biệt.",
                     f"Vế phải khác 0 nên phương trình có {n} nghiệm phân biệt."])


@generator("dstt_g2_can_bac_hai")
def can_bac_hai(rng: random.Random) -> Draw:
    p, q = rng.randint(1, 5), nonzero(rng, -5, 5)
    re, im = _mul((p, q), (p, q))
    return Draw(
        params={"w": [re, im]},
        prompt_vi=(f"Số phức w = {complex_text(re, im)} có hai căn bậc hai. Tìm căn có phần thực dương. "
                   f"{RE_IM}"),
        answer=nums([p, q]),
        solution_vi=["Gọi căn cần tìm là x + yi. Bình phương lên: x^2 - y^2 bằng phần thực của w và 2xy "
                     "bằng phần ảo của w.",
                     f"x^2 - y^2 = {re} và 2xy = {im}. Thêm nữa x^2 + y^2 = |w| = {p * p + q * q}.",
                     f"Suy ra x^2 = {p * p} và y^2 = {q * q}. Lấy x = {p} dương thì y = {q} để 2xy = {im}.",
                     f"Căn cần tìm là {complex_text(p, q)}."])
