def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ext_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

t = int(input())
for _ in range(t):
    a, n, b, m = map(int, input().split())
    g, s, _ = ext_gcd(n, m)
    diff = b - a
    if diff % g != 0:
        print("No solution")
        continue
    mod = m // g
    k = (diff // g * s) % mod
    lcm = n // g * m
    x = (a + k * n) % lcm
    print(x, n * m)