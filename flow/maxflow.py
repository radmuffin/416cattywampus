from kactl_pushrelabel import PushRelabel

n, m, s, t = map(int, input().split())
G = PushRelabel(n)
for _ in range(m):
    u, v, c = map(int, input().split())
    G.addEdge(u, v, c)

maxF = G.calc(s, t)
edges = G.retrieveFlow()

print(n, maxF, len(edges))
for e in edges:
    print(e[0], e[1], e[2])