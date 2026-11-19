"""Tối Ưu và Toán Rời Rạc, floor 8 (bài toán tối ưu, tập lồi và hàm lồi): generators. Ids
start with `tr_g8_`.

Everything is small and exact: quadratics in one or two variables, a quartic whose second
derivative has integer roots, a triangle with integer corners, three lines. The generators
work the way the floor teaches (closed formulas for the optimum of a fence or a box, the
signs of a 2 x 2 Hessian by its entries and its determinant, Cramer's rule for the stationary
point, barycentric weights from signed areas, the breakpoints of a maximum of lines);
tools/math_verify_tr_t7.py redoes each with sympy (diff and solve, the eigenvalues of the
Hessian, solveset of an inequality, a linear system, a linear programme)."""
from __future__ import annotations

import itertools
import random
from fractions import Fraction

from . import Draw, generator, num, nums, paren, vec_text


# ------------------------------------------------------------------ writing polynomials
def poly_text(terms) -> str:
    """[(coefficient, monomial), ...] as 2x^2 - xy + 3: zero terms dropped, signs merged."""
    out = []
    for coef, mono in terms:
        c = Fraction(coef)
        if c == 0:
            continue
        mag = abs(c)
        body = num(mag) if not mono else ("" if mag == 1 else (num(mag) if mag.denominator == 1 else f"({num(mag)})")) + mono
        if not out:
            out.append(("-" if c < 0 else "") + body)
        else:
            out.append(("- " if c < 0 else "+ ") + body)
    return " ".join(out) if out else "0"


def quad2_text(a, b, c, d=0, e=0, f0=0) -> str:
    return poly_text([(a, "x^2"), (b, "xy"), (c, "y^2"), (d, "x"), (e, "y"), (f0, "")])


def stationary(a, b, c, d, e) -> tuple[Fraction, Fraction]:
    """The point where 2ax + by + d = 0 and bx + 2cy + e = 0 (Cramer's rule)."""
    det = 4 * a * c - b * b
    return Fraction(-d * 2 * c + b * e, det), Fraction(-2 * a * e + b * d, det)


def quad2_value(a, b, c, d, e, x, y) -> Fraction:
    return a * x * x + b * x * y + c * y * y + d * x + e * y


# ------------------------------------------------------------------ phát biểu bài toán tối ưu
@generator("tr_g8_hang_rao")
def hang_rao(rng: random.Random) -> Draw:
    river = rng.random() < 0.5
    d = rng.randint(0, 3)
    L = rng.choice(range(12, 121, 4))
    k = d + 2
    x = Fraction(L, 2 * k)
    if river:
        y = Fraction(L, 2)
        area = Fraction(L * L, 4 * k)
        setting = (f"Một khu vườn hình chữ nhật nằm sát bờ sông; cạnh dọc bờ sông không cần rào. Ngoài ba cạnh còn "
                   f"lại, vườn được chia thành {d + 1} ô bằng {d} hàng rào song song với hai cạnh vuông góc bờ sông"
                   if d else "Một khu vườn hình chữ nhật nằm sát bờ sông; cạnh dọc bờ sông không cần rào, ba cạnh còn lại "
                   "được rào")
        constraint = f"{k}x + y = {L}"
        objective = f"S = x({L} - {k}x)"
    else:
        y = Fraction(L, 4)
        area = Fraction(L * L, 8 * k)
        setting = (f"Một khu vườn hình chữ nhật được rào cả bốn cạnh, và được chia thành {d + 1} ô bằng {d} hàng rào "
                   "song song với hai cạnh bên" if d else "Một khu vườn hình chữ nhật được rào cả bốn cạnh")
        constraint = f"{k}x + 2y = {L}"
        objective = f"S = x({L} - {k}x)/2"
    prompt = (f"{setting}. Tổng chiều dài rào là {L} mét. Gọi x là chiều dài mỗi cạnh bên (và mỗi hàng rào chia ô), y là "
              "chiều dài cạnh kia. Diện tích lớn nhất của khu vườn là bao nhiêu mét vuông?")
    return Draw(params={"river": river, "d": d, "L": L}, prompt_vi=prompt, answer=num(area),
                solution_vi=[f"Ràng buộc: {constraint}, với x > 0, y > 0. Hàm mục tiêu: diện tích S = xy.",
                             f"Thế y theo x: {objective}, một parabol quay xuống (hàm lõm).",
                             f"S'(x) = 0 cho x = {num(x)}; khi đó y = {num(y)}.",
                             f"Diện tích lớn nhất: {num(x)} . {num(y)} = {num(area)}."])


_EISENSTEIN = [(3, 8), (5, 8), (7, 15), (8, 15), (5, 21), (16, 21)]   # a^2 - ab + b^2 is a perfect square


@generator("tr_g8_hop")
def hop(rng: random.Random) -> Draw:
    a0, b0 = rng.choice(_EISENSTEIN)
    k = rng.choice([1, 2, 3]) if a0 * b0 < 100 else 1
    a, b = a0 * k, b0 * k
    if rng.random() < 0.5:
        a, b = b, a
    c = int(round((a * a - a * b + b * b) ** 0.5))
    x = Fraction(a + b - c, 6)
    vol = x * (a - 2 * x) * (b - 2 * x)
    return Draw(params={"a": a, "b": b},
                prompt_vi=(f"Từ một tấm bìa hình chữ nhật {a} x {b} (đơn vị dm), cắt ở bốn góc bốn hình vuông cạnh x "
                           "rồi gập lên thành một cái hộp không nắp. Nhập hai số: giá trị x làm thể tích hộp lớn nhất, "
                           "rồi thể tích lớn nhất đó."),
                answer=nums([x, vol]),
                solution_vi=[f"Thể tích V(x) = x({a} - 2x)({b} - 2x) với 0 < x < {num(Fraction(min(a, b), 2))}.",
                             f"V'(x) = 12x^2 - {4 * (a + b)}x + {a * b}.",
                             f"V'(x) = 0 cho x = ({a + b} - {c})/6 = {num(x)} hoặc x = ({a + b} + {c})/6 = "
                             f"{num(Fraction(a + b + c, 6))}; chỉ nghiệm thứ nhất nằm trong miền.",
                             "V liên tục, bằng 0 ở hai đầu miền và dương bên trong, nên điểm dừng duy nhất trong miền là "
                             "điểm lớn nhất.",
                             f"V({num(x)}) = {num(x)} . {paren(a - 2 * x)} . {paren(b - 2 * x)} = {num(vol)}."])


# ------------------------------------------------------------------ tập lồi
@generator("tr_g8_tap_muc")
def tap_muc(rng: random.Random) -> Draw:
    a = rng.choice([-3, -2, -1, 1, 2, 3])
    sign = rng.choice(["<=", ">="])
    roots = rng.random() < 0.75
    if roots:
        r1, r2 = sorted(rng.sample(range(-6, 7), 2))
        b, c = -a * (r1 + r2), a * r1 * r2
    else:
        h, q = rng.randint(-4, 4), rng.randint(1, 5)
        b, c = -2 * a * h, a * (h * h + q)
    if not roots and ((a > 0) == (sign == "<=")):        # the empty set: avoid it, flip the sign
        sign = ">=" if sign == "<=" else "<="
    text = poly_text([(a, "x^2"), (b, "x"), (c, "")])
    opens_up = a > 0
    if roots:
        inside = opens_up == (sign == "<=")          # the set is the closed interval between the roots
        ok = inside
        shape = (f"đoạn [{r1}, {r2}]" if inside else f"hợp hai nửa đường thẳng (-vô cùng, {r1}] và [{r2}, +vô cùng)")
        why = [f"Tam thức có hai nghiệm {r1} và {r2}, hệ số của x^2 là {a} "
               f"({'dương' if opens_up else 'âm'}).",
               f"Tập S là {shape}."]
        why.append("Một đoạn là tập lồi: khẳng định đúng." if ok else
                   f"S không lồi: {r1} và {r2} thuộc S nhưng trung điểm {num(Fraction(r1 + r2, 2))} của đoạn nối chúng "
                   "không thuộc S. Khẳng định sai.")
    else:
        ok = True
        why = ["Biệt thức âm nên tam thức luôn cùng dấu với hệ số của x^2.",
               "Vì vậy S là cả đường thẳng R, một tập lồi. Khẳng định đúng."]
    return Draw(params={"a": a, "b": b, "c": c, "sign": sign},
                prompt_vi=f"Cho S = {{x thuộc R : {text} {sign} 0}}. Khẳng định: S là một tập lồi.",
                answer=ok, solution_vi=["Trên đường thẳng, một tập là lồi khi và chỉ khi nó là một khoảng (đoạn, "
                                        "nửa đường thẳng, cả R, hay rỗng)."] + why)


def _area2(p, q, r) -> int:
    return (q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])


@generator("tr_g8_to_hop_loi")
def to_hop_loi(rng: random.Random) -> Draw:
    while True:
        pts = [(rng.randint(-4, 6), rng.randint(-4, 6)) for _ in range(3)]
        if _area2(*pts) != 0:
            break
    A, B, C = pts
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    P = (rng.randint(min(xs), max(xs)), rng.randint(min(ys), max(ys)))
    total = _area2(A, B, C)
    w = [Fraction(_area2(P, B, C), total), Fraction(_area2(A, P, C), total), Fraction(_area2(A, B, P), total)]
    inside = all(v >= 0 for v in w)
    return Draw(params={"A": list(A), "B": list(B), "C": list(C), "P": list(P)},
                prompt_vi=(f"Cho A{vec_text(A)}, B{vec_text(B)}, C{vec_text(C)} và P{vec_text(P)}. Tìm các số a, b, c "
                           "với a + b + c = 1 và P = aA + bB + cC; nhập a, b, c."),
                answer=nums(w),
                solution_vi=["Viết theo tọa độ: a + b + c = 1, "
                             f"{A[0]}a + {paren(B[0])}b + {paren(C[0])}c = {P[0]}, "
                             f"{A[1]}a + {paren(B[1])}b + {paren(C[1])}c = {P[1]}.",
                             "Giải hệ ba phương trình bậc nhất (ví dụ bằng quy tắc Cramer, mỗi hệ số là tỉ số hai diện "
                             "tích có dấu).",
                             f"a = {num(w[0])}, b = {num(w[1])}, c = {num(w[2])}.",
                             ("Cả ba hệ số đều không âm, nên P nằm trong tam giác ABC (bao lồi của A, B, C)."
                              if inside else "Có hệ số âm, nên P nằm ngoài tam giác ABC (bao lồi của A, B, C).")])


# ------------------------------------------------------------------ hàm lồi
@generator("tr_g8_hesse")
def hesse(rng: random.Random) -> Draw:
    want = rng.random() < 0.5
    while True:
        a, c = rng.randint(-2, 4), rng.randint(-2, 4)
        b = rng.randint(-6, 6)
        if a == 0 and b == 0 and c == 0:
            continue
        ok = a >= 0 and c >= 0 and 4 * a * c - b * b >= 0
        if ok == want:
            break
    d, e = rng.randint(-5, 5), rng.randint(-5, 5)
    det = 4 * a * c - b * b
    steps = [f"Ma trận Hesse là hằng số: H = [{2 * a}, {b}; {b}, {2 * c}].",
             "f lồi trên R^2 khi và chỉ khi H nửa xác định dương: hai phần tử chéo không âm và det H >= 0."]
    if a < 0 or c < 0:
        steps.append(f"Có phần tử chéo âm ({2 * a if a < 0 else 2 * c}), nên theo một trục tọa độ f là parabol quay "
                     "xuống: f không lồi. Khẳng định sai.")
    elif det < 0:
        steps.append(f"det H = {2 * a} . {2 * c} - {paren(b)}^2 = {det} < 0: H có một trị riêng âm, f không lồi. "
                     "Khẳng định sai.")
    else:
        steps.append(f"Phần tử chéo {2 * a}, {2 * c} không âm và det H = {det} >= 0, nên H nửa xác định dương và f lồi. "
                     "Khẳng định đúng.")
    return Draw(params={"a": a, "b": b, "c": c, "d": d, "e": e},
                prompt_vi=f"Cho f(x, y) = {quad2_text(a, b, c, d, e)}. Khẳng định: f là hàm lồi trên R^2.",
                answer=ok, solution_vi=steps)


@generator("tr_g8_khoang_lom")
def khoang_lom(rng: random.Random) -> Draw:
    r1, r2 = sorted(rng.sample(range(-4, 5), 2))
    A, B = -2 * (r1 + r2), 6 * r1 * r2
    C, D = rng.randint(-9, 9), rng.randint(-9, 9)
    f = poly_text([(1, "x^4"), (A, "x^3"), (B, "x^2"), (C, "x"), (D, "")])
    return Draw(params={"r1": r1, "r2": r2, "C": C, "D": D},
                prompt_vi=(f"Hàm f(x) = {f} lõm trên đúng một đoạn [p, q], và lồi trên (-vô cùng, p] cũng như trên "
                           "[q, +vô cùng). Nhập p, q."),
                answer=nums([r1, r2]),
                solution_vi=[f"f''(x) = {poly_text([(12, 'x^2'), (6 * A, 'x'), (2 * B, '')])} = "
                             f"12(x - {paren(r1)})(x - {paren(r2)}).",
                             f"f''(x) <= 0 đúng khi x nằm giữa hai nghiệm, tức trên [{r1}, {r2}]: ở đó f lõm.",
                             f"Ngoài đoạn đó f''(x) >= 0 nên f lồi. Đáp số: {r1}, {r2}."])


# ------------------------------------------------------------------ điều kiện tối ưu
def _definite(rng: random.Random) -> tuple[int, int, int]:
    while True:
        a, c, b = rng.randint(1, 4), rng.randint(1, 4), rng.randint(-5, 5)
        if 4 * a * c - b * b > 0:
            return a, b, c


@generator("tr_g8_diem_dung")
def diem_dung(rng: random.Random) -> Draw:
    while True:
        a, b, c = rng.randint(-3, 4), rng.randint(-5, 5), rng.randint(-3, 4)
        if a and c and 4 * a * c - b * b != 0:
            break
    d, e = rng.randint(-8, 8), rng.randint(-8, 8)
    x, y = stationary(a, b, c, d, e)
    return Draw(params={"a": a, "b": b, "c": c, "d": d, "e": e},
                prompt_vi=f"Tìm điểm dừng (x, y) của f(x, y) = {quad2_text(a, b, c, d, e)}; nhập x, y.",
                answer=nums([x, y]),
                solution_vi=[f"f_x = {poly_text([(2 * a, 'x'), (b, 'y'), (d, '')])}, "
                             f"f_y = {poly_text([(b, 'x'), (2 * c, 'y'), (e, '')])}.",
                             "Điểm dừng: giải hệ f_x = 0, f_y = 0 (hệ hai phương trình bậc nhất, định thức "
                             f"{2 * a} . {2 * c} - {paren(b)}^2 = {4 * a * c - b * b} khác 0 nên có đúng một nghiệm).",
                             f"Nghiệm: x = {num(x)}, y = {num(y)}."])


@generator("tr_g8_cuc_tieu")
def cuc_tieu(rng: random.Random) -> Draw:
    a, b, c = _definite(rng)
    d, e = rng.randint(-8, 8), rng.randint(-8, 8)
    if d == 0 and e == 0:
        d = rng.choice([-2, 2])
    x, y = stationary(a, b, c, d, e)
    value = quad2_value(a, b, c, d, e, x, y)
    return Draw(params={"a": a, "b": b, "c": c, "d": d, "e": e},
                prompt_vi=f"Tìm giá trị nhỏ nhất của f(x, y) = {quad2_text(a, b, c, d, e)} trên R^2.",
                answer=num(value),
                solution_vi=[f"H = [{2 * a}, {b}; {b}, {2 * c}] có {2 * a} > 0 và det H = {4 * a * c - b * b} > 0: xác "
                             "định dương, f lồi chặt, nên điểm dừng là cực tiểu toàn cục.",
                             f"Giải f_x = {poly_text([(2 * a, 'x'), (b, 'y'), (d, '')])} = 0, "
                             f"f_y = {poly_text([(b, 'x'), (2 * c, 'y'), (e, '')])} = 0: x = {num(x)}, y = {num(y)}.",
                             f"Giá trị nhỏ nhất f({num(x)}, {num(y)}) = {num(value)}."])


# ------------------------------------------------------------------ bài toán lồi
@generator("tr_g8_toan_cuc")
def toan_cuc(rng: random.Random) -> Draw:
    kind = rng.choice(["min", "min", "yen", "lech", "max"])
    if kind in ("min", "lech"):
        a, b, c = _definite(rng)
    elif kind == "max":
        a, b, c = (-v for v in _definite(rng))
    else:
        while True:
            a, b, c = rng.randint(-3, 3), rng.randint(-5, 5), rng.randint(-3, 3)
            if 4 * a * c - b * b < 0:
                break
    d, e = rng.randint(-8, 8), rng.randint(-8, 8)
    x, y = stationary(a, b, c, d, e)
    if kind == "lech":
        x, y = x + rng.choice([-1, 1]), y + rng.choice([-1, 0, 1])
    gx, gy = 2 * a * x + b * y + d, b * x + 2 * c * y + e
    det = 4 * a * c - b * b
    ok = kind == "min"
    steps = [f"Gradient tại ({num(x)}, {num(y)}): f_x = {num(gx)}, f_y = {num(gy)}.",
             f"Ma trận Hesse H = [{2 * a}, {b}; {b}, {2 * c}], det H = {det}."]
    if kind == "lech":
        steps.append("Gradient khác 0, nên điểm này không là điểm dừng, không thể là cực tiểu. Khẳng định sai.")
    elif kind == "yen":
        steps.append("Gradient bằng 0 nhưng det H < 0: H có một trị riêng dương và một trị riêng âm, điểm dừng là điểm "
                     "yên ngựa, không là cực tiểu. Khẳng định sai.")
    elif kind == "max":
        steps.append("Gradient bằng 0 nhưng H xác định âm (phần tử chéo âm, det H > 0): f lõm, đây là cực đại toàn cục, "
                     "không phải cực tiểu. Khẳng định sai.")
    else:
        steps.append("Gradient bằng 0 và H xác định dương (phần tử chéo dương, det H > 0): f lồi, nên điểm dừng là cực "
                     "tiểu toàn cục. Khẳng định đúng.")
    return Draw(params={"a": a, "b": b, "c": c, "d": d, "e": e, "x": num(x), "y": num(y)},
                prompt_vi=(f"Cho f(x, y) = {quad2_text(a, b, c, d, e)}. Khẳng định: điểm ({num(x)}, {num(y)}) là "
                           "điểm cực tiểu toàn cục của f trên R^2."),
                answer=ok, solution_vi=steps)


@generator("tr_g8_max_duong")
def max_duong(rng: random.Random) -> Draw:
    while True:
        slopes = [rng.randint(-4, -1), rng.randint(-3, 3), rng.randint(1, 4)]
        lines = [(s, rng.randint(-8, 8)) for s in slopes]
        if len({l for l in lines}) == 3 and len(set(slopes)) == 3:
            break
    cands = []
    for (a1, b1), (a2, b2) in itertools.combinations(lines, 2):
        x = Fraction(b2 - b1, a1 - a2)
        cands.append((max(a * x + b for a, b in lines), x))
    value, xbest = min(cands)
    text = ", ".join(poly_text([(a, "x"), (b, "")]) for a, b in lines)
    return Draw(params={"lines": [list(l) for l in lines]},
                prompt_vi=f"Cho f(x) = max({text}). Tìm giá trị nhỏ nhất của f trên R.",
                answer=num(value),
                solution_vi=["f là cực đại của các hàm tuyến tính nên là hàm lồi, tuyến tính từng khúc; nó có hệ số góc "
                             "âm và dương nên đạt giá trị nhỏ nhất tại một điểm gãy.",
                             "Điểm gãy nằm ở giao điểm của hai đường; tính f tại các giao điểm: "
                             + "; ".join(f"x = {num(x)}: f = {num(v)}" for v, x in cands) + ".",
                             f"Giá trị nhỏ nhất là {num(value)} (tại x = {num(xbest)})."])
