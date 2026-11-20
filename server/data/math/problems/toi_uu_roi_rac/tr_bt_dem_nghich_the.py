"""Reference solution - server side only, never sent to the game.
Sắp xếp trộn, mỗi lần lấy phần tử bên phải thì cộng số phần tử còn lại bên trái."""
import sys


def tron(a):
    if len(a) <= 1:
        return a, 0
    giua = len(a) // 2
    trai, dem_trai = tron(a[:giua])
    phai, dem_phai = tron(a[giua:])
    dem = dem_trai + dem_phai
    ra = []
    i = j = 0
    while i < len(trai) and j < len(phai):
        if trai[i] <= phai[j]:
            ra.append(trai[i])
            i += 1
        else:
            ra.append(phai[j])
            j += 1
            dem += len(trai) - i
    ra.extend(trai[i:])
    ra.extend(phai[j:])
    return ra, dem


data = sys.stdin.read().split()
n = int(data[0])
print(tron(list(map(int, data[1:1 + n])))[1])
