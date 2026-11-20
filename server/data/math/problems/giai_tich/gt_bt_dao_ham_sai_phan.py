"""Reference solution - server side only, never sent to the game.
Sai phân tiến, sai phân trung tâm và đạo hàm đúng của x^3 - 2x."""
import sys


def f(x):
    return x ** 3 - 2 * x


x, h = map(float, sys.stdin.read().split())
tien = (f(x + h) - f(x)) / h
trung_tam = (f(x + h) - f(x - h)) / (2 * h)
dung = 3 * x * x - 2
print(f"{tien:.6f} {trung_tam:.6f} {dung:.6f}")
