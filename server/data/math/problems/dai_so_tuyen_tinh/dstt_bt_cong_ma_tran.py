"""Reference solution - server side only, never sent to the game.
C = A + k*B từng phần tử."""
import sys

data = list(map(int, sys.stdin.read().split()))
n, m, k = data[0], data[1], data[2]
vi = 3
A = []
for _ in range(n):
    A.append(data[vi:vi + m])
    vi += m
B = []
for _ in range(n):
    B.append(data[vi:vi + m])
    vi += m
for i in range(n):
    print(*(A[i][j] + k * B[i][j] for j in range(m)))
