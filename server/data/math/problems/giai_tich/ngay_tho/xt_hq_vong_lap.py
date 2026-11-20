"""Naive program - must NOT pass: updates a first, then computes the slope for b with the
new a (the two derivatives must both be taken at the old point)."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
pts = [(float(data[1 + 2 * i]), float(data[2 + 2 * i])) for i in range(n)]
a, b, lr = float(data[1 + 2 * n]), float(data[2 + 2 * n]), float(data[3 + 2 * n])
T = int(data[4 + 2 * n])
for _ in range(T):
    da = sum(2 * (a * x + b - y) * x / n for x, y in pts)
    a -= lr * da
    db = sum(2 * (a * x + b - y) / n for x, y in pts)
    b -= lr * db
L = sum((a * x + b - y) ** 2 for x, y in pts) / n
print(f"{a:.6f} {b:.6f} {L:.6f}")
