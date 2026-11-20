"""Reference solution - server side only, never sent to the game.
Gieo N lần bằng bộ sinh số tự viết, đếm mặt."""
import sys

seed, N = map(int, sys.stdin.read().split())
s = seed


def rnd():
    global s
    s = (s * 1103515245 + 12345) % 2147483648
    return s >> 16


dem = [0] * 7
for _ in range(N):
    dem[rnd() % 6 + 1] += 1
print(*dem[1:])
print(f"{dem[6] / N:.6f}")
