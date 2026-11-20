"""Naive program - must NOT pass: reads the 64 numbers column by column, so the picture comes
out transposed (a 7 would lie on its side)."""
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
side = int(round(d ** 0.5))
images, labels = [], []
pos = 2
for _ in range(n):
    images.append([int(v) for v in data[pos:pos + d]])
    labels.append(int(data[pos + d]))
    pos += d + 1
i = int(data[pos]) - 1
for c in range(side):
    print("".join("#" if images[i][r * side + c] >= 8 else "." for r in range(side)))
print(labels[i])
print(" ".join(str(labels.count(c)) for c in range(10)))
