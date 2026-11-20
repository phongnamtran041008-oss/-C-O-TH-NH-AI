"""Reference solution - server side only, never sent to the game.
Hiệu d = pB - pA, khoảng tin cậy 95% d +- 1.96 sqrt(pA(1-pA)/nA + pB(1-pB)/nB), thống kê z
với tỉ lệ gộp p = (kA + kB)/(nA + nB): z = d / sqrt(p(1-p)(1/nA + 1/nB)); kết luận theo |z| > 1.96."""
import math
import sys

na, ka, nb, kb = (int(v) for v in sys.stdin.read().split())
pa, pb = ka / na, kb / nb
d = pb - pa
h = 1.96 * math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
p = (ka + kb) / (na + nb)
se = math.sqrt(p * (1 - p) * (1 / na + 1 / nb))
z = d / se if se > 0 else 0.0
print(f"{d:.6f} {d - h:.6f} {d + h:.6f}")
print(f"{z:.6f}")
print("B" if z > 1.96 else "A" if z < -1.96 else "0")
