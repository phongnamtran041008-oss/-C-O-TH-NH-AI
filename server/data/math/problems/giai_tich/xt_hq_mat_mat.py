"""Reference solution - server side only, never sent to the game.
L(a, b) = (1/n) * tổng (a*x + b - y)^2; dL/da = (2/n) * tổng e*x; dL/db = (2/n) * tổng e."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
pts = [(float(data[1 + 2 * i]), float(data[2 + 2 * i])) for i in range(n)]
a, b = float(data[1 + 2 * n]), float(data[2 + 2 * n])
L = da = db = 0.0
for x, y in pts:
    e = a * x + b - y
    L += e * e
    da += 2 * e * x
    db += 2 * e
print(f"{L / n:.6f} {da / n:.6f} {db / n:.6f}")
