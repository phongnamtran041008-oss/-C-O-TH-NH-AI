"""Reference solution - server side only, never sent to the game.
Vectơ trung bình và ma trận hiệp phương sai mẫu (chia n - 1)."""
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
X = [[float(v) for v in data[2 + i * d:2 + (i + 1) * d]] for i in range(n)]
mu = [sum(x[j] for x in X) / n for j in range(d)]
print(" ".join(f"{v:.6f}" for v in mu))
for a in range(d):
    print(" ".join(f"{sum((x[a] - mu[a]) * (x[b] - mu[b]) for x in X) / (n - 1):.6f}" for b in range(d)))
