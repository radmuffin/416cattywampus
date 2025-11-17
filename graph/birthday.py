from collections import defaultdict

class N:
    def __init__(self, v):
        self.v = v
        self.dt = None
        self.low = None

    def __repr__(self):
        return "{} d:{} l:{}".format(self.v, self.dt, self.low)


class BS:
    def __init__(self, graph, n=None):
        self.adj = graph
        if n is None:
            nodes = set(self.adj.keys())
            for neighs in self.adj.values():
                nodes.update(neighs)
            self.n = max(nodes) + 1 if nodes else 0
        else:
            self.n = n

        self.ns = {i: N(i) for i in range(self.n)}
        self.bridges = []
        self._run_tarjan()

    def _run_tarjan(self):
        t = 0

        def dfs(x, parent=-1):
            nonlocal t
            node = self.ns[x]
            node.dt = t
            node.low = t
            t += 1

            for c in self.adj.get(x, []):
                if self.ns[c].dt is None:
                    dfs(c, x)
                    node.low = min(node.low, self.ns[c].low)
                    if self.ns[c].low > node.dt:
                        self.bridges.append((x, c))
                elif c != parent:
                    node.low = min(node.low, self.ns[c].dt)
        for i in range(self.n):
            if self.ns[i].dt is None:
                dfs(i, -1)

    def bs(self):
        return list(self.bridges)


if __name__ == '__main__':
    p, c = map(int, input().split())
    while p != 0 or c != 0:
        adj = defaultdict(list)

        for _ in range(c):
            a,b = map(int, input().split())
            adj[a].append(b)
            adj[b].append(a)

        bs = BS(adj, p)
        print('Yes' if bs.bs() else 'No')

        p, c = map(int, input().split())
