"""Reference solution - server side only, never sent to the game.
Đơn ánh: ảnh đôi một khác nhau; toàn ánh: ảnh phủ hết {1..m}."""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
f = list(map(int, data[2:2 + n]))
don = len(set(f)) == n
toan = len(set(f)) == m
print(*("co" if x else "khong" for x in (don, toan, don and toan)))
