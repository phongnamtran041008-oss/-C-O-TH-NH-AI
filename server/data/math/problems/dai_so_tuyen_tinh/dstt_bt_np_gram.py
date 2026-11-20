"""Reference solution - server side only, never sent to the game.
G = X^T X: phần tử (i, j) là tích vô hướng của cột i với cột j của X."""
import sys

du_lieu = list(map(int, sys.stdin.read().split()))
n, d = du_lieu[0], du_lieu[1]
X = [du_lieu[2 + i * d:2 + (i + 1) * d] for i in range(n)]
XT = [[X[i][j] for i in range(n)] for j in range(d)]
for a in range(d):
    hang = []
    for b in range(d):
        hang.append(sum(XT[a][k] * X[k][b] for k in range(n)))
    print(*hang)
