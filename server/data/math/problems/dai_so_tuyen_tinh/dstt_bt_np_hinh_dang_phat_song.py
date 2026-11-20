"""Reference solution - server side only, never sent to the game.
Hình dạng kết quả khi cộng hai mảng theo luật phát sóng (broadcasting)."""
import sys

dong = sys.stdin.read().split("\n")
a = list(map(int, dong[0].split()))
b = list(map(int, dong[1].split()))
n = max(len(a), len(b))
a = [1] * (n - len(a)) + a
b = [1] * (n - len(b)) + b
kq = []
for x, y in zip(a, b):
    if x == y or x == 1 or y == 1:
        kq.append(max(x, y))
    else:
        kq = None
        break
print("KHONG" if kq is None else " ".join(map(str, kq)))
