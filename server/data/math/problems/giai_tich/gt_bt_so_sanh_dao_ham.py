"""Reference solution - server side only, never sent to the game.
Đạo hàm đa thức bằng quy tắc lũy thừa so với sai phân trung tâm."""
import sys

data = sys.stdin.read().split()
n = int(data[0])
c = [int(v) for v in data[1:2 + n]]
x0 = float(data[2 + n])


def f(x):
    return sum(c[k] * x ** k for k in range(n + 1))


tay = sum(k * c[k] * x0 ** (k - 1) for k in range(1, n + 1))
h = 0.00001
so = (f(x0 + h) - f(x0 - h)) / (2 * h)
print(f"{tay:.6f} {so:.6f} {abs(tay - so):.6f}")
