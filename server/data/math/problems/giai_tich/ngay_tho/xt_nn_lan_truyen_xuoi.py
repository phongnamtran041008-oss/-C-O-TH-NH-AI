"""Naive program - must NOT pass: uses sigmoid in the hidden layer instead of tanh."""
import math
import sys

data = sys.stdin.read().split()
d, H = int(data[0]), int(data[1])
pos = 2
W1 = [[float(v) for v in data[pos + j * d:pos + (j + 1) * d]] for j in range(H)]
pos += H * d
b1 = [float(v) for v in data[pos:pos + H]]
pos += H
W2 = [float(v) for v in data[pos:pos + H]]
pos += H
b2 = float(data[pos])
x = [float(v) for v in data[pos + 1:pos + 1 + d]]
h = [1 / (1 + math.exp(-(sum(w * v for w, v in zip(W1[j], x)) + b1[j]))) for j in range(H)]
z = sum(w * v for w, v in zip(W2, h)) + b2
print(" ".join(f"{v:.6f}" for v in h))
print(f"{1 / (1 + math.exp(-z)):.6f}")
