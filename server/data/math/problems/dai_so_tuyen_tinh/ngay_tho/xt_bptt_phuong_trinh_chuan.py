"""Naive program - must NOT pass: multiplies on the wrong side, A A^T (m x m) instead of A^T A."""
import sys

data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
A = [[int(v) for v in data[2 + i * n:2 + (i + 1) * n]] for i in range(m)]
b = [int(v) for v in data[2 + m * n:2 + m * n + m]]
for i in range(m):
    print(" ".join(str(sum(A[i][c] * A[j][c] for c in range(n))) for j in range(m)))
print(" ".join(str(sum(A[r][i] * b[r] for r in range(m))) for i in range(n)))
