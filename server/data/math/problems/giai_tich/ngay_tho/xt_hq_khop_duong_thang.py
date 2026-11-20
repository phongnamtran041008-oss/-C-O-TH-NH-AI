"""Naive program - must NOT pass: predict the mean of the training y for every x."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
ys = [float(data[2 + 2 * i]) for i in range(n)]
m = int(data[1 + 2 * n])
mean = sum(ys) / n
print("\n".join(f"{mean:.4f}" for _ in range(m)))
