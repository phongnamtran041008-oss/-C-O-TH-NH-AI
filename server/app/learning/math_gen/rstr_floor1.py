"""Thuật Toán và Tối Ưu: generators added by the curriculum review (see rsdstt_floor1.py for why).
Ids start with `tr_gx_`. Graphs are drawn from the rng and written out as edge lists in the
prompt; tools/math_verify_rasoat.py recomputes each answer another way (itertools permutations,
Floyd-Warshall, matrix powers, an explicit stack, sympy for the Hessian)."""
from __future__ import annotations

import itertools
import math
import random

from . import Draw, generator, nums


def _edges_text(edges: list[tuple[int, int]]) -> str:
    return ", ".join(f"{a}-{b}" for a, b in edges)


def _random_graph(rng: random.Random, n: int, extra: int, connected: bool = True) -> list[tuple[int, int]]:
    """A simple graph on 1..n: a random spanning tree (when connected) plus `extra` more edges."""
    edges: set[tuple[int, int]] = set()
    if connected:
        order = list(range(1, n + 1))
        rng.shuffle(order)
        for i in range(1, n):
            a, b = order[i], order[rng.randrange(i)]
            edges.add((min(a, b), max(a, b)))
    free = [(a, b) for a in range(1, n + 1) for b in range(a + 1, n + 1) if (a, b) not in edges]
    rng.shuffle(free)
    edges.update(free[:extra])
    return sorted(edges)


def _adjacency(n: int, edges) -> dict[int, list[int]]:
    adj: dict[int, list[int]] = {v: [] for v in range(1, n + 1)}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return {v: sorted(ns) for v, ns in adj.items()}


# ------------------------------------------------------------------ floor 3
@generator("tr_gx_hoan_vi_thu_may")
def hoan_vi_thu_may(rng: random.Random) -> Draw:
    """Tier 3: the place of a permutation in the lexicographic list of all permutations of 1..n."""
    n = rng.choice([4, 4, 5])
    perm = list(range(1, n + 1))
    rng.shuffle(perm)
    rank, steps = 0, []
    left = sorted(perm)
    for i, v in enumerate(perm):
        smaller = left.index(v)
        block = math.factorial(n - 1 - i)
        rank += smaller * block
        steps.append(f"Vị trí {i + 1}: trong các số còn lại {left} có {smaller} số nhỏ hơn {v}, mỗi số đứng đầu cho "
                     f"{n - 1 - i}! = {block} hoán vị đứng trước, cộng {smaller * block}.")
        left.remove(v)
    return Draw(
        params={"n": n, "perm": perm},
        prompt_vi=f"Liệt kê mọi hoán vị của 1, 2, ..., {n} theo thứ tự từ điển; hoán vị đầu tiên là "
                  f"{', '.join(map(str, range(1, n + 1)))} và là hoán vị thứ 1. Hoán vị ({', '.join(map(str, perm))}) "
                  f"đứng thứ mấy?",
        answer=str(rank + 1),
        solution_vi=["Đếm xem có bao nhiêu hoán vị đứng trước nó, theo từng vị trí."] + steps
                    + [f"Có {rank} hoán vị đứng trước, nên nó đứng thứ {rank} + 1 = {rank + 1}."])


# ------------------------------------------------------------------ floor 5
@generator("tr_gx_danh_sach_ke_dem")
def danh_sach_ke_dem(rng: random.Random) -> Draw:
    """Tier 4: read an adjacency list: number of edges, the largest degree, or the number of leaves."""
    n = rng.choice([6, 7, 8])
    edges = _random_graph(rng, n, rng.randint(1, 4), connected=rng.random() < 0.7)
    adj = _adjacency(n, edges)
    lines = "; ".join(f"Ke({v}) = {', '.join(map(str, ns)) if ns else 'rỗng'}" for v, ns in adj.items())
    ask = rng.choice(["edges", "maxdeg", "sum"])
    m = len(edges)
    degs = {v: len(ns) for v, ns in adj.items()}
    if ask == "edges":
        q, ans = "Đồ thị có bao nhiêu cạnh?", m
        sol = [f"Mỗi cạnh xuất hiện đúng hai lần trong danh sách kề (một lần ở mỗi đầu mút).",
               f"Tổng độ dài các danh sách = {' + '.join(map(str, degs.values()))} = {2 * m}.",
               f"Số cạnh = {2 * m}/2 = {m}."]
    elif ask == "maxdeg":
        top = max(degs.values())
        q, ans = "Bậc lớn nhất của một đỉnh là bao nhiêu?", top
        sol = ["Bậc của một đỉnh là độ dài danh sách kề của nó.",
               "Các bậc: " + ", ".join(f"deg({v}) = {d}" for v, d in degs.items()) + ".",
               f"Lớn nhất là {top}."]
    else:
        q, ans = "Nếu lưu bằng danh sách kề thì tổng số phần tử của tất cả các danh sách là bao nhiêu?", 2 * m
        sol = [f"Mỗi cạnh được ghi hai lần, nên tổng bằng 2 . (số cạnh) = 2 . {m} = {2 * m}.",
               "Cách kiểm: cộng các bậc " + " + ".join(map(str, degs.values())) + f" = {2 * m}."]
    return Draw(
        params={"n": n, "edges": [list(e) for e in edges], "ask": ask},
        prompt_vi=f"Đồ thị đơn vô hướng G có các đỉnh 1, 2, ..., {n} được lưu bằng danh sách kề: {lines}. {q}",
        answer=str(ans),
        solution_vi=sol)


@generator("tr_gx_thanh_phan_lien_thong")
def thanh_phan_lien_thong(rng: random.Random) -> Draw:
    """Tier 4: number of connected components, or edges to add to connect the graph."""
    n = rng.choice([7, 8, 9])
    # build several blocks of a forest so the count is not trivially 1
    k = rng.randint(2, 4)
    sizes = [1] * k
    for _ in range(n - k):
        sizes[rng.randrange(k)] += 1
    edges: list[tuple[int, int]] = []
    start = 1
    order = list(range(1, n + 1))
    rng.shuffle(order)
    for s in sizes:
        block = order[start - 1:start - 1 + s]
        start += s
        sub = _random_graph(rng, s, rng.randint(0, 1)) if s > 1 else []
        for a, b in sub:
            x, y = block[a - 1], block[b - 1]
            edges.append((min(x, y), max(x, y)))
    edges = sorted(set(edges))
    comps = sorted(sorted(order[sum(sizes[:i]):sum(sizes[:i + 1])]) for i in range(k))
    ask = rng.choice(["count", "add"])
    isolated = [c for c in comps if len(c) == 1]
    q = "Đồ thị có bao nhiêu thành phần liên thông?" if ask == "count" else \
        "Cần thêm ít nhất bao nhiêu cạnh để đồ thị trở thành liên thông?"
    ans = k if ask == "count" else k - 1
    shown = _edges_text(edges) if edges else "(không có cạnh nào)"
    return Draw(
        params={"n": n, "edges": [list(e) for e in edges], "ask": ask},
        prompt_vi=f"Đồ thị vô hướng G có các đỉnh 1, 2, ..., {n} và các cạnh {shown}. {q}",
        answer=str(ans),
        solution_vi=["Đi từ một đỉnh chưa thăm, gom mọi đỉnh tới được: mỗi lần như vậy là một thành phần liên thông.",
                     "Các thành phần: " + "; ".join("{" + ", ".join(map(str, c)) + "}" for c in comps) + f" ({k} thành phần"
                     + (f", trong đó {len(isolated)} đỉnh đứng một mình" if isolated else "") + ").",
                     f"Số thành phần liên thông là {k}." if ask == "count"
                     else f"Nối {k} thành phần thành một cần ít nhất {k} - 1 = {k - 1} cạnh."])


# ------------------------------------------------------------------ floor 6
def _bfs_dist(n: int, adj, src: int) -> dict[int, int]:
    dist, queue = {src: 0}, [src]
    for u in queue:
        for w in adj[u]:
            if w not in dist:
                dist[w] = dist[u] + 1
                queue.append(w)
    return dist


@generator("tr_gx_bfs_khoang_cach")
def bfs_khoang_cach(rng: random.Random) -> Draw:
    """Tier 4: the least number of edges between two vertices (a BFS), or how many vertices are
    exactly d edges from the source."""
    n = rng.choice([7, 8, 9])
    edges = _random_graph(rng, n, rng.randint(1, 3))
    adj = _adjacency(n, edges)
    src = rng.randint(1, n)
    dist = _bfs_dist(n, adj, src)
    layers: dict[int, list[int]] = {}
    for v, d in dist.items():
        layers.setdefault(d, []).append(v)
    ask = rng.choice(["to", "layer"])
    layer_text = "; ".join(f"cách {d} cạnh: {{{', '.join(map(str, sorted(vs)))}}}" for d, vs in sorted(layers.items()))
    target, d = 0, 0
    if ask == "to":
        far = max(dist.values())
        target = rng.choice(sorted(layers[rng.randint(max(1, far - 1), far)]))
        q, ans = f"Đường đi ít cạnh nhất từ đỉnh {src} tới đỉnh {target} có bao nhiêu cạnh?", dist[target]
    else:
        d = rng.randint(1, max(layers))
        q, ans = f"Có bao nhiêu đỉnh cách đỉnh {src} đúng {d} cạnh (theo đường đi ngắn nhất)?", len(layers[d])
    return Draw(
        params={"n": n, "edges": [list(e) for e in edges], "src": src, "ask": ask, "target": target, "d": d},
        prompt_vi=f"Đồ thị vô hướng G có các đỉnh 1, 2, ..., {n} và các cạnh {_edges_text(edges)}. {q}",
        answer=str(ans),
        solution_vi=[f"Chạy BFS từ đỉnh {src}: đỉnh nào được thăm ở lượt thứ d thì cách nguồn đúng d cạnh.",
                     f"Các lớp: cách 0 cạnh: {{{src}}}; {layer_text}.",
                     f"Đáp án: {ans}."])


@generator("tr_gx_dfs_thu_tu")
def dfs_thu_tu(rng: random.Random) -> Draw:
    """Tier 4: the order in which DFS from vertex 1 visits the vertices, smaller neighbour first."""
    n = rng.choice([6, 7, 8])
    edges = _random_graph(rng, n, rng.randint(1, 3))
    adj = _adjacency(n, edges)
    seen: list[int] = []

    def visit(u: int):
        seen.append(u)
        for w in adj[u]:
            if w not in seen:
                visit(w)
    visit(1)
    return Draw(
        params={"n": n, "edges": [list(e) for e in edges]},
        prompt_vi=f"Đồ thị vô hướng G có các đỉnh 1, 2, ..., {n} và các cạnh {_edges_text(edges)}. Chạy DFS từ đỉnh 1, "
                  f"mỗi lần chọn đỉnh kề chưa thăm có số nhỏ nhất. Nhập thứ tự thăm các đỉnh, cách nhau bằng dấu phẩy.",
        answer=nums(seen),
        solution_vi=["DFS đi sâu nhất có thể rồi mới quay lui; khi có nhiều lựa chọn thì lấy đỉnh nhỏ nhất.",
                     "Kề của từng đỉnh: " + "; ".join(f"{v}: {', '.join(map(str, ns))}" for v, ns in adj.items()) + ".",
                     f"Thứ tự thăm: {', '.join(map(str, seen))}."],
        unordered=False)


# ------------------------------------------------------------------ floors 7-8
@generator("tr_gx_cay_dem_la")
def cay_dem_la(rng: random.Random) -> Draw:
    """Tier 5: the degree sum of a tree is 2(n - 1), so leaves can be counted; or a forest's edges."""
    if rng.random() < 0.7:
        a, b, c = rng.randint(1, 5), rng.randint(0, 3), rng.randint(0, 4)    # vertices of degree 3, 4, 2
        n = 2 * a + 3 * b + c + 2                    # from 3a + 4b + 2c + L = 2(n - 1) and n = a + b + c + L
        leaves = n - a - b - c
        return Draw(
            params={"kind": "la", "n": n, "a": a, "b": b, "c": c},
            prompt_vi=f"Một cây có {n} đỉnh. Trong đó có {a} đỉnh bậc 3, {b} đỉnh bậc 4, {c} đỉnh bậc 2, còn lại đều "
                      f"là lá (bậc 1). Cây có bao nhiêu lá?",
            answer=str(leaves),
            solution_vi=[f"Tổng bậc của cây có {n} đỉnh là 2 . ({n} - 1) = {2 * (n - 1)} (cây có {n} - 1 cạnh).",
                         f"Gọi L là số lá: 3 . {a} + 4 . {b} + 2 . {c} + L = {2 * (n - 1)}, tức "
                         f"{3 * a + 4 * b + 2 * c} + L = {2 * (n - 1)}.",
                         f"Suy ra L = {leaves}. (Kiểm: {a} + {b} + {c} + {leaves} = {n} đỉnh.)"])
    n, k = rng.randint(10, 30), rng.randint(2, 5)
    return Draw(
        params={"kind": "rung", "n": n, "k": k},
        prompt_vi=f"Một rừng gồm {k} cây rời nhau, tổng cộng {n} đỉnh (mỗi cây là một đồ thị liên thông không có chu "
                  f"trình). Rừng có bao nhiêu cạnh?",
        answer=str(n - k),
        solution_vi=["Một cây có m đỉnh có m - 1 cạnh.", f"Cộng {k} cây: số cạnh = (tổng số đỉnh) - (số cây) = {n} - {k} = {n - k}."])


@generator("tr_gx_ham_loi_hesse")
def ham_loi_hesse(rng: random.Random) -> Draw:
    """Tier 5, true/false: is f(x, y) = a x^2 + b x y + c y^2 convex? (Hessian [[2a, b], [b, 2c]])"""
    a, c = rng.randint(1, 5), rng.choice([-2, -1, 1, 2, 3, 4, 5])
    edge = 2 * math.isqrt(max(a * c, 0)) if a * c > 0 else 0
    b = rng.choice([0, 1, 2, 3, 4, 5, 6, edge, edge + 1, max(edge - 1, 0), -edge, -edge - 1])
    det = 4 * a * c - b * b
    convex = a > 0 and c > 0 and det >= 0
    f_text = f"{a}x^2 {'+' if b >= 0 else '-'} {abs(b)}xy {'+' if c >= 0 else '-'} {abs(c)}y^2"
    if convex:
        why = [f"Ma trận Hesse của f là H = [[{2 * a}, {b}], [{b}, {2 * c}]] (đạo hàm riêng cấp hai).",
               f"{2 * a} > 0 và det H = {2 * a} . {2 * c} - {b}^2 = {det} >= 0, nên H nửa xác định dương.",
               "Hesse nửa xác định dương ở mọi điểm: f là hàm lồi."]
    else:
        why = [f"Ma trận Hesse của f là H = [[{2 * a}, {b}], [{b}, {2 * c}]] (đạo hàm riêng cấp hai).",
               (f"det H = {2 * a} . {2 * c} - {b}^2 = {det} < 0, nên H có một trị riêng âm."
                if det < 0 else f"Phần tử đường chéo {2 * c} < 0 nên H có trị riêng âm."),
               "Hesse không nửa xác định dương: f không là hàm lồi (mất mát kiểu này có điểm yên ngựa hoặc cực đại)."]
    return Draw(
        params={"a": a, "b": b, "c": c},
        prompt_vi=f"Hàm mất mát f(x, y) = {f_text} là một hàm lồi trên R^2.",
        answer=convex,
        solution_vi=why)
