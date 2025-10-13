import math

n = int(input())
for _ in range(n):
    i = int(input())
    print(math.comb(2*i, i) // (i + 1))