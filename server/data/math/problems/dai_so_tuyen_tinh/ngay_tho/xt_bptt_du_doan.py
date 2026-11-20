"""Naive program - must NOT pass: predict the mean of the training y for every point."""
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
ys = [float(data[2 + i * (d + 1) + d]) for i in range(n)]
m = int(data[2 + n * (d + 1)])
mean = sum(ys) / n
print("\n".join(f"{mean:.4f}" for _ in range(m)))
