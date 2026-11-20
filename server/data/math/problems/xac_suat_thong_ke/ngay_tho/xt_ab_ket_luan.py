"""Naive program - must NOT pass: crown whichever arm had the higher rate in this one run,
never admitting that the difference could be chance."""
import sys

data = sys.stdin.read().split()
K = int(data[0])
out = []
for i in range(K):
    na, ka, nb, kb = (int(v) for v in data[1 + 4 * i:5 + 4 * i])
    out.append("B" if kb / nb > ka / na else "A" if kb / nb < ka / na else "0")
print("\n".join(out))
