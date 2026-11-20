"""Reference solution - server side only, never sent to the game.
k láng giềng gần nhất, k = 5, khoảng cách Euclid; hòa phiếu thì lấy nhãn của láng giềng gần nhất
trong các nhãn hòa."""
import sys

data = sys.stdin.read().split()
pos = 0
n, d = int(data[0]), int(data[1])
pos = 2
train = []
for _ in range(n):
    x = [float(v) for v in data[pos:pos + d]]
    train.append((x, data[pos + d]))
    pos += d + 1
m = int(data[pos])
pos += 1
K = 5
out = []
for _ in range(m):
    q = [float(v) for v in data[pos:pos + d]]
    pos += d
    near = sorted(train, key=lambda t: sum((a - b) ** 2 for a, b in zip(t[0], q)))[:K]
    votes = {}
    for _, label in near:
        votes[label] = votes.get(label, 0) + 1
    most = max(votes.values())
    out.append(next(label for _, label in near if votes[label] == most))
print("\n".join(out))
