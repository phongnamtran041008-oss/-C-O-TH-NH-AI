"""Reference solution - server side only, never sent to the game.
Đếm cặp i<j có a_i + a_j = S bằng dict đếm tần số."""
import sys
from collections import Counter

data = sys.stdin.read().split()
n, s = int(data[0]), int(data[1])
thay = Counter()
ketqua = 0
for x in map(int, data[2:2 + n]):
    ketqua += thay[s - x]
    thay[x] += 1
print(ketqua)
