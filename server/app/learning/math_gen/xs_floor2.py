"""Xác Suất và Thống Kê, tầng 2 (định nghĩa cổ điển và thống kê của xác suất): generators.

The probabilities here come from counting formulas (math.comb, powers, sums of a table);
tools/math_verify_xs.py lists the whole sample space instead and counts the favourable
outcomes one by one."""
from __future__ import annotations

import math
import random
from fractions import Fraction

from . import Draw, generator, num


def _p(fav: int, total: int) -> str:
    return num(Fraction(fav, total))


# ------------------------------------------------------------------ xác suất cổ điển
@generator("xs_g2_tong_hai_xuc_xac")
def tong_hai_xuc_xac(rng: random.Random) -> Draw:
    kind = rng.choice(["=", ">=", "<="])
    s = rng.randint(2, 12) if kind == "=" else rng.randint(4, 10)
    ways = {t: 6 - abs(t - 7) for t in range(2, 13)}
    sums = [t for t in ways if (t == s if kind == "=" else t >= s if kind == ">=" else t <= s)]
    fav = sum(ways[t] for t in sums)
    ask = {"=": f"bằng {s}", ">=": f"lớn hơn hoặc bằng {s}", "<=": f"nhỏ hơn hoặc bằng {s}"}[kind]
    detail = " + ".join(str(ways[t]) for t in sums)
    return Draw(
        params={"kind": kind, "s": s},
        prompt_vi=f"Gieo đồng thời hai con xúc xắc cân đối, phân biệt được với nhau. "
                  f"Tính xác suất để tổng số chấm {ask}.",
        answer=_p(fav, 36),
        solution_vi=["Mỗi kết quả là một cặp (số chấm xúc xắc 1, số chấm xúc xắc 2): có 6 . 6 = 36 kết quả "
                     "đồng khả năng.",
                     "Tổng t (từ 2 đến 12) có 6 - |t - 7| cặp: tổng 7 có nhiều cặp nhất, hai đầu ít nhất.",
                     f"Số kết quả thuận lợi: {detail} = {fav}." if len(sums) > 1
                     else f"Số kết quả thuận lợi: {fav}.",
                     f"Xác suất là {fav}/36 = {_p(fav, 36)}."])


@generator("xs_g2_dong_xu")
def dong_xu(rng: random.Random) -> Draw:
    n = rng.randint(2, 6)
    k = rng.randint(0, n)
    fav, total = math.comb(n, k), 2 ** n
    return Draw(
        params={"n": n, "k": k},
        prompt_vi=f"Tung {n} đồng xu cân đối, phân biệt được với nhau. Tính xác suất "
                  + (f"có đúng {k} đồng xu ra mặt ngửa." if k else "không có đồng xu nào ra mặt ngửa."),
        answer=_p(fav, total),
        solution_vi=[f"Mỗi đồng xu có 2 mặt, nên có 2^{n} = {total} kết quả đồng khả năng.",
                     f"Một kết quả thuận lợi được xác định bằng việc chọn {k} đồng xu ngửa trong {n} đồng: "
                     f"C({n}, {k}) = {fav} cách.",
                     f"Xác suất là {fav}/{total} = {_p(fav, total)}."])


# ------------------------------------------------------------------ xác suất cổ điển dùng tổ hợp
@generator("xs_g2_rut_bi")
def rut_bi(rng: random.Random) -> Draw:
    while True:
        a, b = rng.randint(2, 6), rng.randint(2, 6)
        k = rng.randint(2, min(4, a + b - 1))
        r = rng.randint(0, k)
        if r <= a and k - r <= b:
            break
    fav = math.comb(a, r) * math.comb(b, k - r)
    total = math.comb(a + b, k)
    return Draw(
        params={"red": a, "blue": b, "k": k, "r": r},
        prompt_vi=f"Một hộp có {a} bi đỏ và {b} bi xanh, các bi cùng cỡ. Lấy ngẫu nhiên đồng thời {k} bi. "
                  f"Tính xác suất lấy được đúng {r} bi đỏ.",
        answer=_p(fav, total),
        solution_vi=[f"Lấy đồng thời nên không kể thứ tự: không gian mẫu có C({a + b}, {k}) = {total} kết quả.",
                     f"Đúng {r} bi đỏ nghĩa là {r} bi đỏ và {k - r} bi xanh: "
                     f"C({a}, {r}) . C({b}, {k - r}) = {math.comb(a, r)} . {math.comb(b, k - r)} = {fav} cách.",
                     f"Xác suất là {fav}/{total} = {_p(fav, total)}."])


# kind -> (the event, the favourable count of 2-card hands, how it is counted)
CARD_EVENTS = {
    "co": ("cả hai lá đều là lá cơ", math.comb(13, 2), "Chọn 2 trong 13 lá cơ: C(13, 2) = 78."),
    "do": ("cả hai lá đều màu đỏ", math.comb(26, 2), "Chọn 2 trong 26 lá đỏ (rô và cơ): C(26, 2) = 325."),
    "at": ("cả hai lá đều là át", math.comb(4, 2), "Chọn 2 trong 4 lá át: C(4, 2) = 6."),
    "hinh": ("cả hai lá đều là J, Q hoặc K", math.comb(12, 2), "Chọn 2 trong 12 lá J, Q, K: C(12, 2) = 66."),
    "cung_chat": ("hai lá cùng chất", 4 * math.comb(13, 2),
                  "Chọn chất (4 cách) rồi chọn 2 trong 13 lá của chất đó: 4 . 78 = 312."),
    "at_k": ("một lá là át và lá kia là K", 4 * 4, "Chọn 1 trong 4 lá át và 1 trong 4 lá K: 4 . 4 = 16."),
    "khac_mau": ("hai lá khác màu", 26 * 26, "Chọn 1 trong 26 lá đỏ và 1 trong 26 lá đen: 26 . 26 = 676."),
    "dung_mot_co": ("có đúng một lá cơ", 13 * 39, "Chọn 1 trong 13 lá cơ và 1 trong 39 lá không phải cơ: 13 . 39 = 507."),
    "it_nhat_mot_at": ("có ít nhất một lá át", math.comb(52, 2) - math.comb(48, 2),
                       "Lấy phần bù: bỏ đi các cặp không có át, C(52, 2) - C(48, 2) = 1326 - 1128 = 198."),
    "cung_gia_tri": ("hai lá cùng giá trị (cùng số hoặc cùng chữ)", 13 * math.comb(4, 2),
                     "Chọn giá trị (13 cách) rồi chọn 2 trong 4 lá của giá trị đó: 13 . 6 = 78."),
}


@generator("xs_g2_rut_bai")
def rut_bai(rng: random.Random) -> Draw:
    kind = rng.choice(sorted(CARD_EVENTS))
    text, fav, how = CARD_EVENTS[kind]
    total = math.comb(52, 2)
    return Draw(
        params={"kind": kind},
        prompt_vi=f"Rút ngẫu nhiên đồng thời 2 lá từ bộ bài tây 52 lá (4 chất, mỗi chất 13 lá từ 2 đến 10, J, Q, K, át). "
                  f"Tính xác suất {text}.",
        answer=_p(fav, total),
        solution_vi=["Rút đồng thời nên không kể thứ tự: có C(52, 2) = 1326 kết quả đồng khả năng.",
                     how,
                     f"Xác suất là {fav}/1326 = {_p(fav, total)}."])


# ------------------------------------------------------------------ có hoàn lại và không hoàn lại
@generator("xs_g2_hoan_lai")
def hoan_lai(rng: random.Random) -> Draw:
    w, b = rng.randint(2, 6), rng.randint(2, 6)
    back = rng.random() < 0.5
    event = rng.choice(["trang", "den", "khac_mau"])
    n = w + b
    total = n * n if back else n * (n - 1)
    if event == "trang":
        fav = w * w if back else w * (w - 1)
        ask, how = "cả hai lần đều được bi trắng", f"{w} . {w if back else w - 1}"
    elif event == "den":
        fav = b * b if back else b * (b - 1)
        ask, how = "cả hai lần đều được bi đen", f"{b} . {b if back else b - 1}"
    else:
        fav = 2 * w * b
        ask, how = "hai bi lấy được khác màu", f"{w} . {b} + {b} . {w}"
    mode = "có hoàn lại (lấy xong trả bi vào hộp rồi mới lấy lần sau)" if back else "không hoàn lại"
    space = (f"Có hoàn lại nên lần nào cũng có {n} bi: {n} . {n} = {total} kết quả có thứ tự." if back
             else f"Không hoàn lại nên lần sau còn {n - 1} bi: {n} . {n - 1} = {total} kết quả có thứ tự.")
    return Draw(
        params={"white": w, "black": b, "back": back, "event": event},
        prompt_vi=f"Một hộp có {w} bi trắng và {b} bi đen, các bi cùng cỡ. Lấy lần lượt 2 bi {mode}. "
                  f"Tính xác suất {ask}.",
        answer=_p(fav, total),
        solution_vi=[space,
                     f"Số kết quả thuận lợi (kể thứ tự): {how} = {fav}.",
                     f"Xác suất là {fav}/{total} = {_p(fav, total)}."])


# ------------------------------------------------------------------ sự kiện đối
@generator("xs_g2_it_nhat_mot")
def it_nhat_mot(rng: random.Random) -> Draw:
    kind = rng.choice(["sau", "chan", "ngua"])
    n = rng.randint(2, 6) if kind == "ngua" else rng.randint(2, 4)
    if kind == "ngua":
        what, thing, faces, bad = "ra mặt ngửa", f"Tung {n} đồng xu cân đối", 2, 1
        none, bad_text = "mọi đồng xu đều ra mặt sấp", "mỗi đồng xu chỉ có 1 cách (mặt sấp)"
    elif kind == "sau":
        what, thing, faces, bad = "ra mặt 6 chấm", f"Gieo {n} con xúc xắc cân đối", 6, 5
        none, bad_text = "không con xúc xắc nào ra mặt 6", "mỗi xúc xắc có 5 cách (từ 1 đến 5 chấm)"
    else:
        what, thing, faces, bad = "ra mặt chẵn", f"Gieo {n} con xúc xắc cân đối", 6, 3
        none, bad_text = "mọi xúc xắc đều ra mặt lẻ", "mỗi xúc xắc có 3 cách (1, 3 hoặc 5 chấm)"
    total, p_none = faces ** n, Fraction(bad ** n, faces ** n)
    return Draw(
        params={"kind": kind, "n": n},
        prompt_vi=f"{thing}, phân biệt được với nhau. Tính xác suất có ít nhất một "
                  f"{'đồng xu' if kind == 'ngua' else 'con xúc xắc'} {what}.",
        answer=num(1 - p_none),
        solution_vi=[f"Không gian mẫu có {faces}^{n} = {total} kết quả đồng khả năng.",
                     f"Sự kiện đối của 'có ít nhất một' là '{none}'.",
                     f"Đếm sự kiện đối: {bad_text}, nên có {bad}^{n} = {bad ** n} kết quả; "
                     f"xác suất của nó là {bad ** n}/{total}"
                     + ("." if p_none.denominator == total else f" = {num(p_none)}."),
                     f"Xác suất cần tìm là 1 - {num(p_none)} = {num(1 - p_none)}."])


# ------------------------------------------------------------------ tần suất
@generator("xs_g2_tan_suat")
def tan_suat(rng: random.Random) -> Draw:
    days = rng.randint(2, 4)
    shots = [rng.randint(2, 6) * 5 for _ in range(days)]
    hits = [rng.randint(s // 2, s) for s in shots]
    miss = rng.random() < 0.5
    total, good = sum(shots), sum(hits)
    want = total - good if miss else good
    table = "; ".join(f"ngày {d + 1}: bắn {s} phát, trúng {h} phát" for d, (s, h) in enumerate(zip(shots, hits)))
    word = "trượt" if miss else "trúng"
    return Draw(
        params={"shots": shots, "hits": hits, "miss": miss},
        prompt_vi=f"Một xạ thủ tập bắn {days} ngày: {table}. Tính tần suất bắn {word} của xạ thủ trong "
                  "toàn bộ các lần bắn đó.",
        answer=_p(want, total),
        solution_vi=["Tần suất = số lần sự kiện xảy ra / tổng số lần thử, tính trên tất cả các ngày gộp lại.",
                     f"Tổng số phát bắn: {' + '.join(map(str, shots))} = {total}; "
                     f"số phát trúng: {' + '.join(map(str, hits))} = {good}."
                     + (f" Số phát trượt: {total} - {good} = {want}." if miss else ""),
                     f"Tần suất bắn {word} là {want}/{total} = {_p(want, total)}."])


@generator("xs_g2_uoc_luong_so_ca")
def uoc_luong_so_ca(rng: random.Random) -> Draw:
    while True:
        marked = rng.randint(4, 20) * 10
        caught = rng.randint(4, 15) * 10
        again = rng.randint(3, 30)
        if again < caught and (marked * caught) % again == 0:
            break
    n = marked * caught // again
    return Draw(
        params={"marked": marked, "caught": caught, "again": again},
        prompt_vi=f"Để ước lượng số cá trong một hồ, người ta bắt {marked} con, đánh dấu rồi thả lại. Ít ngày sau "
                  f"bắt {caught} con thì thấy {again} con có dấu. Coi tần suất cá có dấu trong lần bắt sau bằng "
                  "tỷ lệ cá có dấu trong cả hồ. Ước lượng số cá trong hồ.",
        answer=str(n),
        solution_vi=[f"Tần suất cá có dấu ở lần bắt sau là {again}/{caught}.",
                     f"Nếu hồ có N con thì tỷ lệ cá có dấu là {marked}/N, nên {marked}/N = {again}/{caught}.",
                     f"N = {marked} . {caught} / {again} = {n}."])
