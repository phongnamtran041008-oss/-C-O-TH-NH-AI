"""Reference solution - server side only, never sent to the game.
Lũy thừa nhanh ma trận theo modulo M."""
import sys

data = list(map(int, sys.stdin.read().split()))
n, k, M = data[0], data[1], data[2]
A = [data[3 + i * n:3 + (i + 1) * n] for i in range(n)]


def nhan(X, Y):
    return [[sum(X[i][t] * Y[t][j] for t in range(n)) % M for j in range(n)] for i in range(n)]


ket_qua = [[1 % M if i == j else 0 for j in range(n)] for i in range(n)]
co_so = [[x % M for x in hang] for hang in A]
while k:
    if k & 1:
        ket_qua = nhan(ket_qua, co_so)
    co_so = nhan(co_so, co_so)
    k >>= 1
for hang in ket_qua:
    print(*hang)
