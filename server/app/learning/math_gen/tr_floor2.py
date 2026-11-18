"""Tối Ưu và Toán Rời Rạc, floor 2 (bài toán đếm): generators. Ids start with `tr_g2_`.

Every answer here comes from a closed formula (n^k, A_n^k, C_n^k, bù trừ, a recurrence run
forward); tools/math_verify_tr.py recounts by listing the configurations or by sympy."""
from __future__ import annotations

import math
import random

from . import Draw, generator


def _fact_text(n: int) -> str:
    return " . ".join(str(v) for v in range(n, 0, -1))


# ------------------------------------------------------------------ chỉnh hợp
@generator("tr_g2_chinh_hop_lap")
def chinh_hop_lap(rng: random.Random) -> Draw:
    n, k = rng.randint(2, 9), rng.randint(2, 4)
    total = n ** k
    return Draw(
        params={"n": n, "k": k},
        prompt_vi=(f"Một mật lệnh gồm {k} ký tự viết liền nhau, mỗi ký tự là một trong {n} phù văn và "
                   "một phù văn được dùng nhiều lần. Có bao nhiêu mật lệnh khác nhau?"),
        answer=str(total),
        solution_vi=[f"Mật lệnh là một dãy có thứ tự {k} ký tự, được lặp lại: một chỉnh hợp lặp chập {k} của {n}.",
                     f"Mỗi vị trí có {n} cách chọn, không phụ thuộc các vị trí khác.",
                     f"Số mật lệnh là {n}^{k} = {total}."])


@generator("tr_g2_chinh_hop")
def chinh_hop(rng: random.Random) -> Draw:
    n, k = rng.randint(5, 12), rng.randint(2, 4)
    total = math.perm(n, k)
    roles = ["chưởng môn", "đại trưởng lão", "nhị trưởng lão", "chấp sự"][:k]
    return Draw(
        params={"n": n, "k": k},
        prompt_vi=(f"Từ {n} đệ tử, chọn ra {k} người giữ {k} chức vụ khác nhau ({', '.join(roles)}), "
                   "mỗi người giữ một chức. Có bao nhiêu cách?"),
        answer=str(total),
        solution_vi=[f"Chức vụ khác nhau nên thứ tự chọn có ý nghĩa, và một người không giữ hai chức: "
                     f"đây là chỉnh hợp không lặp chập {k} của {n}.",
                     f"Chức thứ nhất có {n} cách, mỗi chức sau ít hơn một cách.",
                     f"A_{n}^{k} = {' . '.join(str(n - i) for i in range(k))} = {total}."])


# ------------------------------------------------------------------ hoán vị
_ROW_THEMES = ["đệ tử thành một hàng dọc", "cuốn bí kíp khác nhau lên một giá sách", "lá cờ khác màu thành một hàng"]


@generator("tr_g2_hoan_vi")
def hoan_vi(rng: random.Random) -> Draw:
    n, theme = rng.randint(3, 8), rng.randrange(len(_ROW_THEMES))
    total = math.factorial(n)
    return Draw(
        params={"n": n, "theme": theme},
        prompt_vi=f"Có bao nhiêu cách xếp {n} {_ROW_THEMES[theme]}?",
        answer=str(total),
        solution_vi=[f"Mỗi cách xếp là một hoán vị của {n} vật khác nhau.",
                     f"Vị trí đầu có {n} cách, vị trí sau ít hơn một cách, cho đến vị trí cuối còn 1 cách.",
                     f"{n}! = {_fact_text(n)} = {total}."])


@generator("tr_g2_hoan_vi_lap")
def hoan_vi_lap(rng: random.Random) -> Draw:
    kinds = rng.randint(2, 3)
    counts = [rng.randint(1, 4) for _ in range(kinds)]
    while sum(counts) < 4 or max(counts) < 2:
        counts = [rng.randint(1, 4) for _ in range(kinds)]
    colours = ["đỏ", "xanh", "vàng"][:kinds]
    n = sum(counts)
    total = math.factorial(n)
    for c in counts:
        total //= math.factorial(c)
    parts = ", ".join(f"{c} viên {col}" for c, col in zip(counts, colours))
    return Draw(
        params={"counts": counts},
        prompt_vi=(f"Xếp {n} viên linh thạch thành một hàng: {parts}; các viên cùng màu giống hệt nhau. "
                   "Có bao nhiêu hàng khác nhau?"),
        answer=str(total),
        solution_vi=[f"Nếu mọi viên đều khác nhau thì có {n}! cách xếp.",
                     "Đổi chỗ các viên cùng màu cho nhau không tạo ra hàng mới, nên chia cho giai thừa của số viên mỗi màu.",
                     f"{n}!/({'! . '.join(str(c) for c in counts)}!) = {total}."])


_NAME_PAIRS = [("Lam", "Mai"), ("An", "Bình"), ("Tùng", "Cúc")]


@generator("tr_g2_canh_nhau")
def canh_nhau(rng: random.Random) -> Draw:
    n = rng.randint(4, 7)
    apart = rng.random() < 0.5
    one, two = rng.choice(_NAME_PAIRS)
    together = 2 * math.factorial(n - 1)
    total = math.factorial(n) - together if apart else together
    steps = [f"Buộc {one} và {two} thành một khối, coi như một người.",
             f"Xếp {n - 1} 'người' thành hàng: {n - 1}! = {math.factorial(n - 1)} cách; trong khối, hai người đổi chỗ được: 2 cách.",
             f"Số cách hai người đứng cạnh nhau là 2 . {math.factorial(n - 1)} = {together}."]
    if apart:
        steps.append(f"Lấy tổng số cách xếp trừ đi: {n}! - {together} = {math.factorial(n)} - {together} = {total}.")
    return Draw(
        params={"n": n, "apart": apart, "names": [one, two]},
        prompt_vi=(f"Xếp {n} đệ tử, trong đó có {one} và {two}, thành một hàng ngang. Có bao nhiêu cách xếp mà "
                   f"{one} và {two} {'không ' if apart else ''}đứng cạnh nhau?"),
        answer=str(total), solution_vi=steps)


# ------------------------------------------------------------------ tổ hợp
@generator("tr_g2_to_hop")
def to_hop(rng: random.Random) -> Draw:
    n = rng.randint(5, 15)
    k = rng.randint(2, min(4, n - 2))
    total = math.comb(n, k)
    return Draw(
        params={"n": n, "k": k},
        prompt_vi=f"Từ {n} đệ tử, chọn {k} người cùng đi hái thuốc (không phân biệt vai trò). Có bao nhiêu cách?",
        answer=str(total),
        solution_vi=["Nhóm được chọn không có thứ tự, nên mỗi cách chọn là một tổ hợp.",
                     f"C_{n}^{k} = A_{n}^{k}/{k}! = {math.perm(n, k)}/{math.factorial(k)} = {total}."])


@generator("tr_g2_hai_nhom")
def hai_nhom(rng: random.Random) -> Draw:
    m, w = rng.randint(3, 8), rng.randint(3, 8)
    a, b = rng.randint(1, min(3, m - 1)), rng.randint(1, min(3, w - 1))
    total = math.comb(m, a) * math.comb(w, b)
    return Draw(
        params={"m": m, "w": w, "a": a, "b": b},
        prompt_vi=(f"Một tông môn có {m} kiếm tu và {w} pháp tu. Chọn một đội gồm đúng {a} kiếm tu và {b} pháp tu. "
                   "Có bao nhiêu cách?"),
        answer=str(total),
        solution_vi=["Chọn đội theo hai bước nối tiếp: chọn kiếm tu, rồi chọn pháp tu.",
                     f"Chọn {a} trong {m} kiếm tu: C_{m}^{a} = {math.comb(m, a)}. "
                     f"Chọn {b} trong {w} pháp tu: C_{w}^{b} = {math.comb(w, b)}.",
                     f"Theo quy tắc nhân: {math.comb(m, a)} . {math.comb(w, b)} = {total}."])


# ------------------------------------------------------------------ tổ hợp lặp
def _vars(k: int) -> str:
    return " + ".join(f"x_{i}" for i in range(1, k + 1))


@generator("tr_g2_nghiem_nguyen")
def nghiem_nguyen(rng: random.Random) -> Draw:
    k, n = rng.randint(2, 4), rng.randint(3, 10)
    total = math.comb(n + k - 1, k - 1)
    return Draw(
        params={"k": k, "n": n},
        prompt_vi=f"Phương trình {_vars(k)} = {n} có bao nhiêu nghiệm nguyên không âm?",
        answer=str(total),
        solution_vi=[f"Mỗi nghiệm ứng với một cách xếp {n} viên đá và {k - 1} vách ngăn thành một hàng: "
                     "số đá giữa các vách là các x_i.",
                     f"Hàng có {n + k - 1} vị trí, chọn {k - 1} vị trí cho vách.",
                     f"C_{n + k - 1}^{k - 1} = {total}."])


@generator("tr_g2_nghiem_can_duoi")
def nghiem_can_duoi(rng: random.Random) -> Draw:
    k, m = rng.randint(2, 4), rng.randint(1, 2)
    n = rng.randint(k * m + 1, k * m + 7)
    rest = n - k * m
    total = math.comb(rest + k - 1, k - 1)
    return Draw(
        params={"k": k, "m": m, "n": n},
        prompt_vi=f"Phương trình {_vars(k)} = {n} có bao nhiêu nghiệm nguyên thỏa mãn x_i >= {m} với mọi i?",
        answer=str(total),
        solution_vi=[f"Đặt y_i = x_i - {m} thì y_i >= 0.",
                     f"Phương trình trở thành {_vars(k).replace('x', 'y')} = {n} - {k} . {m} = {rest}.",
                     f"Số nghiệm nguyên không âm là C_{rest + k - 1}^{k - 1} = {total}."])


# ------------------------------------------------------------------ nguyên lý bù trừ
def _lcm(*xs: int) -> int:
    out = 1
    for x in xs:
        out = out * x // math.gcd(out, x)
    return out


@generator("tr_g2_bu_tru_hai_so")
def bu_tru_hai_so(rng: random.Random) -> Draw:
    a, b = sorted(rng.sample(range(2, 10), 2))
    big = rng.randint(30, 200)
    l = _lcm(a, b)
    na, nb, nab = big // a, big // b, big // l
    total = na + nb - nab
    return Draw(
        params={"n": big, "a": a, "b": b},
        prompt_vi=f"Có bao nhiêu số nguyên từ 1 đến {big} chia hết cho {a} hoặc chia hết cho {b}?",
        answer=str(total),
        solution_vi=[f"Gọi A là tập các số chia hết cho {a}, B là tập các số chia hết cho {b}: cần |A hợp B|.",
                     f"|A| = phần nguyên của {big}/{a} = {na}; |B| = phần nguyên của {big}/{b} = {nb}.",
                     f"Số chia hết cho cả hai là số chia hết cho BCNN({a}, {b}) = {l}: |A giao B| = {nab}.",
                     f"|A hợp B| = {na} + {nb} - {nab} = {total}."])


@generator("tr_g2_bu_tru_ba_so")
def bu_tru_ba_so(rng: random.Random) -> Draw:
    a, b, c = sorted(rng.sample([2, 3, 5, 7], 3))
    big = rng.randint(50, 300)
    singles = [big // a, big // b, big // c]
    pairs = [big // _lcm(a, b), big // _lcm(a, c), big // _lcm(b, c)]
    triple = big // _lcm(a, b, c)
    union = sum(singles) - sum(pairs) + triple
    total = big - union
    return Draw(
        params={"n": big, "divisors": [a, b, c]},
        prompt_vi=(f"Có bao nhiêu số nguyên từ 1 đến {big} không chia hết cho số nào trong các số {a}, {b}, {c}?"),
        answer=str(total),
        solution_vi=[f"Đếm phần bù: lấy {big} trừ đi số các số chia hết cho ít nhất một trong {a}, {b}, {c}.",
                     f"Chia hết cho từng số: {singles[0]}, {singles[1]}, {singles[2]}.",
                     f"Chia hết cho cả hai số của từng cặp, tức là chia hết cho {a * b}, {a * c}, {b * c}: "
                     f"{pairs[0]}, {pairs[1]}, {pairs[2]}; "
                     f"chia hết cho cả ba ({a * b * c}): {triple}.",
                     f"Theo nguyên lý bù trừ: {sum(singles)} - {sum(pairs)} + {triple} = {union} số chia hết cho ít nhất một số.",
                     f"Đáp số: {big} - {union} = {total}."])


# ------------------------------------------------------------------ hệ thức truy hồi
def _term(c: int, name: str) -> str:
    if c == 1:
        return name
    if c == -1:
        return f"-{name}"
    return f"{c}{name}"


@generator("tr_g2_truy_hoi")
def truy_hoi(rng: random.Random) -> Draw:
    c1 = rng.choice([1, 2, 3, -1, -2])
    c2 = rng.choice([1, 2, -1, 3])
    a0, a1 = rng.randint(0, 3), rng.randint(1, 4)
    n = rng.randint(4, 6)
    seq = [a0, a1]
    for _ in range(2, n + 1):
        seq.append(c1 * seq[-1] + c2 * seq[-2])
    rhs = _term(c1, "a_(n - 1)") + (" + " if c2 > 0 else " - ") + _term(abs(c2), "a_(n - 2)")
    return Draw(
        params={"c1": c1, "c2": c2, "a0": a0, "a1": a1, "n": n},
        prompt_vi=f"Dãy a_n thỏa mãn a_0 = {a0}, a_1 = {a1} và a_n = {rhs} với n >= 2. Tính a_{n}.",
        answer=str(seq[n]),
        solution_vi=["Tính lần lượt từng số hạng, mỗi số hạng dùng hai số hạng đứng ngay trước nó.",
                     "; ".join(f"a_{i} = {seq[i]}" for i in range(2, n + 1)) + ".",
                     f"Vậy a_{n} = {seq[n]}."])


@generator("tr_g2_xau_cam")
def xau_cam(rng: random.Random) -> Draw:
    run = rng.choice([2, 3])
    n = rng.randint(4, 12)
    # s[m] = number of good strings of length m, for m = 0..n
    s = [2 ** m for m in range(run)]
    for m in range(run, n + 1):
        s.append(sum(s[m - j] for j in range(1, run + 1)))
    banned = "1" * run
    if run == 2:
        rule = "s_n = s_(n - 1) + s_(n - 2)"
        why = "Xâu tốt kết thúc bằng 0 hoặc bằng 01, bỏ phần đuôi đó đi vẫn là xâu tốt."
    else:
        rule = "s_n = s_(n - 1) + s_(n - 2) + s_(n - 3)"
        why = "Xâu tốt kết thúc bằng 0, 01 hoặc 011, bỏ phần đuôi đó đi vẫn là xâu tốt."
    start = ", ".join(f"s_{m} = {s[m]}" for m in range(run))
    return Draw(
        params={"run": run, "n": n},
        prompt_vi=f"Có bao nhiêu xâu nhị phân độ dài {n} không chứa {run} chữ số 1 đứng liền nhau (không chứa {banned})?",
        answer=str(s[n]),
        solution_vi=[f"Gọi s_n là số xâu cần đếm có độ dài n. {why}",
                     f"Vậy {rule}, với {start}.",
                     "Tính dần: " + ", ".join(str(s[m]) for m in range(n + 1)) + ".",
                     f"s_{n} = {s[n]}."])
