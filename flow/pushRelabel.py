from typing import DefaultDict, List, Set, Tuple
from collections import deque


class PushRelabelG:
    def __init__(self, n: int):
        self.n = n
        self.excess = [0] * n
        self.height = [0] * n
        self.seen = [0] * n
        self.graph = DefaultDict(list)
        self.edges = {}
        self.original_edges: Set[Tuple[int, int]] = set()
        self.active = deque()

    def add_edge(self, u: int, v: int, cap: int) -> None:
        if (u, v) not in self.edges:
            self.edges[(u, v)] = 0
            self.edges[(v, u)] = 0
            self.graph[u].append(v)
            self.graph[v].append(u)
        self.edges[(u, v)] += cap
        # Track the original directed edge regardless of whether it was seen before
        self.original_edges.add((u, v))

    def push(self, u: int, v: int) -> None:
        d = min(self.excess[u], self.edges[(u, v)])
        self.edges[(u, v)] -= d
        self.edges[(v, u)] += d
        self.excess[u] -= d
        self.excess[v] += d
        if d and self.excess[v] == d:
            self.active.append(v)

    def relabel(self, u: int) -> None:
        min_height = float('inf')
        for v in self.graph[u]:
            if self.edges[(u, v)] > 0:
                min_height = min(min_height, self.height[v])
        self.height[u] = min_height + 1

    def discharge(self, u: int) -> None:
        while self.excess[u] > 0:
            if self.seen[u] < len(self.graph[u]):
                v = self.graph[u][self.seen[u]]
                if self.edges[(u, v)] > 0 and self.height[u] > self.height[v]:
                    self.push(u, v)
                else:
                    self.seen[u] += 1
            else:
                self.relabel(u)
                self.seen[u] = 0

    def max_flow(self, source: int, sink: int) -> int:
        self.height = [0] * self.n
        self.height[source] = self.n
        self.excess = [0] * self.n
        self.excess[source] = float('inf')

        for v in self.graph[source]:
            self.push(source, v)

        while self.active:
            u = self.active.popleft()
            if u != source and u != sink:
                self.discharge(u)

        return self.excess[sink]

    def extract_flows(self) -> List[Tuple[int, int, int]]:
        """
        Return a list of (u, v, flow) for each original directed edge u->v
        that carries positive flow after max_flow has been computed.
        """
        flows: List[Tuple[int, int, int]] = []
        for u, v in self.original_edges:
            f = self.edges.get((v, u), 0)  # flow on u->v stored on reverse arc
            if f > 0:
                flows.append((u, v, f))
        return flows
