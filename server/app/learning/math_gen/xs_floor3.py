"""Xác Suất và Thống Kê, tầng 3 (công thức cộng, nhân, xác suất có điều kiện, Bernoulli): generators.

The answers here come from the formulas of the floor (addition rule, multiplication rule,
P(AB)/P(B), Bernoulli); tools/math_verify_xs.py recomputes them by listing the outcomes or
with sympy.stats, never by the same formula."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from . import Draw, generator, num, paren


def _lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)


# ------------------------------------------------------------------ công thức cộng
@generator("xs_g3_chia_het")
def chia_het(rng: random.Random) -> Draw:
    while True:
        n = rng.randint(12, 60)
        a, b = sorted(rng.sample(range(2, 8), 2))
        if b % a and n // _lcm(a, b) >= 1:
            break
    na, nb, nab = n // a, n // b, n // _lcm(a, b)
    fav = na + nb - nab
    return Draw(
        params={"n": n, "a": a, "b": b},
        prompt_vi=f"Chọn ngẫu nhiên một số nguyên từ 1 đến {n}, mỗi số cùng khả năng được chọn. "
                  f"Tính xác suất số được chọn chia hết cho {a} hoặc chia hết cho {b}.",
        answer=num(Fraction(fav, n)),
        solution_vi=[f"A: chia hết cho {a}, B: chia hết cho {b}. Cần P(A + B) = P(A) + P(B) - P(AB).",
                     f"Từ 1 đến {n} có {na} số chia hết cho {a} và {nb} số chia hết cho {b}.",
                     f"AB là chia hết cho cả {a} và {b}, tức chia hết cho {_lcm(a, b)}: có {nab} số.",
                     f"P(A + B) = ({na} + {nb} - {nab})/{n} = {fav}/{n} = {num(Fraction(fav, n))}."])


@generator("xs_g3_cong_tim_giao")
def cong_tim_giao(rng: random.Random) -> Draw:
    while True:
        n = rng.choice([10, 12, 20, 24, 30])
        na, nb = rng.randint(1, n - 1), rng.randint(1, n - 1)
        nab = rng.randint(max(0, na + nb - n), min(na, nb))
        if 0 < nab < min(na, nb):
            break
    pa, pb, pab = Fraction(na, n), Fraction(nb, n), Fraction(nab, n)
    pu = pa + pb - pab
    kind = rng.choice(["giao", "khong_ca_hai"])
    if kind == "giao":
        given = f"P(A) = {num(pa)}, P(B) = {num(pb)} và P(A + B) = {num(pu)}"
        ask, ans = "P(AB)", pab
        steps = ["Công thức cộng: P(A + B) = P(A) + P(B) - P(AB), nên P(AB) = P(A) + P(B) - P(A + B).",
                 f"P(AB) = {num(pa)} + {num(pb)} - {num(pu)} = {num(pab)}."]
    else:
        given = f"P(A) = {num(pa)}, P(B) = {num(pb)} và P(AB) = {num(pab)}"
        ask, ans = "xác suất để cả A và B đều không xảy ra", 1 - pu
        steps = ["'Cả A và B đều không xảy ra' là sự kiện đối của A + B.",
                 f"P(A + B) = {num(pa)} + {num(pb)} - {num(pab)} = {num(pu)}.",
                 f"Xác suất cần tìm là 1 - {num(pu)} = {num(1 - pu)}."]
    return Draw(
        params={"pa": num(pa), "pb": num(pb), "given": num(pu if kind == "giao" else pab), "kind": kind},
        prompt_vi=f"Cho hai sự kiện A, B với {given}. Tính {ask}.",
        answer=num(ans), solution_vi=steps)


# ------------------------------------------------------------------ xác suất có điều kiện
@generator("xs_g3_bang_dieu_kien")
def bang_dieu_kien(rng: random.Random) -> Draw:
    t = {(g, r): rng.randint(4, 30) for g in ("nam", "nu") for r in ("dat", "truot")}
    kind = rng.choice(["dat|nu", "dat|nam", "nu|dat", "nam|truot"])
    event, cond = kind.split("|")
    short = {"nam": "nam", "nu": "nữ", "dat": "đạt", "truot": "không đạt"}
    words = {"nam": "là nam", "nu": "là nữ", "dat": "thi đạt", "truot": "thi không đạt"}

    def count(*keys) -> int:
        return sum(v for (g, r), v in t.items() if all(k in (g, r) for k in keys))

    both, base = count(event, cond), count(cond)
    total = sum(t.values())
    return Draw(
        params={"table": [t[("nam", "dat")], t[("nam", "truot")], t[("nu", "dat")], t[("nu", "truot")]],
                "kind": kind},
        prompt_vi=f"Kết quả một kỳ thi của một lớp: nam có {t[('nam', 'dat')]} bạn đạt và {t[('nam', 'truot')]} bạn "
                  f"không đạt; nữ có {t[('nu', 'dat')]} bạn đạt và {t[('nu', 'truot')]} bạn không đạt. Chọn ngẫu "
                  f"nhiên một bạn trong lớp. Biết bạn đó {words[cond]}, tính xác suất bạn đó {words[event]}.",
        answer=num(Fraction(both, base)),
        solution_vi=[f"Điều kiện '{short[cond]}' thu hẹp lớp ({total} bạn) lại còn {base} bạn.",
                     f"Trong {base} bạn đó, có {both} bạn {short[event]}.",
                     f"P({short[event]} | {short[cond]}) = {both}/{base} = {num(Fraction(both, base))}."])


@generator("xs_g3_dieu_kien_xuc_xac")
def dieu_kien_xuc_xac(rng: random.Random) -> Draw:
    s = rng.randint(4, 10)
    kind = rng.choice(["bang_nhau", "co_sau", "dau_lon_hon", "dau_chan"])
    pairs = [(x, s - x) for x in range(max(1, s - 6), min(6, s - 1) + 1)]
    test = {"bang_nhau": lambda p: p[0] == p[1], "co_sau": lambda p: 6 in p,
            "dau_lon_hon": lambda p: p[0] > p[1], "dau_chan": lambda p: p[0] % 2 == 0}[kind]
    ask = {"bang_nhau": "hai xúc xắc ra cùng số chấm", "co_sau": "có ít nhất một xúc xắc ra mặt 6",
           "dau_lon_hon": "xúc xắc thứ nhất có số chấm lớn hơn xúc xắc thứ hai",
           "dau_chan": "xúc xắc thứ nhất ra mặt chẵn"}[kind]
    good = [p for p in pairs if test(p)]
    shown = ", ".join(f"({x}, {y})" for x, y in pairs)
    return Draw(
        params={"s": s, "kind": kind},
        prompt_vi=f"Gieo hai con xúc xắc cân đối, phân biệt xúc xắc thứ nhất và thứ hai. Biết tổng số chấm "
                  f"bằng {s}, tính xác suất {ask}.",
        answer=num(Fraction(len(good), len(pairs))),
        solution_vi=[f"Biết tổng bằng {s}, chỉ còn các cặp đồng khả năng: {shown}; có {len(pairs)} cặp.",
                     f"Trong đó có {len(good)} cặp thỏa mãn.",
                     f"Xác suất có điều kiện là {len(good)}/{len(pairs)} = {num(Fraction(len(good), len(pairs)))}."])


# ------------------------------------------------------------------ công thức nhân
@generator("xs_g3_khong_hoan_lai")
def khong_hoan_lai(rng: random.Random) -> Draw:
    n = rng.randint(6, 12)
    d = rng.randint(1, min(4, n - 4))                     # n - d >= 4: the good ones never run out
    kind = rng.choice(["tat_ca_tot", "tot_roi_hong"])
    if kind == "tat_ca_tot":
        k = rng.randint(2, 3)
        factors = [Fraction(n - d - i, n - i) for i in range(k)]
        ask = f"cả {k} sản phẩm lấy ra đều là chính phẩm"
        lines = [f"Lần {i + 1}: còn {n - i} sản phẩm, trong đó {n - d - i} chính phẩm, xác suất {n - d - i}/{n - i}."
                 for i in range(k)]
    else:
        k = 2
        factors = [Fraction(n - d, n), Fraction(d, n - 1)]
        ask = "lần thứ nhất lấy được chính phẩm và lần thứ hai lấy được phế phẩm"
        lines = [f"Lần 1 lấy chính phẩm: {n - d}/{n}.",
                 f"Biết lần 1 đã lấy đi một chính phẩm, còn {n - 1} sản phẩm với {d} phế phẩm: {d}/{n - 1}."]
    p = math.prod(factors)
    return Draw(
        params={"n": n, "d": d, "k": k, "kind": kind},
        prompt_vi=f"Một lô có {n} sản phẩm, trong đó {d} phế phẩm. Lấy lần lượt {k} sản phẩm không hoàn lại. "
                  f"Tính xác suất {ask}.",
        answer=num(p),
        solution_vi=["Công thức nhân: xác suất của các lần lấy nối tiếp bằng tích các xác suất có điều kiện, "
                     "mỗi lần tính trên số sản phẩm còn lại.",
                     *lines,
                     f"Nhân lại: {' . '.join(paren(f) for f in factors)} = {num(p)}."])


# ------------------------------------------------------------------ sự kiện độc lập
SHOT_P = [Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(3, 5), Fraction(4, 5),
          Fraction(7, 10), Fraction(9, 10), Fraction(5, 6)]


@generator("xs_g3_doc_lap_ban")
def doc_lap_ban(rng: random.Random) -> Draw:
    p1, p2 = rng.choice(SHOT_P), rng.choice(SHOT_P)
    q1, q2 = 1 - p1, 1 - p2
    kind = rng.choice(["it_nhat_mot", "dung_mot", "khong_ai"])
    if kind == "it_nhat_mot":
        ans = 1 - q1 * q2
        ask = "có ít nhất một người bắn trúng"
        steps = [f"Sự kiện đối là cả hai cùng trượt: {num(q1)} . {num(q2)} = {num(q1 * q2)} (nhân vì độc lập).",
                 f"Xác suất cần tìm là 1 - {num(q1 * q2)} = {num(ans)}."]
    elif kind == "dung_mot":
        ans = p1 * q2 + q1 * p2
        ask = "có đúng một người bắn trúng"
        steps = ["Đúng một người trúng gồm hai trường hợp xung khắc: người 1 trúng, người 2 trượt; "
                 "hoặc người 1 trượt, người 2 trúng.",
                 f"{num(p1)} . {num(q2)} + {num(q1)} . {num(p2)} = {num(p1 * q2)} + {num(q1 * p2)} = {num(ans)}."]
    else:
        ans = q1 * q2
        ask = "cả hai người đều bắn trượt"
        steps = [f"Người 1 trượt với xác suất 1 - {num(p1)} = {num(q1)}, người 2 trượt với xác suất "
                 f"1 - {num(p2)} = {num(q2)}.",
                 f"Hai người bắn độc lập nên nhân: {num(q1)} . {num(q2)} = {num(ans)}."]
    return Draw(
        params={"p1": num(p1), "p2": num(p2), "kind": kind},
        prompt_vi=f"Hai xạ thủ cùng bắn một phát vào bia, độc lập với nhau. Xác suất bắn trúng của người thứ nhất "
                  f"là {num(p1)}, của người thứ hai là {num(p2)}. Tính xác suất {ask}.",
        answer=num(ans), solution_vi=steps)


DIE_A = {
    "chan": ("số chấm chẵn", (2, 4, 6)),
    "le": ("số chấm lẻ", (1, 3, 5)),
    "chia3": ("số chấm chia hết cho 3", (3, 6)),
    "nguyen_to": ("số chấm là số nguyên tố", (2, 3, 5)),
    "tu5": ("số chấm từ 5 trở lên", (5, 6)),
}


@generator("xs_g3_doc_lap_tf")
def doc_lap_tf(rng: random.Random) -> Draw:
    a = rng.choice(sorted(DIE_A))
    k = rng.randint(1, 5)
    a_set, b_set = set(DIE_A[a][1]), set(range(1, k + 1))
    ab = a_set & b_set
    indep = 6 * len(ab) == len(a_set) * len(b_set)
    pa, pb, pab = Fraction(len(a_set), 6), Fraction(len(b_set), 6), Fraction(len(ab), 6)
    return Draw(
        params={"a": a, "k": k},
        prompt_vi=f"Gieo một con xúc xắc cân đối. A là sự kiện ra {DIE_A[a][0]}, B là sự kiện số chấm nhỏ hơn "
                  f"hoặc bằng {k}. Hai sự kiện A và B độc lập.",
        answer=indep,
        solution_vi=[f"P(A) = {num(pa)}, P(B) = {num(pb)}, nên P(A) P(B) = {num(pa * pb)}.",
                     (f"AB = {{{', '.join(map(str, sorted(ab)))}}}, nên P(AB) = {num(pab)}." if ab
                      else "A và B không có kết quả chung, nên P(AB) = 0."),
                     f"P(AB) {'=' if indep else '!='} P(A) P(B), nên A và B "
                     f"{'độc lập' if indep else 'không độc lập'}."])


# ------------------------------------------------------------------ công thức Bernoulli
# p -> how the trial is told
BERNOULLI = {
    "1/2": ("tung một đồng xu cân đối", "ra mặt ngửa", "lần tung"),
    "1/4": ("trả lời ngẫu nhiên một câu trắc nghiệm có 4 phương án, trong đó đúng 1 phương án đúng",
            "trả lời đúng", "câu"),
    "1/6": ("gieo một con xúc xắc cân đối", "ra mặt 6", "lần gieo"),
    "1/3": ("một xạ thủ bắn một phát, trúng với xác suất 1/3", "bắn trúng", "phát"),
    "2/3": ("một xạ thủ bắn một phát, trúng với xác suất 2/3", "bắn trúng", "phát"),
    "1/5": ("một sản phẩm của máy là phế phẩm với xác suất 1/5", "là phế phẩm", "sản phẩm"),
}


def _bernoulli_setup(rng: random.Random):
    key = rng.choice(sorted(BERNOULLI))
    p = Fraction(key)
    act, success, unit = BERNOULLI[key]
    return key, p, act, success, unit


def _term(n: int, k: int, p: Fraction) -> Fraction:
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


@generator("xs_g3_bernoulli")
def bernoulli(rng: random.Random) -> Draw:
    key, p, act, success, unit = _bernoulli_setup(rng)
    n = rng.randint(3, 6)
    k = rng.randint(0, n)
    ans = _term(n, k, p)
    return Draw(
        params={"p": key, "n": n, "k": k},
        prompt_vi=f"Một phép thử là: {act}. Làm phép thử đó {n} lần độc lập. Tính xác suất có đúng {k} {unit} "
                  f"{success}.",
        answer=num(ans),
        solution_vi=[f"Đây là {n} phép thử Bernoulli với xác suất thành công p = {key} ở mỗi lần.",
                     f"Công thức Bernoulli: P = C({n}, {k}) p^{k} (1 - p)^{n - k}.",
                     f"P = {math.comb(n, k)} . ({key})^{k} . ({num(1 - p)})^{n - k} = {num(ans)}."])


@generator("xs_g3_bernoulli_it_nhat")
def bernoulli_it_nhat(rng: random.Random) -> Draw:
    key, p, act, success, unit = _bernoulli_setup(rng)
    n = rng.randint(3, 6)
    k = rng.randint(1, n)
    ans = sum(_term(n, j, p) for j in range(k, n + 1))
    below = 1 - ans
    if k == 1:
        how = [f"Sự kiện đối là không {unit} nào {success}: (1 - p)^{n} = ({num(1 - p)})^{n} = {num(below)}.",
               f"Xác suất cần tìm là 1 - {num(below)} = {num(ans)}."]
    else:
        terms = " + ".join(num(_term(n, j, p)) for j in range(k, n + 1))
        how = [f"Cộng các trường hợp xung khắc j = {k}, ..., {n}, mỗi trường hợp tính bằng C({n}, j) p^j (1 - p)^({n} - j).",
               f"P = {terms} = {num(ans)}."]
    return Draw(
        params={"p": key, "n": n, "k": k},
        prompt_vi=f"Một phép thử là: {act}. Làm phép thử đó {n} lần độc lập. Tính xác suất có ít nhất {k} {unit} "
                  f"{success}.",
        answer=num(ans),
        solution_vi=[f"Đây là {n} phép thử Bernoulli với p = {key}.", *how])
