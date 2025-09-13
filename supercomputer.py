import math

class Node:
    def __init__(self, val, start, end, l=None, r=None):
        self.val = val
        self.start = start
        self.end = end
        self.l = l
        self.r = r

    def __repr__(self):
        return f"[{self.start}-{self.end}]:{self.val}"

def growTree(start, end):
    if end == start:
        return Node(0, start, start)
    mid = math.floor((start + end) / 2)
    return Node(0, start, end, growTree(start, mid), growTree(mid+1, end))

def flip(i):
    affected = {root}
    x = root
    while x.end != i or x.start != i:
        mid = mid = math.floor((x.start + x.end) / 2)
        if i <= mid:
            affected.add(x.l)
            x = x.l
        else:
            affected.add(x.r)
            x = x.r
    newVal = 1 if x.val == 0 else -1
    for node in affected:
        node.val += newVal

def query(l,r):
    searching = [root]
    res = 0
    while searching:
        for node in searching:
            if node.start >= l and node.end <= r:
                res += node.val
                searching.remove(node)
            elif node.start > r or node.end < l:
                searching.remove(node)
            elif node.start < l or node.end > r:
                searching.append(node.l)
                searching.append(node.r)
                searching.remove(node)
    return res




n,k = map(int,input().split())
layers = math.ceil(math.log2(n))
dummyN = 2 ** layers    # rounding to closest upper power of 2 for nice tree

root = growTree(1, dummyN)

for _ in range(k):
    line = input().split()
    flipOr = line[0]
    ints = list(map(int, line[1:]))

    if flipOr == 'F':
        flip(ints[0])
    else:
        print(query(ints[0], ints[1]))
