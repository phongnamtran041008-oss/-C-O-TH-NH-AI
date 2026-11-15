"""Reference solution - server side only, never sent to the game.
Giao của hai tập hợp, in theo thứ tự tăng dần."""
import sys

data = list(map(int, sys.stdin.read().split()))
i = 0
n = data[i]
i += 1
a = set(data[i:i + n])
i += n
m = data[i]
i += 1
b = set(data[i:i + m])
chung = sorted(a & b)
print(len(chung))
print(" ".join(str(x) for x in chung))
