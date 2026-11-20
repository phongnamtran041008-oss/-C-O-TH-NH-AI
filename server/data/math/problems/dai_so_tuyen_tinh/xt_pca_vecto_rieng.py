"""Reference solution - server side only, never sent to the game.
Giá trị riêng lớn nhất và vectơ riêng đơn vị của nó bằng phép lặp lũy thừa: v <- Cv / |Cv|
cho tới khi không đổi nữa; lambda = v . Cv. Đổi dấu để thành phần có trị tuyệt đối lớn nhất dương."""
import math
import sys

data = sys.stdin.read().split()
d = int(data[0])
C = [[float(v) for v in data[1 + i * d:1 + (i + 1) * d]] for i in range(d)]
v = [1.0] * d
for _ in range(5000):
    w = [sum(C[i][j] * v[j] for j in range(d)) for i in range(d)]
    norm = math.sqrt(sum(t * t for t in w))
    w = [t / norm for t in w]
    if max(abs(a - b) for a, b in zip(w, v)) < 1e-15:
        v = w
        break
    v = w
lam = sum(v[i] * sum(C[i][j] * v[j] for j in range(d)) for i in range(d))
big = max(range(d), key=lambda i: abs(v[i]))
if v[big] < 0:
    v = [-t for t in v]
print(f"{lam:.6f}")
print(" ".join(f"{t:.6f}" for t in v))
