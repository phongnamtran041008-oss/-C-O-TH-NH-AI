"""Naive program - must NOT pass: call every message the most common kind in the training data."""
import sys

lines = sys.stdin.read().split("\n")
n = int(lines[0])
labels = [line.split()[0] for line in lines[1:1 + n]]
m = int(lines[1 + n])
top = max(set(labels), key=labels.count)
print("\n".join([top] * m))
