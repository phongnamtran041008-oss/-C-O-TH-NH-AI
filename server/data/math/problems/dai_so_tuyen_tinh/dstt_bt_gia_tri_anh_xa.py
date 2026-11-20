"""Reference solution - server side only, never sent to the game.
f(x) = 2x^2 - 3x + 1 tại từng điểm."""
import sys


def f(x):
    return 2 * x * x - 3 * x + 1


data = sys.stdin.read().split()
n = int(data[0])
print(" ".join(str(f(int(x))) for x in data[1:1 + n]))
