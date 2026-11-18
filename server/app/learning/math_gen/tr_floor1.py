"""Tối Ưu và Toán Rời Rạc, floor 1 (cấu hình tổ hợp, quy tắc cộng và nhân, logic mệnh đề,
quy nạp): generators. Ids start with `tr_g1_`.

A proposition is kept as plain JSON so that it can sit in `Draw.params`: a variable is a
string ("p"), a compound is a list [op, a] or [op, a, b] with op one of not, and, or, imp,
iff. tools/math_verify_tr.py turns the same lists into sympy.logic expressions."""
from __future__ import annotations

import itertools
import random
from fractions import Fraction

from . import Draw, generator, num

WORD = {"and": "và", "or": "hoặc", "imp": "=>", "iff": "<=>"}
VALUE = {True: "đúng", False: "sai"}
RULE = {
    "not": "phủ định đổi chân trị",
    "and": "hội chỉ đúng khi cả hai vế đều đúng",
    "or": "tuyển chỉ sai khi cả hai vế đều sai",
    "imp": "kéo theo chỉ sai khi vế trước đúng và vế sau sai",
    "iff": "tương đương đúng khi hai vế cùng chân trị",
}


# ------------------------------------------------------------------ propositions
def ftext(f, top: bool = True) -> str:
    """The proposition as the game writes it: (không p) hoặc q, p => (q và r)."""
    if isinstance(f, str):
        return f
    if f[0] == "not":
        body = f"không {ftext(f[1], False)}"
    else:
        body = f"{ftext(f[1], False)} {WORD[f[0]]} {ftext(f[2], False)}"
    return body if top else f"({body})"


def value(f, env: dict) -> bool:
    if isinstance(f, str):
        return env[f]
    if f[0] == "not":
        return not value(f[1], env)
    a, b = value(f[1], env), value(f[2], env)
    if f[0] == "and":
        return a and b
    if f[0] == "or":
        return a or b
    if f[0] == "imp":
        return (not a) or b
    return a == b


def explain(f, env: dict) -> list[str]:
    """One line per compound part, inside out: the value of each part and the rule used."""
    lines: list[str] = []

    def walk(g) -> bool:
        if isinstance(g, str):
            return env[g]
        parts = [walk(x) for x in g[1:]]
        v = value(g, env)
        given = " và ".join(f"{ftext(x)} {VALUE[pv]}" for x, pv in zip(g[1:], parts))
        lines.append(f"{given}, mà {RULE[g[0]]}: {ftext(g)} {VALUE[v]}.")
        return v

    walk(f)
    return lines


def variables(f) -> list[str]:
    if isinstance(f, str):
        return [f]
    out: list[str] = []
    for x in f[1:]:
        out += [v for v in variables(x) if v not in out]
    return out


def env_text(env: dict) -> str:
    return ", ".join(f"{k} {VALUE[v]}" for k, v in env.items())


def _maybe_not(rng: random.Random, f, chance: float):
    return ["not", f] if rng.random() < chance else f


def _three_way(rng: random.Random):
    """A compound of p, q, r (each used once) with two binary connectives."""
    a, b, c = rng.sample(["p", "q", "r"], 3)
    op1, op2 = rng.choice(list(WORD)), rng.choice(list(WORD))
    a, b, c = (_maybe_not(rng, v, 0.25) for v in (a, b, c))
    if rng.random() < 0.5:
        return [op1, [op2, a, b], c]
    return [op1, a, [op2, b, c]]


# ------------------------------------------------------------------ mệnh đề và các phép nối
@generator("tr_g1_chan_tri")
def chan_tri(rng: random.Random) -> Draw:
    env = {"p": rng.random() < 0.5, "q": rng.random() < 0.5}
    op = rng.choice(list(WORD))
    left = _maybe_not(rng, "p", 0.3)
    right = _maybe_not(rng, "q", 0.3) if left == "p" else "q"
    f = [op, left, right]
    v = value(f, env)
    return Draw(
        params={"env": env, "f": f},
        prompt_vi=(f"Cho p là mệnh đề {VALUE[env['p']]} và q là mệnh đề {VALUE[env['q']]}. "
                   f"Mệnh đề {ftext(f)} đúng."),
        answer=v,
        solution_vi=[*explain(f, env),
                     f"Vậy mệnh đề {ftext(f)} {VALUE[v]}, nên câu đã cho {'đúng' if v else 'sai'}."])


@generator("tr_g1_chan_tri_hop")
def chan_tri_hop(rng: random.Random) -> Draw:
    env = {k: rng.random() < 0.5 for k in ("p", "q", "r")}
    f = _three_way(rng)
    v = value(f, env)
    return Draw(
        params={"env": env, "f": f},
        prompt_vi=f"Cho {env_text(env)}. Mệnh đề {ftext(f)} đúng.",
        answer=v,
        solution_vi=["Tính từ trong ngoặc ra ngoài.", *explain(f, env),
                     f"Vậy câu đã cho {'đúng' if v else 'sai'}."])


# ------------------------------------------------------------------ bảng chân trị và tương đương logic
_PAIRS = [
    (["imp", "p", "q"], ["or", ["not", "p"], "q"], "kéo theo viết lại bằng tuyển"),
    (["imp", "p", "q"], ["imp", "q", "p"], None),
    (["imp", "p", "q"], ["imp", ["not", "q"], ["not", "p"]], "mệnh đề phản đảo"),
    (["imp", "p", "q"], ["imp", ["not", "p"], ["not", "q"]], None),
    (["not", ["and", "p", "q"]], ["or", ["not", "p"], ["not", "q"]], "luật De Morgan"),
    (["not", ["and", "p", "q"]], ["and", ["not", "p"], ["not", "q"]], None),
    (["not", ["or", "p", "q"]], ["and", ["not", "p"], ["not", "q"]], "luật De Morgan"),
    (["not", ["or", "p", "q"]], ["or", ["not", "p"], ["not", "q"]], None),
    (["iff", "p", "q"], ["and", ["imp", "p", "q"], ["imp", "q", "p"]], "tương đương là kéo theo hai chiều"),
    (["not", ["imp", "p", "q"]], ["and", "p", ["not", "q"]], "phủ định của kéo theo"),
    (["not", ["imp", "p", "q"]], ["imp", ["not", "p"], ["not", "q"]], None),
    (["and", "p", ["or", "q", "r"]], ["or", ["and", "p", "q"], ["and", "p", "r"]], "luật phân phối"),
    (["or", "p", ["and", "q", "r"]], ["and", ["or", "p", "q"], "r"], None),
    (["not", ["iff", "p", "q"]], ["iff", ["not", "p"], "q"], "phủ định của tương đương"),
]


def _rename(f, names: dict):
    if isinstance(f, str):
        return names[f]
    return [f[0], *(_rename(x, names) for x in f[1:])]


def _rows(vs: list[str]):
    for bits in itertools.product([True, False], repeat=len(vs)):
        yield dict(zip(vs, bits))


@generator("tr_g1_tuong_duong")
def tuong_duong(rng: random.Random) -> Draw:
    x, y, law = rng.choice(_PAIRS)
    names = dict(zip(["p", "q", "r"], rng.choice([["p", "q", "r"], ["a", "b", "c"], ["q", "p", "r"]])))
    x, y = _rename(x, names), _rename(y, names)
    if rng.random() < 0.5:
        x, y = y, x
    vs = sorted(set(variables(x)) | set(variables(y)))
    bad = next((env for env in _rows(vs) if value(x, env) != value(y, env)), None)
    if bad is None:
        steps = [f"Lập bảng chân trị theo {', '.join(vs)}: ở mọi dòng hai mệnh đề có cùng chân trị.",
                 f"Đây chính là {law}.", "Vậy hai mệnh đề tương đương logic."]
    else:
        steps = [f"Chỉ cần một dòng của bảng chân trị mà hai mệnh đề khác chân trị: {env_text(bad)}.",
                 f"Khi đó {ftext(x)} {VALUE[value(x, bad)]}, còn {ftext(y)} {VALUE[value(y, bad)]}.",
                 "Vậy hai mệnh đề không tương đương logic."]
    return Draw(
        params={"x": x, "y": y},
        prompt_vi=f"Hai mệnh đề {ftext(x)} và {ftext(y)} tương đương logic.",
        answer=bad is None, solution_vi=steps)


@generator("tr_g1_dem_dong_dung")
def dem_dong_dung(rng: random.Random) -> Draw:
    f = _three_way(rng)
    rows = list(_rows(["p", "q", "r"]))
    good = [env for env in rows if value(f, env)]
    shown = "; ".join(f"({', '.join('Đ' if env[k] else 'S' for k in 'pqr')})" for env in good) or "không có dòng nào"
    return Draw(
        params={"f": f},
        prompt_vi=(f"Lập bảng chân trị của mệnh đề {ftext(f)} theo ba biến p, q, r. "
                   "Có bao nhiêu dòng mà mệnh đề đó đúng?"),
        answer=str(len(good)),
        solution_vi=["Ba biến cho 2 . 2 . 2 = 8 dòng, mỗi dòng là một bộ chân trị của (p, q, r).",
                     "Với từng dòng, tính phần trong ngoặc trước rồi đến phép nối ngoài cùng.",
                     f"Các dòng làm mệnh đề đúng, viết (p, q, r) với Đ là đúng, S là sai: {shown}.",
                     f"Có {len(good)} dòng."])


# ------------------------------------------------------------------ quy tắc cộng và quy tắc nhân
_PRODUCT_THEMES = [
    ("Một đan sư có {0} loại linh thảo chính, {1} loại phụ dược và {2} kiểu lò. Mỗi mẻ đan dùng "
     "một linh thảo chính, một phụ dược và một kiểu lò. Có bao nhiêu cách chọn cho một mẻ?",
     ["linh thảo chính", "phụ dược", "kiểu lò"]),
    ("Một bộ pháp y gồm một áo choàng, một đai lưng và một đôi giày. Kho có {0} áo choàng, {1} đai "
     "lưng và {2} đôi giày. Có bao nhiêu bộ pháp y khác nhau?",
     ["áo choàng", "đai lưng", "đôi giày"]),
    ("Một trận pháp cần một trận nhãn, một lá cờ và một viên linh thạch. Có {0} chỗ đặt trận nhãn, "
     "{1} lá cờ và {2} viên linh thạch khác nhau. Có bao nhiêu cách bày trận?",
     ["trận nhãn", "lá cờ", "linh thạch"]),
]


@generator("tr_g1_quy_tac_nhan")
def quy_tac_nhan(rng: random.Random) -> Draw:
    k = rng.randrange(len(_PRODUCT_THEMES))
    text, parts = _PRODUCT_THEMES[k]
    sizes = [rng.randint(2, 7) for _ in range(3)]
    total = sizes[0] * sizes[1] * sizes[2]
    return Draw(
        params={"theme": k, "sizes": sizes},
        prompt_vi=text.format(*sizes),
        answer=str(total),
        solution_vi=["Việc chọn gồm ba bước nối tiếp nhau, mỗi bước chọn một thứ.",
                     "; ".join(f"chọn {p}: {n} cách" for p, n in zip(parts, sizes)) + ".",
                     "Số cách ở mỗi bước không phụ thuộc vào lựa chọn ở bước trước, nên dùng quy tắc nhân.",
                     f"{sizes[0]} . {sizes[1]} . {sizes[2]} = {total}."])


@generator("tr_g1_quy_tac_cong")
def quy_tac_cong(rng: random.Random) -> Draw:
    a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(1, 5)
    total = a * b + c
    return Draw(
        params={"ab": a, "bc": b, "ac": c},
        prompt_vi=(f"Từ động phủ A đến trấn B có {a} con đường, từ trấn B đến tông môn C có {b} con đường, "
                   f"và có {c} con đường đi thẳng từ A đến C không qua B. Có bao nhiêu cách đi từ A đến C?"),
        answer=str(total),
        solution_vi=["Chia thành hai trường hợp rời nhau: đi qua B, hoặc đi thẳng không qua B.",
                     f"Đi qua B: chọn đường A đến B rồi đường B đến C, theo quy tắc nhân có {a} . {b} = {a * b} cách.",
                     f"Đi thẳng: có {c} cách.",
                     f"Hai trường hợp không có cách đi nào chung, theo quy tắc cộng: {a * b} + {c} = {total}."])


# ------------------------------------------------------------------ cấu hình tổ hợp
_BINARY_KINDS = {
    "all": ("", lambda n: 2 ** n),
    "start1": (" bắt đầu bằng chữ số 1", lambda n: 2 ** (n - 1)),
    "same_ends": (" có chữ số đầu và chữ số cuối giống nhau", lambda n: 2 ** (n - 1)),
    "end01": (" kết thúc bằng 01", lambda n: 2 ** (n - 2)),
}


@generator("tr_g1_xau_nhi_phan")
def xau_nhi_phan(rng: random.Random) -> Draw:
    kind = rng.choice(list(_BINARY_KINDS))
    n = rng.randint(3, 9)
    words, count = _BINARY_KINDS[kind]
    value_ = count(n)
    free = {"all": n, "start1": n - 1, "same_ends": n - 1, "end01": n - 2}[kind]
    why = {"all": f"Mỗi vị trí trong {n} vị trí có 2 cách: 0 hoặc 1.",
           "start1": f"Vị trí đầu đã cố định là 1, còn {n - 1} vị trí tự do.",
           "same_ends": f"Chọn tự do {n - 1} vị trí đầu; chữ số cuối buộc phải bằng chữ số đầu nên chỉ có 1 cách.",
           "end01": f"Hai vị trí cuối đã cố định là 0 rồi 1, còn {n - 2} vị trí tự do."}[kind]
    return Draw(
        params={"kind": kind, "n": n},
        prompt_vi=f"Có bao nhiêu xâu nhị phân độ dài {n}{words}?",
        answer=str(value_),
        solution_vi=["Một xâu nhị phân độ dài n là một dãy n chữ số, mỗi chữ số là 0 hoặc 1.", why,
                     f"Theo quy tắc nhân có 2^{free} = {value_} xâu."])


_ALPHABET_KINDS = {
    "same_ends": "có chữ cái đầu và chữ cái cuối giống nhau",
    "no_repeat_neighbour": "không có hai chữ cái giống nhau đứng liền nhau",
    "no_a": "không chứa chữ A",
}


@generator("tr_g1_dem_cau_hinh")
def dem_cau_hinh(rng: random.Random) -> Draw:
    kind = rng.choice(list(_ALPHABET_KINDS))
    k, n = rng.randint(2, 5), rng.randint(3, 5)
    letters = "ABCDE"[:k]
    if kind == "same_ends":
        total = k ** (n - 1)
        steps = [f"Chọn tự do {n - 1} chữ cái đầu: {k}^{n - 1} cách.",
                 "Chữ cái cuối buộc phải bằng chữ cái đầu: 1 cách.",
                 f"Theo quy tắc nhân có {k}^{n - 1} = {total} xâu."]
    elif kind == "no_repeat_neighbour":
        total = k * (k - 1) ** (n - 1)
        steps = [f"Chữ cái đầu có {k} cách chọn.",
                 f"Mỗi chữ cái sau chỉ cần khác chữ cái đứng ngay trước nó: {k - 1} cách.",
                 f"Theo quy tắc nhân có {k} . {k - 1}^{n - 1} = {total} xâu."]
    else:
        total = (k - 1) ** n
        steps = [f"Mỗi vị trí chỉ được dùng {k - 1} chữ cái khác A.",
                 f"Theo quy tắc nhân có {k - 1}^{n} = {total} xâu."]
    return Draw(
        params={"kind": kind, "k": k, "n": n},
        prompt_vi=(f"Một bảng chữ gồm {k} chữ cái {', '.join(letters)}. Có bao nhiêu xâu độ dài {n} "
                   f"lập từ các chữ cái đó (được lặp lại) mà {_ALPHABET_KINDS[kind]}?"),
        answer=str(total),
        solution_vi=["Lập xâu từ trái sang phải, đếm số cách ở mỗi vị trí.", *steps])


# ------------------------------------------------------------------ quy nạp
_SUMS_1 = {
    "natural": ("1 + 2 + 3 + ... + n = n(n + 1)/2", lambda n: f"1 + 2 + 3 + ... + {n}",
                lambda n: Fraction(n * (n + 1), 2), lambda n: f"{n} . {n + 1}/2"),
    "odd": ("1 + 3 + 5 + ... + (2n - 1) = n^2", lambda n: f"1 + 3 + 5 + ... + {2 * n - 1}",
            lambda n: Fraction(n * n), lambda n: f"{n}^2"),
    "even": ("2 + 4 + 6 + ... + 2n = n(n + 1)", lambda n: f"2 + 4 + 6 + ... + {2 * n}",
             lambda n: Fraction(n * (n + 1)), lambda n: f"{n} . {n + 1}"),
}

_SUMS_2 = {
    "squares": ("1^2 + 2^2 + ... + n^2 = n(n + 1)(2n + 1)/6", lambda n: f"1^2 + 2^2 + ... + {n}^2",
                lambda n: Fraction(n * (n + 1) * (2 * n + 1), 6), lambda n: f"{n} . {n + 1} . {2 * n + 1}/6"),
    "cubes": ("1^3 + 2^3 + ... + n^3 = (n(n + 1)/2)^2", lambda n: f"1^3 + 2^3 + ... + {n}^3",
              lambda n: Fraction(n * (n + 1), 2) ** 2, lambda n: f"({n} . {n + 1}/2)^2"),
    "products": ("1 . 2 + 2 . 3 + ... + n(n + 1) = n(n + 1)(n + 2)/3",
                 lambda n: f"1 . 2 + 2 . 3 + ... + {n} . {n + 1}",
                 lambda n: Fraction(n * (n + 1) * (n + 2), 3), lambda n: f"{n} . {n + 1} . {n + 2}/3"),
    "powers": ("1 + 2 + 4 + ... + 2^(n - 1) = 2^n - 1", lambda n: f"1 + 2 + 4 + ... + 2^{n - 1}",
               lambda n: Fraction(2 ** n - 1), lambda n: f"2^{n} - 1"),
    "telescoping": ("1/(1 . 2) + 1/(2 . 3) + ... + 1/(n(n + 1)) = n/(n + 1)",
                    lambda n: f"1/(1 . 2) + 1/(2 . 3) + ... + 1/({n} . {n + 1})",
                    lambda n: Fraction(n, n + 1), lambda n: f"{n}/{n + 1}"),
}


def _sum_draw(rng: random.Random, table: dict, lo: int, hi: int) -> Draw:
    kind = rng.choice(list(table))
    n = rng.randint(lo, hi)
    formula, shown, val, work = table[kind]
    total = val(n)
    return Draw(
        params={"kind": kind, "n": n},
        prompt_vi=(f"Bằng quy nạp ta chứng minh được {formula} với mọi n >= 1. "
                   f"Dùng công thức đó, tính {shown(n)}."),
        answer=num(total),
        solution_vi=[f"Tổng cần tính là vế trái của công thức với n = {n}.",
                     f"Thay n = {n} vào vế phải: {work(n)} = {num(total)}.",
                     "Có thể thử lại công thức với n = 1 hay n = 2 để chắc chắn đã chép đúng."])


@generator("tr_g1_tong_quy_nap")
def tong_quy_nap(rng: random.Random) -> Draw:
    return _sum_draw(rng, _SUMS_1, 5, 40)


@generator("tr_g1_tong_quy_nap_2")
def tong_quy_nap_2(rng: random.Random) -> Draw:
    return _sum_draw(rng, _SUMS_2, 4, 12)
