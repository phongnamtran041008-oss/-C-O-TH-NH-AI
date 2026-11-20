"""Reference solution - server side only, never sent to the game.
Quay lui sinh hoán vị, thử số nhỏ trước nên ra đúng thứ tự từ điển."""
import sys


def sinh(vi_tri, n, dang, dung, ra):
    if vi_tri == n:
        ra.append(" ".join(map(str, dang)))
        return
    for x in range(1, n + 1):
        if not dung[x]:
            dung[x] = True
            dang.append(x)
            sinh(vi_tri + 1, n, dang, dung, ra)
            dang.pop()
            dung[x] = False


n = int(sys.stdin.read())
ra = []
sinh(0, n, [], [False] * (n + 1), ra)
print(len(ra))
print("\n".join(ra))
