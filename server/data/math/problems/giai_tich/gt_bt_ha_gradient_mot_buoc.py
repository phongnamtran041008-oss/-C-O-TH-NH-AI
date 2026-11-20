"""Reference solution - server side only, never sent to the game.
T bước hạ gradient x -= lr * f'(x) trên a(x-c)^2 + d."""
import sys

a, c, d, x0, lr, T = sys.stdin.read().split()
a, c, d, x, T = int(a), int(c), int(d), int(x0), int(T)
lr = float(lr)
for _ in range(T):
    dao_ham = 2 * a * (x - c)
    x = x - lr * dao_ham
print(f"{x:.6f} {a * (x - c) ** 2 + d:.6f}")
