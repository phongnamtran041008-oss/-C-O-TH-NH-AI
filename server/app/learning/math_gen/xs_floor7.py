"""Xác Suất và Thống Kê, tầng 7 (tổng thể, mẫu, trung bình và phương sai mẫu, phân phối của trung
bình mẫu, ước lượng không chệch, ước lượng hợp lý cực đại): generators.

The answers come from the formulas of the floor (the short form sum x^2 - n x_tb^2 of the sample
variance, sigma/sqrt(n) for the mean, the closed forms of the maximum likelihood estimators, the
sum of the coefficients of a linear estimator); tools/math_verify_xs_t7.py recomputes them another
way (pairwise differences, sympy.stats, solving d(ln L) = 0 with sympy). Data are built so that
every answer is exact: n is a perfect square where sqrt(n) is needed, and a normal probability is
the exact sum of the Laplace table values the prompt gives."""
from __future__ import annotations

import random
from decimal import Decimal
from fractions import Fraction

from . import Draw, generator, num, paren

# The Laplace function Phi(x): the integral of the N(0, 1) density from 0 to x, to 4 decimals.
LAPLACE = {"0.5": "0.1915", "1": "0.3413", "1.5": "0.4332", "2": "0.4772", "2.5": "0.4938", "3": "0.4987"}
Z_STEPS = (Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2))


def dec(x) -> str:
    """An exact finite decimal: 3.92, -2, 0.0228 (raises if x has no finite decimal form)."""
    f = Fraction(x)
    d = Decimal(f.numerator) / Decimal(f.denominator)
    if Fraction(d) != f:
        raise ValueError(f"{f} is not a finite decimal")
    text = format(d.normalize(), "f")
    return "0" if text in ("-0", "") else text


def z_text(z) -> str:
    return dec(z)


def phi(z: Fraction) -> Decimal:
    """Phi(z) from the table, odd: Phi(-z) = -Phi(z)."""
    v = Decimal(LAPLACE[z_text(abs(z))])
    return v if z >= 0 else -v


def _ratio(a: int, b: int) -> str:
    """a/b and its value, without saying 32/5 = 32/5."""
    q = Fraction(a, b)
    return f"{a}/{b}" if num(q) == f"{a}/{b}" else f"{a}/{b} = {num(q)}"


def data_text(xs) -> str:
    return ", ".join(num(x) for x in xs)


# ------------------------------------------------------------------ trung bình và phương sai mẫu
@generator("xs_g7_phuong_sai_mau")
def phuong_sai_mau(rng: random.Random) -> Draw:
    n = rng.randint(4, 7)
    while True:
        xs = [rng.randint(0, 15) for _ in range(n)]
        if len(set(xs)) > 1:
            break
    total = sum(xs)
    mean = Fraction(total, n)
    squares = sum(x * x for x in xs)
    ss = squares - n * mean * mean
    s2 = ss / (n - 1)
    return Draw(
        params={"data": xs},
        prompt_vi=f"Số viên linh thạch một đệ tử thu được trong {n} ngày là: {data_text(xs)}. Coi đây là một mẫu "
                  f"cỡ n = {n}. Tính trung bình mẫu x_tb và phương sai mẫu hiệu chỉnh "
                  f"s^2 = [tổng của (x_i - x_tb)^2]/(n - 1). Nhập hai số theo thứ tự x_tb, s^2.",
        answer=f"{num(mean)}, {num(s2)}",
        solution_vi=[f"x_tb = ({' + '.join(map(str, xs))})/{n} = {_ratio(total, n)}.",
                     f"Tổng các x_i^2 = {' + '.join(str(x * x) for x in xs)} = {squares}.",
                     f"Tổng của (x_i - x_tb)^2 = tổng x_i^2 - n x_tb^2 = {squares} - {n} . {paren(mean)}^2 = {num(ss)}.",
                     f"s^2 = {paren(ss)}/{n - 1} = {num(s2)} (chia cho n - 1, không chia cho n)."])


@generator("xs_g7_bang_tan_so")
def bang_tan_so(rng: random.Random) -> Draw:
    k = rng.randint(3, 4)
    step = rng.choice([1, 2, 5, 10])
    values = [v * step for v in sorted(rng.sample(range(1, 10), k))]
    counts = [rng.randint(1, 6) for _ in range(k)]
    n = sum(counts)
    total = sum(v * c for v, c in zip(values, counts))
    mean = Fraction(total, n)
    squares = sum(v * v * c for v, c in zip(values, counts))
    ss = squares - n * mean * mean
    s2 = ss / (n - 1)
    table = "; ".join(f"giá trị {v} xuất hiện {c} lần" for v, c in zip(values, counts))
    return Draw(
        params={"values": values, "counts": counts},
        prompt_vi=f"Đo một đại lượng trên một mẫu, được bảng tần số: {table}. Tính trung bình mẫu x_tb và phương "
                  f"sai mẫu hiệu chỉnh s^2 = [tổng của n_i (x_i - x_tb)^2]/(n - 1), với n là cỡ mẫu. "
                  f"Nhập hai số theo thứ tự x_tb, s^2.",
        answer=f"{num(mean)}, {num(s2)}",
        solution_vi=[f"Cỡ mẫu n = {' + '.join(map(str, counts))} = {n}.",
                     f"x_tb = ({' + '.join(f'{v} . {c}' for v, c in zip(values, counts))})/{n} = {_ratio(total, n)}.",
                     f"Tổng n_i x_i^2 = {' + '.join(f'{v * v} . {c}' for v, c in zip(values, counts))} = {squares}.",
                     f"Tổng n_i (x_i - x_tb)^2 = {squares} - {n} . {paren(mean)}^2 = {num(ss)}.",
                     f"s^2 = {paren(ss)}/{n - 1} = {num(s2)}."])


# ------------------------------------------------------------------ phân phối của trung bình mẫu
@generator("xs_g7_trung_binh_mau_chuan")
def trung_binh_mau_chuan(rng: random.Random) -> Draw:
    k = rng.randint(2, 10)
    sd = rng.choice([1, 2, 3, 4, 5])
    sigma, n = sd * k, k * k
    mu = rng.choice([20, 50, 80, 100, 120, 250, 500])
    kind = rng.choice(["giua", "giua", "lon_hon", "nho_hon"])
    if kind == "giua":
        z1, z2 = -rng.choice(Z_STEPS), rng.choice(Z_STEPS)
        lo, hi = mu + z1 * sd, mu + z2 * sd
        ans = phi(z2) - phi(z1)
        used = sorted({z_text(-z1), z_text(z2)}, key=float)
        event = f"{dec(lo)} < X_tb < {dec(hi)}"
        steps = [f"Chuẩn hóa: ({dec(lo)} - {mu})/{sd} = {z_text(z1)} và ({dec(hi)} - {mu})/{sd} = {z_text(z2)}.",
                 f"P({event}) = Phi({z_text(z2)}) - Phi({z_text(z1)}) = {phi(z2)} + {-phi(z1)} = {ans}."]
    else:
        z = rng.choice(Z_STEPS) * rng.choice([1, -1])
        c = mu + z * sd
        used = [z_text(abs(z))]
        if kind == "lon_hon":
            ans, event = Decimal("0.5") - phi(z), f"X_tb > {dec(c)}"
            steps = [f"Chuẩn hóa: ({dec(c)} - {mu})/{sd} = {z_text(z)}.",
                     f"P({event}) = 0.5 - Phi({z_text(z)}) = 0.5 - ({phi(z)}) = {ans}."]
        else:
            ans, event = Decimal("0.5") + phi(z), f"X_tb < {dec(c)}"
            steps = [f"Chuẩn hóa: ({dec(c)} - {mu})/{sd} = {z_text(z)}.",
                     f"P({event}) = 0.5 + Phi({z_text(z)}) = 0.5 + ({phi(z)}) = {ans}."]
    table = ", ".join(f"Phi({u}) = {LAPLACE[u]}" for u in used)
    return Draw(
        params={"mu": mu, "sigma": sigma, "n": n, "event": event},
        prompt_vi=f"Tổng thể có phân phối chuẩn với kỳ vọng mu = {mu} và độ lệch chuẩn sigma = {sigma}. Lấy một mẫu "
                  f"ngẫu nhiên cỡ n = {n} và gọi X_tb là trung bình mẫu. Dùng hàm Laplace Phi (tích phân của mật độ "
                  f"N(0, 1) từ 0 đến x) với {table}. Tính P({event}) (đáp số là số thập phân đúng, không làm tròn thêm).",
        answer=str(ans),
        solution_vi=[f"X_tb có phân phối chuẩn với kỳ vọng {mu} và độ lệch chuẩn sigma/sqrt(n) = {sigma}/{k} = {sd}.",
                     *steps])


# ------------------------------------------------------------------ ước lượng không chệch
COEFFS = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(1, 6), Fraction(2, 3),
          Fraction(3, 4), Fraction(2, 5), Fraction(1, 8), Fraction(3, 8))


def _term(c: Fraction, i: int, first: bool) -> str:
    sign = "-" if c < 0 else "+"
    mag = abs(c)
    body = f"X_{i}" if mag == 1 else (f"{mag.numerator}X_{i}" if mag.denominator == 1 else f"({num(mag)})X_{i}")
    if first:
        return body if c > 0 else f"-{body}"
    return f"{sign} {body}"


@generator("xs_g7_khong_chech_tf")
def khong_chech_tf(rng: random.Random) -> Draw:
    n = rng.randint(3, 4)
    truth = rng.random() < 0.5
    while True:
        cs = [rng.choice(COEFFS) for _ in range(n - 1)]
        last = 1 - sum(cs)
        if not truth:
            last += rng.choice([Fraction(-1, 2), Fraction(-1, 4), Fraction(1, 4), Fraction(1, 2), Fraction(1, 6)])
        if last != 0 and abs(last) <= 2:
            break
    cs.append(last)
    t = " ".join(_term(c, i + 1, i == 0) for i, c in enumerate(cs))
    total = sum(cs)
    verdict = ("Tổng bằng 1 nên E(T) = mu với mọi mu: T không chệch. Mệnh đề đúng." if total == 1 else
               f"Tổng khác 1 nên E(T) = {num(total)} mu khác mu (khi mu khác 0): T bị chệch. Mệnh đề sai.")
    return Draw(
        params={"coeffs": [num(c) for c in cs]},
        prompt_vi=f"X_1, ..., X_{n} là một mẫu ngẫu nhiên (độc lập, cùng phân phối) từ một tổng thể có kỳ vọng mu "
                  f"chưa biết. Thống kê T = {t} là một ước lượng không chệch của mu (tức E(T) = mu với mọi giá trị "
                  f"của mu).",
        answer=total == 1,
        solution_vi=["Kỳ vọng tuyến tính và E(X_i) = mu với mọi i, nên E(T) = (tổng các hệ số) . mu.",
                     f"Tổng các hệ số = {' + '.join(paren(c) for c in cs)} = {num(total)}.",
                     verdict])


# ------------------------------------------------------------------ ước lượng hợp lý cực đại
MODELS = ("bernoulli", "poisson", "mu", "hinh_hoc")


@generator("xs_g7_hop_ly")
def hop_ly(rng: random.Random) -> Draw:
    model = rng.choice(MODELS)
    if model == "bernoulli":
        n = rng.randint(6, 12)
        while True:
            xs = [rng.randint(0, 1) for _ in range(n)]
            if 0 < sum(xs) < n:
                break
        est = Fraction(sum(xs), n)
        law = ("X có phân phối Bernoulli: P(X = 1) = p, P(X = 0) = 1 - p, với 0 < p < 1 chưa biết "
               "(X = 1 là một lần thành công)")
        name = "p"
        steps = [f"ln L(p) = k ln p + (n - k) ln(1 - p), với k = {sum(xs)} lần thành công trong n = {n} lần.",
                 "(ln L)'(p) = k/p - (n - k)/(1 - p) = 0 cho p = k/n.",
                 f"p* = {sum(xs)}/{n} = {num(est)}."]
    elif model == "poisson":
        n = rng.randint(5, 8)
        while True:
            xs = [rng.randint(0, 6) for _ in range(n)]
            if sum(xs) > 0:
                break
        est = Fraction(sum(xs), n)
        law = ("X có phân phối Poisson: P(X = k) = e^(-lambda) lambda^k / k! với k = 0, 1, 2, ..., tham số "
               "lambda > 0 chưa biết")
        name = "lambda"
        steps = ["ln L(lambda) = -n lambda + (tổng x_i) ln lambda - ln(x_1! ... x_n!).",
                 "(ln L)'(lambda) = -n + (tổng x_i)/lambda = 0 cho lambda = x_tb.",
                 f"lambda* = {sum(xs)}/{n} = {num(est)}."]
    elif model == "mu":
        n = rng.randint(3, 6)
        xs = [rng.randint(1, 12) for _ in range(n)]
        est = Fraction(n, sum(xs))
        law = ("thời gian chờ X (phút) có phân phối mũ: mật độ lambda e^(-lambda x) khi x > 0, tham số lambda > 0 "
               "chưa biết")
        name = "lambda"
        steps = ["ln L(lambda) = n ln lambda - lambda (tổng x_i).",
                 "(ln L)'(lambda) = n/lambda - tổng x_i = 0 cho lambda = n/(tổng x_i) = 1/x_tb.",
                 f"lambda* = {n}/{sum(xs)} = {num(est)}."]
    else:
        n = rng.randint(4, 7)
        while True:
            xs = [rng.randint(1, 8) for _ in range(n)]
            if sum(xs) > n:
                break
        est = Fraction(n, sum(xs))
        law = ("X là số lần thử cho đến lần thành công đầu tiên: P(X = k) = p(1 - p)^(k - 1) với k = 1, 2, 3, ..., "
               "0 < p < 1 chưa biết")
        name = "p"
        steps = ["ln L(p) = n ln p + (tổng x_i - n) ln(1 - p).",
                 "(ln L)'(p) = n/p - (tổng x_i - n)/(1 - p) = 0 cho p = n/(tổng x_i) = 1/x_tb.",
                 f"p* = {n}/{sum(xs)} = {num(est)}."]
    return Draw(
        params={"model": model, "data": xs},
        prompt_vi=f"Trong một tổng thể, {law}. Một mẫu ngẫu nhiên cỡ n = {len(xs)} cho các giá trị: {data_text(xs)}. "
                  f"Tìm ước lượng hợp lý cực đại {name}* của {name} (nhập một số hoặc phân số tối giản).",
        answer=num(est),
        solution_vi=[f"Hàm hợp lý L({name}) là tích các xác suất (hay mật độ) tại {len(xs)} giá trị của mẫu; "
                     "lấy logarit để tích thành tổng.", *steps])
