"""Reference solution - server side only, never sent to the game.
Tập hợp không có phần tử lặp: đếm số phần tử khác nhau."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
print(len({int(x) for x in data[1:1 + n]}))
