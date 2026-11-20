"""Reference solution - server side only, never sent to the game.
C = A*B bằng ba vòng lặp."""
import sys

data = list(map(int, sys.stdin.read().split()))
p, q, r = data[0], data[1], data[2]
vi = 3
A = []
for _ in range(p):
    A.append(data[vi:vi + q])
    vi += q
B = []
for _ in range(q):
    B.append(data[vi:vi + r])
    vi += r
for i in range(p):
    hang = []
    for j in range(r):
        tong = 0
        for k in range(q):
            tong += A[i][k] * B[k][j]
        hang.append(tong)
    print(*hang)
