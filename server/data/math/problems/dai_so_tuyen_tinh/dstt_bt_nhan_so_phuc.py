"""Reference solution - server side only, never sent to the game.
(a + bi)(c + di) = (ac - bd) + (ad + bc)i."""
a, b, c, d = map(int, input().split())
print(a * c - b * d, a * d + b * c)
