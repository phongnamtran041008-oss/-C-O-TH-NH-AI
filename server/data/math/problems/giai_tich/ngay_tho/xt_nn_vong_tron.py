"""Naive program - must NOT pass: a straight line (logistic regression with no hidden layer)
cannot cut a disc out of a square, so it does about as well as guessing the majority."""
import math
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
pos = 2
X, Y = [], []
for _ in range(n):
    X.append([float(v) for v in data[pos:pos + d]])
    Y.append(float(data[pos + d]))
    pos += d + 1
m = int(data[pos])
pos += 1
Q = [[float(v) for v in data[pos + i * d:pos + (i + 1) * d]] for i in range(m)]
w, b = [0.0] * d, 0.0
for _ in range(200):
    gw, gb = [0.0] * d, 0.0
    for x, y in zip(X, Y):
        p = 1 / (1 + math.exp(-(sum(a * c for a, c in zip(w, x)) + b)))
        for k in range(d):
            gw[k] += (p - y) * x[k]
        gb += p - y
    w = [a - 0.5 * g / n for a, g in zip(w, gw)]
    b -= 0.5 * gb / n
print("\n".join("1" if sum(a * c for a, c in zip(w, q)) + b >= 0 else "0" for q in Q))
