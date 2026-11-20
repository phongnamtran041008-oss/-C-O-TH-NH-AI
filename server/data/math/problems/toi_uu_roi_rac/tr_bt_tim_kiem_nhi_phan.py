"""Reference solution - server side only, never sent to the game.
Tìm kiếm nhị phân đúng như đề tả, đếm số lần thăm."""
import sys

data = sys.stdin.read().split()
n, q = int(data[0]), int(data[1])
a = list(map(int, data[2:2 + n]))
ra = []
for x in map(int, data[2 + n:2 + n + q]):
    lo, hi, tham = 0, n - 1, 0
    vi_tri = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        tham += 1
        if a[mid] == x:
            vi_tri = mid
            break
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    ra.append(f"{vi_tri} {tham}")
print("\n".join(ra))
