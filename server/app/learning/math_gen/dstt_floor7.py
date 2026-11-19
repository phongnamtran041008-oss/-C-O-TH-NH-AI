"""Đại Số Tuyến Tính, tầng 7 (không gian vectơ, cơ sở, số chiều, tọa độ): generators.

Every answer here comes from how the numbers were built, never from a general solver: a vector
in a span is a known combination, a dependent family has a known relation, a family of rank r
is r echelon rows mixed by a known coefficient matrix, coordinates are the coefficients that
were drawn. tools/math_verify_dstt_t7.py redoes each answer with sympy by another route
(determinants, nullspace, columnspace, LUsolve)."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, nonzero, nums, paren, vec_text


def lin(coefs, vecs) -> list[int]:
    """sum of coefs[k] * vecs[k], coordinate by coordinate."""
    return [sum(c * v[i] for c, v in zip(coefs, vecs)) for i in range(len(vecs[0]))]


def det3(m) -> int:
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def rank_of(rows) -> int:
    """Rank by Gaussian elimination over the rationals (used only to check a draw)."""
    m = [[Fraction(v) for v in r] for r in rows]
    r = 0
    for c in range(len(m[0]) if m else 0):
        pivot = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


def coef_text(coefs, names) -> str:
    """2u - v + 3w, written the usual way (zero terms left out)."""
    out = ""
    for c, n in zip(coefs, names):
        if c == 0:
            continue
        mag = "" if abs(c) == 1 else str(abs(c))
        if not out:
            out = f"{'-' if c < 0 else ''}{mag}{n}"
        else:
            out += f" {'-' if c < 0 else '+'} {mag}{n}"
    return out or "0"


# ------------------------------------------------------------------ tổ hợp tuyến tính
@generator("dstt_g7_to_hop")
def to_hop(rng: random.Random) -> Draw:
    while True:
        u = [rng.randint(-3, 3) for _ in range(3)]
        v = [rng.randint(-3, 3) for _ in range(3)]
        d = u[0] * v[1] - u[1] * v[0]
        if d in (-1, 1, -2, 2) and u[2] != 0 and v[2] != 0:
            break
    a, b = nonzero(rng, -3, 3), nonzero(rng, -3, 3)
    w = lin([a, b], [u, v])
    m = w[2]
    return Draw(
        params={"u": u, "v": v, "w12": w[:2]},
        prompt_vi=(f"Trong R^3 cho u = {vec_text(u)}, v = {vec_text(v)} và w = ({w[0]}, {w[1]}, m). "
                   "Tìm m để w thuộc span{u, v}."),
        answer=str(m),
        solution_vi=[f"w thuộc span{{u, v}} khi có a, b với au + bv = w. Hai tọa độ đầu cho hệ "
                     f"{coef_text([u[0], v[0]], ['a', 'b'])} = {w[0]} và {coef_text([u[1], v[1]], ['a', 'b'])} = {w[1]}.",
                     f"Hệ này có định thức {d} khác 0, nghiệm duy nhất a = {a}, b = {b}.",
                     f"Tọa độ thứ ba phải khớp: m = {paren(a)} . {paren(u[2])} + {paren(b)} . {paren(v[2])} = {m}."])


# ------------------------------------------------------------------ độc lập tuyến tính
@generator("dstt_g7_doc_lap")
def doc_lap(rng: random.Random) -> Draw:
    truth = rng.random() < 0.5
    while True:
        u = [rng.randint(-3, 3) for _ in range(3)]
        v = [rng.randint(-3, 3) for _ in range(3)]
        if rank_of([u, v]) < 2:
            continue
        if truth:
            w = [rng.randint(-4, 4) for _ in range(3)]
            if det3([u, v, w]) != 0:
                break
        else:
            a, b = nonzero(rng, -2, 2), nonzero(rng, -2, 2)
            w = lin([a, b], [u, v])
            if max(abs(t) for t in w) <= 9:
                break
    d = det3([u, v, w])
    steps = ["Ba vectơ của R^3 độc lập tuyến tính khi và chỉ khi ma trận có ba hàng u, v, w có định thức khác 0 "
             "(hệ au + bv + cw = 0 chỉ có nghiệm tầm thường)."]
    if truth:
        steps += [f"Định thức đó bằng {d}, khác 0.", "Vậy họ u, v, w độc lập tuyến tính: mệnh đề đúng."]
    else:
        steps += ["Định thức đó bằng 0.",
                  f"Thật vậy w = {coef_text([a, b], ['u', 'v'])}, nên {coef_text([a, b, -1], ['u', 'v', 'w'])} = 0 "
                  "là một quan hệ không tầm thường: họ phụ thuộc tuyến tính, mệnh đề sai."]
    return Draw(
        params={"u": u, "v": v, "w": w},
        prompt_vi=f"Trong R^3, họ u = {vec_text(u)}, v = {vec_text(v)}, w = {vec_text(w)} độc lập tuyến tính.",
        answer=truth, solution_vi=steps)


# ------------------------------------------------------------------ cơ sở và số chiều
def _echelon(rng: random.Random, r: int, n: int) -> list[list[int]]:
    """r rows of length n in echelon form with pivots 1 at increasing random columns."""
    cols = sorted(rng.sample(range(n), r))
    rows = []
    for k, c in enumerate(cols):
        row = [0] * n
        row[c] = 1
        for j in range(c + 1, n):
            row[j] = rng.randint(-2, 2)
        rows.append(row)
    return rows


@generator("dstt_g7_so_chieu")
def so_chieu(rng: random.Random) -> Draw:
    while True:
        n = rng.choice([3, 4])                      # the vectors live in R^n
        k = rng.choice([3, 4])                      # how many vectors are listed
        r = rng.randint(1, min(n, k) - (1 if k == n else 0))     # a rank below the obvious bound
        e = _echelon(rng, r, n)
        mix = [[rng.randint(-2, 2) for _ in range(r)] for _ in range(k)]
        for i in range(r):                          # r rows of `mix` are an identity block (rank r)
            mix[i] = [1 if j == i else 0 for j in range(r)]
        vecs = [lin(mix[i], e) for i in range(k)]
        for i in range(r):                          # hide the echelon look: add a later basis row to it
            if i + 1 < r:
                vecs[i] = lin([1, rng.randint(-1, 1)], [vecs[i], vecs[i + 1]])
        rng.shuffle(vecs)
        if all(any(x) for x in vecs) and max(abs(x) for v in vecs for x in v) <= 9 and rank_of(vecs) == r \
                and len({tuple(v) for v in vecs}) == k:
            break
    names = [f"u{i + 1}" for i in range(k)]
    listing = ", ".join(f"{nm} = {vec_text(v)}" for nm, v in zip(names, vecs))
    return Draw(
        params={"vectors": vecs},
        prompt_vi=f"Trong R^{n} cho {listing}. Tìm số chiều của W = span{{{', '.join(names)}}}.",
        answer=str(r),
        solution_vi=["dim W bằng hạng của ma trận có các hàng là các vectơ đã cho.",
                     "Khử Gauss ma trận đó (các phép biến đổi hàng không làm đổi bao tuyến tính của các hàng).",
                     f"Dạng bậc thang còn {r} hàng khác 0, nên dim W = {r}."
                     + (" Các vectơ còn lại là tổ hợp tuyến tính của các vectơ ứng với hàng trụ." if r < k else "")])


# ------------------------------------------------------------------ tọa độ
@generator("dstt_g7_toa_do")
def toa_do(rng: random.Random) -> Draw:
    while True:
        low = [[1, 0, 0], [rng.randint(-1, 1), 1, 0], [rng.randint(-1, 1), rng.randint(-1, 1), 1]]
        up = [[1, rng.randint(-2, 2), rng.randint(-2, 2)], [0, 1, rng.randint(-2, 2)], [0, 0, 1]]
        p = [[sum(low[i][t] * up[t][j] for t in range(3)) for j in range(3)] for i in range(3)]   # det 1
        basis = [[p[i][j] for i in range(3)] for j in range(3)]          # the columns of p
        c = [rng.randint(-3, 3) for _ in range(3)]
        x = lin(c, basis)
        if all(any(b) for b in basis) and sum(1 for t in c if t != 0) >= 2 and max(abs(t) for t in x) <= 12 \
                and not all(basis[j][i] == (1 if i == j else 0) for i in range(3) for j in range(3)):
            break
    return Draw(
        params={"basis": basis, "x": x},
        prompt_vi=(f"Các vectơ b1 = {vec_text(basis[0])}, b2 = {vec_text(basis[1])}, b3 = {vec_text(basis[2])} "
                   f"lập thành một cơ sở của R^3. Tìm tọa độ của x = {vec_text(x)} trong cơ sở đó. "
                   "Nhập ba tọa độ theo thứ tự b1, b2, b3, cách nhau bằng dấu phẩy."),
        answer=nums(c),
        solution_vi=["Tọa độ (a, b, c) thỏa a b1 + b b2 + c b3 = x: một hệ ba phương trình, ba ẩn, "
                     "ma trận hệ số có các cột là b1, b2, b3.",
                     "Giải hệ bằng khử Gauss.",
                     f"Nghiệm: {vec_text(c)}. Thử lại: {coef_text(c, ['b1', 'b2', 'b3'])} = {vec_text(x)}."])
