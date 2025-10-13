import math
MOD = (10 ** 9) + 7
# i = int(input())
# print((math.comb(2*i, i) // (i + 1)) % MOD)


def modinv(a):
    return pow(a, MOD - 2, MOD)

i = int(input())
max_n = 2 * i

# Precompute factorials and inverse factorials
fact = [1] * (max_n + 1)
inv_fact = [1] * (max_n + 1)
for n in range(1, max_n + 1):
    fact[n] = fact[n - 1] * n % MOD
inv_fact[max_n] = modinv(fact[max_n])
for n in range(max_n - 1, -1, -1):
    inv_fact[n] = inv_fact[n + 1] * (n + 1) % MOD

# Catalan number: (2i)! / (i! * (i+1)!)
result = fact[2 * i] * inv_fact[i] % MOD * inv_fact[i + 1] % MOD
print(result)