"""Đại Số Tuyến Tính, tầng 3 (vectơ trong R^n và ma trận): generators. Matrices are sent
as figures (Draw.matrices); the game draws them, the text only names them."""
from __future__ import annotations

import random

from . import Draw, generator, matrix, nonzero, nums, paren, vec_text

BY_ROWS = "Nhập bốn phần tử theo từng hàng, cách nhau bằng dấu phẩy."


def term(coef: int, name: str) -> str:
    """coef * name written the usual way: u, -u, 2u, -3u."""
    return {1: name, -1: f"-{name}"}.get(coef, f"{coef}{name}")


def combo(a: int, x: str, b: int, y: str) -> str:
    """a*x + b*y written the usual way: 2A - 3B, -u + v."""
    return f"{term(a, x)} {'+' if b > 0 else '-'} {term(abs(b), y)}"


def _flat(m: list[list[int]]) -> list[int]:
    return [v for row in m for v in row]


# ------------------------------------------------------------------ vectơ trong R^n
@generator("dstt_g3_to_hop_vecto")
def to_hop_vecto(rng: random.Random) -> Draw:
    u = [rng.randint(-5, 5) for _ in range(3)]
    v = [rng.randint(-5, 5) for _ in range(3)]
    a, b = nonzero(rng, -3, 3), nonzero(rng, -3, 3)
    au, bv = [a * x for x in u], [b * x for x in v]
    res = [x + y for x, y in zip(au, bv)]
    return Draw(
        params={"u": u, "v": v, "a": a, "b": b},
        prompt_vi=(f"Cho u = {vec_text(u)} và v = {vec_text(v)} trong R^3. Tính {combo(a, 'u', b, 'v')}. "
                   "Nhập các tọa độ theo thứ tự, cách nhau bằng dấu phẩy."),
        answer=nums(res),
        solution_vi=[f"Nhân từng tọa độ: {term(a, 'u')} = {vec_text(au)} và {term(b, 'v')} = {vec_text(bv)}.",
                     "Cộng hai vectơ đó theo từng tọa độ tương ứng.",
                     f"Kết quả: {vec_text(res)}."])


@generator("dstt_g3_vecto_an")
def vecto_an(rng: random.Random) -> Draw:
    a = rng.choice([-4, -3, -2, 2, 3, 4])
    x = [rng.randint(-4, 4) for _ in range(3)]
    u = [rng.randint(-5, 5) for _ in range(3)]
    v = [a * xi + ui for xi, ui in zip(x, u)]
    diff = [vi - ui for vi, ui in zip(v, u)]
    return Draw(
        params={"a": a, "u": u, "v": v},
        prompt_vi=(f"Cho u = {vec_text(u)} và v = {vec_text(v)} trong R^3. Tìm vectơ x thỏa mãn "
                   f"{term(a, 'x')} + u = v. Nhập các tọa độ của x, cách nhau bằng dấu phẩy."),
        answer=nums(x),
        solution_vi=[f"Chuyển u sang vế phải: {term(a, 'x')} = v - u = {vec_text(diff)}.",
                     f"Chia từng tọa độ cho {a}: x = {vec_text(x)}."])


# ------------------------------------------------------------------ kích thước, phần tử a_ij
@generator("dstt_g3_phan_tu")
def phan_tu(rng: random.Random) -> Draw:
    rows, cols = rng.randint(2, 3), rng.randint(2, 4)
    while True:
        m = matrix(rng, rows, cols, -9, 9)
        i, j = rng.randint(1, rows), rng.randint(1, cols)
        mirror_exists = j <= rows and i <= cols
        if i != j and (not mirror_exists or m[i - 1][j - 1] != m[j - 1][i - 1]):
            break
    value = m[i - 1][j - 1]
    return Draw(
        params={"rows": m, "i": i, "j": j},
        prompt_vi=f"Cho ma trận A như hình. Phần tử a_{i}{j} bằng bao nhiêu?",
        answer=str(value), matrices={"A": m},
        solution_vi=[f"Trong a_{i}{j}, chỉ số thứ nhất là hàng, chỉ số thứ hai là cột.",
                     f"Hàng {i} của A là {vec_text(m[i - 1])}.",
                     f"Phần tử thứ {j} của hàng đó là {value}."])


@generator("dstt_g3_cong_thuc_hang")
def cong_thuc_hang(rng: random.Random) -> Draw:
    m, n = rng.randint(2, 3), rng.randint(3, 4)
    p, q = rng.randint(1, 3), nonzero(rng, -3, 3)
    r = rng.randint(1, m)
    row = [p * r + q * j for j in range(1, n + 1)]
    return Draw(
        params={"m": m, "n": n, "p": p, "q": q, "row": r},
        prompt_vi=(f"Ma trận A cỡ {m} x {n} có a_ij = {combo(p, 'i', q, 'j')}. "
                   f"Tính tổng các phần tử ở hàng {r}."),
        answer=str(sum(row)),
        solution_vi=[f"Hàng {r} gồm các phần tử có i = {r} và j chạy từ 1 đến {n}.",
                     f"Các phần tử đó là {nums(row)}.",
                     f"Tổng là {sum(row)}."])


# ------------------------------------------------------------------ cộng ma trận, nhân với một số
@generator("dstt_g3_cong_ma_tran")
def cong_ma_tran(rng: random.Random) -> Draw:
    a, b = matrix(rng, 2, 2, -6, 9), matrix(rng, 2, 2, -6, 9)
    op = rng.choice(["+", "-"])
    sign = 1 if op == "+" else -1
    res = [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
    return Draw(
        params={"a": a, "b": b, "op": op},
        prompt_vi=f"Cho hai ma trận A và B như hình. Tính A {op} B. {BY_ROWS}",
        answer=nums(_flat(res)), matrices={"A": a, "B": b},
        solution_vi=[f"{'Cộng' if op == '+' else 'Trừ'} từng cặp phần tử ở cùng vị trí.",
                     f"Hàng 1: {vec_text(res[0])}. Hàng 2: {vec_text(res[1])}.",
                     f"Nhập theo từng hàng: {nums(_flat(res))}."])


@generator("dstt_g3_to_hop_ma_tran")
def to_hop_ma_tran(rng: random.Random) -> Draw:
    a, b = matrix(rng, 2, 3, -5, 6), matrix(rng, 2, 3, -5, 6)
    p, q = rng.choice([-2, 2, 3]), rng.choice([-3, -2, -1, 2, 3])
    i, j = rng.randint(1, 2), rng.randint(1, 3)
    x, y = a[i - 1][j - 1], b[i - 1][j - 1]
    value = p * x + q * y
    return Draw(
        params={"a": a, "b": b, "p": p, "q": q, "i": i, "j": j},
        prompt_vi=(f"Cho hai ma trận A và B như hình. Phần tử ở hàng {i}, cột {j} của "
                   f"{combo(p, 'A', q, 'B')} bằng bao nhiêu?"),
        answer=str(value), matrices={"A": a, "B": b},
        solution_vi=[f"Chỉ cần phần tử ở hàng {i}, cột {j} của mỗi ma trận: a_{i}{j} = {x} và b_{i}{j} = {y}.",
                     f"{paren(p)} . {paren(x)} + {paren(q)} . {paren(y)} = {value}."])


# ------------------------------------------------------------------ chuyển vị
@generator("dstt_g3_chuyen_vi_phan_tu")
def chuyen_vi_phan_tu(rng: random.Random) -> Draw:
    rows, cols = rng.choice([(2, 3), (3, 2), (2, 4), (3, 4)])
    while True:
        m = matrix(rng, rows, cols, -9, 9)
        i, j = rng.randint(1, cols), rng.randint(1, rows)          # a position of A^T (cols x rows)
        same_place_in_a = i <= rows and j <= cols
        if i != j and (not same_place_in_a or m[i - 1][j - 1] != m[j - 1][i - 1]):
            break
    value = m[j - 1][i - 1]
    return Draw(
        params={"rows": m, "i": i, "j": j},
        prompt_vi=f"Cho ma trận A như hình. Phần tử ở hàng {i}, cột {j} của A^T bằng bao nhiêu?",
        answer=str(value), matrices={"A": m},
        solution_vi=["Chuyển vị đổi hàng thành cột: phần tử ở hàng i, cột j của A^T là phần tử ở hàng j, "
                     "cột i của A.",
                     f"Cần lấy phần tử ở hàng {j}, cột {i} của A.",
                     f"Đó là {value}."])


@generator("dstt_g3_chuyen_vi_tong")
def chuyen_vi_tong(rng: random.Random) -> Draw:
    while True:
        a = matrix(rng, 2, 2, -6, 9)
        if a[0][1] != a[1][0]:
            break
    b = matrix(rng, 2, 2, -6, 9)
    op = rng.choice(["+", "-"])
    sign = 1 if op == "+" else -1
    at = [[a[0][0], a[1][0]], [a[0][1], a[1][1]]]
    res = [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(at, b)]
    return Draw(
        params={"a": a, "b": b, "op": op},
        prompt_vi=f"Cho hai ma trận A và B như hình. Tính A^T {op} B. {BY_ROWS}",
        answer=nums(_flat(res)), matrices={"A": a, "B": b},
        solution_vi=[f"Các cột của A thành các hàng của A^T: hàng 1 là {vec_text(at[0])}, hàng 2 là "
                     f"{vec_text(at[1])}.",
                     f"{'Cộng' if op == '+' else 'Trừ'} từng phần tử với B: hàng 1 là {vec_text(res[0])}, "
                     f"hàng 2 là {vec_text(res[1])}.",
                     f"Nhập theo từng hàng: {nums(_flat(res))}."])


# ------------------------------------------------------------------ vết
@generator("dstt_g3_vet")
def vet(rng: random.Random) -> Draw:
    m = matrix(rng, 3, 3, -9, 9)
    diag = [m[k][k] for k in range(3)]
    return Draw(
        params={"rows": m},
        prompt_vi="Cho ma trận A như hình. Tính vết tr(A).",
        answer=str(sum(diag)), matrices={"A": m},
        solution_vi=["Vết là tổng các phần tử trên đường chéo chính.",
                     f"Đường chéo chính của A: {nums(diag)}.",
                     f"tr(A) = {sum(diag)}."])


@generator("dstt_g3_vet_to_hop")
def vet_to_hop(rng: random.Random) -> Draw:
    a, b = matrix(rng, 2, 2, -6, 9), matrix(rng, 2, 2, -6, 9)
    p, q = rng.choice([-2, 2, 3]), rng.choice([-3, -1, 2, 3])
    ta, tb = a[0][0] + a[1][1], b[0][0] + b[1][1]
    value = p * ta + q * tb
    expr = combo(p, "A", q, "B")
    return Draw(
        params={"a": a, "b": b, "p": p, "q": q},
        prompt_vi=f"Cho hai ma trận A và B như hình. Tính tr({expr}).",
        answer=str(value), matrices={"A": a, "B": b},
        solution_vi=[f"Vết có tính tuyến tính, nên chỉ cần tr(A) = {ta} và tr(B) = {tb}.",
                     f"tr({expr}) = {paren(p)} . {paren(ta)} + {paren(q)} . {paren(tb)} = {value}."])


# ------------------------------------------------------------------ các ma trận đặc biệt
def _symmetric(rng: random.Random) -> list[list[int]]:
    """A symmetric 3 x 3 matrix whose three off-diagonal values are all different."""
    off = rng.sample(range(-6, 10), 3)
    d = [rng.randint(-5, 9) for _ in range(3)]
    return [[d[0], off[0], off[1]], [off[0], d[1], off[2]], [off[1], off[2], d[2]]]


@generator("dstt_g3_dac_biet")
def dac_biet(rng: random.Random) -> Draw:
    kind = rng.choice(["symmetric", "upper", "diagonal"])
    truth = rng.random() < 0.5
    if kind == "symmetric":
        m = _symmetric(rng)
        claim = "ma trận đối xứng"
        rule = "Ma trận vuông là đối xứng khi a_ij = a_ji với mọi i, j."
        if truth:
            steps = [rule, f"Kiểm tra ba cặp: a_12 = a_21 = {m[0][1]}, a_13 = a_31 = {m[0][2]}, "
                           f"a_23 = a_32 = {m[1][2]}.", "Mọi cặp đều bằng nhau nên A đối xứng."]
        else:
            i, j = rng.choice([(1, 2), (1, 3), (2, 3)])
            m[i - 1][j - 1] += rng.choice([-2, -1, 1, 2])
            steps = [rule, f"a_{i}{j} = {m[i - 1][j - 1]} nhưng a_{j}{i} = {m[j - 1][i - 1]}.",
                     "Có một cặp khác nhau nên A không đối xứng."]
    elif kind == "upper":
        m = [[nonzero(rng, -5, 9) if c >= r else 0 for c in range(3)] for r in range(3)]
        claim = "ma trận tam giác trên"
        rule = "Ma trận tam giác trên có mọi phần tử nằm dưới đường chéo chính bằng 0."
        if truth:
            steps = [rule, "Các phần tử a_21, a_31, a_32 của A đều bằng 0.", "Vậy A là ma trận tam giác trên."]
        else:
            i, j = rng.choice([(2, 1), (3, 1), (3, 2)])
            m[i - 1][j - 1] = nonzero(rng, -5, 9)
            steps = [rule, f"a_{i}{j} = {m[i - 1][j - 1]} khác 0 và nằm dưới đường chéo chính.",
                     "Vậy A không phải là ma trận tam giác trên."]
    else:
        m = [[nonzero(rng, -5, 9) if c == r else 0 for c in range(3)] for r in range(3)]
        claim = "ma trận chéo"
        rule = "Ma trận chéo là ma trận vuông có mọi phần tử nằm ngoài đường chéo chính bằng 0."
        if truth:
            steps = [rule, "Sáu phần tử nằm ngoài đường chéo chính của A đều bằng 0.", "Vậy A là ma trận chéo."]
        else:
            i, j = rng.choice([(1, 2), (1, 3), (2, 3), (2, 1), (3, 1), (3, 2)])
            m[i - 1][j - 1] = nonzero(rng, -5, 9)
            steps = [rule, f"a_{i}{j} = {m[i - 1][j - 1]} khác 0 và nằm ngoài đường chéo chính.",
                     "Vậy A không phải là ma trận chéo."]
    return Draw(params={"kind": kind, "rows": m}, prompt_vi=f"Ma trận A như hình là {claim}.",
                answer=truth, matrices={"A": m}, solution_vi=steps)


@generator("dstt_g3_doi_xung_dien")
def doi_xung_dien(rng: random.Random) -> Draw:
    m = _symmetric(rng)
    (i, j), (r, c) = rng.sample([(1, 2), (1, 3), (2, 3)], 2)
    vx, vy = m[i - 1][j - 1], m[r - 1][c - 1]
    shown: list[list] = [list(row) for row in m]
    shown[i - 1][j - 1] = "x"           # x above the diagonal, y below it
    shown[c - 1][r - 1] = "y"
    return Draw(
        params={"rows": shown},
        prompt_vi="Ma trận A như hình là ma trận đối xứng. Tìm x và y. Nhập x rồi y, cách nhau bằng dấu phẩy.",
        answer=nums([vx, vy]), matrices={"A": shown},
        solution_vi=["Ma trận đối xứng có a_ij = a_ji với mọi i, j.",
                     f"x nằm ở hàng {i}, cột {j} nên x = a_{j}{i} = {vx}.",
                     f"y nằm ở hàng {c}, cột {r} nên y = a_{r}{c} = {vy}."])
