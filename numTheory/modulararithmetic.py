while True:
    n, t = map(int, input().split())
    if n == t == 0:
        break
    for _ in range(t):
        line = input().split()
        x, op, y = int(line[0]), line[1], int(line[2])
        match op:
            case '+':
                print((x + y) % n)
            case '-':
                print((x - y) % n)
            case '*':
                print((x * y) % n)
            case '/':
                try:
                    inv = pow(y, -1, n)
                    print((x * inv) % n)
                except ValueError:
                    print(-1)
