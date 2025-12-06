from collections import defaultdict

n, m = map(int, input().split())
l = input().split()
adj = defaultdict(list)
for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)

t = 0


def amount(x):
    return 1 / (2 ** (x - 1))

# dags, optimizing