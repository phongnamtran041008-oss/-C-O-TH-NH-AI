"""Reference solution - server side only, never sent to the game.
Hồi quy logistic: chuẩn hóa từng đặc trưng (trừ trung bình, chia độ lệch chuẩn), hạ gradient
trên mất mát log trung bình, ngưỡng 0.5. In mất mát ra stderr."""
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

mu = [sum(x[k] for x in X) / n for k in range(d)]
sd = [math.sqrt(sum((x[k] - mu[k]) ** 2 for x in X) / n) or 1.0 for k in range(d)]


def norm(x):
    return [(v - a) / s for v, a, s in zip(x, mu, sd)]


Xn = [norm(x) for x in X]


def sigmoid(z):
    return 1 / (1 + math.exp(-z)) if z > -40 else 0.0


w, b, lr = [0.0] * d, 0.0, 0.5
for epoch in range(200):
    gw, gb, loss = [0.0] * d, 0.0, 0.0
    for x, y in zip(Xn, Y):
        p = min(max(sigmoid(sum(a * c for a, c in zip(w, x)) + b), 1e-9), 1 - 1e-9)
        loss -= y * math.log(p) + (1 - y) * math.log(1 - p)
        for k in range(d):
            gw[k] += (p - y) * x[k]
        gb += p - y
    w = [a - lr * g / n for a, g in zip(w, gw)]
    b -= lr * gb / n
    if epoch % 10 == 0:
        print(f"#loss {epoch} {loss / n:.6f}", file=sys.stderr)
print("\n".join("1" if sigmoid(sum(a * c for a, c in zip(w, norm(q))) + b) >= 0.5 else "0" for q in Q))
