"""Reference solution - server side only, never sent to the game.
Tháp Hà Nội: chuyển n-1 đĩa sang cọc phụ, đĩa to sang đích, rồi n-1 đĩa về đích."""
import sys


def chuyen(n, tu, qua, den, nuoc):
    if n == 0:
        return
    chuyen(n - 1, tu, den, qua, nuoc)
    nuoc.append(f"{tu} {den}")
    chuyen(n - 1, qua, tu, den, nuoc)


n = int(sys.stdin.read())
nuoc = []
chuyen(n, "A", "B", "C", nuoc)
print(len(nuoc))
print("\n".join(nuoc))
