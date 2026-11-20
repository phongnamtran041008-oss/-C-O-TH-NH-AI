"""Reference solution - server side only, never sent to the game.
Bayes ngây thơ đa thức, làm trơn Laplace (cộng 1), cộng log để khỏi tràn số."""
import math
import sys

lines = sys.stdin.read().split("\n")
n = int(lines[0])
count = {0: {}, 1: {}}
words_in = {0: 0, 1: 0}
docs = {0: 0, 1: 0}
for line in lines[1:1 + n]:
    parts = line.split()
    y = int(parts[0])
    docs[y] += 1
    for w in parts[1:]:
        count[y][w] = count[y].get(w, 0) + 1
        words_in[y] += 1
vocab = set(count[0]) | set(count[1])
V = len(vocab)
m = int(lines[1 + n])
out = []
for line in lines[2 + n:2 + n + m]:
    best, best_y = None, 0
    for y in (0, 1):
        s = math.log(docs[y] / n)
        for w in line.split():
            s += math.log((count[y].get(w, 0) + 1) / (words_in[y] + V))
        if best is None or s > best:
            best, best_y = s, y
    out.append(str(best_y))
print("\n".join(out))
