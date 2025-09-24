from kactl_pushrelabel import PushRelabel

n, m, p = map(int, input().split())
numV = n + m + p + 2
# 0 src numV-1 dst (1 indexing)
# kids: 1--n, toys n+1--n+m, grps n+m+1--n+m+p
G = PushRelabel(numV)
for i in range(1, n+1):
    G.addEdge(0, i, 1)
    #edges src to kids
for i in range(n):
    goodToys = list(map(int, input().split()))
    goodToys.pop(0) #drop n toys, don't need
    for t in goodToys:
        G.addEdge(i + 1, t + n, 1)
        #edges kid to toy
noGroupToys = set([i for i in range(1,m+1)])
for i in range(p):
    grpLine = list(map(int, input().split()))
    nToys = grpLine[0]
    for toy in grpLine[1:nToys+1]:
        noGroupToys.remove(toy)
        G.addEdge(toy+n, i+1+n+m, 1)
        #edges toy to grp
    G.addEdge(n+m+i+1, numV - 1, grpLine[-1])
    #edge grp to dst
for toy in noGroupToys:
    G.addEdge(toy + n, numV -1, 1)
    # grpless toys to dest
G.plotGraph()
print(G.calc(0, numV - 1))






