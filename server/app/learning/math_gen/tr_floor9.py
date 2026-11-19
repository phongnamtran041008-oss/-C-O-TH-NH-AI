"""Tối Ưu và Toán Rời Rạc, floor 9 (quy hoạch tuyến tính, quy hoạch phi tuyến; mở rộng AI:
nhân tử Lagrange, hạ gradient, hàm mất mát): generators, all tier 5. Ids start with `tr_g9_`.

Every linear programme has two variables x, y >= 0 and two or three constraints
a x + b y <= r with positive coefficients, so its feasible region is a bounded polygon; the
generator keeps only instances whose optimum is one vertex (no ties), and for the simplex
step and the dual only those whose ratio test and dual solution are unique. The generators
work the way the floor teaches (the vertices of the polygon, one pivot of the simplex
dictionary, complementary slackness, the Lagrange system solved by hand, a descent step);
tools/math_verify_tr_t7.py recomputes with sympy's own simplex (lpmax / lpmin), a tableau
pivot with sympy matrices, sympy's solve on the Lagrange and KKT systems, and the gradient
with diff and Rationals."""
from __future__ import annotations

import itertools
import random
from fractions import Fraction

from . import Draw, generator, num, nums, paren
from .tr_floor8 import poly_text


# ------------------------------------------------------------------ linear programmes in two variables
def lp_vertices(cons) -> list[tuple[Fraction, Fraction]]:
    """The vertices of {x, y >= 0, a x + b y <= r for (a, b, r) in cons}."""
    lines = [tuple(c) for c in cons] + [(-1, 0, 0), (0, -1, 0)]
    out = []
    for (a1, b1, r1), (a2, b2, r2) in itertools.combinations(lines, 2):
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        x, y = Fraction(r1 * b2 - r2 * b1, det), Fraction(a1 * r2 - a2 * r1, det)
        if x >= 0 and y >= 0 and all(a * x + b * y <= r for a, b, r in cons) and (x, y) not in out:
            out.append((x, y))
    return sorted(out)


def lp_best(c, cons) -> tuple[tuple[Fraction, Fraction], Fraction, list] | None:
    """The optimal vertex, its value and every vertex with its value; None when two vertices tie."""
    verts = lp_vertices(cons)
    vals = [(c[0] * x + c[1] * y, (x, y)) for x, y in verts]
    vals.sort(reverse=True)
    if len(vals) < 2 or vals[0][0] == vals[1][0]:
        return None
    return vals[0][1], vals[0][0], vals


def cons_text(cons, names=("x", "y")) -> str:
    return ", ".join(f"{poly_text([(a, names[0]), (b, names[1])])} <= {r}" for a, b, r in cons)


def random_lp(rng: random.Random, m: int, both_positive: bool = False):
    """(c, cons, best) with a unique optimum; both_positive: the optimum has x, y > 0 and is
    the crossing of the first two constraints (so the dual has one solution)."""
    while True:
        cons = [(rng.randint(1, 6), rng.randint(1, 6), rng.randint(6, 30)) for _ in range(m)]
        if len({(a, b) for a, b, _ in cons}) < m:
            continue
        c = (rng.randint(1, 8), rng.randint(1, 8))
        best = lp_best(c, cons)
        if best is None:
            continue
        (x, y), value, _ = best
        if both_positive:
            tight = [k for k, (a, b, r) in enumerate(cons) if a * x + b * y == r]
            if not (x > 0 and y > 0 and tight == [0, 1]):
                continue
        elif x == 0 and y == 0:
            continue
        return c, cons, best


def _vertex_lines(vals) -> str:
    return "; ".join(f"({num(x)}, {num(y)}): {num(v)}" for v, (x, y) in sorted(vals, key=lambda t: t[1]))


def _lp_prompt(c, cons) -> str:
    return (f"max z = {poly_text([(c[0], 'x'), (c[1], 'y')])} với các ràng buộc {cons_text(cons)}, x >= 0, y >= 0")


# ------------------------------------------------------------------ mô hình
@generator("tr_g9_san_xuat")
def san_xuat(rng: random.Random) -> Draw:
    c, cons, best = random_lp(rng, 2)
    (x, y), value, vals = best
    (a1, b1, r1), (a2, b2, r2) = cons
    prompt = (f"Một lò luyện đan làm hai loại đan dược A và B. Mỗi cân đan A cần {a1} cân linh thảo và {a2} giờ lửa; mỗi "
              f"cân đan B cần {b1} cân linh thảo và {b2} giờ lửa. Lò có {r1} cân linh thảo và {r2} giờ lửa. Mỗi cân đan A "
              f"lãi {c[0]} linh thạch, mỗi cân đan B lãi {c[1]} linh thạch; số cân có thể không nguyên. Tiền lãi lớn nhất "
              "là bao nhiêu linh thạch?")
    return Draw(params={"c": list(c), "cons": [list(k) for k in cons]}, prompt_vi=prompt, answer=num(value),
                solution_vi=["Gọi x, y là số cân đan A, B. Mô hình: "
                             f"{_lp_prompt(c, cons)}.",
                             "Miền ràng buộc là một đa giác lồi; nghiệm tối ưu nằm ở một đỉnh. Đỉnh và giá trị z: "
                             + _vertex_lines(vals) + ".",
                             f"Lãi lớn nhất {num(value)} linh thạch, tại x = {num(x)}, y = {num(y)}."])


# ------------------------------------------------------------------ phương pháp hình học
@generator("tr_g9_gia_tri_qhtt")
def gia_tri_qhtt(rng: random.Random) -> Draw:
    c, cons, best = random_lp(rng, 3)
    (x, y), value, vals = best
    return Draw(params={"c": list(c), "cons": [list(k) for k in cons]},
                prompt_vi=f"Giải bài toán {_lp_prompt(c, cons)}. Nhập giá trị tối ưu của z.",
                answer=num(value),
                solution_vi=["Miền ràng buộc là đa giác lồi bị chặn; hàm mục tiêu tuyến tính nên đạt max tại một đỉnh.",
                             "Các đỉnh (giao của hai đường biên thỏa mọi ràng buộc) và giá trị z: " + _vertex_lines(vals) + ".",
                             f"Giá trị tối ưu z = {num(value)} tại ({num(x)}, {num(y)})."])


@generator("tr_g9_dinh_qhtt")
def dinh_qhtt(rng: random.Random) -> Draw:
    c, cons, best = random_lp(rng, rng.choice([2, 3]))
    (x, y), value, vals = best
    return Draw(params={"c": list(c), "cons": [list(k) for k in cons]},
                prompt_vi=f"Bài toán {_lp_prompt(c, cons)} có đúng một nghiệm tối ưu (x, y). Nhập x, y.",
                answer=nums([x, y]),
                solution_vi=["Liệt kê các đỉnh của miền ràng buộc rồi tính z ở mỗi đỉnh: " + _vertex_lines(vals) + ".",
                             f"z lớn nhất bằng {num(value)}, chỉ đạt tại một đỉnh: x = {num(x)}, y = {num(y)}."])


@generator("tr_g9_rang_buoc_long")
def rang_buoc_long(rng: random.Random) -> Draw:
    c, cons, best = random_lp(rng, 3)
    (x, y), value, vals = best
    k = rng.randrange(3)
    a, b, r = cons[k]
    lhs = a * x + b * y
    slack = lhs < r
    return Draw(params={"c": list(c), "cons": [list(t) for t in cons], "k": k},
                prompt_vi=(f"Xét bài toán {_lp_prompt(c, cons)}. Khẳng định: tại nghiệm tối ưu, ràng buộc "
                           f"{poly_text([(a, 'x'), (b, 'y')])} <= {r} không chặt (vế trái nhỏ hơn hẳn {r})."),
                answer=slack,
                solution_vi=["Các đỉnh và giá trị z: " + _vertex_lines(vals) + f"; nghiệm tối ưu ({num(x)}, {num(y)}).",
                             f"Thay vào: {poly_text([(a, 'x'), (b, 'y')])} = {num(lhs)} "
                             f"{'<' if slack else '='} {r}.",
                             "Ràng buộc lỏng (còn dư): khẳng định đúng." if slack else
                             "Ràng buộc chặt (dùng hết): khẳng định sai."])


# ------------------------------------------------------------------ phương pháp đơn hình
@generator("tr_g9_don_hinh")
def don_hinh(rng: random.Random) -> Draw:
    while True:
        m = rng.choice([2, 3])
        cons = [(rng.randint(0, 5), rng.randint(0, 5), rng.randint(4, 24)) for _ in range(m)]
        if any(a == 0 and b == 0 for a, b, _ in cons):
            continue
        c = rng.sample(range(1, 9), 2)
        j = 0 if c[0] > c[1] else 1
        ratios = [(Fraction(r, k[j]), i) for i, (*k, r) in enumerate(cons) if k[j] > 0]
        ratios = [(t, i) for t, i in sorted(ratios)]
        if len(ratios) >= 1 and (len(ratios) == 1 or ratios[0][0] != ratios[1][0]):
            break
    t, leave = ratios[0]
    z = c[j] * t
    names = ["x1", "x2"]
    dictionary = "; ".join(_slack_row(i, a, b, r) for i, (a, b, r) in enumerate(cons))
    return Draw(params={"c": list(c), "cons": [list(k) for k in cons]},
                prompt_vi=(f"Giải max z = {poly_text([(c[0], 'x1'), (c[1], 'x2')])} với các biến không âm, bằng phương "
                           f"pháp đơn hình, xuất phát từ từ vựng (bảng) ban đầu: {dictionary}; z = "
                           f"{poly_text([(c[0], 'x1'), (c[1], 'x2')])}. Biến vào là biến có hệ số dương lớn nhất trong "
                           "z, biến ra theo quy tắc tỉ số nhỏ nhất. Sau bước lặp đầu tiên, nhập giá trị của biến vào "
                           "rồi giá trị của z."),
                answer=nums([t, z]),
                solution_vi=[f"Hệ số trong z: {c[0]} (x1), {c[1]} (x2); biến vào là {names[j]}.",
                             "Tỉ số r / (hệ số của biến vào) ở các hàng có hệ số dương: "
                             + "; ".join(f"hàng s{i + 1}: {num(q)}" for q, i in ratios) + ".",
                             f"Tỉ số nhỏ nhất {num(t)} ở hàng s{leave + 1}: s{leave + 1} ra khỏi cơ sở, "
                             f"{names[j]} = {num(t)}, biến kia vẫn bằng 0.",
                             f"z = {c[j]} . {paren(t)} = {num(z)}. Đáp số: {num(t)}, {num(z)}."])


def _slack_row(i: int, a: int, b: int, r: int) -> str:
    terms = "".join(f" - {'' if k == 1 else k}{v}" for k, v in ((a, "x1"), (b, "x2")) if k)
    return f"s{i + 1} = {r}{terms}"


# ------------------------------------------------------------------ đối ngẫu
def _dual_text(c, cons) -> str:
    (a1, b1, r1), (a2, b2, r2) = cons
    return (f"min w = {poly_text([(r1, 'u'), (r2, 'v')])} với {poly_text([(a1, 'u'), (a2, 'v')])} >= {c[0]}, "
            f"{poly_text([(b1, 'u'), (b2, 'v')])} >= {c[1]}, u >= 0, v >= 0")


@generator("tr_g9_doi_ngau_gia_tri")
def doi_ngau_gia_tri(rng: random.Random) -> Draw:
    c, cons, best = random_lp(rng, 2)
    (x, y), value, vals = best
    return Draw(params={"c": list(c), "cons": [list(k) for k in cons]},
                prompt_vi=(f"Bài toán gốc: {_lp_prompt(c, cons)}. Viết bài toán đối ngẫu của nó (biến đối ngẫu u, v "
                           "ứng với hai ràng buộc) và nhập giá trị tối ưu của bài toán đối ngẫu."),
                answer=num(value),
                solution_vi=[f"Bài toán đối ngẫu: {_dual_text(c, cons)}.",
                             "Định lý đối ngẫu mạnh: bài gốc có nghiệm tối ưu thì bài đối ngẫu cũng có, và hai giá trị "
                             "tối ưu bằng nhau.",
                             "Giải bài gốc bằng các đỉnh: " + _vertex_lines(vals) + f"; max z = {num(value)}.",
                             f"Vậy min w = {num(value)}."])


@generator("tr_g9_doi_ngau_nghiem")
def doi_ngau_nghiem(rng: random.Random) -> Draw:
    c, cons, best = random_lp(rng, 2, both_positive=True)
    (x, y), value, vals = best
    (a1, b1, r1), (a2, b2, r2) = cons
    det = a1 * b2 - a2 * b1
    u = Fraction(c[0] * b2 - c[1] * a2, det)
    v = Fraction(a1 * c[1] - b1 * c[0], det)
    return Draw(params={"c": list(c), "cons": [list(k) for k in cons]},
                prompt_vi=(f"Bài toán gốc: {_lp_prompt(c, cons)}. Bài toán đối ngẫu: {_dual_text(c, cons)}. Nhập "
                           "nghiệm tối ưu u, v của bài toán đối ngẫu."),
                answer=nums([u, v]),
                solution_vi=["Đỉnh và giá trị của bài gốc: " + _vertex_lines(vals)
                             + f"; nghiệm tối ưu x = {num(x)}, y = {num(y)}, cả hai dương.",
                             "Độ lệch bù: x > 0 nên ràng buộc đối ngẫu thứ nhất chặt, y > 0 nên ràng buộc thứ hai chặt: "
                             f"{poly_text([(a1, 'u'), (a2, 'v')])} = {c[0]}, {poly_text([(b1, 'u'), (b2, 'v')])} = {c[1]}.",
                             f"Giải hệ: u = {num(u)}, v = {num(v)} (đều không âm). Kiểm tra: "
                             f"{r1} . {paren(u)} + {r2} . {paren(v)} = {num(r1 * u + r2 * v)} = max z."])


# ------------------------------------------------------------------ Lagrange và KKT
@generator("tr_g9_lagrange")
def lagrange(rng: random.Random) -> Draw:
    kind = rng.choice(["min", "min", "tich"])
    if kind == "min":
        a, b = rng.randint(1, 4), rng.randint(1, 4)
        p, q = rng.choice([-3, -2, -1, 1, 2, 3]), rng.choice([-3, -2, -1, 1, 2, 3])
        r = rng.randint(1, 12)
        lam = Fraction(r) / (Fraction(p * p, 2 * a) + Fraction(q * q, 2 * b))
        x, y = lam * p / (2 * a), lam * q / (2 * b)
        best = a * x * x + b * y * y
        params = {"kind": kind, "a": a, "b": b, "p": p, "q": q, "r": r}
        f, g = poly_text([(a, "x^2"), (b, "y^2")]), poly_text([(p, "x"), (q, "y")])
        prompt = (f"Tìm giá trị nhỏ nhất của f(x, y) = {f} với ràng buộc {g} = {r}. Nhập x, y tại điểm đạt min, rồi giá "
                  "trị nhỏ nhất.")
        steps = [f"L(x, y, lambda) = {f} - lambda({g} - {r}).",
                 f"L_x = {2 * a}x - {paren(p)}lambda = 0, L_y = {2 * b}y - {paren(q)}lambda = 0, nên x = "
                 f"{num(Fraction(p, 2 * a))}lambda, y = {num(Fraction(q, 2 * b))}lambda.",
                 f"Thay vào ràng buộc: lambda = {num(lam)}, x = {num(x)}, y = {num(y)}.",
                 f"f là hàm lồi chặt và ràng buộc tuyến tính, nên điểm này là cực tiểu toàn cục: f = {num(best)}."]
    else:
        p, q, r = rng.randint(1, 5), rng.randint(1, 5), rng.randint(2, 20)
        x, y = Fraction(r, 2 * p), Fraction(r, 2 * q)
        best = x * y
        lam = Fraction(r, 2 * p * q)
        params = {"kind": kind, "p": p, "q": q, "r": r}
        g = poly_text([(p, "x"), (q, "y")])
        prompt = (f"Tìm giá trị lớn nhất của f(x, y) = xy với ràng buộc {g} = {r}. Nhập x, y tại điểm đạt max, rồi giá trị "
                  "lớn nhất.")
        steps = [f"L(x, y, lambda) = xy - lambda({g} - {r}).",
                 f"L_x = y - {p}lambda = 0, L_y = x - {q}lambda = 0, nên y = {p}lambda, x = {q}lambda.",
                 f"Thay vào ràng buộc: {2 * p * q}lambda = {r}, lambda = {num(lam)}, x = {num(x)}, y = {num(y)}.",
                 f"Trên đường thẳng ràng buộc, xy là một parabol theo x quay xuống, nên đây là max: {num(best)}."]
    return Draw(params=params, prompt_vi=prompt, answer=nums([x, y, best]), solution_vi=steps)


@generator("tr_g9_kkt")
def kkt(rng: random.Random) -> Draw:
    a, b = rng.randint(-5, 5), rng.randint(-5, 5)
    p, q = rng.choice([1, 2, -1, 1]), rng.choice([1, 2, 1, -1])
    r = rng.randint(-6, 6)
    if p * a + q * b == r:
        r += 1
    kind = rng.choice(["chat", "tam", "chieu"])
    inside = p * a + q * b <= r
    t = Fraction(p * a + q * b - r, p * p + q * q)
    proj = (a - t * p, b - t * q)
    g = poly_text([(p, "x"), (q, "y")])
    f = f"{_shift('x', a)}^2 + {_shift('y', b)}^2"
    if kind == "chat":
        claim, ok = f"tại nghiệm tối ưu, ràng buộc chặt ({g} = {r})", not inside
    elif kind == "tam":
        claim, ok = f"nghiệm tối ưu là điểm ({a}, {b})", inside
    else:
        claim, ok = f"nghiệm tối ưu là điểm ({num(proj[0])}, {num(proj[1])})", not inside
    steps = [f"Bỏ ràng buộc thì f nhỏ nhất (bằng 0) tại ({a}, {b}). Kiểm tra: {g} tại đó bằng {p * a + q * b}, "
             f"{'<=' if inside else '>'} {r}."]
    if inside:
        steps.append(f"({a}, {b}) thỏa ràng buộc nên là nghiệm, với nhân tử mu = 0 và ràng buộc không chặt.")
    else:
        steps.append(f"({a}, {b}) vi phạm ràng buộc, nên tại nghiệm ràng buộc chặt (mu > 0): nghiệm là hình chiếu của "
                     f"({a}, {b}) lên đường thẳng {g} = {r}, tức ({num(proj[0])}, {num(proj[1])}), với mu = {num(2 * t)}.")
    steps.append("Khẳng định đúng." if ok else "Khẳng định sai.")
    return Draw(params={"a": a, "b": b, "p": p, "q": q, "r": r, "kind": kind},
                prompt_vi=(f"Xét bài toán min f(x, y) = {f} với ràng buộc {g} <= {r}. Khẳng định: {claim}."),
                answer=ok, solution_vi=steps)


def _shift(var: str, a: int) -> str:
    if a == 0:
        return var
    return f"({var} - {a})" if a > 0 else f"({var} + {-a})"


# ------------------------------------------------------------------ hạ gradient
@generator("tr_g9_gd_buoc")
def gd_buoc(rng: random.Random) -> Draw:
    a, b = rng.randint(1, 4), rng.randint(1, 4)
    c, d = rng.randint(-6, 6), rng.randint(-6, 6)
    x0, y0 = rng.randint(-3, 3), rng.randint(-3, 3)
    eta = Fraction(1, rng.choice([4, 5, 8, 10]))
    steps_n = rng.choice([1, 2])
    pts = [(Fraction(x0), Fraction(y0))]
    lines = []
    for k in range(steps_n):
        x, y = pts[-1]
        gx, gy = 2 * a * x + c, 2 * b * y + d
        nxt = (x - eta * gx, y - eta * gy)
        lines.append(f"Bước {k + 1}: gradient tại ({num(x)}, {num(y)}) là ({num(gx)}, {num(gy)}); điểm mới "
                     f"({num(x)} - {num(eta)} . {paren(gx)}, {num(y)} - {num(eta)} . {paren(gy)}) = "
                     f"({num(nxt[0])}, {num(nxt[1])}).")
        pts.append(nxt)
    f = poly_text([(a, "x^2"), (b, "y^2"), (c, "x"), (d, "y")])
    return Draw(params={"a": a, "b": b, "c": c, "d": d, "x0": x0, "y0": y0, "eta": num(eta), "n": steps_n},
                prompt_vi=(f"Chạy hạ gradient cho f(x, y) = {f} từ điểm ({x0}, {y0}) với bước học {num(eta)}: mỗi bước "
                           f"thay điểm p bằng p - {num(eta)} . grad f(p). Sau {steps_n} bước, nhập tọa độ x, y của điểm."),
                answer=nums(pts[-1]),
                solution_vi=[f"grad f(x, y) = ({poly_text([(2 * a, 'x'), (c, '')])}, {poly_text([(2 * b, 'y'), (d, '')])})."]
                            + lines)


@generator("tr_g9_gd_hoi_tu")
def gd_hoi_tu(rng: random.Random) -> Draw:
    a = rng.randint(1, 5)
    m = rng.randint(-4, 4)
    eta = Fraction(rng.choice([1, 2, 3, 4, 5, 6, 8]), 4 * a)
    factor = 1 - 2 * a * eta
    kind = rng.choice(["hoi_tu", "giam"])
    f = f"{'' if a == 1 else a}{_shift('x', m)}^2"
    x0 = m + rng.choice([-3, -2, -1, 1, 2, 3])
    ok = abs(factor) < 1
    if kind == "hoi_tu":
        claim = f"với mọi điểm xuất phát, dãy hạ gradient hội tụ về {m}"
    else:
        claim = f"xuất phát từ x0 = {x0}, sau một bước giá trị của f giảm hẳn"
    dx, dnew = _shift("x", m), _shift("x mới", m)
    steps = [f"f'(x) = {2 * a}{dx}, nên {dnew} = {dx} - {num(eta)} . {2 * a}{dx} = {paren(factor)}{dx}.",
             f"Khoảng cách tới {m} nhân với |{num(factor)}| sau mỗi bước, và f nhân với {num(factor * factor)}."]
    if ok:
        steps.append(f"|{num(factor)}| < 1: khoảng cách và f đều giảm dần về 0. Khẳng định đúng.")
    elif factor == -1:
        steps.append("Hệ số bằng -1: điểm nhảy qua lại giữa hai vị trí đối xứng, f không đổi, không hội tụ. Khẳng định sai.")
    else:
        steps.append(f"|{num(factor)}| > 1: bước học quá lớn, điểm văng ra xa dần và f tăng. Khẳng định sai.")
    return Draw(params={"a": a, "m": m, "eta": num(eta), "kind": kind, "x0": x0},
                prompt_vi=(f"Chạy hạ gradient cho f(x) = {f} với bước học {num(eta)} (mỗi bước x mới = x - {num(eta)} . "
                           f"f'(x)). Khẳng định: {claim}."),
                answer=ok, solution_vi=steps)


@generator("tr_g9_mat_mat")
def mat_mat(rng: random.Random) -> Draw:
    k = rng.choice([2, 3])
    xs = rng.sample([1, 2, 3, 4, -1, -2], k)
    ys = [rng.randint(-6, 9) for _ in range(k)]
    w0 = rng.randint(-2, 3)
    eta = Fraction(1, rng.choice([10, 20, 40, 50]))
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    grad = 2 * (w0 * sxx - sxy)
    w1 = w0 - eta * grad
    wstar = Fraction(sxy, sxx)
    data = ", ".join(f"({x}, {y})" for x, y in zip(xs, ys))
    return Draw(params={"xs": xs, "ys": ys, "w0": w0, "eta": num(eta)},
                prompt_vi=(f"Mô hình y = wx được học từ các điểm {data} bằng hàm mất mát L(w) = tổng các (wx_i - y_i)^2. "
                           f"Từ w0 = {w0}, chạy một bước hạ gradient với bước học {num(eta)}. Nhập w1, rồi điểm cực tiểu "
                           "w* của L."),
                answer=nums([w1, wstar]),
                solution_vi=[f"L'(w) = 2 tổng x_i(wx_i - y_i) = 2(w . {sxx} - {paren(sxy)}), vì tổng x_i^2 = {sxx} và tổng "
                             f"x_i y_i = {sxy}.",
                             f"L'({w0}) = 2({w0} . {sxx} - {paren(sxy)}) = {grad}.",
                             f"w1 = {w0} - {num(eta)} . {paren(grad)} = {num(w1)}.",
                             f"L là parabol quay lên (lồi), cực tiểu khi L'(w) = 0: w* = {sxy}/{sxx} = {num(wstar)}."])
