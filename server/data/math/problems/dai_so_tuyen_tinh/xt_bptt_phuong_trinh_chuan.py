"""Reference solution - server side only, never sent to the game.
In A^T A (n x n) và A^T b, với A là m x n và b có m số. Số nguyên vào, số nguyên ra."""
import sys

data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
A = [[int(v) for v in data[2 + i * n:2 + (i + 1) * n]] for i in range(m)]
b = [int(v) for v in data[2 + m * n:2 + m * n + m]]
for i in range(n):
    print(" ".join(str(sum(A[r][i] * A[r][j] for r in range(m))) for j in range(n)))
print(" ".join(str(sum(A[r][i] * b[r] for r in range(m))) for i in range(n)))
