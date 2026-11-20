"""Reference solution - server side only, never sent to the game.
Hạng của A và của [A|b] bằng khử Gauss, rồi biện luận."""
import sys
from fractions import Fraction


def hang(M, cot):
    M = [h[:] for h in M]
    r = 0
    for c in range(cot):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(r + 1, len(M)):
            f = M[i][c] / M[r][c]
            M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r


data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
M = [[Fraction(int(data[2 + i * (n + 1) + j])) for j in range(n + 1)] for i in range(m)]
ra = hang(M, n)
rb = hang(M, n + 1)
if ra < rb:
    print("vo_nghiem", ra, rb)
elif ra == n:
    print("duy_nhat", ra, rb)
else:
    print("vo_so_nghiem", ra, rb)
