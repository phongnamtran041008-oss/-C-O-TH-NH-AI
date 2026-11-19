"""Đại Số Tuyến Tính, tầng 4 (nhân ma trận): generators. Matrices are sent as figures
(Draw.matrices); the game draws them, the text only names them. The arithmetic here is done
by hand on lists; tools/math_verify_dstt_t4.py redoes it with sympy Matrix products."""
from __future__ import annotations

import random

from . import Draw, generator, matrix, nonzero, nums, paren, vec_text

BY_ROWS = "Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy."


def _flat(m: list[list[int]]) -> list[int]:
    return [v for row in m for v in row]


def _mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _dot_text(u: list[int], v: list[int]) -> str:
    return " + ".join(f"{paren(a)} . {paren(b)}" for a, b in zip(u, v))


# ------------------------------------------------------------------ tích vô hướng
@generator("dstt_g4_tich_vo_huong")
def tich_vo_huong(rng: random.Random) -> Draw:
    n = rng.choice([3, 4])
    u = [rng.randint(-5, 6) for _ in range(n)]
    v = [rng.randint(-5, 6) for _ in range(n)]
    value = sum(a * b for a, b in zip(u, v))
    return Draw(
        params={"u": u, "v": v},
        prompt_vi=f"Tính tích vô hướng của u = {vec_text(u)} và v = {vec_text(v)} trong R^{n}.",
        answer=str(value),
        solution_vi=["Nhân từng cặp tọa độ cùng vị trí rồi cộng lại.",
                     f"u . v = {_dot_text(u, v)} = {value}."])


# ------------------------------------------------------------------ điều kiện kích thước
@generator("dstt_g4_nhan_duoc")
def nhan_duoc(rng: random.Random) -> Draw:
    m, n, q = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5)
    p = n if rng.random() < 0.5 else rng.choice([v for v in range(1, 6) if v != n])
    ok = n == p
    return Draw(
        params={"a": [m, n], "b": [p, q]},
        prompt_vi=f"A có cỡ {m} x {n} và B có cỡ {p} x {q}. Tích AB xác định.",
        answer=ok,
        solution_vi=["AB xác định khi số cột của A bằng số hàng của B.",
                     f"A có {n} cột, B có {p} hàng.",
                     f"{n} = {p} nên AB xác định và có cỡ {m} x {q}." if ok
                     else f"{n} khác {p} nên AB không xác định."])


@generator("dstt_g4_co_tich_ba")
def co_tich_ba(rng: random.Random) -> Draw:
    m, n, p, q = (rng.randint(1, 6) for _ in range(4))
    order = rng.choice(["ABC", "CTBTAT"])
    if order == "ABC":
        prompt = f"A có cỡ {m} x {n}, B có cỡ {n} x {p} và C có cỡ {p} x {q}. Tích ABC có cỡ bao nhiêu?"
        rows, cols = m, q
        steps = [f"AB có cỡ {m} x {p}, vì số cột của A bằng số hàng của B.",
                 f"(AB)C có cỡ {m} x {q}, vì số cột của AB là {p} bằng số hàng của C."]
    else:
        prompt = (f"A có cỡ {m} x {n}, B có cỡ {n} x {p} và C có cỡ {p} x {q}. Tích C^T B^T A^T có cỡ "
                  "bao nhiêu?")
        rows, cols = q, m
        steps = [f"C^T có cỡ {q} x {p}, B^T có cỡ {p} x {n}, A^T có cỡ {n} x {m}.",
                 f"Nhân lần lượt: C^T B^T có cỡ {q} x {n}, rồi C^T B^T A^T có cỡ {q} x {m}.",
                 "Đó cũng là cỡ của (ABC)^T, vì C^T B^T A^T = (ABC)^T."]
    return Draw(
        params={"m": m, "n": n, "p": p, "q": q, "order": order},
        prompt_vi=prompt + " Nhập số hàng rồi số cột, cách nhau bằng dấu phẩy.",
        answer=nums([rows, cols]),
        solution_vi=steps + [f"Kết quả: {rows} hàng, {cols} cột."])


# ------------------------------------------------------------------ nhân hai ma trận
@generator("dstt_g4_phan_tu_tich")
def phan_tu_tich(rng: random.Random) -> Draw:
    a, b = matrix(rng, 2, 3, -4, 5), matrix(rng, 3, 2, -4, 5)
    i, j = rng.randint(1, 2), rng.randint(1, 2)
    row, col = a[i - 1], [b[k][j - 1] for k in range(3)]
    value = sum(x * y for x, y in zip(row, col))
    return Draw(
        params={"a": a, "b": b, "i": i, "j": j},
        prompt_vi=(f"Cho A cỡ 2 x 3 và B cỡ 3 x 2 như hình. Tính phần tử ở hàng {i}, cột {j} của AB."),
        answer=str(value), matrices={"A": a, "B": b},
        solution_vi=[f"Phần tử hàng {i}, cột {j} của AB là hàng {i} của A nhân cột {j} của B.",
                     f"Hàng {i} của A là {vec_text(row)}, cột {j} của B là {vec_text(col)}.",
                     f"{_dot_text(row, col)} = {value}."])


@generator("dstt_g4_tich_2x2")
def tich_2x2(rng: random.Random) -> Draw:
    a, b = matrix(rng, 2, 2, -4, 5), matrix(rng, 2, 2, -4, 5)
    c = _mul(a, b)
    return Draw(
        params={"a": a, "b": b},
        prompt_vi=f"Cho hai ma trận A và B như hình. Tính AB. {BY_ROWS}",
        answer=nums(_flat(c)), matrices={"A": a, "B": b},
        solution_vi=["Phần tử hàng i, cột j của AB là hàng i của A nhân cột j của B.",
                     f"Hàng 1: ({_dot_text(a[0], [b[0][0], b[1][0]])}, {_dot_text(a[0], [b[0][1], b[1][1]])}) = "
                     f"{vec_text(c[0])}.",
                     f"Hàng 2: ({_dot_text(a[1], [b[0][0], b[1][0]])}, {_dot_text(a[1], [b[0][1], b[1][1]])}) = "
                     f"{vec_text(c[1])}."])


# ------------------------------------------------------------------ AB != BA
@generator("dstt_g4_giao_hoan")
def giao_hoan(rng: random.Random) -> Draw:
    while True:
        a = matrix(rng, 2, 2, -3, 4)
        if a[0][1] != 0 or a[1][0] != 0:        # not diagonal: some B does not commute with it
            break
    if rng.random() < 0.5:                      # B = pA + qI always commutes with A
        p, q = nonzero(rng, -2, 2), rng.randint(-3, 3)
        b = [[p * a[r][c] + (q if r == c else 0) for c in range(2)] for r in range(2)]
    else:
        b = matrix(rng, 2, 2, -3, 4)
    ab, ba = _mul(a, b), _mul(b, a)
    same = ab == ba
    return Draw(
        params={"a": a, "b": b},
        prompt_vi="Cho hai ma trận A và B như hình. Ta có AB = BA.",
        answer=same, matrices={"A": a, "B": b},
        solution_vi=[f"AB có hàng {vec_text(ab[0])} và {vec_text(ab[1])}.",
                     f"BA có hàng {vec_text(ba[0])} và {vec_text(ba[1])}.",
                     "Hai ma trận bằng nhau: A và B giao hoán." if same
                     else "Hai ma trận khác nhau: phép nhân ma trận không giao hoán."])


# ------------------------------------------------------------------ tính chất
@generator("dstt_g4_chuyen_vi_tich")
def chuyen_vi_tich(rng: random.Random) -> Draw:
    a, b = matrix(rng, 2, 2, -4, 5), matrix(rng, 2, 2, -4, 5)
    i, j = rng.choice([(1, 2), (2, 1)])
    ab = _mul(a, b)
    value = ab[j - 1][i - 1]                     # (AB)^T at (i, j) = (AB) at (j, i)
    return Draw(
        params={"a": a, "b": b, "i": i, "j": j},
        prompt_vi=(f"Cho hai ma trận A và B như hình. Tính phần tử ở hàng {i}, cột {j} của B^T A^T."),
        answer=str(value), matrices={"A": a, "B": b},
        solution_vi=["B^T A^T = (AB)^T, nên phần tử hàng i, cột j của nó là phần tử hàng j, cột i của AB.",
                     f"Cần hàng {j} của A nhân cột {i} của B: {vec_text(a[j - 1])} . "
                     f"{vec_text([b[0][i - 1], b[1][i - 1]])}.",
                     f"{_dot_text(a[j - 1], [b[0][i - 1], b[1][i - 1]])} = {value}."])


# ------------------------------------------------------------------ lũy thừa
@generator("dstt_g4_binh_phuong")
def binh_phuong(rng: random.Random) -> Draw:
    a = matrix(rng, 2, 2, -3, 4)
    sq = _mul(a, a)
    return Draw(
        params={"a": a},
        prompt_vi=f"Cho ma trận A như hình. Tính A^2. {BY_ROWS}",
        answer=nums(_flat(sq)), matrices={"A": a},
        solution_vi=["A^2 = A . A: nhân hàng của A với cột của A, không bình phương từng ô.",
                     f"Hàng 1: {vec_text(sq[0])}. Hàng 2: {vec_text(sq[1])}.",
                     f"Nhập theo từng hàng: {nums(_flat(sq))}."])


@generator("dstt_g4_luy_thua_n")
def luy_thua_n(rng: random.Random) -> Draw:
    a, n = nonzero(rng, -5, 5), rng.randint(3, 12)
    kind = rng.choice(["upper", "lower"])
    shown = [[1, a], [0, 1]] if kind == "upper" else [[1, 0], [a, 1]]
    pos = "hàng 1, cột 2" if kind == "upper" else "hàng 2, cột 1"
    return Draw(
        params={"a": a, "n": n, "kind": kind},
        prompt_vi=f"Cho ma trận A như hình. Tính phần tử ở {pos} của A^{n}.",
        answer=str(n * a), matrices={"A": shown},
        solution_vi=[f"A^2 = A . A có phần tử ở {pos} bằng {a} + {paren(a)} = {2 * a}, các phần tử khác như của A.",
                     f"Mỗi lần nhân thêm A, phần tử ở {pos} tăng thêm {a}, còn đường chéo vẫn là 1.",
                     f"Vậy A^{n} có phần tử ở {pos} bằng {n} . {paren(a)} = {n * a}."])
