"""Reference solution - server side only, never sent to the game.
Vẽ lại ảnh thứ i (8 x 8, giá trị 0..16): '#' nếu điểm ảnh >= 8, '.' nếu không; in nhãn của nó,
rồi số ảnh của từng chữ số 0..9 trong cả bộ."""
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
for r in range(side):
    print("".join("#" if v >= 8 else "." for v in images[i][r * side:(r + 1) * side]))
print(labels[i])
print(" ".join(str(labels.count(c)) for c in range(10)))
