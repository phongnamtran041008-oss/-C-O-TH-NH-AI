"""Reference solution - server side only, never sent to the game.
Dijkstra với heapq từ đỉnh 1."""
import heapq
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
ke = [[] for _ in range(n + 1)]
for i in range(m):
    u, v, w = int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])
    ke[u].append((v, w))
    ke[v].append((u, w))
VO_CUNG = float("inf")
kc = [VO_CUNG] * (n + 1)
kc[1] = 0
heap = [(0, 1)]
while heap:
    d, u = heapq.heappop(heap)
    if d > kc[u]:
        continue
    for v, w in ke[u]:
        if d + w < kc[v]:
            kc[v] = d + w
            heapq.heappush(heap, (kc[v], v))
print(*(x if x != VO_CUNG else -1 for x in kc[1:]))
