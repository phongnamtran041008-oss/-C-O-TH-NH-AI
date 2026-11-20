"""Naive program - must NOT pass: always predict the most common kind of the training data."""
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
labels = [data[2 + i * (d + 1) + d] for i in range(n)]
m = int(data[2 + n * (d + 1)])
top = max(set(labels), key=labels.count)
print("\n".join([top] * m))
