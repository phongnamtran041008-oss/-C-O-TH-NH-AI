"""Đại Số Tuyến Tính, tầng 8 (ánh xạ tuyến tính và ma trận của nó): generators.

Bases are drawn with determinant 1 or -1, so coordinates and inverses stay whole numbers; a
matrix of rank r is r echelon rows mixed by a coefficient matrix that contains an identity
block. The arithmetic here is plain list arithmetic; tools/math_verify_dstt_t7.py redoes each
answer with sympy by another route (inverse matrices, nullspace, symbolic substitution,
solving P B = A P)."""
from __future__ import annotations

import random

from . import Draw, generator, nonzero, nums, paren, vec_text
from .dstt_floor7 import _echelon, coef_text, lin, rank_of

UNIMODULAR = [((1, 0), (1, 1)), ((1, 1), (1, 2)), ((2, 1), (1, 1)), ((1, 2), (1, 3)), ((1, 1), (0, 1)),
              ((2, 1), (3, 2)), ((1, -1), (0, 1)), ((1, 1), (1, 0)), ((1, 2), (0, 1)), ((3, 2), (1, 1)),
              ((1, -1), (-1, 2)), ((2, 3), (1, 2))]
BY_ROWS = "Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy."


def mul(a, b):
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def flat(m) -> list:
    return [v for row in m for v in row]


def inv2(p):
    """Inverse of a 2 x 2 matrix with determinant 1 or -1 (whole entries)."""
    d = p[0][0] * p[1][1] - p[0][1] * p[1][0]
    return [[p[1][1] * d, -p[0][1] * d], [-p[1][0] * d, p[0][0] * d]]     # (1/d = d when d = +-1)


def basis2(rng: random.Random):
    b1, b2 = rng.choice(UNIMODULAR)
    if rng.random() < 0.5:
        b1, b2 = b2, b1
    return list(b1), list(b2)


def form_text(row, names=("x", "y", "z")) -> str:
    return coef_text(row, names[:len(row)])


# ------------------------------------------------------------------ ánh xạ tuyến tính
@generator("dstt_g8_anh_vecto")
def anh_vecto(rng: random.Random) -> Draw:
    while True:
        b1, b2 = basis2(rng)
        p = [rng.randint(-4, 4) for _ in range(2)]
        q = [rng.randint(-4, 4) for _ in range(2)]
        c = [nonzero(rng, -3, 3), nonzero(rng, -3, 3)]
        v = lin(c, [b1, b2])
        img = lin(c, [p, q])
        if any(p) and any(q) and p != q and v not in (b1, b2) and max(abs(t) for t in v) <= 9:
            break
    return Draw(
        params={"b1": b1, "b2": b2, "p": p, "q": q, "v": v},
        prompt_vi=(f"Ánh xạ tuyến tính f: R^2 -> R^2 có f{vec_text(b1)} = {vec_text(p)} và "
                   f"f{vec_text(b2)} = {vec_text(q)}. Tính f{vec_text(v)}. Nhập hai tọa độ, cách nhau bằng dấu phẩy."),
        answer=nums(img),
        solution_vi=[f"Viết {vec_text(v)} = a{vec_text(b1)} + b{vec_text(b2)}; giải hệ hai ẩn được a = {c[0]}, b = {c[1]}.",
                     f"Vì f tuyến tính: f{vec_text(v)} = {paren(c[0])} . {vec_text(p)} + {paren(c[1])} . {vec_text(q)}.",
                     f"= {vec_text(img)}."])


# ------------------------------------------------------------------ định lý số chiều
@generator("dstt_g8_so_chieu_nhan")
def so_chieu_nhan(rng: random.Random) -> Draw:
    while True:
        m, n = rng.choice([(3, 4), (4, 4), (3, 3), (4, 3), (2, 4)])
        r = rng.randint(1, min(m, n) - (1 if m == n else 0))
        e = _echelon(rng, r, n)
        mix = [[rng.randint(-2, 2) for _ in range(r)] for _ in range(m)]
        for i in range(r):
            mix[i] = [1 if j == i else 0 for j in range(r)]
        rows = [lin(mix[i], e) for i in range(m)]
        for i in range(r - 1):
            rows[i] = lin([1, rng.randint(-1, 1)], [rows[i], rows[i + 1]])
        rng.shuffle(rows)
        if all(any(x) for x in rows) and max(abs(x) for row in rows for x in row) <= 9 and rank_of(rows) == r:
            break
    which = rng.choice(["ker", "im"])
    ans = n - r if which == "ker" else r
    asked = "dim Ker f" if which == "ker" else "dim Im f"
    return Draw(
        params={"a": rows, "which": which},
        prompt_vi=f"Ánh xạ tuyến tính f: R^{n} -> R^{m} cho bởi f(x) = Ax, với ma trận A như hình. Tìm {asked}.",
        answer=str(ans), matrices={"A": rows},
        solution_vi=["dim Im f bằng hạng của A (Im f được sinh bởi các cột của A).",
                     f"Khử Gauss: dạng bậc thang của A còn {r} hàng khác 0, nên rank A = {r} = dim Im f.",
                     f"Định lý số chiều: dim Ker f = {n} - {r} = {n - r}."])


# ------------------------------------------------------------------ ma trận của ánh xạ
@generator("dstt_g8_ma_tran_co_so")
def ma_tran_co_so(rng: random.Random) -> Draw:
    """The matrix of f: R^3 -> R^2 (a formula) in a basis b1, b2, b3 of R^3 and the standard
    basis of R^2: its column j is f(b_j)."""
    while True:
        f = [[rng.randint(-2, 3) for _ in range(3)] for _ in range(2)]
        low = [[1, 0, 0], [rng.randint(-1, 1), 1, 0], [rng.randint(-1, 1), rng.randint(-1, 1), 1]]
        up = [[1, rng.randint(-1, 1), rng.randint(-1, 1)], [0, 1, rng.randint(-1, 1)], [0, 0, 1]]
        p = mul(low, up)                              # columns: the basis
        basis = [[p[i][j] for i in range(3)] for j in range(3)]
        res = mul(f, p)
        if all(any(r) for r in f) and max(abs(v) for v in flat(res)) <= 12 and \
                sum(1 for j in range(3) if basis[j] != [1 if i == j else 0 for i in range(3)]) >= 2:
            break
    images = [[res[0][j], res[1][j]] for j in range(3)]
    return Draw(
        params={"f": f, "basis": basis},
        prompt_vi=(f"Cho f: R^3 -> R^2, f(x, y, z) = ({form_text(f[0])}, {form_text(f[1])}), và cơ sở "
                   f"b1 = {vec_text(basis[0])}, b2 = {vec_text(basis[1])}, b3 = {vec_text(basis[2])} của R^3. "
                   f"Tìm ma trận của f đối với cơ sở đó của R^3 và cơ sở chính tắc của R^2 (cỡ 2 x 3). {BY_ROWS}"),
        answer=nums(flat(res)),
        solution_vi=["Cột thứ j của ma trận là tọa độ của f(b_j) trong cơ sở đích; với cơ sở chính tắc của R^2, "
                     "đó chính là f(b_j).",
                     f"f(b1) = {vec_text(images[0])}, f(b2) = {vec_text(images[1])}, f(b3) = {vec_text(images[2])}.",
                     f"Đặt ba vectơ đó thành ba cột: hàng 1 là {vec_text(res[0])}, hàng 2 là {vec_text(res[1])}."])


# ------------------------------------------------------------------ hợp ánh xạ
@generator("dstt_g8_hop")
def hop(rng: random.Random) -> Draw:
    while True:
        f = [[rng.randint(-3, 3) for _ in range(2)] for _ in range(2)]
        g = [[rng.randint(-3, 3) for _ in range(2)] for _ in range(2)]
        if all(any(r) for r in f + g) and mul(g, f) != mul(f, g):
            break
    order = rng.choice(["gf", "fg"])
    res = mul(g, f) if order == "gf" else mul(f, g)
    name, first = ("g o f", "f") if order == "gf" else ("f o g", "g")
    left, right = ("A_g", "A_f") if order == "gf" else ("A_f", "A_g")
    return Draw(
        params={"f": f, "g": g, "order": order},
        prompt_vi=(f"Cho f(x, y) = ({form_text(f[0])}, {form_text(f[1])}) và g(x, y) = ({form_text(g[0])}, "
                   f"{form_text(g[1])}). Tìm ma trận chính tắc của {name} (làm {first} trước). {BY_ROWS}"),
        answer=nums(flat(res)),
        solution_vi=[f"Ma trận chính tắc: A_f có hàng {vec_text(f[0])}, {vec_text(f[1])}; A_g có hàng "
                     f"{vec_text(g[0])}, {vec_text(g[1])}.",
                     f"Ánh xạ làm {first} trước có ma trận {left} {right} (ma trận của ánh xạ làm sau đứng bên trái).",
                     f"{left} {right} có hàng {vec_text(res[0])} và {vec_text(res[1])}."])


# ------------------------------------------------------------------ đổi cơ sở
@generator("dstt_g8_doi_co_so")
def doi_co_so(rng: random.Random) -> Draw:
    while True:
        b1, b2 = basis2(rng)
        p = [[b1[0], b2[0]], [b1[1], b2[1]]]
        a = [[rng.randint(-3, 4) for _ in range(2)] for _ in range(2)]
        res = mul(inv2(p), mul(a, p))
        if max(abs(v) for v in flat(res)) <= 15 and res != a and any(flat(a)):
            break
    pinv = inv2(p)
    ap = mul(a, p)
    return Draw(
        params={"a": a, "p": p},
        prompt_vi=(f"Ánh xạ tuyến tính f: R^2 -> R^2 có ma trận chính tắc A như hình. Cơ sở mới b1 = {vec_text(b1)}, "
                   f"b2 = {vec_text(b2)} là hai cột của P. Tìm ma trận B của f trong cơ sở b1, b2. {BY_ROWS}"),
        answer=nums(flat(res)), matrices={"A": a, "P": p},
        solution_vi=["B = P^(-1) A P.",
                     f"det P = {p[0][0] * p[1][1] - p[0][1] * p[1][0]}, nên P^(-1) có hàng {vec_text(pinv[0])} "
                     f"và {vec_text(pinv[1])}.",
                     f"AP có hàng {vec_text(ap[0])} và {vec_text(ap[1])}.",
                     f"B = P^(-1)(AP) có hàng {vec_text(res[0])} và {vec_text(res[1])}."])
