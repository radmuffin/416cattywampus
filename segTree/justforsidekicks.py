import math

class Node:
    def __init__(self, counts, start, end, l=None, r=None):
        self.counts = counts    # array of counts of each gem type
        self.start = start
        self.end = end
        self.l = l
        self.r = r

    def __repr__(self):
        return f"({self.start}-{self.end}): {self.counts}"

    def getVal(self, curRates):
        return sum(r * co for r, co in zip(curRates, self.counts))

def growTree(start, end):
    if end == start:
        counts = [0] * 6
        counts[gems[start - 1] - 1] = 1         # WHY NOT ZERO BASED
        return Node(counts, start, start)
    mid = math.floor((start + end) / 2)
    leftBranch, rightBranch = growTree(start, mid), growTree(mid+1, end)
    bigCount = [le + ri for le, ri in zip(leftBranch.counts, rightBranch.counts)]
    return Node(bigCount, start, end, leftBranch, rightBranch)

def swap(i, nValueI):
    affected = {root}
    x = root
    while x.start != x.end:
        mid = math.floor((x.start + x.end) / 2)
        if i <= mid:
            affected.add(x.l)
            x = x.l
        else:
            affected.add(x.r)
            x = x.r
    old = x.counts.index(1)
    for node in affected:
        node.counts[old] -= 1
        node.counts[nValueI - 1] += 1      # gonna be 1-6 need 0-5 grrrr

def query(start, end):
    search = [root]
    res = 0
    while search:
        for x in search:
            search.remove(x)
            if x.start >= start and x.end <= end:
                res += x.getVal(rates)
            elif x.start > end or x.end < start:
                pass
            else: #x.start >= start or x.end <= end:
                search.append(x.l)
                search.append(x.r)
    return res



# keep in mind, prob uses dumb 1 based counting. plan to convert on input (rate changes, and gem swaps)
# not converting for query ranges tho....... yeah the inconsistency hurts too
n,q = map(int, input().split())
rates = list(map(int, input().split()))
gemString = input()
gems = [int(d) for d in gemString]
root = growTree(1, n)

for _ in range(q):
    a,b,c = map(int, input().split())
    match a:
        case 1:
            swap(b, c)
        case 2:
            rates[b - 1] = c
        case 3:
            print(query(b, c))

