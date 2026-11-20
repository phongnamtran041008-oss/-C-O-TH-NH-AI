"""Reference solution - server side only, never sent to the game.
Tích Descartes của hai tập đã bỏ trùng, in theo thứ tự từ điển."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
A = sorted(set(map(int, data[1:1 + n])))
m = int(data[1 + n])
B = sorted(set(map(int, data[2 + n:2 + n + m])))
print(len(A) * len(B))
for a in A:
    for b in B:
        print(a, b)
