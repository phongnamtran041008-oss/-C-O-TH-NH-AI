"""Naive program - must NOT pass: forgets the prior P(loại) and multiplies the word
likelihoods only."""
import math
import sys

lines = sys.stdin.read().split("\n")
n = int(lines[0])
words = {"1": 0, "0": 0}
count = {"1": {}, "0": {}}
for line in lines[1:1 + n]:
    parts = line.split()
    y = parts[0]
    words[y] += len(parts) - 1
    for w in parts[1:]:
        count[y][w] = count[y].get(w, 0) + 1
V = len(set(count["1"]) | set(count["0"]))
msg = lines[1 + n].split()
score = {}
for y in ("1", "0"):
    score[y] = sum(math.log((count[y].get(w, 0) + 1) / (words[y] + V)) for w in msg)
top = max(score.values())
p1 = math.exp(score["1"] - top) / (math.exp(score["1"] - top) + math.exp(score["0"] - top))
print(f"{p1:.6f}")
print(1 if p1 > 0.5 else 0)
