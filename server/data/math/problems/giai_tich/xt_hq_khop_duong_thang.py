"""Reference solution - server side only, never sent to the game.
Khớp y = a*x + b bằng hạ gradient trên sai số bình phương trung bình. x được dời về quanh 0
(trừ trung bình) để a và b học cùng nhịp; in mất mát ra stderr để game vẽ."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
xs = [float(data[1 + 2 * i]) for i in range(n)]
ys = [float(data[2 + 2 * i]) for i in range(n)]
m = int(data[1 + 2 * n])
qs = [float(v) for v in data[2 + 2 * n:2 + 2 * n + m]]

mx = sum(xs) / n
us = [x - mx for x in xs]
a, b, lr = 0.0, 0.0, 0.05
for epoch in range(300):
    da = db = loss = 0.0
    for u, y in zip(us, ys):
        e = a * u + b - y
        loss += e * e
        da += 2 * e * u
        db += 2 * e
    a -= lr * da / n
    b -= lr * db / n
    if epoch % 10 == 0:
        print(f"#loss {epoch} {loss / n:.6f}", file=sys.stderr)
print("\n".join(f"{a * (q - mx) + b:.4f}" for q in qs))
