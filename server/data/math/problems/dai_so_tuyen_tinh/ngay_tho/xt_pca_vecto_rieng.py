"""Naive program - must NOT pass: stops the power iteration after three steps, long before
the vector has settled."""
import math
import sys

data = sys.stdin.read().split()
d = int(data[0])
C = [[float(v) for v in data[1 + i * d:1 + (i + 1) * d]] for i in range(d)]
v = [1.0] * d
for _ in range(3):
    w = [sum(C[i][j] * v[j] for j in range(d)) for i in range(d)]
    norm = math.sqrt(sum(t * t for t in w))
    v = [t / norm for t in w]
lam = sum(v[i] * sum(C[i][j] * v[j] for j in range(d)) for i in range(d))
big = max(range(d), key=lambda i: abs(v[i]))
if v[big] < 0:
    v = [-t for t in v]
print(f"{lam:.6f}")
print(" ".join(f"{t:.6f}" for t in v))
