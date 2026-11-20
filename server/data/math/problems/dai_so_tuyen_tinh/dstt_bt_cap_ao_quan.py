"""Reference solution - server side only, never sent to the game.
Đếm cặp (áo, quần) khác màu bằng hai vòng lặp."""
import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
ao = data[2:2 + n]
quan = data[2 + n:2 + n + m]
dem = 0
for a in ao:
    for q in quan:
        if a != q:
            dem += 1
print(dem)
