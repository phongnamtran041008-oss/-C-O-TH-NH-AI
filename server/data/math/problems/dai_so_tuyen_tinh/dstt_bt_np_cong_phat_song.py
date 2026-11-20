"""Reference solution - server side only, never sent to the game.
Cộng vectơ b vào từng hàng của X (phát sóng một hàng ra r hàng)."""
import sys

du_lieu = list(map(int, sys.stdin.read().split()))
r, c = du_lieu[0], du_lieu[1]
X = [du_lieu[2 + i * c:2 + (i + 1) * c] for i in range(r)]
b = du_lieu[2 + r * c:2 + r * c + c]
for i in range(r):
    print(*[X[i][j] + b[j] for j in range(c)])
