def method_name():
    global n, ps, i, x
    n = int(input())
    for _ in range(n):
        k = int(input())
        n = input()
        ps, p = False, False
        for i in range(k):
            x = input()
            if x == 'pea soup':
                ps = True
            elif x == 'pancakes':
                p = True
            if ps and p:
                print(n)
                return
    print('Anywhere is fine I guess')


method_name()