"""Naive program - must NOT pass: uses the spread of B alone, as if A were known exactly."""
import math
import sys

na, ka, nb, kb = (int(v) for v in sys.stdin.read().split())
pa, pb = ka / na, kb / nb
d = pb - pa
se = math.sqrt(pb * (1 - pb) / nb)
z = d / se if se > 0 else 0.0
print(f"{d:.6f} {d - 1.96 * se:.6f} {d + 1.96 * se:.6f}")
print(f"{z:.6f}")
print("B" if z > 1.96 else "A" if z < -1.96 else "0")
