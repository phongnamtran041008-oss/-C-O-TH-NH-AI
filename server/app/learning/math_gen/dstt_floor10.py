"""Đại Số Tuyến Tính, tầng 10 (Tài Năng: quan hệ, phép toán hai ngôi, nhóm, vành và trường, dạng song tuyến tính):
generators.

Everything is exact (whole numbers and fractions). The finite structures are small residue rings Z_n, so each answer
is a whole number that a learner can reach by hand; a relation is a handful of pairs on {1, 2, 3, 4}.
tools/math_verify_dstt_t10.py recomputes each answer another way: relations as 0/1 matrices (reflexive = trace n,
symmetric = M equals its transpose, transitive = the Boolean square of M is under M), the identity and the inverse of an
operation by solving the defining equation with sympy, associativity by expanding (a*b)*c - a*(b*c), orders of
elements by sympy's n_order or by running through the multiples, and bilinear forms as sympy matrix products."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from . import Draw, generator, num


# ------------------------------------------------------------------ quan hệ hai ngôi
def _pairs_text(rel) -> str:
    return ", ".join(f"({a}, {b})" for a, b in sorted(rel))


def _reflexive(a_set, rel) -> bool:
    return all((a, a) in rel for a in a_set)


def _symmetric(rel) -> bool:
    return all((b, a) in rel for a, b in rel)


def _transitive(rel) -> bool:
    return all((a, d) in rel for a, b in rel for c, d in rel if b == c)


def _partition(rng: random.Random, n: int) -> list[list[int]]:
    blocks_n = rng.choice([2, 2, 3])
    labels = [rng.randrange(blocks_n) for _ in range(n)]
    while len(set(labels)) < 2:
        labels = [rng.randrange(blocks_n) for _ in range(n)]
    return [[i + 1 for i in range(n) if labels[i] == k] for k in sorted(set(labels))]


@generator("dstt_g10_quan_he_tf")
def quan_he_tf(rng: random.Random) -> Draw:
    n = 4
    a_set = list(range(1, n + 1))
    blocks = _partition(rng, n)
    rel = {(a, b) for blk in blocks for a in blk for b in blk}
    for _ in range(rng.choice([0, 1, 1, 2])):                         # damage the equivalence a little
        move = rng.choice(["diag", "one_way", "add"])
        if move == "diag":
            rel.discard((rng.choice(a_set),) * 2)
        elif move == "one_way":
            off = sorted((a, b) for a, b in rel if a != b)
            if off:
                rel.discard(rng.choice(off))
        else:
            rel.add((rng.choice(a_set), rng.choice(a_set)))
    prop = rng.choice(["phản xạ", "đối xứng", "bắc cầu", "là một quan hệ tương đương"])
    refl, sym, trans = _reflexive(a_set, rel), _symmetric(rel), _transitive(rel)
    truth = {"phản xạ": refl, "đối xứng": sym, "bắc cầu": trans,
             "là một quan hệ tương đương": refl and sym and trans}[prop]
    lead = "R có tính chất" if prop != "là một quan hệ tương đương" else "R"
    prompt = f"Trên A = {{1, 2, 3, 4}} cho quan hệ R gồm các cặp {_pairs_text(rel)}. {lead} {prop}."
    sol = []
    missing_diag = [a for a in a_set if (a, a) not in rel]
    broken_sym = sorted((b, a) for a, b in rel if (b, a) not in rel)
    broken_trans = sorted((a, b, c, d) for a, b in rel for c, d in rel if b == c and (a, d) not in rel)

    def reason(kind: str) -> str:
        if kind == "phản xạ":
            return ("Mọi cặp (a, a) đều có trong R: phản xạ." if refl else
                    f"Thiếu cặp ({missing_diag[0]}, {missing_diag[0]}): không phản xạ.")
        if kind == "đối xứng":
            return ("Mỗi cặp (a, b) đều đi với cặp đảo (b, a): đối xứng." if sym else
                    f"Có cặp ({broken_sym[0][1]}, {broken_sym[0][0]}) nhưng thiếu cặp đảo {broken_sym[0]}: không đối xứng.")
        a, b, c, d = broken_trans[0] if broken_trans else (0, 0, 0, 0)
        return ("Mỗi khi (a, b) và (b, c) cùng thuộc R thì (a, c) cũng thuộc R: bắc cầu." if trans else
                f"({a}, {b}) và ({c}, {d}) thuộc R (b = c = {b}) nhưng ({a}, {d}) không thuộc R: không bắc cầu.")
    if prop == "là một quan hệ tương đương":
        sol = [reason("phản xạ"), reason("đối xứng"), reason("bắc cầu"),
               "Quan hệ tương đương đòi hỏi cả ba tính chất: " + ("cả ba đều có, mệnh đề đúng." if truth else "có tính chất không thoả, mệnh đề sai.")]
    else:
        sol = [reason(prop), "Mệnh đề " + ("đúng." if truth else "sai.")]
    return Draw(params={"rel": sorted([a, b] for a, b in rel), "prop": prop}, prompt_vi=prompt, answer=truth, solution_vi=sol)


@generator("dstt_g10_so_lop")
def so_lop(rng: random.Random) -> Draw:
    m = rng.randint(3, 7)
    n = rng.randint(m + 2, 22)
    x = rng.randint(1, n)
    ask = rng.choice(["so_lop", "lop_cua_x", "so_cap"])
    classes = {}
    for a in range(1, n + 1):
        classes.setdefault(a % m, []).append(a)
    head = (f"Trên tập A = {{1, 2, ..., {n}}} xét quan hệ a ~ b khi a - b chia hết cho {m}. Đây là một quan hệ tương đương. ")
    sizes = [len(v) for v in classes.values()]
    if ask == "so_lop":
        ans = len(classes)
        prompt = head + "Có bao nhiêu lớp tương đương? Nhập một số."
        sol = [f"Hai số cùng lớp khi cùng số dư trong phép chia cho {m}; các số dư có thể là 0, 1, ..., {m - 1}.",
               f"Với A = 1..{n} (ít nhất {m} số liên tiếp) mọi số dư đều xuất hiện: có {ans} lớp."]
    elif ask == "lop_cua_x":
        cls = [b for b in range(1, n + 1) if (x - b) % m == 0]
        ans = len(cls)
        prompt = head + f"Lớp tương đương của số {x} có bao nhiêu phần tử? Nhập một số."
        sol = [f"Lớp của {x} gồm mọi b trong A có cùng số dư với {x} khi chia cho {m} (số dư {x % m}): " + ", ".join(map(str, cls)) + ".",
               f"Có {ans} phần tử."]
    else:
        ans = sum(s * s for s in sizes)
        prompt = head + "Có bao nhiêu cặp có thứ tự (a, b) thuộc A x A mà a ~ b? Nhập một số."
        sol = [f"Mỗi lớp có k phần tử cho k . k cặp (a, b) cùng lớp (cả a = b và hai chiều). Kích thước các lớp: " + ", ".join(map(str, sizes)) + ".",
               "Tổng bình phương kích thước: " + " + ".join(f"{s}^2" for s in sizes) + f" = {ans}."]
    return Draw(params={"m": m, "n": n, "x": x, "ask": ask}, prompt_vi=prompt, answer=str(ans), solution_vi=sol)


# ------------------------------------------------------------------ phép toán hai ngôi
def _lin(coef: int, var: str) -> str:
    return var if coef == 1 else f"{coef}{var}"


@generator("dstt_g10_trung_hoa")
def trung_hoa(rng: random.Random) -> Draw:
    kind = rng.choice(["cong_hang", "cong_tich"])
    ask = rng.choice(["trung_hoa", "nguoc", "nguoc"])
    if kind == "cong_hang":
        k = rng.choice([v for v in range(-6, 7) if v])
        text = f"a * b = a + b {'+' if k > 0 else '-'} {abs(k)}"
        e = Fraction(-k)
        inv = lambda x: Fraction(-x - 2 * k)               # noqa: E731
        x = rng.randint(-6, 8)
        sol_e = [f"a * e = a + e {'+' if k > 0 else '-'} {abs(k)} = a cho e = {num(e)}; phép toán giao hoán nên e * a cũng bằng a."]
        sol_i = [f"Phần tử trung hoà là e = {num(e)} (a + e {'+' if k > 0 else '-'} {abs(k)} = a).",
                 f"x * y = e: {x} + y {'+' if k > 0 else '-'} {abs(k)} = {num(e)} cho y = {num(inv(x))}."]
    else:
        k = rng.choice([-3, -2, -1, 1, 2, 3])
        kt = "ab" if k == 1 else ("-ab" if k == -1 else f"{'+ ' if k > 0 else '- '}{abs(k)}ab")
        text = f"a * b = a + b {kt}" if k not in (1, -1) else (f"a * b = a + b + ab" if k == 1 else "a * b = a + b - ab")
        e = Fraction(0)
        while True:
            x = rng.randint(-5, 6)
            if 1 + k * x != 0:
                break
        inv = lambda t: Fraction(-t, 1 + k * t)             # noqa: E731
        sol_e = [f"a * e = a + e + ({k}) a e = a cho e (1 + ({k}) a) = 0 với mọi a, nên e = 0."]
        sol_i = ["Phần tử trung hoà là e = 0 (a * 0 = a).",
                 f"x * y = 0 cho {x} + y + ({k}) . {x} y = 0, tức y (1 + ({k}) . {x}) = {-x}, y = {num(inv(x))}."]
    if ask == "trung_hoa":
        prompt = f"Trên R xét phép toán {text}. Tìm phần tử trung hoà e (a * e = e * a = a với mọi a). Nhập một số hoặc phân số tối giản."
        ans, sol = e, sol_e
    else:
        prompt = (f"Trên R xét phép toán {text}, giao hoán và kết hợp, có phần tử trung hoà. Tìm phần tử ngược của {x}, "
                  f"tức số y có {x} * y bằng phần tử trung hoà. Nhập một số hoặc phân số tối giản.")
        ans, sol = inv(x), sol_i
    return Draw(params={"kind": kind, "k": k, "ask": ask, "x": x}, prompt_vi=prompt, answer=num(ans), solution_vi=sol)


def _poly(ca: int, cb: int, cc: int, c0: int) -> str:
    """ca a + cb b + cc c + c0 written the usual way: 2a - b + 3, -c, 0."""
    out = ""
    for coef, var in ((ca, "a"), (cb, "b"), (cc, "c"), (c0, "")):
        if coef == 0:
            continue
        mag = abs(coef)
        body = str(mag) if var == "" else (var if mag == 1 else f"{mag}{var}")
        out += (("-" if coef < 0 else "") + body) if not out else f" {'+' if coef > 0 else '-'} {body}"
    return out or "0"


@generator("dstt_g10_ket_hop_tf")
def ket_hop_tf(rng: random.Random) -> Draw:
    p = rng.choice([0, 1, 1, 1, 2, -1])
    q = rng.choice([0, 1, 1, 1, 2, -1])
    r = rng.choice([-2, -1, 0, 0, 1, 2])
    which = rng.choice(["kết hợp", "giao hoán"])
    expr = _poly(p, q, 0, r)
    head = f"a * b = {expr}."
    if which == "giao hoán":
        truth = p == q
        sol = [head + f" Đổi chỗ: b * a = {_poly(q, p, 0, r)}.",
               f"Hiệu a * b - b * a = ({p} - {q})(a - b) = {p - q}(a - b).",
               ("Hiệu bằng 0 với mọi a, b vì hệ số của a và của b bằng nhau. Mệnh đề đúng." if truth else
                f"Hiệu khác 0 khi a khác b: ví dụ a = 1, b = 0 cho a * b = {p + r} và b * a = {q + r}. Mệnh đề sai.")]
    else:
        truth = p * p == p and q * q == q and r * p == r * q
        left, right = _poly(p * p, p * q, q, p * r + r), _poly(p, q * p, q * q, q * r + r)
        sol = [head,
               f"(a * b) * c = {left}.",
               f"a * (b * c) = {right}.",
               ("Hai vế có cùng hệ số của a, b, c và cùng hằng số với mọi a, b, c. Mệnh đề đúng." if truth else
                "Hai vế khác nhau ở ít nhất một hệ số hoặc hằng số (a: p^2 so với p; c: q so với q^2; hằng số: pr + r so với qr + r), "
                "nên có a, b, c làm chúng khác nhau. Mệnh đề sai.")]
    return Draw(params={"p": p, "q": q, "r": r, "which": which},
                prompt_vi=f"Phép toán hai ngôi a * b = {expr} trên R có tính chất {which}.",
                answer=truth, solution_vi=sol)


# ------------------------------------------------------------------ nhóm
@generator("dstt_g10_cap_cong")
def cap_cong(rng: random.Random) -> Draw:
    n = rng.randint(8, 40)
    a = rng.randint(1, n - 1)
    k = n // math.gcd(a, n)
    return Draw(params={"n": n, "a": a},
                prompt_vi=f"Trong nhóm cộng Z_{n} (số dư modulo {n}, phép cộng modulo {n}), phần tử {a} có cấp bao nhiêu, tức số nguyên "
                          f"dương k nhỏ nhất để {a} cộng với chính nó k lần được 0? Nhập một số.",
                answer=str(k),
                solution_vi=[f"Cấp của a trong Z_n là n/gcd(a, n): gcd({a}, {n}) = {math.gcd(a, n)}.",
                             f"Cấp = {n}/{math.gcd(a, n)} = {k}. (Kiểm tra: {k} . {a} = {k * a} = {k * a // n} . {n}, chia hết {n}.)"])


@generator("dstt_g10_cap_nhan")
def cap_nhan(rng: random.Random) -> Draw:
    p = rng.choice([5, 7, 11, 13])
    a = rng.randint(2, p - 1)
    seq, cur = [], 1
    while True:
        cur = cur * a % p
        seq.append(cur)
        if cur == 1:
            break
    return Draw(params={"p": p, "a": a},
                prompt_vi=f"Trong nhóm các phần tử khác 0 của Z_{p} với phép nhân modulo {p}, phần tử {a} có cấp bao nhiêu, tức số nguyên "
                          f"dương k nhỏ nhất để {a}^k = 1? Nhập một số.",
                answer=str(len(seq)),
                solution_vi=["Các lũy thừa liên tiếp của " + str(a) + " modulo " + str(p) + ": " + ", ".join(map(str, seq)) + ".",
                             f"Lũy thừa đầu tiên bằng 1 là số mũ {len(seq)}, nên cấp là {len(seq)} (và chia hết cấp {p - 1} của nhóm)."])


@generator("dstt_g10_dem_don_vi")
def dem_don_vi(rng: random.Random) -> Draw:
    n = rng.randint(6, 40)
    units = [a for a in range(1, n) if math.gcd(a, n) == 1]
    ask = rng.choice(["don_vi", "uoc_cua_0", "phan_tu_sinh"])
    if ask == "don_vi":
        ans = len(units)
        prompt = (f"Các phần tử khả nghịch của Z_{n} (a trong 1..{n - 1} có a . b = 1 modulo {n} với một b nào đó) lập thành một nhóm với phép "
                  f"nhân modulo {n}. Nhóm đó có bao nhiêu phần tử? Nhập một số.")
        sol = [f"a khả nghịch modulo {n} khi và chỉ khi gcd(a, {n}) = 1.",
               f"Có {ans} số như vậy trong 1..{n - 1}: " + ", ".join(map(str, units[:12])) + (", ..." if len(units) > 12 else "") + "."]
    elif ask == "uoc_cua_0":
        ans = n - 1 - len(units)
        prompt = (f"Trong vành Z_{n}, một ước của 0 là phần tử a khác 0 có a . b = 0 (modulo {n}) với một b khác 0 nào đó. "
                  f"Z_{n} có bao nhiêu ước của 0? Nhập một số.")
        sol = [f"Mọi phần tử khác 0 hoặc khả nghịch (gcd(a, {n}) = 1) hoặc là ước của 0 (gcd(a, {n}) > 1).",
               f"Có {n - 1} phần tử khác 0, trong đó {len(units)} khả nghịch; vậy có {n - 1} - {len(units)} = {ans} ước của 0."]
    else:
        ans = len(units)
        prompt = f"Trong nhóm cộng Z_{n}, có bao nhiêu phần tử sinh ra cả nhóm? Nhập một số."
        sol = [f"a sinh Z_{n} khi và chỉ khi gcd(a, {n}) = 1 (cấp của a là {n}/gcd(a, {n}) phải bằng {n}).",
               f"Có {ans} số a trong 1..{n - 1} thoả điều đó (phi({n}) = {ans})."]
    return Draw(params={"n": n, "ask": ask}, prompt_vi=prompt, answer=str(ans), solution_vi=sol)


# ------------------------------------------------------------------ vành và trường
@generator("dstt_g10_nghich_dao_mod")
def nghich_dao_mod(rng: random.Random) -> Draw:
    n = rng.randint(7, 40)
    a = rng.choice([a for a in range(2, n) if math.gcd(a, n) == 1])
    inv = next(b for b in range(1, n) if a * b % n == 1)
    return Draw(params={"n": n, "a": a},
                prompt_vi=f"Trong vành Z_{n} (số dư modulo {n}), tìm nghịch đảo của {a}, tức số b trong 1..{n - 1} có {a} . b = 1 modulo {n}. Nhập một số.",
                answer=str(inv),
                solution_vi=[f"gcd({a}, {n}) = 1 nên {a} khả nghịch modulo {n}; tìm b với {a} b - {n} t = 1 (đẳng thức Bezout).",
                             f"b = {inv}: {a} . {inv} = {a * inv} = {a * inv // n} . {n} + 1, tức bằng 1 modulo {n}."])


# ------------------------------------------------------------------ dạng song tuyến tính
@generator("dstt_g10_ma_tran_song_tuyen")
def ma_tran_song_tuyen(rng: random.Random) -> Draw:
    k = rng.choice([2, 2, 3])
    a = [[rng.randint(-4, 5) for _ in range(k)] for _ in range(k)]
    u = [rng.randint(-3, 4) for _ in range(k)]
    v = [rng.randint(-3, 4) for _ in range(k)]
    av = [sum(a[i][j] * v[j] for j in range(k)) for i in range(k)]
    val = sum(u[i] * av[i] for i in range(k))
    vec = lambda t: "(" + ", ".join(map(str, t)) + ")"     # noqa: E731
    return Draw(params={"a": a, "u": u, "v": v},
                prompt_vi=f"Dạng song tuyến tính f trên R^{k} có ma trận A như hình, nghĩa là f(x, y) = x^T A y. Tính f(u, v) với u = {vec(u)} và v = {vec(v)}. Nhập một số.",
                answer=str(val),
                solution_vi=[f"A v = {vec(av)} (mỗi thành phần là hàng của A nhân với v).",
                             f"f(u, v) = u^T (A v) = " + " + ".join(f"({u[i]}) . ({av[i]})" for i in range(k)) + f" = {val}."],
                matrices={"A": a})


@generator("dstt_g10_he_so_cheo")
def he_so_cheo(rng: random.Random) -> Draw:
    a, b, c = rng.randint(-4, 6), rng.randint(-8, 8), rng.randint(-4, 6)
    if a == 0 and c == 0:
        a = 1
    ask = rng.choice(["b12", "dinh_thuc", "gia_tri"])
    u = (rng.randint(-3, 3), rng.randint(-3, 3))

    def term(coef: int, mono: str, first: bool) -> str:
        if coef == 0:
            return ""
        sign = "-" if coef < 0 else "+"
        mag = abs(coef)
        body = mono if mag == 1 else f"{mag} {mono}"
        return (("-" if coef < 0 else "") + body) if first else f" {sign} {body}"
    parts, first = "", True
    for coef, mono in ((a, "x1^2"), (b, "x1 x2"), (c, "x2^2")):
        t = term(coef, mono, first)
        if t:
            parts += t
            first = False
    q = f"q(x) = {parts}"
    head = f"Dạng toàn phương trên R^2: {q}, tức q(x) = x^T B x với B là ma trận đối xứng. "
    b12 = Fraction(b, 2)
    if ask == "b12":
        ans = b12
        prompt = head + "Tìm phần tử b12 của B. Nhập một số hoặc phân số tối giản."
        sol = ["x^T B x = b11 x1^2 + 2 b12 x1 x2 + b22 x2^2, nên hệ số của x1 x2 bằng 2 b12.",
               f"b12 = {b}/2 = {num(ans)}."]
    elif ask == "dinh_thuc":
        ans = a * c - b12 ** 2
        prompt = head + "Tính định thức của B. Nhập một số hoặc phân số tối giản."
        sol = [f"B có đường chéo {a}, {c} và b12 = b21 = {b}/2 = {num(b12)}.",
               f"det B = {a} . {c} - ({num(b12)})^2 = {num(ans)}."]
    else:
        ans = a * u[0] ** 2 + b * u[0] * u[1] + c * u[1] ** 2
        prompt = head + f"Tính q({u[0]}, {u[1]}). Nhập một số."
        sol = [f"Thay x1 = {u[0]}, x2 = {u[1]} vào q: {a} . ({u[0]})^2 + ({b}) . ({u[0]}) . ({u[1]}) + {c} . ({u[1]})^2 = {ans}."]
    return Draw(params={"a": a, "b": b, "c": c, "ask": ask, "u": list(u)}, prompt_vi=prompt, answer=num(ans), solution_vi=sol)
