"""Reference solution - server side only, never sent to the game.
Độ chính xác, khoảng tin cậy 95% của nó (p +- 1.96 sqrt(p(1-p)/n), cắt về [0, 1]), và lỗi hay
gặp nhất: cặp (nhãn thật, nhãn đoán) sai nhiều lần nhất, hòa thì nhãn thật nhỏ hơn rồi nhãn đoán
nhỏ hơn đi trước; không có lỗi nào thì in "-1 -1 0"."""
import math
import sys

data = sys.stdin.read().split()
n = int(data[0])
truth = [int(v) for v in data[1:1 + n]]
guess = [int(v) for v in data[1 + n:1 + 2 * n]]
right = sum(a == b for a, b in zip(truth, guess))
p = right / n
h = 1.96 * math.sqrt(p * (1 - p) / n)
print(f"{p:.6f} {max(0.0, p - h):.6f} {min(1.0, p + h):.6f}")
pairs = {}
for a, b in zip(truth, guess):
    if a != b:
        pairs[(a, b)] = pairs.get((a, b), 0) + 1
if pairs:
    (a, b), c = min(pairs.items(), key=lambda kv: (-kv[1], kv[0]))
    print(a, b, c)
else:
    print(-1, -1, 0)
