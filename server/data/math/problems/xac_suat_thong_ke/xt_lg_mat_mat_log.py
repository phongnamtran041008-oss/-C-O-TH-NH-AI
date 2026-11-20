"""Reference solution - server side only, never sent to the game.
Mất mát log trung bình (âm log hợp lý chia n) của hồi quy logistic và gradient của nó:
dL/dw = (1/n) tổng (p - y) x, dL/db = (1/n) tổng (p - y)."""
import math
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
pos = 2
rows = []
for _ in range(n):
    rows.append(([float(v) for v in data[pos:pos + d]], float(data[pos + d])))
    pos += d + 1
w = [float(v) for v in data[pos:pos + d]]
b = float(data[pos + d])
L, gw, gb = 0.0, [0.0] * d, 0.0
for x, y in rows:
    p = 1 / (1 + math.exp(-(sum(a * c for a, c in zip(w, x)) + b)))
    L -= y * math.log(p) + (1 - y) * math.log(1 - p)
    for k in range(d):
        gw[k] += (p - y) * x[k]
    gb += p - y
print(f"{L / n:.6f}")
print(" ".join(f"{g / n:.6f}" for g in gw))
print(f"{gb / n:.6f}")
