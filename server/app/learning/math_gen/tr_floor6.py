"""Tối Ưu và Toán Rời Rạc, floor 6 (tìm kiếm trên đồ thị, đồ thị Euler và Hamilton):
generators. Ids start with `tr_g6_`.

Traversals fix their tie-break in the prompt (adjacent vertices are taken in increasing
order), so a BFS or DFS order is unique. The generators run BFS with a queue and DFS by
recursion, and build Euler and Hamilton instances so that they have (or lack) the property
by construction; tools/math_verify_tr_t4.py recomputes BFS levels from powers of the
adjacency matrix, DFS with an explicit stack, reachability from (I + A)^(n-1), Euler's
condition from the degrees, and Hamilton cycles by trying every permutation."""
from __future__ import annotations

import itertools
import math
import random

from . import Draw, generator, nums
from .tr_floor5 import components, connected_graph, graph_text, neighbours, norm, clustered_graph, degrees

_TIE = "thăm các đỉnh kề theo thứ tự số tăng dần"


def bfs(n: int, edges, s: int) -> tuple[list[int], dict[int, int], dict[int, int]]:
    nb = neighbours(n, edges)
    order, dist, prev = [s], {s: 0}, {}
    queue = [s]
    while queue:
        u = queue.pop(0)
        for v in nb[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                prev[v] = u
                order.append(v)
                queue.append(v)
    return order, dist, prev


def dfs(n: int, edges, s: int) -> list[int]:
    nb = neighbours(n, edges)
    order: list[int] = []

    def visit(u):
        order.append(u)
        for v in nb[u]:
            if v not in order:
                visit(v)

    visit(s)
    return order


# ------------------------------------------------------------------ BFS
@generator("tr_g6_bfs_thu_tu")
def bfs_thu_tu(rng: random.Random) -> Draw:
    n = rng.randint(6, 8)
    edges = connected_graph(rng, n, rng.randint(1, 4))
    s = rng.randint(1, n)
    order, dist, _ = bfs(n, edges, s)
    levels = {}
    for v in order:
        levels.setdefault(dist[v], []).append(v)
    shown = "; ".join(f"khoảng cách {d}: {', '.join(map(str, vs))}" for d, vs in sorted(levels.items()))
    return Draw(params={"n": n, "edges": edges, "s": s},
                prompt_vi=(f"Đồ thị G có {graph_text(n, edges)}. Chạy BFS từ đỉnh {s}, {_TIE}. Nhập thứ tự thăm các đỉnh, "
                           "cách nhau bằng dấu phẩy."),
                answer=nums(order),
                solution_vi=[f"Đưa {s} vào hàng đợi. Mỗi lần lấy đỉnh đầu hàng đợi ra, đưa các đỉnh kề chưa thăm của nó "
                             "vào cuối hàng đợi theo thứ tự tăng dần.",
                             f"Các đỉnh được thăm theo từng lớp: {shown}.",
                             f"Thứ tự thăm: {', '.join(map(str, order))}."])


@generator("tr_g6_bfs_khoang_cach")
def bfs_khoang_cach(rng: random.Random) -> Draw:
    n = rng.randint(6, 8)
    edges = connected_graph(rng, n, rng.randint(0, 3))
    s = rng.randint(1, n)
    order, dist, prev = bfs(n, edges, s)
    t = max(order[1:], key=lambda v: (dist[v], rng.random()))
    path = [t]
    while path[-1] != s:
        path.append(prev[path[-1]])
    path.reverse()
    return Draw(params={"n": n, "edges": edges, "s": s, "t": t},
                prompt_vi=(f"Đồ thị G có {graph_text(n, edges)}. Đường đi từ {s} đến {t} có ít cạnh nhất là bao nhiêu cạnh?"),
                answer=str(dist[t]),
                solution_vi=[f"Chạy BFS từ {s}: BFS thăm các đỉnh theo khoảng cách tăng dần, và khoảng cách của một đỉnh "
                             "bằng khoảng cách của đỉnh đã đưa nó vào hàng đợi cộng 1.",
                             f"Lần ngược theo đỉnh đứng trước trên cây BFS: {' - '.join(map(str, path))}.",
                             f"Đường đi ngắn nhất có {dist[t]} cạnh."])


# ------------------------------------------------------------------ DFS
@generator("tr_g6_dfs_thu_tu")
def dfs_thu_tu(rng: random.Random) -> Draw:
    n = rng.randint(6, 8)
    edges = connected_graph(rng, n, rng.randint(1, 4))
    s = rng.randint(1, n)
    order = dfs(n, edges, s)
    nb = neighbours(n, edges)
    lists = "; ".join(f"{v}: {', '.join(map(str, nb[v]))}" for v in range(1, n + 1))
    return Draw(params={"n": n, "edges": edges, "s": s},
                prompt_vi=(f"Đồ thị G có {graph_text(n, edges)}. Chạy DFS (đệ quy) từ đỉnh {s}, {_TIE}. Nhập thứ tự thăm "
                           "các đỉnh, cách nhau bằng dấu phẩy."),
                answer=nums(order),
                solution_vi=[f"Danh sách kề (đã xếp tăng dần): {lists}.",
                             "DFS(u): thăm u, rồi lần lượt với mỗi đỉnh kề v chưa thăm gọi DFS(v). Khi u hết đỉnh kề chưa "
                             "thăm thì quay lui về đỉnh đã gọi nó, không nhảy sang đỉnh không kề.",
                             f"Thứ tự thăm: {', '.join(map(str, order))}."])


# ------------------------------------------------------------------ ứng dụng
@generator("tr_g6_noi_duoc")
def noi_duoc(rng: random.Random) -> Draw:
    n = rng.randint(7, 8)
    edges = clustered_graph(rng, n, rng.randint(2, 3))
    u, v = sorted(rng.sample(range(1, n + 1), 2))
    order, _, _ = bfs(n, edges, u)
    ok = v in order
    return Draw(params={"n": n, "edges": edges, "u": u, "v": v},
                prompt_vi=f"Đồ thị G có {graph_text(n, edges)}. Khẳng định: có đường đi từ {u} đến {v}.",
                answer=ok,
                solution_vi=[f"Chạy BFS (hoặc DFS) từ {u}; có đường đi đến {v} khi và chỉ khi {v} được thăm.",
                             f"Các đỉnh được thăm: {', '.join(map(str, sorted(order)))}.",
                             f"{v} {'có' if ok else 'không có'} trong đó: khẳng định {'đúng' if ok else 'sai'}."])


@generator("tr_g6_thanh_phan")
def thanh_phan(rng: random.Random) -> Draw:
    n = rng.randint(7, 9)
    edges = clustered_graph(rng, n, rng.randint(1, 4))
    comps = components(n, edges)
    kind = rng.choice(["count", "size"])
    shown = "; ".join("{" + ", ".join(map(str, c)) + "}" for c in comps)
    if kind == "count":
        params = {"n": n, "edges": edges, "kind": kind}
        prompt = (f"Đồ thị G có {graph_text(n, edges)}. Chương trình duyệt v = 1, 2, ..., {n}; gặp đỉnh v chưa thăm thì "
                  "gọi DFS(v). DFS được gọi từ vòng duyệt này bao nhiêu lần?")
        answer = len(comps)
        last = f"Mỗi lần gọi thăm trọn một thành phần liên thông, nên số lần gọi là số thành phần: {answer}."
    else:
        w = rng.randint(1, n)
        params = {"n": n, "edges": edges, "kind": kind, "w": w}
        prompt = (f"Đồ thị G có {graph_text(n, edges)}. Chạy BFS từ đỉnh {w}. BFS thăm tất cả bao nhiêu đỉnh, kể cả {w}?")
        answer = len(next(c for c in comps if w in c))
        last = f"BFS từ {w} thăm đúng thành phần liên thông chứa {w}, gồm {answer} đỉnh."
    return Draw(params=params, prompt_vi=prompt, answer=str(answer),
                solution_vi=["Một lần duyệt từ một đỉnh thăm đúng những đỉnh nối được với nó.",
                             f"Các thành phần liên thông của G: {shown}.", last])


# ------------------------------------------------------------------ Euler
def _euler_base(rng: random.Random, n: int) -> list[tuple[int, int]]:
    """A Hamilton cycle through all n vertices plus a second, edge-disjoint cycle: connected
    and every degree even, so it has an Euler circuit by construction."""
    while True:
        p = list(range(1, n + 1))
        rng.shuffle(p)
        edges = {tuple(sorted((p[i], p[(i + 1) % n]))) for i in range(n)}
        q = rng.sample(range(1, n + 1), rng.choice([3, 4]))
        second = {tuple(sorted((q[i], q[(i + 1) % len(q)]))) for i in range(len(q))}
        if not edges & second:
            return sorted(edges | second)


@generator("tr_g6_euler")
def euler(rng: random.Random) -> Draw:
    n = rng.randint(6, 7)
    edges = _euler_base(rng, n)
    change = rng.choice(["none", "none", "drop", "add"])
    if change == "drop":
        edges.remove(rng.choice(edges))
    elif change == "add":
        free = [p for p in itertools.combinations(range(1, n + 1), 2) if p not in edges]
        edges.append(rng.choice(free))
    edges = norm(edges)
    deg = degrees(n, edges)
    odd = [v for v in range(1, n + 1) if deg[v - 1] % 2]
    ok = change == "none"
    return Draw(params={"n": n, "edges": edges},
                prompt_vi=f"Đồ thị G có {graph_text(n, edges)}. Khẳng định: G có chu trình Euler.",
                answer=ok,
                solution_vi=["Đồ thị liên thông có chu trình Euler khi và chỉ khi mọi đỉnh có bậc chẵn. G liên thông "
                             "(mọi đỉnh nối được với đỉnh 1).",
                             f"Bậc của các đỉnh 1, ..., {n}: {', '.join(map(str, deg))}.",
                             "Mọi bậc đều chẵn: khẳng định đúng." if ok else
                             f"Các đỉnh {', '.join(map(str, odd))} có bậc lẻ: không có chu trình Euler, khẳng định sai."])


@generator("tr_g6_euler_duong")
def euler_duong(rng: random.Random) -> Draw:
    n = rng.randint(6, 7)
    edges = _euler_base(rng, n)
    if rng.random() < 0.5:
        edges.remove(rng.choice(edges))
    else:
        free = [p for p in itertools.combinations(range(1, n + 1), 2) if p not in edges]
        edges.append(rng.choice(free))
    edges = norm(edges)
    deg = degrees(n, edges)
    odd = [v for v in range(1, n + 1) if deg[v - 1] % 2]
    return Draw(params={"n": n, "edges": edges},
                prompt_vi=(f"Đồ thị liên thông G có {graph_text(n, edges)}. G có đường đi Euler nhưng không có chu trình "
                           "Euler. Mọi đường đi Euler của G phải bắt đầu ở một trong hai đỉnh nào? Nhập hai đỉnh đó."),
                answer=nums(odd), unordered=True,
                solution_vi=[f"Bậc của các đỉnh 1, ..., {n}: {', '.join(map(str, deg))}.",
                             f"Có đúng hai đỉnh bậc lẻ: {odd[0]} và {odd[1]}.",
                             "Trên một đường đi Euler, mỗi lần đi qua một đỉnh ở giữa dùng hai cạnh của nó; chỉ hai đầu "
                             "đường có bậc lẻ. Vậy đường đi Euler bắt đầu ở một đỉnh bậc lẻ và kết thúc ở đỉnh kia: "
                             f"{odd[0]}, {odd[1]}."])


# ------------------------------------------------------------------ Hamilton
def _relabel(rng: random.Random, n: int, edges) -> tuple[list[list[int]], dict[int, int]]:
    p = list(range(1, n + 1))
    rng.shuffle(p)
    m = {i + 1: p[i] for i in range(n)}
    return norm([(m[u], m[v]) for u, v in edges]), m


@generator("tr_g6_hamilton")
def hamilton(rng: random.Random) -> Draw:
    kind = rng.choice(["yes", "yes", "leaf", "cut", "bip"])
    if kind == "yes":
        n = rng.randint(5, 6)
        base = [(i, i % n + 1) for i in range(1, n + 1)]
        chords = [p for p in itertools.combinations(range(1, n + 1), 2) if p not in {tuple(sorted(e)) for e in base}]
        base += rng.sample(chords, rng.randint(0, 2))
    elif kind == "leaf":
        n = rng.randint(5, 6)
        base = [(i, i % (n - 1) + 1) for i in range(1, n)] + [(1, n)]        # a cycle on 1..n-1, n hangs on 1
        if rng.random() < 0.5:
            base.append((1, 3))
    elif kind == "cut":
        n = 5
        base = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (3, 5)]               # two triangles sharing vertex 3
    else:
        n = rng.choice([5, 6])
        small = 2
        left, right = list(range(1, small + 1)), list(range(small + 1, n + 1))
        base = [(a, b) for a in left for b in right]                          # K_(2, n-2), n-2 > 2
    edges, m = _relabel(rng, n, base)
    ok = kind == "yes"
    if kind == "yes":
        cyc = [m[i] for i in range(1, n + 1)] + [m[1]]
        why = [f"Chu trình {' - '.join(map(str, cyc))} đi qua mỗi đỉnh đúng một lần rồi trở về: khẳng định đúng."]
    elif kind == "leaf":
        why = [f"Đỉnh {m[n]} chỉ có bậc 1, mà trên một chu trình mỗi đỉnh dùng hai cạnh của nó.",
               "Vậy không có chu trình Hamilton: khẳng định sai."]
    elif kind == "cut":
        why = [f"Bỏ đỉnh {m[3]} đi thì đồ thị rời thành hai phần {{{m[1]}, {m[2]}}} và {{{m[4]}, {m[5]}}}.",
               f"Một chu trình Hamilton đi từ phần này sang phần kia rồi quay về phải qua {m[3]} hai lần.",
               "Vậy không có chu trình Hamilton: khẳng định sai."]
    else:
        why = [f"Mọi cạnh nối một đỉnh của {{{m[1]}, {m[2]}}} với một đỉnh trong {n - 2} đỉnh còn lại: G là đồ thị hai "
               f"phía với hai phần 2 và {n - 2} đỉnh.",
               "Một chu trình Hamilton phải đi xen kẽ hai phần, nên hai phần phải có cùng số đỉnh.",
               f"2 khác {n - 2}: không có chu trình Hamilton, khẳng định sai."]
    return Draw(params={"n": n, "edges": edges},
                prompt_vi=f"Đồ thị G có {graph_text(n, edges)}. Khẳng định: G có chu trình Hamilton.",
                answer=ok, solution_vi=["Chu trình Hamilton đi qua mỗi đỉnh đúng một lần rồi trở về đỉnh đầu."] + why)


@generator("tr_g6_dem_hamilton")
def dem_hamilton(rng: random.Random) -> Draw:
    kind = rng.choice(["kn", "kn", "knn"])
    if kind == "kn":
        n = rng.randint(4, 8)
        total = math.factorial(n - 1) // 2
        prompt = f"Đồ thị đầy đủ K_{n}"
        steps = [f"Cố định đỉnh xuất phát; thứ tự đi qua {n - 1} đỉnh còn lại là một hoán vị bất kỳ: ({n} - 1)! = "
                 f"{math.factorial(n - 1)} cách.",
                 "Mỗi chu trình được đếm hai lần, một lần cho mỗi chiều đi.",
                 f"Số chu trình Hamilton: {math.factorial(n - 1)}/2 = {total}."]
        params = {"kind": kind, "n": n}
    else:
        n = rng.randint(2, 4)
        total = math.factorial(n) ** 2 // (2 * n)
        prompt = f"Đồ thị hai phía đầy đủ K_({n}, {n}) (hai phần mỗi phần {n} đỉnh, mỗi đỉnh kề mọi đỉnh phần kia)"
        steps = [f"Cố định một đỉnh xuất phát ở phần thứ nhất. Chu trình đi xen kẽ: {n} đỉnh phần kia xếp theo {n}! "
                 f"cách, {n - 1} đỉnh còn lại của phần thứ nhất xếp theo {n - 1}! cách.",
                 f"Được {n}! . {n - 1}! = {math.factorial(n) * math.factorial(n - 1)} cách; mỗi chu trình được đếm hai lần "
                 "(hai chiều đi).",
                 f"Số chu trình Hamilton: {total}."]
        params = {"kind": kind, "n": n}
    return Draw(params=params,
                prompt_vi=(f"{prompt} có bao nhiêu chu trình Hamilton? Hai chu trình chỉ khác nhau ở đỉnh xuất phát hoặc ở "
                           "chiều đi được coi là một."),
                answer=str(total), solution_vi=steps)
