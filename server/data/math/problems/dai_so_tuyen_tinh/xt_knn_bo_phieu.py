"""Reference solution - server side only, never sent to the game.
Lấy k điểm gần nhất (bằng khoảng cách thì điểm đứng trước trong dữ liệu đi trước), bỏ phiếu;
hòa phiếu thì thắng là nhãn có láng giềng xuất hiện sớm nhất trong danh sách k điểm."""
import sys

data = sys.stdin.read().split()
n, k = int(data[0]), int(data[1])
pts = []
for i in range(n):
    x, y, lab = int(data[2 + 3 * i]), int(data[3 + 3 * i]), data[4 + 3 * i]
    pts.append((x, y, lab, i))
qx, qy = int(data[2 + 3 * n]), int(data[3 + 3 * n])
near = sorted(pts, key=lambda p: ((p[0] - qx) ** 2 + (p[1] - qy) ** 2, p[3]))[:k]
labels = [p[2] for p in near]
votes = {}
for lab in labels:
    votes[lab] = votes.get(lab, 0) + 1
most = max(votes.values())
print(" ".join(labels))
print(next(lab for lab in labels if votes[lab] == most))
