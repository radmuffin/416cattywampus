r,f = map(int, input().split())
rot =  f / r
m = rot % 2
print('up' if m < .5 else 'down')
#180 == down 360 == up (starts top)