from collections import defaultdict

n = 6
edges = [(0,1), (1,2), (2,0), (1,3), (3,4), (4,5), (5,3)]


class N:
    def __init__(self, v):
        self.v = v
        self.dt = None
        self.low = None

    def __repr__(self):
        return f"{self.v} d:{self.dt} l:{self.low}"

ns = {}
adj = defaultdict(list)

for a,b in edges:
    adj[a].append(b)
for i in range(n):
    ns[i] = N(i)

root = 0
t = 0
def dfs(x, parent=-1):
    global t
    ns[x].dt = t
    ns[x].low = t  # Initialize low to discovery time
    t += 1
    for c in adj[x]:
        if ns[c].dt is None:  # Tree edge - unvisited child
            dfs(c, x)
            # Update low value from child
            ns[x].low = min(ns[x].low, ns[c].low)
        elif c != parent:  # Back edge - visited ancestor (but not parent)
            ns[x].low = min(ns[x].low, ns[c].dt)

dfs(root)

bridges = []
def findBridges(x, parent=-1):
    for c in adj[x]:
        if c != parent and ns[c].dt > ns[x].dt:  # This is a tree edge to a child
            if ns[c].low > ns[x].dt:  # Low of child is higher than discovery of parent = bridge
                bridges.append((x, c))
            findBridges(c, x)

findBridges(root)

print(bridges)