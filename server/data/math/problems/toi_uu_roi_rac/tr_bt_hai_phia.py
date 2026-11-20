"""Reference solution - server side only, never sent to the game.
Tô màu BFS từng thành phần, cạnh cùng màu thì không hai phía."""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
canh = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
from collections import deque

ke = [[] for _ in range(n + 1)]
for u, v in canh:
    ke[u].append(v)
    ke[v].append(u)
mau = [-1] * (n + 1)
hai_phia = True
for s in range(1, n + 1):
    if mau[s] != -1:
        continue
    mau[s] = 0
    hang = deque([s])
    while hang:
        u = hang.popleft()
        for v in ke[u]:
            if mau[v] == -1:
                mau[v] = 1 - mau[u]
                hang.append(v)
            elif mau[v] == mau[u]:
                hai_phia = False
if hai_phia:
    print("co")
    print(*mau[1:])
else:
    print("khong")
