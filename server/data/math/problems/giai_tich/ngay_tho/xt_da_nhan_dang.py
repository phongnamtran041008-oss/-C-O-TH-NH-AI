"""Naive program - must NOT pass: compare each image with the mean image of every digit and
take the nearest mean (one template per digit; real handwriting varies more than that)."""
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
pos = 2
sums, counts = {}, {}
for _ in range(n):
    x = [int(v) for v in data[pos:pos + d]]
    y = data[pos + d]
    pos += d + 1
    s = sums.setdefault(y, [0] * d)
    for i in range(d):
        s[i] += x[i]
    counts[y] = counts.get(y, 0) + 1
means = {y: [v / counts[y] for v in s] for y, s in sums.items()}
m = int(data[pos])
pos += 1
out = []
for _ in range(m):
    q = [int(v) for v in data[pos:pos + d]]
    pos += d
    out.append(min(means, key=lambda y: sum((a - b) ** 2 for a, b in zip(means[y], q))))
print("\n".join(out))
