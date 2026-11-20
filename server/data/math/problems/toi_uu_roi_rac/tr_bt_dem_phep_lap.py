"""Reference solution - server side only, never sent to the game.
A = n(n+1)/2; B = n * (floor(log2 n) + 1) = n * n.bit_length()."""
n = int(input())
A = n * (n + 1) // 2
B = n * n.bit_length()
print(A, B)
