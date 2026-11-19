"""Tối Ưu và Toán Rời Rạc, floor 4 (bài toán tối ưu tổ hợp, độ phức tạp thuật toán):
generators. Ids start with `tr_g4_`.

The generators solve their instances the way a program would (dynamic programming for the
knapsack, listing the tours of a small travelling-salesman instance, greedy choices, closed
formulas for loop counts); tools/math_verify_tr_t4.py instead tries every subset or every
permutation, runs the loops, and takes limits with sympy."""
from __future__ import annotations

import itertools
import math
import random

from . import Draw, generator


def _items_text(weights, values) -> str:
    return "; ".join(f"đồ vật {i + 1} nặng {a}, giá trị {c}" for i, (a, c) in enumerate(zip(weights, values)))


def _set_text(xs) -> str:
    return "{" + ", ".join(str(v) for v in xs) + "}"


# ------------------------------------------------------------------ duyệt toàn bộ
_COUNT_KINDS = {
    "tui": ("Duyệt toàn bộ bài toán cái túi với {n} đồ vật: mỗi phương án là một xâu nhị phân x_1 x_2 ... x_{n} "
            "(x_i = 1 khi lấy đồ vật i). Có tất cả bao nhiêu xâu phải xét, chưa kể ràng buộc khối lượng?"),
    "du_lich": ("Duyệt toàn bộ bài toán người du lịch với {n} thành phố, hành trình luôn xuất phát và trở về thành "
                "phố 1; hai hành trình đi ngược chiều nhau vẫn tính là hai. Có bao nhiêu hành trình phải xét?"),
    "phan_viec": ("Có {n} đệ tử và {n} việc; mỗi người làm đúng một việc, mỗi việc do đúng một người làm. Duyệt "
                  "toàn bộ phải xét bao nhiêu cách phân việc?"),
}


@generator("tr_g4_so_phuong_an")
def so_phuong_an(rng: random.Random) -> Draw:
    kind = rng.choice(list(_COUNT_KINDS))
    n = rng.randint(5, 12) if kind == "tui" else rng.randint(4, 8)
    if kind == "tui":
        total = 2 ** n
        steps = ["Mỗi đồ vật có 2 khả năng: lấy hoặc không lấy.",
                 f"Theo quy tắc nhân có 2^{n} = {total} xâu nhị phân độ dài {n}."]
    elif kind == "du_lich":
        total = math.factorial(n - 1)
        steps = ["Thành phố 1 đã cố định ở đầu và cuối hành trình.",
                 f"Mỗi hành trình là một hoán vị của {n - 1} thành phố còn lại.",
                 f"Có ({n} - 1)! = {n - 1}! = {total} hành trình."]
    else:
        total = math.factorial(n)
        steps = [f"Một cách phân việc cho người 1, 2, ..., {n} các việc đôi một khác nhau: đó là một hoán vị của {n} việc.",
                 f"Có {n}! = {total} hoán vị."]
    return Draw(params={"kind": kind, "n": n}, prompt_vi=_COUNT_KINDS[kind].format(n=n),
                answer=str(total), solution_vi=steps)


@generator("tr_g4_cai_tui")
def cai_tui(rng: random.Random) -> Draw:
    k = rng.choice([4, 5])
    weights = [rng.randint(2, 9) for _ in range(k)]
    values = [rng.randint(3, 15) for _ in range(k)]
    cap = rng.randint(max(weights) + 1, sum(weights) - 2)
    # dynamic programming over (first i objects, capacity left)
    best = [[0] * (cap + 1) for _ in range(k + 1)]
    for i in range(1, k + 1):
        a, c = weights[i - 1], values[i - 1]
        for w in range(cap + 1):
            best[i][w] = best[i - 1][w]
            if a <= w and best[i - 1][w - a] + c > best[i][w]:
                best[i][w] = best[i - 1][w - a] + c
    chosen, w = [], cap
    for i in range(k, 0, -1):
        if best[i][w] != best[i - 1][w]:
            chosen.append(i)
            w -= weights[i - 1]
    chosen.reverse()
    load = sum(weights[i - 1] for i in chosen)
    return Draw(
        params={"weights": weights, "values": values, "cap": cap},
        prompt_vi=(f"Bài toán cái túi: túi chịu được khối lượng tối đa {cap}; {_items_text(weights, values)}. Mỗi đồ vật "
                   "lấy hoặc không lấy. Chọn các đồ vật có tổng khối lượng không vượt quá sức chứa và tổng giá trị lớn "
                   "nhất. Tổng giá trị lớn nhất đó là bao nhiêu?"),
        answer=str(best[k][cap]),
        solution_vi=[f"Có 2^{k} = {2 ** k} tập đồ vật; chỉ xét các tập có tổng khối lượng không quá {cap}.",
                     "Một cách xét gọn: bỏ ngay các tập quá nặng, so giá trị các tập còn lại, giữ tập có giá trị lớn nhất.",
                     f"Một phương án tốt nhất là lấy các đồ vật {_set_text(chosen)}: khối lượng {load}, "
                     f"giá trị {best[k][cap]}.",
                     f"Không tập nào nặng không quá {cap} có giá trị lớn hơn, nên đáp số là {best[k][cap]}."])


_CITY_PAIRS = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]


@generator("tr_g4_nguoi_du_lich")
def nguoi_du_lich(rng: random.Random) -> Draw:
    d = {pair: rng.randint(2, 20) for pair in _CITY_PAIRS}

    def dist(a, b):
        return d[(min(a, b), max(a, b))]

    tours = [(1, 2, 3, 4), (1, 2, 4, 3), (1, 3, 2, 4)]
    lengths = [sum(dist(t[i], t[(i + 1) % 4]) for i in range(4)) for t in tours]
    best = min(lengths)
    shown = "; ".join(f"d({a}, {b}) = {d[(a, b)]}" for a, b in _CITY_PAIRS)
    lines = [f"{'-'.join(str(v) for v in t)}-1: "
             + " + ".join(str(dist(t[i], t[(i + 1) % 4])) for i in range(4)) + f" = {L}"
             for t, L in zip(tours, lengths)]
    return Draw(
        params={"d": [d[p] for p in _CITY_PAIRS]},
        prompt_vi=(f"Bốn thành phố 1, 2, 3, 4 có khoảng cách hai chiều: {shown}. Một người xuất phát từ thành phố 1, "
                   "đi qua mỗi thành phố còn lại đúng một lần rồi trở về 1. Hành trình ngắn nhất dài bao nhiêu?"),
        answer=str(best),
        solution_vi=["Cố định thành phố 1. Có 3! = 6 hoán vị của 2, 3, 4, nhưng mỗi hành trình và hành trình ngược "
                     "chiều của nó dài bằng nhau, nên chỉ cần xét 3 hành trình.",
                     "; ".join(lines) + ".",
                     f"Hành trình ngắn nhất dài {best}."])


# ------------------------------------------------------------------ phát biểu: bài toán phân việc
@generator("tr_g4_phan_viec")
def phan_viec(rng: random.Random) -> Draw:
    cost = [[rng.randint(1, 9) for _ in range(3)] for _ in range(3)]
    rows = []
    for p in itertools.permutations(range(3)):
        total = sum(cost[i][p[i]] for i in range(3))
        rows.append((total, p))
    best = min(t for t, _ in rows)
    listed = "; ".join(f"việc ({p[0] + 1}, {p[1] + 1}, {p[2] + 1}): "
                       f"{cost[0][p[0]]} + {cost[1][p[1]]} + {cost[2][p[2]]} = {t}" for t, p in rows)
    return Draw(
        params={"cost": cost},
        prompt_vi=("Ba đệ tử nhận ba việc, mỗi người đúng một việc, mỗi việc đúng một người. Phần tử hàng i cột j của "
                   "ma trận C là chi phí khi đệ tử i làm việc j. Tìm cách phân việc có tổng chi phí nhỏ nhất. Tổng chi "
                   "phí nhỏ nhất là bao nhiêu?"),
        answer=str(best),
        matrices={"C": cost},
        solution_vi=["Tập phương án là các hoán vị (j_1, j_2, j_3) của 1, 2, 3: đệ tử i làm việc j_i. Hàm mục tiêu là "
                     "C(1, j_1) + C(2, j_2) + C(3, j_3).",
                     "Xét cả 3! = 6 hoán vị: " + listed + ".",
                     f"Giá trị nhỏ nhất là {best}."])


# ------------------------------------------------------------------ nhánh cận
@generator("tr_g4_nhanh_can")
def nhanh_can(rng: random.Random) -> Draw:
    while True:
        weights = [rng.randint(2, 8) for _ in range(4)]
        values = [rng.randint(3, 20) for _ in range(4)]
        ratios = [c / a for a, c in zip(weights, values)]
        if len(set(ratios)) == 4:
            break
    order = sorted(range(4), key=lambda i: -ratios[i])
    weights = [weights[i] for i in order]
    values = [values[i] for i in order]
    cap = rng.randint(max(weights[0], weights[1]) + 2, sum(weights) - 2)
    while True:
        x = [rng.randint(0, 1), rng.randint(0, 1)]
        if x[0] * weights[0] + x[1] * weights[1] <= cap:
            break
    v = x[0] * values[0] + x[1] * values[1]
    w = x[0] * weights[0] + x[1] * weights[1]
    feasible = [sum(values[i] for i in s) for r in range(5) for s in itertools.combinations(range(4), r)
                if sum(weights[i] for i in s) <= cap]
    left = cap - w
    bound_num, bound_den = v * weights[2] + left * values[2], weights[2]       # v + left * c_3/a_3
    # a record that cuts the branch about half of the time (when the data allow both)
    cutting = sorted({r for r in feasible if bound_num <= r * bound_den})
    going = sorted({r for r in feasible if bound_num > r * bound_den})
    want_cut = rng.random() < 0.5
    record = rng.choice(cutting if (want_cut and cutting) or not going else going)
    g = math.gcd(bound_num, bound_den)
    bound_text = f"{bound_num // g}" if bound_den // g == 1 else f"{bound_num // g}/{bound_den // g}"
    cut = bound_num <= record * bound_den
    return Draw(
        params={"weights": weights, "values": values, "cap": cap, "x": x, "record": record},
        prompt_vi=(f"Giải bài toán cái túi (tìm giá trị lớn nhất) bằng nhánh cận. Sức chứa {cap}; "
                   f"{_items_text(weights, values)}; các đồ vật đã xếp theo tỉ số giá trị/khối lượng giảm dần. Nhánh đang "
                   f"xét đã chọn x_1 = {x[0]}, x_2 = {x[1]}. Cận trên của nhánh là giá trị đã có cộng sức chứa còn lại nhân "
                   f"tỉ số c_3/a_3 = {values[2]}/{weights[2]}. Kỷ lục hiện có là {record}. Khẳng định: nhánh này bị cắt."),
        answer=cut,
        solution_vi=[f"Giá trị đã có: {v}; khối lượng đã dùng: {w}; sức chứa còn lại: {cap} - {w} = {left}.",
                     f"Cận trên: {v} + {left} . {values[2]}/{weights[2]} = {bound_text}.",
                     (f"Cận trên {bound_text} không lớn hơn kỷ lục {record}: nhánh không thể cho phương án tốt hơn, "
                      "nên bị cắt. Khẳng định đúng." if cut else
                      f"Cận trên {bound_text} lớn hơn kỷ lục {record}: nhánh có thể còn phương án tốt hơn, phải xét "
                      "tiếp. Khẳng định sai.")])


# ------------------------------------------------------------------ tham lam
@generator("tr_g4_tham_lam_xu")
def tham_lam_xu(rng: random.Random) -> Draw:
    want = rng.random() < 0.5            # draw again (a few times) until the answer is the wanted one
    for _ in range(30):
        a = rng.randint(2, 6)
        b = rng.randint(a + 1, 12)
        x = rng.randint(b + 1, 30)
        coins = [b, a, 1]
        rest, greedy = x, []
        for c in coins:
            while rest >= c:
                rest -= c
                greedy.append(c)
        fewest = [0] + [10 ** 9] * x
        for t in range(1, x + 1):
            fewest[t] = min(fewest[t - c] + 1 for c in coins if c <= t)
        ok = len(greedy) == fewest[x]
        if ok == want:
            break
    return Draw(
        params={"a": a, "b": b, "x": x},
        prompt_vi=(f"Có đủ nhiều đồng linh thạch mệnh giá 1, {a} và {b}. Cần trả đúng {x}. Thuật toán tham lam: mỗi bước "
                   f"lấy đồng có mệnh giá lớn nhất không vượt quá số còn phải trả. Khẳng định: với số tiền {x}, thuật toán "
                   "tham lam dùng ít đồng nhất có thể."),
        answer=ok,
        solution_vi=[f"Tham lam trả {x} = {' + '.join(str(c) for c in greedy)}: dùng {len(greedy)} đồng.",
                     f"Số đồng ít nhất có thể (xét mọi cách trả) là {fewest[x]}.",
                     "Hai số bằng nhau: khẳng định đúng." if ok else
                     f"{len(greedy)} > {fewest[x]}: tham lam không tối ưu ở đây, khẳng định sai."])


@generator("tr_g4_lich")
def lich(rng: random.Random) -> Draw:
    k = rng.randint(5, 6)
    talks = set()
    while len(talks) < k:
        s = rng.randint(0, 10)
        talks.add((s, s + rng.randint(1, 4)))
    talks = sorted(talks)
    chosen, end = [], -1
    for s, f in sorted(talks, key=lambda t: (t[1], t[0])):
        if s >= end:
            chosen.append((s, f))
            end = f
    shown = ", ".join(f"[{s}, {f}]" for s, f in talks)
    return Draw(
        params={"talks": [list(t) for t in talks]},
        prompt_vi=(f"Một phòng luyện công chỉ dùng được cho một buổi tại mỗi lúc. Có {k} buổi xin dùng phòng, buổi [s, f] "
                   f"bắt đầu lúc s giờ và kết thúc lúc f giờ: {shown}. Hai buổi xếp được cùng nhau khi buổi này kết thúc "
                   "không muộn hơn lúc buổi kia bắt đầu. Xếp được nhiều nhất bao nhiêu buổi?"),
        answer=str(len(chosen)),
        solution_vi=["Tham lam đúng cho bài này: mỗi bước chọn buổi kết thúc sớm nhất trong các buổi còn xếp được.",
                     "Các buổi được chọn lần lượt: " + ", ".join(f"[{s}, {f}]" for s, f in chosen) + ".",
                     f"Xếp được nhiều nhất {len(chosen)} buổi. (Chọn buổi kết thúc sớm nhất để lại nhiều thời gian nhất "
                     "cho các buổi sau, nên không phương án nào xếp được nhiều hơn.)"])


# ------------------------------------------------------------------ ký hiệu O
_LOOPS = {
    "full": ("for i = 1 to n: for j = 1 to n: x = x + 1", "n . n = n^2"),
    "tri": ("for i = 1 to n: for j = i to n: x = x + 1", "n + (n - 1) + ... + 1 = n(n + 1)/2"),
    "strict": ("for i = 1 to n: for j = i + 1 to n: x = x + 1", "(n - 1) + (n - 2) + ... + 0 = n(n - 1)/2"),
    "seq": ("for i = 1 to n: x = x + 1, rồi sau đó for i = 1 to n: for j = 1 to n: x = x + 1", "n + n^2"),
    "halve": ("for i = 1 to n: (j = 1; while j <= n: j = 2j; x = x + 1)",
              "n . (số lần nhân đôi j từ 1 cho đến khi vượt n)"),
}


def _loop_count(kind: str, n: int) -> int:
    if kind == "full":
        return n * n
    if kind == "tri":
        return n * (n + 1) // 2
    if kind == "strict":
        return n * (n - 1) // 2
    if kind == "seq":
        return n + n * n
    return n * (n.bit_length())          # j = 1, 2, 4, ..., the largest power of 2 not above n


@generator("tr_g4_dem_vong_lap")
def dem_vong_lap(rng: random.Random) -> Draw:
    kind = rng.choice(list(_LOOPS))
    n = rng.randint(5, 20)
    code, formula = _LOOPS[kind]
    total = _loop_count(kind, n)
    steps = [f"Đếm theo công thức: {formula}."]
    if kind == "halve":
        steps.append(f"Với n = {n}, j nhận các giá trị 1, 2, 4, ..., {2 ** (n.bit_length() - 1)}: "
                     f"{n.bit_length()} lần trong mỗi vòng i.")
    steps.append(f"Với n = {n}: lệnh x = x + 1 chạy {total} lần.")
    return Draw(params={"kind": kind, "n": n},
                prompt_vi=f"Đoạn chương trình sau chạy với n = {n}: {code}. Lệnh x = x + 1 được thực hiện bao nhiêu lần?",
                answer=str(total), solution_vi=steps)


def _pw(e: int) -> str:
    """n to the power e, written the usual way: n, n^2."""
    return "n" if e == 1 else f"n^{e}"


def _poly_text(a: int, p: int, b: int, q: int) -> str:
    def term(c, e):
        return f"{c}{_pw(e)}" if e else str(c)
    return f"{term(a, p)} + {term(b, q)}"


@generator("tr_g4_o_lon")
def o_lon(rng: random.Random) -> Draw:
    kind = rng.choice(["poly", "poly", "exp"])
    if kind == "poly":
        p = rng.randint(1, 4)
        q = rng.randint(0, p - 1)
        a, b = rng.randint(2, 9), rng.randint(2, 50)
        k = rng.randint(1, 4)
        ok = p <= k
        f = _poly_text(a, p, b, q)
        claim = _pw(k)
        steps = [f"Số hạng tăng nhanh nhất của f(n) = {f} là {a}{_pw(p)}; khi n >= 1 thì f(n) <= {a + b}{_pw(p)}.",
                 (f"Vì {p} <= {k} nên {_pw(p)} <= {_pw(k)} với n >= 1, do đó f(n) <= {a + b}{_pw(k)}: "
                  f"f(n) = O({claim}). Khẳng định đúng." if ok else
                  f"f(n)/{_pw(k)} >= {a}{_pw(p - k)} tăng mãi, không bị chặn bởi hằng số nào: f(n) không là "
                  f"O({claim}). Khẳng định sai.")]
        params = {"kind": kind, "a": a, "p": p, "b": b, "q": q, "k": k}
    else:
        c = rng.choice([2, 3])
        d = rng.choice([2, 3])
        a, b, p = rng.randint(1, 5), rng.randint(1, 9), rng.randint(1, 3)
        ok = c <= d
        f = f"{a} . {c}^n + {b}{_pw(p)}"
        claim = f"{d}^n"
        steps = [f"{_pw(p)} tăng chậm hơn {c}^n, nên số hạng chính của f(n) = {f} là {a} . {c}^n.",
                 (f"Vì {c} <= {d} nên f(n) <= C . {d}^n với một hằng số C khi n đủ lớn: f(n) = O({claim}). "
                  "Khẳng định đúng." if ok else
                  f"f(n)/{d}^n >= {a} . (3/2)^n tăng mãi: không có hằng số C nào để f(n) <= C . {d}^n. Khẳng định sai.")]
        params = {"kind": kind, "a": a, "c": c, "b": b, "p": p, "d": d}
    return Draw(params=params, prompt_vi=f"Cho f(n) = {f}. Khẳng định: f(n) = O({claim}).", answer=ok, solution_vi=steps)
