"""Naive program - must NOT pass: forgets the derivative of tanh (the factor 1 - h^2) on the
way back through the hidden layer."""
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
y = float(data[pos + 1 + d])
h = [math.tanh(sum(w * v for w, v in zip(W1[j], x)) + b1[j]) for j in range(H)]
p = 1 / (1 + math.exp(-(sum(w * v for w, v in zip(W2, h)) + b2)))
L = -(y * math.log(p) + (1 - y) * math.log(1 - p))
dz = p - y
da = [dz * W2[j] for j in range(H)]
print(f"{L:.6f}")
for j in range(H):
    print(" ".join(f"{da[j] * v:.6f}" for v in x))
print(" ".join(f"{v:.6f}" for v in da))
print(" ".join(f"{dz * v:.6f}" for v in h))
print(f"{dz:.6f}")
