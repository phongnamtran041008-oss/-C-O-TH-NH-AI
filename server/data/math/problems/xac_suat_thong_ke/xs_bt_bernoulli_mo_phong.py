"""Reference solution - server side only, never sent to the game.
Đếm thí nghiệm có đúng k thành công; so với C(n,k) p^k (1-p)^(n-k)."""
import sys
from math import comb

data = sys.stdin.read().split()
seed = int(data[0])
n, q, T, k = map(int, data[1:5])
s = seed


def rnd():
    global s
    s = (s * 1103515245 + 12345) % 2147483648
    return s >> 16


dung = 0
for _ in range(T):
    thanh_cong = 0
    for _ in range(n):
        if rnd() % 100 < q:
            thanh_cong += 1
    if thanh_cong == k:
        dung += 1
p = q / 100
print(dung, f"{dung / T:.6f}", f"{comb(n, k) * p ** k * (1 - p) ** (n - k):.6f}")
