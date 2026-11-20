"""Xạ Trường (docs/THUC_CHIEN_TRONG_GAME.md, tier 1): the data the Thực Chiến exercises
train and are scored on, generated from a seed.

Every set is made here, by code, from a seed written in the exercise's JSON ("data":
{"gen": ..., "seeds": [...], "practice_seeds": [...], "params": {...}}). Nothing is
downloaded and nothing has a licence to worry about: the points, the lines, the messages
and the digits are all drawn by this file. The same seed gives the same set on every
machine and every Python 3 (only `random.Random.random` and `gauss` are used, and every
number is printed with a fixed number of decimals).

A generator returns (input, labels):

  * `input` is what the player's program reads on stdin: the training data with its labels,
    then the points to predict, without theirs;
  * `labels` is the truth for those points, one per line. It never leaves the server for a
    hidden set (seeds); for a practice set (practice_seeds) it is shown, like any sample.

Pure Python and standard library only, like everything the player is asked to write.
"""
from __future__ import annotations

import math
import random
from typing import Callable

Generated = tuple[str, str]


def _num(v: float, places: int = 2) -> str:
    text = f"{v:.{places}f}"
    return "0" if text.strip("-0.") == "" else text   # never "-0.00"


def _rows(rows: list[list[float]], places: int = 2) -> str:
    return "".join(" ".join(_num(v, places) for v in row) + "\n" for row in rows)


def _choice(rng: random.Random, seq):
    return seq[int(rng.random() * len(seq))]


def _shuffle(rng: random.Random, items: list) -> None:
    for i in range(len(items) - 1, 0, -1):
        j = int(rng.random() * (i + 1))
        items[i], items[j] = items[j], items[i]


def _labelled(train: list[tuple[list[float], object]], test: list[list[float]], places: int = 2) -> str:
    d = len(train[0][0])
    out = [f"{len(train)} {d}\n"]
    out += [" ".join(_num(v, places) for v in x) + f" {y}\n" for x, y in train]
    out.append(f"{len(test)}\n")
    out.append(_rows(test, places))
    return "".join(out)


# ------------------------------------------------------------------ k láng giềng
def knn_linh_thu(rng: random.Random, n_train: int = 200, n_test: int = 100, centers: int = 7,
                 classes: int = 3, flip: float = 0.05) -> Generated:
    """Points in the square [0, 10]^2. The land belongs to `centers` hidden dens, each of
    one of `classes` kinds of beast; a point is of the kind of its nearest den, and a
    `flip` share of points stray to another kind. Nothing straight separates the kinds,
    so a straight-line rule or a single mean per kind does poorly, and k-NN does well."""
    while True:
        dens = [((rng.random() * 10, rng.random() * 10), i % classes) for i in range(centers)]
        if len({k for _, k in dens}) == classes:
            break

    def point() -> tuple[list[float], int]:
        x = [round(rng.random() * 10, 2), round(rng.random() * 10, 2)]
        _, kind = min(dens, key=lambda d: (d[0][0] - x[0]) ** 2 + (d[0][1] - x[1]) ** 2)
        if rng.random() < flip:
            kind = (kind + 1 + int(rng.random() * (classes - 1))) % classes
        return x, kind
    train = [point() for _ in range(n_train)]
    test = [point() for _ in range(n_test)]
    return _labelled(train, [x for x, _ in test]), "".join(f"{y}\n" for _, y in test)


# ------------------------------------------------------------------ thư rác
# Messages in Vietnamese written without diacritics, the way many text messages are typed
# (and because the exercise data goes through stdin as ASCII). Every word is ours.
_SPAM = [
    "chuc mung quy khach da trung thuong {qua} tri gia {tien} trieu dong",
    "nhan ngay {qua} mien phi khi dang ky goi cuoc moi soan tin gui {so}",
    "vay tien nhanh lai suat thap chi can can cuoc giai ngan trong ngay lien he {so}",
    "khuyen mai soc giam gia {phan} phan tram tat ca san pham chi hom nay bam link {link}",
    "tai khoan cua ban sap bi khoa vui long xac nhan thong tin tai {link}",
    "co hoi viec lam them tai nha thu nhap {tien} trieu moi thang khong can kinh nghiem",
    "ban da duoc chon nhan qua tri an {qua} nhan qua tai {link} truoc ngay mai",
    "nap the hom nay tang {phan} phan tram gia tri the cao chuong trinh co han",
    "uu dai dac biet danh rieng cho ban mua mot tang mot lien he {so} ngay",
    "dau tu sinh loi {phan} phan tram moi tuan cam ket hoan von bam {link}",
    "xo so trung thuong lon quay so mien phi moi ngay soan tin {so}",
    "goi vip moi khuyen mai lon dang ky ngay de nhan {tien} trieu vao tai khoan",
]
_HAM = [
    "toi nay {ai} ve an com khong de {ai2} nau them",
    "mai hop lop luc {gio} gio nho mang theo bao cao nhe",
    "{ai} oi chieu nay di da bong khong cho cu",
    "con da den truong roi {ai} dung lo",
    "sieu thi dang khuyen mai sua {ai} mua them hai hop nhe",
    "toi gui ban file bai tap giai tich chieu nay xem giup nhe",
    "nho tra tien dien thang nay cho {ai} nhe",
    "cuoi tuan nay ca nha ve que tham {ai2} nhe",
    "{ai} co the cho minh muon sach xac suat thong ke khong",
    "nhom minh hop luc {gio} gio o thu vien nhe ai den truoc giu cho",
    "chuc mung sinh nhat {ai} nhe chuc moi dieu tot dep",
    "minh vua trung tuyen thuc tap roi toi nay di an mung nhe",
    "ban oi link tai lieu mon hoc may minh gui o nhom roi do",
    "{ai} nho uong thuoc dung gio nhe mai con ve",
    "tien do an thang nay minh chuyen roi nhe ban kiem tra giup",
]
_FILL = {
    "qua": ["xe may", "dien thoai", "phieu mua hang", "chuyen du lich", "laptop", "vang"],
    "tien": ["5", "10", "20", "50", "100"],
    "phan": ["30", "50", "70", "90"],
    "so": ["9029", "8077", "6066", "1900 1234"],
    "link": ["bitly vn qua", "tinyurl nhanqua", "khuyenmai vip", "nhanthuong online"],
    "ai": ["me", "bo", "anh", "chi", "em", "ban"],
    "ai2": ["ong ba", "co chu", "me", "bo", "chi hai"],
    "gio": ["bay", "tam", "chin", "hai", "ba"],
}
_EVERYDAY = ("nhe oi a roi nha vay di ve hom nay mai ban minh toi la co khong duoc cho "
             "luc nay con em anh chi").split()


def _message(rng: random.Random, template: str, drop: float, noise: int) -> list[str]:
    text = template
    while "{" in text:
        a = text.index("{")
        b = text.index("}", a)
        text = text[:a] + _choice(rng, _FILL[text[a + 1:b]]) + text[b + 1:]
    words = [w for w in text.split() if rng.random() >= drop]
    for _ in range(int(rng.random() * (noise + 1))):
        words.insert(int(rng.random() * (len(words) + 1)), _choice(rng, _EVERYDAY))
    return words or [_choice(rng, _EVERYDAY)]


def nb_thu_rac(rng: random.Random, n_train: int = 300, n_test: int = 150, spam_share: float = 0.35,
               drop: float = 0.35, noise: int = 4, mix: float = 0.3, flip: float = 0.02) -> Generated:
    """Messages made from the templates above: words dropped at random, everyday words
    thrown in, and a `mix` share of messages that borrow half of their words from a
    template of the other kind (an honest message about a sale, spam that sounds like a
    friend). A `flip` share is labelled the other way, as real data is."""
    def one() -> tuple[list[str], int]:
        spam = rng.random() < spam_share
        words = _message(rng, _choice(rng, _SPAM if spam else _HAM), drop, noise)
        if rng.random() < mix:
            other = _message(rng, _choice(rng, _HAM if spam else _SPAM), 0.5, 0)
            words += other[:max(1, len(other) // 3)]
        label = int(spam)
        if rng.random() < flip:
            label = 1 - label
        return words, label
    train = [one() for _ in range(n_train)]
    test = [one() for _ in range(n_test)]
    text = [f"{n_train}\n"] + [f"{y} {' '.join(w)}\n" for w, y in train]
    text += [f"{n_test}\n"] + [" ".join(w) + "\n" for w, _ in test]
    return "".join(text), "".join(f"{y}\n" for _, y in test)


# ------------------------------------------------------------------ hồi quy
def hq_duong_thang(rng: random.Random, n_train: int = 100, n_test: int = 50, noise: float = 1.0) -> Generated:
    """y = a*x + b + noise, with x in [0, 10], |a| in [1, 3] and b in [-5, 5]. The labels
    of the points to predict carry the same noise: that is how a model is judged."""
    a = (1 + 2 * rng.random()) * (1 if rng.random() < 0.5 else -1)
    b = -5 + 10 * rng.random()

    def point() -> tuple[float, float]:
        x = round(10 * rng.random(), 2)
        return x, round(a * x + b + rng.gauss(0, noise), 2)
    train = [point() for _ in range(n_train)]
    test = [point() for _ in range(n_test)]
    text = [f"{n_train}\n"] + [f"{_num(x)} {_num(y)}\n" for x, y in train]
    text += [f"{n_test}\n"] + [f"{_num(x)}\n" for x, _ in test]
    return "".join(text), "".join(f"{_num(y)}\n" for _, y in test)


SCALES = (1.0, 10.0, 100.0, 0.1)


def bptt_nhieu_bien(rng: random.Random, n_train: int = 120, n_test: int = 60, noise: float = 0.5) -> Generated:
    """y = w.x + b + noise with four features on very different scales (about 1, 10, 100
    and 0.1), the second one correlated with the first. Normal equations do not care about
    scales; plain gradient descent on raw features crawls."""
    d = len(SCALES)
    w = [(1 + 2 * rng.random()) * (1 if rng.random() < 0.5 else -1) / s for s in SCALES]
    b = -5 + 10 * rng.random()

    def point() -> tuple[list[float], float]:
        z = [rng.gauss(0, 1) for _ in range(d)]
        z[1] = 0.6 * z[0] + 0.8 * z[1]
        x = [round(3 * s + s * v, 3) for s, v in zip(SCALES, z)]
        y = sum(wi * xi for wi, xi in zip(w, x)) + b + rng.gauss(0, noise)
        return x, round(y, 3)
    train = [point() for _ in range(n_train)]
    test = [point() for _ in range(n_test)]
    text = [f"{n_train} {d}\n"] + [" ".join(_num(v, 3) for v in x) + f" {_num(y, 3)}\n" for x, y in train]
    text += [f"{n_test}\n"] + [" ".join(_num(v, 3) for v in x) + "\n" for x, _ in test]
    return "".join(text), "".join(f"{_num(y, 3)}\n" for _, y in test)


# ------------------------------------------------------------------ mạng nơ-ron
def nn_vong_tron(rng: random.Random, n_train: int = 200, n_test: int = 100, radius: float = 0.8,
                 flip: float = 0.03) -> Generated:
    """Points in [-1, 1]^2: kind 1 inside the circle of `radius` (about half of the
    square), kind 0 outside. No straight line separates them; one hidden layer does."""
    def point() -> tuple[list[float], int]:
        x = [round(2 * rng.random() - 1, 3), round(2 * rng.random() - 1, 3)]
        y = int(x[0] ** 2 + x[1] ** 2 < radius ** 2)
        if rng.random() < flip:
            y = 1 - y
        return x, y
    train = [point() for _ in range(n_train)]
    test = [point() for _ in range(n_test)]
    return _labelled(train, [x for x, _ in test], 3), "".join(f"{y}\n" for _, y in test)


# ------------------------------------------------------------------ logistic
def lg_linh_thao(rng: random.Random, n_train: int = 200, n_test: int = 100, d: int = 5,
                 gap: float = 2.8, share: float = 0.4) -> Generated:
    """Two kinds of herb measured five ways. Each kind is a cloud around its own centre,
    the two centres `gap` standard deviations apart (the best possible rule is right about
    Phi(gap/2) of the time, about 92%), each measure on its own scale and offset."""
    direction = [rng.gauss(0, 1) for _ in range(d)]
    norm = math.sqrt(sum(v * v for v in direction))
    direction = [v / norm for v in direction]
    scale = [0.5 + 4.5 * rng.random() for _ in range(d)]
    offset = [-10 + 20 * rng.random() for _ in range(d)]

    def point() -> tuple[list[float], int]:
        y = int(rng.random() < share)
        sign = 0.5 if y else -0.5
        x = [offset[i] + scale[i] * (rng.gauss(0, 1) + sign * gap * direction[i]) for i in range(d)]
        return [round(v, 3) for v in x], y
    train = [point() for _ in range(n_train)]
    test = [point() for _ in range(n_test)]
    return _labelled(train, [x for x, _ in test], 3), "".join(f"{y}\n" for _, y in test)


# ------------------------------------------------------------------ PCA
def pca_khu_nhieu(rng: random.Random, n_train: int = 150, n_test: int = 50, d: int = 8, k: int = 2,
                  noise: float = 0.5) -> Generated:
    """Clean points lie on a k-dimensional plane through a centre in R^d (the plane spans k
    random orthonormal directions, with spreads 3 and 2 along them); every point we see has
    noise of standard deviation `noise` in every one of the d coordinates. The labels are
    the clean points: projecting on the plane removes the noise that sticks out of it."""
    basis: list[list[float]] = []
    while len(basis) < k:                       # Gram-Schmidt on random directions
        v = [rng.gauss(0, 1) for _ in range(d)]
        for u in basis:
            dot = sum(a * b for a, b in zip(u, v))
            v = [a - dot * b for a, b in zip(v, u)]
        n = math.sqrt(sum(a * a for a in v))
        if n > 1e-6:
            basis.append([a / n for a in v])
    spread = [3.0, 2.0, 1.5, 1.2][:k]
    centre = [-5 + 10 * rng.random() for _ in range(d)]

    def point() -> tuple[list[float], list[float]]:
        z = [rng.gauss(0, s) for s in spread]
        clean = [centre[i] + sum(z[j] * basis[j][i] for j in range(k)) for i in range(d)]
        seen = [c + rng.gauss(0, noise) for c in clean]
        return [round(v, 3) for v in seen], [round(v, 3) for v in clean]
    train = [point()[0] for _ in range(n_train)]
    test = [point() for _ in range(n_test)]
    text = [f"{n_train} {d} {k}\n", _rows(train, 3), f"{n_test}\n", _rows([s for s, _ in test], 3)]
    return "".join(text), _rows([c for _, c in test], 3)


# ------------------------------------------------------------------ A/B
def ab_ket_luan(rng: random.Random, experiments: int = 100, null_share: float = 0.5,
                effect_se: float = 4.5) -> Generated:
    """`experiments` A/B tests. Each has its own size n per arm (200 to 5000, spread
    evenly on a log scale) and its own base rate. In a `null_share` of them A and B are
    truly the same; in the rest one is better by `effect_se` standard errors of the
    difference, so a 5% two-sided test finds it about 99% of the time. Counts use the
    normal approximation to the binomial (exact enough at these sizes, and fast).
    The truth is A, B or 0 (no real difference)."""
    rows, truth = [], []
    for _ in range(experiments):
        n = int(round(math.exp(math.log(200) + rng.random() * (math.log(5000) - math.log(200)))))
        p = 0.1 + 0.8 * rng.random()
        if rng.random() < null_share:
            pa = pb = p
            winner = "0"
        else:
            delta = effect_se * math.sqrt(2 * p * (1 - p) / n)
            if rng.random() < 0.5:
                pa, pb, winner = p, min(0.99, p + delta), "B"
            else:
                pa, pb, winner = min(0.99, p + delta), p, "A"

        def count(q: float) -> int:
            k = round(n * q + math.sqrt(n * q * (1 - q)) * rng.gauss(0, 1))
            return max(0, min(n, int(k)))
        rows.append(f"{n} {count(pa)} {n} {count(pb)}\n")
        truth.append(f"{winner}\n")
    return f"{experiments}\n" + "".join(rows), "".join(truth)


# ------------------------------------------------------------------ chữ số
# Ten digits as strokes in a unit box (x to the right, y down), the way one writes them.
# Each stroke is a polyline; curves are a few short segments.
def _arc(cx: float, cy: float, rx: float, ry: float, a0: float, a1: float, steps: int = 8) -> list[tuple[float, float]]:
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / steps), cy + ry * math.sin(a0 + (a1 - a0) * i / steps))
            for i in range(steps + 1)]


_PI = math.pi
#: digit -> its writing styles; a style is a list of strokes. People write 1, 4, 7 and 9 in
#: more than one way, which is exactly what a single "average digit" cannot capture.
DIGIT_STROKES: dict[int, list[list[list[tuple[float, float]]]]] = {
    0: [[_arc(0.5, 0.5, 0.28, 0.40, 0, 2 * _PI, 12)],
        [_arc(0.5, 0.5, 0.2, 0.40, 0, 2 * _PI, 12)]],
    1: [[[(0.35, 0.25), (0.55, 0.1), (0.55, 0.9)]],
        [[(0.35, 0.25), (0.55, 0.1), (0.55, 0.9)], [(0.33, 0.9), (0.77, 0.9)]],
        [[(0.52, 0.1), (0.48, 0.9)]]],
    2: [[_arc(0.5, 0.32, 0.27, 0.22, -_PI, 0.25 * _PI, 6) + [(0.22, 0.9), (0.8, 0.9)]]],
    3: [[_arc(0.48, 0.3, 0.26, 0.2, -0.9 * _PI, 0.5 * _PI, 6), _arc(0.48, 0.69, 0.29, 0.21, -0.5 * _PI, 0.9 * _PI, 6)],
        [[(0.25, 0.1), (0.75, 0.1), (0.45, 0.42)] + _arc(0.48, 0.67, 0.29, 0.23, -0.5 * _PI, 0.9 * _PI, 6)]],
    4: [[[(0.6, 0.1), (0.2, 0.62), (0.82, 0.62)], [(0.62, 0.35), (0.62, 0.9)]],
        [[(0.3, 0.1), (0.26, 0.55), (0.8, 0.55)], [(0.66, 0.2), (0.66, 0.9)]]],
    5: [[[(0.78, 0.1), (0.3, 0.1), (0.27, 0.45)] + _arc(0.48, 0.65, 0.29, 0.24, -0.75 * _PI, 0.85 * _PI, 7)]],
    6: [[[(0.7, 0.12), (0.4, 0.3), (0.24, 0.62)], _arc(0.5, 0.67, 0.26, 0.22, 0, 2 * _PI, 10)]],
    7: [[[(0.2, 0.1), (0.8, 0.1), (0.42, 0.9)]],
        [[(0.2, 0.1), (0.8, 0.1), (0.42, 0.9)], [(0.38, 0.5), (0.74, 0.5)]]],
    8: [[_arc(0.5, 0.29, 0.22, 0.19, 0, 2 * _PI, 10), _arc(0.5, 0.69, 0.27, 0.21, 0, 2 * _PI, 10)]],
    9: [[_arc(0.5, 0.33, 0.26, 0.22, 0, 2 * _PI, 10), [(0.76, 0.35), (0.62, 0.65), (0.35, 0.9)]],
        [_arc(0.5, 0.33, 0.26, 0.22, 0, 2 * _PI, 10), [(0.76, 0.33), (0.74, 0.9)]]],
}


def _segments(rng: random.Random, digit: int) -> list[tuple[float, float, float, float]]:
    """The digit's strokes after a random slant, rotation, size, shift and wobble."""
    angle = rng.gauss(0, 0.08)
    shear = rng.gauss(0, 0.12)
    sx, sy = 0.78 + 0.22 * rng.random(), 0.8 + 0.2 * rng.random()
    dx, dy = rng.gauss(0, 0.05), rng.gauss(0, 0.045)
    ca, sa = math.cos(angle), math.sin(angle)
    out = []
    for stroke in _choice(rng, DIGIT_STROKES[digit]):
        pts = []
        for x, y in stroke:
            x, y = (x - 0.5) * sx, (y - 0.5) * sy
            x += shear * -y
            x, y = ca * x - sa * y, sa * x + ca * y
            pts.append((x + 0.5 + dx + rng.gauss(0, 0.015), y + 0.5 + dy + rng.gauss(0, 0.015)))
        out += [(a[0], a[1], b[0], b[1]) for a, b in zip(pts, pts[1:])]
    return out


def _render(rng: random.Random, digit: int, size: int = 8) -> list[int]:
    """Rasterise on a size x size grid with values 0..16: ink falls off with the distance
    from the pixel centre to the nearest stroke, then a little noise is added."""
    segs = _segments(rng, digit)
    width = 0.07 + 0.05 * rng.random()
    ink = 13 + 3 * rng.random()
    pixels = []
    for r in range(size):
        py = (r + 0.5) / size
        for c in range(size):
            px = (c + 0.5) / size
            best = 9.0
            for x0, y0, x1, y1 in segs:
                vx, vy = x1 - x0, y1 - y0
                ln = vx * vx + vy * vy
                t = 0.0 if ln == 0 else max(0.0, min(1.0, ((px - x0) * vx + (py - y0) * vy) / ln))
                ex, ey = x0 + t * vx - px, y0 + t * vy - py
                dd = ex * ex + ey * ey
                if dd < best:
                    best = dd
            v = ink * max(0.0, 1 - (math.sqrt(best) - width) / 0.09) if best > width * width else ink
            v += rng.gauss(0, 1.0)
            pixels.append(max(0, min(16, int(round(v)))))
    return pixels


def digit_image(rng: random.Random, digit: int, size: int = 8) -> list[int]:
    return _render(rng, digit, size)


def da_chu_so(rng: random.Random, n_train: int = 600, n_test: int = 150, size: int = 8) -> Generated:
    """Synthetic handwritten digits, size x size pixels with values 0..16 (the format of the
    8x8 digits often used to teach): strokes drawn by DIGIT_STROKES, then slanted, turned,
    scaled, shifted, thickened or thinned, and sprinkled with noise. Digits in equal
    shares, in random order."""
    def batch(n: int) -> list[tuple[list[int], int]]:
        labels = [i % 10 for i in range(n)]
        _shuffle(rng, labels)
        return [(_render(rng, y, size), y) for y in labels]
    train, test = batch(n_train), batch(n_test)
    text = [f"{n_train} {size * size}\n"] + [" ".join(map(str, x)) + f" {y}\n" for x, y in train]
    text += [f"{n_test}\n"] + [" ".join(map(str, x)) + "\n" for x, _ in test]
    return "".join(text), "".join(f"{y}\n" for _, y in test)


GENERATORS: dict[str, Callable[..., Generated]] = {
    "knn_linh_thu": knn_linh_thu,
    "nb_thu_rac": nb_thu_rac,
    "hq_duong_thang": hq_duong_thang,
    "bptt_nhieu_bien": bptt_nhieu_bien,
    "nn_vong_tron": nn_vong_tron,
    "lg_linh_thao": lg_linh_thao,
    "pca_khu_nhieu": pca_khu_nhieu,
    "ab_ket_luan": ab_ket_luan,
    "da_chu_so": da_chu_so,
}


def generate(name: str, seed: int, params: dict | None = None) -> Generated:
    """One set: the same name, seed and params always give the same text."""
    return GENERATORS[name](random.Random(seed), **(params or {}))
