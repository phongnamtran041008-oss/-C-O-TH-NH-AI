"""Xác Suất và Thống Kê, tầng 10 (Tài Năng: hàm của biến ngẫu nhiên, vectơ ngẫu nhiên, hiệp phương sai,
hồi quy): generators.

Everything is exact: probabilities come from whole counts over a total, so every answer is a fraction in
lowest terms. The joint tables are shown as a matrix P (rows = values of X, columns = values of Y).
tools/math_verify_xs_t10.py recomputes each answer another way: sympy.stats for the law of a function of X,
the definition E[(X - E X)(Y - E Y)] for the covariance, a direct enumeration over the cells for the variance
of aX + bY, the independence test cell by cell, and the normal equations of least squares solved with sympy."""
from __future__ import annotations

import random
from fractions import Fraction

from . import Draw, generator, num, paren


# ------------------------------------------------------------------ helpers
def _composition(rng: random.Random, total: int, parts: int, low: int = 0) -> list[int]:
    """`parts` whole numbers >= low with sum `total`, uniformly among the ways to cut."""
    spare = total - low * parts
    cuts = sorted(rng.sample(range(1, spare + parts), parts - 1)) if spare + parts - 1 >= parts - 1 else []
    bars = [0] + cuts + [spare + parts]
    return [bars[i + 1] - bars[i] - 1 + low for i in range(parts)]


def _p(count: int, total: int) -> str:
    return num(Fraction(count, total))


def _mean_text(name: str, total: int, n: int) -> str:
    raw = f"{total}/{n}"
    value = num(Fraction(total, n))
    return f"{name} = {raw}" if raw == value else f"{name} = {raw} = {value}"


def _table_matrix(counts: list[list[int]], total: int) -> dict[str, list[list[str]]]:
    return {"P": [[_p(c, total) for c in row] for row in counts]}


def _values_text(vals: list[int]) -> str:
    return ", ".join(str(v) for v in vals)


# ------------------------------------------------------------------ hàm của một biến ngẫu nhiên rời rạc
@generator("xs_g10_ham_roi_rac")
def ham_roi_rac(rng: random.Random) -> Draw:
    while True:
        k = rng.choice([4, 5])
        xs = sorted(rng.sample(range(-3, 5), k))
        w = _composition(rng, 20, k, low=1)
        kind = rng.choice(["binh_phuong", "tuyet_doi", "lech_binh_phuong"])
        c = 0 if kind == "binh_phuong" else rng.choice([c for c in range(-2, 4) if c])

        def g(x):
            return x * x if kind == "binh_phuong" else abs(x - c) if kind == "tuyet_doi" else (x - c) ** 2
        ys: dict[int, int] = {}
        for x, wi in zip(xs, w):
            ys[g(x)] = ys.get(g(x), 0) + wi
        ask = rng.choice(["xac_suat", "xac_suat", "ky_vong"])
        merged = [y for y, wy in ys.items() if sum(1 for x in xs if g(x) == y) >= 2]
        if ask == "xac_suat" and not merged:
            continue
        break
    expr = {"binh_phuong": "X^2", "tuyet_doi": "|X|" if c == 0 else f"|X - {c}|" if c > 0 else f"|X + {-c}|",
            "lech_binh_phuong": f"({'X - ' + str(c) if c > 0 else 'X + ' + str(-c)})^2"}[kind]
    dist = ", ".join(_p(wi, 20) for wi in w)
    head = (f"Biến ngẫu nhiên X nhận các giá trị {_values_text(xs)} với xác suất lần lượt {dist}. Đặt Y = {expr}. ")
    rows = ", ".join(f"X = {x} cho {g(x)}" for x in xs)
    if ask == "xac_suat":
        y0 = rng.choice(merged)
        who = [x for x in xs if g(x) == y0]
        ans = Fraction(ys[y0], 20)
        prompt = head + f"Tính P(Y = {y0}). Nhập một số hoặc phân số tối giản."
        sol = [f"Giá trị của Y: {rows}.",
               f"Y = {y0} xảy ra khi X = {' hoặc X = '.join(str(x) for x in who)}: các giá trị khác nhau của X cho cùng "
               f"một giá trị của Y thì cộng xác suất.",
               f"P(Y = {y0}) = {' + '.join(_p(w[xs.index(x)], 20) for x in who)} = {num(ans)}."]
        params = {"xs": xs, "w": w, "kind": kind, "c": c, "ask": ask, "y0": y0}
    else:
        ans = Fraction(sum(g(x) * wi for x, wi in zip(xs, w)), 20)
        prompt = head + "Tính E(Y). Nhập một số hoặc phân số tối giản."
        sol = [f"Giá trị của Y: {rows}.",
               "E(Y) = tổng của g(x) P(X = x): lấy giá trị của Y ở từng x nhân với xác suất của chính x đó (không cần lập bảng của Y).",
               f"E(Y) = {' + '.join(f'{g(x)} . {_p(wi, 20)}' for x, wi in zip(xs, w))} = {num(ans)}."]
        params = {"xs": xs, "w": w, "kind": kind, "c": c, "ask": ask, "y0": 0}
    return Draw(params=params, prompt_vi=prompt, answer=num(ans), solution_vi=sol)


# ------------------------------------------------------------------ bảng phân phối đồng thời: biên và điều kiện
def _draw_counts(rng: random.Random, rows: int, cols: int, total: int, zeros: bool = False) -> list[list[int]]:
    flat = _composition(rng, total, rows * cols, low=0 if zeros else 1)
    return [flat[r * cols:(r + 1) * cols] for r in range(rows)]


@generator("xs_g10_bang_bien")
def bang_bien(rng: random.Random) -> Draw:
    rows, cols = rng.choice([(2, 3), (3, 2), (3, 3), (2, 2)])
    total = rng.choice([20, 24, 30, 36, 40, 48, 50, 60])
    counts = _draw_counts(rng, rows, cols, total)
    kind = rng.choice(["bien_x", "bien_y", "dieu_kien_y", "dieu_kien_x", "tong"])
    i, j = rng.randrange(rows), rng.randrange(cols)
    row_sum = [sum(r) for r in counts]
    col_sum = [sum(counts[r][c] for r in range(rows)) for c in range(cols)]
    head = (f"Bảng phân phối đồng thời P(X = i, Y = j) của hai biến ngẫu nhiên ở ma trận P: hàng ứng với X = "
            f"{_values_text(list(range(rows)))}, cột ứng với Y = {_values_text(list(range(cols)))}. ")
    if kind == "bien_x":
        ans = Fraction(row_sum[i], total)
        prompt = head + f"Tính P(X = {i}). Nhập một số hoặc phân số tối giản."
        sol = [f"Phân phối biên của X: cộng các ô trên hàng X = {i}.",
               f"P(X = {i}) = {' + '.join(_p(c, total) for c in counts[i])} = {num(ans)}."]
    elif kind == "bien_y":
        ans = Fraction(col_sum[j], total)
        prompt = head + f"Tính P(Y = {j}). Nhập một số hoặc phân số tối giản."
        sol = [f"Phân phối biên của Y: cộng các ô trên cột Y = {j}.",
               f"P(Y = {j}) = {' + '.join(_p(counts[r][j], total) for r in range(rows))} = {num(ans)}."]
    elif kind == "dieu_kien_y":
        ans = Fraction(counts[i][j], row_sum[i])
        prompt = head + f"Tính P(Y = {j} | X = {i}). Nhập một số hoặc phân số tối giản."
        sol = [f"P(X = {i}) = tổng hàng X = {i} = {_p(row_sum[i], total)}.",
               f"P(Y = {j} | X = {i}) = P(X = {i}, Y = {j})/P(X = {i}) = {_p(counts[i][j], total)}/{_p(row_sum[i], total)} = {num(ans)}.",
               "Chia cho tổng của hàng chứa điều kiện, không chia cho tổng của cột."]
    elif kind == "dieu_kien_x":
        ans = Fraction(counts[i][j], col_sum[j])
        prompt = head + f"Tính P(X = {i} | Y = {j}). Nhập một số hoặc phân số tối giản."
        sol = [f"P(Y = {j}) = tổng cột Y = {j} = {_p(col_sum[j], total)}.",
               f"P(X = {i} | Y = {j}) = P(X = {i}, Y = {j})/P(Y = {j}) = {_p(counts[i][j], total)}/{_p(col_sum[j], total)} = {num(ans)}.",
               "Chia cho tổng của cột chứa điều kiện, không chia cho tổng của hàng."]
    else:
        s = rng.randint(1, rows + cols - 3)
        cells = [(r, c) for r in range(rows) for c in range(cols) if r + c == s]
        ans = Fraction(sum(counts[r][c] for r, c in cells), total)
        prompt = head + f"Tính P(X + Y = {s}). Nhập một số hoặc phân số tối giản."
        sol = [f"X + Y = {s} xảy ra ở các ô (X, Y) = " + ", ".join(f"({r}, {c})" for r, c in cells) + ".",
               f"P(X + Y = {s}) = {' + '.join(_p(counts[r][c], total) for r, c in cells)} = {num(ans)}."]
    return Draw(params={"counts": counts, "total": total, "kind": kind, "i": i, "j": j,
                        "s": s if kind == "tong" else 0},
                prompt_vi=prompt, answer=num(ans), solution_vi=sol, matrices=_table_matrix(counts, total))


# ------------------------------------------------------------------ độc lập hay không
@generator("xs_g10_doc_lap_tf")
def doc_lap_tf(rng: random.Random) -> Draw:
    truth = rng.random() < 0.5
    while True:
        a, b = rng.choice([(4, 6), (5, 4), (3, 6), (6, 5), (4, 4), (5, 6)])
        wx = _composition(rng, a, 2, low=1)
        wy = _composition(rng, b, 3, low=1)
        total = a * b
        counts = [[wx[i] * wy[j] for j in range(3)] for i in range(2)]
        if not truth:
            j, k = rng.sample(range(3), 2)
            d = rng.randint(1, 2)
            # keep every margin: +d at (0, j) and (1, k), -d at (0, k) and (1, j)
            counts[0][j] += d
            counts[1][k] += d
            counts[0][k] -= d
            counts[1][j] -= d
        if all(v >= 0 for r in counts for v in r) and total <= 60:
            break
    row_sum = [sum(r) for r in counts]
    col_sum = [counts[0][c] + counts[1][c] for c in range(3)]
    indep = all(counts[i][c] * total == row_sum[i] * col_sum[c] for i in range(2) for c in range(3))
    assert indep == truth
    bad = next(((i, c) for i in range(2) for c in range(3) if counts[i][c] * total != row_sum[i] * col_sum[c]), None)
    sol = [f"Phân phối biên: P(X = 0) = {_p(row_sum[0], total)}, P(X = 1) = {_p(row_sum[1], total)}; "
           f"P(Y = 0) = {_p(col_sum[0], total)}, P(Y = 1) = {_p(col_sum[1], total)}, P(Y = 2) = {_p(col_sum[2], total)}."]
    if indep:
        sol.append("Cả sáu ô đều bằng tích hai xác suất biên của nó, nên X và Y độc lập. Mệnh đề đúng.")
    else:
        i, c = bad
        prod = Fraction(row_sum[i], total) * Fraction(col_sum[c], total)
        sol.append(f"Ô (X = {i}, Y = {c}): P(X = {i}) P(Y = {c}) = {num(prod)} nhưng P(X = {i}, Y = {c}) = "
                   f"{_p(counts[i][c], total)}. Một ô lệch là đủ để kết luận X và Y không độc lập (kiểm tra mọi ô, không chỉ một ô). "
                   f"Mệnh đề sai.")
    return Draw(params={"counts": counts, "total": total},
                prompt_vi="Bảng phân phối đồng thời P(X = i, Y = j) ở ma trận P: hàng ứng với X = 0, 1, cột ứng với Y = 0, 1, 2. "
                          "X và Y độc lập.",
                answer=indep, solution_vi=sol, matrices=_table_matrix(counts, total))


# ------------------------------------------------------------------ hiệp phương sai và phương sai của tổ hợp tuyến tính
VALUE_SETS_X = ([0, 1], [1, 2], [-1, 1], [0, 1, 2])
VALUE_SETS_Y = ([0, 1], [1, 2], [0, 1, 2], [1, 2, 3])


def _moments(counts, xs, ys, total):
    px = [Fraction(sum(r), total) for r in counts]
    py = [Fraction(sum(counts[i][j] for i in range(len(xs))), total) for j in range(len(ys))]
    ex = sum(x * p for x, p in zip(xs, px))
    ey = sum(y * p for y, p in zip(ys, py))
    exy = sum(xs[i] * ys[j] * Fraction(counts[i][j], total) for i in range(len(xs)) for j in range(len(ys)))
    vx = sum(x * x * p for x, p in zip(xs, px)) - ex ** 2
    vy = sum(y * y * p for y, p in zip(ys, py)) - ey ** 2
    return ex, ey, exy, vx, vy


def _joint_head(xs, ys) -> str:
    return (f"Bảng phân phối đồng thời P(X = i, Y = j) của (X, Y) ở ma trận P: hàng ứng với X = {_values_text(xs)}, "
            f"cột ứng với Y = {_values_text(ys)}. ")


@generator("xs_g10_hiep_phuong_sai")
def hiep_phuong_sai(rng: random.Random) -> Draw:
    xs, ys = rng.choice(VALUE_SETS_X), rng.choice(VALUE_SETS_Y)
    total = rng.choice([8, 10, 12, 16, 20])
    counts = _draw_counts(rng, len(xs), len(ys), total, zeros=True)
    ex, ey, exy, _, _ = _moments(counts, xs, ys, total)
    cov = exy - ex * ey
    return Draw(
        params={"xs": xs, "ys": ys, "counts": counts, "total": total},
        prompt_vi=_joint_head(xs, ys) + "Tính hiệp phương sai Cov(X, Y) = E(XY) - E(X)E(Y). Nhập một số hoặc phân số tối giản.",
        answer=num(cov),
        solution_vi=[f"E(X) = {num(ex)} (cộng hàng rồi nhân với giá trị của X) và E(Y) = {num(ey)} (cộng cột rồi nhân với giá trị của Y).",
                     f"E(XY) = tổng của x y P(X = x, Y = y) trên mọi ô = {num(exy)}.",
                     f"Cov(X, Y) = {num(exy)} - {paren(ex)} . {paren(ey)} = {num(cov)}."],
        matrices=_table_matrix(counts, total))


@generator("xs_g10_phuong_sai_tong")
def phuong_sai_tong(rng: random.Random) -> Draw:
    xs, ys = rng.choice(VALUE_SETS_X), rng.choice(VALUE_SETS_Y)
    total = rng.choice([8, 10, 12, 16, 20])
    counts = _draw_counts(rng, len(xs), len(ys), total, zeros=True)
    a = rng.choice([-3, -2, -1, 1, 2, 3])
    b = rng.choice([-3, -2, -1, 1, 2, 3])
    ex, ey, exy, vx, vy = _moments(counts, xs, ys, total)
    cov = exy - ex * ey
    var = a * a * vx + b * b * vy + 2 * a * b * cov
    head = f"{a}X" if a not in (1, -1) else ("X" if a == 1 else "-X")
    tail = f"{'+' if b > 0 else '-'} {abs(b)}Y" if abs(b) != 1 else f"{'+' if b > 0 else '-'} Y"
    return Draw(
        params={"xs": xs, "ys": ys, "counts": counts, "total": total, "a": a, "b": b},
        prompt_vi=_joint_head(xs, ys) + f"Tính V({head} {tail}). Nhập một số hoặc phân số tối giản.",
        answer=num(var),
        solution_vi=[f"E(X) = {num(ex)}, E(Y) = {num(ey)}, E(XY) = {num(exy)}, nên Cov(X, Y) = {num(cov)}.",
                     f"V(X) = {num(vx)} và V(Y) = {num(vy)} (E(X^2) - (E(X))^2, E(Y^2) - (E(Y))^2).",
                     f"V(aX + bY) = a^2 V(X) + b^2 V(Y) + 2ab Cov(X, Y) với a = {a}, b = {b}: "
                     f"{a * a} . {paren(vx)} + {b * b} . {paren(vy)} + {2 * a * b} . {paren(cov)} = {num(var)}."],
        matrices=_table_matrix(counts, total))


# ------------------------------------------------------------------ hồi quy tuyến tính đơn
@generator("xs_g10_hoi_quy")
def hoi_quy(rng: random.Random) -> Draw:
    while True:
        n = rng.randint(4, 6)
        start = rng.randint(0, 3)
        step = rng.choice([1, 1, 2])
        xs = [start + step * k for k in range(n)]
        ys = [rng.randint(0, 12) for _ in range(n)]
        if len(set(ys)) > 1:
            break
    xb, yb = Fraction(sum(xs), n), Fraction(sum(ys), n)
    sxx = sum((x - xb) ** 2 for x in xs)
    sxy = sum((x - xb) * (y - yb) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = yb - b * xb
    ask = rng.choice(["he_so_goc", "he_so_chan", "du_doan"])
    x0 = xs[-1] + step * rng.randint(1, 2)
    pts = ", ".join(f"({x}, {y})" for x, y in zip(xs, ys))
    head = f"Mẫu {n} điểm (x, y): {pts}. "
    steps = [f"{_mean_text('x_tb', sum(xs), n)} và {_mean_text('y_tb', sum(ys), n)}.",
             f"Sxx = tổng (x - x_tb)^2 = {num(sxx)}; Sxy = tổng (x - x_tb)(y - y_tb) = {num(sxy)}.",
             f"Hệ số góc b = Sxy/Sxx = {num(b)}."]
    if ask == "he_so_goc":
        prompt, ans = head + "Tìm hệ số góc b của đường hồi quy tuyến tính y theo x (bình phương tối thiểu). Nhập một số hoặc phân số tối giản.", b
    elif ask == "he_so_chan":
        prompt = head + "Tìm hệ số chặn a của đường hồi quy tuyến tính y = a + bx (bình phương tối thiểu). Nhập một số hoặc phân số tối giản."
        ans = a
        steps.append(f"Hệ số chặn a = y_tb - b x_tb = {num(yb)} - {paren(b)} . {paren(xb)} = {num(a)}.")
    else:
        prompt = head + f"Dùng đường hồi quy tuyến tính y theo x (bình phương tối thiểu) để dự đoán y khi x = {x0}. Nhập một số hoặc phân số tối giản."
        ans = a + b * x0
        steps.append(f"Hệ số chặn a = y_tb - b x_tb = {num(a)}; y = {num(a)} + {paren(b)} x.")
        steps.append(f"Tại x = {x0}: y = {num(a)} + {paren(b)} . {x0} = {num(ans)}.")
    return Draw(params={"xs": xs, "ys": ys, "ask": ask, "x0": x0}, prompt_vi=prompt, answer=num(ans), solution_vi=steps)
