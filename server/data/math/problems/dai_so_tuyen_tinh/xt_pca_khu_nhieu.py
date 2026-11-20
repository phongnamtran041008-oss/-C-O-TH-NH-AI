"""Reference solution - server side only, never sent to the game.
PCA bằng phép lặp lũy thừa có xuống thang: ma trận hiệp phương sai của dữ liệu huấn luyện,
k vectơ riêng lớn nhất, rồi chiếu từng điểm mới lên mặt phẳng qua trung bình mà chúng căng."""
import sys

data = sys.stdin.read().split()
n, d, k = int(data[0]), int(data[1]), int(data[2])
pos = 3
X = [[float(v) for v in data[pos + i * d:pos + (i + 1) * d]] for i in range(n)]
pos += n * d
m = int(data[pos])
pos += 1
Q = [[float(v) for v in data[pos + i * d:pos + (i + 1) * d]] for i in range(m)]

mu = [sum(x[j] for x in X) / n for j in range(d)]
C = [[sum((x[a] - mu[a]) * (x[b] - mu[b]) for x in X) / (n - 1) for b in range(d)] for a in range(d)]
basis = []
for _ in range(k):
    v = [1.0 / (j + 1) for j in range(d)]
    for _ in range(500):
        w = [sum(C[a][b] * v[b] for b in range(d)) for a in range(d)]
        for u in basis:                 # bỏ phần nằm trên các hướng đã tìm
            dot = sum(p * q for p, q in zip(u, w))
            w = [p - dot * q for p, q in zip(w, u)]
        norm = sum(p * p for p in w) ** 0.5
        v = [p / norm for p in w]
    basis.append(v)
out = []
for q in Q:
    c = [p - a for p, a in zip(q, mu)]
    r = list(mu)
    for u in basis:
        t = sum(p * s for p, s in zip(u, c))
        r = [a + t * s for a, s in zip(r, u)]
    out.append(" ".join(f"{v:.4f}" for v in r))
print("\n".join(out))
