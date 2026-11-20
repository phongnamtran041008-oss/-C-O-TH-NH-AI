"""Reference solution - server side only, never sent to the game.
n! bằng đệ quy với điều kiện dừng 0! = 1."""
import sys


def giai_thua(n):
    if n == 0:
        return 1
    return n * giai_thua(n - 1)


print(giai_thua(int(sys.stdin.read())))
