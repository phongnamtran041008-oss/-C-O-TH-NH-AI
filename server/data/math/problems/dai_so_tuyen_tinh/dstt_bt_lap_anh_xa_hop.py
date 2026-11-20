"""Reference solution - server side only, never sent to the game.
Đếm bước và giá trị lớn nhất khi lặp f(n) tới 1."""
n = int(input())
buoc = 0
lon = n
while n != 1:
    n = n // 2 if n % 2 == 0 else 3 * n + 1
    buoc += 1
    lon = max(lon, n)
print(buoc, lon)
