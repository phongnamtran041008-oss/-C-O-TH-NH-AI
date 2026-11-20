"""Naive program - must NOT pass: counts the messages that contain a word, not how many
times the word appears (a word said twice counts once)."""
import sys

lines = sys.stdin.read().split("\n")
n = int(lines[0])
docs = {"1": 0, "0": 0}
words = {"1": 0, "0": 0}
count = {"1": {}, "0": {}}
for line in lines[1:1 + n]:
    parts = line.split()
    y = parts[0]
    docs[y] += 1
    words[y] += len(parts) - 1
    for w in set(parts[1:]):
        count[y][w] = count[y].get(w, 0) + 1
q = int(lines[1 + n])
print(docs["1"], docs["0"], words["1"], words["0"])
for w in lines[2 + n:2 + n + q]:
    w = w.strip()
    print(count["1"].get(w, 0), count["0"].get(w, 0))
