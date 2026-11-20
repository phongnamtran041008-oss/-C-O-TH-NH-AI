"""Reference solution - server side only, never sent to the game.
Giao, hợp, hiệu, hiệu đối xứng dưới dạng phép logic trên p, q."""
import sys

data = sys.stdin.read().split()
t = int(data[0])
for i in range(t):
    p = int(data[1 + 2 * i])
    q = int(data[2 + 2 * i])
    print(p & q, p | q, int(p == 1 and q == 0), p ^ q)
