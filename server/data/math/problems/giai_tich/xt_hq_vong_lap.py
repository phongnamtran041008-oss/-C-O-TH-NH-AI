"""Reference solution - server side only, never sent to the game.
T bước hạ gradient trên cả lô: tính cả hai đạo hàm tại (a, b) cũ rồi mới cập nhật cả hai."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
pts = [(float(data[1 + 2 * i]), float(data[2 + 2 * i])) for i in range(n)]
a, b, lr = float(data[1 + 2 * n]), float(data[2 + 2 * n]), float(data[3 + 2 * n])
T = int(data[4 + 2 * n])
for _ in range(T):
    da = db = 0.0
    for x, y in pts:
        e = a * x + b - y
        da += 2 * e * x / n
        db += 2 * e / n
    a, b = a - lr * da, b - lr * db
L = sum((a * x + b - y) ** 2 for x, y in pts) / n
print(f"{a:.6f} {b:.6f} {L:.6f}")
