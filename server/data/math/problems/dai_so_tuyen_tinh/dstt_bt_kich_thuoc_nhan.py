"""Reference solution - server side only, never sent to the game.
Nhân dãy ma trận từ trái sang phải, cộng số phép nhân số a*b*d."""
import sys

data = list(map(int, sys.stdin.read().split()))
k = data[0]
co = [(data[1 + 2 * i], data[2 + 2 * i]) for i in range(k)]
hang, cot = co[0]
phep = 0
for a, b in co[1:]:
    if cot != a:
        print("khong nhan duoc")
        break
    phep += hang * cot * b
    cot = b
else:
    print(hang, cot, phep)
