"""Giải Tích, tầng 10 (Tài Năng: số thực, giới hạn trên và dưới, khả tích Riemann, hàm lồi, không gian metric):
generators.

Everything is exact (whole numbers and fractions). A set of reals is given by a formula whose sup and inf a learner can
read off; a sequence is built so that every subsequence limit is a whole number; the Darboux sums are taken for a monotone
function on a partition with rational end points; a Jensen gap is a difference of two rational numbers.
tools/math_verify_gt_t10.py recomputes each answer another way: sup and inf as the larger and smaller of the first term
and the sympy limit of a monotone sequence (or of an interval), limsup and liminf as the extreme sympy limits of the
subsequences n = k m + r, the Darboux sums by sympy's maximum and minimum of f on each sub-interval, the convexity point
by solving f'' = 0, the Jensen gap from the two sides of the inequality, vector norms by sympy's Matrix.norm, and the
verdict on a candidate metric by a search for a violated axiom over a grid of exact rationals."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, num, paren


def _signed(c: int, body: str, first: bool = False) -> str:
    """c * body written the usual way: 3x, -x, 4 (body '' for the constant)."""
    mag = abs(c)
    text = str(mag) if body == "" else (body if mag == 1 else f"{mag}{body}")
    if first:
        return ("-" if c < 0 else "") + text
    return f" {'+' if c > 0 else '-'} {text}"


# ------------------------------------------------------------------ cận trên đúng và cận dưới đúng
@generator("gt_g10_sup_inf")
def sup_inf(rng: random.Random) -> Draw:
    kind = rng.choice(["a_cong_b_n", "a_cong_b_n", "khoang", "n_tren_n_cong_m"])
    ask = rng.choice(["sup", "inf"])
    if kind == "a_cong_b_n":
        a = rng.randint(-3, 5)
        b = rng.choice([v for v in range(-6, 7) if v])
        text = f"{{{a} {'+' if b > 0 else '-'} {abs(b)}/n : n = 1, 2, 3, ...}}"
        first, limit = Fraction(a + b), Fraction(a)
        sup, inf = (first, limit) if b > 0 else (limit, first)
        attained_sup, attained_inf = b > 0, b < 0
        why = (f"Dãy {a} {'+' if b > 0 else '-'} {abs(b)}/n {'giảm' if b > 0 else 'tăng'} dần theo n: số hạng đầu (n = 1) là {a + b}, "
               f"và giới hạn khi n lớn là {a} (không bao giờ đạt được vì {abs(b)}/n khác 0).")
    elif kind == "khoang":
        c = rng.randint(-4, 5)
        d = rng.randint(1, 6)
        text = f"{{x thuộc R : |x - {c}| < {d}}}" if c >= 0 else f"{{x thuộc R : |x + {-c}| < {d}}}"
        sup, inf = Fraction(c + d), Fraction(c - d)
        attained_sup = attained_inf = False
        why = f"|x - ({c})| < {d} nghĩa là {c - d} < x < {c + d}: một khoảng mở."
    else:
        m = rng.randint(1, 6)
        text = f"{{n/(n + {m}) : n = 1, 2, 3, ...}}"
        sup, inf = Fraction(1), Fraction(1, 1 + m)
        attained_sup, attained_inf = False, True
        why = (f"n/(n + {m}) = 1 - {m}/(n + {m}) tăng dần theo n: số hạng đầu (n = 1) là 1/{1 + m}, và tiến tới 1 từ dưới "
               f"(không bao giờ bằng 1).")
    ans = sup if ask == "sup" else inf
    attained = attained_sup if ask == "sup" else attained_inf
    note = ("giá trị này thuộc tập (là max)" if attained and ask == "sup" else
            "giá trị này thuộc tập (là min)" if attained else "giá trị này không thuộc tập, nhưng vẫn là cận đúng")
    prompt = (f"Tập A = {text}. Tìm {'cận trên đúng sup' if ask == 'sup' else 'cận dưới đúng inf'} A. "
              f"Nhập một số hoặc phân số tối giản.")
    return Draw(params={"kind": kind, "ask": ask, "a": a if kind == "a_cong_b_n" else 0, "b": b if kind == "a_cong_b_n" else 0,
                        "c": c if kind == "khoang" else 0, "d": d if kind == "khoang" else 0,
                        "m": m if kind == "n_tren_n_cong_m" else 0},
                prompt_vi=prompt, answer=num(ans),
                solution_vi=[why, f"{'sup' if ask == 'sup' else 'inf'} A = {num(ans)} ({note})."])


# ------------------------------------------------------------------ giới hạn trên và giới hạn dưới
@generator("gt_g10_gioi_han_tren")
def gioi_han_tren(rng: random.Random) -> Draw:
    kind = rng.choice(["dau", "chu_ky"])
    ask = rng.choice(["limsup", "liminf"])
    if kind == "dau":
        a = rng.randint(-3, 5)
        b = rng.choice([v for v in range(-5, 6) if v])
        head = "a_n = " + (str(a) if a else "") + _signed(b, "(-1)^n (1 + 1/n)", first=not a)
        hi, lo = a + abs(b), a - abs(b)
        sol = [f"Dãy con chỉ số chẵn: a_(2k) = {a} + ({b})(1 + 1/(2k)) tiến tới {a + b}. Dãy con chỉ số lẻ: a_(2k+1) = {a} - ({b})(1 + 1/(2k+1)) tiến tới {a - b}.",
               f"Chỉ có hai giới hạn dãy con: {a + b} và {a - b}; lớn nhất là {hi}, nhỏ nhất là {lo}."]
        params = {"kind": kind, "ask": ask, "a": a, "b": b, "u": [0, 0, 0]}
    else:
        u = [rng.randint(-4, 6) for _ in range(3)]
        while len(set(u)) < 2:
            u = [rng.randint(-4, 6) for _ in range(3)]
        head = (f"a_n = {u[1]} + 1/n nếu n chia 3 dư 1, a_n = {u[2]} + 1/n nếu n chia 3 dư 2, a_n = {u[0]} + 1/n nếu n chia hết cho 3")
        hi, lo = max(u), min(u)
        sol = [f"Ba dãy con theo số dư của n khi chia cho 3 có giới hạn {u[1]}, {u[2]}, {u[0]} (vì 1/n tiến tới 0).",
               f"Mọi số hạng thuộc một trong ba dãy con đó, nên các giới hạn dãy con chỉ là {sorted(set(u))}; lớn nhất là {hi}, nhỏ nhất là {lo}."]
        params = {"kind": kind, "ask": ask, "a": 0, "b": 0, "u": u}
    ans = hi if ask == "limsup" else lo
    what = "giới hạn trên limsup" if ask == "limsup" else "giới hạn dưới liminf"
    return Draw(params=params,
                prompt_vi=f"Dãy {head}, n = 1, 2, 3, ... Tìm {what} của a_n, tức giới hạn {'lớn' if ask == 'limsup' else 'nhỏ'} nhất của các dãy con hội tụ. Nhập một số.",
                answer=str(ans), solution_vi=sol + [f"{ask} a_n = {ans}."])


# ------------------------------------------------------------------ tổng Darboux
@generator("gt_g10_tong_darboux")
def tong_darboux(rng: random.Random) -> Draw:
    kind = rng.choice(["tuyen_tinh_tang", "tuyen_tinh_giam", "binh_phuong", "lap_phuong"])
    top = rng.randint(2, 6)
    cuts = sorted(rng.sample(range(1, top), rng.randint(1, min(3, top - 1))))
    pts = [0] + cuts + [top]
    ask = rng.choice(["U", "L", "U_tru_L"])
    a = rng.randint(1, 4)
    b = rng.randint(0, 5)
    if kind == "tuyen_tinh_tang":
        f, name, inc = (lambda x: a * x + b), "f(x) = " + (f"{a}x" if a != 1 else "x") + (f" + {b}" if b else ""), True
    elif kind == "tuyen_tinh_giam":
        b = rng.randint(a * top, a * top + 6)
        f, name, inc = (lambda x: b - a * x), f"f(x) = {b} - " + (f"{a}x" if a != 1 else "x"), False
    elif kind == "binh_phuong":
        f, name, inc = (lambda x: x * x), "f(x) = x^2", True
    else:
        f, name, inc = (lambda x: x ** 3), "f(x) = x^3", True
    hi = (lambda lo_, hi_: f(hi_)) if inc else (lambda lo_, hi_: f(lo_))        # the sup on [lo_, hi_]
    lo = (lambda lo_, hi_: f(lo_)) if inc else (lambda lo_, hi_: f(hi_))         # the inf
    segs = list(zip(pts, pts[1:]))
    U = sum(hi(p, q) * (q - p) for p, q in segs)
    L = sum(lo(p, q) * (q - p) for p, q in segs)
    ans = {"U": U, "L": L, "U_tru_L": U - L}[ask]
    side = "mút phải" if inc else "mút trái"
    other = "mút trái" if inc else "mút phải"
    sol = [f"{name} {'tăng' if inc else 'giảm'} trên [0, {top}], nên trên mỗi đoạn con sup lấy ở {side} và inf ở {other}.",
           "Trên các đoạn con " + ", ".join(f"[{p}, {q}]" for p, q in segs) + ": sup = " + ", ".join(str(hi(p, q)) for p, q in segs)
           + "; inf = " + ", ".join(str(lo(p, q)) for p, q in segs) + ".",
           f"U = " + " + ".join(f"{hi(p, q)} . {q - p}" for p, q in segs) + f" = {U}; L = " + " + ".join(f"{lo(p, q)} . {q - p}" for p, q in segs) + f" = {L}."]
    if ask == "U_tru_L":
        sol.append(f"U - L = {U} - {L} = {U - L}.")
    prompt = (f"{name} trên [0, {top}], phân hoạch P = {{{', '.join(map(str, pts))}}}. Tính "
              f"{'tổng Darboux trên U(f, P)' if ask == 'U' else 'tổng Darboux dưới L(f, P)' if ask == 'L' else 'U(f, P) - L(f, P)'}"
              f" (U = tổng của sup f trên mỗi đoạn con x độ dài đoạn con, L tương tự với inf). Nhập một số.")
    return Draw(params={"kind": kind, "top": top, "pts": pts, "ask": ask, "a": a, "b": b}, prompt_vi=prompt,
                answer=str(ans), solution_vi=sol)


# ------------------------------------------------------------------ hàm lồi
@generator("gt_g10_diem_uon_so")
def diem_uon_so(rng: random.Random) -> Draw:
    a = rng.choice([1, 2, 3])
    b = rng.randint(-9, 9)
    c = rng.randint(-6, 6)
    d = rng.randint(-5, 5)
    f = "f(x) = " + _signed(a, "x^3", first=True)
    for coef, body in ((b, "x^2"), (c, "x"), (d, "")):
        if coef:
            f += _signed(coef, body)
    x0 = Fraction(-b, 3 * a)
    return Draw(params={"a": a, "b": b, "c": c, "d": d},
                prompt_vi=f"{f}. Tìm số x0 nhỏ nhất sao cho f là hàm lồi (f'' >= 0) trên [x0, +vô cùng). Nhập một số hoặc phân số tối giản.",
                answer=num(x0),
                solution_vi=[f"f''(x) = {6 * a}x" + (f" + {2 * b}" if b > 0 else f" - {-2 * b}" if b < 0 else "") + ".",
                             f"f''(x) >= 0 khi x >= {num(x0)} (nghiệm của f'' = 0, vì hệ số {6 * a} dương). Vậy x0 = {num(x0)}, hoành độ điểm uốn."])


@generator("gt_g10_jensen_hieu")
def jensen_hieu(rng: random.Random) -> Draw:
    power = rng.choice([2, 2, 3, 4])
    lam = rng.choice([Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(2, 3), Fraction(3, 4), Fraction(1, 5)])
    x, y = sorted(rng.sample(range(1, 8), 2))
    f = lambda t: Fraction(t) ** power              # noqa: E731
    mid = lam * x + (1 - lam) * y
    lhs, rhs = f(mid), lam * f(x) + (1 - lam) * f(y)
    domain = "R" if power % 2 == 0 else "[0, +vô cùng)"
    return Draw(params={"power": power, "lam": num(lam), "x": x, "y": y},
                prompt_vi=f"Hàm f(x) = x^{power} lồi trên {domain}. Với x = {x}, y = {y} và hệ số l = {num(lam)}, tính hiệu "
                          f"l f(x) + (1 - l) f(y) - f(l x + (1 - l) y), vế phải trừ vế trái của bất đẳng thức Jensen. Nhập một số hoặc phân số tối giản.",
                answer=num(rhs - lhs),
                solution_vi=[f"l x + (1 - l) y = {num(lam)} . {x} + {num(1 - lam)} . {y} = {num(mid)}, nên f(l x + (1 - l) y) = {num(lhs)}.",
                             f"l f(x) + (1 - l) f(y) = {num(lam)} . {x ** power} + {num(1 - lam)} . {y ** power} = {num(rhs)}.",
                             f"Hiệu = {num(rhs)} - {num(lhs)} = {num(rhs - lhs)}, không âm đúng như Jensen cho hàm lồi."])


# ------------------------------------------------------------------ chuẩn và khoảng cách trong R^n
PYTHAGOREAN = ((3, 4, 0), (5, 12, 0), (8, 6, 0), (1, 2, 2), (2, 3, 6), (2, 6, 9), (1, 4, 8), (4, 4, 7), (3, 4, 12), (6, 6, 7),
               (2, 10, 11), (4, 8, 8), (9, 12, 0))


@generator("gt_g10_chuan_vecto")
def chuan_vecto(rng: random.Random) -> Draw:
    which = rng.choice(["d1", "d2", "dinf"])
    k = rng.choice([2, 3])
    trip = list(rng.choice([t for t in PYTHAGOREAN if k == 3 or 0 in t]))
    if k == 2:
        trip = [v for v in trip if v][:2] if 0 in trip else trip[:2]
        if len(trip) < 2:
            trip = [3, 4]
    rng.shuffle(trip)
    diff = [t * rng.choice([-1, 1]) for t in trip[:k]]
    u = [rng.randint(-5, 5) for _ in range(k)]
    v = [a - d for a, d in zip(u, diff)]                   # u - v = diff
    vec = lambda t: "(" + ", ".join(map(str, t)) + ")"      # noqa: E731
    if which == "d1":
        ans = sum(abs(d) for d in diff)
        name, rule = "d_1 (tổng |u_i - v_i|)", f"{' + '.join(str(abs(d)) for d in diff)} = {ans}"
    elif which == "dinf":
        ans = max(abs(d) for d in diff)
        name, rule = "d_inf (lớn nhất |u_i - v_i|)", f"lớn nhất của {', '.join(str(abs(d)) for d in diff)} là {ans}"
    else:
        sq = sum(d * d for d in diff)
        ans = round(sq ** 0.5)
        assert ans * ans == sq
        name, rule = "d_2 (khoảng cách Euclid)", f"sqrt({' + '.join(str(d * d) for d in diff)}) = sqrt({sq}) = {ans}"
    return Draw(params={"u": u, "v": v, "which": which},
                prompt_vi=f"Trong R^{k}, tính khoảng cách {name} giữa u = {vec(u)} và v = {vec(v)}. Nhập một số.",
                answer=str(ans),
                solution_vi=[f"u - v = {vec(diff)}.", f"{which} = {rule}."])


# ------------------------------------------------------------------ có phải khoảng cách không
METRICS = (
    ("|x - y|", True, "Đây là khoảng cách thông thường trên R."),
    ("(x - y)^2", False, "Vi phạm bất đẳng thức tam giác: d(0, 2) = 4 > d(0, 1) + d(1, 2) = 2."),
    ("|x^2 - y^2|", False, "Bằng 0 với x = 1, y = -1 dù x khác y."),
    ("|x - y|/(1 + |x - y|)", True, "Không âm, bằng 0 khi x = y, đối xứng, và thoả bất đẳng thức tam giác (t -> t/(1 + t) tăng và g(s + t) <= g(s) + g(t))."),
    ("min(|x - y|, 1)", True, "Cắt khoảng cách thông thường ở 1; vẫn thoả mọi tiên đề (min của hai metric-hàm giữ bất đẳng thức tam giác nhờ min(s + t, 1) <= min(s, 1) + min(t, 1))."),
    ("sqrt(|x - y|)", True, "Căn bậc hai là hàm tăng, g(s + t) <= g(s) + g(t), nên d vẫn thoả bất đẳng thức tam giác."),
    ("2|x - y|", True, "Bội dương của khoảng cách thông thường vẫn là khoảng cách."),
    ("|x - y|^3", False, "Vi phạm bất đẳng thức tam giác: d(0, 2) = 8 > d(0, 1) + d(1, 2) = 2."),
    ("max(x - y, 0)", False, "Không đối xứng: d(1, 0) = 1 nhưng d(0, 1) = 0; cũng bằng 0 khi x < y dù x khác y."),
    ("|x^3 - y^3|", True, "x -> x^3 là đơn ánh, nên |f(x) - f(y)| vẫn bằng 0 chỉ khi x = y; các tiên đề còn lại thừa hưởng từ |.|."),
)


@generator("gt_g10_metric_tf")
def metric_tf(rng: random.Random) -> Draw:
    k = rng.randrange(len(METRICS))
    text, truth, why = METRICS[k]
    return Draw(params={"k": k, "text": text},
                prompt_vi=f"d(x, y) = {text} là một khoảng cách (metric) trên tập số thực R.",
                answer=truth,
                solution_vi=[why, "Mệnh đề " + ("đúng." if truth else "sai.")])
