"""Reference solution - server side only, never sent to the game.
A^T: dòng i của A thành cột i của A^T."""
import sys

data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
o = data[2:2 + m * n]
a = [o[r * n:(r + 1) * n] for r in range(m)]
for c in range(n):
    print(" ".join(a[r][c] for r in range(m)))
