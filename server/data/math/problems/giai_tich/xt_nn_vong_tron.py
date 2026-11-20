"""Reference solution - server side only, never sent to the game.
Mạng 2 -> 8 (tanh) -> 1 (sigmoid), mất mát entropy chéo nhị phân, hạ gradient ngẫu nhiên từng
mẫu, khởi tạo bằng hạt giống cố định. In mất mát trung bình mỗi vòng ra stderr."""
import math
import random
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

H = 8
rng = random.Random(1)
W1 = [[rng.gauss(0, 1) for _ in range(d)] for _ in range(H)]
b1 = [0.0] * H
W2 = [rng.gauss(0, 1) / math.sqrt(H) for _ in range(H)]
b2 = 0.0


def forward(x):
    h = [math.tanh(sum(w * v for w, v in zip(W1[j], x)) + b1[j]) for j in range(H)]
    z = sum(w * v for w, v in zip(W2, h)) + b2
    p = 1 / (1 + math.exp(-z)) if z > -40 else 0.0
    return h, p


lr = 0.1
order = list(range(n))
for epoch in range(120):
    rng.shuffle(order)
    loss = 0.0
    for i in order:
        x, y = X[i], Y[i]
        h, p = forward(x)
        p = min(max(p, 1e-9), 1 - 1e-9)
        loss -= y * math.log(p) + (1 - y) * math.log(1 - p)
        dz = p - y
        for j in range(H):
            dh = dz * W2[j] * (1 - h[j] * h[j])
            W2[j] -= lr * dz * h[j]
            b1[j] -= lr * dh
            row = W1[j]
            for k in range(d):
                row[k] -= lr * dh * x[k]
        b2 -= lr * dz
    if epoch % 5 == 0:
        print(f"#loss {epoch} {loss / n:.6f}", file=sys.stderr)
print("\n".join("1" if forward(q)[1] >= 0.5 else "0" for q in Q))
