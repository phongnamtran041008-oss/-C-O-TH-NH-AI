"""Xác Suất và Thống Kê: generators added by the curriculum review (see rsdstt_floor1.py for why).
Ids are `xs_g<floor>_<name>`. Floors 7-8 had generators only at tier 4, so tier 5 repeated two
hand-written questions: the ones here ask the same ideas the other way round (find n from an
interval, find the unbiased weight, find the maximum-likelihood estimate from data). Every answer
is an exact fraction or decimal; tools/math_verify_rasoat.py recomputes each one with sympy."""
from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

from . import Draw, generator, nonzero, num, nums, paren
from .xs_floor7 import dec
from .xs_floor8 import PROPORTION_SAMPLES, Z_LEVELS, _sqrt_fraction, _z_given


# ------------------------------------------------------------------ floor 2 (tier 1)
@generator("xs_g2_rut_mau_cung_nhan")
def rut_mau_cung_nhan(rng: random.Random) -> Draw:
    """Tier 1: classical probability with combinations: draw k items at once, all of one kind."""
    good, bad = rng.randint(3, 9), rng.randint(2, 8)
    k = rng.choice([2, 2, 3])
    if good < k:
        good = k
    total = good + bad
    p = Fraction(math.comb(good, k), math.comb(total, k))
    return Draw(
        params={"good": good, "bad": bad, "k": k},
        prompt_vi=f"Một lô dữ liệu có {good} mẫu gắn nhãn đúng và {bad} mẫu gắn nhãn sai. Lấy ngẫu nhiên đồng thời "
                  f"{k} mẫu. Tính xác suất cả {k} mẫu đều gắn nhãn đúng. Nhập số nguyên hoặc phân số tối giản.",
        answer=num(p),
        solution_vi=[f"Không gian mẫu: chọn {k} trong {total} mẫu, có C({total}, {k}) = {math.comb(total, k)} cách.",
                     f"Thuận lợi: chọn {k} trong {good} mẫu đúng, có C({good}, {k}) = {math.comb(good, k)} cách.",
                     f"Xác suất = {math.comb(good, k)}/{math.comb(total, k)} = {num(p)}."])


@generator("xs_g2_it_nhat_mot_rs")
def it_nhat_mot(rng: random.Random) -> Draw:
    """Tier 1: P(at least one) = 1 - P(none), with independent trials."""
    miss = rng.choice([Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
                       Fraction(1, 6), Fraction(1, 8)])
    n = rng.randint(2, 4)
    p = 1 - (1 - miss) ** n
    return Draw(
        params={"miss": num(miss), "n": n},
        prompt_vi=f"Một bộ lọc thư rác bỏ sót mỗi thư rác với xác suất {num(miss)}, các thư độc lập với nhau. Có {n} "
                  f"thư rác gửi tới. Tính xác suất có ít nhất một thư rác lọt qua. Nhập số nguyên hoặc phân số tối giản.",
        answer=num(p),
        solution_vi=["Dùng sự kiện đối: 'ít nhất một thư lọt' là đối của 'không thư nào lọt'.",
                     f"Mỗi thư bị chặn với xác suất 1 - {num(miss)} = {num(1 - miss)}; cả {n} thư bị chặn: "
                     f"({num(1 - miss)})^{n} = {num((1 - miss) ** n)}.",
                     f"Xác suất cần tìm = 1 - {num((1 - miss) ** n)} = {num(p)}."])


# ------------------------------------------------------------------ floor 7 (tier 5)
@generator("xs_g7_mau_co_hoan_lai")
def mau_co_hoan_lai(rng: random.Random) -> Draw:
    """Tier 5: a population of three values, samples of two with replacement: P(X_tb >= m)."""
    values = sorted(rng.sample(range(1, 10), 3))
    pairs = list(itertools.product(values, repeat=2))
    means = sorted({Fraction(a + b, 2) for a, b in pairs})
    m = rng.choice(means[1:-1] or means)
    good = sum(1 for a, b in pairs if Fraction(a + b, 2) >= m)
    p = Fraction(good, 9)
    table = "; ".join(f"X_tb = {num(mu)}: {sum(1 for a, b in pairs if Fraction(a + b, 2) == mu)} mẫu" for mu in means)
    return Draw(
        params={"values": values, "m": num(m)},
        prompt_vi=f"Tổng thể gồm ba số {values[0]}, {values[1]}, {values[2]}, mỗi số được chọn với xác suất như nhau. "
                  f"Lấy mẫu ngẫu nhiên có hoàn lại cỡ n = 2 và gọi X_tb là trung bình mẫu. Tính P(X_tb >= {num(m)}). "
                  f"Nhập số nguyên hoặc phân số tối giản.",
        answer=num(p),
        solution_vi=["Có 3 . 3 = 9 mẫu có thứ tự, mỗi mẫu xác suất 1/9.",
                     f"Phân bố của X_tb: {table}.",
                     f"Số mẫu có X_tb >= {num(m)} là {good}, nên xác suất = {good}/9 = {num(p)}."])


@generator("xs_g7_gia_tri_thieu")
def gia_tri_thieu(rng: random.Random) -> Draw:
    """Tier 5: n - 1 values and the sample mean are given; find the missing value, then s^2."""
    n = rng.randint(5, 7)
    mean = rng.randint(20, 60)
    data = [mean + rng.randint(-9, 9) for _ in range(n - 1)]
    missing = n * mean - sum(data)
    full = data + [missing]
    ss = sum((x - mean) ** 2 for x in full)
    s2 = Fraction(ss, n - 1)
    return Draw(
        params={"n": n, "mean": mean, "data": data},
        prompt_vi=f"Một mẫu cỡ {n} có trung bình mẫu x_tb = {mean}. {n - 1} giá trị đã đọc được là {', '.join(map(str, data))} "
                  f"(còn một giá trị chưa đọc). Tìm giá trị còn thiếu rồi tính phương sai mẫu hiệu chỉnh s^2. Nhập "
                  f"hai số theo thứ tự đó, cách nhau bằng dấu phẩy.",
        answer=nums([missing, s2]),
        solution_vi=[f"Tổng của cả mẫu là {n} . {mean} = {n * mean}; tổng các giá trị đã biết là {sum(data)}.",
                     f"Giá trị thiếu = {n * mean} - {sum(data)} = {missing}.",
                     "Độ lệch so với trung bình: " + ", ".join(str(x - mean) for x in full) + ".",
                     f"Tổng bình phương độ lệch = {ss}; s^2 = {ss}/({n} - 1) = {num(s2)}."])


@generator("xs_g7_phan_phoi_trung_binh_mau")
def phan_phoi_trung_binh_mau(rng: random.Random) -> Draw:
    """Tier 5: the spread of the sample mean shrinks like sigma/sqrt(n): find n, or Var of the mean."""
    if rng.random() < 0.5:
        d = rng.choice([Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3)])
        k = rng.randint(3, 12)
        sigma = d * k
        n = k * k
        return Draw(
            params={"kind": "n", "sigma": dec(sigma), "d": dec(d)},
            prompt_vi=f"Điểm của một bài kiểm tra có độ lệch chuẩn sigma = {dec(sigma)}. Cần lấy mẫu ngẫu nhiên bao "
                      f"nhiêu người để độ lệch chuẩn của điểm trung bình mẫu bằng đúng {dec(d)}?",
            answer=str(n),
            solution_vi=["Độ lệch chuẩn của trung bình mẫu là sigma/sqrt(n).",
                         f"Đặt {dec(sigma)}/sqrt(n) = {dec(d)}, suy ra sqrt(n) = {dec(sigma)}/{dec(d)} = {k}.",
                         f"Vậy n = {k}^2 = {n}."])
    n = rng.choice([4, 5, 8, 10, 16, 20, 25])
    var = rng.choice([6, 8, 10, 12, 15, 18, 20, 24, 30])
    ans = Fraction(var, n)
    return Draw(
        params={"kind": "var", "n": n, "var": var},
        prompt_vi=f"Thời gian một phép thử có kỳ vọng 50 và phương sai {var}. Lấy {n} phép thử độc lập và tính trung "
                  f"bình. Phương sai của trung bình mẫu X_tb bằng bao nhiêu? Nhập số nguyên hoặc phân số tối giản.",
        answer=num(ans),
        solution_vi=["Với các lần đo độc lập, cùng phân phối: Var(X_tb) = sigma^2/n.",
                     f"Var(X_tb) = {var}/{n} = {num(ans)}. (Kỳ vọng 50 không ảnh hưởng tới phương sai.)"])


@generator("xs_g7_uoc_luong_khong_chech_trong_so")
def uoc_luong_khong_chech(rng: random.Random) -> Draw:
    """Tier 5: T = a X1 + b X2 + c X3 is unbiased for mu iff a + b + c = 1; find c, then Var(T)."""
    a, b = rng.choice([Fraction(1, 5), Fraction(1, 4), Fraction(1, 3), Fraction(1, 6), Fraction(1, 2)]), \
        rng.choice([Fraction(1, 5), Fraction(1, 4), Fraction(1, 6), Fraction(1, 8), Fraction(1, 10)])
    c = 1 - a - b
    sigma2 = rng.choice([4, 6, 8, 10, 12, 20])
    var = sigma2 * (a * a + b * b + c * c)
    return Draw(
        params={"a": num(a), "b": num(b), "sigma2": sigma2},
        prompt_vi=f"X_1, X_2, X_3 là mẫu ngẫu nhiên độc lập từ một tổng thể có kỳ vọng mu chưa biết và phương sai "
                  f"sigma^2 = {sigma2}. Ước lượng T = {num(a)}X_1 + {num(b)}X_2 + c X_3 là ước lượng không chệch của mu. "
                  f"Tìm c, rồi tính Var(T). Nhập hai số theo thứ tự đó, cách nhau bằng dấu phẩy (phân số tối giản).",
        answer=nums([c, var]),
        solution_vi=["E(T) = (a + b + c) mu, nên T không chệch khi a + b + c = 1.",
                     f"c = 1 - {num(a)} - {num(b)} = {num(c)}.",
                     f"Var(T) = (a^2 + b^2 + c^2) sigma^2 = ({num(a * a)} + {num(b * b)} + {num(c * c)}) . {sigma2} "
                     f"= {num(var)}."])


@generator("xs_g7_hop_ly_tu_so_lieu")
def hop_ly_tu_so_lieu(rng: random.Random) -> Draw:
    """Tier 5: the maximum-likelihood estimate from data, three families."""
    kind = rng.choice(["poisson", "mu", "bernoulli"])
    if kind == "poisson":
        n = rng.randint(4, 7)
        data = [rng.randint(0, 6) for _ in range(n)]
        est = Fraction(sum(data), n)
        return Draw(
            params={"kind": kind, "data": data},
            prompt_vi=f"Số yêu thú xuất hiện mỗi đêm tuân theo phân phối Poisson với tham số lambda chưa biết. Quan sát "
                      f"{n} đêm được {', '.join(map(str, data))}. Tìm ước lượng hợp lý cực đại của lambda. Nhập số "
                      f"nguyên hoặc phân số tối giản.",
            answer=num(est),
            solution_vi=["Hàm hợp lý L(lambda) = tích của e^(-lambda) lambda^(x_i)/(x_i!); lấy logarit: "
                         "ln L = -n lambda + (tổng x_i) ln lambda - (hằng số).",
                         f"Đạo hàm theo lambda bằng 0: -n + (tổng x_i)/lambda = 0, nên lambda = (tổng x_i)/n = x_tb.",
                         f"Tổng = {sum(data)}, n = {n}: lambda = {num(est)}."])
    if kind == "mu":
        n = rng.randint(3, 6)
        data = [rng.randint(1, 9) for _ in range(n)]
        est = Fraction(n, sum(data))
        return Draw(
            params={"kind": kind, "data": data},
            prompt_vi=f"Thời gian chờ (phút) giữa hai lần truyền tin có mật độ lambda e^(-lambda x) khi x > 0, với "
                      f"lambda > 0 chưa biết. {n} lần chờ cho {', '.join(map(str, data))}. Tìm ước lượng hợp lý cực đại "
                      f"của lambda. Nhập số nguyên hoặc phân số tối giản.",
            answer=num(est),
            solution_vi=["Hàm hợp lý L = lambda^n e^(-lambda (tổng x_i)); ln L = n ln lambda - lambda (tổng x_i).",
                         "Đạo hàm bằng 0: n/lambda - (tổng x_i) = 0, nên lambda = n/(tổng x_i) = 1/x_tb.",
                         f"Tổng = {sum(data)}, n = {n}: lambda = {num(est)}."])
    trials = rng.randint(2, 4)
    runs = rng.randint(4, 8)
    data = [rng.randint(0, trials) for _ in range(runs)]
    est = Fraction(sum(data), trials * runs)
    return Draw(
        params={"kind": kind, "trials": trials, "data": data},
        prompt_vi=f"Mỗi đệ tử thử một chiêu {trials} lần, mỗi lần thành công với xác suất theta chưa biết (các lần độc "
                  f"lập). Số lần thành công của {runs} đệ tử là {', '.join(map(str, data))}. Tìm ước lượng hợp lý cực "
                  f"đại của theta. Nhập số nguyên hoặc phân số tối giản.",
        answer=num(est),
        solution_vi=[f"Tổng số lần thử là {runs} . {trials} = {trials * runs}, tổng số lần thành công là {sum(data)}.",
                     "Hàm hợp lý của các lần thử Bernoulli độc lập: theta^(số thành công) (1 - theta)^(số thất bại); "
                     "đạo hàm của logarit bằng 0 cho theta = (số thành công)/(số lần thử).",
                     f"theta = {sum(data)}/{trials * runs} = {num(est)}."])


# ------------------------------------------------------------------ floor 8 (tier 5)
@generator("xs_g8_tin_cay_tim_n")
def tin_cay_tim_n(rng: random.Random) -> Draw:
    """Tier 5: an interval for the mean (sigma known) is given; find the sample size."""
    level = rng.choice(list(Z_LEVELS))
    z = Fraction(Z_LEVELS[level][0])
    k = rng.randint(3, 10)
    se = rng.choice([Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3), Fraction(4)])
    sigma = se * k
    xbar = Fraction(rng.randint(100, 900), 10)
    eps = z * se
    lo, hi = xbar - eps, xbar + eps
    n = k * k
    return Draw(
        params={"lo": dec(lo), "hi": dec(hi), "sigma": dec(sigma), "z": dec(z)},
        prompt_vi=f"Một đại lượng có phân phối chuẩn với độ lệch chuẩn sigma = {dec(sigma)} đã biết. Từ một mẫu, khoảng "
                  f"tin cậy đối xứng độ tin cậy {level} cho kỳ vọng là ({dec(lo)}; {dec(hi)}), dùng {_z_given(level)}. "
                  f"Mẫu có cỡ n bằng bao nhiêu?",
        answer=str(n),
        solution_vi=[f"Sai số epsilon = (đầu mút lớn - đầu mút nhỏ)/2 = ({dec(hi)} - {dec(lo)})/2 = {dec(eps)}.",
                     f"epsilon = z sigma/sqrt(n) nên sqrt(n) = z sigma/epsilon = {dec(z)} . {dec(sigma)}/{dec(eps)} = {k}.",
                     f"Vậy n = {k}^2 = {n}. (Trung bình mẫu là điểm giữa: {dec(xbar)}.)"])


@generator("xs_g8_tin_cay_ty_le_nguoc")
def tin_cay_ty_le_nguoc(rng: random.Random) -> Draw:
    """Tier 5: an interval for a proportion is given with n; find how many cases the sample had."""
    n, m = rng.choice(PROPORTION_SAMPLES)
    level = rng.choice(list(Z_LEVELS))
    z = Fraction(Z_LEVELS[level][0])
    f = Fraction(m, n)
    eps = z * _sqrt_fraction(f * (1 - f) / n)
    lo, hi = f - eps, f + eps
    return Draw(
        params={"n": n, "lo": dec(lo), "hi": dec(hi)},
        prompt_vi=f"Khảo sát mẫu {n} người dùng thử một tính năng, khoảng tin cậy đối xứng độ tin cậy {level} cho tỷ lệ "
                  f"người thích nó là ({dec(lo)}; {dec(hi)}). Có bao nhiêu người trong mẫu thích tính năng đó?",
        answer=str(m),
        solution_vi=["Khoảng tin cậy đối xứng quanh tần suất mẫu f, nên f là điểm giữa của hai đầu mút.",
                     f"f = ({dec(lo)} + {dec(hi)})/2 = {dec(f)}.",
                     f"Số người thích = f . n = {dec(f)} . {n} = {m}."])


@generator("xs_g8_co_mau_xau_nhat")
def co_mau_xau_nhat(rng: random.Random) -> Draw:
    """Tier 5: the sample size for a proportion when nothing is known about it, using f(1 - f) <= 1/4."""
    level = rng.choice(list(Z_LEVELS))
    z = Fraction(Z_LEVELS[level][0])
    eps = rng.choice([Fraction(1, 100), Fraction(1, 50), Fraction(1, 40), Fraction(1, 25), Fraction(1, 20)])
    bound = z * z / (4 * eps * eps)
    n = math.ceil(bound)
    return Draw(
        params={"z": dec(z), "eps": dec(eps)},
        prompt_vi=f"Chưa biết gì về tỷ lệ p cần ước lượng. Cần cỡ mẫu n nhỏ nhất để khoảng tin cậy đối xứng độ tin cậy "
                  f"{level} cho p có sai số không vượt quá {dec(eps)}, dùng {_z_given(level)} và đánh giá xấu nhất "
                  f"f(1 - f) <= 1/4. Tìm n.",
        answer=str(n),
        solution_vi=["Sai số là z sqrt(f(1 - f)/n); vì f(1 - f) <= 1/4 nên sai số <= z/(2 sqrt(n)).",
                     f"Cần z/(2 sqrt(n)) <= {dec(eps)}, tức n >= z^2/(4 epsilon^2) = {dec(z)}^2/(4 . {dec(eps)}^2) = {dec(bound)}.",
                     f"n là số nguyên nhỏ nhất không nhỏ hơn {dec(bound)}: n = {n}."])


@generator("xs_g8_chebyshev_tim_n")
def chebyshev_tim_n(rng: random.Random) -> Draw:
    """Tier 5: Chebyshev for the sample mean: P(|X_tb - mu| >= eps) <= sigma^2/(n eps^2) <= delta; find n."""
    sigma2 = rng.choice([4, 9, 16, 25, 36, 49, 64, 100])
    eps = rng.choice([Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3)])
    delta = rng.choice([Fraction(1, 10), Fraction(1, 20), Fraction(1, 25), Fraction(1, 5), Fraction(1, 100)])
    bound = Fraction(sigma2) / (delta * eps * eps)
    n = math.ceil(bound)
    return Draw(
        params={"sigma2": sigma2, "eps": dec(eps), "delta": dec(delta)},
        prompt_vi=f"Các lần đo X_1, ..., X_n độc lập, cùng kỳ vọng mu và phương sai {sigma2}. Dùng bất đẳng thức "
                  f"Chebyshev: tìm n nhỏ nhất để chắc chắn P(|X_tb - mu| >= {dec(eps)}) <= {dec(delta)}.",
        answer=str(n),
        solution_vi=["X_tb có kỳ vọng mu và phương sai sigma^2/n; Chebyshev: P(|X_tb - mu| >= epsilon) <= sigma^2/(n epsilon^2).",
                     f"Cần {sigma2}/(n . {dec(eps)}^2) <= {dec(delta)}, tức n >= {sigma2}/({dec(delta)} . {dec(eps)}^2) = "
                     f"{dec(bound) if bound.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 50, 100) else num(bound)}.",
                     f"n là số nguyên nhỏ nhất không nhỏ hơn giá trị đó: n = {n}."])


@generator("xs_g8_clt_nguong")
def clt_nguong(rng: random.Random) -> Draw:
    """Tier 5: the threshold t with P(S > t) = tail for a sum of n independent terms (CLT)."""
    n = rng.choice([25, 36, 49, 64, 81, 100, 144])
    mu = rng.randint(2, 12)
    sigma = rng.randint(1, 6)
    tail, z, phi = rng.choice([("0.05", Fraction("1.645"), "0.45"), ("0.025", Fraction("1.96"), "0.475"),
                               ("0.005", Fraction("2.58"), "0.495")])
    root = math.isqrt(n)
    t = n * mu + z * sigma * root
    return Draw(
        params={"n": n, "mu": mu, "sigma": sigma, "z": dec(z)},
        prompt_vi=f"Tổng S của {n} biến độc lập cùng phân phối, mỗi biến có kỳ vọng {mu} và độ lệch chuẩn {sigma}. Xấp xỉ "
                  f"S bằng phân phối chuẩn (định lý giới hạn trung tâm). Tìm ngưỡng t sao cho P(S > t) = {tail}, biết "
                  f"Phi({dec(z)}) = {phi} (Phi là hàm Laplace, tức P(0 < Z < {dec(z)}) với Z chuẩn tắc). Nhập t là số "
                  f"thập phân đúng.",
        answer=dec(t),
        solution_vi=[f"E(S) = {n} . {mu} = {n * mu}; độ lệch chuẩn của S là {sigma} . sqrt({n}) = {sigma * root}.",
                     f"P(S > t) = {tail} nghĩa là P(0 < Z < (t - {n * mu})/{sigma * root}) = 0.5 - {tail} = {phi}, "
                     f"nên (t - {n * mu})/{sigma * root} = {dec(z)}.",
                     f"t = {n * mu} + {dec(z)} . {sigma * root} = {dec(t)}."])


# ------------------------------------------------------------------ more cells found thin (floors 2-6)
@generator("xs_g2_khong_gian_mau_cach_lay")
def khong_gian_mau_cach_lay(rng: random.Random) -> Draw:
    """Tier 1: the size of the sample space for drawing k of n numbered tickets, by the way of drawing."""
    n = rng.randint(5, 12)
    k = rng.randint(2, 3)
    way = rng.choice(["hoan_lai", "khong_hoan_lai", "dong_thoi"])
    if way == "hoan_lai":
        size = n ** k
        how = f"lần lượt {k} phiếu có hoàn lại (rút xong trả phiếu vào hộp), ghi số theo thứ tự rút"
        step = f"Mỗi lần rút có {n} khả năng và các lần độc lập: {n}^{k} = {size}."
    elif way == "khong_hoan_lai":
        size = math.perm(n, k)
        how = f"lần lượt {k} phiếu không hoàn lại, ghi số theo thứ tự rút"
        step = f"Lần đầu {n} khả năng, các lần sau mỗi lần ít đi một: {' . '.join(str(n - i) for i in range(k))} = {size}."
    else:
        size = math.comb(n, k)
        how = f"đồng thời {k} phiếu (không phân biệt thứ tự)"
        step = f"Số cách chọn {k} trong {n}: C({n}, {k}) = {size}."
    return Draw(
        params={"n": n, "k": k, "way": way},
        prompt_vi=f"Một hộp có {n} phiếu đánh số từ 1 đến {n}. Rút {how}. Không gian mẫu có bao nhiêu kết quả?",
        answer=str(size),
        solution_vi=["Xem rút kiểu nào: có hoàn lại, không hoàn lại hay đồng thời; mỗi kiểu có một cách đếm.", step])


@generator("xs_g3_chuoi_khong_hoan")
def chuoi_khong_hoan(rng: random.Random) -> Draw:
    """Tier 3: the multiplication rule for three draws without replacement, in one given colour order."""
    red, blue = rng.randint(3, 7), rng.randint(3, 7)
    total = red + blue
    order = [rng.choice("DX") for _ in range(3)]
    left = {"D": red, "X": blue}
    p, texts = Fraction(1), []
    name = {"D": "đỏ", "X": "xanh"}
    used = total
    for c in order:
        texts.append(f"{left[c]}/{used}")
        p *= Fraction(left[c], used)
        left[c] -= 1
        used -= 1
    seq = ", ".join(name[c] for c in order)
    return Draw(
        params={"red": red, "blue": blue, "order": "".join(order)},
        prompt_vi=f"Một hộp có {red} bi đỏ và {blue} bi xanh. Lấy lần lượt 3 bi không hoàn lại. Tính xác suất được lần "
                  f"lượt các bi {seq}. Nhập số nguyên hoặc phân số tối giản.",
        answer=num(p),
        solution_vi=["Công thức nhân: P(ABC) = P(A) P(B|A) P(C|AB); sau mỗi lần lấy, hộp ít đi một bi.",
                     "Các nhân tử: " + " . ".join(texts) + ".",
                     f"Tích = {num(p)}."])


@generator("xs_g4_bayes_thu_rac")
def bayes_thu_rac(rng: random.Random) -> Draw:
    """Tier 2: Bayes with a spam filter: P(spam | the word appears)."""
    spam = rng.choice([Fraction(1, 5), Fraction(3, 10), Fraction(2, 5), Fraction(1, 2), Fraction(1, 10)])
    in_spam = rng.choice([Fraction(1, 2), Fraction(3, 5), Fraction(7, 10), Fraction(4, 5), Fraction(9, 10)])
    in_ham = rng.choice([Fraction(1, 10), Fraction(1, 20), Fraction(1, 5), Fraction(1, 25)])
    both = spam * in_spam
    other = (1 - spam) * in_ham
    p = both / (both + other)
    return Draw(
        params={"spam": num(spam), "in_spam": num(in_spam), "in_ham": num(in_ham)},
        prompt_vi=f"{num(spam)} số thư nhận được là thư rác. Từ \"trúng thưởng\" xuất hiện trong {num(in_spam)} số thư rác "
                  f"và trong {num(in_ham)} số thư thường. Một thư có từ đó. Tính xác suất nó là thư rác. Nhập số nguyên "
                  f"hoặc phân số tối giản.",
        answer=num(p),
        solution_vi=[f"P(rác và có từ) = {num(spam)} . {num(in_spam)} = {num(both)}.",
                     f"P(thường và có từ) = {num(1 - spam)} . {num(in_ham)} = {num(other)}.",
                     f"Bayes: P(rác | có từ) = ({num(both)})/(({num(both)}) + ({num(other)})) = {num(p)}."])


@generator("xs_g4_bayes_phat_hien")
def bayes_phat_hien(rng: random.Random) -> Draw:
    """Tier 2: Bayes for a detector (rare event, sensitivity, false alarm rate)."""
    rate = rng.choice([Fraction(1, 100), Fraction(1, 50), Fraction(1, 20), Fraction(1, 10)])
    sens = rng.choice([Fraction(9, 10), Fraction(19, 20), Fraction(4, 5), Fraction(99, 100)])
    false_alarm = rng.choice([Fraction(1, 20), Fraction(1, 10), Fraction(1, 50), Fraction(1, 25)])
    hit = rate * sens
    miss = (1 - rate) * false_alarm
    p = hit / (hit + miss)
    return Draw(
        params={"rate": num(rate), "sens": num(sens), "false_alarm": num(false_alarm)},
        prompt_vi=f"Một bộ phát hiện gian lận báo động đúng với {num(sens)} số vụ gian lận thật và báo nhầm với "
                  f"{num(false_alarm)} số giao dịch bình thường. Chỉ {num(rate)} số giao dịch là gian lận. Một giao dịch "
                  f"bị báo động. Xác suất nó thật sự gian lận là bao nhiêu? Nhập số nguyên hoặc phân số tối giản.",
        answer=num(p),
        solution_vi=[f"P(gian lận và báo động) = {num(rate)} . {num(sens)} = {num(hit)}.",
                     f"P(bình thường và báo động) = {num(1 - rate)} . {num(false_alarm)} = {num(miss)}.",
                     f"Bayes: P(gian lận | báo động) = ({num(hit)})/(({num(hit)}) + ({num(miss)})) = {num(p)}. "
                     "Con số này khác độ nhạy: một báo động chưa chắc là gian lận thật, vì có cả báo nhầm."])


@generator("xs_g4_toan_phan_ba_nhanh")
def toan_phan_ba_nhanh(rng: random.Random) -> Draw:
    """Tier 3: total probability over a complete system of three groups."""
    a = rng.choice([Fraction(1, 5), Fraction(1, 4), Fraction(3, 10), Fraction(1, 2)])
    b = rng.choice([Fraction(1, 5), Fraction(1, 4), Fraction(3, 10)])
    c = 1 - a - b
    rates = [rng.choice([Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), Fraction(3, 100), Fraction(2, 25)])
             for _ in range(3)]
    total = a * rates[0] + b * rates[1] + c * rates[2]
    return Draw(
        params={"shares": [num(a), num(b), num(c)], "rates": [num(r) for r in rates]},
        prompt_vi=f"Ba mô hình A, B, C xử lý lần lượt {num(a)}, {num(b)} và {num(c)} số yêu cầu; tỷ lệ trả lời sai của chúng "
                  f"là {num(rates[0])}, {num(rates[1])} và {num(rates[2])}. Một yêu cầu bất kỳ bị trả lời sai với xác "
                  f"suất bao nhiêu? Nhập số nguyên hoặc phân số tối giản.",
        answer=num(total),
        solution_vi=["A, B, C xử lý mọi yêu cầu và không yêu cầu nào qua hai mô hình: chúng lập một hệ đầy đủ.",
                     "Công thức xác suất toàn phần: P(sai) = P(A) P(sai|A) + P(B) P(sai|B) + P(C) P(sai|C).",
                     f"= {num(a)} . {num(rates[0])} + {num(b)} . {num(rates[1])} + {num(c)} . {num(rates[2])} = {num(total)}."])


@generator("xs_g4_so_do_cay_hai_tang")
def so_do_cay_hai_tang(rng: random.Random) -> Draw:
    """Tier 3: a two-stage tree: P(B) = P(A) P(B|A) + P(not A) P(B|not A)."""
    pa = rng.choice([Fraction(1, 3), Fraction(2, 3), Fraction(3, 5), Fraction(2, 5), Fraction(1, 4), Fraction(3, 4)])
    pb_a = rng.choice([Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(4, 5), Fraction(1, 5)])
    pb_na = rng.choice([Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 10)])
    path = pa * pb_a
    both = path + (1 - pa) * pb_na
    return Draw(
        params={"pa": num(pa), "pb_a": num(pb_a), "pb_na": num(pb_na)},
        prompt_vi=f"Một đệ tử đi vào hang theo lối trái với xác suất {num(pa)}, nếu không thì đi lối phải. Đi lối trái, "
                  f"gặp yêu thú với xác suất {num(pb_a)}; đi lối phải, gặp yêu thú với xác suất {num(pb_na)}. Vẽ sơ đồ "
                  f"cây và tính xác suất đệ tử gặp yêu thú. Nhập số nguyên hoặc phân số tối giản.",
        answer=num(both),
        solution_vi=[f"Nhánh trái rồi gặp: {num(pa)} . {num(pb_a)} = {num(path)}.",
                     f"Nhánh phải rồi gặp: {num(1 - pa)} . {num(pb_na)} = {num((1 - pa) * pb_na)}.",
                     f"Hai đường đi này xung khắc, cộng lại: {num(both)}."])


@generator("xs_g6_ky_vong_tuyen_tinh")
def ky_vong_tuyen_tinh(rng: random.Random) -> Draw:
    """Tier 4: E(aX + b) from a four-value table (probabilities in twentieths)."""
    values = sorted(rng.sample(range(-3, 9), 4))
    cuts = sorted(rng.sample(range(1, 20), 3))
    ps = [Fraction(hi - lo, 20) for lo, hi in zip([0] + cuts, cuts + [20])]
    a, b = nonzero(rng, -3, 4), rng.randint(-5, 5)
    ex = sum(v * p for v, p in zip(values, ps))
    ans = a * ex + b
    return Draw(
        params={"values": values, "ps": [num(p) for p in ps], "a": a, "b": b},
        prompt_vi=f"Biến ngẫu nhiên X nhận các giá trị {', '.join(map(str, values))} với xác suất lần lượt "
                  f"{', '.join(num(p) for p in ps)}. Tính E({a}X {'+' if b >= 0 else '-'} {abs(b)}). Nhập số nguyên "
                  f"hoặc phân số tối giản.",
        answer=num(ans),
        solution_vi=["E(X) = tổng của (giá trị . xác suất) = "
                     + " + ".join(f"{paren(v)} . {num(p)}" for v, p in zip(values, ps)) + f" = {num(ex)}.",
                     f"Tính chất E(aX + b) = a E(X) + b: {a} . {paren(ex)} + {paren(b)} = {num(ans)}."])
