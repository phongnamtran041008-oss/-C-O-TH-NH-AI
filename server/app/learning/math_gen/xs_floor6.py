"""Xác Suất và Thống Kê, tầng 6 (kỳ vọng, phương sai, nhị thức, Poisson, đều, mũ, chuẩn): generators.

The answers come from the formulas of the floor (sum of x p, E(X^2) - E(X)^2, np, np(1 - p),
lambda/k, (b - a)^2/12, standardising with the Laplace function); tools/math_verify_xs_t4.py
recomputes them with sympy.stats (FiniteRV, Binomial, Poisson, Uniform, E, variance, P). For
the normal law the prompt gives the table value it needs, so the answer is an exact decimal
(the sum of table values), never a rounded one."""
from __future__ import annotations

import math
import random
from decimal import Decimal
from fractions import Fraction

from . import Draw, generator, linear_text, num, paren

DENOMS = (4, 5, 8, 10)


def _table(rng: random.Random) -> tuple[list[int], list[Fraction]]:
    size = rng.randint(3, 4)
    d = rng.choice(DENOMS)
    while d < size:
        d = rng.choice(DENOMS)
    cuts = sorted(rng.sample(range(1, d), size - 1))
    parts = [b - a for a, b in zip([0, *cuts], [*cuts, d])]
    values = sorted(rng.sample(range(-2, 6), size))
    return values, [Fraction(p, d) for p in parts]


def _table_text(values, probs) -> str:
    return (f"X nhận các giá trị {', '.join(map(str, values))} với xác suất lần lượt "
            f"{', '.join(num(p) for p in probs)}")


def _mean(values, probs) -> Fraction:
    return sum((v * p for v, p in zip(values, probs)), Fraction(0))


def _var(values, probs) -> Fraction:
    m = _mean(values, probs)
    return sum((v * v * p for v, p in zip(values, probs)), Fraction(0)) - m * m


# ------------------------------------------------------------------ kỳ vọng
@generator("xs_g6_ky_vong")
def ky_vong(rng: random.Random) -> Draw:
    values, probs = _table(rng)
    m = _mean(values, probs)
    return Draw(
        params={"values": values, "probs": [num(p) for p in probs]},
        prompt_vi=f"Biến ngẫu nhiên rời rạc {_table_text(values, probs)}. Tính kỳ vọng E(X).",
        answer=num(m),
        solution_vi=["E(X) = tổng của x_i p_i theo mọi giá trị.",
                     f"E(X) = {' + '.join(f'{paren(v)} . {paren(p)}' for v, p in zip(values, probs))} = {num(m)}."])


# ------------------------------------------------------------------ phương sai
@generator("xs_g6_phuong_sai")
def phuong_sai(rng: random.Random) -> Draw:
    values, probs = _table(rng)
    m = _mean(values, probs)
    m2 = sum((v * v * p for v, p in zip(values, probs)), Fraction(0))
    return Draw(
        params={"values": values, "probs": [num(p) for p in probs]},
        prompt_vi=f"Biến ngẫu nhiên rời rạc {_table_text(values, probs)}. Tính phương sai V(X).",
        answer=num(m2 - m * m),
        solution_vi=[f"E(X) = {num(m)}.",
                     f"E(X^2) = {' + '.join(f'{v * v} . {paren(p)}' for v, p in zip(values, probs))} = {num(m2)}.",
                     f"V(X) = E(X^2) - (E(X))^2 = {num(m2)} - {paren(m)}^2 = {num(m2 - m * m)}."])


@generator("xs_g6_bien_doi")
def bien_doi(rng: random.Random) -> Draw:
    values, probs = _table(rng)
    a = rng.choice([-3, -2, -1, 2, 3, 4])
    b = rng.randint(-5, 5)
    ask = rng.choice(["E", "V"])
    m, v = _mean(values, probs), _var(values, probs)
    y = linear_text(a, b, "X")
    if ask == "E":
        ans = a * m + b
        steps = [f"E(X) = {num(m)}.", f"E({y}) = {a} E(X) {'+' if b >= 0 else '-'} {abs(b)} = {num(ans)}."]
    else:
        ans = a * a * v
        steps = [f"E(X) = {num(m)}, V(X) = E(X^2) - (E(X))^2 = {num(v)}.",
                 f"Hằng số cộng thêm không làm đổi phương sai, còn hệ số nhân ra ngoài thì bình phương lên: "
                 f"V({y}) = {a}^2 V(X) = {a * a} . {paren(v)} = {num(ans)}." if a > 0 else
                 f"Hằng số cộng thêm không làm đổi phương sai, còn hệ số nhân ra ngoài thì bình phương lên: "
                 f"V({y}) = ({a})^2 V(X) = {a * a} . {paren(v)} = {num(ans)}."]
    return Draw(
        params={"values": values, "probs": [num(p) for p in probs], "a": a, "b": b, "ask": ask},
        prompt_vi=f"Biến ngẫu nhiên rời rạc {_table_text(values, probs)}. Đặt Y = {y}. Tính {ask}(Y).",
        answer=num(ans), solution_vi=steps)


# ------------------------------------------------------------------ nhị thức và Poisson
BIN_P = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(1, 10), Fraction(2, 5),
         Fraction(3, 4))


@generator("xs_g6_nhi_thuc")
def nhi_thuc(rng: random.Random) -> Draw:
    n = rng.randint(4, 30)
    p = rng.choice(BIN_P)
    ask = rng.choice(["E", "V", "P"])
    if ask == "E":
        ans, what = n * p, "kỳ vọng E(X)"
        steps = [f"E(X) = np = {n} . {paren(p)} = {num(ans)}."]
    elif ask == "V":
        ans, what = n * p * (1 - p), "phương sai V(X)"
        steps = [f"V(X) = np(1 - p) = {n} . {paren(p)} . {paren(1 - p)} = {num(ans)}."]
    else:
        n = min(n, 6)
        k = rng.randint(0, n)
        ans, what = math.comb(n, k) * p ** k * (1 - p) ** (n - k), f"xác suất P(X = {k})"
        steps = [f"P(X = {k}) = C({n}, {k}) p^{k} (1 - p)^{n - k} = {math.comb(n, k)} . {paren(p)}^{k} . "
                 f"{paren(1 - p)}^{n - k} = {num(ans)}."]
    return Draw(
        params={"n": n, "p": num(p), "ask": ask, "k": (k if ask == "P" else None)},
        prompt_vi=f"Biến ngẫu nhiên X có phân phối nhị thức B({n}, {num(p)}): số lần thành công trong {n} phép "
                  f"thử độc lập, mỗi lần thành công với xác suất {num(p)}. Tính {what}.",
        answer=num(ans),
        solution_vi=[f"X ~ B(n, p) với n = {n}, p = {num(p)}.", *steps])


@generator("xs_g6_poisson_ti_so")
def poisson_ti_so(rng: random.Random) -> Draw:
    lam = rng.choice([Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3), Fraction(4),
                      Fraction(5), Fraction(6)])
    k = rng.randint(1, 5)
    ans = lam / k
    return Draw(
        params={"lam": num(lam), "k": k},
        prompt_vi=f"Số khách X đến một quầy trong một phút có phân phối Poisson với tham số lambda = {num(lam)}, "
                  f"tức P(X = j) = e^(-lambda) lambda^j / j! với j = 0, 1, 2, ... Tính tỉ số "
                  f"P(X = {k}) / P(X = {k - 1}).",
        answer=num(ans),
        solution_vi=[f"P(X = {k}) / P(X = {k - 1}) = [e^(-lambda) lambda^{k}/{k}!] / [e^(-lambda) lambda^{k - 1}/"
                     f"{k - 1}!].",
                     f"e^(-lambda) giản ước, còn lại lambda/{k} = {paren(lam)}/{k} = {num(ans)}."])


# ------------------------------------------------------------------ phân phối đều
@generator("xs_g6_deu")
def deu(rng: random.Random) -> Draw:
    a = rng.randint(-4, 6)
    b = a + rng.randint(2, 10)
    ask = rng.choice(["E", "V", "P"])
    if ask == "E":
        ans, what = Fraction(a + b, 2), "E(X)"
        steps = [f"E(X) = (a + b)/2 = ({a} + {b})/2 = {num(ans)}."]
    elif ask == "V":
        ans, what = Fraction((b - a) ** 2, 12), "V(X)"
        steps = [f"V(X) = (b - a)^2/12 = {b - a}^2/12 = {num(ans)}."]
    else:
        c, d = sorted(rng.sample(range(a, b + 1), 2))
        ans, what = Fraction(d - c, b - a), f"P({c} < X < {d})"
        steps = [f"Mật độ bằng 1/{b - a} trên [{a}, {b}], nên xác suất tỉ lệ với độ dài khoảng.",
                 f"P({c} < X < {d}) = ({d} - {paren(c)})/{b - a} = {num(ans)}."]
    return Draw(
        params={"a": a, "b": b, "ask": ask, "cd": ([c, d] if ask == "P" else None)},
        prompt_vi=f"Biến ngẫu nhiên X có phân phối đều trên đoạn [{a}, {b}]. Tính {what}.",
        answer=num(ans),
        solution_vi=[f"X đều trên [{a}, {b}]: mật độ f(x) = 1/{b - a} trên đoạn đó, bằng 0 ngoài đoạn.", *steps])


# ------------------------------------------------------------------ phân phối chuẩn
# The Laplace function Phi(x): the integral of the N(0, 1) density from 0 to x, to 4 decimals.
LAPLACE = {"0.5": "0.1915", "1": "0.3413", "1.5": "0.4332", "2": "0.4772", "2.5": "0.4938"}
Z_STEPS = (Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(5, 2))


def _z_text(z: Fraction) -> str:
    return f"{float(z):g}"


def _phi(z: Fraction) -> Decimal:
    """Phi(z) from the table, odd: Phi(-z) = -Phi(z)."""
    v = Decimal(LAPLACE[_z_text(abs(z))])
    return v if z >= 0 else -v


@generator("xs_g6_chuan")
def chuan(rng: random.Random) -> Draw:
    mu = rng.choice([10, 20, 50, 100, 165])
    sigma = rng.choice([2, 4, 5, 10])
    kind = rng.choice(["giua", "giua", "lon_hon", "nho_hon"])
    if kind == "giua":
        z1, z2 = rng.choice(Z_STEPS), rng.choice(Z_STEPS)
        z1 = -z1
        if rng.random() < 0.3:                 # both on the same side
            z1, z2 = sorted([abs(z1), z2])
            if z1 == z2:
                z1 = -z1
        lo, hi = mu + z1 * sigma, mu + z2 * sigma
        ans = _phi(z2) - _phi(z1)
        used = sorted({_z_text(abs(z1)), _z_text(abs(z2))}, key=float)
        event = f"{_z_text(lo)} < X < {_z_text(hi)}"
        steps = [f"Chuẩn hóa: ({_z_text(lo)} - {mu})/{sigma} = {_z_text(z1)} và ({_z_text(hi)} - {mu})/{sigma} "
                 f"= {_z_text(z2)}.",
                 f"P({event}) = Phi({_z_text(z2)}) - Phi({_z_text(z1)}), với Phi(-x) = -Phi(x).",
                 f"= {_phi(z2)} - ({_phi(z1)}) = {ans}."]
    else:
        z = rng.choice(Z_STEPS) * rng.choice([1, -1])
        c = mu + z * sigma
        used = [_z_text(abs(z))]
        if kind == "lon_hon":
            ans = Decimal("0.5") - _phi(z)
            event = f"X > {_z_text(c)}"
            steps = [f"Chuẩn hóa: ({_z_text(c)} - {mu})/{sigma} = {_z_text(z)}.",
                     f"P({event}) = 0.5 - Phi({_z_text(z)}) = 0.5 - ({_phi(z)}) = {ans}."]
        else:
            ans = Decimal("0.5") + _phi(z)
            event = f"X < {_z_text(c)}"
            steps = [f"Chuẩn hóa: ({_z_text(c)} - {mu})/{sigma} = {_z_text(z)}.",
                     f"P({event}) = 0.5 + Phi({_z_text(z)}) = 0.5 + ({_phi(z)}) = {ans}."]
    table = ", ".join(f"Phi({u}) = {LAPLACE[u]}" for u in used)
    return Draw(
        params={"mu": mu, "sigma": sigma, "event": event},
        prompt_vi=f"Biến ngẫu nhiên X có phân phối chuẩn với kỳ vọng {mu} và độ lệch chuẩn {sigma}, tức "
                  f"X ~ N({mu}, {sigma * sigma}). Dùng hàm Laplace Phi (tích phân của mật độ N(0, 1) từ 0 đến x) "
                  f"với {table}. Tính P({event}) (đáp số là số thập phân đúng, không làm tròn thêm).",
        answer=str(ans),
        solution_vi=["Với X ~ N(mu, sigma^2): P(a < X < b) = Phi((b - mu)/sigma) - Phi((a - mu)/sigma).", *steps])
