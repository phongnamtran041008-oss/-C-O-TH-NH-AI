"""Tối Ưu và Toán Rời Rạc, floor 3 (bài toán tồn tại và bài toán liệt kê): generators. Ids
start with `tr_g3_`.

The listing generators work the way the floor teaches (the next configuration is built by
the generation rule, a rank is counted block by block); tools/math_verify_tr.py instead
lists every configuration in order with itertools / sympy and looks the answer up."""
from __future__ import annotations

import math
import random

from . import Draw, generator, nums


def _digits(bits) -> str:
    return "".join(str(b) for b in bits)


def _perm_text(p) -> str:
    return "(" + ", ".join(str(v) for v in p) + ")"


def _set_text(s) -> str:
    return "{" + ", ".join(str(v) for v in s) + "}"


# ------------------------------------------------------------------ nguyên lý Dirichlet
_BOX_THEMES = [
    ("Một túi đựng linh thạch {k} màu, màu nào cũng rất nhiều viên. Bịt mắt lấy ra từng viên. Phải lấy "
     "ít nhất bao nhiêu viên để chắc chắn có {m} viên cùng màu?", "màu"),
    ("Một tông môn chia đệ tử vào {k} phong. Phải nhận ít nhất bao nhiêu đệ tử để chắc chắn có một phong "
     "nhận ít nhất {m} người?", "phong"),
    ("Mỗi bài kiểm tra được chấm một trong {k} mức điểm. Lớp phải có ít nhất bao nhiêu đệ tử để chắc chắn "
     "có {m} người cùng mức điểm?", "mức điểm"),
]


@generator("tr_g3_dirichlet_min")
def dirichlet_min(rng: random.Random) -> Draw:
    t = rng.randrange(len(_BOX_THEMES))
    k, m = rng.randint(3, 9), rng.randint(2, 5)
    text, box = _BOX_THEMES[t]
    total = k * (m - 1) + 1
    return Draw(
        params={"theme": t, "k": k, "m": m},
        prompt_vi=text.format(k=k, m=m),
        answer=str(total),
        solution_vi=[f"Coi mỗi {box} là một hộp: có {k} hộp.",
                     f"Với {k} . {m - 1} = {k * (m - 1)} vật vẫn có thể xếp mỗi hộp đúng {m - 1} vật, chưa có hộp nào đủ {m}.",
                     f"Thêm một vật nữa, tức là {total} vật, thì theo nguyên lý Dirichlet có một hộp chứa ít nhất "
                     f"trần({total}/{k}) = {m} vật.",
                     f"Vậy cần ít nhất {total}."])


@generator("tr_g3_dirichlet_tran")
def dirichlet_tran(rng: random.Random) -> Draw:
    k = rng.randint(3, 9)
    n = rng.randint(k + 2, 6 * k)
    q, r = divmod(n, k)
    total = q + (1 if r else 0)
    return Draw(
        params={"n": n, "k": k},
        prompt_vi=(f"Cất {n} viên đan dược vào {k} bình. Dù cất thế nào, chắc chắn có một bình chứa ít nhất "
                   "bao nhiêu viên? (Tìm số lớn nhất có thể khẳng định.)"),
        answer=str(total),
        solution_vi=[f"Theo nguyên lý Dirichlet, có một bình chứa ít nhất trần({n}/{k}) viên.",
                     f"{n} = {k} . {q} + {r}, nên trần({n}/{k}) = {total}.",
                     f"Không khẳng định được nhiều hơn: chia đều càng tốt (mỗi bình {q} hoặc {q + 1} viên) "
                     f"thì bình nhiều nhất chỉ có {total} viên."])


_PAIR_KINDS = {
    "sum": ("có tổng bằng {s}", "{a} và {b}"),
    "next": ("là hai số liên tiếp", None),
    "gap": ("có hiệu bằng {n}", "{a} và {b}"),
}


def _pair_boxes(kind: str, n: int) -> list[tuple[int, int]]:
    if kind == "sum":
        return [(i, 2 * n + 1 - i) for i in range(1, n + 1)]
    if kind == "next":
        return [(2 * i - 1, 2 * i) for i in range(1, n + 1)]
    return [(i, i + n) for i in range(1, n + 1)]


@generator("tr_g3_dirichlet_cap")
def dirichlet_cap(rng: random.Random) -> Draw:
    kind, n = rng.choice(list(_PAIR_KINDS)), rng.randint(3, 7)
    words = _PAIR_KINDS[kind][0].format(s=2 * n + 1, n=n)
    boxes = _pair_boxes(kind, n)
    shown = "; ".join(f"{{{a}, {b}}}" for a, b in boxes)
    avoid = {"sum": f"1, 2, ..., {n}", "next": ", ".join(str(2 * i - 1) for i in range(1, n + 1)),
             "gap": f"1, 2, ..., {n}"}[kind]
    return Draw(
        params={"kind": kind, "n": n},
        prompt_vi=(f"Chọn các số khác nhau từ tập {{1, 2, ..., {2 * n}}}. Phải chọn ít nhất bao nhiêu số để chắc chắn "
                   f"trong đó có hai số {words}?"),
        answer=str(n + 1),
        solution_vi=[f"Chia {2 * n} số thành {n} hộp, mỗi hộp là một cặp số {words}: {shown}.",
                     f"Chọn {n + 1} số thì theo nguyên lý Dirichlet có hai số rơi vào cùng một hộp, tức là thành một cặp như vậy.",
                     f"Chọn {n} số thì chưa chắc: ví dụ {avoid} không có cặp nào như vậy.",
                     f"Vậy cần ít nhất {n + 1} số."])


# ------------------------------------------------------------------ chẵn lẻ và bất biến
@generator("tr_g3_bat_bien")
def bat_bien(rng: random.Random) -> Draw:
    n = rng.randint(4, 20)
    op = rng.choice(["sum", "diff"])
    claim_odd = rng.random() < 0.5
    total = n * (n + 1) // 2
    final_odd = total % 2 == 1
    write = "a + b" if op == "sum" else "|a - b|"
    why = ("Tổng mới bằng tổng cũ, nên tổng không đổi." if op == "sum" else
           "Tổng mới bằng tổng cũ trừ 2 . min(a, b), một số chẵn, nên tính chẵn lẻ của tổng không đổi.")
    return Draw(
        params={"n": n, "op": op, "claim_odd": claim_odd},
        prompt_vi=(f"Trên bảng có các số 1, 2, ..., {n}. Mỗi lượt xóa hai số a, b bất kỳ và viết thêm số {write}. "
                   f"Sau {n - 1} lượt trên bảng còn một số. Số đó chắc chắn là số {'lẻ' if claim_odd else 'chẵn'}."),
        answer=claim_odd == final_odd,
        solution_vi=["Tìm đại lượng không đổi: tính chẵn lẻ của tổng các số trên bảng.",
                     f"Khi thay a, b bằng {write}: {why}",
                     f"Lúc đầu tổng là 1 + 2 + ... + {n} = {total}, là số {'lẻ' if final_odd else 'chẵn'}.",
                     f"Số cuối cùng chính là tổng lúc cuối, nên luôn là số {'lẻ' if final_odd else 'chẵn'}; "
                     f"câu đã cho {'đúng' if claim_odd == final_odd else 'sai'}."])


@generator("tr_g3_lat_coc")
def lat_coc(rng: random.Random) -> Draw:
    n = rng.randint(5, 9)
    k = rng.choice([2, 3])
    d = rng.randint(1, n)
    possible = d % 2 == 0 if k == 2 else True
    if k == 2:
        steps = ["Gọi d là số cốc đang úp. Lật 2 cốc: d giảm 2, tăng 2 hoặc giữ nguyên (một úp, một ngửa).",
                 "Vậy tính chẵn lẻ của d không bao giờ đổi: đó là bất biến.",
                 (f"Lúc đầu d = {d} là số chẵn, nên có thể về 0: mỗi lượt lật 2 cốc đang úp." if possible else
                  f"Lúc đầu d = {d} là số lẻ, còn mục tiêu d = 0 là số chẵn, nên không thể đạt tới.")]
    else:
        steps = ["Gọi d là số cốc đang úp. Lật 3 cốc thì d đổi đi -3, -1, +1 hoặc +3: tính chẵn lẻ của d đổi mỗi lượt, "
                 "nên ở đây chẵn lẻ không cản trở.",
                 "Cách làm: khi d >= 3 thì lật 3 cốc đang úp, cho đến khi d bằng 0, 1 hoặc 2.",
                 "Còn 2 cốc úp: lật 1 cốc úp cùng 2 cốc ngửa thì d = 3, rồi lật cả 3 cốc úp.",
                 "Còn 1 cốc úp: lật nó cùng 2 cốc ngửa thì d = 2, rồi làm như trên. Vậy luôn làm được."]
    return Draw(
        params={"n": n, "k": k, "d": d},
        prompt_vi=(f"Trên bàn có {n} cái cốc, trong đó {d} cốc đang úp, còn lại ngửa. Mỗi lượt phải lật đúng {k} cốc "
                   "khác nhau. Có thể sau một số lượt làm cho mọi cốc đều ngửa."),
        answer=possible, solution_vi=steps)


# ------------------------------------------------------------------ thứ tự từ điển
@generator("tr_g3_so_sanh")
def so_sanh(rng: random.Random) -> Draw:
    n = rng.randint(4, 6)
    x = rng.sample(range(1, n + 1), n)
    y = x[:]
    while y == x:
        y = rng.sample(range(1, n + 1), n)
    i = next(j for j in range(n) if x[j] != y[j])
    before = x[i] < y[i]
    return Draw(
        params={"x": x, "y": y},
        prompt_vi=f"Theo thứ tự từ điển, hoán vị {_perm_text(x)} đứng trước hoán vị {_perm_text(y)}.",
        answer=before,
        solution_vi=["So sánh từng thành phần từ trái sang phải; vị trí khác nhau đầu tiên quyết định thứ tự.",
                     f"Hai hoán vị giống nhau ở {i} thành phần đầu và khác nhau ở thành phần thứ {i + 1}: {x[i]} và {y[i]}.",
                     f"{min(x[i], y[i])} nhỏ hơn, nên {_perm_text(x if before else y)} đứng trước; "
                     f"câu đã cho {'đúng' if before else 'sai'}."])


# ------------------------------------------------------------------ phương pháp sinh
@generator("tr_g3_xau_ke_tiep")
def xau_ke_tiep(rng: random.Random) -> Draw:
    n = rng.randint(5, 8)
    bits = [rng.randint(0, 1) for _ in range(n)]
    if all(bits):
        bits[rng.randrange(n)] = 0
    i = max(j for j in range(n) if bits[j] == 0)
    nxt = bits[:i] + [1] + [0] * (n - i - 1)
    return Draw(
        params={"bits": bits},
        prompt_vi=(f"Sinh các xâu nhị phân độ dài {n} theo thứ tự từ điển. Tìm xâu liền sau xâu {_digits(bits)}. "
                   "Nhập các chữ số của nó, cách nhau bằng dấu phẩy."),
        answer=nums(nxt),
        solution_vi=["Từ phải sang trái, tìm chữ số 0 đầu tiên gặp được.",
                     f"Đó là chữ số thứ {i + 1}. Đổi nó thành 1, và đổi mọi chữ số bên phải nó thành 0.",
                     f"Xâu liền sau là {_digits(nxt)}."])


@generator("tr_g3_tap_con_ke_tiep")
def tap_con_ke_tiep(rng: random.Random) -> Draw:
    n = rng.randint(5, 8)
    k = rng.randint(2, 4)
    last = list(range(n - k + 1, n + 1))
    s = sorted(rng.sample(range(1, n + 1), k))
    while s == last:
        s = sorted(rng.sample(range(1, n + 1), k))
    i = max(j for j in range(k) if s[j] != n - k + 1 + j)
    nxt = s[:i] + [s[i] + 1 + t for t in range(k - i)]
    return Draw(
        params={"n": n, "subset": s},
        prompt_vi=(f"Sinh các tập con {k} phần tử của {{1, 2, ..., {n}}} theo thứ tự từ điển, mỗi tập viết các phần tử "
                   f"tăng dần. Tìm tập liền sau {_set_text(s)}. Nhập các phần tử theo thứ tự tăng dần."),
        answer=nums(nxt),
        solution_vi=[f"Phần tử ở vị trí thứ j (tính từ 1) lớn nhất được phép là {n} - {k} + j.",
                     f"Từ phải sang trái, phần tử đầu tiên chưa đạt giá trị lớn nhất của nó là {s[i]} (vị trí thứ {i + 1}).",
                     f"Tăng nó lên {s[i] + 1}, các phần tử sau nó lấy các số liền tiếp: {_set_text(nxt)}."])


@generator("tr_g3_hoan_vi_ke_tiep")
def hoan_vi_ke_tiep(rng: random.Random) -> Draw:
    n = rng.randint(4, 6)
    p = rng.sample(range(1, n + 1), n)
    while p == sorted(p, reverse=True):
        p = rng.sample(range(1, n + 1), n)
    i = max(j for j in range(n - 1) if p[j] < p[j + 1])
    j = max(t for t in range(i + 1, n) if p[t] > p[i])
    q = p[:]
    q[i], q[j] = q[j], q[i]
    q[i + 1:] = reversed(q[i + 1:])
    return Draw(
        params={"p": p},
        prompt_vi=(f"Sinh các hoán vị của {{1, 2, ..., {n}}} theo thứ tự từ điển. Tìm hoán vị liền sau "
                   f"{_perm_text(p)}. Nhập các số theo thứ tự."),
        answer=nums(q),
        solution_vi=[f"Từ phải sang trái, tìm số đầu tiên nhỏ hơn số đứng ngay sau nó: số {p[i]} ở vị trí {i + 1}.",
                     f"Trong đoạn bên phải nó, số nhỏ nhất còn lớn hơn {p[i]} là {p[j]}; đổi chỗ hai số này.",
                     "Đoạn bên phải lúc này giảm dần; đảo ngược nó để thành tăng dần.",
                     f"Hoán vị liền sau là {_perm_text(q)}."])


# ------------------------------------------------------------------ thứ hạng của cấu hình
@generator("tr_g3_hang_xau")
def hang_xau(rng: random.Random) -> Draw:
    n = rng.randint(4, 8)
    bits = [rng.randint(0, 1) for _ in range(n)]
    v = sum(b << (n - 1 - i) for i, b in enumerate(bits))
    terms = " + ".join(f"2^{n - 1 - i}" for i, b in enumerate(bits) if b) or "0"
    return Draw(
        params={"bits": bits},
        prompt_vi=(f"Xếp mọi xâu nhị phân độ dài {n} theo thứ tự từ điển, xâu {'0' * n} đứng thứ 1. "
                   f"Xâu {_digits(bits)} đứng thứ mấy?"),
        answer=str(v + 1),
        solution_vi=["Theo thứ tự từ điển, các xâu độ dài n xếp đúng như các số 0, 1, 2, ... viết trong hệ nhị phân.",
                     f"Xâu {_digits(bits)} biểu diễn số {terms} = {v}.",
                     f"Có {v} xâu đứng trước nó (ứng với 0, 1, ..., {v - 1}) nên nó đứng thứ {v + 1}." if v else
                     "Không có xâu nào đứng trước nó, nên nó đứng thứ 1."])


@generator("tr_g3_hang_hoan_vi")
def hang_hoan_vi(rng: random.Random) -> Draw:
    n = rng.randint(4, 6)
    p = rng.sample(range(1, n + 1), n)
    before = 0
    lines = []
    for i, v in enumerate(p):
        smaller = sum(1 for w in p[i + 1:] if w < v)
        block = smaller * math.factorial(n - 1 - i)
        before += block
        if i < n - 1:
            lines.append(f"vị trí {i + 1} là {v}: còn {smaller} số nhỏ hơn chưa dùng, "
                         f"{smaller} . {n - 1 - i}! = {block}")
    return Draw(
        params={"p": p},
        prompt_vi=(f"Xếp các hoán vị của {{1, 2, ..., {n}}} theo thứ tự từ điển, hoán vị {_perm_text(list(range(1, n + 1)))} "
                   f"đứng thứ 1. Hoán vị {_perm_text(p)} đứng thứ mấy?"),
        answer=str(before + 1),
        solution_vi=["Đếm các hoán vị đứng trước: ở mỗi vị trí, đặt một số nhỏ hơn chưa dùng thì mọi cách xếp phần còn lại "
                     "đều đứng trước.",
                     "; ".join(lines) + ".",
                     f"Có {before} hoán vị đứng trước, nên {_perm_text(p)} đứng thứ {before + 1}."])


@generator("tr_g3_hang_tap_con")
def hang_tap_con(rng: random.Random) -> Draw:
    n = rng.randint(5, 8)
    k = rng.randint(2, 3)
    s = sorted(rng.sample(range(1, n + 1), k))
    before, prev, lines = 0, 0, []
    for i, v in enumerate(s):
        block = sum(math.comb(n - w, k - 1 - i) for w in range(prev + 1, v))
        if block:
            lines.append(f"vị trí {i + 1} đặt số từ {prev + 1} đến {v - 1} thay cho {v}: {block} tập")
        before += block
        prev = v
    detail = "; ".join(lines) + "." if lines else "Không vị trí nào có thể đặt số nhỏ hơn."
    return Draw(
        params={"n": n, "subset": s},
        prompt_vi=(f"Xếp các tập con {k} phần tử của {{1, 2, ..., {n}}} theo thứ tự từ điển (mỗi tập viết tăng dần), "
                   f"tập {_set_text(list(range(1, k + 1)))} đứng thứ 1. Tập {_set_text(s)} đứng thứ mấy?"),
        answer=str(before + 1),
        solution_vi=["Đếm các tập đứng trước: giữ nguyên các phần tử đầu, đặt ở một vị trí một số nhỏ hơn rồi đếm mọi cách "
                     "chọn các phần tử còn lại lớn hơn nó.",
                     detail,
                     f"Có {before} tập đứng trước, nên {_set_text(s)} đứng thứ {before + 1}."])


# ------------------------------------------------------------------ quay lui
@generator("tr_g3_quay_lui_tong")
def quay_lui_tong(rng: random.Random) -> Draw:
    b = rng.randint(2, 5)
    s = rng.randint(b, 2 * b + 1)
    total = 0
    for j in range(4):
        sign = -1 if j % 2 else 1
        rest = s - j * (b + 1)
        if rest < 0:
            break
        total += sign * math.comb(3, j) * math.comb(rest + 2, 2)
    by_first = []
    for x1 in range(b + 1):
        r = s - x1
        cnt = sum(1 for x2 in range(b + 1) if 0 <= r - x2 <= b)
        by_first.append(cnt)
    return Draw(
        params={"b": b, "s": s},
        prompt_vi=(f"Thuật toán quay lui liệt kê mọi bộ (x_1, x_2, x_3) gồm các số nguyên với 0 <= x_i <= {b} và "
                   f"x_1 + x_2 + x_3 = {s}. Nó in ra bao nhiêu bộ?"),
        answer=str(total),
        solution_vi=["Quay lui chọn x_1, rồi x_2; khi đó x_3 = tổng còn lại, chỉ nhận nếu 0 <= x_3 <= " + str(b) + ".",
                     "Số bộ in ra theo từng giá trị x_1 = 0, 1, ...: " + ", ".join(str(c) for c in by_first) + ".",
                     f"Cộng lại: {' + '.join(str(c) for c in by_first)} = {total}."])


@generator("tr_g3_quay_lui_tap_con")
def quay_lui_tap_con(rng: random.Random) -> Draw:
    n = rng.randint(6, 10)
    s = rng.randint(n, 2 * n + 2)
    ways = [1] + [0] * s           # ways[t] = number of subsets of the numbers seen so far with sum t
    for v in range(1, n + 1):
        for t in range(s, v - 1, -1):
            ways[t] += ways[t - v]
    return Draw(
        params={"n": n, "s": s},
        prompt_vi=(f"Thuật toán quay lui liệt kê mọi tập con của {{1, 2, ..., {n}}} có tổng các phần tử bằng {s}. "
                   "Nó in ra bao nhiêu tập?"),
        answer=str(ways[s]),
        solution_vi=["Quay lui xét lần lượt từng số 1, 2, ..., n: chọn hoặc không chọn, và cắt nhánh ngay khi tổng đã vượt "
                     f"{s}.",
                     "Đếm gọn hơn: gọi T(v, t) là số tập con của {1, ..., v} có tổng t; T(v, t) = T(v - 1, t) + T(v - 1, t - v) "
                     "(không chọn v, hoặc chọn v).",
                     f"Tính bảng đó đến v = {n}, t = {s} được {ways[s]} tập."])
