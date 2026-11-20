"""Reference solution - server side only, never sent to the game.
Khoảng cách Euclid từ điểm hỏi tới từng điểm, rồi chỉ số (từ 1) của điểm gần nhất."""
import math
import sys

data = sys.stdin.read().split()
d = int(data[0])
q = [float(v) for v in data[1:1 + d]]
n = int(data[1 + d])
pos = 2 + d
dist = []
for _ in range(n):
    p = [float(v) for v in data[pos:pos + d]]
    pos += d
    dist.append(math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q))))
print(" ".join(f"{v:.6f}" for v in dist))
print(min(range(n), key=lambda i: (dist[i], i)) + 1)
