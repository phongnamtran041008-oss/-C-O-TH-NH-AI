"""Reference solution - server side only, never sent to the game.
Tỉ lệ mẫu p = k/n và khoảng tin cậy 95% xấp xỉ chuẩn p +- 1.96 sqrt(p(1-p)/n), cắt về [0, 1]."""
import math
import sys

n, k = (int(v) for v in sys.stdin.read().split())
p = k / n
h = 1.96 * math.sqrt(p * (1 - p) / n)
print(f"{p:.6f} {max(0.0, p - h):.6f} {min(1.0, p + h):.6f}")
