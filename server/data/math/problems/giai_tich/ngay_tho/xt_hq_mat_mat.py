"""Naive program - must NOT pass: drops the 2 that comes down from the square."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
pts = [(float(data[1 + 2 * i]), float(data[2 + 2 * i])) for i in range(n)]
a, b = float(data[1 + 2 * n]), float(data[2 + 2 * n])
L = da = db = 0.0
for x, y in pts:
    e = a * x + b - y
    L += e * e
    da += e * x
    db += e
print(f"{L / n:.6f} {da / n:.6f} {db / n:.6f}")
