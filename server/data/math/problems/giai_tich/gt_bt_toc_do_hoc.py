"""Reference solution - server side only, never sent to the game.
Mô phỏng x -= lr*2x trong T bước, xếp loại theo |x|."""
import sys

data = sys.stdin.read().split()
x0, T, q = int(data[0]), int(data[1]), int(data[2])
for lr in map(float, data[3:3 + q]):
    x = float(x0)
    for _ in range(T):
        x = x - lr * 2 * x
    if abs(x) < 0.001:
        print("hoi_tu")
    elif abs(x) > 1000:
        print("phan_ky")
    else:
        print("chua_hoi_tu")
