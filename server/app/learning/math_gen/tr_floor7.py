"""Tối Ưu và Toán Rời Rạc, floor 7 (cây, liệt kê cây, bài toán tối ưu trên đồ thị):
generators. Ids start with `tr_g7_`.

A graph is text that cannot be misread: its vertices 1..n and its edge list, each edge with
its weight in brackets ("1-2 (4)"); a network lists its arcs with their capacities
("1->2 (5)"). Weights are distinct wherever an algorithm's tie-break would matter, so
Kruskal, Prim and Dijkstra each have one run and the minimum spanning tree is unique.

The generators solve their instances the way the floor teaches (the handshake count, Kruskal
with union-find, Prim with a growing tree, Dijkstra with fixed labels, augmenting paths found
by BFS); tools/math_verify_tr_t7.py recomputes every answer another way (sympy equations,
the rank of the incidence matrix, the matrix-tree theorem, every spanning tree, every simple
path, Floyd-Warshall, every s-t cut)."""
from __future__ import annotations

import itertools
import random

from . import Draw, generator, nums
from .tr_floor5 import components, connected_graph, clustered_graph, edge_text, norm


# ------------------------------------------------------------------ weighted graphs as text
def wedge_text(wedges) -> str:
    return ", ".join(f"{u}-{v} ({w})" for u, v, w in wedges)


def wgraph_text(n: int, wedges) -> str:
    return f"các đỉnh 1, 2, ..., {n}; các cạnh (trọng số trong ngoặc): {wedge_text(wedges)}"


def weighted_graph(rng: random.Random, n: int, extra: int, top: int = 20) -> list[list[int]]:
    """A connected graph with distinct weights 1..top, as sorted [u, v, w] (the params form)."""
    edges = connected_graph(rng, n, extra)
    weights = rng.sample(range(1, top + 1), len(edges))
    return [[u, v, w] for (u, v), w in zip(edges, weights)]


class _Forest:
    def __init__(self, n: int):
        self.parent = list(range(n + 1))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def join(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[ra] = rb
        return True


def kruskal(n: int, wedges) -> tuple[list[tuple[int, int, int]], list[str]]:
    """The tree edges in the order they are taken, and one line per edge looked at."""
    forest, tree, lines = _Forest(n), [], []
    for u, v, w in sorted(wedges, key=lambda e: e[2]):
        if len(tree) == n - 1:
            break
        if forest.join(u, v):
            tree.append((u, v, w))
            lines.append(f"{u}-{v} ({w}): nhận")
        else:
            lines.append(f"{u}-{v} ({w}): bỏ, vì {u} và {v} đã nối với nhau, thêm vào sẽ tạo chu trình")
    return tree, lines


def prim(n: int, wedges, start: int = 1) -> list[tuple[int, int, int]]:
    """Prim's tree edges (tree vertex, new vertex, weight) in the order they are added."""
    inside, added = {start}, []
    while len(inside) < n:
        u, v, w = min(((a, b, w) if a in inside else (b, a, w) for a, b, w in wedges
                       if (a in inside) != (b in inside)), key=lambda e: e[2])
        inside.add(v)
        added.append((u, v, w))
    return added


def dijkstra(n: int, wedges, s: int) -> tuple[dict[int, int], dict[int, int], list[int]]:
    """Distances, predecessors and the order in which the labels become fixed."""
    adj = {v: [] for v in range(1, n + 1)}
    for u, v, w in wedges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist, prev, fixed = {s: 0}, {}, []
    while len(fixed) < len(dist):
        u = min((v for v in dist if v not in fixed), key=lambda v: (dist[v], v))
        fixed.append(u)
        for v, w in adj[u]:
            if v not in fixed and (v not in dist or dist[u] + w < dist[v]):
                dist[v], prev[v] = dist[u] + w, u
    return dist, prev, fixed


def path_to(prev: dict[int, int], s: int, t: int) -> list[int]:
    path = [t]
    while path[-1] != s:
        path.append(prev[path[-1]])
    return path[::-1]


# ------------------------------------------------------------------ cây
@generator("tr_g7_dem_la")
def dem_la(rng: random.Random) -> Draw:
    kind = rng.choice(["la", "dinh", "rung"])
    if kind in ("la", "dinh"):
        c2, c3, c4 = rng.randint(0, 4), rng.randint(0, 4), rng.randint(1, 3)
        leaves = 2 + c3 + 2 * c4
        n = c2 + c3 + c4 + leaves
        params = {"kind": kind, "c2": c2, "c3": c3, "c4": c4}
        given = f"{c4} đỉnh bậc 4, {c3} đỉnh bậc 3, {c2} đỉnh bậc 2, các đỉnh còn lại đều là lá (bậc 1)"
        ask = "Cây có bao nhiêu lá?" if kind == "la" else "Cây có tất cả bao nhiêu đỉnh?"
        answer = leaves if kind == "la" else n
        steps = [f"Gọi số lá là L. Cây có {c2 + c3 + c4} + L đỉnh, nên có {c2 + c3 + c4} + L - 1 cạnh.",
                 f"Tổng các bậc: 4 . {c4} + 3 . {c3} + 2 . {c2} + L = {4 * c4 + 3 * c3 + 2 * c2} + L.",
                 f"Định lý bắt tay: {4 * c4 + 3 * c3 + 2 * c2} + L = 2({c2 + c3 + c4} + L - 1), "
                 f"suy ra L = {leaves}.",
                 f"Cây có {leaves} lá và {n} đỉnh; đáp số {answer}."]
        prompt = f"Một cây có {given}. {ask}"
    else:
        n = rng.randint(12, 40)
        k = rng.randint(2, 7)
        params = {"kind": kind, "n": n, "k": k}
        answer = n - k
        prompt = (f"Một rừng (đồ thị không có chu trình) có {n} đỉnh và đúng {k} thành phần liên thông. "
                  "Rừng có bao nhiêu cạnh?")
        steps = ["Mỗi thành phần liên thông của rừng là một cây; cây có n_i đỉnh thì có n_i - 1 cạnh.",
                 f"Cộng lại trên {k} cây: (n_1 + ... + n_{k}) - {k} = {n} - {k}.",
                 f"Rừng có {answer} cạnh."]
    return Draw(params=params, prompt_vi=prompt, answer=str(answer), solution_vi=steps)


# ------------------------------------------------------------------ cây khung
@generator("tr_g7_xoa_canh")
def xoa_canh(rng: random.Random) -> Draw:
    n = rng.randint(7, 9)
    k = rng.randint(1, 3)
    edges = clustered_graph(rng, n, k)
    inside = [list(p) for c in components(n, edges) for p in itertools.combinations(c, 2) if list(p) not in edges]
    edges = norm(edges + rng.sample(inside, min(len(inside), rng.randint(1, 3))))
    comps = components(n, edges)
    k = len(comps)
    m = len(edges)
    answer = m - n + k
    shown = "; ".join("{" + ", ".join(map(str, c)) + "}" for c in comps)
    return Draw(params={"n": n, "edges": edges},
                prompt_vi=(f"Đồ thị G có các đỉnh 1, 2, ..., {n}; các cạnh: {edge_text(edges)}. Cần xóa ít nhất "
                           "bao nhiêu cạnh để G không còn chu trình mà số thành phần liên thông không đổi (tức là "
                           "còn lại một rừng khung của G)?"),
                answer=str(answer),
                solution_vi=[f"G có {m} cạnh. Các thành phần liên thông: {shown}, tức k = {k}.",
                             "Rừng khung giữ mỗi thành phần n_i đỉnh bằng một cây n_i - 1 cạnh, nên có "
                             f"{n} - {k} = {n - k} cạnh.",
                             f"Phải xóa {m} - {n - k} = {answer} cạnh (số này gọi là số chu trình độc lập của G)."])


def _spanning_trees(n: int, edges) -> list[tuple]:
    out = []
    for sub in itertools.combinations([tuple(e) for e in edges], n - 1):
        forest = _Forest(n)
        if all(forest.join(u, v) for u, v in sub):
            out.append(sub)
    return out


@generator("tr_g7_dem_cay_khung")
def dem_cay_khung(rng: random.Random) -> Draw:
    n = rng.choice([4, 5, 5])
    extra = 2 if n == 5 else rng.randint(2, 3)
    edges = connected_graph(rng, n, extra)
    m = len(edges)
    drop = m - n + 1
    trees = _spanning_trees(n, edges)
    total = len(list(itertools.combinations(range(m), n - 1)))
    return Draw(params={"n": n, "edges": edges},
                prompt_vi=(f"Đồ thị G có các đỉnh 1, 2, ..., {n}; các cạnh: {edge_text(edges)}. "
                           "G có bao nhiêu cây khung khác nhau (hai cây khác nhau khi tập cạnh khác nhau)?"),
                answer=str(len(trees)),
                solution_vi=[f"Một cây khung có {n - 1} cạnh, tức là giữ {n - 1} trong {m} cạnh và bỏ {drop} cạnh.",
                             f"Có C_{m}^{drop} = {total} cách bỏ {drop} cạnh. Cách bỏ nào để lại một chu trình (khi đó "
                             "phần còn lại cũng không liên thông) thì không cho cây.",
                             f"Kiểm tra từng cách: {total - len(trees)} cách để lại chu trình, còn {len(trees)} cách "
                             "để lại một cây.",
                             f"G có {len(trees)} cây khung (kiểm tra lại bằng định lý Kirchhoff: định thức của ma trận "
                             "Laplace bỏ một hàng một cột)."])


# ------------------------------------------------------------------ cây khung nhỏ nhất
@generator("tr_g7_kruskal_tong")
def kruskal_tong(rng: random.Random) -> Draw:
    n = 6
    wedges = weighted_graph(rng, n, rng.randint(3, 4))
    tree, lines = kruskal(n, wedges)
    total = sum(w for _, _, w in tree)
    return Draw(params={"n": n, "wedges": wedges},
                prompt_vi=(f"Đồ thị G có {wgraph_text(n, wedges)}. Cây khung nhỏ nhất của G có tổng trọng số "
                           "bằng bao nhiêu?"),
                answer=str(total),
                solution_vi=["Thuật toán Kruskal: xét các cạnh theo trọng số tăng dần, nhận cạnh nếu nó không tạo "
                             f"chu trình với các cạnh đã nhận, dừng khi đủ {n - 1} cạnh."]
                            + ["; ".join(lines) + "."]
                            + [f"Cây khung nhỏ nhất: {', '.join(f'{u}-{v}' for u, v, _ in tree)}; tổng trọng số "
                               f"{' + '.join(str(w) for _, _, w in tree)} = {total}."])


@generator("tr_g7_kruskal_cuoi")
def kruskal_cuoi(rng: random.Random) -> Draw:
    n = 7
    wedges = weighted_graph(rng, n, rng.randint(3, 5), top=25)
    tree, lines = kruskal(n, wedges)
    total = sum(w for _, _, w in tree)
    rejected = sum(1 for line in lines if "bỏ" in line)
    last = tree[-1]
    return Draw(params={"n": n, "wedges": wedges},
                prompt_vi=(f"Đồ thị G có {wgraph_text(n, wedges)}. Chạy thuật toán Kruskal trên G. Nhập hai số: "
                           "tổng trọng số của cây khung nhỏ nhất, rồi trọng số của cạnh được nhận cuối cùng."),
                answer=nums([total, last[2]]),
                solution_vi=["Xét các cạnh theo trọng số tăng dần, nhận cạnh nếu nó không tạo chu trình, dừng khi đủ "
                             f"{n - 1} cạnh."]
                            + ["; ".join(lines) + "."]
                            + [f"Đã bỏ {rejected} cạnh. Cây: {', '.join(f'{u}-{v}' for u, v, _ in tree)}; tổng "
                               f"{' + '.join(str(w) for _, _, w in tree)} = {total}.",
                               f"Cạnh nhận cuối cùng là {last[0]}-{last[1]} ({last[2]}), cũng là cạnh nặng nhất của "
                               f"cây. Đáp số: {total}, {last[2]}."])


@generator("tr_g7_prim")
def prim_thu_tu(rng: random.Random) -> Draw:
    n = 6
    wedges = weighted_graph(rng, n, rng.randint(3, 5))
    start = rng.randint(1, n)
    added = prim(n, wedges, start)
    order = [start] + [v for _, v, _ in added]
    steps = [f"Bắt đầu với cây chỉ có đỉnh {start}. Mỗi bước thêm cạnh nhẹ nhất nối một đỉnh trong cây với một "
             "đỉnh ngoài cây."]
    steps += ["; ".join(f"thêm {v} qua cạnh {u}-{v} ({w})" for u, v, w in added) + "."]
    steps += [f"Thứ tự các đỉnh được thêm: {nums(order)}; tổng trọng số {sum(w for _, _, w in added)}."]
    return Draw(params={"n": n, "wedges": wedges, "start": start},
                prompt_vi=(f"Đồ thị G có {wgraph_text(n, wedges)}. Chạy thuật toán Prim từ đỉnh {start}. Nhập các "
                           f"đỉnh theo thứ tự chúng được đưa vào cây, bắt đầu bằng {start}."),
                answer=nums(order), solution_vi=steps)


# ------------------------------------------------------------------ đường đi ngắn nhất
@generator("tr_g7_dijkstra")
def dijkstra_kc(rng: random.Random) -> Draw:
    n = 6
    wedges = weighted_graph(rng, n, rng.randint(3, 5), top=15)
    s = 1
    dist, prev, fixed = dijkstra(n, wedges, s)
    t = rng.choice([v for v in range(2, n + 1) if len(path_to(prev, s, v)) >= 3] or list(range(2, n + 1)))
    path = path_to(prev, s, t)
    return Draw(params={"n": n, "wedges": wedges, "t": t},
                prompt_vi=(f"Đồ thị vô hướng G có {wgraph_text(n, wedges)}. Độ dài đường đi ngắn nhất từ đỉnh 1 "
                           f"đến đỉnh {t} bằng bao nhiêu?"),
                answer=str(dist[t]),
                solution_vi=["Thuật toán Dijkstra từ đỉnh 1: mỗi bước cố định đỉnh chưa cố định có nhãn nhỏ nhất, rồi "
                             "giảm nhãn các đỉnh kề nó.",
                             "Thứ tự cố định và nhãn cuối: " + ", ".join(f"{v} ({dist[v]})" for v in fixed) + ".",
                             f"Đường đi ngắn nhất: {' - '.join(map(str, path))}, độ dài {dist[t]}."])


@generator("tr_g7_dijkstra_moi")
def dijkstra_moi(rng: random.Random) -> Draw:
    n = 6
    wedges = weighted_graph(rng, n, rng.randint(3, 5), top=15)
    s = rng.randint(1, n)
    dist, prev, fixed = dijkstra(n, wedges, s)
    others = [v for v in range(1, n + 1) if v != s]
    return Draw(params={"n": n, "wedges": wedges, "s": s},
                prompt_vi=(f"Đồ thị vô hướng G có {wgraph_text(n, wedges)}. Tìm khoảng cách (độ dài đường đi ngắn "
                           f"nhất) từ đỉnh {s} đến các đỉnh {', '.join(map(str, others))}; nhập theo đúng thứ tự đó."),
                answer=nums([dist[v] for v in others]),
                solution_vi=[f"Chạy Dijkstra từ {s}; trọng số đều dương nên nhãn của một đỉnh đã cố định là khoảng "
                             "cách đúng.",
                             "Thứ tự cố định và nhãn: " + ", ".join(f"{v} ({dist[v]})" for v in fixed) + ".",
                             "Đường đi: " + "; ".join(f"đến {v}: {' - '.join(map(str, path_to(prev, s, v)))}"
                                                      for v in others) + ".",
                             f"Đáp số: {nums([dist[v] for v in others])}."])


# ------------------------------------------------------------------ luồng cực đại
def network(rng: random.Random) -> tuple[int, list[list[int]]]:
    """Vertices 1..n, source 1, sink n; arcs u->v with u < v and capacities 1..9, every vertex
    on some path from 1 to n."""
    n = rng.randint(5, 6)
    arcs = set()
    for v in range(2, n):
        arcs.add((rng.randint(1, v - 1), v))
        arcs.add((v, rng.randint(v + 1, n)))
    others = [(u, v) for u, v in itertools.combinations(range(1, n + 1), 2) if (u, v) not in arcs and (u, v) != (1, n)]
    arcs |= set(rng.sample(others, min(len(others), rng.randint(1, 3))))
    return n, [[u, v, rng.randint(1, 9)] for u, v in sorted(arcs)]


def net_text(n: int, arcs) -> str:
    return (f"các đỉnh 1, 2, ..., {n}, đỉnh phát 1, đỉnh thu {n}; các cung (khả năng thông qua trong ngoặc): "
            + ", ".join(f"{u}->{v} ({c})" for u, v, c in arcs))


def max_flow(n: int, arcs) -> tuple[int, list[tuple[list[int], int]], list[int]]:
    """Edmonds-Karp: the value, the augmenting paths with their amounts, and the source side
    of a minimum cut (what the last search reaches)."""
    cap: dict[tuple[int, int], int] = {}
    for u, v, c in arcs:
        cap[(u, v)] = cap.get((u, v), 0) + c
        cap.setdefault((v, u), 0)
    nb = {v: sorted({b for a, b in cap if a == v}) for v in range(1, n + 1)}
    value, found = 0, []
    while True:
        prev, queue = {1: None}, [1]
        while queue and n not in prev:
            u = queue.pop(0)
            for v in nb[u]:
                if v not in prev and cap[(u, v)] > 0:
                    prev[v] = u
                    queue.append(v)
        if n not in prev:
            return value, found, sorted(prev)
        path = [n]
        while path[-1] != 1:
            path.append(prev[path[-1]])
        path.reverse()
        amount = min(cap[(a, b)] for a, b in zip(path, path[1:]))
        for a, b in zip(path, path[1:]):
            cap[(a, b)] -= amount
            cap[(b, a)] += amount
        value += amount
        found.append((path, amount))


def cut_capacity(arcs, side) -> int:
    return sum(c for u, v, c in arcs if u in side and v not in side)


def _flow_lines(n: int, arcs) -> tuple[int, list[str], list[int]]:
    value, found, side = max_flow(n, arcs)
    lines = ["Tìm đường tăng luồng (theo BFS trên mạng thặng dư) và tăng hết mức cho tới khi không còn đường:",
             "; ".join(f"{'->'.join(map(str, p))} thêm {a}" for p, a in found) + f"; tổng {value}.",
             f"Các đỉnh còn tới được từ 1 trong mạng thặng dư: S = {{{', '.join(map(str, side))}}}. Lát cắt (S, T) "
             f"có khả năng thông qua {cut_capacity(arcs, side)} = {value}, nên luồng đã là cực đại."]
    return value, lines, side


@generator("tr_g7_luong_max")
def luong_max(rng: random.Random) -> Draw:
    n, arcs = network(rng)
    value, lines, _ = _flow_lines(n, arcs)
    return Draw(params={"n": n, "arcs": arcs},
                prompt_vi=f"Mạng G có {net_text(n, arcs)}. Giá trị luồng cực đại từ 1 đến {n} bằng bao nhiêu?",
                answer=str(value), solution_vi=lines + [f"Đáp số: {value}."])


@generator("tr_g7_lat_cat")
def lat_cat(rng: random.Random) -> Draw:
    n, arcs = network(rng)
    value, lines, side = _flow_lines(n, arcs)
    inner = list(range(2, n))
    cuts = []
    for r in range(len(inner) + 1):
        for extra in itertools.combinations(inner, r):
            s_side = [1, *extra]
            cuts.append((s_side, cut_capacity(arcs, s_side)))
    wrong = sorted({c for _, c in cuts if c != value})
    if wrong and rng.random() < 0.5:
        s_side, claim = rng.choice([sc for sc in cuts if sc[1] != value])
        ok = False
    else:
        s_side, claim = rng.choice([sc for sc in cuts if sc[1] == value])
        ok = True
    shown = "{" + ", ".join(map(str, s_side)) + "}"
    verdict = ("Lát cắt này có khả năng thông qua bằng giá trị luồng cực đại: nó là lát cắt hẹp nhất. "
               "Khẳng định đúng." if ok else
               f"Giá trị luồng cực đại là {value}, khác {claim}: lát cắt này không hẹp nhất. Khẳng định sai.")
    return Draw(params={"n": n, "arcs": arcs, "side": s_side},
                prompt_vi=(f"Mạng G có {net_text(n, arcs)}. Xét lát cắt S = {shown}, T là các đỉnh còn lại. Khẳng "
                           "định: giá trị luồng cực đại từ 1 đến "
                           f"{n} bằng khả năng thông qua của lát cắt (S, T)."),
                answer=ok,
                solution_vi=[f"Khả năng thông qua của (S, T) là tổng khả năng các cung đi từ S sang T: {claim}."]
                            + lines + [verdict])
