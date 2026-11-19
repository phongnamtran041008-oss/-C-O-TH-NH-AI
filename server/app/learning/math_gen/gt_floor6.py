"""Giải Tích, tầng 6 (đơn điệu, cực trị, lồi lõm, tiệm cận, khảo sát): generators. Ids
start with `gt_g6_`.

Most questions use a cubic built from its two critical points r < s:
f(x) = k(2x^3 - 3(r + s)x^2 + 6rs x) + d has f'(x) = 6k(x - r)(x - s), so every critical
point, extreme value and interval is a whole number or a fraction. Convexity follows the
library's convention: lồi where f'' > 0 (the graph bends upward), lõm where f'' < 0."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, linear_text, nonzero, num, nums, paren
from .gt_floor1 import factor_text, poly_text, value_at


def _cubic(k: int, r: int, s: int, d: int) -> list[int]:
    return [2 * k, -3 * k * (r + s), 6 * k * r * s, d]


def _crit_cubic(rng: random.Random, lo: int = -4, hi: int = 4) -> tuple[int, int]:
    r, s = sorted(rng.sample(range(lo, hi + 1), 2))
    return r, s


def _fprime_text(k: int, r: int, s: int) -> str:
    return f"{6 * k}{factor_text(r)}{factor_text(s)}"


def _factored(lead: int, mult: dict) -> str:
    """lead . x^a (x - r)^b ...: the factor x first, a power only when the root is repeated."""
    parts = []
    for v in sorted(mult, key=lambda v: (v != 0, v)):
        base = "x" if v == 0 else factor_text(v)
        parts.append(base if mult[v] == 1 else f"{base}^{mult[v]}")
    return f"{lead}" + "".join(parts)


# ------------------------------------------------------------------ đơn điệu
@generator("gt_g6_don_dieu")
def don_dieu(rng: random.Random) -> Draw:
    r, s = _crit_cubic(rng)
    k = rng.choice([-1, 1])
    d = rng.randint(-5, 5)
    coeffs = _cubic(k, r, s, d)
    ask = "nghịch biến" if k > 0 else "đồng biến"
    other = "đồng biến" if k > 0 else "nghịch biến"
    return Draw(
        params={"coeffs": coeffs, "k": k},
        prompt_vi=(f"Hàm f(x) = {poly_text(coeffs)} {ask} trên một đoạn [a, b] và {other} trên mỗi khoảng còn lại "
                   "của R. Nhập a, b theo đúng thứ tự."),
        answer=nums([r, s]),
        solution_vi=[f"f'(x) = {poly_text([6 * k, -6 * k * (r + s), 6 * k * r * s])} = {_fprime_text(k, r, s)}.",
                     f"f'(x) = 0 tại x = {r} và x = {s}.",
                     f"Hệ số {6 * k} {'dương' if k > 0 else 'âm'} nên f' {'âm' if k > 0 else 'dương'} giữa hai nghiệm "
                     f"và {'dương' if k > 0 else 'âm'} ở ngoài.",
                     f"f {ask} trên [{r}, {s}]: a = {r}, b = {s}."])


@generator("gt_g6_dong_bien_tf")
def dong_bien_tf(rng: random.Random) -> Draw:
    b = rng.randint(-4, 4)
    m = rng.randint(-6, 8)
    # f(x) = x^3 + b x^2 + m x + 1, f'(x) = 3x^2 + 2b x + m >= 0 for all x iff 4b^2 - 12m <= 0
    ok = b * b <= 3 * m
    coeffs = [1, b, m, 1]
    disc = 4 * b * b - 12 * m
    steps = [f"f'(x) = {poly_text([3, 2 * b, m])}, một tam thức bậc hai có hệ số x^2 dương.",
             "f đồng biến trên R khi f'(x) >= 0 với mọi x, tức biệt thức của tam thức f'(x) không dương.",
             f"Biệt thức = {paren(2 * b)}^2 - 4 . 3 . {paren(m)} = {disc}."]
    steps.append("Biệt thức <= 0 nên f' không âm (chỉ bằng 0 tại nhiều nhất một điểm): f đồng biến trên R, mệnh đề đúng."
                 if ok else "Biệt thức > 0 nên f' âm giữa hai nghiệm của nó: f không đồng biến trên R, mệnh đề sai.")
    return Draw(params={"coeffs": coeffs},
                prompt_vi=f"Hàm f(x) = {poly_text(coeffs)} đồng biến trên R.",
                answer=ok, solution_vi=steps)


# ------------------------------------------------------------------ cực trị
@generator("gt_g6_cuc_tri")
def cuc_tri(rng: random.Random) -> Draw:
    r, s = _crit_cubic(rng)
    k = rng.choice([-1, 1])
    d = rng.randint(-5, 5)
    coeffs = _cubic(k, r, s, d)
    ask = rng.choice(["cực đại", "cực tiểu"])
    # k > 0: maximum at r, minimum at s; k < 0 the other way round
    at = (r if ask == "cực đại" else s) if k > 0 else (s if ask == "cực đại" else r)
    value = value_at(coeffs, at)
    return Draw(
        params={"coeffs": coeffs, "ask": ask},
        prompt_vi=f"Tìm giá trị {ask} của hàm số f(x) = {poly_text(coeffs)}.",
        answer=num(value),
        solution_vi=[f"f'(x) = {_fprime_text(k, r, s)}, bằng 0 tại x = {r} và x = {s}.",
                     f"Hệ số {6 * k} {'dương' if k > 0 else 'âm'}: f' đổi dấu từ "
                     f"{'+ sang - tại ' + str(r) + ' và từ - sang + tại ' + str(s) if k > 0 else '- sang + tại ' + str(r) + ' và từ + sang - tại ' + str(s)}.",
                     f"Điểm {ask} là x = {at}; giá trị {ask} f({at}) = {num(value)}."])


@generator("gt_g6_so_cuc_tri")
def so_cuc_tri(rng: random.Random) -> Draw:
    k = rng.choice([-1, 1])
    r, s = rng.randint(-3, 3), rng.randint(-3, 3)
    # f'(x) = 12k x (x - r)(x - s): f = k(3x^4 - 4(r + s)x^3 + 6rs x^2)
    coeffs = [3 * k, -4 * k * (r + s), 6 * k * r * s, 0, 0]
    roots = [0, r, s]
    mult = {v: roots.count(v) for v in roots}
    extrema = sorted(v for v, c in mult.items() if c % 2 == 1)
    lines = [f"f'(x) = {poly_text([12 * k, -12 * k * (r + s), 12 * k * r * s, 0])} = {_factored(12 * k, mult)}.",
             "f' đổi dấu khi đi qua một nghiệm bội lẻ, không đổi dấu qua một nghiệm bội chẵn.",
             "Bội của các nghiệm: " + ", ".join(f"x = {v} bội {c}" for v, c in sorted(mult.items())) + "."]
    lines.append(f"Số điểm cực trị: {len(extrema)}.")
    return Draw(
        params={"coeffs": coeffs},
        prompt_vi=f"Hàm số f(x) = {poly_text(coeffs)} có bao nhiêu điểm cực trị?",
        answer=str(len(extrema)), solution_vi=lines)


# ------------------------------------------------------------------ GTLN, GTNN
@generator("gt_g6_gtln")
def gtln(rng: random.Random) -> Draw:
    r, s = _crit_cubic(rng, -3, 3)
    d = rng.randint(-5, 5)
    coeffs = _cubic(1, r, s, d)
    u = rng.randint(-4, r)
    v = rng.randint(max(u + 1, r), 4)
    cands = [u, v] + [c for c in (r, s) if u < c < v]
    values = {c: value_at(coeffs, c) for c in cands}
    hi, lo = max(values.values()), min(values.values())
    return Draw(
        params={"coeffs": coeffs, "u": u, "v": v},
        prompt_vi=(f"Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = {poly_text(coeffs)} trên đoạn [{u}, {v}]. "
                   "Nhập GTLN rồi GTNN."),
        answer=nums([hi, lo]),
        solution_vi=[f"f'(x) = {_fprime_text(1, r, s)}, bằng 0 tại x = {r} và x = {s}.",
                     "Điểm tới hạn nằm trong khoảng (" + f"{u}, {v}): "
                     + (", ".join(str(c) for c in cands[2:]) if cands[2:] else "không có") + ".",
                     "So các giá trị tại điểm tới hạn và hai đầu đoạn: "
                     + ", ".join(f"f({c}) = {num(values[c])}" for c in sorted(values)) + ".",
                     f"GTLN = {num(hi)}, GTNN = {num(lo)}."])


@generator("gt_g6_x_nghich")
def x_nghich(rng: random.Random) -> Draw:
    a = rng.randint(1, 4)
    u = rng.randint(1, 5)
    v = rng.randint(u + 1, 7)
    m = a * a
    f = {c: c + Fraction(m, c) for c in (u, v)}
    inside = u < a < v
    if inside:
        f[a] = Fraction(2 * a)
    hi, lo = max(f.values()), min(f.values())
    return Draw(
        params={"m": m, "u": u, "v": v},
        prompt_vi=(f"Tìm giá trị lớn nhất và giá trị nhỏ nhất của f(x) = x + {m}/x trên đoạn [{u}, {v}]. "
                   "Nhập GTLN rồi GTNN."),
        answer=nums([hi, lo]),
        solution_vi=[f"f'(x) = 1 - {m}/x^2 = (x^2 - {m}) / x^2, bằng 0 tại x = {a} (xét x > 0).",
                     (f"x = {a} nằm trong ({u}, {v}): f({a}) = {2 * a}." if inside else
                      f"x = {a} không nằm trong ({u}, {v}): f đơn điệu trên đoạn."),
                     "Hai đầu đoạn: " + ", ".join(f"f({c}) = {num(f[c])}" for c in (u, v)) + ".",
                     f"GTLN = {num(hi)}, GTNN = {num(lo)}."])


# ------------------------------------------------------------------ lồi, lõm, điểm uốn
@generator("gt_g6_diem_uon")
def diem_uon(rng: random.Random) -> Draw:
    a = nonzero(rng, -2, 2)
    x0 = rng.randint(-3, 3)
    b = -3 * a * x0
    c, d = rng.randint(-6, 6), rng.randint(-6, 6)
    coeffs = [a, b, c, d]
    y0 = value_at(coeffs, x0)
    return Draw(
        params={"coeffs": coeffs},
        prompt_vi=f"Tìm điểm uốn (x0, y0) của đồ thị y = {poly_text(coeffs)}. Nhập x0, y0 theo đúng thứ tự.",
        answer=nums([x0, y0]),
        solution_vi=[f"y' = {poly_text([3 * a, 2 * b, c])}, y'' = {poly_text([6 * a, 2 * b])}.",
                     f"y'' = 0 tại x = {x0}, và y'' là hàm bậc nhất nên đổi dấu qua {x0}.",
                     f"y({x0}) = {num(y0)}: điểm uốn ({x0}, {num(y0)})."])


@generator("gt_g6_uon_tf")
def uon_tf(rng: random.Random) -> Draw:
    b, c = rng.randint(-4, 4), rng.randint(-4, 6)
    # f = x^4 + b x^3 + c x^2: f'' = 12x^2 + 6b x + 2c changes sign iff 36b^2 - 96c > 0
    disc = 36 * b * b - 96 * c
    has = disc > 0
    claim = rng.choice(["có hai điểm uốn", "không có điểm uốn nào"])
    ok = has if claim == "có hai điểm uốn" else not has
    coeffs = [1, b, c, 0, 0]
    steps = [f"f''(x) = {poly_text([12, 6 * b, 2 * c])}, tam thức bậc hai có biệt thức "
             f"{paren(6 * b)}^2 - 4 . 12 . {paren(2 * c)} = {disc}.",
             ("Biệt thức dương: f'' có hai nghiệm phân biệt và đổi dấu qua cả hai, nên đồ thị có hai điểm uốn."
              if has else
              "Biệt thức <= 0: f'' không đổi dấu (nghiệm kép, nếu có, không làm đổi dấu), nên đồ thị không có điểm uốn.")]
    steps.append("Mệnh đề đúng." if ok else "Mệnh đề sai.")
    return Draw(params={"coeffs": coeffs, "claim": claim},
                prompt_vi=f"Đồ thị của f(x) = {poly_text(coeffs)} {claim}.",
                answer=ok, solution_vi=steps)


# ------------------------------------------------------------------ tiệm cận
@generator("gt_g6_tiem_can")
def tiem_can(rng: random.Random) -> Draw:
    while True:
        a, b = nonzero(rng, -5, 5), rng.randint(-6, 6)
        c, d = nonzero(rng, -3, 3), rng.randint(-6, 6)
        if a * d - b * c != 0:
            break
    x0, y0 = Fraction(-d, c), Fraction(a, c)
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d},
        prompt_vi=(f"Đồ thị y = ({linear_text(a, b)}) / ({linear_text(c, d)}) có tiệm cận đứng x = x0 và tiệm cận "
                   "ngang y = y0. Nhập x0, y0 theo đúng thứ tự."),
        answer=nums([x0, y0]),
        solution_vi=[f"Mẫu bằng 0 tại x = {num(x0)}, còn tử tại đó khác 0 (vì {a} . {paren(d)} - {paren(b)} . "
                     f"{paren(c)} khác 0), nên y -> vô cùng: tiệm cận đứng x = {num(x0)}.",
                     f"Khi x -> vô cùng, y -> {a} / {paren(c)} = {num(y0)}: tiệm cận ngang y = {num(y0)}.",
                     f"Đáp án: {num(x0)}, {num(y0)}."])


@generator("gt_g6_tiem_can_xien")
def tiem_can_xien(rng: random.Random) -> Draw:
    while True:
        a, b, c = nonzero(rng, -3, 3), rng.randint(-5, 5), rng.randint(-6, 6)
        d = rng.randint(-4, 4)
        rem = a * d * d + b * d + c
        if rem != 0:
            break
    p, q = a, b + a * d
    top = [a, b, c]
    return Draw(
        params={"top": top, "d": d},
        prompt_vi=(f"Đồ thị y = ({poly_text(top)}) / ({linear_text(1, -d)}) có tiệm cận xiên y = px + q. "
                   "Nhập p, q theo đúng thứ tự."),
        answer=nums([p, q]),
        solution_vi=[f"Chia đa thức: {poly_text(top)} = ({linear_text(1, -d)})({linear_text(p, q)}) + {paren(rem)}.",
                     f"Nên y = {linear_text(p, q)} + {paren(rem)} / ({linear_text(1, -d)}).",
                     f"Phần {paren(rem)} / ({linear_text(1, -d)}) -> 0 khi x -> vô cùng: tiệm cận xiên "
                     f"y = {linear_text(p, q)}.",
                     f"p = {p}, q = {q}."])


# ------------------------------------------------------------------ khảo sát
@generator("gt_g6_so_nghiem")
def so_nghiem(rng: random.Random) -> Draw:
    r, s = _crit_cubic(rng, -3, 3)
    coeffs = _cubic(1, r, s, 0)
    big, small = value_at(coeffs, r), value_at(coeffs, s)      # maximum at r, minimum at s
    m = rng.choice([big, small, rng.randint(int(small) - 3, int(big) + 3)])
    if m > big or m < small:
        count = 1
    elif m == big or m == small:
        count = 2
    else:
        count = 3
    return Draw(
        params={"coeffs": coeffs, "m": int(m)},
        prompt_vi=f"Phương trình {poly_text(coeffs)} = {num(m)} có bao nhiêu nghiệm thực phân biệt?",
        answer=str(count),
        solution_vi=[f"Đặt f(x) = {poly_text(coeffs)}: f'(x) = {_fprime_text(1, r, s)}.",
                     f"f tăng trên (-vô cùng, {r}], giảm trên [{r}, {s}], tăng trên [{s}, +vô cùng); "
                     f"cực đại f({r}) = {num(big)}, cực tiểu f({s}) = {num(small)}.",
                     "Số nghiệm là số giao điểm của đồ thị với đường ngang y = m: 3 khi m nằm giữa hai giá trị cực trị, "
                     "2 khi m bằng một trong hai, 1 khi m nằm ngoài.",
                     f"Với m = {num(m)}: {count} nghiệm."])
