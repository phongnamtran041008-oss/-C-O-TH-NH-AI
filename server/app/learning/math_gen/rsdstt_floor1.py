"""Đại Số Tuyến Tính: generators added by the curriculum review (tools/audit_curriculum.py found
these micro-skill x tier cells with only two or three hand-written questions and no generator, so a
learner met the same question again within a few answers). Ids start with `dstt_gx_`; each one
sits on the tier the cell is asked at. Matrices are sent as figures (Draw.matrices).
tools/math_verify_rasoat.py redoes every answer with sympy (Matrix products, rank, solve)."""
from __future__ import annotations

import random

from . import Draw, generator, linear_text, matrix, nonzero, num, nums, paren, vec_text

BY_ROWS = "Nhập các phần tử theo từng hàng, cách nhau bằng dấu phẩy."


def _mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _flat(m) -> list:
    return [v for row in m for v in row]


def _det2(m) -> int:
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def _inv2(m):
    """Inverse of an integer 2 x 2 matrix with determinant +-1 (still integers)."""
    d = _det2(m)
    return [[m[1][1] * d, -m[0][1] * d], [-m[1][0] * d, m[0][0] * d]]


def _unimodular(rng: random.Random) -> list[list[int]]:
    """An integer 2 x 2 matrix with determinant 1 or -1, small entries, not the identity."""
    while True:
        a, b, c = rng.randint(-2, 3), rng.randint(-2, 3), rng.randint(-2, 3)
        # d from a d - b c = +-1
        sign = rng.choice([1, -1])
        if a == 0:
            continue
        if (sign + b * c) % a:
            continue
        d = (sign + b * c) // a
        m = [[a, b], [c, d]]
        if m != [[1, 0], [0, 1]] and all(abs(v) <= 4 for v in _flat(m)):
            return m


# ------------------------------------------------------------------ floor 4
@generator("dstt_gx_tvh_tim_m")
def tvh_tim_m(rng: random.Random) -> Draw:
    """Tier 3: the dot product of two feature vectors is given; find the unknown coordinate."""
    m = rng.randint(-6, 6)
    a, b = rng.randint(-5, 5), rng.randint(-5, 5)
    c = nonzero(rng, -4, 4)
    d, e = rng.randint(-5, 5), rng.randint(-5, 5)
    k = m * c + a * d + b * e
    rest = a * d + b * e
    return Draw(
        params={"a": a, "b": b, "c": c, "d": d, "e": e, "k": k},
        prompt_vi=f"Hai bài viết được biểu diễn bằng hai vectơ đặc trưng u = (m, {a}, {b}) và v = ({c}, {d}, {e}). "
                  f"Độ giống nhau của chúng, tức tích vô hướng u . v, bằng {k}. Tìm m.",
        answer=str(m),
        solution_vi=[f"u . v = m . {paren(c)} + {paren(a)} . {paren(d)} + {paren(b)} . {paren(e)} = "
                     f"{c}m + {rest}.",
                     f"Đặt {c}m + {rest} = {k}, suy ra {c}m = {k - rest}.",
                     f"Vậy m = {k - rest}/{c} = {m}."])


@generator("dstt_gx_ab_tru_ba")
def ab_tru_ba(rng: random.Random) -> Draw:
    """Tier 2: one entry of AB - BA, to feel that AB != BA."""
    while True:
        a, b = matrix(rng, 2, 2, -3, 4), matrix(rng, 2, 2, -3, 4)
        ab, ba = _mul(a, b), _mul(b, a)
        if ab != ba:
            break
    i, j = rng.randint(1, 2), rng.randint(1, 2)
    value = ab[i - 1][j - 1] - ba[i - 1][j - 1]
    return Draw(
        params={"a": a, "b": b, "i": i, "j": j},
        prompt_vi=f"Cho hai ma trận A và B như hình. Tính phần tử ở hàng {i}, cột {j} của AB - BA.",
        answer=str(value),
        solution_vi=[f"(AB) hàng {i} cột {j} = {' + '.join(f'{paren(a[i - 1][k])} . {paren(b[k][j - 1])}' for k in range(2))}"
                     f" = {ab[i - 1][j - 1]}.",
                     f"(BA) hàng {i} cột {j} = {' + '.join(f'{paren(b[i - 1][k])} . {paren(a[k][j - 1])}' for k in range(2))}"
                     f" = {ba[i - 1][j - 1]}.",
                     f"Hiệu: {ab[i - 1][j - 1]} - {paren(ba[i - 1][j - 1])} = {value}. "
                     f"(AB = {nums(_flat(ab))}; BA = {nums(_flat(ba))}: hai ma trận này khác nhau.)"],
        matrices={"A": a, "B": b})


# ------------------------------------------------------------------ floor 7
@generator("dstt_gx_con_khong_gian")
def con_khong_gian(rng: random.Random) -> Draw:
    """Tier 5, true/false: is W a subspace of R^2 or R^3? (zero vector, sums and scalar multiples)"""
    kind = rng.choice(["line", "shifted", "product", "halfplane", "plane3", "shifted3", "square"])
    a, b = nonzero(rng, -4, 4), nonzero(rng, -4, 4)
    c = nonzero(rng, -5, 5)
    if kind == "line":
        text = f"{a}x + {b}y = 0".replace("+ -", "- ")
        space, ok = "R^2", True
        why = ["Có (0, 0): 0a + 0b = 0, nên W không rỗng.",
               "Cộng hai nghiệm của một phương trình thuần nhất vẫn là nghiệm, nhân một nghiệm với số thực cũng vậy.",
               "Vậy W đóng với phép cộng và nhân vô hướng: W là không gian con."]
    elif kind == "shifted":
        text, space, ok = f"{a}x + {b}y = {c}".replace("+ -", "- "), "R^2", False
        why = [f"Thử vectơ không: {a} . 0 + {b} . 0 = 0, khác {c}.",
               "Vectơ không không thuộc W, nên W không thể là không gian con (hoặc: tổng hai phần tử của W "
               f"cho vế trái bằng 2 . {c}, không phải {c})."]
    elif kind == "product":
        text, space, ok = "x . y = 0", "R^2", False
        why = ["(1, 0) và (0, 1) đều thuộc W vì x . y = 0.", "Tổng của chúng là (1, 1), có x . y = 1, khác 0.",
               "W không đóng với phép cộng nên không là không gian con."]
    elif kind == "halfplane":
        text, space, ok = "x >= 0", "R^2", False
        why = ["(1, 0) thuộc W vì x = 1 >= 0.", "Nhân với -1 được (-1, 0), có x = -1 < 0, không thuộc W.",
               "W không đóng với phép nhân vô hướng nên không là không gian con."]
    elif kind == "plane3":
        text, space, ok = f"{a}x + {b}y - {abs(c)}z = 0".replace("- -", "+ ").replace("+ -", "- "), "R^3", True
        why = ["Một mặt phẳng đi qua gốc tọa độ: có vectơ không.",
               "Cộng hai nghiệm, hoặc nhân một nghiệm với số thực, vẫn thỏa phương trình thuần nhất.",
               "Vậy W là không gian con của R^3."]
    elif kind == "shifted3":
        text, space, ok = f"x + y + z = {abs(c)}", "R^3", False
        why = [f"Vectơ không có x + y + z = 0, khác {abs(c)}: không thuộc W.",
               "Không có vectơ không thì W không là không gian con."]
    else:
        text, space, ok = "y = x^2", "R^2", False
        why = ["(1, 1) thuộc W vì 1 = 1^2.", "Nhân đôi được (2, 2): 2 khác 2^2 = 4, nên không thuộc W.",
               "W không đóng với phép nhân vô hướng."]
    var = "(x, y, z)" if space == "R^3" else "(x, y)"
    return Draw(
        params={"kind": kind, "a": a, "b": b, "c": abs(c)},
        prompt_vi=f"Tập W = {{{var} thuộc {space} : {text}}} là một không gian con của {space}.",
        answer=ok,
        solution_vi=why)


@generator("dstt_gx_thuoc_bao_tuyen_tinh")
def thuoc_bao_tuyen_tinh(rng: random.Random) -> Draw:
    """Tier 5: w = (w1, m, w3) lies in span{u, v}; find m."""
    while True:
        u, v = [rng.randint(-3, 4) for _ in range(3)], [rng.randint(-3, 4) for _ in range(3)]
        if u[0] * v[2] - u[2] * v[0] != 0:
            break
    s, t = nonzero(rng, -3, 3), nonzero(rng, -3, 3)
    w = [s * u[i] + t * v[i] for i in range(3)]
    m = w[1]
    return Draw(
        params={"u": u, "v": v, "w1": w[0], "w3": w[2], "m": m},
        prompt_vi=f"Trong R^3 cho u = {vec_text(u)}, v = {vec_text(v)} và w = ({w[0]}, m, {w[2]}). Tìm m để w thuộc "
                  f"span{{u, v}} (bao tuyến tính của u và v).",
        answer=str(m),
        solution_vi=["w thuộc span{u, v} khi w = s u + t v với hai số thực s, t.",
                     f"Tọa độ thứ nhất và thứ ba: {u[0]}s + {paren(v[0])}t = {w[0]} và "
                     f"{u[2]}s + {paren(v[2])}t = {w[2]}.".replace("+ -", "- "),
                     f"Giải hệ này được s = {s}, t = {t}.",
                     f"Tọa độ thứ hai: m = {u[1]} . {paren(s)} + {paren(v[1])} . {paren(t)} = {m}."])


@generator("dstt_gx_toa_do_doi_co_so")
def toa_do_doi_co_so(rng: random.Random) -> Draw:
    """Tier 5: coordinates in B are given; find them in B'."""
    while True:
        pb = _unimodular(rng)
        pc = [[rng.randint(-2, 3), rng.randint(-2, 3)], [rng.randint(-2, 3), rng.randint(-2, 3)]]
        if _det2(pc) != 0:
            break
    p, q = nonzero(rng, -3, 3), nonzero(rng, -3, 3)
    b1, b2 = [pb[0][0], pb[1][0]], [pb[0][1], pb[1][1]]
    c1, c2 = [pc[0][0], pc[1][0]], [pc[0][1], pc[1][1]]
    x = [p * b1[0] + q * b2[0], p * b1[1] + q * b2[1]]
    d = _det2(pc)
    from fractions import Fraction
    r = Fraction(x[0] * pc[1][1] - x[1] * pc[0][1], d)
    s = Fraction(pc[0][0] * x[1] - pc[1][0] * x[0], d)
    return Draw(
        params={"b1": b1, "b2": b2, "c1": c1, "c2": c2, "p": p, "q": q},
        prompt_vi=f"Trong R^2 có cơ sở B = {{b1 = {vec_text(b1)}, b2 = {vec_text(b2)}}} và cơ sở B' = "
                  f"{{c1 = {vec_text(c1)}, c2 = {vec_text(c2)}}}. Vectơ x có tọa độ trong B là [x]_B = ({p}, {q}). "
                  f"Tìm tọa độ [x]_B' của x trong B'. Nhập hai số, cách nhau bằng dấu phẩy.",
        answer=nums([r, s]),
        solution_vi=[f"Đổi về tọa độ chính tắc: x = {p} b1 + {paren(q)} b2 = {vec_text(x)}.",
                     f"Cần r, s với r c1 + s c2 = x, tức hệ {c1[0]}r + {paren(c2[0])}s = {x[0]} và "
                     f"{c1[1]}r + {paren(c2[1])}s = {x[1]}.".replace("+ -", "- "),
                     f"Định thức của hệ là {d} (khác 0, nên B' là cơ sở). Giải được r = {num(r)}, s = {num(s)}.",
                     f"Vậy [x]_B' = ({num(r)}, {num(s)})."])


# ------------------------------------------------------------------ floor 8
@generator("dstt_gx_doi_co_so_ma_tran")
def doi_co_so_ma_tran(rng: random.Random) -> Draw:
    """Tier 5: B = P^-1 A P with P of determinant +-1 (so every entry is a whole number)."""
    a = matrix(rng, 2, 2, -3, 4)
    p = _unimodular(rng)
    pinv = _inv2(p)
    b = _mul(_mul(pinv, a), p)
    ap = _mul(a, p)
    return Draw(
        params={"a": a, "p": p},
        prompt_vi=f"Ánh xạ f: R^2 -> R^2 có ma trận chính tắc A như hình. Cơ sở mới của R^2 gồm hai cột của P như "
                  f"hình. Tìm ma trận B của f trong cơ sở mới, B = P^(-1) A P. {BY_ROWS}",
        answer=nums(_flat(b)),
        solution_vi=[f"AP = {nums(_flat(ap))} (theo từng hàng).",
                     f"det P = {_det2(p)}, nên P^(-1) = {nums(_flat(pinv))} (theo từng hàng): các phần tử đều nguyên.",
                     f"B = P^(-1)(AP) = {nums(_flat(b))} (theo từng hàng)."],
        matrices={"A": a, "P": p})


@generator("dstt_gx_hop_anh_xa_gia_tri")
def hop_anh_xa_gia_tri(rng: random.Random) -> Draw:
    """Tier 5: (g o f)(p, q) for two linear maps R^2 -> R^2, through the product of their matrices."""
    af = [[nonzero(rng, -3, 4) for _ in range(2)] for _ in range(2)]
    ag = [[nonzero(rng, -3, 4) for _ in range(2)] for _ in range(2)]
    p, q = rng.randint(-4, 5), rng.randint(-4, 5)

    def text(m):
        return f"({linear_text(m[0][0], 0, 'x')} {'+' if m[0][1] >= 0 else '-'} {abs(m[0][1])}y, " \
               f"{linear_text(m[1][0], 0, 'x')} {'+' if m[1][1] >= 0 else '-'} {abs(m[1][1])}y)"
    prod = _mul(ag, af)
    out = [prod[0][0] * p + prod[0][1] * q, prod[1][0] * p + prod[1][1] * q]
    return Draw(
        params={"af": af, "ag": ag, "p": p, "q": q},
        prompt_vi=f"Hai ánh xạ tuyến tính R^2 -> R^2: f(x, y) = {text(af)} và g(x, y) = {text(ag)}. Tính "
                  f"(g o f)({p}, {q}), nghĩa là g(f({p}, {q})). Nhập hai số, cách nhau bằng dấu phẩy.",
        answer=nums(out),
        solution_vi=[f"Ma trận của f là A_f = {nums(_flat(af))} và của g là A_g = {nums(_flat(ag))} (theo từng hàng).",
                     f"Ma trận của g o f là tích A_g A_f = {nums(_flat(prod))} (theo từng hàng).",
                     f"(g o f)({p}, {q}) = ({prod[0][0]} . {paren(p)} + {paren(prod[0][1])} . {paren(q)}, "
                     f"{prod[1][0]} . {paren(p)} + {paren(prod[1][1])} . {paren(q)}) = ({out[0]}, {out[1]})."],
        )


def _low_rank(rng: random.Random, rows: int, cols: int, rank: int) -> list[list[int]]:
    while True:
        left, right = matrix(rng, rows, rank, -2, 3), matrix(rng, rank, cols, -2, 3)
        m = _mul(left, right)
        from sympy import Matrix
        if Matrix(m).rank() == rank:
            return m


@generator("dstt_gx_nhan_va_anh")
def nhan_va_anh(rng: random.Random) -> Draw:
    """Tier 5: dim Ker f and dim Im f of the map x -> Ax."""
    rows, cols = rng.choice([(3, 4), (3, 3), (2, 4), (4, 3), (4, 4)])
    rank = rng.randint(1, min(rows, cols) - (1 if rows == cols else 0))
    m = _low_rank(rng, rows, cols, rank)
    return Draw(
        params={"m": m, "rank": rank},
        prompt_vi=f"Ánh xạ tuyến tính f: R^{cols} -> R^{rows} có f(x) = Ax với A như hình. Tìm dim Ker f và dim Im f. "
                  f"Nhập hai số theo thứ tự đó, cách nhau bằng dấu phẩy.",
        answer=nums([cols - rank, rank]),
        solution_vi=["Đưa A về dạng bậc thang bằng các phép biến đổi hàng: số hàng khác không còn lại là hạng của A.",
                     f"Ở đây rank A = {rank}, và dim Im f = rank A = {rank}.",
                     f"Định lý số chiều: dim Ker f + dim Im f = {cols} (số cột của A), nên dim Ker f = {cols} - {rank} = {cols - rank}."],
        matrices={"A": m})


@generator("dstt_gx_so_chieu_nhan")
def so_chieu_nhan(rng: random.Random) -> Draw:
    """Tier 5: from the rank-nullity theorem: given two of (dim domain, dim Ker, dim Im) find the third."""
    n = rng.randint(4, 8)
    r = rng.randint(1, n - 1)
    ask = rng.choice(["ker", "im", "n"])
    k = n - r
    if ask == "ker":
        q = f"f: R^{n} -> R^m là ánh xạ tuyến tính có dim Im f = {r}. Tìm dim Ker f."
        ans, steps = k, f"dim Ker f = {n} - {r} = {k}."
    elif ask == "im":
        q = f"f: R^{n} -> R^m là ánh xạ tuyến tính có dim Ker f = {k}. Tìm dim Im f."
        ans, steps = r, f"dim Im f = {n} - {k} = {r}."
    else:
        q = f"f: R^n -> R^m là ánh xạ tuyến tính có dim Ker f = {k} và dim Im f = {r}. Tìm n."
        ans, steps = n, f"n = {k} + {r} = {n}."
    return Draw(
        params={"n": n, "r": r, "ask": ask},
        prompt_vi=q,
        answer=str(ans),
        solution_vi=["Định lý số chiều: dim Ker f + dim Im f = số chiều của không gian nguồn.", steps])
