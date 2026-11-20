"""Reference solution - server side only, never sent to the game.
Bình phương tối thiểu: thêm cột 1 cho hệ số tự do, lập phương trình chuẩn (A^T A) w = A^T y
và giải bằng khử Gauss có chọn phần tử trội."""
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
pos = 2
rows, ys = [], []
for _ in range(n):
    rows.append([float(v) for v in data[pos:pos + d]] + [1.0])
    ys.append(float(data[pos + d]))
    pos += d + 1
m = int(data[pos])
pos += 1
qs = []
for _ in range(m):
    qs.append([float(v) for v in data[pos:pos + d]] + [1.0])
    pos += d

k = d + 1
ata = [[sum(r[i] * r[j] for r in rows) for j in range(k)] for i in range(k)]
aty = [sum(r[i] * y for r, y in zip(rows, ys)) for i in range(k)]
M = [ata[i] + [aty[i]] for i in range(k)]
for c in range(k):
    p = max(range(c, k), key=lambda r: abs(M[r][c]))
    M[c], M[p] = M[p], M[c]
    for r in range(c + 1, k):
        f = M[r][c] / M[c][c]
        for j in range(c, k + 1):
            M[r][j] -= f * M[c][j]
w = [0.0] * k
for c in range(k - 1, -1, -1):
    w[c] = (M[c][k] - sum(M[c][j] * w[j] for j in range(c + 1, k))) / M[c][c]
print("\n".join(f"{sum(a * b for a, b in zip(q, w)):.4f}" for q in qs))
