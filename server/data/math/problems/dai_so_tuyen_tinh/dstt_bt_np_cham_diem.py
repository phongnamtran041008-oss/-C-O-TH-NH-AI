"""Reference solution - server side only, never sent to the game.
điểm của mỗi hàng = tích vô hướng của hàng với w, cộng thêm b (X @ w + b)."""
import sys

du_lieu = list(map(int, sys.stdin.read().split()))
n, d = du_lieu[0], du_lieu[1]
X = [du_lieu[2 + i * d:2 + (i + 1) * d] for i in range(n)]
w = du_lieu[2 + n * d:2 + n * d + d]
b = du_lieu[2 + n * d + d]
diem = []
for hang in X:
    tong = b
    for j in range(d):
        tong += hang[j] * w[j]
    diem.append(tong)
print(*diem)
