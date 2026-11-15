"""Reference solution - server side only, never sent to the game.
Tích vô hướng u.v = u1*v1 + ... + un*vn."""
import sys

data = list(map(int, sys.stdin.read().split()))
n = data[0]
u = data[1:1 + n]
v = data[1 + n:1 + 2 * n]
print(sum(x * y for x, y in zip(u, v)))
