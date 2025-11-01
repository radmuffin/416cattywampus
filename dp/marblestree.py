from collections import defaultdict

class MarbBalancer:
    def __init__(self, n: int):
        self.n = n
        self.adj = defaultdict(list)
        self.nodes = {}
        self.moves = 0

    def dfs(self, u: int) -> int:
        # net marbles to push to parent (\>0 means excess going up, \<0 means need coming down)
        balance = self.nodes[u] - 1
        for v in self.adj.get(u, ()):
            balance += self.dfs(v)
        self.moves += abs(balance)
        return balance

    def run(self) -> None:
        all_nodes = set()
        children = set()

        for _ in range(self.n):
            line = list(map(int, input().split()))
            v, m, d = line[:3]
            self.nodes[v] = m
            all_nodes.add(v)
            for c in line[3:]:
                self.adj[v].append(c)
                children.add(c)

        # find root (node that is never a child)
        roots = list(all_nodes - children)
        root = roots[0] if roots else 1

        self.dfs(root)
        print(self.moves)

n = int(input())
while n != 0:
    MarbBalancer(n).run()
    n = int(input())