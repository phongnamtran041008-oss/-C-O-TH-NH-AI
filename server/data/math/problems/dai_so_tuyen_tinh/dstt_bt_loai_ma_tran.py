"""Reference solution - server side only, never sent to the game.
Nhận diện ma trận chéo, tam giác, đối xứng, đơn vị."""
import sys

data = list(map(int, sys.stdin.read().split()))
n = data[0]
A = [data[1 + i * n:1 + (i + 1) * n] for i in range(n)]
R = range(n)
duong_cheo = all(A[i][j] == 0 for i in R for j in R if i != j)
tren = all(A[i][j] == 0 for i in R for j in R if i > j)
duoi = all(A[i][j] == 0 for i in R for j in R if i < j)
doi_xung = all(A[i][j] == A[j][i] for i in R for j in R)
don_vi = all(A[i][j] == (1 if i == j else 0) for i in R for j in R)
tim = [ten for ten, co in (('duong_cheo', duong_cheo), ('tam_giac_tren', tren), ('tam_giac_duoi', duoi),
                           ('doi_xung', doi_xung), ('don_vi', don_vi)) if co]
print(*(tim or ['khong']))
