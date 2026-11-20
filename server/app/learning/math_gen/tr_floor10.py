"""Tối Ưu và Toán Rời Rạc, tầng 10 (phương pháp tính: sai số, chia đôi, lặp đơn, Newton): generators.

Everything is exact: a decimal such as 0.05 is held as a Fraction, an iteration is run with Fractions (so x_k is an exact
fraction, never a rounded float), and a step count is the smallest whole n that satisfies an inequality checked with
exact arithmetic. The rules a prompt relies on are stated in it (first-order error rules, the trustworthy-digit rule
Delta <= 0.5 . 10^s, the error (b - a)/2^(n+1) of the midpoint after n bisections).
tools/math_verify_tr_t10.py recomputes each answer another way: the error from the differential sum |df/dv| Delta_v with
sympy, a trustworthy digit by comparing sympy Rationals, the number of bisections from a sympy logarithm, the bisection
and the iterations by running them again over sympy Rationals, the contraction constant as sympy's maximum of g', the
verdict on convergence from |g'(x*)| and Newton's step from x - f/f' with sympy's derivative."""
from __future__ import annotations

import random
from decimal import Decimal
from fractions import Fraction

from . import Draw, generator, num, paren


def _dec(x) -> str:
    """An exact finite decimal: 12.5, 0.05, 4."""
    f = Fraction(x)
    d = Decimal(f.numerator) / Decimal(f.denominator)
    if Fraction(d) != f:
        raise ValueError(f"{f} is not a finite decimal")
    text = format(d.normalize(), "f")
    return "0" if text in ("-0", "") else text


# ------------------------------------------------------------------ sai số của một phép tính
@generator("tr_g10_sai_so_phep_tinh")
def sai_so_phep_tinh(rng: random.Random) -> Draw:
    op = rng.choice(["tong", "hieu", "tich", "thuong"])
    x = Fraction(rng.randint(8, 400), 10)
    y = Fraction(rng.randint(8, 400), 10)
    dx = Fraction(rng.randint(1, 12), 100)
    dy = Fraction(rng.randint(1, 12), 100)
    if op == "tich":
        ans, rule = abs(y) * dx + abs(x) * dy, "Delta_A = |y| Delta_x + |x| Delta_y"
        what, sym = "tích A = x y", "A"
        sol = [f"Delta_A = {_dec(y)} . {_dec(dx)} + {_dec(x)} . {_dec(dy)} = {_dec(y * dx)} + {_dec(x * dy)} = {_dec(ans)}."]
    elif op == "thuong":
        ans, rule = dx / abs(y) + abs(x) * dy / (y * y), "Delta_Q = Delta_x/|y| + |x| Delta_y/y^2"
        what, sym = "thương Q = x/y", "Q"
        sol = [f"Delta_Q = {_dec(dx)}/{_dec(y)} + {_dec(x)} . {_dec(dy)}/({_dec(y)})^2 = {num(dx / abs(y))} + {num(abs(x) * dy / (y * y))} = {num(ans)}."]
    else:
        ans = dx + dy
        rule = "Delta = Delta_x + Delta_y (sai số cộng, cả khi trừ)"
        what, sym = ("tổng x + y", "S") if op == "tong" else ("hiệu x - y", "D")
        sol = [f"Delta_{sym} = Delta_x + Delta_y = {_dec(dx)} + {_dec(dy)} = {_dec(ans)}."]
    prompt = (f"Hai số đo gần đúng x = {_dec(x)} với sai số tuyệt đối Delta_x = {_dec(dx)} và y = {_dec(y)} với sai số tuyệt đối "
              f"Delta_y = {_dec(dy)}. Dùng công thức {rule}, tính sai số tuyệt đối của {what}. Nhập một số hoặc phân số tối giản.")
    return Draw(params={"op": op, "x": _dec(x), "y": _dec(y), "dx": _dec(dx), "dy": _dec(dy)}, prompt_vi=prompt,
                answer=num(ans), solution_vi=sol)


# ------------------------------------------------------------------ sai số của một hàm
@generator("tr_g10_sai_so_ham")
def sai_so_ham(rng: random.Random) -> Draw:
    kind = rng.choice(["binh_phuong", "lap_phuong", "can", "nghich_dao"])
    dx = Fraction(rng.randint(1, 15), 100)
    if kind == "binh_phuong":
        x0 = rng.randint(2, 15)
        text, dfun, dtext = "f(x) = x^2", Fraction(2 * x0), f"f'(x) = 2x nên f'({x0}) = {2 * x0}"
    elif kind == "lap_phuong":
        x0 = rng.randint(2, 9)
        text, dfun, dtext = "f(x) = x^3", Fraction(3 * x0 * x0), f"f'(x) = 3x^2 nên f'({x0}) = {3 * x0 * x0}"
    elif kind == "can":
        r = rng.randint(2, 12)
        x0 = r * r
        text, dfun, dtext = "f(x) = sqrt(x)", Fraction(1, 2 * r), f"f'(x) = 1/(2 sqrt(x)) nên f'({x0}) = 1/{2 * r}"
    else:
        x0 = rng.randint(2, 10)
        text, dfun, dtext = "f(x) = 1/x", Fraction(-1, x0 * x0), f"f'(x) = -1/x^2 nên f'({x0}) = -1/{x0 * x0}"
    ans = abs(dfun) * dx
    return Draw(params={"kind": kind, "x0": x0, "dx": _dec(dx)},
                prompt_vi=f"Đo được x = {x0} với sai số tuyệt đối Delta_x = {_dec(dx)}. Dùng Delta_f = |f'(x)| Delta_x, tính sai số tuyệt đối của "
                          f"{text} tại x = {x0}. Nhập một số hoặc phân số tối giản.",
                answer=num(ans),
                solution_vi=[f"{dtext}.", f"Delta_f = {num(abs(dfun))} . {_dec(dx)} = {num(ans)}."])


# ------------------------------------------------------------------ chữ số đáng tin
@generator("tr_g10_chu_so_dang_tin")
def chu_so_dang_tin(rng: random.Random) -> Draw:
    while True:
        decimals = rng.randint(2, 4)
        whole = rng.randint(1, 99)
        frac = rng.randint(1, 10 ** decimals - 1)
        a = Fraction(whole * 10 ** decimals + frac, 10 ** decimals)
        delta = Fraction(rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]), 10 ** rng.randint(1, decimals + 1))
        digits = list(range(-decimals, len(str(whole))))                       # the weights s of the digits of a
        good = [s for s in digits if delta <= Fraction(1, 2) * Fraction(10) ** s]
        if 0 < len(good) < len(digits) and len(good) == len([s for s in digits if s >= min(good)]):
            break
    shown = f"{whole}.{str(frac).zfill(decimals)}"
    return Draw(params={"a": shown, "delta": _dec(delta)},
                prompt_vi=f"Số gần đúng a = {shown} có sai số tuyệt đối Delta_a = {_dec(delta)}. Một chữ số hàng 10^s là đáng tin khi "
                          f"Delta_a <= 0.5 . 10^s. Số a có bao nhiêu chữ số đáng tin (tính từ chữ số đầu bên trái)? Nhập một số nguyên.",
                answer=str(len(good)),
                solution_vi=[f"Chữ số hàng 10^s đáng tin khi 0.5 . 10^s >= {_dec(delta)}, tức s >= {min(good)} (hàng 10^{min(good)} cho ngưỡng "
                             f"{_dec(Fraction(1, 2) * Fraction(10) ** min(good))}).",
                             f"Các hàng của {shown} từ {max(digits)} xuống {min(digits)} có {len(digits)} chữ số, trong đó các hàng từ {max(digits)} đến {min(good)} đáng tin: "
                             f"{len(good)} chữ số. Các chữ số bên phải nằm trong vùng bất định của sai số."])


# ------------------------------------------------------------------ chia đôi
@generator("tr_g10_chia_doi_so_buoc")
def chia_doi_so_buoc(rng: random.Random) -> Draw:
    length = rng.choice([1, 2, 3, 4, 5, 6, 8, 10])
    eps = rng.choice([Fraction(1, 10), Fraction(1, 20), Fraction(1, 100), Fraction(1, 200), Fraction(1, 1000), Fraction(1, 10000)])
    n = 0
    while Fraction(length, 2 ** (n + 1)) > eps:
        n += 1
    return Draw(params={"length": length, "eps": _dec(eps)},
                prompt_vi=f"Phương trình f(x) = 0 có nghiệm trong một đoạn dài {length}. Sau n lần chia đôi, đoạn nghiệm dài {length}/2^n, và lấy trung điểm "
                          f"của nó làm nghiệm gần đúng thì sai số không quá {length}/2^(n+1). Cần ít nhất bao nhiêu lần chia đôi để sai số không quá "
                          f"{_dec(eps)}? Nhập một số nguyên.",
                answer=str(n),
                solution_vi=[f"Cần {length}/2^(n+1) <= {_dec(eps)}, tức 2^(n+1) >= {num(length / eps)}.",
                             f"2^{n} = {2 ** n} và 2^{n + 1} = {2 ** (n + 1)}: n + 1 = {n + 1} là số mũ nhỏ nhất đủ lớn, nên n = {n} "
                             f"(với n = {n}: {length}/{2 ** (n + 1)} = {num(Fraction(length, 2 ** (n + 1)))} <= {_dec(eps)}"
                             + (f"; với n = {n - 1}: {length}/{2 ** n} = {num(Fraction(length, 2 ** n))} > {_dec(eps)})." if n else ").")])


@generator("tr_g10_chia_doi_dau_doan")
def chia_doi_dau_doan(rng: random.Random) -> Draw:
    while True:
        c = rng.randint(2, 30)
        m = next(k for k in range(1, 7) if (k + 1) ** 2 > c)
        if m * m == c:
            continue
        steps = rng.choice([2, 3])
        a, b = Fraction(m), Fraction(m + 1)
        f = lambda t: t * t - c                      # noqa: E731
        ok = True
        for _ in range(steps):
            mid = (a + b) / 2
            if f(mid) == 0:
                ok = False
                break
            if f(a) * f(mid) < 0:
                b = mid
            else:
                a = mid
        if ok:
            break
    side = rng.choice(["trái", "phải"])
    ans = a if side == "trái" else b
    mids = []
    aa, bb = Fraction(m), Fraction(m + 1)
    for _ in range(steps):
        mid = (aa + bb) / 2
        mids.append((mid, f(mid)))
        if f(aa) * f(mid) < 0:
            bb = mid
        else:
            aa = mid
    sol = [f"f(x) = x^2 - {c} có f({m}) = {m * m - c} < 0 và f({m + 1}) = {(m + 1) ** 2 - c} > 0, nên nghiệm sqrt({c}) nằm trong [{m}, {m + 1}]."]
    lo, hi = Fraction(m), Fraction(m + 1)
    for k, (mid, fm) in enumerate(mids, 1):
        sol.append(f"Lần {k}: c = {num(mid)}, f(c) = {num(fm)} {'< 0' if fm < 0 else '> 0'}; nghiệm nằm trong "
                   + (f"[{num(mid)}, {num(hi)}]" if fm < 0 else f"[{num(lo)}, {num(mid)}]") + ".")
        lo, hi = (mid, hi) if fm < 0 else (lo, mid)
    return Draw(params={"c": c, "m": m, "steps": steps, "side": side},
                prompt_vi=f"Chia đôi f(x) = x^2 - {c} trên [{m}, {m + 1}] (f đổi dấu): mỗi bước tính f ở trung điểm và giữ nửa đoạn mà f đổi dấu. "
                          f"Sau {steps} lần chia đôi, đầu {side} của đoạn nghiệm là bao nhiêu? Nhập một số hoặc phân số tối giản.",
                answer=num(ans), solution_vi=sol + [f"Sau {steps} lần: [{num(lo)}, {num(hi)}], đầu {side} là {num(ans)}."])


# ------------------------------------------------------------------ lặp đơn
@generator("tr_g10_lap_don_buoc")
def lap_don_buoc(rng: random.Random) -> Draw:
    a = rng.randint(1, 3)
    b = rng.randint(1, 4)
    x0 = Fraction(rng.randint(1, 4))
    k = rng.randint(2, 4)
    xs = [x0]
    for _ in range(k):
        xs.append(a + b / xs[-1])
    return Draw(params={"a": a, "b": b, "x0": num(x0), "k": k},
                prompt_vi=f"Phép lặp x_(n+1) = {a} + {b}/x_n bắt đầu từ x_0 = {num(x0)}. Tính x_{k}. Nhập một số hoặc phân số tối giản.",
                answer=num(xs[-1]),
                solution_vi=[f"x_{i + 1} = {a} + {b}/{paren(xs[i])} = {num(xs[i + 1])}." for i in range(k)])


@generator("tr_g10_lap_don_he_so_co")
def lap_don_he_so_co(rng: random.Random) -> Draw:
    kind = rng.choice(["binh_phuong", "lap_phuong"])
    t = rng.randint(1, 3)
    if kind == "binh_phuong":
        m = rng.randint(2 * t + 1, 4 * t + 3)
        c = rng.randint(1, 5)
        text, dtext, q = f"g(x) = (x^2 + {c})/{m}", f"g'(x) = 2x/{m}", Fraction(2 * t, m)
        params = {"kind": kind, "c": c, "m": m, "t": t}
    else:
        m = rng.randint(3 * t * t + 1, 3 * t * t + 8)
        c = rng.randint(1, 5)
        text, dtext, q = f"g(x) = x^3/{m} + {c}", f"g'(x) = 3x^2/{m}", Fraction(3 * t * t, m)
        params = {"kind": kind, "c": c, "m": m, "t": t}
    return Draw(params=params,
                prompt_vi=f"Cho {text} trên đoạn [0, {t}]. Tìm hệ số co q = lớn nhất của |g'(x)| trên [0, {t}]. Nhập một số hoặc phân số tối giản.",
                answer=num(q),
                solution_vi=[f"{dtext} không âm và tăng trên [0, {t}], nên |g'| lớn nhất ở đầu phải x = {t}.",
                             f"q = g'({t}) = {num(q)} < 1: nếu thêm g ánh xạ [0, {t}] vào chính nó thì phép lặp hội tụ."])


@generator("tr_g10_lap_don_hoi_tu_tf")
def lap_don_hoi_tu_tf(rng: random.Random) -> Draw:
    r1, r2 = rng.sample(range(1, 8), 2)
    m, c = r1 + r2, r1 * r2
    r = rng.choice([r1, r2])
    deriv = Fraction(2 * r, m)
    truth = deriv < 1
    return Draw(params={"r1": r1, "r2": r2, "r": r},
                prompt_vi=f"Phương trình x^2 - {m}x + {c} = 0 có hai nghiệm {min(r1, r2)} và {max(r1, r2)}, viết thành x = g(x) với g(x) = (x^2 + {c})/{m}. "
                          f"Phép lặp x_(n+1) = g(x_n) hội tụ về nghiệm x* = {r} khi x_0 đủ gần {r}.",
                answer=truth,
                solution_vi=[f"g'(x) = 2x/{m} nên g'({r}) = {2 * r}/{m} = {num(deriv)}.",
                             (f"|g'({r})| = {num(deriv)} < 1: {r} là điểm hút, mệnh đề đúng." if truth else
                              f"|g'({r})| = {num(deriv)} >= 1: {r} là điểm đẩy (nghiệm lớn hơn của hai nghiệm), phép lặp rời xa nó, mệnh đề sai. "
                              f"Nghiệm nhỏ hơn {min(r1, r2)} có |g'| = {num(Fraction(2 * min(r1, r2), m))} < 1 nên là điểm hút.")])


# ------------------------------------------------------------------ Newton
@generator("tr_g10_newton_buoc")
def newton_buoc(rng: random.Random) -> Draw:
    a = rng.choice([v for v in range(2, 41) if int(v ** 0.5) ** 2 != v])
    x0 = Fraction(rng.randint(1, 7))
    k = rng.choice([1, 2])
    xs = [x0]
    for _ in range(k):
        xs.append(xs[-1] - (xs[-1] ** 2 - a) / (2 * xs[-1]))
    sol = [f"f(x) = x^2 - {a}, f'(x) = 2x, nên x_(n+1) = x_n - (x_n^2 - {a})/(2 x_n) = (x_n + {a}/x_n)/2."]
    for i in range(k):
        sol.append(f"x_{i + 1} = ({paren(xs[i])} + {a}/{paren(xs[i])})/2 = {num(xs[i + 1])}.")
    return Draw(params={"a": a, "x0": num(x0), "k": k},
                prompt_vi=f"Dùng phương pháp Newton x_(n+1) = x_n - f(x_n)/f'(x_n) cho f(x) = x^2 - {a} (để tìm sqrt({a})) với x_0 = {num(x0)}. "
                          f"Tính x_{k}. Nhập một số hoặc phân số tối giản.",
                answer=num(xs[-1]), solution_vi=sol)


@generator("tr_g10_newton_da_thuc")
def newton_da_thuc(rng: random.Random) -> Draw:
    while True:
        b, c, d = rng.randint(-3, 3), rng.randint(-6, 6), rng.randint(-9, 9)
        x0 = rng.randint(-3, 4)
        fp = 3 * x0 * x0 + 2 * b * x0 + c
        if fp != 0:
            break
    f = x0 ** 3 + b * x0 ** 2 + c * x0 + d
    x1 = Fraction(x0) - Fraction(f, fp)
    text = "f(x) = x^3"
    for coef, mono in ((b, "x^2"), (c, "x"), (d, "")):
        if coef:
            mag = abs(coef)
            body = str(mag) if mono == "" else (mono if mag == 1 else f"{mag}{mono}")
            text += f" {'+' if coef > 0 else '-'} {body}"
    dtext = "f'(x) = 3x^2" + (f" {'+' if b > 0 else '-'} {abs(2 * b)}x" if b else "") + (f" {'+' if c > 0 else '-'} {abs(c)}" if c else "")
    return Draw(params={"b": b, "c": c, "d": d, "x0": x0},
                prompt_vi=f"Dùng một bước Newton x_1 = x_0 - f(x_0)/f'(x_0) cho {text} với x_0 = {x0}. Tính x_1. Nhập một số hoặc phân số tối giản.",
                answer=num(x1),
                solution_vi=[f"{dtext}; f({x0}) = {f} và f'({x0}) = {fp}.",
                             f"x_1 = {x0} - {paren(Fraction(f))}/{paren(Fraction(fp))} = {num(x1)}."])
