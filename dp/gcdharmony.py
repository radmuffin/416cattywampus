import functools
from collections import defaultdict
import math
import sys

sys.setrecursionlimit(2000)

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

n = int(input())
ns = {}
aj = defaultdict(list)
# Tree representation for DP
children = defaultdict(list)
parent = {}

for i in range(n):
    v = int(input())
    ns[i + 1] = v

edges = []
for _ in range(n - 1):
    a, b = map(int, input().split())
    aj[a].append(b)
    aj[b].append(a)
    edges.append((a, b))

if n == 1:
    print(0)
    sys.exit()

# Build tree from root
root = 1
q = [root]
visited = {root}
parent[root] = -1
head = 0
while head < len(q):
    u = q[head]
    head += 1
    for v_ in aj[u]:
        if v_ not in visited:
            visited.add(v_)
            parent[v_] = u
            children[u].append(v_)
            q.append(v_)

@functools.lru_cache(maxsize=None)
def dp(u, p_val):
    cost = 0
    if ns[u] % p_val != 0:
        cost = p_val

    for v in children[u]:
        min_child_cost = float('inf')
        for p_child_val in primes:
            if math.gcd(p_val, p_child_val) > 1:
                min_child_cost = min(min_child_cost, dp(v, p_child_val))
        cost += min_child_cost
    return cost

min_total_cost = float('inf')
for p in primes:
    min_total_cost = min(min_total_cost, dp(root, p))

print(min_total_cost)
