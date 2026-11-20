"""Reference solution - server side only, never sent to the game.
Khử Gauss có đổi hàng, thế ngược, số học phân số chính xác."""
import sys
from fractions import Fraction

data = sys.stdin.read().split()
n = int(data[0])
M = [[Fraction(int(data[1 + i * (n + 1) + j])) for j in range(n + 1)] for i in range(n)]
for c in range(n):
    p = next(r for r in range(c, n) if M[r][c] != 0)
    M[c], M[p] = M[p], M[c]
    for r in range(c + 1, n):
        f = M[r][c] / M[c][c]
        M[r] = [x - f * y for x, y in zip(M[r], M[c])]
x = [Fraction(0)] * n
for i in range(n - 1, -1, -1):
    s = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
    x[i] = s / M[i][i]
print(*(str(v) for v in x))
