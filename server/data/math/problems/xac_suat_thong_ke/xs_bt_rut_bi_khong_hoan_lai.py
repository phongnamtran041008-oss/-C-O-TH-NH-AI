"""Reference solution - server side only, never sent to the game.
Rút k bi không hoàn lại T lần bằng bộ sinh số tự viết; so với C(a,k)/C(a+b,k)."""
import sys
from math import comb

data = sys.stdin.read().split()
seed = int(data[0])
a, b, k, T = map(int, data[1:5])
s = seed


def rnd():
    global s
    s = (s * 1103515245 + 12345) % 2147483648
    return s >> 16


dung = 0
for _ in range(T):
    hop = ["do"] * a + ["xanh"] * b
    tat_ca_do = True
    for _ in range(k):
        vi_tri = rnd() % len(hop)
        if hop.pop(vi_tri) != "do":
            tat_ca_do = False
    if tat_ca_do:
        dung += 1
print(dung, f"{dung / T:.6f}", f"{comb(a, k) / comb(a + b, k):.6f}")
