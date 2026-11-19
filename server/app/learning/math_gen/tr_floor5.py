"""Tối Ưu và Toán Rời Rạc, floor 5 (đồ thị: khái niệm cơ bản, biểu diễn trên máy tính):
generators. Ids start with `tr_g5_`.

A graph has no picture in the game, so it is always given as text that cannot be misread:
its vertices 1..n and its edge list, its adjacency lists, or (4 vertices) its adjacency
matrix. The generators count the way the floor teaches (degrees, neighbours, union-find,
Havel-Hakimi); tools/math_verify_tr_t4.py works from the adjacency matrix with sympy instead
(traces and powers, the rank of the Laplacian, the Erdős-Gallai inequalities)."""
from __future__ import annotations

import itertools
import random

from . import Draw, generator


# ------------------------------------------------------------------ graphs as text (also used by floor 6)
def edge_text(edges) -> str:
    return ", ".join(f"{u}-{v}" for u, v in edges)


def graph_text(n: int, edges) -> str:
    return f"các đỉnh 1, 2, ..., {n}; các cạnh: {edge_text(edges)}"


def neighbours(n: int, edges) -> dict[int, list[int]]:
    out = {v: [] for v in range(1, n + 1)}
    for u, v in edges:
        out[u].append(v)
        out[v].append(u)
    return {v: sorted(ns) for v, ns in out.items()}


def degrees(n: int, edges) -> list[int]:
    nb = neighbours(n, edges)
    return [len(nb[v]) for v in range(1, n + 1)]


def norm(edges) -> list[list[int]]:
    """Edges as sorted [u, v] with u < v, in lexicographic order (also the JSON params form)."""
    return sorted([min(u, v), max(u, v)] for u, v in edges)


def random_graph(rng: random.Random, n: int, m: int) -> list[list[int]]:
    pairs = list(itertools.combinations(range(1, n + 1), 2))
    return norm(rng.sample(pairs, m))


def connected_graph(rng: random.Random, n: int, extra: int) -> list[list[int]]:
    """A random spanning tree plus `extra` more edges: always connected."""
    order = list(range(1, n + 1))
    rng.shuffle(order)
    edges = {tuple(sorted((order[i], order[rng.randrange(i)]))) for i in range(1, n)}
    others = [p for p in itertools.combinations(range(1, n + 1), 2) if p not in edges]
    edges |= set(rng.sample(others, min(extra, len(others))))
    return norm(edges)


def components(n: int, edges) -> list[list[int]]:
    """Union-find; each component sorted, components ordered by their smallest vertex."""
    parent = list(range(n + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v)
    groups: dict[int, list[int]] = {}
    for v in range(1, n + 1):
        groups.setdefault(find(v), []).append(v)
    return sorted(groups.values())


def clustered_graph(rng: random.Random, n: int, k: int) -> list[list[int]]:
    """A graph with exactly k components: the vertices are split into k groups, each joined by
    a random tree plus maybe one more edge."""
    order = list(range(1, n + 1))
    rng.shuffle(order)
    cuts = sorted(rng.sample(range(1, n), k - 1))
    groups = [order[a:b] for a, b in zip([0] + cuts, cuts + [n])]
    edges = set()
    for g in groups:
        for i in range(1, len(g)):
            edges.add(tuple(sorted((g[i], g[rng.randrange(i)]))))
        inside = [p for p in itertools.combinations(sorted(g), 2) if p not in edges]
        if inside and rng.random() < 0.6:
            edges.add(rng.choice(inside))
    return norm(edges)


# ------------------------------------------------------------------ khái niệm
@generator("tr_g5_day_du")
def day_du(rng: random.Random) -> Draw:
    kind = rng.choice(["kn", "kmn", "bu", "co_huong"])
    if kind == "kn":
        n = rng.randint(4, 15)
        params = {"kind": kind, "n": n}
        prompt = f"Đồ thị đầy đủ K_{n} (đồ thị đơn vô hướng {n} đỉnh, mọi cặp đỉnh khác nhau đều kề nhau) có bao nhiêu cạnh?"
        total = n * (n - 1) // 2
        steps = [f"Mỗi cạnh ứng với một cặp hai đỉnh không kể thứ tự: C_{n}^2 cạnh.",
                 f"C_{n}^2 = {n} . {n - 1}/2 = {total}."]
    elif kind == "kmn":
        a, b = rng.randint(2, 7), rng.randint(2, 7)
        params = {"kind": kind, "a": a, "b": b}
        prompt = (f"Đồ thị hai phía đầy đủ K_({a}, {b}) có một phần {a} đỉnh, một phần {b} đỉnh, và mỗi đỉnh phần này kề "
                  "mọi đỉnh phần kia (không có cạnh trong cùng một phần). Nó có bao nhiêu cạnh?")
        total = a * b
        steps = [f"Mỗi cạnh nối một trong {a} đỉnh phần thứ nhất với một trong {b} đỉnh phần thứ hai.",
                 f"Theo quy tắc nhân có {a} . {b} = {total} cạnh."]
    elif kind == "bu":
        n = rng.randint(5, 12)
        m = rng.randint(n - 2, n * (n - 1) // 2 - 2)
        params = {"kind": kind, "n": n, "m": m}
        prompt = (f"Đồ thị đơn vô hướng G có {n} đỉnh và {m} cạnh. Đồ thị bù của G (cùng tập đỉnh, hai đỉnh kề nhau khi "
                  "và chỉ khi chúng không kề nhau trong G) có bao nhiêu cạnh?")
        full = n * (n - 1) // 2
        total = full - m
        steps = [f"Mỗi cặp đỉnh là cạnh của đúng một trong hai đồ thị G và đồ thị bù, nên tổng số cạnh là C_{n}^2 = {full}.",
                 f"Đồ thị bù có {full} - {m} = {total} cạnh."]
    else:
        n = rng.randint(3, 12)
        params = {"kind": kind, "n": n}
        prompt = (f"Một đồ thị có hướng {n} đỉnh không có khuyên, và với mỗi cặp đỉnh có thứ tự (u, v), u khác v, có đúng "
                  "một cung đi từ u đến v. Đồ thị có bao nhiêu cung?")
        total = n * (n - 1)
        steps = ["Mỗi cung ứng với một cặp có thứ tự gồm hai đỉnh khác nhau.",
                 f"Có A_{n}^2 = {n} . {n - 1} = {total} cung (gấp đôi số cạnh của K_{n})."]
    return Draw(params=params, prompt_vi=prompt, answer=str(total), solution_vi=steps)


def two_colouring(n: int, edges) -> dict[int, int] | None:
    nb = neighbours(n, edges)
    colour: dict[int, int] = {}
    for s in range(1, n + 1):
        if s in colour:
            continue
        colour[s] = 0
        queue = [s]
        while queue:
            u = queue.pop(0)
            for v in nb[u]:
                if v not in colour:
                    colour[v] = 1 - colour[u]
                    queue.append(v)
                elif colour[v] == colour[u]:
                    return None
    return colour


@generator("tr_g5_hai_phia")
def hai_phia(rng: random.Random) -> Draw:
    n = rng.randint(6, 7)
    want = rng.random() < 0.5
    labels = list(range(1, n + 1))
    rng.shuffle(labels)
    if want:
        k = rng.randint(2, n - 2)
        left, right = labels[:k], labels[k:]
        cross = [tuple(sorted(p)) for p in itertools.product(left, right)]
        edges = rng.sample(cross, rng.randint(n - 1, min(len(cross), n + 2)))
    else:
        cyc = labels[:rng.choice([3, 5])]
        edges = {tuple(sorted((cyc[i], cyc[(i + 1) % len(cyc)]))) for i in range(len(cyc))}
        others = [p for p in itertools.combinations(range(1, n + 1), 2) if p not in edges]
        edges = list(edges | set(rng.sample(others, rng.randint(2, 4))))
    edges = norm(edges)
    colour = two_colouring(n, edges)
    ok = colour is not None
    if ok:
        a = [v for v in range(1, n + 1) if colour[v] == 0]
        b = [v for v in range(1, n + 1) if colour[v] == 1]
        steps = ["Tô màu dần theo BFS: một đỉnh màu A thì mọi đỉnh kề nó màu B, và ngược lại.",
                 f"Được hai phần {{{', '.join(map(str, a))}}} và {{{', '.join(map(str, b))}}}, mỗi cạnh nối hai phần khác nhau.",
                 "Vậy G là đồ thị hai phía: khẳng định đúng."]
    else:
        steps = ["Đồ thị hai phía không thể có chu trình độ dài lẻ: đi quanh chu trình, màu phải đổi ở mỗi cạnh.",
                 "Thử tô hai màu theo BFS thì gặp một cạnh có hai đầu cùng màu: G có chu trình độ dài lẻ "
                 f"(chu trình lẻ ngắn nhất của G có {_odd_len(n, edges)} đỉnh).",
                 "Vậy G không là đồ thị hai phía: khẳng định sai."]
    return Draw(params={"n": n, "edges": edges},
                prompt_vi=f"Đồ thị G có {graph_text(n, edges)}. Khẳng định: G là đồ thị hai phía.",
                answer=ok, solution_vi=steps)


def _odd_len(n: int, edges) -> int:
    """Length of a shortest odd cycle (BFS from every vertex)."""
    nb = neighbours(n, edges)
    best = n + 1
    for s in range(1, n + 1):
        dist = {s: 0}
        queue = [s]
        while queue:
            u = queue.pop(0)
            for v in nb[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
                elif dist[v] == dist[u]:
                    best = min(best, 2 * dist[u] + 1)
    return best


# ------------------------------------------------------------------ bậc
@generator("tr_g5_bat_tay")
def bat_tay(rng: random.Random) -> Draw:
    n = rng.randint(6, 8)
    edges = random_graph(rng, n, rng.randint(n, 2 * n))
    deg = degrees(n, edges)
    total = sum(deg)
    return Draw(params={"n": n, "edges": edges},
                prompt_vi=(f"Một đồ thị đơn vô hướng có {n} đỉnh; bậc của các đỉnh 1, 2, ..., {n} lần lượt là "
                           f"{', '.join(map(str, deg))}. Đồ thị có bao nhiêu cạnh?"),
                answer=str(total // 2),
                solution_vi=["Định lý bắt tay: tổng các bậc bằng hai lần số cạnh, vì mỗi cạnh góp 1 vào bậc của mỗi đầu.",
                             f"Tổng các bậc: {' + '.join(map(str, deg))} = {total}.",
                             f"Số cạnh: {total}/2 = {total // 2}."])


def havel_hakimi(seq) -> tuple[bool, list[str]]:
    seq = sorted(seq, reverse=True)
    lines = []
    while True:
        if any(d < 0 for d in seq):
            lines.append("Xuất hiện bậc âm: không dựng được.")
            return False, lines
        seq = sorted(seq, reverse=True)
        if not seq or seq[0] == 0:
            lines.append("Còn lại toàn số 0: dựng được.")
            return True, lines
        d, rest = seq[0], seq[1:]
        if d > len(rest):
            lines.append(f"Một đỉnh cần bậc {d} nhưng chỉ còn {len(rest)} đỉnh khác: không dựng được.")
            return False, lines
        new = [x - 1 for x in rest[:d]] + rest[d:]
        lines.append(f"Bỏ đỉnh bậc {d}, trừ 1 ở {d} bậc lớn nhất còn lại: {', '.join(map(str, sorted(new, reverse=True)))}.")
        seq = new


@generator("tr_g5_day_bac")
def day_bac(rng: random.Random) -> Draw:
    n = rng.randint(5, 6)
    mode = rng.choice(["graph", "graph", "random", "odd"])
    if mode == "graph":
        seq = sorted(degrees(n, random_graph(rng, n, rng.randint(n - 1, 2 * n - 2))), reverse=True)
    else:
        while True:
            seq = sorted((rng.randint(1, n - 1) for _ in range(n)), reverse=True)
            if (sum(seq) % 2 == 1) == (mode == "odd"):
                break
    if sum(seq) % 2:
        ok, lines = False, [f"Tổng các bậc là {sum(seq)}, một số lẻ; theo định lý bắt tay tổng các bậc luôn chẵn.",
                            "Vậy không có đồ thị nào có dãy bậc này."]
    else:
        ok, lines = havel_hakimi(seq)
        lines = [f"Tổng các bậc {sum(seq)} là số chẵn, nên phải thử dựng (thuật toán Havel-Hakimi): nối đỉnh bậc lớn "
                 "nhất với các đỉnh có bậc lớn nhất tiếp theo."] + lines
    lines.append("Khẳng định đúng." if ok else "Khẳng định sai.")
    return Draw(params={"seq": seq},
                prompt_vi=(f"Khẳng định: có một đồ thị đơn vô hướng {n} đỉnh mà bậc của các đỉnh là "
                           f"{', '.join(map(str, seq))}."),
                answer=ok, solution_vi=lines)


# ------------------------------------------------------------------ liên thông
@generator("tr_g5_lien_thong")
def lien_thong(rng: random.Random) -> Draw:
    n = rng.randint(7, 9)
    k = rng.randint(1, 4)
    edges = clustered_graph(rng, n, k)
    comps = components(n, edges)
    shown = "; ".join("{" + ", ".join(map(str, c)) + "}" for c in comps)
    return Draw(params={"n": n, "edges": edges},
                prompt_vi=f"Đồ thị G có {graph_text(n, edges)}. G có bao nhiêu thành phần liên thông?",
                answer=str(len(comps)),
                solution_vi=["Bắt đầu từ đỉnh nhỏ nhất chưa xét, đi theo các cạnh để gom mọi đỉnh nối được với nó; "
                             "lặp lại với đỉnh nhỏ nhất còn lại. Đỉnh không có cạnh nào là một thành phần riêng.",
                             f"Các thành phần: {shown}.",
                             f"G có {len(comps)} thành phần liên thông."])


# ------------------------------------------------------------------ ma trận kề
@generator("tr_g5_hanh_trinh_2")
def hanh_trinh_2(rng: random.Random) -> Draw:
    n = rng.randint(5, 6)
    edges = random_graph(rng, n, rng.randint(n, 2 * n - 1))
    u, v = sorted(rng.sample(range(1, n + 1), 2))
    nb = neighbours(n, edges)
    common = sorted(set(nb[u]) & set(nb[v]))
    return Draw(params={"n": n, "edges": edges, "u": u, "v": v},
                prompt_vi=(f"Đồ thị G có {graph_text(n, edges)}. Gọi A là ma trận kề của G. Phần tử hàng {u} cột {v} của "
                           "A^2 bằng bao nhiêu?"),
                answer=str(len(common)),
                solution_vi=[f"Phần tử ({u}, {v}) của A^2 là tổng các tích a_{u}w . a_w{v}: nó đếm các đỉnh w kề cả {u} "
                             f"lẫn {v}, tức số đường đi độ dài 2 từ {u} đến {v}.",
                             f"Đỉnh kề {u}: {', '.join(map(str, nb[u])) or 'không có'}; đỉnh kề {v}: "
                             f"{', '.join(map(str, nb[v])) or 'không có'}.",
                             f"Đỉnh kề cả hai: {', '.join(map(str, common)) or 'không có'}; phần tử bằng {len(common)}."])


@generator("tr_g5_hanh_trinh_3")
def hanh_trinh_3(rng: random.Random) -> Draw:
    n = 5
    edges = random_graph(rng, n, rng.randint(5, 8))
    u, v = sorted(rng.sample(range(1, n + 1), 2))
    nb = neighbours(n, edges)
    parts = [(a, len(set(nb[a]) & set(nb[v]))) for a in nb[u]]
    total = sum(c for _, c in parts)
    detail = "; ".join(f"a = {a}: {c} cách chọn b" for a, c in parts) or f"đỉnh {u} không có đỉnh kề"
    return Draw(params={"n": n, "edges": edges, "u": u, "v": v},
                prompt_vi=(f"Đồ thị G có {graph_text(n, edges)}. Một hành trình độ dài 3 từ {u} đến {v} là một dãy đỉnh "
                           f"{u}, a, b, {v} mà mỗi hai đỉnh liền nhau kề nhau (đỉnh được phép lặp lại). Có bao nhiêu hành "
                           f"trình như vậy? (Đó là phần tử hàng {u} cột {v} của A^3, A là ma trận kề.)"),
                answer=str(total),
                solution_vi=[f"Chọn a kề {u}, rồi b kề cả a lẫn {v}.",
                             f"Đỉnh kề {u}: {', '.join(map(str, nb[u])) or 'không có'}; đỉnh kề {v}: "
                             f"{', '.join(map(str, nb[v])) or 'không có'}.",
                             detail + ".",
                             f"Cộng lại: {total} hành trình."])


@generator("tr_g5_ma_tran_canh")
def ma_tran_canh(rng: random.Random) -> Draw:
    while True:
        edges = random_graph(rng, 4, rng.randint(2, 6))
        if edges:
            break
    a = [[0] * 4 for _ in range(4)]
    for u, v in edges:
        a[u - 1][v - 1] = a[v - 1][u - 1] = 1
    kind = rng.choice(["edges", "degree"])
    if kind == "edges":
        total = sum(sum(r) for r in a)
        params = {"edges": edges, "kind": kind}
        prompt = "A là ma trận kề của một đồ thị đơn vô hướng có 4 đỉnh 1, 2, 3, 4. Đồ thị có bao nhiêu cạnh?"
        answer = total // 2
        steps = ["Mỗi cạnh u-v cho hai số 1 trong A: ở vị trí (u, v) và (v, u).",
                 f"Tổng mọi phần tử của A là {total}.", f"Số cạnh: {total}/2 = {answer}."]
    else:
        w = rng.randint(1, 4)
        params = {"edges": edges, "kind": kind, "w": w}
        prompt = f"A là ma trận kề của một đồ thị đơn vô hướng có 4 đỉnh 1, 2, 3, 4. Đỉnh {w} có bậc bao nhiêu?"
        answer = sum(a[w - 1])
        steps = [f"Bậc của đỉnh {w} là số đỉnh kề nó, tức số số 1 trên hàng {w} của A.",
                 f"Hàng {w}: {' '.join(map(str, a[w - 1]))}; tổng bằng {answer}."]
    return Draw(params=params, prompt_vi=prompt, answer=str(answer), solution_vi=steps, matrices={"A": a})


# ------------------------------------------------------------------ danh sách kề
@generator("tr_g5_ban_bac_vao")
def ban_bac_vao(rng: random.Random) -> Draw:
    n = rng.randint(5, 6)
    arcs = sorted(rng.sample([p for p in itertools.permutations(range(1, n + 1), 2)], rng.randint(n + 1, 2 * n)))
    out = {u: sorted(v for a, v in arcs if a == u) for u in range(1, n + 1)}
    lists = "; ".join(f"Ke({u}) = " + (", ".join(map(str, out[u])) if out[u] else "rỗng") for u in range(1, n + 1))
    w = rng.randint(1, n)
    ins = [u for u in range(1, n + 1) if w in out[u]]
    return Draw(params={"n": n, "arcs": [list(p) for p in arcs], "w": w},
                prompt_vi=(f"Một đồ thị có hướng {n} đỉnh được lưu bằng danh sách kề, Ke(u) là danh sách các đỉnh v có cung "
                           f"đi từ u đến v: {lists}. Có bao nhiêu cung đi vào đỉnh {w}?"),
                answer=str(len(ins)),
                solution_vi=[f"Danh sách kề chỉ ghi các cung đi ra. Cung đi vào {w} là những lần {w} xuất hiện trong "
                             "danh sách của một đỉnh khác.",
                             f"{w} có mặt trong danh sách của: {', '.join(map(str, ins)) or 'không đỉnh nào'}.",
                             f"Bán bậc vào của {w} là {len(ins)}."])
