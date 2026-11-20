"""Reference solution - server side only, never sent to the game.
Danh sách kề hai chiều, bậc, tổng bậc, số đỉnh bậc lẻ."""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
canh = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]
ke = [[] for _ in range(n + 1)]
for u, v in canh:
    ke[u].append(v)
    ke[v].append(u)
for i in range(1, n + 1):
    ke[i].sort()
    print(len(ke[i]), *ke[i])
print(sum(len(ke[i]) for i in range(1, n + 1)), sum(1 for i in range(1, n + 1) if len(ke[i]) % 2 == 1))
