"""Reference solution - server side only, never sent to the game.
Ước lượng P(A | B) = nAB / nB bằng mô phỏng hai xúc xắc."""
import sys

seed, N = map(int, sys.stdin.read().split())
s = seed


def rnd():
    global s
    s = (s * 1103515245 + 12345) % 2147483648
    return s >> 16


nB = nAB = 0
for _ in range(N):
    x = rnd() % 6 + 1
    y = rnd() % 6 + 1
    if x == 6 or y == 6:
        nB += 1
        if x + y >= 10:
            nAB += 1
print(nB, nAB, f"{(nAB / nB if nB else 0):.6f}")
