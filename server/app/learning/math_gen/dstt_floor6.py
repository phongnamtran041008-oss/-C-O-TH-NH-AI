"""Đại Số Tuyến Tính, tầng 6 (định thức, hạng, ma trận nghịch đảo): generators.

Determinants here are worked out by hand (Sarrus, cofactor expansion along the row that has
the zeros), inverses by the adjugate; tools/math_verify_dstt_t4.py redoes every answer with
sympy (det, cofactor, rank, inv, linsolve). Matrices are built so that answers stay small:
an invertible 3 x 3 matrix is L U with unit diagonals, so its determinant is 1 and its inverse
has whole entries."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, matrix, nonzero, num, nums, paren, vec_text
from .dstt_floor5 import _apply, _mul, eq_text, lu_pair, rank


def det2(m) -> int:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def det3(m) -> int:
    """Sarrus."""
    down = m[0][0] * m[1][1] * m[2][2] + m[0][1] * m[1][2] * m[2][0] + m[0][2] * m[1][0] * m[2][1]
    up = m[0][2] * m[1][1] * m[2][0] + m[0][0] * m[1][2] * m[2][1] + m[0][1] * m[1][0] * m[2][2]
    return down - up


def minor(m, i: int, j: int) -> list[list[int]]:
    """m without row i and column j (0-based)."""
    return [[v for c, v in enumerate(row) if c != j] for r, row in enumerate(m) if r != i]


def cofactor(m, i: int, j: int) -> int:
    sub = minor(m, i, j)
    d = det2(sub) if len(sub) == 2 else det3(sub)
    return (-1) ** (i + j) * d


def rows_text(m) -> str:
    return ", ".join(vec_text(r) for r in m)


# ------------------------------------------------------------------ định thức cấp 2 và 3
@generator("dstt_g6_dinh_thuc_3")
def dinh_thuc_3(rng: random.Random) -> Draw:
    a = matrix(rng, 3, 3, -3, 4)
    down = [a[0][0] * a[1][1] * a[2][2], a[0][1] * a[1][2] * a[2][0], a[0][2] * a[1][0] * a[2][1]]
    up = [a[0][2] * a[1][1] * a[2][0], a[0][0] * a[1][2] * a[2][1], a[0][1] * a[1][0] * a[2][2]]
    d = det3(a)
    return Draw(
        params={"a": a},
        prompt_vi="Tính định thức của ma trận A cấp 3 như hình.",
        answer=str(d), matrices={"A": a},
        solution_vi=["Quy tắc Sarrus: cộng ba tích theo đường chéo xuống, trừ ba tích theo đường chéo lên.",
                     f"Ba tích đường chéo xuống: {nums(down)}; ba tích đường chéo lên: {nums(up)}.",
                     f"det A = ({' + '.join(paren(v) for v in down)}) - ({' + '.join(paren(v) for v in up)}) = {d}."])


@generator("dstt_g6_tim_x_det")
def tim_x_det(rng: random.Random) -> Draw:
    while True:
        a = matrix(rng, 3, 3, -3, 4)
        i, j = rng.randint(0, 2), rng.randint(0, 2)
        c = cofactor(a, i, j)
        if c != 0:
            break
    a[i][j] = 0
    rest = det3(a)                              # the determinant is c * x + rest
    target = rng.randint(-12, 12)
    x = Fraction(target - rest, c)
    shown = [list(r) for r in a]
    shown[i][j] = "x"
    return Draw(
        params={"rows": shown, "target": target},
        prompt_vi=f"Cho ma trận A như hình, trong đó x là một số thực. Tìm x để det A = {target}.",
        answer=num(x), matrices={"A": shown},
        solution_vi=[f"Khai triển theo hàng {i + 1}: x chỉ xuất hiện ở vị trí ({i + 1}, {j + 1}), nên det A = "
                     f"x . C_{i + 1}{j + 1} + (phần còn lại).",
                     f"C_{i + 1}{j + 1} = {c}; các số hạng còn lại cộng được {rest} (bằng det A khi x = 0).",
                     f"Giải {c}x + {paren(rest)} = {target}: x = {num(x)}."])


# ------------------------------------------------------------------ khai triển
@generator("dstt_g6_phan_bu")
def phan_bu(rng: random.Random) -> Draw:
    a = matrix(rng, 3, 3, -4, 5)
    i, j = rng.randint(1, 3), rng.randint(1, 3)
    sub = minor(a, i - 1, j - 1)
    c = cofactor(a, i - 1, j - 1)
    return Draw(
        params={"a": a, "i": i, "j": j},
        prompt_vi=f"Cho ma trận A như hình. Tính phần bù đại số C_{i}{j}.",
        answer=str(c), matrices={"A": a},
        solution_vi=[f"Bỏ hàng {i} và cột {j} của A: định thức con M_{i}{j} có hàng {rows_text(sub)}, "
                     f"bằng {det2(sub)}.",
                     f"Dấu ở vị trí ({i}, {j}) là (-1)^({i} + {j}) = {(-1) ** (i + j)}.",
                     f"C_{i}{j} = {(-1) ** (i + j)} . {paren(det2(sub))} = {c}."])


@generator("dstt_g6_khai_trien_4")
def khai_trien_4(rng: random.Random) -> Draw:
    a = matrix(rng, 4, 4, -2, 3)
    r, c = rng.randint(0, 3), rng.randint(0, 3)
    value = nonzero(rng, -3, 3)
    for k in range(4):
        a[r][k] = 0
    a[r][c] = value
    sub = minor(a, r, c)
    m = det3(sub)
    sign = (-1) ** (r + c)
    d = value * sign * m
    return Draw(
        params={"a": a},
        prompt_vi="Tính định thức của ma trận A cấp 4 như hình.",
        answer=str(d), matrices={"A": a},
        solution_vi=[f"Hàng {r + 1} chỉ có một phần tử khác 0 là a_{r + 1}{c + 1} = {value}: khai triển theo hàng đó.",
                     f"Định thức con M_{r + 1}{c + 1} (bỏ hàng {r + 1}, cột {c + 1}) có hàng {rows_text(sub)}; "
                     f"theo Sarrus nó bằng {m}.",
                     f"Dấu (-1)^({r + 1} + {c + 1}) = {sign}, nên det A = {value} . {paren(sign)} . {paren(m)} = {d}."])


# ------------------------------------------------------------------ tính chất
@generator("dstt_g6_tinh_chat")
def tinh_chat(rng: random.Random) -> Draw:
    n, d = rng.choice([2, 3]), nonzero(rng, -4, 5)
    kind = rng.choice(["kA", "AT", "A2", "inv", "neg", "AB"])
    k, e = rng.choice([-2, 2, 3]), nonzero(rng, -3, 3)
    base = f"A là ma trận vuông cấp {n} có det A = {d}."
    if kind == "kA":
        expr, value = f"det({k}A)", Fraction(k) ** n * d
        why = [f"{k}A nhân cả {n} hàng của A với {k}, mỗi hàng nhân định thức với {k}.",
               f"det({k}A) = {paren(k)}^{n} . {paren(d)} = {num(value)}."]
    elif kind == "AT":
        expr, value = "det(A^T)", Fraction(d)
        why = ["Chuyển vị không đổi định thức.", f"det(A^T) = det A = {d}."]
    elif kind == "A2":
        expr, value = "det(A^2)", Fraction(d) ** 2
        why = ["Định thức nhân tính: det(A^2) = det A . det A.", f"det(A^2) = {paren(d)}^2 = {num(value)}."]
    elif kind == "inv":
        expr, value = "det(A^(-1))", Fraction(1, d)
        why = ["A A^(-1) = I nên det A . det(A^(-1)) = 1.", f"det(A^(-1)) = 1/{paren(d)} = {num(value)}."]
    elif kind == "neg":
        expr, value = "det(-A)", Fraction(-1) ** n * d
        why = [f"-A nhân cả {n} hàng của A với -1.", f"det(-A) = (-1)^{n} . {paren(d)} = {num(value)}."]
    else:
        base += f" B cùng cấp có det B = {e}."
        expr, value = "det(A^T B)", Fraction(d * e)
        why = ["Định thức nhân tính và det(A^T) = det A.", f"det(A^T B) = {paren(d)} . {paren(e)} = {num(value)}."]
    return Draw(
        params={"n": n, "d": d, "kind": kind, "k": k, "e": e},
        prompt_vi=f"{base} Tính {expr}.",
        answer=num(value),
        solution_vi=why)


# ------------------------------------------------------------------ hạng
@generator("dstt_g6_hang")
def hang(rng: random.Random) -> Draw:
    r = rng.choice([1, 2, 2, 3, 3])
    while True:
        p = matrix(rng, 4, r, -2, 2)
        q = matrix(rng, r, 3, -2, 3)
        a = _mul(p, q)
        if rank(a) == r and all(max(abs(v) for v in row) <= 9 for row in a) and all(any(row) for row in a):
            break
    return Draw(
        params={"a": a},
        prompt_vi="Tìm hạng của ma trận A cỡ 4 x 3 như hình.",
        answer=str(r), matrices={"A": a},
        solution_vi=["Khử Gauss đưa A về dạng bậc thang; hạng là số hàng khác không của dạng đó.",
                     f"Dạng bậc thang của A có {r} hàng khác không; các hàng còn lại bị khử thành 0 vì chúng là "
                     "tổ hợp của các hàng khác.",
                     f"rank A = {r}."])


# ------------------------------------------------------------------ nghịch đảo
@generator("dstt_g6_nghich_dao_2")
def nghich_dao_2(rng: random.Random) -> Draw:
    while True:
        a = matrix(rng, 2, 2, -4, 5)
        d = det2(a)
        if d in (-3, -2, -1, 1, 2, 3, 4):
            break
    inv = [[Fraction(a[1][1], d), Fraction(-a[0][1], d)], [Fraction(-a[1][0], d), Fraction(a[0][0], d)]]
    flat = [v for row in inv for v in row]
    return Draw(
        params={"a": a},
        prompt_vi="Tìm ma trận nghịch đảo của A như hình. Nhập bốn phần tử của A^(-1) theo từng hàng, cách nhau "
                  "bằng dấu phẩy (phân số viết a/b).",
        answer=nums(flat), matrices={"A": a},
        solution_vi=[f"det A = {paren(a[0][0])} . {paren(a[1][1])} - {paren(a[0][1])} . {paren(a[1][0])} = {d}, "
                     "khác 0, nên A khả nghịch.",
                     f"Với ma trận cấp 2: đổi chỗ hai phần tử trên đường chéo chính, đổi dấu hai phần tử còn lại, "
                     f"rồi chia cho det A = {d}.",
                     f"A^(-1) có hàng ({nums(flat[:2])}) và ({nums(flat[2:])})."])


@generator("dstt_g6_kha_nghich")
def kha_nghich(rng: random.Random) -> Draw:
    if rng.random() < 0.5:
        l, u = lu_pair(rng, [nonzero(rng, -2, 2), nonzero(rng, -2, 2), nonzero(rng, -2, 2)])
        a = _mul(l, u)
    else:
        while True:
            c1, c2 = [rng.randint(-3, 3) for _ in range(3)], [rng.randint(-3, 3) for _ in range(3)]
            s, t = rng.randint(-2, 2), rng.randint(-2, 2)
            cols = [c1, c2, [s * x + t * y for x, y in zip(c1, c2)]]
            cols = rng.sample(cols, 3)                  # a column that depends on the other two
            a = [[cols[c][r] for c in range(3)] for r in range(3)]
            if rank(a) == 2:
                break
    d = det3(a)
    return Draw(
        params={"a": a},
        prompt_vi="Ma trận A vuông cấp 3 như hình là ma trận khả nghịch.",
        answer=d != 0, matrices={"A": a},
        solution_vi=["A khả nghịch khi và chỉ khi det A khác 0.",
                     f"Theo Sarrus (hoặc khử Gauss), det A = {d}.",
                     "det A khác 0 nên A khả nghịch: mệnh đề đúng." if d
                     else "det A = 0 (một cột là tổ hợp của hai cột kia), nên A không khả nghịch: mệnh đề sai."])


# ------------------------------------------------------------------ giải hệ bằng nghịch đảo, Cramer
@generator("dstt_g6_cramer")
def cramer(rng: random.Random) -> Draw:
    while True:
        a = matrix(rng, 2, 2, -4, 5)
        d = det2(a)
        if d != 0:
            break
    b = [rng.randint(-6, 6), rng.randint(-6, 6)]
    which = rng.choice(["x", "y"])
    col = 0 if which == "x" else 1
    swapped = [[b[r] if c == col else a[r][c] for c in range(2)] for r in range(2)]
    dk = det2(swapped)
    return Draw(
        params={"a": a, "b": b, "which": which},
        prompt_vi=(f"Dùng quy tắc Cramer để tìm {which} của hệ {eq_text(a[0], b[0], 'xy')} và "
                   f"{eq_text(a[1], b[1], 'xy')}."),
        answer=num(Fraction(dk, d)),
        solution_vi=[f"det A = {paren(a[0][0])} . {paren(a[1][1])} - {paren(a[0][1])} . {paren(a[1][0])} = {d}, "
                     "khác 0, nên dùng được quy tắc Cramer.",
                     f"Thay cột {col + 1} của A bằng vế phải: ma trận có hàng {rows_text(swapped)}, định thức {dk}.",
                     f"{which} = {dk}/{paren(d)} = {num(Fraction(dk, d))}."])


def _inverse_unimodular(a: list[list[int]]) -> list[list[int]]:
    """The inverse of a 3 x 3 integer matrix of determinant 1 or -1: adjugate / det."""
    d = det3(a)
    return [[cofactor(a, j, i) // d for j in range(3)] for i in range(3)]


@generator("dstt_g6_giai_he_nd")
def giai_he_nd(rng: random.Random) -> Draw:
    l, u = lu_pair(rng, [rng.choice([1, -1]), rng.choice([1, -1]), rng.choice([1, -1])])
    a = _mul(l, u)
    inv = _inverse_unimodular(a)
    b = [rng.randint(-4, 4) for _ in range(3)]
    x = _apply(inv, b)
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=(f"Ma trận A như hình có det A = {det3(a)}. Giải hệ Ax = b với b = {vec_text(b)} bằng cách "
                   "tìm A^(-1). Nhập ba tọa độ của x, cách nhau bằng dấu phẩy."),
        answer=nums(x), matrices={"A": a},
        solution_vi=["A khả nghịch vì det A khác 0, nên x = A^(-1) b.",
                     f"Khử Gauss-Jordan trên (A | I) (hoặc lấy phần phụ hợp chia cho det A): A^(-1) có hàng "
                     f"{rows_text(inv)}.",
                     f"Nhân A^(-1) với b: x = {vec_text(x)}. Thử lại: A x = {vec_text(_apply(a, x))} = b."])
