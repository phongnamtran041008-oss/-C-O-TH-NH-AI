"""Đại Số Tuyến Tính, tầng 9 (giá trị riêng, chéo hóa, không gian Euclide, dạng toàn phương,
phép chiếu): generators. Every question here is tier 5: a whole problem of several steps.

Matrices with known eigenvalues are built as P D P^(-1) with P = L U (unit diagonals, so
det P = 1 and P^(-1) has whole entries); a matrix that cannot be diagonalised is P J P^(-1)
with a Jordan block J, or has a rotation block with no real eigenvalue. The answer comes from
how a question was built (D, the Jordan block, Sylvester's leading minors, a projection along
the normal); tools/math_verify_dstt_t7.py redoes each with sympy by another route (eigenvals,
is_diagonalizable, matrix powers, GramSchmidt, is_positive_definite, orthonormal projections)."""
from __future__ import annotations

import random
from fractions import Fraction
from math import gcd

from . import Draw, generator, nonzero, num, nums, paren, vec_text
from .dstt_floor7 import coef_text
from .dstt_floor8 import flat, mul


def unit_lu(rng: random.Random, n: int, lo: int = -1, hi: int = 1):
    """P = L U with unit diagonals, and its inverse (both whole)."""
    low = [[1 if i == j else (rng.randint(lo, hi) if j < i else 0) for j in range(n)] for i in range(n)]
    up = [[1 if i == j else (rng.randint(lo, hi) if j > i else 0) for j in range(n)] for i in range(n)]
    return mul(low, up), mul(_unit_inv(up, upper=True), _unit_inv(low, upper=False))


def _unit_inv(t, upper: bool):
    """Inverse of a unit triangular matrix by back substitution, column by column."""
    n = len(t)
    out = [[0] * n for _ in range(n)]
    for c in range(n):
        x = [0] * n
        order = range(n - 1, -1, -1) if upper else range(n)
        for i in order:
            s = (1 if i == c else 0) - sum(t[i][k] * x[k] for k in range(n) if k != i)
            x[i] = s                                    # (t[i][i] = 1)
        for i in range(n):
            out[i][c] = x[i]
    return out


def conj(p, d, pinv):
    return mul(mul(p, d), pinv)


def diag(vals):
    return [[v if i == j else 0 for j in range(len(vals))] for i, v in enumerate(vals)]


def is_triangular(a) -> bool:
    n = len(a)
    return all(a[i][j] == 0 for i in range(n) for j in range(i)) or \
        all(a[i][j] == 0 for i in range(n) for j in range(i + 1, n))


def dot(u, v):
    return sum(Fraction(a) * b for a, b in zip(u, v))


# ------------------------------------------------------------------ giá trị riêng
@generator("dstt_g9_tri_rieng")
def tri_rieng(rng: random.Random) -> Draw:
    while True:
        p, pinv = unit_lu(rng, 3)
        vals = rng.sample([-3, -2, -1, 1, 2, 3, 4], 3)
        a = conj(p, diag(vals), pinv)
        if max(abs(v) for v in flat(a)) <= 12 and not is_triangular(a):
            break
    tr = sum(a[i][i] for i in range(3))
    return Draw(
        params={"a": a},
        prompt_vi=("Ma trận A như hình có ba giá trị riêng khác nhau, đều là số nguyên. Tìm chúng. "
                   "Nhập ba giá trị riêng, cách nhau bằng dấu phẩy, theo thứ tự bất kỳ."),
        answer=nums(sorted(vals)), unordered=True, matrices={"A": a},
        solution_vi=["Giá trị riêng là nghiệm của đa thức đặc trưng p(t) = det(A - tI), một đa thức bậc 3.",
                     f"Kiểm tra nhanh: tổng ba giá trị riêng bằng vết tr A = {tr}, tích bằng det A = "
                     f"{vals[0] * vals[1] * vals[2]}.",
                     "Nghiệm nguyên của p(t) là ước của hệ số tự do det A: thử các ước đó, rồi chia đa thức.",
                     f"Ba giá trị riêng: {nums(sorted(vals))}."])


# ------------------------------------------------------------------ chéo hóa
@generator("dstt_g9_cheo_hoa")
def cheo_hoa(rng: random.Random) -> Draw:
    truth = rng.random() < 0.5
    kind = rng.choice(["distinct2", "repeat3"] if truth else ["jordan2", "complex2", "jordan3"])
    n = 3 if kind.endswith("3") else 2
    while True:
        p, pinv = unit_lu(rng, n)
        if kind == "distinct2":
            a0, b0 = rng.sample([-2, -1, 1, 2, 3, 4], 2)
            core = diag([a0, b0])
        elif kind == "repeat3":
            a0, b0 = rng.sample([-2, -1, 1, 2, 3], 2)
            core = diag([a0, a0, b0])
        elif kind == "jordan2":
            a0 = rng.choice([-2, -1, 1, 2, 3])
            core = [[a0, 1], [0, a0]]
        elif kind == "complex2":
            a0, b0 = rng.randint(-2, 2), nonzero(rng, -2, 2)
            core = [[a0, -b0], [b0, a0]]
        else:
            a0, b0 = rng.sample([-2, -1, 1, 2, 3], 2)
            core = [[a0, 1, 0], [0, a0, 0], [0, 0, b0]]
        a = conj(p, core, pinv)
        if max(abs(v) for v in flat(a)) <= 9 and not is_triangular(a):
            break
    tr = sum(a[i][i] for i in range(n))
    if kind == "distinct2":
        steps = [f"p(t) = t^2 - {paren(tr)}t + {paren(a0 * b0)}, có hai nghiệm thực phân biệt {a0} và {b0}.",
                 "Ma trận cấp 2 có hai giá trị riêng thực phân biệt thì có hai vectơ riêng độc lập.",
                 "Vậy A chéo hóa được trên R: mệnh đề đúng."]
    elif kind == "repeat3":
        steps = [f"Giá trị riêng: {a0} (bội 2) và {b0}.",
                 f"A - ({a0})I có hạng 1, nên không gian riêng ứng với {a0} có số chiều 3 - 1 = 2, bằng bội.",
                 "Tổng số chiều các không gian riêng là 2 + 1 = 3: A chéo hóa được trên R, mệnh đề đúng."]
    elif kind == "jordan2":
        steps = [f"p(t) = (t - {paren(a0)})^2: giá trị riêng duy nhất {a0}, bội 2.",
                 f"A - ({a0})I khác ma trận không nên có hạng 1; không gian riêng chỉ có số chiều 1.",
                 "Không đủ hai vectơ riêng độc lập: A không chéo hóa được, mệnh đề sai."]
    elif kind == "complex2":
        steps = [f"p(t) = t^2 - {paren(tr)}t + {paren(a0 * a0 + b0 * b0)}.",
                 f"Biệt thức bằng {tr * tr - 4 * (a0 * a0 + b0 * b0)} < 0: A không có giá trị riêng thực.",
                 "Không có vectơ riêng thực nào, nên A không chéo hóa được trên R: mệnh đề sai."]
    else:
        steps = [f"Giá trị riêng: {a0} (bội 2) và {b0}.",
                 f"A - ({a0})I có hạng 2, nên không gian riêng ứng với {a0} chỉ có số chiều 3 - 2 = 1, nhỏ hơn bội 2.",
                 "Tổng số chiều các không gian riêng là 1 + 1 = 2 < 3: A không chéo hóa được, mệnh đề sai."]
    return Draw(params={"a": a, "kind": kind},
                prompt_vi="Ma trận A như hình chéo hóa được trên R (có P khả nghịch, thực, và D chéo với A = P D P^(-1)).",
                answer=truth, matrices={"A": a}, solution_vi=steps)


@generator("dstt_g9_luy_thua")
def luy_thua(rng: random.Random) -> Draw:
    while True:
        p, pinv = unit_lu(rng, 2, -2, 2)
        vals = rng.sample([-2, -1, 1, 2], 2)
        a = conj(p, diag(vals), pinv)
        if max(abs(v) for v in flat(a)) <= 9 and not is_triangular(a):
            break
    k = rng.randint(3, 6)
    i, j = rng.randint(1, 2), rng.randint(1, 2)
    an = conj(p, diag([v ** k for v in vals]), pinv)
    return Draw(
        params={"a": a, "n": k, "i": i, "j": j},
        prompt_vi=(f"Cho ma trận A như hình. Chéo hóa A rồi tính phần tử ở hàng {i}, cột {j} của A^{k}."),
        answer=str(an[i - 1][j - 1]), matrices={"A": a},
        solution_vi=[f"p(t) = det(A - tI) có hai nghiệm {vals[0]} và {vals[1]}; giải (A - tI)x = 0 cho mỗi giá trị "
                     f"được hai vectơ riêng, đặt làm hai cột của P: P có hàng {vec_text(p[0])}, {vec_text(p[1])}.",
                     f"A = P D P^(-1) với D chéo ({vals[0]}, {vals[1]}), P^(-1) có hàng {vec_text(pinv[0])}, "
                     f"{vec_text(pinv[1])}.",
                     f"A^{k} = P D^{k} P^(-1), với D^{k} chéo ({vals[0] ** k}, {vals[1] ** k}).",
                     f"A^{k} có hàng {vec_text(an[0])} và {vec_text(an[1])}; phần tử cần tìm là {an[i - 1][j - 1]}."])


# ------------------------------------------------------------------ Gram-Schmidt
@generator("dstt_g9_gram_schmidt")
def gram_schmidt(rng: random.Random) -> Draw:
    while True:
        us = [[rng.randint(-1, 2) for _ in range(3)] for _ in range(3)]
        if any(not any(u) for u in us):
            continue
        v1 = [Fraction(t) for t in us[0]]
        c21 = dot(us[1], v1) / dot(v1, v1)
        v2 = [a - c21 * b for a, b in zip(us[1], v1)]
        if not any(v2):
            continue
        c31, c32 = dot(us[2], v1) / dot(v1, v1), dot(us[2], v2) / dot(v2, v2)
        v3 = [a - c31 * b - c32 * c for a, b, c in zip(us[2], v1, v2)]
        if any(v3) and c21 != 0 and (c31 != 0 or c32 != 0) and \
                max(t.denominator for t in v2 + v3) <= 12:
            break
    return Draw(
        params={"u": us},
        prompt_vi=(f"Trực giao hóa Gram-Schmidt (không chuẩn hóa) ba vectơ u1 = {vec_text(us[0])}, "
                   f"u2 = {vec_text(us[1])}, u3 = {vec_text(us[2])} của R^3, với tích vô hướng thông thường: "
                   "v1 = u1, rồi v2, rồi v3. Nhập ba tọa độ của v3 (phân số viết a/b), cách nhau bằng dấu phẩy."),
        answer=nums(v3),
        solution_vi=[f"v1 = u1 = {vec_text(v1)}.",
                     f"v2 = u2 - (u2 . v1 / v1 . v1) v1 = u2 - ({num(c21)}) v1 = {vec_text(v2)}.",
                     f"v3 = u3 - (u3 . v1 / v1 . v1) v1 - (u3 . v2 / v2 . v2) v2, với hai hệ số {num(c31)} và {num(c32)}.",
                     f"v3 = {vec_text(v3)}; thử lại v3 . v1 = 0 và v3 . v2 = 0."])


# ------------------------------------------------------------------ dạng toàn phương
QTERMS = ["x^2", "y^2", "z^2", "xy", "xz", "yz"]


def leading_minors(a) -> list[int]:
    d1 = a[0][0]
    d2 = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    d3 = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
          + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    return [d1, d2, d3]


@generator("dstt_g9_xac_dinh")
def xac_dinh(rng: random.Random) -> Draw:
    truth = rng.random() < 0.5
    while True:
        if truth:
            up = [[1, rng.randint(-1, 1), rng.randint(-1, 1)], [0, 1, rng.randint(-1, 1)], [0, 0, 1]]
            d = [rng.randint(1, 2) for _ in range(3)]
            ut = [[up[j][i] for j in range(3)] for i in range(3)]
            a = mul(mul(ut, diag(d)), up)               # U^T D U with D > 0
        else:
            dg = [rng.randint(-1, 4) for _ in range(3)]
            off = [rng.randint(-3, 3) for _ in range(3)]
            a = [[dg[0], off[0], off[1]], [off[0], dg[1], off[2]], [off[1], off[2], dg[2]]]
        minors = leading_minors(a)
        pd = all(m > 0 for m in minors)
        if pd == truth and max(abs(v) for v in flat(a)) <= 6 and sum(1 for v in (a[0][1], a[0][2], a[1][2]) if v) >= 2:
            break
    coefs = [a[0][0], a[1][1], a[2][2], 2 * a[0][1], 2 * a[0][2], 2 * a[1][2]]
    first_bad = next((k for k, m in enumerate(minors) if m <= 0), None)
    steps = [f"Ma trận đối xứng của q có hàng {vec_text(a[0])}, {vec_text(a[1])}, {vec_text(a[2])} "
             "(hệ số của xy, xz, yz chia đôi).",
             f"Các định thức con chính: D1 = {minors[0]}, D2 = {minors[1]}, D3 = {minors[2]}."]
    if truth:
        steps.append("Cả ba đều dương: theo tiêu chuẩn Sylvester, q xác định dương. Mệnh đề đúng.")
    else:
        steps.append(f"D{first_bad + 1} = {minors[first_bad]} không dương, nên theo tiêu chuẩn Sylvester q không "
                     "xác định dương. Mệnh đề sai.")
    return Draw(params={"a": a},
                prompt_vi=f"Dạng toàn phương q(x, y, z) = {coef_text(coefs, QTERMS)} trên R^3 xác định dương.",
                answer=truth, solution_vi=steps)


# ------------------------------------------------------------------ phép chiếu
def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def _reduced(v):
    g = gcd(gcd(abs(v[0]), abs(v[1])), abs(v[2])) or 1
    return [t // g for t in v]


@generator("dstt_g9_chieu")
def chieu(rng: random.Random) -> Draw:
    units = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    while True:
        nvec = [rng.randint(-2, 2) for _ in range(3)]
        if sum(1 for t in nvec if t) < 2:
            continue
        i, j = rng.sample(range(3), 2)
        a1, a2 = _reduced(cross(nvec, units[i])), _reduced(cross(nvec, units[j]))
        if not any(a1) or not any(a2) or not any(cross(a1, a2)):
            continue
        if rng.random() < 0.5:
            a2 = [x + y for x, y in zip(a1, a2)]             # not an orthogonal pair, on purpose
        b = [rng.randint(-3, 3) for _ in range(3)]
        nvec = _reduced(nvec)
        bn, nn = dot(b, nvec), dot(nvec, nvec)
        if bn == 0 or not any(a2) or max(abs(t) for t in a1 + a2) > 4:
            continue
        p = [x - bn / nn * y for x, y in zip(b, nvec)]
        if any(p):
            break
    return Draw(
        params={"a1": a1, "a2": a2, "b": b},
        prompt_vi=(f"Trong R^3 với tích vô hướng thông thường, cho W = span{{a1, a2}} với a1 = {vec_text(a1)}, "
                   f"a2 = {vec_text(a2)}, và b = {vec_text(b)}. Tìm hình chiếu trực giao p của b lên W. "
                   "Nhập ba tọa độ (phân số viết a/b), cách nhau bằng dấu phẩy."),
        answer=nums(p),
        solution_vi=[f"W là một mặt phẳng qua gốc; một vectơ pháp tuyến của nó là n = {vec_text(nvec)} "
                     "(vuông góc với cả a1 và a2).",
                     f"Phần dư b - p nằm dọc theo n: b - p = (b . n / n . n) n = ({num(bn)}/{num(nn)}) n.",
                     f"p = b - ({num(bn / nn)}) n = {vec_text(p)}; thử lại p . n = 0."])
