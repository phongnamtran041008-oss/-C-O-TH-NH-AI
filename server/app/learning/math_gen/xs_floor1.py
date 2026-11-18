"""Xác Suất và Thống Kê, tầng 1 (phép thử, sự kiện, giải tích kết hợp): generators.

Every count here is done with a formula (product rule, n!, n!/(n-k)!, math.comb);
tools/math_verify_xs.py recounts the same questions by listing every outcome."""
from __future__ import annotations

import math
import random

from . import Draw, generator, nums, set_text

# The die events this floor names, as sets of faces (math_verify_xs.py rebuilds them from
# their definitions instead of reading these tables).
DIE_EVENTS = {
    "chan": ("số chấm là số chẵn", (2, 4, 6)),
    "le": ("số chấm là số lẻ", (1, 3, 5)),
    "chia3": ("số chấm chia hết cho 3", (3, 6)),
    "nguyen_to": ("số chấm là số nguyên tố", (2, 3, 5)),
}


def _coins_dice_text(coins: int, dice: int) -> str:
    parts = []
    if coins:
        parts.append(f"tung {coins} đồng xu" if coins > 1 else "tung 1 đồng xu")
    if dice:
        parts.append(f"gieo {dice} con xúc xắc sáu mặt" if dice > 1 else "gieo 1 con xúc xắc sáu mặt")
    text = " và ".join(parts)
    return text[0].upper() + text[1:]


def _all_text(coins: int, dice: int) -> str:
    if coins and dice:
        return "mọi đồng xu và xúc xắc"
    return "các đồng xu" if coins else "các xúc xắc"


def _record_text(coins: int, dice: int) -> str:
    parts = (["mặt của từng đồng xu"] if coins else []) + (["số chấm của từng xúc xắc"] if dice else [])
    return " và ".join(parts)


# ------------------------------------------------------------------ phép thử và không gian mẫu
@generator("xs_g1_khong_gian_mau")
def khong_gian_mau(rng: random.Random) -> Draw:
    while True:
        coins, dice = rng.randint(0, 4), rng.randint(0, 3)
        if coins + dice >= 2:
            break
    size = 2 ** coins * 6 ** dice
    steps = []
    if coins:
        steps.append(f"Mỗi đồng xu có 2 mặt: {coins} đồng xu cho 2^{coins} = {2 ** coins} khả năng.")
    if dice:
        steps.append(f"Mỗi xúc xắc có 6 mặt: {dice} xúc xắc cho 6^{dice} = {6 ** dice} khả năng.")
    return Draw(
        params={"coins": coins, "dice": dice},
        prompt_vi=f"{_coins_dice_text(coins, dice)}, {_all_text(coins, dice)} đều phân biệt được với nhau. "
                  f"Một kết quả ghi {_record_text(coins, dice)}. Không gian mẫu có bao nhiêu phần tử?",
        answer=str(size),
        solution_vi=["Một kết quả chọn đồng thời mặt của mọi đồng xu và mọi xúc xắc, nên dùng quy tắc nhân.",
                     *steps,
                     f"Không gian mẫu có {size} phần tử."])


# ------------------------------------------------------------------ quan hệ giữa các sự kiện
@generator("xs_g1_su_kien")
def su_kien(rng: random.Random) -> Draw:
    while True:
        a = rng.choice(sorted(DIE_EVENTS))
        side = rng.choice([">", "<"])
        k = rng.randint(2, 5)
        op = rng.choice(["tich", "tong"])
        a_set = set(DIE_EVENTS[a][1])
        b_set = {f for f in range(1, 7) if (f > k if side == ">" else f < k)}
        out = sorted(a_set & b_set) if op == "tich" else sorted(a_set | b_set)
        if out and len(out) < 6:
            break
    b_text = f"số chấm lớn hơn {k}" if side == ">" else f"số chấm nhỏ hơn {k}"
    if op == "tich":
        ask, rule = "AB (A và B cùng xảy ra)", "AB gồm các kết quả thuộc cả A và B."
    else:
        ask, rule = "A + B (ít nhất một trong hai sự kiện xảy ra)", "A + B gồm các kết quả thuộc A hoặc thuộc B."
    return Draw(
        params={"a": a, "side": side, "k": k, "op": op},
        prompt_vi=f"Gieo một con xúc xắc sáu mặt. A là sự kiện {DIE_EVENTS[a][0]}, B là sự kiện {b_text}. "
                  f"Liệt kê các kết quả (số chấm) của sự kiện {ask}.",
        answer=nums(out), unordered=True,
        solution_vi=[f"A = {set_text(sorted(a_set))} và B = {set_text(sorted(b_set))}.",
                     rule,
                     f"Sự kiện cần tìm là {set_text(out)}."])


# ------------------------------------------------------------------ quy tắc cộng và quy tắc nhân
@generator("xs_g1_thuc_don")
def thuc_don(rng: random.Random) -> Draw:
    a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 5)
    return Draw(
        params={"a": a, "b": b, "c": c},
        prompt_vi=f"Một quán có {a} món khai vị, {b} món chính và {c} món tráng miệng, các món đều khác nhau. "
                  "Một suất ăn gồm đúng 1 món khai vị, 1 món chính và 1 món tráng miệng. "
                  "Có bao nhiêu suất ăn khác nhau?",
        answer=str(a * b * c),
        solution_vi=["Chọn suất ăn gồm ba bước nối tiếp: chọn khai vị, chọn món chính, chọn tráng miệng.",
                     f"Các bước có lần lượt {a}, {b} và {c} cách, bước sau không phụ thuộc bước trước.",
                     f"Theo quy tắc nhân: {a} . {b} . {c} = {a * b * c} suất ăn."])


@generator("xs_g1_ma_so")
def ma_so(rng: random.Random) -> Draw:
    n, k = rng.randint(3, 9), rng.randint(2, 4)
    kind = rng.choice(["tu_do", "cuoi_le"])
    odd = (n + 1) // 2
    if kind == "tu_do":
        count = n ** k
        extra = ""
        steps = [f"Mỗi vị trí có {n} cách chọn, vì được lặp lại.",
                 f"Theo quy tắc nhân: {n}^{k} = {count} mã."]
    else:
        count = n ** (k - 1) * odd
        extra = " và chữ số cuối cùng là số lẻ"
        steps = [f"Chữ số cuối phải lẻ: trong các chữ số từ 1 đến {n} có {odd} số lẻ, nên có {odd} cách.",
                 f"Mỗi vị trí trong {k - 1} vị trí còn lại có {n} cách, vì được lặp lại.",
                 f"Theo quy tắc nhân: {n}^{k - 1} . {odd} = {count} mã."]
    return Draw(
        params={"n": n, "k": k, "kind": kind},
        prompt_vi=f"Một mã số gồm {k} chữ số, mỗi chữ số lấy trong các chữ số từ 1 đến {n} và được phép lặp lại. "
                  f"Có bao nhiêu mã số như vậy{extra}?",
        answer=str(count),
        solution_vi=["Lập mã là chọn lần lượt từng chữ số, từ trái sang phải.", *steps])


# ------------------------------------------------------------------ hoán vị và chỉnh hợp
@generator("xs_g1_hoan_vi")
def hoan_vi(rng: random.Random) -> Draw:
    n = rng.randint(3, 7)
    fixed = rng.random() < 0.5
    if fixed:
        count = math.factorial(n - 1)
        ask = f"Có bao nhiêu cách xếp {n} bạn, trong đó có Lan, thành một hàng dọc sao cho Lan đứng đầu hàng?"
        steps = ["Vị trí đầu hàng đã là của Lan, chỉ còn xếp các bạn khác.",
                 f"{n - 1} bạn còn lại xếp vào {n - 1} chỗ còn lại: {n - 1}! = {count} cách."]
    else:
        count = math.factorial(n)
        ask = f"Có bao nhiêu cách xếp {n} bạn thành một hàng dọc?"
        steps = ["Mỗi cách xếp là một hoán vị của các bạn.",
                 f"Số hoán vị của {n} phần tử là {n}! = {count}."]
    return Draw(params={"n": n, "fixed": fixed}, prompt_vi=ask, answer=str(count), solution_vi=steps)


ROLES = {2: "một trưởng nhóm và một phó nhóm",
         3: "một trưởng nhóm, một phó nhóm và một thư ký",
         4: "một trưởng nhóm, một phó nhóm, một thư ký và một thủ quỹ"}


@generator("xs_g1_chinh_hop")
def chinh_hop(rng: random.Random) -> Draw:
    n, k = rng.randint(5, 12), rng.randint(2, 4)
    count = math.perm(n, k)
    factors = " . ".join(str(n - i) for i in range(k))
    return Draw(
        params={"n": n, "k": k},
        prompt_vi=f"Một nhóm có {n} người. Chọn ra {ROLES[k]}, mỗi người giữ nhiều nhất một chức vụ. "
                  "Có bao nhiêu cách chọn?",
        answer=str(count),
        solution_vi=["Các chức vụ khác nhau, nên đổi chỗ hai người là một cách chọn khác: thứ tự có ý nghĩa.",
                     f"Đây là chỉnh hợp chập {k} của {n}: chức vụ đầu có {n} cách, mỗi chức vụ sau ít đi một cách.",
                     f"A({n}, {k}) = {factors} = {count}."])


# ------------------------------------------------------------------ tổ hợp
@generator("xs_g1_to_hop")
def to_hop(rng: random.Random) -> Draw:
    n, k = rng.randint(5, 12), rng.randint(2, 4)
    count = math.comb(n, k)
    return Draw(
        params={"n": n, "k": k},
        prompt_vi=f"Một tổ có {n} bạn. Chọn {k} bạn đi trực nhật cùng nhau (không phân công việc riêng). "
                  "Có bao nhiêu cách chọn?",
        answer=str(count),
        solution_vi=["Các bạn được chọn làm cùng một việc, nên chỉ quan tâm nhóm gồm những ai: không kể thứ tự.",
                     f"Đây là tổ hợp chập {k} của {n}: C({n}, {k}) = A({n}, {k}) / {k}!.",
                     f"C({n}, {k}) = {math.perm(n, k)} / {math.factorial(k)} = {count}."])


@generator("xs_g1_hai_nhom")
def hai_nhom(rng: random.Random) -> Draw:
    m, w = rng.randint(4, 8), rng.randint(3, 7)
    a, b = rng.randint(1, 3), rng.randint(1, 3)
    cm, cw = math.comb(m, a), math.comb(w, b)
    return Draw(
        params={"men": m, "women": w, "a": a, "b": b},
        prompt_vi=f"Một câu lạc bộ có {m} nam và {w} nữ. Chọn một đội gồm {a} nam và {b} nữ "
                  "(không phân biệt vai trò trong đội). Có bao nhiêu cách chọn?",
        answer=str(cm * cw),
        solution_vi=[f"Chọn {a} nam trong {m} nam: C({m}, {a}) = {cm} cách.",
                     f"Chọn {b} nữ trong {w} nữ: C({w}, {b}) = {cw} cách.",
                     f"Hai bước nối tiếp nên nhân: {cm} . {cw} = {cm * cw} cách."])


@generator("xs_g1_thu_tu_tf")
def thu_tu_tf(rng: random.Random) -> Draw:
    n, k = rng.randint(5, 10), rng.randint(2, 3)
    ordered = rng.random() < 0.5
    perm, comb = math.perm(n, k), math.comb(n, k)
    shown = rng.choice([perm, comb])
    right = perm if ordered else comb
    if ordered:
        task = f"chọn {k} bạn rồi giao cho họ {ROLES[k]}"
        why = f"Các chức vụ khác nhau nên thứ tự có ý nghĩa: số cách là A({n}, {k}) = {perm}."
    else:
        task = f"chọn {k} bạn vào một nhóm làm việc chung, không phân biệt vai trò"
        why = f"Chỉ quan tâm nhóm gồm những ai, không kể thứ tự: số cách là C({n}, {k}) = {comb}."
    return Draw(
        params={"n": n, "k": k, "ordered": ordered, "shown": shown},
        prompt_vi=f"Có {n} bạn. Số cách {task} là {shown}.",
        answer=shown == right,
        solution_vi=[why,
                     f"Mệnh đề nói {shown}, nên mệnh đề {'đúng' if shown == right else 'sai'}."])
