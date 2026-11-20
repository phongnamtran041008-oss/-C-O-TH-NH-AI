"""Reference solution - server side only, never sent to the game.
Sắp theo thời điểm kết thúc, lấy việc bắt đầu >= kết thúc của việc đã chọn."""
import sys

data = list(map(int, sys.stdin.read().split()))
n = data[0]
viec = sorted((data[2 + 2 * i], data[1 + 2 * i]) for i in range(n))
chon = 0
cuoi = -1
for ket_thuc, bat_dau in viec:
    if bat_dau >= cuoi:
        chon += 1
        cuoi = ket_thuc
print(chon)
