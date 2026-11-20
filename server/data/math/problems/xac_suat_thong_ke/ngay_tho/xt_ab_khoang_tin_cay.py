"""Naive program - must NOT pass: forgets to divide by n inside the square root, so the
interval does not shrink as the sample grows."""
import math
import sys

n, k = (int(v) for v in sys.stdin.read().split())
p = k / n
h = 1.96 * math.sqrt(p * (1 - p))
print(f"{p:.6f} {max(0.0, p - h):.6f} {min(1.0, p + h):.6f}")
