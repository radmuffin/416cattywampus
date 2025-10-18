def build_sa(s):
    #suffix arrayyyy
    n = len(s)
    sa = list(range(n))
    ranks = [ord(c) for c in s]
    tmp = [0]*n
    k = 1
    while k < n:
        sa.sort(key=lambda i: (ranks[i], ranks[i+k] if i+k < n else -1))
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev, cur = sa[i-1], sa[i]
            left = (ranks[prev], ranks[prev+k] if prev+k < n else -1)
            right = (ranks[cur], ranks[cur+k] if cur+k < n else -1)
            tmp[cur] = tmp[prev] + (1 if left != right else 0)
        ranks, tmp = tmp, ranks
        if ranks[sa[-1]] == n-1:
            break
        k <<= 1
    return sa

def build_lcp(s, sa):
    n = len(s)
    rank = [0]*n
    for i, si in enumerate(sa):
        rank[si] = i
    lcp = [0]*n
    h = 0
    for i in range(n):
        r = rank[i]
        if r == 0:
            continue
        j = sa[r-1]
        while i+h < n and j+h < n and s[i+h] == s[j+h]:
            h += 1
        lcp[r] = h
        if h:
            h -= 1
    return lcp

def main():
    s = input()
    sa = build_sa(s)
    lcp = build_lcp(s, sa)
    max_l = max(lcp)
    # collect candidates (substrings of length max_l) from adjacent pairs with lcp == max_l
    candidates = [s[sa[i]:sa[i]+max_l] for i in range(1, len(s)) if lcp[i] == max_l]
    print(min(candidates))

if __name__ == "__main__":
    main()