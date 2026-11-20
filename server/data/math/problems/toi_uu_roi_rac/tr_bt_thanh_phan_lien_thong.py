"""Reference solution - server side only, never sent to the game.
DFS đệ quy từ mỗi đỉnh chưa thăm, đếm thành phần và cỡ lớn nhất."""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
canh = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
sys.setrecursionlimit(10000)
ke = [[] for _ in range(n + 1)]
for u, v in canh:
    ke[u].append(v)
    ke[v].append(u)
thay = [False] * (n + 1)


def dfs(u):
    thay[u] = True
    dem = 1
    for v in ke[u]:
        if not thay[v]:
            dem += dfs(v)
    return dem


so = 0
lon = 0
for u in range(1, n + 1):
    if not thay[u]:
        so += 1
        lon = max(lon, dfs(u))
print(so, lon)
