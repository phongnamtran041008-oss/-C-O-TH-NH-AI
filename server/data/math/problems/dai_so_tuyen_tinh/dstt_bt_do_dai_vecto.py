"""Reference solution - server side only, never sent to the game.
||v|| = sqrt(v1^2 + ... + vn^2), in ra 6 chữ số sau dấu chấm."""
import math
import sys

data = sys.stdin.read().split()
n = int(data[0])
v = [float(x) for x in data[1:1 + n]]
print(f"{math.sqrt(sum(x * x for x in v)):.6f}")
