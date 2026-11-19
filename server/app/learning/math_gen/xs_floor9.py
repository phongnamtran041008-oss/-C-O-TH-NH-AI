"""Xác Suất và Thống Kê, tầng 9 (kiểm định giả thuyết: một tổng thể và so sánh hai tổng thể): generators.

The value of a test statistic is asked as an exact number: n is a perfect square, a sample is
built so that its corrected standard deviation is a whole number, a proportion test uses a
pair (p0, n) for which sqrt(p0(1 - p0)/n) is an exact decimal, and two known standard errors
form a Pythagorean triple. The decision (reject H0 or not) is a true/false statement whose
critical value is given in the prompt. tools/math_verify_xs_t7.py recomputes each statistic from
the raw numbers with sympy and decides by the p-value (from erf), not by the critical value."""
from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

from . import Draw, generator, num, paren
from .xs_floor7 import data_text, dec


# ------------------------------------------------------------------ kiểm định trung bình, biết sigma
@generator("xs_g9_z_trung_binh")
def z_trung_binh(rng: random.Random) -> Draw:
    k = rng.randint(3, 10)
    se = rng.choice([Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5)])
    sigma, n = se * k, k * k
    mu0 = rng.choice([20, 40, 50, 75, 100, 120, 250, 500])
    z = rng.choice([Fraction(v, 4) for v in range(-14, 15) if v not in (0,)])
    xbar = mu0 + z * se
    alt = rng.choice(["!=", ">", "<"])
    return Draw(
        params={"xbar": dec(xbar), "mu0": mu0, "sigma": dec(sigma), "n": n},
        prompt_vi=f"Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = {dec(sigma)} đã biết. Kiểm định "
                  f"H0: mu = {mu0} với đối thuyết H1: mu {alt} {mu0}. Một mẫu cỡ n = {n} có trung bình mẫu "
                  f"x_tb = {dec(xbar)}. Tính giá trị của thống kê kiểm định z = (x_tb - mu_0)/(sigma/sqrt(n)) "
                  f"(số thập phân đúng).",
        answer=dec(z),
        solution_vi=[f"sigma/sqrt(n) = {dec(sigma)}/{k} = {dec(se)}.",
                     f"z = ({dec(xbar)} - {mu0})/{dec(se)} = {dec(xbar - mu0)}/{dec(se)} = {dec(z)}."])


# ------------------------------------------------------------------ kiểm định trung bình, chưa biết sigma
def _patterns(n: int, spread: int) -> list[tuple[int, ...]]:
    """Deviations from the mean (sum 0) whose corrected variance is a nonzero perfect square."""
    out = []
    for devs in itertools.combinations_with_replacement(range(-spread, spread + 1), n):
        if sum(devs) == 0:
            ss = sum(d * d for d in devs)
            if ss and ss % (n - 1) == 0 and math.isqrt(ss // (n - 1)) ** 2 == ss // (n - 1):
                out.append(devs)
    return out


PATTERNS = {4: _patterns(4, 6), 9: _patterns(9, 5)}


@generator("xs_g9_t_trung_binh")
def t_trung_binh(rng: random.Random) -> Draw:
    n = rng.choice([4, 9])
    devs = list(rng.choice(PATTERNS[n]))
    rng.shuffle(devs)
    center = rng.randint(10, 60)
    xs = [center + d for d in devs]
    s = math.isqrt(sum(d * d for d in devs) // (n - 1))
    mu0 = center + rng.choice([d for d in range(-5, 6) if d])
    k = math.isqrt(n)
    t = Fraction(center - mu0) * k / s
    ss = sum(d * d for d in devs)
    return Draw(
        params={"data": xs, "mu0": mu0},
        prompt_vi=f"Một đại lượng có phân phối chuẩn, phương sai chưa biết. Kiểm định H0: mu = {mu0} với đối thuyết "
                  f"H1: mu != {mu0} từ một mẫu cỡ n = {n}: {data_text(xs)}. Tính giá trị của thống kê kiểm định "
                  f"t = (x_tb - mu_0)/(s/sqrt(n)), trong đó s là độ lệch chuẩn mẫu hiệu chỉnh (chia cho n - 1). "
                  f"Nhập một số hoặc phân số tối giản.",
        answer=num(t),
        solution_vi=[f"x_tb = {sum(xs)}/{n} = {center}.",
                     f"Tổng của (x_i - x_tb)^2 = {ss}; s^2 = {ss}/{n - 1} = {s * s}, s = {s}.",
                     f"s/sqrt(n) = {s}/{k} = {num(Fraction(s, k))}.",
                     f"t = ({center} - {mu0})/{paren(Fraction(s, k))} = {num(t)}."])


# ------------------------------------------------------------------ kiểm định tỷ lệ
# (p0, n): sqrt(p0 (1 - p0)/n) is an exact decimal
P0_SAMPLES = ((Fraction(1, 10), 100), (Fraction(1, 10), 400), (Fraction(1, 10), 900), (Fraction(1, 5), 100),
              (Fraction(1, 5), 400), (Fraction(1, 5), 625), (Fraction(1, 4), 300), (Fraction(3, 10), 525),
              (Fraction(2, 5), 150), (Fraction(2, 5), 600), (Fraction(1, 2), 100), (Fraction(1, 2), 400),
              (Fraction(1, 2), 625), (Fraction(3, 5), 600), (Fraction(4, 5), 400), (Fraction(9, 10), 900))


def _sqrt_fraction(q: Fraction) -> Fraction:
    a, b = math.isqrt(q.numerator), math.isqrt(q.denominator)
    assert a * a == q.numerator and b * b == q.denominator, q
    return Fraction(a, b)


@generator("xs_g9_ty_le")
def ty_le(rng: random.Random) -> Draw:
    while True:
        p0, n = rng.choice(P0_SAMPLES)
        se = _sqrt_fraction(p0 * (1 - p0) / n)
        z = rng.choice([Fraction(v, 2) for v in range(-6, 7) if v])
        m = n * (p0 + z * se)
        if m.denominator == 1 and 0 < m < n:
            break
    m = int(m)
    f = Fraction(m, n)
    return Draw(
        params={"p0": dec(p0), "n": n, "m": m},
        prompt_vi=f"Một nhà sản xuất công bố tỷ lệ p0 = {dec(p0)}. Kiểm định H0: p = {dec(p0)} từ một mẫu ngẫu nhiên "
                  f"{n} phần tử, trong đó có {m} phần tử có tính chất đang xét. Tính giá trị của thống kê kiểm định "
                  f"z = (f - p0)/sqrt(p0(1 - p0)/n), f là tần suất mẫu (số thập phân đúng).",
        answer=dec(z),
        solution_vi=[f"f = {m}/{n} = {dec(f)}.",
                     f"Khi H0 đúng: sqrt(p0(1 - p0)/n) = sqrt({dec(p0)} . {dec(1 - p0)}/{n}) = {dec(se)}.",
                     f"z = ({dec(f)} - {dec(p0)})/{dec(se)} = {dec(z)}."])


# ------------------------------------------------------------------ so sánh hai trung bình
# standard errors (a, b) of the two means with sqrt(a^2 + b^2) exact
TRIPLES = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (Fraction(3, 2), 2, Fraction(5, 2)), (Fraction(3, 5), Fraction(4, 5), 1),
           (Fraction(6, 5), Fraction(8, 5), 2), (8, 6, 10), (4, 3, 5))


@generator("xs_g9_hai_trung_binh")
def hai_trung_binh(rng: random.Random) -> Draw:
    a, b, c = (Fraction(v) for v in rng.choice(TRIPLES))
    k1, k2 = rng.choice([5, 6, 8, 10]), rng.choice([5, 6, 8, 10])
    s1, s2 = a * k1, b * k2
    n1, n2 = k1 * k1, k2 * k2
    z = rng.choice([Fraction(v, 2) for v in range(-6, 7) if v])
    x2 = Fraction(rng.randint(400, 900), 10)
    x1 = x2 + z * c
    return Draw(
        params={"x1": dec(x1), "x2": dec(x2), "s1": dec(s1), "s2": dec(s2), "n1": n1, "n2": n2},
        prompt_vi=f"Hai tổng thể có phân phối chuẩn với độ lệch chuẩn đã biết sigma_1 = {dec(s1)}, sigma_2 = {dec(s2)}. "
                  f"Hai mẫu độc lập: mẫu 1 cỡ n_1 = {n1} có trung bình x_tb1 = {dec(x1)}; mẫu 2 cỡ n_2 = {n2} có trung "
                  f"bình x_tb2 = {dec(x2)}. Kiểm định H0: mu_1 = mu_2. Tính giá trị của thống kê "
                  f"z = (x_tb1 - x_tb2)/sqrt(sigma_1^2/n_1 + sigma_2^2/n_2) (số thập phân đúng).",
        answer=dec(z),
        solution_vi=[f"sigma_1^2/n_1 = {dec(s1 * s1)}/{n1} = {dec(a * a)}; sigma_2^2/n_2 = {dec(s2 * s2)}/{n2} = "
                     f"{dec(b * b)}.",
                     f"Sai số chuẩn của hiệu: sqrt({dec(a * a)} + {dec(b * b)}) = sqrt({dec(c * c)}) = {dec(c)} "
                     "(cộng phương sai, không cộng độ lệch chuẩn).",
                     f"z = ({dec(x1)} - {dec(x2)})/{dec(c)} = {dec(x1 - x2)}/{dec(c)} = {dec(z)}."])


# ------------------------------------------------------------------ quyết định: bác bỏ H0 hay không
CRITICAL = {("!=", "0.05"): "1.96", ("!=", "0.01"): "2.58", (">", "0.05"): "1.645", (">", "0.01"): "2.33",
            ("<", "0.05"): "1.645", ("<", "0.01"): "2.33"}
Z_VALUES = (Fraction(1, 2), Fraction(1), Fraction(6, 5), Fraction(3, 2), Fraction(9, 5), Fraction(11, 5),
            Fraction(5, 2), Fraction(14, 5), Fraction(3))


@generator("xs_g9_quyet_dinh")
def quyet_dinh(rng: random.Random) -> Draw:
    k = rng.randint(3, 10)
    se = rng.choice([Fraction(1, 2), Fraction(1), Fraction(2), Fraction(4), Fraction(5)])
    sigma, n = se * k, k * k
    mu0 = rng.choice([30, 50, 80, 100, 200, 500])
    alt = rng.choice(["!=", ">", "<"])
    alpha = rng.choice(["0.05", "0.01"])
    z = rng.choice(Z_VALUES) * rng.choice([1, -1])
    xbar = mu0 + z * se
    crit = Fraction(CRITICAL[(alt, alpha)])
    if alt == "!=":
        reject = abs(z) > crit
        rule = f"hai phía: bác bỏ H0 khi |z| > {dec(crit)}"
        compare = f"|z| = {dec(abs(z))} {'>' if reject else '<'} {dec(crit)}"
    elif alt == ">":
        reject = z > crit
        rule = f"phía phải: bác bỏ H0 khi z > {dec(crit)}"
        compare = f"z = {dec(z)} {'>' if reject else '<'} {dec(crit)}"
    else:
        reject = z < -crit
        rule = f"phía trái: bác bỏ H0 khi z < -{dec(crit)}"
        compare = f"z = {dec(z)} {'<' if reject else '>'} -{dec(crit)}"
    return Draw(
        params={"xbar": dec(xbar), "mu0": mu0, "sigma": dec(sigma), "n": n, "alt": alt, "alpha": alpha},
        prompt_vi=f"Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = {dec(sigma)} đã biết. Kiểm định "
                  f"H0: mu = {mu0} với đối thuyết H1: mu {alt} {mu0} ở mức ý nghĩa {alpha}, dùng thống kê "
                  f"z = (x_tb - mu_0)/(sigma/sqrt(n)) và giá trị tới hạn {dec(crit)} (Phi({dec(crit)}) = "
                  f"{dec(Fraction(1, 2) - Fraction(alpha) / (2 if alt == '!=' else 1))}). Một mẫu cỡ n = {n} có "
                  f"x_tb = {dec(xbar)}. Khẳng định: với mẫu này, kiểm định bác bỏ H0.",
        answer=reject,
        solution_vi=[f"z = ({dec(xbar)} - {mu0})/({dec(sigma)}/{k}) = {dec(xbar - mu0)}/{dec(se)} = {dec(z)}.",
                     f"Miền bác bỏ {rule}.",
                     f"{compare}: {'bác bỏ H0, khẳng định đúng' if reject else 'chưa đủ cơ sở bác bỏ H0, khẳng định sai'}."])
