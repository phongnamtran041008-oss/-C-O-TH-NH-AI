"""Reference solution - server side only, never sent to the game.
Đếm x trong [a, b] với x >= 1 và x != 4."""
import sys

a, b = map(int, sys.stdin.read().split())
dem = 0
for x in range(a, b + 1):
    if x >= 1 and x != 4:
        dem += 1
print(dem)
