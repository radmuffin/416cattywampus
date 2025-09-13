h, w, l, c = map(int,input().split())
b = h * w * l
if b > c:
    print('SO MUCH SPACE')
elif b == c:
    print('COZY')
else:
    print('TOO TIGHT')