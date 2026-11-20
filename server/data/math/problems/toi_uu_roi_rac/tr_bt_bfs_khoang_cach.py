"""Reference solution - server side only, never sent to the game.
BFS từ s, khoảng cách tính bằng số cạnh, -1 nếu không tới được."""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
canh = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
from collections import deque

s = int(data[2 + 2 * m])
ke = [[] for _ in range(n + 1)]
for u, v in canh:
    ke[u].append(v)
    ke[v].append(u)
kc = [-1] * (n + 1)
kc[s] = 0
hang = deque([s])
while hang:
    u = hang.popleft()
    for v in ke[u]:
        if kc[v] == -1:
            kc[v] = kc[u] + 1
            hang.append(v)
print(*kc[1:])
