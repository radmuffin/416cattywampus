BASE = 9973
MOD = (2**64) - 1
MOD64 = 1 << 64

word = input()
n = len(word)
pres = [0] * (n + 1)
pBase = [1] * (n + 1)
for i in range(n):
    pres[i+1] = (pres[i] * BASE + ord(word[i])) % MOD
    pBase[i+1] = (pBase[i] * BASE) % MOD

def query(l, r):
    return ((pres[r] - pres[l] * pBase[r-l] + MOD) % MOD) % MOD64

qs = int(input())
for _ in range(qs):
    l, r = map(int, input().split())
    print(query(l, r))
