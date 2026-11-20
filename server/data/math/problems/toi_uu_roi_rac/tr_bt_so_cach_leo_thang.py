"""Reference solution - server side only, never sent to the game.
f(n) = f(n-1) + f(n-2), có ghi nhớ."""
import sys
from functools import lru_cache


@lru_cache(maxsize=None)
def f(n):
    if n <= 1:
        return 1
    return f(n - 1) + f(n - 2)


print(f(int(sys.stdin.read())))
