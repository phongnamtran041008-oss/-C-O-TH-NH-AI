"""Naive program - must NOT pass: finds the k nearest right, then trusts the single nearest
one instead of counting the votes."""
import sys

data = sys.stdin.read().split()
n, k = int(data[0]), int(data[1])
pts = []
for i in range(n):
    x, y, lab = int(data[2 + 3 * i]), int(data[3 + 3 * i]), data[4 + 3 * i]
    pts.append((x, y, lab, i))
qx, qy = int(data[2 + 3 * n]), int(data[3 + 3 * n])
near = sorted(pts, key=lambda p: ((p[0] - qx) ** 2 + (p[1] - qy) ** 2, p[3]))[:k]
print(" ".join(p[2] for p in near))
print(near[0][2])
