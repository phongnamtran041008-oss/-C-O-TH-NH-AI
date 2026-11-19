"""Xác Suất và Thống Kê, tầng 5 (biến ngẫu nhiên, bảng phân phối, hàm phân phối, mật độ): generators.

The floor follows the course's convention F(x) = P(X < x): a jump of F at a value v shows up
only for x > v. Densities are polynomials k x^n on [0, a], so every integral is exact. The
answers come from closed forms; tools/math_verify_xs_t4.py recomputes them with sympy.stats
(FiniteRV, P), by listing the draws one by one, or by integrating and solving with sympy."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from . import Draw, generator, num, paren

# tables: denominators that give readable fractions
DENOMS = (8, 10, 12, 20)


def _table(rng: random.Random, size: int) -> tuple[list[int], list[Fraction]]:
    """size values and positive probabilities with one common denominator, summing to 1."""
    d = rng.choice(DENOMS)
    cuts = sorted(rng.sample(range(1, d), size - 1))
    parts = [b - a for a, b in zip([0, *cuts], [*cuts, d])]
    start = rng.randint(-2, 2)
    values = list(range(start, start + size))
    return values, [Fraction(p, d) for p in parts]


def _table_text(values, probs) -> str:
    return (f"X nhận các giá trị {', '.join(map(str, values))} với xác suất lần lượt "
            f"{', '.join(num(p) for p in probs)}")


# ------------------------------------------------------------------ bảng phân phối
@generator("xs_g5_bang_thieu")
def bang_thieu(rng: random.Random) -> Draw:
    size = rng.randint(3, 5)
    values, probs = _table(rng, size)
    hole = rng.randrange(size)
    shown = [("p" if n == hole else num(p)) for n, p in enumerate(probs)]
    others = [p for n, p in enumerate(probs) if n != hole]
    return Draw(
        params={"values": values, "shown": shown},
        prompt_vi=f"Biến ngẫu nhiên rời rạc X nhận các giá trị {', '.join(map(str, values))} với xác suất lần lượt "
                  f"{', '.join(shown)}. Tìm p.",
        answer=num(probs[hole]),
        solution_vi=["Trong một bảng phân phối, các xác suất cộng lại bằng 1.",
                     f"p = 1 - ({' + '.join(num(p) for p in others)}) = 1 - {num(sum(others))} = {num(probs[hole])}."])


@generator("xs_g5_rut_bi_bang")
def rut_bi_bang(rng: random.Random) -> Draw:
    red, blue = rng.randint(2, 5), rng.randint(2, 5)
    m = rng.randint(2, 3)
    k = rng.randint(max(0, m - blue), min(m, red))
    ans = Fraction(math.comb(red, k) * math.comb(blue, m - k), math.comb(red + blue, m))
    return Draw(
        params={"red": red, "blue": blue, "m": m, "k": k},
        prompt_vi=f"Một hộp có {red} bi đỏ và {blue} bi xanh. Lấy ngẫu nhiên cùng lúc {m} bi. Gọi X là số bi đỏ "
                  f"lấy được. Tính P(X = {k}) trong bảng phân phối của X.",
        answer=num(ans),
        solution_vi=[f"Không gian mẫu: C({red + blue}, {m}) = {math.comb(red + blue, m)} cách lấy đồng khả năng.",
                     f"X = {k}: chọn {k} bi đỏ trong {red} và {m - k} bi xanh trong {blue}: "
                     f"C({red}, {k}) . C({blue}, {m - k}) = {math.comb(red, k) * math.comb(blue, m - k)} cách.",
                     f"P(X = {k}) = {math.comb(red, k) * math.comb(blue, m - k)}/{math.comb(red + blue, m)} "
                     f"= {num(ans)}."])


# ------------------------------------------------------------------ hàm phân phối
@generator("xs_g5_ham_phan_phoi")
def ham_phan_phoi(rng: random.Random) -> Draw:
    size = rng.randint(3, 5)
    values, probs = _table(rng, size)
    c = rng.randint(values[0], values[-1] + 1)
    below = [(v, p) for v, p in zip(values, probs) if v < c]
    ans = sum((p for _, p in below), Fraction(0))
    if below:
        how = (f"Các giá trị nhỏ hơn hẳn {c} là {', '.join(str(v) for v, _ in below)}, nên "
               f"F({c}) = {' + '.join(num(p) for _, p in below)} = {num(ans)}.")
    else:
        how = f"Không có giá trị nào của X nhỏ hơn {c}, nên F({c}) = 0."
    return Draw(
        params={"values": values, "probs": [num(p) for p in probs], "c": c},
        prompt_vi=f"Biến ngẫu nhiên rời rạc {_table_text(values, probs)}. Với hàm phân phối F(x) = P(X < x), "
                  f"tính F({c}).",
        answer=num(ans),
        solution_vi=[f"F({c}) = P(X < {c}): cộng xác suất của các giá trị nhỏ hơn hẳn {c}, "
                     f"không tính giá trị bằng {c}.", how])


# ------------------------------------------------------------------ hàm mật độ
def _density_setup(rng: random.Random):
    n = rng.randint(1, 3)
    a = rng.randint(1, 4)
    k = Fraction(n + 1, a ** (n + 1))         # the integral of k x^n over [0, a] is k a^(n+1)/(n+1)
    return n, a, k


def _coef(c: Fraction) -> str:
    return "" if c == 1 else paren(c)


def _power(n: int) -> str:
    return "x" if n == 1 else f"x^{n}"


@generator("xs_g5_hang_so")
def hang_so(rng: random.Random) -> Draw:
    n, a, k = _density_setup(rng)
    return Draw(
        params={"n": n, "a": a},
        prompt_vi=f"Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = k{_power(n)} khi 0 <= x <= {a} và f(x) = 0 "
                  f"khi x nằm ngoài [0, {a}]. Tìm hằng số k.",
        answer=num(k),
        solution_vi=["Tích phân của hàm mật độ trên cả trục số phải bằng 1; ngoài [0, " + str(a) + "] f bằng 0.",
                     f"Tích phân của k{_power(n)} từ 0 đến {a} là k . {a}^{n + 1}/{n + 1} = k . {num(Fraction(a ** (n + 1), n + 1))}.",
                     f"Cho bằng 1: k = {num(k)}."])


@generator("xs_g5_mat_do_tf")
def mat_do_tf(rng: random.Random) -> Draw:
    n, a, k = _density_setup(rng)
    shown = rng.choice([k, k, 2 * k, k / 2, Fraction(1, a)])
    ok = shown == k
    total = shown * Fraction(a ** (n + 1), n + 1)
    return Draw(
        params={"n": n, "a": a, "k": num(shown)},
        prompt_vi=f"Hàm f(x) = {_coef(shown)}{_power(n)} khi 0 <= x <= {a} và f(x) = 0 khi x nằm ngoài [0, {a}] "
                  f"là hàm mật độ của một biến ngẫu nhiên liên tục.",
        answer=ok,
        solution_vi=["Hàm mật độ cần f(x) >= 0 với mọi x (ở đây đúng) và tích phân trên cả trục số bằng 1.",
                     f"Tích phân của {_coef(shown)}{_power(n)} từ 0 đến {a} là {paren(shown)} . {a}^{n + 1}/{n + 1} "
                     f"= {num(total)}.",
                     "Tích phân bằng 1 nên f là hàm mật độ." if ok
                     else f"Tích phân bằng {num(total)}, khác 1, nên f không là hàm mật độ."])


# ------------------------------------------------------------------ xác suất rơi vào một khoảng
@generator("xs_g5_khoang")
def khoang(rng: random.Random) -> Draw:
    n, a, k = _density_setup(rng)
    lo, hi = sorted(rng.sample([Fraction(j, 2) for j in range(0, 2 * a + 1)], 2))
    big = rng.random() < 0.25                  # sometimes the interval runs past a
    if big:
        hi = Fraction(a + rng.randint(1, 2))

    def cdf(x: Fraction) -> Fraction:
        x = min(max(x, Fraction(0)), Fraction(a))
        return (x / a) ** (n + 1)

    ans = cdf(hi) - cdf(lo)

    def txt(x: Fraction) -> str:
        return str(x.numerator // x.denominator) if x.denominator == 1 else f"{float(x):g}"

    return Draw(
        params={"n": n, "a": a, "lo": num(lo), "hi": num(hi)},
        prompt_vi=f"Biến ngẫu nhiên liên tục X có hàm mật độ f(x) = {_coef(k)}{_power(n)} khi 0 <= x <= {a} và "
                  f"f(x) = 0 khi x nằm ngoài [0, {a}]. Tính P({txt(lo)} <= X < {txt(hi)}).",
        answer=num(ans),
        solution_vi=[f"Hàm phân phối trên [0, {a}]: F(x) = tích phân của f từ 0 đến x = (x/{a})^{n + 1}; "
                     f"F(x) = 0 khi x <= 0 và F(x) = 1 khi x > {a}.",
                     f"P({txt(lo)} <= X < {txt(hi)}) = F({txt(hi)}) - F({txt(lo)}) = {num(cdf(hi))} - "
                     f"{num(cdf(lo))} = {num(ans)}."])
