"""Reference solution - server side only, never sent to the game.
Tạo ảnh của y bằng dict giá trị -> các chỉ số."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
anh = {}
for i in range(1, n + 1):
    anh.setdefault(int(data[i]), []).append(i)
q = int(data[n + 1])
for y in data[n + 2:n + 2 + q]:
    cac = anh.get(int(y), [])
    print(len(cac), *cac)
