def polygon_area_direction(points):
    n = len(points)
    area = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += (x1 * y2 - x2 * y1)
    direction = "CCW" if area > 0 else "CW"
    area = abs(area) / 2
    return direction, area

while True:
    line = input()
    if not line.strip():
        continue
    n = int(line)
    if n == 0:
        break
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    direction, area = polygon_area_direction(points)
    print(f"{direction} {area:.1f}")
    