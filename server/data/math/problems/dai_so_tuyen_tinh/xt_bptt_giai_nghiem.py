"""Reference solution - server side only, never sent to the game.
Nghiệm bình phương tối thiểu: giải (A^T A) x = A^T b bằng khử Gauss có chọn phần tử trội,
rồi in độ dài phần dư |Ax - b|."""
import math
import sys

data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
A = [[float(v) for v in data[2 + i * n:2 + (i + 1) * n]] for i in range(m)]
b = [float(v) for v in data[2 + m * n:2 + m * n + m]]
M = [[sum(A[r][i] * A[r][j] for r in range(m)) for j in range(n)] + [sum(A[r][i] * b[r] for r in range(m))]
     for i in range(n)]
for c in range(n):
    p = max(range(c, n), key=lambda r: abs(M[r][c]))
    M[c], M[p] = M[p], M[c]
    for r in range(c + 1, n):
        f = M[r][c] / M[c][c]
        for j in range(c, n + 1):
            M[r][j] -= f * M[c][j]
x = [0.0] * n
for c in range(n - 1, -1, -1):
    x[c] = (M[c][n] - sum(M[c][j] * x[j] for j in range(c + 1, n))) / M[c][c]
res = math.sqrt(sum((sum(A[r][j] * x[j] for j in range(n)) - b[r]) ** 2 for r in range(m)))
print(" ".join(f"{v:.6f}" for v in x))
print(f"{res:.6f}")
