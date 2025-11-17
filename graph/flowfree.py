import functools
from copy import deepcopy


def getWCoord(state, r, c):
    index = (r * 4) + c
    return state[index]

class Cell:
    def __init__(self, color = 'W'):
        self.conns = None
        self.max = 1 if color != 'W' else 2
        self.color = None if color == 'W' else color

    def complete(self):
        return self.conns is not None and len(self.conns) == self.max

    def validMove(self, i, j, state) -> bool:
        c = getWCoord(state, i, j)
        if c.complete(): # c is full
            return False
        if c.color and self.color != c.color: # can't combine paths of dif colors
            return False
        return self.conns is None or (i,j) not in self.conns # check we haven't already gone there

    def move(self, r, c, state):
        cs = [] if self.conns is None else list(self.conns)
        cs.append((r,c))
        if not self.color: # update blank cells
            self.color = getWCoord(state,r,c).color
        self.conns = tuple(cs)

    def __hash__(self):
        return hash((self.color, self.conns))

    def __eq__(self, other):
        if other is None:
            return False
        return self.color == other.color and self.conns == other.conns

    def __repr__(self):
        return f"{self.color}: {self.conns}" if self.color else 'Empty'

def solvable(state) -> bool:
    return all(x.complete() for x in state)

def getNeighs(r,c):
    ops = [(r-1,c),(r,c-1),(r+1,c),(r,c+1)] # just return the inbounds neighbors
    return [x for x in ops if 0 <= x[0] < 4 and 0 <= x[1] < 4]

seen = set()

def pruneWorthy(state) -> bool:
    for i in range(4):
        for j in range(4):
            look = getWCoord(state, i, j)
            if not look.complete(): # only care about disconnected cells
                if look.color is not None:
                    if all(noPathColor(look, getWCoord(state, rr, rc)) for rr, rc in getNeighs(i,j)):
                        # this colored cell has no valid paths to add
                        return True
                else:
                    if all(getWCoord(state,rr,rc).complete() for rr,rc in getNeighs(i,j)):
                        # this blank cell is has no possible paths to add
                        return True
    return False

# time to bfs
# @functools.cache
def bfs(state) -> bool:
    if solvable(state):
        return True
    ops = [] # states for different valid moves
    # check each cell and make all valid connections
    # expand one from each color path, skip the blank cells for now
    for i in range(4):
        for j in range(4):
            # do I need to deep copy? tuple immutability
            look = getWCoord(state, i, j)
            if look.complete() or look.color is None:
                continue
            # incomplete colored cell, exploring expansion
            for nc, nr in getNeighs(i,j):
                optCopy = deepcopy(state)
                look = getWCoord(optCopy, i, j)
                neigh = getWCoord(optCopy, nc, nr)
                if look.validMove(nc,nr,optCopy):
                    look.move(nc, nr, optCopy)
                    neigh.move(i,j,optCopy) # add connection both ways
                    if optCopy not in seen: #don't recheck possibilities
                        ops.append(optCopy)
                        seen.add(optCopy)

    return any(bfs(x) for x in ops)


start = []

for _ in range(4):
    line = input()
    for j in line:
        start.append(Cell(j))

start = tuple(start)
print(f"{'not ' if not bfs(start) else ''}solvable")