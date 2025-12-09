import random

MX=2 ** 63
DRAW = True
if DRAW:
    from matplotlib import pyplot as plt
from matplotlib.patches import Circle

MX = 2 ** 10


class Treap:
    def __init__(S, v=0):
        S.value = v
        S.priority = random.randint(1, MX)
        S.left = None
        S.right = None
        S.count = 1
        S.sum = 0

    # split returns two treaps a left and a right
    def split(S, numleft):
        # TODO FILL THIS IN, splitting S into two treaps L and R

        return L, R

    # returns the root after joining two treaps together
    def mergeright(S, T):
        # TODO FILL THIS IN, producing T2 = S+T
        return T2

    # TODO TEST!  This is untested
    def insert(S, v, numleft):
        V = Treap(v)
        L, R = S.split(numleft)
        L.mergeright(V)
        L.mergeright(R)

    def __repr__(S):
        s = '[ '
        s += S.left.__repr__() if S.left else '-'
        s += f' <{S.value},{S.priority}> '
        s += S.right.__repr__() if S.right else '-'
        s += ' ]'
        return s

    def readout(S, A=None):
        if A == None: A = []
        if S.left:
            S.left.readout(A)
        A.append(S.value)
        if S.right:
            S.right.readout(A)
        return A

    def priorities(S, P):
        top = len(P) == 0
        if S.left:
            S.left.priorities(P)
        P.add(S.priority)
        if S.right:
            S.right.priorities(P)

        if top:
            o = sorted(P)
            M = {x: len(o) - i - 1 for i, x in enumerate(o)}
            return M

    def depths(S, D=None, depth=1):
        top = False
        if D == None:
            D = {}
            top = True
        if not depth in D: D[depth] = 0
        D[depth] += 1
        if S.left: S.left.depths(D, depth + 1)
        if S.right: S.right.depths(D, depth + 1)
        if top:
            return D

    def draw(S, subplot=0, wait=False):
        if subplot == 0:
            ax = plt.axes()
        else:
            ax = plt.subplot(1, 3, subplot)
        ax.set_aspect('equal')
        P = S.priorities(set())
        S._drawhelp(0, P, ax)
        T = S.count
        ax.set_xlim(-.5, T - .5)
        ax.set_ylim(-.5, T - .5)
        ax.axis('off')
        if not wait:
            plt.show()

    def _drawhelp(S, cnt_left, P, ax):
        x = cnt_left
        lcen = None
        rcen = None
        if S.left:
            lcen = S.left._drawhelp(x, P, ax)
            x += S.left.count
        pri = P[S.priority]
        cen = (x, pri)
        x += 1
        if S.right:
            rcen = S.right._drawhelp(x, P, ax)
        if lcen: plt.plot([lcen[0], cen[0]], [lcen[1], cen[1]], 'k', zorder=1)
        if rcen: plt.plot([rcen[0], cen[0]], [rcen[1], cen[1]], 'k', zorder=1)

        C = Circle(cen, .5, zorder=2)
        ax.add_patch(C)
        plt.text(cen[0], cen[1], str(S.value), ha='center', va='center', color='k', zorder=3)
        plt.text(cen[0], cen[1] - 1.0, str(S.priority), ha='center', va='center', color='g', zorder=3)
        plt.text(cen[0], cen[1] - 2.0, str(S.count), ha='center', va='center', color='r', zorder=3)

        return cen


def randarray(N):
    A = list(range(1, N + 1))
    random.shuffle(A)
    return A


def array2treap(A):
    T = None if len(A) == 0 else Treap(A[0])
    for i in range(1, len(A)):
        t = Treap(A[i])
        T = T.mergeright(t)
    return T


def test_depth(N, NTRIALS):
    depths = []
    SEQ = randarray(N)
    if DRAW:
        print(SEQ)
    STATS = []

    for _ in range(NTRIALS):
        T = array2treap(SEQ)

        D = T.depths()
        STATS.append(max(D.keys()))
    # print(STATS)
    import math
    L = math.log(N, 2)
    print(f'log({N}) = L = {L}')
    from collections import Counter
    S = Counter(STATS)
    for c in sorted(S):
        f = c / L
        pct = S[c] / NTRIALS
        print(f'{c}={f} * L : {100 * pct:.02f}%')

    return SEQ, T


def test_rigorous(SEQ, NUPDATES):
    N = len(SEQ)
    A = [x for x in SEQ]
    T = array2treap(A)
    print(A)

    for i in range(NUPDATES):
        a, b = sorted([random.randint(0, N - 1) for _ in range(2)])

        # print(f'{a=},{b=}')
        if b == N - 1:
            continue  # no change (nothing from end that needs to go before removed section

        l = A[:a]
        m = A[a:(b + 1)]
        r = A[(b + 1):]
        A = l + r + m

        if a == 0:
            # nothing  before removed section
            L, R = T.split(b + 1)
            T = R.mergeright(L)
        else:
            # 3 sections
            M, R = T.split(b + 1)
            L, M = M.split(a)
            T = L.mergeright(R)
            T = T.mergeright(M)
        # print(f'  {T.readout()}')
        # print(' ',A)
    print(f'After {NUPDATES} cut/paste operations:')
    print(A)
    print(T.readout())

    if DRAW:
        T.draw()


if __name__ == '__main__':

    N = 32 if DRAW else 1000
    NTRIALS = 1000

    if True:
        # This does a bunch of trials of creating a random array, turning it into a treap representation and splitting that in half
        # It will draw the final trial if DRAW is enabled
        A, T = test_depth(N, NTRIALS)

        if DRAW and N <= 100:
            T.draw(1, wait=True)
            L, R = T.split(N // 2)
            L.draw(2, wait=True)
            R.draw(3)

    if True:
        # This takes a starting array and repeatedly cuts out the middle and adds it onto the right end.  It is done both on the array and the treap to test that they end up the same
        # It will draw if DRAW is enabled
        A = randarray(N)
        NUPDATES = 10000
        test_rigorous(A, NUPDATES)

