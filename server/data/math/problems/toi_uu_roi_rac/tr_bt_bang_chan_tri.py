"""Reference solution - server side only, never sent to the game.
Bốn phép nối: và, hoặc, kéo theo, khi và chỉ khi."""
import sys

data = sys.stdin.read().split()
t = int(data[0])
for i in range(t):
    p = int(data[1 + 2 * i])
    q = int(data[2 + 2 * i])
    print(p & q, p | q, int((not p) or q), int(p == q))
