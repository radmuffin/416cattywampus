from kactl_pushrelabel import PushRelabel

n, m, s, t = map(int, input().split())
G = PushRelabel(n)
for _ in range(m):
    u, v, w = map(int, input().split())
    G.addEdge(u, v, w)
G.calc(s, t)
cut = G.retrieveCut()
verts = [x for x in range(n) if G.leftOfMinCut(x)]
print(len(verts))
for ve in verts:
    print(ve)


#not passing yet, dky
