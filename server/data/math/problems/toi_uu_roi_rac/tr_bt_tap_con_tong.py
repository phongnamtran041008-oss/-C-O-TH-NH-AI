"""Reference solution - server side only, never sent to the game.
Quay lui lấy hoặc bỏ từng số, đếm các cách đủ tổng."""
import sys

data = list(map(int, sys.stdin.read().split()))
n, s = data[0], data[1]
a = data[2:2 + n]


def dem(i, con_lai):
    if i == n:
        return 1 if con_lai == 0 else 0
    return dem(i + 1, con_lai) + dem(i + 1, con_lai - a[i])


print(dem(0, s))
