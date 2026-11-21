"""Reference solution - server side only, never sent to the game.
Tổng theo trục: axis = 0 cộng dọc từng cột, axis = 1 cộng ngang từng hàng."""
import sys

du_lieu = list(map(int, sys.stdin.read().split()))
r, c, truc = du_lieu[0], du_lieu[1], du_lieu[2]
A = [du_lieu[3 + i * c:3 + (i + 1) * c] for i in range(r)]
if truc == 0:
    kq = [sum(A[i][j] for i in range(r)) for j in range(c)]
else:
    kq = [sum(hang) for hang in A]
print(*kq)
