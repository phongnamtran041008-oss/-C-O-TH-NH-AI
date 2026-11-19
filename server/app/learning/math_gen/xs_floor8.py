"""Xác Suất và Thống Kê, tầng 8 (khoảng tin cậy cho trung bình và tỷ lệ, cỡ mẫu, luật số lớn và bất
đẳng thức Chebyshev, định lý giới hạn trung tâm): generators.

Every prompt gives the critical value it needs (z = 1.96, t(15; 0.025) = 2.131, a value of the
Laplace function), and the data are built so that the standard error is an exact decimal: n is a
perfect square for a mean, and f(1 - f)/n is the square of a decimal for a proportion. So every
answer is an exact decimal or a whole number, never a rounded one. tools/math_verify_xs_t7.py
recomputes them another way: it solves |x_tb - mu| = epsilon for mu, searches the smallest n by
bisection, and rebuilds the table values from erf and the Student law."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from . import Draw, generator, num, paren
from .xs_floor7 import LAPLACE, Z_STEPS, dec, phi, z_text

# level -> (z, Phi(z)) for a two-sided interval
Z_LEVELS = {"90%": ("1.645", "0.45"), "95%": ("1.96", "0.475"), "99%": ("2.58", "0.495")}
# (degrees of freedom, upper tail) -> Student critical value t(df; tail): P(T > t) = tail
T_TABLE = {(3, "0.025"): "3.182", (3, "0.05"): "2.353", (8, "0.025"): "2.306", (8, "0.05"): "1.860",
           (15, "0.025"): "2.131", (15, "0.05"): "1.753", (24, "0.025"): "2.064", (24, "0.05"): "1.711"}


def _z_given(level: str) -> str:
    z, p = Z_LEVELS[level]
    return f"z = {z} (Phi({z}) = {p})" if level != "99%" else f"z = {z}"


# ------------------------------------------------------------------ khoảng tin cậy cho trung bình
@generator("xs_g8_khoang_biet_sigma")
def khoang_biet_sigma(rng: random.Random) -> Draw:
    k = rng.randint(3, 10)
    se = rng.choice([Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(4), Fraction(5)])
    sigma, n = se * k, k * k
    xbar = Fraction(rng.randint(200, 1800), 10)
    level = rng.choice(list(Z_LEVELS))
    z = Fraction(Z_LEVELS[level][0])
    eps = z * se
    lo, hi = xbar - eps, xbar + eps
    return Draw(
        params={"xbar": dec(xbar), "sigma": dec(sigma), "n": n, "z": dec(z)},
        prompt_vi=f"Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = {dec(sigma)} đã biết. Một mẫu cỡ "
                  f"n = {n} có trung bình mẫu x_tb = {dec(xbar)}. Lập khoảng tin cậy đối xứng độ tin cậy {level} cho "
                  f"kỳ vọng mu, dùng {_z_given(level)}. Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, "
                  f"không làm tròn).",
        answer=f"{dec(lo)}, {dec(hi)}",
        solution_vi=["Biết sigma: khoảng tin cậy (x_tb - epsilon; x_tb + epsilon) với epsilon = z sigma/sqrt(n).",
                     f"sigma/sqrt(n) = {dec(sigma)}/{k} = {dec(se)}; epsilon = {dec(z)} . {dec(se)} = {dec(eps)}.",
                     f"Khoảng tin cậy: ({dec(xbar)} - {dec(eps)}; {dec(xbar)} + {dec(eps)}) = ({dec(lo)}; {dec(hi)})."])


@generator("xs_g8_khoang_t")
def khoang_t(rng: random.Random) -> Draw:
    n = rng.choice([4, 9, 16, 25])
    k, df = math.isqrt(n), n - 1
    se = rng.choice([Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3)])
    s = se * k
    xbar = Fraction(rng.randint(100, 900), 10)
    level, tail = rng.choice([("95%", "0.025"), ("90%", "0.05")])
    t = Fraction(T_TABLE[(df, tail)])
    eps = t * se
    lo, hi = xbar - eps, xbar + eps
    return Draw(
        params={"xbar": dec(xbar), "s": dec(s), "n": n, "t": dec(t)},
        prompt_vi=f"Một đại lượng có phân phối chuẩn, phương sai chưa biết. Một mẫu cỡ n = {n} có trung bình mẫu "
                  f"x_tb = {dec(xbar)} và độ lệch chuẩn mẫu hiệu chỉnh s = {dec(s)}. Lập khoảng tin cậy đối xứng độ "
                  f"tin cậy {level} cho kỳ vọng mu, dùng giá trị tới hạn Student t({df}; {tail}) = {dec(t)} (tức "
                  f"P(T > {dec(t)}) = {tail} với T có phân phối Student {df} bậc tự do). Nhập hai đầu mút, đầu nhỏ "
                  f"trước (số thập phân đúng, không làm tròn).",
        answer=f"{dec(lo)}, {dec(hi)}",
        solution_vi=[f"Chưa biết sigma, mẫu nhỏ: dùng phân phối Student n - 1 = {df} bậc tự do, mức "
                     f"(1 - {level})/2 = {tail} mỗi phía.",
                     f"s/sqrt(n) = {dec(s)}/{k} = {dec(se)}; epsilon = {dec(t)} . {dec(se)} = {dec(eps)}.",
                     f"Khoảng tin cậy: ({dec(lo)}; {dec(hi)})."])


# ------------------------------------------------------------------ khoảng tin cậy cho tỷ lệ
# (n, m): samples whose standard error sqrt(f(1 - f)/n) is an exact decimal, with nf, n(1 - f) >= 10
PROPORTION_SAMPLES = ((100, 10), (100, 20), (100, 36), (100, 50), (100, 64), (100, 80), (100, 90), (150, 60),
                      (150, 90), (225, 81), (225, 144), (300, 75), (300, 225), (350, 98), (400, 40), (400, 80),
                      (400, 144), (400, 200), (400, 256), (400, 320), (525, 84), (600, 240), (625, 125),
                      (625, 225), (900, 90), (900, 324), (900, 576))


def _sqrt_fraction(q: Fraction) -> Fraction:
    a, b = math.isqrt(q.numerator), math.isqrt(q.denominator)
    assert a * a == q.numerator and b * b == q.denominator, q
    return Fraction(a, b)


@generator("xs_g8_ty_le")
def ty_le(rng: random.Random) -> Draw:
    n, m = rng.choice(PROPORTION_SAMPLES)
    level = rng.choice(list(Z_LEVELS))
    z = Fraction(Z_LEVELS[level][0])
    f = Fraction(m, n)
    se = _sqrt_fraction(f * (1 - f) / n)
    eps = z * se
    what = rng.choice(["sản phẩm là phế phẩm", "người được hỏi ủng hộ một đề xuất", "hạt giống nảy mầm"])
    return Draw(
        params={"n": n, "m": m, "z": dec(z)},
        prompt_vi=f"Trong một mẫu ngẫu nhiên {n} phần tử có {m} trường hợp {what}. Lập khoảng tin cậy đối xứng độ "
                  f"tin cậy {level} cho tỷ lệ p của tổng thể, dùng xấp xỉ chuẩn với {_z_given(level)} và sai số "
                  f"chuẩn sqrt(f(1 - f)/n), f là tần suất mẫu. Nhập hai đầu mút, đầu nhỏ trước (số thập phân đúng, "
                  f"không làm tròn).",
        answer=f"{dec(f - eps)}, {dec(f + eps)}",
        solution_vi=[f"f = {m}/{n} = {dec(f)}.",
                     f"Sai số chuẩn sqrt(f(1 - f)/n) = sqrt({dec(f)} . {dec(1 - f)}/{n}) = {dec(se)}.",
                     f"epsilon = {dec(z)} . {dec(se)} = {dec(eps)}.",
                     f"Khoảng tin cậy: ({dec(f - eps)}; {dec(f + eps)})."])


# ------------------------------------------------------------------ cỡ mẫu
@generator("xs_g8_co_mau")
def co_mau(rng: random.Random) -> Draw:
    level = rng.choice(list(Z_LEVELS))
    z = Fraction(Z_LEVELS[level][0])
    kind = rng.choice(["trung_binh", "trung_binh", "ty_le"])
    if kind == "trung_binh":
        sigma = Fraction(rng.choice([4, 5, 6, 8, 10, 12, 15, 20, 25]))
        eps = rng.choice([Fraction(1, 2), Fraction(1), Fraction(2), Fraction(5, 2), Fraction(4), Fraction(5)])
        bound = (z * sigma / eps) ** 2
        n = math.ceil(bound)
        params = {"kind": kind, "sigma": dec(sigma), "eps": dec(eps), "z": dec(z)}
        prompt = (f"Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = {dec(sigma)} đã biết. Cần cỡ mẫu n "
                  f"nhỏ nhất để khoảng tin cậy đối xứng độ tin cậy {level} cho kỳ vọng có sai số epsilon = "
                  f"z sigma/sqrt(n) không vượt quá {dec(eps)}, dùng {_z_given(level)}. Tìm n.")
        steps = [f"z sigma/sqrt(n) <= {dec(eps)} tương đương n >= (z sigma/epsilon)^2.",
                 f"(z sigma/epsilon)^2 = ({dec(z)} . {dec(sigma)}/{dec(eps)})^2 = {dec(z * sigma / eps)}^2 = "
                 f"{dec(bound)}.",
                 f"n là số nguyên nhỏ nhất không nhỏ hơn {dec(bound)}: n = {n}."]
    else:
        f = rng.choice([Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), Fraction(2, 5), Fraction(1, 2)])
        eps = rng.choice([Fraction(1, 50), Fraction(1, 25), Fraction(1, 20)])
        bound = z * z * f * (1 - f) / (eps * eps)
        n = math.ceil(bound)
        params = {"kind": kind, "f": dec(f), "eps": dec(eps), "z": dec(z)}
        prompt = (f"Một mẫu thử cho tần suất f = {dec(f)}; coi f(1 - f) = {dec(f * (1 - f))} không đổi khi lấy mẫu "
                  f"chính thức. Cần cỡ mẫu n nhỏ nhất để khoảng tin cậy đối xứng độ tin cậy {level} cho tỷ lệ có sai "
                  f"số epsilon = z sqrt(f(1 - f)/n) không vượt quá {dec(eps)}, dùng {_z_given(level)}. Tìm n.")
        steps = ["z sqrt(f(1 - f)/n) <= epsilon tương đương n >= z^2 f(1 - f)/epsilon^2.",
                 f"z^2 f(1 - f)/epsilon^2 = {dec(z)}^2 . {dec(f * (1 - f))}/{dec(eps)}^2 = {dec(bound)}.",
                 f"n là số nguyên nhỏ nhất không nhỏ hơn {dec(bound)}: n = {n}."]
    params["level"] = level
    return Draw(params=params, prompt_vi=prompt, answer=str(n), solution_vi=steps)


# ------------------------------------------------------------------ luật số lớn (Chebyshev)
@generator("xs_g8_chebyshev")
def chebyshev(rng: random.Random) -> Draw:
    var = Fraction(rng.choice([1, 2, 4, 5, 9, 10, 16, 25]))
    eps = rng.choice([Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(1, 2), Fraction(1)])
    kind = rng.choice(["can", "co_mau"])
    if kind == "can":
        while True:
            n = rng.choice([25, 50, 100, 200, 400, 500, 1000, 2500])
            bound = var / (n * eps * eps)
            if bound < 1:
                break
            var = Fraction(rng.choice([1, 2, 4, 5, 9, 10, 16, 25]))
            eps = rng.choice([Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(1, 2), Fraction(1)])
        params = {"kind": kind, "var": num(var), "eps": dec(eps), "n": n}
        prompt = (f"X_1, ..., X_{n} độc lập, cùng phân phối với kỳ vọng mu và phương sai {num(var)}; X_tb là trung "
                  f"bình của chúng. Dùng bất đẳng thức Chebyshev P(|Y - E(Y)| >= epsilon) <= V(Y)/epsilon^2, tìm cận "
                  f"trên của P(|X_tb - mu| >= {dec(eps)}) (nhập phân số tối giản).")
        answer = num(bound)
        steps = [f"V(X_tb) = sigma^2/n = {num(var)}/{n} = {num(var / n)}.",
                 f"P(|X_tb - mu| >= {dec(eps)}) <= V(X_tb)/epsilon^2 = {paren(var / n)}/{dec(eps)}^2 = {num(bound)}."]
    else:
        delta = rng.choice([Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), Fraction(1, 4)])
        bound = var / (delta * eps * eps)
        n = math.ceil(bound)
        params = {"kind": kind, "var": num(var), "eps": dec(eps), "delta": dec(delta)}
        prompt = (f"X_1, X_2, ... độc lập, cùng phân phối với kỳ vọng mu và phương sai {num(var)}; X_tb là trung bình "
                  f"của n biến đầu. Dùng bất đẳng thức Chebyshev P(|Y - E(Y)| >= epsilon) <= V(Y)/epsilon^2, tìm số n "
                  f"nhỏ nhất để cận trên Chebyshev của P(|X_tb - mu| >= {dec(eps)}) không vượt quá {dec(delta)}.")
        answer = str(n)
        steps = [f"Cận Chebyshev: V(X_tb)/epsilon^2 = {num(var)}/(n . {dec(eps)}^2).",
                 f"{num(var)}/(n . {dec(eps * eps)}) <= {dec(delta)} tương đương n >= {num(var)}/({dec(delta)} . "
                 f"{dec(eps * eps)}) = {dec(bound) if (bound * 10 ** 6).denominator == 1 else num(bound)}.",
                 f"n nhỏ nhất là {n}."]
    return Draw(params=params, prompt_vi=prompt, answer=answer, solution_vi=steps)


# ------------------------------------------------------------------ định lý giới hạn trung tâm
CLT_SETTINGS = (
    ("Khối lượng mỗi bao gạo (kg)", "tổng khối lượng của {n} bao"),
    ("Số linh thạch một đệ tử nộp mỗi tháng", "tổng số linh thạch {n} đệ tử nộp"),
    ("Thời gian phục vụ một khách (phút)", "tổng thời gian phục vụ {n} khách"),
)


@generator("xs_g8_tong_clt")
def tong_clt(rng: random.Random) -> Draw:
    k = rng.choice([5, 6, 7, 8, 10, 12])
    n = k * k
    sd = rng.choice([1, 2, 3, 4, 5])
    m = rng.choice([2, 3, 5, 10, 20, 50])
    what, total = rng.choice(CLT_SETTINGS)
    mean_s, sd_s = n * m, sd * k
    kind = rng.choice(["giua", "lon_hon", "nho_hon"])
    if kind == "giua":
        z1, z2 = -rng.choice(Z_STEPS), rng.choice(Z_STEPS)
        lo, hi = mean_s + z1 * sd_s, mean_s + z2 * sd_s
        ans = phi(z2) - phi(z1)
        used = sorted({z_text(-z1), z_text(z2)}, key=float)
        event = f"{dec(lo)} < S < {dec(hi)}"
        steps = [f"Chuẩn hóa: ({dec(lo)} - {mean_s})/{sd_s} = {z_text(z1)}, ({dec(hi)} - {mean_s})/{sd_s} = "
                 f"{z_text(z2)}.",
                 f"P xấp xỉ Phi({z_text(z2)}) - Phi({z_text(z1)}) = {phi(z2)} + {-phi(z1)} = {ans}."]
    else:
        z = rng.choice(Z_STEPS) * rng.choice([1, -1])
        c = mean_s + z * sd_s
        used = [z_text(abs(z))]
        if kind == "lon_hon":
            ans, event = Fraction(1, 2) - Fraction(phi(z)), f"S > {dec(c)}"
            steps = [f"Chuẩn hóa: ({dec(c)} - {mean_s})/{sd_s} = {z_text(z)}.",
                     f"P xấp xỉ 0.5 - Phi({z_text(z)}) = 0.5 - ({phi(z)}) = {dec(ans)}."]
        else:
            ans, event = Fraction(1, 2) + Fraction(phi(z)), f"S < {dec(c)}"
            steps = [f"Chuẩn hóa: ({dec(c)} - {mean_s})/{sd_s} = {z_text(z)}.",
                     f"P xấp xỉ 0.5 + Phi({z_text(z)}) = 0.5 + ({phi(z)}) = {dec(ans)}."]
    table = ", ".join(f"Phi({u}) = {LAPLACE[u]}" for u in used)
    return Draw(
        params={"n": n, "m": m, "sd": sd, "event": event},
        prompt_vi=f"{what} là một biến ngẫu nhiên có kỳ vọng {m} và độ lệch chuẩn {sd} (không nhất thiết có phân "
                  f"phối chuẩn), và giá trị này ở các cá thể khác nhau độc lập với nhau. Gọi S là {total.format(n=n)}. Dùng định lý giới "
                  f"hạn trung tâm (xấp xỉ S bằng phân phối chuẩn) và hàm Laplace Phi (tích phân của mật độ N(0, 1) từ "
                  f"0 đến x) với {table}, tính xấp xỉ P({event}) (đáp số là số thập phân đúng, không làm tròn thêm).",
        answer=dec(ans),
        solution_vi=[f"E(S) = n . {m} = {mean_s}; V(S) = n . {sd}^2 = {n * sd * sd}, độ lệch chuẩn của S = "
                     f"{sd} . sqrt({n}) = {sd_s}.", *steps])
