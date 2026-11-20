"""Reference solution - server side only, never sent to the game.
Kiểm định hai tỉ lệ (z, gộp tỉ lệ dưới giả thuyết không), mức ý nghĩa 5% hai phía."""
import math
import sys

data = sys.stdin.read().split()
K = int(data[0])
out = []
for i in range(K):
    na, ka, nb, kb = (int(v) for v in data[1 + 4 * i:5 + 4 * i])
    pa, pb = ka / na, kb / nb
    p = (ka + kb) / (na + nb)
    se = math.sqrt(p * (1 - p) * (1 / na + 1 / nb))
    z = (pb - pa) / se if se > 0 else 0.0
    out.append("B" if z > 1.96 else "A" if z < -1.96 else "0")
print("\n".join(out))
