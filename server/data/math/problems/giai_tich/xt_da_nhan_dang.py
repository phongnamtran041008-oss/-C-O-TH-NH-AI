"""Reference solution - server side only, never sent to the game.
Nhận dạng chữ số: k láng giềng gần nhất (k = 3) trên 64 điểm ảnh, khoảng cách bình phương;
hòa phiếu thì lấy nhãn của láng giềng gần nhất."""
import sys

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
pos = 2
train = []
for _ in range(n):
    train.append(([int(v) for v in data[pos:pos + d]], data[pos + d]))
    pos += d + 1
m = int(data[pos])
pos += 1
out = []
for _ in range(m):
    q = [int(v) for v in data[pos:pos + d]]
    pos += d
    near = sorted(((sum((a - b) * (a - b) for a, b in zip(x, q)), y) for x, y in train))[:3]
    votes = {}
    for _, y in near:
        votes[y] = votes.get(y, 0) + 1
    most = max(votes.values())
    out.append(next(y for _, y in near if votes[y] == most))
print("\n".join(out))
