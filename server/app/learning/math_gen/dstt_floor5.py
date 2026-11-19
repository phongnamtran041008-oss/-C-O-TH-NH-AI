"""Đại Số Tuyến Tính, tầng 5 (hệ phương trình tuyến tính và khử Gauss): generators.

Systems are built backwards so that every answer is a small integer: a solution is drawn
first and the right-hand side computed from it, and a 3 x 3 system is A = L U with L unit
lower triangular, so Gaussian elimination without row swaps gives exactly U. The arithmetic
here is done by hand on lists of Fractions; tools/math_verify_dstt_t4.py redoes every answer
with sympy (linsolve, rank, nullspace, elementary matrices)."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, linear_text, matrix, nonzero, num, nums, paren, vec_text


def _mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _apply(a: list[list[int]], x: list[int]) -> list[int]:
    return [sum(r * v for r, v in zip(row, x)) for row in a]


def rank(rows: list[list]) -> int:
    """Rank by Gaussian elimination over the rationals."""
    m = [[Fraction(v) for v in row] for row in rows]
    r = 0
    for c in range(len(m[0]) if m else 0):
        pivot = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        for i in range(r + 1, len(m)):
            f = m[i][c] / m[r][c]
            m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        r += 1
    return r


def lu_pair(rng: random.Random, diag: list[int]) -> tuple[list[list[int]], list[list[int]]]:
    """(L, U): L unit lower triangular, U upper triangular with this diagonal, small entries."""
    l = [[1, 0, 0], [rng.randint(-2, 2), 1, 0], [rng.randint(-2, 2), rng.randint(-2, 2), 1]]
    u = [[diag[0], rng.randint(-2, 3), rng.randint(-2, 3)], [0, diag[1], rng.randint(-2, 3)], [0, 0, diag[2]]]
    return l, u


def eq_text(coefs: list[int], rhs: int, names: str = "xyz") -> str:
    """2x - y + 3z = 4, written the usual way (terms with coefficient 0 left out)."""
    out = ""
    for c, v in zip(coefs, names):
        if c == 0:
            continue
        mag = "" if abs(c) == 1 else str(abs(c))
        if not out:
            out = f"{'-' if c < 0 else ''}{mag}{v}"
        else:
            out += f" {'-' if c < 0 else '+'} {mag}{v}"
    return f"{out or '0'} = {rhs}"


def row_text(coefs: list, rhs) -> str:
    return "(" + ", ".join(num(c) for c in coefs) + " | " + num(rhs) + ")"


# ------------------------------------------------------------------ viết hệ dưới dạng Ax = b
@generator("dstt_g5_tim_b")
def tim_b(rng: random.Random) -> Draw:
    a = matrix(rng, 3, 3, -3, 4)
    x = [rng.randint(-3, 3) for _ in range(3)]
    b = _apply(a, x)
    return Draw(
        params={"a": a, "x": x},
        prompt_vi=(f"Hệ Ax = b có ma trận hệ số A như hình (ẩn x, y, z) và nhận (x, y, z) = {vec_text(x)} làm "
                   "nghiệm. Tìm vế phải b. Nhập ba tọa độ, cách nhau bằng dấu phẩy."),
        answer=nums(b), matrices={"A": a},
        solution_vi=["Vì (x, y, z) là nghiệm nên b = A nhân vectơ nghiệm: mỗi tọa độ của b là một hàng của A "
                     "nhân với nghiệm.",
                     *[f"Hàng {i + 1}: {' + '.join(f'{paren(c)} . {paren(v)}' for c, v in zip(a[i], x))} = {b[i]}."
                       for i in range(3)],
                     f"b = {vec_text(b)}."])


# ------------------------------------------------------------------ ba phép biến đổi sơ cấp
@generator("dstt_g5_cong_boi_hang")
def cong_boi_hang(rng: random.Random) -> Draw:
    a = matrix(rng, 3, 3, -4, 5)
    i, j = rng.sample([1, 2, 3], 2)
    k = nonzero(rng, -3, 3)
    new = [x + k * y for x, y in zip(a[i - 1], a[j - 1])]
    op = f"R{i} <- R{i} {'+' if k > 0 else '-'} {'' if abs(k) == 1 else abs(k)}R{j}"
    return Draw(
        params={"a": a, "i": i, "j": j, "k": k},
        prompt_vi=(f"Cho ma trận A như hình. Làm phép {op}. Nhập hàng {i} mới, cách nhau bằng dấu phẩy."),
        answer=nums(new), matrices={"A": a},
        solution_vi=[f"Phép này chỉ thay hàng {i}: lấy hàng {i} cộng {paren(k)} lần hàng {j}; hàng {j} giữ nguyên.",
                     f"Hàng {i} là {vec_text(a[i - 1])}, {paren(k)} lần hàng {j} là "
                     f"{vec_text([k * y for y in a[j - 1]])}.",
                     f"Cộng từng tọa độ: {vec_text(new)}."])


# ------------------------------------------------------------------ thế ngược
@generator("dstt_g5_giai_he_2")
def giai_he_2(rng: random.Random) -> Draw:
    while True:
        a = [[nonzero(rng, -4, 4), rng.randint(-4, 4)], [rng.randint(-4, 4), rng.randint(-4, 4)]]
        if a[0][0] * a[1][1] - a[0][1] * a[1][0] != 0:
            break
    x = [rng.randint(-5, 5), rng.randint(-5, 5)]
    b = _apply(a, x)
    p, q = a[0][0], a[1][0]
    new = [0, p * a[1][1] - q * a[0][1]]
    new_rhs = p * b[1] - q * b[0]
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=(f"Giải hệ {eq_text(a[0], b[0], 'xy')} và {eq_text(a[1], b[1], 'xy')}. "
                   "Nhập x rồi y, cách nhau bằng dấu phẩy."),
        answer=nums(x),
        solution_vi=[f"Ma trận bổ sung có hàng {row_text(a[0], b[0])} và {row_text(a[1], b[1])}.",
                     (f"Khử x ở hàng 2: R2 <- {paren(p)} . R2 - {paren(q)} . R1, được {row_text(new, new_rhs)}."
                      if q else f"Hàng 2 không có x; nhân nó với {paren(p)} cho gọn: {row_text(new, new_rhs)}."),
                     f"Từ hàng 2: y = {num(Fraction(new_rhs, new[1]))}.",
                     f"Thế vào hàng 1: {paren(a[0][0])}x = {b[0]} - {paren(a[0][1])} . {paren(x[1])}, "
                     f"nên x = {x[0]}."])


@generator("dstt_g5_giai_he_3")
def giai_he_3(rng: random.Random) -> Draw:
    l, u = lu_pair(rng, [rng.choice([1, -1, 2]), rng.choice([1, -1, 2, -2]), rng.choice([1, -1, 2, 3])])
    a = _mul(l, u)
    x = [rng.randint(-3, 3) for _ in range(3)]
    b = _apply(a, x)
    c = _apply(u, x)                       # the right-hand side after elimination
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=("Giải hệ ba phương trình, ba ẩn x, y, z có ma trận bổ sung M như hình (cột cuối là vế phải). "
                   "Nhập x, y, z theo thứ tự, cách nhau bằng dấu phẩy."),
        answer=nums(x), matrices={"M": [row + [rhs] for row, rhs in zip(a, b)]},
        solution_vi=[f"Khử Gauss, không cần đổi chỗ hàng: dùng hàng 1 khử x ở hàng 2 và 3, rồi dùng hàng 2 mới "
                     "khử y ở hàng 3.",
                     f"Dạng bậc thang có các hàng {row_text(u[0], c[0])}, {row_text(u[1], c[1])}, "
                     f"{row_text(u[2], c[2])}.",
                     f"Thế ngược: z = {c[2]}/{paren(u[2][2])} = {x[2]}, rồi y = {x[1]}, rồi x = {x[0]}.",
                     f"Nghiệm (x, y, z) = {vec_text(x)}."])


# ------------------------------------------------------------------ biện luận số nghiệm
KINDS_VI = {"unique": "có nghiệm duy nhất", "none": "vô nghiệm", "many": "có vô số nghiệm"}


@generator("dstt_g5_so_nghiem")
def so_nghiem(rng: random.Random) -> Draw:
    kind = rng.choice(list(KINDS_VI))
    claim = kind if rng.random() < 0.5 else rng.choice([k for k in KINDS_VI if k != kind])
    r1 = [nonzero(rng, -3, 4), rng.randint(-3, 4), rng.randint(-3, 4), rng.randint(-5, 5)]
    r2 = [0, nonzero(rng, -3, 4), rng.randint(-3, 4), rng.randint(-5, 5)]
    if kind == "unique":
        r3 = [0, 0, nonzero(rng, -3, 4), rng.randint(-5, 5)]
        why = "Mỗi ẩn x, y, z đều có trụ và không có hàng (0, 0, 0 | khác 0), nên hệ có nghiệm duy nhất."
    elif kind == "none":
        r3 = [0, 0, 0, nonzero(rng, -5, 5)]
        why = f"Hàng 3 nói 0 = {r3[3]}, vô lý, nên hệ vô nghiệm."
    else:
        r3 = [0, 0, 0, 0]
        why = "Hàng 3 là 0 = 0; z không có trụ nên là ẩn tự do, và hệ có vô số nghiệm."
    return Draw(
        params={"rows": [r1, r2, r3], "claim": claim},
        prompt_vi=(f"Hệ ẩn x, y, z có ma trận bổ sung M như hình, đã ở dạng bậc thang (cột cuối là vế phải). "
                   f"Hệ {KINDS_VI[claim]}."),
        answer=kind == claim, matrices={"M": [r1, r2, r3]},
        solution_vi=["Đọc số nghiệm từ dạng bậc thang: hàng (0, 0, 0 | khác 0) thì vô nghiệm; nếu không, ẩn nào "
                     "cũng có trụ thì nghiệm duy nhất, còn có ẩn tự do thì vô số nghiệm.",
                     why,
                     "Mệnh đề đúng." if kind == claim else f"Mệnh đề sai: hệ {KINDS_VI[kind]}."])


@generator("dstt_g5_tham_so")
def tham_so(rng: random.Random) -> Draw:
    while True:
        p, q, r = nonzero(rng, -3, 3), nonzero(rng, -4, 4), nonzero(rng, -4, 4)
        if (q * r) % p == 0:
            break
    m = q * r // p
    b1, b2 = rng.randint(-5, 5), rng.randint(-5, 5)
    return Draw(
        params={"p": p, "q": q, "r": r, "b": [b1, b2]},
        prompt_vi=(f"Cho hệ {eq_text([p, q], b1, 'xy')} và {eq_text([r], b2, 'x').split(' = ')[0]} + my = {b2}, "
                   "với m là tham số. "
                   "Tìm giá trị m để hệ KHÔNG có nghiệm duy nhất."),
        answer=str(m),
        solution_vi=[f"Khử x ở hàng 2: R2 <- {paren(p)} . R2 - {paren(r)} . R1. Hệ số của y ở hàng 2 mới là "
                     f"{paren(p)} . m - {paren(r)} . {paren(q)} = {linear_text(p, -r * q, 'm')}.",
                     "Hệ có nghiệm duy nhất khi và chỉ khi hệ số đó khác 0, tức là y có trụ.",
                     f"Hệ số bằng 0 khi m = {num(Fraction(r * q, p))}: khi đó hệ vô nghiệm hoặc vô số nghiệm."])


# ------------------------------------------------------------------ hệ thuần nhất
@generator("dstt_g5_tam_thuong")
def tam_thuong(rng: random.Random) -> Draw:
    if rng.random() < 0.5:
        l, u = lu_pair(rng, [nonzero(rng, -2, 2), nonzero(rng, -2, 2), nonzero(rng, -2, 2)])
        a = _mul(l, u)
    else:
        while True:
            r1, r2 = [rng.randint(-3, 3) for _ in range(3)], [rng.randint(-3, 3) for _ in range(3)]
            s, t = rng.randint(-2, 2), rng.randint(-2, 2)
            a = [r1, r2, [s * x + t * y for x, y in zip(r1, r2)]]
            if rank(a) == 2:
                break
        a = rng.sample(a, 3)                    # the dependent row is not always the last one
    full = rank(a) == 3
    return Draw(
        params={"a": a},
        prompt_vi="Cho ma trận A vuông cấp 3 như hình. Hệ thuần nhất Ax = 0 chỉ có nghiệm tầm thường x = 0.",
        answer=full, matrices={"A": a},
        solution_vi=["Khử Gauss ma trận A và đếm số trụ (số hàng khác không của dạng bậc thang).",
                     f"Dạng bậc thang có {rank(a)} hàng khác không.",
                     "Đủ 3 trụ cho 3 ẩn, không có ẩn tự do: chỉ có nghiệm tầm thường." if full
                     else "Chỉ có 2 trụ cho 3 ẩn, còn một ẩn tự do: hệ có nghiệm khác 0."])


@generator("dstt_g5_an_tu_do")
def an_tu_do(rng: random.Random) -> Draw:
    r = rng.choice([1, 2, 2, 3])
    while True:
        p = matrix(rng, 3, r, -2, 2)
        q = matrix(rng, r, 4, -2, 3)
        a = _mul(p, q)
        if rank(a) == r and all(max(abs(v) for v in row) <= 9 for row in a):
            break
    return Draw(
        params={"a": a},
        prompt_vi=("Cho ma trận A cỡ 3 x 4 như hình. Hệ thuần nhất Ax = 0 có bốn ẩn. Khi giải bằng khử Gauss, "
                   "có bao nhiêu ẩn tự do?"),
        answer=str(4 - r), matrices={"A": a},
        solution_vi=["Khử Gauss ma trận A; mỗi hàng khác không của dạng bậc thang cho một trụ.",
                     f"Dạng bậc thang có {r} hàng khác không, tức là {r} ẩn có trụ.",
                     f"Số ẩn tự do là 4 - {r} = {4 - r}."])
