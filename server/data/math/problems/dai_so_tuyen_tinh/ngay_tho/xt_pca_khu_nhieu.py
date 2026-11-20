"""Naive program - must NOT pass: hand every noisy point back unchanged (no denoising at all)."""
import sys

data = sys.stdin.read().split()
n, d, k = int(data[0]), int(data[1]), int(data[2])
pos = 3 + n * d
m = int(data[pos])
pos += 1
for i in range(m):
    print(" ".join(data[pos + i * d:pos + (i + 1) * d]))
