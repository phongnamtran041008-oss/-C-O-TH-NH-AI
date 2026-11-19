"""Xác Suất và Thống Kê, tầng 4 (hệ đầy đủ, sơ đồ cây, công thức xác suất đầy đủ, Bayes): generators.

The answers here come from the formulas of the floor (product along a branch, the total
probability sum, Bayes' quotient); tools/math_verify_xs_t4.py recomputes them another way:
by counting a population of products or people, by listing every (box, ball) outcome with
its weight, or with sympy sets."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, num, paren

FACES = (1, 2, 3, 4, 5, 6)


def _set(xs) -> str:
    return "{" + ", ".join(str(x) for x in sorted(xs)) + "}"


# ------------------------------------------------------------------ hệ đầy đủ
@generator("xs_g4_he_day_du_tf")
def he_day_du_tf(rng: random.Random) -> Draw:
    faces = list(FACES)
    rng.shuffle(faces)
    k = rng.randint(2, 4)
    cuts = sorted(rng.sample(range(1, 6), k - 1))
    groups = [sorted(faces[a:b]) for a, b in zip([0, *cuts], [*cuts, 6])]
    flaw = rng.choice(["none", "none", "thieu", "trung"])
    if flaw == "thieu":                       # drop one face from a group that keeps at least one
        g = next(g for g in groups if len(g) > 1) if any(len(g) > 1 for g in groups) else None
        if g is None:
            flaw = "none"
        else:
            g.remove(rng.choice(g))
    elif flaw == "trung":                     # one face also put in another group
        i, j = rng.sample(range(len(groups)), 2)
        extra = rng.choice([f for f in groups[i]])
        groups[j] = sorted(groups[j] + [extra])
    flat = sorted(f for g in groups for f in g)
    ok = flat == list(FACES)                  # every face exactly once
    names = ", ".join(f"H_{n + 1} = {_set(g)}" for n, g in enumerate(groups))
    if ok:
        why = ["Mỗi mặt từ 1 đến 6 nằm trong đúng một sự kiện của họ.",
               "Vậy các sự kiện đôi một xung khắc và tổng của chúng là sự kiện chắc chắn: đó là hệ đầy đủ."]
    elif len(flat) < 6:
        missing = sorted(set(FACES) - set(flat))
        why = [f"Mặt {', '.join(map(str, missing))} không thuộc sự kiện nào của họ.",
               "Tổng của các sự kiện không phải là sự kiện chắc chắn, nên họ này không là hệ đầy đủ."]
    else:
        twice = sorted({f for f in flat if flat.count(f) > 1})
        why = [f"Mặt {', '.join(map(str, twice))} thuộc hai sự kiện của họ.",
               "Hai sự kiện đó không xung khắc, nên họ này không là hệ đầy đủ."]
    return Draw(
        params={"groups": groups},
        prompt_vi=f"Gieo một con xúc xắc sáu mặt và ghi số chấm. Xét họ sự kiện {names}. "
                  f"Họ này là một hệ đầy đủ các sự kiện.",
        answer=ok,
        solution_vi=["Hệ đầy đủ: các sự kiện đôi một xung khắc và tổng của chúng là sự kiện chắc chắn.", *why])


# ------------------------------------------------------------------ sơ đồ cây
BOX_COLOURS = ("đỏ", "xanh")


@generator("xs_g4_cay_hai_hop")
def cay_hai_hop(rng: random.Random) -> Draw:
    k = rng.randint(1, 5)                     # faces 1..k choose box I
    r1, b1 = rng.randint(1, 5), rng.randint(1, 5)
    r2, b2 = rng.randint(1, 5), rng.randint(1, 5)
    box = rng.choice([1, 2])
    colour = rng.choice(["do", "xanh"])
    p_box = Fraction(k, 6) if box == 1 else Fraction(6 - k, 6)
    red, blue = (r1, b1) if box == 1 else (r2, b2)
    p_ball = Fraction(red if colour == "do" else blue, red + blue)
    ans = p_box * p_ball
    name = "I" if box == 1 else "II"
    cname = "đỏ" if colour == "do" else "xanh"
    rule = (f"ra mặt từ 1 đến {k}" if k > 1 else "ra mặt 1")
    return Draw(
        params={"k": k, "box1": [r1, b1], "box2": [r2, b2], "box": box, "colour": colour},
        prompt_vi=f"Hộp I có {r1} bi đỏ và {b1} bi xanh; hộp II có {r2} bi đỏ và {b2} bi xanh. Gieo một con xúc "
                  f"xắc cân đối: nếu {rule} thì chọn hộp I, còn lại chọn hộp II; rồi lấy ngẫu nhiên 1 bi từ hộp đã "
                  f"chọn. Tính xác suất chọn được hộp {name} và lấy được bi {cname}.",
        answer=num(ans),
        solution_vi=[f"Nhánh thứ nhất của sơ đồ cây: chọn hộp {name} với xác suất {num(p_box)}.",
                     f"Nhánh thứ hai: hộp {name} có {red} bi đỏ, {blue} bi xanh, nên lấy được bi {cname} với "
                     f"xác suất có điều kiện {num(p_ball)}.",
                     f"Nhân dọc đường đi: {paren(p_box)} . {paren(p_ball)} = {num(ans)}."])


# ------------------------------------------------------------------ công thức đầy đủ và Bayes
SHARES = {2: [(Fraction(1, 2), Fraction(1, 2)), (Fraction(3, 5), Fraction(2, 5)), (Fraction(2, 3), Fraction(1, 3)),
              (Fraction(3, 4), Fraction(1, 4)), (Fraction(7, 10), Fraction(3, 10))],
          3: [(Fraction(1, 2), Fraction(3, 10), Fraction(1, 5)), (Fraction(2, 5), Fraction(7, 20), Fraction(1, 4)),
              (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)), (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2))]}
RATES = [Fraction(1, 100), Fraction(1, 50), Fraction(1, 25), Fraction(1, 20), Fraction(3, 100),
         Fraction(1, 10), Fraction(2, 25), Fraction(3, 50)]
ROMAN = ("I", "II", "III")


def _factories(rng: random.Random):
    m = rng.choice([2, 3])
    shares = rng.choice(SHARES[m])
    rates = [rng.choice(RATES) for _ in range(m)]
    told = "; ".join(f"phân xưởng {ROMAN[i]} làm {num(s)} số sản phẩm, với tỉ lệ phế phẩm {num(r)}"
                     for i, (s, r) in enumerate(zip(shares, rates)))
    return shares, rates, told


@generator("xs_g4_day_du")
def day_du(rng: random.Random) -> Draw:
    shares, rates, told = _factories(rng)
    terms = [s * r for s, r in zip(shares, rates)]
    ans = sum(terms)
    return Draw(
        params={"shares": [num(s) for s in shares], "rates": [num(r) for r in rates]},
        prompt_vi=f"Một nhà máy có {len(shares)} phân xưởng: {told}. Lấy ngẫu nhiên một sản phẩm của nhà máy. "
                  f"Tính xác suất sản phẩm đó là phế phẩm.",
        answer=num(ans),
        solution_vi=["Hệ đầy đủ: H_i là sản phẩm do phân xưởng thứ i làm ra; A là sản phẩm là phế phẩm.",
                     "Công thức xác suất đầy đủ: P(A) = tổng của P(H_i) P(A|H_i).",
                     f"P(A) = {' + '.join(f'{paren(s)} . {paren(r)}' for s, r in zip(shares, rates))} "
                     f"= {' + '.join(num(t) for t in terms)} = {num(ans)}."])


@generator("xs_g4_bayes")
def bayes(rng: random.Random) -> Draw:
    shares, rates, told = _factories(rng)
    terms = [s * r for s, r in zip(shares, rates)]
    total = sum(terms)
    i = rng.randrange(len(shares))
    ans = terms[i] / total
    return Draw(
        params={"shares": [num(s) for s in shares], "rates": [num(r) for r in rates], "i": i},
        prompt_vi=f"Một nhà máy có {len(shares)} phân xưởng: {told}. Lấy ngẫu nhiên một sản phẩm của nhà máy và "
                  f"thấy nó là phế phẩm. Tính xác suất sản phẩm đó do phân xưởng {ROMAN[i]} làm ra.",
        answer=num(ans),
        solution_vi=["H_i: sản phẩm do phân xưởng thứ i làm ra; A: sản phẩm là phế phẩm.",
                     f"Công thức đầy đủ: P(A) = {' + '.join(num(t) for t in terms)} = {num(total)}.",
                     f"Công thức Bayes: P(H_{i + 1}|A) = P(H_{i + 1}) P(A|H_{i + 1}) / P(A) "
                     f"= {paren(terms[i])}/{paren(total)} = {num(ans)}."])


@generator("xs_g4_chuyen_bi")
def chuyen_bi(rng: random.Random) -> Draw:
    w1, k1 = rng.randint(1, 5), rng.randint(1, 5)
    w2, k2 = rng.randint(1, 5), rng.randint(1, 5)
    n1, n2 = w1 + k1, w2 + k2 + 1
    ph1, ph2 = Fraction(w1, n1), Fraction(k1, n1)
    pa1, pa2 = Fraction(w2 + 1, n2), Fraction(w2, n2)
    ans = ph1 * pa1 + ph2 * pa2
    return Draw(
        params={"box1": [w1, k1], "box2": [w2, k2]},
        prompt_vi=f"Hộp I có {w1} bi trắng và {k1} bi đen; hộp II có {w2} bi trắng và {k2} bi đen. Lấy ngẫu nhiên "
                  f"1 bi từ hộp I bỏ sang hộp II, rồi từ hộp II lấy ngẫu nhiên 1 bi. Tính xác suất bi lấy từ hộp II "
                  f"là bi trắng.",
        answer=num(ans),
        solution_vi=[f"Hệ đầy đủ theo bi được chuyển: H_1 là bi trắng, P(H_1) = {num(ph1)}; H_2 là bi đen, "
                     f"P(H_2) = {num(ph2)}.",
                     f"Sau khi chuyển, hộp II có {n2} bi: P(A|H_1) = {w2 + 1}/{n2}, P(A|H_2) = {w2}/{n2}.",
                     f"P(A) = {paren(ph1)} . {paren(pa1)} + {paren(ph2)} . {paren(pa2)} = {num(ans)}."])


PREVALENCE = [Fraction(1, 100), Fraction(1, 50), Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), Fraction(1, 1000)]
SENSITIVITY = [Fraction(9, 10), Fraction(19, 20), Fraction(99, 100), Fraction(4, 5), Fraction(1)]
FALSE_POS = [Fraction(1, 10), Fraction(1, 20), Fraction(1, 50), Fraction(1, 100), Fraction(3, 100)]


@generator("xs_g4_xet_nghiem")
def xet_nghiem(rng: random.Random) -> Draw:
    p, s, f = rng.choice(PREVALENCE), rng.choice(SENSITIVITY), rng.choice(FALSE_POS)
    sick, healthy = p * s, (1 - p) * f
    ans = sick / (sick + healthy)
    return Draw(
        params={"p": num(p), "s": num(s), "f": num(f)},
        prompt_vi=f"Một bệnh có tỉ lệ mắc trong cộng đồng là {num(p)}. Một xét nghiệm cho kết quả dương tính với "
                  f"xác suất {num(s)} nếu người được xét nghiệm mắc bệnh, và với xác suất {num(f)} nếu người đó "
                  f"không mắc bệnh. Chọn ngẫu nhiên một người trong cộng đồng, xét nghiệm và được kết quả dương "
                  f"tính. Tính xác suất người đó mắc bệnh.",
        answer=num(ans),
        solution_vi=["Hệ đầy đủ: B là mắc bệnh, P(B) = " + num(p) + "; không mắc bệnh có xác suất " + num(1 - p) + ".",
                     f"P(dương tính) = {paren(p)} . {paren(s)} + {paren(1 - p)} . {paren(f)} = {num(sick)} + "
                     f"{num(healthy)} = {num(sick + healthy)}.",
                     f"Bayes: P(B | dương tính) = {paren(sick)}/{paren(sick + healthy)} = {num(ans)}.",
                     "Tỉ lệ mắc bệnh (tỉ lệ nền) càng nhỏ thì số người khỏe bị dương tính nhầm càng lấn át."])
