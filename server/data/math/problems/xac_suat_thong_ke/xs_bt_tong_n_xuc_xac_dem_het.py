"""Reference solution - server side only, never sent to the game.
Duyệt hết 6^n kết quả, đếm tổng s, phân số tối giản."""
import sys
from fractions import Fraction
from itertools import product

n, s = map(int, sys.stdin.read().split())
thuan = sum(1 for kq in product(range(1, 7), repeat=n) if sum(kq) == s)
print(Fraction(thuan, 6 ** n))
